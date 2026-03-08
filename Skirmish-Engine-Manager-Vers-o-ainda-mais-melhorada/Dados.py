from Codigos import (
    Personagem, Ranged, Melee, Protecao, Item, BuffDebuff,
    Consumivel, Municao, Melhoria, Equipamento, Poder, Habilidade,
    Proficiencia, NPC, KitEquipamento, gerar_id
)

import json
import os
from typing import Dict, Any
from datetime import datetime

### JSON ###
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "dados")
os.makedirs(BASE_PATH, exist_ok=True)

ARQUIVOS_JSON = {
    "Itens": "itens.json",
    "Consumiveis": "consumiveis.json",
    "Municoes": "municoes.json",
    "Melhorias": "melhorias.json",
    "Equipamentos": "equipamentos.json",
    "Rangeds": "rangeds.json",
    "Melees": "melees.json",
    "Protecoes": "protecoes.json",
    "Proficiencias": "proficiencias.json",
    "Poderes": "poderes.json",
    "Habilidades": "habilidades.json",
    "BuffsDebuffs": "buffs_debuffs.json",
    "NPCs": "npcs.json",
    "sessoes": "sessoes.json"
}

def _load_json(nome_arquivo: str) -> Dict[str, Any]:
    caminho = os.path.join(BASE_PATH, nome_arquivo)
    if not os.path.exists(caminho):
        return {}

    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar {nome_arquivo}: {e}")
        return {}

def _save_json(nome_arquivo: str, dados: Dict[str, Any]) -> bool:
    caminho = os.path.join(BASE_PATH, nome_arquivo)
    try:
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar {nome_arquivo}: {e}")
        return False
### JSON ###

### Carregar ###
def carregar_por_classe(arquivo, classe):
    dados = _load_json(arquivo)
    return {nome: classe.from_dict(data) for nome, data in dados.items()}

def carregar_itens(): return carregar_por_classe("itens.json", Item)

def carregar_consumiveis(): return carregar_por_classe("consumiveis.json", Consumivel)

def carregar_municoes(): return carregar_por_classe("municoes.json", Municao)

def carregar_melhorias(): return carregar_por_classe("melhorias.json", Melhoria)

def carregar_equipamentos(): return carregar_por_classe("equipamentos.json", Equipamento)

def carregar_rangeds(): return carregar_por_classe("rangeds.json", Ranged)

def carregar_melees(): return carregar_por_classe("melees.json", Melee)

def carregar_protecoes(): return carregar_por_classe("protecoes.json", Protecao)

def carregar_proficiencias():
    dados = _load_json("proficiencias.json")
    return {nome: deserialize_object_with_class(data) for nome, data in dados.items()}

def carregar_habilidades():
    dados = _load_json("habilidades.json")
    return {nome: deserialize_object_with_class(data) for nome, data in dados.items()}

def carregar_poderes():
    dados = _load_json("poderes.json")
    return {nome: deserialize_object_with_class(data) for nome, data in dados.items()}

def carregar_buffs_debuffs():
    dados = _load_json("buffs_debuffs.json")
    return {nome: deserialize_object_with_class(data) for nome, data in dados.items()}

def carregar_npcs():
    dados = _load_json("npcs.json")
    kits = carregar_kits()  # necessário para recompor os kits do NPC
    resultado = {}
    for nome, data in dados.items():
        try:
            resultado[nome] = NPC.from_dict(data, kits_disponiveis=kits)
        except Exception as e:
            print(f"[carregar_npcs] ⚠️ Erro ao carregar NPC '{nome}': {e}")
    return resultado

def carregar_todos_dados():
    return {
        "Itens": carregar_itens(),
        "Municoes": carregar_municoes(),
        "Melhorias": carregar_melhorias(),
        "Rangeds": carregar_rangeds(),
        "Melees": carregar_melees(),
        "Protecoes": carregar_protecoes(),
        "Proficiencias": carregar_proficiencias(),
        "Poderes": carregar_poderes(),
        "Habilidades": carregar_habilidades(),
        "BuffsDebuffs": carregar_buffs_debuffs(),
        "Kits": carregar_kits(),
        "Npcs": carregar_npcs(),
    }

def carregar_tabela_especifica(nome_tabela):
    tabelas_disponiveis = {
        "Itens": carregar_itens,
        "Municoes": carregar_municoes,
        "Melhorias": carregar_melhorias,
        "Rangeds": carregar_rangeds,
        "Melees": carregar_melees,
        "Protecoes": carregar_protecoes,
        "Consumiveis": carregar_consumiveis,
        "Equipamentos": carregar_equipamentos,
        "Proficiencias": carregar_proficiencias,
        "Poderes": carregar_poderes,
        "Habilidades": carregar_habilidades,
        "BuffsDebuffs": carregar_buffs_debuffs,
        "Kits": carregar_kits,
        "Npcs": carregar_npcs,
    }

    if nome_tabela in tabelas_disponiveis:
        return tabelas_disponiveis[nome_tabela]()
    else:
        print(f"Tabela '{nome_tabela}' não encontrada.")
        return {}

def carregar_item_por_nome(nome_item):
    tabelas_itens = {
        "Itens": carregar_itens,
        "Municoes": carregar_municoes,
        "Melhorias": carregar_melhorias,
        "Rangeds": carregar_rangeds,
        "Melees": carregar_melees,
        "Protecoes": carregar_protecoes
    }

    nome_item_lower = nome_item.lower()

    for tabela_nome, funcao_carregar in tabelas_itens.items():
        dados_tabela = funcao_carregar()
        for chave, item in dados_tabela.items():
            if chave.lower() == nome_item_lower:
                print(f"✅ Item '{nome_item}' encontrado na tabela {tabela_nome}")
                return item

    print(f"❌ Item '{nome_item}' não encontrado em nenhuma tabela")
    return None
### Carregar ###

### salvar/editar/remover ###
def salvar_generico(obj, arquivo):
    data = _load_json(arquivo)
    obj_data = serializar_objeto(obj)
    nome = obj_data.get("nome")

    if not nome:
        raise ValueError("Objeto sem nome não pode ser salvo")

    data[nome] = obj_data
    _save_json(arquivo, data)
    return obj

def editar_generico(nome, novos_dados, arquivo):
    data = _load_json(arquivo)
    if nome not in data:
        return None

    data[nome].update(novos_dados)
    _save_json(arquivo, data)
    return data[nome]

def remover_generico(nome, arquivo):
    data = _load_json(arquivo)
    if nome in data:
        del data[nome]
        _save_json(arquivo, data)
        return True
    return False

def salvar_npc(npc: NPC):
    dados = _load_json("npcs.json")
    dados[npc.nome] = npc.to_dict()
    _save_json("npcs.json", dados)
    return True

def remover_npc(nome: str):
    return remover_generico(nome, "npcs.json")
### salvar/editar/remover ###

### serialização ###
MAPA_CLASSES = {
    "Item": Item,
    "Consumivel": Consumivel,
    "Municao": Municao,
    "Melee": Melee,
    "Ranged": Ranged,
    "Protecao": Protecao,
    "Equipamento": Equipamento,
    "Melhoria": Melhoria,
    "BuffDebuff": BuffDebuff,
    "Poder": Poder,           # ← novo
    "Habilidade": Habilidade, # ← novo
    "Proficiencia": Proficiencia, # ← novo
    "NPC": NPC,               # ← novo
}

def deserialize_object_with_class(obj):
    if isinstance(obj, (int, float, str, bool)) or obj is None:
        return obj

    if isinstance(obj, list):
        return [deserialize_object_with_class(i) for i in obj]

    if isinstance(obj, dict):
        raw_class = obj.get("__class__")
        cls = MAPA_CLASSES.get(raw_class)

        if cls and hasattr(cls, "from_dict"):
            data = {
                k: deserialize_object_with_class(v)
                for k, v in obj.items()
                if k != "__class__"
            }
            return cls.from_dict(data)

        return {
            k: deserialize_object_with_class(v)
            for k, v in obj.items()
        }

    return obj

def serializar_objeto(obj):
    if obj is None or isinstance(obj,(int,float,str,bool)): return obj
    if isinstance(obj,list): return [serializar_objeto(i) for i in obj]
    if isinstance(obj,dict): return {k:serializar_objeto(v) for k,v in obj.items()}
    if hasattr(obj,"to_dict"):
        data=obj.to_dict()
        if not isinstance(data,dict): raise TypeError(f"to_dict() inválido em {type(obj)}")
        data={k:serializar_objeto(v) for k,v in data.items()}
        data["__class__"]=obj.__class__.__name__
        return data
    if hasattr(obj,"__dict__"):
        data={k:serializar_objeto(v) for k,v in obj.__dict__.items() if not k.startswith("_")}
        data["__class__"]=obj.__class__.__name__
        return data
    raise TypeError(f"Objeto não serializável: {type(obj)}")

def deserializar_objeto(obj):
    return deserialize_object_with_class(obj)

def reconstruct_item_from_data(item_data):
    return deserialize_object_with_class(item_data)
### serialização ###

# === SISTEMA DE SESSÕES === #
GruposDePersonagens = {}
KitsDisponíveis = []
EstadoCombate = {}
LogCombate    = []
EstadoMapa    = {}

def salvar_sessao(nome_da_sessao, sobrescrever=False):
    """Salva a sessão atual no arquivo sessoes.json"""
    try:
        arquivo = "sessoes.json"
        dados = _load_json(arquivo)
        
        if nome_da_sessao in dados and not sobrescrever:
            print(f"⚠️ Sessão '{nome_da_sessao}' já existe. Use sobrescrever=True para atualizar.")
            return False
        
        dados_sessao = {}

        # ── Grupos de personagens ─────────────────────────────────────────
        for grupo, lista in GruposDePersonagens.items():
            dados_sessao[grupo] = []
            for personagem in lista:
                if hasattr(personagem, 'to_dict'):
                    dados_personagem = personagem.to_dict()
                else:
                    dados_personagem = vars(personagem)
                dados_sessao[grupo].append(serializar_objeto(dados_personagem))
        
        # ── Kits disponíveis ─────────────────────────────────────────────
        if KitsDisponíveis:
            dados_sessao["__kits_disponiveis__"] = serializar_objeto(KitsDisponíveis)

        # ── Estado de combate ─────────────────────────────────────────────
        if EstadoCombate:
            dados_sessao["__estado_combate__"] = serializar_objeto(EstadoCombate)

        # ── Log de combate ────────────────────────────────────────────────
        if LogCombate:
            dados_sessao["__log_combate__"] = serializar_objeto(LogCombate)

        # ── Estado do mapa ────────────────────────────────────────────────
        if EstadoMapa:
            # img_original é PIL.Image — não pode serializar. Remove antes de salvar.
            estado_mapa_serializavel = {k: v for k, v in EstadoMapa.items() if k != "img_original"}
            dados_sessao["__estado_mapa__"] = serializar_objeto(estado_mapa_serializavel)
        
        dados[nome_da_sessao] = {
            "conteudo": dados_sessao,
            "data_criacao": datetime.utcnow().isoformat()
        }
        
        if _save_json(arquivo, dados):
            print(f"✅ Sessão '{nome_da_sessao}' salva com sucesso")
            return True
        else:
            return False
        
    except Exception as e:
        import traceback
        print(f"❌ Erro ao salvar sessão: {e}")
        traceback.print_exc()
        return False

def carregar_sessao(nome_da_sessao):
    """Carrega uma sessão do arquivo sessoes.json"""
    global LogCombate,GruposDePersonagens,KitsDisponíveis,EstadoCombate,EstadoMapa
    import traceback
    if LogCombate is None: LogCombate=[]
    try:
        print(f"🔄 Carregando sessão '{nome_da_sessao}'...")
        dados=_load_json("sessoes.json")
        if nome_da_sessao not in dados:
            print(f"❌ Sessão '{nome_da_sessao}' não encontrada")
            return False

        dados_sessao=dados[nome_da_sessao]["conteudo"]
        print("🔄 Reconstruindo personagens e equipamentos...")

        GruposDePersonagens={}
        personagens_carregados=0
        personagens_com_erro=0

        for grupo,lista_personagens in dados_sessao.items():

            if grupo=="__kits_disponiveis__":
                try:
                    KitsDisponíveis=deserializar_objeto(lista_personagens)
                    print(f"📦 {len(KitsDisponíveis)} kits carregados")
                except Exception as e:
                    print(f"⚠️ Erro ao carregar kits: {e}")
                    traceback.print_exc()
                continue

            if grupo=="__estado_combate__":
                try:
                    EstadoCombate.clear(); EstadoCombate.update(deserializar_objeto(lista_personagens))
                    print("⚔️ Estado de combate carregado")
                except Exception as e:
                    print(f"⚠️ Erro ao carregar estado de combate: {e}")
                    traceback.print_exc()
                continue

            if grupo=="__log_combate__":
                try:
                    dados_log=deserializar_objeto(lista_personagens)
                    if dados_log is None: dados_log=[]
                    if LogCombate is None: LogCombate=[]
                    LogCombate.clear(); LogCombate.extend(dados_log)
                    print(f"📋 {len(LogCombate)} entradas de log carregadas")
                except Exception as e:
                    print(f"⚠️ Erro ao carregar log: {e}")
                    traceback.print_exc()
                continue

            if grupo=="__estado_mapa__":
                try:
                    EstadoMapa.clear(); EstadoMapa.update(deserializar_objeto(lista_personagens))
                    print("🗺 Estado do mapa carregado")
                except Exception as e:
                    print(f"⚠️ Erro ao carregar mapa: {e}")
                    traceback.print_exc()
                continue

            if grupo not in GruposDePersonagens: GruposDePersonagens[grupo]=[]

            for idx,dados_personagem in enumerate(lista_personagens):
                try:
                    print(f"  👤 Carregando personagem {idx+1}...")
                    dados_deserializados=deserializar_objeto(dados_personagem)
                    if hasattr(Personagem,'from_dict'): personagem=Personagem.from_dict(dados_deserializados)
                    else:
                        personagem=Personagem(); [setattr(personagem,attr,valor) for attr,valor in dados_deserializados.items() if not attr.startswith('__')]
                    GruposDePersonagens[grupo].append(personagem)
                    personagens_carregados+=1
                    print(f"    ✅ {getattr(personagem,'nome','Sem nome')} carregado")
                except Exception as e:
                    print(f"    ❌ Erro ao carregar personagem {idx+1}: {e}")
                    traceback.print_exc()
                    personagens_com_erro+=1
                    continue

        print(f"\n{'='*60}")
        print("✅ Sessão carregada:")
        print(f"   • {len(GruposDePersonagens)} grupos")
        print(f"   • {personagens_carregados} personagens carregados")
        if personagens_com_erro>0: print(f"   ⚠️  {personagens_com_erro} personagens com erro")
        print(f"{'='*60}\n")

        return True

    except Exception as e:
        print(f"❌ ERRO CRÍTICO ao carregar sessão: {e}")
        traceback.print_exc()
        return False

def validar_sessao(nome_da_sessao):
    """Valida se uma sessão pode ser carregada corretamente"""
    try:
        dados = _load_json("sessoes.json")
        
        if nome_da_sessao not in dados:
            return False, "Sessão não encontrada"
        
        dados_sessao = dados[nome_da_sessao]["conteudo"]
        
        if not isinstance(dados_sessao, dict):
            return False, "Estrutura de dados inválida"
        
        total_personagens = 0
        problemas = []
        
        for grupo, lista in dados_sessao.items():
            if grupo == "__kits_disponiveis__":
                continue
                
            if not isinstance(lista, list):
                problemas.append(f"Grupo '{grupo}' não é uma lista")
                continue
                
            for i, dados_personagem in enumerate(lista):
                try:
                    deserializar_objeto(dados_personagem)
                    total_personagens += 1
                except Exception as e:
                    problemas.append(f"Erro no personagem {i+1} do grupo '{grupo}': {str(e)}")
        
        if problemas:
            return False, f"Problemas encontrados: {'; '.join(problemas[:3])}"
        
        grupos_validos = len([g for g in dados_sessao.keys() if g != '__kits_disponiveis__'])
        return True, f"Sessão válida: {total_personagens} personagens em {grupos_validos} grupos"
        
    except Exception as e:
        return False, f"Erro na validação: {e}"

def listar_sessoes():
    """
    Retorna lista de dicts com info de cada sessão salva.
    Cada dict: {"nome": str, "total_personagens": int, "total_grupos": int, "data_criacao": str}
    """
    try:
        dados = _load_json("sessoes.json")
        resultado = []

        for nome_sessao, conteudo_sessao in dados.items():
            try:
                dados_sessao = conteudo_sessao.get("conteudo", {})
                data_criacao = conteudo_sessao.get("data_criacao", "")

                # Conta grupos e personagens (ignora chaves internas __)
                grupos = [g for g in dados_sessao.keys() if not g.startswith("__")]
                total_grupos = len(grupos)
                total_personagens = sum(
                    len(lista) for g, lista in dados_sessao.items()
                    if not g.startswith("__") and isinstance(lista, list)
                )

                resultado.append({
                    "nome":               nome_sessao,
                    "total_personagens":  total_personagens,
                    "total_grupos":       total_grupos,
                    "data_criacao":       data_criacao,
                })
            except Exception as e:
                print(f"⚠️ Erro ao processar sessão '{nome_sessao}': {e}")
                continue

        return resultado

    except Exception as e:
        print(f"❌ Erro ao listar sessões: {e}")
        return []

def deletar_sessao(nome_da_sessao):
    """Remove uma sessão do arquivo sessoes.json"""
    try:
        arquivo = "sessoes.json"
        dados = _load_json(arquivo)

        if nome_da_sessao not in dados:
            print(f"❌ Sessão '{nome_da_sessao}' não encontrada")
            return False

        del dados[nome_da_sessao]

        if _save_json(arquivo, dados):
            print(f"✅ Sessão '{nome_da_sessao}' deletada com sucesso")
            return True
        else:
            return False

    except Exception as e:
        print(f"❌ Erro ao deletar sessão: {e}")
        return False

def clonar_sessao(nome_original, nome_novo):
    """
    Copia uma sessão com um novo nome.
    Usado internamente pela função renomear (clone + delete).
    """
    try:
        arquivo = "sessoes.json"
        dados = _load_json(arquivo)

        if nome_original not in dados:
            print(f"❌ Sessão original '{nome_original}' não encontrada")
            return False

        if nome_novo in dados:
            print(f"❌ Já existe uma sessão com o nome '{nome_novo}'")
            return False

        import copy
        dados[nome_novo] = copy.deepcopy(dados[nome_original])
        # Atualiza a data de criação do clone
        dados[nome_novo]["data_criacao"] = datetime.utcnow().isoformat()

        if _save_json(arquivo, dados):
            print(f"✅ Sessão '{nome_original}' clonada como '{nome_novo}'")
            return True
        else:
            return False

    except Exception as e:
        print(f"❌ Erro ao clonar sessão: {e}")
        return False
# === SISTEMA DE SESSÕES === #

# === SISTEMA DE KITS === #
def carregar_kits():
    dados = _load_json("kits.json") or {}
    if isinstance(dados, dict):
        from Codigos import KitEquipamento
        return {
            nome: KitEquipamento.from_dict(data) 
            for nome, data in dados.items()
        }
    return {}

def salvar_kit_no_banco(kit):
    """✅ NOVO NOME (era: salvar_kit)"""
    dados = _load_json("kits.json") or {}
    dados[kit.nome] = kit.to_dict()
    return _save_json("kits.json", dados)

def deletar_kit_do_banco(nome):
    """✅ NOVO NOME (era: deletar_kit)"""
    dados = _load_json("kits.json") or {}
    if nome in dados:
        del dados[nome]
        return _save_json("kits.json", dados)
    return False

def carregar_kit_por_nome(nome):
    kits = carregar_kits()
    if nome in kits:
        return kits[nome]
    raise ValueError(f"Kit '{nome}' não encontrado")

def refresh_kits():
    global KitsDisponíveis
    KitsDisponíveis = carregar_kits()

def filtrar_kits(filtros=None):
    kits = carregar_kits()
    if not filtros:
        return kits
    
    return {
        nome: kit for nome, kit in kits.items()
        if all(
            getattr(kit, k, None) == v or 
            (isinstance(v, list) and getattr(kit, k, None) in v)
            for k, v in filtros.items()
        )
    }

def criar_item_por_nome(nome_item):
    tabelas = [
        carregar_rangeds(), carregar_melees(), carregar_protecoes(),
        carregar_municoes(), carregar_consumiveis(),
        carregar_itens(), carregar_melhorias()
    ]

    for tabela in tabelas:
        if nome_item in tabela:
            item_data = tabela[nome_item]
            
            if hasattr(item_data, "to_dict") and hasattr(item_data.__class__, "from_dict"):
                return item_data.__class__.from_dict(item_data.to_dict())

            mapa = {
                "Ranged": Ranged, "Melee": Melee, "Protecao": Protecao,
                "Consumivel": Consumivel, "Municao": Municao,
                "Melhoria": Melhoria, "Item": Item,
            }
            cls = mapa.get(item_data.__class__.__name__, Item)
            return cls(nome=item_data.nome)

    return None
# === SISTEMA DE KITS === #

# === Funções RAW === #
# item #
def carregar_itens_raw():
    dados = _load_json("itens.json")
    if isinstance(dados, list):
        return {item.get("nome"): item for item in dados}
    return dados or {}

def salvar_itens_raw(dados):
    _save_json("itens.json", dados)

def remover_item_raw(nome):
    dados = carregar_itens_raw()
    if nome in dados:
        del dados[nome]
        salvar_itens_raw(dados)
        return True
    return False    
# item #

# consumivel #
def carregar_consumiveis_raw():
    dados=_load_json("consumiveis.json")
    if isinstance(dados,list):
        return {item.get("nome"):item for item in dados if "nome" in item}
    return dados or {}

def salvar_consumiveis_raw(dados):
    _save_json("consumiveis.json",dados)

def remover_consumiveis_raw(nome):
    dados=carregar_consumiveis_raw()
    if nome in dados:
        del dados[nome]
        salvar_consumiveis_raw(dados)
        return True
    return False
# consumivel #

# munição #
def carregar_municoes_raw():
    dados=_load_json("municoes.json")
    if isinstance(dados,list): return {i.get("nome"):i for i in dados}
    return dados or {}

def salvar_municoes_raw(dados):
    _save_json("municoes.json",dados)

def remover_municao_raw(nome):
    dados=carregar_municoes_raw()
    if nome in dados:
        dados.pop(nome)
        salvar_municoes_raw(dados)
        return True
    return False
# munição #

# equipamento #

# equipamento #

# ranged #
def carregar_rangeds_raw():
    dados=_load_json("rangeds.json")
    if isinstance(dados,list): return {i.get("nome"):i for i in dados}
    return dados or {}

def salvar_rangeds_raw(dados):
    _save_json("rangeds.json",dados)

def remover_ranged_raw(nome):
    dados=carregar_rangeds_raw()
    if nome in dados:
        dados.pop(nome)
        salvar_rangeds_raw(dados)
        return True
    return False
# ranged #

# melee #
def carregar_melees_raw():
    dados=_load_json("melees.json")
    if isinstance(dados,list): return {i.get("nome"):i for i in dados}
    return dados or {}

def salvar_melees_raw(dados):
    _save_json("melees.json",dados)

def remover_melee_raw(nome):
    dados=carregar_melees_raw()
    if nome in dados:
        dados.pop(nome)
        salvar_melees_raw(dados)
        return True
    return False
# melee #

# proteção #
def carregar_protecoes_raw():
    dados=_load_json("protecoes.json")
    if isinstance(dados,list): return {i.get("nome"):i for i in dados}
    return dados or {}

def salvar_protecoes_raw(dados):
    _save_json("protecoes.json",dados)

def remover_protecao_raw(nome):
    dados=carregar_protecoes_raw()
    if nome in dados:
        dados.pop(nome)
        salvar_protecoes_raw(dados)
        return True
    return False
# proteção #

# melhoria #
def carregar_melhorias_raw():
    try:
        dados = _load_json("melhorias.json")
        if isinstance(dados, list):
            return {item.get("nome"): item for item in dados if "nome" in item}
        return dados or {}
    except Exception as e:
        print(f"Erro ao carregar melhorias.json: {e}")
        return {}

def salvar_melhorias_raw(dados):
    try:
        _save_json("melhorias.json", dados)
        print(f"Melhorias salvas: {list(dados.keys())}")
    except Exception as e:
        print(f"Erro ao salvar melhorias.json: {e}")

def remover_melhoria_raw(nome):
    try:
        dados = carregar_melhorias_raw()
        if nome in dados:
            del dados[nome]
            salvar_melhorias_raw(dados)
            return True
        return False
    except Exception as e:
        print(f"Erro ao remover melhoria: {e}")
        return False
# melhoria #

# npc #
def carregar_npcs_raw():
    dados = _load_json("npcs.json")
    if isinstance(dados, list):
        return {item.get("nome"): item for item in dados}
    return dados or {}

def salvar_npcs_raw(dados):
    _save_json("npcs.json", dados)

def remover_npc_raw(nome):
    dados = carregar_npcs_raw()
    if nome in dados:
        dados.pop(nome)
        salvar_npcs_raw(dados)
        return True
    return False
# npc #

# efeitos #
def carregar_buffs_debuffs_raw():
    dados=_load_json("buffs_debuffs.json")
    if isinstance(dados,list): return {i["nome"]:i for i in dados}
    return dados or {}

def salvar_buffs_debuffs_raw(dados):
    _save_json("buffs_debuffs.json",dados)

def remover_buff_debuff_raw(nome):
    dados=carregar_buffs_debuffs_raw()
    if nome in dados:
        dados.pop(nome)
        salvar_buffs_debuffs_raw(dados)
        return True
    return False
# efeitos #

# habilidade #
def carregar_habilidades_raw():
    dados = _load_json("habilidades.json")
    if isinstance(dados, list):
        return {item.get("nome"): item for item in dados if "nome" in item}
    return dados or {}

def salvar_habilidades_raw(dados):
    _save_json("habilidades.json", dados)

def remover_habilidade_raw(nome):
    dados = carregar_habilidades_raw()
    if nome in dados:
        del dados[nome]
        salvar_habilidades_raw(dados)
        return True
    return False
# habilidade #

# poder #
def carregar_poderes_raw():
    dados = _load_json("poderes.json")
    if isinstance(dados, list):
        return {item.get("nome"): item for item in dados if "nome" in item}
    return dados or {}

def salvar_poderes_raw(dados):
    _save_json("poderes.json", dados)

def remover_poder_raw(nome):
    dados = carregar_poderes_raw()
    if nome in dados:
        del dados[nome]
        salvar_poderes_raw(dados)
        return True
    return False
# poder #

"""
Oque precisa ser feito:
    Código base:
        Criatura:
        - Implementar no APP e nas funções de acerto

        NPC:
        - Funciomaneto de gerar com habilidades e poderes

        Funções de ataque:
        - Desarmado
    Munições:
"""