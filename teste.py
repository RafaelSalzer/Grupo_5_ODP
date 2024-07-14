import cv2
import os

# Carregar a imagem
imagem = cv2.imread('fotos_jogadas/foto_jogada_1.png')

# Definir as ROIs
rois = [
    (174, 71, 41, 41),
    (214, 73, 42, 37),
    (257, 71, 41, 37),
    (299, 68, 42, 39),
    (343, 67, 44, 38),
    (387, 66, 45, 36),
    (433, 63, 46, 39),
    (477, 61, 49, 38),
    (174, 113, 39, 39),
    (172, 155, 39, 39),
    (172, 197, 38, 40),
    (168, 238, 40, 47),
    (166, 288, 41, 43),
    (164, 333, 42, 45),
    (162, 379, 43, 46),
    (216, 113, 40, 38),
    (215, 153, 40, 43),
    (211, 197, 41, 44),
    (259, 112, 39, 40),
    (257, 152, 41, 42),
    (256, 199, 42, 36),
    (300, 110, 42, 40),
    (299, 152, 42, 42),
    (300, 195, 42, 44),
    (344, 108, 43, 38),
    (389, 109, 43, 36),
    (433, 107, 46, 39),
    (480, 100, 48, 45),
    (343, 149, 45, 43),
    (390, 148, 44, 45),
    (435, 147, 46, 44),
    (481, 147, 48, 42),
    (344, 196, 45, 41),
    (390, 197, 44, 41),
    (437, 194, 43, 43),
    (482, 194, 49, 42),
    (212, 241, 40, 45),
    (255, 240, 42, 47),
    (300, 241, 42, 45),
    (343, 243, 45, 43),
    (390, 242, 45, 44),
    (437, 242, 45, 44),
    (484, 240, 48, 46),
    (209, 286, 42, 45),
    (253, 289, 42, 42),
    (297, 289, 45, 44),
    (343, 290, 46, 43),
    (391, 290, 45, 44),
    (438, 290, 47, 44),
    (485, 286, 49, 49),
    (208, 334, 41, 46),
    (251, 333, 44, 46),
    (296, 336, 45, 43),
    (343, 336, 45, 43),
    (206, 381, 45, 43),
    (253, 382, 41, 46),
    (296, 382, 45, 46),
    (343, 382, 45, 48),
    (390, 337, 47, 44),
    (438, 336, 47, 47),
    (486, 336, 52, 49),
    (390, 383, 49, 47),
    (440, 384, 46, 46),
    (487, 386, 50, 48)
]

# Desenhar os retângulos das ROIs na imagem
for (x, y, w, h) in rois:
    cv2.rectangle(imagem, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Criar a pasta 'fotoscomROIs' se ela não existir
if not os.path.exists('fotos_com_ROIs'):
    os.makedirs('fotos_com_ROIs')

# Salvar a imagem com as ROIs na pasta
caminho_para_salvar = os.path.join('fotos_com_ROIs', 'imagem_com_ROIs.jpg')
cv2.imwrite(caminho_para_salvar, imagem)

# Exibir a imagem com as ROIs desenhadas (opcional)
cv2.imshow('Imagem com ROIs', imagem)
cv2.waitKey(0)
cv2.destroyAllWindows()