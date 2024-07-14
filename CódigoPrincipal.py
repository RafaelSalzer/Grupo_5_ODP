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

###################################################################################
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
            flag , img = cv2.VideoCapture('https://192.168.2.107:8080/video').read()
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
    ret , img = cv2.VideoCapture('https://192.168.2.107:8080/video').read()
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
while True:
        print("do you want to calibrate new Points for corners [y/n]:",end=" ")
        ans = str(input())
        if ans == "y" or ans == "Y":
            ret , img = cv2.VideoCapture('https://192.168.2.107:8080/video').read()
            img =   cv2.resize(img,(800,800))
            img = get_warp_img(img,dir_path,img_resize)
            points = []
            for i in range(9):
                pt = get_points(img,9)
                points.append(pt)
            np.savez(dir_path+"/chess_board_points.npz",points=points)
            break
        elif ans == "n" or ans == "N":
            # do some work
            ret , img = cv2.VideoCapture('https://192.168.2.107:8080/video').read()
            img = cv2.resize(img,(800,800))
            img = get_warp_img(img,dir_path,img_resize)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            points = []

            
            import glob
            
            # termination criteria
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            
            # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
            objp = np.zeros((6*7,3), np.float32)
            objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
            
            # Arrays to store object points and image points from all the images.
            objpoints = [] # 3d point in real world space
            imgpoints = [] # 2d points in image plane.
            
            
            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(img, (8,8), None)
            
            # If found, add object points, image points (after refining them)
            if ret == True:
                 corners2 = cv2.cornerSubPix(img,corners, (11,11), (-1,-1), criteria)
                 imgpoints.append(corners2)
            
            # Draw and display the corners
            cv2.drawChessboardCorners(img, (8,8), corners2, ret)
            cv2.imshow('img', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            
           ## points = np.load(dir_path+'/chess_board_points.npz')['points']
           ## print("points Load successfully")
            break
        else:
            print("something wrong input")