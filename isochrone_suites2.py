#!/usr/bin/env python
import numpy as np
import subprocess
import sys
import codecs
import re as re
 
#last updated  11/5/17
#IS.update_cont(cont_file, CMIXLA, Z, Y) ## updated to pass Y 8/22/17
def update_cont(cont_file, CMIXLA, Z, Y,NMOD): 
	# Y_BBN=0.245
	# Y_solar=0.28
	Z_solar=0.019
	Zabund = Z
	RSCLZ = str(Z)#+'D0'

	Yabund = Y
	#float(Y_BBN) + ( (float(Y_solar) - float(Y_BBN))/float(Z_solar) ) * float(Zabund)
	Xabund = 1.00-float(Yabund)-float(Zabund)
	RSCLX  =  str(Xabund)


	#finds the previous X and Z values to replace them with new ones
	filef=open(cont_file,"r")
	oldZ=[]
	oldX=[]
	old_alpha=[]
	old_NMOD=[]
	#old_alpha2=[]
	for line in filef:
		line=str(line)
		#print "line: ", line
		if "CMIXLA(1)=" in line:
			old_alpha.append( str(line.split(" CMIXLA(1)=")[1].split("D0")[0]))	
			#print "old_alpha: ", old_alpha 
		# if " CMIXLA(2)=" in line:
		# 	old_alpha2.append( str(line.split(" CMIXLA(2)=")[1].split("D0")[0]))	
		if " RSCLX(1)=" in line:
			oldX.append( str(line.split(" RSCLX(1)=")[1].split("D0")[0]))
		if " RSCLZ(1)=" in line:
			oldZ.append( str(line.split(" RSCLZ(1)=")[1].split("D0")[0]))
		#	 NMODLS(2)=557
		if "NMODLS(2)" in line:
			old_NMOD.append(str(line.split("=")[1]))

	filef.seek(0)	
	oldZ=oldZ[0].strip()
	oldX=oldX[0].strip()
	old_alpha=old_alpha[0].strip()
	old_NMOD=old_NMOD[0].strip()
	#old_alpha2=old_alpha2[0].strip()
	print "old_alpha: ", old_alpha, "\nnew_alpha: ",CMIXLA # old_alpha2,
	#print "old_alpha: ", old_alpha, old_alpha2, "\nnew_alpha: ",CMIXLA
	print "oldZ: ", oldZ, "\toldX: ",oldX, "\nnewZ: ",RSCLZ, "\tnewX: ", RSCLX

	#updates RSCLZ	
	f = codecs.open(cont_file)
	contents = f.read()
	newcontents = contents.replace(' RSCLZ(1)='+str(oldZ),' RSCLZ(1)='+RSCLZ)
	f.seek(0)
	f.close()
	outf=open(cont_file,"w")
	print >>outf, newcontents
	outf.seek(0)
	outf.close()

	#updates RSCLX, computed above
	f2 = codecs.open(cont_file)
	contents = f2.read()
	newcontents = contents.replace(' RSCLX(1)='+str(oldX),' RSCLX(1)='+RSCLX)
	f2.seek(0)
	f2.close()
	outf2=open(cont_file,"w")
	print >>outf2, newcontents
	outf2.seek(0)
	outf2.close()

	#updates ZALEX (should be same as RSCLZ)
	f3 = codecs.open(cont_file)
	contents = f3.read()
	newcontents = contents.replace(' ZALEX='+str(oldZ),' ZALEX='+RSCLZ)
	f3.seek(0)
	f3.close()
	outf3=open(cont_file,"w")
	print >>outf3, newcontents
	outf3.seek(0)
	outf3.close()

	#-----------------------------------------------
	# THIS FUCKING THING now updates ALL CMIXLA(n) for all n, so who knows what the fuck was happening before
	#
	f4 = codecs.open(cont_file)
	contents = f4.read()
	new_value=str(CMIXLA)+"D0"#9999##[200,400]
	def replace_a(matchobj):
		return 'CMIXLA({})={}'.format(matchobj.group(1), new_value)
	newcontents=re.sub(r'CMIXLA\((\d+)\)=([^\s]+)',replace_a, contents)
	f4.seek(0)
	f4.close()
	outf4=open(cont_file,"w")
	print >>outf4, newcontents
	outf4.seek(0)
	outf4.close()

	#updates NMOD 		#	 NMODLS(2)=557
	f5 = codecs.open(cont_file)
	contents = f5.read()
	newcontents = contents.replace(' NMODLS(2)='+str(old_NMOD),' NMODLS(2)='+ str(NMOD))
	f5.seek(0)
	f5.close()
	outf5=open(cont_file,"w")
	print >>outf5, newcontents
	outf5.seek(0)
	outf5.close()


#this one is fine	
def update_shell(run_file, input_model, output_iso_name, prems_dir): #function which takes input model name, output iso name, shell script name
	filef=open(run_file,"r")
	old_iso_name=[]
	old_prems_name=[]
	old_input_model=[]

	for line in filef:
		line=str(line)
		if "outname=" in line:
			old_iso_name.append( str(line.split("=")[1]).strip() )	
		if " ln -s $prems/" in line:
			old_input_model.append( str(line.split("/")[2].split("fort")[0].strip() ) )
			old_prems_name.append( str(line.split('ln -s $prems/')[1].split('/')[0].strip() ) )
	filef.seek(0)	
	print "old_iso_name: ", old_iso_name
	print "old_prems_name: ", old_prems_name, "\nnew prems: ",  prems_dir

	old_iso_name=old_iso_name[0]
	old_input_model=old_input_model[0]
	print "old_input_model: ", old_input_model, "\n new input model: ", input_model
	
	f = codecs.open(run_file)
	contents = f.read()
	newcontents = contents.replace('outname='+str(old_iso_name),'outname='+str(output_iso_name))
	f.seek(0)
	f.close()
	outf=open(run_file,"w")
	print >>outf, newcontents
	outf.seek(0)
	outf.close()


	f1 = codecs.open(run_file)
	contents = f1.read()
	newcontents = contents.replace('ln -s $prems/'+str(old_prems_name)+'/','ln -s $prems/'+str(prems_dir)+'/')
	f1.seek(0)
	f1.close()
	outf1=open(run_file,"w")
	print >>outf1, newcontents
	outf1.seek(0)
	outf1.close()


	f2 = codecs.open(run_file)
	contents = f2.read()
	# ln -s $prems/ML_Apr17/
	print '\n\n$prems/'+str(prems_dir)+'/'+str(old_input_model)
	print '$prems/'+str(prems_dir)+'/'+str(input_model), "\n\n" 

	newcontents = contents.replace('$prems/'+str(prems_dir)+'/'\
		+str(old_input_model),'$prems/'+str(prems_dir)+'/'+str(input_model))
	f2.seek(0)
	f2.close()
	outf2=open(run_file,"w")
	print >>outf2, newcontents
	outf2.seek(0)
	outf2.close()

