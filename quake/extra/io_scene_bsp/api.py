from collections import namedtuple

import numpy as np

from .quake.bsp import Bsp as QBsp

VertexCoordinate = namedtuple('VertexCoordinate', ['x', 'y', 'z'])
UVTextureMapCoordinate = namedtuple('UVTextureCoordinate', ['u', 'v'])
UVLightMapCoordinate = namedtuple('UVLightmapCoordinate', ['u', 'v'])
TextureMap = namedtuple('TextureMap', ['size', 'pixels'])
LightMap = namedtuple('LightMap', ['size', 'luxels'])

_texture_cache = {}
_vertex_cache = {}


class Face(object):
    def __init__(self, face, bsp_file):
        self._face = face
        self._bsp_file = bsp_file

    @property
    def texture(self):
        try:
            return self._texture
        except AttributeError:
            f = self._face
            b = self._bsp_file
            texture_info = b.texture_infos[f.texture_info]
            miptex_id = texture_info.miptexture_number

            try:
                return _texture_cache[miptex_id]

            except KeyError:
                miptex = b.miptextures[miptex_id]
                w = miptex.width
                h = miptex.height
                pixels = miptex.pixels[:w*h]
                _texture_cache[miptex_id] = TextureMap((w, h), pixels)

            return _texture_cache[miptex_id]

    @property
    def lightmap(self):
        pass

    @property
    def texture_uvs(self):
        try:
            return self._texture_uvs

        except AttributeError:
            f = self._face
            b = self._bsp_file
            texture_info = b.texture_infos[f.texture_info]
            s = texture_info.s
            ds = texture_info.s_offset
            t = texture_info.t
            dt = texture_info.t_offset
            w, h = self.texture.size
            uvs = [((np.dot(v, s) + ds) / w, -(np.dot(v, t) + dt) / h) for v in self.vertexes]
            uvs = [UVTextureMapCoordinate(*uv) for uv in uvs]
            self._texture_uvs = uvs

        return self._texture_uvs

    @property
    def lightmap_uvs(self):
        pass

    @property
    def vertexes(self):
        try:
            return self._vertexes

        except AttributeError:
            f = self._face
            b = self._bsp_file
            edges = b.surf_edges[f.first_edge:f.first_edge+f.number_of_edges]

            verts = []
            for e in edges:
                vs = b.edges[abs(e)].vertexes
                v0, v1 = vs if e > 0 else reversed(vs)

                if len(verts) == 0:
                    verts.append(v0)

                if v1 != verts[0]:
                    verts.append(v1)

            result = []
            for v in reversed(verts):
                try:
                    vertex = _vertex_cache[v]

                except KeyError:
                    vertex = VertexCoordinate(*b.vertexes[v][:])
                    _vertex_cache[v] = vertex

                result.append(vertex)

            self._vertexes = result

        return self._vertexes

    @property
    def normal(self):
        pass


class Bsp(QBsp):
    def open(file, mode='r'):
        bsp = QBsp.open(file, mode)
        bsp.ffaces = [Face(f, bsp) for f in bsp.faces]

        return bsp
