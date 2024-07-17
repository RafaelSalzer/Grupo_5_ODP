import cv2
import numpy as np

# Lista para armazenar os pontos selecionados
pontos = []

def selecionar_pontos(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pontos.append((x, y))
        cv2.circle(imagem, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Selecione os 4 cantos do tabuleiro", imagem)

def warp_perspective_tabuleiro(image, pontos):
    # Ordenar os pontos do contorno para obter a ordem correta: top-left, top-right, bottom-right, bottom-left
    pontos_ordenados = np.array(pontos, dtype="float32")
    
    # Definir os pontos de destino para a transformação de perspectiva
    (tl, tr, br, bl) = pontos_ordenados
    largura_max = max(int(np.linalg.norm(br - bl)), int(np.linalg.norm(tr - tl)))
    altura_max = max(int(np.linalg.norm(tr - br)), int(np.linalg.norm(tl - bl)))
    
    pontos_destino = np.array([
        [0, 0],
        [largura_max - 1, 0],
        [largura_max - 1, altura_max - 1],
        [0, altura_max - 1]], dtype="float32")
    
    # Calcular a matriz de transformação de perspectiva
    matriz = cv2.getPerspectiveTransform(pontos_ordenados, pontos_destino)
    
    # Aplicar a transformação de perspectiva
    warp = cv2.warpPerspective(image, matriz, (largura_max, altura_max))
    
    return warp

def main():
    global imagem
    # Carregar a imagem do tabuleiro de xadrez
    imagem = cv2.imread('fotos_jogadas/images.png')
    if imagem is None:
        print("Erro ao carregar a imagem.")
        return
    
    # Exibir a imagem e configurar a função de callback do mouse
    cv2.imshow("Selecione os 4 cantos do tabuleiro", imagem)
    cv2.setMouseCallback("Selecione os 4 cantos do tabuleiro", selecionar_pontos)
    
    # Esperar até que 4 pontos sejam selecionados
    while len(pontos) < 4:
        cv2.waitKey(1)
    
    # Aplicar a transformação de perspectiva
    warp = warp_perspective_tabuleiro(imagem, pontos)
    
    # Exibir a imagem transformada
    cv2.imshow("Warp Perspective", warp)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()