;Function: preprocess ARMBE2D data from Qi Tang
;          so that the time dimension is consistent with /home/qin5/Data/WRF_postprocessing/OBS/mcstrack_20110501-0831.ncrcat.nc, in which time dimension is only 2943 hours.

load "~/Programming/NCL/my_funcs_and_procs/Calendar.ncl"
begin
dir = "/home/qin5/Data/WRF_postprocessing/OBS/"
f1 = addfile(dir+"mcstrack_20110501-0831.ncrcat.nc","r")

ds_ARMBE2D_05 = addfile("/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110501.000000.nc","r")
ds_ARMBE2D_06 = addfile("/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110601.000000.nc","r")
ds_ARMBE2D_07 = addfile("/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110701.000000.nc","r")
ds_ARMBE2D_08 = addfile("/home/qin5/Data/ARMBE2DGRID/sgparmbe2dgridX1.c1.20110801.000000.nc","r")

str_var = "sensible_heat_flux"

var05 = ds_ARMBE2D_05->$str_var$
var06 = ds_ARMBE2D_06->$str_var$
var07 = ds_ARMBE2D_07->$str_var$
var08 = ds_ARMBE2D_08->$str_var$

var056 = array_append_record(var05,var06,0)
var078 = array_append_record(var07,var08,0)
var = array_append_record(var056,var078,0)

printVarSummary(var05)
printVarSummary(var056)
printVarSummary(var)

time1 = f1->time
time2 = var&time

print(time1(2942))

asciiwrite("./08_a_time1.mask.txt", Calendar(time1))
asciiwrite("./08_a_time2.pr05678.ARMBE2D.txt", Calendar(time2))
;;; the ARMBE2D has small deviations from exact 00 minutes, hard to tell this way.

;------ devise a time yourself so that you could check which hours are missing in the time of the MCS_mask
time_new = new(2952,integer)
time_new@units = "Seconds since 1970-1-1 0:00:00 0:00"
time_new@long_name = "Base time in Epoch"

time_new = ispan(1304208000,1314831600 ,3600)
asciiwrite("./08_a_time3.new.txt", Calendar(time_new))

;=========================
;the following hours are missing:
; 14:00Z 12 Jul 2011
;16:00Z 12 Jul 2011
;10:00Z 14 Jul 2011
; 13:00Z 11 Aug 2011
; 05:00Z 16 Aug 2011
; 05:00Z 23 Aug 2011
; 05:00Z 26 Aug 2011
; 05:00Z 27 Aug 2011
; 05:00Z 29 Aug 2011

time_new_check1 = time_new(1-1:1742-1)
time_new_check2 = time_new(1744-1)
time_new_check3 = time_new(1746-1:1786-1)
time_new_check4 = time_new(1788-1:2461-1)
time_new_check5 = time_new(2463-1:2573-1)
time_new_check6 = time_new(2575-1:2741-1)
time_new_check7 = time_new(2743-1:2813-1)
time_new_check8 = time_new(2815-1:2837-1)
time_new_check9 = time_new(2839-1:2885-1)
time_new_check10 = time_new(2887-1:)

time_new_revise12 = array_append_record(time_new_check1,time_new_check2,0)
time_new_revise34 = array_append_record(time_new_check3,time_new_check4,0)
time_new_revise56 = array_append_record(time_new_check5,time_new_check6,0)
time_new_revise78 = array_append_record(time_new_check7,time_new_check8,0)
time_new_revise910 = array_append_record(time_new_check9,time_new_check10,0)
time_new_revise1234 = array_append_record(time_new_revise12,time_new_revise34,0)
time_new_revise5678 = array_append_record(time_new_revise56,time_new_revise78,0)
time_new_revise1_8 = array_append_record(time_new_revise1234,time_new_revise5678,0)
time_new_revise1_10 = array_append_record(time_new_revise1_8,time_new_revise910,0)

asciiwrite("./08_a_time_new_revise.txt", Calendar(time_new_revise1_10))
;check diff 08_a_time1.mask.txt 08_a_time_new_revise.txt would produce nothing, then it's good to go

;;process var0567 variable (remove hours to make it consistent with MCS_mask obs data) and save as .nc files
var_check1 = var(1-1:1742-1,:,:)
var_check2 = var(1744-1,:,:)
var_check2_temp = new((/1,15,17/),float)
var_check2_temp(0,:,:) = var_check2
printVarSummary(var_check2)
printVarSummary(var_check2_temp)

var_check3 = var(1746-1:1786-1,:,:)
var_check4 = var(1788-1:2461-1,:,:)
var_check5 = var(2463-1:2573-1,:,:)
var_check6 = var(2575-1:2741-1,:,:)
var_check7 = var(2743-1:2813-1,:,:)
var_check8 = var(2815-1:2837-1,:,:)
var_check9 = var(2839-1:2885-1,:,:)
var_check10 = var(2887-1:,:,:)

;var_revise12 = array_append_record(var_check1,var_check2,0)
var_revise12 = array_append_record(var_check1,var_check2_temp,0)
var_revise34 = array_append_record(var_check3,var_check4,0)
var_revise56 = array_append_record(var_check5,var_check6,0)
var_revise78 = array_append_record(var_check7,var_check8,0)
var_revise910 = array_append_record(var_check9,var_check10,0)
var_revise1234 = array_append_record(var_revise12,var_revise34,0)
var_revise5678 = array_append_record(var_revise56,var_revise78,0)
var_revise1_8 = array_append_record(var_revise1234,var_revise5678,0)
var_revise1_10 = array_append_record(var_revise1_8,var_revise910,0)

;------
;-----
out_dir = "/home/qin5/Data/ARMBE2DGRID/OBS_MCS_mask_consistency/"
system("rm -f " +out_dir+"sgparmbe2dgridX1.c1.201105_08.time_revise."+str_var+".nc")   ; remove any pre-existing file
ncdf = addfile(out_dir+"sgparmbe2dgridX1.c1.201105_08.time_revise."+str_var+".nc" ,"c")  ; open output netCDF file
 filedimdef(ncdf,"time",-1,True)

ncdf->$str_var$  = var_revise1_10





end
