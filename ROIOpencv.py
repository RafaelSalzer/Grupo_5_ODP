import cv2

# Lista para armazenar as ROIs
rois = []

# Variável global para armazenar o ponto inicial do clique
start_point = None

# Função de callback do mouse para capturar os eventos de clique e arrasto
def select_rois(event, x, y, flags, param):
    global start_point, rois, image_copy

    if event == cv2.EVENT_LBUTTONDOWN:
        # Quando o botão esquerdo do mouse é pressionado, armazenar o ponto inicial
        start_point = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        # Quando o botão esquerdo do mouse é solto, armazenar a ROI e desenhar o retângulo
        end_point = (x, y)
        roi = (start_point[0], start_point[1], x - start_point[0], y - start_point[1])
        rois.append(roi)
        cv2.rectangle(image_copy, start_point, end_point, (255, 0, 0), 2)
        cv2.imshow("Selecione as ROIs e pressione 'Enter' quando terminar", image_copy)

# Carregar a imagem para selecionar as ROIs
image = cv2.imread('fotos/foto_jogada_1.png')
image_copy = image.copy()

cv2.namedWindow("Selecione as ROIs e pressione 'Enter' quando terminar")
cv2.setMouseCallback("Selecione as ROIs e pressione 'Enter' quando terminar", select_rois)

# Exibir a imagem e aguardar a seleção das ROIs
while True:
    cv2.imshow("Selecione as ROIs e pressione 'Enter' quando terminar", image_copy)
    key = cv2.waitKey(1) & 0xFF
    if key == 13:  # Tecla Enter
        break

cv2.destroyAllWindows()

# Imprimir as coordenadas de todas as ROIs selecionadas
print("ROIs selecionadas:")
for i, roi in enumerate(rois):
    print(f"ROI {i+1}: x={roi[0]}, y={roi[1]}, largura={roi[2]}, altura={roi[3]}")

# Iniciar a captura da webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao abrir a webcam")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar frame da webcam")
        break

    # Desenhar as ROIs no frame da webcam
    for roi in rois:
        x, y, w, h = roi
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Exibir o frame com as ROIs
    cv2.imshow("Webcam com ROIs", frame)

    # Sair do loop ao pressionar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar a captura da webcam e fechar as janelas
cap.release()
cv2.destroyAllWindows()
