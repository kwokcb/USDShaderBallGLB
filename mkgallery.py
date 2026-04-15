import os
import argparse

IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.tiff'}

def get_image_files(input_folder):
    files = []
    for entry in os.listdir(input_folder):
        path = os.path.join(input_folder, entry)
        if os.path.isfile(path):
            ext = os.path.splitext(entry)[1].lower()
            if ext in IMAGE_EXTENSIONS:
                files.append(entry)
    return sorted(files)

def make_markdown_gallery(image_files, input_folder, columns, size=256):
    md = []
    row = []
    # Add header with centered text like this:
    # |  | |  |  |
    # | :--: | :--: | :--: | :--: |
    row.append(' | ')
    for i in range(columns):
        row.append(' |')
    md.append(' '.join(row))

    row = []
    row.append(' | ')
    for i in range(columns):
        row.append(':--: |')
    md.append(' '.join(row))
    row = []
    for idx, filename in enumerate(image_files):
        title = os.path.splitext(filename)[0]
        rel_path = os.path.join(input_folder, filename)
        # Split words by _ and capitalize them for better display
        title = ' '.join([word.capitalize() for word in title.split('_')])
        # Use HTML for image size control
        cell = f'<img src="{rel_path}" alt="{title}" width="{size}"/><br>{title}'
        row.append(cell)
        if (idx + 1) % columns == 0:
            md.append(' | '.join(row))
            row = []
    if row:
        md.append(' | '.join(row))
    return '\n'.join(md)

def main():
    parser = argparse.ArgumentParser(description='Create a markdown image gallery from a folder of images.')
    parser.add_argument('input_folder', help='Input folder containing images')
    parser.add_argument('-o', '--output_file', help='Output markdown file (default: print to console)', default=None    )
    parser.add_argument('--columns', type=int, default=4, help='Number of images per row (default: 4)')
    parser.add_argument('--size', type=int, default=256, help='Image width in pixels (default: 256)')
    args = parser.parse_args()

    image_files = get_image_files(args.input_folder)
    if not image_files:
        print('No images found in the input folder.')
        return
    gallery_md = make_markdown_gallery(image_files, args.input_folder, args.columns, args.size)
    output_file = args.output_file
    if not output_file:
        input_folder_name = os.path.basename(os.path.normpath(args.input_folder))
        output_file = f'{input_folder_name}_gallery.md' 
    if output_file:
        gallery_md = f'### Image Gallery for {args.input_folder}\n\n' + gallery_md
        with open(output_file, 'w') as f:
            f.write(gallery_md)
        print(f'Markdown gallery written to {output_file}')
    else:   
        print(gallery_md)   

if __name__ == '__main__':
    main()
