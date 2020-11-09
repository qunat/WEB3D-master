#!/usr/bin/env python

#
#Copyright 2009-2014 Thomas Paviot (tpaviot@gmail.com)
##
##This file is part of pythonOCC.
##
##pythonOCC is free software: you can redistribute it and/or modify
##it under the terms of the GNU Lesser General Public License as published by
##the Free Software Foundation, either version 3 of the License, or
##(at your option) any later version.
##
##pythonOCC is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Lesser General Public License for more details.
##
##You should have received a copy of the GNU Lesser General Public License
##along with pythonOCC.  If not, see <http://www.gnu.org/licenses/>.

from OCC.Display.WebGl import x3dom_renderer
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRepTools import breptools_Read
from OCC.Extend.DataExchange import read_step_file


from OCC.Display.SimpleGui import init_display
from OCC.Core.TopoDS import topods_Edge
from OCC.Extend.DataExchange import read_step_file
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Display.OCCViewer import rgb_color
from OCC.Core.AIS import AIS_ColoredShape
from random import random
from OCC.Core.AIS import AIS_Shape
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.Quantity import Quantity_Color
from OCC.Core.Quantity import Quantity_Color,Quantity_TOC_RGB
from OCC.Display.SimpleGui import init_display
from OCC.Display.OCCViewer import Viewer3d
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox


the_shape = read_step_file('SFU01610-4.step')
print(type(the_shape))
# loads brep shape
#cylinder_head = TopoDS_Shape()
#builder = BRep_Builder()
#breptools_Read(cylinder_head, './models/cylinder_head.brep', builder)
# render cylinder head in x3dom
my_renderer = x3dom_renderer.X3DomRenderer(path="d:\\123")
ais_shape=AIS_ColoredShape(the_shape)

#display.DisplayShape(my_box,update=True)
#display.Context.Display(cube,True)
for e in TopologyExplorer(the_shape).shells():
        rnd_color = (random(), random(), random())
        ais_shape.SetCustomColor(e, rgb_color(random(), random(), random()))
        my_renderer.DisplayShape(e,export_edges=True,color=(random(), random(), random()))

my_renderer.render()
