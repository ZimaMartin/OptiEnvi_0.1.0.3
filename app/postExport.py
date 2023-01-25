#!/usr/bin/env python3




def postprocessData_foamImport():

	def importData(path)
		with open(path) as file:
		
		# last line sample
	    		for line in file:
				pass
		value_out = float(line.split()[1])
		return value_out



	path = ["openFoam/postProcessing/calculation_outlet/0/surfaceFieldValue.dat",
		"openFoam/postProcessing/calculation_inlet/0/surfaceFieldValue.dat"
		]


	p_out = postprocessData_foamImport(path[0])
	p_in  = postprocessData_foamImport(path[1])
	delta_p = abs(p_in-p_out)

	f = open("exportData.dat","x")
	f.write("delta_p	" + str(delta_p))
	f.close()




   




