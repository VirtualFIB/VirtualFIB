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
                       Panel
                       )

# -------------------------------------------------------------------
#   Operators
# -------------------------------------------------------------------


class EBeamView(Operator):
    bl_idname = "view3d.ebeam_view"
    bl_label = "e-beam"

    def execute(self, context):
        bpy.context.scene.camera = bpy.data.scenes["Chamber Scene"].objects["e-beam view"]
        current_context = bpy.context.region_data.view_perspective
        if "C" not in current_context:
            bpy.ops.view3d.view_camera()
        return {'FINISHED'}


class IBeamView(Operator):
    bl_idname = "view3d.ibeam_view"
    bl_label = "i-beam"

    def execute(self, context):
        bpy.context.scene.camera = bpy.data.scenes["Chamber Scene"].objects["i-beam view"]
        current_context = bpy.context.region_data.view_perspective
        if "C" not in current_context:
            bpy.ops.view3d.view_camera()
        return {'FINISHED'}


class LaserView(Operator):
    bl_idname = "view3d.laser_view"
    bl_label = "Laser"

    def execute(self, context):
        bpy.context.scene.camera = bpy.data.scenes["Chamber Scene"].objects["laser view"]
        current_context = bpy.context.region_data.view_perspective
        if "C" not in current_context:
            bpy.ops.view3d.view_camera()
        return {'FINISHED'}


class BeamViewLiftoutPanel(Panel):
    bl_idname = "FIBSIM_PT_beamview_liftout_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'Liftout Animator'
    bl_label = "Beam View"

    def draw(self, context):
        layout = self.layout

        row1 = layout.row(align=True)
        row1.scale_y = 1.2
        row1.operator("view3d.ebeam_view")
        row1.operator("view3d.ibeam_view")
        # row1.operator("view3d.laser_view")


class BeamViewPostSimPanel(Panel):
    bl_idname = "FIBSIM_PT_beamview_postsim_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'Post Simulator'
    bl_label = "Beam View"

    def draw(self, context):
        layout = self.layout

        row1 = layout.row(align=True)
        row1.scale_y = 1.2
        row1.operator("view3d.ebeam_view")
        row1.operator("view3d.ibeam_view")
        # row1.operator("view3d.laser_view")


class BeamViewStageSimPanel(Panel):
    bl_idname = "FIBSIM_PT_beamview_stagesim_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'Stage Simulator'
    bl_label = "Beam View"

    def draw(self, context):
        layout = self.layout

        row1 = layout.row(align=True)
        row1.scale_y = 1.2
        row1.operator("view3d.ebeam_view")
        row1.operator("view3d.ibeam_view")
        row1.operator("view3d.laser_view")

# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------


__classes__ = (
    EBeamView,
    IBeamView,
    LaserView,
    BeamViewLiftoutPanel,
    BeamViewStageSimPanel,
    BeamViewPostSimPanel
    )

register, unregister = bpy.utils.register_classes_factory(__classes__)

if __name__ == "__main__":
    register()
