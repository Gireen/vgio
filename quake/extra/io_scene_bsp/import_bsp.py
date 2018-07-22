import bpy
import bmesh
import math
import numpy
from collections import namedtuple
from mathutils import Matrix, Vector

from .quake.bsp import is_bspfile
from .api import Bsp


LightMapFaceInfo = namedtuple('LightMapStruct', ['size', 'pixels', 'uvs'])


def load(operator, context, filepath='',
         global_scale=1.0,
         use_worldspawn_entity=True,
         use_brush_entities=True,
         use_point_entities=True):

    if not is_bspfile(filepath):
        operator.report(
            {'ERROR'},
            '{} not a recognized BSP file'.format(filepath)
        )
        return {'CANCELLED'}

    b = Bsp.open(filepath)

    me = bpy.data.meshes.new('worldspawn')
    bm = bmesh.new()
    uv_layer = bm.loops.layers.uv.new('UVMap')

    bvert_cache = {}

    global_matrix = Matrix.Scale(global_scale, 4)

    def create_vertex(vertex):
        try:
            return bvert_cache[vertex]
        except KeyError:
            bvert = bm.verts.new(vertex[:])
            bvert.co = global_matrix * bvert.co
            bvert_cache[vertex] = bvert

        return bvert_cache[vertex]

    for face in b.ffaces:
        bverts = [create_vertex(v) for v in face.vertexes]
        bm.verts.ensure_lookup_table()
        bface = bm.faces.new(bverts)
        for i, loop in enumerate(bface.loops):
            loop[uv_layer].uv = face.texture_uvs[i]

    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new('worldspawn', me)
    bpy.context.scene.objects.link(ob)

    return {'FINISHED'}