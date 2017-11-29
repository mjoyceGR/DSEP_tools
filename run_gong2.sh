#! /bin/bash
#LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/free_eos-2.2.1/install_dir/lib

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/meridith/free_eos-2.2.1/lib
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/free_eos-2.2.1/lib
ldd /home/meridith/dsep3/dsepX/dsepX

local=$HOME/dsep3
nml=$local/nml
out=$local/out
prog=$local/dsepX
zams=$local/zams
prems=$local/prems
opac=$local/opac
atm=$local/surfBC
opal=$opac/OPAL
phx=$opac/phoenix
bcphx=$atm/phoenix/GS98
bckur=$atm/atmk
out_meridith=$local/run/out_meridith/alphaCen

outname=m093.0.acen.gong.ML1.81.Z0.026.Y0.28

rm fort.*

 ln -s $nml/phys_gong2.nml		fort.13
 ln -s $nml/cont_gong2.nml                    fort.14 

#input opacities/boundry conditions; Fergson low T specified in CONTROL nml
 ln -s $opac/FERMI.TAB                  fort.15
 ln -s $bckur/atmk1990p00.tab           fort.38
 ln -s $opal/GS98hz                     fort.48 
#Phoenix boundary conditions, code picks correct Z, multipe ones 
#to allow for correct BC when rescaling

 ln -s $bcphx/z_p0d0.afe_p0d0.dat       fort.95
 ln -s $bcphx/z_m0d5.afe_p0d0.dat       fort.96
 ln -s $bcphx/z_m0d7.afe_p0d0.dat       fort.97
 ln -s $bcphx/z_m1d0.afe_p0d0.dat       fort.98
 ln -s $bcphx/z_m1d5.afe_p0d0.dat       fort.99

#input model
 ln -s $prems/alpha_cen/m093.0.acen.gong.ML1.81.Z0.026.Y0.28 fort.12

#output
 ln -s $out/$outname.track                  fort.19
 ln -s $out/$outname.short                  fort.20

#PULSE output
 ln -s $out_meridith/$outname.fpmod					fort.24
 ln -s $out_meridith/$outname.fpenv					fort.25
 ln -s $out_meridith/$outname.fpatm					fort.26

 ln -s $out_meridith/$outname.iso		    fort.37
 ln -s $out/$outname.last                   fort.11

time $prog/dsepX













































