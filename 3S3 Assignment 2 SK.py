"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""
        
import Rhino.Geometry as rg
import math

#1.
#compute face normals using rg.Mesh.FaceNormals.ComputeFaceNormals()
#output the vectors to a
m.FaceNormals.ComputeFaceNormals()
faceNormals = m.FaceNormals
a = faceNormals


#2.
#get the centers of each faces using rg.Mesh.Faces.GetFaceCenter()
#store the centers into a list called centers 
#output that list to b
centers = []
for i in range(len(m.Faces)):
    centers.append(m.Faces.GetFaceCenter(i))
b = centers

#3.
#calculate the angle between the sun and each FaceNormal using rg.Vector3d.VectorAngle()
#store the angles in a list called angleList and output it to c

angleList = []
for vec in faceNormals:
    angleList.append(rg.Vector3d.VectorAngle(vec, s))
c = angleList


#4. explode the mesh - convert each face of the mesh into a mesh
#for this, you have to first copy the mesh using rg.Mesh.Duplicate()
#then iterate through each face of the copy, extract it using rg.Mesh.ExtractFaces
#and store the result into a list called exploded in output d


exploded = []
for i in range(len(m.Faces)):
    meshCopy = m.Duplicate()
    meshFace = meshCopy.Faces.ExtractFaces([i])
    exploded.append(meshFace)

d = exploded

breps = []
for i in range(len(exploded)):
    mesh = exploded[i]
    edge = mesh.GetNakedEdges()
    outer_crv = edge[0].ToNurbsCurve()
    sun_angle = angleList[i]
    scale_factor = sun_angle / math.pi
    #print(sun_angle)
    xform = rg.Transform.Scale(centers[i], scale_factor)
    inner_crv = outer_crv.Duplicate()
    inner_crv.Transform(xform)
    loops = []
    loops.append(inner_crv)
    loops.append(outer_crv)
    brep = rg.Brep.CreateFromLoft(loops, rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal, False)
    
    breps.append(brep[0])

Breps = breps
#after here, your task is to apply a transformation to each face of the mesh
#the transformation should correspond to the angle value that corresponds that face to it... 
#the result should be a mesh that responds to the sun position... its up to you!