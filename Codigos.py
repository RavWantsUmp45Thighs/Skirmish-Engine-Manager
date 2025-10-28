from uuid import uuid4
import json
import os
import random

def gerar_id():
    return str(uuid4())[:7]

def serializar_item(item):
    """Serializa um item para dicionário, incluindo o tipo da classe"""
    if item is None:
        return None
    
    item_dict = item.to_dict()
    item_dict["__class__"] = item.__class__.__name__
    return item_dict

def deserializar_item(item_data):
    """Deserializa um item de um dicionário, criando a instância correta da classe"""
    if item_data is None:
        return None
    
    # Mapeamento de classes
    classes_disponiveis = {
        "Consumivel": Consumivel,
        "Explosivo": Explosivo,
        "Municao": Municao,
        "Melhoria": Melhoria,
        "Melee": Melee,
        "Ranged": Ranged,
        "Protecao": Protecao,
        "Item": Item  # classe base, se necessário
    }
    
    nome_classe = item_data.get("__class__")
    if nome_classe and nome_classe in classes_disponiveis:
        classe = classes_disponiveis[nome_classe]
        # Remove o identificador de classe antes de deserializar
        dados_limpos = {k: v for k, v in item_data.items() if k != "__class__"}
        return classe.from_dict(dados_limpos)
    
    return None


### CLASSE PERSONAGEM ###
### CLASSE PERSONAGEM ###
### CLASSE PERSONAGEM ###
class Personagem:
    def __init__(self, nome, nivel, Forca, Agilidade, Vigor, Inteligencia, Presenca, Tatica, proficiencias_base=None):
        self.nome: str = nome
        self.nivel: int = nivel
        self.XPlvlUp: int = 500 + (500 * nivel)
        self.XPAtual: int = 0
        #atributos#
        self.Forca: int = Forca
        self.Agilidade: int = Agilidade
        self.Vigor: int = Vigor
        self.Inteligencia: int = Inteligencia
        self.Presenca: int = Presenca
        self.Tatica: int = Tatica
        #stats#
        self.vidaMax: int = 100 + (10 * Vigor)
        self.vidaAtual: int = self.vidaMax
        self.PeMax: int = 4 + Presenca
        self.PeAtual: int = self.PeMax
        self.bloqueio: int = 5 + Forca
        self.esquiva: int = 5 + Agilidade
        self.CargaMax: float = 15 + (Forca * 2)
        self.cargaAtual: float = 0
        self.mobilidade: int = 5 + (Agilidade * 2)
        self.percepcao: int = Inteligencia

        #Corpo#
        self.Cabeça = None
        self.Rosto = None
        self.Torso = None
        self.Pernas = None
        self.Braços = None
        #Inventário#
        self.inventario = Inventario()
        self.equipados = Inventario()
        #proficiências#
        self.proficiencias = SistemaDeProficiencias()
        if proficiencias_base:
            for nome, criador in proficiencias_base.items():
                self.proficiencias.proficiencias[nome] = criador
        self.recalcularAtributos()
        self.poderes = GerenciadorDePoderes()
        self.habilidades = GerenciadorDeHabilidades()
        self.buffs_debuffs = GerenciadorDeBuffsDebuffs()
        

    def CriarPersonagem(nome, nivel, Forca, Agilidade, Vigor, Inteligencia, Presenca, Tatica, proficiencias_base=None):
        return Personagem(nome, nivel, Forca, Agilidade, Vigor, Inteligencia, Presenca, Tatica, proficiencias_base)

# funções principais #
    def calcular_peso_total(self):
        peso_total = 0
        
        # Verificar itens no inventário
        for item_data in self.inventario.itens:
            item = item_data['item']
            if hasattr(item, 'peso') and item.peso:
                peso_total += item.peso * item_data['quantidade']
        
        # Verificar itens equipados
        for item_data in self.equipados.itens:
            item = item_data['item']
            if hasattr(item, 'peso') and item.peso:
                peso_total += item.peso * item_data['quantidade']   
        
        # Verificar proteções equipadas
        protecoes = [self.Cabeça, self.Torso, self.Pernas, self.Braços]
        for protecao in protecoes:
            if protecao is not None and hasattr(protecao, 'peso') and protecao.peso:
                peso_total += (protecao.peso // 2)  # Proteção equipada tem peso reduzido

        # Atualiza o peso atual no personagem
        self.cargaAtual = peso_total

    def TomarDano(self, dano):
        self.vidaAtual = max(0, self.vidaAtual - dano)
    
    def TomarCura(self, cura):
        self.vidaAtual += cura
        if self.vidaAtual > self.vidaMax:
            self.vidaAtual = self.vidaMax
        
    def GastarEnergia(self, energia):
        self.PeAtual = max(0, self.PeAtual - energia)

    def GanharEnergia(self, energia):
        self.PeAtual += energia
        if self.PeAtual > self.PeMax:
            self.PeAtual = self.PeMax

    def GanharXP(self, xp):
        self.XPAtual += xp
        if self.XPAtual >= self.XPlvlUp:
            self.XPAtual -= self.XPlvlUp
            self.levelUp()
    
    def levelUp(self):
        self.XPAtual = 0
        self.nivel += 1
        self.recalcularAtributos()
    
    def recalcularAtributos(self):
        self.XPlvlUp = 500 + (500 * self.nivel)

        # Obter níveis das proficiências específicas
        bonus_profs = self.proficiencias.obter_proficiencias("Vitalidade", "Carga", "Combate", "Reflexo", "Atletismo", "Percepção")
        bonus_vida = bonus_profs.get("Vitalidade", 0) * 2
        bonus_carga = bonus_profs.get("Carga", 0) * 1
        bonus_combate = int(bonus_profs.get("Combate", 0) // 2)
        bonus_reflexo = int(bonus_profs.get("Reflexo", 0) // 2)
        bonus_atletismo = int(bonus_profs.get("Atletismo", 0) * 2)
        bonus_percepcao = bonus_profs.get("Percepção", 0) * 1

        # Recalcular atributos com bônus de proficiências
        self.vidaMax = 100 + (10 * self.Vigor) + bonus_vida
        self.vidaAtual = min(self.vidaAtual, self.vidaMax)
        self.PeMax = 4 + self.Presenca
        self.PeAtual = min(self.PeAtual, self.PeMax)
        self.bloqueio = 5 + self.Forca + bonus_combate
        self.esquiva = 5 + self.Agilidade + bonus_reflexo
        self.CargaMax = 15 + (self.Forca * 2) + bonus_carga
        self.mobilidade = 5 + (self.Agilidade * 2) + bonus_atletismo
        self.percepcao: int = self.Inteligencia + bonus_percepcao

        self.calcular_peso_total()
    
    def equipar_item(self, item):
        if self.inventario.remover_item(item):
            self.equipados.adicionar_item_objeto(item)
            return True
        return False

    def desequipar_item(self, item):
        if self.equipados.remover_item(item):
            self.inventario.adicionar_item_objeto(item)
            return True
        return False

    def ReceberKit(self, kit):
        try:
            # Verifica se o kit tem uma lista de itens
            if hasattr(kit, 'itens'):
                # Se kit.itens é uma lista de dicionários com 'item' e 'quantidade'
                if isinstance(kit.itens, list):
                    for item_data in kit.itens:
                        if isinstance(item_data, dict) and 'item' in item_data:
                            item = item_data['item']
                            quantidade = item_data.get('quantidade', 1)
                            self.inventario.adicionar_item_objeto(item, quantidade)
                        else:
                            # Se for apenas um objeto item
                            self.inventario.adicionar_item_objeto(item_data, 1)
                
                # Se kit.itens é um dicionário de itens
                elif isinstance(kit.itens, dict):
                    for nome_item, quantidade in kit.itens.items():
                        if hasattr(quantidade, '__call__'):  # Se for uma função construtora
                            item = quantidade()
                            self.inventario.adicionar_item_objeto(item, 1)
                        else:
                            # Assumindo que é uma quantidade numérica e precisamos do objeto
                            # Neste caso, seria necessário ter acesso aos dicionários de itens
                            pass
            
            # Se o kit é uma lista direta de itens
            elif isinstance(kit, list):
                for item in kit:
                    if isinstance(item, dict) and 'item' in item:
                        objeto_item = item['item']
                        quantidade = item.get('quantidade', 1)
                        self.inventario.adicionar_item_objeto(objeto_item, quantidade)
                    else:
                        self.inventario.adicionar_item_objeto(item, 1)
            
            # Se o kit é um dicionário direto
            elif isinstance(kit, dict):
                for nome_item, item_info in kit.items():
                    if isinstance(item_info, dict) and 'item' in item_info:
                        item = item_info['item']
                        quantidade = item_info.get('quantidade', 1)
                        self.inventario.adicionar_item_objeto(item, quantidade)
                    elif hasattr(item_info, '__call__'):  # Se for uma função construtora
                        item = item_info()
                        self.inventario.adicionar_item_objeto(item, 1)
                    else:
                        # Tratamento para outros tipos de estrutura
                        self.inventario.adicionar_item_objeto(item_info, 1)
            
            # Recalcula o peso após adicionar os itens
            self.calcular_peso_total()
            
            print(f"{self.nome} recebeu o kit com sucesso!")
            return True
            
        except Exception as e:
            print(f"Erro ao receber kit: {e}")
            return False
# funções principais #

# funções de proteção #
    def equipar_do_inventario(self, regiao, nome_protecao):
        if not hasattr(self, regiao):
            print(f"[ERRO] Região inválida: {regiao}")
            return False
        item_encontrado = next((i for i in self.inventario.itens if i["item"].nome == nome_protecao), None)
        if not item_encontrado:
            print(f"[ERRO] Item '{nome_protecao}' não encontrado no inventário.")
            return False

        protecao_nova = item_encontrado["item"]
        protecao_atual = getattr(self, regiao)

        if protecao_atual:
            self.inventario.gerenciar_item(item_objeto=protecao_atual, quantidade=1, operacao="adicionar")

        setattr(self, regiao, protecao_nova)

        if hasattr(protecao_nova, "Id"):
            self.inventario.remover_item_por_id(protecao_nova.Id)
        else:
            self.inventario.remover_item(item_objeto=protecao_nova, quantidade=1)

        self.calcular_peso_total()
        return True

    def remover_protecao(self, regiao):
        if not hasattr(self, regiao):
            return
        protecao_atual = getattr(self, regiao, None)
        if not protecao_atual:
            return
        self.inventario.gerenciar_item(item_objeto=protecao_atual, quantidade=1, operacao="adicionar")
        setattr(self, regiao, None)
        self.calcular_peso_total()

    def listar_protecoes(self):
        print("Proteções Equipadas:")
        regioes = ["Cabeça", "Rosto", "Torso", "Pernas", "Braços"]
        for regiao in regioes:
            protecao = getattr(self, regiao, None)
            if protecao:
                print(f"{regiao}: {protecao.nome}")
            else:
                print(f"{regiao}: Nenhuma proteção equipada.")

    def receber_kit_avancado(self, kit, modo="basico"):
        """
        Recebe um kit com diferentes modos de aplicação.
        
        Args:
            kit: Objeto Kit que contém os itens
            modo: String que define como aplicar o kit
                - "basico": Apenas adiciona todos os itens ao inventário
                - "equipar_protecoes": Adiciona itens e equipa proteções automaticamente
                - "equipar_tudo": Adiciona itens, equipa proteções e todas as armas
                - "equipar_arma": (mesmo comportamento de equipar_tudo, mantido por compatibilidade)
        
        Returns:
            dict: Relatório das ações realizadas
        """
        relatorio = {
            "sucesso": False,
            "itens_adicionados": [],
            "protecoes_equipadas": {},
            "armas_equipadas": [],
            "erros": []
        }
        
        try:
            itens_kit = kit.listar_itens()
            protecoes, armas_melee, armas_ranged, outros_itens = [], [], [], []

            # === 1. Adicionar todos os itens ao inventário e categorizar === #
            for item_info in itens_kit:
                item_obj = item_info["objeto"]
                quantidade = item_info["quantidade"]

                for _ in range(quantidade):
                    if hasattr(item_obj, "Id"):
                        # Criar cópias seguras se possível
                        if hasattr(item_obj, "to_dict") and hasattr(item_obj.__class__, "from_dict"):
                            item_dict = item_obj.to_dict()
                            nova_instancia = item_obj.__class__.from_dict(item_dict)
                            self.inventario.adicionar_item_objeto(nova_instancia, 1)
                            relatorio["itens_adicionados"].append(nova_instancia.nome)
                            alvo = nova_instancia
                        else:
                            self.inventario.adicionar_item_objeto(item_obj, 1)
                            relatorio["itens_adicionados"].append(item_obj.nome)
                            alvo = item_obj

                        # Categorizar
                        if self._eh_protecao(alvo):
                            protecoes.append(alvo)
                        elif self._eh_arma_melee(alvo):
                            armas_melee.append(alvo)
                        elif self._eh_arma_ranged(alvo):
                            armas_ranged.append(alvo)
                        else:
                            outros_itens.append(alvo)

                    else:
                        # Itens empilháveis (munição, consumíveis etc.)
                        self.inventario.adicionar_item_objeto(item_obj, quantidade)
                        relatorio["itens_adicionados"].append(f"{item_obj.nome} x{quantidade}")
                        outros_itens.append(item_obj)
                        break

            # === 2. Equipar proteções, se aplicável === #
            if modo in ["equipar_protecoes", "equipar_tudo", "equipar_arma"]:
                relatorio["protecoes_equipadas"] = self._equipar_protecoes_automatico(protecoes)

            # === 3. Equipar TODAS as armas === #
            if modo in ["equipar_tudo", "equipar_arma"]:
                todas_armas = armas_melee + armas_ranged
                for arma in todas_armas:
                    if self._equipar_arma(arma):
                        relatorio["armas_equipadas"].append(arma.nome)
                    else:
                        relatorio["erros"].append(f"Falha ao equipar arma: {arma.nome}")

                # === 4. Carregar todas as armas de fogo com munição compatível === #
                try:
                    # filtra todas as munições do inventário
                    municoes_disp = [
                        i["item"] for i in self.inventario.itens
                        if hasattr(i["item"], "calibre") or "Municao" in i["item"].__class__.__name__
                    ]

                    for arma in armas_ranged:
                        if hasattr(arma, "carregar_municao") and hasattr(arma, "calibre"):
                            # encontra munição compatível
                            muni_comp = next(
                                (m for m in municoes_disp if getattr(m, "calibre", None) == arma.calibre),
                                None
                            )
                            if muni_comp:
                                # quantidade total da munição no inventário
                                qtd_disp = next(
                                    (i["quantidade"] for i in self.inventario.itens if i["item"] == muni_comp),
                                    0
                                )
                                if qtd_disp > 0:
                                    qtd_carregada = arma.carregar_municao(muni_comp, qtd_disp)
                                    self.inventario.remover_item(muni_comp, qtd_carregada)
                                    print(f"[{self.nome}] {arma.nome} carregada com {qtd_carregada}x {muni_comp.nome}.")
                                else:
                                    print(f"[{self.nome}] Sem munição suficiente para {arma.nome}.")
                            else:
                                print(f"[{self.nome}] Nenhuma munição compatível para {arma.nome}.")
                except Exception as e:
                    relatorio["erros"].append(f"Erro ao carregar munições: {str(e)}")

            # === 5. Atualizar atributos === #
            self.calcular_peso_total()
            self.recalcularAtributos()

            relatorio["sucesso"] = True
            print(f"{self.nome} recebeu o kit '{kit.nome}' no modo '{modo}' com sucesso!")
        
        except Exception as e:
            relatorio["erros"].append(f"Erro geral: {str(e)}")
            print(f"Erro ao aplicar kit: {e}")

        return relatorio

    def _eh_protecao(self, item):
        """Verifica se um item é uma proteção baseado em seus atributos"""
        return hasattr(item, 'regiao') or hasattr(item, 'defesa') or 'Protecao' in item.__class__.__name__

    def _eh_arma_melee(self, item):
        """Verifica se um item é uma arma corpo a corpo"""
        return (hasattr(item, 'tipo') and 'melee' in item.tipo.lower()) or \
            'Melee' in item.__class__.__name__ or \
            (hasattr(item, 'categoria') and 'melee' in item.categoria.lower())

    def _eh_arma_ranged(self, item):
        """Verifica se um item é uma arma à distância"""
        return (hasattr(item, 'tipo') and 'ranged' in item.tipo.lower()) or \
            'Ranged' in item.__class__.__name__ or \
            (hasattr(item, 'categoria') and 'ranged' in item.categoria.lower())

    def _equipar_protecoes_automatico(self, protecoes):
        """Equipa proteções automaticamente nas regiões apropriadas"""
        protecoes_equipadas = {}
        
        for protecao in protecoes:
            if hasattr(protecao, 'regiao'):
                regiao = protecao.regiao
                
                # Mapear nomes de região para atributos do personagem
                mapeamento_regioes = {
                    'cabeça': 'Cabeça',
                    'cabeca': 'Cabeça',
                    'rosto': 'Rosto',
                    'torso': 'Torso',
                    'peitoral': 'Torso',
                    'peito': 'Torso',
                    'pernas': 'Pernas',
                    'braços': 'Braços',
                    'bracos': 'Braços'
                }
                
                regiao_normalizada = mapeamento_regioes.get(regiao.lower(), regiao)
                
                if hasattr(self, regiao_normalizada):
                    # Remove a proteção do inventário
                    if self.inventario.remover_item(protecao, 1):
                        # Se já há uma proteção equipada, move para o inventário
                        protecao_atual = getattr(self, regiao_normalizada)
                        if protecao_atual:
                            self.inventario.adicionar_item_objeto(protecao_atual, 1)
                        
                        # Equipa a nova proteção
                        setattr(self, regiao_normalizada, protecao)
                        protecoes_equipadas[regiao_normalizada] = protecao.nome
        
        return protecoes_equipadas

    def _equipar_arma(self, arma):
        """Equipa uma arma no inventário equipados"""
        try:
            # Remove a arma do inventário principal
            if self.inventario.remover_item(arma, 1):
                # Adiciona ao inventário de equipados
                return self.equipados.adicionar_item_objeto(arma, 1)
            return False
        except Exception as e:
            print(f"Erro ao equipar arma {arma.nome}: {e}")
            return False

    @classmethod
    def from_dict(cls, data):
        personagem = cls(
            nome=data.get("nome", "SemNome"),
            nivel=data.get("nivel", 1),
            Forca=data.get("Forca", 1),
            Agilidade=data.get("Agilidade", 1),
            Vigor=data.get("Vigor", 1),
            Inteligencia=data.get("Inteligencia", 1),
            Presenca=data.get("Presenca", 1),
            Tatica=data.get("Tatica", 1)
        )

        personagem.XPAtual = data.get("XPAtual", 0)
        personagem.XPlvlUp = data.get("XPlvlUp", 1000 + 500 * personagem.nivel)
        personagem.vidaAtual = data.get("vidaAtual", personagem.vidaMax)
        personagem.vidaMax = data.get("vidaMax", personagem.vidaMax)
        personagem.PeAtual = data.get("PeAtual", personagem.PeMax)
        personagem.PeMax = data.get("PeMax", personagem.PeMax)
        personagem.bloqueio = data.get("bloqueio", 5 + personagem.Forca)
        personagem.esquiva = data.get("esquiva", 5 + personagem.Agilidade)
        personagem.CargaMax = data.get("CargaMax", 15 + 2 * personagem.Forca)
        personagem.cargaAtual = data.get("cargaAtual", 0)
        personagem.mobilidade = data.get("mobilidade", 5 + 2 * personagem.Agilidade)

        # Correção para proteções equipadas - deserializar se necessário
        personagem.Cabeça = deserializar_item(data.get("Cabeça"))
        personagem.Rosto = deserializar_item(data.get("Rosto"))
        personagem.Torso = deserializar_item(data.get("Torso"))
        personagem.Pernas = deserializar_item(data.get("Pernas"))
        personagem.Braços = deserializar_item(data.get("Braços"))

        personagem.inventario = Inventario.from_dict(data.get("inventario", {}))
        personagem.equipados = Inventario.from_dict(data.get("equipados", {}))
        personagem.proficiencias = SistemaDeProficiencias.from_dict(data.get("proficiencias", {}))
        personagem.poderes = GerenciadorDePoderes.from_dict(data.get("poderes", {}))
        personagem.habilidades = GerenciadorDeHabilidades.from_dict(data.get("habilidades", {}))
        personagem.buffs_debuffs = GerenciadorDeBuffsDebuffs.from_dict(data.get("buffs_debuffs", {}))

        return personagem

    def to_dict(self):
        return {
            "nome": self.nome,
            "nivel": self.nivel,
            "XPAtual": self.XPAtual,
            "XPlvlUp": self.XPlvlUp,
            "Forca": self.Forca,
            "Agilidade": self.Agilidade,
            "Vigor": self.Vigor,
            "Inteligencia": self.Inteligencia,
            "Presenca": self.Presenca,
            "Tatica": self.Tatica,
            "vidaMax": self.vidaMax,
            "vidaAtual": self.vidaAtual,
            "PeMax": self.PeMax,
            "PeAtual": self.PeAtual,
            "bloqueio": self.bloqueio,
            "esquiva": self.esquiva,
            "CargaMax": self.CargaMax,
            "cargaAtual": self.cargaAtual,
            "mobilidade": self.mobilidade,
            "Cabeça": serializar_item(self.Cabeça),
            "Rosto": serializar_item(self.Rosto),
            "Torso": serializar_item(self.Torso),
            "Pernas": serializar_item(self.Pernas),
            "Braços": serializar_item(self.Braços),
            "inventario": self.inventario.to_dict(),
            "equipados": self.equipados.to_dict(),
            "proficiencias": self.proficiencias.to_dict(),
            "poderes": self.poderes.to_dict(),
            "habilidades": self.habilidades.to_dict(),
            "buffs_debuffs": self.buffs_debuffs.to_dict()
        }
### CLASSE PERSONAGEM ###
### CLASSE PERSONAGEM ###
### CLASSE PERSONAGEM ###


### CLASSE PODER ###
class Poder:
    def __init__(self, nome, tipo, custo, efeitos, descricao):
        self.nome = nome
        self.tipo = tipo  # "ativo" ou "passivo"
        self.custo = custo  # Custo em PE (0 para passivos)
        self.efeitos = efeitos  # Lista de nomes de buffs/debuffs ou descrição de efeitos
        self.descricao = descricao
    
    def __str__(self):
        tipo_symbol = "⚡" if self.tipo == "ativo" else "🛡️"
        custo_text = f"(Custo: {self.custo} PE)" if self.custo > 0 else "(Passivo)"
        return f"[🔮{tipo_symbol}] {self.nome}: {self.descricao} | Efeitos: {self.efeitos} {custo_text}"
    
    def to_dict(self):
        return {
            "nome": self.nome,
            "tipo": self.tipo,
            "custo": self.custo,
            "efeitos": self.efeitos,
            "descricao": self.descricao
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            nome=data.get("nome", ""),
            tipo=data.get("tipo", "ativo"),
            custo=data.get("custo", 0),
            efeitos=data.get("efeitos", ""),
            descricao=data.get("descricao", "")
        )

class GerenciadorDePoderes:
    def __init__(self):
        self.poderes = []
    
    def adicionar_poder(self, nome, tipo, custo, efeitos, descricao):
        """Adiciona um novo poder à lista"""
        poder = Poder(nome, tipo, custo, efeitos, descricao)
        self.poderes.append(poder)
        return poder
    
    def adicionar_poder_objeto(self, poder):
        """Adiciona um objeto Poder diretamente"""
        self.poderes.append(poder)
        return poder
    
    def remover_poder(self, nome):
        """Remove um poder pelo nome"""
        self.poderes = [p for p in self.poderes if p.nome != nome]
    
    def limpar_poderes(self):
        """Remove todos os poderes"""
        self.poderes.clear()
    
    def obter_poder(self, nome):
        """Retorna um poder específico pelo nome"""
        for poder in self.poderes:
            if poder.nome == nome:
                return poder
        return None
    
    def listar_poderes(self):
        """Retorna todos os poderes"""
        return self.poderes.copy()
    
    def listar_ativos(self):
        """Retorna apenas os poderes ativos"""
        return [p for p in self.poderes if p.tipo == "ativo"]
    
    def listar_passivos(self):
        """Retorna apenas os poderes passivos"""
        return [p for p in self.poderes if p.tipo == "passivo"]
    
    def to_dict(self):
        return {
            "poderes": [poder.to_dict() for poder in self.poderes]
        }
    
    @classmethod
    def from_dict(cls, data):
        gerenciador = cls()
        for poder_data in data.get("poderes", []):
            poder = Poder.from_dict(poder_data)
            gerenciador.poderes.append(poder)
        return gerenciador
### CLASSE PODER ###

### CLASSE HABILIDADE ###
class Habilidade:
    def __init__(self, nome, tipo, custo, efeitos, descricao):
        self.nome = nome
        self.tipo = tipo  # "ativo" ou "passivo"
        self.custo = custo  # Custo em PE (0 para passivos)
        self.efeitos = efeitos  # Lista de nomes de buffs/debuffs ou descrição de efeitos
        self.descricao = descricao
    
    def __str__(self):
        tipo_symbol = "⚡" if self.tipo == "ativo" else "🛡️"
        custo_text = f"(Custo: {self.custo} PE)" if self.custo > 0 else "(Passivo)"
        return f"[⚔️{tipo_symbol}] {self.nome}: {self.descricao} | Efeitos: {self.efeitos} {custo_text}"
    
    def to_dict(self):
        return {
            "nome": self.nome,
            "tipo": self.tipo,
            "custo": self.custo,
            "efeitos": self.efeitos,
            "descricao": self.descricao
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            nome=data.get("nome", ""),
            tipo=data.get("tipo", "ativo"),
            custo=data.get("custo", 0),
            efeitos=data.get("efeitos", ""),
            descricao=data.get("descricao", "")
        )

class GerenciadorDeHabilidades:
    def __init__(self):
        self.habilidades = []
    
    def adicionar_habilidade(self, nome, tipo, custo, efeitos, descricao):
        """Adiciona uma nova habilidade à lista"""
        habilidade = Habilidade(nome, tipo, custo, efeitos, descricao)
        self.habilidades.append(habilidade)
        return habilidade
    
    def adicionar_habilidade_objeto(self, habilidade):
        """Adiciona um objeto Habilidade diretamente"""
        self.habilidades.append(habilidade)
        return habilidade
    
    def remover_habilidade(self, nome):
        """Remove uma habilidade pelo nome"""
        self.habilidades = [h for h in self.habilidades if h.nome != nome]
    
    def limpar_habilidades(self):
        """Remove todas as habilidades"""
        self.habilidades.clear()
    
    def obter_habilidade(self, nome):
        """Retorna uma habilidade específica pelo nome"""
        for habilidade in self.habilidades:
            if habilidade.nome == nome:
                return habilidade
        return None
    
    def listar_habilidades(self):
        """Retorna todas as habilidades"""
        return self.habilidades.copy()
    
    def listar_ativas(self):
        """Retorna apenas as habilidades ativas"""
        return [h for h in self.habilidades if h.tipo == "ativo"]
    
    def listar_passivas(self):
        """Retorna apenas as habilidades passivas"""
        return [h for h in self.habilidades if h.tipo == "passivo"]
    
    def to_dict(self):
        return {
            "habilidades": [habilidade.to_dict() for habilidade in self.habilidades]
        }
    
    @classmethod
    def from_dict(cls, data):
        gerenciador = cls()
        for habilidade_data in data.get("habilidades", []):
            habilidade = Habilidade.from_dict(habilidade_data)
            gerenciador.habilidades.append(habilidade)
        return gerenciador
### CLASSE HABILIDADE ###

### CLASSE BUFF/DEBUFF ###
class BuffDebuff:
    def __init__(self, nome, duracao, efeito, descricao, tipo="buff"):
        self.nome = nome
        self.duracao = duracao  # Número de turnos, "permanente", ou None
        self.efeito = efeito  # Descrição do efeito mecânico
        self.descricao = descricao  # Descrição narrativa
        self.tipo = tipo  # "buff" ou "debuff"
        self.turnos_restantes = None if duracao == "permanente" else duracao
    
    def eh_permanente(self):
        """Verifica se o efeito é permanente"""
        return self.duracao == "permanente"
    
    def decrementar_turno(self):
        """Reduz a duração em 1 turno. Retorna True se o efeito ainda está ativo"""
        if self.eh_permanente():
            return True
        
        if self.turnos_restantes is not None and self.turnos_restantes > 0:
            self.turnos_restantes -= 1
            return self.turnos_restantes > 0
        return False
    
    def resetar_duracao(self):
        """Reseta a duração para o valor original"""
        if not self.eh_permanente():
            self.turnos_restantes = self.duracao
    
    def __str__(self):
        tipo_symbol = "✨" if self.tipo == "buff" else "💀"
        if self.eh_permanente():
            duracao_text = "Permanente"
        else:
            duracao_text = f"{self.turnos_restantes}/{self.duracao} turnos"
        
        return f"[{tipo_symbol}] {self.nome}: {self.descricao} | Efeito: {self.efeito} | Duração: {duracao_text}"
    
    def to_dict(self):
        return {
            "nome": self.nome,
            "duracao": self.duracao,
            "efeito": self.efeito,
            "descricao": self.descricao,
            "tipo": self.tipo,
            "turnos_restantes": self.turnos_restantes
        }
    
    @classmethod
    def from_dict(cls, data):
        buff = cls(
            nome=data.get("nome", ""),
            duracao=data.get("duracao", 1),
            efeito=data.get("efeito", ""),
            descricao=data.get("descricao", ""),
            tipo=data.get("tipo", "buff")
        )
        buff.turnos_restantes = data.get("turnos_restantes", buff.turnos_restantes)
        return buff

class GerenciadorDeBuffsDebuffs:
    def __init__(self):
        self.efeitos = []
    
    def adicionar_efeito(self, nome, duracao, efeito, descricao, tipo="buff"):
        """Adiciona um novo buff/debuff à lista"""
        buff_debuff = BuffDebuff(nome, duracao, efeito, descricao, tipo)
        self.efeitos.append(buff_debuff)
        return buff_debuff
    
    def adicionar_efeito_objeto(self, buff_debuff):
        """Adiciona um objeto BuffDebuff diretamente"""
        self.efeitos.append(buff_debuff)
        return buff_debuff
    
    def remover_efeito(self, nome):
        """Remove um efeito pelo nome"""
        self.efeitos = [e for e in self.efeitos if e.nome != nome]
    
    def limpar_efeitos(self):
        """Remove todos os efeitos"""
        self.efeitos.clear()
    
    def limpar_temporarios(self):
        """Remove apenas os efeitos temporários (mantém permanentes)"""
        self.efeitos = [e for e in self.efeitos if e.eh_permanente()]
    
    def obter_efeito(self, nome):
        """Retorna um efeito específico pelo nome"""
        for efeito in self.efeitos:
            if efeito.nome == nome:
                return efeito
        return None
    
    def listar_efeitos(self):
        """Retorna todos os efeitos"""
        return self.efeitos.copy()
    
    def listar_buffs(self):
        """Retorna apenas os buffs"""
        return [e for e in self.efeitos if e.tipo == "buff"]
    
    def listar_debuffs(self):
        """Retorna apenas os debuffs"""
        return [e for e in self.efeitos if e.tipo == "debuff"]
    
    def listar_permanentes(self):
        """Retorna apenas os efeitos permanentes"""
        return [e for e in self.efeitos if e.eh_permanente()]
    
    def listar_temporarios(self):
        """Retorna apenas os efeitos temporários"""
        return [e for e in self.efeitos if not e.eh_permanente()]
    
    def processar_turnos(self):
        """Decrementa todos os efeitos temporários e remove os que expiraram"""
        efeitos_expirados = []
        
        for efeito in self.efeitos[:]:  # Cria cópia para iterar
            if not efeito.eh_permanente():
                if not efeito.decrementar_turno():
                    efeitos_expirados.append(efeito.nome)
                    self.efeitos.remove(efeito)
        
        return efeitos_expirados
    
    def to_dict(self):
        return {
            "efeitos": [efeito.to_dict() for efeito in self.efeitos]
        }
    
    @classmethod
    def from_dict(cls, data):
        gerenciador = cls()
        for efeito_data in data.get("efeitos", []):
            efeito = BuffDebuff.from_dict(efeito_data)
            gerenciador.efeitos.append(efeito)
        return gerenciador
### CLASSE BUFF/DEBUFF ###

class Inventario:
    def __init__(self):
        self.itens = []

    def gerenciar_item(self, nome_item=None, item_objeto=None, quantidade=1, dicionarios=None, operacao="adicionar"):
        item = item_objeto or (dicionarios.get(nome_item)() if nome_item and dicionarios and nome_item in dicionarios else None)
        if not item:
            return False

        if hasattr(item, "Id"):
            if operacao == "adicionar":
                for _ in range(quantidade):
                    self.itens.append({"item": item, "quantidade": 1})
                return True
            elif operacao == "remover":
                removidos = 0
                for i in list(self.itens):  # cópia segura para remoção
                    if hasattr(i["item"], "Id") and i["item"].Id == item.Id:
                        self.itens.remove(i)
                        removidos += 1
                        if removidos == quantidade:
                            break
                return removidos == quantidade

        for i in self.itens:
            if i['item'].nome == item.nome and not hasattr(i['item'], "Id"):
                if operacao == "adicionar":
                    i['quantidade'] += quantidade
                    return True
                elif operacao == "remover":
                    if i['quantidade'] >= quantidade:
                        i['quantidade'] -= quantidade
                        if i['quantidade'] == 0:
                            self.itens.remove(i)
                        return True
                    return False

        if operacao == "adicionar":
            self.itens.append({"item": item, "quantidade": quantidade})
            return True

        return False

    def adicionar_item(self, nome_item, quantidade, dicionarios):
        return self.gerenciar_item(nome_item=nome_item, quantidade=quantidade, dicionarios=dicionarios, operacao="adicionar")
    
    def adicionar_item_objeto(self, item_objeto, quantidade=1):
        return self.gerenciar_item(item_objeto=item_objeto, quantidade=quantidade, operacao="adicionar")
    
    def remover_item(self, item_objeto, quantidade=1):
        return self.gerenciar_item(item_objeto=item_objeto, quantidade=quantidade, operacao="remover")
    
    def remover_item_por_id(self, item_id):
        item = self.obter_item_por_id(item_id)
        if item:
            return self.gerenciar_item(item_objeto=item["item"], quantidade=1, operacao="remover")
        return False

    def transferir_item(self, nome_item, quantidade, inventario_destinatario):
        item_data = next((i["item"] for i in self.itens if i["item"].nome == nome_item), None)
        if item_data and self.gerenciar_item(item_objeto=item_data, quantidade=quantidade, operacao="remover"):
            return inventario_destinatario.gerenciar_item(item_objeto=item_data, quantidade=quantidade, operacao="adicionar")
        return False

    def obter_item_por_id(self, id_item):
        return next((i for i in self.itens if hasattr(i['item'], "Id") and i['item'].Id == id_item), None)

    def listar_itens(self):
        resultado = []
        for i in self.itens:
            item = i["item"]
            if not hasattr(item, "nome"):
                info = {
                    "nome": str(item),
                    "quantidade": i.get("quantidade", 1),
                    "id": None,
                    "stats": None,
                    "objeto": item
                }
                resultado.append(info)
                continue
            item_id = getattr(item, "Id", None)
            info = {
                "nome": item.nome,
                "quantidade": i.get("quantidade", 1),
                "id": item_id,
                "stats": item.stats() if hasattr(item, "stats") else None,
                "objeto": item
            }
            resultado.append(info)
        return resultado

    def to_dict(self):
        lista_serializada = []
        for entrada in self.itens:
            item = entrada["item"]
            qtd = entrada["quantidade"]
            # Se o item tem um método to_dict(), usa ele; senão, salva nome + tipo
            if hasattr(item, "to_dict"):
                item_dict = item.to_dict()
                item_dict["_classe"] = item.__class__.__name__
                lista_serializada.append({"item": item_dict, "quantidade": qtd})
            elif hasattr(item, "Id"):  # fallback: serializa por Id
                lista_serializada.append({
                    "item": {"Id": item.Id, "nome": item.nome, "_classe": item.__class__.__name__},
                    "quantidade": qtd
                })
            else:
                lista_serializada.append({
                    "item": {"nome": item.nome, "_classe": item.__class__.__name__},
                    "quantidade": qtd
                })
        return lista_serializada

    @classmethod
    def from_dict(cls, data):
        inventario = cls()
        
        # Função para criar item baseado na classe e dados
        def criar_item_por_classe(classe_nome, item_data):
            try:
                # Tenta obter a classe do escopo global
                if classe_nome in globals():
                    item_class = globals()[classe_nome]
                    if hasattr(item_class, 'from_dict'):
                        return item_class.from_dict(item_data)
                    else:
                        # Se não tem from_dict, cria instância básica
                        return item_class()
                else:
                    # Se a classe não foi encontrada, retorna um objeto simples com os dados
                    class ItemGenerico:
                        def __init__(self, data):
                            for key, value in data.items():
                                if key != '_classe':
                                    setattr(self, key, value)
                            self.nome = data.get('nome', f'Item_{classe_nome}')
                    
                    return ItemGenerico(item_data)
            except Exception as e:
                print(f"[Inventario] Erro ao criar item {classe_nome}: {e}")
                # Fallback: cria objeto simples
                class ItemFallback:
                    def __init__(self, nome):
                        self.nome = nome
                return ItemFallback(item_data.get('nome', 'Item Desconhecido'))
        
        # Verifica se data é uma lista ou dicionário
        if isinstance(data, list):
            # Se data for uma lista, trata como lista de itens diretamente
            itens_data = data
        elif isinstance(data, dict):
            # Se data for um dicionário, busca a chave "itens"
            itens_data = data.get("itens", [])
        else:
            # Se não for nem lista nem dicionário, cria lista vazia
            print(f"[Inventario] Formato de dados inválido: {type(data)}")
            itens_data = []
        
        # Processa os itens
        if isinstance(itens_data, list):
            for entrada in itens_data:
                if isinstance(entrada, dict) and "item" in entrada:
                    item_data = entrada["item"]
                    classe_nome = item_data.get("_classe", "Item")
                    
                    # Cria o item usando a função auxiliar
                    item = criar_item_por_classe(classe_nome, item_data)
                    inventario.itens.append({
                        "item": item,
                        "quantidade": entrada.get("quantidade", 1)
                    })
                else:
                    print(f"[Inventario] Entrada inválida no inventário: {repr(entrada)}")
        else:
            print(f"[Inventario] 'itens' não é uma lista: {type(itens_data)}")
        
        return inventario

### CLASSE PROFICIENCIA ###
class Proficiencia:
    def __init__(self, nome, atributo, nivel=0):
        self.nome: str = nome
        self.atributo: str = atributo
        self.nivel: int = nivel
        
    def adicionar_pontos(self, pontos):
        self.nivel += pontos
        if self.nivel >= 10:
            self.nivel = 10

    def remover_pontos(self, pontos):
        self.nivel -= pontos
        if self.nivel <= -10:
            self.nivel = -10

    def __str__(self):
        return f"{self.nome}: {self.nivel} ponto(s)"
    
    def to_dict(self):
        return {
            "nome": self.nome,
            "atributo": self.atributo,
            "nivel": self.nivel,
        }

    @classmethod
    def from_dict(cls, data):
        prof = cls(data["nome"], data["atributo"])
        prof.nivel = data.get("nivel", 0)
        return prof

class SistemaDeProficiencias:
    def __init__(self):
        self.proficiencias = {}

    def adicionar_proficiencia(self, nome, atributo ,pontos):
        if nome not in self.proficiencias:
            self.proficiencias[nome] = Proficiencia(nome, atributo)
        self.proficiencias[nome].adicionar_pontos(pontos)

    def remover_proficiencia(self, nome, pontos):
        if nome in self.proficiencias:
            self.proficiencias[nome].remover_pontos(pontos)
            if self.proficiencias[nome].nivel == 0:
                del self.proficiencias[nome]  # Remove se a proficiência atingir 0

    def listar_proficiencias(self):
        if not self.proficiencias:
            print("Nenhuma proficiência encontrada.")
            return
        for prof in self.proficiencias.values():
            print(prof)
    
    def obter_bonus(self, nome, atributo=None):
        prof = self.proficiencias.get(nome)
        if prof:
            return prof.nivel
        return 0

    def obter_proficiencias(self, *nomes):
        """Retorna os níveis de várias proficiências."""
        return {nome: self.obter_bonus(nome) for nome in nomes}
    
    def items(self):
        return self.proficiencias.items()

    def to_dict(self):
        return {
            nome: prof.to_dict()
            for nome, prof in self.proficiencias.items()
            if hasattr(prof, "to_dict")
        }

    @classmethod
    def from_dict(cls, data):
        sistema = cls()

        # Se os dados vierem no formato {'proficiencias': {...}}, extrair
        if isinstance(data, dict) and "proficiencias" in data:
            data = data["proficiencias"]

        for nome, dados in data.items():
            # CORREÇÃO: Verificar se dados já é um objeto Proficiencia
            if isinstance(dados, Proficiencia):
                # Se já é um objeto Proficiencia, usar diretamente
                sistema.proficiencias[nome] = dados
            elif isinstance(dados, dict):
                # Se é um dicionário, deserializar
                prof = Proficiencia.from_dict(dados)
                sistema.proficiencias[nome] = prof
            else:
                # Fallback: tentar criar uma proficiência básica
                print(f"Aviso: Dados inesperados para proficiência '{nome}': {type(dados)}")
                # Assumir que é um valor numérico (nível)
                prof = Proficiencia(nome, "Desconhecido", int(dados) if isinstance(dados, (int, float)) else 0)
                sistema.proficiencias[nome] = prof

        return sistema
### CLASSE PROFICIENCIA ###

class Item:
    def __init__(self, nome, peso=None):
        self.nome: str = nome
        if peso is not None:
            self.peso: float = peso

    def stats(self):
        stats_dict = {"Nome": self.nome}
        if hasattr(self, 'peso'):
            stats_dict["Peso"] = f"{self.peso} kg"
        return stats_dict

    def to_dict(self):
        data = {"nome": self.nome}
        if hasattr(self, 'peso'):
            data["peso"] = self.peso
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            nome=data["nome"],
            peso=data.get("peso")
        )


class Consumivel(Item):
    def __init__(self, nome, peso, cura, energia):
        super().__init__(nome, peso)
        self.cura: int = cura
        self.energia: int = energia

    def stats(self):
        return {
            "Nome": self.nome,
            "Peso": f"{self.peso} kg",
            "Cura": self.cura,
            "Energia": self.energia
        }

    def to_dict(self):
        return {
            "nome": self.nome,
            "peso": self.peso,
            "cura": self.cura,
            "energia": self.energia
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            nome=data["nome"],
            peso=data["peso"],
            cura=data["cura"],
            energia=data["energia"]
        )


class Explosivo(Item):
    def __init__(self, nome, peso, raio, dano, tipo_dano):
        super().__init__(nome, peso)
        self.raio: int = raio
        self.dano: int = dano
        self.tipo_dano: int = tipo_dano

    def stats(self):
        return {
            "Nome": self.nome,
            "Peso": f"{self.peso} kg",
            "Raio": self.raio,
            "Dano": self.dano,
            "Tipo de Dano": self.tipo_dano
        }

    def to_dict(self):
        return {
            "nome": self.nome,
            "peso": self.peso,
            "raio": self.raio,
            "dano": self.dano,
            "tipo_dano": self.tipo_dano
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            nome=data["nome"],
            peso=data["peso"],
            raio=data["raio"],
            dano=data["dano"],
            tipo_dano=data["tipo_dano"]
        )


class Municao(Item):
    def __init__(self, nome, calibre, perfuracao, dano):
        super().__init__(nome)
        self.calibre = calibre
        self.perfuracao = perfuracao
        self.dano = dano

    def stats(self):
        return {
            "Nome": self.nome,
            "Calibre": self.calibre,
            "Perfuração": self.perfuracao,
            "Dano": self.dano,
        }

    def to_dict(self):
        return {
            "nome": self.nome,
            "calibre": self.calibre,
            "perfuracao": self.perfuracao,
            "dano": self.dano
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            nome=data["nome"],
            calibre=data["calibre"],
            perfuracao=data["perfuracao"],
            dano=data["dano"]
        )


class Melhoria(Item):
    def __init__(self, nome, peso, tipo, modificadores):
        super().__init__(nome, peso)
        self.tipo = tipo
        self.modificadores = modificadores

    def aplicar(self, item):
        melhorias_destino = None
        for nome_lista in ["Acessorios", "Melhorias", "melhorias_equipadas"]:
            if hasattr(item, nome_lista):
                melhorias_destino = getattr(item, nome_lista)
                break

        if melhorias_destino is None:
            return False
        if self in melhorias_destino:
            return False

        if (self.tipo == "ranged" and isinstance(item, Ranged)) or \
        (self.tipo == "melee" and isinstance(item, Melee)) or \
        (self.tipo == "protecao" and isinstance(item, Protecao)):

            for atributo, valor in self.modificadores.items():
                if hasattr(item, atributo):
                    setattr(item, atributo, getattr(item, atributo) + valor)

            melhorias_destino.append(self)
            return True
        else:
            return False

    def remover(self, item):
        melhorias_destino = None
        for nome_lista in ["Acessorios", "Melhorias", "melhorias_equipadas"]:
            if hasattr(item, nome_lista):
                melhorias_destino = getattr(item, nome_lista)
                break
        if melhorias_destino is None:
            return False
        if self in melhorias_destino:
            for atributo, valor in self.modificadores.items():
                if hasattr(item, atributo):
                    setattr(item, atributo, getattr(item, atributo) - valor)

            melhorias_destino.remove(self)
            return True
        else:
            return False

    @classmethod
    def from_dict(cls, data):
        return cls(
            nome=data["nome"],
            peso=data["peso"],
            tipo=data["tipo"],
            modificadores=data["modificadores"]
        )
    
    def to_dict(self):
        return {
            "nome": self.nome,
            "peso": self.peso,
            "tipo": self.tipo,
            "modificadores": self.modificadores
        }


class Melee(Item):
    def __init__(self, nome, peso, classe, tipo_dano, raridade):
        super().__init__(nome, peso)
        
        self.classe = classe
        self.tipo_dano = tipo_dano
        self.raridade = raridade
        self.Melhorias = []
        self.Id = gerar_id()

        self.dano_simples = 1
        self.critico_simples = 2
        self.valor_critico_simples = 20

        self.dano_forte = 1
        self.critico_forte = 2
        self.valor_critico_forte = 20

        self.dano_investida = 1
        self.critico_investida = 2
        self.valor_critico_investida = 20

        self.dano_arremesso = 1
        self.critico_arremesso = 2
        self.valor_critico_arremesso = 20

        # Subclasse e Raridade #
        if self.classe == "Faca":
            self.dano_simples = 35
            self.critico_simples = 3
            self.valor_critico_simples = 25

            self.dano_forte = 20
            self.critico_forte = 2
            self.valor_critico_forte = 20

            self.dano_investida = 20
            self.critico_investida = 2
            self.valor_critico_investida = 20

            self.dano_arremesso = 35
            self.critico_arremesso = 3
            self.valor_critico_arremesso = 25
        elif self.classe == "Adaga":
            self.dano_simples = 30
            self.critico_simples = 2
            self.valor_critico_simples = 19

            self.dano_forte = 30
            self.critico_forte = 2
            self.valor_critico_forte = 19

            self.dano_investida = 30
            self.critico_investida = 2
            self.valor_critico_investida = 20

            self.dano_arremesso = 30
            self.critico_arremesso = 2
            self.valor_critico_arremesso = 19
        elif self.classe == "Espada curta":
            self.dano_simples = 25
            self.critico_simples = 2
            self.valor_critico_simples = 20

            self.dano_forte = 35
            self.critico_forte = 2
            self.valor_critico_forte = 19

            self.dano_investida = 30
            self.critico_investida = 2
            self.valor_critico_investida = 20

            self.dano_arremesso = 20
            self.critico_arremesso = 2
            self.valor_critico_arremesso = 20
        elif self.classe == "Espada longa":
            self.dano_simples = 20
            self.critico_simples = 2
            self.valor_critico_simples = 20

            self.dano_forte = 40
            self.critico_forte = 2
            self.valor_critico_forte = 19

            self.dano_investida = 40
            self.critico_investida = 2
            self.valor_critico_investida = 19

            self.dano_arremesso = 20
            self.critico_arremesso = 2
            self.valor_critico_arremesso = 20
        elif self.classe == "Sabre":
            self.dano_simples = 20
            self.critico_simples = 3
            self.valor_critico_simples = 25

            self.dano_forte = 40
            self.critico_forte = 2
            self.valor_critico_forte = 20

            self.dano_investida = 20
            self.critico_investida = 2
            self.valor_critico_investida = 20

            self.dano_arremesso = 20
            self.critico_arremesso = 2
            self.valor_critico_arremesso = 20
        elif self.classe == "Machadinha":
            self.dano_simples = 35
            self.critico_simples = 2
            self.valor_critico_simples = 25

            self.dano_forte = 20
            self.critico_forte = 2
            self.valor_critico_forte = 20

            self.dano_investida = 15
            self.critico_investida = 2
            self.valor_critico_investida = 20

            self.dano_arremesso = 40
            self.critico_arremesso = 2
            self.valor_critico_arremesso = 25
        elif self.classe == "Machado":
            self.dano_simples = 20
            self.critico_simples = 2
            self.valor_critico_simples = 20

            self.dano_forte = 40
            self.critico_forte = 3
            self.valor_critico_forte = 25

            self.dano_investida = 15
            self.critico_investida = 2
            self.valor_critico_investida = 20

            self.dano_arremesso = 15
            self.critico_arremesso = 2
            self.valor_critico_arremesso = 20
        elif self.classe == "Lança":
            self.dano_simples = 20
            self.critico_simples = 2
            self.valor_critico_simples = 20

            self.dano_forte = 20
            self.critico_forte = 2
            self.valor_critico_forte = 20

            self.dano_investida = 40
            self.critico_investida = 2
            self.valor_critico_investida = 18

            self.dano_arremesso = 40
            self.critico_arremesso = 2
            self.valor_critico_arremesso = 18
        elif self.classe == "Martelo":
            self.dano_simples = 30
            self.critico_simples = 3
            self.valor_critico_simples = 19

            self.dano_forte = 30
            self.critico_forte = 3
            self.valor_critico_forte = 19

            self.dano_investida = 15
            self.critico_investida = 2
            self.valor_critico_investida = 20

            self.dano_arremesso = 15
            self.critico_arremesso = 2
            self.valor_critico_arremesso = 20
        elif self.classe == "Porrete":
            self.dano_simples = 25
            self.critico_simples = 2
            self.valor_critico_simples = 19

            self.dano_forte = 35
            self.critico_forte = 2
            self.valor_critico_forte = 19

            self.dano_investida = 15
            self.critico_investida = 2
            self.valor_critico_investida = 20

            self.dano_arremesso = 15
            self.critico_arremesso = 2
            self.valor_critico_arremesso = 20
        elif self.classe == "Taco":
            self.dano_simples = 35
            self.critico_simples = 3
            self.valor_critico_simples = 25

            self.dano_forte = 35
            self.critico_forte = 3
            self.valor_critico_forte = 25

            self.dano_investida = 15
            self.critico_investida = 2
            self.valor_critico_investida = 25

            self.dano_arremesso = 15
            self.critico_arremesso = 2
            self.valor_critico_arremesso = 20
        elif self.classe == "Maça":
            self.dano_simples = 25
            self.critico_simples = 2
            self.valor_critico_simples = 25

            self.dano_forte = 35
            self.critico_forte = 3
            self.valor_critico_forte = 25

            self.dano_investida = 15
            self.critico_investida = 2
            self.valor_critico_investida = 20

            self.dano_arremesso = 15
            self.critico_arremesso = 2
            self.valor_critico_arremesso = 20
        elif self.classe == "Marreta":
            self.dano_simples = 20
            self.critico_simples = 2
            self.valor_critico_simples = 20

            self.dano_forte = 45
            self.critico_forte = 3
            self.valor_critico_forte = 20

            self.dano_investida = 15
            self.critico_investida = 2
            self.valor_critico_investida = 20

            self.dano_arremesso = 15
            self.critico_arremesso = 2
            self.valor_critico_arremesso = 20
        else:
            print(f"Erro: Subclasse '{self.subclasse}' não reconhecida.")
    
        if raridade == "Comum":
            self.dano_simples += 0
            self.dano_forte += 0
            self.dano_investida += 0
            self.dano_arremesso += 0
        elif raridade == "Incomum":
            self.dano_simples += 5
            self.dano_forte += 5
            self.dano_investida += 5
            self.dano_arremesso += 5
        elif raridade == "Rara":
            self.dano_simples += 10
            self.dano_forte += 10
            self.dano_investida += 10
            self.dano_arremesso += 10
        elif raridade == "Épica":
            self.dano_simples += 15
            self.dano_forte += 15
            self.dano_investida += 15
            self.dano_arremesso += 15
        elif raridade == "Exótica":
            self.dano_simples += 20
            self.dano_forte += 20
            self.dano_investida += 20
            self.dano_arremesso += 20
        elif raridade == "Lendária":
            self.dano_simples += 25
            self.dano_forte += 25
            self.dano_investida += 25
            self.dano_arremesso += 25
        else:
            print(f"Erro: Raridade '{raridade}' não reconhecida.")
        # Subclasse e Raridade #

    # Atributos base #
        self.base_dano_simples = self.dano_simples
        self.base_critico_simples = self.critico_simples
        self.base_valor_critico_simples = self.valor_critico_simples

        self.base_dano_forte = self.dano_forte
        self.base_critico_forte = self.critico_forte
        self.base_valor_critico_forte = self.valor_critico_forte

        self.base_dano_investida = self.dano_investida
        self.base_critico_investida = self.critico_investida
        self.base_valor_critico_investida = self.valor_critico_investida

        self.base_dano_arremesso = self.dano_arremesso
        self.base_critico_arremesso = self.critico_arremesso
        self.base_valor_critico_arremesso = self.valor_critico_arremesso

    def recalcular_atributos(self):
        self.dano_simples = self.base_dano_simples
        self.critico_simples = self.base_critico_simples
        self.valor_critico_simples = self.base_valor_critico_simples

        self.dano_forte = self.base_dano_forte
        self.critico_forte = self.base_critico_forte
        self.valor_critico_forte = self.base_valor_critico_forte

        self.dano_investida = self.base_dano_investida
        self.critico_investida = self.base_critico_investida
        self.valor_critico_investida = self.base_valor_critico_investida

        self.dano_arremesso = self.base_dano_arremesso
        self.critico_arremesso = self.base_critico_arremesso
        self.valor_critico_arremesso = self.base_valor_critico_arremesso
        for melhoria in self.Melhorias:
            self.dano_simples += melhoria.modificadores.get("dano_simples", 0)
            self.critico_simples += melhoria.modificadores.get("critico_simples", 0)
            self.valor_critico_simples += melhoria.modificadores.get("valor_critico_simples", 0)

            self.dano_forte += melhoria.modificadores.get("dano_forte", 0)
            self.critico_forte += melhoria.modificadores.get("critico_forte", 0)
            self.valor_critico_forte += melhoria.modificadores.get("valor_critico_forte", 0)

            self.dano_investida += melhoria.modificadores.get("dano_investida", 0)
            self.critico_investida += melhoria.modificadores.get("critico_investida", 0)
            self.valor_critico_investida += melhoria.modificadores.get("valor_critico_investida", 0)

            self.dano_arremesso += melhoria.modificadores.get("dano_arremesso", 0)
            self.critico_arremesso += melhoria.modificadores.get("critico_arremesso", 0)
            self.valor_critico_arremesso += melhoria.modificadores.get("valor_critico_arremesso", 0)
            self.peso += melhoria.modificadores.get("Peso", 0)

    def stats(self):
        return {
            "Nome": self.nome,
            "Peso": self.peso,
            "Classe": self.classe,
            "Tipo de dano": self.tipo_dano,
            "Dano Simples": self.dano_simples,
            "Crítico Simples": self.critico_simples,
            "Valor Crítico Simples": self.valor_critico_simples,
            "Dano Forte": self.dano_forte,
            "Crítico Forte": self.critico_forte,
            "Valor Crítico Forte": self.valor_critico_forte,
            "Dano Investida": self.dano_investida,
            "Crítico Investida": self.critico_investida,
            "Valor Crítico Investida": self.valor_critico_investida,
            "Dano Arremesso": self.dano_arremesso,
            "Crítico Arremesso": self.critico_arremesso,
            "Valor Crítico Arremesso": self.valor_critico_arremesso,
        }
    
    def adicionar_melhoria(self, melhoria):
        if melhoria in self.Melhorias:
            return
        self.Melhorias.append(melhoria)
        self.recalcular_atributos()

    def remover_melhoria(self, melhoria):
        if melhoria in self.Melhorias:
            self.Melhorias.remove(melhoria)
            self.recalcular_atributos()
            return

    @classmethod
    def from_dict(cls, data):
        instance = cls(
            nome=data["nome"],
            peso=data["peso"],
            classe=data["classe"],
            tipo_dano=data["tipo_dano"],
            raridade=data["raridade"]
        )
        
        # Restaura atributos específicos
        for attr in ["dano_simples", "critico_simples", "valor_critico_simples",
                    "dano_forte", "critico_forte", "valor_critico_forte",
                    "dano_investida", "critico_investida", "valor_critico_investida",
                    "dano_arremesso", "critico_arremesso", "valor_critico_arremesso",
                    "Id"]:
            if attr in data:
                setattr(instance, attr, data[attr])
        
        # Deserializar melhorias
        if "Melhorias" in data:
            instance.Melhorias = []
            for melhoria_data in data["Melhorias"]:
                if isinstance(melhoria_data, dict):
                    melhoria = deserializar_item(melhoria_data)
                    if melhoria:
                        instance.Melhorias.append(melhoria)
                else:
                    instance.Melhorias.append(melhoria_data)  # Se já é objeto
        
        return instance

    def to_dict(self):
        return {
            "nome": self.nome,
            "peso": self.peso,
            "classe": self.classe,
            "tipo_dano": self.tipo_dano,
            "raridade": self.raridade,
            "dano_simples": self.dano_simples,
            "critico_simples": self.critico_simples,
            "valor_critico_simples": self.valor_critico_simples,
            "dano_forte": self.dano_forte,
            "critico_forte": self.critico_forte,
            "valor_critico_forte": self.valor_critico_forte,
            "dano_investida": self.dano_investida,
            "critico_investida": self.critico_investida,
            "valor_critico_investida": self.valor_critico_investida,
            "dano_arremesso": self.dano_arremesso,
            "critico_arremesso": self.critico_arremesso,
            "valor_critico_arremesso": self.valor_critico_arremesso,
            "Id": self.Id,
            "Melhorias": [serializar_item(melhoria) for melhoria in self.Melhorias]
        }


class Ranged(Item):
    def __init__(self, nome, peso, classe, acao, raridade, calibre, capacidade):
        super().__init__(nome, peso)
        self.classe = classe
        self.acao = acao
        self.raridade = raridade
        self.calibre = calibre
        self.recuo = 0
        self.capacidade = capacidade
        self.capacidadeBase = capacidade
        self.pesoBase = peso
        self.calibre = calibre
        self.munições = 0
        self.municao = None
        self.Id = gerar_id()
        self.Acessorios = []

        self.dano = 0
        self.recuo = 0
        self.MaxRange = 0
        self.MinRange = 0
        self.ShortCrit = 0
        self.MediumCrit = 0
        self.LongCrit = 0
        
        if classe == "Pistola":
            self.dano = 25
            self.recuo = 2
            self.MaxRange = 40
            self.MinRange = 5
            self.ShortCrit = 18
            self.MediumCrit = 25
            self.LongCrit = 30
        elif classe == "Revolver":
            self.dano = 35
            self.recuo = 3
            self.MaxRange = 50
            self.MinRange = 5
            self.ShortCrit = 20
            self.MediumCrit = 22
            self.LongCrit = 28
        elif classe == "Submetralhadora":
            self.dano = 25
            self.recuo = 2
            self.MaxRange = 45
            self.MinRange = 5
            self.ShortCrit = 18
            self.MediumCrit = 25
            self.LongCrit = 29
        elif classe == "Escopeta":
            self.dano = 50
            self.recuo = 3
            self.MaxRange = 45
            self.MinRange = 5
            self.ShortCrit = 20
            self.MediumCrit = 30
            self.LongCrit = 40
        elif classe == "Espingarda":
            self.dano = 35
            self.recuo = 3
            self.MaxRange = 60
            self.MinRange = 5
            self.ShortCrit = 22
            self.MediumCrit = 28
            self.LongCrit = 34
        elif classe == "Carabina":
            self.dano = 20
            self.recuo = 3
            self.MaxRange = 60
            self.MinRange = 5
            self.ShortCrit = 20
            self.MediumCrit = 24
            self.LongCrit = 30
        elif classe == "Fuzil De Assalto":
            self.dano = 20
            self.recuo = 3
            self.MaxRange = 80
            self.MinRange = 5
            self.ShortCrit = 22
            self.MediumCrit = 24
            self.LongCrit = 28
        elif classe == "Fuzil De Batalha":
            self.dano = 25
            self.recuo = 4
            self.MaxRange = 100
            self.MinRange = 5
            self.ShortCrit = 22
            self.MediumCrit = 21
            self.LongCrit = 22
        elif classe == "DMR":
            self.dano = 25
            self.recuo = 3
            self.MaxRange = 130
            self.MinRange = 5
            self.ShortCrit = 28
            self.MediumCrit = 24
            self.LongCrit = 19
        elif classe == "Fuzil De Precisão":
            self.dano = 50
            self.recuo = 3
            self.MaxRange = 150
            self.MinRange = 8
            self.ShortCrit = 32
            self.MediumCrit = 22
            self.LongCrit = 18
        elif classe == "Metralhadora leve":
            self.dano = 20
            self.recuo = 3
            self.MaxRange = 80
            self.MinRange = 8
            self.ShortCrit = 25
            self.MediumCrit = 22
            self.LongCrit = 25
        elif classe == "Metralhadora média":
            self.dano = 20
            self.recuo = 4
            self.MaxRange = 100
            self.MinRange = 10
            self.ShortCrit = 25
            self.MediumCrit = 25
            self.LongCrit = 25
        elif classe == "Metralhadora pesada":
            self.dano = 20
            self.recuo = 3
            self.MaxRange = 150
            self.MinRange = 5
            self.ShortCrit = 30
            self.MediumCrit = 30
            self.LongCrit = 30
        elif classe == "Fuzil Antimaterial":
            self.dano = 50
            self.recuo = 5
            self.MaxRange = 250
            self.MinRange = 10
            self.ShortCrit = 35
            self.MediumCrit = 25
            self.LongCrit = 20
        else:
            print(f"Erro: Classe '{classe}' não reconhecida.")
        
        if acao == "Simples":
            self.recuo -= 1
            self.dano += 10
            self.MinRange += 1
            self.MaxRange += 5
        elif acao == "Semi":
            self.recuo += 1
            self.dano += 0
            self.MinRange += 0
            self.MaxRange += 0
        elif acao == "Dupla":
            self.recuo += 0
            self.dano += 5
            self.MinRange += 0
            self.MaxRange += 0
        elif acao == "Rajada":
            self.recuo += 1
            self.dano += 2
            self.MinRange += 0
            self.MaxRange += 0
        elif acao == "Auto":
            self.recuo += 2
            self.dano -= 5
            self.MinRange += 0
            self.MaxRange -= 5
        elif acao == "Pump":
            self.recuo -= 1
            self.dano += 5
            self.MinRange += 0
            self.MaxRange += 0
        elif acao == "Alavanca":
            self.recuo -= 1
            self.dano += 5
            self.MinRange += 1
            self.MaxRange += 5
        elif acao == "Bolt":
            self.recuo -= 1
            self.dano += 5
            self.MinRange += 2
            self.MaxRange += 10
        else:
            print(f"Erro: Ação '{acao}' não reconhecida.")
        
        if raridade == "Comum":
            pass
        elif raridade == "Incomum":
            self.dano += 2
            self.MaxRange += 5
        elif raridade == "Rara":
            self.dano += 5
            self.MaxRange += 15
        elif raridade == "Épica":
            self.dano += 8
            self.MaxRange += 20
        elif raridade == "Exótica":
            self.dano += 11
            self.MaxRange += 25
        elif raridade == "Lendária":
            self.dano += 15
            self.MaxRange += 30
        else:
            print(f"Erro: Raridade '{raridade}' não reconhecida.")

        self.danoBase = self.dano
        self.recuoBase = self.recuo
        self.MaxRangeBase = self.MaxRange
        self.MinRangeBase = self.MinRange
        self.ShortCritBase = self.ShortCrit
        self.MediumCritBase = self.MediumCrit
        self.LongCritBase = self.LongCrit

    def carregar_municao(self, municao: "Municao", quantidade: int):
        if self.municao is None or self.munições == 0:
            self.municao = municao
            self.Perfuracao = municao.perfuracao
            if self.munições == 0:
                self.munições = 0

        if self.municao.nome != municao.nome:
            self.municao = municao
            self.Perfuracao = municao.perfuracao
            self.munições = 0

        espaco_restante = self.capacidade - self.munições
        quantidade_a_carregar = min(quantidade, espaco_restante)
        self.munições += quantidade_a_carregar
        self.recalcular_atributos()
        return quantidade_a_carregar
        
    def descarregar_municao(self, quantidade=None):
        if self.munições == 0:
            self.Perfuracao = 0
            return []

        municoes_removidas = []
        if quantidade is None or quantidade >= self.munições:
            municoes_removidas = [self.municao for _ in range(self.munições)]
            self.munições = 0
            self.municao = None
            self.Perfuracao = 0
        else:
            municoes_removidas = [self.municao for _ in range(quantidade)]
            self.munições -= quantidade
        self.recalcular_atributos()
        return municoes_removidas
        
    def disparar(self, quantidade):
        if self.munições == 0 or self.municao is None:
            return
        if quantidade > self.munições:
            quantidade = self.munições
        
        self.munições -= quantidade
        
        if self.munições == 0:
            self.municao = None
            self.Perfuracao = 0
        
        self.recalcular_atributos()
        
    def adicionar_acessorio(self, Acessorio):
        self.Acessorios.append(Acessorio)
        self.recalcular_atributos()
        
    def remover_acessorio(self, acessorio):
        if acessorio in self.Acessorios:
            self.Acessorios.remove(acessorio)
            self.recalcular_atributos()
        else:
            pass

    def recalcular_atributos(self):
        self.dano = self.danoBase
        self.recuo = self.recuoBase
        self.MaxRange = self.MaxRangeBase
        self.MinRange = self.MinRangeBase
        self.ShortCrit = self.ShortCritBase
        self.MediumCrit = self.MediumCritBase
        self.LongCrit = self.LongCritBase
        self.capacidade = self.capacidadeBase
        self.peso = self.pesoBase

        if hasattr(self, "municao") and self.municao:
            self.dano += self.municao.dano

        for acessorio in self.Acessorios:
            self.dano += acessorio.modificadores.get("dano", 0)
            self.recuo += acessorio.modificadores.get("recuo", 0)
            self.MaxRange += acessorio.modificadores.get("MaxRange", 0)
            self.MinRange += acessorio.modificadores.get("MinRange", 0)
            self.ShortCrit += acessorio.modificadores.get("ShortCrit", 0)
            self.MediumCrit += acessorio.modificadores.get("MediumCrit", 0)
            self.LongCrit += acessorio.modificadores.get("LongCrit", 0)
            self.capacidade += acessorio.modificadores.get("capacidade", 0)
            self.peso += acessorio.peso
    
    def stats(self):
        return {
            "Nome": self.nome,
            "Peso": self.peso,
            "Classe": self.classe,
            "Calibre": self.calibre,
            "Ação": self.acao,
            "Raridade": self.raridade,
            "Dano": self.dano,
            "Recuo": self.recuo,
            "Alcance Mínimo": self.MinRange,
            "Alcance Máximo": self.MaxRange,
            "Crítico Curto": self.ShortCrit,
            "Crítico Médio": self.MediumCrit,
            "Crítico Longo": self.LongCrit,
            "Capacidade Total": self.capacidade,
            "munições": self.munições,
            "Munição": {
                "Tipo": self.municao.nome if self.municao else "Descarregada",
                "Dano": self.municao.dano if self.municao else 0,
                "Perfuração": self.Perfuracao if self.municao else 0,
            },
            "Acessórios": [
                acessorio.stats() for acessorio in self.Acessorios
            ] if self.Acessorios else "Nenhum acessório equipado."
        }

    @classmethod
    def from_dict(cls, data):
        instance = cls(
            nome=data["nome"],
            peso=data["peso"],
            classe=data["classe"],
            acao=data["acao"],
            raridade=data["raridade"],
            calibre=data["calibre"],
            capacidade=data["capacidade"]
        )
        
        # Restaura atributos específicos
        for attr in ["dano", "recuo", "MaxRange", "MinRange", "ShortCrit", "MediumCrit", "LongCrit",
                    "munições", "Id", "Perfuracao"]:
            if attr in data:
                setattr(instance, attr, data[attr])
        
        # Deserializar munição
        if "municao" in data and data["municao"]:
            if isinstance(data["municao"], dict):
                instance.municao = deserializar_item(data["municao"])
            else:
                instance.municao = data["municao"]
        
        # Deserializar acessórios
        if "Acessorios" in data:
            instance.Acessorios = []
            for acessorio_data in data["Acessorios"]:
                if isinstance(acessorio_data, dict):
                    acessorio = deserializar_item(acessorio_data)
                    if acessorio:
                        instance.Acessorios.append(acessorio)
                else:
                    instance.Acessorios.append(acessorio_data)  # Se já é objeto
        
        return instance

    def to_dict(self):
        return {
            "nome": self.nome,
            "peso": self.peso,
            "classe": self.classe,
            "acao": self.acao,
            "raridade": self.raridade,
            "calibre": self.calibre,
            "capacidade": self.capacidade,
            "dano": self.dano,
            "recuo": self.recuo,
            "MaxRange": self.MaxRange,
            "MinRange": self.MinRange,
            "ShortCrit": self.ShortCrit,
            "MediumCrit": self.MediumCrit,
            "LongCrit": self.LongCrit,
            "munições": self.munições,
            "municao": serializar_item(self.municao),
            "Id": self.Id,
            "Acessorios": [serializar_item(acessorio) for acessorio in self.Acessorios],
            "Perfuracao": getattr(self, 'Perfuracao', 0)
        }


class Protecao(Item):
    def __init__(self, nome, peso, nivelBalistico, absorcaoFisica, absorcaoBalistica, regiao):
        super().__init__(nome, peso)
        self.nivelBalisticoBase: int = nivelBalistico
        self.nivelBalistico: int = nivelBalistico
        self.absorcaoFisicaBase: int = absorcaoFisica
        self.absorcaoFisica: int = absorcaoFisica
        self.absorcaoBalisticaBase: int = absorcaoBalistica
        self.absorcaoBalistica: int = absorcaoBalistica
        self.regiao = regiao
        self.Melhorias: list[Melhoria] = []
        self.Id = gerar_id()

    def adicionar_melhoria(self, melhoria):
        if melhoria in self.Melhorias:
            return
        self.Melhorias.append(melhoria)
        self.recalcular_atributos()

    def remover_melhoria(self, melhoria):
        if melhoria in self.Melhorias:
            self.Melhorias.remove(melhoria)
            self.recalcular_atributos()
            return

    def recalcular_atributos(self):
        self.nivelBalistico = self.nivelBalisticoBase
        self.absorcaoFisica = self.absorcaoFisicaBase
        self.absorcaoBalistica = self.absorcaoBalisticaBase
        for melhoria in self.Melhorias:
            self.nivelBalistico += melhoria.modificadores.get("nivelBalistico", 0)
            self.absorcaoFisica += melhoria.modificadores.get("absorcaoFisica", 0)
            self.absorcaoBalistica += melhoria.modificadores.get("absorcaoBalistica", 0)

    def stats(self):
        return {
            "Nome": self.nome,
            "Peso": self.peso,
            "Nível Balístico": self.nivelBalistico,
            "Absorção Física": self.absorcaoFisica,
            "Absorção Balística": self.absorcaoBalistica,
            "Região": self.regiao,
        }

    @classmethod
    def from_dict(cls, data):
        instance = cls(
            nome=data["nome"],
            peso=data["peso"],
            nivelBalistico=data["nivelBalistico"],
            absorcaoFisica=data["absorcaoFisica"],
            absorcaoBalistica=data["absorcaoBalistica"],
            regiao=data["regiao"]
        )
        
        if "Id" in data:
            instance.Id = data["Id"]
        
        # Deserializar melhorias
        if "Melhorias" in data:
            instance.Melhorias = []
            for melhoria_data in data["Melhorias"]:
                if isinstance(melhoria_data, dict):
                    melhoria = deserializar_item(melhoria_data)
                    if melhoria:
                        instance.Melhorias.append(melhoria)
                else:
                    instance.Melhorias.append(melhoria_data)  # Se já é objeto
        
        return instance

    def to_dict(self):
        return {
            "nome": self.nome,
            "peso": self.peso,
            "nivelBalistico": self.nivelBalistico,
            "absorcaoFisica": self.absorcaoFisica,
            "absorcaoBalistica": self.absorcaoBalistica,
            "regiao": self.regiao,
            "Id": self.Id,
            "Melhorias": [serializar_item(melhoria) for melhoria in self.Melhorias]
        }


class Kits:
    def __init__(self, nome, raridade):
        self.nome = nome
        self.Id = gerar_id()
        self.raridade = raridade
        self.inventario = Inventario()

    def adicionar_item(self, item_objeto, quantidade=1):
        """Adiciona um item ao kit usando o sistema de inventário"""
        return self.inventario.adicionar_item_objeto(item_objeto, quantidade)

    def adicionar_item_por_nome(self, nome_item, quantidade, dicionarios):
        """Adiciona um item ao kit usando nome e dicionários de classes"""
        return self.inventario.adicionar_item(nome_item, quantidade, dicionarios)

    def remover_item(self, item_objeto, quantidade=1):
        """Remove um item do kit"""
        return self.inventario.remover_item(item_objeto, quantidade)

    def remover_item_por_id(self, item_id):
        """Remove um item específico do kit pelo ID"""
        return self.inventario.remover_item_por_id(item_id)

    def obter_item_por_id(self, item_id):
        """Obtém um item específico pelo ID"""
        return self.inventario.obter_item_por_id(item_id)

    def listar_itens(self):
        """Lista todos os itens do kit"""
        return self.inventario.listar_itens()

    def transferir_item_para_inventario(self, nome_item, quantidade, inventario_destinatario):
        """Transfere um item do kit para outro inventário"""
        return self.inventario.transferir_item(nome_item, quantidade, inventario_destinatario)

    def aplicar_kit_em_inventario(self, inventario_destinatario):
        """Aplica todo o conteúdo do kit em um inventário de destino"""
        itens_kit = self.listar_itens()
        sucesso_total = True
        
        for item_info in itens_kit:
            item_obj = item_info["objeto"]
            quantidade = item_info["quantidade"]
            
            # Se o item tem ID único, cria uma nova instância para cada unidade
            if hasattr(item_obj, "Id"):
                for _ in range(quantidade):
                    # Para itens únicos, adiciona cada um separadamente
                    if not inventario_destinatario.adicionar_item_objeto(item_obj, 1):
                        sucesso_total = False
            else:
                # Para itens stackáveis, adiciona a quantidade total
                if not inventario_destinatario.adicionar_item_objeto(item_obj, quantidade):
                    sucesso_total = False
        
        return sucesso_total

    def duplicar_kit(self):
        """Cria uma cópia do kit (útil para kits que podem ser usados múltiplas vezes)"""
        novo_kit = Kits(self.nome, self.raridade)
        
        # Copia todos os itens do kit original
        for item_info in self.listar_itens():
            item_obj = item_info["objeto"]
            quantidade = item_info["quantidade"]
            
            # Se o item tem método to_dict, usa ele para criar uma cópia
            if hasattr(item_obj, "to_dict") and hasattr(item_obj.__class__, "from_dict"):
                item_dict = item_obj.to_dict()
                item_class = item_obj.__class__
                nova_instancia = item_class.from_dict(item_dict)
                novo_kit.adicionar_item(nova_instancia, quantidade)
            else:
                # Para itens simples, adiciona o mesmo objeto
                novo_kit.adicionar_item(item_obj, quantidade)
        
        return novo_kit

    def stats(self):
        """Retorna as estatísticas do kit"""
        itens_info = self.listar_itens()
        total_itens = sum(item["quantidade"] for item in itens_info)
        
        return {
            "Nome": self.nome,
            "ID": self.Id,
            "Raridade": self.raridade,
            "Total de Itens": total_itens,
            "Tipos de Itens": len(itens_info),
            "Conteúdo": itens_info
        }

    def to_dict(self):
        """Serializa o kit para dicionário"""
        return {
            "nome": self.nome,
            "Id": self.Id,
            "raridade": self.raridade,
            "inventario": self.inventario.to_dict()
        }

    @classmethod
    def from_dict(cls, data):
        kit = cls(data["nome"], data["raridade"])
        kit.Id = data["Id"]

        inv_data = data.get("inventario", [])
        kit.inventario = Inventario.from_dict(inv_data)

        return kit

    def __str__(self):
        return f"Kit: {self.nome} (Raridade: {self.raridade}) - {len(self.listar_itens())} tipos de itens"

    def __repr__(self):
        return f"Kits(nome='{self.nome}', raridade='{self.raridade}', Id='{self.Id}')"


class NPC:
    def __init__(self, grupo, classe, forca, agilidade, vigor, inteligencia, presenca, tatica):
        self.grupo = grupo
        self.classe = classe
        self.forca = forca
        self.agilidade = agilidade
        self.vigor = vigor
        self.inteligencia = inteligencia
        self.presenca = presenca
        self.tatica = tatica

    def __repr__(self):
        return {"Grupo": self.grupo,
                "Classe": self.classe,
                "Força": self.forca,
                "Agilidade": self.agilidade,
                "Vigor": self.vigor,
                "Inteligência": self.inteligencia,
                "Presença": self.presenca,
                "Tática": self.tatica,
                }

### Funções de Geração ###
def Gerador(npc: NPC, nivel=None, nome=None, proficiencias_base=None):
    if nivel is None:
        nivel = 1
    f = npc.forca
    a = npc.agilidade
    v = npc.vigor
    i = npc.inteligencia
    p = npc.presenca
    t = npc.tatica

    nome_base = nome or f"{npc.classe} ({npc.grupo})"

    # Criar o personagem
    inimigo = Personagem.CriarPersonagem(
        nome=nome_base, 
        nivel=nivel, 
        Forca=f, 
        Agilidade=a, 
        Vigor=v, 
        Inteligencia=i, 
        Presenca=p, 
        Tatica=t, 
        proficiencias_base=proficiencias_base
    )
    
    return inimigo

def Gerador_grupo(self, grupo_destino, configuracoes):
    for config in configuracoes:
        npc_base = config['npc_base']
        nivel = config['nivel']
        nome = config['nome']
        personagem = Gerador(npc=npc_base, nivel=nivel, nome=nome)
        self.GruposDePersonagens[grupo_destino].append(personagem)
    self.refresh()
### Funções de Geração ###

### Funções de Acerto ###
def acerto_melee(atacante: Personagem, alvo: Personagem, rolagem: int, id_arma, regiao: str, tipo_ataque: str, BuffDano: int=0, DebuffDano: int=0, BuffAcerto: int=0, DebuffAcerto: int=0):
    resultado = ""
    Acerto = rolagem
    DebuffDano += alvo.proficiencias.obter_bonus("Fortitude")

    arma_data = None
    if hasattr(atacante, 'equipados') and hasattr(atacante.equipados, 'itens'):
        for item in atacante.equipados.itens:
            item_obj = item["item"] if isinstance(item, dict) else item
            if hasattr(item_obj, 'Id') and item_obj.Id == id_arma:
                arma_data = {"item": item_obj}
                break

    if not arma_data:
        resultado += "Arma não encontrada no inventário"
        return resultado
    arma_obj = arma_data["item"]

    Classe = arma_obj.classe
    if tipo_ataque == "simples":
        DanoBase = arma_obj.dano_simples
        BuffAcerto += atacante.proficiencias.obter_bonus("Luta")
        Crit = arma_obj.critico_simples
        ValorPraCritar = arma_obj.base_valor_critico_simples
    elif tipo_ataque == "forte":
        DanoBase = arma_obj.dano_forte
        BuffAcerto += atacante.proficiencias.obter_bonus("Luta")
        Crit = arma_obj.critico_forte
        ValorPraCritar = arma_obj.base_valor_critico_forte
    elif tipo_ataque == "investida":
        DanoBase = arma_obj.dano_investida
        BuffAcerto += atacante.proficiencias.obter_bonus("Atletismo")
        Crit = arma_obj.critico_investida
        ValorPraCritar = arma_obj.base_valor_critico_investida
    else:
        DanoBase = arma_obj.dano_arremesso
        BuffAcerto += atacante.proficiencias.obter_bonus("Arremesso")
        Crit = arma_obj.critico_arremesso
        ValorPraCritar = arma_obj.base_valor_critico_arremesso
    
    mapa_regioes = {'Aleatoria': 'Aleatoria', 'Cabeça': 'Cabeça', 'Rosto': 'Rosto', 'Torso': 'Torso', 'Pernas': 'Pernas', 'Braços': 'Braços'}
    if mapa_regioes[regiao] == 'Aleatoria':
        Chance = random.randint(0,100)
        if Chance in range(0,10):
            regiao = 'Cabeça'
        elif Chance in range(11,20):
            regiao = 'Rosto'
        elif Chance in range(21,50):
            regiao = 'Torso'
        elif Chance in range(46,85):
            regiao = 'Pernas'
        else:
            regiao = 'Braços'
    
    if mapa_regioes[regiao] == 'Cabeça':
        Dano = int(DanoBase * 1.3)
    elif mapa_regioes[regiao] == 'Rosto':
        Dano = int(DanoBase * 1.6)
    elif mapa_regioes[regiao] == 'Braços':
        Dano = int(DanoBase * 0.8)
    elif mapa_regioes[regiao] == 'Pernas':
        Dano = int(DanoBase * 0.8)
    else:
        Dano = max(1,DanoBase)

    Protecao = getattr(alvo, mapa_regioes[regiao], None)
    Absorcao = Protecao.absorcaoFisica if Protecao else 0

    Acerto += BuffAcerto - DebuffAcerto

    if ValorPraCritar > 20:
        if Acerto >= alvo.bloqueio and Acerto >= alvo.esquiva:
            if rolagem >= ValorPraCritar:
                DanoFinal = max(1,((Dano * Crit) - Absorcao - DebuffDano + BuffDano))
                alvo.TomarDano(DanoFinal)
                resultado += f"({regiao}) -> Dano crítico:{(Dano * Crit)} - absorção: {Absorcao} - Debuffs: {DebuffDano}.\n"
                resultado += f"Dano total:{DanoFinal}.\n"
            else:
                DanoFinal = max(1,(Dano - Absorcao - DebuffDano + BuffDano))
                alvo.TomarDano(DanoFinal)
                resultado += f"({regiao}) -> Dano:{(Dano)} - absorção: {Absorcao} - Debuffs: {DebuffDano}.\n"
                resultado += f"Dano total:{DanoFinal}.\n"
    elif ValorPraCritar <= 20:
        if rolagem >= alvo.bloqueio and Acerto >= alvo.esquiva:
            if Acerto >= ValorPraCritar:
                DanoFinal = max(1,((Dano * Crit) - Absorcao - DebuffDano + BuffDano))
                alvo.TomarDano(DanoFinal)
                resultado += f"({regiao}) -> Dano crítico:{(Dano * Crit)} - absorção: {Absorcao} - Debuffs: {DebuffDano}.\n"
                resultado += f"Dano total:{DanoFinal}.\n"
            else:
                DanoFinal = max(1,((Dano) - Absorcao - DebuffDano + BuffDano))
                alvo.TomarDano(DanoFinal)
                resultado += f"({regiao}) -> Dano:{(Dano)} - absorção: {Absorcao} - Debuffs: {DebuffDano}.\n"
                resultado += f"Dano total:{DanoFinal}.\n"
        else:
            resultado += f"{atacante.nome} errou o ataque {tipo_ataque}.\n"
    return resultado


def acerto_ranged(atacante: Personagem, alvo: Personagem, Rolagem: int, id_arma, distancia: int, disparos: int, regiao: str, BuffAcerto: int=0, BuffDano: int=0, DebuffAcerto: int=0, DebuffDano: int=0, cobertura: str = "Nenhuma", material: str = "Madeira"):
    import random
    resultado = ""
    Acerto = Rolagem

    # Obtém dados da arma
    arma_data = atacante.equipados.obter_item_por_id(id_arma)
    arma_obj = arma_data["item"]

    if not arma_obj.municao:
        resultado += "Click... (sem munição)"
        return resultado

    Perfuracao = arma_obj.municao.perfuracao
    DanoBase = arma_obj.dano
    Recuo = arma_obj.recuo

    # Mapeamento de regiões
    mapa_regioes = {'Aleatorio': 'Aleatorio', 'Aleatório': 'Aleatorio', 'Aleatoria': 'Aleatorio',
                    'Cabeça': 'Cabeça', 'Rosto': 'Rosto', 'Torso': 'Torso', 'Pernas': 'Pernas', 'Braços': 'Braços', 'Bracos': 'Braços'}
    regioes_validas = ['Cabeça', 'Rosto', 'Torso', 'Pernas', 'Braços']

    # Probabilidades para seleção aleatória de regiões
    # Torso: 57%, Pernas: 20%, Braços: 16%, Rosto: 3%, Cabeça: 4%
    def escolher_regiao_aleatoria():
        rand = random.randint(1, 100)
        if rand <= 4:
            return 'Cabeça'
        elif rand <= 7:
            return 'Rosto'
        elif rand <= 64:
            return 'Torso'
        elif rand <= 84:
            return 'Pernas'
        else:
            return 'Braços'

    # Inicializa dificuldade base
    Dificuldade = 0

    # Cálculos de distância e críticos
    if distancia <= 50:
        ValorPraCrit = arma_obj.ShortCrit
    elif 51 <= distancia <= 101:
        ValorPraCrit = arma_obj.MediumCrit
    else:
        ValorPraCrit = arma_obj.LongCrit

    BonusConta = ValorPraCrit > 20

    # Modificadores de distância
    if distancia < arma_obj.MinRange:
        DebuffAcerto += (arma_obj.MinRange - distancia)
    elif distancia > arma_obj.MaxRange:
        debuff_dano_dist = 5 * int((distancia - arma_obj.MaxRange) // 2)
        debuff_acerto_dist = (distancia - arma_obj.MaxRange) // 5
        DebuffDano += debuff_dano_dist
        DebuffAcerto += debuff_acerto_dist

    # Probabilidade inicial
    BuffAcerto += atacante.proficiencias.obter_bonus("Pontaria")
    Probabilidade_inicial = Rolagem * 5

    # Mapas de cobertura e materiais
    cobertura_para_regioes = {
        "Nenhuma": ['Cabeça', 'Rosto', 'Torso', 'Pernas', 'Braços'],
        "Baixa": ['Torso', 'Pernas', 'Braços'],
        "Alta": ['Pernas', 'Braços'],
        "Total": []
    }
    material_limite = {
        "Nenhum": 0,
        "Gesso": 4,
        "Madeira": 8,
        "Veiculo": 10,
        "Concreto": 12,
        "Aço": 16
    }

    # normaliza strings recebidas
    regiao_param = mapa_regioes.get(regiao, regiao)
    cobertura = cobertura if cobertura in cobertura_para_regioes else "Nenhuma"
    material = material if material in material_limite else material.capitalize()
    limiar = material_limite.get(material, 999)

    # Loop de disparos (respeita munição)
    muni_atual = arma_obj.munições if hasattr(arma_obj, "munições") else getattr(arma_obj, "municoes", 0)
    for disparo in range(min(disparos, muni_atual)):
        if getattr(arma_obj, "munições", 0) == 0:
            resultado += f"Disparo {disparo + 1}: Click... (Sem munição)\n"
            break

        # Escolhe região para este disparo
        if regiao_param == 'Aleatorio':
            regiao_atual = escolher_regiao_aleatoria()
        else:
            regiao_atual = regiao_param if regiao_param in regioes_validas else 'Torso'

        # Calcula dano base e dificuldade por região
        if regiao_atual == 'Cabeça':
            DificuldadeAtual = 15
            DanoAtual = int(DanoBase * 2)
        elif regiao_atual == 'Rosto':
            DificuldadeAtual = 20
            DanoAtual = int(DanoBase * 2)
        elif regiao_atual == 'Braços':
            DificuldadeAtual = 5
            DanoAtual = int(DanoBase * 0.8)
        elif regiao_atual == 'Pernas':
            DificuldadeAtual = 4
            DanoAtual = int(DanoBase * 0.9)
        else:
            DificuldadeAtual = 0
            DanoAtual = DanoBase

        # Proteção do alvo na região
        protecao = getattr(alvo, regiao_atual, None)
        Nivel = protecao.nivelBalistico if protecao else 0
        absorcao = protecao.absorcaoBalistica if protecao else 0

        # Ajuste de absorção segundo perfuração
        if Perfuracao > Nivel:
            if Perfuracao > (Nivel + 1):
                absorcao = absorcao // 3
            else: absorcao = absorcao // 2
        elif Perfuracao < Nivel:
            if Perfuracao < (Nivel - 1):
                absorcao = absorcao * 3
            else: absorcao = absorcao * 2

        # Recalcula probabilidade com dificuldade atual
        Probabilidade_atual = max(4, (Probabilidade_inicial - (DificuldadeAtual * 2) + (BuffAcerto * 2) - (DebuffAcerto * 2)))

        Critico = False
        if BonusConta:
            if Acerto + BuffAcerto >= ValorPraCrit:
                Critico = True
        else:
            if Acerto >= ValorPraCrit:
                Critico = True

        # ---- Lógica de cobertura ----
        regioes_expostas = cobertura_para_regioes.get(cobertura, cobertura_para_regioes["Nenhuma"])
        disparo_bloqueado = False
        multiplicador_cobertura = 1.0
        info_cobertura = "Sem cobertura"

        if regiao_atual not in regioes_expostas:
            # região está por trás da cobertura
            if cobertura in ["Baixa", "Alta", "Total"]:
                # cobertura existe, agora testamos a perfuração contra o limiar do material
                if Perfuracao > limiar:
                    info_cobertura = f"Varou"
                    multiplicador_cobertura = 1.0
                elif Perfuracao == limiar:
                    info_cobertura = f"Penetrou"
                    multiplicador_cobertura = 0.5
                else:
                    disparo_bloqueado = True
                    info_cobertura = f"Bloqueado"
            else:
                # caso raro: tipo de cobertura não definido
                disparo_bloqueado = False
                multiplicador_cobertura = 1.0
                info_cobertura = "????"

        # Rolagem de acerto
        Chance = random.randint(1, 100)
        if Chance <= Probabilidade_atual and not disparo_bloqueado:
            # calcular dano final (aplicando crítico, absorção e multiplicador da cobertura)
            if Critico:
                bruto = DanoAtual + 20
            else:
                bruto = DanoAtual

            antes_absorv = max(1, bruto - absorcao)
            com_multiplicador = int(max(0, antes_absorv * multiplicador_cobertura))
            DanoFinal = max(1, com_multiplicador + BuffDano - DebuffDano)
            # garante ao menos 1 ponto quando não bloqueado e dano positivo após buffs
            if DanoFinal <= 0:
                DanoFinal = 0

            if Critico:
                resultado += f"({regiao_atual}): Dano crítico: {bruto} - Absorção: {absorcao}, {info_cobertura} | dano final: {DanoFinal}.)\n"
            else:
                resultado += f"({regiao_atual}): Dano: {bruto} - Absorção: {absorcao}, {info_cobertura} | dano final: {DanoFinal}.)\n"

            if DanoFinal > 0:
                alvo.TomarDano(DanoFinal)
        else:
            # errou ou disparo foi bloqueado
            if disparo_bloqueado:
                resultado += f"({regiao_atual}): {info_cobertura}.\n"
            else:
                resultado += f"({regiao_atual}): Errou.)\n"

        recuo_aplicado = random.randint(1, Recuo)
        Probabilidade_inicial -= (recuo_aplicado * 4)
        Acerto -= recuo_aplicado
        if hasattr(arma_obj, "munições"):
            arma_obj.munições -= 1
        elif hasattr(arma_obj, "municoes"):
            arma_obj.municoes -= 1

        #print(f"Probabilidade: {Probabilidade_atual} | Chance: {Chance} | Recuo aplicado: {recuo_aplicado} | Acerto atual: {Acerto} | Dificuldade: {DificuldadeAtual}")

    return resultado


def acerto_explosivos():
    pass


def acerto_poderes():
    pass
### Funções de Acerto ###