Lẽ um .csv com cursos modulos e aulas e imagens base em vários formatos e cria capas de aulas inserindo o texto de cada aula na respectiva imagem conforme as configurações descritas em config.yaml


O diretorio de origem deve conter 
    - o arquivo .csv com a lista de cursos, modulos e aulas na coluna 1
        - o curso será identificado pela palavra 'CURSO' na célula
        - o modulo por ter uma celula em branco acima
        -as aulas estando entre um modulo e outro
    - um subdiretorio ./origin com as pastas (mesmo nome do curso) com os arquivos de capa de "Cpa aula" e o texto do formato
    - o arquivo config.yaml com as configurações de cada formato (posição, tamanhos do texto etc)
    - um subdiretorio ./fonts com o arquivo .ttf da fonte a ser usada indicana no config.yaml

O script criará um subdiretório ./results com subsdiretorios baseados em curso e modulo