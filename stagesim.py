
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


def stage_moved(self, context):
	# bpy.data.objects['Stage'].pose.bones['Tilt axis'], "rotation_quaternion")
	print("Something happened!")

class StageSimProps(bpy.types.PropertyGroup):

	stage_x : bpy.props.FloatProperty(
		name = "Stage X",
		description = "Stage X coordinate, -155 mm -> 155 mm",
		default = 0,
		min = -155,
		max = 155,
		update = stage_moved
		)

	stage_y : bpy.props.FloatProperty(
		name = "Stage Y",
		description = "Stage Y coordinate, -155 mm -> 155 mm",
		default = 0,
		min = -155,
		max = 155,
		update = stage_moved
		)

	stage_z : bpy.props.FloatProperty(
		name = "Stage Z",
		description = "Stage Z coordinate, defined as 0 at Eucentric, -20 mm -> 20 mm",
		default = 0,
		min = -20,
		max = 20,
		update = stage_moved
		)

	stage_r : bpy.props.FloatProperty(
		name = "Stage R",
		description = "Stage R coordinate in deg, -360 mm -> 360 mm",
		default = 0,
		min = -360,
		max = 360,
		update = stage_moved
		)


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

		row1 = layout.column()
		row1.prop(pointer, "stage_x")
		row1.prop(pointer, "stage_y")
		row1.prop(pointer, "stage_z")
		row1.prop(pointer, "stage_r")

def register():

	bpy.utils.register_class(StageSimProps)
	bpy.types.Scene.StageSim_pointer = bpy.types.PointerProperty(type=StageSimProps)
	bpy.utils.register_class(StageSimPanel)

def unregister():
	bpy.utils.unregister_class(StageSimPanel)
	del bpy.types.Scene.StageSim_pointer
	bpy.utils.register_class(StageSimProps)

if __name__ == "__main__":
	register()