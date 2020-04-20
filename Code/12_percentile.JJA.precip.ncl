;Function: box plot analysis

load "/home/qin5/Programming/NCL/my_funcs_and_procs/Calendar.ncl"

begin

dir_WRF = "/home/qin5/Data/WRF.postprocessing.extract.hourly.nc"
dir_WRF_Thom = "/home/qin5/Data/WRF.postprocessing.extract.hourly.Thom.05678.nc"

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

RAIN_WRF_SGP_JJA = RAIN_WRF_SGP(738:)

;;========= WRF_Thom
RAIN_tot_regrid_Thom = f_WRF_Thom->RAIN_tot_regrid

RAIN_WRF_Thom_SGP = dim_avg_n_Wrap(dim_avg_n_Wrap(RAIN_tot_regrid_Thom(:,{lat_1:lat_2},{lon_1:lon_2}),1),1)
RAIN_WRF_Thom_SGP = RAIN_WRF_Thom_SGP * 24.0
RAIN_WRF_Thom_SGP@units = "mm/day"
printVarSummary(RAIN_WRF_Thom_SGP)

RAIN_WRF_Thom_SGP_May = RAIN_WRF_Thom_SGP(0:737)
RAIN_WRF_Thom_SGP_Jun = RAIN_WRF_Thom_SGP(738:1457)
RAIN_WRF_Thom_SGP_Jul = RAIN_WRF_Thom_SGP(1458:2201)
RAIN_WRF_Thom_SGP_Aug = RAIN_WRF_Thom_SGP(2202:)

RAIN_WRF_Thom_SGP_JJA = RAIN_WRF_Thom_SGP(738:)

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

precip_ARM_SGP_JJA = array_append_record(array_append_record (precip_ARM_SGP_Jun, precip_ARM_SGP_Jul, 0), precip_ARM_SGP_Aug,0)
printVarSummary(precip_ARM_SGP_JJA)

;;----------------- Calculate stats of WRF
JJA_WRF_val = new(5,double)

WRF_stats_temp = stat_dispersion(RAIN_WRF_SGP_JJA,False)
JJA_WRF_val(0) = WRF_stats_temp(0) ; mean
JJA_WRF_val(1) = WRF_stats_temp(8) ; median
JJA_WRF_val(2) = WRF_stats_temp(25) ; 95th percentile
JJA_WRF_val(3) = WRF_stats_temp(26) ; 99th percentile
JJA_WRF_val(4) = WRF_stats_temp(27)  ; 99.9th percentile

;-------------- calculate stats of WRF_Thom
JJA_WRF_Thom_val = new(5,double)

WRF_stats_temp = stat_dispersion(RAIN_WRF_Thom_SGP_JJA,False)
JJA_WRF_Thom_val(0) = WRF_stats_temp(0) 
JJA_WRF_Thom_val(1) = WRF_stats_temp(8) 
JJA_WRF_Thom_val(2) = WRF_stats_temp(25) 
JJA_WRF_Thom_val(3) = WRF_stats_temp(26) 
JJA_WRF_Thom_val(4) = WRF_stats_temp(27) 

;;---------------- Calculate stats of ARMBE
JJA_ARM_val = new(5,double)

ARM_stats_temp = stat_dispersion(precip_ARM_SGP_JJA,False)
JJA_ARM_val(0) = ARM_stats_temp(0) 
JJA_ARM_val(1) = ARM_stats_temp(8) 
JJA_ARM_val(2) = ARM_stats_temp(25) 
JJA_ARM_val(3) = ARM_stats_temp(26) 
JJA_ARM_val(4) = ARM_stats_temp(27) 

;;--------------plot ------------
wks = gsn_open_wks("png","../Figure/percentile.precip")

plot = new(1,graphic)

res = True
res@tiYAxisString = "mm/day"

res@gsnDraw = False
res@gsnFrame = False

res@trXMinF = 0.0
res@trXMaxF = 6.0

;res@tmXBLabels = (/"WRF_Morri","WRF_Thom","ARMBE2D"/) ; labels for each box

res@tmXBMode        = "Explicit"
res@tmXBLabels      = (/"Mean","Median","95th p","99th p","99.9th p"/)
res@tmXBValues      = (/1.0,2.0,3.0,4.0,5.0/)

res@xyMarkLineMode     = "Markers"
;res@xyMonoMarkerColor  = False          ; Allow different colors for markers
res@xyMarkerColors     = (/"green","blue","black"/)
res@xyMarkerSizeF     = 0.01

res@xyMarkers          = (/0,2,4,5,6/)

  res@pmLegendDisplayMode    = "Always"            ; turn on legend
  res@pmLegendSide           = "Top"               ; Change location of 
  res@pmLegendParallelPosF   = .15                  ; move units right
  res@pmLegendOrthogonalPosF = -0.5                ; move units down
  res@pmLegendWidthF         = 0.15                ; Change width and
  res@pmLegendHeightF        = 0.18                ; height of legend.
  res@lgPerimOn              = False               ; turn off box around
  res@lgLabelFontHeightF     = .015                 ; label font height
  res@xyExplicitLegendLabels = (/"WRF_Morri","WRF_Thom","ARMBE2D"/)         ; create explicit labels

res@tiMainString = "precip, JJA, WRF"
plot(0) = gsn_csm_xy(wks, (/1.0,2.0,3.0,4.0,5.0/), (/JJA_WRF_val,JJA_WRF_Thom_val,JJA_ARM_val/), res)

;;------------------
;------------------------

resP = True

resP@amJust = "TopRight"
gsn_panel(wks,plot,(/1,1/),resP)


end
