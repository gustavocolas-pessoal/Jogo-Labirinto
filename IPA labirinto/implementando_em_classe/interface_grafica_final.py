import pygame as pg
import sys

import gera_labirintos as gl
from robo import Robo

# VARIÁVEIS:

SIZE = 10 # variável!
PORTAL = True # variável!
QUANTAS_CHAVES = 4 # variável!


lista_labirintos = [
    gl.gerador_labirintos(
        SIZE,
        PORTAL,
        QUANTAS_CHAVES
    )
]

qual_labirinto = lista_labirintos[0]

labirinto_robo = gl.converte_para_robo(
    SIZE,
    qual_labirinto
)

robo = Robo(
    labirinto_robo,
    SIZE,
    SIZE
)

pg.init()

largura = 900
altura = 600

tela = pg.display.set_mode((largura, altura))
pg.display.set_caption("LABIRINTO")

arial = pg.font.SysFont("Arial", 30)

branco = (230,230,230)
preto = (0,0,0)
vermelhin = (150,3,3)
bege = (194,176,146)
azulzin_1 = (135,206,235)

piskel_chave = pg.image.load(
    "imagens/chave.png"
).convert_alpha()

piskel_portal = pg.image.load(
    "imagens/portal.png"
).convert_alpha()

tamanho_px = 500
pos_inicial = 50


def define_o_labirinto(
    tamanho_do_labirinto=SIZE
):

    tamanho_celula = (
        tamanho_px //
        tamanho_do_labirinto
    )

    labirinto = pg.Rect(
        pos_inicial,
        pos_inicial,
        tamanho_px,
        tamanho_px
    )

    coords = [
        pos_inicial + k*tamanho_celula
        for k in range(
            tamanho_do_labirinto + 1
        )
    ]

    return (
        labirinto,
        coords,
        tamanho_do_labirinto
    )

labirinto, coords, tamanho_do_labirinto = (
    define_o_labirinto()
)

tamanho_celula = (tamanho_px //tamanho_do_labirinto)

chave_redimensionada = pg.transform.scale(
    piskel_chave,
    (tamanho_celula, tamanho_celula))

portal_redimensionado = pg.transform.scale(
    piskel_portal,
    (tamanho_celula, tamanho_celula))


def desenha_grade():

    pg.draw.rect(tela,azulzin_1,labirinto)

    for x in coords:
        for y in coords:

            grid_h = pg.Rect(
                x,y,
                tamanho_celula,3
            )

            grid_v = pg.Rect(
                x,y,
                3,tamanho_celula + 3
            )

            if x != coords[-1]:
                pg.draw.rect(
                    tela,
                    bege,
                    grid_h
                )

            if y != coords[-1]:
                pg.draw.rect(
                    tela,
                    bege,
                    grid_v
                )

def desenha_paredes(qual):

    for ph in qual[0]:

        x = coords[ph[0]]
        y = coords[ph[1]]

        pg.draw.rect(
            tela,
            preto,
            (
                x,y,
                tamanho_celula,4))
    
    texto_qual_labirinto = arial.render(
        f"LABIRINTO {lista_labirintos.index(qual)+1}:", True, preto)

    tela.blit(texto_qual_labirinto, (50,10))

    for pv in qual[1]:

        x = coords[pv[0]]
        y = coords[pv[1]]

        pg.draw.rect(
            tela,
            preto,
            (
                x,y,
                4,tamanho_celula + 3
            )
        )

def desenha_pos_atual(robo):

    x = (
        pos_inicial +
        tamanho_celula//4 +
        robo.x*tamanho_celula
    )

    y = (
        pos_inicial +
        tamanho_celula//4 +
        robo.y*tamanho_celula
    )

    pg.draw.rect(
        tela,
        vermelhin,
        (x,y,
        tamanho_celula//2,tamanho_celula//2)
    )

def desenha_portais(portais):

    for portal in portais:

        x = pos_inicial + portal[0]*tamanho_celula
        y = pos_inicial + portal[1]*tamanho_celula

        tela.blit(
            portal_redimensionado,
            (x, y)
        )

def desenha_chaves(chaves, robo):

    for chave in chaves:

        if chave not in robo.chaves_coletadas:

            x = (
                pos_inicial +
                chave[0]*tamanho_celula
            )

            y = (
                pos_inicial +
                chave[1]*tamanho_celula
            )

            tela.blit(
                chave_redimensionada,
                (x, y)
            )

def desenha_ganhou(robo):

    if robo.venceu():

        texto = arial.render(
            "GANHOOOOOU!",
            True,
            preto
        )

        tela.blit(
            texto,
            (350,10)
        )

rodando = True
desenhar_labirinto = True
indice_labirinto = 0

while rodando:

    for event in pg.event.get():

        if event.type == pg.QUIT:
            rodando = False

        elif event.type == pg.KEYDOWN:

            if event.key == pg.K_SPACE:
                rodando = False

            elif event.key == pg.K_l:

                desenhar_labirinto = (
                    not desenhar_labirinto
                )

            elif event.key == pg.K_c:

                print(robo.chaves_coletadas)

            elif event.key == pg.K_n:

                lista_labirintos.append(
                    gl.gerador_labirintos(
                        SIZE,
                        PORTAL,
                        QUANTAS_CHAVES
                    )
                )

            elif event.key == pg.K_r:

                indice_labirinto += 1

                qual_labirinto = (
                    lista_labirintos[
                        indice_labirinto %
                        len(lista_labirintos)
                    ]
                )

                labirinto_robo = (
                    gl.converte_para_robo(
                        SIZE,
                        qual_labirinto
                    )
                )

                robo = Robo(
                    labirinto_robo,
                    SIZE,
                    SIZE
                )

            elif event.key == pg.K_UP:

                robo.orientacao = 'V_e'
                robo.anda_reto()

            elif event.key == pg.K_DOWN:

                robo.orientacao = 'V_s'
                robo.anda_reto()

            elif event.key == pg.K_RIGHT:

                robo.orientacao = 'H_s'
                robo.anda_reto()

            elif event.key == pg.K_LEFT:

                robo.orientacao = 'H_e'
                robo.anda_reto()

    tela.fill(branco)

    desenha_grade()

    if desenhar_labirinto:
        desenha_paredes(
            qual_labirinto
        )

    desenha_portais(
        qual_labirinto[2]
    )

    desenha_chaves(
        qual_labirinto[3],
        robo
    )

    desenha_pos_atual(
        robo
    )

    desenha_ganhou(
        robo
    )

    pg.display.flip()

pg.quit()
sys.exit()
