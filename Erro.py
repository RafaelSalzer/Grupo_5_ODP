import cv2
import os
def processa_imagem(imagem, rois, jogada):  
    
    # Processamento da imagem
    imgCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    imgTh = cv2.adaptiveThreshold(imgCinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)

    # Desenhar os retângulos das ROIs na imagem
    for (x, y, w, h) in rois:
        cv2.rectangle(imgTh, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Criar a pasta 'fotos_com_ROIs' se ela não existir
    if not os.path.exists('fotos_com_ROIs'):
        os.makedirs('fotos_com_ROIs')
    
    # Salvar a imagem com as ROIs na pasta
    caminho_para_salvar = os.path.join('fotos_com_ROIs', f'foto_com_ROIs_jogada_{jogada}.jpg')
    cv2.imwrite(caminho_para_salvar, imgTh)

    return imgTh
  
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
        for roi in rois:
            x, y, w, h = roi
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Exibir o frame com as ROIs
        cv2.imshow("Webcam com ROIs", frame)

        # Verifica a tecla pressionada
        key = cv2.waitKey(30) & 0xFF

        # Verifica se a tecla 'x' foi pressionada
        if key == ord('x'):
            # Salva a imagem capturada
            img_name = f"fotos_jogadas/foto_jogada_{jogada}.png"
            cv2.imwrite(img_name, frame)
            print(f"Foto salva como {img_name}")
    
            # Lê a imagem da jogada
            imagem = cv2.imread(f'fotos_jogadas/foto_jogada_{jogada}.png')
    
            # Processamento da imagem
            imgCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
            imgTh = cv2.adaptiveThreshold(imgCinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    
            # Desenhar as ROIs na imagem processada
            for roi in rois:
                x, y, w, h = roi
                cv2.rectangle(imgTh, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
            # Exibir a imagem processada com as ROIs
            cv2.imshow(f'Imagem processada com ROIs da jogada {jogada}', imgTh)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            # Criar a pasta 'fotos_com_ROIs' se ela não existir
            if not os.path.exists('fotos_com_ROIs'):
                os.makedirs('fotos_com_ROIs')
    
            # Salvar a imagem com as ROIs na pasta
            caminho_para_salvar = os.path.join('fotos_com_ROIs', f'foto_com_ROIs_jogada_{jogada}.jpg')
            cv2.imwrite(caminho_para_salvar, imgTh)
            
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

        # Verifica se a tecla 'q' foi pressionada para sair
        elif key == ord('q'):
            break

    # Libera a câmera e fecha todas as janelas abertas
    cap.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()