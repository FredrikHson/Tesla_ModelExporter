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


class Vertex:
    __slots__ = (
        "pos_x", "pos_y", "pos_z",
        "normal_x", "normal_y", "normal_z",
        "tangent_x", "tangent_y", "tangent_z",
        "binormal_sign",
        "texcoord0_x", "texcoord0_y"
    )

    def __init__(self, pos_x=0, pos_y=0, pos_z=0,
                 normal_x=0, normal_y=0, normal_z=0,
                 tangent_x=0, tangent_y=0, tangent_z=0,
                 binormal_sign=1,
                 texcoord0_x=0, texcoord0_y=0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.normal_x = normal_x
        self.normal_y = normal_y
        self.normal_z = normal_z
        self.tangent_x = tangent_x
        self.tangent_y = tangent_y
        self.tangent_z = tangent_z
        self.texcoord0_x = texcoord0_x
        self.texcoord0_y = texcoord0_y
        self.binormal_sign = binormal_sign

    def __str__(self):
        return "X:{0} Y:{1} Z:{2}".format(self.pos_x, self.pos_y, self.pos_z)

    def __eq__(self, other):
        if self.pos_x != other.pos_x:
            return False
        if self.pos_y != other.pos_y:
            return False
        if self.pos_z != other.pos_z:
            return False
        if self.normal_x != other.normal_x:
            return False
        if self.normal_y != other.normal_y:
            return False
        if self.normal_z != other.normal_z:
            return False
        if self.tangent_x != other.tangent_x:
            return False
        if self.tangent_y != other.tangent_y:
            return False
        if self.tangent_z != other.tangent_z:
            return False
        if self.binormal_sign != other.binormal_sign:
            return False
        if self.texcoord0_x != other.texcoord0_x:
            return False
        if self.texcoord0_y != other.texcoord0_y:
            return False
        return True

    def __hash__(self):
        return hash((
            self.pos_x, self.pos_y, self.pos_z,
            self.normal_x, self.normal_y, self.normal_z,
            self.tangent_x, self.tangent_y, self.tangent_z,
            self.texcoord0_x, self.texcoord0_y,
            self.binormal_sign
        ))


def Deindex(vertlist):
    newvertlist = list(set(vertlist))
    keys = {s: i for i, s in enumerate(newvertlist)}
    indexTranslation = [keys[s] for s in vertlist]
    return indexTranslation, newvertlist


class NodeTypes:
    Root = 0
    Transform = 1
    Object = 2
    Mesh = 3
    VertexArray = 4
    IndexArray = 5
    Material = 6


class Node:

    def __init__(self):
        self.type = 0
        self.numChildren = 0

    def WriteData(self, exporter):
        return

    def GetSize(self):
        return 0


class NodeRoot(Node):
    type = NodeTypes.Root


class NodeTransform(Node):

    def __init__(self):
        Node.__init__(self)
        self.type = NodeTypes.Transform
        self.matrix = [1.0, 0.0, 0.0, 0.0,
                       0.0, 1.0, 0.0, 0.0,
                       0.0, 0.0, 1.0, 0.0,
                       0.0, 0.0, 0.0, 1.0]

    def WriteData(self, exporter):
        exporter.WriteFloatArray(self.matrix)

    def GetSize(self):
        return 16 * 4


class NodeVertexArray(Node):

    def __init__(self):
        Node.__init__(self)
        self.type = NodeTypes.VertexArray
        self.attrib = "unknown attribute"
        self.vertlen = 3
        self.verts = []

    def WriteData(self, exporter):
        exporter.WriteLenChars(self.attrib)
        exporter.WriteUInt8(self.vertlen)
        exporter.WriteUInt32(len(self.verts))
        exporter.WriteFloatArray(self.verts)

    def GetSize(self):
        return getLenTextSize(self.attrib) + 1 + 4 + 4 * len(self.verts)

    def AppendVertex(self, vert=[]):
        for v in vert:
            self.verts.append(v)


class NodeIndexArray(Node):

    def __init__(self):
        Node.__init__(self)
        self.type = NodeTypes.IndexArray
        self.sides = 3
        self.faces = []

    def WriteData(self, exporter):
        exporter.WriteUInt8(self.sides)
        exporter.WriteUInt32(len(self.faces))
        exporter.WriteUInt32Array(self.faces)

    def GetSize(self):
        return 1 + 4 + 4 * len(self.faces)

    def AppendFace(self, face=[]):
        for f in face:
            self.faces.append(f)


class NodeMaterial(Node):

    def __init__(self):
        Node.__init__(self)
        self.name = 'defaultmaterial'
        self.type = NodeTypes.Material

    def WriteData(self, exporter):
        exporter.WriteLenChars(self.name)

    def GetSize(self):
        return getLenTextSize(self.name)


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
        self.WriteUInt32(node.GetSize())
        self.WriteUInt16(node.type)
        self.WriteUInt16(node.numChildren)
        node.WriteData(self)

    def HandleObject(self, object, handledParents=False):
        if(object.parent):
            self.HandleObject(object.parent)
        node = NodeMaterial()
        node.name = object.name
        self.WriteNode(node)

    def execute(self, context):
        self.file = open(self.filepath, "wb")
        self.WriteChars('FULHAX')

        self.exportAll = not self.option_export_selection

        scene = context.scene
        for object in scene.objects:
            if (self.exportAll or object.select):
                self.HandleObject(object)

        node = NodeVertexArray()
        node.attrib = "TexCoord0"
        node.vertlen = 2
        node.AppendVertex([0.1, 0.1])
        node.AppendVertex([0.5, 3.1])
        node.AppendVertex([0.5, 2.1])
        self.WriteNode(node)

        node = NodeVertexArray()
        node.attrib = "Position"
        node.vertlen = 4
        node.AppendVertex([1.1, 0.3, 0.5, 0.1])
        node.AppendVertex([2.1, 2.3, 0.5, 3.1])
        node.AppendVertex([3.1, 3.3, 0.5, 2.1])
        self.WriteNode(node)

        node = NodeIndexArray()
        node.AppendFace([0, 1, 2])
        node.AppendFace([1, 2, 3])
        self.WriteNode(node)

        node = NodeMaterial()
        self.WriteNode(node)

        node = NodeTransform()
        self.WriteNode(node)

        node = NodeMaterial()
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
