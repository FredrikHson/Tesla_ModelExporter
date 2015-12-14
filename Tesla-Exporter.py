bl_info = {
    "name": "Tesla (.tesm)",
    "description": "Tesla Game Engine Exporter",
    "author": "Fredrik Hansson",
    "version": (0, 0, 0, 1),
    "location": "File > Import-Export",
    "wiki_url": "",
    "category": "Import-Export"}


import bpy
import math
import struct
from bpy_extras.io_utils import ExportHelper


class NodeTypes:
    Root = 0
    Transform = 1
    Object = 2
    Mesh = 3
    VertexArray = 4
    IndexArray = 5
    Material = 6


class Node:
    size = 0
    type = 0
    numChildren = 0
    def WriteData(self, exporter):
        return

class NodeRoot(Node):
    size = 8
    type = 0


class NodeTransform(Node):
    type = 1
    size = 8 + 16 * 4
    matrix = [1.0, 0.0, 0.0, 0.0,
              0.0, 1.0, 0.0, 0.0,
              0.0, 0.0, 1.0, 0.0,
              0.0, 0.0, 0.0, 1.0]

    def WriteData(self, exporter):
        exporter.WriteFloatArray(self.matrix)


class TeslaExporter(bpy.types.Operator, ExportHelper):
    """Export to Tesla Model"""
    bl_idname = "export_scene.tesm"
    bl_label = "Export Tesla Model"
    filename_ext = ".tesm"

    option_export_selection = bpy.props.BoolProperty(
        name="Export Selection Only", description="Export only selected objects", default=True)

    # helper functions for writing binary data to files
    def WriteDouble(self, val):
        self.file.write(struct.pack('d', val))

    def WriteFloat(self, val):
        self.file.write(struct.pack('f', val))

    def WriteInt8(self, val):
        self.file.write(struct.pack('b', val))

    def WriteUInt8(self, val):
        self.file.write(struct.pack('B', val))

    def WriteInt16(self, val):
        self.file.write(struct.pack('h', val))

    def WriteUInt16(self, val):
        self.file.write(struct.pack('H', val))

    def WriteInt32(self, val):
        self.file.write(struct.pack('i', val))

    def WriteUInt32(self, val):
        self.file.write(struct.pack('I', val))

    def WriteInt64(self, val):
        self.file.write(struct.pack('q', val))

    def WriteUInt64(self, val):
        self.file.write(struct.pack('Q', val))

    def WriteDoubleArray(self, val):
        self.file.write(struct.pack('d' * len(val), *val))

    def WriteFloatArray(self, val):
        self.file.write(struct.pack('f' * len(val), *val))

    def WriteInt8Array(self, val):
        self.file.write(struct.pack('b' * len(val), *val))

    def WriteUInt8Array(self, val):
        self.file.write(struct.pack('B' * len(val), *val))

    def WriteInt16Array(self, val):
        self.file.write(struct.pack('h' * len(val), *val))

    def WriteUInt16Array(self, val):
        self.file.write(struct.pack('H' * len(val), *val))

    def WriteInt32Array(self, val):
        self.file.write(struct.pack('i' * len(val), *val))

    def WriteUInt32Array(self, val):
        self.file.write(struct.pack('I' * len(val), *val))

    def WriteInt64Array(self, val):
        self.file.write(struct.pack('q' * len(val), *val))

    def WriteUInt64Array(self, val):
        self.file.write(struct.pack('Q' * len(val), *val))

    def WriteChars(self, text):
        text = bytes(text, 'utf-8')
        self.file.write(struct.pack('b' * len(text), *text))

    def WriteCharsZeroTerm(self, text):
        text = bytes(text, 'utf-8')
        self.file.write(struct.pack('b' * len(text), *text))
        self.file.write(struct.pack('b', 0))

    def WriteNode(self, node):
        self.WriteUInt32(node.size)
        self.WriteUInt16(node.type)
        self.WriteUInt16(node.numChildren)
        node.WriteData(node,self)

    def execute(self, context):
        self.file = open(self.filepath, "wb")
        self.WriteChars('FULHAX')
        node = NodeTransform
        self.WriteNode(node)
        self.file.close()
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(TeslaExporter.bl_idname, text="Tesla (.tesm)")


def register():
    bpy.utils.register_class(TeslaExporter)
    bpy.types.INFO_MT_file_export.append(menu_func)


def unregister():
    bpy.types.INFO_MT_file_export.remove(menu_func)
    bpy.utils.unregister_class(TeslaExporter)

if __name__ == "__main__":
    register()
