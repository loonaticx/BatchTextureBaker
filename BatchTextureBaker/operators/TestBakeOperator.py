"""
https://blender.stackexchange.com/questions/44525/cycles-bake-script-error-circular-dependency
"""

# list items in a group names 'bake'

import bpy

# bpy.ops.baketool.bibake() - quick test to use BAKETOOL addon for baking from CI - it works well

bake_size = 512
uv_channel_name = "B"


# function to create new image
def create_new_image(name):
    # create blank image
    bpy.ops.image.new(name = name, width = bake_size, height = bake_size)  # new image

    return


# function to add nodes
def add_bake_nodes(mat, name):

    # make sure using nodes
    if mat.use_nodes == False:
        mat.use_nodes = True

    nodes = mat.node_tree.nodes

    node = nodes.new(type = "ShaderNodeTexImage")
    bake_img_txt = "bake_img_" + name
    node.name = bake_img_txt
    nodes[bake_img_txt].location = 300, 160
    nodes[bake_img_txt].image = bpy.data.images[name]
    nodes[bake_img_txt].select = True

    node = nodes.new(type = "ShaderNodeUVMap")
    bake_uv_map = "bake_uv_" + name
    node.name = bake_uv_map
    nodes[bake_uv_map].location = 100, 160
    nodes[bake_uv_map].uv_map = uv_channel_name
    # connect nodes
    outn = nodes[bake_uv_map].outputs[0]
    inn = nodes[bake_img_txt].inputs[0]
    mat.node_tree.links.new(outn, inn)

    return


def remove_bake_nodes(mat, name):

    nodes = mat.node_tree.nodes
    bake_img_txt = "bake_img_" + name
    nodes.remove(nodes[bake_img_txt])
    bake_uv_map = "bake_uv_" + name
    nodes.remove(nodes[bake_uv_map])

    return


def select_none():
    for obj in bpy.context.scene.objects:
        obj.select = False
    return


bakegroup = bpy.data.groups['bake']

print("ITEMS TO BAKE: " + str(len(bakegroup.objects)))

# select none
select_none()

for object in bakegroup.objects:
    objName = object.name
    print("name: " + objName)
    object.select = True
    bpy.context.scene.objects.active = object

    # num materials
    num_materials = len(object.data.materials)

    # create new image for bake
    create_new_image(objName)

    # add bake nodes
    for num in range(0, num_materials):
        print("  -material " + str(num) + ": " + object.data.materials[num].name)
        object.active_material_index = num
        material = object.active_material
        # add bake nodes to material
        add_bake_nodes(material, objName)

    # bake object to internal img data
    # assume bake settings are set
    # select UV channel B
    uv_textures = object.data.uv_textures
    uv_textures.active = object.data.uv_textures[uv_channel_name]
    bpy.ops.object.bake(type = 'COMBINED')

    # remove bake nodes
    for num in range(0, num_materials):
        object.active_material_index = num
        material = object.active_material
        remove_bake_nodes(material, objName)

    object.select = False
