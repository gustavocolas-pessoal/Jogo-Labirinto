import time

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
        # tentou_parar = False,
        funcao_de_desenho=None):

    acoes = [
        'anda_reto', 'recua', 'vira_direita', 
        'vira_esquerda', 'vira_180', 'anda_aleatorio'
    ]
    
    while (not robo.venceu() and
            robo.passos < max_passos 
            # and not tentou_parar
            ):
        acao_executada = False
        i = 0
        
        while i < len(lista_dos_comandos):
            comando = lista_dos_comandos[i]
            
            if comando == 'se':
                i += 1
                condicao_tokens = [] # abre a aba do 'se' pra avaliar a expressão formada
                
                # coleta todos os sensores e operadores até encontrar uma ação (ou o final do script)
                while (i < len(lista_dos_comandos) and 
                        lista_dos_comandos[i] not in acoes and
                        lista_dos_comandos[i] not in ['se', 'senao']):
                    
                    condicao_tokens.append(lista_dos_comandos[i])
                    i += 1
                    
                # a ação a ser executada será o token imediatamente após a condição
                acao_alvo = lista_dos_comandos[i] if (i < len(lista_dos_comandos) and lista_dos_comandos[i] in acoes) else None
                
                # traduz a expressão 'natural' pra 'linguagem de programação'
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
                        # EVAL é a chave que permite avaliar as sentenças!!!
                        condicao_verdadeira = eval(" ".join(expressao), {"robo": robo})
                    except Exception:
                        # se a lógica não faz sentido - tipo montar parênteses vazios,
                        # ele vai simplesmente considerar falso
                        condicao_verdadeira = False
                        pass 
                        
                if condicao_verdadeira and acao_alvo:
                    getattr(robo, acao_alvo)()
                    acao_executada = True
                    break # recomeça o loop do algoritmo para o próximo passo
                    
                # se a expressao final foi falsa, pula a ação para não executá-la
                if acao_alvo:
                    i += 1 
                    
            elif comando == 'senao': # é um elif
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
                i += 1 # CORREÇÃO: Ignora blocos quebrados/soltos e continua a leitura
                
        # atualização da tela
        if acao_executada and funcao_de_desenho:
            funcao_de_desenho()
            
        # impede o jogo de travar se o algoritmo gerar um loop que nunca é executado
        if not acao_executada:
            break
            
    return robo.venceu()