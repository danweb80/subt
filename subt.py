import os, textwrap

from PIL import Image, ImageFont, ImageDraw

dir_destino = "result/"
dir_origem = "origin/"
font_path = './fonts/Rubik-Regular.ttf'
color = '#b4963c'


image_arq = 'Capa aula 1200x768.png'
text = 'O Início da Carreira Psicanalítica de Freud #1'.strip().upper()
max_text_len = len(text)
left_pos = 120  # PIXEL
vert_pos  = 75  # PERCENTUAL %
right_pos = 200 # PIXEL
font_size = 68

# Prepara IMAGEM
img = Image.open(dir_origem + image_arq)
print('IMAGE SIZE: ', img.size)
draw = ImageDraw.Draw(img)
image_width, image_height = img.size
# Prepara FONTE do texto
font = ImageFont.truetype(font_path, font_size)
left, top, right, bottom = font.getbbox(text)
text_width = right - left
text_height = bottom - top

# Se o texto não couber quebra linha (insere um \n no meio)
# achar quantos caracteres (text length) cabem no espaço destinado a uma linha de texto (text width))
if (left_pos + text_width) > (image_width - right_pos):
    teste = text
    while (left_pos + text_width) > (image_width - right_pos):
        teste = teste[:-1]
        max_text_len = len(teste)
        left, top, right, bottom = font.getbbox(teste)
        text_width = right - left
    text = textwrap.fill(text, width=max_text_len)
    text_height = text_height * 2

top_pos = int(image_height*vert_pos/100) - bottom 

draw.multiline_text(
    #((image_width -text_width) / 2, (image_height - text_height) / 2), # CENTRALIZADO
    (left_pos,top_pos),
    text,
    fill=color,
    font=font,
    # anchor='lb', #left bottom === não funciona no multiline :(
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

