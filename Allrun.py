#!/usr/bin/env python3



#-------------------------  RUN  --------------------------------------------#

from API.openFoamAPI import caseBuild
from app.extFunctions import timer
from dataclasses import dataclass
import numpy as np
from CoolProp.CoolProp import PropsSI

#------------------ BOUNDARY CONDITIONS -----------------#


Re=       np.array([1e4, 2e4, 3e4, 4e4,6e4,1e5  ])
T_in= 	  np.array([400  ,400,400,400,400,400  ])
T_wall=   np.array([600  ,600,600,600,600,600  ])
heatFlux= np.array([1e3 ,1e3,1e3,1e3,1e3,1e3 ])
p_in= 	  np.array([3e5,3e5,3e5,3e5,3e5,3e5])
R=  287.05
Dh= 30e-3
L = 0.4


A        = np.pi * Dh **2 / 4
nu       = PropsSI('V', 'T', T_in, 'P', p_in, 'Air')
kappaAir = PropsSI('conductivity', 'T', T_in, 'P', p_in, 'Air')
rho      = p_in / (R * T_in)
m_dot_in = Re * nu * A / Dh
m_dotVol_in = m_dot_in / rho


#------------ DESTINATIONS AND SOLVER PREREQ ------------#

path_onMaster = 'app/openFoam'


total_iter_no = 20		
solver        = 'buoyantSimpleFoam'


count = 0 
data_save = []



	
t0 = timer('Whole study')
t0.start()

for i in range(2):
	t = timer('Run ' + str(i+1))
	t.start()
	count += 1 
		

	bcs = {'Re':Re[i], 'T_in':T_in[i],'heatFlux':heatFlux[i],'p_in':p_in[i],'R':R,'Dh':Dh ,'m_dot_in':m_dot_in[i],'rho':rho[i], 'nu':nu[i],'A':A,'L':L, 'm_dotVol_in':m_dotVol_in[i], 'kappaAir':kappaAir[i],'T_wall':T_wall[i]}



	case = caseBuild(	path_onMaster, 
				count,
				bcs,
				total_iter_no,
				solver
				)
	
	
	case.folder_create ()
	case.openFoam_import()
	case.openFoam_BCs ()
	case.openFoam_runControl()
	case.openFoam_plotResiduals(iput=False)
	case.openFoam_run()
	case.openFoam_runControl_automatic()

	[dp, dT] = case.postprocess_openFoamExport(toFile =True)

        
	
	data_save = case.postprocess_openFoam_residuals(data_save)
		
	t.stop()
    
case.postprocess_openFoam_residuals_plots(data_save)
		
t0.stop()		
		
		
		
		
		

