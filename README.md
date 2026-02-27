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

