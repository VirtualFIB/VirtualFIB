# <FIBsim - the friendly neighborhood FIB 3D simulator>
# Copyright (C) <2021>  <Aleksander B. Mosberg>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import bpy
from bpy.types import (Operator,
                       PropertyGroup,
                       Panel
                       )
from bpy.props import FloatProperty
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

# -------------------------------------------------------------------
#   Operators
# -------------------------------------------------------------------


class ZeroStage(Operator):
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


class StageSimProps(PropertyGroup):

    stage_x: FloatProperty(
        name="Stage X",
        description="Stage X coordinate, -155 mm -> 155 mm",
        min=-155,
        max=155,
        update=stage_moved
        )
    stage_x_def = 0

    stage_y: FloatProperty(
        name="Stage Y",
        description="Stage Y coordinate, -155 mm -> 155 mm",
        min=-155,
        max=155,
        update=stage_moved
        )
    stage_y_def = 0

    stage_z: FloatProperty(
        name="Stage Z",
        description="Stage Z coordinate, defined as 0 at Eucentric, -20 mm -> 20 mm",
        min=-20,
        max=20,
        update=stage_moved
        )
    stage_z_def = 0

    stage_r: FloatProperty(
        name="Stage R",
        description="Stage R coordinate in deg, -360d -> 360d",
        min=-360,
        max=360,
        update=stage_moved
        )
    stage_r_def = 0

    stage_t: FloatProperty(
        name="Stage T",
        description="Stage T coordinate in deg, -36d -> 60d",
        min=-36,
        max=60,
        update=stage_moved
        )
    stage_t_def = 0


class StageSimPanel(Panel):
    bl_idname = "OBJECT_PT_StageSim_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Stage Simulator"
    bl_label = "Stage Simulator"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        pointer = scene.StageSim_pointer

        layout.label(text=" Stage coordinates:")

        col1 = layout.column(align=True)
        col1.prop(pointer, "stage_x")
        col1.prop(pointer, "stage_y")
        col1.prop(pointer, "stage_z")
        col1.prop(pointer, "stage_t")
        col1.prop(pointer, "stage_r")

        layout.operator("object.zero_stage")

# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------


__classes__ = (StageSimProps,
               ZeroStage,
               StageSimPanel
               )


def register():
    from bpy.utils import register_class
    register_class(__classes__[0])
    bpy.types.Scene.StageSim_pointer = bpy.props.PointerProperty(type=StageSimProps)
    for cls in __classes__[1:]:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reverse(__classes__[1:]):
        unregister_class(cls)
    del bpy.types.Scene.StageSim_pointer
    unregister_class(__classes__[0])


if __name__ == "__main__":
    register()


# import bpy

# for item in bpy.context.selected_objects:
#     item.select_set(False)
    
# sample = bpy.data.objects['Sample 2.001']
# stub = bpy.data.objects['Stub_customizable.001']
    
# sample.select_set(True)
# stub.select_set(True)

# bpy.context.view_layer.objects.active = stub
# bpy.ops.object.parent_set(keep_transform=True)
