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
        
        # Converter as quinas para uma matriz 2D para facilitar a manipulação
        quinas = quinas.reshape(tamanho_tabuleiro[1], tamanho_tabuleiro[0], 2)

        # Inicializar a imagem para desenhar as caixas e as coordenadas dos retângulos
        img_box = imagem.copy()
        boxes = np.zeros((8, 8, 4), dtype=int)
        pontos = np.zeros((9, 9, 2), dtype=int)  # Usando uma matriz 9x9 para incluir todos os pontos

        # Preencher os pontos internos
        pontos[1:8, 1:8] = quinas

        # Extrapolar os pontos externos
        for i in range(1, 8):
            pontos[0, i] = 2 * pontos[1, i] - pontos[2, i]
            pontos[8, i] = 2 * pontos[7, i] - pontos[6, i]
            pontos[i, 0] = 2 * pontos[i, 1] - pontos[i, 2]
            pontos[i, 8] = 2 * pontos[i, 7] - pontos[i, 6]

        # Cálculo dos cantos do tabuleiro
        pontos[0, 0] = 2 * pontos[1, 1] - pontos[2, 2]
        pontos[0, 8] = 2 * pontos[1, 7] - pontos[2, 6]
        pontos[8, 0] = 2 * pontos[7, 1] - pontos[6, 2]
        pontos[8, 8] = 2 * pontos[7, 7] - pontos[6, 6]

        # Preencher boxes com as coordenadas dos pontos
        for i in range(8):
            for j in range(8):
                boxes[i, j, 0] = pontos[i, j, 0]
                boxes[i, j, 1] = pontos[i, j, 1]
                boxes[i, j, 2] = pontos[i + 1, j + 1, 0]
                boxes[i, j, 3] = pontos[i + 1, j + 1, 1]

        # Desenhar as caixas ao redor de cada casa e adicionar texto
        for i in range(8):
            for j in range(8):
                box1 = boxes[i, j]
                cv2.rectangle(img_box, (box1[0], box1[1]), (box1[2], box1[3]), (255, 0, 0), 2)
                cv2.putText(img_box, "({},{})".format(i, j), (box1[2] - 70, box1[3] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Mostrar a imagem com as caixas desenhadas
        cv2.imshow("Casas do Tabuleiro", img_box)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Não foi possível encontrar o tabuleiro de xadrez na imagem.")

# Caminho para a imagem do tabuleiro de xadrez
imagem_path = "tabuleiroxadrezVerde.png"
detectar_quinas_tabuleiro(imagem_path, tamanho_tabuleiro=(7, 7))
