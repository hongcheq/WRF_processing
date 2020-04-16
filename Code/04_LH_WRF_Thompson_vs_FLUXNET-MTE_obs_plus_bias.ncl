;Function: WRF output vs obs
;Date: 20200311

;load "/Users/qin5/Documents/Programming/NCL/my_funcs_and_procs/Calendar.ncl"
load "/home/qin5/Programming/NCL/my_funcs_and_procs/Calendar.ncl"

begin

;label_string = "_Morrison"
label_string = "_Thompson"

VAR_WRF_str = (/"LH_regrid"/)
VAR_obs_str = (/"hfls"/)

WRF_file = "/home/qin5/Data/WRF.postprocessing.extract.Thom.nc"
obs_file = "/home/qin5/Data/CAUSES_obs/LE_H_FLUXNET_2011_conus_1dgrid.nc"

WRF_f = addfile(WRF_file,"r")
obs_f = addfile(obs_file,"r")


VAR_WRF = WRF_f->$VAR_WRF_str$

VAR_obs = obs_f->$VAR_obs_str$

printVarSummary(VAR_WRF)
printVarSummary(VAR_obs)

;--------------- Calculate monthly values -----

VAR_WRF_month = calculate_monthly_values(VAR_WRF, "avg", 0, False)

printVarSummary(VAR_WRF_month)

;------------- May, Jun, Jul, Aug --------

VAR_WRF_May = VAR_WRF_month(0,:,:)
VAR_WRF_Jun = VAR_WRF_month(1,:,:)
VAR_WRF_Jul = VAR_WRF_month(2,:,:)
VAR_WRF_Aug = VAR_WRF_month(3,:,:)
printVarSummary(VAR_WRF_May)

VAR_obs_May = VAR_obs(4,:,:)
VAR_obs_Jun = VAR_obs(5,:,:)
VAR_obs_Jul = VAR_obs(6,:,:)
VAR_obs_Aug = VAR_obs(7,:,:)
printVarSummary(VAR_obs_May)

VAR_bias_May = VAR_obs_May ; metadata
VAR_bias_May = VAR_WRF_May - VAR_obs_May

VAR_bias_Jun = VAR_obs_Jun ; metadata
VAR_bias_Jun = VAR_WRF_Jun - VAR_obs_Jun

VAR_bias_Jul = VAR_obs_Jul ; metadata
VAR_bias_Jul = VAR_WRF_Jul - VAR_obs_Jul

VAR_bias_Aug = VAR_obs_Aug ; metadata
VAR_bias_Aug = VAR_WRF_Aug - VAR_obs_Aug

printVarSummary(VAR_bias_May)

;--------- panel plot ---------
  wks = gsn_open_wks("png","../Figure/"+VAR_WRF_str+label_string)              ; send graphics to PNG file

  plot = new(12,graphic)                          ; create a plot array
  
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

  res@gsnCenterString = "WRF, May"
  plot(0) = gsn_csm_contour_map(wks,VAR_WRF_May,res) 
  res@gsnCenterString = "WRF, Jun"
  plot(1) = gsn_csm_contour_map(wks,VAR_WRF_Jun,res) 
  res@gsnCenterString = "WRF, Jul"
  plot(2) = gsn_csm_contour_map(wks,VAR_WRF_Jul,res) 
  res@gsnCenterString = "WRF, Aug"
  plot(3) = gsn_csm_contour_map(wks,VAR_WRF_Aug,res) 

  res@gsnCenterString = "FLUXNET, May"
  plot(4) = gsn_csm_contour_map(wks,VAR_obs_May,res) 
  res@gsnCenterString = "FLUXNET, Jun"
  plot(5) = gsn_csm_contour_map(wks,VAR_obs_Jun,res) 
  res@gsnCenterString = "FLUXNET, Jul"
  plot(6) = gsn_csm_contour_map(wks,VAR_obs_Jul,res) 
  res@gsnCenterString = "FLUXNET, Aug"
  plot(7) = gsn_csm_contour_map(wks,VAR_obs_Aug,res) 

  res@cnLevelSelectionMode =  "ManualLevels"   
  res@cnMinLevelValF       = -70.
  res@cnMaxLevelValF       =  70.
  res@cnLevelSpacingF      =   10. 

  res@gsnCenterString = "WRF - FLUXNET, May"
  plot(8) = gsn_csm_contour_map(wks,VAR_bias_May,res) 
  res@gsnCenterString = "WRF - FLUXNET, Jun"
  plot(9) = gsn_csm_contour_map(wks,VAR_bias_Jun,res) 
  res@gsnCenterString = "WRF - FLUXNET, Jul"
  plot(10) = gsn_csm_contour_map(wks,VAR_bias_Jul,res) 
  res@gsnCenterString = "WRF - FLUXNET, Aug"
  plot(11) = gsn_csm_contour_map(wks,VAR_bias_Aug,res) 

;************************************************
; create panel
;************************************************
  resP                     = True                ; modify the panel plot
  resP@gsnPanelMainString = "Latent heat flux, WRF"+label_string+" vs FLUXNET obs"

 ; resP@gsnPanelLabelBar    = True                ; add common colorbar
  resP@lbLabelFontHeightF  = 0.007               ; make labels smaller

  gsn_panel(wks,plot,(/3,4/),resP)               ; now draw as one plot



end
