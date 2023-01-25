import subprocess
from subprocess import call, PIPE
import shutil
import os
import time
from app.extFunctions import timer, process_check 

class caseBuild():
	def __init__(self,dir,count,prms,stopAt,solver,control=False):
	
		self.count = count
		self.solver = solver
		def folder_name(count):
			if self.count < 10: 					  
				folder_name ='/run00' + str(count)
			elif self.count > 10 and self.count < 100:
				folder_name ='/run0'  + str(count)
			else: 							          folder_name ='/run'   + str(count)
			return folder_name
		
		self.path_project = dir
		self.path_onMaster_runs = dir + folder_name(self.count)
		self.path_onMaster_init = dir + '/_initial'	
		self.stopAt = stopAt
		self.prms = prms
		self.residualsPosprocess = ['Ux_final', 'Uy_final', 'Uz_final', 'p_rgh_final', 'h_final','k_final', 'omega_final'] 

			
	def folder_create(self, clear=True):
		'''create folder for case storing / remove subdirectories and files in existing folders'''
		
		
		if not os.path.exists(self.path_onMaster_runs):
			os.mkdir(self.path_onMaster_runs)
		elif clear:
			os.system("rm -r " + self.path_onMaster_runs + "/*")
			
	def openFoam_import(self):
		'''make archive, move to case dir and unpack'''
		
		print(f'Preparing structure of the Run{self.count} ...')	
		
		shutil.make_archive('export', 'zip' , self.path_onMaster_init)
		shutil.move('export.zip', self.path_onMaster_runs)
		shutil.unpack_archive(self.path_onMaster_runs + '/' + 'export.zip' , self.path_onMaster_runs )
		os.system("rm " + self.path_onMaster_runs + "/export.zip")
		
		print(f'... end')
		
	def openFoam_BCs(self):
		'''assign boundary conditions to the case'''
		
		with open(self.path_onMaster_runs + '/boundaryConditions', 'w+') as f:
			for i in self.prms:
				f.write(f'{i} 	{self.prms[i]};\n')

		
	def openFoam_runControl(self):
		'''stops run after no_iterations. When is assigned True, it continues, when False terminates'''
		
		with open(self.path_onMaster_runs + '/system/controlDict', 'r') as f:
			data = f.readlines()
		data[20] = f'endTime         {self.stopAt};\n'
		data[16] = f'application     {self.solver};\n'
		with open(self.path_onMaster_runs + '/system/controlDict', 'w') as f:	
			f.writelines(data)
	
	def openFoam_plotResiduals(self,iput=True):
		if iput:
			with open(self.path_onMaster_runs + '/Allrun-parallel', 'a') as f:
				f.write('gnuplot resPlot.txt -\n')
		
		
	
		
	def openFoam_run(self):

		
		cmd = 'chmod 755 '  + self.path_onMaster_runs
		cmd2 = ['/Allclean','/Allrun.pre','/Allrun-parallel']
		
		try:
			for cmd2_part in cmd2: 
				subprocess.Popen(cmd + cmd2_part, shell=True)
				cmd3 = 'sh ' +  self.path_onMaster_runs + cmd2_part	
				run_call = subprocess.Popen(cmd3, shell=True, stdout=PIPE)
				print(f'Processing {cmd2_part}')
				
				time.sleep(30)
			print(f'The Run{self.count} is solved... ')	
			
		except: print(f'Can not run the case')
		
	def openFoam_runControl_automatic(self):
		'''untill the process (solver) is running'''
		
		process = True
		process_name = self.solver

		time.sleep(10)
		while process:
			time.sleep(5)			
			process = process_check(process_name)
		
		#try:
		#	subprocess.Popen(f'reconstructPar -case {self.path_onMaster_runs}', shell=True)
		#	subprocess.Popen(f'{self.solver} -postProcess -func yPlus -case {self.path_onMaster_runs}', shell=True)
		#except: print('reconstructPar and yPlus not resolved')

		print(f'...end')
	def postprocess_openFoamExport(self,toFile = False):
    
		def importData(dir):
			with open(dir) as file:
				for line in file:
					pass
					
			p      = float(line.split()[1])
			T      = float(line.split()[2])
			try: htCoef = float(line.split()[3])
			except: htCoef = False
			return [p, T, htCoef]
    
    

		path = [self.path_onMaster_runs + "/postProcessing/calculation_outlet/0/surfaceFieldValue.dat",
			self.path_onMaster_runs + "/postProcessing/calculation_inlet/0/surfaceFieldValue.dat",
			self.path_onMaster_runs + "/postProcessing/calculation_walls/0/surfaceFieldValue.dat"
				]
       
       
		s_In = importData(path[0])
		s_Out= importData(path[1])
		s_Wall=importData(path[2])
		
		delta_p = abs(s_In[0]-s_Out[0])
		delta_T = abs(s_In[1]-s_Out[1])
		htCoef  = abs(s_Wall[2])
		
		f_D = delta_p * 2 * self.prms["Dh"]  / ( self.prms["rho"] * self.prms["L"] * ( self.prms["m_dotVol_in"] / self.prms["A"])**2 )
		
		Nu  = htCoef * self.prms["Dh"] / self.prms["kappaAir"]
		j_fact= Nu / (self.prms["Re"] * 0.7**(1/3))
		 
		
		
		if toFile:
			if self.count == 1:
				with open(self.path_project + '/' + 'output_file', 'w') as f:	
					f.write('Re  ; delta_p ; f ; delta_T ; Nu ; j_fact\n')
				
			with open(self.path_project + '/' + 'output_file', 'a') as f:	
				f.write(f'{self.prms["Re"]} ; {delta_p} ; {f_D} ; {delta_T} ; {Nu} ; {j_fact}\n')
				
			print(f'Postprocess data wrote to {self.path_project}/output_file')
		return [delta_p, delta_T]
		
		
	def postprocess_openFoam_residuals(self, data_save, cols=True):
		
		import pandas as pd

		if cols:
			cols = self.residualsPosprocess
		dir = self.path_onMaster_runs + "/postProcessing/solverInfo/0/"
		dir_dat = dir +"solverInfo.dat"
		
		with open(dir_dat , 'r') as f:
			data = f.read()
			data = data.replace('#',' ')
		with open(dir_dat, 'w') as f:    
			f.write(data)
		
		data = pd.read_csv(dir_dat ,skiprows=1, delimiter='\s+',usecols=cols)
		data.iloc[:, 1:]
		data.shift(+1,axis=1)
        
        
		data_save.append(data)
		return data_save 

					
					
	def postprocess_openFoam_residuals_plots(self,data_save,cols=True):	
			
		import matplotlib.pyplot as plt
		import numpy as np
		
		if cols:
			cols = self.residualsPosprocess
		
		
		len_1 = len(data_save[0]['Ux_final'])
		len_2 = len(data_save)
		
		a=np.empty((len_1,len_2))  
		b=np.empty((len_1,3))  
		c=np.empty((len_1,1))  
		for column in cols:
			for i in range(len_1):
				for j in range(len_2):
    
    
					a[i,j] = (data_save[j][column][i])
    

				c[i,0] = i

				b[i,2] = np.mean(a[i,:])
				b[i,0] = abs(max(a[i,:]) - np.mean(a[i,:]))
				b[i,1] = abs(min(a[i,:]) - np.mean(a[i,:]))

			fig1, ax1 = plt.subplots()    


			ax1.errorbar(c,b[:,2],yerr=[b[:,1],b[:,0]])
			ax1.set_title(column)
			ax1.set_yscale('log')
			fig1.savefig(self.path_project + "/residuals_" + column + ".png",dpi=600)




