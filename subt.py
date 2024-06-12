import os

from PIL import Image, ImageFont, ImageDraw

dir_destino = "result"
dir_origem = "origin"

image_arq = 'AvatarMaker.png'
text = 'Aula 01 - Pensamentos animados'
img = Image.open(dir_origem + '//' + image_arq)
# font = ImageFont.truetype('arial.ttf', 20)
# draw = ImageDraw.Draw(img)
# iw, ih = img.size
# fw, fh = font.getsize(text)
# draw.text(
#     ((iw -fw) / 2, (ih - fh) / 2),
#     text,
#     fill='red',
#     fonto=font
# )


# Verifique se o pastaetório já existe
if not os.path.exists(dir_destino):
    os.mkdir(dir_destino)
img.save(dir_destino + '//' + image_arq )

