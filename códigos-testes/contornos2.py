import cv2
import numpy as np

# Função para obter os pontos de um clique do usuário
def get_points(image, num_points=4):
    points = []

    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN and len(points) < num_points:
            points.append((x, y))
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)
            cv2.imshow("Image", image)

    cv2.imshow("Image", image)
    cv2.setMouseCallback("Image", mouse_callback)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return points

# Função para calcular a homografia e aplicar a transformação
def apply_perspective_transform(image, src_points):
    dst_points = np.array([[0, 0], [800, 0], [800, 800], [0, 800]], dtype='float32')
    M = cv2.getPerspectiveTransform(np.array(src_points, dtype='float32'), dst_points)
    warped = cv2.warpPerspective(image, M, (800, 800))
    return warped, M

# Função para criar um grid de 64 quadrados
def draw_chessboard_grid(image):
    cell_size = 800 // 8
    for i in range(8):
        for j in range(8):
            x1, y1 = i * cell_size, j * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 1)
            cv2.putText(image, f"{chr(97+i)}{8-j}", (x1 + 10, y1 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    return image

# Função para detectar peças de xadrez e identificar as casas
def detect_chess_pieces(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY_INV)
    
    cv2.imshow('i',blurred)
    cv2.imshow('e',thresh)
    # Detectar contornos
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    cell_size = 800 // 8
    house_contours = set()  # Usar um set para evitar duplicatas

    for contour in contours:
        if cv2.contourArea(contour) > 100:  # Ignorar pequenos contornos
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            i, j = x // cell_size, y // cell_size
            house = chr(97+i) + str(8-j)
            house_contours.add(house)  # Adicionar ao set
    
    return image, sorted(house_contours)  # Ordenar as casas para consistência

# Inicialização da câmera
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Erro ao abrir a câmera.")
    exit()

# Captura do primeiro frame
print("Aponte a câmera para o tabuleiro de xadrez e pressione 'c' para capturar a imagem.")
while True:
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar a imagem.")
        cap.release()
        exit()

    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord('c'):
        break

# Captura a imagem inicial e define os pontos para a transformação de perspectiva
points = get_points(frame)
warped1, M = apply_perspective_transform(frame, points)

# Desenha a grade do tabuleiro e detecta as peças no primeiro frame
warped_with_grid1 = draw_chessboard_grid(warped1.copy())
warped_with_contours1, house_contours1 = detect_chess_pieces(warped_with_grid1.copy())
cv2.imshow("Warped Chessboard with Contours and Grid - Frame 1", warped_with_contours1)
print("Contornos das peças detectadas no primeiro frame nas casas:", house_contours1)

cv2.waitKey(0)

# Captura do segundo frame
print("Modifique o tabuleiro, depois aponte a câmera para o tabuleiro e pressione 'c' para capturar a imagem.")
while True:
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar a imagem.")
        cap.release()
        exit()

    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord('c'):
        break

# Aplica a mesma transformação de perspectiva ao segundo frame
warped2 = cv2.warpPerspective(frame, M, (800, 800))

# Desenha a grade do tabuleiro e detecta as peças no segundo frame
warped_with_grid2 = draw_chessboard_grid(warped2.copy())
warped_with_contours2, house_contours2 = detect_chess_pieces(warped_with_grid2.copy())
cv2.imshow("Warped Chessboard with Contours and Grid - Frame 2", warped_with_contours2)
print("Contornos das peças detectadas no segundo frame nas casas:", house_contours2)

cv2.waitKey(0)

# Encontrar as casas que estão em ambos os frames
common_houses = set(house_contours1).intersection(set(house_contours2))
print("Casas com contornos em ambos os frames:", sorted(common_houses))

cap.release()
cv2.destroyAllWindows()
