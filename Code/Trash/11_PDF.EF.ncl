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

threshold = 10.0
;threshold = 50.0

;;========= WRF areal average 
LH_regrid = f_WRF->LH_regrid
HFX_regrid = f_WRF->HFX_regrid

EF_regrid = LH_regrid
EF_regrid@_FillValue = LH_regrid@missing_value
EF_regrid = LH_regrid / where( (LH_regrid+HFX_regrid) .gt. threshold , (HFX_regrid+LH_regrid), EF_regrid@_FillValue )

EF_WRF_SGP = dim_avg_n_Wrap(dim_avg_n_Wrap(EF_regrid(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)
printVarSummary(EF_WRF_SGP)

EF_WRF_SGP_May = EF_WRF_SGP(0:737)
EF_WRF_SGP_Jun = EF_WRF_SGP(738:1457)
EF_WRF_SGP_Jul = EF_WRF_SGP(1458:2201)
EF_WRF_SGP_Aug = EF_WRF_SGP(2202:)

;;============= WRF_Thom
LH_regrid_Thom = f_WRF_Thom->LH_regrid
HFX_regrid_Thom = f_WRF_Thom->HFX_regrid

EF_regrid_Thom = LH_regrid_Thom
EF_regrid_Thom@_FillValue = LH_regrid_Thom@missing_value
EF_regrid_Thom = LH_regrid_Thom / where( (LH_regrid_Thom+HFX_regrid_Thom) .gt. threshold , (HFX_regrid_Thom+LH_regrid_Thom), EF_regrid_Thom@_FillValue )

EF_WRF_Thom_SGP = dim_avg_n_Wrap(dim_avg_n_Wrap(EF_regrid_Thom(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)
printVarSummary(EF_WRF_Thom_SGP)

EF_WRF_Thom_SGP_May = EF_WRF_Thom_SGP(:)   ; the test .nc only has a few days
;------- uncomment
;EF_WRF_Thom_SGP_May = EF_WRF_Thom_SGP(0:737)
;EF_WRF_Thom_SGP_Jun = EF_WRF_Thom_SGP(738:1457)
;EF_WRF_Thom_SGP_Jul = EF_WRF_Thom_SGP(1458:2201)
;EF_WRF_Thom_SGP_Aug = EF_WRF_Thom_SGP(2202:)

;;----------ARMBE2DGRID areal average----------------
lh05 = f_ARM_05->latent_heat_flux
lh06 = f_ARM_06->latent_heat_flux
lh07 = f_ARM_07->latent_heat_flux
lh08 = f_ARM_08->latent_heat_flux

lh05 = -lh05
lh06 = -lh06
lh07 = -lh07
lh08 = -lh08

sh05 = f_ARM_05->sensible_heat_flux
sh06 = f_ARM_06->sensible_heat_flux
sh07 = f_ARM_07->sensible_heat_flux
sh08 = f_ARM_08->sensible_heat_flux

sh05 = -sh05
sh06 = -sh06
sh07 = -sh07
sh08 = -sh08

ef05 = lh05
ef05@_FillValue = -9999
ef05 = lh05 / where( (lh05+sh05) .gt. threshold , (sh05+lh05), ef05@_FillValue )

ef06 = lh06
ef06@_FillValue = -9999
ef06 = lh06 / where( (lh06+sh06) .gt. threshold , (sh06+lh06), ef06@_FillValue )

ef07 = lh07
ef07@_FillValue = -9999
ef07 = lh07 / where( (lh07+sh07) .gt. threshold , (sh07+lh07), ef07@_FillValue )

ef08 = lh08
ef08@_FillValue = -9999
ef08 = lh08 / where( (lh08+sh08) .gt. threshold , (sh08+lh08), ef08@_FillValue )

ef_ARM_SGP_May = dim_avg_n_Wrap(dim_avg_n_Wrap(ef05(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)
ef_ARM_SGP_Jun = dim_avg_n_Wrap(dim_avg_n_Wrap(ef06(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)
ef_ARM_SGP_Jul = dim_avg_n_Wrap(dim_avg_n_Wrap(ef07(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)
ef_ARM_SGP_Aug = dim_avg_n_Wrap(dim_avg_n_Wrap(ef08(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)

;;----------------- Calculate PDF of WRF
opt = True

bin_min = 0.0
bin_max = 2.0
bin_n  = 50
bin_width = (bin_max - bin_min) / bin_n

opt          = True
opt@bin_min = bin_min
opt@bin_max = bin_max

EF_WRF_May_pdf = pdfx(EF_WRF_SGP_May,bin_n,opt)
EF_WRF_May_pdf = EF_WRF_May_pdf / bin_width

EF_WRF_Jun_pdf = pdfx(EF_WRF_SGP_Jun,bin_n,opt)
EF_WRF_Jun_pdf = EF_WRF_Jun_pdf / bin_width

EF_WRF_Jul_pdf = pdfx(EF_WRF_SGP_Jul,bin_n,opt)
EF_WRF_Jul_pdf = EF_WRF_Jul_pdf / bin_width

EF_WRF_Aug_pdf = pdfx(EF_WRF_SGP_Aug,bin_n,opt)
EF_WRF_Aug_pdf = EF_WRF_Aug_pdf / bin_width

;--------------- calculate PDF of WRF_Thom
EF_WRF_Thom_May_pdf = pdfx(EF_WRF_Thom_SGP_May,bin_n,opt)
EF_WRF_Thom_May_pdf = EF_WRF_Thom_May_pdf / bin_width

;-------- uncomment
;EF_WRF_Thom_Jun_pdf = pdfx(EF_WRF_Thom_SGP_Jun,bin_n,opt)
;EF_WRF_Thom_Jun_pdf = EF_WRF_Thom_Jun_pdf / bin_width
;
;EF_WRF_Thom_Jul_pdf = pdfx(EF_WRF_Thom_SGP_Jul,bin_n,opt)
;EF_WRF_Thom_Jul_pdf = EF_WRF_Thom_Jul_pdf / bin_width
;
;EF_WRF_Thom_Aug_pdf = pdfx(EF_WRF_Thom_SGP_Aug,bin_n,opt)
;EF_WRF_Thom_Aug_pdf = EF_WRF_Thom_Aug_pdf / bin_width
;--------------

;;---------------- Calculate PDF of ARMBE
ef_ARM_SGP_May_pdf = pdfx(ef_ARM_SGP_May,bin_n,opt)
ef_ARM_SGP_May_pdf = ef_ARM_SGP_May_pdf / bin_width

ef_ARM_SGP_Jun_pdf = pdfx(ef_ARM_SGP_Jun,bin_n,opt)
ef_ARM_SGP_Jun_pdf = ef_ARM_SGP_Jun_pdf / bin_width

ef_ARM_SGP_Jul_pdf = pdfx(ef_ARM_SGP_Jul,bin_n,opt)
ef_ARM_SGP_Jul_pdf = ef_ARM_SGP_Jul_pdf / bin_width

ef_ARM_SGP_Aug_pdf = pdfx(ef_ARM_SGP_Aug,bin_n,opt)
ef_ARM_SGP_Aug_pdf = ef_ARM_SGP_Aug_pdf / bin_width

;;--------------plot ------------
wks = gsn_open_wks("x11","../Figure/PDF.EF")

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
res@tiMainString = "EF, PDF, May"
res@tiYAxisString = "PDF, [% / unitless]"
res@tiXAxisString = "unitless"

plot(0) = gsn_csm_xy(wks,EF_WRF_May_pdf@bin_center,(/EF_WRF_May_pdf,EF_WRF_Thom_May_pdf,ef_ARM_SGP_May_pdf/),res)

;----------- uncomment
;res@tiMainString = "EF, PDF, Jun"
;plot(1) = gsn_csm_xy(wks,EF_WRF_Jun_pdf@bin_center,(/EF_WRF_Jun_pdf,EF_WRF_Thom_Jun_pdf ,ef_ARM_SGP_Jun_pdf/),res)
;
;res@tiMainString = "EF, PDF, Jul"
;plot(2) = gsn_csm_xy(wks,EF_WRF_Jul_pdf@bin_center,(/EF_WRF_Jul_pdf,EF_WRF_Thom_Jul_pdf,ef_ARM_SGP_Jul_pdf/),res)
;
;res@tiMainString = "EF, PDF, Aug"
;plot(3) = gsn_csm_xy(wks,EF_WRF_Aug_pdf@bin_center,(/EF_WRF_Aug_pdf,EF_WRF_Thom_Aug_pdf,ef_ARM_SGP_Aug_pdf/),res)
;--------------------

;----------------------
resP = True

resP@amJust = "TopRight"
gsn_panel(wks,plot,(/1,4/),resP)


end
