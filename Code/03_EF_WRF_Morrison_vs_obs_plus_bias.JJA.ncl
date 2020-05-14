;Function: WRF output vs obs
;Date: 20200311

;load "/Users/qin5/Documents/Programming/NCL/my_funcs_and_procs/Calendar.ncl"
load "/home/qin5/Programming/NCL/my_funcs_and_procs/Calendar.ncl"

begin
label_string = "_Morrison"

VAR_WRF_str = (/"HFX_regrid"/)
VAR_obs_str = (/"hfss"/)

VAR2_WRF_str = (/"LH_regrid"/)
VAR2_obs_str = (/"hfls"/)

;WRF_file = "/home/qin5/Data/WRF.postprocessing.extract.nc"
WRF_file = "/home/qin5/Data/WRF.postprocessing.extract.hourly.Morri.nc"
obs_file = "/home/qin5/Data/CAUSES_obs/LE_H_FLUXNET_2011_conus_1dgrid.nc"

WRF_f = addfile(WRF_file,"r")
obs_f = addfile(obs_file,"r")

VAR_WRF = WRF_f->$VAR_WRF_str$
VAR_obs = obs_f->$VAR_obs_str$

VAR2_WRF = WRF_f->$VAR2_WRF_str$
VAR2_obs = obs_f->$VAR2_obs_str$

printVarSummary(VAR_WRF)
printVarSummary(VAR_obs)

printVarSummary(VAR2_WRF)
printVarSummary(VAR2_obs)

;--------------- Calculate monthly values -----

VAR_WRF_month = calculate_monthly_values(VAR_WRF, "avg", 0, False)
VAR2_WRF_month = calculate_monthly_values(VAR2_WRF, "avg", 0, False)

printVarSummary(VAR_WRF_month)

;-------- calculate EF
EF_WRF = VAR2_WRF_month ; metadata
;EF_WRF = VAR2_WRF_month / (VAR_WRF_month+VAR2_WRF_month)
EF_WRF = VAR2_WRF_month / where( (VAR_WRF_month+VAR2_WRF_month) .gt. 10.0, VAR_WRF_month+VAR2_WRF_month, EF_WRF@_FillValue)
printVarSummary(EF_WRF)

EF_obs = VAR2_obs ; metadata
;EF_obs = VAR2_obs / (VAR_obs+VAR2_obs)
EF_obs = VAR2_obs / where( (VAR_obs+VAR2_obs) .gt. 10.0, (VAR_obs+VAR2_obs), EF_obs@_FillValue)
printVarSummary(EF_obs)

;------------- May, Jun, Jul, Aug --------

EF_WRF_May = EF_WRF(0,:,:)
EF_WRF_Jun = EF_WRF(1,:,:)
EF_WRF_Jul = EF_WRF(2,:,:)
EF_WRF_Aug = EF_WRF(3,:,:)
EF_WRF_JJA = dim_avg_n_Wrap(EF_WRF(1:3,:,:),0)
printVarSummary(EF_WRF_May)
printVarSummary(EF_WRF_JJA)

EF_obs_May = EF_obs(4,:,:)
EF_obs_Jun = EF_obs(5,:,:)
EF_obs_Jul = EF_obs(6,:,:)
EF_obs_Aug = EF_obs(7,:,:)
EF_obs_JJA = dim_avg_n_Wrap(EF_obs(5:7,:,:),0)
printVarSummary(EF_obs_May)

EF_bias_May = EF_obs_May ; metadata
EF_bias_May = EF_WRF_May - EF_obs_May

EF_bias_Jun = EF_obs_Jun ; metadata
EF_bias_Jun = EF_WRF_Jun - EF_obs_Jun

EF_bias_Jul = EF_obs_Jul ; metadata
EF_bias_Jul = EF_WRF_Jul - EF_obs_Jul

EF_bias_Aug = EF_obs_Aug ; metadata
EF_bias_Aug = EF_WRF_Aug - EF_obs_Aug

EF_bias_JJA = EF_obs_JJA ; metadata
EF_bias_JJA = EF_WRF_JJA - EF_obs_JJA

printVarSummary(EF_bias_May)

;--------- panel plot ---------
  wks = gsn_open_wks("png","../Figure/EF_"+label_string)              ; send graphics to PNG file 
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
  res@cnMaxLevelValF       =  1.
;  res@cnMaxLevelValF       =  260.
  res@cnLevelSpacingF      =   0.1 
  
  res@gsnAddCyclic = False 

  res@mpMaxLatF                   = 52.0           ; choose subregion           
  res@mpMinLatF                   = 25.0
  res@mpMaxLonF                   = 290.0
  res@mpMinLonF                   = 235.0

res@mpOutlineBoundarySets     = "GeophysicalAndUSStates"; turn on states
  res@mpDataBaseVersion         = "MediumRes"             ; select database
  res@mpDataSetName             = "Earth..2"

  res@gsnLeftString = "EF"
  res@gsnCenterString = "WRF_Morri, JJA"
print(max(EF_WRF_JJA))
  plot(0) = gsn_csm_contour_map(wks,EF_WRF_JJA,res) 

  res@gsnCenterString = "FLUXNET, JJA"
  plot(1) = gsn_csm_contour_map(wks,EF_obs_JJA,res) 

  res@cnLevelSelectionMode =  "ManualLevels"   
  res@cnMinLevelValF       = -0.3
  res@cnMaxLevelValF       =  0.3
  res@cnLevelSpacingF      =   0.05 

  res@gsnCenterString = "WRF_Morri - FLUXNET, JJA"
  plot(2) = gsn_csm_contour_map(wks,EF_bias_JJA,res) 

;************************************************
; create panel
;************************************************
  resP                     = True                ; modify the panel plot
  resP@gsnPanelMainString = "EF, WRF"+label_string+" vs FLUXNET obs"

 ; resP@gsnPanelLabelBar    = True                ; add common colorbar
  resP@lbLabelFontHeightF  = 0.007               ; make labels smaller

  gsn_panel(wks,plot,(/3,1/),resP)               ; now draw as one plot



end
