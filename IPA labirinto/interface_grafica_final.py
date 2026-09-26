# INTERFACE GRÁFICA FINAL

import pygame as pg
import sys
import gera_labirintos as gl
from robo import Robo
import define_algoritmos as da  

SIZE = 6
PORTAL = False 
QUANTAS_CHAVES = 0

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
pg.display.set_caption("LABIRINTO DO ROBÔ - PERDIDOS NA LÓGICA")

arial = pg.font.SysFont("Arial", 30)
arial_pequena = pg.font.SysFont("Arial", 15) 
arial_titulo = pg.font.SysFont("Arial", 44, bold=True)
arial_subtitulo = pg.font.SysFont("Arial", 16, bold=True)

branco = (230,230,230)
branco_puro = (255, 255, 255)
preto = (0,0,0)
vermelhin = (150,3,3)
bege = (194,176,146)
azulzin = (135,206,235)
azul_destaque = (100, 180, 225)
verde_botao = (50, 200, 50)
verde_hover = (40, 220, 40)
laranja_parar = (220, 100, 0)
roxo_memoria = (180, 150, 220)

piskel_chave = pg.image.load("imagens/chave.png").convert_alpha()
piskel_portal = pg.image.load("imagens/portal.png").convert_alpha()
piskel_robo = pg.image.load("imagens/robo_atualizado.png").convert_alpha()

botao_categoria_logica = pg.Rect(950, 45, 150, 35)
botao_categoria_sensor = pg.Rect(950, 85, 150, 35)
botao_categoria_acao = pg.Rect(950, 125, 150, 35)
botao_categoria_memoria = pg.Rect(950, 165, 150, 35)

botao_executar = pg.Rect(600, 620, 130, 40)
botao_parar = pg.Rect(740, 620, 80, 40)
botao_limpar = pg.Rect(830, 620, 90, 40)
botao_voltar_menu = pg.Rect(50, 630, 120, 35)

caixa_principal = pg.Rect(390, 50, 520, 480)
botao_size_menos = pg.Rect(530, 250, 45, 45)
botao_size_mais = pg.Rect(725, 250, 45, 45)
botao_jogar = pg.Rect(470, 360, 360, 55)

caixa_inferior = pg.Rect(390, 550, 520, 95)
botao_toggle_portal = pg.Rect(415, 585, 210, 40)
botao_chave_menos = pg.Rect(740, 585, 35, 35)
botao_chave_mais = pg.Rect(845, 585, 35, 35)

sensores_disponiveis = [
    "tem_parede_frente", 
    "tem_parede_direita", 
    "tem_parede_esquerda",
    "tem_parede_atras"
]
if PORTAL:
    sensores_disponiveis.append("tem_portal")
if QUANTAS_CHAVES > 0:
    sensores_disponiveis.append("tem_chave")

opcoes_por_categoria = {
    'SENSOR': sensores_disponiveis,
    'AÇÃO': [
        "anda_reto", 
        "recua", 
        "vira_direita", 
        "vira_esquerda", 
        "vira_180",
        ("anda_bussola", "V_e"), # Norte
        ("anda_bussola", "V_s"), # Sul
        ("anda_bussola", "H_s"), # Leste
        ("anda_bussola", "H_e"), # Oeste
        "anda_aleatorio"
    ],
    'LÓGICA': [
        "se", 
        "senao", 
        "e", 
        "ou", 
        "nao",
        "(",                   
        ")"
    ],
    'MEMÓRIA': [
        "ja_passou_frente",
        "ja_passou_direita",
        "ja_passou_esquerda",
        "ja_passou_atras",
        "ja_passou_norte",
        "ja_passou_sul",
        "ja_passou_leste",
        "ja_passou_oeste",
        "limpar_memoria_passos"
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
robo_redimensionado = pg.transform.scale(piskel_robo, (tamanho_celula//2, tamanho_celula//2))

def inicializar_jogo():
    global lista_labirintos, qual_labirinto, labirinto_robo, robo
    global labirinto, coords, tamanho_do_labirinto, tamanho_celula
    global chave_redimensionada, portal_redimensionado, robo_redimensionado
    global opcoes_por_categoria, sensores_disponiveis
    global categoria_atual, algoritmo_montado
    
    lista_labirintos = [gl.gerador_labirintos(SIZE, PORTAL, QUANTAS_CHAVES)]
    qual_labirinto = lista_labirintos[0]
    labirinto_robo = gl.converte_para_robo(SIZE, qual_labirinto)
    robo = Robo(labirinto_robo, SIZE, SIZE)

    labirinto, coords, tamanho_do_labirinto = define_o_labirinto(SIZE)
    tamanho_celula = (tamanho_px // tamanho_do_labirinto)

    chave_redimensionada = pg.transform.scale(piskel_chave, (tamanho_celula, tamanho_celula))
    portal_redimensionado = pg.transform.scale(piskel_portal, (tamanho_celula, tamanho_celula))
    robo_redimensionado = pg.transform.scale(piskel_robo, (tamanho_celula//2, tamanho_celula//2))

    sensores_disponiveis = [
        "tem_parede_frente", 
        "tem_parede_direita", 
        "tem_parede_esquerda",
        "tem_parede_atras"
    ]
    if PORTAL:
        sensores_disponiveis.append("tem_portal")
    if QUANTAS_CHAVES > 0:
        sensores_disponiveis.append("tem_chave")

    opcoes_por_categoria['SENSOR'] = sensores_disponiveis
    
    categoria_atual = None
    algoritmo_montado.clear()

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
    angulos = {'H_s': 0,'V_e': 90,'H_e': 180,'V_s': 270}
    angulo = angulos.get(robo.orientacao, 0)
    robo_rotacionado = pg.transform.rotate(robo_redimensionado, angulo)
    
    centro_x = pos_inicial + robo.x * tamanho_celula + tamanho_celula // 2
    centro_y = pos_inicial + robo.y * tamanho_celula + tamanho_celula // 2
    rect_robo = robo_rotacionado.get_rect(center=(centro_x, centro_y))
    tela.blit(robo_rotacionado, rect_robo.topleft)

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
        texto1 = arial.render(f"PARABÉNS! Você venceu com {robo.passos} passos", True, preto)
        tela.blit(texto1, (50,570))
        texto2 = arial.render(f"O caminho mais rápido era de {qual_labirinto[4]} passos", True, preto)
        if not PORTAL and QUANTAS_CHAVES == 0:
            tela.blit(texto2, (50,600))

def desenha_botoes():
    botoes_sub_ativos.clear() 

    caixa_alg = pg.Rect(600, 50, 320, 550)
    pg.draw.rect(tela, branco_puro, caixa_alg) 
    pg.draw.rect(tela, preto, caixa_alg, 2) 
    tela.blit(arial.render("ALGORITMO MONTADO:", True, preto), (600, 10))

    y_algoritmo = 60
    for i, bloco in enumerate(algoritmo_montado):
        if isinstance(bloco, tuple):
            if bloco[0] in ["anda_bussola", "anda_absoluto"]:
                rotulos = {'V_e': 'norte', 'V_s': 'sul', 'H_s': 'leste', 'H_e': 'oeste'}
                texto_str = f"anda_bussola({rotulos.get(bloco[1], bloco[1])})"
            else:
                texto_str = f"{bloco[0]} ({bloco[1:]})"
        else:
            texto_str = str(bloco)

        texto_bloco = arial_pequena.render(f"{i+1}. {texto_str}", True, vermelhin)
        if i < 22:
            tela.blit(texto_bloco, (620, y_algoritmo))
        elif i == 22:
            y_algoritmo = 60
            tela.blit(texto_bloco, (770, y_algoritmo))
        else:
            tela.blit(texto_bloco, (770, y_algoritmo))
        y_algoritmo += 24

    tela.blit(arial.render("FUNÇÕES:", True, preto), (950, 10))
    
    cores_ativacao = {
        'SENSOR': azulzin if categoria_atual == 'SENSOR' else bege,
        'AÇÃO': azulzin if categoria_atual == 'AÇÃO' else bege,
        'LÓGICA': azulzin if categoria_atual == 'LÓGICA' else bege,
        'MEMÓRIA': roxo_memoria if categoria_atual == 'MEMÓRIA' else bege
    }
    
    botoes_categorias = [
        (botao_categoria_logica, 'LÓGICA'),
        (botao_categoria_sensor, 'SENSOR'),
        (botao_categoria_acao, 'AÇÃO'),
        (botao_categoria_memoria, 'MEMÓRIA')
    ]

    for botao, titulo in botoes_categorias:
        pg.draw.rect(tela, cores_ativacao[titulo], botao)
        pg.draw.rect(tela, preto, botao, 2)
        tela.blit(arial_pequena.render(titulo, True, preto), (botao.x + 10, botao.y + 8))

    caixa_opcoes = pg.Rect(950, 215, 300, 385)
    pg.draw.rect(tela, bege, caixa_opcoes, 2) 
    
    if categoria_atual:
        tela.blit(arial_pequena.render(f"Opções de {categoria_atual}:", True, preto), (960, 220))
        y_opcoes = 242
        for opcao in opcoes_por_categoria[categoria_atual]:
            botao_opcao = pg.Rect(960, y_opcoes, 280, 28)
            
            cor_fundo = roxo_memoria if categoria_atual == 'MEMÓRIA' else azulzin
            pg.draw.rect(tela, cor_fundo, botao_opcao)
            pg.draw.rect(tela, preto, botao_opcao, 1)
            
            if isinstance(opcao, tuple):
                if opcao[0] in ["anda_bussola", "anda_absoluto"]:
                    rotulos = {'V_e': 'norte', 'V_s': 'sul', 'H_s': 'leste', 'H_e': 'oeste'}
                    nome_exibir = f"anda_bussola ({rotulos.get(opcao[1], opcao[1])})"
                else:
                    nome_exibir = f"{opcao[0]}: {opcao[1]}"
            else:
                nome_exibir = str(opcao)

            tela.blit(
                arial_pequena.render(nome_exibir, True, preto), 
                (botao_opcao.x + 10, botao_opcao.y + 5)
            )
            botoes_sub_ativos.append((botao_opcao, opcao))
            y_opcoes += 32 
    else:
        tela.blit(arial_pequena.render("Clique em uma função", True, preto), (960, 220))

    pg.draw.rect(tela, verde_botao, botao_executar) 
    pg.draw.rect(tela, preto, botao_executar, 2)
    tela.blit(arial_pequena.render("EXECUTAR", True, branco_puro), (botao_executar.x + 15, botao_executar.y + 10))

    pg.draw.rect(tela, laranja_parar, botao_parar)
    pg.draw.rect(tela, preto, botao_parar, 2)
    tela.blit(arial_pequena.render("PARAR", True, branco_puro), (botao_parar.x + 10, botao_parar.y + 10))
    
    pg.draw.rect(tela, vermelhin, botao_limpar)
    pg.draw.rect(tela, preto, botao_limpar, 2)
    tela.blit(arial_pequena.render("LIMPAR", True, branco_puro), (botao_limpar.x + 12, botao_limpar.y + 10))

    pg.draw.rect(tela, bege, botao_voltar_menu)
    pg.draw.rect(tela, preto, botao_voltar_menu, 2)
    tela.blit(arial_pequena.render("< MENU", True, preto), (botao_voltar_menu.x + 20, botao_voltar_menu.y + 8))

def checar_parada():
    global tentou_parar
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if botao_parar.collidepoint(event.pos):
                tentou_parar = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                tentou_parar = True
    return tentou_parar

def atualiza_tela_animacao():
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
    pg.time.delay(100) 

def desenha_tela_inicio():
    pos_mouse = pg.mouse.get_pos()
    tela.fill(branco)

    pg.draw.rect(tela, bege, caixa_principal)
    pg.draw.rect(tela, preto, caixa_principal, 2)

    txt_titulo = arial_titulo.render("PERDIDOS NA LÓGICA", True, preto)
    tela.blit(txt_titulo, (largura // 2 - txt_titulo.get_width() // 2, 90))

    txt_sub = arial_subtitulo.render("LABIRINTO DO ROBÔ", True, vermelhin)
    tela.blit(txt_sub, (largura // 2 - txt_sub.get_width() // 2, 145))

    txt_size_label = arial_pequena.render("TAMANHO DO LABIRINTO:", True, preto)
    tela.blit(txt_size_label, (largura // 2 - txt_size_label.get_width() // 2, 215))

    caixa_valor_size = pg.Rect(590, 250, 120, 45)
    pg.draw.rect(tela, branco_puro, caixa_valor_size)
    pg.draw.rect(tela, preto, caixa_valor_size, 2)
    txt_size_val = arial.render(f"{SIZE} x {SIZE}", True, preto)
    tela.blit(txt_size_val, txt_size_val.get_rect(center=caixa_valor_size.center))

    cor_btn_menos = azul_destaque if botao_size_menos.collidepoint(pos_mouse) else azulzin
    pg.draw.rect(tela, cor_btn_menos, botao_size_menos)
    pg.draw.rect(tela, preto, botao_size_menos, 2)
    txt_menos = arial.render("-", True, preto)
    tela.blit(txt_menos, txt_menos.get_rect(center=botao_size_menos.center))

    cor_btn_mais = azul_destaque if botao_size_mais.collidepoint(pos_mouse) else azulzin
    pg.draw.rect(tela, cor_btn_mais, botao_size_mais)
    pg.draw.rect(tela, preto, botao_size_mais, 2)
    txt_mais = arial.render("+", True, preto)
    tela.blit(txt_mais, txt_mais.get_rect(center=botao_size_mais.center))

    cor_jogar = verde_hover if botao_jogar.collidepoint(pos_mouse) else verde_botao
    pg.draw.rect(tela, cor_jogar, botao_jogar)
    pg.draw.rect(tela, preto, botao_jogar, 2)
    txt_jogar = arial.render("JOGAR", True, branco_puro)
    tela.blit(txt_jogar, txt_jogar.get_rect(center=botao_jogar.center))

    pg.draw.rect(tela, branco_puro, caixa_inferior)
    pg.draw.rect(tela, preto, caixa_inferior, 2)

    cor_portal = azulzin if PORTAL else bege
    if botao_toggle_portal.collidepoint(pos_mouse):
        cor_portal = azul_destaque if PORTAL else (210, 195, 165)
    
    pg.draw.rect(tela, cor_portal, botao_toggle_portal)
    pg.draw.rect(tela, preto, botao_toggle_portal, 2)
    txt_portal_status = "PORTAIS: ATIVOS" if PORTAL else "PORTAIS: INATIVOS"
    txt_portal = arial_pequena.render(txt_portal_status, True, preto)
    tela.blit(txt_portal, txt_portal.get_rect(center=botao_toggle_portal.center))

    txt_chaves_label = arial_pequena.render("CHAVES:", True, preto)
    tela.blit(txt_chaves_label, (680, 595))

    caixa_val_chave = pg.Rect(785, 585, 50, 35)
    pg.draw.rect(tela, roxo_memoria, caixa_val_chave)
    pg.draw.rect(tela, preto, caixa_val_chave, 2)
    txt_val_chaves = arial_pequena.render(str(QUANTAS_CHAVES), True, preto)
    tela.blit(txt_val_chaves, txt_val_chaves.get_rect(center=caixa_val_chave.center))

    cor_ch_menos = azul_destaque if botao_chave_menos.collidepoint(pos_mouse) else azulzin
    pg.draw.rect(tela, cor_ch_menos, botao_chave_menos)
    pg.draw.rect(tela, preto, botao_chave_menos, 2)
    txt_ch_menos = arial_pequena.render("-", True, preto)
    tela.blit(txt_ch_menos, txt_ch_menos.get_rect(center=botao_chave_menos.center))

    cor_ch_mais = azul_destaque if botao_chave_mais.collidepoint(pos_mouse) else azulzin
    pg.draw.rect(tela, cor_ch_mais, botao_chave_mais)
    pg.draw.rect(tela, preto, botao_chave_mais, 2)
    txt_ch_mais = arial_pequena.render("+", True, preto)
    tela.blit(txt_ch_mais, txt_ch_mais.get_rect(center=botao_chave_mais.center))

    pg.display.flip()

rodando = True
desenhar_labirinto = True
indice_labirinto = 0
categoria_atual = None
botoes_sub_ativos = [] 
algoritmo_montado = [] 
tentou_parar = False
estado = "inicio"

while rodando:
    if estado == "inicio":
        for event in pg.event.get():
            if event.type == pg.QUIT:
                rodando = False

            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pos_mouse = event.pos
                
                if botao_size_menos.collidepoint(pos_mouse) and SIZE > 3:
                    SIZE -= 1
                elif botao_size_mais.collidepoint(pos_mouse) and SIZE < 15:
                    SIZE += 1
                elif botao_toggle_portal.collidepoint(pos_mouse):
                    PORTAL = not PORTAL
                elif botao_chave_menos.collidepoint(pos_mouse) and QUANTAS_CHAVES > 0:
                    QUANTAS_CHAVES -= 1
                elif botao_chave_mais.collidepoint(pos_mouse) and QUANTAS_CHAVES < 5:
                    QUANTAS_CHAVES += 1
                elif botao_jogar.collidepoint(pos_mouse):
                    inicializar_jogo()
                    estado = "jogo"

            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                rodando = False

        desenha_tela_inicio()

    elif estado == "jogo":
        for event in pg.event.get():
            if event.type == pg.QUIT:
                rodando = False

            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    pos_mouse = event.pos
                    
                    if botao_voltar_menu.collidepoint(pos_mouse):
                        estado = "inicio"

                    elif botao_categoria_sensor.collidepoint(pos_mouse):
                        categoria_atual = 'SENSOR'
                    elif botao_categoria_acao.collidepoint(pos_mouse):
                        categoria_atual = 'AÇÃO'
                    elif botao_categoria_logica.collidepoint(pos_mouse):
                        categoria_atual = 'LÓGICA'
                    elif botao_categoria_memoria.collidepoint(pos_mouse):
                        categoria_atual = 'MEMÓRIA'
                        
                    for rect_botao, nome_opcao in botoes_sub_ativos:
                        if rect_botao.collidepoint(pos_mouse):
                            algoritmo_montado.append(nome_opcao)
                            
                    if botao_limpar.collidepoint(pos_mouse):
                        if algoritmo_montado:
                            algoritmo_montado.pop(-1)
                        categoria_atual = None
                        robo.reset(inicio=(0, 0), orientacao='H_s')

                    if botao_parar.collidepoint(pos_mouse):
                        tentou_parar = True
                        
                    if botao_executar.collidepoint(pos_mouse):
                        tentou_parar = False
                        robo.reset(inicio=(0, 0), orientacao='H_s')
                        
                        da.executar_algoritmo_customizado(
                            robo, 
                            algoritmo_montado, 
                            tentou_parar_func=checar_parada,
                            funcao_de_desenho=atualiza_tela_animacao,
                        )

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    estado = "inicio"

                elif event.key == pg.K_SPACE:
                    tentou_parar = True

                elif event.key == pg.K_l:
                    desenhar_labirinto = not desenhar_labirinto

                elif event.key == pg.K_c:
                    print(robo.chaves_coletadas)

                elif event.key == pg.K_n:
                    lista_labirintos.append(gl.gerador_labirintos(SIZE, PORTAL, QUANTAS_CHAVES))

                elif event.key == pg.K_r:
                    robo.reset()
                    tentou_parar = True

                elif event.key == pg.K_p:
                    indice_labirinto += 1
                    qual_labirinto = lista_labirintos[indice_labirinto % len(lista_labirintos)]
                    labirinto_robo = gl.converte_para_robo(SIZE, qual_labirinto)
                    robo = Robo(labirinto_robo, SIZE, SIZE)

                elif event.key == pg.K_UP:
                    robo.anda_bussola('V_e')     

                elif event.key == pg.K_DOWN:
                    robo.anda_bussola('V_s')     

                elif event.key == pg.K_RIGHT:
                    robo.anda_bussola('H_s')     

                elif event.key == pg.K_LEFT:
                    robo.anda_bussola('H_e')     

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
