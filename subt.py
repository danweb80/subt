import os

from PIL import Image, ImageFont, ImageDraw

dir_destino = "result/"
dir_origem = "origin/"
font_path = './fonts/Rubik-Regular.ttf'
color = '#b4963c'


image_arq = 'Capa aula 1200x768.png'
text = 'O Início da Carreira Psicanalítica de Freud #1'.upper()
left_pos = 120
right_pos = 200
font_size = 60

img = Image.open(dir_origem + image_arq)
# print(img.size)
font = ImageFont.truetype(font_path, font_size)
draw = ImageDraw.Draw(img)
image_widht, image_height = img.size
left, top, right, bottom = bbox = font.getbbox(text)
# bbox = font.getbbox(text)
print(bbox)
text_widht = right - left
text_height = bottom - top
print("text_height: ", text_height)

draw.text(
    #((image_widht -text_widht) / 2, (image_height - text_height) / 2),
    (left_pos,(3*image_height/4)-bottom),
    # (100,500),
    text,
    fill=color,
    font=font
)


# Verifique se o pastaetório já existe
if not os.path.exists(dir_destino):
    os.mkdir(dir_destino)
img.save(dir_destino + '//' + image_arq )

