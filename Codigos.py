#Versão 2

from uuid import uuid4
def gerar_id():
    return str(uuid4())[:5]

### CLASSE PERSONAGEM ###
### CLASSE PERSONAGEM ###
### CLASSE PERSONAGEM ###
class Personagem:
    def __init__(self, nome, nivel, Forca, Agilidade, Vigor, Inteligencia, Presenca, Tatica, proficiencias_base=None):
        self.nome: str = nome
        self.nivel: int = nivel
        self.XPlvlUp: int = 1000 + (500 * nivel)
        self.XPAtual: int = 0
        #atributos#
        self.Forca: int = Forca
        self.Agilidade: int = Agilidade
        self.Vigor: int = Vigor
        self.Inteligencia: int = Inteligencia
        self.Presenca: int = Presenca
        self.Tatica: int = Tatica
        #stats#
        self.vidaMax: int = 50 + (10 * Vigor) + (5 * nivel)
        self.vidaAtual: int = self.vidaMax
        self.PeMax: int = 5 + Presenca + (nivel // 2)
        self.PeAtual: int = self.PeMax
        self.bloqueio: int = 5 + Forca
        self.esquiva: int = 5 + Agilidade
        self.CargaMax: float = 10 + (Forca * 2)
        self.cargaAtual: float = 0
        self.mobilidade: int = 5 + (Agilidade * 2)
        #Corpo#
        self.Cabeça = None
        self.Rosto = None
        self.Torso = None
        self.Pernas = None
        self.Braços = None
        #Inventário#
        self.inventario = Inventario()
        #proficiências#
        self.proficiencias = SistemaDeProficiencias()
        if proficiencias_base:
            for nome, criador in proficiencias_base.items():
                self.proficiencias.proficiencias[nome] = criador()
        self.recalcularAtributos()
        

    def CriarPersonagem(nome, nivel, Forca, Agilidade, Vigor, Inteligencia, Presenca, Tatica, proficiencias_base=None):
        return Personagem(nome, nivel, Forca, Agilidade, Vigor, Inteligencia, Presenca, Tatica, proficiencias_base)

# funções principais #
    def calcular_peso_total(self):
        peso_total = 0
        for item_data in self.inventario.itens:
            item = item_data['item']
            peso_total += item.peso * item_data['quantidade']    
        protecoes = [self.Cabeça, self.Torso, self.Pernas, self.Braços]
        for protecao in protecoes:
            if protecao is not None:
                peso_total += (protecao.peso // 2) # Proteção equipada tem peso reduzido

        # Atualiza o peso atual no personagem
        self.cargaAtual = peso_total

    def TomarDano(self, dano):
        self.vidaAtual = max(0, self.vidaAtual - dano)
    
    def TomarCura(self, cura):
        self.vidaAtual += cura
        if self.vidaAtual > self.vidaMax:
            self.vidaAtual = self.vidaMax

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
        self.XPlvlUp = 200 + (50 * self.nivel)
        self.vidaMax = 30 + (5 * self.Vigor) + (5 * self.nivel)
        self.vidaAtual = self.vidaMax
        self.PeMax = 3 + 1 * self.Presenca
        self.mobilidade = (self.Agilidade * 2) + (self.Vigor)
        self.PeAtual = self.PeMax
        self.bloqueio = 4 + self.Forca
        self.esquiva = 4 + self.Agilidade
        self.mobilidade = (self.Agilidade * 4)
        self.calcular_peso_total()
# funções principais #

# funções de proteção #
    def equipar_do_inventario(self, regiao, nome_protecao):
        if not hasattr(self, regiao):
            return
        item_encontrado = next((i for i in self.inventario.itens if i["item"].nome == nome_protecao), None)
        if not item_encontrado:
            return
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
# funções de proteção #
### CLASSE PERSONAGEM ###
### CLASSE PERSONAGEM ###
### CLASSE PERSONAGEM ###

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
            if not hasattr(item, "nome") or not hasattr(item, "peso"):
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

class Proficiencia:
    def __init__(self, nome, nivel=0):
        self.nome: str = nome
        self.nivel: int = nivel

    def adicionar_pontos(self, pontos):
        self.nivel += pontos

    def remover_pontos(self, pontos):
        self.nivel -= pontos

    def __str__(self):
        return f"{self.nome}: {self.nivel} ponto(s)"

class SistemaDeProficiencias:
    def __init__(self):
        self.proficiencias = {}

    def adicionar_proficiencia(self, nome, pontos):
        if nome not in self.proficiencias:
            self.proficiencias[nome] = Proficiencia(nome)
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
    
    def obter_bonus(self, nome):
        return self.proficiencias.get(nome, Proficiencia(nome)).nivel

    def obter_proficiencias(self, *nomes):
        """Retorna os níveis de várias proficiências."""
        return {nome: self.obter_bonus(nome) for nome in nomes}
    
    def items(self):
        return self.proficiencias.items()

# Classe Base para Itens
class Item:
    def __init__(self, nome, peso):
        self.nome: str = nome
        self.peso: float = peso

    def stats(self):
        return {
            "Nome": self.nome,
            "Peso": f"{self.peso} kg",
        }
 
  
class Municao(Item):
    def __init__(self, nome, peso, calibre, perfuracao, dano):
        super().__init__(nome, peso)
        self.calibre: str = calibre
        self.perfuracao: int = perfuracao
        self.dano: int = dano

    def stats(self):
        return {
            "Nome": self.nome,
            "Peso": f"{self.peso} kg",
            "Calibre": self.calibre,
            "Perfuração": self.perfuracao,
            "Dano": self.dano,
        }


class Melee(Item):
    def __init__(self, nome, peso, classe, subclasse, raridade):
        super().__init__(nome, peso)
        
        self.classe = classe
        self.subclasse = subclasse
        self.raridade = raridade
        self.Melhorias = []
        self.Id = gerar_id()

        self.dano_simples = 0
        self.critico_simples = 0
        self.valor_critico_simples = 0

        self.dano_forte = 0
        self.critico_forte = 0
        self.valor_critico_forte = 0

        self.dano_investida = 0
        self.critico_investida = 0
        self.valor_critico_investida = 0

        self.dano_arremesso = 0
        self.critico_arremesso = 0
        self.valor_critico_arremesso = 0

        # Subclasse e Raridade #
        if self.subclasse == "Faca":
            self.dano_simples = 12
            self.critico_simples = 2
            self.valor_critico_simples = 19

            self.dano_forte = 8
            self.critico_forte = 4
            self.valor_critico_forte = 30

            self.dano_investida = 8
            self.critico_investida = 32
            self.valor_critico_investida = 30

            self.dano_arremesso = 10
            self.critico_arremesso = 3
            self.valor_critico_arremesso = 19
        elif self.subclasse == "Adaga":
            self.dano_simples = 10
            self.critico_simples = 2
            self.valor_critico_simples = 20

            self.dano_forte = 10
            self.critico_forte = 3
            self.valor_critico_forte = 25

            self.dano_investida = 10
            self.critico_investida = 3
            self.valor_critico_investida = 25

            self.dano_arremesso = 10
            self.critico_arremesso = 2
            self.valor_critico_arremesso = 20
        elif self.subclasse == "Espada curta":
            self.dano_simples = 8
            self.critico_simples = 3
            self.valor_critico_simples = 22

            self.dano_forte = 12
            self.critico_forte = 2
            self.valor_critico_forte = 20

            self.dano_investida = 12
            self.critico_investida = 2
            self.valor_critico_investida = 22

            self.dano_arremesso = 8
            self.critico_arremesso = 3
            self.valor_critico_arremesso = 25
        elif self.subclasse == "Espada longa":
            self.dano_simples = 8
            self.critico_simples = 2
            self.valor_critico_simples = 25

            self.dano_forte = 15
            self.critico_forte = 2
            self.valor_critico_forte = 20

            self.dano_investida = 15
            self.critico_investida = 2
            self.valor_critico_investida = 20

            self.dano_arremesso = 10
            self.critico_arremesso = 3
            self.valor_critico_arremesso = 30
        elif self.subclasse == "Sabre":
            self.dano_simples = 10
            self.critico_simples = 4
            self.valor_critico_simples = 25

            self.dano_forte = 15
            self.critico_forte = 3
            self.valor_critico_forte = 25

            self.dano_investida = 15
            self.critico_investida = 3
            self.valor_critico_investida = 25

            self.dano_arremesso = 10
            self.critico_arremesso = 3
            self.valor_critico_arremesso = 30
        elif self.subclasse == "Machadinha":
            self.dano_simples = 10
            self.critico_simples = 2
            self.valor_critico_simples = 25

            self.dano_forte = 15
            self.critico_forte = 3
            self.valor_critico_forte = 25

            self.dano_investida = 15
            self.critico_investida = 2
            self.valor_critico_investida = 25

            self.dano_arremesso = 15
            self.critico_arremesso = 2
            self.valor_critico_arremesso = 20
        elif self.subclasse == "Machado":
            self.dano_simples = 10
            self.critico_simples = 2
            self.valor_critico_simples = 25

            self.dano_forte = 15
            self.critico_forte = 4
            self.valor_critico_forte = 25

            self.dano_investida = 20
            self.critico_investida = 2
            self.valor_critico_investida = 25

            self.dano_arremesso = 10
            self.critico_arremesso = 4
            self.valor_critico_arremesso = 30
        elif self.subclasse == "Lança":
            self.dano_simples = 10
            self.critico_simples = 1
            self.valor_critico_simples = 20

            self.dano_forte = 10
            self.critico_forte = 3
            self.valor_critico_forte = 22

            self.dano_investida = 14
            self.critico_investida = 3
            self.valor_critico_investida = 20

            self.dano_arremesso = 14
            self.critico_arremesso = 3
            self.valor_critico_arremesso = 22
        elif self.subclasse == "Martelo":
            self.dano_simples = 10
            self.critico_simples = 2
            self.valor_critico_simples = 25

            self.dano_forte = 10
            self.critico_forte = 2
            self.valor_critico_forte = 18

            self.dano_investida = 14
            self.critico_investida = 2
            self.valor_critico_investida = 25

            self.dano_arremesso = 10
            self.critico_arremesso = 2
            self.valor_critico_arremesso = 20
        elif self.subclasse == "Porrete":
            self.dano_simples = 8
            self.critico_simples = 2
            self.valor_critico_simples = 25

            self.dano_forte = 14
            self.critico_forte = 2
            self.valor_critico_forte = 20

            self.dano_investida = 14
            self.critico_investida = 2
            self.valor_critico_investida = 20

            self.dano_arremesso = 8
            self.critico_arremesso = 2
            self.valor_critico_arremesso = 25
        elif self.subclasse == "Taco":
            self.dano_simples = 10
            self.critico_simples = 2
            self.valor_critico_simples = 20

            self.dano_forte = 15
            self.critico_forte = 2
            self.valor_critico_forte = 18

            self.dano_investida = 15
            self.critico_investida = 2
            self.valor_critico_investida = 18

            self.dano_arremesso = 10
            self.critico_arremesso = 2
            self.valor_critico_arremesso = 25
        elif self.subclasse == "Maça":
            self.dano_simples = 8
            self.critico_simples = 2
            self.valor_critico_simples = 20

            self.dano_forte = 15
            self.critico_forte = 3
            self.valor_critico_forte = 23

            self.dano_investida = 15
            self.critico_investida = 3
            self.valor_critico_investida = 23

            self.dano_arremesso = 8
            self.critico_arremesso = 2
            self.valor_critico_arremesso = 20
        elif self.subclasse == "Marreta":
            self.dano_simples = 10
            self.critico_simples = 2
            self.valor_critico_simples = 20

            self.dano_forte = 20
            self.critico_forte = 3
            self.valor_critico_forte = 30

            self.dano_investida = 20
            self.critico_investida = 3
            self.valor_critico_investida = 30

            self.dano_arremesso = 10
            self.critico_arremesso = 3
            self.valor_critico_arremesso = 30
        else:
            print(f"Erro: Subclasse '{self.subclasse}' não reconhecida.")
    
        if raridade == "Quebrada":
            self.dano_simples -= 2
            self.dano_forte -= 2
            self.dano_investida -= 2
            self.dano_arremesso -= 2
        elif raridade == "Comum":
            self.dano_simples += 0
            self.dano_forte += 0
            self.dano_investida += 0
            self.dano_arremesso += 0
        elif raridade == "Incomum":
            self.dano_simples += 2
            self.dano_forte += 2
            self.dano_investida += 2
            self.dano_arremesso += 2
        elif raridade == "Rara":
            self.dano_simples += 4
            self.dano_forte += 4
            self.dano_investida += 4
            self.dano_arremesso += 4
        elif raridade == "Épica":
            self.dano_simples += 6
            self.dano_forte += 6
            self.dano_investida += 6
            self.dano_arremesso += 6
        elif raridade == "Exótica":
            self.dano_simples += 8
            self.dano_forte += 8
            self.dano_investida += 8
            self.dano_arremesso += 8
        elif raridade == "Lendária":
            self.dano_simples += 10
            self.dano_forte += 10
            self.dano_investida += 10
            self.dano_arremesso += 10
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
            "Subclasse": self.subclasse,
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
            self.dano = 10
            self.recuo = 2
            self.MaxRange = 40
            self.MinRange = 2
            self.ShortCrit = 18
            self.MediumCrit = 25
            self.LongCrit = 30
        elif classe == "Revolver":
            self.dano = 14
            self.recuo = 3
            self.MaxRange = 50
            self.MinRange = 2
            self.ShortCrit = 20
            self.MediumCrit = 22
            self.LongCrit = 28
        elif classe == "Submetralhadora":
            self.dano = 10
            self.recuo = 2
            self.MaxRange = 45
            self.MinRange = 3
            self.ShortCrit = 18
            self.MediumCrit = 25
            self.LongCrit = 29
        elif classe == "Escopeta":
            self.dano = 20
            self.recuo = 3
            self.MaxRange = 45
            self.MinRange = 4
            self.ShortCrit = 20
            self.MediumCrit = 30
            self.LongCrit = 40
        elif classe == "Espingarda":
            self.dano = 16
            self.recuo = 3
            self.MaxRange = 60
            self.MinRange = 3
            self.ShortCrit = 22
            self.MediumCrit = 28
            self.LongCrit = 34
        elif classe == "Carabina":
            self.dano = 10
            self.recuo = 3
            self.MaxRange = 60
            self.MinRange = 4
            self.ShortCrit = 20
            self.MediumCrit = 24
            self.LongCrit = 30
        elif classe == "Fuzil De Assalto":
            self.dano = 10
            self.recuo = 3
            self.MaxRange = 80
            self.MinRange = 5
            self.ShortCrit = 22
            self.MediumCrit = 24
            self.LongCrit = 28
        elif classe == "Fuzil De Batalha":
            self.dano = 12
            self.recuo = 3
            self.MaxRange = 100
            self.MinRange = 6
            self.ShortCrit = 22
            self.MediumCrit = 21
            self.LongCrit = 22
        elif classe == "DMR":
            self.dano = 20
            self.recuo = 3
            self.MaxRange = 130
            self.MinRange = 6
            self.ShortCrit = 28
            self.MediumCrit = 24
            self.LongCrit = 19
        elif classe == "Fuzil De Precisão":
            self.dano = 20
            self.recuo = 3
            self.MaxRange = 150
            self.MinRange = 7
            self.ShortCrit = 32
            self.MediumCrit = 22
            self.LongCrit = 18
        elif classe == "Metralhadora leve":
            self.dano = 10
            self.recuo = 3
            self.MaxRange = 80
            self.MinRange = 8
            self.ShortCrit = 25
            self.MediumCrit = 22
            self.LongCrit = 25
        elif classe == "Metralhadora média":
            self.dano = 14
            self.recuo = 3
            self.MaxRange = 100
            self.MinRange = 15
            self.ShortCrit = 25
            self.MediumCrit = 25
            self.LongCrit = 25
        elif classe == "Metralhadora média":
            self.dano = 20
            self.recuo = 4
            self.MaxRange = 150
            self.MinRange = 20
            self.ShortCrit = 30
            self.MediumCrit = 30
            self.LongCrit = 30
        elif classe == "Fuzil anti-material":
            self.dano = 35
            self.recuo = 5
            self.MaxRange = 250
            self.MinRange = 25
            self.ShortCrit = 35
            self.MediumCrit = 25
            self.LongCrit = 20
        else:
            print(f"Erro: Classe '{classe}' não reconhecida.")
        
        if acao == "Simples":
            self.recuo -= 1
            self.dano += 4
            self.MinRange += 1
            self.MaxRange += 5
        elif acao == "Semi":
            self.recuo += 1
            self.dano += 2
            self.MinRange += 0
            self.MaxRange += 0
        elif acao == "Dupla":
            self.recuo += 0
            self.dano += 4
            self.MinRange += 0
            self.MaxRange += 0
        elif acao == "Rajada":
            self.recuo += 0
            self.dano += 2
            self.MinRange += 0
            self.MaxRange += 0
        elif acao == "Auto":
            self.recuo += 1
            self.dano -= 2
            self.MinRange += 0
            self.MaxRange -= 5
        elif acao == "Pump":
            self.recuo -= 1
            self.dano += 4
            self.MinRange += 1
            self.MaxRange += 5
        elif acao == "Alavanca":
            self.recuo -= 1
            self.dano += 4
            self.MinRange += 1
            self.MaxRange += 5
        elif acao == "Bolt":
            self.recuo -= 1
            self.dano += 4
            self.MinRange += 2
            self.MaxRange += 10
        else:
            print(f"Erro: Ação '{acao}' não reconhecida.")
        
        if raridade == "Quebrada":
            self.dano -= 2
            self.MaxRange -= 5
        elif raridade == "Comum":
            pass
        elif raridade == "Incomum":
            self.dano += 1
            self.MaxRange += 2
        elif raridade == "Rara":
            self.dano += 2
            self.MaxRange += 4
        elif raridade == "Épica":
            self.dano += 3
            self.MaxRange += 6
        elif raridade == "Exótica":
            self.dano += 4
            self.MaxRange += 8
        elif raridade == "Lendária":
            self.dano += 5
            self.MaxRange += 10
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
        """
        Carrega a munição na arma, define a penetração da munição carregada e retorna a quantidade carregada.
        """
        if self.municao is None:
            self.municao = municao
            self.Perfuracao = municao.perfuracao

        if self.municao.nome != municao.nome:
            print(f"Erro: Já há outra munição ({self.municao.nome}) carregada na arma.")
            return 0

        # Calcula a quantidade de munição que pode ser carregada
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
        }


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

        if self.classe == "Bandidos": pass
        if self.classe == "NRDN": pass
        if self.classe == "Aberrações": pass
        if self.classe == "Nexus Core Agency": pass
        if self.classe == "Bandido": pass
        if self.classe == "Bandido": pass
        if self.classe == "Bandido": pass

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

class Kit:
    def __init__(self, nome, itens, pools):
        self.nome = nome
        self.pools = pools
        self.itens_simples = set()
        self.itens_com_quantidade = {}

        for item in itens:
            if isinstance(item, str):
                self.itens_simples.add(item)
            elif isinstance(item, tuple) and len(item) == 2:
                nome, qtd = item
                self.itens_com_quantidade[nome] = qtd

        self.itens = self.gerar_itens()

    def gerar_itens(self):
        resultado = []
        for nome in self.itens_simples:
            if nome in self.pools:
                resultado.append(self.pools[nome]())
        for nome, qtd in self.itens_com_quantidade.items():
            if nome in self.pools:
                for _ in range(qtd):
                    resultado.append(self.pools[nome]())
        return resultado

    def buscar_em_pools(self, nome):
        for pool in self.pools:
            if nome in pool:
                return pool[nome]
        return None

### Funções de Geração ###
def Gerador(npc: NPC, kit=None, nivel=None, nome=None, proficiencias_base=None):
    if nivel is None:
        nivel = 1
    f = npc.forca
    a = npc.agilidade
    v = npc.vigor
    i = npc.inteligencia
    p = npc.presenca
    t = npc.tatica

    nome_base = nome or f"{npc.classe} ({npc.grupo})"

    inimigo = Personagem.CriarPersonagem(nome=nome_base, nivel=nivel, Forca=f, Agilidade=a, Vigor=v, Inteligencia=i, Presenca=p, Tatica=t, proficiencias_base=proficiencias_base)
    if kit:
        for item in kit.itens:
            inimigo.inventario.adicionar_item_objeto(item)
    return inimigo

def Gerador_grupo(self, grupo_destino, configuracoes):
    for config in configuracoes:
        npc_base = config['npc_base']
        kit = config['kit']
        nivel = config['nivel']
        nome = config['nome']

        personagem = Gerador(npc=npc_base, kit=kit, nivel=nivel, nome=nome)
        self.GruposDePersonagens[grupo_destino].append(personagem)

    self.refresh()
### Funções de Geração ###

### Funções de Acerto ###
def acerto_melee(atacante: Personagem, alvo: Personagem, rolagem: int, id_arma, regiao: str, debuff: int, tipo_ataque: str):
    resultado = ""

    arma_data = atacante.inventario.obter_item_por_id(id_arma)
    if not arma_data:
        return
    arma_obj = arma_data["item"]

    arma_obj = arma_data["item"]
    classe = arma_obj.classe

    if classe == "Cortante":
        BonusClasseArma = atacante.proficiencias.obter_bonus("Arma")
    elif classe == "Concussiva":
        BonusClasseArma = atacante.proficiencias.obter_bonus("luta")
    else:
        BonusClasseArma = 0

    if not isinstance(arma_obj, Melee):
        return "Erro: A arma utilizada não é corpo a corpo.\n"

    mapa_regioes = {'Cabeça': 'Cabeça', 'Rosto': 'Rosto', 'Torso': 'Torso', 'Pernas': 'Pernas', 'Braços': 'Braços'}
    if regiao not in mapa_regioes:
        return "Erro: Região inválida para calcular acerto.\n"

    protecao = getattr(alvo, mapa_regioes[regiao], None)
    debuff_total = alvo.proficiencias.obter_bonus("fortitude") + debuff

    if tipo_ataque == "simples":
        dano_base = arma_obj.dano_simples
        crit_mult = arma_obj.critico_simples
        valor_pra_crit = arma_obj.base_valor_critico_simples
    elif tipo_ataque == "forte":
        dano_base = arma_obj.dano_forte
        crit_mult = arma_obj.critico_forte
        valor_pra_crit = arma_obj.base_valor_critico_forte
    elif tipo_ataque == "investida":
        dano_base = arma_obj.dano_investida
        crit_mult = arma_obj.critico_investida
        valor_pra_crit = arma_obj.base_valor_critico_investida
    elif tipo_ataque == "arremesso":
        dano_base = arma_obj.dano_arremesso
        crit_mult = arma_obj.critico_arremesso
        valor_pra_crit = arma_obj.base_valor_critico_arremesso
    else:
        return "Erro: Tipo de ataque inválido. Escolha entre 'simples', 'forte', 'investida' ou 'arremesso'.\n"

    absorcao = protecao.absorcaoFisica if protecao else 0

    bonusconta = valor_pra_crit > 20
    acerto_final = rolagem + atacante.proficiencias.obter_bonus("luta")

    if bonusconta == True:
        if acerto_final >= atacante.bloqueio:
            if acerto_final >= valor_pra_crit:
                dano_final = (dano_base * crit_mult) + BonusClasseArma - (absorcao + debuff_total)
                dano_final = max(1, dano_final)
                alvo.TomarDano(dano_final)
                resultado += f"{atacante.nome} causou {dano_final} de dano crítico com {arma_obj.nome} em um ataque {tipo_ataque}.\n"
            else:
                dano_final = (dano_base) + BonusClasseArma - (absorcao + debuff_total)
                dano_final = max(1, dano_final)
                alvo.TomarDano(dano_final)
                resultado += f"{atacante.nome} causou {dano_final} de dano com {arma_obj.nome} ({tipo_ataque}).\n"
    else:
        if acerto_final >= atacante.bloqueio:
            if rolagem >= valor_pra_crit:
                dano_final = (dano_base * crit_mult) + BonusClasseArma - (absorcao + debuff_total)
                dano_final = max(1, dano_final)
                alvo.TomarDano(dano_final)
                resultado += f"{atacante.nome} causou {dano_final} de dano crítico com {arma_obj.nome} em um ataque {tipo_ataque}.\n"
            else:
                dano_final = (dano_base) + BonusClasseArma - (absorcao + debuff_total)
                dano_final = max(1, dano_final)
                alvo.TomarDano(dano_final)
                resultado += f"{atacante.nome} causou {dano_final} de dano com {arma_obj.nome} ({tipo_ataque}).\n"
        else:
            resultado += f"{atacante.nome} errou o ataque {tipo_ataque} com a/ou {arma_obj.nome}.\n"
    return resultado


def acerto_ranged(atacante: Personagem, alvo: Personagem, rolagem: int, id_arma, distancia: int, disparos: int, regiao: str, debuff: int):
    resultado = ""

    arma_data = atacante.inventario.obter_item_por_id(id_arma)
    if not arma_data:
        print(f"[ERRO] Arma com ID {id_arma} não encontrada no inventário de {atacante.nome}")
        return
    
    arma_obj = arma_data["item"]

    if not isinstance(arma_obj, Ranged):
        return "Erro: A arma utilizada não é de fogo.\n"

    mapa_regioes = {'Cabeça': 'Cabeça', 'Rosto': 'Rosto', 'Torso': 'Torso', 'Pernas': 'Pernas', 'Braços': 'Braços'}

    if regiao not in mapa_regioes:
        return "Erro: Região inválida para calcular acerto.\n"

    protecao = getattr(alvo, mapa_regioes[regiao], None)

    dano = arma_obj.dano
    debuff_acerto, debuff_dano = 0, 0

    if distancia <= 50:
        ValorPraCrit = arma_obj.ShortCrit
    elif distancia > 51 and distancia <= 100:
        ValorPraCrit = arma_obj.MediumCrit
    else:
        ValorPraCrit = arma_obj.LongCrit

    if distancia < arma_obj.MinRange:
        debuff_acerto = 2 * (arma_obj.MinRange - distancia)
    elif distancia > arma_obj.MaxRange:
        debuff_dano = 2 * ((distancia - arma_obj.MaxRange) // 5)
        debuff_acerto = (distancia - arma_obj.MaxRange) // 5

    nivel = protecao.nivelBalistico if protecao else 0
    absorcao = protecao.absorcaoBalistica if protecao else 0
    
    if arma_obj.municao: perfuracao = arma_obj.municao.perfuracao
    else: 
        resultado += "Sem munição"
        return resultado

    if perfuracao > nivel:
        absorcao //= 2
    elif perfuracao < nivel:
        absorcao *= 2

    dano_final = dano - debuff_dano
    acerto_final = rolagem + atacante.proficiencias.obter_bonus("pontaria") - debuff_acerto - debuff

    for disparo in range(min(disparos, arma_obj.munições)):
        if arma_obj.munições == 0:
            resultado += f"Disparo {disparo + 1}: Click... (Sem munição)\n"
            break
        if ValorPraCrit > 20:
            BonusConta = True
        else:
            BonusConta = False
        if BonusConta == True:
            if acerto_final >= ValorPraCrit:
                if acerto_final >= alvo.esquiva:
                    dano_tiro = max(1, ((dano_final * 2) - absorcao))
                    resultado += f"Disparo {disparo + 1}: {dano_tiro} de dano crítico.\n"
                    alvo.TomarDano(dano_tiro)
                else:
                    resultado += f"Disparo {disparo + 1}: Errou.\n"
            else:
                if acerto_final >= alvo.esquiva:
                    dano_tiro = max(1, (dano_final - absorcao))
                    resultado += f"Disparo {disparo + 1}: {dano_tiro} de dano.\n"
                    alvo.TomarDano(dano_tiro)
                else:
                    resultado += f"Disparo {disparo + 1}: Errou.\n"
        else:
            if rolagem >= ValorPraCrit:
                if acerto_final >= alvo.esquiva:
                    dano_tiro = max(1, ((dano_final * 2) - absorcao))
                    resultado += f"Disparo {disparo + 1}: {dano_tiro} de dano crítico.\n"
                    alvo.TomarDano(dano_tiro)
                else:
                    resultado += f"Disparo {disparo + 1}: Errou.\n"
            else:
                if acerto_final >= alvo.esquiva:
                    dano_tiro = max(1, (dano_final - absorcao))
                    resultado += f"Disparo {disparo + 1}: {dano_tiro} de dano.\n"
                    alvo.TomarDano(dano_tiro)
                else:
                    resultado += f"Disparo {disparo + 1}: Errou.\n"
        acerto_final -= arma_obj.recuo
        arma_obj.munições -= 1

    return resultado
### Funções de Acerto ###