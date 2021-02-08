
bl_info = {
	"name": "Post Position",
	"description": "3D simulator of FIB lift-out post welding",
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


def post_moved(self, context):
	# bpy.data.objects['Post'].pose.bones['Tilt axis'], "rotation_quaternion")
	props = bpy.context.scene.PostSim_pointer
	bones = bpy.data.objects['Post Armature'].pose.bones
	bones["T Bone"].rotation_mode = "XYZ"
	bones["T Bone"].rotation_euler[0] = rad(props.post_t)
	bones["R Bone"].rotation_mode = "XYZ"
	bones["R Bone"].rotation_euler[1] = rad(props.post_r)
	bones["XYZ Bone"].location = [-props.post_x, props.post_z, props.post_y]

class ZeroPost(bpy.types.Operator):
	bl_idname = "object.zero_post"
	bl_label = "Zero Post"

	def execute(self, context):
		props = bpy.context.scene.PostSim_pointer
		
		props.post_x = props.post_x_def
		props.post_y = props.post_y_def
		props.post_z = props.post_z_def
		props.post_r = props.post_r_def
		props.post_t = props.post_t_def

		return {'FINISHED'}

class PostSimProps(bpy.types.PropertyGroup):

	post_x : bpy.props.FloatProperty(
		name = "Post X",
		description = "Post X coordinate, -155 mm -> 155 mm",
		min = -155,
		max = 155,
		update = post_moved
		)
	post_x_def = 0

	post_y : bpy.props.FloatProperty(
		name = "Post Y",
		description = "Post Y coordinate, -155 mm -> 155 mm",
		min = -155,
		max = 155,
		update = post_moved
		)
	post_y_def = 0

	post_z : bpy.props.FloatProperty(
		name = "Post Z",
		description = "Post Z coordinate, defined as 0 at Eucentric, -20 mm -> 20 mm",
		min = -20,
		max = 20,
		update = post_moved
		)
	post_z_def = 0

	post_r : bpy.props.FloatProperty(
		name = "Post R",
		description = "Post R coordinate in deg, -360d -> 360d",
		min = -360,
		max = 360,
		update = post_moved
		)
	post_r_def = 0

	post_t : bpy.props.FloatProperty(
		name = "Post T",
		description = "Post T coordinate in deg, -12d -> 60d",
		min = -12,
		max = 60,
		update = post_moved
		)
	post_t_def = 0


class PostSimPanel(bpy.types.Panel):
	bl_idname = "OBJECT_PT_PostSim_panel"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "Post Simulator"
	bl_label = "Post Simulator"

	def draw(self, context):
		layout = self.layout
		scene = context.scene
		pointer = scene.PostSim_pointer

		layout.label(text=" Post coordinates:")

		col1 = layout.column(align=True)
		col1.prop(pointer, "post_x")
		col1.prop(pointer, "post_y")
		col1.prop(pointer, "post_z")
		col1.prop(pointer, "post_t")
		col1.prop(pointer, "post_r")

		layout.operator("object.zero_post")

		layout.label(text="Go to viewpoint:")
		row1 = layout.row(align=True)
		# Pull in ebeam-ibeam-laser view from StageSim
		row1.operator("wm.ebeam_view")
		row1.operator("wm.ibeam_view")
		row1.operator("wm.laser_view")

		row2 = layout.row()
		row2.scale_y = 1.75
		row2.operator("wm.change_to_liftout")

class PostSimLiftoutPanel(bpy.types.Panel):
	bl_idname = "OBJECT_PT_PostSimLiftout_panel"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "Post Simulator"
	bl_label = "PostSim Liftout animator"
	# bl_context = "scene"

	def draw(self, context):
		layout = self.layout
		scene = context.scene
		mytool = scene.my_tool
		obj = context.object

		col1 = layout.column(align=True)
		col1.prop(mytool, "first_rot")
		col1.prop(mytool, "second_rot")
		col1.prop(mytool, "third_rot")

		row = layout.row()
		row.scale_y = 1.5
		if not context.screen.is_animation_playing:
			row.operator("screen.animation_play", icon="PLAY", text="Play")
		else:
			row.operator("screen.animation_play", icon="PAUSE", text="Pause")
		row.operator("wm.magic_angles_animator", icon="CAMERA_DATA")
		layout.label(text="Lamella type:")
		row2 = layout.row(align=True)
		row2.scale_y = 1.2
		row2.operator("object.xsec_lamella")
		row2.operator("object.planview_lamella")
		# row2.operator("wm.show_angle_components")
		
		layout.label(text="Liftout mode:")
		row3 = layout.row(align=True)
		row3.operator("wm.anim_mode")
		row3.operator("wm.sim_mode")

		layout.operator('wm.lamella_position_reset')
		layout.operator("wm.restore_defaults")
		# layout.operator("ANIM_OT_keyframe_clear_v3d")
		row3 = layout.row()
		row3.scale_y = 1.75
		row3.operator("wm.change_to_stagesim")

		box = layout.box()
		row = box.row()
		row.prop(mytool, "expanded",
		    icon="TRIA_DOWN" if mytool.expanded else "TRIA_RIGHT",
		    icon_only=False, emboss=False
		)
		# row.label(text="Animation Options:")

		if mytool.expanded:
			# box.prop(obj, "name")
			box.prop(mytool, "rotation_frames")
			box.prop(mytool, "rest_frames")
			box.prop(mytool, "play_on_animate")
			row3 = box.row()
			row3.prop(mytool, "live_update")
			# row3.prop(mytool, "follow_lamella")
			box.prop(mytool, "finish_on_frame")
			box.prop(mytool, "rotation_mode")
			box.prop(mytool, "printout_mode")
			box.prop(mytool, "insert_needle")

			col2 = box.column(align=True)
			col2.prop(mytool, "initial_eulerX")
			col2.prop(mytool, "initial_eulerY")
			col2.prop(mytool, "initial_eulerZ")


class ChangeToPostSim(bpy.types.Operator):
	bl_idname = "wm.change_to_postsim"
	bl_label = "Change to Post Welder"

	def execute(self, context):
		
		bpy.context.window.scene = bpy.data.scenes["Postwelder Scene"]
		bpy.context.window.workspace = bpy.data.workspaces['Post Welder']

		return {'FINISHED'}


def register():

	bpy.utils.register_class(PostSimProps)
	bpy.types.Scene.PostSim_pointer = bpy.props.PointerProperty(type=PostSimProps)
	bpy.utils.register_class(ZeroPost)
	bpy.utils.register_class(ChangeToPostSim)
	bpy.utils.register_class(PostSimPanel)
	bpy.utils.register_class(PostSimLiftoutPanel)

def unregister():
	bpy.utils.unregister_class(PostSimLiftoutPanel)
	bpy.utils.unregister_class(PostSimPanel)
	bpy.utils.unregister_class(ChangeToPostSim)
	bpy.utils.unregister_class(ZeroPost)
	del bpy.types.Scene.PostSim_pointer
	bpy.utils.register_class(PostSimProps)

if __name__ == "__main__":
	register()