import tempfile
from pathlib import Path

import bpy
from PIL import Image

bl_info = {
    "name": "MakeWebp",
    "author": "tsutomu",
    "version": (0, 1),
    "blender": (3, 1, 0),
    "support": "TESTING",
    "category": "Object",
    "description": "",
    "location": "View3D > Object",
    "warning": "",
    "doc_url": "https://github.com/SaitoTsutomu/MakeWebp",
}


class CMW_OT_make_webp(bpy.types.Operator):
    bl_idname = "object.make_webp"
    bl_label = "Make Webp"
    bl_description = "Make webp file."

    def execute(self, context):
        scene = context.scene
        pre_filepath = scene.render.filepath
        pre_format = scene.render.image_settings.file_format
        with tempfile.TemporaryDirectory() as tmpdir:
            scene.render.filepath = str(Path(tmpdir) / "_")[:-1]
            scene.render.image_settings.file_format = "JPEG"
            bpy.ops.render.render(animation=True)
            scene.render.filepath = pre_filepath
            scene.render.image_settings.file_format = pre_format
            imgs = [Image.open(f) for f in sorted(Path(tmpdir).glob("*.jpg"))]
            imgs[0].save(
                Path(pre_filepath) / "webp.webp",
                save_all=True,
                append_images=imgs[1:],
            )
        return {"FINISHED"}


def draw_item(self, context):
    self.layout.operator(CMW_OT_make_webp.bl_idname)


def register():
    bpy.utils.register_class(CMW_OT_make_webp)
    bpy.types.VIEW3D_MT_object.append(draw_item)


def unregister():
    bpy.utils.unregister_class(CMW_OT_make_webp)
    bpy.types.VIEW3D_MT_object.remove(draw_item)


if __name__ == "__main__":
    register()
