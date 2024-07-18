import cv2
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
        

def main():
    global image
    # Carregar a imagem do tabuleiro de xadrez
    image = cv2.imread('fotos_jogadas/images (1).png')
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
    desenhar_roi_original(image, cantos_casas, matriz_inversa)
    
    # Exibir a imagem original com as ROIs das casas marcadas
    cv2.imshow("Imagem Original com ROIs das Casas", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()