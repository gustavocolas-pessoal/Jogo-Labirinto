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

    acoes_simples = [
        'anda_reto', 'recua', 'vira_direita', 
        'vira_esquerda', 'vira_180', 'anda_aleatorio', 'limpar_memoria_passos'
    ]
    
    def executar_bloco(tokens, idx):
        """
        Interpreta recursivamente a lista de tokens.
        Retorna (acoes_executadas, novo_idx).
        """
        if idx >= len(tokens):
            return False, idx

        comando = tokens[idx]

        if isinstance(comando, tuple) and comando[0] == 'anda_bussola':
            robo.anda_bussola(comando[1])
            return True, idx + 1

        elif comando in acoes_simples:
            getattr(robo, comando)()
            return True, idx + 1

        elif comando == 'se':
            idx += 1

            
            condicao_tokens = []
            if idx < len(tokens) and tokens[idx] == '(':
                idx += 1
                nivel = 1
                while idx < len(tokens) and nivel > 0:
                    if tokens[idx] == '(':
                        nivel += 1
                        condicao_tokens.append('(')
                    elif tokens[idx] == ')':
                        nivel -= 1
                        if nivel > 0:
                            condicao_tokens.append(')')
                    else:
                        condicao_tokens.append(tokens[idx])
                    idx += 1
            else:
                # Se não usou parênteses na condição, pega tokens até a próxima ação/parêntese/palavra reservada
                while (idx < len(tokens) and 
                       tokens[idx] not in acoes_simples and 
                       not isinstance(tokens[idx], tuple) and 
                       tokens[idx] not in ['se', 'senao', '(']):
                    condicao_tokens.append(tokens[idx])
                    idx += 1

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
                elif hasattr(robo, tok): 
                    expressao.append(f"robo.{tok}()")

            condicao_verdadeira = False
            if expressao:
                try:
                    condicao_verdadeira = eval(" ".join(expressao), {"robo": robo})
                except Exception:
                    condicao_verdadeira = False

            
            acoes_se_tokens = []
            if idx < len(tokens) and tokens[idx] == '(':
                idx += 1
                nivel = 1
                while idx < len(tokens) and nivel > 0:
                    if tokens[idx] == '(':
                        nivel += 1
                        acoes_se_tokens.append('(')
                    elif tokens[idx] == ')':
                        nivel -= 1
                        if nivel > 0:
                            acoes_se_tokens.append(')')
                    else:
                        acoes_se_tokens.append(tokens[idx])
                    idx += 1
            elif idx < len(tokens):
                acoes_se_tokens.append(tokens[idx])
                idx += 1

            fez_acao = False
            if condicao_verdadeira:
                sub_i = 0
                while sub_i < len(acoes_se_tokens):
                    act, sub_i = executar_bloco(acoes_se_tokens, sub_i)
                    if act:
                        fez_acao = True

            if idx < len(tokens) and tokens[idx] == 'senao':
                idx += 1
                acoes_senao_tokens = []
                if idx < len(tokens) and tokens[idx] == '(':
                    idx += 1
                    nivel = 1
                    while idx < len(tokens) and nivel > 0:
                        if tokens[idx] == '(':
                            nivel += 1
                            acoes_senao_tokens.append('(')
                        elif tokens[idx] == ')':
                            nivel -= 1
                            if nivel > 0:
                                acoes_senao_tokens.append(')')
                        else:
                            acoes_senao_tokens.append(tokens[idx])
                        idx += 1
                elif idx < len(tokens):
                    acoes_senao_tokens.append(tokens[idx])
                    idx += 1

                if not condicao_verdadeira:
                    sub_i = 0
                    while sub_i < len(acoes_senao_tokens):
                        act, sub_i = executar_bloco(acoes_senao_tokens, sub_i)
                        if act:
                            fez_acao = True

            return fez_acao, idx

        # 3. SENAO ISOLADO (caso seja colocado fora do 'se')
        elif comando == 'senao':
            idx += 1
            if idx < len(tokens) and tokens[idx] == '(':
                idx += 1
                nivel = 1
                sub_tokens = []
                while idx < len(tokens) and nivel > 0:
                    if tokens[idx] == '(':
                        nivel += 1
                        sub_tokens.append('(')
                    elif tokens[idx] == ')':
                        nivel -= 1
                        if nivel > 0:
                            sub_tokens.append(')')
                    else:
                        sub_tokens.append(tokens[idx])
                    idx += 1
                
                fez_acao = False
                sub_i = 0
                while sub_i < len(sub_tokens):
                    act, sub_i = executar_bloco(sub_tokens, sub_i)
                    if act:
                        fez_acao = True
                return fez_acao, idx
            else:
                return executar_bloco(tokens, idx)

        return False, idx + 1

    i = 0
    while not robo.venceu() and robo.passos < max_passos:
        if tentou_parar_func and tentou_parar_func():
            break

        if not lista_dos_comandos:
            break

        if i >= len(lista_dos_comandos):
            i = 0

        acao_executada, novo_i = executar_bloco(lista_dos_comandos, i)
        
        # se nenhuma instrução avançou o índice, incrementa para evitar loop infinito
        if novo_i == i:
            i += 1
        else:
            i = novo_i

        if acao_executada and funcao_de_desenho:
            funcao_de_desenho()

        if not acao_executada and i >= len(lista_dos_comandos):
            i = 0

    return robo.venceu()
