    # ROBO
import random

DIRECOES = ['V_e', 'H_s', 'V_s', 'H_e']

DELTA = {
    'V_e': (0, -1),
    'H_s': (1, 0),
    'V_s': (0, 1),
    'H_e': (-1, 0)
}

PAREDES = 0
PORTAL = 1
CHAVE = 2

class Robo:

    def __init__(
        self,
        labirinto,
        largura,
        altura,
        inicio=(0, 0),
        objetivo=None,
        orientacao='H_s'
    ):

        self.labirinto = labirinto
        self.largura = largura
        self.altura = altura

        self.x, self.y = inicio
        self.orientacao = orientacao

        self.objetivo = (
            objetivo
            if objetivo is not None
            else (largura - 1, altura - 1)
        )

        self.passos = 0
        self.ja_passou = [inicio]
        self.chaves_coletadas = []
        self.total_chaves = sum(1
            for c in labirinto
            if labirinto[c][CHAVE]
        )

    def posicao(self):
        pos = self.x,self.y
        return pos
    
    def tem_parede_frente(self):
        return self.labirinto[self.posicao()][PAREDES][self.orientacao]

    def tem_parede_direita(self):
        i = DIRECOES.index(self.orientacao)
        direita = DIRECOES[(i + 1) % 4]
        return self.labirinto[self.posicao()][PAREDES][direita]

    def tem_parede_esquerda(self):
        i = DIRECOES.index(self.orientacao)
        esquerda = DIRECOES[(i - 1) % 4]
        return self.labirinto[self.posicao()][PAREDES][esquerda]

    def tem_parede_atras(self):
        i = DIRECOES.index(self.orientacao)
        atras = DIRECOES[(i + 2) % 4]
        return self.labirinto[self.posicao()][PAREDES][atras]

    def paredes_ao_redor(self):
        return dict(
            self.labirinto[self.posicao()][PAREDES]
        )


    def tem_portal(self):
        return self.labirinto[self.posicao()][PORTAL]

    def teletransporta(self):
        portais = []
        if not self.tem_portal():
            return False
        
        for casa in self.labirinto:
            if self.labirinto[casa][PORTAL]:
                portais.append(casa)

        indice = portais.index(self.posicao())
        destino = portais[indice - 1]
        self.x, self.y = destino
        self.ja_passou.append(destino)

        if len(portais) < 2:
                    return False
        return self.posicao() == self.objetivo and len(self.chaves_coletadas) == self.total_chaves

    def tem_chave(self):
            return self.labirinto[self.posicao()][CHAVE]

    def coleta_chave(self):
        if self.tem_chave():
            pos = self.posicao()
            if pos not in self.chaves_coletadas:
                self.chaves_coletadas.append(pos)    

    def anda_reto(self):
        if not self.tem_parede_frente():
            dx, dy = DELTA[self.orientacao]
            self.x += dx
            self.y += dy
            self.ja_passou.append(self.posicao())
            self.coleta_chave()
            self.teletransporta()
            self.passos += 1
            return True
        self.passos += 1
        return False

    def recua(self):
        i = DIRECOES.index(self.orientacao)
        orientacao_oposta = DIRECOES[(i + 2) % 4]
        if not self.labirinto[self.posicao()][PAREDES][orientacao_oposta]:
            dx, dy = DELTA[orientacao_oposta]
            self.x += dx
            self.y += dy
            self.ja_passou.append(self.posicao())
            self.coleta_chave()
            self.teletransporta()
        self.passos += 1

    def vira_direita(self):
        i = DIRECOES.index(self.orientacao)
        self.orientacao = DIRECOES[(i + 1) % 4]

    def vira_esquerda(self):
        i = DIRECOES.index(self.orientacao)
        self.orientacao = DIRECOES[(i - 1) % 4]

    def vira_180(self):
        self.vira_direita()
        self.vira_direita()

    def anda_aleatorio(self, n=1):
        for _ in range(n):
            livres = [
                d for d in DIRECOES
                if not self.labirinto[self.posicao()][PAREDES][d]]

            if livres:
                self.orientacao = random.choice(livres)
                self.anda_reto()


    def reset(self, inicio=(0, 0), orientacao='H_s'):
        self.x, self.y = inicio
        self.orientacao = orientacao
        self.passos = 0
        self.ja_passou = [inicio]
        self.chaves_coletadas = []

    def venceu(self):
        return (self.posicao() == self.objetivo and
            len(self.chaves_coletadas) == self.total_chaves)