# DEFINE ALGORITMOS 

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
    return robo.chegou_no_objetivo()

def executar_algoritmo_customizado(
        robo, lista_dos_comandos, 
        max_passos=3000,
        tentou_parar_func=None,
        funcao_de_desenho=None):

    acoes = [
        'anda_reto', 'recua', 'vira_direita', 
        'vira_esquerda', 'vira_180', 'anda_aleatorio'
    ]
    
    while (not robo.venceu() and
            robo.passos < max_passos):
        
        # Checa se o usuário pediu para parar durante a execução
        if tentou_parar_func and tentou_parar_func():
            break
            
        acao_executada = False
        i = 0
        
        while i < len(lista_dos_comandos):
            comando = lista_dos_comandos[i]
            
            if comando == 'se':
                i += 1
                condicao_tokens = []
                
                while (i < len(lista_dos_comandos) and 
                        lista_dos_comandos[i] not in acoes and
                        lista_dos_comandos[i] not in ['se', 'senao']):
                    
                    condicao_tokens.append(lista_dos_comandos[i])
                    i += 1
                    
                acao_alvo = lista_dos_comandos[i] if (i < len(lista_dos_comandos) and lista_dos_comandos[i] in acoes) else None
                
                expressao = []
                for tok in condicao_tokens:
                    if tok == 'e': 
                        expressao.append('and')
                    elif tok == 'ou': 
                        expressao.append('or')
                    elif tok == 'nao': 
                        expressao.append('not')
                    elif tok in ['(', ')']: 
                        expressao.append(tok) 
                    elif hasattr(robo, tok): expressao.append(f"robo.{tok}()")
                
                condicao_verdadeira = False
                if expressao:
                    try:
                        condicao_verdadeira = eval(" ".join(expressao), {"robo": robo})
                    except Exception:
                        condicao_verdadeira = False
                        pass 
                        
                if condicao_verdadeira and acao_alvo:
                    getattr(robo, acao_alvo)()
                    acao_executada = True
                    break
                    
                if acao_alvo:
                    i += 1 
                    
            elif comando == 'senao':
                i += 1
                if i < len(lista_dos_comandos) and lista_dos_comandos[i] in acoes:
                    getattr(robo, lista_dos_comandos[i])()
                    acao_executada = True
                    break
        
            elif comando in acoes:
                getattr(robo, comando)()
                acao_executada = True
                break
                
            else:
                i += 1
                
        # Atualização da tela com o passo do robô
        if acao_executada and funcao_de_desenho:
            funcao_de_desenho()
            
        if not acao_executada:
            break
            
    return robo.venceu()
