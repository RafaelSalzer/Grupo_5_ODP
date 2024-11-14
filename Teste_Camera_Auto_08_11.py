import cv2
import numpy as np

def detect_red_circles_from_camera(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define o intervalo de cores vermelhas no espaço HSV
    lower_red = np.array([0, 110, 130])
    upper_red = np.array([10, 230, 200])

    # Cria uma máscara para isolar as bolinhas vermelhas
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Detecta contornos na máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Lista para armazenar as coordenadas das bolinhas
    points = []
    # Itera sobre os contornos detectados
    for contour in contours:
        # Calcula o círculo mínimo que envolve o contorno
        ((x, y), radius) = cv2.minEnclosingCircle(contour)

        # Filtra por tamanho mínimo do círculo (para evitar ruídos)
        if radius > 1:
            points.append((int(x), int(y)))
    print(points)        
    filtered_points = []
    proximity_threshold = 20  # Distância mínima entre dois pontos considerados duplicados

    for i, (x1, y1) in enumerate(points):
        duplicate = False
        for j, (x2, y2) in enumerate(points):
            if i != j and np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) < proximity_threshold:
                duplicate = True
                break
        if not duplicate:
            filtered_points.append((x1, y1))

            # Desenha o círculo detectado na imagem
            cv2.circle(frame, (int(x1), int(y1)), int(radius), (0, 255, 0), 2)

    # Exibe a imagem com os círculos detectados
    cv2.imshow("Detected Circles", frame)
    # Libera a câmera e fecha as janelas
    cv2.destroyAllWindows()
    return filtered_points

# Função para calcular a homografia e aplicar a transformação
def apply_perspective_transform(image, src_points):
    dst_points = np.array([[0, 0], [640, 0], [0, 640], [640, 640]], dtype='float32')
    M = cv2.getPerspectiveTransform(np.array(src_points, dtype='float32'), dst_points)
    warped = cv2.warpPerspective(image, M, (640, 640))
    return warped, M

# Função para criar um grid de 64 quadrados
def draw_chessboard_grid(image):
    cell_size = 640 // 8
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
    _, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)
    
    # Operações de morfologia para remover ruídos pequenos
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    # Debug prints
    cv2.imshow("Gray", gray)
    cv2.imshow("Thresh", thresh)
    cv2.waitKey(1)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    changes = []
    cell_size = 640 // 8
    min_area = cell_size * cell_size // 4  # Define a área mínima para considerar uma mudança como relevante

    # Copia da imagem para desenhar os retângulos
    debug_image = frame2.copy()

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        x=x+25
        y=y+25
        if w * h > min_area:  # Apenas considere mudanças com uma área maior que min_area
            i, j = x // cell_size, y // cell_size
            house = chr(97+i) + str(8-j)
            changes.append((house, x, y, w, h))
            cv2.rectangle(debug_image, (x+10, y+10), (x + w//2, y + h//2), (0, 255, 0), 2)
            cv2.putText(debug_image, f"x:{x}, y:{y}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            print(f"Change detected in house: {house} at position x: {x}, y: {y}, width: {w}, height: {h}")  # Debug print
    
    cv2.imshow("Debug Image with Rectangles", debug_image)
    cv2.waitKey(1)

    print("Detected changes:", changes)  # Debug print
    return changes

def tab_base():
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
    points = detect_red_circles_from_camera(frame)
    warped, num = apply_perspective_transform(frame, points)

    # Desenha a grade do tabuleiro
    warped_with_grid = draw_chessboard_grid(warped.copy())
    cv2.imshow("Warped Chessboard", warped_with_grid)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return num

def tab_base_auto():
    print("Aponte a câmera para o tabuleiro de xadrez e pressione 'c' para capturar a imagem.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar a imagem.")
            cap.release()
            exit()

        cv2.imshow("Camera", frame)
        break

    # Captura a imagem inicial e define os pontos para a transformação de perspectiva
    points = detect_red_circles_from_camera(frame)
    warped, num = apply_perspective_transform(frame, points)

    # Desenha a grade do tabuleiro
    warped_with_grid = draw_chessboard_grid(warped.copy())
    cv2.imshow("Warped Chessboard", warped_with_grid)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return num

# Inicialização da câmera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao abrir a câmera.")
    exit()

M = tab_base()

frame1 = None
frame2 = None

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar a imagem.")
        cap.release()
        exit()

    warped_frame = cv2.warpPerspective(frame, M, (640, 640))
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
            changes_sorted = sorted(changes, key=lambda c: c[1] + c[2] )  # Ordenar pelas coordenadas x e y
            print(f"Moveu de {changes_sorted[0][0]} para {changes_sorted[-1][0]}")
        else:
            print("Nenhuma mudança detectada.")
        M = tab_base_auto()
        frame1 = frame2  # Atualiza o frame1 para a próxima iteração
        cv2.waitKey(1)
        
cap.release()
cv2.destroyAllWindows()