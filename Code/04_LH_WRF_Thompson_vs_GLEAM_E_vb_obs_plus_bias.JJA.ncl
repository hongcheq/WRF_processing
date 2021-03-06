;Function: WRF output vs obs
;Date: 20200311

;load "/Users/qin5/Documents/Programming/NCL/my_funcs_and_procs/Calendar.ncl"
load "/home/qin5/Programming/NCL/my_funcs_and_procs/Calendar.ncl"

begin
;label_string = "_Morrison"
label_string = "_Thompson"

VAR_WRF_str = (/"LH_regrid"/)
VAR_obs_str = (/"E_b_regrid"/)

WRF_file = "/home/qin5/Data/WRF.postprocessing.extract.hourly.Thom.05678.nc"
obs_file = "/home/qin5/Data/GLEAM/E_2011_GLEAM.processed.daily.nc"

WRF_f = addfile(WRF_file,"r")
obs_f = addfile(obs_file,"r")

VAR_WRF = WRF_f->$VAR_WRF_str$

VAR_obs = obs_f->$VAR_obs_str$

VAR_obs = VAR_obs * 2265000.0 / (3600*24)   ; from Evaporation mm/day to W/m2
VAR_obs@units = "W/m2"
VAR_obs@long_name = "ET in W/m2 derived from ET in mm/day"

printVarSummary(VAR_WRF)
printVarSummary(VAR_obs)

;--------------- Calculate monthly values -----

VAR_WRF_month = calculate_monthly_values(VAR_WRF, "avg", 0, False)
VAR_obs_month = calculate_monthly_values(VAR_obs, "avg", 0, False)

printVarSummary(VAR_WRF_month)
printVarSummary(VAR_obs_month)

;------------- May, Jun, Jul, Aug --------

VAR_WRF_May = VAR_WRF_month(0,:,:)
VAR_WRF_Jun = VAR_WRF_month(1,:,:)
VAR_WRF_Jul = VAR_WRF_month(2,:,:)
VAR_WRF_Aug = VAR_WRF_month(3,:,:)
VAR_WRF_JJA = dim_avg_n_Wrap(VAR_WRF_month(1:3,:,:),0)
printVarSummary(VAR_WRF_May)

VAR_obs_May = VAR_obs_month(4,:,:)
VAR_obs_Jun = VAR_obs_month(5,:,:)
VAR_obs_Jul = VAR_obs_month(6,:,:)
VAR_obs_Aug = VAR_obs_month(7,:,:)
VAR_obs_JJA = dim_avg_n_Wrap(VAR_obs_month(5:7,:,:),0)
printVarSummary(VAR_obs_May)

VAR_bias_May = VAR_obs_May ; metadata
VAR_bias_May = VAR_WRF_May - VAR_obs_May

VAR_bias_Jun = VAR_obs_Jun ; metadata
VAR_bias_Jun = VAR_WRF_Jun - VAR_obs_Jun

VAR_bias_Jul = VAR_obs_Jul ; metadata
VAR_bias_Jul = VAR_WRF_Jul - VAR_obs_Jul

VAR_bias_Aug = VAR_obs_Aug ; metadata
VAR_bias_Aug = VAR_WRF_Aug - VAR_obs_Aug

VAR_bias_JJA = VAR_obs_JJA ; metadata
VAR_bias_JJA = VAR_WRF_JJA - VAR_obs_JJA

printVarSummary(VAR_bias_May)

;--------- panel plot ---------
  wks = gsn_open_wks("png","../Figure/LH_WRF_vs_GLEAM_E_vb"+label_string)              ; send graphics to PNG file

  plot = new(3,graphic)                          ; create a plot array
  
  res                     = True
  res@gsnDraw             = False           ; don't draw
  res@gsnFrame            = False           ; don't advance frame
  res@cnInfoLabelOn       = False           ; turn off cn info label
  res@cnFillOn            = True            ; turn on color
  ;res@lbLabelBarOn        = False           ; turn off individual cb's
  res@cnLinesOn           = False

  res@cnLevelSelectionMode =  "ManualLevels"   
  res@cnMinLevelValF       = 0.
  res@cnMaxLevelValF       =  160.
  res@cnLevelSpacingF      =   10. 
  
  res@gsnAddCyclic = False 

  res@mpMaxLatF                   = 57.0           ; choose subregion           
  res@mpMinLatF                   = 18.0
  res@mpMaxLonF                   = 292.0
  res@mpMinLonF                   = 233.0

 res@mpOutlineBoundarySets     = "GeophysicalAndUSStates"; turn on states
  res@mpDataBaseVersion         = "MediumRes"             ; select database
  res@mpDataSetName             = "Earth..2"

res@gsnLeftString = ""
  res@gsnCenterString = "WRF_Thom, JJA"
  plot(0) = gsn_csm_contour_map(wks,VAR_WRF_JJA,res) 

  res@gsnCenterString = "GLEAM vb, JJA"
  plot(1) = gsn_csm_contour_map(wks,VAR_obs_JJA,res) 

  res@cnLevelSelectionMode =  "ManualLevels"   
  res@cnMinLevelValF       = -70.
  res@cnMaxLevelValF       =  70.
  res@cnLevelSpacingF      =   10. 

  res@gsnCenterString = "WRF_Thom - GLEAM vb, JJA"
  plot(2) = gsn_csm_contour_map(wks,VAR_bias_JJA,res) 

;************************************************
; create panel
;************************************************
  resP                     = True                ; modify the panel plot
  resP@gsnPanelMainString = "Latent heat flux, WRF"+label_string+" vs GLEAM E_vb"

 ; resP@gsnPanelLabelBar    = True                ; add common colorbar
  resP@lbLabelFontHeightF  = 0.007               ; make labels smaller

  gsn_panel(wks,plot,(/3,1/),resP)               ; now draw as one plot



end
