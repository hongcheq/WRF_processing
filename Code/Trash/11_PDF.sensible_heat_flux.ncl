;Function: PDF analysis

load "/home/qin5/Programming/NCL/my_funcs_and_procs/Calendar.ncl"

begin

dir_WRF = "/home/qin5/Data/WRF.postprocessing.extract.hourly.nc"
dir_WRF_Thom = "/home/qin5/Data/WRF.postprocessing.extract.hourly.Thom.nc"

f_WRF = addfile(dir_WRF,"r")
f_WRF_Thom = addfile(dir_WRF_Thom,"r")

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
HFX_regrid = f_WRF->HFX_regrid

HFX_WRF_SGP = dim_avg_n_Wrap(dim_avg_n_Wrap(HFX_regrid(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)
printVarSummary(HFX_WRF_SGP)

HFX_WRF_SGP_May = HFX_WRF_SGP(0:737)
HFX_WRF_SGP_Jun = HFX_WRF_SGP(738:1457)
HFX_WRF_SGP_Jul = HFX_WRF_SGP(1458:2201)
HFX_WRF_SGP_Aug = HFX_WRF_SGP(2202:)

;-------------- WRF_Thom areal average
HFX_regrid_Thom = f_WRF_Thom->HFX_regrid

HFX_WRF_Thom_SGP = dim_avg_n_Wrap(dim_avg_n_Wrap(HFX_regrid_Thom(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)
printVarSummary(HFX_WRF_Thom_SGP)

HFX_WRF_Thom_SGP_May = HFX_WRF_Thom_SGP(:)  ; the test.nc has only a few days
;-------- uncomment
;HFX_WRF_Thom_SGP_May = HFX_WRF_Thom_SGP(0:737)
;HFX_WRF_Thom_SGP_Jun = HFX_WRF_Thom_SGP(738:1457)
;HFX_WRF_Thom_SGP_Jul = HFX_WRF_Thom_SGP(1458:2201)
;HFX_WRF_Thom_SGP_Aug = HFX_WRF_Thom_SGP(2202:)
;----------

;;----------ARMBE2DGRID areal average----------------
sh05 = f_ARM_05->sensible_heat_flux
sh06 = f_ARM_06->sensible_heat_flux
sh07 = f_ARM_07->sensible_heat_flux
sh08 = f_ARM_08->sensible_heat_flux

sh05 = -sh05
sh06 = -sh06
sh07 = -sh07
sh08 = -sh08

sh_ARM_SGP_May = dim_avg_n_Wrap(dim_avg_n_Wrap(sh05(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)
sh_ARM_SGP_Jun = dim_avg_n_Wrap(dim_avg_n_Wrap(sh06(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)
sh_ARM_SGP_Jul = dim_avg_n_Wrap(dim_avg_n_Wrap(sh07(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)
sh_ARM_SGP_Aug = dim_avg_n_Wrap(dim_avg_n_Wrap(sh08(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)

;;----------------- Calculate PDF of WRF
opt = True

bin_min = -100.0
bin_max = 450.0
bin_n  = 50
bin_width = (bin_max - bin_min) / bin_n

opt          = True
opt@bin_min = bin_min
opt@bin_max = bin_max

HFX_WRF_May_pdf = pdfx(HFX_WRF_SGP_May,bin_n,opt)
HFX_WRF_May_pdf = HFX_WRF_May_pdf / bin_width

HFX_WRF_Jun_pdf = pdfx(HFX_WRF_SGP_Jun,bin_n,opt)
HFX_WRF_Jun_pdf = HFX_WRF_Jun_pdf / bin_width

HFX_WRF_Jul_pdf = pdfx(HFX_WRF_SGP_Jul,bin_n,opt)
HFX_WRF_Jul_pdf = HFX_WRF_Jul_pdf / bin_width

HFX_WRF_Aug_pdf = pdfx(HFX_WRF_SGP_Aug,bin_n,opt)
HFX_WRF_Aug_pdf = HFX_WRF_Aug_pdf / bin_width
;
;------------ calculate PDF of WRF_Thom
HFX_WRF_Thom_May_pdf = pdfx(HFX_WRF_Thom_SGP_May,bin_n,opt)
HFX_WRF_Thom_May_pdf = HFX_WRF_Thom_May_pdf / bin_width

;;-------------- uncomment
;HFX_WRF_Thom_Jun_pdf = pdfx(HFX_WRF_Thom_SGP_Jun,bin_n,opt)
;HFX_WRF_Thom_Jun_pdf = HFX_WRF_Thom_Jun_pdf / bin_width
;
;HFX_WRF_Thom_Jul_pdf = pdfx(HFX_WRF_Thom_SGP_Jul,bin_n,opt)
;HFX_WRF_Thom_Jul_pdf = HFX_WRF_Thom_Jul_pdf / bin_width
;
;HFX_WRF_Thom_Aug_pdf = pdfx(HFX_WRF_Thom_SGP_Aug,bin_n,opt)
;HFX_WRF_Thom_Aug_pdf = HFX_WRF_Thom_Aug_pdf / bin_width
;;-----------------------------

;;---------------- Calculate PDF of ARMBE
sh_ARM_SGP_May_pdf = pdfx(sh_ARM_SGP_May,bin_n,opt)
sh_ARM_SGP_May_pdf = sh_ARM_SGP_May_pdf / bin_width

sh_ARM_SGP_Jun_pdf = pdfx(sh_ARM_SGP_Jun,bin_n,opt)
sh_ARM_SGP_Jun_pdf = sh_ARM_SGP_Jun_pdf / bin_width

sh_ARM_SGP_Jul_pdf = pdfx(sh_ARM_SGP_Jul,bin_n,opt)
sh_ARM_SGP_Jul_pdf = sh_ARM_SGP_Jul_pdf / bin_width

sh_ARM_SGP_Aug_pdf = pdfx(sh_ARM_SGP_Aug,bin_n,opt)
sh_ARM_SGP_Aug_pdf = sh_ARM_SGP_Aug_pdf / bin_width

;;--------------plot ------------
wks = gsn_open_wks("x11","../Figure/PDF.sensible_heat_flux")

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
 res@xyExplicitLegendLabels = (/"WRF_Morri","WRF_Thom","ARMBE2D"/)
 res@xyLineColors      = (/"blue","green","black"/)
 res@xyDashPatterns  = (/1,2,0/)
;==========================
 res@xyLineThicknesses = (/3.0,3.0,3.0/)
 ;res@xyXStyle          = "Log"

;------------------------
res@tiMainString = "Sensible heat flux, PDF, May"
res@tiYAxisString = "PDF, [% / (W/m2)]"
res@tiXAxisString = "W/m2"

plot(0) = gsn_csm_xy(wks,HFX_WRF_May_pdf@bin_center,(/HFX_WRF_May_pdf,HFX_WRF_Thom_May_pdf,sh_ARM_SGP_May_pdf/),res)

;----------- uncomment
;res@tiMainString = "Sensible heat flux, PDF, Jun"
;plot(1) = gsn_csm_xy(wks,HFX_WRF_Jun_pdf@bin_center,(/HFX_WRF_Jun_pdf,HFX_WRF_Thom_Jun_pdf,sh_ARM_SGP_Jun_pdf/),res)
;
;res@tiMainString = "Sensible heat flux, PDF, Jul"
;plot(2) = gsn_csm_xy(wks,HFX_WRF_Jul_pdf@bin_center,(/HFX_WRF_Jul_pdf,HFX_WRF_Thom_Jul_pdf,sh_ARM_SGP_Jul_pdf/),res)
;
;res@tiMainString = "Sensible heat flux, PDF, Aug"
;plot(3) = gsn_csm_xy(wks,HFX_WRF_Aug_pdf@bin_center,(/HFX_WRF_Aug_pdf,HFX_WRF_Thom_Aug_pdf,sh_ARM_SGP_Aug_pdf/),res)
;-----------------

;----------------------
resP = True

resP@amJust = "TopRight"
gsn_panel(wks,plot,(/1,4/),resP)


end
