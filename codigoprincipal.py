import cv2

def main():
    # Inicializa a câmera
    cap = cv2.VideoCapture(0)

    while True:
        # Lê o frame da câmera
        ret, frame = cap.read()
        if not ret:
            print("Falha ao capturar imagem da câmera.")
            break

        # Converte para escala de cinza
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Aplica a binarização
        img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)

        # Exibe o frame binarizado
        cv2.imshow('Frame Binarizado', img)

        # Sai do loop quando a tecla 'q' é pressionada
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera a câmera e fecha todas as janelas abertas
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
# teste