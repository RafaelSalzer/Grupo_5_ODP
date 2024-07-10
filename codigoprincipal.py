import cv2
import os

def main():
    jogada = 1
    # Inicializa a captura de vídeo da webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro ao abrir a câmera")
        return

    # Cria um diretório para armazenar as fotos, se não existir
    if not os.path.exists('fotos'):
        os.makedirs('fotos')

    while True:
        # Captura frame por frame
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar o frame")
            break

        # Mostra o frame capturado
        cv2.imshow('Webcam', frame)

        # Verifica se a tecla 'x' foi pressionada
        if cv2.waitKey(1) & 0xFF == ord('x'):
            # Salva a imagem capturada
            img_name = f"fotos/foto_jogada_{jogada}.png"
            cv2.imwrite(img_name, frame)
            print(f"Foto salva como {img_name}")
            jogada += 1

        # Verifica se a tecla 'z' foi pressionada
        if cv2.waitKey(1) & 0xFF == ord('z'):
        # Exclui todas as fotos na pasta 'fotos'
            for file in os.listdir('fotos'):
                file_path = os.path.join('fotos', file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                        print(f"Foto excluída: {file_path}")
                except Exception as e:
                    print(f"Erro ao excluir {file_path}: {e}")

        # Verifica se a tecla 'q' foi pressionada para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera a câmera e fecha todas as janelas abertas
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()