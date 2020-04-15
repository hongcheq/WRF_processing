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
T2_regrid = f_WRF->T2_regrid

T2_WRF_SGP = dim_avg_n_Wrap(dim_avg_n_Wrap(T2_regrid(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)

T2_WRF_SGP_May = T2_WRF_SGP(0:737)
T2_WRF_SGP_Jun = T2_WRF_SGP(738:1457)
T2_WRF_SGP_Jul = T2_WRF_SGP(1458:2201)
T2_WRF_SGP_Aug = T2_WRF_SGP(2202:)

;;----------ARMBE2DGRID areal average----------------
temp05 = f_ARM_05->temp
temp06 = f_ARM_06->temp
temp07 = f_ARM_07->temp
temp08 = f_ARM_08->temp

temp_ARM_SGP_May = dim_avg_n_Wrap(dim_avg_n_Wrap(temp05(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)

temp_ARM_SGP_Jun = dim_avg_n_Wrap(dim_avg_n_Wrap(temp06(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)

temp_ARM_SGP_Jul = dim_avg_n_Wrap(dim_avg_n_Wrap(temp07(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)

temp_ARM_SGP_Aug = dim_avg_n_Wrap(dim_avg_n_Wrap(temp08(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)

;;----------------- Calculate PDF of WRF
opt = True

bin_min = 270.0
bin_max = 330.0
bin_n  = 50
bin_width = (bin_max - bin_min) / bin_n

opt          = True
opt@bin_min = bin_min
opt@bin_max = bin_max

T2_WRF_May_pdf = pdfx(T2_WRF_SGP_May,bin_n,opt)
T2_WRF_May_pdf = T2_WRF_May_pdf / bin_width

T2_WRF_Jun_pdf = pdfx(T2_WRF_SGP_Jun,bin_n,opt)
T2_WRF_Jun_pdf = T2_WRF_Jun_pdf / bin_width

T2_WRF_Jul_pdf = pdfx(T2_WRF_SGP_Jul,bin_n,opt)
T2_WRF_Jul_pdf = T2_WRF_Jul_pdf / bin_width

T2_WRF_Aug_pdf = pdfx(T2_WRF_SGP_Aug,bin_n,opt)
T2_WRF_Aug_pdf = T2_WRF_Aug_pdf / bin_width

;;---------------- Calculate PDF of ARMBE
temp_ARM_SGP_May_pdf = pdfx(temp_ARM_SGP_May,bin_n,opt)
temp_ARM_SGP_May_pdf = temp_ARM_SGP_May_pdf / bin_width

temp_ARM_SGP_Jun_pdf = pdfx(temp_ARM_SGP_Jun,bin_n,opt)
temp_ARM_SGP_Jun_pdf = temp_ARM_SGP_Jun_pdf / bin_width

temp_ARM_SGP_Jul_pdf = pdfx(temp_ARM_SGP_Jul,bin_n,opt)
temp_ARM_SGP_Jul_pdf = temp_ARM_SGP_Jul_pdf / bin_width

temp_ARM_SGP_Aug_pdf = pdfx(temp_ARM_SGP_Aug,bin_n,opt)
temp_ARM_SGP_Aug_pdf = temp_ARM_SGP_Aug_pdf / bin_width

;;--------------plot ------------
wks = gsn_open_wks("png","../Figure/PDF.T2")

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
; res@xyXStyle          = "Log"

;------------------------
res@tiMainString = "T2m, PDF, May"
res@tiYAxisString = "PDF, [% / K]"
res@tiXAxisString = "K"

plot(0) = gsn_csm_xy(wks,T2_WRF_May_pdf@bin_center,(/T2_WRF_May_pdf,temp_ARM_SGP_May_pdf/),res)

res@tiMainString = "T2m, PDF, Jun"
plot(1) = gsn_csm_xy(wks,T2_WRF_Jun_pdf@bin_center,(/T2_WRF_Jun_pdf,temp_ARM_SGP_Jun_pdf/),res)

res@tiMainString = "T2m, PDF, Jul"
plot(2) = gsn_csm_xy(wks,T2_WRF_Jul_pdf@bin_center,(/T2_WRF_Jul_pdf,temp_ARM_SGP_Jul_pdf/),res)

res@tiMainString = "T2m, PDF, Aug"
plot(3) = gsn_csm_xy(wks,T2_WRF_Aug_pdf@bin_center,(/T2_WRF_Aug_pdf,temp_ARM_SGP_Aug_pdf/),res)

;----------------------
resP = True

resP@amJust = "TopRight"
gsn_panel(wks,plot,(/1,4/),resP)


end
