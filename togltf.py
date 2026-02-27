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
    bpy.ops.wm.usd_import(filepath=filepath,
                          import_materials=False)
    
def remove_non_geometry(geom_patterns):
    """
    Remove objects that are not geometry as well as geometry provided as argument
    @param geom_patterns: list of names of meshes to delete
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

        # 2. For meshes, check if the name indicates it's a floor
        name_lower = obj.name.lower()
        for pattern in geom_patterns:
            if pattern in name_lower:
                print('Remove object:', obj.name)
                objects_to_delete.append(obj)
                break   # No need to check other patterns

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
    argparser.add_argument("--usd", type=str, default="./full_assets/StandardShaderBall/standard_shader_ball_scene.usda", help="Path to the input USD file")
    argparser.add_argument("--glb", type=str, default="./standard_shader_ball_scene.glb", help="Path to the output GLB file")
    args = argparser.parse_args()

    USD_FILE_PATH = args.usd
    GLB_EXPORT_PATH = args.glb

    # Geometry to remove
    REMOVE_NAME_PATTERN = ["grid", "back", "backplane", "backplane.001", "front", "right", "top", "left"]          # Names of meshes to remove (case‑insensitive)

    # 1. Start with a clean scene
    clear_scene()

    # 2. Import the USD file
    if not os.path.exists(USD_FILE_PATH):
        raise FileNotFoundError(f"USD file not found: {USD_FILE_PATH}")
    import_usd(USD_FILE_PATH)

    # 3. Remove floor and other non‑geometry objects
    remove_non_geometry(REMOVE_NAME_PATTERN)

    # 4. Transform geometry to world coordinates
    transform_geometry_to_world()

    # 5. Export as GLB without materials
    export_glb_no_materials(GLB_EXPORT_PATH)

    print(f"GLB exported successfully to:\n{GLB_EXPORT_PATH}")

if __name__ == "__main__":
    main()