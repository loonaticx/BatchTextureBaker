import bpy

print("test run")

# scene = bpy.context.scene
# for obj in scene.objects:
#    print(obj)

bpy.context.scene.objects["supertoonCape"].select_set(True)
print(bpy.context.scene.objects["supertoonCape"].select_get())

"""
import bpy
import os, sys
 
 
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

filename = os.path.join("C:\\Users\\Loonatic-V\\PycharmProjects\\BlenderProjects\\Addon - bakerblend", "main.py")
exec(compile(open(filename).read(), filename, 'exec'))
"""