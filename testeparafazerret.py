import cv2
import numpy as np
import os

def detectar_tabuleiro_xadrez(caminho_imagem):
    # Carrega a imagem
    imagem = cv2.imread(caminho_imagem)
    if imagem is None:
        print(f"Não foi possível carregar a imagem: {caminho_imagem}")
        return

    # Converte a imagem para escala de cinza
    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Aplica o filtro de borda Canny
    bordas = cv2.Canny(imagem_cinza, 50, 150, apertureSize=3)

    # Detecta as linhas usando a Transformada de Hough
    linhas = cv2.HoughLinesP(bordas, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

    if linhas is not None:
        # Desenha as linhas detectadas na imagem original
        for linha in linhas:
            x1, y1, x2, y2 = linha[0]
            cv2.line(imagem, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Identifica as interseções das linhas para determinar as casas do tabuleiro
        # (Esta parte pode ser complexa e depende da precisão das linhas detectadas)
        # Aqui, vamos apenas desenhar as linhas detectadas

    # Exibe a imagem com as linhas detectadas
    cv2.imshow('Tabuleiro de Xadrez Detectado', imagem)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Verifica se há imagens na pasta 'fotos'
    pasta_fotos = 'fotos'
    if not os.path.exists(pasta_fotos):
        print(f"Pasta '{pasta_fotos}' não encontrada.")
    else:
        imagens = [os.path.join(pasta_fotos, f) for f in os.listdir(pasta_fotos) if f.endswith('.png')]
        if not imagens:
            print(f"Nenhuma imagem encontrada na pasta '{pasta_fotos}'.")
        else:
            # Usa a primeira imagem encontrada na pasta 'fotos'
            detectar_tabuleiro_xadrez(imagens[0])