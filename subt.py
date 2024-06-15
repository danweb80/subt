import os, textwrap, csv

import yaml
from PIL import Image, ImageFont, ImageDraw

caminho = (os.getcwd())
dir_destino = "result"
dir_origem = "origin"

# ABRE O ARQUIVO DE CONFIGURAÇÃO YAML
# PARA PEGAR OS FORMATOS DE IMAGEM
with open('config.yaml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

font_path = './fonts/'+config['fonte']['nome']
color = config['fonte']['color']
formatos = config['formatos']

# ABRE O CSV COM A LISTA DE CUROSOS/MÓDULOS/AULAS
# ITERA E CLASSIFICA CADA ITEM PARA PROCURA-LOS NA PASTA
with open(dir_origem+'/modulos.csv', 'r') as csv_file:
    modulos = csv.reader(csv_file)
    
    curso_atual_num = 0
    modulo_atual_num = 0
    aula_atual_num = 0
    curso_atual_nome = ''
    modulo_atual_nome = ''
    aula_atual_nome = ''
    for linha in modulos:
        # print (linha)
        if 'CURSO' in linha[0]:
            curso_atual_num += 1    # indica que um novo curso foi achado
            curso_atual_nome = ''   # indica que não sabemos o nome e na prox linha o encontraremos
            modulo_atual_num = 0    # zera o módulo 
            modulo_atual_nome = ''
        
        elif curso_atual_num and not curso_atual_nome:
            # pega o NOME do CURSO
            curso_atual_nome = linha[0]
            print(f'>> Curso {curso_atual_num}: {curso_atual_nome} <<')
        
        #elif curso_atual_num and curso curso_atual_nome # PODERIA SER SÓ UM ELSE  ????
        elif not modulo_atual_nome:
            if linha[0]:
                #pega o NOME do novo MODULO
                modulo_atual_nome = linha[0]
                modulo_atual_num += 1
                aula_atual_num = 0
                print(f'\tMódulo {modulo_atual_num}: {modulo_atual_nome}')
        elif not linha[0]:
                # linha em branco, troca de módulo
                modulo_atual_nome = ''
        else:
            #pega o NOME da AULA
            aula_atual_nome = linha[0]
            aula_atual_num += 1
            print(f'\t\tAula {aula_atual_num}: {aula_atual_nome}')
            
            ###############################
            ######   Fazer os PARANAUÊS
            ###############################

            # procurar pasta com o nome do curso
            list_dir = os.listdir(dir_origem)
            for dir in list_dir:
                dir_path = caminho+'/'+dir_origem+'/'+dir
                if os.path.isdir(dir_path):
                    if curso_atual_nome in dir:
                        # achei a pasta, entra nela então...
                        list_dir_curso = os.listdir(dir_origem+'/'+dir)
                        for arq in list_dir_curso:
                            if os.path.isfile(dir_path+'/'+arq):
                                # Neste caso estou procurando arquivos que começam com o texto 'Capa aula'
                                if 'Capa aula' in arq:
                                    # Faz a varredura para encontrar os arquivos de cada formato definido no config.yaml
                                    for formato in formatos:
                                        if formato in arq:
                                            print(f'Formato {formato} encontrado no arquivo {arq}')
                                            text = aula_atual_nome.strip().upper()
                                                                                        
                                            # Prepara IMAGEM
                                            img = Image.open(dir_path+'/'+arq)
                                            print('IMAGE SIZE: ', img.size)
                                            draw = ImageDraw.Draw(img)
                                            image_width, image_height = img.size
                                            # Pega os dados do yaml e ajsuta para o tamanho da imagem para determinar a box do texto
                                            top_pos =   int(config['formatos'][formato]['top_pos'] * image_height / 100)
                                            bottom_pos = int((100 - config['formatos'][formato]['bottom_pos']) * image_height / 100)
                                            text_box_height = bottom_pos - top_pos
                                            left_pos  = int(config['formatos'][formato]['left_pos'] * image_width / 100)
                                            right_pos = int((100 - config['formatos'][formato]['right_pos']) * image_width / 100)
                                            text_box_width = right_pos - left_pos
                                            # print(f'top: {top_pos}, bottom: {bottom_pos} - left: {left_pos}, right: {right_pos}')
                                            # print(f'Box_Width: {text_box_width} - Box_Heght: {text_box_height}')

                                            # Prepara FONTE do texto
                                            font_size = config['formatos'][formato]['font_size']
                                            font = ImageFont.truetype(font_path, font_size)
                                            left, top, right, bottom = font.getbbox(text)
                                            text_width = right - left
                                            text_height = bottom

                                            teste = ''
                                            max_text_len = len(text)
                                            # vai fazendo wrap e diminuindo max_len enquanto couber na altura
                                            while text_width > text_box_width:
                                                max_text_len -= 1
                                                teste = textwrap.wrap(text, width=max_text_len)
                                                # verificar nova largura e altura
                                                text_width = 0
                                                text_height = 0
                                                for linha in teste:
                                                    # pega o maior valor entre as larguras
                                                    left, top, right, bottom = font.getbbox(linha)
                                                    if text_width < right - left:
                                                        text_width = right - left
                                                    # pega a soma das alturas
                                                    text_height += bottom
                                                teste_linhas = len(teste)
                                                # print(f'Reduz max_len .... max: {max_text_len} - linhas: {teste_linhas} - width: {text_width} - height: {text_height} - font_size: {font_size} --- {teste} ')
                                                # input('OK! Texto inserido!')
                                                
                                            while text_height > text_box_height or text_width > text_box_width:
                                                font_size -= 1
                                                font = ImageFont.truetype(font_path, font_size)
                                                teste = textwrap.wrap(text, width=max_text_len)
                                                text_width = 0
                                                text_height = 0
                                                for linha in teste:
                                                    # pega o maior valor entre as larguras
                                                    left, top, right, bottom = font.getbbox(linha)
                                                    if text_width < right - left:
                                                        text_width = right - left
                                                    # pega a soma das alturas
                                                    text_height += bottom
                                                # faz o ajuste fino, compensando os novos ajustes 
                                                if text_width < text_box_width:
                                                    max_text_len += 1
                                                elif text_width > text_box_width:
                                                    max_text_len -= 1
                                                teste_linhas = len(teste)
                                                # print(f'Reduz fonte.... max: {max_text_len} - linhas: {teste_linhas} - width: {text_width} - font_size: {font_size} --- {teste} ')
                                                # input()

                                            line_thikness = config['formatos'][formato]['line_thikness']
                                            line_space = config['formatos'][formato]['line_space']

                                            if teste:
                                                for linha in teste:
                                                    draw.text((left_pos,top_pos), linha, fill=color, font=font) # anchor='lb', stroke_width=2, stroke_fill='black'
                                                    top_pos = top_pos + bottom + 5
                                                line_height = top_pos + line_space #(image_height*5/100)
                                            else:
                                                draw.text((left_pos,top_pos), text, fill=color, font=font) # anchor='lb', stroke_width=2, stroke_fill='black'
                                                line_height = top_pos + bottom + line_space #(image_height*5/100)
                                            
                                            # DESENHA A LINHA
                                            if(line_thikness):
                                                line_width = text_width + left_pos + (image_width*3/100)
                                                draw.line((0, line_height, line_width, line_height), fill=color, width=line_thikness)

                                            # SALVA A IMAGEM
                                            if not os.path.exists(dir_destino+'/'+dir+'/'+modulo_atual_nome):   # Verifique se o pastaetório já existe
                                                os.makedirs (dir_destino+'/'+dir+'/'+modulo_atual_nome)
                                            img.save(dir_destino+'/'+dir+'/'+modulo_atual_nome+'/'+aula_atual_nome+' ['+formato+']'+'.png')

                                        
