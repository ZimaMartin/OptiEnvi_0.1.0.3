#!/usr/bin/env python3

###
### This file is generated automatically by SALOME v9.9.0 with dump python functionality
###

import sys
#import salome
from ..extFunctions import timer



def gen_mesh(h_1,w_1,h_2,w_2,L,path_mesh):
	
    t = timer("Mesh build time")
    t.start()
    import os
    import salome	
    import salome_notebook
    
    	
    path_case = os.path.dirname(os.path.realpath(sys.argv[0]))
    
    salome.salome_init()
    
    notebook = salome_notebook.NoteBook()
    sys.path.insert(0, path_mesh)
    
    
    ###
    ### SHAPER component
    ###
       
    from salome.shaper import model
    
    model.begin()
    partSet = model.moduleDocument()
    
    ### Create Part
    Part_1 = model.addPart(partSet)
    Part_1_doc = Part_1.document()
    model.addParameter(Part_1_doc, "h_1", str(h_1))
    model.addParameter(Part_1_doc, "w_1", str(w_1))
    model.addParameter(Part_1_doc, "L",   str(L))
    model.addParameter(Part_1_doc, "h_2", str(h_2))
    model.addParameter(Part_1_doc, "w_2", str(w_2))
    
    ### Create Plane
    Plane_4 = model.addPlane(Part_1_doc, model.selection("FACE", "PartSet/XOY"), "L", False)
    
    ### Create Sketch
    Sketch_1 = model.addSketch(Part_1_doc, model.defaultPlane("XOY"))
    
    ### Create SketchLine
    SketchLine_1 = Sketch_1.addLine(25, 0, 0, 0)
    
    ### Create SketchProjection
    SketchProjection_1 = Sketch_1.addProjection(model.selection("VERTEX", "PartSet/Origin"), False)
    SketchPoint_1 = SketchProjection_1.createdFeature()
    Sketch_1.setCoincident(SketchLine_1.endPoint(), SketchPoint_1.result())
    
    ### Create SketchLine
    SketchLine_2 = Sketch_1.addLine(0, 0, 0, 50)
    
    ### Create SketchLine
    SketchLine_3 = Sketch_1.addLine(0, 50, 25, 50)
    
    ### Create SketchLine
    SketchLine_4 = Sketch_1.addLine(25, 50, 25, 0)
    Sketch_1.setCoincident(SketchLine_4.endPoint(), SketchLine_1.startPoint())
    Sketch_1.setCoincident(SketchLine_1.endPoint(), SketchLine_2.startPoint())
    Sketch_1.setCoincident(SketchLine_2.endPoint(), SketchLine_3.startPoint())
    Sketch_1.setCoincident(SketchLine_3.endPoint(), SketchLine_4.startPoint())
    Sketch_1.setHorizontal(SketchLine_1.result())
    Sketch_1.setVertical(SketchLine_2.result())
    Sketch_1.setHorizontal(SketchLine_3.result())
    Sketch_1.setVertical(SketchLine_4.result())
    Sketch_1.setLength(SketchLine_4.result(), "h_1")
    Sketch_1.setLength(SketchLine_3.result(), "w_1")
    model.do()
    
    ### Create Sketch
    Sketch_2 = model.addSketch(Part_1_doc, model.selection("FACE", "all-in-Plane_1"))
    
    ### Create SketchLine
    SketchLine_5 = Sketch_2.addLine(25, 0, 0, 0)
    
    ### Create SketchProjection
    SketchProjection_2 = Sketch_2.addProjection(model.selection("VERTEX", "PartSet/Origin"), False)
    SketchPoint_2 = SketchProjection_2.createdFeature()
    Sketch_2.setCoincident(SketchLine_5.endPoint(), SketchPoint_2.result())
    
    ### Create SketchLine
    SketchLine_6 = Sketch_2.addLine(0, 0, 0, 50)
    
    ### Create SketchLine
    SketchLine_7 = Sketch_2.addLine(0, 50, 25, 50)
    
    ### Create SketchLine
    SketchLine_8 = Sketch_2.addLine(25, 50, 25, 0)
    Sketch_2.setCoincident(SketchLine_8.endPoint(), SketchLine_5.startPoint())
    Sketch_2.setCoincident(SketchLine_5.endPoint(), SketchLine_6.startPoint())
    Sketch_2.setCoincident(SketchLine_6.endPoint(), SketchLine_7.startPoint())
    Sketch_2.setCoincident(SketchLine_7.endPoint(), SketchLine_8.startPoint())
    Sketch_2.setHorizontal(SketchLine_5.result())
    Sketch_2.setVertical(SketchLine_6.result())
    Sketch_2.setHorizontal(SketchLine_7.result())
    Sketch_2.setVertical(SketchLine_8.result())
    Sketch_2.setLength(SketchLine_7.result(), "w_2")
    Sketch_2.setLength(SketchLine_8.result(), "h_2")
    model.do()
    
    ### Create Pipe
    Pipe_1 = model.addPipe(Part_1_doc, [model.selection("COMPOUND", "all-in-Sketch_1"), model.selection("COMPOUND", "all-in-Sketch_2")], model.selection("EDGE", "PartSet/OZ"), [])
    
    ### Create Export
    Export_1 = model.exportToXAO(Part_1_doc, '/tmp/shaper_3r6pminu.xao', model.selection("SOLID", "Pipe_1_1"), 'XAO')
    
    model.end()
    
    ###
    ### SHAPERSTUDY component
    ###
    
    model.publishToShaperStudy()
    import SHAPERSTUDY
    Pipe_1_1, = SHAPERSTUDY.shape(model.featureStringId(Pipe_1))
    ###
    ### GEOM component
    ###
    
    import GEOM
    from salome.geom import geomBuilder
    import math
    import SALOMEDS
    
    
    geompy = geomBuilder.New()
    
    (imported, Pipe, [], [], []) = geompy.ImportXAO("/tmp/shaper_3r6pminu.xao")
    walls = geompy.CreateGroup(Pipe, geompy.ShapeType["FACE"])
    geompy.UnionIDs(walls, [3, 13, 20, 27])
    inlet = geompy.CreateGroup(Pipe, geompy.ShapeType["FACE"])
    geompy.UnionIDs(inlet, [31])
    outlet = geompy.CreateGroup(Pipe, geompy.ShapeType["FACE"])
    geompy.UnionIDs(outlet, [33])
    [walls, inlet, outlet] = geompy.GetExistingSubObjects(Pipe, False)
    geompy.addToStudy( Pipe, 'Pipe' )
    geompy.addToStudyInFather( Pipe, walls, 'wall' )
    geompy.addToStudyInFather( Pipe, inlet, 'inlet' )
    geompy.addToStudyInFather( Pipe, outlet, 'outlet' )
    
    ###
    ### SMESH component
    ###
    
    import  SMESH, SALOMEDS
    from salome.smesh import smeshBuilder
    
    smesh = smeshBuilder.New()
    #smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:
                                 # multiples meshes built in parallel, complex and numerous mesh edition (performance)
    
    Mesh = smesh.Mesh(Pipe,'Mesh')
    NETGEN_1D_2D_3D = Mesh.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
    NETGEN_3D_Parameters_1 = NETGEN_1D_2D_3D.Parameters()
    NETGEN_3D_Parameters_1.SetMaxSize( 5 )
    NETGEN_3D_Parameters_1.SetMinSize( 1 )
    NETGEN_3D_Parameters_1.SetSecondOrder( 0 )
    NETGEN_3D_Parameters_1.SetOptimize( 1 )
    NETGEN_3D_Parameters_1.SetFineness( 2 )
    NETGEN_3D_Parameters_1.SetChordalError( -1 )
    NETGEN_3D_Parameters_1.SetChordalErrorEnabled( 0 )
    NETGEN_3D_Parameters_1.SetUseSurfaceCurvature( 1 )
    NETGEN_3D_Parameters_1.SetFuseEdges( 1 )
    NETGEN_3D_Parameters_1.SetQuadAllowed( 1 )
    NETGEN_3D_Parameters_1.SetCheckChartBoundary( 3 )
    
    NETGEN_3D_Parameters_1.SetLocalSizeOnShape(walls, 2)
    
    
    walls_1 = Mesh.GroupOnGeom(walls,'walls',SMESH.FACE)
    inlet_1 = Mesh.GroupOnGeom(inlet,'inlet',SMESH.FACE)
    outlet_1 = Mesh.GroupOnGeom(outlet,'outlet',SMESH.FACE)
    isDone = Mesh.Compute()
    [ walls_1, inlet_1, outlet_1 ] = Mesh.GetGroups()
    aCriteria = []
    aCriterion = smesh.GetCriterion(SMESH.ALL,SMESH.FT_BelongToGeom,SMESH.FT_Undefined,Pipe)
    aCriteria.append(aCriterion)
    NETGEN_3D_Parameters_1.SetQuadAllowed( 0 )
    NETGEN_3D_Parameters_1.SetCheckChartBoundary( 3 )
    isDone = Mesh.Compute()
    [ walls_1, inlet_1, outlet_1 ] = Mesh.GetGroups()
    

    try:
        Mesh.ExportUNV( path_case + path_mesh +'/mesh_l' + str(L) + '.unv')
        pass
    except:
        print('ExportUNV() failed. Invalid file name?')
    
    
    ## Set names of Mesh objects
    smesh.SetName(inlet_1, 'inlet')
    smesh.SetName(outlet_1, 'outlet')
    smesh.SetName(walls_1, 'walls')
    smesh.SetName(NETGEN_1D_2D_3D.GetAlgorithm(), 'NETGEN 1D-2D-3D')
    smesh.SetName(Mesh.GetMesh(), 'Mesh')
    smesh.SetName(NETGEN_3D_Parameters_1, 'NETGEN 3D Parameters_1')
    
    
    
    if salome.sg.hasDesktop():
      	salome.sg.updateObjBrowser()
      
    t.stop()

	  

