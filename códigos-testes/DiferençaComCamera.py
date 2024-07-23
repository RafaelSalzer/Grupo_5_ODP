import cv2
import numpy as np

from read_warp_img import get_warp_img
img_resize = (400,400)

# Função para redimensionar a imagem
def resize_image(image, fixed_size=(400, 400)):
    resized_image = cv2.resize(image, fixed_size)
    return resized_image

# Função para encontrar diferenças entre duas imagens
def find_differences(image1, image2, threshold=50):
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(gray1, gray2)
    _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    return thresh

# Função para identificar as casas alteradas no tabuleiro
def identify_changed_squares(thresh, grid_size=8):
    height, width = thresh.shape
    square_height = height // grid_size
    square_width = width // grid_size

    changed_squares = []
    for row in range(grid_size):
        for col in range(grid_size):
            x1 = col * square_width
            y1 = row * square_height
            x2 = (col + 1) * square_width
            y2 = (row + 1) * square_height
            square = thresh[y1:y2, x1:x2]
            if np.any(square):
                changed_squares.append((row, col))

    return changed_squares

# Função para converter coordenadas de quadrados para notação de xadrez
def square_to_notation(row, col):
    files = 'abcdefgh'
    ranks = '87654321'
    return f"{files[col]}{ranks[row]}"

# Inicializar a câmera
cap = cv2.VideoCapture('https://192.168.2.107:8080/video')

if not cap.isOpened():
    print("Erro ao acessar a câmera.")
    exit()

# Capturar o primeiro frame
print("Capturando o primeiro frame. Pressione 'q' para capturar.")
while True:
    ret, frame1 = cap.read()
    if not ret:
        print("Falha ao capturar o frame da câmera. Tentando novamente...")
        continue
    cv2.imshow('Frame 1', frame1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        resized_image1 = resize_image(frame1)
        break

# Capturar o segundo frame quando o usuário pressionar uma tecla específica
print("Capturando o segundo frame. Pressione 'w' para capturar.")
while True:
    ret, frame2 = cap.read()
    if not ret:
        print("Falha ao capturar o frame da câmera. Tentando novamente...")
        continue
    cv2.imshow('Frame 2', frame2)
    if cv2.waitKey(1) & 0xFF == ord('w'):
        resized_image2 = resize_image(frame2)
        break

# Encontrar diferenças
thresh = find_differences(resized_image1, resized_image2)

# Identificar casas alteradas
changed_squares = identify_changed_squares(thresh)

# Converter coordenadas para notação de xadrez
changed_squares_notation = [square_to_notation(row, col) for row, col in changed_squares]

# Mostrar resultados
print("Casas alteradas:")
for square in changed_squares_notation:
    print(square)

# Mostrar imagens e a imagem da diferença
cv2.imshow("Image 1", resized_image1)
cv2.imshow("Image 2", resized_image2)
cv2.imshow("Differences", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Liberar a câmera
cap.release()
