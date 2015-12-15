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


def getTextSize(text):
    return len(bytes(text, 'utf-8'))


def getTextSizeZeroTerm(text):
    return len(bytes(text, 'utf-8')) + 1


def getLenTextSize(text):
    return 4 + len(bytes(text, 'utf-8'))


class NodeTypes:
    Root = 0
    Transform = 1
    Object = 2
    Mesh = 3
    VertexArray = 4
    IndexArray = 5
    Material = 6


class Node:
    type = 0
    numChildren = 0

    def WriteData(self, exporter):
        return

    def GetSize(self):
        return 8


class NodeRoot(Node):
    type = NodeTypes.Root


class NodeTransform(Node):
    type = NodeTypes.Transform
    matrix = [1.0, 0.0, 0.0, 0.0,
              0.0, 1.0, 0.0, 0.0,
              0.0, 0.0, 1.0, 0.0,
              0.0, 0.0, 0.0, 1.0]

    def WriteData(self, exporter):
        exporter.WriteFloatArray(self.matrix)

    def GetSize(self):
        return 8 + 16 * 4


class NodeVertexArray(Node):
    type = NodeTypes.VertexArray
    attrib = "unknown attribute"
    vertlen = 3
    verts = [0.0, 0.0, 0.0]

    def WriteData(self, exporter):
        exporter.WriteLenChars(self.attrib)
        exporter.WriteUInt8(self.vertlen)
        exporter.WriteUInt32(len(self.verts))
        exporter.WriteFloatArray(self.verts)

    def GetSize(self):
        return 8 + getLenTextSize(self.attrib) + 1 + 4 * len(self.verts)


class NodeIndexArray(Node):
    type = NodeTypes.IndexArray
    sides = 3
    faces = [0, 0, 0]

    def WriteData(self, exporter):
        exporter.WriteUInt8(self.sides)
        exporter.WriteUInt32(len(self.faces))
        exporter.WriteUInt32Array(self.faces)

    def GetSize(self):
        return 8 + 1 + 4 + 4 * len(self.faces)


class NodeMaterial(self):
    name = 'defaultmaterial'

    def WriteData(self, exporter):
        exporter.WriteLenChars(self.name)

    def GetSize(self):
        return 8 + getLenTextSize(name)


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

    def WriteLenChars(self, text):
        text = bytes(text, 'utf-8')
        self.WriteUInt32(len(text))
        self.file.write(struct.pack('b' * len(text), *text))

    def WriteCharsZeroTerm(self, text):
        text = bytes(text, 'utf-8')
        self.file.write(struct.pack('b' * len(text), *text))
        self.file.write(struct.pack('b', 0))

    def WriteNode(self, node):
        self.WriteUInt32(node.GetSize(node))
        self.WriteUInt16(node.type)
        self.WriteUInt16(node.numChildren)
        node.WriteData(node, self)
        self.WriteUInt16(65535)

    def execute(self, context):
        self.file = open(self.filepath, "wb")
        self.WriteChars('FULHAX')
        node = NodeVertexArray
        self.WriteNode(node)
        node = NodeIndexArray
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
