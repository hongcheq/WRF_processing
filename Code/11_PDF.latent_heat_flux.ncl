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
LH_regrid = f_WRF->LH_regrid
;printVarSummary(LH_regrid)

LH_WRF_SGP = dim_avg_n_Wrap(dim_avg_n_Wrap(LH_regrid(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)
printVarSummary(LH_WRF_SGP)

LH_WRF_SGP_May = LH_WRF_SGP(0:737)
LH_WRF_SGP_Jun = LH_WRF_SGP(738:1457)
LH_WRF_SGP_Jul = LH_WRF_SGP(1458:2201)
LH_WRF_SGP_Aug = LH_WRF_SGP(2202:)

;;----------- WRF_Thom areal average
LH_regrid_Thom = f_WRF_Thom->LH_regrid

LH_WRF_Thom_SGP = dim_avg_n_Wrap(dim_avg_n_Wrap(LH_regrid_Thom(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)

LH_WRF_Thom_SGP_May = LH_WRF_Thom_SGP(:)   ; test .nc only has a few days
;---------- uncomment
;LH_WRF_Thom_SGP_May = LH_WRF_Thom_SGP(0:737)
;LH_WRF_Thom_SGP_Jun = LH_WRF_Thom_SGP(738:1457)
;LH_WRF_Thom_SGP_Jul = LH_WRF_Thom_SGP(1458:2201)
;LH_WRF_Thom_SGP_Aug = LH_WRF_Thom_SGP(2202:)
;-------------------

;;----------ARMBE2DGRID areal average----------------
lh05 = f_ARM_05->latent_heat_flux
lh06 = f_ARM_06->latent_heat_flux
lh07 = f_ARM_07->latent_heat_flux
lh08 = f_ARM_08->latent_heat_flux

lh05 = -lh05
lh06 = -lh06
lh07 = -lh07
lh08 = -lh08

lh_ARM_SGP_May = dim_avg_n_Wrap(dim_avg_n_Wrap(lh05(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)
lh_ARM_SGP_Jun = dim_avg_n_Wrap(dim_avg_n_Wrap(lh06(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)
lh_ARM_SGP_Jul = dim_avg_n_Wrap(dim_avg_n_Wrap(lh07(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)
lh_ARM_SGP_Aug = dim_avg_n_Wrap(dim_avg_n_Wrap(lh08(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)

;;----------------- Calculate PDF of WRF
opt = True

bin_min = -100.0
bin_max = 450.0
bin_n  = 50
bin_width = (bin_max - bin_min) / bin_n

opt          = True
opt@bin_min = bin_min
opt@bin_max = bin_max

LH_WRF_May_pdf = pdfx(LH_WRF_SGP_May,bin_n,opt)
LH_WRF_May_pdf = LH_WRF_May_pdf / bin_width

LH_WRF_Jun_pdf = pdfx(LH_WRF_SGP_Jun,bin_n,opt)
LH_WRF_Jun_pdf = LH_WRF_Jun_pdf / bin_width

LH_WRF_Jul_pdf = pdfx(LH_WRF_SGP_Jul,bin_n,opt)
LH_WRF_Jul_pdf = LH_WRF_Jul_pdf / bin_width

LH_WRF_Aug_pdf = pdfx(LH_WRF_SGP_Aug,bin_n,opt)
LH_WRF_Aug_pdf = LH_WRF_Aug_pdf / bin_width

;------------ calculate WRF_Thom
LH_WRF_Thom_May_pdf = pdfx(LH_WRF_Thom_SGP_May,bin_n,opt)
LH_WRF_Thom_May_pdf = LH_WRF_Thom_May_pdf / bin_width

;----------- uncomment
;LH_WRF_Thom_Jun_pdf = pdfx(LH_WRF_Thom_SGP_Jun,bin_n,opt)
;LH_WRF_Thom_Jun_pdf = LH_WRF_Thom_Jun_pdf / bin_width
;
;LH_WRF_Thom_Jul_pdf = pdfx(LH_WRF_Thom_SGP_Jul,bin_n,opt)
;LH_WRF_Thom_Jul_pdf = LH_WRF_Thom_Jul_pdf / bin_width
;
;LH_WRF_Thom_Aug_pdf = pdfx(LH_WRF_Thom_SGP_Aug,bin_n,opt)
;LH_WRF_Thom_Aug_pdf = LH_WRF_Thom_Aug_pdf / bin_width
;;---------------

;;---------------- Calculate PDF of ARMBE
lh_ARM_SGP_May_pdf = pdfx(lh_ARM_SGP_May,bin_n,opt)
lh_ARM_SGP_May_pdf = lh_ARM_SGP_May_pdf / bin_width

lh_ARM_SGP_Jun_pdf = pdfx(lh_ARM_SGP_Jun,bin_n,opt)
lh_ARM_SGP_Jun_pdf = lh_ARM_SGP_Jun_pdf / bin_width

lh_ARM_SGP_Jul_pdf = pdfx(lh_ARM_SGP_Jul,bin_n,opt)
lh_ARM_SGP_Jul_pdf = lh_ARM_SGP_Jul_pdf / bin_width

lh_ARM_SGP_Aug_pdf = pdfx(lh_ARM_SGP_Aug,bin_n,opt)
lh_ARM_SGP_Aug_pdf = lh_ARM_SGP_Aug_pdf / bin_width

;;--------------plot ------------
wks = gsn_open_wks("x11","../Figure/PDF.latent_heat_flux")

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
res@tiMainString = "Latent heat flux, PDF, May"
res@tiYAxisString = "PDF, [% / (W/m2)]"
res@tiXAxisString = "W/m2"

plot(0) = gsn_csm_xy(wks,LH_WRF_May_pdf@bin_center,(/LH_WRF_May_pdf,LH_WRF_Thom_May_pdf,lh_ARM_SGP_May_pdf/),res)

;----------- uncomment
;res@tiMainString = "Latent heat flux, PDF, Jun"
;plot(1) = gsn_csm_xy(wks,LH_WRF_Jun_pdf@bin_center,(/LH_WRF_Jun_pdf,LH_WRF_Thom_Jun_pdf,lh_ARM_SGP_Jun_pdf/),res)
;
;res@tiMainString = "Latent heat flux, PDF, Jul"
;plot(2) = gsn_csm_xy(wks,LH_WRF_Jul_pdf@bin_center,(/LH_WRF_Jul_pdf,LH_WRF_Thom_Jul_pdf,lh_ARM_SGP_Jul_pdf/),res)
;
;res@tiMainString = "Latent heat flux, PDF, Aug"
;plot(3) = gsn_csm_xy(wks,LH_WRF_Aug_pdf@bin_center,(/LH_WRF_Aug_pdf,LH_WRF_Thom_Aug_pdf,lh_ARM_SGP_Aug_pdf/),res)
;--------------

;----------------------
resP = True

resP@amJust = "TopRight"
gsn_panel(wks,plot,(/1,4/),resP)


end
