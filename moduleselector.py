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

yscale = 1.25

# -------------------------------------------------------------------
#   Operators
# -------------------------------------------------------------------


class ChangeToLiftout(Operator):
    bl_idname = "wm.change_to_liftout"
    bl_label = "Liftout Animator"

    def execute(self, context):

        bpy.context.window.scene = bpy.data.scenes["Liftout Scene"]
        bpy.context.window.workspace = bpy.data.workspaces['Liftout Animator']

        return {'FINISHED'}


class ChangeToPostSim(Operator):
    bl_idname = "wm.change_to_postsim"
    bl_label = "Post Welder"

    def execute(self, context):

        bpy.context.window.scene = bpy.data.scenes["Postwelder Scene"]
        bpy.context.window.workspace = bpy.data.workspaces['Post Welder']

        return {'FINISHED'}


class ChangeToStageSim(Operator):
    bl_idname = "wm.change_to_stagesim"
    bl_label = "Stage Simulator"

    def execute(self, context):

        bpy.context.window.scene = bpy.data.scenes["StageSim Scene"]
        bpy.context.window.workspace = bpy.data.workspaces['Stage Simulator']

        return {'FINISHED'}


class LOAModuleChangerPanel(Panel):
    bl_idname = "FIBSIM_PT_loa_modulechanger_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'Liftout Animator'
    bl_label = "Change to Module"

    def draw(self, context):
        layout = self.layout

        row1 = layout.row(align=True)
        row1.scale_y = yscale
        row1.operator("wm.change_to_postsim")
        row1.operator("wm.change_to_stagesim")


class PostSimModuleChangerPanel(Panel):
    bl_idname = "FIBSIM_PT_postsim_modulechanger_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'Post Simulator'
    bl_label = "Change to Module"

    def draw(self, context):
        layout = self.layout

        row1 = layout.row(align=True)
        row1.scale_y = yscale
        row1.operator("wm.change_to_liftout")
        row1.operator("wm.change_to_stagesim")


class StageSimModuleChangerPanel(Panel):
    bl_idname = "FIBSIM_PT_stagesim_modulechanger_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'Stage Simulator'
    bl_label = "Change to Module"

    def draw(self, context):
        layout = self.layout

        row1 = layout.row(align=True)
        row1.scale_y = yscale
        row1.operator("wm.change_to_liftout")
        row1.operator("wm.change_to_postsim")

# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------


__classes__ = (
    ChangeToLiftout,
    ChangeToPostSim,
    ChangeToStageSim,
    LOAModuleChangerPanel,
    PostSimModuleChangerPanel,
    StageSimModuleChangerPanel
    )

register, unregister = bpy.utils.register_classes_factory(__classes__)

if __name__ == "__main__":
    register()
