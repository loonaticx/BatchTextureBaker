import bpy
import os

"""
TARGET_TEXTURE_DIR
    - reads and registers all png files in here as textures,
    - will be iterated through and baked, same file name but located in OUTPUT_TEXTURE_DIR
OUTPUT_TEXTURE_DIR


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

        # append two backslashes if those arent on end of the input
        if self.INPUT_TEXTURE_DIR[-1] != "\\":
            self.INPUT_TEXTURE_DIR += "\\"
        if self.OUTPUT_TEXTURE_DIR[-1] != "\\":
            self.OUTPUT_TEXTURE_DIR += "\\"

        print(f"INPUT_TEXTURE_DIR = {self.INPUT_TEXTURE_DIR}")
        print(f"OUTPUT_TEXTURE_DIR} = {self.OUTPUT_TEXTURE_DIR}")

        # ensure input/output dirs are valid directories
        if not os.path.isdir(self.INPUT_TEXTURE_DIR):
            print("Input texture dir is incorrect, not baking.")
            return {'FAILED'}
        if not os.path.isdir(self.OUTPUT_TEXTURE_DIR):
            print("Output texture dir is incorrect, not baking.")
            return {'FAILED'}

        # we will assume our selected object list is correct and intended for now!
        self.oldModel = bpy.context.selected_objects[0]  # type: active_object
        self.newModel = bpy.context.selected_objects[1]  # type: active_object

        # Configure our bake properties #
        # First, let's ensure we're already in the Cycles engine
        if context.scene.render.engine != 'CYCLES':
            context.scene.render.engine = 'CYCLES'

        # We only want the color; don't consider any light sources.
        bpy.context.scene.render.bake.use_pass_direct = False
        bpy.context.scene.render.bake.use_pass_indirect = False
        bpy.context.scene.render.bake.use_pass_color = True

        bpy.context.scene.render.bake.use_selected_to_active = True

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
            bpy.data.materials.new(name = str(filename))  # Make a new material (returns material obj)

    def bakeTextures(self):
        for object in bpy.context.selected_objects:
            print(object)

        # this method might just become our bakeTextures call
        # should only iterate through this loop once
        for img in bpy.data.images:
            print("name=%s, filepath=%s" % (img.name, img.filepath))

            print("Configuring old model...")
            # Configure the old models material to the imported texture
            self.configureMaterial(img, self.oldModel)

            # we need to generate a new material/image for our new model which will ultimately be our baked output image
            imgNew_path = f"{self.OUTPUT_TEXTURE_DIR}/{img.name}_baked"
            imgNew = bpy.data.images.new(name = imgNew_path, width=1024, height=1024)

            # do i even need this???
            # pixels = [1.0] * (4 * 1024 * 1024)
            # pixels = [chan for px in pixels for chan in px]
            # image.pixels = pixels

            print("Configuring new model...")
            # imgNew = self.images.load(f"{self.OUTPUT_TEXTURE_DIR}/{img.name}")
            self.configureMaterial(imgNew, self.newModel)
            print("Finished configuring materials, beginning baking process...")

            # Like pressing the 'Bake' button in Blender
            # this will remain locked until the bake is complete.
            bpy.ops.object.bake(type = 'DIFFUSE')
            print("Finished baking process, beginning saving process...")

            # save-as by setting the target path and saving
            imgNew.file_format = 'PNG'
            imgNew.filepath_raw = f"{self.OUTPUT_TEXTURE_DIR}/{img.name}"
            imgNew.save()

    def configureMaterial(self, img, model):
        # bpy.context.space_data.context = 'MATERIAL'

        # intended to get the material name and set the proper attributes on it
        # print(f"img filepath: {img.filepath}\nimg name: {img.name}")

        # mat = bpy.data.materials.get(os.path.splitext(img.filepath)[0])
        mat = bpy.data.materials.get(img.name)
        if mat is None:
            print(f"Material was None for {img.name}, generating a new material.")
            mat = bpy.data.materials.new(name = img.name)

        # Enable 'Use nodes':
        mat.use_nodes = True

        nodes = mat.node_tree.nodes
        nodes.clear()

        # Add principled shader node (required default)
        node_principled = nodes.new(type = 'ShaderNodeBsdfPrincipled')
        node_principled.location = 0, 0

        # Assign image texture node (Our texture image)
        node_tex = nodes.new('ShaderNodeTexImage')
        node_tex.image = img
        node_tex.location = -400, 0

        # Add the Output node (required default)
        node_output = nodes.new(type = 'ShaderNodeOutputMaterial')
        node_output.location = 400, 0

        # Link all nodes
        links = mat.node_tree.links
        link = links.new(node_tex.outputs["Color"], node_principled.inputs["Base Color"])
        link = links.new(node_principled.outputs["BSDF"], node_output.inputs["Surface"])

        print(f"mat = ")

        # bpy.context.object.active_material.name = "test"
        # Add our (input) texture to the model
        model.data.materials[0] = mat


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
