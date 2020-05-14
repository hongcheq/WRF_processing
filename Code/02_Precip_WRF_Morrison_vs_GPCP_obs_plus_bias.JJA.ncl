;Function: WRF output vs obs
;Date: 20200311

;load "/Users/qin5/Documents/Programming/NCL/my_funcs_and_procs/Calendar.ncl"
load "/home/qin5/Programming/NCL/my_funcs_and_procs/Calendar.ncl"

begin
VAR_WRF_str = (/"RAIN_tot_regrid"/)
VAR_obs_str = (/"prect"/)

label_string = "_Morrison"

;WRF_file = "WRF.postprocessing.extract.nc"
WRF_file = "/home/qin5/Data/WRF.postprocessing.extract.nc"
obs_file = "/home/qin5/Data/CAUSES_obs/prect_gpcp_2011_daily.nc"

WRF_f = addfile(WRF_file,"r")
obs_f = addfile(obs_file,"r")

VAR_WRF = WRF_f->$VAR_WRF_str$

VAR_obs = obs_f->$VAR_obs_str$

;--------------------------

printVarSummary(VAR_WRF)
printVarSummary(VAR_obs)
printVarSummary(VAR_obs&time)

;--------------- Calculate monthly values -----

;print(Calendar(VAR_WRF&Time))  ; daily values May-Aug
;print(Calendar(VAR_obs_daily&Time)) ; daily values Jan-Dec

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
  wks = gsn_open_wks("png","../Figure/"+VAR_WRF_str+label_string)              ; send graphics to PNG file

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
  res@cnMinLevelValF       = 0.
  res@cnMaxLevelValF       =  7.
  res@cnLevelSpacingF      =   0.5 
  
  res@gsnAddCyclic = False 

  res@mpMaxLatF                   = 52.0           ; choose subregion           
  res@mpMinLatF                   = 25.0
  res@mpMaxLonF                   = 290.0
  res@mpMinLonF                   = 235.0

  gsn_reverse_colormap(wks)
res@mpOutlineBoundarySets     = "GeophysicalAndUSStates"; turn on states
  res@mpDataBaseVersion         = "MediumRes"             ; select database
  res@mpDataSetName             = "Earth..2"

  res@gsnCenterString = "WRF_Morri, JJA"
  plot(0) = gsn_csm_contour_map(wks,VAR_WRF_JJA,res) 

  res@gsnCenterString = "GPCP, JJA"
  plot(1) = gsn_csm_contour_map(wks,VAR_obs_JJA,res) 

  res@cnLevelSelectionMode =  "ManualLevels"   
  res@cnMinLevelValF       = -4.
  res@cnMaxLevelValF       =  4.
  res@cnLevelSpacingF      =   0.5 

  res@gsnCenterString = "WRF_Morri - GPCP, JJA"
  plot(2) = gsn_csm_contour_map(wks,VAR_bias_JJA,res) 

;************************************************
; create panel
;************************************************
  resP                     = True                ; modify the panel plot
  resP@gsnPanelMainString = "Total precip, WRF"+label_string+" vs GPCP obs"

 ; resP@gsnPanelLabelBar    = True                ; add common colorbar
  resP@lbLabelFontHeightF  = 0.007               ; make labels smaller

  gsn_panel(wks,plot,(/3,1/),resP)               ; now draw as one plot



end
