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
from bpy_extras.io_utils import ExportHelper


class TeslaExporter(bpy.types.Operator, ExportHelper):
    """Export to Tesla Model"""
    bl_idname = "export_scene.tesm"
    bl_label = "Export Tesla Model"
    filename_ext = ".tesm"

    def execute(self, context):
        self.file = open(self.filepath, "wb")

        self.file.close()
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(TeslaExporter.bl_idname, text = "Tesla (.tesm)")

def register():
    bpy.utils.register_class(TeslaExporter)
    bpy.types.INFO_MT_file_export.append(menu_func)

def unregister():
    bpy.types.INFO_MT_file_export.remove(menu_func)
    bpy.utils.unregister_class(TeslaExporter)

if __name__ == "__main__":
    register()