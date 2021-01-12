"""
In order to interact with the code at any point, just paste this line:

__import__('code').interact(local=dict(globals(), **locals()))

__import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})

into where you want your breakpoint to be.
(From https://docs.blender.org/api/blender_python_api_2_76_1/info_tips_and_tricks.html)
"""

bl_info = {
	"name": "Liftout Animator",
	"description": "Animator for Magic Angles in FIB lift-out needles.",
	"author": "Aleksander B. Mosberg",
	"version": 5,
	"blender": (2, 91, 0),
	"location": "",
	"warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
	"category": "Object"
	}
#TODO: Fill out further, check https://wiki.blender.org/wiki/Process/Addons/Guidelines/metainfo.
import bpy
import math
from math import degrees, asin
import numpy as np

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       PropertyGroup,
                       )

def angle_changed(self, context):
	if bpy.context.scene.my_tool.live_update is True:
		bpy.ops.wm.magic_angles_animator()
	if bpy.context.scene.my_tool.follow_lamella is True:
		bpy.ops.view3d.view_selected(use_all_regions=False)

class MAASettings(bpy.types.PropertyGroup):

    first_rot : bpy.props.FloatProperty(
        name = "Stage Rotation",
        description = "Stage rotation, -360d -> 360d",
        default = 45.0,
        min = -360.0,
        max = 360.0,
        update = angle_changed
        )
    first_rot_def = 45

    second_rot : bpy.props.FloatProperty(
        name = "Stage Tilt",
        description = "Stage tilt, -12d -> 60d",
        default = 0,
        min = -12.0,
        max = 60.0,
        update = angle_changed
        )
    second_rot_def = 0

    third_rot : bpy.props.FloatProperty(
        name = "Needle Rotation",
        description = "Lift-out needle rotation, -360d -> 360d",
        default = 109.5,
        min = -360,
        max = 360.0,
        update = angle_changed
        )
    third_rot_def = 109.5

    initial_eulerX : bpy.props.FloatProperty(
    	name = "Pretilt X",
    	description = "Euler X-rotation for lamella pretilt",
    	default = 0,
    	min = -360,
    	max = 360,
    	update = angle_changed
    	)
    initial_eulerX_def = 0

    initial_eulerY : bpy.props.FloatProperty(
    	name = "Pretilt Y",
    	description = "Euler Y-rotation for lamella pretilt",
    	default = 0,
    	min = -360,
    	max = 360,
    	update = angle_changed
    	)
    initial_eulerY_def = 0

    initial_eulerZ : bpy.props.FloatProperty(
    	name = "Pretilt Z",
    	description = "Euler Z-rotation for lamella pretilt",
    	default = 0,
    	min = -360,
    	max = 360,
    	update = angle_changed
    	)
    initial_eulerZ_def = 0

    rotation_frames : IntProperty(
    	name = "Rotation Frames",
    	description = "Frames for rotation steps.",
    	default = 50,
    	min = 1,
    	max = 200
    	)
    rotation_frames_def = 50

    rest_frames : IntProperty(
    	name = "Rest Frames",
    	description = "Frames between rotation steps.",
    	default = 25,
    	min = 1,
    	max = 200
    	)
    rest_frames_def = 25

    play_on_animate : bpy.props.BoolProperty(
    	name = "Play on Animation",
    	description = "Play animation when pressing Animate.",
    	default = True
    	)
    play_on_animate_def = True

    live_update : bpy.props.BoolProperty(
    	name = "Live update",
    	description = "Animate and update whenever the angles change.",
    	default = False
    	)
    live_update_def = False

    follow_lamella : bpy.props.BoolProperty(
    	name = "Follow Lamella",
    	description = "Center camera on lamella when live updating.",
    	default = False
		)
    follow_lamella_def = False

    expanded : bpy.props.BoolProperty(
		name = "Animation Options:",
		description = "Expand or hide animation options.",
		default = False
		)
    expanded_def = False

    insert_needle : bpy.props.BoolProperty(
    	name = "Insert Needle",
    	description = "Animate the needle being inserted",
    	default = True
    	)
    insert_needle_def = True

    finish_on_frame : EnumProperty(
	    name="Endframe:",
        description="Set which frame to show first when pressing Animate",
        items=[ ('First', "First", "First frame"),
                ('Last', "Last", "Last frame"),
                ("Current", "Current", "Current frame")
               ]
        )
    finish_on_frame_def = 'First'

    rotation_mode : EnumProperty(
	    name="Rotation mode:",
	    description="Select whether to have smooth single rotation step or more accurate, smaller steps.",
	    items=[ ('Smooth', "Smooth", "Smooth transition, in a single keyframe."
	    	" Prettier animation but frames between the initial and final angles will not be correct."),
	            ('Detailed', "Detailed", "Detailed transition using multiple keyframes."
	            	" Splits the rotation up in equal steps for single frames (n=Rotation Frames)."
	            	" Should be more accurate for interpolation, but watch out for float errors."),
	           ]
	    )
    rotation_mode_def = 'Smooth'

    printout_mode : EnumProperty(
    name="Printout mode:",
    description="Select how the angle representation is printed out after animation.",
    items=[ ('Components', "Components", "Normalized global x-y-z components of local axis."),
            ('Angles', "Angles", "Angle between local axis and global axis normal. Parallel axes become 90deg."),
            ('Angles_offset', 'Angles Offset', 'Angle difference between local and global axis. Parallel axes become 0deg.'),
            ('All', 'All', 'All the above.')
           ]
    )
    printout_mode_def = 'Angles'


class RestoreDefaults(bpy.types.Operator):
	bl_idname = "wm.restore_defaults"
	bl_label = "Restore Default MAA Values"

	def execute(self, context):

		mt = bpy.context.scene.my_tool

		mt.first_rot = mt.first_rot_def
		mt.second_rot = mt.second_rot_def
		mt.third_rot = mt.third_rot_def
		mt.initial_eulerX = mt.initial_eulerX_def
		mt.initial_eulerY = mt.initial_eulerY_def
		mt.initial_eulerZ = mt.initial_eulerZ_def
		mt.rotation_frames = mt.rotation_frames_def
		mt.rest_frames = mt.rest_frames_def
		mt.play_on_animate = mt.play_on_animate_def
		mt.live_update = mt.live_update_def
		mt.follow_lamella = mt.follow_lamella_def
		# mt.expanded = mt.expanded_def
		mt.finish_on_frame = mt.finish_on_frame_def
		mt.rotation_mode = mt.rotation_mode_def
		mt.printout_mode = mt.printout_mode_def
		mt.insert_needle = mt.insert_needle_def

		return {'FINISHED'}

class LamellaPositionReset(bpy.types.Operator):
	bl_idname = "wm.lamella_position_reset"
	bl_label = "Reset Lamella Rotation"

	def execute(self, context):

		ob = bpy.data.objects['Lamella']
		ob.rotation_euler = (0,0,0)

		return {'FINISHED'}

class MagicAnglesAnimator(bpy.types.Operator):
	bl_idname = "wm.magic_angles_animator"
	bl_label = "Animate"

	def execute(self, context):

		# Making a new and empty scene for setting rotations as keyframes
		scn = bpy.context.scene
		scn.frame_start = 1

		if bpy.context.scene.view_layers['RenderLayer'].layer_collection.children['Cross-section lamella'].exclude == True:
			planview = True
			bpy.context.scene.view_layers['RenderLayer'].layer_collection.children['Cross-section lamella'].exclude = False
		else: 
			planview = False


		mytool = scn.my_tool

		frame_before = scn.frame_current

		# Change current frame to avoid issues from previous runs
		bpy.context.scene.frame_set(0)

		current_frame = 0
		current_frame += mytool.rest_frames

		# Taking currently selected object as the object to act upon, and resets its rotation
		ob = bpy.data.objects['Lamella']
		ob.rotation_mode = "ZYX"
		init_euler = (mytool.initial_eulerX*math.pi/180.0,
		 mytool.initial_eulerY*math.pi/180.0, mytool.initial_eulerZ*math.pi/180.0)
		ob.rotation_euler = init_euler
		# ob.rotation_euler = (0, 0, 0)

		needle = bpy.data.objects['Lift-out needle']
		needle.rotation_mode = "ZYX"
		needle.rotation_euler = (0,-135*math.pi/180,0)

		# sel is list of currently selected o bjects
		sel = bpy.context.selected_objects
		# Loop over items in sel to deselect them.
		# Can also be done using 'deselect all' operator
		for item in sel:
			item.select_set(False)
		# Then select the needle
		needle.select_set(True)
		bpy.context.view_layer.objects.active = needle
		bpy.ops.anim.keyframe_clear_v3d()
		needle.select_set(False)
		# Then reselect what was selected before
		# for item in sel:
		# 	item.select_set(True)
		# needle.select_set(False)
		# bpy.context.scene.objects.active = ob
		ob.select_set(True)
		bpy.context.view_layer.objects.active = ob

		# Reclear animations for lamella in case it was not selected.
		bpy.ops.anim.keyframe_clear_v3d()
		ob.keyframe_insert(data_path='rotation_euler', frame = current_frame)
		current_frame += mytool.rotation_frames

		# Input values, rotations and axis names
		firstrot = mytool.first_rot
		secondrot = mytool.second_rot
		thirdrot = mytool.third_rot
		axis = 'LON'


		print("\n\nAnimating rotations: {}, {}, {}:\n---------------------"
		.format(firstrot,secondrot,thirdrot))

		# Conversion of degree rotations into radians
		conv = math.pi/180
		radrot1 = firstrot*conv
		radrot2 = -secondrot*conv
		radrot3 = thirdrot*conv

		# Move to frame, rotate and create keyframe.
		if radrot1 != 0:
			bpy.ops.transform.rotate(value=-radrot1, constraint_axis=(True, True, False), orient_type="GLOBAL")
			ob.keyframe_insert(data_path='rotation_euler', frame = current_frame)
			current_frame += mytool.rest_frames
			ob.keyframe_insert(data_path='rotation_euler', frame = current_frame)

		# Repeat for second rotation step.
		if radrot2 != 0:
			bpy.context.scene.frame_set(current_frame+1)
			bpy.context.view_layer.update()
			# bpy.ops.transform.rotate(value=-radrot2, constraint_axis=(False, True, True), orient_type="GLOBAL")
			bpy.ops.transform.rotate(value=-radrot2, orient_axis='X' , orient_type="GLOBAL", orient_matrix_type='GLOBAL')
			current_frame += mytool.rotation_frames
			ob.keyframe_insert(data_path='rotation_euler', frame = current_frame)
			current_frame += mytool.rest_frames
			ob.keyframe_insert(data_path='rotation_euler', frame = current_frame)

		if mytool.insert_needle == True:
		# Before third rotation, insert needle
			needle.location = 8.0,0.0,8.3
			needle.keyframe_insert(data_path='location', frame = current_frame)
			current_frame += mytool.rotation_frames
			needle.location = 5.0,0.0,5.3
			needle.keyframe_insert(data_path='location', frame = current_frame)
			current_frame +=mytool.rest_frames
			ob.keyframe_insert(data_path='rotation_euler', frame = current_frame)
		needle.keyframe_insert(data_path='rotation_euler', frame = current_frame)


		# Set the current frame to where we're actually at so the constraint applies the right way
		print(current_frame)
		bpy.context.scene.frame_set(current_frame)
		bpy.context.view_layer.update()
		print(scn.frame_current)
		# Clear all constraints from lamella
		ob.constraints.clear()

		# Create new Child Of constraint
		ob.constraints.new('CHILD_OF')
		c = ob.constraints[0]

		# Set the constraint target
		c.target = needle

		# Set inverse on the constraint to make it make more sense
		# bpy.ops.constraint.childof_set_inverse(lon.keyframe_insert(data_path='rotation_euler', frame = 153))
		# This was difficult to understand, so let's instead just invert the matrix like StackExchange suggests
		c.inverse_matrix = c.target.matrix_world.inverted()


		# Now let's work with keyframes:
		# First we clear the slate by deleting any existing keyframes for the lamella
		# Which was right to do for figuring out this code but not for the lamella which is cleared earlier
		# ob.animation_data_clear()

		# Then we insert a keyframe at the current frame (default), keying the toggled status (it's on right now) of the constraint
		ob.keyframe_insert('constraints["Child Of"].mute', frame = current_frame)

		# Now we must toggle the keying status
		c.mute=True

		# Finally we add a keyframe at the beginning of the animation where the constraint is off.
		ob.keyframe_insert('constraints["Child Of"].mute', frame=bpy.context.scene.frame_start)


		# Select needle to do rotations on.
		ob.select_set(False)
		needle.select_set(True)
		bpy.context.view_layer.objects.active = needle

		# Repeat for third rotation step.
		if mytool.rotation_mode == "Detailed":
			for _ in range(mytool.rotation_frames):
				current_frame += 1
				
				bpy.ops.transform.rotate(value=radrot3/mytool.rotation_frames, constraint_axis=(True, True, False), orient_type='LOCAL')
				needle.keyframe_insert(data_path='rotation_euler', frame = current_frame)
				

		else:
			current_frame += mytool.rotation_frames
			
			bpy.ops.transform.rotate(value=radrot3, constraint_axis=(True, True, False), orient_type='LOCAL')
			needle.keyframe_insert(data_path='rotation_euler', frame = current_frame)

			
		scn.frame_end = current_frame + mytool.rest_frames
		if mytool.finish_on_frame == 'First':
			scn.frame_current = 1
		elif mytool.finish_on_frame == 'Last':
			scn.frame_current = scn.frame_end
		else:
			scn.frame_current = frame_before

		bpy.ops.wm.show_angle_components()

		# If "Play on Animation" is checked, start the animation (unless it already is playing).
		if mytool.play_on_animate is True:
			if not context.screen.is_animation_playing:
				bpy.ops.screen.animation_play()

		# ob.select_set(False)
		needle.select_set(False)
		# bpy.context.scene.objects.active = sel
		for item in sel:
			item.select_set(True)

		if planview is True:
			bpy.context.scene.view_layers['RenderLayer'].layer_collection.children['Cross-section lamella'].exclude = True

		return {'FINISHED'}

class ShowAngleComponents(bpy.types.Operator):
	bl_idname = "wm.show_angle_components"
	bl_label = "Print Local Angles"

	def execute(self, context):
		ob = bpy.data.objects['Lamella']
		ob.rotation_mode = "QUATERNION"
		scn = bpy.context.scene
		mytool = scn.my_tool

		q = ob.rotation_quaternion.to_matrix()

		x = [q[0][0],q[1][0],q[2][0]]
		y = [q[0][1],q[1][1],q[2][1]]
		z = [q[0][2],q[1][2],q[2][2]]

		dx = []
		for ang in x:
		    dx.append(degrees(asin(ang)))  
		dy = []
		for ang in y:
		    dy.append(degrees(asin(ang)))
		dz = []
		for ang in z:
		    dz.append(degrees(asin(ang)))

		print("Printing Local Angles:\n---------------------")

		if mytool.printout_mode == 'All':
			print("Final axis components")
			print("X: ({:.4f}), ({:.4f}), ({:.4f})".format(x[0],x[1],x[2]))
			print("Y: ({:.4f}), ({:.4f}), ({:.4f})".format(y[0],y[1],y[2]))
			print("Z: ({:.4f}), ({:.4f}), ({:.4f})\n".format(z[0],z[1],z[2]))
			print("Final angle components")
			print("X: ({:.4f}), ({:.4f}), ({:.4f})".format(dx[0],dx[1],dx[2]))
			print("Y: ({:.4f}), ({:.4f}), ({:.4f})".format(dy[0],dy[1],dy[2]))
			print("Z: ({:.4f}), ({:.4f}), ({:.4f})\n".format(dz[0],dz[1],dz[2]))
			print("Final axis offsets")
			print("X: ({:.4f}), ({:.4f}), ({:.4f})".format(90-dx[0],90-dx[1],90-dx[2]))
			print("Y: ({:.4f}), ({:.4f}), ({:.4f})".format(90-dy[0],90-dy[1],90-dy[2]))
			print("Z: ({:.4f}), ({:.4f}), ({:.4f})\n".format(90-dz[0],90-dz[1],90-dz[2]))

		elif mytool.printout_mode == 'Components':
			print("Final axis components")
			print("X: ({:.4f}), ({:.4f}), ({:.4f})".format(x[0],x[1],x[2]))
			print("Y: ({:.4f}), ({:.4f}), ({:.4f})".format(y[0],y[1],y[2]))
			print("Z: ({:.4f}), ({:.4f}), ({:.4f})\n".format(z[0],z[1],z[2]))
		elif mytool.printout_mode == 'Angles':
			print("Final angle components")
			print("X: ({:.4f}), ({:.4f}), ({:.4f})".format(dx[0],dx[1],dx[2]))
			print("Y: ({:.4f}), ({:.4f}), ({:.4f})".format(dy[0],dy[1],dy[2]))
			print("Z: ({:.4f}), ({:.4f}), ({:.4f})\n".format(dz[0],dz[1],dz[2]))
		elif mytool.printout_mode == 'Angles_offset':
			print("Final axis offsets")
			print("X: ({:.4f}), ({:.4f}), ({:.4f})".format(90-dx[0],90-dx[1],90-dx[2]))
			print("Y: ({:.4f}), ({:.4f}), ({:.4f})".format(90-dy[0],90-dy[1],90-dy[2]))
			print("Z: ({:.4f}), ({:.4f}), ({:.4f})\n".format(90-dz[0],90-dz[1],90-dz[2]))

		ob.rotation_mode = "ZYX"

		return {'FINISHED'}

class MagicAnglesAnimatorPanel(bpy.types.Panel):
	bl_idname = "OBJECT_PT_MAA_panel"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "Item"
	bl_label = "Magic Angles Animator"
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
		row2 = layout.row()
		row2.scale_y = 1.2
		row2.operator("wm.show_angle_components")
		
		layout.operator('wm.lamella_position_reset')
		layout.operator("wm.restore_defaults")
		layout.operator("ANIM_OT_keyframe_clear_v3d")

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

			# row = box.row()
			# row.label(text="Hello world!", icon='WORLD_DATA')
		# layout.label(text="Simple Row:")
		# row = layout.row()
  #       row.prop(, "frame_start")
  #       row.prop(scene, "frame_end")

# ------------------------------------------------------------------------
# register and unregister
# ------------------------------------------------------------------------

def register():
	bpy.utils.register_class(MAASettings)
	bpy.types.Scene.my_tool = PointerProperty(type=MAASettings)

	bpy.utils.register_class(RestoreDefaults)
	bpy.utils.register_class(LamellaPositionReset)
	bpy.utils.register_class(MagicAnglesAnimator)
	bpy.utils.register_class(ShowAngleComponents)

	bpy.utils.register_class(MagicAnglesAnimatorPanel)
	# bpy.utils.register_class(__name__)

def unregister():
	bpy.utils.unregister_class(MagicAnglesAnimatorPanel)

	bpy.utils.unregister_class(ShowAngleComponents)
	bpy.utils.unregister_class(MagicAnglesAnimator)
	bpy.utils.unregister_class(LamellaPositionReset)
	bpy.utils.unregister_class(RestoreDefaults)

	# bpy.utils.unregister_class(__name__)

	del bpy.types.Scene.my_tool
	bpy.utils.unregister_class(MAASettings)

if __name__ == "__main__":
	register()
	print("\nMAA Registered")


