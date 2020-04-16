;Function: PDF analysis

load "/home/qin5/Programming/NCL/my_funcs_and_procs/Calendar.ncl"

begin

dir_WRF = "/home/qin5/Data/WRF.postprocessing.extract.hourly.nc"
dir_WRF_Thom = "/home/qin5/Data/WRF.postprocessing.extract.hourly.Thom.nc"

f_WRF = addfile(dir_WRF,"r")
f_WRF_Thom = addfile(dir_WRF_Thom,"r")

obs_file = "/home/qin5/Data/Precip_StageIV/Precip_Stage_IV.2011045678.postprocessing.extract.hourly.nc"
obs_f = addfile(obs_file,"r")

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

;;;========= WRF_Thom
RAIN_tot_regrid_Thom = f_WRF_Thom->RAIN_tot_regrid

RAIN_WRF_Thom_SGP = dim_avg_n_Wrap(dim_avg_n_Wrap(RAIN_tot_regrid_Thom(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)
RAIN_WRF_Thom_SGP = RAIN_WRF_Thom_SGP * 24.0
RAIN_WRF_Thom_SGP@units = "mm/day"
printVarSummary(RAIN_WRF_Thom_SGP)

RAIN_WRF_Thom_SGP_May = RAIN_WRF_Thom_SGP(:) ; the test .nc only contains a few days.
;------- uncomment
;RAIN_WRF_Thom_SGP_May = RAIN_WRF_Thom_SGP(0:737)
;RAIN_WRF_Thom_SGP_Jun = RAIN_WRF_Thom_SGP(738:1457)
;RAIN_WRF_Thom_SGP_Jul = RAIN_WRF_Thom_SGP(1458:2201)
;RAIN_WRF_Thom_SGP_Aug = RAIN_WRF_Thom_SGP(2202:)
;-------

;;----------Stage IV areal average----------------
precip_st4 = obs_f->precip_st4_regrid(:,:,:)  

;; NaN values
if (any(isnan_ieee(precip_st4))) then
      value = 1.e20
      replace_ieeenan (precip_st4, value, 0)
      precip_st4@_FillValue = value
end if
printVarSummary(precip_st4)

precip_st4 = precip_st4 * 24.0 ; from mm accumulated per hour, i.e. mm/hour to mm/day
precip_st4@units = "mm/day"

precip_st4_SGP_May = dim_avg_n_Wrap(dim_avg_n_Wrap(precip_st4(718:1461,{lat_1:lat_2},{lon_1:lon_2}),1),1)

precip_st4_SGP_Jun = dim_avg_n_Wrap(dim_avg_n_Wrap(precip_st4(1462:2181,{lat_1:lat_2},{lon_1:lon_2}),1),1)

precip_st4_SGP_Jul = dim_avg_n_Wrap(dim_avg_n_Wrap(precip_st4(2180:2922,{lat_1:lat_2},{lon_1:lon_2}),1),1)

precip_st4_SGP_Aug = dim_avg_n_Wrap(dim_avg_n_Wrap(precip_st4(2923:,{lat_1:lat_2},{lon_1:lon_2}),1),1)
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

;;; ------------- calculate PDF of WRF_Thom
RAIN_WRF_Thom_May_pdf = pdfx(RAIN_WRF_Thom_SGP_May,bin_n,opt)
RAIN_WRF_Thom_May_pdf = RAIN_WRF_Thom_May_pdf / bin_width

;--------uncomment
;RAIN_WRF_Thom_Jun_pdf = pdfx(RAIN_WRF_Thom_SGP_Jun,bin_n,opt)
;RAIN_WRF_Thom_Jun_pdf = RAIN_WRF_Thom_Jun_pdf / bin_width
;
;RAIN_WRF_Thom_Jul_pdf = pdfx(RAIN_WRF_Thom_SGP_Jul,bin_n,opt)
;RAIN_WRF_Thom_Jul_pdf = RAIN_WRF_Thom_Jul_pdf / bin_width
;
;RAIN_WRF_Thom_Aug_pdf = pdfx(RAIN_WRF_Thom_SGP_Aug,bin_n,opt)
;RAIN_WRF_Thom_Aug_pdf = RAIN_WRF_Thom_Aug_pdf / bin_width
;-------------

;;---------------- Calculate PDF of StageIV
precip_st4_SGP_May_pdf = pdfx(precip_st4_SGP_May,bin_n,opt)
precip_st4_SGP_May_pdf = precip_st4_SGP_May_pdf / bin_width

precip_st4_SGP_Jun_pdf = pdfx(precip_st4_SGP_Jun,bin_n,opt)
precip_st4_SGP_Jun_pdf = precip_st4_SGP_Jun_pdf / bin_width

precip_st4_SGP_Jul_pdf = pdfx(precip_st4_SGP_Jul,bin_n,opt)
precip_st4_SGP_Jul_pdf = precip_st4_SGP_Jul_pdf / bin_width

precip_st4_SGP_Aug_pdf = pdfx(precip_st4_SGP_Aug,bin_n,opt)
precip_st4_SGP_Aug_pdf = precip_st4_SGP_Aug_pdf / bin_width

;;--------------plot ------------
wks = gsn_open_wks("x11","../Figure/PDF.precip.StageIV")

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
 res@xyExplicitLegendLabels = (/"WRF_Morri","WRF_Thom","pr_StageIV"/)
 res@xyLineColors      = (/"blue","green","black"/)
 res@xyDashPatterns  = (/1,2,0/)
;==========================
 res@xyLineThicknesses = (/3.0,3.0,3.0/)
 res@xyXStyle          = "Log"

;------------------------
res@tiMainString = "precip, PDF, May"
res@tiYAxisString = "PDF, [% / (mm/day)]"
res@tiXAxisString = "mm/day"

plot(0) = gsn_csm_xy(wks,RAIN_WRF_May_pdf@bin_center,(/RAIN_WRF_May_pdf,RAIN_WRF_Thom_May_pdf,precip_st4_SGP_May_pdf/),res)

;-------- uncomment
;res@tiMainString = "precip, PDF, Jun"
;plot(1) = gsn_csm_xy(wks,RAIN_WRF_Jun_pdf@bin_center,(/RAIN_WRF_Jun_pdf,RAIN_WRF_Thom_Jun_pdf,precip_st4_SGP_Jun_pdf/),res)
;
;res@tiMainString = "precip, PDF, Jul"
;plot(2) = gsn_csm_xy(wks,RAIN_WRF_Jul_pdf@bin_center,(/RAIN_WRF_Jul_pdf,RAIN_WRF_Thom_Jul_pdf,precip_st4_SGP_Jul_pdf/),res)
;
;res@tiMainString = "precip, PDF, Aug"
;plot(3) = gsn_csm_xy(wks,RAIN_WRF_Aug_pdf@bin_center,(/RAIN_WRF_Aug_pdf,RAIN_WRF_Thom_Aug_pdf,precip_st4_SGP_Aug_pdf/),res)
;;-----------
;
;----------------------
resP = True

resP@amJust = "TopRight"
gsn_panel(wks,plot,(/1,4/),resP)


end
