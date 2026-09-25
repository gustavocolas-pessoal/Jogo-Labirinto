import pygame as pg
import sys
import gera_labirintos as gl
from robo import Robo
import define_algoritmos as da  


# VARIÁVEIS:
SIZE = 10
PORTAL = True 
QUANTAS_CHAVES = 4

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

largura = 1300
altura = 700

tela = pg.display.set_mode((largura, altura))
pg.display.set_caption("LABIRINTO")

arial = pg.font.SysFont("Arial", 30)
arial_pequena = pg.font.SysFont("Arial", 20) 

branco = (230,230,230)
preto = (0,0,0)
vermelhin = (150,3,3)
bege = (194,176,146)
azulzin = (135,206,235)
verde_botao = (50, 200, 50)


piskel_chave = pg.image.load("imagens/chave.png").convert_alpha()
piskel_portal = pg.image.load("imagens/portal.png").convert_alpha()


botao_categoria_logica = pg.Rect(950, 50, 150, 40)
botao_categoria_sensor = pg.Rect(950, 100, 150, 40)
botao_categoria_acao = pg.Rect(950, 150, 150, 40)
botao_executar = pg.Rect(600, 620, 200, 40)
botao_limpar = pg.Rect(820, 620, 100, 40)

opcoes_por_categoria = {
    'SENSOR': [
        "tem_parede_frente", 
        "tem_parede_direita", 
        "tem_parede_esquerda",
        "ja_passou_frente",    
        "ja_passou_direita",   
        "ja_passou_esquerda",  
        "tem_portal",
        "tem_chave"
    ],
    'AÇÃO': [
        "anda_reto", 
        "recua", 
        "vira_direita", 
        "vira_esquerda", 
        "vira_180",
        "anda_aleatorio"
    ],
    'LÓGICA': [
        "se", 
        "senao", # identico ao "elif", pensando se muda o nome pra ficar mais claro
        "e", 
        "ou", 
        "nao",
        "(",                   
        ")"                    
    ]
}

tamanho_px = 500
pos_inicial = 50

def define_o_labirinto(tamanho_do_labirinto=SIZE):
    tamanho_celula = tamanho_px // tamanho_do_labirinto
    labirinto = pg.Rect(pos_inicial, pos_inicial, tamanho_px, tamanho_px)
    coords = [pos_inicial + k*tamanho_celula for k in range(tamanho_do_labirinto + 1)]
    return labirinto, coords, tamanho_do_labirinto

labirinto, coords, tamanho_do_labirinto = define_o_labirinto()
tamanho_celula = (tamanho_px // tamanho_do_labirinto)

chave_redimensionada = pg.transform.scale(piskel_chave, (tamanho_celula, tamanho_celula))
portal_redimensionado = pg.transform.scale(piskel_portal, (tamanho_celula, tamanho_celula))

def desenha_grade():
    pg.draw.rect(tela, azulzin, labirinto)
    for x in coords:
        for y in coords:
            grid_h = pg.Rect(x,y, tamanho_celula, 3)
            grid_v = pg.Rect(x,y, 3, tamanho_celula + 3)
            if x != coords[-1]:
                pg.draw.rect(tela, bege, grid_h)
            if y != coords[-1]:
                pg.draw.rect(tela, bege, grid_v)

def desenha_paredes(qual):
    for ph in qual[0]:
        x = coords[ph[0]]
        y = coords[ph[1]]
        pg.draw.rect(tela, preto, (x, y, tamanho_celula, 4))
    
    texto_qual_labirinto = arial.render(
        f"LABIRINTO {lista_labirintos.index(qual)+1}:", True, preto)
    tela.blit(texto_qual_labirinto, (50,10))

    for pv in qual[1]:
        x = coords[pv[0]]
        y = coords[pv[1]]
        pg.draw.rect(tela, preto, (x, y, 4, tamanho_celula + 3))

def desenha_pos_atual(robo):
    x = pos_inicial + tamanho_celula//4 + robo.x*tamanho_celula
    y = pos_inicial + tamanho_celula//4 + robo.y*tamanho_celula
    pg.draw.rect(tela, vermelhin, (x,y, tamanho_celula//2, tamanho_celula//2))

def desenha_portais(portais):
    for portal in portais:
        x = pos_inicial + portal[0]*tamanho_celula
        y = pos_inicial + portal[1]*tamanho_celula
        tela.blit(portal_redimensionado, (x, y))

def desenha_chaves(chaves, robo):
    for chave in chaves:
        if chave not in robo.chaves_coletadas:
            x = pos_inicial + chave[0]*tamanho_celula
            y = pos_inicial + chave[1]*tamanho_celula
            tela.blit(chave_redimensionada, (x, y))

def desenha_ganhou(robo):
    if robo.venceu():
        texto = arial.render(f"PARABÉNS! Você venceu com {robo.passos} passos", True, preto)
        tela.blit(texto, (50,570))


def desenha_botoes():
    botoes_sub_ativos.clear() 

    caixa_alg = pg.Rect(600, 50, 320, 550)
    pg.draw.rect(tela, branco, caixa_alg) 
    pg.draw.rect(tela, preto, caixa_alg, 2) 
    tela.blit(arial.render("ALGORITMO MONTADO:", True, preto), (600, 10))

    y_algoritmo = 60
    for i, bloco in enumerate(algoritmo_montado):
        texto_bloco = arial_pequena.render(f"{i+1}. {bloco}", True, vermelhin)
        tela.blit(texto_bloco, (620, y_algoritmo))
        y_algoritmo += 25

    tela.blit(arial.render("FUNÇÕES:", True, preto), (950, 10))
    
    cores_ativacao = {
        'SENSOR': azulzin if categoria_atual == 'SENSOR' else bege,
        'AÇÃO': azulzin if categoria_atual == 'AÇÃO' else bege,
        'LÓGICA': azulzin if categoria_atual == 'LÓGICA' else bege
    }
    
    for botao, titulo in [(botao_categoria_logica, 'LÓGICA'), (botao_categoria_sensor, 'SENSOR'), (botao_categoria_acao, 'AÇÃO')]:
        pg.draw.rect(tela, cores_ativacao[titulo], botao)
        pg.draw.rect(tela, preto, botao, 2)
        tela.blit(arial_pequena.render(titulo, True, preto), (botao.x + 10, botao.y + 10))

    caixa_opcoes = pg.Rect(950, 210, 300, 450)
    pg.draw.rect(tela, bege, caixa_opcoes, 2) 
    
    if categoria_atual:
        tela.blit(arial_pequena.render(f"Opções de {categoria_atual}:", True, preto), (960, 220))
        y_opcoes = 250
        for opcao in opcoes_por_categoria[categoria_atual]:
            btn_opcao = pg.Rect(960, y_opcoes, 280, 35)
            pg.draw.rect(tela, azulzin, btn_opcao)
            pg.draw.rect(tela, preto, btn_opcao, 1)
            tela.blit(arial_pequena.render(opcao, True, preto), (btn_opcao.x + 10, btn_opcao.y + 7))
            botoes_sub_ativos.append((btn_opcao, opcao))
            y_opcoes += 45 
    else:
        tela.blit(arial_pequena.render("Clique em uma função", True, preto), (960, 220))

    pg.draw.rect(tela, verde_botao, botao_executar) 
    tela.blit(arial_pequena.render("EXECUTAR", True, branco), (botao_executar.x + 50, botao_executar.y + 10))
    
    pg.draw.rect(tela, vermelhin, botao_limpar)
    tela.blit(arial_pequena.render("LIMPAR", True, branco), (botao_limpar.x + 19, botao_limpar.y + 10))

def atualiza_tela_animacao():
    """
    redesenha a tela toda vez que o robô der um passo.
    """
    pg.event.pump() # CORREÇÃO: Evita que o Windows ache que o jogo "Travou" (Not Responding)
    
    tela.fill(branco)
    desenha_grade()
    if desenhar_labirinto:
        desenha_paredes(qual_labirinto)
    desenha_portais(qual_labirinto[2])
    desenha_chaves(qual_labirinto[3], robo)
    desenha_pos_atual(robo)
    desenha_ganhou(robo)
    desenha_botoes()
    
    pg.display.flip()
    pg.time.delay(300) 


rodando = True
desenhar_labirinto = True
indice_labirinto = 0
categoria_atual = None
botoes_sub_ativos = [] 
algoritmo_montado = [] 
tentou_parar = False


while rodando:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            rodando = False

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1: 
                pos_mouse = event.pos
                
                if botao_categoria_sensor.collidepoint(pos_mouse):
                    categoria_atual = 'SENSOR'
                elif botao_categoria_acao.collidepoint(pos_mouse):
                    categoria_atual = 'AÇÃO'
                elif botao_categoria_logica.collidepoint(pos_mouse):
                    categoria_atual = 'LÓGICA'
                    
                for rect_botao, nome_opcao in botoes_sub_ativos:
                    if rect_botao.collidepoint(pos_mouse):
                        algoritmo_montado.append(nome_opcao)
                        
                if botao_limpar.collidepoint(pos_mouse):
                    algoritmo_montado.clear()
                    categoria_atual = None
                    robo.reset(inicio=(0, 0), orientacao='H_s')
                    
                if botao_executar.collidepoint(pos_mouse):
                    robo.reset(inicio=(0, 0), orientacao='H_s')
                    print(f"Executando lógica montada: {algoritmo_montado}")
                    
                    da.executar_algoritmo_customizado(
                        robo, 
                        algoritmo_montado, 
                        tentou_parar,
                        funcao_de_desenho=atualiza_tela_animacao,
                    )

        elif event.type == pg.KEYDOWN:

            if event.key == pg.K_SPACE:
                tentou_parar = True
                rodando = False
                

            elif event.key == pg.K_l:
                desenhar_labirinto = not desenhar_labirinto

            elif event.key == pg.K_c:
                print(robo.chaves_coletadas)

            elif event.key == pg.K_n:
                lista_labirintos.append(gl.gerador_labirintos(SIZE, PORTAL, QUANTAS_CHAVES))

            elif event.key == pg.K_r:
                indice_labirinto += 1
                qual_labirinto = lista_labirintos[indice_labirinto % len(lista_labirintos)]
                labirinto_robo = gl.converte_para_robo(SIZE, qual_labirinto)
                robo = Robo(labirinto_robo, SIZE, SIZE)
                tentou_parar = True

            elif event.key == pg.K_p:
                print(f'Você deu {robo.passos} passos até agora.')

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
        desenha_paredes(qual_labirinto)

    desenha_portais(qual_labirinto[2])
    desenha_chaves(qual_labirinto[3], robo)
    desenha_pos_atual(robo)
    desenha_botoes()
    desenha_ganhou(robo)

    pg.display.flip()

pg.quit()
sys.exit()