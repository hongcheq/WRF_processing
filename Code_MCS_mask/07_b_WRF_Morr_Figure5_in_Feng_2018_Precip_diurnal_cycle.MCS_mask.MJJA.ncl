;Note: check the consistency of ds_WRF['RAIN_tot_regrid'].where(WRF_MCS_mask > 0)
;      the time dimension of RAIN_tot_regrid and WRF_MCS_mask need to be the same.

load "/home/qin5/Programming/NCL/my_funcs_and_procs/Calendar.ncl"
begin

f1 = addfile("/home/qin5/Data/WRF_postprocessing/WRF_Morri/WRF.postprocessing.extract.hourly.0.04.RAIN_tot.ncrcat.nc","r")
f2 = addfile("/home/qin5/Data/WRF_postprocessing/WRF_Morri/WRF.mask.postprocessing.extract.hourly.0.04.nc","r")

time1 = f1->time
time2 = f2->time

asciiwrite("./07_b_time1.txt", Calendar(time1))
asciiwrite("./07_b_time2.txt", Calendar(time2))

;On Cori, RAIN_tot has been processed to have the same time as pcptracknumber MCS mask
; Use new file WRF.postprocessing.extract.hourly.0.04.RAIN_tot.time_revise.nc







end 
