import MaterialX as mx
import argparse
import os

def add_look(doc):
    # Create a look for the material.
    look_name = doc.createValidChildName('look')
    look = doc.addLook(look_name)
    return look

def add_material_assignment(materialName, defaultName, look):
    # Create a look for the material.
    default_name = 'default'
    assign = look.getMaterialAssign('default')
    count = 1
    while assign:
        default_name = 'default' + str(count)
        assign = look.getMaterialAssign(default_name)
        count += 1
    assign = look.addMaterialAssign(default_name, defaultName)
    assign.setGeom('base,core,sss_bars,Calibration_Mesh')
    assign = look.getMaterialAssign(materialName)
    count = 1
    prevew_name = 'preview'
    assign = look.getMaterialAssign(prevew_name)
    while assign:
        prevew_name = 'preview' + str(count)
        assign = look.getMaterialAssign(prevew_name)
        count += 1
    print('Adding material assignment for material:', materialName, 'with name:', prevew_name)
    assign = look.addMaterialAssign(prevew_name, materialName)
    assign.setGeom('material_surface,Preview_Mesh')
    
def add_default_material(doc, materialName, shader_category='standard_surface'):
    # Create a default material for the material.
    material_name = doc.createValidChildName(materialName)
    material = doc.addMaterialNode(material_name)
    shader_name = doc.createValidChildName('shader_' + materialName)
    shader = doc.addNode(shader_category, shader_name, 'surfaceshader')
    shader_input = shader.addInput('base_color', 'color3')
    shader_input.setValue(mx.Color3(0.2, 0.2, 0.2))
    shader_input = shader.addInput('specular_roughness', 'float')
    shader_input.setValue(1.0)
    input = material.addInput('surfaceshader','surfaceshader')
    input.setConnectedNode(shader)


    return material

def find_materials(doc):
    return doc.getMaterialNodes()

def render_material(render_string, geometry_file, output_path, output_image_path, input_image_path=None):
    '''
    Render using ther provided render string
    @param render_string: a string with the render command, with %g for geometry file, %m for material file, and %o for output image file
    @param geometry_file: path to the geometry file to use for rendering
    @param output_path: path to the material file to use for rendering (will replace %m in the render string)
    @param output_image_path: path to the output image file (will replace %o in the render string)
    @param input_image_path: path to the input image file (will replace %p in the render string)
    '''
    if not render_string:
        return
    
    # Example:
    # python addlook.py ./StandardShaderBall/full_assets/StandardShaderBall/example_materials 
    #   -r "MaterialXView --material %m --mesh %g --screenWidth 512 --screenHeight 512 --captureFilename %o
    #       --cameraPosition 6.53154,14.5,17.9485 --cameraZoom 6" 
    #   --g ./standard_shader_ball_scene.glb    
    #
    # Example:
    # python addlook.py ../bernard_materialx/resources/Materials/Examples/StandardSurface 
    #   -r "~/work/bernard_materialx/build/bin/MaterialXView --material %m --mesh %g --path %p
    #   --screenWidth 480 --screenHeight 480 --captureFilename %o  --cameraPosition 7.5,17.0,17.0 
    #   --cameraZoom 6 --shadowMap true --lightRotation 20 --screenColor 0.6,0.6,0.6" 
    #   --g ./standard_shader_ball_scene_smooth.glb -o resource_materials

    # Fill in %g with GLB file name, and %m with material file name
    render_command = render_string.replace('%g', geometry_file)
    render_command = render_command.replace('%m', output_path)
    # Fill in %o with output image file name (same as material file name but with .png extension)
    output_image_path = os.path.splitext(output_path)[0] + '.png'
    render_command = render_command.replace('%o', output_image_path)
    if input_image_path:
        render_command = render_command.replace('%p', input_image_path)
    print('Rendering with command:', render_command)
    try:
        os.system(render_command)
    except Exception as e:
        print('Error occurred while rendering:', e)

def main():
    parser = argparse.ArgumentParser(description="Add looks to materials in a MaterialX document")
    parser.add_argument(dest='inputFolder', help='Path containing MaterialX files to convert.')
    parser.add_argument('-d', '--defaultShaderCategory', dest='defaultShaderCategory', type=str, default='standard_surface', help="Shader category to use for the default material (default: 'standard_surface')  ")
    parser.add_argument('-o', '--outputFolder', dest='outputFolder', type=str, default="./output", help="Path to the output folder")
    parser.add_argument('-r', '-renderString', dest='renderString', type=str, help="Render the materials")
    parser.add_argument('-g', '--geometryFile', dest='geometryFile', type=str, help="Path to the geometry file to use for rendering")

    args = parser.parse_args()
    input_folder = args.inputFolder
    output_folder = args.outputFolder
    default_shader_category = args.defaultShaderCategory
    render_string = args.renderString

    geometry_file = args.geometryFile
    if render_string:
        if not geometry_file or not os.path.exists(geometry_file):
            print('Geometry file is required for rendering and must exist:', geometry_file)
            exit(-1)

    # create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    for material_file in os.listdir(input_folder):
        print('Checking file:', material_file)
        if material_file.endswith(".mtlx"):
            input_path = os.path.join(input_folder, material_file)
            output_path = os.path.join(output_folder, material_file)
            doc = mx.createDocument()            
            print('Processing file:', input_path)
            mx.readFromXmlFile(doc, input_path)

            materials = find_materials(doc)
            material_count = len(materials)
            if material_count == 0:
                print('No materials found in file:', input_path)
                continue

            write_separate_materials =  material_count > 1

            mat_doc = doc
            mat_output_path = output_path

            if not write_separate_materials:
                # Create one default material
                default_material = add_default_material(mat_doc, 'default', default_shader_category )
                # Add a look
                look = add_look(mat_doc)

            for material in materials:
                if write_separate_materials:
                    mat_output_path = output_path.replace('.mtlx', '_' + material.getName() + '.mtlx')
                    mat_doc = mx.createDocument()
                    mat_doc.copyContentFrom(doc)
                    default_material = add_default_material(mat_doc, 'default', default_shader_category )
                    look = add_look(mat_doc)
                    print('- Add assignment for material:', material.getName())
                    add_material_assignment(material.getName(), default_material.getName(), look)
                    print('Writing output file:', mat_output_path)
                    mx.writeToXmlFile(mat_doc, mat_output_path)
                    render_material(render_string, geometry_file, 
                                    mat_output_path, 
                                    os.path.splitext(mat_output_path)[0] + '.png',
                                    input_folder)   
                else:
                    print('- Add assignment for material:', material.getName())
                    add_material_assignment(material.getName(), default_material.getName(), look)

            if not write_separate_materials:
                print('Writing output file:', mat_output_path)
                mx.writeToXmlFile(mat_doc, mat_output_path)
                render_material(render_string, geometry_file, mat_output_path, 
                                os.path.splitext(mat_output_path)[0] + '.png',
                                input_folder)
           
if __name__ == "__main__":
    main()