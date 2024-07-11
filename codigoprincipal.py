import cv2
import os
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
    if not os.path.exists('fotos'):
        os.makedirs('fotos')

    # Inicializa o contador de jogadas
    jogada = 1

    while True:
        # Captura frame por frame
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar o frame")
            break

        # Mostra o frame capturado
        cv2.imshow('Webcam', frame)

        # Verifica a tecla pressionada
        key = cv2.waitKey(30) & 0xFF

        # Verifica se a tecla 'x' foi pressionada
        if key == ord('x'):
            # Salva a imagem capturada
            img_name = f"fotos/foto_jogada_{jogada}.png"
            cv2.imwrite(img_name, frame)
            print(f"Foto salva como {img_name}")
            jogada += 1

        # Verifica se a tecla 'z' foi pressionada
        elif key == ord('z'):
            jogada = 1
            # Exclui todas as fotos na pasta 'fotos'
            for file in os.listdir('fotos'):
                file_path = os.path.join('fotos', file)
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