import os

from PIL import Image, ImageFont, ImageDraw

dir_destino = "result/"
dir_origem = "origin/"
font_path = './fonts/Rubik-Regular.ttf'
color = '#b4963c'


image_arq = 'Capa aula 1200x768.png'
text = 'O Início da Carreira '.upper()
left_pos = 120  # PIXEL
vert_pos  = 75  # PERCENTUAL %
right_pos = 200 # PIXEL
font_size = 60

img = Image.open(dir_origem + image_arq)
print('IMAGE SIZE: ', img.size)
font = ImageFont.truetype(font_path, font_size)
draw = ImageDraw.Draw(img)
image_width, image_height = img.size
left, top, right, bottom = bbox = font.getbbox(text)
# bbox = font.getbbox(text)
print("text_box(bbox): ", bbox)
text_width = right - left
text_height = bottom - top
print("text_width: ", text_width)
print("text_height: ", text_height)
top_pos = round(image_height*vert_pos/100) - bottom 
print("top_pos: ", top_pos)
draw.text(
    #((image_width -text_width) / 2, (image_height - text_height) / 2),
    (left_pos,top_pos),
    # (100,500),
    text,
    fill=color,
    font=font,
    # stroke_width=2,
    # stroke_fill='black'
)
line_height = top_pos+text_height+30
line_width = text_width + left_pos + 100
draw.line((0,line_height,line_width,line_height), fill=color, width=5)

# Verifique se o pastaetório já existe
if not os.path.exists(dir_destino):
    os.mkdir(dir_destino)
img.save(dir_destino + '//' + image_arq )

