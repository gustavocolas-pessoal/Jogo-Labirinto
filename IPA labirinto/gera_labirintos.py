# GERA LABIRINTOS

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
    while tentativas < 10000:
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

def dfs_lista(grafo_completo, vertice = (0,0), visitados=None):
    if visitados is None:
        visitados = []   
    visitados.append(vertice)                      
    for seguinte in grafo_completo[vertice]:  
        if seguinte not in visitados:
            dfs_lista(grafo_completo, seguinte, visitados)
    return visitados

def cria_portal(grafo,lista):
    casas_candidatas = [e for e in lista if e != (0,0)]
    com_portal = choice(casas_candidatas)
    return com_portal

def cria_chave(grafo, lista, portais = []):
    tamanho= int((len(grafo))**(1/2))
    saida = (tamanho-1,tamanho-1)
    indice = lista.index(saida)
    quase_casas_candidatas = lista[(indice+1):]
    casas_candidatas = [e for e in quase_casas_candidatas if e not in portais]
    com_chave = choice(casas_candidatas)
    return com_chave

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


def gerador_labirintos(tamanho_do_grafo = 8, quer_portal = False, quantas_chaves = 0):
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


    lista = dfs_lista(grafo_criado)
    saida = (tamanho_do_grafo-1,tamanho_do_grafo-1)
    indice = lista.index(saida)
    quantas_chaves_real = min(quantas_chaves,indice)
    portais = []
    if quer_portal:
            portal = cria_portal(grafo_criado,lista)
            portais.append(portal)
            
    chaves = []
    for _ in range(quantas_chaves_real):
        chave = cria_chave(grafo_criado,lista, portais)
        chaves.append(chave) 

    labirinto.append(portais)
    labirinto.append(chaves)
    return labirinto


def converte_para_robo(tamanho_do_grafo, labirinto_em_lista):
    """
    Pega o formato da lista, da função gerador_labirintos:

    [
        paredes_horizontais,
        paredes_verticais,
        portais,
        chaves
    ]

    E converte numa estrura mais compatível com a classe Robo:

    {
        (x,y): (
            {'V_e': bool, 'H_s': bool, 'V_s': bool, 'H_e': bool},
            tem_chave,
            tem_portal
        )
    }
    """

    paredes_h = labirinto_em_lista[0]
    paredes_v = labirinto_em_lista[1]
    portais = labirinto_em_lista[2]
    chaves = labirinto_em_lista[3]

    labirinto_final = {}

    for x, y in gera_grafo(tamanho_do_grafo):

        paredes = {
            'V_e': False,
            'H_s': False,
            'V_s': False,
            'H_e': False
        }

        # Parede na direção vertical sentido entrada
        if (x, y) in paredes_h:
            paredes['V_e'] = True

        # Parede na direção vertical sentido saída
        if (x, y + 1) in paredes_h:
            paredes['V_s'] = True

        # Parede na direção horizontal sentido entrada
        if (x, y) in paredes_v:
            paredes['H_e'] = True

        # Parede na direção horizontal sentido saída
        if (x + 1, y) in paredes_v:
            paredes['H_s'] = True

        tem_portal = (x,y) in portais
        tem_chave = (x, y) in chaves

        labirinto_final[(x,y)] = [paredes,tem_portal,tem_chave]

    return labirinto_final

