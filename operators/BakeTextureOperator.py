"""
BakeTextureOperator

Author: Loonatic
Date: 6/26/2022

"""

import bpy
import os

"""
TARGET_TEXTURE_DIR
    - reads and registers all png files in here as textures,
    - will be iterated through and baked, same file name but located in OUTPUT_TEXTURE_DIR
OUTPUT_TEXTURE_DIR

Notes
- Currently the output texture copies the same dimensions as the input texture, however, this may
cause some ugly quality loss compared to baking a 1024x1024 render and *then* exporting the image.


"""

"""
References

https://blender.stackexchange.com/questions/10860/baking-textures-on-headless-machine-batch-baking

"""


# we need to get oldModel and newModel objects
# be able to assign textures/materials to oldModel
# generate a new material or something for the newModel thatll be saved

class BakeTextureOperator(bpy.types.Operator):
    bl_idname = "object.texbake"
    bl_label = "Texture Bake (Destination<-Source)"

    def execute(self, context):
        self.obj = context.object
        self.images = bpy.data.images
        self.INPUT_TEXTURE_DIR = context.scene.texbake_config.input_dir
        self.OUTPUT_TEXTURE_DIR = context.scene.texbake_config.output_dir
        self.MARGIN_PX = context.scene.texbake_config.margin_px
        # self.MARGIN_TYPE = context.scene.texbake_config.margin_type
        self.OUTPUT_SUFFIX = "_bake" if context.scene.texbake_config.want_bake_suffix else "_bake"

        # append two backslashes if those arent on end of the input
        if self.INPUT_TEXTURE_DIR[-1] != "\\":
            self.INPUT_TEXTURE_DIR += "\\"
        if self.OUTPUT_TEXTURE_DIR[-1] != "\\":
            self.OUTPUT_TEXTURE_DIR += "\\"

        print(f"INPUT_TEXTURE_DIR = {self.INPUT_TEXTURE_DIR}")
        print(f"OUTPUT_TEXTURE_DIR = {self.OUTPUT_TEXTURE_DIR}")

        # ensure input/output dirs are valid directories
        if not os.path.isdir(self.INPUT_TEXTURE_DIR):
            print("Input texture dir is incorrect, not baking.")
            return {'CANCELLED'}
        if not os.path.isdir(self.OUTPUT_TEXTURE_DIR):
            print("Output texture dir is incorrect, not baking.")
            return {'CANCELLED'}

        # we will assume our selected object list is correct and intended for now!
        # SOURCE -> DESTINATION !!
        self.oldModel = bpy.context.selected_objects[0]  # type: active_object
        self.newModel = bpy.context.selected_objects[1]  # type: active_object

        # Configure our bake properties #
        # https://docs.blender.org/api/current/bpy.types.RenderSettings.html

        # First, let's ensure we're already in the Cycles engine
        if context.scene.render.engine != 'CYCLES':
            context.scene.render.engine = 'CYCLES'

        # https://docs.blender.org/api/current/bpy.types.BakeSettings.html

        # We only want the color; don't consider any light sources.
        bpy.context.scene.render.bake.use_pass_direct = False
        bpy.context.scene.render.bake.use_pass_indirect = False
        bpy.context.scene.render.bake.use_pass_color = True
        bpy.context.scene.render.bake.margin = self.MARGIN_PX
        # bpy.context.scene.render.bake.margin_type = self.MARGIN_TYPE

        # test
        bpy.context.scene.render.bake.use_split_materials = True

        # Register all our input textures
        self.registerInputTextures()

        # Aaaaand, let's bake!
        self.bakeTextures()

        return {'FINISHED'}

    def registerInputTextures(self):
        for filename in os.listdir(self.INPUT_TEXTURE_DIR):
            imageFile = os.path.join(self.INPUT_TEXTURE_DIR, filename)
            self.images.load(imageFile, check_existing = True)
            # we don't set the texture on the material here, only registering a new material with textures name.
            print(f"imageFile = {imageFile}")
            print(f"filename = {filename}")
            # bpy.data.materials.new(name = str(filename))  # Make a new material (returns material obj)
            # bpy.ops.material.new(name = str(filename))

    def bakeTextures(self):
        # should only iterate through this loop once
        for img in bpy.data.images:
            # Configure the old models material to the imported texture
            old_model_material = self.configureMaterial(img, self.oldModel)

            # we need to generate a new material/image for our new model which will ultimately be our baked output image
            imgNew = bpy.data.images.new(
                name = f"{img.name}{self.OUTPUT_SUFFIX}", width = img.size[0], height = img.size[1]
            )

            new_model_material = self.configureMaterial(imgNew, self.newModel)

            # Reload images to ensure we dont bake the same texture twice
            bpy.data.images[img.name].update()
            bpy.data.images[imgNew.name].update()
            bpy.data.images[img.name].reload()
            bpy.data.images[imgNew.name].reload()

            self.oldModel.active_material = old_model_material
            self.newModel.active_material = new_model_material

            ## Finished configuring materials, beginning baking process ##

            # Like pressing the 'Bake' button in Blender
            # this will remain locked until the bake is complete.
            bpy.ops.object.bake(type = 'DIFFUSE', use_selected_to_active = True, use_clear = True)

            ## Finished baking, now we will save and remove temp files ##

            img.name = img.name.replace('.jpg', '.png')
            imgNew.name = imgNew.name.replace('.jpg', '.png')
            # lazy hack
            imgNew.name = imgNew.name.replace(f'.png{self.OUTPUT_SUFFIX}', f'{self.OUTPUT_SUFFIX}.png')
            # if self.OUTPUT_SUFFIX:
            #     imgNew.name = imgNew.name.replace(f'.png{self.OUTPUT_SUFFIX}', self.OUTPUT_SUFFIX)
            # else:
            #     imgNew.name = imgNew.name.replace(f'png.001', 'png')

            imgNew.save_render(filepath = f"{self.OUTPUT_TEXTURE_DIR}/{imgNew.name}")

            # Remove old images since we dont need them anymore
            bpy.data.images.remove(img)
            bpy.data.images.remove(imgNew)
            self.removeMaterials(self.oldModel)
            self.removeMaterials(self.newModel)

    def configureMaterial(self, img, model):
        mat = model.data.materials.get(img.name)
        if mat is None:
            print(f"Material was None for {img.name}, generating a new material.")
            mat = bpy.data.materials.new(name = img.name)

        if not model.data.materials:
            bpy.ops.object.material_slot_add()

        # Enable 'Use nodes':
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        nodes.clear()
        for node in nodes:
            nodes.remove(node)

        # Add principled shader node (required default)
        node_principled = nodes.new(type = 'ShaderNodeBsdfPrincipled')
        node_principled.location = 0, 0

        # Assign image texture node (Our texture image)
        node_tex = nodes.new(type = 'ShaderNodeTexImage')
        node_tex.name = 'Bake_node'
        node_tex.image = img
        node_tex.location = -400, 0
        node_tex.select = True
        nodes.active = node_tex

        # Add the Output node (required default)
        node_output = nodes.new(type = 'ShaderNodeOutputMaterial')
        node_output.name = 'node_output'

        # Link all nodes
        links = mat.node_tree.links
        link = links.new(node_tex.outputs["Color"], node_principled.inputs["Base Color"])
        link = links.new(node_principled.outputs["BSDF"], node_output.inputs["Surface"])

        # Add our (input) texture to the model
        if model.data.materials:
            model.data.materials[0] = mat
        else:
            model.data.materials.append(mat)

        return mat

    def removeMaterials(self, model):
        for mat in model.data.materials:
            print(mat)

        for mat in model.data.materials:
            for n in mat.node_tree.nodes:
                if n.name == 'Bake_node':
                    mat.node_tree.nodes.remove(n)


"""
notes

image = bpy.context.data.images["tt_t_chr_avt_acc_pac_supertoonCape.png"]
returns an Image object
<bpy_struct, Image("tt_t_chr_avt_acc_pac_supertoonCape.png") at 0x0000017C4ECD3908>
where we can do
image.file_format
image.filepath_raw
image.save


for obj in bpy.context.selected_objects:
<bpy_struct, Object("supertoonCape unnamed1") at 0x0000017C4C946408>
<bpy_struct, Object("supertoonCape") at 0x0000017C4C946B08>

unnamed1 is index 0
unnamed 1 is also our OLD model
"""

# C:\Users\Loonatic-V\PycharmProjects\BlenderProjects\input_test\
# C:\Users\Loonatic-V\PycharmProjects\BlenderProjects\output_test
