import bpy
import os
import argparse

def clear_scene():
    """Delete all existing objects in the current scene."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def import_usd(filepath):
    """Import USD file into the scene."""
    # Ensure the USD importer is available
    if not hasattr(bpy.ops.wm, 'usd_import'):
        raise Exception("USD Import operator not found. Make sure the USD add-on is enabled.")
    # Blender may have issues with relative paths, so we convert to absolute path
    filepath = os.path.abspath(filepath)
    bpy.ops.wm.usd_import(filepath=filepath,
                          import_materials=False)
    
def process_geometry(geom_patterns, smooth_subdivision=True):
    """
    Process geometry:
    - Remove objects that are not geometry as well as geometry provided as argument
    - Smooth remaining geometry by applying a subdivision surface modifier
    @param geom_patterns: list of names of meshes to delete
    @param smooth_subdivision: whether to apply subdivision surface modifier to remaining geometry
    """
    # Switch to Object mode and deselect all
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    objects_to_delete = []

    for obj in bpy.data.objects:
        # 1. Delete all non‑mesh objects
        if obj.type != 'MESH':
            objects_to_delete.append(obj)
            continue

        part_of_shaderball = True

        # 2. For meshes, check if the name indicates it's not part of the shaderball
        name_lower = obj.name.lower()
        for pattern in geom_patterns:
            if pattern in name_lower:
                print('Remove object:', obj.name)
                objects_to_delete.append(obj)
                part_of_shaderball = False
                break   # No need to check other patterns

        if name_lower == "material_surface" and part_of_shaderball and smooth_subdivision:
            print('Smoothing surface material geometry:', obj.name)
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            
            # Smooth geometry with a subdivision surface modifier
            subdiv_modifier = obj.modifiers.new(name="Subdivision", type='SUBSURF')
            subdiv_modifier.levels = 1  
            subdiv_modifier.render_levels = 1 
            subdiv_modifier.subdivision_type = 'CATMULL_CLARK' 
            
            # Apply the modifier if you want to make it permanent
            bpy.ops.object.modifier_apply(modifier=subdiv_modifier.name)

    # Select and delete the collected objects
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects_to_delete:
        obj.select_set(True)
    if objects_to_delete:
        bpy.ops.object.delete()

    print(f"Removed {len(objects_to_delete)} object(s).")

def export_glb_no_materials(filepath):
    """
    Export the current scene as GLB without materials.
    @param filepath: output file path for the GLB
    """
    # Deselect everything before export (optional)
    bpy.ops.object.select_all(action='DESELECT')

    # glTF export settings
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',              # Write single GLB binary
        export_materials='NONE',          # Do not export any materials
        export_image_format='NONE',       # No images
        export_keep_originals=False,
        export_apply=True,                # Apply modifiers (optional)
        #export_colors=False,             # Skip vertex colors
        export_attributes=False,          # Skip custom attributes
        export_cameras=False,             # Skip cameras
        export_lights=False,              # Skip lights
        export_extras=False,              # Skip extras
        export_yup=True                   # Keep Y‑up orientation 
    )

def transform_geometry_to_world():
    """
    Transform to Y-Up and bake transforms
    """
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.transform.rotate(value=1.5708, orient_axis='X')
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    bpy.ops.object.select_all(action='DESELECT')


def main():
    argparser = argparse.ArgumentParser(description="Convert USD to GLB using Blender")
    argparser.add_argument("--usd", type=str, default="./StandardShaderBall/full_assets/StandardShaderBall/standard_shader_ball_scene.usda", help="Path to the input USD file")
    argparser.add_argument("--glb", type=str, default="./standard_shader_ball_scene.glb", help="Path to the output GLB file")
    argparser.add_argument("--blend", type=str, default="./standard_shader_ball_scene.blend", help="Path to the output Blender file (optional)")
    argparser.add_argument("--smooth", action='store_true', help="Enable smoothing of geometry")
    args = argparser.parse_args()

    USD_FILE_PATH = args.usd
    GLB_EXPORT_PATH = args.glb
    BLENDER_FILE_PATH = args.blend
    smooth_subdivision = args.smooth
    if smooth_subdivision:
        GLB_EXPORT_PATH = GLB_EXPORT_PATH.replace('.glb', '_smooth.glb')
        BLENDER_FILE_PATH = BLENDER_FILE_PATH.replace('.blend', '_smooth.blend')

    # Geometry to remove
    REMOVE_NAME_PATTERN = ["grid", "back", "backplane", "backplane.001", "front", "right", "top", "left"]          # Names of meshes to remove (case‑insensitive)

    # 1. Start with a clean scene
    clear_scene()

    # 2. Import the USD file
    if not os.path.exists(USD_FILE_PATH):
        raise FileNotFoundError(f"USD file not found: {USD_FILE_PATH}")
    import_usd(USD_FILE_PATH)

    # 3. Process geometry. Remove floor and other non‑geometry objects and smooth geometry
    process_geometry(REMOVE_NAME_PATTERN, smooth_subdivision=smooth_subdivision)

    # 4. Transform geometry to world coordinates
    transform_geometry_to_world()

    # 5. Export as GLB without materials
    export_glb_no_materials(GLB_EXPORT_PATH)

    if BLENDER_FILE_PATH:
        bpy.ops.wm.save_as_mainfile(filepath=BLENDER_FILE_PATH)
        print(f"Blender file saved to:\n{BLENDER_FILE_PATH}")

    print(f"GLB exported successfully to:\n{GLB_EXPORT_PATH}")

if __name__ == "__main__":
    main()