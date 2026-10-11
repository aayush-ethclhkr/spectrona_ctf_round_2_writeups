import bpy
from pathlib import Path
bpy.context.scene.render.engine='BLENDER_WORKBENCH'
bpy.context.scene.display.shading.light='STUDIO'
bpy.context.scene.display.shading.color_type='MATERIAL'
bpy.context.scene.render.resolution_x=1400
bpy.context.scene.render.resolution_y=850
bpy.context.scene.render.resolution_percentage=100
bpy.context.scene.render.filepath=str(Path(bpy.data.filepath).with_suffix('.png'))
bpy.ops.render.render(write_still=True)
