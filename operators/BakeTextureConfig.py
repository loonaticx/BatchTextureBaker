"""
BakeTextureConfig

Configuration properties for setting input and output directories utilized by the script.

Author: Loonatic
Date: 6/26/2022

"""

# https://docs.blender.org/api/current/bpy.props.html#propertygroup-example

import bpy

INPUT_TEXTURE_DIR = ""
OUTPUT_TEXTURE_DIR = ""
MARGIN_PX = 16
MARGIN_TYPE = "ADJACENT_FACES"
WANT_BAKE_SUFFIX = True


class BakeTextureConfig(bpy.types.PropertyGroup):
    input_dir: bpy.props.StringProperty(
        name = "Input Texture Directory",
        description = "Directory that has image maps to convert.",
        default = INPUT_TEXTURE_DIR
    )
    output_dir: bpy.props.StringProperty(
        name = "Output Texture Directory",
        description = "Directory to save baked image maps to.",
        default = OUTPUT_TEXTURE_DIR
    )
    margin_px: bpy.props.IntProperty(
        name = "Texture Bleed Margining (px)",
        description = "My description",
        default = MARGIN_PX,
        min = 0,
        max = 32767
    )

    # for some reason this doesn't work, seems to be a blender api issue...

    #  (identifier, name, description) and optionally an icon name and unique number
    margin_types = [
        ("ADJACENT_FACES", "Adjacent Faces", "Default option"),
        ("EXTEND", "Extend", "Extends faces to the edges"),
    ]
    margin_type: bpy.props.EnumProperty(
        name = "Texture Bleed Type",
        description = "My description",
        default = MARGIN_TYPE,
        items = margin_types,
    )

    want_bake_suffix: bpy.props.BoolProperty(
        name = "Include _bake suffix?",
        description = "Determine whether or not to add _bake at the end of the save image.",
        default = WANT_BAKE_SUFFIX
    )
