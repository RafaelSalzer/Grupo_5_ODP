# Cria uma matriz 8x8 inicializada com zeros
posicoes = [['   ' for _ in range(8)] for _ in range(8)]

#preencher os peoes pretos
for j in range(8):
    posicoes[1][j] = 'P_P'

#preencher os torres prertas 
posicoes[0][0] = 'T_P' 
posicoes[0][7] = 'T_P'

#preencher os cavalos pretos
posicoes[0][1] = 'C_P'
posicoes[0][6] = 'C_P'

#preencher os bispos pretos
posicoes[0][2] = 'B_P'
posicoes[0][5] = 'B_P'

#preencher a rainha preta
posicoes[0][3] = 'Q_P'

#preencher o rei preto
posicoes[0][4] = 'K_P'

#preencher os peoes brancos
for j in range(8):
    posicoes[6][j] = 'P_B'

#preencher os torres brancas
posicoes[7][0] = 'T_B'
posicoes[7][7] = 'T_B'

#preencher os cavalos brancos
posicoes[7][1] = 'C_B'
posicoes[7][6] = 'C_B'

#preencher os bispos brancos
posicoes[7][2] = 'B_B'
posicoes[7][5] = 'B_B'

#preencher a rainha branca
posicoes[7][3] = 'Q_B'

#preencher o rei branco
posicoes[7][4] = 'K_B'

# Exibe a matriz
for linha in posicoes:
    print(linha)