import pygame as pg
import sys 
import logica_do_jogo as lg

pg.init() 

largura = 900
altura = 600

tela = pg.display.set_mode((largura, altura)) 
pg.display.set_caption("LABIRINTO") 

arial = pg.font.SysFont("Arial", 30)
arial_pequeno = pg.font.SysFont("Arial", 22)
arial_huge = pg.font.SysFont("Arial", 50)

branco = (230,230,230)
preto = (0,0,0)
quase_preto = (30,30,30)
verdin = (40,147,47)
vermelhin = (150,3,3)
bege = (194,176,146)
cinza = (50,50,50)
azulzin_1 = (135, 206, 235)
azulzin_2 = (50,150,250)

tamanho_px = 500
pos_inicial = 50


def define_o_labirinto(tamanho_do_labirinto=8):
    tamanho_celula = tamanho_px // tamanho_do_labirinto
    labirinto = pg.Rect(pos_inicial, pos_inicial, tamanho_px, tamanho_px)
    coords = [pos_inicial + k * tamanho_celula for k in range(tamanho_do_labirinto + 1)]
    return labirinto, coords, tamanho_do_labirinto

labirinto, coords = define_o_labirinto(lg.size)[0],define_o_labirinto(lg.size)[1]
tamanho_do_labirinto = define_o_labirinto(lg.size)[2]
tamanho_celula = tamanho_px//tamanho_do_labirinto

def desenha_grade():
    pg.draw.rect(tela, azulzin_1, labirinto)
    for x in coords:
        for y in coords:
            grid_h = pg.Rect(x, y, tamanho_celula, 3) 
            grid_v = pg.Rect(x, y, 3, (tamanho_celula)+3) 
            if x != coords[-1]:
                pg.draw.rect(tela, bege, grid_h)
            if y != coords[-1]:
                pg.draw.rect(tela, bege, grid_v)

def desenha_paredes(qual):
    for ph in qual[0]:
        x = coords[ph[0]]
        y = coords[ph[1]]
        parede = (x,y,tamanho_celula,4)
        pg.draw.rect(tela,preto,parede)
    for pv in qual[1]:
        x = coords[pv[0]]
        y = coords[pv[1]]
        parede = (x,y,4,tamanho_celula+3)
        pg.draw.rect(tela,preto,parede)

    texto_qual_labirinto = arial.render(
        f"LABIRINTO {lg.lista_labirintos.index(qual)+1}:", True, preto)
    tela.blit(texto_qual_labirinto, (50,10))

def desenha_pos_atual(pos):
    x = pos_inicial + tamanho_celula//4 + (pos[0])*tamanho_celula
    y = pos_inicial + tamanho_celula//4 + (pos[1])*tamanho_celula
    onde = pg.Rect(x,y,tamanho_celula//2,tamanho_celula//2)
    pg.draw.rect(tela,vermelhin,onde)

rodando = True
desenhar_labirinto = True
n = 0

# Sincroniza o labirinto inicial
qual_labirinto = lg.lista_labirintos[0]
lg.qual_labirinto = qual_labirinto

while rodando:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            rodando = False

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                rodando = False

            elif event.key == pg.K_r:
                n += 1
                qual_labirinto = lg.lista_labirintos[(n % (len(lg.lista_labirintos)))]
                # ATUALIZA o labirinto dentro do módulo de lógica também!
                lg.qual_labirinto = qual_labirinto
                # Reinicia a posição ao mudar de labirinto
                lg.pos_atual = (0, 0)

            elif event.key == pg.K_l:
                desenhar_labirinto = not desenhar_labirinto

            elif event.key == pg.K_n:
                lg.lista_labirintos.append(lg.gerador_labirintos(lg.size))

            # Movimentos atualizando a variável lg.pos_atual diretamente
            elif event.key == pg.K_UP:
                lg.permite_movimento(lg.tenta_vertical_entrada()[0])

            elif event.key == pg.K_DOWN:
                lg.permite_movimento(lg.tenta_vertical_saida()[0])

            elif event.key == pg.K_RIGHT:
                lg.permite_movimento(lg.tenta_horizontal_saida()[0])

            elif event.key == pg.K_LEFT:
                lg.permite_movimento(lg.tenta_horizontal_entrada()[0])

    tela.fill(branco)
    desenha_grade()
    
    # Desenha a posição atualizada vinda direto da lógica do jogo
    desenha_pos_atual(lg.pos_atual)

    if desenhar_labirinto:
        desenha_paredes(qual_labirinto)

    pg.display.flip() 

pg.quit()
sys.exit()
