from random import choice
import copy # Importante para a função cria_parede não alterar o grafo original antes de verificar
from itertools import product


def gera_grafo(tamanho_do_grafo):
    grafo = {}
    for h in range(tamanho_do_grafo):
        for v in range(tamanho_do_grafo):
            vizinhos = [(h-1,v),(h+1,v),(h,v-1),(h,v+1)]
            if (h-1) < 0:
                vizinhos.remove((h-1,v))
            elif (h+1) > tamanho_do_grafo-1:
                vizinhos.remove((h+1,v))
            if (v-1) < 0:
                vizinhos.remove((h,v-1))
            elif (v+1) > tamanho_do_grafo-1:
                vizinhos.remove((h,v+1))
            grafo[(h,v)] = vizinhos
    return grafo

def cria_parede(grafo):
    novo_grafo = copy.deepcopy(grafo)
    casas_candidatas = [k for k, v in novo_grafo.items() if len(v) > 1]  
    if not casas_candidatas:
        return novo_grafo 
    tentativas = 0
    # Loop de segurança para tentar encontrar duas casas válidas para separar
    while tentativas < 100:
        casa = choice(casas_candidatas)
        parede_criada = choice(novo_grafo[casa])
        if len(novo_grafo[parede_criada]) > 1:
            novo_grafo[casa].remove(parede_criada)
            novo_grafo[parede_criada].remove(casa)
            return novo_grafo 
        tentativas += 1
        
    return novo_grafo 

def verifica_caminhos(grafo):
    primeiro = (0,0)

    def dfs(grafo_completo, vertice, visitados=None):
        if visitados is None:
            visitados = set()   
        visitados.add(vertice)                      
        for seguinte in grafo_completo[vertice]:  
            if seguinte not in visitados:
                dfs(grafo_completo, seguinte, visitados)
        return visitados
    
    quem_esta_ligado_ao_primeiro = dfs(grafo, primeiro)    
    todas_as_casas = set(grafo.keys())

    return todas_as_casas == quem_esta_ligado_ao_primeiro


def criando_o_grafo_final(tamanho_do_grafo):
    inicio = gera_grafo(tamanho_do_grafo)
    contador = 0
    grafo_base = None
    rodou = 0
    while (contador < ((tamanho_do_grafo-1)**2)) or rodou < 5000:
        if grafo_base is None:
            grafo_base = inicio
            
        possivel_novo_grafo = cria_parede(grafo_base)
        if verifica_caminhos(possivel_novo_grafo) and possivel_novo_grafo != grafo_base: 
                grafo_base = possivel_novo_grafo
                contador += 1  
        rodou +=1
        
    return grafo_base
        
        
def desconverte_de_grafo(grafo):
    nao_parede_horizontal = []
    nao_parede_vertical = []
    for casa in grafo:
        hc,vc = casa[0],casa[1]
        for ligado in grafo[casa]: 
            hl,vl = ligado[0],ligado[1]
            if hc == hl and vl>vc:
                nao_parede_horizontal.append(ligado)
            elif vc == vl and hl>hc:
                nao_parede_vertical.append(ligado)
    return nao_parede_horizontal,nao_parede_vertical 

def gerador_labirintos(tamanho_do_grafo = 8):
    labirinto = []
    coordenadas1 = [i for i in range(tamanho_do_grafo+1)]
    coordenadas2 = [i for i in range(tamanho_do_grafo)]
    todas_horizontais = list(product(coordenadas2,coordenadas1))
    lista_h = todas_horizontais.copy()
    
    todas_verticais = list(product(coordenadas1,coordenadas2))
    todas_verticais.remove((0,0))
    todas_verticais.remove((tamanho_do_grafo,tamanho_do_grafo-1))
    lista_v = todas_verticais.copy()
    
    grafo_criado = criando_o_grafo_final(tamanho_do_grafo)
    nph,npv = desconverte_de_grafo(grafo_criado)
    for ph in nph:
        if ph in lista_h:
            lista_h.remove(ph)
    for pv in npv:
        if pv in lista_v:
            lista_v.remove(pv)
    labirinto.append(lista_h)
    labirinto.append(lista_v)
    return labirinto

gerador_labirintos()
