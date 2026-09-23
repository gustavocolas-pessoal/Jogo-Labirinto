# ALGORITMOS
def segue_parede(robo, max_passos=3000, visualizar=False, atraso=0.03):
    while not robo.chegou_no_objetivo() and robo.passos < max_passos:
        if not robo.tem_parede_direita():
            robo.vira_direita()
            robo.anda_reto()
        elif not robo.tem_parede_frente():
            robo.anda_reto()
        elif not robo.tem_parede_esquerda():
            robo.vira_esquerda()
            robo.anda_reto()
        else:
            robo.vira_180()
            robo.anda_reto()

        # if visualizar:
        #     desenha_labirinto(robo)
        #     time.sleep(atraso)

    return robo.chegou_no_objetivo()

def defina_o_seu():
    return
