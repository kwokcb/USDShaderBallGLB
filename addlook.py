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
    assign = look.addMaterialAssign('default', defaultName)
    assign.setGeom('base,core,sss_bars,Calibration_Mesh')
    assign = look.addMaterialAssign('preview', materialName)
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
            if len(materials) == 0:
                print('No materials found in file:', input_path)
                continue

            # Create one default material
            default_material = add_default_material(doc, 'default', default_shader_category )
            look = add_look(doc)
            for material in materials:
                print('- Add assignment for material:', material.getName())
                add_material_assignment(material.getName(), default_material.getName(), look)

            print('Writing output file:', output_path)
            mx.writeToXmlFile(doc, output_path)


            # Example:
            # python addlook.py ./StandardShaderBall/full_assets/StandardShaderBall/example_materials 
            #   -r "MaterialXView --material %m --mesh %g --screenWidth 512 --screenHeight 512 --captureFilename %o" 
            #   --g ./standard_shader_ball_scene.glb
            if render_string:
                # Fill in %g with GLB file name, and %m with material file name
                render_command = render_string.replace('%g', geometry_file)
                render_command = render_command.replace('%m', output_path)
                # Fill in %o with output image file name (same as material file name but with .png extension)
                output_image_path = os.path.splitext(output_path)[0] + '.png'
                render_command = render_command.replace('%o', output_image_path)
                print('Rendering with command:', render_command)
                try:
                    os.system(render_command)
                except Exception as e:
                    print('Error occurred while rendering:', e)

if __name__ == "__main__":
    main()