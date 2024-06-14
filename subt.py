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
color = '#'+config['fonte']['color']
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
                                if 'Capa aula' in arq:
                                    for formato in formatos:
                                        if formato in arq:
                                            # print(f'Formato {formato} encontrado no arquivo {arq}')
                                            text = aula_atual_nome.strip().upper()
                                            max_text_len = len(text)
                                            left_pos  = config['formatos'][formato]['left_pos']
                                            vert_pos  = config['formatos'][formato]['vert_pos']
                                            right_pos = config['formatos'][formato]['right_pos']
                                            font_size = config['formatos'][formato]['font_size']
                                            line_thikness = config['formatos'][formato]['line_thikness']
                                            line_space = config['formatos'][formato]['line_space']

                                            # Prepara IMAGEM
                                            img = Image.open(dir_path+'/'+arq)
                                            # print('IMAGE SIZE: ', img.size)
                                            draw = ImageDraw.Draw(img)
                                            image_width, image_height = img.size
                                            # Prepara FONTE do texto
                                            font = ImageFont.truetype(font_path, font_size)
                                            left, top, right, bottom = font.getbbox(text)
                                            text_width = right - left
                                            text_height = bottom

                                            # Se o texto não couber, quebra a linha (insere um \n no meio)
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
                                            
                                            if(line_thikness):
                                                line_height = top_pos + text_height + line_space #(image_height*5/100)
                                                line_width = text_width + left_pos + (image_width*5/100)
                                                draw.line((0, line_height, line_width, line_height), fill=color, width=line_thikness)

                                            # SALVA A IMAGEM
                                            if not os.path.exists(dir_destino+'/'+dir+'/'+modulo_atual_nome):   # Verifique se o pastaetório já existe
                                                os.makedirs (dir_destino+'/'+dir+'/'+modulo_atual_nome)
                                            img.save(dir_destino+'/'+dir+'/'+modulo_atual_nome+'/'+aula_atual_nome+' ['+formato+']'+'.png')

                                        
