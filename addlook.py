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
    input = material.addInput('surfaceshader','surfaceshader')
    shader_name = doc.createValidChildName('shader_' + materialName)
    shader = doc.addNode(shader_category, shader_name, 'surfaceshader')
    input.setConnectedNode(shader)
    return material

def find_materials(doc):
    return doc.getMaterialNodes()

def main():
    parser = argparse.ArgumentParser(description="Add looks to materials in a MaterialX document")
    parser.add_argument(dest='inputFolder', help='Path containing MaterialX files to convert.')
    parser.add_argument('-d', '--defaultShaderCategory', dest='defaultShaderCategory', type=str, default='standard_surface', help="Shader category to use for the default material (default: 'standard_surface')  ")
    parser.add_argument('-o', '--outputFolder', dest='outputFolder', type=str, default="./output", help="Path to the output folder")

    args = parser.parse_args()
    input_folder = args.inputFolder
    output_folder = args.outputFolder
    default_shader_category = args.defaultShaderCategory

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
            

if __name__ == "__main__":
    main()