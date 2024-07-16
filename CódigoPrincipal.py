###################################################################################
## Import Libraries
###################################################################################
import os
import chess
import chess.engine
import cv2
import numpy as np


###################################################################################
## Import files
###################################################################################
from detect_points import get_points
from read_warp_img import get_warp_img
from find_position_black import find_current_past_position


###################################################################################
## Define Main Variables
###################################################################################

points = []    # contains chess board corners points
boxes = np.zeros((8,8,4),dtype=int)    # contains top-left and bottom-right point of chessboard boxes
fen_line = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR' # fen line of chess board
board = chess.Board(fen=fen_line) # object of chess board
dir_path = os.path.dirname(os.path.realpath(__file__))+"/numpy_saved" # path of current directory

# device = cv2.VideoCapture(1) # set devidce for read image (1: for tacking input from usb-webcam)
img_resize = (800,800) # set o/p image size
image = []
engine = chess.engine.SimpleEngine.popen_uci(r"C:\Users\Arthur\Desktop\Braço\stockfish_10_x64.exe" ) # stockfish engine
chess_board = []   # it will store chess board matrix
player_bool_position =[]
bool_position = np.zeros((8,8),dtype=int)
number_to_position_map = []
last_move = ""
game_img = ""
#
##################################################################################
## Code For Run Program
###################################################################################

print("Enter Code for Special Run : ")
code = str(input())
dir_path += "/"+code
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

###################################################################################
## camara position calibration
###################################################################################

while True:
    print("Do you want to set camara Position[y/n] : ",end=" ")
    answer = str(input())
    if answer == "y" or answer == "Y":
        print("Press q for exit : ")
        while True:
            ## show frame from camera and set positon by moving camera
            flag , img = cv2.VideoCapture(1).read()
            img = cv2.resize(img,img_resize)
            if flag:
                cv2.imshow("Set camera position",img)
                k = cv2.waitKey(1)
                if k == ord('q'):
                    cv2.destroyAllWindows()
                    break
        break
    elif answer == "n" or answer == "N":
        print("\nHope that camera position already set...\n")
        break
    else:
        print("Invalid Input ")

###################################################################################
## Image warp_prespective
###################################################################################

while True:
    print("DO you want to warp prespective image[y/n] :",end=" ")
    answer = str(input())
    ret , img = cv2.VideoCapture(1).read()
    img =   cv2.resize(img,(800,800))
    width,height = 800,800
    if answer == "y" or answer == "Y":
        warp_points = get_points(img,4)
        pts1 = np.float32([[warp_points[0][0],warp_points[0][1]],
                        [warp_points[1][0],warp_points[1][1]],
                        [warp_points[3][0],warp_points[3][1]],
                        [warp_points[2][0],warp_points[2][1]]])
        pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
        np.savez(dir_path+"/chess_board_warp_prespective.npz",pts1=pts1,pts2=pts2)
        result = get_warp_img(img,dir_path,img_resize)
        cv2.imshow("result",result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        break
    else:
        print("Enter valid input")

###################################################################################
## calibrate points for chess corners
## Parte Nova
###################################################################################
def detectar_quinas_tabuleiro(imagem, tamanho_tabuleiro=(7, 7)):
    # Converter para escala de cinza
    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Encontrar as quinas do tabuleiro de xadrez
    ret, quinas = cv2.findChessboardCorners(cinza, tamanho_tabuleiro, None)
    if ret:
        # Refinar as coordenadas das quinas
        quinas = cv2.cornerSubPix(cinza, quinas, (11, 11), (-1, -1), 
                                  (cv2.TermCriteria_EPS + cv2.TermCriteria_MAX_ITER, 30, 0.001))
        
        # Inicializar a imagem para desenhar as caixas e as coordenadas dos retângulos
        img_box = imagem.copy()
        boxes = np.zeros((tamanho_tabuleiro[1], tamanho_tabuleiro[0], 4), dtype=int)

        # Preencher as caixas e desenhar os retângulos
        for i in range(tamanho_tabuleiro[1] - 1):
            for j in range(tamanho_tabuleiro[0] - 1):
                # Calcular os índices dos quatro cantos de cada casa
                top_left = i * tamanho_tabuleiro[0] + j
                top_right = top_left + 1
                bottom_left = top_left + tamanho_tabuleiro[0]
                bottom_right = bottom_left + 1

                # Obter as coordenadas dos quatro cantos e converter para inteiros
                pontos = [tuple(map(int, quinas[top_left][0])),
                          tuple(map(int, quinas[top_right][0])),
                          tuple(map(int, quinas[bottom_right][0])),
                          tuple(map(int, quinas[bottom_left][0]))]

                # Definir a caixa para a casa
                boxes[i][j][0] = pontos[0][0]
                boxes[i][j][1] = pontos[0][1]
                boxes[i][j][2] = pontos[2][0]
                boxes[i][j][3] = pontos[2][1]
        np.savez(dir_path + "/chess_board_Box.npz", boxes=boxes)

        # Desenhar as caixas ao redor de cada casa e adicionar texto
        for i in range(tamanho_tabuleiro[1] - 1):
            for j in range(tamanho_tabuleiro[0] - 1):
                box1 = boxes[i, j]
                cv2.rectangle(img_box, (int(box1[0]), int(box1[1])), (int(box1[2]), int(box1[3])), (255, 0, 0), 2)
                cv2.putText(img_box, "({},{})".format(i, j), (int(box1[2]) - 70, int(box1[3]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        return img_box
    else:
        print("Não foi possível encontrar o tabuleiro de xadrez na imagem.")
        return imagem

while True:
    print("Do you want to calibrate new points for corners [y/n]:", end=" ")
    ans = input().strip().lower()
    
    if ans == "y":
        ret, img = cv2.VideoCapture(1).read()
        img = cv2.resize(img, (800, 800))
        # Suponho que as funções get_warp_img e get_points estejam definidas em outro lugar
        img = get_warp_img(img, dir_path, img_resize)
        points = []
        for i in range(9):
            pt = get_points(img, 9)
            points.append(pt)
        np.savez(dir_path + "/chess_board_points.npz", points=points)
        break
    elif ans == "n":
        ret, img = cv2.VideoCapture(1).read()
        if not ret:
            print("Erro ao capturar imagem do vídeo.")
            break
        img = cv2.resize(img, (800, 800))
        img = get_warp_img(img, dir_path, (800, 800))
        img_box = detectar_quinas_tabuleiro(img, tamanho_tabuleiro=(7, 7))
        
        # Mostrar a imagem com as caixas desenhadas
        cv2.imshow("Casas do Tabuleiro", img_box)
        # Parar o loop ao pressionar a tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break  
    else:
        print("Something wrong with input")

cv2.VideoCapture(1).release()
cv2.destroyAllWindows()

