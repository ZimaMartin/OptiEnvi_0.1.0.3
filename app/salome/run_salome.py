#!/usr/bin/env python3


import os
from def_salome import gen_mesh



L = 500
h_1 = 50
w_1 = 50
h_2 = 50
w_2 = 50
path_onMaster_export = '/app/openFoam/_initial/geometry'


gen_mesh(h_1,w_1,h_2,w_2,L[i],path_onMaster_export)
