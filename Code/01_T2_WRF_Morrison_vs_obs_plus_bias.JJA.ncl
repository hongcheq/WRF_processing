;Function: WRF output vs obs
;Date: 20200311

;load "/Users/qin5/Documents/Programming/NCL/my_funcs_and_procs/Calendar.ncl"
load "/home/qin5/Programming/NCL/my_funcs_and_procs/Calendar.ncl"

begin
label_string = "_Morrison"
WRF_file = "/home/qin5/Data/WRF.postprocessing.extract.nc"

VAR_WRF_str = (/"T2_regrid"/)
VAR_obs_str = (/"t2m"/)

obs_file = "/home/qin5/Data/CAUSES_obs/noaa_conus_T2M_temperature_1p0deg_hourly_2011_MAMJJA.nc"

WRF_f = addfile(WRF_file,"r")
obs_f = addfile(obs_file,"r")

VAR_WRF = WRF_f->$VAR_WRF_str$
VAR_WRF = VAR_WRF - 273.15   ; from K to degree Celsius
VAR_WRF@units = "degree Celsius"

;VAR_WRF&lon = obs_f->Longitude  ; from -125 -- -70  to 235 -- 290

VAR_obs = obs_f->$VAR_obs_str$

VAR_obs!0 = "Time"
VAR_obs&Time = obs_f->Time
VAR_obs&Time@units = "hours since 2011-04-01 00:00:00"

VAR_obs!1 = "lat"
VAR_obs&lat = WRF_f->lat
VAR_obs!2 = "lon"
VAR_obs&lon = WRF_f->lon

;--------- Very Important!!! -------------
;-------- this NOAA t2m has NaN but does not have _FillValues, if not replaced, the final plot is arkward! 
if (any(isnan_ieee(VAR_obs))) then
    if(.not.isatt(VAR_obs,"_FillValue")) then
      VAR_obs@_FillValue = default_fillvalue(typeof(VAR_obs))
    end if
    replace_ieeenan (VAR_obs, VAR_obs@_FillValue, 0)
  end if
;--------------------------

printVarSummary(VAR_WRF)
printVarSummary(VAR_obs)
printVarSummary(VAR_obs&Time)
printVarSummary(VAR_obs&lon)
printVarSummary(VAR_obs&lat)
printVarSummary(VAR_WRF&lat)

;print(VAR_obs&lat)
;print(VAR_WRF&lat)

;--------------- Calculate monthly values -----

;print(Calendar(VAR_WRF&Time))  ; daily values May-Aug
;print(Calendar(VAR_obs_daily&Time)) ; daily values Apr-Aug

VAR_WRF_month = calculate_monthly_values(VAR_WRF, "avg", 0, False)
VAR_obs_month = calculate_monthly_values(VAR_obs, "avg", 0, False)

VAR_obs_test = dim_avg_n_Wrap(VAR_obs,0)

printVarSummary(VAR_WRF_month)
printVarSummary(VAR_obs_month)
printVarSummary(VAR_obs_test)

;------------- May, Jun, Jul, Aug --------

VAR_WRF_May = VAR_WRF_month(0,:,:)
VAR_WRF_Jun = VAR_WRF_month(1,:,:)
VAR_WRF_Jul = VAR_WRF_month(2,:,:)
VAR_WRF_Aug = VAR_WRF_month(3,:,:)
VAR_WRF_JJA = dim_avg_n_Wrap(VAR_WRF_month(1:3,:,:),0)
printVarSummary(VAR_WRF_May)

VAR_obs_May = VAR_obs_month(1,:,:)
VAR_obs_Jun = VAR_obs_month(2,:,:)
VAR_obs_Jul = VAR_obs_month(3,:,:)
VAR_obs_Aug = VAR_obs_month(4,:,:)
VAR_obs_JJA = dim_avg_n_Wrap(VAR_obs_month(2:4,:,:),0)
printVarSummary(VAR_obs_May)

VAR_bias_May = VAR_obs_May ; metadata
VAR_bias_May = VAR_WRF_May - VAR_obs_May

VAR_bias_Jun = VAR_obs_Jun ; metadata
VAR_bias_Jun = VAR_WRF_Jun - VAR_obs_Jun

VAR_bias_Jul = VAR_obs_Jul ; metadata
VAR_bias_Jul = VAR_WRF_Jul - VAR_obs_Jul

VAR_bias_Aug = VAR_obs_Aug ; metadata
VAR_bias_Aug = VAR_WRF_Aug - VAR_obs_Aug

VAR_bias_JJA = VAR_obs_JJA
VAR_bias_JJA = VAR_WRF_JJA - VAR_obs_JJA

printVarSummary(VAR_bias_May)

;--------- panel plot ---------
  wks = gsn_open_wks("png","../Figure/JJA_"+VAR_WRF_str+label_string)              ; send graphics to PNG file

  plot = new(3,graphic)                          ; create a plot array
  
  res                     = True
  res@gsnDraw             = False           ; don't draw
  res@gsnFrame            = False           ; don't advance frame
  res@cnInfoLabelOn       = False           ; turn off cn info label
  res@cnFillOn            = True            ; turn on color
  ;res@lbLabelBarOn        = False           ; turn off individual cb's
  res@cnLinesOn           = False

; to have a common label bar, both plots should be set to the same interval
; b/c the label bar is drawn by default from the interval of the first plot.
  res@cnLevelSelectionMode =  "ManualLevels"   
  res@cnMinLevelValF       = 10.
  res@cnMaxLevelValF       =  38.
  res@cnLevelSpacingF      =   1.0 
  
  res@gsnAddCyclic = False 

  res@mpMaxLatF                   = 57.0           ; choose subregion           
  res@mpMinLatF                   = 18.0
  res@mpMaxLonF                   = 292.0
  res@mpMinLonF                   = 233.0

  res@gsnCenterString = "WRF_Morri, JJA"
  plot(0) = gsn_csm_contour_map(wks,VAR_WRF_JJA,res) 

  res@gsnCenterString = "NOAA, JJA"
  plot(1) = gsn_csm_contour_map(wks,VAR_obs_JJA,res) 

  res@cnLevelSelectionMode =  "ManualLevels"   
  res@cnMinLevelValF       = -5.
  res@cnMaxLevelValF       =  5.
  res@cnLevelSpacingF      =   0.5 

  res@gsnCenterString = "WRF_Morri - NOAA, JJA"
  plot(2) = gsn_csm_contour_map(wks,VAR_bias_JJA,res) 

;************************************************
; create panel
;************************************************
  resP                     = True                ; modify the panel plot
  resP@gsnPanelMainString = "2-m air Temp, WRF"+label_string+" vs NOAA obs"

 ; resP@gsnPanelLabelBar    = True                ; add common colorbar
  resP@lbLabelFontHeightF  = 0.007               ; make labels smaller

  gsn_panel(wks,plot,(/3,1/),resP)               ; now draw as one plot



end
