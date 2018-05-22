import os, sys, subprocess
import click
from PIL import ImageColor, Image

#make sure the image is good
def check_image(image_file):
    #does the file exist?
    if not os.path.isfile(image_file):
        print('File not found')
        exit()

    #is the file an image?
    if not image_file.endswith(('.jpg', '.jpeg')):
        print('Filetype not supported bucko!')

    #see if image is loadable
    try:
        im = Image.open(image_file)
        return im
    except:
        print('Something broke (probably your file tbh)')
        exit()


#counting generator
def simple_generator(x):
    for i in range(x):
        yield i


#automatically open the html file when the script is done
def open_when_done(output_file):
    if sys.platform == "win32":
        os.startfile(output_file)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, output_file])


#collect command line args/flags for the script
@click.command()
@click.option('--image_file', '-i', prompt='Image File', help='Image File')
@click.option('--output_file', '-o', default='image.html', help='Output File')
def start_script(image_file, output_file):

    #verify the image and get it's size
    im = check_image(image_file)
    W = im.width
    H = im.height
    print('\nWorking...')

    #make the output html file
    with open(output_file, 'w') as file:
        def fw(to_write):
            file.write(to_write)

        #use an html file as a template for the start of the site
        with open('grid.html', 'r') as template:
            fw(template.read())

        #wrap rows in <tr> tags, and wrap the table in <table> tags
        def table_tags(f):
            def inner(col='', opening_tag='<table>', closing_tag='</table>'):
                fw(opening_tag)
                f(col)
                fw(closing_tag)
            return inner

        @table_tags
        def table(null):
            for col in simple_generator(H):
                row(col)

        @table_tags
        def row(col, opening_tag='<tr>', closing_tag='</tr>'):
            for row in simple_generator(W):
                pixel_color = im.getpixel((row, col))
                fw(f'<td style="background-color:rgb{pixel_color}"></td>')

        table()
        print('\n\nDone!\n\n')
        open_when_done(output_file)


if __name__ == '__main__':
    start_script()
