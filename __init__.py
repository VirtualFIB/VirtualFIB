import bpy
from bpy.app.handlers import persistent
from . import loa, stagesim

@persistent
def load_handler_for_preferences(_):
    print("Changing Preference Defaults!")
    from bpy import context

    prefs = context.preferences
    prefs.use_preferences_save = False

    kc = context.window_manager.keyconfigs["blender"]
    kc_prefs = kc.preferences
    if kc_prefs is not None:
        kc_prefs.select_mouse = 'LEFT'
        kc_prefs.spacebar_action = 'SEARCH'
        kc_prefs.use_pie_click_drag = True

    view = prefs.view
    view.header_align = 'BOTTOM'


@persistent
def load_handler_for_startup(_):
    print("Changing Startup Defaults!")

    # Use smooth faces.
    for mesh in bpy.data.meshes:
        for poly in mesh.polygons:
            poly.use_smooth = False

    # Use material preview shading.
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'
                    space.shading.use_scene_lights = True


def register():
    print("Registering to Change Defaults")
    bpy.app.handlers.load_factory_preferences_post.append(load_handler_for_preferences)
    bpy.app.handlers.load_factory_startup_post.append(load_handler_for_startup)
    loa.register()
    stagesim.register()


def unregister():
    print("Unregistering to Change Defaults")
    bpy.app.handlers.load_factory_preferences_post.remove(load_handler_for_preferences)
    bpy.app.handlers.load_factory_startup_post.remove(load_handler_for_startup)
    loa.unregister()
    stagesim.unregister()