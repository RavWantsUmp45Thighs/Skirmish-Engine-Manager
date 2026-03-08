from uuid import uuid4
import json
import os
import random
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple, Union

def gerar_id():
    return str(uuid4())[:7]

def serializar_item(item):
    """Serializa um item em dict, incluindo o nome da classe"""
    if item is None:
        return None

    if hasattr(item, "to_dict"):
        data = item.to_dict()
    else:
        # fallback simples
        data = item.__dict__.copy()

    data["__class__"] = item.__class__.__name__
    return data

def deserializar_item(item_data):
    """Deserializa um item a partir de dict usando from_dict da própria classe"""
    if item_data is None:
        return None

    if not isinstance(item_data, dict):
        return item_data

    class_name = item_data.get("__class__")
    if not class_name:
        return item_data

    # Busca a classe SOMENTE no escopo atual (sem importar Dados)
    cls = globals().get(class_name)
    if not cls:
        print(f"⚠️ Classe '{class_name}' não encontrada ao deserializar item.")
        return item_data

    dados_limpos = {k: v for k, v in item_data.items() if k != "__class__"}

    if hasattr(cls, "from_dict"):
        try:
            return cls.from_dict(dados_limpos)
        except Exception as e:
            print(f"⚠️ Erro ao deserializar {class_name}: {e}")
            return None

    try:
        return cls(**dados_limpos)
    except Exception as e:
        print(f"⚠️ Falha ao instanciar {class_name} diretamente: {e}")
        return None

tipos_de_dano = ["contundente","concussivo","cortante","perfurante","balístico","rasgante","explosivo","incendiário","congelante","envenenante","eletrocutante","mental"]
tipos_de_teste =  ["iniciativa","sorte","força","agilidade","vigor","inteligencia","presença","tática","poder","físico","mental","vocal","qualquer teste"]
palavras_chave_atributo = ["vida","energia","mana","vidaMax","energiaMax","manaMax","movimentação","bloqueio","esquiva","resistência","carga","percepção"]

class InventarioMundo:
    """Repositório global de itens soltos no cenário (arremessados, dropados, etc.)
    Cada entrada: {"item": obj, "origem": str, "local": str}
    """
    _instancia = None

    @classmethod
    def get(cls):
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def __init__(self):
        self.itens = []  # [{"item": obj, "origem": str, "local": str}]

    def adicionar(self, item, origem="desconhecido", local="campo"):
        self.itens.append({"item": item, "origem": origem, "local": local})

    def remover(self, item):
        self.itens = [e for e in self.itens if e["item"] is not item]

    def listar(self, local=None):
        if local:
            return [e for e in self.itens if e["local"] == local]
        return self.itens.copy()

    def limpar(self):
        self.itens.clear()

    def to_dict(self):
        return [{"item": serializar_item(e["item"]), "origem": e["origem"], "local": e["local"]} for e in self.itens]

    @classmethod
    def from_dict(cls, data):
        inst = cls()
        for e in data:
            item = deserializar_item(e.get("item"))
            if item:
                inst.itens.append({"item": item, "origem": e.get("origem", ""), "local": e.get("local", "campo")})
        return inst

### CLASSE PERSONAGEM ###
### CLASSE PERSONAGEM ###
### CLASSE PERSONAGEM ###
class Personagem:
    def __init__(self, nome, Nivel, Forca, Agilidade, Vigor, Inteligencia, Presenca, Tatica, Poder, proficiencias_base=None, recalcular=True):
        self.nome: str = nome
        self.Nivel: int = Nivel
        self.XPlvlUp: int = 500 + (500 * Nivel)
        self.XPAtual: int = 0
        self.VidaMax: int = 100 + (10 * Vigor)
        self.VidaAtual: int = self.VidaMax
        self.EnergiaMax: int = 2 + Forca
        self.EnergiaAtual: int = self.EnergiaMax
        self.ManaMax: int = 1 + Poder * 2
        self.ManaAtual: int = self.ManaMax
        self.Bloqueio: int = 5 + Forca
        self.Esquiva: int = 5 + Agilidade
        self.Percepcao: int = 5
        self.Movimento: int = 5 + (Agilidade * 2)
        self.Disparada: int = 8 + (Agilidade * 4)
        self.CargaMax: float = 15 + (Forca * 2)
        self.CargaAtual: float = 0
        self.Forca: int = Forca
        self.Agilidade: int = Agilidade
        self.Vigor: int = Vigor
        self.Inteligencia: int = Inteligencia
        self.Presenca: int = Presenca
        self.Tatica: int = Tatica
        self.Poder: int = Poder
        self.inventario = Inventario()
        self.regioes_corpo = {"cabeça": None, "rosto": None, "pescoço": None, "peito": None, "costas": None, "abdômen": None, "braços": None, "pernas": None}
        self.slots = {"mao_direita": SlotEquipamento("Mão Direita", "mao"), "mao_esquerda": SlotEquipamento("Mão Esquerda", "mao")}
        self.equipamentos_slots = []
        self.proficiencias = SistemaDeProficiencias()
        if proficiencias_base: self.proficiencias.carregar_base(proficiencias_base)
        
        # NOVO: Sistema unificado de resistências
        self.resistencias_base = {tipo: 0 for tipo in tipos_de_dano}  # valores naturais (positivo=resistência, negativo=vulnerabilidade)
        self.resistencias_mod = {tipo: 0 for tipo in tipos_de_dano}   # modificações de efeitos (buffs/debuffs/poderes/habilidades)
        self.imunidades_mod = set()   # imunidades de modificações
        
        self.mod_desarmado = {"dano_bonus":0,"crit_mult":0,"crit_valor":0,}
        self.mod_testes = {teste: 0 for teste in tipos_de_teste}
        self.mod_efeitos = {atributo: 0 for atributo in palavras_chave_atributo}
        self.mod_temporarios = []
        self.mod_efeitos_ativos = []
        self.bonus_testes = {teste: 0 for teste in tipos_de_teste}
        self.bonus_atributos = {"forca": 0, "agilidade": 0, "vigor": 0,"inteligencia": 0, "presenca": 0, "tatica": 0, "poder": 0}
        self.poderes = GerenciadorDePoderes(self)
        self.habilidades = GerenciadorDeHabilidades(self)
        self.buffs_debuffs = GerenciadorDeBuffsDebuffs(self)
        if recalcular: self.recalcularAtributos()

    @staticmethod
    def CriarPersonagem(nome, nivel, Forca, Agilidade, Vigor, Inteligencia, Presenca, Tatica, Poder, proficiencias_base=None):
        return Personagem(nome, nivel, Forca, Agilidade, Vigor, Inteligencia, Presenca, Tatica, Poder, proficiencias_base)

    def base_vida(self): return 100 + (10 * self.Vigor)
    def base_mana(self): return 1 + (2 * self.Poder)
    def base_energia(self): return 2 + self.Forca
    def base_bloqueio(self): return 5 + self.Forca
    def base_esquiva(self): return 5 + self.Agilidade
    def base_movimento(self): return 5 + (self.Agilidade * 2)
    def base_disparada(self): return 8 + (self.Agilidade * 4)
    def base_carga(self): return 15 + (self.Forca * 2)
    def base_percepcao(self): return 5

    def bonus_proficiencias(self):
        return self.proficiencias.obter_proficiencias("Vitalidade","Carga","Luta","Reflexo","Atletismo","Percepção","Mana")
    
    def bonus_vida(self): return self.bonus_proficiencias().get("Vitalidade",0)*2
    def bonus_mana(self): return self.bonus_proficiencias().get("Mana",0)
    def bonus_carga(self): return self.bonus_proficiencias().get("Carga",0)
    def bonus_bloqueio(self): return self.bonus_proficiencias().get("Luta",0)//2
    def bonus_esquiva(self): return self.bonus_proficiencias().get("Reflexo",0)//2
    def bonus_movimento(self): return self.bonus_proficiencias().get("Atletismo",0)
    def bonus_disparada(self): return self.bonus_proficiencias().get("Atletismo",0)
    def bonus_percepcao(self): return self.bonus_proficiencias().get("Percepção",0)

    def breakdown(self, atributo):
        base = getattr(self, f"base_{atributo}")()
        bonus = getattr(self, f"bonus_{atributo}")() if hasattr(self, f"bonus_{atributo}") else 0
        mod = self.mod_efeitos.get(atributo, 0)
        final = base + bonus + mod
        return base, bonus, mod, final

    def get_teste(self, nome: str) -> int:
        nome = nome.lower()
        return self.mod_testes.get(nome, 0) + self.bonus_testes.get(nome, 0)

    def get_atributo(self, nome: str) -> int:
        nome = nome.lower()
        base = getattr(self, nome.capitalize(), 0)
        bonus = self.bonus_atributos.get(nome, 0)
        return base + bonus

    def calcular_peso_total(self):
        peso_total=0; contados=set()
        for equipamento in self.equipamentos_slots:
            if hasattr(equipamento,"peso") and id(equipamento) not in contados:
                peso_total+=equipamento.peso; contados.add(id(equipamento))
        for slot in self.slots.values():
            if slot.item and hasattr(slot.item,"peso") and id(slot.item) not in contados:
                peso_total+=slot.item.peso; contados.add(id(slot.item))
        for entrada in self.inventario.itens:
            item=entrada.get("item"); qtd=entrada.get("quantidade",1)
            if item and hasattr(item,"peso"): peso_total+=item.peso*qtd
        self.CargaAtual=peso_total
        return peso_total

    def recalcularAtributos(self):
        self.VidaMax    = max(1, self.base_vida()    + self.bonus_vida()    + self.mod_efeitos.get("vidamax",    0))
        self.VidaAtual  = min(self.VidaAtual,  self.VidaMax)
        self.EnergiaMax  = max(1, self.base_energia() +                        self.mod_efeitos.get("energiamax", 0))
        self.EnergiaAtual = min(self.EnergiaAtual, self.EnergiaMax)
        self.ManaMax    = max(1, self.base_mana()    + self.bonus_mana()    + self.mod_efeitos.get("manamax",    0))
        self.ManaAtual  = min(self.ManaAtual,  self.ManaMax)
        self.Bloqueio   = self.base_bloqueio()   + self.bonus_bloqueio()
        self.Esquiva    = self.base_esquiva()    + self.bonus_esquiva()
        self.CargaMax   = self.base_carga()      + self.bonus_carga()
        self.Movimento  = self.base_movimento()  + self.bonus_movimento()
        self.Disparada  = self.base_disparada()  + self.bonus_disparada()
        self.Percepcao  = self.base_percepcao()  + self.bonus_percepcao()
        self.calcular_peso_total()

    def preencher_recursos_ao_maximo(self):
        """Preenche Vida, Energia e Mana ao máximo"""
        self.VidaAtual = self.VidaMax; self.EnergiaAtual = self.EnergiaMax; self.ManaAtual = self.ManaMax

    def obter_resistencia_total(self, tipo):
        """Retorna a resistência total (base + modificações). Positivo=resistência, negativo=vulnerabilidade"""
        return self.resistencias_base.get(tipo, 0) + self.resistencias_mod.get(tipo, 0)
    
    def obter_imunidade(self, tipo):
        resistencia = self.obter_resistencia_total(tipo)
        return resistencia >= 100 or tipo in self.imunidades_mod
    
    def modificar_resistencia_base(self, tipo, valor):
        """Modifica a resistência NATURAL do personagem"""
        if tipo in self.resistencias_base:
            self.resistencias_base[tipo] = max(-100, min(100, self.resistencias_base[tipo] + valor))
    
    def modificar_resistencia_mod(self, tipo, valor):
        """Modifica a resistência por EFEITOS (buffs/debuffs/poderes)"""
        if tipo in self.resistencias_mod:
            self.resistencias_mod[tipo] = max(-100, min(100, self.resistencias_mod[tipo] + valor))
   
    def toggle_imunidade_mod(self, tipo):
        """Adiciona/remove imunidade por EFEITOS"""
        if tipo in self.imunidades_mod:
            self.imunidades_mod.discard(tipo)
        else:
            self.imunidades_mod.add(tipo)

    def modificar_nivel(self, delta):
        self.Nivel = max(1, self.Nivel + delta)
        self.XPlvlUp = 500 + (500 * self.Nivel)
        self.XPAtual = min(self.XPAtual, self.XPlvlUp - 1)

    def calcular_dano_recebido(self, dano, tipo):
        if self.obter_imunidade(tipo):
            return 0
        
        resistencia = self.obter_resistencia_total(tipo)
        
        if resistencia >= 100:
            return 0  # Imunidade completa por resistência
        if resistencia <= -100:
            return int(dano * 2)  # Vulnerabilidade extrema (dobro do dano)
        
        if resistencia > 0:
            dano_final = dano * (1 - resistencia / 100)
        elif resistencia < 0:
            dano_final = dano * (1 - resistencia / 100)  # negativo aumenta o dano
        else:
            dano_final = dano
        
        return max(0, int(dano_final))
    
    def aplicar_efeito_com_chance(self, efeito_data, alvo=None, fonte="item"):
        """
        Aplica um efeito com chance de sucesso ao personagem ou alvo especificado.
        """
        if alvo is None:
            alvo = self
        
        tipo = efeito_data.get("tipo", "")
        nome = efeito_data.get("nome", "Efeito Desconhecido")
        chance = efeito_data.get("chance", 100)
        duracao = efeito_data.get("duracao", 1)
        descricao = efeito_data.get("descricao", "")
        valor = efeito_data.get("valor", 0)
        
        if not isinstance(chance, (int, float)) or chance < 0 or chance > 100:
            return {"aplicado": False, "mensagem": f"Chance inválida: {chance}"}
        
        roll = random.randint(1, 100)
        if roll > chance:
            return {
                "aplicado": False,
                "mensagem": f"{nome} falhou no teste de chance ({roll}% vs {chance}%)"
            }
        
        try:
            if tipo == "cura":
                alvo.ModificarVida(valor)
                return {
                    "aplicado": True,
                    "mensagem": f"{nome} curou {abs(valor)} de vida"
                }
            
            elif tipo == "energia":
                alvo.ModificarEnergia(valor)
                return {
                    "aplicado": True,
                    "mensagem": f"{nome} restaurou {abs(valor)} de energia"
                }
            
            elif tipo == "mana":
                alvo.ModificarMana(valor)
                return {
                    "aplicado": True,
                    "mensagem": f"{nome} restaurou {abs(valor)} de mana"
                }
            
            elif tipo == "dano":
                subtipo = efeito_data.get("subtipo", "")
                tipo_dano = SUBTIPO_PARA_TIPO_DANO.get(subtipo, subtipo) if subtipo else "perfurante"
                dano_final = alvo.calcular_dano_recebido(valor, tipo_dano) if tipo_dano else valor
                alvo.ModificarVida(-dano_final)
                return {
                    "aplicado": True,
                    "mensagem": f"{nome} causou {dano_final} de dano ({tipo_dano})"
                }
            
            elif tipo in ("buff", "debuff"):
                efeito = efeito_data.get("efeito", [])
                
                if isinstance(efeito, dict):
                    efeito = [efeito]
                elif not isinstance(efeito, list):
                    efeito = []
                
                bb = BuffDebuff(
                    nome=nome,
                    duracao=duracao,
                    efeito=efeito,
                    descricao=descricao,
                    tipo=tipo
                )
                alvo.buffs_debuffs.adicionar_efeito_objeto(bb)
                
                tipo_symbol = "✨ Buff" if tipo == "buff" else "💀 Debuff"
                return {
                    "aplicado": True,
                    "mensagem": f"{tipo_symbol}: {nome} aplicado por {duracao} turno(s)"
                }
            
            else:
                alvo.aplicar_efeito_estruturado(efeito_data, alvo=alvo, fonte=fonte)
                return {
                    "aplicado": True,
                    "mensagem": f"{nome} foi aplicado"
                }
        
        except Exception as e:
            return {
                "aplicado": False,
                "mensagem": f"Erro ao aplicar {nome}: {str(e)}"
            }

    def aplicar_efeitos_multiplos_com_chance(self, efeitos_lista, alvo=None, fonte="item"):
        """
        Aplica múltiplos efeitos com chance de sucesso.
        """
        if alvo is None:
            alvo = self
        
        resultados = []
        
        if not isinstance(efeitos_lista, list):
            return [{
                "aplicado": False,
                "mensagem": "Efeitos deve ser uma lista"
            }]
        
        for efeito in efeitos_lista:
            if not isinstance(efeito, dict):
                resultados.append({
                    "aplicado": False,
                    "mensagem": "Efeito inválido (não é dict)"
                })
                continue
            
            resultado = self.aplicar_efeito_com_chance(efeito, alvo=alvo, fonte=fonte)
            resultados.append(resultado)
        
        return resultados

    def aplicar_efeito_estruturado(self, efeito_data, alvo=None, duracao_override=None, fonte="efeito"):
        if alvo is None:
            alvo = self

        efeitos = efeito_data.get("efeito", [])
        if isinstance(efeitos, dict):
            efeitos = [efeitos]

        for entrada in efeitos:
            if isinstance(entrada, str):
                continue

            if entrada.get("por_turno", False):
                continue

            tags = entrada.get("tags", [])
            valor = entrada.get("valor", 0)
            atributo = entrada.get("atributo")
            duracao = duracao_override if duracao_override is not None else entrada.get("duracao")

            # atributo direto (legado)
            if atributo in ["vida", "energia", "mana"]:
                if atributo == "vida":
                    alvo.ModificarVida(valor)
                elif atributo == "energia":
                    alvo.ModificarEnergia(valor)
                elif atributo == "mana":
                    alvo.ModificarMana(valor)
                continue

            if tags:
                alvo.aplicar_modificador_generico(tags=tags, valor=valor, duracao=duracao, fonte=fonte)

    def _aplicar_tag_individual(self, tag, valor):
        tag = tag.lower()
        # bonus_atributo
        if tag.startswith("bonus_") and not tag.startswith("bonus_teste_"):
            chave = tag.replace("bonus_", "")
            if chave in self.bonus_atributos:
                self.bonus_atributos[chave] += valor
                return
        # bonus_teste
        if tag.startswith("bonus_teste_"):
            chave = tag.replace("bonus_teste_", "")
            if chave in self.bonus_testes:
                self.bonus_testes[chave] += valor
                return
            if chave == "qualquer":
                for t in self.bonus_testes:
                    if t not in {"sorte", "iniciativa"}:
                        self.bonus_testes[t] += valor
                return
        # mod_testes
        if tag in self.mod_testes:
            self.mod_testes[tag] += valor
            return
        if tag == "qualquer teste":
            for t in self.mod_testes:
                if t not in {"sorte", "iniciativa"}:
                    self.mod_testes[t] += valor
            return
        # mod_efeitos (movimentação, bloqueio, etc.)
        if tag in self.mod_efeitos:
            self.mod_efeitos[tag] += valor
            return
        # vidaMax / energiaMax / manaMax — acumula em mod_efeitos e recalcula
        if tag == "vidamax":
            self.mod_efeitos["vidamax"] = self.mod_efeitos.get("vidamax", 0) + valor
            self.recalcularAtributos()
            return
        if tag == "energiamax":
            self.mod_efeitos["energiamax"] = self.mod_efeitos.get("energiamax", 0) + valor
            self.recalcularAtributos()
            return
        if tag == "manamax":
            self.mod_efeitos["manamax"] = self.mod_efeitos.get("manamax", 0) + valor
            self.recalcularAtributos()
            return
        # vida_max legado
        if tag == "vida_max":
            self.mod_efeitos["vidamax"] = self.mod_efeitos.get("vidamax", 0) + valor
            self.recalcularAtributos()
            return
        # resistencia_<tipo> — modifica resistências
        if tag.startswith("resistencia_"):
            tipo = tag.replace("resistencia_", "")
            if tipo in self.resistencias_mod:
                self.modificar_resistencia_mod(tipo, valor)
            return
        # imune_<tipo>
        if tag.startswith("imune_"):
            tipo = tag.replace("imune_", "")
            if valor != 0:
                self.toggle_imunidade_mod(tipo)
            return
        if tag == "desarmado_dano":
            self.mod_desarmado["dano_bonus"] += valor
            return
        if tag == "desarmado_crit_mult":
            self.mod_desarmado["crit_mult"] += valor
            return
        if tag == "desarmado_crit_valor":
            self.mod_desarmado["crit_valor"] += valor
            return
        # tipo de dano direto — aplica dano imediato no personagem
        if tag in tipos_de_dano:
            dano_final = self.calcular_dano_recebido(abs(valor), tag)
            self.ModificarVida(-dano_final)
            return
        
    def aplicar_modificador_generico(self, tags, valor, duracao=None, fonte="temporario"):
        registro = {"tags": tags, "valor": valor, "duracao": duracao, "fonte": fonte}
        if duracao is not None and duracao > 0:
            self.mod_temporarios.append(registro)
        for tag in tags:
            self._aplicar_tag_individual(tag, valor)
        self.recalcularAtributos()

    def remover_modificador_generico(self, tags, valor):
        for tag in tags:
            tag = tag.lower()
            if tag.startswith("bonus_") and not tag.startswith("bonus_teste_"):
                chave = tag.replace("bonus_", "")
                if chave in self.bonus_atributos:
                    self.bonus_atributos[chave] -= valor
                    continue
            if tag.startswith("bonus_teste_"):
                chave = tag.replace("bonus_teste_", "")
                if chave in self.bonus_testes:
                    self.bonus_testes[chave] -= valor
                    continue
                if chave == "qualquer":
                    for t in self.bonus_testes:
                        if t not in {"sorte", "iniciativa"}:
                            self.bonus_testes[t] -= valor
                    continue
            if tag in self.mod_testes:
                self.mod_testes[tag] -= valor
                continue
            if tag == "qualquer teste":
                for t in self.mod_testes:
                    if t not in {"sorte", "iniciativa"}:
                        self.mod_testes[t] -= valor
                continue
            if tag in self.mod_efeitos:
                self.mod_efeitos[tag] -= valor
                continue
            # vidaMax / energiaMax / manaMax — reverte em mod_efeitos
            if tag == "vidamax":
                self.mod_efeitos["vidamax"] = self.mod_efeitos.get("vidamax", 0) - valor
                continue
            if tag == "energiamax":
                self.mod_efeitos["energiamax"] = self.mod_efeitos.get("energiamax", 0) - valor
                continue
            if tag == "manamax":
                self.mod_efeitos["manamax"] = self.mod_efeitos.get("manamax", 0) - valor
                continue
            if tag == "vida_max":
                self.mod_efeitos["vidamax"] = self.mod_efeitos.get("vidamax", 0) - valor
                continue
            if tag.startswith("resistencia_"):
                tipo = tag.replace("resistencia_", "")
                if tipo in self.resistencias_mod:
                    self.modificar_resistencia_mod(tipo, -valor)
                continue
            if tag.startswith("imune_"):
                tipo = tag.replace("imune_", "")
                if valor != 0:
                    self.toggle_imunidade_mod(tipo)
                continue
            if tag == "desarmado_dano":
                self.mod_desarmado["dano_bonus"] -= valor
                continue
            if tag == "desarmado_crit_mult":
                self.mod_desarmado["crit_mult"] -= valor
                continue
            if tag == "desarmado_crit_valor":
                self.mod_desarmado["crit_valor"] -= valor
                continue
            # tipo de dano direto — ao remover não faz nada (dano já foi aplicado)
            if tag in tipos_de_dano:
                continue
        self.recalcularAtributos()

    def ModificarVida(self, valor):
        self.VidaAtual = max(0, min(self.VidaMax, self.VidaAtual + valor))

    def ModificarEnergia(self, valor):
        self.EnergiaAtual = max(0, min(self.EnergiaMax, self.EnergiaAtual + valor))

    def ModificarMana(self, valor):
        self.ManaAtual = max(0, min(self.ManaMax, self.ManaAtual + valor))

    def ModificarXP(self, valor):
        self.XPAtual += valor
        if self.XPAtual < 0:
            self.XPAtual = 0
        while self.XPAtual >= self.XPlvlUp:
            self.XPAtual -= self.XPlvlUp
            self.levelUp()

    def levelUp(self):
        self.Nivel += 1
        self.XPlvlUp = int(self.XPlvlUp * 1.2)

    def aplicar_efeito(self, efeito):
        for entrada in efeito["efeito"]:
            atributo = entrada["atributo"]
            valor = entrada["valor"]
            if atributo in self.mod_efeitos:
                self.mod_efeitos[atributo] += valor
            elif atributo in self.mod_testes:
                self.mod_testes[atributo] += valor

    def remover_efeito(self, efeito):
        for entrada in efeito["efeito"]:
            atributo = entrada["atributo"]
            valor = entrada["valor"]
            if atributo in self.mod_efeitos:
                self.mod_efeitos[atributo] -= valor
            elif atributo in self.mod_testes:
                self.mod_testes[atributo] -= valor

    def receber_efeito(self, efeito_data, duracao=None):
        efeito = efeito_data.get("efeito")
        tipo = efeito_data.get("tipo", "debuff")
        nome = efeito_data.get("nome", "Efeito Desconhecido")
        descricao = efeito_data.get("descricao", "")

        if isinstance(efeito, list):
            por_turno = any(e.get("por_turno") for e in efeito)
        else:
            por_turno = efeito.get("por_turno", False)

        if por_turno:
            duracao_final = duracao if duracao is not None else 1
            novo = BuffDebuff(nome=nome, duracao=duracao_final, efeito=efeito, descricao=descricao, tipo=tipo)
            self.buffs_debuffs.adicionar_efeito_objeto(novo)
        else:
            self.aplicar_efeito(efeito)

    def _eh_arma_melee(self, item):
        return (hasattr(item, 'tipo') and 'melee' in item.tipo.lower()) or 'Melee' in item.__class__.__name__ or (hasattr(item, 'categoria') and 'melee' in item.categoria.lower())

    def _eh_arma_ranged(self, item):
        return (hasattr(item, 'tipo') and 'ranged' in item.tipo.lower()) or 'Ranged' in item.__class__.__name__ or (hasattr(item, 'categoria') and 'ranged' in item.categoria.lower())

    def _suporte_compativel(self,slot,arma):
        aceita=getattr(slot,"aceita",[])
        requer=getattr(slot,"requer_maos",1)
        classe=arma.__class__.__name__
        return classe in aceita and getattr(arma,"maos",1)==requer

    def armas_em_maos(self):
        armas = []
        for nome in ["mao_direita", "mao_esquerda"]:
            slot = self.slots.get(nome)
            if slot and slot.item:
                armas.append(slot.item)
        return armas

    def arma_principal(self):
        direita = self.slots["mao_direita"].item
        esquerda = self.slots["mao_esquerda"].item
        return direita or esquerda

    def equipar_item(self, item, nome_slot=None, forcar=False):
        if not item: return False
        if self._eh_protecao(item): return self._equipar_protecao_obj(item)
        if isinstance(item,Equipamento): return self.equipar_equipamento_slot(item)
        if self._eh_arma_melee(item) or self._eh_arma_ranged(item):return self._equipar_arma(item, nome_slot, forcar)
        return False
    
    def desequipar_item(self, item):
        for slot in self.slots.values():
            if slot.item == item:
                slot.item = None
        self.inventario.gerenciar_item(item_objeto=item,quantidade=1,operacao="adicionar")
        self.calcular_peso_total()
        return True
    
    def _equipar_arma(self, arma, nome_slot=None, forcar=False, usar_duas_maos=False):
        maos_item = max(1, getattr(arma, "maos", 1))
        slots_mao = [(k, s) for k, s in self.slots.items() if s.tipo == "mao"]

        def limpar_item(item):
            if not item: return
            for s in self.slots.values():
                if s.item == item: s.item = None
            self.inventario.adicionar_item_objeto(item, 1)

        if nome_slot:
            slot = self.slots.get(nome_slot)
            if not slot: return False

            if slot.tipo == "mao":
                if not usar_duas_maos:
                    if slot.item:
                        if not forcar: return False
                        limpar_item(slot.item)
                    for _, s in slots_mao:
                        if s.item and getattr(s.item, "maos", 1) == 2:
                            limpar_item(s.item); break
                    if not self.inventario.remover_item(arma, 1): return False
                    slot.item = arma; self.calcular_peso_total(); return True

                if usar_duas_maos:
                    outras = [k for k, _ in slots_mao if k != nome_slot]
                    if not outras: return False
                    slot2 = self.slots[outras[0]]
                    if (slot.item or slot2.item) and not forcar: return False
                    antigos = set([slot.item, slot2.item])
                    for antigo in antigos: limpar_item(antigo)
                    if not self.inventario.remover_item(arma, 1): return False
                    slot.item = arma; slot2.item = arma; self.calcular_peso_total(); return True

            if slot.tipo == "suporte":
                if not slot.pode_receber(arma): return False
                if slot.item:
                    if not forcar: return False
                    limpar_item(slot.item)
                if not self.inventario.remover_item(arma, 1): return False
                slot.item = arma; self.calcular_peso_total(); return True

            return False

        livres = [k for k, s in slots_mao if s.item is None]

        if maos_item == 1:
            if livres:
                if not self.inventario.remover_item(arma, 1): return False
                self.slots[livres[0]].item = arma; self.calcular_peso_total(); return True

            # NOVO: tenta suporte compatível antes de forçar substituição na mão
            for nome, slot in self.slots.items():
                if slot.tipo == "suporte" and slot.pode_receber(arma) and not slot.item:
                    if not self.inventario.remover_item(arma, 1): return False
                    slot.item = arma; self.calcular_peso_total(); return True

            alvo = slots_mao[0][1]
            limpar_item(alvo.item)
            if not self.inventario.remover_item(arma, 1): return False
            alvo.item = arma; self.calcular_peso_total(); return True

        if maos_item == 2:
            antigos = set([s.item for _, s in slots_mao if s.item])
            for antigo in antigos: limpar_item(antigo)
            if not self.inventario.remover_item(arma, 1): return False
            for k, _ in slots_mao[:2]: self.slots[k].item = arma
            self.calcular_peso_total(); return True

        return False

    def _desequipar_arma(self,arma):
        for s in self.slots.values():
            if s.tipo=="mao" and s.item==arma: s.item=None
        self.inventario.adicionar_item_objeto(arma,1); self.calcular_peso_total(); return True

    def desequipar_item_generico(self,item):
        if not item: return False
        if isinstance(item,Equipamento): return self.remover_equipamento_slot(item)
        for s in self.slots.values():
            if s.item==item:
                for s2 in self.slots.values():
                    if s2.item==item: s2.item=None
                self.inventario.gerenciar_item(item_objeto=item,quantidade=1,operacao="adicionar")
                self.calcular_peso_total()
                return True
        for regiao,prot in self.regioes_corpo.items():
            if prot==item:
                self.regioes_corpo[regiao]=None
                self.inventario.gerenciar_item(item_objeto=item,quantidade=1,operacao="adicionar")
                self.calcular_peso_total()
                return True
        return False

    def _remover_do_inventario_generico(self, item):
        if hasattr(item, "Id"):
            self.inventario.remover_item_por_id(item.Id)
            return True
        self.inventario.remover_item(item, 1)
        return True

    def equipar_equipamento_slot(self,equipamento):
        if not isinstance(equipamento,Equipamento): return False
        if equipamento in self.equipamentos_slots: return False
        if not self.inventario.remover_item(equipamento,1): return False
        novos_slots=equipamento.criar_slots()
        for nome in novos_slots:
            if nome in self.slots: self.inventario.adicionar_item_objeto(equipamento,1); return False
        self.slots.update(novos_slots); self.equipamentos_slots.append(equipamento); self.calcular_peso_total(); return True

    def remover_equipamento_slot(self,equipamento):
        if equipamento not in self.equipamentos_slots: return False
        for dados in equipamento.slots_criados:
            nome=dados.get("nome")
            slot=self.slots.get(nome)
            if slot and slot.item: self.inventario.adicionar_item_objeto(slot.item,1)
            self.slots.pop(nome,None)
        self.equipamentos_slots.remove(equipamento); self.inventario.adicionar_item_objeto(equipamento,1); self.calcular_peso_total(); return True

    def mover_item_para_slot(self,item,nome_slot):
        slot=self.slots.get(nome_slot)
        if not slot or not slot.pode_receber(item): return False
        if slot.item: self.inventario.gerenciar_item(item_objeto=slot.item,quantidade=1,operacao="adicionar")
        if not self.inventario.remover_item(item,1): return False
        slot.item=item; self.calcular_peso_total(); return True

    def remover_item_do_slot(self, nome_slot):
        slot = self.slots.get(nome_slot)
        if not slot or not slot.item:
            return False

        item = slot.item
        item_id = getattr(item, "Id", None)

        for s in self.slots.values():
            if s.item:
                s_id = getattr(s.item, "Id", None)
                if item_id and s_id == item_id:
                    s.item = None
                elif not item_id and s.item.nome == item.nome:
                    s.item = None

        if item_id:
            self.inventario.gerenciar_item(item_objeto=item, quantidade=1, operacao="adicionar")
        else:
            self.inventario.adicionar_item_objeto(item, 1)

        self.calcular_peso_total()
        return True

    def _mover_para_suporte_ou_inventario(self,item):
        for s in self.slots.values():
            if s.tipo=="suporte" and not s.item and self._suporte_compativel(s,item):
                s.item=item
                return True
        self.inventario.adicionar_item_objeto(item,1)
        return True

    def _equipar_protecao_obj(self, item):
        regiao_indicada = getattr(item, "regiao_indicada", None) or getattr(item, "regiao", None)
        if not regiao_indicada or regiao_indicada not in self.regioes_corpo: return False
        if hasattr(item, "Id"):
            if not self.inventario.remover_item_por_id(item.Id): return False
        else:
            if not self.inventario.remover_item(item, 1): return False
        regioes_a_cobrir = [r for r in getattr(item, "regioes_cobertas", [regiao_indicada]) if r in self.regioes_corpo]
        if not regioes_a_cobrir: regioes_a_cobrir = [regiao_indicada]
        ja_devolvidos = set()
        for regiao in regioes_a_cobrir:
            atual = self.regioes_corpo.get(regiao)
            if atual and id(atual) not in ja_devolvidos:
                self.inventario.adicionar_item_objeto(atual, 1)
                ja_devolvidos.add(id(atual))
            self.regioes_corpo[regiao] = item
        self.calcular_peso_total(); return True

    def remover_protecao(self, regiao):
        if regiao not in self.regioes_corpo: return
        protecao = self.regioes_corpo.get(regiao)
        if not protecao: return
        regioes_com_item = [r for r, p in self.regioes_corpo.items() if p is protecao]
        for r in regioes_com_item: self.regioes_corpo[r] = None
        self.inventario.gerenciar_item(item_objeto=protecao, quantidade=1, operacao="adicionar")
        self.calcular_peso_total()

    def listar_protecoes(self):
        print("Proteções Equipadas:")
        for regiao,protecao in self.regioes_corpo.items():
            if protecao: print(f"{regiao}: {protecao.nome}")
            else: print(f"{regiao}: Nenhuma")
    
    def _eh_protecao(self, item):
        return hasattr(item, 'regiao') or hasattr(item, 'defesa') or 'Protecao' in item.__class__.__name__    
    
    def obter_regioes_compativeis(self,item):
        if not hasattr(item,"regioes_cobertas"): return []
        return [r for r in item.regioes_cobertas if r in self.regioes_corpo]
    
    def _equipar_protecao_obj_em_regiao(self, item_obj, regiao):
        if not item_obj or not regiao: return False
        item_obj.regiao = regiao
        return self._equipar_protecao_obj(item_obj)

    def equipar_do_inventario(self, regiao, nome_protecao):
        if regiao not in self.regioes_corpo:
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

    def processar_turno(self):
        for efeito in self.buffs_debuffs.listar_efeitos():
            efeito_list = efeito.efeito if isinstance(efeito.efeito, list) else [efeito.efeito]

            for entrada in efeito_list:
                if isinstance(entrada, str):
                    continue

                if not entrada.get("por_turno", False):
                    continue

                atributo = entrada.get("atributo")
                valor = entrada.get("valor", 0)
                tags = entrada.get("tags", [])

                # vida/energia/mana via atributo
                if atributo == "vida":
                    self.ModificarVida(valor)
                elif atributo == "energia":
                    self.ModificarEnergia(valor)
                elif atributo == "mana":
                    self.ModificarMana(valor)

                # via tags — tipo de dano ou vida/energia/mana como tag
                for tag in [t.lower() for t in tags]:
                    if tag in tipos_de_dano:
                        dano_final = self.calcular_dano_recebido(abs(valor), tag)
                        self.ModificarVida(-dano_final)
                    elif tag == "vida":
                        self.ModificarVida(valor)
                    elif tag == "energia":
                        self.ModificarEnergia(valor)
                    elif tag == "mana":
                        self.ModificarMana(valor)

        # mod_temporarios
        remover_lista = []
        for mod in self.mod_temporarios:
            if mod["duracao"] is not None:
                mod["duracao"] -= 1
            if mod["duracao"] <= 0:
                self.remover_modificador_generico(mod["tags"], mod["valor"])
                remover_lista.append(mod)
        for r in remover_lista:
            self.mod_temporarios.remove(r)

        expirados = self.buffs_debuffs.processar_turnos()
        return expirados

    def _garantir_efeito_lista(self, efeito):
        """
        Converte efeito (dict ou list) para sempre retornar uma list.
        Pula entradas inválidas (strings).
        """
        if isinstance(efeito, dict):
            return [efeito]
        elif isinstance(efeito, list):
            return efeito
        else:
            return []
    
    def calcular_ataque_desarmado(self) -> dict:
        prof_luta = self.proficiencias.obter_bonus("Luta")

        dano_base  = 10 + (2 * self.get_atributo("forca"))
        dano_final = dano_base + self.mod_desarmado["dano_bonus"]

        crit_mult_base  = 2
        crit_mult_final = crit_mult_base + self.mod_desarmado["crit_mult"]

        crit_valor_base  = 20 - (prof_luta // 2)
        crit_valor_final = crit_valor_base + self.mod_desarmado["crit_valor"]

        return {
            "dano":             max(1, dano_final),
            "crit_mult":        max(1, crit_mult_final),
            "crit_valor":       max(14, crit_valor_final),
            "dano_base":        dano_base,
            "dano_mod":         self.mod_desarmado["dano_bonus"],
            "crit_mult_base":   crit_mult_base,
            "crit_mult_mod":    self.mod_desarmado["crit_mult"],
            "crit_valor_base":  crit_valor_base,
            "crit_valor_mod":   self.mod_desarmado["crit_valor"],
            "prof_luta":        prof_luta,
        }

    @classmethod
    def from_dict(cls, data):
        personagem = cls(nome=data.get("nome"), Nivel=data.get("Nivel"), Forca=data.get("Forca"), Agilidade=data.get("Agilidade"), Vigor=data.get("Vigor"), Inteligencia=data.get("Inteligencia"), Presenca=data.get("Presenca"), Tatica=data.get("Tatica"), Poder=data.get("Poder"), proficiencias_base=None, recalcular=False)

        personagem.XPAtual = data.get("XPAtual", 0)
        personagem.XPlvlUp = data.get("XPlvlUp", personagem.XPlvlUp)
        personagem.VidaMax = data.get("VidaMax", personagem.VidaMax)
        personagem.VidaAtual = data.get("VidaAtual", personagem.VidaMax)
        personagem.EnergiaMax = data.get("EnergiaMax", personagem.EnergiaMax)
        personagem.EnergiaAtual = data.get("EnergiaAtual", personagem.EnergiaMax)
        personagem.ManaMax = data.get("ManaMax", personagem.ManaMax)
        personagem.ManaAtual = data.get("ManaAtual", personagem.ManaMax)
        personagem.Bloqueio = data.get("Bloqueio", personagem.Bloqueio)
        personagem.Esquiva = data.get("Esquiva", personagem.Esquiva)
        personagem.Percepcao = data.get("Percepcao", personagem.Percepcao)
        personagem.Movimento = data.get("Movimento", personagem.Movimento)
        personagem.Disparada = data.get("Disparada", personagem.Disparada)
        personagem.CargaMax = data.get("CargaMax", personagem.CargaMax)
        personagem.CargaAtual = data.get("CargaAtual", personagem.CargaAtual)

        personagem.mod_testes.update(data.get("mod_testes", {}))
        personagem.mod_efeitos.update(data.get("mod_efeitos", {}))

        # NOVO: Carregar dados unificados de resistências
        personagem.resistencias_base.update(data.get("resistencias_base", {}))
        personagem.resistencias_mod.update(data.get("resistencias_mod", {}))
        personagem.imunidades_mod = set(data.get("imunidades_mod", []))

        personagem.mod_temporarios = data.get("mod_temporarios", [])
        personagem.mod_efeitos_ativos = data.get("mod_efeitos_ativos", [])

        inventario_data = data.get("inventario", [])
        personagem.inventario = Inventario()

        for entrada in inventario_data:
            item_obj = deserializar_item(entrada.get("item"))
            qtd = entrada.get("quantidade", 1)
            if item_obj:
                personagem.inventario.adicionar_item_objeto(item_obj, qtd)

        for regiao, item_data in data.get("equipamentos", {}).items():
            if regiao in personagem.regioes_corpo:
                if isinstance(item_data, dict):
                    personagem.regioes_corpo[regiao] = deserializar_item(item_data)
                else:
                    personagem.regioes_corpo[regiao] = item_data
        
        for nome_slot, item_data in data.get("slots", {}).items():
            if nome_slot in personagem.slots and item_data:
                if isinstance(item_data, dict):
                    personagem.slots[nome_slot].item = deserializar_item(item_data)
                else:
                    personagem.slots[nome_slot].item = item_data

        if "proficiencias" in data: 
            personagem.proficiencias = SistemaDeProficiencias.from_dict(data["proficiencias"])

        # PODERES
        if "poderes" in data:
            poderes_data = data["poderes"]
            # Se já é dict com as chaves corretas, passa direto
            if isinstance(poderes_data, dict):
                personagem.poderes = GerenciadorDePoderes.from_dict(poderes_data, personagem=personagem)
            else:
                # Compatibilidade: lista legada só com poderes antigos
                personagem.poderes = GerenciadorDePoderes.from_dict({"poderes": poderes_data, "poderes_ofensivos": []}, personagem=personagem)

        # HABILIDADES
        if "habilidades" in data:
            habilidades_data = data["habilidades"]
            if isinstance(habilidades_data, dict):
                personagem.habilidades = GerenciadorDeHabilidades.from_dict(habilidades_data, personagem=personagem)
            else:
                personagem.habilidades = GerenciadorDeHabilidades.from_dict({"habilidades": habilidades_data, "habilidades_ofensivas": []}, personagem=personagem)

        if "buffs_debuffs" in data: 
            personagem.buffs_debuffs = GerenciadorDeBuffsDebuffs.from_dict(data["buffs_debuffs"], personagem=personagem)

        personagem.recalcularAtributos()
        return personagem

    def to_dict(self):
        return {
            "nome": self.nome,
            "Nivel": self.Nivel,
            "XPAtual": self.XPAtual,
            "XPlvlUp": self.XPlvlUp,
            "Forca": self.Forca,
            "Agilidade": self.Agilidade,
            "Vigor": self.Vigor,
            "Inteligencia": self.Inteligencia,
            "Presenca": self.Presenca,
            "Tatica": self.Tatica,
            "Poder": self.Poder,
            "VidaMax": self.VidaMax,
            "VidaAtual": self.VidaAtual,
            "EnergiaMax": self.EnergiaMax,
            "EnergiaAtual": self.EnergiaAtual,
            "ManaMax": self.ManaMax,
            "ManaAtual": self.ManaAtual,
            "Bloqueio": self.Bloqueio,
            "Esquiva": self.Esquiva,
            "Percepcao": self.Percepcao,
            "Movimento": self.Movimento,
            "Disparada": self.Disparada,
            "CargaMax": self.CargaMax,
            "CargaAtual": self.CargaAtual,
            "mod_testes": self.mod_testes,
            "mod_efeitos": self.mod_efeitos,
            # NOVO: Dados unificados
            "resistencias_base": self.resistencias_base,
            "resistencias_mod": self.resistencias_mod,
            "imunidades_mod": list(self.imunidades_mod),
            "mod_temporarios": self.mod_temporarios,
            "mod_efeitos_ativos": self.mod_efeitos_ativos,
            "equipamentos": {regiao: serializar_item(item) for regiao, item in self.regioes_corpo.items()},
            "slots": {nome: serializar_item(slot.item) if slot.item else None for nome, slot in self.slots.items()},
            "inventario": [{"item": serializar_item(entrada["item"]), "quantidade": entrada["quantidade"]} for entrada in self.inventario.itens],
            "proficiencias": self.proficiencias.to_dict(),
            "poderes": self.poderes.to_dict(),
            "habilidades": self.habilidades.to_dict(),
            "buffs_debuffs": self.buffs_debuffs.to_dict()
        }

# Slots de equipamento #
class SlotEquipamento:
    def __init__(self, nome, tipo, aceita=None, requer_maos=0, saque_rapido=False):
        self.nome = nome
        self.tipo = tipo  # "mao", "prontidao", "costas", etc
        self.aceita = aceita or ["qualquer"]  # categorias aceitas
        self.requer_maos = requer_maos
        self.saque_rapido = saque_rapido
        self.item = None

    def esta_livre(self):
        return self.item is None

    def pode_receber(self,item):
        if self.tipo=="mao": return isinstance(item,(Ranged,Melee))
        if self.tipo=="protecao": return isinstance(item,Protecao)
        if self.tipo=="suporte":
            classe=item.__class__.__name__
            if self.aceita!=["qualquer"] and classe not in self.aceita: return False
            if self.requer_maos and getattr(item,"maos",1)!=self.requer_maos: return False
            return True
        return False
# Slots de equipamento #
# Classe poder #
class Poder:
    def __init__(self, nome, tipo, custo=0, tags=None, valor=0,
                 por_turno=False, duracao=None, descricao="",
                 # Novos campos para ativos
                 custo_mana=0, dano=None, efeitos_ativos=None, ignora_resistencias=False):
        self.nome      = nome
        self.tipo      = tipo        # "ativo" ou "passivo"
        self.custo     = custo       # custo em Energia
        self.custo_mana = custo_mana
        self.tags      = tags or []
        self.valor     = valor
        self.por_turno = por_turno
        self.duracao   = duracao
        self.descricao = descricao
        # Campos de ativo (dano + efeitos com chance)
        self.dano               = dano or []           # [{"tipo": "incendiário", "valor": 20}]
        self.efeitos_ativos     = efeitos_ativos or [] # [{"nome": "Queimando", "chance": 80, "duracao": 3}]
        self.ignora_resistencias = ignora_resistencias

    def aplicar_passivo(self, personagem):
        if self.tipo != "passivo": return
        tags = self.tags if isinstance(self.tags, list) else [self.tags]
        valores = self.valor if isinstance(self.valor, list) else [self.valor] * len(tags)
        for tag, val in zip(tags, valores):
            personagem.aplicar_modificador_generico(tags=[tag], valor=val)

    def remover_passivo(self, personagem):
        if self.tipo != "passivo": return
        tags = self.tags if isinstance(self.tags, list) else [self.tags]
        valores = self.valor if isinstance(self.valor, list) else [self.valor] * len(tags)
        for tag, val in zip(tags, valores):
            personagem.remover_modificador_generico([tag], val)

    def usar(self, conjurador, alvo=None):
        if self.tipo == "passivo": return False
        if conjurador.EnergiaAtual < self.custo: return False
        if conjurador.ManaAtual < self.custo_mana: return False
        conjurador.ModificarEnergia(-self.custo)
        conjurador.ModificarMana(-self.custo_mana)

        alvo_real = alvo or conjurador

        # Aplica danos
        for entrada_dano in self.dano:
            tipo_dano = entrada_dano.get("tipo", "contundente")
            valor_dano = entrada_dano.get("valor", 0)
            if self.ignora_resistencias:
                alvo_real.ModificarVida(-valor_dano)
            else:
                dano_final = alvo_real.calcular_dano_recebido(valor_dano, tipo_dano)
                alvo_real.ModificarVida(-dano_final)

        # Aplica efeitos com chance (referencia buffs/debuffs do dicionário)
        for efeito_ref in self.efeitos_ativos:
            alvo_real.aplicar_efeito_com_chance(efeito_ref, alvo=alvo_real, fonte="poder")

        return True

    def to_dict(self):
        return {
            "nome": self.nome, "tipo": self.tipo,
            "custo": self.custo, "custo_mana": self.custo_mana,
            "tags": self.tags, "valor": self.valor,
            "por_turno": self.por_turno, "duracao": self.duracao,
            "descricao": self.descricao,
            "dano": self.dano, "efeitos_ativos": self.efeitos_ativos,
            "ignora_resistencias": self.ignora_resistencias,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            nome=data.get("nome",""), tipo=data.get("tipo","ativo"),
            custo=data.get("custo",0), custo_mana=data.get("custo_mana",0),
            tags=data.get("tags",[]), valor=data.get("valor",0),
            por_turno=data.get("por_turno",False), duracao=data.get("duracao",None),
            descricao=data.get("descricao",""),
            dano=data.get("dano",[]), efeitos_ativos=data.get("efeitos_ativos",[]),
            ignora_resistencias=data.get("ignora_resistencias",False),
        )

class PoderOfensivo:
    """
    Poder ofensivo simplificado.
    - Dano por tipo (lista de {tipo, valor})
    - Custo de energia e/ou mana
    - Efeitos com chance e duração
    - Pode atingir múltiplos alvos
    - Sem rolagem de acerto, sem distância, sem cobertura
    """
    def __init__(self,
                 nome: str,
                 descricao: str = "",
                 custo_energia: int = 0,
                 custo_mana: int = 0,
                 dano: List[Dict] = None,        # [{"tipo": "incendiário", "valor": 20}, ...]
                 efeitos: List[Dict] = None,     # [{"nome": "...", "chance": 80, "duracao": 3}, ...]
                 ignora_resistencias: bool = False,
                 ):
        self.nome = nome
        self.descricao = descricao
        self.custo_energia = custo_energia
        self.custo_mana = custo_mana
        self.dano = dano or []
        self.efeitos = efeitos or []
        self.ignora_resistencias = ignora_resistencias

    def pode_usar(self, personagem: "Personagem") -> Tuple[bool, str]:
        if personagem.EnergiaAtual < self.custo_energia:
            return False, f"Energia insuficiente (precisa {self.custo_energia}, tem {personagem.EnergiaAtual})"
        if personagem.ManaAtual < self.custo_mana:
            return False, f"Mana insuficiente (precisa {self.custo_mana}, tem {personagem.ManaAtual})"
        return True, ""

    def consumir_recursos(self, personagem: "Personagem"):
        personagem.ModificarEnergia(-self.custo_energia)
        personagem.ModificarMana(-self.custo_mana)

    def to_dict(self):
        return {
            "__class__": self.__class__.__name__,
            "nome": self.nome, "descricao": self.descricao,
            "custo_energia": self.custo_energia, "custo_mana": self.custo_mana,
            "dano": self.dano, "efeitos": self.efeitos,
            "ignora_resistencias": self.ignora_resistencias,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            nome=data.get("nome",""), descricao=data.get("descricao",""),
            custo_energia=data.get("custo_energia",0), custo_mana=data.get("custo_mana",0),
            dano=data.get("dano",[]), efeitos=data.get("efeitos",[]),
            ignora_resistencias=data.get("ignora_resistencias",False),
        )

    def __str__(self):
        custos = []
        if self.custo_energia: custos.append(f"{self.custo_energia} Energia")
        if self.custo_mana:    custos.append(f"{self.custo_mana} Mana")
        custo_txt  = " | " + ", ".join(custos) if custos else ""
        danos_txt  = ", ".join(f"{d['valor']}({d['tipo'][:3]})" for d in self.dano) or "sem dano"
        return f"[✨] {self.nome}: {danos_txt}{custo_txt}"

class GerenciadorDePoderes:
    def __init__(self, personagem=None):
        self.poderes            = []      # Poder antigos (modificadores/buffs)
        self.poderes_ofensivos  = []      # PoderOfensivo novos (ataques)
        self.personagem         = personagem

    # ─────────────────────────────────────────────────────────────────────────
    # PODERES ANTIGOS (Poder - modificadores/buffs)
    # ─────────────────────────────────────────────────────────────────────────

    def adicionar_poder(self, nome, tipo, custo=0, tags=None, valor=0,
                        por_turno=False, duracao=None, descricao=""):
        """Adiciona poder antigo (Poder)"""
        poder = Poder(nome, tipo, custo, tags, valor, por_turno, duracao, descricao)
        self.poderes.append(poder)
        if tipo == "passivo" and self.personagem:
            poder.aplicar_passivo(self.personagem)
        return poder

    def adicionar_poder_objeto(self, poder):
        """Adiciona objeto Poder"""
        # Verifica se é Poder ou PoderOfensivo
        if isinstance(poder, PoderOfensivo):
            return self.adicionar_poder_ofensivo(poder)
        
        self.poderes.append(poder)
        if poder.tipo == "passivo" and self.personagem:
            poder.aplicar_passivo(self.personagem)
        return poder

    def remover_poder(self, nome):
        """Remove poder por nome (antigo)"""
        for p in self.poderes:
            if p.nome == nome and p.tipo == "passivo" and self.personagem:
                p.remover_passivo(self.personagem)
        self.poderes = [p for p in self.poderes if p.nome != nome]

    # ─────────────────────────────────────────────────────────────────────────
    # PODERES OFENSIVOS (PoderOfensivo - ataques diretos)
    # ─────────────────────────────────────────────────────────────────────────

    def adicionar_poder_ofensivo(self, poder):
        """Adiciona um poder ofensivo (PoderOfensivo)"""
        if not isinstance(poder, PoderOfensivo):
            raise TypeError(f"Esperado PoderOfensivo, recebido {type(poder).__name__}")
        self.poderes_ofensivos.append(poder)
        return poder

    def remover_poder_ofensivo(self, nome):
        """Remove poder ofensivo por nome"""
        self.poderes_ofensivos = [p for p in self.poderes_ofensivos if p.nome != nome]

    def obter_poder_ofensivo(self, nome):
        """Retorna poder ofensivo por nome"""
        return next((p for p in self.poderes_ofensivos if p.nome == nome), None)

    def executar_poder_ofensivo(self, nome_poder, alvo=None, 
                                alvos_distancias=None, distancia=0, 
                                regiao="aleatoria"):
        """
        Executa um poder ofensivo
        
        O personagem (atacante) vem do self.personagem
        """
        if not self.personagem:
            return {"sucesso": False, "erro": "Nenhum personagem associado"}
        
        poder = self.obter_poder_ofensivo(nome_poder)
        if not poder:
            return {
                "sucesso": False, 
                "erro": f"Poder ofensivo '{nome_poder}' não encontrado"
            }
        
        return poder.usar(
            atacante=self.personagem,
            alvo=alvo,
            alvos_distancias=alvos_distancias,
            distancia=distancia,
            regiao=regiao
        )

    # ─────────────────────────────────────────────────────────────────────────
    # LISTAGEM E BUSCA
    # ─────────────────────────────────────────────────────────────────────────

    def listar_poderes(self):
        """Lista todos os poderes ANTIGOS"""
        return self.poderes.copy()

    def listar_ativos(self):
        """Lista poderes ANTIGOS ativos"""
        return [p for p in self.poderes if p.tipo == "ativo"]

    def listar_passivos(self):
        """Lista poderes ANTIGOS passivos"""
        return [p for p in self.poderes if p.tipo == "passivo"]

    def listar_poderes_ofensivos(self):
        """Lista todos os poderes OFENSIVOS"""
        return self.poderes_ofensivos.copy()

    def listar_tudo(self):
        """Lista todos os poderes (antigos + ofensivos)"""
        return {
            "poderes": self.poderes,
            "poderes_ofensivos": self.poderes_ofensivos
        }

    def listar_disponiveis(self):
        """
        Lista poderes ofensivos disponíveis agora 
        (que o personagem tem recursos para usar)
        """
        if not self.personagem:
            return []
        
        disponiveis = []
        for poder in self.poderes_ofensivos:
            pode_usar, _ = poder.pode_usar(self.personagem)
            if pode_usar:
                disponiveis.append(poder)
        
        return disponiveis

    # ─────────────────────────────────────────────────────────────────────────
    # SERIALIZAÇÃO
    # ─────────────────────────────────────────────────────────────────────────

    def to_dict(self):
        """Serializa AMBOS os tipos de poder"""
        return {
            "poderes": [p.to_dict() for p in self.poderes],
            "poderes_ofensivos": [p.to_dict() for p in self.poderes_ofensivos]
        }

    @classmethod
    def from_dict(cls, data, personagem=None):
        """Desserializa AMBOS os tipos de poder"""
        ger = cls(personagem)
        
        # ─── Carregar poderes antigos ───
        for p_data in data.get("poderes", []):
            poder = Poder.from_dict(p_data)
            ger.poderes.append(poder)
            if poder.tipo == "passivo" and personagem:
                poder.aplicar_passivo(personagem)
        
        # ─── Carregar poderes ofensivos ───
        for po_data in data.get("poderes_ofensivos", []):
            poder_ofensivo = PoderOfensivo.from_dict(po_data)
            ger.poderes_ofensivos.append(poder_ofensivo)
        
        return ger

    # ─────────────────────────────────────────────────────────────────────────
    # VISUALIZAÇÃO E EXIBIÇÃO
    # ─────────────────────────────────────────────────────────────────────────

    def listar_todos_poderes(self):
        """Lista todos os poderes: antigos e ofensivos"""
        resultado = {
            "poderes_antigos": self.poderes.copy(),
            "poderes_ofensivos": self.poderes_ofensivos.copy(),
            "total": len(self.poderes) + len(self.poderes_ofensivos)
        }
        return resultado

    def exibir_poderes_formatado(self):
        """Exibe todos os poderes em formato tabular"""
        print("\n" + "="*80)
        print("PODERES DO PERSONAGEM")
        print("="*80)
        
        # PODERES ANTIGOS
        if self.poderes:
            print("\n🔮 PODERES ANTIGOS (Modificadores):")
            print("-" * 80)
            for poder in self.poderes:
                tipo_symbol = "⚡" if poder.tipo == "ativo" else "🛡️"
                custo_text = f"Custo: {poder.custo} En" if poder.tipo == "ativo" else "Passivo"
                print(f"  {tipo_symbol} {poder.nome:<30} | {custo_text:<20} | Tags: {poder.tags}")
        else:
            print("\n🔮 PODERES ANTIGOS: Nenhum")
        
        # PODERES OFENSIVOS
        if self.poderes_ofensivos:
            print("\n⚔️ PODERES OFENSIVOS (Ataques):")
            print("-" * 80)
            for poder in self.poderes_ofensivos:
                tipo_ataque = poder.tipo_ataque.upper()
                custos = []
                if poder.custo_energia: custos.append(f"{poder.custo_energia} En")
                if poder.custo_mana: custos.append(f"{poder.custo_mana} Ma")
                custo_txt = " + ".join(custos) if custos else "Grátis"
                
                danos_txt = ", ".join([f"{d['valor']}({d['tipo'][:3]})" for d in poder.dano])
                
                print(f"  ⚡ {poder.nome:<25} | {tipo_ataque:<6} | Dano: {danos_txt:<25} | {custo_txt}")
        else:
            print("\n⚔️ PODERES OFENSIVOS: Nenhum")
        
        print("\n" + "="*80 + "\n")

    def exibir_poder_detalhado(self, nome_poder):
        """Exibe detalhes completos de um poder específico"""
        # Procura em antigos
        poder_antigo = next((p for p in self.poderes if p.nome == nome_poder), None)
        if poder_antigo:
            return self._exibir_poder_antigo_detalhado(poder_antigo)
        
        # Procura em ofensivos
        poder_ofensivo = self.obter_poder_ofensivo(nome_poder)
        if poder_ofensivo:
            return self._exibir_poder_ofensivo_detalhado(poder_ofensivo)
        
        print(f"[ERRO] Poder '{nome_poder}' não encontrado")
        return None

    def _exibir_poder_antigo_detalhado(self, poder):
        """Exibe detalhes de um poder antigo"""
        print("\n" + "="*60)
        print(f"PODER ANTIGO: {poder.nome}")
        print("="*60)
        print(f"Tipo:        {poder.tipo}")
        print(f"Descrição:   {poder.descricao}")
        print(f"Tags:        {', '.join(poder.tags)}")
        print(f"Valor:       {poder.valor}")
        print(f"Por Turno:   {'Sim' if poder.por_turno else 'Não'}")
        print(f"Duração:     {poder.duracao if poder.duracao else 'Permanente/Instantâneo'}")
        if poder.tipo == "ativo":
            print(f"Custo:       {poder.custo} Energia")
        print("="*60 + "\n")
        return poder

    def _exibir_poder_ofensivo_detalhado(self, poder):
        """Exibe detalhes de um poder ofensivo"""
        print("\n" + "="*80)
        print(f"PODER OFENSIVO: {poder.nome}")
        print("="*80)
        print(f"Tipo de Ataque:    {poder.tipo_ataque.upper()}")
        print(f"Descrição:         {poder.descricao}")
        
        # Custos
        print("\n📊 CUSTOS:")
        if poder.custo_energia or poder.custo_mana:
            if poder.custo_energia: print(f"  Energia: {poder.custo_energia}")
            if poder.custo_mana: print(f"  Mana:    {poder.custo_mana}")
        else:
            print("  Grátis")
        
        # Dano
        print("\n⚡ DANO:")
        if poder.dano:
            for entrada_dano in poder.dano:
                tipo = entrada_dano.get("tipo", "generico")
                valor = entrada_dano.get("valor", 0)
                print(f"  {valor} {tipo}")
        else:
            print("  Nenhum dano direto")
        
        # Multiplicador
        if poder.multiplicador_dano != 1.0:
            print(f"  Multiplicador: x{poder.multiplicador_dano}")
            if poder.aplica_a_arma_equipada:
                print(f"  Amplifica arma equipada: SIM")
        
        # Ignora resistências
        if poder.ignora_resistencias:
            print("  Ignora Resistências: SIM")
        
        # Área/Alcance
        if poder.tipo_ataque == "area":
            print(f"\n🎯 ÁREA:")
            print(f"  Raio: {poder.raio}m")
            print(f"  Raio Letal: {poder.raio_letal}m")
            print(f"  Falloff: {poder.falloff}")
            if poder.num_alvos_maximo:
                print(f"  Máximo de Alvos: {poder.num_alvos_maximo}")
        
        elif poder.tipo_ataque == "ranged":
            print(f"\n🎯 ALCANCE:")
            print(f"  Mínimo: {poder.alcance_min}m")
            print(f"  Máximo: {poder.alcance_max}m")
            print(f"  Falloff: {poder.falloff}")
        
        # Efeitos
        if poder.efeitos:
            print(f"\n💫 EFEITOS:")
            for efeito in poder.efeitos:
                nome = efeito.get("nome", "Efeito")
                chance = efeito.get("chance", 100)
                duracao = efeito.get("duracao", 1)
                print(f"  - {nome} ({chance}% de chance, {duracao}t)")
        
        print("="*80 + "\n")
        return poder

    def listar_poderes_por_tipo(self, tipo_ataque=None):
        """Lista poderes ofensivos filtrados por tipo de ataque"""
        if not tipo_ataque:
            return self.poderes_ofensivos.copy()
        
        tipo_ataque = tipo_ataque.lower()
        return [p for p in self.poderes_ofensivos if p.tipo_ataque.lower() == tipo_ataque]

    def exibir_resumo_combate(self):
        """Exibe resumo de todos os ataques disponíveis em combate"""
        print("\n" + "="*80)
        print("RESUMO DE COMBATE - ATAQUES DISPONÍVEIS")
        print("="*80)
        
        if not self.personagem:
            print("[ERRO] Nenhum personagem associado")
            return
        
        recursos = f"Energia: {self.personagem.EnergiaAtual}/{self.personagem.EnergiaMax} | Mana: {self.personagem.ManaAtual}/{self.personagem.ManaMax}"
        print(f"\n{recursos}\n")
        
        # Poderes ofensivos disponíveis
        disponiveis = self.listar_disponiveis()
        
        if disponiveis:
            print("✅ ATAQUES DISPONÍVEIS:")
            print("-" * 80)
            for idx, poder in enumerate(disponiveis, 1):
                tipo_ataque = poder.tipo_ataque.upper()
                custos = []
                if poder.custo_energia: custos.append(f"{poder.custo_energia}En")
                if poder.custo_mana: custos.append(f"{poder.custo_mana}Ma")
                custo_txt = "+".join(custos) if custos else "Grátis"
                
                print(f"  [{idx}] {poder.nome:<25} ({tipo_ataque:<6}) | {custo_txt}")
        else:
            print("❌ NENHUM ATAQUE DISPONÍVEL (recursos insuficientes)")
        
        # Poderes não disponíveis
        nao_disponiveis = [p for p in self.poderes_ofensivos if p not in disponiveis]
        
        if nao_disponiveis:
            print("\n⚠️ ATAQUES INDISPONÍVEIS (recursos insuficientes):")
            print("-" * 80)
            for poder in nao_disponiveis:
                pode_usar, erro = poder.pode_usar(self.personagem)
                print(f"  ❌ {poder.nome:<25} | {erro}")
        
        print("\n" + "="*80 + "\n")
# Classe poder #
# Classe habilidade #
class Habilidade:
    def __init__(self, nome, tipo, custo=0, tags=None, valor=0,
                 por_turno=False, duracao=None, descricao="",
                 # Novos campos para ativos
                 custo_mana=0, dano=None, efeitos_ativos=None, ignora_resistencias=False):
        self.nome      = nome
        self.tipo      = tipo        # "ativo" ou "passivo"
        self.custo     = custo       # custo em Energia
        self.custo_mana = custo_mana
        self.tags      = tags or []
        self.valor     = valor
        self.por_turno = por_turno
        self.duracao   = duracao
        self.descricao = descricao
        # Campos de ativo (dano + efeitos com chance)
        self.dano               = dano or []           # [{"tipo": "incendiário", "valor": 20}]
        self.efeitos_ativos     = efeitos_ativos or [] # [{"nome": "Queimando", "chance": 80, "duracao": 3}]
        self.ignora_resistencias = ignora_resistencias

    def aplicar_passivo(self, personagem):
        if self.tipo != "passivo": return
        tags = self.tags if isinstance(self.tags, list) else [self.tags]
        valores = self.valor if isinstance(self.valor, list) else [self.valor] * len(tags)
        for tag, val in zip(tags, valores):
            personagem.aplicar_modificador_generico(tags=[tag], valor=val)

    def remover_passivo(self, personagem):
        if self.tipo != "passivo": return
        tags = self.tags if isinstance(self.tags, list) else [self.tags]
        valores = self.valor if isinstance(self.valor, list) else [self.valor] * len(tags)
        for tag, val in zip(tags, valores):
            personagem.remover_modificador_generico([tag], val)

    def usar(self, conjurador, alvo=None):
        if self.tipo == "passivo": return False
        if conjurador.EnergiaAtual < self.custo: return False
        if conjurador.ManaAtual < self.custo_mana: return False
        conjurador.ModificarEnergia(-self.custo)
        conjurador.ModificarMana(-self.custo_mana)

        alvo_real = alvo or conjurador

        # Aplica danos
        for entrada_dano in self.dano:
            tipo_dano = entrada_dano.get("tipo", "contundente")
            valor_dano = entrada_dano.get("valor", 0)
            if self.ignora_resistencias:
                alvo_real.ModificarVida(-valor_dano)
            else:
                dano_final = alvo_real.calcular_dano_recebido(valor_dano, tipo_dano)
                alvo_real.ModificarVida(-dano_final)

        # Aplica efeitos com chance (referencia buffs/debuffs do dicionário)
        for efeito_ref in self.efeitos_ativos:
            alvo_real.aplicar_efeito_com_chance(efeito_ref, alvo=alvo_real, fonte="poder")

        return True

    def to_dict(self):
        return {
            "nome": self.nome, "tipo": self.tipo,
            "custo": self.custo, "custo_mana": self.custo_mana,
            "tags": self.tags, "valor": self.valor,
            "por_turno": self.por_turno, "duracao": self.duracao,
            "descricao": self.descricao,
            "dano": self.dano, "efeitos_ativos": self.efeitos_ativos,
            "ignora_resistencias": self.ignora_resistencias,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            nome=data.get("nome",""), tipo=data.get("tipo","ativo"),
            custo=data.get("custo",0), custo_mana=data.get("custo_mana",0),
            tags=data.get("tags",[]), valor=data.get("valor",0),
            por_turno=data.get("por_turno",False), duracao=data.get("duracao",None),
            descricao=data.get("descricao",""),
            dano=data.get("dano",[]), efeitos_ativos=data.get("efeitos_ativos",[]),
            ignora_resistencias=data.get("ignora_resistencias",False),
        )

class HabilidadeOfensiva:
    """
    Habilidade customizável que pode causar dano de múltiplas formas:
    - Múltiplos tipos de dano simultâneos
    - Efeitos com chances individuais
    - Custos mistos (energia + mana)
    - Multiplicadores de dano (em vez de dano base)
    - Alcance, raio, falloff customizáveis
    
    Usa o mesmo sistema que PoderOfensivo, mas é uma Habilidade
    """    
    def __init__(self,
                 nome: str,
                 descricao: str = "",
                 custo_energia: int = 0,
                 custo_mana: int = 0,
                 dano: List[Dict] = None,        # [{"tipo": "incendiário", "valor": 20}, ...]
                 efeitos: List[Dict] = None,     # [{"nome": "...", "chance": 80, "duracao": 3}, ...]
                 ignora_resistencias: bool = False,
                 ):
        self.nome = nome
        self.descricao = descricao
        self.custo_energia = custo_energia
        self.custo_mana = custo_mana
        self.dano = dano or []
        self.efeitos = efeitos or []
        self.ignora_resistencias = ignora_resistencias

    def pode_usar(self, personagem: "Personagem") -> Tuple[bool, str]:
        if personagem.EnergiaAtual < self.custo_energia:
            return False, f"Energia insuficiente (precisa {self.custo_energia}, tem {personagem.EnergiaAtual})"
        if personagem.ManaAtual < self.custo_mana:
            return False, f"Mana insuficiente (precisa {self.custo_mana}, tem {personagem.ManaAtual})"
        return True, ""

    def consumir_recursos(self, personagem: "Personagem"):
        personagem.ModificarEnergia(-self.custo_energia)
        personagem.ModificarMana(-self.custo_mana)

    def to_dict(self):
        return {
            "__class__": self.__class__.__name__,
            "nome": self.nome, "descricao": self.descricao,
            "custo_energia": self.custo_energia, "custo_mana": self.custo_mana,
            "dano": self.dano, "efeitos": self.efeitos,
            "ignora_resistencias": self.ignora_resistencias,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            nome=data.get("nome",""), descricao=data.get("descricao",""),
            custo_energia=data.get("custo_energia",0), custo_mana=data.get("custo_mana",0),
            dano=data.get("dano",[]), efeitos=data.get("efeitos",[]),
            ignora_resistencias=data.get("ignora_resistencias",False),
        )
    
    def __str__(self):
        custos = []
        if self.custo_energia: custos.append(f"{self.custo_energia} Energia")
        if self.custo_mana:    custos.append(f"{self.custo_mana} Mana")
        custo_txt = " | " + ", ".join(custos) if custos else ""
        danos_txt = ", ".join(f"{d['valor']}({d['tipo'][:3]})" for d in self.dano) or "sem dano"
        return f"[⚔️] {self.nome}: {danos_txt}{custo_txt}"

class GerenciadorDeHabilidades:
    def __init__(self, personagem=None):
        self.habilidades            = []      # Habilidade antigos (modificadores)
        self.habilidades_ofensivas  = []      # HabilidadeOfensiva novos (ataques)
        self.personagem             = personagem

    # ─────────────────────────────────────────────────────────────────────────
    # HABILIDADES ANTIGOS (Habilidade - modificadores/buffs)
    # ─────────────────────────────────────────────────────────────────────────

    def adicionar_habilidade(self, nome, tipo, custo=0, tags=None, valor=0,
                             por_turno=False, duracao=None, descricao=""):
        """Adiciona habilidade antigo (Habilidade)"""
        habilidade = Habilidade(nome, tipo, custo, tags, valor,
                                por_turno, duracao, descricao)
        self.habilidades.append(habilidade)
        if tipo == "passivo" and self.personagem:
            habilidade.aplicar_passivo(self.personagem)
        return habilidade

    def adicionar_habilidade_objeto(self, habilidade):
        """Adiciona objeto Habilidade"""
        # Verifica se é Habilidade ou HabilidadeOfensiva
        if isinstance(habilidade, HabilidadeOfensiva):
            return self.adicionar_habilidade_ofensiva(habilidade)
        
        self.habilidades.append(habilidade)
        if habilidade.tipo == "passivo" and self.personagem:
            habilidade.aplicar_passivo(self.personagem)
        return habilidade

    def remover_habilidade(self, nome):
        """Remove habilidade por nome (antigo)"""
        for h in self.habilidades:
            if h.nome == nome and h.tipo == "passivo" and self.personagem:
                h.remover_passivo(self.personagem)
        self.habilidades = [h for h in self.habilidades if h.nome != nome]

    # ─────────────────────────────────────────────────────────────────────────
    # HABILIDADES OFENSIVOS (HabilidadeOfensiva - ataques diretos)
    # ─────────────────────────────────────────────────────────────────────────

    def adicionar_habilidade_ofensiva(self, habilidade):
        """Adiciona uma habilidade ofensiva (HabilidadeOfensiva)"""
        if not isinstance(habilidade, HabilidadeOfensiva):
            raise TypeError(f"Esperado HabilidadeOfensiva, recebido {type(habilidade).__name__}")
        self.habilidades_ofensivas.append(habilidade)
        return habilidade

    def remover_habilidade_ofensiva(self, nome):
        """Remove habilidade ofensiva por nome"""
        self.habilidades_ofensivas = [h for h in self.habilidades_ofensivas if h.nome != nome]

    def obter_habilidade_ofensiva(self, nome):
        """Retorna habilidade ofensiva por nome"""
        return next((h for h in self.habilidades_ofensivas if h.nome == nome), None)

    def executar_habilidade_ofensiva(self, nome_habilidade, alvo=None, 
                                     alvos_distancias=None, distancia=0, 
                                     regiao="aleatoria"):
        """
        Executa uma habilidade ofensiva
        
        O personagem (usuário) vem do self.personagem
        """
        if not self.personagem:
            return {"sucesso": False, "erro": "Nenhum personagem associado"}
        
        habilidade = self.obter_habilidade_ofensiva(nome_habilidade)
        if not habilidade:
            return {
                "sucesso": False, 
                "erro": f"Habilidade ofensiva '{nome_habilidade}' não encontrada"
            }
        
        return habilidade.usar(
            usuario=self.personagem,
            alvo=alvo,
            alvos_distancias=alvos_distancias,
            distancia=distancia,
            regiao=regiao
        )

    # ─────────────────────────────────────────────────────────────────────────
    # LISTAGEM E BUSCA
    # ─────────────────────────────────────────────────────────────────────────

    def listar_habilidades(self):
        """Lista todas as habilidades ANTIGOS"""
        return self.habilidades.copy()

    def listar_ativas(self):
        """Lista habilidades ANTIGOS ativos"""
        return [h for h in self.habilidades if h.tipo == "ativo"]

    def listar_passivas(self):
        """Lista habilidades ANTIGOS passivos"""
        return [h for h in self.habilidades if h.tipo == "passivo"]

    def listar_habilidades_ofensivas(self):
        """Lista todas as habilidades OFENSIVAS"""
        return self.habilidades_ofensivas.copy()

    def listar_tudo(self):
        """Lista todas as habilidades (antigos + ofensivos)"""
        return {
            "habilidades": self.habilidades,
            "habilidades_ofensivas": self.habilidades_ofensivas
        }

    def listar_disponiveis(self):
        """
        Lista habilidades ofensivas disponíveis agora 
        (que o personagem tem recursos para usar)
        """
        if not self.personagem:
            return []
        
        disponiveis = []
        for habilidade in self.habilidades_ofensivas:
            pode_usar, _ = habilidade.pode_usar(self.personagem)
            if pode_usar:
                disponiveis.append(habilidade)
        
        return disponiveis

    # ─────────────────────────────────────────────────────────────────────────
    # SERIALIZAÇÃO
    # ─────────────────────────────────────────────────────────────────────────

    def to_dict(self):
        """Serializa AMBOS os tipos de habilidade"""
        return {
            "habilidades": [h.to_dict() for h in self.habilidades],
            "habilidades_ofensivas": [h.to_dict() for h in self.habilidades_ofensivas]
        }

    @classmethod
    def from_dict(cls, data, personagem=None):
        """Desserializa AMBOS os tipos de habilidade"""
        ger = cls(personagem)
        
        # ─── Carregar habilidades antigos ───
        for h_data in data.get("habilidades", []):
            habilidade = Habilidade.from_dict(h_data)
            ger.habilidades.append(habilidade)
            if habilidade.tipo == "passivo" and personagem:
                habilidade.aplicar_passivo(personagem)
        
        # ─── Carregar habilidades ofensivos ───
        for ho_data in data.get("habilidades_ofensivas", []):
            habilidade_ofensiva = HabilidadeOfensiva.from_dict(ho_data)
            ger.habilidades_ofensivas.append(habilidade_ofensiva)
        
        return ger

    # ─────────────────────────────────────────────────────────────────────────
    # VISUALIZAÇÃO E EXIBIÇÃO
    # ─────────────────────────────────────────────────────────────────────────

    def listar_todas_habilidades(self):
        """Lista todas as habilidades: antigos e ofensivos"""
        resultado = {
            "habilidades_antigos": self.habilidades.copy(),
            "habilidades_ofensivos": self.habilidades_ofensivas.copy(),
            "total": len(self.habilidades) + len(self.habilidades_ofensivas)
        }
        return resultado

    def exibir_habilidades_formatado(self):
        """Exibe todas as habilidades em formato tabular"""
        print("\n" + "="*80)
        print("HABILIDADES DO PERSONAGEM")
        print("="*80)
        
        # HABILIDADES ANTIGOS
        if self.habilidades:
            print("\n🛡️ HABILIDADES ANTIGOS (Modificadores):")
            print("-" * 80)
            for habilidade in self.habilidades:
                tipo_symbol = "⚡" if habilidade.tipo == "ativo" else "🛡️"
                custo_text = f"Custo: {habilidade.custo} En" if habilidade.tipo == "ativo" else "Passivo"
                print(f"  {tipo_symbol} {habilidade.nome:<30} | {custo_text:<20} | Tags: {habilidade.tags}")
        else:
            print("\n🛡️ HABILIDADES ANTIGOS: Nenhum")
        
        # HABILIDADES OFENSIVOS
        if self.habilidades_ofensivas:
            print("\n⚔️ HABILIDADES OFENSIVAS (Ataques):")
            print("-" * 80)
            for habilidade in self.habilidades_ofensivas:
                tipo_ataque = habilidade.tipo_ataque.upper()
                custos = []
                if habilidade.custo_energia: custos.append(f"{habilidade.custo_energia} En")
                if habilidade.custo_mana: custos.append(f"{habilidade.custo_mana} Ma")
                custo_txt = " + ".join(custos) if custos else "Grátis"
                
                danos_txt = ", ".join([f"{d['valor']}({d['tipo'][:3]})" for d in habilidade.dano])
                
                print(f"  ⚡ {habilidade.nome:<25} | {tipo_ataque:<6} | Dano: {danos_txt:<25} | {custo_txt}")
        else:
            print("\n⚔️ HABILIDADES OFENSIVAS: Nenhum")
        
        print("\n" + "="*80 + "\n")

    def exibir_habilidade_detalhada(self, nome_habilidade):
        """Exibe detalhes completos de uma habilidade específica"""
        # Procura em antigos
        habilidade_antigo = next((h for h in self.habilidades if h.nome == nome_habilidade), None)
        if habilidade_antigo:
            return self._exibir_habilidade_antigo_detalhado(habilidade_antigo)
        
        # Procura em ofensivos
        habilidade_ofensivo = self.obter_habilidade_ofensiva(nome_habilidade)
        if habilidade_ofensivo:
            return self._exibir_habilidade_ofensivo_detalhado(habilidade_ofensivo)
        
        print(f"[ERRO] Habilidade '{nome_habilidade}' não encontrada")
        return None

    def _exibir_habilidade_antigo_detalhado(self, habilidade):
        """Exibe detalhes de uma habilidade antigo"""
        print("\n" + "="*60)
        print(f"HABILIDADE ANTIGO: {habilidade.nome}")
        print("="*60)
        print(f"Tipo:        {habilidade.tipo}")
        print(f"Descrição:   {habilidade.descricao}")
        print(f"Tags:        {', '.join(habilidade.tags)}")
        print(f"Valor:       {habilidade.valor}")
        print(f"Por Turno:   {'Sim' if habilidade.por_turno else 'Não'}")
        print(f"Duração:     {habilidade.duracao if habilidade.duracao else 'Permanente/Instantâneo'}")
        if habilidade.tipo == "ativo":
            print(f"Custo:       {habilidade.custo} Energia")
        print("="*60 + "\n")
        return habilidade

    def _exibir_habilidade_ofensivo_detalhado(self, habilidade):
        """Exibe detalhes de uma habilidade ofensivo"""
        print("\n" + "="*80)
        print(f"HABILIDADE OFENSIVA: {habilidade.nome}")
        print("="*80)
        print(f"Tipo de Ataque:    {habilidade.tipo_ataque.upper()}")
        print(f"Descrição:         {habilidade.descricao}")
        
        # Custos
        print("\n📊 CUSTOS:")
        if habilidade.custo_energia or habilidade.custo_mana:
            if habilidade.custo_energia: print(f"  Energia: {habilidade.custo_energia}")
            if habilidade.custo_mana: print(f"  Mana:    {habilidade.custo_mana}")
        else:
            print("  Grátis")
        
        # Dano
        print("\n⚡ DANO:")
        if habilidade.dano:
            for entrada_dano in habilidade.dano:
                tipo = entrada_dano.get("tipo", "generico")
                valor = entrada_dano.get("valor", 0)
                print(f"  {valor} {tipo}")
        else:
            print("  Nenhum dano direto")
        
        # Multiplicador
        if habilidade.multiplicador_dano != 1.0:
            print(f"  Multiplicador: x{habilidade.multiplicador_dano}")
            if habilidade.aplica_a_arma_equipada:
                print(f"  Amplifica arma equipada: SIM")
        
        # Ignora resistências
        if habilidade.ignora_resistencias:
            print("  Ignora Resistências: SIM")
        
        # Área/Alcance
        if habilidade.tipo_ataque == "area":
            print(f"\n🎯 ÁREA:")
            print(f"  Raio: {habilidade.raio}m")
            print(f"  Raio Letal: {habilidade.raio_letal}m")
            print(f"  Falloff: {habilidade.falloff}")
            if habilidade.num_alvos_maximo:
                print(f"  Máximo de Alvos: {habilidade.num_alvos_maximo}")
        
        elif habilidade.tipo_ataque == "ranged":
            print(f"\n🎯 ALCANCE:")
            print(f"  Mínimo: {habilidade.alcance_min}m")
            print(f"  Máximo: {habilidade.alcance_max}m")
            print(f"  Falloff: {habilidade.falloff}")
        
        # Efeitos
        if habilidade.efeitos:
            print(f"\n💫 EFEITOS:")
            for efeito in habilidade.efeitos:
                nome = efeito.get("nome", "Efeito")
                chance = efeito.get("chance", 100)
                duracao = efeito.get("duracao", 1)
                print(f"  - {nome} ({chance}% de chance, {duracao}t)")
        
        print("="*80 + "\n")
        return habilidade

    def listar_habilidades_por_tipo(self, tipo_ataque=None):
        """Lista habilidades ofensivos filtrados por tipo de ataque"""
        if not tipo_ataque:
            return self.habilidades_ofensivas.copy()
        
        tipo_ataque = tipo_ataque.lower()
        return [h for h in self.habilidades_ofensivas if h.tipo_ataque.lower() == tipo_ataque]

    def exibir_resumo_combate(self):
        """Exibe resumo de todas as habilidades de ataque disponíveis em combate"""
        print("\n" + "="*80)
        print("RESUMO DE COMBATE - HABILIDADES DE ATAQUE DISPONÍVEIS")
        print("="*80)
        
        if not self.personagem:
            print("[ERRO] Nenhum personagem associado")
            return
        
        recursos = f"Energia: {self.personagem.EnergiaAtual}/{self.personagem.EnergiaMax} | Mana: {self.personagem.ManaAtual}/{self.personagem.ManaMax}"
        print(f"\n{recursos}\n")
        
        # Habilidades ofensivos disponíveis
        disponiveis = self.listar_disponiveis()
        
        if disponiveis:
            print("✅ HABILIDADES DE ATAQUE DISPONÍVEIS:")
            print("-" * 80)
            for idx, habilidade in enumerate(disponiveis, 1):
                tipo_ataque = habilidade.tipo_ataque.upper()
                custos = []
                if habilidade.custo_energia: custos.append(f"{habilidade.custo_energia}En")
                if habilidade.custo_mana: custos.append(f"{habilidade.custo_mana}Ma")
                custo_txt = "+".join(custos) if custos else "Grátis"
                
                print(f"  [{idx}] {habilidade.nome:<25} ({tipo_ataque:<6}) | {custo_txt}")
        else:
            print("❌ NENHUMA HABILIDADE DE ATAQUE DISPONÍVEL (recursos insuficientes)")
        
        # Habilidades não disponíveis
        nao_disponiveis = [h for h in self.habilidades_ofensivas if h not in disponiveis]
        
        if nao_disponiveis:
            print("\n⚠️ HABILIDADES DE ATAQUE INDISPONÍVEIS (recursos insuficientes):")
            print("-" * 80)
            for habilidade in nao_disponiveis:
                pode_usar, erro = habilidade.pode_usar(self.personagem)
                print(f"  ❌ {habilidade.nome:<25} | {erro}")
        
        print("\n" + "="*80 + "\n")
# Classe habilidade #
# Classe buff/debuff #
class BuffDebuff:
    def __init__(self, nome, duracao, efeito, descricao, tipo="buff"):
        self.nome = nome
        self.duracao = duracao  # Número de turnos, "permanente", ou None
        self.efeito = efeito
        self.descricao = descricao
        self.tipo = tipo
        # Garantir que turnos_restantes seja int
        if duracao == "permanente":
            self.turnos_restantes = None
        else:
            try:
                self.turnos_restantes = int(duracao)
            except:
                self.turnos_restantes = 1
    
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
    def __init__(self, personagem=None):
        self.personagem = personagem
        self.efeitos = []

    def adicionar_efeito(self, nome, duracao, efeito, descricao, tipo="buff"):
        """Adiciona um novo buff/debuff à lista"""
        buff_debuff = BuffDebuff(nome, duracao, efeito, descricao, tipo)
        self.efeitos.append(buff_debuff)
        return buff_debuff
    
    def adicionar_efeito_objeto(self, buff_debuff):
        existente = next((e for e in self.efeitos if e.nome == buff_debuff.nome), None)
        if existente:
            existente.turnos_restantes = max(existente.turnos_restantes, buff_debuff.duracao)
            return existente
        self.efeitos.append(buff_debuff)

    def processar_turnos(self):
        """Processa os turnos de todos os efeitos e remove os expirados"""
        efeitos_expirados = []

        for efeito in self.efeitos[:]:
            if not efeito.eh_permanente():
                if not efeito.decrementar_turno():

                    # Remove modificadores corretamente
                    if self.personagem:
                        # ✅ Garantir que efeito.efeito seja sempre uma lista
                        efeito_list = efeito.efeito if isinstance(efeito.efeito, list) else [efeito.efeito]
                        
                        for entrada in efeito_list:
                            # ✅ Pular se entrada for string
                            if isinstance(entrada, str):
                                continue
                            
                            # ✅ Agora é seguro chamar .get()
                            tags = entrada.get("tags", [])
                            valor = entrada.get("valor", 0)

                            if tags:
                                self.personagem.remover_modificador_generico(tags, valor)

                    efeitos_expirados.append(efeito.nome)
                    self.efeitos.remove(efeito)

        return efeitos_expirados
    
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
    
    def to_dict(self):
        return {
            "efeitos": [efeito.to_dict() for efeito in self.efeitos]
        }
    
    @classmethod
    def from_dict(cls, data, personagem=None):
        """Restaura buffs/debuffs de um dict e APLICA os efeitos no personagem"""
        gerenciador = cls(personagem=personagem)
        
        for efeito_data in data.get("efeitos", []):
            efeito = BuffDebuff.from_dict(efeito_data)
            gerenciador.efeitos.append(efeito)
            
            # ✅ NOVO: Reaplica os efeitos no personagem ao carregar
            if personagem:
                # Verificar se efeito é uma lista ou string
                efeito_list = efeito.efeito if isinstance(efeito.efeito, list) else [efeito.efeito]
                
                for entrada in efeito_list:
                    # ✅ Se entrada for string, pula (não pode processar)
                    if isinstance(entrada, str):
                        continue
                    
                    # Se entrada for dict, processa normalmente
                    if isinstance(entrada, dict):
                        tags = entrada.get("tags", [])
                        valor = entrada.get("valor", 0)
                        atributo = entrada.get("atributo")

                        if tags:
                            # Efeito com tags
                            personagem.aplicar_modificador_generico(
                                tags=tags,
                                valor=valor
                            )
                        elif atributo in ["vida", "energia", "mana"]:
                            # Efeito direto em recursos
                            if atributo == "vida":
                                personagem.ModificarVida(valor)
                            elif atributo == "energia":
                                personagem.ModificarEnergia(valor)
                            elif atributo == "mana":
                                personagem.ModificarMana(valor)
        
        return gerenciador
# Classe buff/debuff #
# Classe inventário #
class Inventario:
    def __init__(self):
        self.itens = []
    
    def _garantir_objetos(self):
        """Garante que todos os itens no inventário sejam objetos, não dicionários"""
        CLASSES_DISPONIVEIS = {
            'Item': Item,
            'Municao': Municao,
            'Melhoria': Melhoria,
            'Melee': Melee,
            'Ranged': Ranged,
            'Protecao': Protecao,
            'Arma': Arma,
            'Equipamento': Equipamento
        }
        
        for entrada in self.itens:
            if isinstance(entrada['item'], dict):
                item_dict = entrada['item']
                classe_nome = item_dict.get('_classe') or item_dict.get('__class__', 'Item')
                
                if classe_nome in CLASSES_DISPONIVEIS:
                    item_class = CLASSES_DISPONIVEIS[classe_nome]
                    if hasattr(item_class, 'from_dict'):
                        entrada['item'] = item_class.from_dict(item_dict)
                        print(f"[Inventario] 🔧 Convertido '{item_dict.get('nome')}' de dict para {classe_nome}")

    def gerenciar_item(self, nome_item=None, item_objeto=None, quantidade=1, dicionarios=None, operacao="adicionar"):
        # Garante que todos os itens existentes sejam objetos
        self._garantir_objetos()
        
        item = item_objeto or (dicionarios.get(nome_item)() if nome_item and dicionarios and nome_item in dicionarios else None)
        if not item: return False

        # CORREÇÃO CRÍTICA: Converter dicionário em objeto se necessário
        if isinstance(item, dict):
            print(f"[Inventario] ⚠️ Convertendo item dicionário '{item.get('nome', 'desconhecido')}' para objeto...")
            
            # Dicionário de classes disponíveis
            CLASSES_DISPONIVEIS = {
                'Item': Item,
                'Municao': Municao,
                'Melhoria': Melhoria,
                'Melee': Melee,
                'Ranged': Ranged,
                'Protecao': Protecao,
                'Arma': Arma,
                'Equipamento': Equipamento
            }
            
            classe_nome = item.get('_classe') or item.get('__class__', 'Item')
            
            if classe_nome in CLASSES_DISPONIVEIS:
                item_class = CLASSES_DISPONIVEIS[classe_nome]
                if hasattr(item_class, 'from_dict'):
                    item = item_class.from_dict(item)
                    print(f"[Inventario] ✅ Item convertido para {classe_nome}")
                else:
                    print(f"[Inventario] ❌ Classe {classe_nome} não tem from_dict")
                    return False
            else:
                print(f"[Inventario] ❌ Classe '{classe_nome}' não reconhecida")
                return False

        # Itens únicos (com Id)
        if hasattr(item, "Id"):
            if operacao == "adicionar":
                [self.itens.append({"item": item, "quantidade": 1}) for _ in range(quantidade)]
                return True
            if operacao == "remover":
                removidos = 0
                for i in list(self.itens):
                    if hasattr(i["item"], "Id") and i["item"].Id == item.Id:
                        self.itens.remove(i)
                        removidos += 1
                        if removidos == quantidade: break
                return removidos == quantidade

        # Itens empilháveis (sem Id)
        for i in self.itens:
            if i['item'].nome == item.nome and not hasattr(i['item'], "Id"):
                if operacao == "adicionar": i['quantidade'] += quantidade; return True
                if operacao == "remover":
                    if i['quantidade'] >= quantidade:
                        i['quantidade'] -= quantidade
                        if i['quantidade'] == 0: self.itens.remove(i)
                        return True
                    return False

        # Se não achou o item e operação é adicionar
        if operacao == "adicionar": self.itens.append({"item": item, "quantidade": quantidade}); return True
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
        """Retorna lista de itens para UI, com quantidade real para stackáveis."""
        result = []
        for idx, entrada in enumerate(self.itens):
            item = entrada.get("item")
            if item:
                tem_id = hasattr(item, "Id") and item.Id
                result.append({
                    "nome":       getattr(item, "nome", "Desconhecido"),
                    "quantidade": 1 if tem_id else entrada.get("quantidade", 1),
                    "tipo":       item.__class__.__name__,
                    "slot":       entrada.get("slot", "inventario"),
                    "unico":      bool(tem_id),   # True → não stackável
                    "_idx":       idx,            # índice real em self.itens
                    "objeto":     item,
                })
        return result

    def consumir(self,item,quantidade=1):
        return self.remover_item(item,quantidade)

    def to_dict(self):
        lista_serializada=[]
        for entrada in self.itens:
            item=entrada["item"]; qtd=entrada["quantidade"]
            if hasattr(item,"to_dict"):
                item_dict=item.to_dict()
                item_dict["_classe"]=item.__class__.__name__
                lista_serializada.append({"item":item_dict,"quantidade":qtd})
            elif hasattr(item,"Id"):
                lista_serializada.append({"item":{"Id":item.Id,"nome":item.nome,"_classe":item.__class__.__name__},"quantidade":qtd})
            else:
                lista_serializada.append({"item":{"nome":item.nome,"_classe":item.__class__.__name__},"quantidade":qtd})
        return {"itens":lista_serializada}

    @classmethod
    def from_dict(cls, data):
        inventario = cls()
        itens_data=data.get("itens",data) if isinstance(data,dict) else data
        CLASSES_DISPONIVEIS = {
            'Item': Item, 'Municao': Municao, 'Melhoria': Melhoria,
            'Melee': Melee, 'Ranged': Ranged, 'Protecao': Protecao,
            'Arma': Arma, 'Equipamento': Equipamento
        }

        for e in itens_data:
            if isinstance(e, dict) and "item" in e:
                item_dict = e["item"]
                classe_nome = item_dict.get("_classe", "Item")
                item_class = CLASSES_DISPONIVEIS.get(classe_nome, Item)
                # Usa from_dict seguro
                if hasattr(item_class, "from_dict"):
                    item_obj = item_class.from_dict(item_dict)
                else:
                    item_obj = item_class()
                    if hasattr(item_obj, "nome") and "nome" in item_dict:
                        item_obj.nome = item_dict["nome"]
                inventario.itens.append({"item": item_obj, "quantidade": e.get("quantidade", 1)})
        return inventario
# Classe inventário #
# Classe proficiencia #
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
    
    def carregar_base(self, proficiencias_base):
        if not proficiencias_base: return
        if isinstance(proficiencias_base, SistemaDeProficiencias):
            self.proficiencias = proficiencias_base.proficiencias.copy()
            return
        if isinstance(proficiencias_base, dict):
            for nome, dados in proficiencias_base.items():
                if isinstance(dados, Proficiencia):
                    self.proficiencias[nome] = dados
                elif isinstance(dados, dict):
                    self.proficiencias[nome] = Proficiencia.from_dict(dados)
                else:
                    self.proficiencias[nome] = Proficiencia(nome, "Desconhecido", int(dados) if isinstance(dados,(int,float)) else 0)

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
# Classe proficiencia #
### CLASSE PERSONAGEM ###
### CLASSE PERSONAGEM ###
### CLASSE PERSONAGEM ###


### CLASSE CRIATURA ###
### CLASSE CRIATURA ###
### CLASSE CRIATURA ###
class Criatura(Personagem):
    """
    Subclasse de Personagem para entidades não-humanas.
    Mantém toda a lógica de combate, modificadores e inventário,
    mas adiciona suporte a tamanho, tipo, traços naturais e anatomia customizada.
    """

    TAMANHOS = ["Minúsculo", "Pequeno", "Médio", "Grande", "Enorme", "Colossal"]

    def __init__(
        self,
        nome, Nivel, Forca, Agilidade, Vigor, Inteligencia, Presenca, Tatica, Poder,
        tipo_criatura="Besta",          # "Besta", "Morto-vivo", "Elemental", "Demônio", etc.
        tamanho="Médio",                # Define bônus/penalidades automáticas
        regioes_corpo=None,             # Permite anatomia customizada
        slots_extras=None,              # Slots adicionais (ex: "boca", "cauda")
        tracos_naturais=None,           # Lista de TracoNatural
        proficiencias_base=None,
    ):
        super().__init__(
            nome, Nivel, Forca, Agilidade, Vigor, Inteligencia,
            Presenca, Tatica, Poder, proficiencias_base
        )

        self.tipo_criatura: str = tipo_criatura
        self.tamanho: str = tamanho if tamanho in self.TAMANHOS else "Médio"
        self.tracos_naturais: list = tracos_naturais or []  # lista de TracoNatural

        # Substitui regiões do corpo se fornecidas (ex: cobra não tem "braços")
        if regioes_corpo is not None:
            self.regioes_corpo = {r: None for r in regioes_corpo}

        # Adiciona slots extras além de mão_direita/mão_esquerda
        if slots_extras:
            for nome_slot, slot_obj in slots_extras.items():
                self.slots[nome_slot] = slot_obj

        # Aplica modificadores de tamanho automaticamente
        self._aplicar_bonus_tamanho()

    # ==============================
    # BÔNUS DE TAMANHO
    # ==============================
    _BONUS_TAMANHO = {
        "Minúsculo": {"forca": -4, "vigor": -2, "esquiva": +4, "movimento": -2},
        "Pequeno":   {"forca": -2, "vigor": -1, "esquiva": +2},
        "Médio":     {},  # baseline
        "Grande":    {"forca": +2, "vigor": +2, "esquiva": -2, "carga": +10},
        "Enorme":    {"forca": +4, "vigor": +4, "esquiva": -4, "carga": +25, "movimento": +2},
        "Colossal":  {"forca": +6, "vigor": +6, "esquiva": -6, "carga": +50, "movimento": +4},
    }

    def _aplicar_bonus_tamanho(self):
        bonus = self._BONUS_TAMANHO.get(self.tamanho, {})
        for chave, valor in bonus.items():
            if chave in self.bonus_atributos:
                self.bonus_atributos[chave] += valor
            elif chave == "esquiva":
                self.mod_efeitos["esquiva"] = self.mod_efeitos.get("esquiva", 0) + valor
            elif chave == "carga":
                # bônus direto de carga via mod_efeitos
                self.mod_efeitos["carga"] = self.mod_efeitos.get("carga", 0) + valor
            elif chave == "movimento":
                self.mod_efeitos["movimento"] = self.mod_efeitos.get("movimento", 0) + valor
        self.recalcularAtributos()

    # ==============================
    # TRAÇOS NATURAIS
    # ==============================
    def adicionar_traco(self, traco):
        """Adiciona um TracoNatural e aplica seus modificadores."""
        self.tracos_naturais.append(traco)
        traco.aplicar(self)

    def remover_traco(self, nome_traco):
        """Remove um traço pelo nome e reverte seus modificadores."""
        for traco in self.tracos_naturais:
            if traco.nome == nome_traco:
                traco.remover(self)
                self.tracos_naturais.remove(traco)
                return True
        return False

    def listar_tracos(self):
        if not self.tracos_naturais:
            print(f"{self.nome} não possui traços naturais.")
            return
        print(f"Traços de {self.nome}:")
        for t in self.tracos_naturais:
            print(f"  [{t.nome}] {t.descricao}")

    # ==============================
    # SERIALIZAÇÃO
    # ==============================
    def to_dict(self):
        data = super().to_dict()
        data["tipo_criatura"] = self.tipo_criatura
        data["tamanho"] = self.tamanho
        data["tracos_naturais"] = [t.to_dict() for t in self.tracos_naturais]
        data["regioes_corpo_keys"] = list(self.regioes_corpo.keys())
        return data

    @classmethod
    def from_dict(cls, data):
        criatura = cls(
            nome=data["nome"],
            Nivel=data["Nivel"],
            Forca=data["Forca"],
            Agilidade=data["Agilidade"],
            Vigor=data["Vigor"],
            Inteligencia=data["Inteligencia"],
            Presenca=data["Presenca"],
            Tatica=data["Tatica"],
            Poder=data["Poder"],
            tipo_criatura=data.get("tipo_criatura", "Besta"),
            tamanho=data.get("tamanho", "Médio"),
            regioes_corpo=data.get("regioes_corpo_keys"),
            proficiencias_base=data.get("proficiencias", {}),
        )
        # Reaproveita o from_dict do pai para o restante
        # (recursos, inventário, mods, etc.)
        pai_dict = data.copy()
        Personagem.from_dict.__func__(criatura, pai_dict)  # aplica campos do pai
        return criatura

    @staticmethod
    def Criar(nome, nivel, Forca, Agilidade, Vigor, Inteligencia, Presenca, Tatica, Poder,
              tipo_criatura="Besta", tamanho="Médio", regioes_corpo=None,
              slots_extras=None, tracos_naturais=None, proficiencias_base=None):
        return Criatura(
            nome, nivel, Forca, Agilidade, Vigor, Inteligencia, Presenca, Tatica, Poder,
            tipo_criatura, tamanho, regioes_corpo, slots_extras, tracos_naturais, proficiencias_base
        )

class TracoNatural:
    def __init__(self, nome, descricao="", tags=None, valor=0, efeito_fn=None, remover_fn=None):
        """
        nome       : str  — nome do traço ("Garra Afiada", "Carapaça", etc.)
        descricao  : str  — texto descritivo
        tags       : list — tags de modificador a aplicar (mesmo sistema do personagem)
        valor      : int  — valor aplicado via tags
        efeito_fn  : callable(personagem) — lógica customizada ao aplicar
        remover_fn : callable(personagem) — lógica customizada ao remover
        """
        self.nome = nome
        self.descricao = descricao
        self.tags = tags or []
        self.valor = valor
        self._efeito_fn = efeito_fn
        self._remover_fn = remover_fn

    def aplicar(self, personagem):
        if self.tags and self.valor:
            personagem.aplicar_modificador_generico(self.tags, self.valor, duracao=None, fonte="traco_natural")
        if self._efeito_fn:
            self._efeito_fn(personagem)

    def remover(self, personagem):
        if self.tags and self.valor:
            personagem.remover_modificador_generico(self.tags, self.valor)
        if self._remover_fn:
            self._remover_fn(personagem)

    def to_dict(self):
        return {"nome": self.nome, "descricao": self.descricao, "tags": self.tags, "valor": self.valor}

    @classmethod
    def from_dict(cls, data):
        return cls(nome=data["nome"], descricao=data.get("descricao",""), tags=data.get("tags",[]), valor=data.get("valor",0))
### CLASSE CRIATURA ###
### CLASSE CRIATURA ###
### CLASSE CRIATURA ###


### CLASSES DE ITEM ###
### CLASSES DE ITEM ###
### CLASSES DE ITEM ###
class Item:
    def __init__(self, nome, peso=None, descricao=None, uso=None, efeitos=None):
        self.nome = nome
        if peso is not None: self.peso = peso
        if descricao: self.descricao = descricao
        self.uso = uso
        self.efeitos = efeitos or []

    def stats(self):
        data = {"Nome": self.nome}
        if hasattr(self, "peso"): data["Peso"] = self.peso
        if hasattr(self, "descricao"): data["Descrição"] = self.descricao
        if self.uso is not None: data["Uso"] = self.uso
        if self.efeitos: data["Efeitos"] = self.efeitos
        return data

    def to_dict(self):
        data = {"tipo": self.__class__.__name__, "nome": self.nome}
        if hasattr(self, "peso"): data["peso"] = self.peso
        if hasattr(self, "descricao"): data["descricao"] = self.descricao
        if self.uso is not None: data["uso"] = self.uso
        if self.efeitos: data["efeitos"] = self.efeitos
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            nome=data["nome"],
            peso=data.get("peso"),
            descricao=data.get("descricao"),
            uso=data.get("uso"),
            efeitos=data.get("efeitos", [])
        )

# Subtipo do efeito → tipo_de_dano canônico
SUBTIPO_PARA_TIPO_DANO = {
    "explosivo": "explosivo",
    "fragmentacao": "perfurante",
    "concussao": "concussivo",
    "incendiario": "incendiário",
    "gas": "envenenante",
    "eletrico": "eletrocutante",
    "congelante": "congelante",
    "mental": "mental",
}
class Consumivel(Item):
    def __init__(self,
        nome,peso=None,descricao=None,uso=None,efeitos=None,raio=None,raio_letal=None,falloff="linear",perfuracao=0):
        super().__init__(nome, peso, descricao)
        self.uso = uso or "consumir"
        self.efeitos = efeitos or []
        self.raio = raio # None ou 0 = sem área

        # Dados de explosão (ignorados se raio for None/0)
        self.raio_letal = raio_letal # se None, calculado como 30% do raio na hora do uso
        self.falloff    = falloff
        self.perfuracao = perfuracao

    # ── eh_area ───────────────────────────────────────────
    def eh_area(self) -> bool:
        """True se este consumível afeta uma área."""
        return bool(self.raio and self.raio > 0)

    # ── aplicar (alvo único) ──────────────────────────────
    def aplicar(self, personagem):
        """
        Aplica efeitos diretos no personagem (sem área).
        Para explosões/granadas, use usar_consumivel().
        """
        for efeito in self.efeitos:
            tipo = efeito.get("tipo", "")

            if tipo == "cura":
                personagem.ModificarVida(efeito.get("valor", 0))

            elif tipo == "energia":
                personagem.ModificarEnergia(efeito.get("valor", 0))

            elif tipo == "mana":
                personagem.ModificarMana(efeito.get("valor", 0))

            elif tipo in ("buff", "debuff"):
                bb = BuffDebuff(
                    nome      = efeito.get("nome", ""),
                    duracao   = efeito.get("duracao", 1),
                    efeito    = efeito.get("efeito", []),
                    descricao = efeito.get("descricao", ""),
                    tipo      = tipo,
                )
                personagem.buffs_debuffs.adicionar_efeito_objeto(bb)

            elif tipo == "dano":
                # dano direto sem área (ex: veneno injetável)
                subtipo    = efeito.get("subtipo", "")
                tipo_dano  = SUBTIPO_PARA_TIPO_DANO.get(subtipo, subtipo)
                valor      = efeito.get("valor", 0)
                dano_final = personagem.calcular_dano_recebido(valor, tipo_dano) if tipo_dano else valor
                personagem.ModificarVida(-dano_final)

    def stats(self):
        return {
            "Nome": self.nome,
            "Peso": getattr(self, "peso", "—"),
            "Uso": self.uso,
            "Efeito em Área": self.eh_area(),
            "Raio": self.raio if self.raio else "—",
            "Raio Letal": self.raio_letal if self.raio_letal else (round(self.raio * 0.3, 1) if self.raio else "—"),
            "Falloff": self.falloff if self.raio else "—",
            "Perfuração": self.perfuracao if self.raio else "—",
            "Efeitos": self.efeitos if self.efeitos else "Nenhum",
            "Descrição": getattr(self, "descricao", "—"),
        }

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "uso":        self.uso,
            "efeitos":    self.efeitos,
            "raio":       self.raio,
            "raio_letal": self.raio_letal,
            "falloff":    self.falloff,
            "perfuracao": self.perfuracao,
        })
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            nome        = data["nome"],
            peso        = data.get("peso"),
            descricao   = data.get("descricao"),
            uso         = data.get("uso"),
            efeitos     = data.get("efeitos", []),
            raio        = data.get("raio"),
            raio_letal  = data.get("raio_letal"),
            falloff     = data.get("falloff", "linear"),
            perfuracao  = data.get("perfuracao", 0),
        )


class Equipamento(Item):
    def __init__(self, nome, peso, slots_criados, descricao=None):
        super().__init__(nome, peso)
        self.slots_criados = slots_criados
        self.descricao = descricao or ""

    def criar_slots(self):
        slots = {}
        for dados in self.slots_criados:
            slot = SlotEquipamento(**dados)
            slots[slot.nome] = slot
        return slots
    
    def stats(self):
        return {
            "Nome": self.nome,
            "Peso": self.peso,
            "Slots Criados": len(self.slots_criados),
            "Detalhes dos Slots": self.slots_criados if self.slots_criados else "Nenhum",
            "Descrição": self.descricao or "—"
        }

    def to_dict(self):
        return {"tipo": self.__class__.__name__, "nome": self.nome, "peso": self.peso, "slots_criados": self.slots_criados, "descricao": self.descricao}

    @classmethod
    def from_dict(cls, data):
        return cls(nome=data["nome"], peso=data.get("peso"), slots_criados=data.get("slots_criados", []), descricao=data.get("descricao"))


class Municao(Item):
    def __init__(self, nome, calibre, dano, tipo_dano, perfuracao=0, efeitos=None, peso=None, descricao=None):
        super().__init__(nome, peso=peso)
        self.calibre = calibre
        self.dano = dano
        self.tipo_dano = tipo_dano
        self.perfuracao = perfuracao
        self.efeitos = efeitos or []
        self.descricao = descricao or ""

    def stats(self):
        return {
            "Nome": self.nome,
            "Calibre": self.calibre,
            "Dano": self.dano,
            "Tipo de Dano": self.tipo_dano,
            "Perfuração": self.perfuracao,
            "Efeitos": self.efeitos if self.efeitos else "Nenhum",
            "Descrição": self.descricao or "—"
        }

    def to_dict(self):
        return {
            "tipo": self.__class__.__name__,
            "nome": self.nome,
            "calibre": self.calibre,
            "dano": self.dano,
            "tipo_dano": self.tipo_dano,
            "perfuracao": self.perfuracao,
            "efeitos": self.efeitos,
            "descricao": self.descricao,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data.get("nome"), data.get("calibre"), data.get("dano"), data.get("tipo_dano"),
                   data.get("perfuracao", 0), data.get("efeitos"), data.get("peso"), data.get("descricao"))


class Melhoria(Item):
    def __init__(self, nome, peso, tipo, modificadores,descricao=None):
        super().__init__(nome, peso)
        self.tipo = tipo  # "melee", "ranged", "protecao"
        self.modificadores = modificadores
        self.descricao = descricao or ""
    
    def stats(self):
        return {
            "Nome": self.nome,
            "Peso": self.peso,
            "Tipo": self.tipo,
            "Modificadores": self.modificadores,
            "Descrição": self.descricao or "—"
        }

    def to_dict(self):
        return {"nome": self.nome, "peso": self.peso, "tipo": self.tipo, "modificadores": self.modificadores, "descricao": self.descricao}

    @classmethod
    def from_dict(cls, data):
        return cls(nome=data["nome"], peso=data["peso"], tipo=data["tipo"], modificadores=data["modificadores"], descricao=data.get("descricao"))


class Arma(Item):
    def __init__(self,nome,peso,maos=1):
        super().__init__(nome,peso,uso="equipar")
        self.maos=maos
        self.modos_uso=[]
        self.Id=gerar_id()


class Melee(Arma):
    BONUS_RARIDADE={"Comum":0,"Incomum":2,"Rara":4,"Épica":6,"Exótica":8,"Lendária":10}
    def __init__(self,nome,peso,dano_base,crit_mult,crit_valor,tags,raridade,descricao=None):
        self.tags=set(tags)
        super().__init__(nome,peso,1)
        self.modos_uso=["melee"]
        self.raridade=raridade
        self.Melhorias=[]
        self.descricao = descricao or ""

        # 🔹 Atributos base
        self.danoBase=dano_base+self.BONUS_RARIDADE.get(raridade,0)
        self.critico_multiplicadorBase=crit_mult
        self.valor_criticoBase=crit_valor
        self.pesoBase=peso
        self.mod_acertoBase=0
        self.ignora_armaduraBase=0
        self.tipo_danoBase=None
        self.efeito_criticoBase=None
        self.alcanceBase=1
        self.usa_agilidadeBase=False
        self.arremessavelBase=False
        self.nao_letalBase=False
        self.maosBase=1

        self.recalcular_atributos()

    def recalcular_atributos(self):
        # 🔹 Reset para base
        self.dano=self.danoBase
        self.critico_multiplicador=self.critico_multiplicadorBase
        self.valor_critico=self.valor_criticoBase
        self.peso=self.pesoBase
        self.mod_acerto=self.mod_acertoBase
        self.ignora_armadura=self.ignora_armaduraBase
        self.tipo_dano=self.tipo_danoBase
        self.efeito_critico=self.efeito_criticoBase
        self.alcance=self.alcanceBase
        self.usa_agilidade=self.usa_agilidadeBase
        self.arremessavel=self.arremessavelBase
        self.nao_letal=self.nao_letalBase
        self.maos=self.maosBase

        # 🔹 Aplicar tags
        for tag in self.tags:
            data=TAGS_MELEE.get(tag,{})
            self.mod_acerto+=data.get("mod_acerto",0)
            self.dano+=data.get("mod_dano",0)
            self.ignora_armadura+=data.get("ignora_armadura",0)
            self.valor_critico+=data.get("crit_valor",0)
            self.critico_multiplicador+=data.get("crit_mult_bonus",0)
            if "tipo_dano" in data: self.tipo_dano=data["tipo_dano"]
            if "efeito_critico" in data: self.efeito_critico=data["efeito_critico"]
            if "alcance" in data: self.alcance=data["alcance"]
            if data.get("usa_agilidade"): self.usa_agilidade=True
            if data.get("arremessavel"): self.arremessavel=True
            if data.get("nao_letal"): self.nao_letal=True
            if "maos" in data: self.maos=data["maos"]

        # 🔹 Aplicar melhorias
        for melhoria in self.Melhorias:
            mods=melhoria.modificadores
            self.dano+=mods.get("dano",0)
            self.critico_multiplicador+=mods.get("critico_multiplicador",0)
            self.valor_critico+=mods.get("valor_critico",0)
            self.peso+=mods.get("peso",0)
            self.mod_acerto+=mods.get("mod_acerto",0)
            self.ignora_armadura+=mods.get("ignora_armadura",0)
            self.maos+=mods.get("maos",0)
            for tag in mods.get("add_tags",[]): self.tags.add(tag)
            for tag in mods.get("remove_tags",[]): self.tags.discard(tag)

        if self.maos<1: self.maos=1

    def adicionar_melhoria(self,melhoria):
        if melhoria.tipo!="melee" or melhoria in self.Melhorias: return False
        self.Melhorias.append(melhoria)
        self.recalcular_atributos()
        return True

    def remover_melhoria(self,melhoria):
        if melhoria in self.Melhorias:
            self.Melhorias.remove(melhoria)
            self.recalcular_atributos()

    def stats(self):
        return {
            "Nome":self.nome,
            "Peso":self.peso,
            "Dano":self.dano,
            "Valor para Crítico":self.valor_critico,
            "Multiplicador Crítico":self.critico_multiplicador,
            "Tipo de Dano":self.tipo_dano,
            "Ignora Armadura":self.ignora_armadura,
            "Efeito no Crítico":self.efeito_critico,
            "Alcance":self.alcance,
            "Usa Agilidade":self.usa_agilidade,
            "Não Letal":self.nao_letal,
            "Arremessável":self.arremessavel,
            "Mãos":self.maos,
            "Tags":sorted(self.tags),
            "Raridade":self.raridade,
            "Melhorias":[m.stats() for m in self.Melhorias] if self.Melhorias else "Nenhuma",
            "Descrição": self.descricao or "—"
        }

    def to_dict(self):
        return {
            "nome": self.nome, "peso": self.pesoBase, "dano_base": self.danoBase - self.BONUS_RARIDADE.get(self.raridade, 0),
            "crit_mult": self.critico_multiplicadorBase, "crit_valor": self.valor_criticoBase,
            "tags": list(self.tags), "raridade": self.raridade, "Id": self.Id,
            "Melhorias": [serializar_item(m) for m in self.Melhorias],
            "descricao": self.descricao,
        }

    @classmethod
    def from_dict(cls, data):
        instance = cls(data["nome"], data["peso"], data["dano_base"], data["crit_mult"], data["crit_valor"],
                       data["tags"], data["raridade"], descricao=data.get("descricao"))
        instance.Id = data.get("Id", instance.Id)
        instance.Melhorias = [deserializar_item(m) for m in data.get("Melhorias", []) if deserializar_item(m)]
        instance.recalcular_atributos()
        return instance
    

class Ranged(Arma):
    def __init__(self, nome, peso, classe, acoes_disparo, raridade, calibre, capacidade, tpm, ruido, tipo_dano, maos=1, descricao=None):
        super().__init__(nome,peso,1)
        self.classe = classe
        self.tipo_dano = tipo_dano
        self.raridade = raridade
        self.calibre = calibre

        self.acoes_disparo = acoes_disparo
        self.modo_disparo_atual = acoes_disparo[0]

        self.capacidade = capacidade
        self.Perfuracao = 0
        self.TPM = int(tpm)
        self.ruido = int(ruido)

        self.munições = 0
        self.municao = None
        self.Acessorios = []

        self.maos=maos
        self.descricao = descricao or ""

        #stats avançados#
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
        elif classe == "Fuzil de assalto":
            self.dano = 20
            self.recuo = 3
            self.MaxRange = 80
            self.MinRange = 5
            self.ShortCrit = 22
            self.MediumCrit = 24
            self.LongCrit = 28
        elif classe == "Fuzil de batalha":
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
        elif classe == "Fuzil de precisão":
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
        elif classe == "Fuzil antimaterial":
            self.dano = 50
            self.recuo = 5
            self.MaxRange = 250
            self.MinRange = 10
            self.ShortCrit = 35
            self.MediumCrit = 25
            self.LongCrit = 20
        else:
            print(f"Erro: Classe '{classe}' não reconhecida.")

        self.modificadores_modo = {
            "Simples": {"recuo": 2, "dano": 0, "MaxRange": 5, "MinRange": 1},
            "Semi": {"recuo": 1, "dano": 0, "MaxRange": -5, "MinRange": 0},
            "Dupla": {"recuo": 1, "dano": 0, "MaxRange": 0, "MinRange": 0},
            "Rajada": {"recuo": 1, "dano": 0, "MaxRange": -10, "MinRange": 0},
            "Auto": {"recuo": 2, "dano": 0, "MaxRange": -20, "MinRange": 0},
            "Pump": {"recuo": 3, "dano": 0, "MaxRange": -5, "MinRange": 0},
            "Alavanca": {"recuo": 3, "dano": 0, "MaxRange": -5, "MinRange": 0},
            "Bolt": {"recuo": 3, "dano": 0, "MaxRange": -5, "MinRange": 0},
        }
        
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
        self.capacidadeBase = self.capacidade
        self.pesoBase = self.peso

        self.maosBase= self.maos

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
        
    def adicionar_acessorio(self, acessorio):
        if acessorio.tipo != "ranged":
            return False
        self.Acessorios.append(acessorio)
        self.recalcular_atributos()
        return True
        
    def remover_acessorio(self, acessorio):
        if acessorio in self.Acessorios:
            self.Acessorios.remove(acessorio)
            self.recalcular_atributos()
        else:
            pass
    
    def trocar_modo_disparo(self):
        idx = self.acoes_disparo.index(self.modo_disparo_atual)
        self.modo_disparo_atual = self.acoes_disparo[(idx + 1) % len(self.acoes_disparo)]
        self.recalcular_atributos()
        return self.modo_disparo_atual
    
    def definir_modo_disparo(self, modo):
        if modo not in self.acoes_disparo:
            return False
        self.modo_disparo_atual = modo
        self.recalcular_atributos()
        return True

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
        self.efeitos = []

        self.maos=self.maosBase

        if self.municao:
            self.efeitos.extend(getattr(self.municao, "efeitos", []))
            self.dano += self.municao.dano

        # aplicar modificadores dos acessórios sem duplicar efeitos
        seen_efeitos = set()
        for acessorio in self.Acessorios:
            for e in acessorio.modificadores.get("efeitos", []):
                if str(e) not in seen_efeitos:
                    self.efeitos.append(e)
                    seen_efeitos.add(str(e))
            self.dano += acessorio.modificadores.get("dano", 0)
            self.recuo += acessorio.modificadores.get("recuo", 0)
            self.MaxRange += acessorio.modificadores.get("MaxRange", 0)
            self.MinRange += acessorio.modificadores.get("MinRange", 0)
            self.ShortCrit += acessorio.modificadores.get("ShortCrit", 0)
            self.MediumCrit += acessorio.modificadores.get("MediumCrit", 0)
            self.LongCrit += acessorio.modificadores.get("LongCrit", 0)
            self.capacidade += acessorio.modificadores.get("capacidade", 0)
            self.peso += acessorio.peso

        mod = self.modificadores_modo.get(self.modo_disparo_atual)
        if mod:
            self.recuo += mod.get("recuo", 0)
            self.dano += mod.get("dano", 0)
            self.MaxRange += mod.get("MaxRange", 0)
            self.MinRange += mod.get("MinRange", 0)
    
    def stats(self):
        return {
            "Nome":self.nome,
            "Peso":self.peso,
            "Classe":self.classe,
            "Calibre":self.calibre,
            "Ação":self.modo_disparo_atual,
            "Raridade":self.raridade,
            "Dano":self.dano,
            "Recuo":self.recuo,
            "Alcance Mínimo":self.MinRange,
            "Alcance Máximo":self.MaxRange,
            "Crítico Curto":self.ShortCrit,
            "Crítico Médio":self.MediumCrit,
            "Crítico Longo":self.LongCrit,
            "Capacidade Total":self.capacidade,
            "Ruído":self.ruido,
            "Munições":self.munições,
            "Munição":{
                "Tipo":self.municao.nome if self.municao else "Descarregada",
                "Dano Extra":self.municao.dano if self.municao else 0,
                "Perfuração":self.Perfuracao if self.municao else 0
            },
            "Acessórios":[a.stats() for a in self.Acessorios] if self.Acessorios else [],
            "Modo de empunhar":self.maos,
            "Descrição": self.descricao or "—"
        }

    def to_dict(self):
        return {
            "nome": self.nome, "peso": self.pesoBase, "classe": self.classe, "raridade": self.raridade,
            "calibre": self.calibre, "capacidade": self.capacidadeBase, "TPM": self.TPM, "ruido": self.ruido,
            "tipo_dano": self.tipo_dano, "acoes_disparo": self.acoes_disparo, "modo_disparo_atual": self.modo_disparo_atual,
            "munições": self.munições, "municao": serializar_item(self.municao) if self.municao else None,
            "Id": self.Id, "Acessorios": [serializar_item(a) for a in self.Acessorios],
            "Perfuracao": self.Perfuracao, "maos": self.maosBase, "descricao": self.descricao,
        }

    @classmethod
    def from_dict(cls, data):
        instance = cls(
            nome=data["nome"], peso=data["peso"], classe=data["classe"], acoes_disparo=data.get("acoes_disparo", ["Semi"]),
            raridade=data["raridade"], calibre=data["calibre"], capacidade=data["capacidade"],
            tpm=data.get("TPM", 0), ruido=data.get("ruido", 0), tipo_dano=data.get("tipo_dano", "perfurante"),
            maos=data.get("maos", 1), descricao=data.get("descricao"),
        )
        instance.Id = data.get("Id", instance.Id)
        instance.modo_disparo_atual = data.get("modo_disparo_atual", instance.acoes_disparo[0])
        instance.munições = data.get("munições", 0)
        instance.Perfuracao = data.get("Perfuracao", 0)
        instance.municao = deserializar_item(data["municao"]) if data.get("municao") else None
        instance.Acessorios = [deserializar_item(a) for a in data.get("Acessorios", []) if deserializar_item(a)]
        instance.recalcular_atributos()
        return instance


class Protecao(Item):
    def __init__(self,nome,peso,nivelBalistico,absorcoes:dict,regioes_cobertas:list[str],regiao_indicada=None,durabilidade_max=100, descricao=None):
        super().__init__(nome,peso)
        self.regioes_cobertas=[r.lower() for r in regioes_cobertas]
        self.regiao_indicada=regiao_indicada.lower() if regiao_indicada else (self.regioes_cobertas[0] if self.regioes_cobertas else None)
        self.nivelBalisticoBase=nivelBalistico; self.absorcoesBase=absorcoes.copy(); self.pesoBase=peso
        self.durabilidadeMax=durabilidade_max; self.durabilidade=durabilidade_max
        self.Melhorias=[]; self.Id=gerar_id()
        self.descricao = descricao or ""
        self.recalcular_atributos()

    def recalcular_atributos(self):
        # reset para valores base
        self.nivelBalistico = self.nivelBalisticoBase
        self.absorcoes = self.absorcoesBase.copy()
        self.peso = self.pesoBase
        self.regioes_cobertas = [r.lower() for r in self.regioes_cobertas]  # mantém base

        for melhoria in self.Melhorias:
            for chave, valor in melhoria.modificadores.items():
                if chave == "nivelBalistico":
                    self.nivelBalistico += valor
                elif chave == "peso":
                    self.peso += valor
                elif chave == "durabilidade":
                    self.durabilidadeMax += valor
                    self.durabilidade = min(self.durabilidade, self.durabilidadeMax)
                elif chave == "regioes_cobertas":
                    # adiciona novas regiões sem duplicar
                    for reg in valor:
                        if reg.lower() not in self.regioes_cobertas:
                            self.regioes_cobertas.append(reg.lower())
                else:
                    # aplica modificadores em absorções específicas ou novos tipos de dano
                    self.absorcoes[chave] = self.absorcoes.get(chave, 0) + valor

    def aplicar_dano(self, tipo_dano: str, dano_bruto: int):
        absorcao = self.absorcoes.get(tipo_dano, 0)
        dano_pos_absorcao = max(0, dano_bruto - absorcao)

        desgaste = max(1, absorcao // 8) if dano_bruto > 0 else 0
        self.durabilidade = max(0, self.durabilidade - desgaste)

        if self.durabilidade == 0:
            dano_pos_absorcao += 2  # trauma leve

        return dano_pos_absorcao, absorcao, desgaste

    def adicionar_melhoria(self, melhoria):
        if melhoria.tipo != "protecao":
            return False
        if melhoria not in self.Melhorias:
            self.Melhorias.append(melhoria)
            self.recalcular_atributos()
            return True
        return False

    def remover_melhoria(self, melhoria):
        if melhoria in self.Melhorias:
            self.Melhorias.remove(melhoria)
            self.recalcular_atributos()

    def cobre_regiao(self, regiao: str) -> bool:
        return regiao.lower() in self.regioes_cobertas

    def stats(self):
        return {
            "Nome": self.nome,
            "Peso": self.peso,
            "Regiões Cobertas": self.regioes_cobertas,
            "Nível Balístico": self.nivelBalistico,
            "Durabilidade": f"{self.durabilidade}/{self.durabilidadeMax}",
            "Absorções": self.absorcoes,
            "Melhorias": [m.nome for m in self.Melhorias] if self.Melhorias else "Nenhuma",
            "Descrição": self.descricao or "—"
        }

    def to_dict(self):
        return {
            "nome": self.nome, "peso": self.pesoBase, "nivelBalistico": self.nivelBalisticoBase,
            "absorcoes": self.absorcoesBase, "regioes_cobertas": self.regioes_cobertas,
            "durabilidade": self.durabilidade, "durabilidadeMax": self.durabilidadeMax,
            "regiao_indicada": self.regiao_indicada, "Id": self.Id,
            "Melhorias": [serializar_item(m) for m in self.Melhorias],
            "descricao": self.descricao,
        }

    @classmethod
    def from_dict(cls, data):
        instance = cls(
            nome=data["nome"], peso=data.get("peso", data.get("pesoBase", 0)),
            nivelBalistico=data.get("nivelBalistico", data.get("nivelBalisticoBase", 0)),
            absorcoes=data.get("absorcoes", data.get("absorcoesBase", {})),
            regioes_cobertas=data.get("regioes_cobertas", []),
            durabilidade_max=data.get("durabilidadeMax", 100),
            descricao=data.get("descricao"),
        )
        instance.Id = data.get("Id", instance.Id)
        instance.durabilidade = data.get("durabilidade", instance.durabilidadeMax)
        instance.Melhorias = data.get("Melhorias", [])
        reg_indicada = data.get("regiao_indicada", None)
        if reg_indicada: instance.regiao_indicada = reg_indicada.lower()
        elif instance.regioes_cobertas: instance.regiao_indicada = instance.regioes_cobertas[0]
        else: instance.regiao_indicada = None
        instance.recalcular_atributos()
        return instance
### CLASSES DE ITEM ###
### CLASSES DE ITEM ###
### CLASSES DE ITEM ###

class KitEquipamento:
    """Kit de equipamento para NPCs."""
    RARIDADES = ["Comum", "Incomum", "Rara", "Épica", "Exótica", "Lendária"]
    def __init__(self, nome, itens=None, raridade="Comum"):
        self.nome = nome
        self.itens = itens if itens is not None else []
        
        if raridade not in self.RARIDADES:
            self.raridade = "Comum"
        else:
            self.raridade = raridade
        
        try:
            self.Id = gerar_id()
        except:
            self.Id = f"kit_{id(self)}"

    def adicionar_item(self, item, slot="inventario", quantidade=1):
        """Adiciona um item ao kit, com suporte a stacking para itens sem ID."""
        tem_id = hasattr(item, "Id") and item.Id

        if not tem_id:
            # Stackável: procura entrada existente do mesmo tipo/nome
            for entrada in self.itens:
                item_existente = entrada.get("item")
                if (item_existente and
                    item_existente.__class__.__name__ == item.__class__.__name__ and
                    getattr(item_existente, "nome", None) == getattr(item, "nome", None)):
                    entrada["quantidade"] = entrada.get("quantidade", 1) + quantidade
                    return
            # Não encontrou: cria nova entrada
            self.itens.append({"item": item, "slot": slot, "quantidade": quantidade})
        else:
            # Único (com ID): sempre adiciona como entrada separada
            self.itens.append({"item": item, "slot": slot, "quantidade": 1})

    def remover_item(self, item=None, slot=None, quantidade=1, indice=None):
        """Remove um item do kit. Pode remover por índice, por objeto ou pelo último."""

        if indice is not None:
            if 0 <= indice < len(self.itens):
                self.itens.pop(indice)
            return

        if item is not None:
            tem_id = hasattr(item, "Id") and item.Id

            if not tem_id:
                for entrada in self.itens:
                    item_existente = entrada.get("item")
                    if (item_existente and
                        item_existente.__class__.__name__ == item.__class__.__name__ and
                        getattr(item_existente, "nome", None) == getattr(item, "nome", None)):
                        qtd_atual = entrada.get("quantidade", 1)
                        if qtd_atual <= quantidade:
                            self.itens.remove(entrada)
                        else:
                            entrada["quantidade"] = qtd_atual - quantidade
                        return
            else:
                for entrada in self.itens:
                    if entrada.get("item") is item:
                        self.itens.remove(entrada)
                        return

        if self.itens:
            self.itens.pop()

    def listar_itens(self):
        result = []
        for idx, entrada in enumerate(self.itens):
            item = entrada.get("item")
            if item:
                tem_id = hasattr(item, "Id") and item.Id
                result.append({
                    "nome":       getattr(item, "nome", "Desconhecido"),
                    "quantidade": 1 if tem_id else entrada.get("quantidade", 1),
                    "tipo":       item.__class__.__name__,
                    "slot":       entrada.get("slot", "inventario"),
                    "unico":      bool(tem_id),
                    "_idx":       idx,
                    "objeto":     item,
                })
        return result

    def equipar_em(self, personagem):
        import random

        # 1. Tudo pro inventário
        for entrada in self.itens:
            item = entrada.get("item")
            if not item:
                continue
            qtd = 1 if (hasattr(item, "Id") and item.Id) else entrada.get("quantidade", 1)
            personagem.inventario.adicionar_item_objeto(item, qtd)

        # 2. Separar categorias
        rangeds   = [e["item"] for e in self.itens if isinstance(e.get("item"), Ranged)]
        melees    = [e["item"] for e in self.itens if isinstance(e.get("item"), Melee)]
        protecoes = [e["item"] for e in self.itens if isinstance(e.get("item"), Protecao)]
        municoes  = [(e["item"], e.get("quantidade", 1)) for e in self.itens if isinstance(e.get("item"), Municao)]

        # 3. Carregar munição
        for arma in rangeds:
            compativeis = [(m, qtd) for m, qtd in municoes if m.calibre == arma.calibre]
            if compativeis:
                municao_escolhida, qtd_disponivel = random.choice(compativeis)
                qtd_a_carregar = min(qtd_disponivel, arma.capacidade)
                arma.carregar_municao(municao_escolhida, qtd_a_carregar)

        # 4. Equipar armas
        arma_ranged_equipar = random.choice(rangeds) if rangeds else None
        arma_melee_equipar  = random.choice(melees)  if melees  else None

        if arma_ranged_equipar:
            personagem._equipar_arma(arma_ranged_equipar)

        if arma_melee_equipar:
            personagem._equipar_arma(arma_melee_equipar)

        # 5. Equipar proteções
        for prot in protecoes:
            regiao = getattr(prot, "regiao_indicada", None)
            if not regiao or regiao not in personagem.regioes_corpo:
                for r in getattr(prot, "regioes_cobertas", []):
                    if r in personagem.regioes_corpo:
                        prot.regiao_indicada = r
                        regiao = r
                        break
            if regiao:
                personagem._equipar_protecao_obj(prot)

    def to_dict(self):
        itens_ser = []
        for entrada in self.itens:
            item = entrada.get("item")
            if item and hasattr(item, "to_dict"):
                try:
                    tem_id = hasattr(item, "Id") and item.Id
                    itens_ser.append({
                        "item": {
                            **item.to_dict(),
                            "_classe": item.__class__.__name__
                        },
                        "slot":      entrada.get("slot"),
                        "quantidade": 1 if tem_id else entrada.get("quantidade", 1),  # ✅ salva quantidade
                    })
                except:
                    pass

        return {
            "__class__": "KitEquipamento",
            "nome":     self.nome,
            "raridade": self.raridade,
            "Id":       self.Id,
            "itens":    itens_ser
        }

    @classmethod
    def from_dict(cls, data):
        try:
            from Codigos import Ranged, Melee, Protecao, Item, Consumivel, Municao, Melhoria
        except:
            return cls(nome=data.get("nome", "Kit"), itens=[], raridade=data.get("raridade", "Comum"))

        MAPA = {
            "Ranged": Ranged, "Melee": Melee, "Protecao": Protecao,
            "Item": Item, "Consumivel": Consumivel, "Municao": Municao, "Melhoria": Melhoria
        }

        itens_rec = []
        for entrada in data.get("itens", []):
            item_data = entrada.get("item")
            slot      = entrada.get("slot")
            quantidade = entrada.get("quantidade", 1)  # ✅ restaura quantidade

            if not item_data:
                continue

            classe   = item_data.get("_classe", "Item")
            cls_item = MAPA.get(classe, Item)

            try:
                item_obj = cls_item.from_dict(item_data)
                itens_rec.append({
                    "item":      item_obj,
                    "slot":      slot,
                    "quantidade": quantidade,  # ✅
                })
            except:
                pass

        return cls(
            nome=data.get("nome", "Kit"),
            itens=itens_rec,
            raridade=data.get("raridade", "Comum")
        )

    def __str__(self):
        return f"🎒 {self.nome} ({self.raridade}) - {len(self.itens)} itens"

class NPC:
    def __init__(self, nome, nivel, classe, grupo, Forca, Agilidade, Vigor, Inteligencia, Presenca, Tatica, Poder, proficiencias_base=None, poder_inicial=None, habilidade_inicial=None, kits=None, kit_fixo=None, resistencias_base=None):
        self.nome = nome; self.nivel = nivel; self.classe = classe; self.grupo = grupo
        self.atributos = {"Forca": Forca, "Agilidade": Agilidade, "Vigor": Vigor, "Inteligencia": Inteligencia, "Presenca": Presenca, "Tatica": Tatica, "Poder": Poder}
        self.proficiencias_base = proficiencias_base or {}; self.poder_inicial = poder_inicial; self.habilidade_inicial = habilidade_inicial
        self.kits = kits or []; self.kit_fixo = kit_fixo; self.resistencias_base = resistencias_base or {}

    def gerar(self) -> "Personagem":
        nome_final = self.nome or (f"{self.classe} ({self.grupo})" if self.classe else "NPC")
        p = Personagem.CriarPersonagem(nome=nome_final, nivel=self.nivel, Forca=self.atributos["Forca"], Agilidade=self.atributos["Agilidade"], Vigor=self.atributos["Vigor"], Inteligencia=self.atributos["Inteligencia"], Presenca=self.atributos["Presenca"], Tatica=self.atributos["Tatica"], Poder=self.atributos["Poder"], proficiencias_base={nome: Proficiencia(nome, prof.atributo, nivel=prof.nivel) for nome, prof in self.proficiencias_base.items()})
        if self.poder_inicial: poderes = self.poder_inicial if isinstance(self.poder_inicial, list) else [self.poder_inicial]; [p.poderes.adicionar_poder_objeto(poder) for poder in poderes]
        if self.habilidade_inicial: habs = self.habilidade_inicial if isinstance(self.habilidade_inicial, list) else [self.habilidade_inicial]; [p.habilidades.adicionar_habilidade_objeto(hab) for hab in habs]
        for tipo, valor in self.resistencias_base.items(): p.resistencias_base[tipo] = max(-100, min(100, valor))
        kit_escolhido = self.kit_fixo or (random.choice(self.kits) if self.kits else None); kit_escolhido and kit_escolhido.equipar_em(p)
        return p

    def to_dict(self):
        return {"__class__": "NPC", "nome": self.nome, "nivel": self.nivel, "classe": self.classe, "grupo": self.grupo, **self.atributos, "proficiencias_base": {nome: (prof.to_dict() if isinstance(prof, Proficiencia) else {"nome": nome, "atributo": None, "nivel": int(prof)}) for nome, prof in self.proficiencias_base.items()}, "poder_inicial": [p.to_dict() for p in (self.poder_inicial if isinstance(self.poder_inicial, list) else ([self.poder_inicial] if self.poder_inicial else []))], "habilidade_inicial": [h.to_dict() for h in (self.habilidade_inicial if isinstance(self.habilidade_inicial, list) else ([self.habilidade_inicial] if self.habilidade_inicial else []))], "kits": [k.nome for k in self.kits], "kit_fixo": self.kit_fixo.nome if self.kit_fixo else None, "resistencias_base": self.resistencias_base}

    @classmethod
    def from_dict(cls, data, kits_disponiveis=None):
        kits_disponiveis = kits_disponiveis or {}
        proficiencias_base = {}
        for nome, p in data.get("proficiencias_base", {}).items():
            if isinstance(p, Proficiencia): proficiencias_base[nome] = p
            elif isinstance(p, dict): proficiencias_base[nome] = Proficiencia.from_dict(p)
            elif isinstance(p, (int, float)): proficiencias_base[nome] = Proficiencia(nome, None, nivel=int(p))
            else: proficiencias_base[nome] = Proficiencia(nome, None, nivel=0)
        poderes = [Poder.from_dict(p) for p in data.get("poder_inicial", [])]
        habilidades = [Habilidade.from_dict(h) for h in data.get("habilidade_inicial", [])]
        kits = [kits_disponiveis[n] for n in data.get("kits", []) if n in kits_disponiveis]
        kit_fixo = kits_disponiveis.get(data.get("kit_fixo")) if data.get("kit_fixo") else None
        resistencias_base = data.get("resistencias_base", data.get("resistencias", {}))
        return cls(nome=data["nome"], nivel=data["nivel"], classe=data.get("classe"), grupo=data.get("grupo"), Forca=data["Forca"], Agilidade=data["Agilidade"], Vigor=data["Vigor"], Inteligencia=data["Inteligencia"], Presenca=data["Presenca"], Tatica=data["Tatica"], Poder=data["Poder"], proficiencias_base=proficiencias_base, poder_inicial=poderes or None, habilidade_inicial=habilidades or None, kits=kits, kit_fixo=kit_fixo, resistencias_base=resistencias_base)
### Kits e NPC ###

### Funções de Geração ###
def Gerador(npc: NPC, nivel=None, nome=None):
    if nivel is None:
        nivel = npc.nivel

    nome_base = nome or f"{npc.classe} ({npc.grupo})"

    inimigo = Personagem.CriarPersonagem(
        nome=nome_base,
        nivel=nivel,
        Forca=npc.atributos["Forca"],
        Agilidade=npc.atributos["Agilidade"],
        Vigor=npc.atributos["Vigor"],
        Inteligencia=npc.atributos["Inteligencia"],
        Presenca=npc.atributos["Presenca"],
        Tatica=npc.atributos["Tatica"],
        Poder=npc.atributos["Poder"],
        proficiencias_base={nome: Proficiencia(nome, prof.atributo, nivel=prof.nivel) for nome, prof in npc.proficiencias_base.items()}
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

def aplicar_tags_melee(arma, atacante, BuffAcerto, BuffDano, ataque_arremesso=False, furtivo=False):
    crit_mult = arma.critico_multiplicador
    crit_valor = arma.valor_critico
    for tag in arma.tags:
        data = TAGS_MELEE.get(tag,{})
        BuffAcerto += data.get("mod_acerto",0)
        BuffDano += data.get("mod_dano",0)
        crit_mult += data.get("crit_mult_bonus",0)
        crit_valor += data.get("crit_valor_penal",0)
    if furtivo and "furtiva" in arma.tags: crit_mult = max(crit_mult,3)
    if ataque_arremesso and arma.arremessavel: BuffAcerto += atacante.proficiencias.obter_bonus("Pontaria")
    return BuffAcerto, BuffDano, crit_mult, crit_valor

### Funções de Acerto ###
### FUNÇÃO ACERTO MELEE ###
REGIOES_MELEE = ["cabeça", "rosto", "pescoço", "peito", "costas", "abdômen", "braços", "pernas"]
MULT_REGIAO_MELEE = {"cabeça": 1.5, "rosto": 1.3, "pescoço": 1.3, "peito": 1.0,"costas": 1.0, "abdômen": 1.0, "braços": 0.8, "pernas": 0.9}

def acerto_melee(atacante: "Personagem", alvo: "Personagem", rolagem: int,
                 id_arma=None, regiao="aleatoria", furtivo=False, arremesso=False,
                 BuffDano=0, DebuffDano=0, BuffAcerto=0, DebuffAcerto=0) -> dict:
    resultado = {
        "acertou": False, "critico": False, "regiao": None,
        "dano_bruto": 0, "absorcao": 0, "dano_final": 0,
        "tipo_dano": None, "efeito_critico": None,
        "efeitos_aplicados": [],
        "arremesso": arremesso, "arma_perdida": False, "log": []
    }

    # --- 1. Buscar arma ---
    arma = None
    for slot in atacante.slots.values():
        if slot.item and getattr(slot.item, "Id", None) == id_arma:
            arma = slot.item; break
    if arma is None:
        for entrada in atacante.inventario.itens:
            item = entrada.get("item") if isinstance(entrada, dict) else entrada
            if getattr(item, "Id", None) == id_arma:
                arma = item; break
    if arma is None or not isinstance(arma, Melee):
        resultado["log"].append("Arma não encontrada ou inválida."); return resultado

    tem_tag_arremesso = "arremessavel" in arma.tags

    # --- 2. Bônus de acerto ---
    acerto_total = rolagem + atacante.proficiencias.obter_bonus("Luta") + BuffAcerto - DebuffAcerto
    dificuldade = max(alvo.Bloqueio, alvo.Esquiva)

    # --- 3. Checar acerto ---
    if acerto_total < dificuldade and not furtivo:
        resultado["log"].append(f"Errou. (Acerto {acerto_total} < Dificuldade {dificuldade})")
        if arremesso:
            _remover_arma_de_atacante(atacante, arma)
            InventarioMundo.get().adicionar(arma, origem=atacante.nome, local="campo")
            resultado["arma_perdida"] = True
            resultado["log"].append(f"{arma.nome} arremessada e caiu no campo.")
        return resultado

    resultado["acertou"] = True

    # --- 4. Região ---
    regiao_final = random.choice(REGIOES_MELEE) if regiao.lower() == "aleatoria" else regiao.lower()
    resultado["regiao"] = regiao_final
    mult_regiao = MULT_REGIAO_MELEE.get(regiao_final, 1.0)

    # --- 5. Crítico ---
    crit_valor = arma.valor_critico
    crit_mult = arma.critico_multiplicador
    critou = furtivo or (rolagem >= crit_valor)
    resultado["critico"] = critou
    if critou and furtivo and "furtiva" in arma.tags:
        crit_mult = max(crit_mult, 3)

    # --- 6. Dano bruto ---
    dano_base = int(arma.dano * mult_regiao)
    if arremesso and not tem_tag_arremesso:
        dano_base = max(1, dano_base // 4)
    dano_bruto = int(dano_base * crit_mult) if critou else dano_base
    resultado["dano_bruto"] = dano_bruto
    resultado["tipo_dano"] = arma.tipo_dano

    # --- 7. Proteção ---
    protecao = alvo.regioes_corpo.get(regiao_final)
    absorcao = 0
    if protecao and arma.tipo_dano:
        dano_bruto, absorcao, _ = protecao.aplicar_dano(arma.tipo_dano, dano_bruto)
    resultado["absorcao"] = absorcao

    # --- 8. Resistência / Vulnerabilidade / Imunidade ---
    dano_pos_res = alvo.calcular_dano_recebido(dano_bruto, arma.tipo_dano) if arma.tipo_dano else dano_bruto

    # --- 9. Dano final ---
    fortitude = alvo.proficiencias.obter_bonus("Fortitude")
    dano_final = max(1, dano_pos_res + BuffDano - DebuffDano - fortitude)
    if arma.nao_letal:
        dano_final = min(dano_final, alvo.VidaAtual - 1)
    resultado["dano_final"] = dano_final
    alvo.ModificarVida(-dano_final)

    # --- 10. Registra efeito crítico (aplicação fica por conta do App) ---
    resultado["efeito_critico"] = arma.efeito_critico if critou else None

    # --- 11. Arremesso: arma vai pro alvo ---
    if arremesso:
        _remover_arma_de_atacante(atacante, arma)
        alvo.inventario.adicionar_item_objeto(arma, 1)
        resultado["log"].append(f"{arma.nome} arremessada e ficou com {alvo.nome}.")

    resultado["log"].append(
        f"({'CRÍTICO! ' if critou else ''}{regiao_final}) "
        f"Dano: {dano_final} | Bruto: {dano_bruto} | Abs: {absorcao}"
        + (f" | ¼ dano (sem tag arremessável)" if arremesso and not tem_tag_arremesso else "")
    )
    return resultado

def _remover_arma_de_atacante(atacante: "Personagem", arma: "Melee"):
    for slot in atacante.slots.values():
        if slot.item is arma:
            slot.item = None
    atacante.inventario.remover_item(arma, 1)
### FUNÇÃO ACERTO MELEE ###

### FUNÇÃO ACERTO RANGED ###
REGIOES_RANGED = ["cabeça", "rosto", "pescoço", "peito", "costas", "abdômen", "braços", "pernas"]
MULT_REGIAO_RANGED = {"cabeça": 2.0, "rosto": 2.0, "pescoço": 1.5, "peito": 1.0, "costas": 1.0, "abdômen": 1.0, "braços": 0.8, "pernas": 0.9}
COBERTURA_REGIOES_EXPOSTAS = {
    "Nenhuma": [],
    "Parcial": ["cabeça", "rosto", "pescoço", "peito", "costas"],
    "Alta": ["cabeça", "rosto", "pescoço"],
    "Total": ["cabeça", "rosto", "pescoço", "peito", "costas", "abdômen", "braços", "pernas"],
}
MATERIAL_LIMITE_PERFURACAO = {"Nenhum": 0, "Gesso": 4, "Madeira": 8, "Veiculo": 10, "Concreto": 12, "Aço": 16}

def calcular_disparos_por_tempo(tpm: int, capacidade: int, municoes_atuais: int, segundos: float) -> int:
    """Dado TPM, capacidade e tempo em segundos, retorna quantos disparos ocorrem (limitado pela munição disponível)."""
    tps = tpm / 60.0
    disparos = int(tps * segundos)
    return max(1, min(disparos, municoes_atuais))

def acerto_ranged(atacante: "Personagem", alvo: "Personagem", rolagem: int, id_arma, distancia: int, disparos: int = 1, regiao: str = "aleatoria", cobertura: str = "Nenhuma", material: str = "Nenhum", BuffAcerto: int = 0, DebuffAcerto: int = 0, BuffDano: int = 0, DebuffDano: int = 0) -> dict:
    resultado_geral = {
        "acertou_algum": False,
        "disparos_totais": disparos,
        "disparos_realizados": 0,
        "arma_nome": "",
        "modo_disparo": "",
        "municao_nome": "",
        "por_disparo": [],
        "log": []
    }

    # === 1. BUSCAR ARMA ===
    arma = None
    for slot in atacante.slots.values():
        if slot.item and getattr(slot.item, "Id", None) == id_arma:
            arma = slot.item; break
    if arma is None:
        resultado_geral["log"].append("Arma não encontrada nos slots."); return resultado_geral
    if not isinstance(arma, Ranged):
        resultado_geral["log"].append("Item selecionado não é uma arma ranged."); return resultado_geral
    if arma.munições <= 0 or arma.municao is None:
        resultado_geral["log"].append("Click... (sem munição)."); return resultado_geral

    resultado_geral["arma_nome"] = arma.nome
    resultado_geral["modo_disparo"] = arma.modo_disparo_atual
    resultado_geral["municao_nome"] = arma.municao.nome if arma.municao else "—"

    # === 2. BÔNUS BASE ===
    bonus_pontaria = atacante.proficiencias.obter_bonus("Pontaria")
    fortitude_alvo = alvo.proficiencias.obter_bonus("Fortitude")

    # === 3. PENALIDADE DE DISTÂNCIA ===
    debuff_distancia_acerto = 0
    debuff_distancia_dano = 0
    if distancia < arma.MinRange:
        debuff_distancia_acerto += arma.MinRange - distancia
    elif distancia > arma.MaxRange:
        excesso = distancia - arma.MaxRange
        debuff_distancia_acerto += excesso // 5
        debuff_distancia_dano += (excesso // 5) * 2

    # === 4. COBERTURA ===
    expostas = COBERTURA_REGIOES_EXPOSTAS.get(cobertura, REGIOES_RANGED)
    limiar_material = MATERIAL_LIMITE_PERFURACAO.get(material, 0)
    perfuracao = arma.Perfuracao

    # === 5. CRÍTICO ===
    if distancia <= 50:   crit_valor = arma.ShortCrit
    elif distancia <= 100: crit_valor = arma.MediumCrit
    else:                  crit_valor = arma.LongCrit

    # === 6. ACERTO BASE ===
    acerto_base = rolagem + bonus_pontaria + BuffAcerto - DebuffAcerto - debuff_distancia_acerto
    prob_conversao = max(5, rolagem * 4)

    disparos_a_fazer = min(disparos, arma.munições)
    resultado_geral["disparos_realizados"] = disparos_a_fazer

    for n in range(disparos_a_fazer):
        tiro = {
            "numero": n + 1,
            "regiao": None,
            "acertou": False,
            "critico": False,
            "bloqueado_cobertura": False,
            "dano_bruto": 0,
            "absorcao_armadura": 0,
            "dano_final": 0,
            "tipo_dano": arma.tipo_dano,
            "efeitos_aplicados": [],
            "log": ""
        }

        regiao_final = random.choice(REGIOES_RANGED) if regiao.lower() == "aleatoria" else regiao.lower()
        tiro["regiao"] = regiao_final

        bloqueado = (regiao_final not in expostas) and (perfuracao <= limiar_material)
        tiro["bloqueado_cobertura"] = bloqueado

        if bloqueado:
            tiro["log"] = f"Tiro {n+1} ({regiao_final}): Bloqueado pela cobertura ({material})."
            resultado_geral["por_disparo"].append(tiro)
            arma.disparar(1)
            _degradar_recuo(arma, resultado_geral)
            acerto_base -= arma.recuo
            prob_conversao = max(5, prob_conversao - arma.recuo * 4)
            continue

        chance = random.randint(1, 100)
        if chance > prob_conversao:
            tiro["log"] = f"Tiro {n+1} ({regiao_final}): Errou (recuo/estabilidade)."
            resultado_geral["por_disparo"].append(tiro)
            arma.disparar(1)
            acerto_base -= arma.recuo
            prob_conversao = max(5, prob_conversao - arma.recuo * 4)
            continue

        tiro["acertou"] = True
        resultado_geral["acertou_algum"] = True

        critou = acerto_base >= crit_valor
        tiro["critico"] = critou
        mult_regiao = MULT_REGIAO_RANGED.get(regiao_final, 1.0)
        dano_bruto = int(arma.dano * mult_regiao)
        if critou:
            dano_bruto = int(dano_bruto * 1.5)

        if regiao_final not in expostas:
            dano_bruto = int(dano_bruto * 0.6)

        absorcao_armadura = 0
        protecao = alvo.regioes_corpo.get(regiao_final)
        if protecao:
            nivel_balistico = protecao.nivelBalistico
            if perfuracao > nivel_balistico + 3:   dano_bruto = int(dano_bruto * 1.75)
            elif perfuracao > nivel_balistico + 2: dano_bruto = int(dano_bruto * 1.50)
            elif perfuracao > nivel_balistico + 1: dano_bruto = int(dano_bruto * 1.25)
            elif perfuracao < nivel_balistico - 3: dano_bruto = int(dano_bruto * 0.25)
            elif perfuracao < nivel_balistico - 2: dano_bruto = int(dano_bruto * 0.50)
            elif perfuracao < nivel_balistico - 1: dano_bruto = int(dano_bruto * 0.75)
            dano_bruto, absorcao_armadura, desgaste = protecao.aplicar_dano(arma.tipo_dano, dano_bruto)

        tiro["dano_bruto"] = dano_bruto
        tiro["absorcao_armadura"] = absorcao_armadura

        dano_pos_res = alvo.calcular_dano_recebido(dano_bruto, arma.tipo_dano) if arma.tipo_dano else dano_bruto

        dano_min = max(1, dano_bruto // 5)
        dano_final = max(dano_min, dano_pos_res + BuffDano - DebuffDano - fortitude_alvo - debuff_distancia_dano)
        tiro["dano_final"] = dano_final

        # --- Aplicar dano (efeitos ficam por conta do App) ---
        alvo.ModificarVida(-dano_final)

        tiro["log"] = (
            f"Tiro {n+1} ({'💥CRÍTICO ' if critou else ''}{regiao_final}): "
            f"Dano {dano_final} (bruto {dano_bruto} | abs {absorcao_armadura})"
        )

        resultado_geral["por_disparo"].append(tiro)
        arma.disparar(1)
        acerto_base -= arma.recuo
        prob_conversao = max(5, prob_conversao - arma.recuo * 4)

    resultado_geral["log"] = [t["log"] for t in resultado_geral["por_disparo"] if t["log"]]
    return resultado_geral

def _degradar_recuo(arma, resultado_geral):
    """Subtrai recuo acumulado (usado nos tiros bloqueados também para manter consistência)."""
    pass

def acerto_ranged_dual_wield(atacante: Personagem, alvo: Personagem, rolagem: int, id_arma_1, id_arma_2, distancia: int, disparos: int, regiao: str, BuffAcerto=0, BuffDano=0, DebuffAcerto=0, DebuffDano=0, cobertura="Nenhuma", material="Madeira"):
    resultado = "=== DUAL WIELD ===\n"
    DebuffAcerto += 3

    armas = []
    for aid in (id_arma_1, id_arma_2):
        data = atacante.equipados.obter_item_por_id(aid)
        if data and data["item"] and isinstance(data["item"], Ranged): armas.append(data["item"])
        else: resultado += f"[Erro] Arma {aid} inválida ou não equipada.\n"

    if len(armas) < 2: return resultado

    for idx, arma in enumerate(armas, start=1):
        if arma.requer_duas_maos: DebuffAcerto += 2
        arma.recuo += 2

        resultado += f"\n-- Arma {idx}: {arma.nome} ({arma.modo_disparo_atual}) --\n"
        resultado += acerto_ranged(atacante,alvo,rolagem,arma.Id,distancia,disparos,regiao,BuffAcerto=BuffAcerto,BuffDano=BuffDano,DebuffAcerto=DebuffAcerto,DebuffDano=DebuffDano,cobertura=cobertura,material=material,usando_uma_mao=True)

    return resultado
### FUNÇÃO ACERTO RANGED ###

### FUNÇÃO ACERTO EM ÁREA ###
REGIOES_EXPLOSAO = ["cabeça", "rosto", "pescoço", "peito", "costas", "abdômen", "braços", "pernas"]
MULT_REGIAO_EXPLOSAO = {
    "cabeça":  0.8,   # menor área exposta
    "rosto":   0.6,
    "pescoço": 0.5,
    "peito":   1.0,   # maior área — recebe mais
    "costas":  1.0,
    "abdômen": 0.9,
    "braços":  0.7,
    "pernas":  0.8,
}

# Cobertura bloqueia regiões (mesma lógica do ranged)
REGIOES_EXPLOSAO = ["cabeça", "rosto", "pescoço", "peito", "costas", "abdômen", "braços", "pernas"]
MULT_REGIAO_EXPLOSAO = {"cabeça":0.8,"rosto":0.6,"pescoço":0.5, "peito":1.0,"costas":1.0,"abdômen":0.9,"braços":0.7,"pernas":0.8,}
COBERTURA_REGIOES_BLOQUEADAS = {
    "Nenhuma": [],
    "Parcial": ["peito", "costas"],
    "Alta": ["peito", "costas", "abdômen", "braços"],
    "Total": ["cabeça", "rosto", "pescoço", "peito", "costas", "abdômen", "braços", "pernas"],
}
MATERIAL_NIVEL_BALISTICO = {
    "Nenhum":   0,
    "Gesso":    4,
    "Madeira":  8,
    "Veiculo":  10,
    "Concreto": 12,
    "Aço":      16,
}
SUBTIPOS_BALISTICOS = {"fragmentacao", "fragmentação"}

def _calcular_falloff(distancia: float, raio_letal: float, raio_total: float, modo: str) -> float:
    if distancia <= raio_letal:
        return 1.0
    if distancia >= raio_total:
        return 0.0
    if modo == "sem_falloff":
        return 1.0

    t = (distancia - raio_letal) / max(0.01, raio_total - raio_letal)

    if modo == "quadratico":
        return (1.0 - t) ** 2
    return 1.0 - t

def calcular_dano_explosao(
    item: Consumivel,
    atacante,
    alvos_distancias: list,
    cobertura: str = "Nenhuma",
    material: str = "Nenhum",          # <-- novo parâmetro
    BuffDano: int = 0,
    DebuffDano: int = 0,
    aplicar: bool = True,
) -> dict:
    raio_total = item.raio or 0
    if raio_total <= 0:
        return {"erro": "Item não tem raio de explosão.", "alvos": []}

    raio_letal = item.raio_letal if item.raio_letal is not None else raio_total * 0.3
    falloff    = item.falloff
    perfuracao = item.perfuracao

    bloqueadas = COBERTURA_REGIOES_BLOQUEADAS.get(cobertura, [])
    expostas   = [r for r in REGIOES_EXPLOSAO if r not in bloqueadas]

    # Nível balístico do material de cobertura (usado só para subtipos balísticos)
    nb_material = MATERIAL_NIVEL_BALISTICO.get(material, 0)

    resultado = {
        "item":       item.nome,
        "raio":       raio_total,
        "raio_letal": raio_letal,
        "falloff":    falloff,
        "cobertura":  cobertura,
        "material":   material,
        "alvos":      [],
        "log":        [],
    }

    efeitos_dano = [e for e in item.efeitos if e.get("tipo") == "dano"]

    for (alvo, distancia) in alvos_distancias:
        entrada_alvo = {
            "personagem":        alvo.nome,
            "distancia":         distancia,
            "mult_falloff":      0.0,
            "atingido":          False,
            "regioes":           [],
            "dano_total":        0,
            "efeitos_aplicados": [],
            "log":               "",
        }

        if distancia > raio_total:
            entrada_alvo["log"] = f"{alvo.nome} (dist {distancia}m): fora do raio."
            resultado["alvos"].append(entrada_alvo)
            resultado["log"].append(entrada_alvo["log"])
            continue

        mult_falloff = _calcular_falloff(distancia, raio_letal, raio_total, falloff)
        entrada_alvo["mult_falloff"] = round(mult_falloff, 3)
        entrada_alvo["atingido"] = True

        dano_total_alvo = 0

        for efeito in efeitos_dano:
            valor_base = efeito.get("valor", 0)
            subtipo    = efeito.get("subtipo", "")
            tipo_dano  = SUBTIPO_PARA_TIPO_DANO.get(subtipo, subtipo)

            # --- Verifica se é subtipo balístico (ex: fragmentação) ---
            eh_balistico = subtipo.lower() in SUBTIPOS_BALISTICOS

            # Multiplicador de penetração contra o material de cobertura
            # Só se aplica a dano balístico e se há algum material de cobertura
            mult_penetracao_cobertura = 1.0
            if eh_balistico and material != "Nenhum":
                if perfuracao > nb_material + 3:
                    mult_penetracao_cobertura = 1.75
                elif perfuracao > nb_material + 2:
                    mult_penetracao_cobertura = 1.50
                elif perfuracao > nb_material + 1:
                    mult_penetracao_cobertura = 1.25
                elif perfuracao < nb_material - 3:
                    mult_penetracao_cobertura = 0.25
                elif perfuracao < nb_material - 2:
                    mult_penetracao_cobertura = 0.50
                elif perfuracao < nb_material - 1:
                    mult_penetracao_cobertura = 0.75
                # perfuracao ≈ nb_material → mult permanece 1.0

            dano_total_base = int(valor_base * mult_falloff * mult_penetracao_cobertura) + BuffDano - DebuffDano
            if dano_total_base <= 0 or not expostas:
                continue

            # Distribui o dano APENAS pelas regiões expostas.
            # O peso de cada região é relativo à soma dos pesos das expostas —
            # as regiões bloqueadas simplesmente não recebem dano (não redistribuem).
            soma_pesos = sum(MULT_REGIAO_EXPLOSAO.get(r, 1.0) for r in expostas)

            for regiao in expostas:
                peso        = MULT_REGIAO_EXPLOSAO.get(regiao, 1.0)
                dano_regiao = int(dano_total_base * (peso / soma_pesos))
                if dano_regiao <= 0:
                    continue

                absorcao = 0
                protecao = alvo.regioes_corpo.get(regiao)
                if protecao and hasattr(protecao, "nivelBalistico"):
                    nb = protecao.nivelBalistico
                    if perfuracao > nb + 3:   dano_regiao = int(dano_regiao * 1.75)
                    elif perfuracao > nb + 2: dano_regiao = int(dano_regiao * 1.50)
                    elif perfuracao > nb + 1: dano_regiao = int(dano_regiao * 1.25)
                    elif perfuracao < nb - 3: dano_regiao = int(dano_regiao * 0.25)
                    elif perfuracao < nb - 2: dano_regiao = int(dano_regiao * 0.50)
                    elif perfuracao < nb - 1: dano_regiao = int(dano_regiao * 0.75)
                    if hasattr(protecao, "aplicar_dano"):
                        dano_regiao, absorcao, _ = protecao.aplicar_dano(tipo_dano, dano_regiao)

                dano_final = max(0, alvo.calcular_dano_recebido(dano_regiao, tipo_dano) if tipo_dano else dano_regiao)
                if aplicar and dano_final > 0:
                    alvo.ModificarVida(-dano_final)

                dano_total_alvo += dano_final
                entrada_alvo["regioes"].append({
                    "regiao":                  regiao,
                    "tipo_dano":               tipo_dano,
                    "mult_penetracao_cobertura": mult_penetracao_cobertura,
                    "dano_bruto":              dano_regiao,
                    "absorcao":                absorcao,
                    "dano_final":              dano_final,
                })

        entrada_alvo["dano_total"] = dano_total_alvo
        entrada_alvo["log"] = (
            f"{alvo.nome} (dist {distancia}m | x{mult_falloff:.2f}): "
            f"Dano total {dano_total_alvo}"
        )

        resultado["alvos"].append(entrada_alvo)
        resultado["log"].append(entrada_alvo["log"])

    return resultado

def usar_consumivel(
    item: Consumivel,
    usuario,
    alvo=None,
    alvos_distancias: list = None,
    cobertura: str = "Nenhuma",
    BuffDano: int = 0,
    DebuffDano: int = 0,
    aplicar: bool = True,
) -> dict:
    resultado = {
        "item":           item.nome,
        "uso":            item.uso,
        "usuario":        usuario.nome,
        "eh_area":        item.eh_area(),
        "resultado_area": None,
        "efeitos_diretos": [],
        "log":            [],
    }

    alvo_direto = alvo or usuario

    if item.eh_area():
        if not alvos_distancias:
            resultado["log"].append(f"[AVISO] {item.nome} é de área mas nenhum alvo/distância foi fornecido.")
            return resultado

        res = calcular_dano_explosao(
            item=item, atacante=usuario,
            alvos_distancias=alvos_distancias,
            cobertura=cobertura,
            BuffDano=BuffDano, DebuffDano=DebuffDano,
            aplicar=aplicar,
        )
        resultado["resultado_area"] = res
        resultado["log"].extend(res.get("log", []))

        if aplicar:
            if usuario.inventario.remover_item(item, 1):
                resultado["log"].append(f"{usuario.nome} consumiu {item.nome}.")
            else:
                resultado["log"].append(f"[ERRO] Falha ao consumir {item.nome}.")
        return resultado

    # Consumível direto — efeitos de status ficam por conta do App
    # Processa apenas efeitos de dano/cura/energia/mana diretos
    if aplicar:
        for efeito in item.efeitos:
            tipo = efeito.get("tipo", "")
            if tipo == "cura":
                alvo_direto.ModificarVida(efeito.get("valor", 0))
                resultado["log"].append(f"Curou {efeito.get('valor', 0)} de vida.")
                resultado["efeitos_diretos"].append({"tipo": tipo, "aplicado": True})
            elif tipo == "energia":
                alvo_direto.ModificarEnergia(efeito.get("valor", 0))
                resultado["log"].append(f"Restaurou {efeito.get('valor', 0)} de energia.")
                resultado["efeitos_diretos"].append({"tipo": tipo, "aplicado": True})
            elif tipo == "mana":
                alvo_direto.ModificarMana(efeito.get("valor", 0))
                resultado["log"].append(f"Restaurou {efeito.get('valor', 0)} de mana.")
                resultado["efeitos_diretos"].append({"tipo": tipo, "aplicado": True})
            elif tipo == "dano":
                subtipo   = efeito.get("subtipo", "")
                tipo_dano = SUBTIPO_PARA_TIPO_DANO.get(subtipo, subtipo)
                valor     = efeito.get("valor", 0)
                dano_final = alvo_direto.calcular_dano_recebido(valor, tipo_dano) if tipo_dano else valor
                alvo_direto.ModificarVida(-dano_final)
                resultado["log"].append(f"Causou {dano_final} de dano ({tipo_dano}).")
                resultado["efeitos_diretos"].append({"tipo": tipo, "aplicado": True})

        if usuario.inventario.remover_item(item, 1):
            resultado["log"].append(f"{usuario.nome} consumiu {item.nome}.")
        else:
            resultado["log"].append(f"[ERRO] Falha ao consumir {item.nome}.")

    return resultado
### FUNÇÃO ACERTO EM ÁREA ###

### Funções de Habilidade/Poder ###
REGIOES_PH = ["cabeça", "rosto", "pescoço", "peito", "costas", "abdômen", "braços", "pernas"]
MULT_REGIAO_PH = {"cabeça": 0.8, "rosto": 0.6, "pescoço": 0.5, "peito": 1.0,  "costas": 1.0, "abdômen": 0.9, "braços": 0.7, "pernas": 0.8}

def _aplicar_dano_ph(ph, alvo: "Personagem", regiao: str,buff_dano: int = 0, debuff_dano: int = 0) -> Tuple[int, int]:
    """Aplica danos de um poder/habilidade a uma região do alvo. Retorna (dano_final, absorcao)."""
    mult = MULT_REGIAO_PH.get(regiao, 1.0)
    protecao = alvo.regioes_corpo.get(regiao) if hasattr(alvo, "regioes_corpo") else None
    fortitude = alvo.proficiencias.obter_bonus("Fortitude") if hasattr(alvo, "proficiencias") else 0

    dano_total = 0
    abs_total  = 0
    for entrada in ph.dano:
        tipo  = entrada.get("tipo")
        valor = int(entrada.get("valor", 0) * mult)
        if valor <= 0:
            continue

        absorcao = 0
        if protecao and tipo:
            valor, absorcao, _ = protecao.aplicar_dano(tipo, valor)
        abs_total += absorcao

        if tipo and not ph.ignora_resistencias:
            valor = alvo.calcular_dano_recebido(valor, tipo)

        dano_final = max(1, valor + buff_dano - debuff_dano - fortitude)
        dano_total += dano_final
        alvo.ModificarVida(-dano_final)

    return dano_total, abs_total

def _aplicar_efeitos_ph(ph, alvo: "Personagem") -> List[str]:
    """Aplica efeitos do poder/habilidade ao alvo com chance individual."""
    banco = {}
    try:
        import Dados as D
        banco = D.carregar_buffs_debuffs()
    except Exception:
        pass

    aplicados = []
    for ef in getattr(ph, "efeitos", []):
        chance = ef.get("chance", 100)
        if random.randint(1, 100) > chance:
            continue
        nome    = ef.get("nome", "Efeito")
        duracao = ef.get("duracao", 1)
        dados_banco = banco.get(nome, {})
        bb = BuffDebuff(
            nome=nome, duracao=duracao,
            efeito=dados_banco.get("efeito", []),
            descricao=dados_banco.get("descricao", ""),
            tipo=dados_banco.get("tipo", "debuff"),
        )
        alvo.buffs_debuffs.adicionar_efeito_objeto(bb)
        aplicados.append(nome)
    return aplicados

def acerto_poder_habilidade(ph: Union["PoderOfensivo", "HabilidadeOfensiva"], usuario: "Personagem",alvos: List["Personagem"],regiao: str = "aleatoria",BuffDano: int = 0,DebuffDano: int = 0,) -> dict:
    """
    Executa um PoderOfensivo ou HabilidadeOfensiva.
    Sem rolagem de acerto, sem distância, sem cobertura.
    Aplica dano por região + resistências + absorção de armadura.
    Pode atingir múltiplos alvos.
    """
    resultado = {
        "nome": ph.nome,
        "usuario": usuario.nome,
        "sucesso": False,
        "alvos": [],
        "log": [],
    }

    pode, motivo = ph.pode_usar(usuario)
    if not pode:
        resultado["log"].append(motivo)
        return resultado

    ph.consumir_recursos(usuario)
    resultado["sucesso"] = True

    for alvo in alvos:
        regiao_final = random.choice(REGIOES_PH) if regiao == "aleatoria" else regiao.lower()
        dano_total, absorcao = _aplicar_dano_ph(ph, alvo, regiao_final, BuffDano, DebuffDano)
        efeitos = _aplicar_efeitos_ph(ph, alvo)

        entrada = {
            "alvo":     alvo.nome,
            "regiao":   regiao_final,
            "dano":     dano_total,
            "absorcao": absorcao,
            "efeitos":  efeitos,
        }
        resultado["alvos"].append(entrada)

        log = f"{alvo.nome} ({regiao_final}): {dano_total} dano | abs {absorcao}"
        if efeitos:
            log += f" | Efeitos: {', '.join(efeitos)}"
        resultado["log"].append(log)

    return resultado
### Funções de Habilidade/Poder ###

# FUNÇÃO ACERTO DESARMADO #
def acerto_desarmado(atacante: "Personagem", alvo: "Personagem", rolagem: int,regiao: str = "aleatoria", furtivo: bool = False,BuffDano: int = 0, DebuffDano: int = 0,BuffAcerto: int = 0, DebuffAcerto: int = 0) -> dict:
    resultado = {
        "acertou": False, "critico": False, "regiao": None,
        "dano_bruto": 0, "absorcao": 0, "dano_final": 0,
        "tipo_dano": "contundente", "efeito_critico": None,
        "efeitos_aplicados": [], "log": []
    }

    # --- 1. Parâmetros do ataque desarmado (dano, crit_mult, crit_valor) ---
    params = atacante.calcular_ataque_desarmado()
    dano_base_calc = params["dano"]
    crit_mult      = params["crit_mult"]
    crit_valor     = params["crit_valor"]

    # --- 2. Bônus de acerto ---
    acerto_total = rolagem + atacante.proficiencias.obter_bonus("Luta") + BuffAcerto - DebuffAcerto
    dificuldade  = max(alvo.Bloqueio, alvo.Esquiva)

    # --- 3. Checar acerto ---
    if acerto_total < dificuldade and not furtivo:
        resultado["log"].append(f"Errou. (Acerto {acerto_total} < Dificuldade {dificuldade})")
        return resultado

    resultado["acertou"] = True

    # --- 4. Região ---
    regiao_final = random.choice(REGIOES_MELEE) if regiao.lower() == "aleatoria" else regiao.lower()
    resultado["regiao"] = regiao_final
    mult_regiao = MULT_REGIAO_MELEE.get(regiao_final, 1.0)

    # --- 5. Crítico ---
    critou = furtivo or (rolagem >= crit_valor)
    resultado["critico"] = critou
    if critou and furtivo:
        crit_mult = max(crit_mult, 3)

    # --- 6. Dano bruto ---
    dano_base = int(dano_base_calc * mult_regiao)
    dano_bruto = int(dano_base * crit_mult) if critou else dano_base
    resultado["dano_bruto"] = dano_bruto

    # --- 7. Proteção ---
    protecao = alvo.regioes_corpo.get(regiao_final)
    absorcao = 0
    if protecao:
        dano_bruto, absorcao, _ = protecao.aplicar_dano("contundente", dano_bruto)
    resultado["absorcao"] = absorcao

    # --- 8. Resistência / Vulnerabilidade / Imunidade ---
    dano_pos_res = alvo.calcular_dano_recebido(dano_bruto, "contundente")

    # --- 9. Dano final ---
    fortitude  = alvo.proficiencias.obter_bonus("Fortitude")
    dano_final = max(1, dano_pos_res + BuffDano - DebuffDano - fortitude)
    resultado["dano_final"] = dano_final
    alvo.ModificarVida(-dano_final)

    # --- 10. Efeito crítico ---
    resultado["efeito_critico"] = "atordoar" if critou else None

    resultado["log"].append(
        f"({'CRÍTICO! ' if critou else ''}{regiao_final}) "
        f"Dano: {dano_final} | Bruto: {dano_bruto} | Abs: {absorcao}"
    )
    return resultado
# FUNÇÃO ACERTO DESARMADO #
### Funções de Acerto ###

### Tags melee ###
TAGS_MELEE = {
    "cortante": {"tipo_dano":"cortante","efeito_critico":"sangramento","vs_desprotegido":1},
    "perfurante": {"tipo_dano":"perfurante","ignora_armadura":3,"crit_mult_bonus":1,"crit_valor_penal":2},
    "concussivo": {"tipo_dano":"concussiva","efeito_critico":"atordoar","mod_dano":-2},

    "leve": {"mod_dano":-2,"crit_valor":-2,"mod_acerto":1, },
    "balanceada": {},
    "pesada": {"mod_dano":5,"crit_valor":2,"mod_acerto":-1},

    "uma_mao": {"maos":1},
    "duas_maos": {"maos":2},

    "alcance_curto": {"alcance":1},
    "alcance_medio": {"alcance":2},
    "alcance_longo": {"alcance":3},

    "sofisticada": {"usa_agilidade":True},
    "arremessavel": {"arremessavel":True},
    "furtiva": {"furtiva":True},
    "nao_letal": {"nao_letal":True}
}
### Tags melee ###