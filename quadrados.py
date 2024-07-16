import cv2
import numpy as np

def detectar_quinas_tabuleiro(imagem_path, tamanho_tabuleiro=(7, 7)):
    # Carregar a imagem
    imagem = cv2.imread(imagem_path)
    if imagem is None:
        print("Erro ao carregar a imagem.")
        return

    # Converter para escala de cinza
    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Encontrar as quinas do tabuleiro de xadrez
    ret, quinas = cv2.findChessboardCorners(cinza, tamanho_tabuleiro, None)

    if ret:
        # Refinar as coordenadas das quinas
        quinas = cv2.cornerSubPix(cinza, quinas, (11, 11), (-1, -1), 
                                  (cv2.TermCriteria_EPS + cv2.TermCriteria_MAX_ITER, 30, 0.001))
        
        # Inicializar a imagem para desenhar as caixas e as coordenadas dos retângulos
        img_box = imagem.copy()
        boxes = np.zeros((tamanho_tabuleiro[1], tamanho_tabuleiro[0], 4), dtype=int)

        # Preencher as caixas e desenhar os retângulos
        for i in range(tamanho_tabuleiro[1] - 1):
            for j in range(tamanho_tabuleiro[0] - 1):
                # Calcular os índices dos quatro cantos de cada casa
                top_left = i * tamanho_tabuleiro[0] + j
                top_right = top_left + 1
                bottom_left = top_left + tamanho_tabuleiro[0]
                bottom_right = bottom_left + 1

                # Obter as coordenadas dos quatro cantos e converter para inteiros
                pontos = [tuple(map(int, quinas[top_left][0])),
                          tuple(map(int, quinas[top_right][0])),
                          tuple(map(int, quinas[bottom_right][0])),
                          tuple(map(int, quinas[bottom_left][0]))]

                # Definir a caixa para a casa
                boxes[i, j] = [pontos[0][0], pontos[0][1], pontos[2][0], pontos[2][1]]

        # Desenhar as caixas ao redor de cada casa e adicionar texto
        for i in range(tamanho_tabuleiro[1] - 1):
            for j in range(tamanho_tabuleiro[0] - 1):
                box1 = boxes[i, j]
                cv2.rectangle(img_box, (int(box1[0]), int(box1[1])), (int(box1[2]), int(box1[3])), (255, 0, 0), 2)
                cv2.putText(img_box, "({},{})".format(i, j), (int(box1[2]) - 70, int(box1[3]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Mostrar a imagem com as caixas desenhadas
        cv2.imshow("Casas do Tabuleiro", img_box)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Não foi possível encontrar o tabuleiro de xadrez na imagem.")

# Caminho para a imagem do tabuleiro de xadrez
imagem_path = "tabuleiroxadrezVerde.png"
detectar_quinas_tabuleiro(imagem_path, tamanho_tabuleiro=(7, 7))
