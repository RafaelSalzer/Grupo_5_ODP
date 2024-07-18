import cv2
import os
import numpy as np
# Lista para armazenar os pontos clicados
pontos_clicados = []

def capturar_pontos(event, x, y, flags, param):
    global pontos_clicados
    if event == cv2.EVENT_LBUTTONDOWN:
        pontos_clicados.append((x, y))
        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Imagem", image)

def warp_perspective_tabuleiro(image, pontos_ordenados):
    # Definir os pontos de destino para a transformação de perspectiva
    largura_max = 800  # Defina a largura desejada da imagem transformada
    altura_max = 800  # Defina a altura desejada da imagem transformada
    
    pontos_destino = np.array([
        [0, 0],
        [largura_max - 1, 0],
        [largura_max - 1, altura_max - 1],
        [0, altura_max - 1]], dtype="float32")
    
    # Calcular a matriz de transformação de perspectiva
    matriz = cv2.getPerspectiveTransform(np.array(pontos_ordenados, dtype="float32"), pontos_destino)
    
    # Aplicar a transformação de perspectiva
    warp = cv2.warpPerspective(image, matriz, (largura_max, altura_max))
    
    return warp, matriz

def detectar_cantos_casas(image):
    altura, largura = image.shape[:2]
    tamanho_casa = altura // 8
    
    cantos_casas = []
    for i in range(8):
        for j in range(8):
            x = j * tamanho_casa
            y = i * tamanho_casa
            cantos_casas.append((x, y, x + tamanho_casa, y + tamanho_casa))

    print(cantos_casas)
    return cantos_casas

def desenhar_roi_original(image, cantos_casas, matriz_inversa):
    for (x1, y1, x2, y2) in cantos_casas:
        pontos = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]], dtype="float32")
        pontos = cv2.perspectiveTransform(np.array([pontos]), matriz_inversa)[0]
        pontos = pontos.astype(int)
        cv2.polylines(image, [pontos], isClosed=True, color=(255, 0, 0), thickness=1)
    return image

def processa_e_analisa_imagem(imagem, jogada):  
    
    # Processamento da imagem
    imgCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    imgTh = cv2.adaptiveThreshold(imgCinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgBlur = cv2.medianBlur(imgTh, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDil = cv2.dilate(imgBlur, kernel)

    # Criar a pasta 'fotos_com_ROIs' se ela não existir
    if not os.path.exists('fotos_processadas'):
        os.makedirs('fotos_processadas')
    
    # Salvar a imagem com as ROIs na pasta
    caminho_para_salvar = os.path.join('fotos_processadas', f'foto_processada_jogada_{jogada}.png')
    cv2.imwrite(caminho_para_salvar, imgDil)
    
    return imgDil
    
  
def inicializar_tabuleiro():
    # Cria uma matriz 8x8 inicializada com zeros
    posicoes = [['   ' for _ in range(8)] for _ in range(8)]

    #preencher os peoes pretos
    for j in range(8):
        posicoes[1][j] = 'P_P'

    #preencher os torres prertas 
    posicoes[0][0] = 'T_P' 
    posicoes[0][7] = 'T_P'

    #preencher os cavalos pretos
    posicoes[0][1] = 'C_P'
    posicoes[0][6] = 'C_P'

    #preencher os bispos pretos
    posicoes[0][2] = 'B_P'
    posicoes[0][5] = 'B_P'

    #preencher a rainha preta
    posicoes[0][3] = 'Q_P'

    #preencher o rei preto
    posicoes[0][4] = 'K_P'

    #preencher os peoes brancos
    for j in range(8):
        posicoes[6][j] = 'P_B'

    #preencher os torres brancas
    posicoes[7][0] = 'T_B'
    posicoes[7][7] = 'T_B'

    #preencher os cavalos brancos
    posicoes[7][1] = 'C_B'
    posicoes[7][6] = 'C_B'

    #preencher os bispos brancos
    posicoes[7][2] = 'B_B'
    posicoes[7][5] = 'B_B'

    #preencher a rainha branca
    posicoes[7][3] = 'Q_B'

    #preencher o rei branco
    posicoes[7][4] = 'K_B'

    return posicoes

def main():
    #Coloca as pecas na posicao inicial
    tabuleiro = inicializar_tabuleiro()
    for linha in tabuleiro:
        print(linha)

    # Inicializa a captura de vídeo da webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro ao abrir a câmera")
        exit()

    # Cria um diretório para armazenar as fotos, se não existir
    if not os.path.exists('fotos_jogadas'):
        os.makedirs('fotos_jogadas')

    # Inicializa o contador de jogadas
    jogada = 1

    # Lista de ROIs (Regiões de Interesse) para capturar as peças de xadrez
    rois = [
    (174, 71, 41, 41),
    (214, 73, 42, 37),
    (257, 71, 41, 37),
    (299, 68, 42, 39),
    (343, 67, 44, 38),
    (387, 66, 45, 36),
    (433, 63, 46, 39),
    (477, 61, 49, 38),
    (174, 113, 39, 39),
    (172, 155, 39, 39),
    (172, 197, 38, 40),
    (168, 238, 40, 47),
    (166, 288, 41, 43),
    (164, 333, 42, 45),
    (162, 379, 43, 46),
    (216, 113, 40, 38),
    (215, 153, 40, 43),
    (211, 197, 41, 44),
    (259, 112, 39, 40),
    (257, 152, 41, 42),
    (256, 199, 42, 36),
    (300, 110, 42, 40),
    (299, 152, 42, 42),
    (300, 195, 42, 44),
    (344, 108, 43, 38),
    (389, 109, 43, 36),
    (433, 107, 46, 39),
    (480, 100, 48, 45),
    (343, 149, 45, 43),
    (390, 148, 44, 45),
    (435, 147, 46, 44),
    (481, 147, 48, 42),
    (344, 196, 45, 41),
    (390, 197, 44, 41),
    (437, 194, 43, 43),
    (482, 194, 49, 42),
    (212, 241, 40, 45),
    (255, 240, 42, 47),
    (300, 241, 42, 45),
    (343, 243, 45, 43),
    (390, 242, 45, 44),
    (437, 242, 45, 44),
    (484, 240, 48, 46),
    (209, 286, 42, 45),
    (253, 289, 42, 42),
    (297, 289, 45, 44),
    (343, 290, 46, 43),
    (391, 290, 45, 44),
    (438, 290, 47, 44),
    (485, 286, 49, 49),
    (208, 334, 41, 46),
    (251, 333, 44, 46),
    (296, 336, 45, 43),
    (343, 336, 45, 43),
    (206, 381, 45, 43),
    (253, 382, 41, 46),
    (296, 382, 45, 46),
    (343, 382, 45, 48),
    (390, 337, 47, 44),
    (438, 336, 47, 47),
    (486, 336, 52, 49),
    (390, 383, 49, 47),
    (440, 384, 46, 46),
    (487, 386, 50, 48)
    ]
    
    while True:
        # Captura frame por frame
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar o frame")
            break

        # Desenhar as ROIs no frame da webcam
        #for roi in rois:
            #x, y, w, h = roi
            #cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Exibir o frame com as ROIs
        cv2.imshow("Webcam com ROIs", frame)

        # Verifica a tecla pressionada
        key = cv2.waitKey(30) & 0xFF
        
        # Verifica se a tecla 'i' foi pressionadaqq
        if key == ord('i'):
            img_name = f"fotos_jogadas/foto_jogada_inicio.png"
            cv2.imwrite(img_name, frame)
            print(f"Foto salva como {img_name}")
            global image
            # Carregar a imagem do tabuleiro de xadrez
            image = cv2.imread('fotos_jogadas/foto_jogada_inicio.png')
            if image is None:
                print("Erro ao carregar a imagem.")
                return
            # Exibir a imagem e capturar os pontos clicados
            cv2.imshow("Imagem", image)
            cv2.setMouseCallback("Imagem", capturar_pontos)
    
            print("Clique nos quatro cantos do tabuleiro de xadrez na ordem: top-left, top-right, bottom-right, bottom-left.")
            cv2.waitKey(0)
    
            if len(pontos_clicados) != 4:
                print("Você deve clicar exatamente em quatro pontos.")
                return   
            # Aplicar a transformação de perspectiva
            warp, matriz = warp_perspective_tabuleiro(image, pontos_clicados)
            
            # Detectar os cantos das casas do tabuleiro
            cantos_casas = detectar_cantos_casas(warp)
            
            # Calcular a matriz inversa da transformação de perspectiva
            matriz_inversa = np.linalg.inv(matriz)
            
            # Desenhar as ROIs na imagem original
            image = desenhar_roi_original(image, cantos_casas, matriz_inversa)
            
            # Exibir a imagem original com as ROIs das casas marcadas
            cv2.imshow("Imagem Original com ROIs das Casas", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # Verifica se a tecla 'x' foi pressionada
        if key == ord('x'):
            # Salva a imagem capturada
            img_name = f"fotos_jogadas/foto_jogada_{jogada}.png"
            cv2.imwrite(img_name, frame)
            print(f"Foto salva como {img_name}")
            
            # Lê a imagem da jogada
            image = cv2.imread(f'fotos_jogadas/foto_jogada_{jogada}.png')
            
            # Aplicar a transformação de perspectiva
            warp, matriz = warp_perspective_tabuleiro(image, pontos_clicados)
            
            # Detectar os cantos das casas do tabuleiro
            cantos_casas = detectar_cantos_casas(warp)
            
            # Calcular a matriz inversa da transformação de perspectiva
            matriz_inversa = np.linalg.inv(matriz)
            image = processa_e_analisa_imagem(image, jogada)
            # Desenhar as ROIs na imagem original
            image_ROIs = desenhar_roi_original(image, cantos_casas, matriz_inversa)

            
            # Criar a pasta 'fotos_com_ROIs' se ela não existir
            if not os.path.exists('fotos_com_ROIs'):
                os.makedirs('fotos_com_ROIs')
    
            # Salvar a imagem com as ROIs na pasta
            caminho_para_salvar = os.path.join('fotos_com_ROIs', f'foto_com_ROIs_jogada_{jogada}.png')
            cv2.imwrite(caminho_para_salvar, image_ROIs)
            

            # Coloca as ROIs na imagem
            #imagem_processada = processa_e_analisa_imagem(imagem, rois, jogada)

            # Exibe a imagem da jogada com as ROIs
            #cv2.imshow(f'Imagem processada da jogada {jogada}', imagem_processada)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

            # Aumenta para a próxima jogada
            jogada += 1

        # Verifica se a tecla 'z' foi pressionada
        elif key == ord('z'):
            jogada = 1
            # Exclui todas as fotos na pasta 'fotos_jogadas'
            for file in os.listdir('fotos_jogadas'):
                file_path = os.path.join('fotos_jogadas', file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                        print(f"Foto excluída: {file_path}")
                except Exception as e:
                    print(f"Erro ao excluir {file_path}: {e}")
            
            # Exclui todas as fotos na pasta 'fotos_com_ROIs'
            for file in os.listdir('fotos_com_ROIs'):
                file_path = os.path.join('fotos_com_ROIs', file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                        print(f"Foto excluída: {file_path}")
                except Exception as e:
                    print(f"Erro ao excluir {file_path}: {e}")
            # Exclui todas as fotos na pasta 'fotos_processadas'
            for file in os.listdir('fotos_processadas'):
                file_path = os.path.join('fotos_processadas', file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                        print(f"Foto excluída: {file_path}")
                except Exception as e:
                    print(f"Erro ao excluir {file_path}: {e}")
        # Verifica se a tecla 'q' foi pressionada para sair
        elif key == ord('q'):
            break

    # Libera a câmera e fecha todas as janelas abertas
    cap.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()