## USD StandardShaderBall Conversion Utility

This repo contains two scripts to allow:

1. Cloning the current USD Standard Shader Ball scene only.
2. Converting the scene used Blender (bpy) to output a glTF (GLB) file.

### Steps

1. Use `usdball_download.py` to clone only the shader ball scene into a new repo folder called `StandardShaderBall`.
2. Use `togltf.py` from the root of that repo to create the GLB file called: `standard_shader_ball_scene.glb`

The non shader ball geometry, cameras, and lights are all stripped away. As well
no materials are saved.

