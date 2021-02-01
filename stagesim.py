
bl_info = {
	"name": "Stage Simulator",
	"description": "3D simulator of FIB stage",
	"author": "Aleksander B. Mosberg",
	"version": 1.0,
	"blender": (2, 91, 0),
	"location": "",
	"warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
	"category": "Object"
	}

import bpy
from math import radians as rad


def stage_moved(self, context):
	# bpy.data.objects['Stage'].pose.bones['Tilt axis'], "rotation_quaternion")
	props = bpy.context.scene.StageSim_pointer
	bones = bpy.data.objects['Stage Armature'].pose.bones
	bones["T Bone"].rotation_mode = "XYZ"
	bones["T Bone"].rotation_euler[0] = rad(props.stage_t)
	bones["R Bone"].rotation_mode = "XYZ"
	bones["R Bone"].rotation_euler[1] = rad(props.stage_r)
	bones["XYZ Bone"].location = [-props.stage_x, props.stage_z, props.stage_y]

class ZeroStage(bpy.types.Operator):
	bl_idname = "object.zero_stage"
	bl_label = "Zero Stage"

	def execute(self, context):
		props = bpy.context.scene.StageSim_pointer
		
		props.stage_x = props.stage_x_def
		props.stage_y = props.stage_y_def
		props.stage_z = props.stage_z_def
		props.stage_r = props.stage_r_def
		props.stage_t = props.stage_t_def

		return {'FINISHED'}

class StageSimProps(bpy.types.PropertyGroup):

	stage_x : bpy.props.FloatProperty(
		name = "Stage X",
		description = "Stage X coordinate, -155 mm -> 155 mm",
		min = -155,
		max = 155,
		update = stage_moved
		)
	stage_x_def = 0

	stage_y : bpy.props.FloatProperty(
		name = "Stage Y",
		description = "Stage Y coordinate, -155 mm -> 155 mm",
		min = -155,
		max = 155,
		update = stage_moved
		)
	stage_y_def = 0

	stage_z : bpy.props.FloatProperty(
		name = "Stage Z",
		description = "Stage Z coordinate, defined as 0 at Eucentric, -20 mm -> 20 mm",
		min = -20,
		max = 20,
		update = stage_moved
		)
	stage_z_def = 0

	stage_r : bpy.props.FloatProperty(
		name = "Stage R",
		description = "Stage R coordinate in deg, -360d -> 360d",
		min = -360,
		max = 360,
		update = stage_moved
		)
	stage_r_def = 0

	stage_t : bpy.props.FloatProperty(
		name = "Stage T",
		description = "Stage T coordinate in deg, -12d -> 60d",
		min = -12,
		max = 60,
		update = stage_moved
		)
	stage_t_def = 0


class StageSimPanel(bpy.types.Panel):
	bl_idname = "OBJECT_PT_StageSim_panel"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "StageSim"
	bl_label = "Stage Simulator"

	def draw(self, context):
		layout = self.layout
		scene = context.scene
		pointer = scene.StageSim_pointer

		layout.label(text=" Stage coordinates:")

		row1 = layout.column(align=True)
		row1.prop(pointer, "stage_x")
		row1.prop(pointer, "stage_y")
		row1.prop(pointer, "stage_z")
		row1.prop(pointer, "stage_t")
		row1.prop(pointer, "stage_r")

		layout.operator("object.zero_stage")
		layout.operator("wm.change_to_liftout")

class ChangeToLiftout(bpy.types.Operator):
	bl_idname = "wm.change_to_liftout"
	bl_label = "Change to Liftout Animator"

	def execute(self, context):
		
		bpy.context.window.scene = bpy.data.scenes["Liftout Scene"]
		bpy.context.window.workspace = bpy.data.workspaces['Liftout Animator']

		return {'FINISHED'}


def register():

	bpy.utils.register_class(StageSimProps)
	bpy.types.Scene.StageSim_pointer = bpy.props.PointerProperty(type=StageSimProps)
	bpy.utils.register_class(ZeroStage)
	bpy.utils.register_class(ChangeToLiftout)
	bpy.utils.register_class(StageSimPanel)

def unregister():
	bpy.utils.unregister_class(StageSimPanel)
	bpy.utils.unregister_class(ChangeToLiftout)
	bpy.utils.unregister_class(ZeroStage)
	del bpy.types.Scene.StageSim_pointer
	bpy.utils.register_class(StageSimProps)

if __name__ == "__main__":
	register()