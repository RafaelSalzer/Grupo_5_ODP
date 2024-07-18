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
###################################################################################
# Função para encontrar os cantos do tabuleiro de xadrez e imprimir as coordenadas
def find_and_print_corners(img):
    # Convertendo a imagem para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Tamanho do tabuleiro de xadrez (número de cruzamentos internos das linhas do tabuleiro)
    chessboard_size = (7, 7)

    # Arrays para armazenar pontos 3D do objeto e pontos 2D da imagem
    objpoints = []  # Pontos 3D no espaço do mundo real
    imgpoints = []  # Pontos 2D no plano da imagem

    # Prepare os pontos do objeto, como (0,0,0), (1,0,0), ..., (6,5,0)
    objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

    # Encontre os cantos do tabuleiro de xadrez
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

    # Se encontrou, adicione pontos de objeto e pontos de imagem (após refiná-los)
    if ret:
        objpoints.append(objp)
        
        # Refinando os cantos para precisão subpixel
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        corners_refined = cv2.cornerSubPix(gray, corners, (9, 9), (-1, -1), criteria)

        imgpoints.append(corners_refined)

        # Imprimir os pontos encontrados
        print("Corners found:")
        for corner in corners_refined:
            print(corner[0])  # Imprime cada ponto encontrado

        # Desenhe os cantos encontrados na imagem (opcional)
        cv2.drawChessboardCorners(img, chessboard_size, corners_refined, ret)
        
        # Mostrar a imagem com os cantos desenhados (opcional)
        cv2.imshow('Chessboard Corners', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Salvar objpoints e imgpoints em um arquivo .npz (opcional)
        # np.savez(dir_path + "/chess_board_points.npz", objpoints=objpoints, imgpoints=imgpoints)
    else:
        print('Corners not found')


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
        img = cv2.resize(img, (800, 800))
        img = get_warp_img(img, dir_path, img_resize)
        find_and_print_corners(img)
        break
    else:
        print("Something wrong with input")



