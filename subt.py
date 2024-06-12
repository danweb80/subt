import os

from PIL import Image, ImageFont, ImageDraw


image_arq = 'AvatarMaker.png'
text = 'Aula 01 - Pensamentos animados'
img = Image.open(image_arq)
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


pasta = "result"
# Verifique se o pastaetório já existe
if not os.path.exists(pasta):
    os.mkdir(pasta)
img.save(pasta + '//' + image_arq )

