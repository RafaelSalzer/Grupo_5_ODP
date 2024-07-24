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

# Função para detectar diferenças entre duas imagens
def detect_changes(frame1, frame2):
    diff = cv2.absdiff(frame1, frame2)  
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    
    # Operações de morfologia para remover ruídos pequenos
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    changes = []
    cell_size = 800 // 8
    min_area = cell_size * cell_size // 4  # Define a área mínima para considerar uma mudança como relevante

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w * h > min_area:  # Apenas considere mudanças com uma área maior que min_area
            i, j = x // cell_size, y // cell_size
            changes.append((chr(97+i) + str(8-j), x, y, w, h))

    return changes

# Inicialização da câmera
cap = cv2.VideoCapture('https://192.168.2.107:8080/video')

if not cap.isOpened():
    print("Erro ao abrir a câmera.")
    exit()

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
warped, M = apply_perspective_transform(frame, points)

# Desenha a grade do tabuleiro
warped_with_grid = draw_chessboard_grid(warped.copy())
cv2.imshow("Warped Chessboard", warped_with_grid)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Pressione 'c' para capturar o primeiro frame.")
frame1 = None
frame2 = None

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar a imagem.")
        cap.release()
        exit()

    warped_frame = cv2.warpPerspective(frame, M, (800, 800))
    warped_with_grid = draw_chessboard_grid(warped_frame.copy())
    cv2.imshow("Warped Chessboard", warped_with_grid)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('c') and frame1 is None:
        frame1 = warped_frame
        print("Primeiro frame capturado. Faça as modificações no tabuleiro e pressione 'c' novamente para capturar o segundo frame.")
    elif key == ord('c') and frame1 is not None:
        frame2 = warped_frame
        print("Segundo frame capturado.")
        changes = detect_changes(frame1, frame2)
        if changes:
            changes_sorted = sorted(changes, key=lambda c: c[1] + c[2])  # Ordenar pelas coordenadas x e y
            print(f"Moveu de {changes_sorted[-1][0]} para {changes_sorted[0][0]}")
        else:
            print("Nenhuma mudança detectada.")
        cv2.imshow("Frame 1", frame1)
        cv2.imshow("Frame 2", frame2)
        cv2.waitKey(0)
        break

cap.release()
cv2.destroyAllWindows()