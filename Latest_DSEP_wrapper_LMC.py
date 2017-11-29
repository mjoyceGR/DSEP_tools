#!/usr/bin/env python
import numpy as np
import subprocess
import sys
import codecs
#my module
import generate_prems as GP 
import isochrone_suites2 as IS #mod 8/22/17: isochrone_suites --> isochrone_suites2
import time as time


####################################################
#
# Run-time parameters
#
# ALPHA CEN A ONLY 11/5/17
#
# best-fit alpha cen A model without overshoot:
# 	alpha = 1.45
#	Z = 0.025
#	Y = 0.29
#	age = 3.3 Gyr
#
#####################################################
config=True
 
NMOD=9999

rundir='run'
model_dir='alpha_cen'

model_ID_head='acen.ovs.ML'

shell_file='run_alphacen_ovs.sh'
contfile='cont_alphacen.nml'



#######################################
#
# Make input models
#
#######################################
cont_file = "/home/meridith/dsep3/nml/"+contfile
run_file = "/home/meridith/dsep3/"+rundir+"/" +shell_file

solar_ML = 1.9258 ##new as of 4/5/17
aFe=0.0

CMIXLA_grid=np.arange(1.35,1.95,0.05)
Zin_list=np.arange(0.015,0.035,0.005)
Yin_list=np.arange(0.25,0.35,0.01)

if config:
	print "using:\n", contfile, "\n", shell_file, "\n"
	print "ML sampled: ", CMIXLA_grid
	print "Z sampled: ", Zin_list
	print "Y sampled: ", Yin_list
else:
	starting_mass=1100
	ending_mass=1120
	interval=10
	for i in range(len(Zin_list)):
		Z= Zin_list[i]
		for j in range(len(CMIXLA_grid)):
			CMIXLA=CMIXLA_grid[j]
			for k in range(len(Yin_list)):
				Y=Yin_list[k]		
				model_ID=model_ID_head+str(CMIXLA)+'.Z'+str(Z)+'.Y'+str(Y)
				print 'model_ID: ', model_ID
				GP.make_prems_model(CMIXLA, Z, Y, aFe, starting_mass, ending_mass, model_dir, interval, model_ID)
##############################################################
#
# Run DSEP to get isochrone files
#
#############################################################
	print "using:\n", contfile, "\n", shell_file, "\n"
	prems_dir=model_dir
	run=run_file.split('/dsep3/run/')[1]
	massgrid=[111.0]

	i=0
	j=0
	k=0
	m=0
	for i in range(len(massgrid)):
		mass = str(massgrid[i])
		for j in range(len(CMIXLA_grid)):
			CMIXLA=CMIXLA_grid[j]
			for k in range(len(Zin_list)):
				Z=Zin_list[k]
				for m in range(len(Yin_list)):
					Y=Yin_list[m]
					print mass, CMIXLA, Z, Y
					time.sleep(2)
			 		model_ID=model_ID_head+str(CMIXLA)+'.Z'+str(Z)+'.Y'+str(Y)
					IS.update_cont(cont_file, CMIXLA, Z, Y, NMOD) ## updated to pass NMOD 11/7/17
					if float(mass) < 100.0:
						out_iso_name ="m0"+mass+"."+model_ID
					else:
						out_iso_name = "m"+mass+"."+model_ID 
					IS.update_shell(run_file, out_iso_name, out_iso_name, prems_dir)
					subprocess.call("./"+run, shell=True)
