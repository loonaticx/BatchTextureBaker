# https://docs.blender.org/api/current/bpy.props.html#propertygroup-example

import bpy

INPUT_TEXTURE_DIR = ""
OUTPUT_TEXTURE_DIR = ""


class BakeTextureConfig(bpy.types.PropertyGroup):
    input_dir: bpy.props.StringProperty(
        name = "Input Texture Directory",
        description = "My description",
        default = INPUT_TEXTURE_DIR
    )
    output_dir: bpy.props.StringProperty(
        name = "Output Texture Directory",
        description = "My description",
        default = OUTPUT_TEXTURE_DIR
    )


def register():
    bpy.utils.register_class(BakeTextureConfig)
    # context.scene.texbake_config
    # context.scene.texbake_config.input_dir
    bpy.types.Scene.texbake_config = bpy.props.PointerProperty(type = BakeTextureConfig)
