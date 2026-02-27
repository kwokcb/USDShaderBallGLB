## USD StandardShaderBall Conversion Utility

This repo contains two scripts to allow:

1. Cloning the current USD Standard Shader Ball scene only.
2. Converting the scene used Blender (bpy) to output a glTF (GLB) file.

### Steps

1. Use `usdball_download.sh` to clone only the shader ball scene into a new repo folder called `StandardShaderBall`.
2. Use `togltf.py` from the root of that repo to create the GLB file called: `standard_shader_ball_scene.glb`

The non shader ball geometry, cameras, and lights are all stripped away. As well no materials are saved.

A Python virtual environment can also be used.
- On non-windows: `bpy_env.sh` sets up a virtual environment and installs `bpy`.
- On Windoows: `bpy_env_win.bat` sets up a virtual environment and installs `bpy`.

### Example

The geometry with just the script conversion is shown below:

| MaterialX Web Viewer (drag geometry into viewer) | Blender |
| :--: | :--: |
| <img width="80%" alt="image" src="https://github.com/user-attachments/assets/97ad1adc-7515-44db-8d49-313c4d52a94a" /> |  <img width="100%" alt="Screenshot 2026-02-27 at 00 33 35" src="https://github.com/user-attachments/assets/a5e05164-eb07-4098-a508-5fe01138429d" /> |

### MaterialX Look Settings

The geometry in the glTF file can be assigned so that the main material to "preview" can be assigned to the outer shell
and ring around the base. The rest can be assigned some "default" material. You can also assign to the "Arnold"shader ball using the same material assignments.

Below is an example look with "base,"core","sss_bars" and "material_surface" the names of geometry in the USD shader ball,
and "Calibration_Mesh" and "Preview_Mesh" the names of geometry in the Arnold shader ball: 

```xml
<look name="look1">
<materialassign name="default" geom="base,core,sss_bars,Calibration_Mesh" material="MY_DEFAULT_MATERIAL" />
 <materialassign name="preview" geom="material_surface,Preview_Mesh" material="MY_PREVIEW_MATERIAL" />
</look>
```

with an example default OpenPBR material:

```xml
<?xml version="1.0"?>
<materialx version="1.39" colorspace="lin_rec709">
  <surfacematerial name="MY_DEFAULT_MATERIAL" type="material">
    <input name="surfaceshader" type="surfaceshader" nodename="open_pbr_surface_surfaceshader" />
  </surfacematerial>
  <open_pbr_surface name="open_pbr_surface_surfaceshader" type="surfaceshader">
    <input name="base_weight" type="float" value="1.0" />
    <input name="base_color" type="color3" value="0.3, 0.3, 0.3" />
    <input name="base_diffuse_roughness" type="float" value="0.2" />
    <input name="base_metalness" type="float" value="0.0" />
    <input name="specular_weight" type="float" value="0.1" />
    <input name="specular_color" type="color3" value="1, 1, 1" />
    <input name="specular_roughness" type="float" value="0.5" />
    <input name="specular_ior" type="float" value="1.5" />
  </open_pbr_surface>
</materialx>
```

Note that the script does not extract out the material from the original USD file though that could be added in the future.

Below is an example using a material from PolyHaven
using the same document but applied to different shader balls.

| USD Shader Ball | Arnold Shader Ball |
| :--: | :--: |
| <img width=100% src="look_example.png"> | <img width=100% src="look_example_2.png"> |

