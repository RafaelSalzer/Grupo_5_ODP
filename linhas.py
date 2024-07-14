import cv2
import numpy as np
import os

def main():
    # Abra a webcam (0 para a webcam integrada, 1 para uma webcam externa, etc.)
    cap = cv2.VideoCapture('https://192.168.2.107:8080/video')

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if not ret:
            print("Falha ao capturar a imagem")
            break

        # Converta a imagem para escala de cinza
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Aplique um filtro Gaussiano para suavizar a imagem e reduzir o ruído
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Detecte bordas na imagem usando o Canny
        edges = cv2.Canny(blurred, 50, 150, apertureSize=3)

        # Detecte linhas na imagem usando a Transformada de Hough
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=50, maxLineGap=10)

        # Desenhe as linhas detectadas na imagem original
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Mostre a imagem com as linhas detectadas
        cv2.imshow('Linhas Detectadas', frame)

        # Pressione 'q' para sair do loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libere a captura e feche as janelas
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

