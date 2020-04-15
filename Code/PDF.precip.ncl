;Function: PDF analysis

load "/home/qin5/Programming/NCL/my_funcs_and_procs/Calendar.ncl"

begin

dir_WRF = "/home/qin5/Data/WRF.postprocessing.extract.hourly.nc"
f_WRF = addfile(dir_WRF,"r")

dir_ARMBE2D_05 = "/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110501.000000.nc"
dir_ARMBE2D_06 = "/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110601.000000.nc"
dir_ARMBE2D_07 = "/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110701.000000.nc"
dir_ARMBE2D_08 = "/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110801.000000.nc"
f_ARM_05 = addfile(dir_ARMBE2D_05,"r")
f_ARM_06 = addfile(dir_ARMBE2D_06,"r")
f_ARM_07 = addfile(dir_ARMBE2D_07,"r")
f_ARM_08 = addfile(dir_ARMBE2D_08,"r")

lat_1 = 35.0
lat_2 = 38.0
lon_1 = -99.0
lon_2 = -96.0

;;========= WRF areal average 
RAIN_tot_regrid = f_WRF->RAIN_tot_regrid
;printVarSummary(RAIN_tot_regrid)

RAIN_WRF_SGP = dim_avg_n_Wrap(dim_avg_n_Wrap(RAIN_tot_regrid(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)
RAIN_WRF_SGP = RAIN_WRF_SGP * 24.0
RAIN_WRF_SGP@units = "mm/day"
printVarSummary(RAIN_WRF_SGP)

RAIN_WRF_SGP_May = RAIN_WRF_SGP(0:737)
RAIN_WRF_SGP_Jun = RAIN_WRF_SGP(738:1457)
RAIN_WRF_SGP_Jul = RAIN_WRF_SGP(1458:2201)
RAIN_WRF_SGP_Aug = RAIN_WRF_SGP(2202:)

;;----------ARMBE2DGRID areal average----------------
precip05 = f_ARM_05->precip_rate
precip06 = f_ARM_06->precip_rate
precip07 = f_ARM_07->precip_rate
precip08 = f_ARM_08->precip_rate

precip_ARM_SGP_May = dim_avg_n_Wrap(dim_avg_n_Wrap(precip05(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)
precip_ARM_SGP_May = precip_ARM_SGP_May * 24.0
precip_ARM_SGP_May@units = "mm/day"

precip_ARM_SGP_Jun = dim_avg_n_Wrap(dim_avg_n_Wrap(precip06(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)
precip_ARM_SGP_Jun = precip_ARM_SGP_Jun * 24.0
precip_ARM_SGP_Jun@units = "mm/day"

precip_ARM_SGP_Jul = dim_avg_n_Wrap(dim_avg_n_Wrap(precip07(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)
precip_ARM_SGP_Jul = precip_ARM_SGP_Jul * 24.0
precip_ARM_SGP_Jul@units = "mm/day"

precip_ARM_SGP_Aug = dim_avg_n_Wrap(dim_avg_n_Wrap(precip08(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)
precip_ARM_SGP_Aug = precip_ARM_SGP_Aug * 24.0
precip_ARM_SGP_Aug@units = "mm/day"
;printVarSummary(precip_ARM_SGP_Aug)

;;----------------- Calculate PDF of WRF
opt = True

bin_min = 0.0
bin_max = 20.0
bin_n  = 50
bin_width = (bin_max - bin_min) / bin_n

opt          = True
opt@bin_min = bin_min
opt@bin_max = bin_max

RAIN_WRF_May_pdf = pdfx(RAIN_WRF_SGP_May,bin_n,opt)
RAIN_WRF_May_pdf = RAIN_WRF_May_pdf / bin_width

RAIN_WRF_Jun_pdf = pdfx(RAIN_WRF_SGP_Jun,bin_n,opt)
RAIN_WRF_Jun_pdf = RAIN_WRF_Jun_pdf / bin_width

RAIN_WRF_Jul_pdf = pdfx(RAIN_WRF_SGP_Jul,bin_n,opt)
RAIN_WRF_Jul_pdf = RAIN_WRF_Jul_pdf / bin_width

RAIN_WRF_Aug_pdf = pdfx(RAIN_WRF_SGP_Aug,bin_n,opt)
RAIN_WRF_Aug_pdf = RAIN_WRF_Aug_pdf / bin_width

;;---------------- Calculate PDF of ARMBE
precip_ARM_SGP_May_pdf = pdfx(precip_ARM_SGP_May,bin_n,opt)
precip_ARM_SGP_May_pdf = precip_ARM_SGP_May_pdf / bin_width

precip_ARM_SGP_Jun_pdf = pdfx(precip_ARM_SGP_Jun,bin_n,opt)
precip_ARM_SGP_Jun_pdf = precip_ARM_SGP_Jun_pdf / bin_width

precip_ARM_SGP_Jul_pdf = pdfx(precip_ARM_SGP_Jul,bin_n,opt)
precip_ARM_SGP_Jul_pdf = precip_ARM_SGP_Jul_pdf / bin_width

precip_ARM_SGP_Aug_pdf = pdfx(precip_ARM_SGP_Aug,bin_n,opt)
precip_ARM_SGP_Aug_pdf = precip_ARM_SGP_Aug_pdf / bin_width

;;--------------plot ------------
wks = gsn_open_wks("png","precipPDF")

plot = new(4,graphic)

res = True
res@gsnDraw = False
res@gsnFrame = False

;======= add a legend
 res@pmLegendDisplayMode    = "Always"              ; turn on legend

 res@pmLegendSide           = "Top"                 ; Change location of 
 res@pmLegendParallelPosF   = .80                   ; move units right
 res@pmLegendOrthogonalPosF = -0.35                  ; more neg = down

 res@pmLegendWidthF         = 0.08                  ; Change width and
 res@pmLegendHeightF        = 0.15                  ; height of legend.
 res@lgLabelFontHeightF     = .015                   ; change font height
 res@lgPerimOn              = False                 ; no box around
; labels for the legend
 res@xyExplicitLegendLabels = (/"WRF_Morri","ARMBE2D"/)
 res@xyLineColors      = (/"blue","black"/)
 res@xyDashPatterns  = (/1,0/)
;==========================
 res@xyLineThicknesses = (/3.0,3.0/)
 res@xyXStyle          = "Log"

;------------------------
res@tiMainString = "precip, PDF, May"
res@tiYAxisString = "PDF, [% / (mm/day)]"
res@tiXAxisString = "mm/day"

plot(0) = gsn_csm_xy(wks,RAIN_WRF_May_pdf@bin_center,(/RAIN_WRF_May_pdf,precip_ARM_SGP_May_pdf/),res)

res@tiMainString = "precip, PDF, Jun"
plot(1) = gsn_csm_xy(wks,RAIN_WRF_Jun_pdf@bin_center,(/RAIN_WRF_Jun_pdf,precip_ARM_SGP_Jun_pdf/),res)

res@tiMainString = "precip, PDF, Jul"
plot(2) = gsn_csm_xy(wks,RAIN_WRF_Jul_pdf@bin_center,(/RAIN_WRF_Jul_pdf,precip_ARM_SGP_Jul_pdf/),res)

res@tiMainString = "precip, PDF, Aug"
plot(3) = gsn_csm_xy(wks,RAIN_WRF_Aug_pdf@bin_center,(/RAIN_WRF_Aug_pdf,precip_ARM_SGP_Aug_pdf/),res)

;----------------------
resP = True

resP@amJust = "TopRight"
gsn_panel(wks,plot,(/1,4/),resP)


















end