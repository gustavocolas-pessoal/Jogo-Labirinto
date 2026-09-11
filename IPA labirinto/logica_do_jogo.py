from gera_labirintos import gerador_labirintos

lista_labirintos = []
size = 10 # VARIÁVEL!!!!
lista_labirintos.append(gerador_labirintos(size))
qual_labirinto = lista_labirintos[0]

n_passos = 0
pos_atual = (0,0)

def tenta_horizontal_saida():
    global n_passos
    direcao = 0
    sentido = 1
    n_passos += 1
    return (direcao,sentido),n_passos

def tenta_horizontal_entrada():
    global n_passos
    direcao = 0
    sentido = -1
    n_passos += 1
    return (direcao,sentido),n_passos

def tenta_vertical_saida():
    global n_passos
    direcao = 1
    sentido = 1
    n_passos += 1
    return (direcao,sentido),n_passos

def tenta_vertical_entrada():
    global n_passos
    direcao = 1
    sentido = -1
    n_passos += 1
    return (direcao,sentido),n_passos

def permite_movimento(tupla_direcao_sentido): 
    '''Retorna True se o movimento é permitido e False caso contrário
    Argumentos = tupla (direção, sentido):

     - direção 0,1 = horizontal,vertical

     - sentido 0,1 = entrada, saída'''  

    global pos_atual


    direcao, sentido = tupla_direcao_sentido[0], tupla_direcao_sentido[1] 

    if direcao == 0:

        if sentido == -1:
            if (pos_atual) in (qual_labirinto[1]):
                print(f"NÃO É POSSÍVEL IR PARA {((pos_atual[0]+sentido),(pos_atual[1]))}")
            else:
                pos_atual = ((pos_atual[0]+sentido),(pos_atual[1]))

        elif sentido == 1:
            if ((pos_atual[0]+sentido),(pos_atual[1])) in (qual_labirinto[1]):
                print(f"NÃO É POSSÍVEL IR PARA {((pos_atual[0]+sentido),(pos_atual[1]))}")
            else:
                pos_atual = ((pos_atual[0]+sentido),(pos_atual[1]))

        
    elif direcao == 1:

        if sentido == 1:
            if ((pos_atual[0]),(pos_atual[1]+sentido)) in (qual_labirinto[0]):
                print(f"NÃO É POSSÍVEL IR PARA {((pos_atual[0]),(pos_atual[1]+sentido))}")

            else:
                pos_atual = ((pos_atual[0]),(pos_atual[1]+sentido))

        if sentido == -1:
            if ((pos_atual[0]),(pos_atual[1])) in (qual_labirinto[0]):
                print(f"NÃO É POSSÍVEL IR PARA {((pos_atual[0]),(pos_atual[1]+sentido))}")
            else:
                pos_atual = ((pos_atual[0]),(pos_atual[1]+sentido))

    return pos_atual