from Codigos import Personagem, Inventario, SistemaDeProficiencias, Ranged, Melee, Protecao, Item, Consumivel, Explosivo, Municao, Melhoria, Proficiencia, Kits, NPC, gerar_id, HabilidadePoder, Efeito
import json
import os
from supabase import create_client, Client
from typing import Dict, List, Any, Optional, Union
import traceback

url = "https://eozqdonfmtlzmhoyyznn.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVvenFkb25mbXRsem1ob3l5em5uIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg3MTQ0NzQsImV4cCI6MjA2NDI5MDQ3NH0.MQgpQHtzgGaHRwAQPONtFd4z3-sG_zRYNMqPjZ-BU94"
supabase: Client = create_client(url, key)
from datetime import datetime

# === FUNÇÕES DE CARREGAMENTO SUPABASE === #
def carregar_itens():
    """Carrega todos os itens da tabela Itens"""
    try:
        response = supabase.table("Itens").select("*").execute()
        return {item["nome"]: item for item in response.data}
    except Exception as e:
        print(f"Erro ao carregar Itens: {e}")
        return {}

def carregar_consumiveis():
    """Carrega todos os consumíveis da tabela Consumiveis"""
    try:
        response = supabase.table("Consumiveis").select("*").execute()
        return {item["nome"]: item for item in response.data}
    except Exception as e:
        print(f"Erro ao carregar Consumiveis: {e}")
        return {}

def carregar_explosivos():
    """Carrega todos os explosivos da tabela Explosivos"""
    try:
        response = supabase.table("Explosivos").select("*").execute()
        return {item["nome"]: item for item in response.data}
    except Exception as e:
        print(f"Erro ao carregar Explosivos: {e}")
        return {}

def carregar_municoes():
    """Carrega todas as munições da tabela Municoes"""
    try:
        response = supabase.table("Municoes").select("*").execute()
        return {item["nome"]: item for item in response.data}
    except Exception as e:
        print(f"Erro ao carregar Municoes: {e}")
        return {}

def carregar_melhorias():
    """Carrega todas as melhorias da tabela Melhorias"""
    try:
        response = supabase.table("Melhorias").select("*").execute()
        return {item["nome"]: item for item in response.data}
    except Exception as e:
        print(f"Erro ao carregar Melhorias: {e}")
        return {}

def carregar_rangeds():
    """Carrega todas as armas ranged da tabela Rangeds"""
    try:
        response = supabase.table("Rangeds").select("*").execute()
        return {item["nome"]: item for item in response.data}
    except Exception as e:
        print(f"Erro ao carregar Rangeds: {e}")
        return {}

def carregar_melees():
    """Carrega todas as armas melee da tabela Melees"""
    try:
        response = supabase.table("Melees").select("*").execute()
        return {item["nome"]: item for item in response.data}
    except Exception as e:
        print(f"Erro ao carregar Melees: {e}")
        return {}

def carregar_protecoes():
    """Carrega todas as proteções da tabela Protecoes"""
    try:
        response = supabase.table("Protecoes").select("*").execute()
        return {item["nome"]: item for item in response.data}
    except Exception as e:
        print(f"Erro ao carregar Protecoes: {e}")
        return {}

def carregar_proficiencias():
    """Carrega todas as proficiências da tabela Proficiencias"""
    try:
        response = supabase.table("Proficiencias").select("*").execute()
        return {item["nome"]: item for item in response.data}
    except Exception as e:
        print(f"Erro ao carregar Proficiencias: {e}")
        return {}

def carregar_efeitos():
    """Carrega todos os efeitos da tabela efeitos"""
    try:
        response = supabase.table("efeitos").select("*").execute()
        return {item["id"]: item for item in response.data}
    except Exception as e:
        print(f"Erro ao carregar efeitos: {e}")
        return {}

def carregar_habilidades_poderes():
    """Carrega todas as habilidades e poderes da tabela habilidades_poderes"""
    try:
        response = supabase.table("habilidades_poderes").select("*").execute()
        return {item["id"]: item for item in response.data}
    except Exception as e:
        print(f"Erro ao carregar habilidades_poderes: {e}")
        return {}

def carregar_npcs():
    """Carrega todos os NPCs da tabela."""
    try:
        response = supabase.table("NPCs").select("*").execute()
        return {npc["classe"]: npc for npc in response.data}
    except Exception as e:
        print(f"Erro ao carregar NPCs: {e}")
        return {}

def carregar_todos_dados():
    """Carrega todos os dados de todas as tabelas de uma vez"""
    return {
        "Itens": carregar_itens(),
        "Consumiveis": carregar_consumiveis(),
        "Explosivos": carregar_explosivos(),
        "Municoes": carregar_municoes(),
        "Melhorias": carregar_melhorias(),
        "Rangeds": carregar_rangeds(),
        "Melees": carregar_melees(),
        "Protecoes": carregar_protecoes(),
        "Proficiencias": carregar_proficiencias(),
        "Efeitos": carregar_efeitos(),
        "HabilidadesPoderes": carregar_habilidades_poderes(),
        "Npcs": carregar_npcs(),
    }

def carregar_tabela_especifica(nome_tabela):
    """Carrega uma tabela específica pelo nome"""
    tabelas_disponiveis = {
        "Itens": carregar_itens,
        "Consumiveis": carregar_consumiveis,
        "Explosivos": carregar_explosivos,
        "Municoes": carregar_municoes,
        "Melhorias": carregar_melhorias,
        "Rangeds": carregar_rangeds,
        "Melees": carregar_melees,
        "Protecoes": carregar_protecoes,
        "Proficiencias": carregar_proficiencias,
        "Efeitos": carregar_efeitos,
        "HabilidadesPoderes": carregar_habilidades_poderes,
        "Npcs": carregar_npcs
    }
    
    if nome_tabela in tabelas_disponiveis:
        return tabelas_disponiveis[nome_tabela]()
    else:
        print(f"Tabela '{nome_tabela}' não encontrada.")
        return {}

_processing_items = set()  # GLOBAL, fora da função

def carregar_item_por_nome(nome_item):
    db_id = f"item_{nome_item}"
    
    if db_id in _processing_items:
        print(f"⚠️ Já processando '{nome_item}', evitando loop")
        return None

    _processing_items.add(db_id)
    try:
        tabelas_itens = {
            "Itens": (carregar_itens, "Item"),
            "Consumiveis": (carregar_consumiveis, "Consumivel"), 
            "Explosivos": (carregar_explosivos, "Explosivo"),
            "Municoes": (carregar_municoes, "Municao"),
            "Melhorias": (carregar_melhorias, "Melhoria"),
            "Rangeds": (carregar_rangeds, "Ranged"),
            "Melees": (carregar_melees, "Melee"),
            "Protecoes": (carregar_protecoes, "Protecao")
        }
        
        for tabela_nome, (funcao_carregar, class_name) in tabelas_itens.items():
            dados_tabela = funcao_carregar()
            if nome_item in dados_tabela:
                print(f"✅ Item '{nome_item}' encontrado na tabela {tabela_nome}")
                item_data = dados_tabela[nome_item]
                return reconstruct_item_from_data(item_data, class_name)
        
        print(f"❌ Item '{nome_item}' não encontrado em nenhuma tabela")
        return None
        
    finally:
        _processing_items.remove(db_id)
# === FUNÇÕES DE CARREGAMENTO SUPABASE === #

# === DESERIALIZAÇÃO DE ITENS === #
def deserialize_object_with_class(obj, _visited_objects=None, _processing_items=None):
    print(f"➡️ Entrando em deserialize_object_with_class: tipo={type(obj).__name__}, id={id(obj)}")
    """
    Deserializa objetos que foram serializados com informação de classe
    Reconstrói objetos customizados baseado no metadado __class__

    ✅ VERSÃO CORRIGIDA
    - Evita loops infinitos
    - Ignora campos crus ("Acessorios", "Melhorias", "municao") e deixa para os reconstruct_* cuidarem
    """
    if _visited_objects is None:
        _visited_objects = set()
    if _processing_items is None:
        _processing_items = set()

    obj_id = id(obj) if isinstance(obj, (dict, list)) else None
    if obj_id and obj_id in _visited_objects:
        print(f"⚠️ Loop detectado em deserialize_object_with_class: id={obj_id}, tipo={type(obj).__name__}")
        print(f"⚠️ Loop detectado, retornando objeto cru")
        return obj
    if obj_id:
        _visited_objects.add(obj_id)

    try:
        if obj is None or isinstance(obj, (str, int, float, bool)):
            print(f"⬅️ Retornando primitivo: {obj}")
            return obj

        if isinstance(obj, list):
            result = [deserialize_object_with_class(item, _visited_objects, _processing_items) for item in obj]
            print(f"⬅️ Retornando lista com {len(result)} itens")
            return result

        if isinstance(obj, dict):
            # Proficiencia simples → retorna como está
            if "nome" in obj and "atributo" in obj and ("nivel" in obj or "valor" in obj) and "__class__" not in obj:
                print(f"⬅️ Retornando proficiencia simples: {obj.get('nome')}")
                return obj

            if "__class__" in obj:
                class_name = obj["__class__"]
                item_identifier = f"{class_name}_{obj.get('nome', 'unknown')}_{obj.get('Id', id(obj))}"

                if item_identifier in _processing_items:
                    print(f"⚠️ {item_identifier} já em processamento, retornando versão simplificada")
                    simple_copy = {k: v for k, v in obj.items() if k not in ["__class__", "Acessorios", "Melhorias", "municao"]}
                    return simple_copy

                _processing_items.add(item_identifier)

                try:
                    # Copia sem __class__
                    data_copy = {k: v for k, v in obj.items() if k != "__class__"}

                    # Deserializa recursivamente, EXCETO melhorias/acessórios/munição crus
                    safe_data = {}
                    for key, value in data_copy.items():
                        if key in ["Acessorios", "Melhorias", "municao"]:
                            # Ignora aqui → reconstruct_* vai cuidar
                            safe_data[key] = value
                        else:
                            safe_data[key] = deserialize_object_with_class(value, _visited_objects, _processing_items)

                    # Casos especiais
                    if class_name == "Proficiencias":
                        print(f"⬅️ Retornando Proficiencias")
                        return safe_data

                    elif class_name == "Inventario":
                        print(f"📦 Reconstruindo Inventario com {len(safe_data.get('itens', []))} itens")
                        try:
                            if hasattr(Inventario, 'from_dict'):
                                result = Inventario.from_dict(safe_data)
                                print(f"⬅️ Retornando Inventario via from_dict")
                                return result
                            inventario = Inventario()
                            if "itens" in safe_data:
                                for item_data in safe_data["itens"]:
                                    if isinstance(item_data, dict) and "__class__" in item_data:
                                        item_class = item_data["__class__"]
                                        item_reconstruido = reconstruct_item_from_data(item_data, item_class, _processing_items)
                                        if item_reconstruido:
                                            inventario.adicionar_item(item_reconstruido)
                                    else:
                                        inventario.adicionar_item(item_data)
                            print(f"⬅️ Retornando Inventario reconstruído")
                            return inventario
                        except Exception as e:
                            print(f"❌ Erro ao reconstruir Inventario: {e}")
                            return safe_data

                    elif class_name in ["Ranged", "Melee", "Protecao", "Consumivel", "Explosivo", "Municao", "Melhoria", "Item"]:
                        print(f"🔧 Tentando reconstruir objeto da classe {class_name}, id={id(obj)}")
                        print(f"🛠 Reconstruindo {class_name}: {safe_data.get('nome', 'sem nome')}, id={id(obj)}")
                        result = reconstruct_item_from_data(safe_data, class_name, _processing_items)
                        print(f"⬅️ Retornando {class_name} reconstruído")
                        return result

                    else:
                        print(f"🔧 Tentando reconstruir objeto da classe {class_name}, id={id(obj)}")
                        try:
                            class_obj = globals().get(class_name)
                            if class_obj and hasattr(class_obj, 'from_dict'):
                                print(f"🔧 Reconstruindo {class_name} via from_dict")
                                result = class_obj.from_dict(safe_data)
                                print(f"⬅️ Retornando {class_name} via from_dict")
                                return result
                            else:
                                print(f"⚠️ Classe {class_name} não reconhecida, mantendo dict")
                                return safe_data
                        except Exception as e:
                            print(f"❌ Erro ao reconstruir {class_name}: {e}")
                            return safe_data

                finally:
                    _processing_items.discard(item_identifier)

            else:
                # Dicionário comum → processa recursivamente
                result = {key: deserialize_object_with_class(value, _visited_objects, _processing_items) for key, value in obj.items()}
                print(f"⬅️ Retornando dicionário comum com {len(result)} chaves")
                return result

        print(f"⬅️ Retornando objeto não tratado: {obj}")
        return obj

    finally:
        print(f"⬅️ Saindo de deserialize_object_with_class: tipo={type(obj).__name__}, id={id(obj)}")
        if obj_id and obj_id in _visited_objects:
            _visited_objects.remove(obj_id)

def serializar_item(item):
    """Serializa um item para dicionário"""
    print(f"➡️ Entrando em serializar_item: tipo={type(item).__name__ if item else 'None'}, id={id(item) if item else 'N/A'}")
    if item is None:
        print(f"⬅️ Saindo de serializar_item: None")
        return None
    if hasattr(item, 'to_dict'):
        item_dict = item.to_dict()
        item_dict["__class__"] = item.__class__.__name__
        print(f"⬅️ Saindo de serializar_item: dict com {len(item_dict)} chaves")
        return item_dict
    print(f"⬅️ Saindo de serializar_item: None (sem to_dict)")
    return None

def serializar_item_com_melhorias(item):
    """
    Serializa itens Ranged, Melee ou Protecao removendo temporariamente as melhorias
    VERSÃO CORRIGIDA - Evita loops na serialização
    """
    print(f"➡️ Entrando em serializar_item_com_melhorias: tipo={type(item).__name__}, id={id(item)}")
    # Cria uma cópia simples dos dados do item SEM melhorias/acessórios
    if hasattr(item, 'to_dict'):
        data = item.to_dict()
    else:
        data = vars(item).copy()
    
    data["__class__"] = item.__class__.__name__
    
    # Remove as listas de melhorias/acessórios dos dados principais
    melhorias_originais = data.pop("Melhorias", [])
    acessorios_originais = data.pop("Acessorios", [])
    
    # Serializa melhorias/acessórios APENAS com dados essenciais (evita recursão)
    if melhorias_originais:
        data["__melhorias_serializadas__"] = []
        for melhoria in melhorias_originais:
            if hasattr(melhoria, 'nome'):
                # Salva apenas dados essenciais da melhoria
                melhoria_simples = {
                    "__class__": "Melhoria",
                    "nome": melhoria.nome,
                    "peso": getattr(melhoria, 'peso', 0.1),
                    "tipo": getattr(melhoria, 'tipo', 'ranged'),
                    "modificadores": getattr(melhoria, 'modificadores', {})
                }
                data["__melhorias_serializadas__"].append(melhoria_simples)
    
    if acessorios_originais:
        data["__acessorios_serializados__"] = []
        for acessorio in acessorios_originais:
            if hasattr(acessorio, 'nome'):
                # Salva apenas dados essenciais do acessório
                acessorio_simples = {
                    "__class__": "Melhoria",
                    "nome": acessorio.nome,
                    "peso": getattr(acessorio, 'peso', 0.1),
                    "tipo": getattr(acessorio, 'tipo', 'ranged'),
                    "modificadores": getattr(acessorio, 'modificadores', {})
                }
                data["__acessorios_serializados__"].append(acessorio_simples)
    
    print(f"⬅️ Saindo de serializar_item_com_melhorias: dict com {len(data)} chaves")
    return data

def deserializar_item(data):
    """Deserializa um item de dicionário para objeto"""
    print(f"➡️ Entrando em deserializar_item: tipo={type(data).__name__}, id={id(data) if data else 'N/A'}")
    if data is None:
        print(f"⬅️ Saindo de deserializar_item: None")
        return None
    
    if isinstance(data, dict) and "__class__" in data:
        class_name = data["__class__"]
        # Remove o metadado da classe
        item_data = data.copy()
        del item_data["__class__"]
        
        # Tenta usar from_dict se a classe existir
        try:
            class_obj = globals().get(class_name)
            if class_obj and hasattr(class_obj, 'from_dict'):
                result = class_obj.from_dict(item_data)
                print(f"⬅️ Saindo de deserializar_item: {class_name} via from_dict")
                return result
        except Exception as e:
            print(f"❌ Erro ao deserializar item {class_name}: {e}")
    
    print(f"⬅️ Saindo de deserializar_item: dados originais")
    return None

def reconstruct_item_from_data(item_data, class_name=None, _processing_items=None):
    """
    Reconstrói um item a partir dos dados serializados.
    VERSÃO ATUALIZADA - Remove referência ao sistema de Pools e evita loops
    
    Args:
        item_data: Dicionário com os dados do item ou objeto já deserializado
        class_name: Nome da classe (opcional, será detectado automaticamente se não fornecido)
        _processing_items: Set para controle de recursão infinita
    
    Returns:
        Objeto da classe apropriada ou os dados originais se falhar
    """
    print(f"➡️ Entrando em reconstruct_item_from_data: {class_name}, nome={item_data.get('nome', 'sem nome')}, id={id(item_data)}")
    try:
        if _processing_items is None:
            _processing_items = set()
            
        # Se item_data já é um objeto (não é dict), retorna como está
        if not isinstance(item_data, dict):
            print(f"⬅️ Saindo de reconstruct_item_from_data: não é dict")
            return item_data
        
        # Detecta automaticamente o tipo de classe se não fornecido
        if class_name is None:
            if "classe" in item_data and "acao" in item_data and "calibre" in item_data:
                class_name = "Ranged"
            elif "classe" in item_data and "tipo_dano" in item_data and "dano_simples" in item_data:
                class_name = "Melee"
            elif "nivelBalistico" in item_data or ("regiao" in item_data and "absorcaoFisica" in item_data):
                class_name = "Protecao"
            elif "calibre" in item_data and "perfuracao" in item_data and "dano" in item_data and "classe" not in item_data:
                class_name = "Municao"
            elif "raio" in item_data and "tipo_dano" in item_data and "dano" in item_data:
                class_name = "Explosivo"
            elif "cura" in item_data and "energia" in item_data:
                class_name = "Consumivel"
            elif "tipo" in item_data and "modificadores" in item_data:
                class_name = "Melhoria"
            else:
                class_name = "Item"
        
        print(f"🔧 Reconstruindo {class_name}: {item_data.get('nome', 'sem nome')}")
        
        # Tenta carregar do banco primeiro (se o nome existir)
        if "nome" in item_data:
            try:
                item_do_banco = carregar_item_por_nome(item_data["nome"])
                if item_do_banco:
                    print(f"✅ Item '{item_data['nome']}' carregado do banco")
                    print(f"⬅️ Saindo de reconstruct_item_from_data: {class_name} carregado do banco")
                    return item_do_banco
            except Exception as e:
                print(f"⚠️ Item '{item_data['nome']}' não encontrado no banco ({e}), reconstruindo...")
        
        # Reconstrói baseado na classe específica
        if class_name == "Ranged":
            result = reconstruct_ranged(item_data, _processing_items)
            print(f"⬅️ Saindo de reconstruct_item_from_data: Ranged reconstruído")
            return result
        elif class_name == "Melee":
            result = reconstruct_melee(item_data, _processing_items)
            print(f"⬅️ Saindo de reconstruct_item_from_data: Melee reconstruído")
            return result
        elif class_name == "Protecao":
            result = reconstruct_protecao(item_data, _processing_items)
            print(f"⬅️ Saindo de reconstruct_item_from_data: Protecao reconstruído")
            return result
        elif class_name == "Municao":
            result = reconstruct_municao(item_data)
            print(f"⬅️ Saindo de reconstruct_item_from_data: Municao reconstruído")
            return result
        elif class_name == "Explosivo":
            result = reconstruct_explosivo(item_data)
            print(f"⬅️ Saindo de reconstruct_item_from_data: Explosivo reconstruído")
            return result
        elif class_name == "Consumivel":
            result = reconstruct_consumivel(item_data)
            print(f"⬅️ Saindo de reconstruct_item_from_data: Consumivel reconstruído")
            return result
        elif class_name == "Melhoria":
            result = reconstruct_melhoria(item_data)
            print(f"⬅️ Saindo de reconstruct_item_from_data: Melhoria reconstruído")
            return result
        elif class_name == "Item":
            result = reconstruct_item(item_data)
            print(f"⬅️ Saindo de reconstruct_item_from_data: Item reconstruído")
            return result
        else:
            print(f"❌ Classe {class_name} não reconhecida")
            print(f"⬅️ Saindo de reconstruct_item_from_data: dados originais (classe não reconhecida)")
            return item_data
            
    except Exception as e:
        print(f"❌ Erro ao reconstituir item {class_name}: {e}")
        import traceback
        traceback.print_exc()
        print(f"⬅️ Saindo de reconstruct_item_from_data: dados originais (erro)")
        return item_data

def reconstruct_item(item_data):
    """Reconstrói um Item básico"""
    print(f"➡️ Entrando em reconstruct_item: nome={item_data.get('nome', 'sem nome')}, id={id(item_data)}")
    from Codigos import Item  # Assumindo que as classes estão em Codigos
    
    item = Item(
        nome=item_data.get("nome", "Item"),
        peso=item_data.get("peso")
    )
    print(f"⬅️ Saindo de reconstruct_item: Item, id={id(item_data)}")
    return item

def reconstruct_consumivel(item_data):
    """Reconstrói um Consumível"""
    print(f"➡️ Entrando em reconstruct_consumivel: nome={item_data.get('nome', 'sem nome')}, id={id(item_data)}")
    from Codigos import Consumivel
    
    item = Consumivel(
        nome=item_data.get("nome", "Consumível"),
        peso=item_data.get("peso", 1.0),
        cura=item_data.get("cura", 0),
        energia=item_data.get("energia", 0)
    )
    print(f"⬅️ Saindo de reconstruct_consumivel: Consumivel, id={id(item_data)}")
    return item

def reconstruct_explosivo(item_data):
    """Reconstrói um Explosivo"""
    print(f"➡️ Entrando em reconstruct_explosivo: nome={item_data.get('nome', 'sem nome')}, id={id(item_data)}")
    from Codigos import Explosivo
    
    item = Explosivo(
        nome=item_data.get("nome", "Explosivo"),
        peso=item_data.get("peso", 1.0),
        raio=item_data.get("raio", 1),
        dano=item_data.get("dano", 10),
        tipo_dano=item_data.get("tipo_dano", 1)
    )
    print(f"⬅️ Saindo de reconstruct_explosivo: Explosivo, id={id(item_data)}")
    return item

def reconstruct_municao(item_data):
    """Reconstrói uma Munição"""
    print(f"➡️ Entrando em reconstruct_municao: nome={item_data.get('nome', 'sem nome')}, id={id(item_data)}")
    from Codigos import Municao
    
    item = Municao(
        nome=item_data.get("nome", "Munição"),
        calibre=item_data.get("calibre", ".22"),
        perfuracao=item_data.get("perfuracao", 1),
        dano=item_data.get("dano", 5)
    )
    print(f"⬅️ Saindo de reconstruct_municao: Municao, id={id(item_data)}")
    return item

def reconstruct_melhoria(item_data):
    """Reconstrói uma Melhoria"""
    print(f"➡️ Entrando em reconstruct_melhoria: nome={item_data.get('nome', 'sem nome')}, id={id(item_data)}")
    from Codigos import Melhoria
    
    item = Melhoria(
        nome=item_data.get("nome", "Melhoria"),
        peso=item_data.get("peso", 0.1),
        tipo=item_data.get("tipo", "ranged"),
        modificadores=item_data.get("modificadores", {})
    )
    print(f"⬅️ Saindo de reconstruct_melhoria: Melhoria, id={id(item_data)}")
    return item

def reconstruct_ranged(item_data, _processing_items=None):
    """Reconstrói uma arma Ranged com proteção contra loops - reconstruindo melhorias separadamente"""
    print(f"➡️ Entrando em reconstruct_ranged: nome={item_data.get('nome', 'sem nome')}, id={id(item_data)}")
    try:
        if _processing_items is None:
            _processing_items = set()
            
        try:
            from Codigos import Ranged, Melhoria, Municao
        except ImportError:
            try:
                Ranged = globals().get('Ranged')
                Melhoria = globals().get('Melhoria') 
                Municao = globals().get('Municao')
                if not all([Ranged, Melhoria, Municao]):
                    raise ImportError("Classes não encontradas")
            except:
                print(f"❌ Não foi possível importar classes necessárias para Ranged")
                return item_data
        
        print(f"🔧 Construindo Ranged com dados: {list(item_data.keys())}")
        
        # Cria o item usando o construtor padrão SEM acessórios
        item = Ranged(
            nome=item_data.get("nome", "Arma de Fogo"),
            peso=item_data.get("peso", 2.0),
            classe=item_data.get("classe", "Pistola"),
            acao=item_data.get("acao", "Semi"),
            raridade=item_data.get("raridade", "Comum"),
            calibre=item_data.get("calibre", ".22"),
            capacidade=item_data.get("capacidade", 10)
        )
        
        # Restaura atributos específicos
        atributos_especificos = [
            "dano", "recuo", "MaxRange", "MinRange", "ShortCrit", "MediumCrit", "LongCrit",
            "munições", "Id", "Perfuracao"
        ]
        
        for attr in atributos_especificos:
            if attr in item_data:
                setattr(item, attr, item_data[attr])
        
        # Reconstrói munição carregada SEM recursão
        if "municao" in item_data and item_data["municao"]:
            municao_data = item_data["municao"]
            if isinstance(municao_data, dict):
                # Constrói munição de forma simples
                municao_clean = municao_data.copy()
                if "__class__" in municao_clean:
                    del municao_clean["__class__"]
                
                try:
                    item.municao = Municao(
                        nome=municao_clean.get("nome", "Munição"),
                        calibre=municao_clean.get("calibre", ".22"),
                        perfuracao=municao_clean.get("perfuracao", 1),
                        dano=municao_clean.get("dano", 5)
                    )
                except:
                    item.municao = None
            else:
                item.municao = municao_data
        
        # RECONSTRUÇÃO SEPARADA DE ACESSÓRIOS
        if "Acessorios" in item_data and item_data["Acessorios"]:
            acessorios_reconstruidos = []
            
            # Primeiro, reconstrói todas as melhorias separadamente
            for acessorio_data in item_data["Acessorios"]:
                try:
                    # Se já é um objeto Melhoria, usa direto
                    if hasattr(acessorio_data, '__class__') and acessorio_data.__class__.__name__ == 'Melhoria':
                        acessorios_reconstruidos.append(acessorio_data)
                    elif isinstance(acessorio_data, dict):
                        # Reconstrói melhoria independentemente
                        melhoria_clean = acessorio_data.copy()
                        if "__class__" in melhoria_clean:
                            del melhoria_clean["__class__"]
                        
                        # Cria a melhoria usando reconstruct_melhoria para garantir consistência
                        melhoria = reconstruct_melhoria(melhoria_clean)
                        if melhoria:
                            acessorios_reconstruidos.append(melhoria)
                        else:
                            # Se falhou, tenta construção direta
                            try:
                                melhoria = Melhoria(
                                    nome=melhoria_clean.get("nome", "Melhoria"),
                                    peso=melhoria_clean.get("peso", 0.1),
                                    tipo=melhoria_clean.get("tipo", "ranged"),
                                    modificadores=melhoria_clean.get("modificadores", {})
                                )
                                acessorios_reconstruidos.append(melhoria)
                            except Exception as e:
                                print(f"⚠️ Erro ao criar melhoria {melhoria_clean.get('nome', 'unknown')}: {e}")
                    else:
                        acessorios_reconstruidos.append(acessorio_data)
                except Exception as e:
                    print(f"⚠️ Erro ao processar acessório: {e}")
                    continue
            
            # Agora equipa todas as melhorias no item usando o método oficial
            for acessorio in acessorios_reconstruidos:
                try:
                    item.adicionar_acessorio(acessorio)
                    print(f"✅ Acessório '{acessorio.nome if hasattr(acessorio, 'nome') else 'unknown'}' equipado")
                except Exception as e:
                    print(f"⚠️ Erro ao equipar acessório: {e}")
        
        print(f"✅ Ranged '{item.nome}' reconstruído com sucesso")
        print(f"⬅️ Saindo de reconstruct_ranged: Ranged, id={id(item_data)}")
        return item
        
    except Exception as e:
        print(f"❌ Erro ao reconstruir Ranged: {e}")
        import traceback
        traceback.print_exc()
        return item_data

def reconstruct_melee(item_data, _processing_items=None):
    """Reconstrói uma arma Melee com proteção contra loops - reconstruindo melhorias separadamente"""
    print(f"➡️ Entrando em reconstruct_melee: nome={item_data.get('nome', 'sem nome')}, id={id(item_data)}")
    try:
        if _processing_items is None:
            _processing_items = set()
            
        try:
            from Codigos import Melee, Melhoria
        except ImportError:
            try:
                Melee = globals().get('Melee')
                Melhoria = globals().get('Melhoria')
                if not all([Melee, Melhoria]):
                    raise ImportError("Classes não encontradas")
            except:
                print(f"❌ Não foi possível importar classes necessárias para Melee")
                return item_data
        
        print(f"🔧 Construindo Melee com dados: {list(item_data.keys())}")
        
        # Cria o item usando o construtor padrão SEM melhorias
        item = Melee(
            nome=item_data.get("nome", "Arma Branca"),
            peso=item_data.get("peso", 1.0),
            classe=item_data.get("classe", "Faca"),
            tipo_dano=item_data.get("tipo_dano", "Cortante"),
            raridade=item_data.get("raridade", "Comum")
        )
        
        # Restaura atributos específicos se existirem nos dados
        atributos_especificos = [
            "dano_simples", "critico_simples", "valor_critico_simples",
            "dano_forte", "critico_forte", "valor_critico_forte", 
            "dano_investida", "critico_investida", "valor_critico_investida",
            "dano_arremesso", "critico_arremesso", "valor_critico_arremesso",
            "Id"
        ]
        
        for attr in atributos_especificos:
            if attr in item_data:
                setattr(item, attr, item_data[attr])
        
        # RECONSTRUÇÃO SEPARADA DE MELHORIAS
        if "Melhorias" in item_data and item_data["Melhorias"]:
            melhorias_reconstruidas = []
            
            # Primeiro, reconstrói todas as melhorias separadamente
            for melhoria_data in item_data["Melhorias"]:
                try:
                    # Se já é um objeto Melhoria, usa direto
                    if hasattr(melhoria_data, '__class__') and melhoria_data.__class__.__name__ == 'Melhoria':
                        melhorias_reconstruidas.append(melhoria_data)
                    elif isinstance(melhoria_data, dict):
                        # Reconstrói melhoria independentemente
                        melhoria_clean = melhoria_data.copy()
                        if "__class__" in melhoria_clean:
                            del melhoria_clean["__class__"]
                        
                        # Cria a melhoria usando reconstruct_melhoria para garantir consistência
                        melhoria = reconstruct_melhoria(melhoria_clean)
                        if melhoria:
                            melhorias_reconstruidas.append(melhoria)
                        else:
                            # Se falhou, tenta construção direta
                            try:
                                melhoria = Melhoria(
                                    nome=melhoria_clean.get("nome", "Melhoria"),
                                    peso=melhoria_clean.get("peso", 0.1),
                                    tipo=melhoria_clean.get("tipo", "melee"),
                                    modificadores=melhoria_clean.get("modificadores", {})
                                )
                                melhorias_reconstruidas.append(melhoria)
                            except Exception as e:
                                print(f"⚠️ Erro ao criar melhoria {melhoria_clean.get('nome', 'unknown')}: {e}")
                    else:
                        melhorias_reconstruidas.append(melhoria_data)
                except Exception as e:
                    print(f"⚠️ Erro ao processar melhoria: {e}")
                    continue
            
            # Agora equipa todas as melhorias no item usando o método oficial
            for melhoria in melhorias_reconstruidas:
                try:
                    item.adicionar_melhoria(melhoria)
                    print(f"✅ Melhoria '{melhoria.nome if hasattr(melhoria, 'nome') else 'unknown'}' equipada")
                except Exception as e:
                    print(f"⚠️ Erro ao equipar melhoria: {e}")
        
        print(f"✅ Melee '{item.nome}' reconstruído com sucesso")
        print(f"⬅️ Saindo de reconstruct_melee: Melee, id={id(item_data)}")
        return item
        
    except Exception as e:
        print(f"❌ Erro ao reconstruir Melee: {e}")
        import traceback
        traceback.print_exc()
        return item_data

def reconstruct_protecao(item_data, _processing_items=None):
    """Reconstrói uma proteção com proteção contra loops - reconstruindo melhorias separadamente"""
    print(f"➡️ Entrando em reconstruct_protecao: nome={item_data.get('nome', 'sem nome')}, id={id(item_data)}")
    try:
        if _processing_items is None:
            _processing_items = set()
            
        try:
            from Codigos import Protecao, Melhoria
        except ImportError:
            try:
                Protecao = globals().get('Protecao')
                Melhoria = globals().get('Melhoria')
                if not all([Protecao, Melhoria]):
                    raise ImportError("Classes não encontradas")
            except:
                print(f"❌ Não foi possível importar classes necessárias para Protecao")
                return item_data
        
        print(f"🔧 Construindo Protecao com dados: {list(item_data.keys())}")
        
        # Cria o item usando o construtor padrão SEM melhorias
        item = Protecao(
            nome=item_data.get("nome", "Proteção"),
            peso=item_data.get("peso", 1.0),
            nivelBalistico=item_data.get("nivelBalistico", 1),
            absorcaoFisica=item_data.get("absorcaoFisica", 1),
            absorcaoBalistica=item_data.get("absorcaoBalistica", 1),
            regiao=item_data.get("regiao", "Torso")
        )
        
        # Restaura ID se existir
        if "Id" in item_data:
            item.Id = item_data["Id"]
        
        # RECONSTRUÇÃO SEPARADA DE MELHORIAS
        if "Melhorias" in item_data and item_data["Melhorias"]:
            melhorias_reconstruidas = []
            
            # Primeiro, reconstrói todas as melhorias separadamente
            for melhoria_data in item_data["Melhorias"]:
                try:
                    # Se já é um objeto Melhoria, usa direto
                    if hasattr(melhoria_data, '__class__') and melhoria_data.__class__.__name__ == 'Melhoria':
                        melhorias_reconstruidas.append(melhoria_data)
                    elif isinstance(melhoria_data, dict):
                        # Reconstrói melhoria independentemente
                        melhoria_clean = melhoria_data.copy()
                        if "__class__" in melhoria_clean:
                            del melhoria_clean["__class__"]
                        
                        # Cria a melhoria usando reconstruct_melhoria para garantir consistência
                        melhoria = reconstruct_melhoria(melhoria_clean)
                        if melhoria:
                            melhorias_reconstruidas.append(melhoria)
                        else:
                            # Se falhou, tenta construção direta
                            try:
                                melhoria = Melhoria(
                                    nome=melhoria_clean.get("nome", "Melhoria"),
                                    peso=melhoria_clean.get("peso", 0.1),
                                    tipo=melhoria_clean.get("tipo", "protection"),
                                    modificadores=melhoria_clean.get("modificadores", {})
                                )
                                melhorias_reconstruidas.append(melhoria)
                            except Exception as e:
                                print(f"⚠️ Erro ao criar melhoria {melhoria_clean.get('nome', 'unknown')}: {e}")
                    else:
                        melhorias_reconstruidas.append(melhoria_data)
                except Exception as e:
                    print(f"⚠️ Erro ao processar melhoria: {e}")
                    continue
            
            # Agora equipa todas as melhorias no item usando o método oficial
            for melhoria in melhorias_reconstruidas:
                try:
                    item.adicionar_melhoria(melhoria)
                    print(f"✅ Melhoria '{melhoria.nome if hasattr(melhoria, 'nome') else 'unknown'}' equipada")
                except Exception as e:
                    print(f"⚠️ Erro ao equipar melhoria: {e}")
        
        print(f"✅ Protecao '{item.nome}' reconstruída com sucesso")
        print(f"⬅️ Saindo de reconstruct_protecao: Protecao, id={id(item_data)}")
        return item
        
    except Exception as e:
        print(f"❌ Erro ao reconstruir Protecao: {e}")
        import traceback
        traceback.print_exc()
        return item_data
# === DESERIALIZAÇÃO DE ITENS === #

# === SISTEMA DE SESSÕES === #
GruposDePersonagens = {}
KitsDisponíveis = {}

def serializar_objeto(obj, _visited_objects=None, _path="root"):
    """
    Serializa qualquer objeto preservando informação de classe e prevenindo loops infinitos
    
    Args:
        obj: Objeto a ser serializado
        _visited_objects: Set de IDs de objetos já visitados (para prevenir loops)
        _path: Caminho atual na árvore de serialização (para debug)
    """
    # Inicializa set de objetos visitados na primeira chamada
    if _visited_objects is None:
        _visited_objects = set()
        print(f"🔄 Iniciando serialização em: {_path}")
    
    # Casos triviais (None e tipos primitivos)
    if obj is None:
        print(f"  ⚪ None em: {_path}")
        return None
    
    if isinstance(obj, (str, int, float, bool)):
        print(f"  📝 Primitivo ({type(obj).__name__}) em: {_path}")
        return obj
    
    # Verifica se objeto já foi visitado (previne loop)
    obj_id = id(obj)
    if obj_id in _visited_objects:
        obj_type = type(obj).__name__
        print(f"  ⚠️  LOOP DETECTADO! {obj_type} (id={obj_id}) já foi visitado em: {_path}")
        return {
            "__circular_ref__": True,
            "__class__": obj_type,
            "__id__": obj_id,
            "__path__": _path
        }
    
    # Marca objeto como visitado
    _visited_objects.add(obj_id)
    
    # Serializa listas
    if isinstance(obj, list):
        print(f"  📦 Serializando lista de {len(obj)} itens em: {_path}")
        resultado = []
        for i, item in enumerate(obj):
            resultado.append(serializar_objeto(item, _visited_objects, f"{_path}[{i}]"))
        return resultado
    
    # Serializa dicionários
    if isinstance(obj, dict):
        print(f"  📚 Serializando dict com {len(obj)} chaves em: {_path}")
        resultado = {}
        for key, value in obj.items():
            resultado[key] = serializar_objeto(value, _visited_objects, f"{_path}.{key}")
        return resultado
    
    # Para objetos com classes customizadas
    if hasattr(obj, '__class__'):
        class_name = obj.__class__.__name__
        print(f"  ➡️  Serializando {class_name} (id={obj_id}) em: {_path}")
        
        # Tratamento especial para itens com melhorias/acessórios
        if class_name in ['Ranged', 'Melee', 'Protecao']:
            resultado = serializar_item_com_melhorias(obj, _visited_objects, _path)
            return resultado
        
        # Usa to_dict() se disponível
        if hasattr(obj, 'to_dict'):
            print(f"    🔧 Usando método to_dict() para {class_name}")
            data = obj.to_dict()
            if isinstance(data, dict):
                data["__class__"] = class_name
                data["__id__"] = obj_id
            return serializar_objeto(data, _visited_objects, f"{_path}.to_dict()")
        else:
            # Fallback usando __dict__
            print(f"    🔧 Usando __dict__ para {class_name}")
            data = vars(obj).copy()
            data["__class__"] = class_name
            data["__id__"] = obj_id
            return serializar_objeto(data, _visited_objects, f"{_path}.__dict__")
    
    print(f"  ⚠️  Fallback para string em: {_path}")
    return str(obj)

def serializar_item_com_melhorias(item, _visited_objects, _path):
    """
    Serializa itens Ranged, Melee ou Protecao removendo temporariamente as melhorias
    
    Args:
        item: Item a ser serializado
        _visited_objects: Set de IDs de objetos já visitados
        _path: Caminho atual na árvore de serialização
    """
    class_name = item.__class__.__name__
    item_id = id(item)
    
    print(f"    🛠  Processando melhorias/acessórios de {class_name} em: {_path}")
    
    melhorias_removidas = []
    acessorios_removidos = []
    
    # Remove melhorias temporariamente
    if hasattr(item, 'Melhorias') and item.Melhorias:
        melhorias_removidas = item.Melhorias.copy()
        print(f"      🔧 Removendo {len(melhorias_removidas)} melhorias: {[getattr(m, 'nome', str(m)) for m in melhorias_removidas]}")
        for melhoria in melhorias_removidas:
            item.remover_melhoria(melhoria)
    
    # Remove acessórios temporariamente
    if hasattr(item, 'Acessorios') and item.Acessorios:
        acessorios_removidos = item.Acessorios.copy()
        print(f"      🔧 Removendo {len(acessorios_removidos)} acessórios: {[getattr(a, 'nome', str(a)) for a in acessorios_removidos]}")
        item.Acessorios.clear()
        if hasattr(item, 'recalcular_atributos'):
            item.recalcular_atributos()
    
    # Serializa o item sem melhorias/acessórios
    print(f"      📦 Serializando item base (sem melhorias)")
    if hasattr(item, 'to_dict'):
        data = item.to_dict()
    else:
        data = vars(item).copy()
    
    data["__class__"] = class_name
    data["__id__"] = item_id
    
    # Serializa melhorias/acessórios separadamente COM proteção contra loops
    if melhorias_removidas:
        print(f"      🛠  Serializando {len(melhorias_removidas)} melhorias separadamente")
        data["__melhorias_serializadas__"] = []
        for i, melhoria in enumerate(melhorias_removidas):
            melhoria_path = f"{_path}.melhorias[{i}]"
            melhoria_serializada = serializar_objeto(melhoria, _visited_objects, melhoria_path)
            data["__melhorias_serializadas__"].append(melhoria_serializada)
    
    if acessorios_removidos:
        print(f"      🛠  Serializando {len(acessorios_removidos)} acessórios separadamente")
        data["__acessorios_serializados__"] = []
        for i, acessorio in enumerate(acessorios_removidos):
            acessorio_path = f"{_path}.acessorios[{i}]"
            acessorio_serializado = serializar_objeto(acessorio, _visited_objects, acessorio_path)
            data["__acessorios_serializados__"].append(acessorio_serializado)
    
    # Re-equipa as melhorias/acessórios
    print(f"      🔄 Re-equipando melhorias e acessórios")
    for melhoria in melhorias_removidas:
        if class_name == 'Ranged':
            item.adicionar_acessorio(melhoria)
        else:
            item.adicionar_melhoria(melhoria)
    
    for acessorio in acessorios_removidos:
        item.Acessorios.append(acessorio)
        if hasattr(item, 'recalcular_atributos'):
            item.recalcular_atributos()
    
    print(f"      ✅ Item {class_name} serializado com sucesso")
    
    # Serializa os dados do item (sem recursão infinita)
    return serializar_objeto(data, _visited_objects, f"{_path}.data")

def deserializar_objeto(obj, pools=None):
    """
    Deserializa objeto e re-equipa melhorias se necessário
    VERSÃO CORRIGIDA - Evita loops na deserialização
    """
    print(f"🔄 Iniciando deserialização")
    
    # Detecta referências circulares
    if isinstance(obj, dict) and obj.get("__circular_ref__"):
        class_name = obj.get("__class__", "Unknown")
        obj_id = obj.get("__id__", "unknown")
        path = obj.get("__path__", "unknown")
        print(f"  ⚠️  Referência circular detectada: {class_name} (id={obj_id}) em {path}")
        return None  # ou retornar um placeholder apropriado
    
    # Primeiro deserializa o objeto base
    resultado = deserialize_object_with_class(obj)
    
    # Se é um dict com dados serializados de melhorias, processa separadamente
    if isinstance(obj, dict) and obj.get("__class__") in ['Ranged', 'Melee', 'Protecao']:
        class_name = obj.get("__class__")
        print(f"  ➡️  Deserializando {class_name} com melhorias")
        
        # Processa melhorias serializadas
        if "__melhorias_serializadas__" in obj:
            melhorias_data = obj["__melhorias_serializadas__"]
            print(f"    🛠  Reequipando {len(melhorias_data)} melhorias")
            
            for i, melhoria_data in enumerate(melhorias_data):
                # Pula referências circulares
                if isinstance(melhoria_data, dict) and melhoria_data.get("__circular_ref__"):
                    print(f"      ⚠️  Pulando melhoria {i} (referência circular)")
                    continue
                
                try:
                    # Tenta carregar do banco primeiro
                    nome_melhoria = melhoria_data.get("nome")
                    if nome_melhoria:
                        print(f"      🔍 Buscando melhoria '{nome_melhoria}' no banco")
                        try:
                            melhoria_do_banco = carregar_item_por_nome(nome_melhoria)
                            if melhoria_do_banco:
                                print(f"        ✅ Melhoria '{nome_melhoria}' carregada do banco")
                                if class_name == 'Ranged':
                                    resultado.adicionar_acessorio(melhoria_do_banco)
                                else:
                                    resultado.adicionar_melhoria(melhoria_do_banco)
                                continue
                        except Exception as e:
                            print(f"        ⚠️  Erro ao carregar do banco: {e}")
                    
                    # Se não encontrou no banco, reconstrói
                    print(f"      🔧 Reconstruindo melhoria a partir dos dados")
                    melhoria = reconstruct_melhoria(melhoria_data)
                    if melhoria and class_name == 'Ranged':
                        resultado.adicionar_acessorio(melhoria)
                        print(f"        ✅ Acessório adicionado")
                    elif melhoria:
                        resultado.adicionar_melhoria(melhoria)
                        print(f"        ✅ Melhoria adicionada")
                except Exception as e:
                    print(f"      ⚠️  Erro ao reequipar melhoria {i}: {e}")
        
        # Processa acessórios serializados
        if "__acessorios_serializados__" in obj:
            acessorios_data = obj["__acessorios_serializados__"]
            print(f"    🛠  Reequipando {len(acessorios_data)} acessórios")
            
            for i, acessorio_data in enumerate(acessorios_data):
                # Pula referências circulares
                if isinstance(acessorio_data, dict) and acessorio_data.get("__circular_ref__"):
                    print(f"      ⚠️  Pulando acessório {i} (referência circular)")
                    continue
                
                try:
                    # Tenta carregar do banco primeiro
                    nome_acessorio = acessorio_data.get("nome")
                    if nome_acessorio:
                        print(f"      🔍 Buscando acessório '{nome_acessorio}' no banco")
                        try:
                            acessorio_do_banco = carregar_item_por_nome(nome_acessorio)
                            if acessorio_do_banco:
                                print(f"        ✅ Acessório '{nome_acessorio}' carregado do banco")
                                resultado.adicionar_acessorio(acessorio_do_banco)
                                continue
                        except Exception as e:
                            print(f"        ⚠️  Erro ao carregar do banco: {e}")
                    
                    # Se não encontrou no banco, reconstrói
                    print(f"      🔧 Reconstruindo acessório a partir dos dados")
                    acessorio = reconstruct_melhoria(acessorio_data)
                    if acessorio:
                        resultado.adicionar_acessorio(acessorio)
                        print(f"        ✅ Acessório adicionado")
                except Exception as e:
                    print(f"      ⚠️  Erro ao reequipar acessório {i}: {e}")
    
    print(f"✅ Deserialização concluída")
    return resultado

def salvar_sessao(nome_da_sessao, sobrescrever=False):
    """
    Salva a sessão atual no banco de dados
    """
    try:
        # Verifica se sessão já existe
        response = supabase.table("sessoes").select("nome").eq("nome", nome_da_sessao).execute()
        sessao_existe = len(response.data) > 0
        
        if sessao_existe and not sobrescrever:
            print(f"⚠️ Sessão '{nome_da_sessao}' já existe. Use sobrescrever=True para atualizar.")
            return False
        
        print("🔄 Processando itens com melhorias...")
        
        # Serializa os dados da sessão
        dados_sessao = {}
        for grupo, lista in GruposDePersonagens.items():
            dados_sessao[grupo] = []
            for personagem in lista:
                if hasattr(personagem, 'to_dict'):
                    dados_personagem = personagem.to_dict()
                else:
                    dados_personagem = vars(personagem)
                
                # Serializa recursivamente para preservar classes
                dados_sessao[grupo].append(serializar_objeto(dados_personagem))
        
        # Inclui dados dos kits disponíveis se existirem
        if KitsDisponíveis:
            dados_sessao["__kits_disponiveis__"] = serializar_objeto(KitsDisponíveis)
        
        # Salva no banco
        if sessao_existe and sobrescrever:
            response = supabase.table("sessoes").update({
                "conteudo": dados_sessao
            }).eq("nome", nome_da_sessao).execute()
        else:
            response = supabase.table("sessoes").insert({
                "nome": nome_da_sessao,
                "conteudo": dados_sessao,
                "data_criacao": datetime.utcnow().isoformat()
            }).execute()
        
        print(f"✅ Sessão '{nome_da_sessao}' salva com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao salvar sessão: {e}")
        return False

def carregar_sessao(nome_da_sessao, carregar_pools=True):
    """
    Carrega uma sessão do banco de dados
    """
    global GruposDePersonagens, KitsDisponíveis
    try:
        print(f"🔄 Carregando sessão '{nome_da_sessao}'...")
        
        # Carrega os pools de dados se solicitado
        pools = None
        if carregar_pools:
            print("📥 Carregando dados do banco...")
            pools = carregar_todos_dados()
        
        # Busca a sessão no banco
        response = supabase.table("sessoes").select("conteudo").eq("nome", nome_da_sessao).order("data_criacao", desc=True).limit(1).execute()
        
        if not response.data:
            print(f"❌ Sessão '{nome_da_sessao}' não encontrada")
            return False
        
        dados_sessao = response.data[0]["conteudo"]
        
        print("🔄 Re-equipando melhorias nos itens...")
        
        # Reconstrói os grupos de personagens
        GruposDePersonagens = {}
        personagens_carregados = 0
        
        for grupo, lista_personagens in dados_sessao.items():
            # Ignora dados especiais dos kits
            if grupo == "__kits_disponiveis__":
                KitsDisponíveis = deserializar_objeto(lista_personagens, pools)
                continue
                
            GruposDePersonagens[grupo] = []
            for dados_personagem in lista_personagens:
                try:
                    # Deserializa recursivamente para reconstituir objetos
                    dados_deserializados = deserializar_objeto(dados_personagem, pools)
                    
                    # Reconstrói o personagem
                    if hasattr(Personagem, 'from_dict'):
                        personagem = Personagem.from_dict(dados_deserializados)
                    else:
                        personagem = Personagem()
                        for attr, valor in dados_deserializados.items():
                            setattr(personagem, attr, valor)
                    
                    GruposDePersonagens[grupo].append(personagem)
                    personagens_carregados += 1
                    
                except Exception as e:
                    print(f"⚠️ Erro ao carregar personagem: {e}")
                    continue
        
        print(f"✅ Sessão carregada: {len(GruposDePersonagens)} grupos, {personagens_carregados} personagens")
        if KitsDisponíveis:
            print(f"📦 {len(KitsDisponíveis)} kits carregados")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao carregar sessão: {e}")
        return False
    
def listar_sessoes():
    """
    Lista todas as sessões disponíveis com informações detalhadas
    """
    try:
        response = supabase.table("sessoes").select("nome, data_criacao, conteudo").order("data_criacao", desc=True).execute()
        
        sessoes = []
        for sessao in response.data:
            # Calcula estatísticas da sessão
            total_personagens = 0
            total_grupos = 0
            
            if sessao.get("conteudo"):
                for grupo, lista in sessao["conteudo"].items():
                    if grupo != "__kits_disponiveis__":
                        total_grupos += 1
                        total_personagens += len(lista) if isinstance(lista, list) else 0
            
            # Formata data
            data_criacao = datetime.fromisoformat(sessao["data_criacao"].replace('Z', '+00:00'))
            
            sessoes.append({
                "nome": sessao["nome"],
                "data_criacao": data_criacao.strftime("%d/%m/%Y %H:%M"),
                "total_grupos": total_grupos,
                "total_personagens": total_personagens
            })
        
        return sessoes
        
    except Exception as e:
        print(f"❌ Erro ao listar sessões: {e}")
        return []

def exibir_sessoes():
    """
    Exibe uma lista formatada das sessões disponíveis
    """
    sessoes = listar_sessoes()
    
    if not sessoes:
        print("📝 Nenhuma sessão encontrada")
        return
    
    print("📋 SESSÕES DISPONÍVEIS:")
    print("=" * 80)
    
    for i, sessao in enumerate(sessoes, 1):
        print(f"{i:2d}. {sessao['nome']}")
        print(f"    📅 Criada: {sessao['data_criacao']}")
        print(f"    👥 {sessao['total_personagens']} personagens em {sessao['total_grupos']} grupos")
        print()

def deletar_sessao(nome_da_sessao):
    """
    Deleta uma sessão do banco de dados
    """
    try:
        response = supabase.table("sessoes").delete().eq("nome", nome_da_sessao).execute()
        
        if response.data:
            print(f"✅ Sessão '{nome_da_sessao}' deletada com sucesso")
            return True
        else:
            print(f"⚠️ Sessão '{nome_da_sessao}' não encontrada")
            return False
        
    except Exception as e:
        print(f"❌ Erro ao deletar sessão: {e}")
        return False

def limpar_sessao_atual():
    """
    Limpa a sessão atual da memória
    """
    global GruposDePersonagens, KitsDisponíveis
    GruposDePersonagens = {}
    KitsDisponíveis = {}
    print("🧹 Sessão atual limpa da memória")

def clonar_sessao(nome_original, nome_clone):
    """
    Clona uma sessão existente com um novo nome
    """
    try:
        # Busca a sessão original
        response = supabase.table("sessoes").select("conteudo").eq("nome", nome_original).execute()
        
        if not response.data:
            print(f"❌ Sessão original '{nome_original}' não encontrada")
            return False
        
        # Verifica se o clone já existe
        response_clone = supabase.table("sessoes").select("nome").eq("nome", nome_clone).execute()
        if response_clone.data:
            print(f"⚠️ Sessão '{nome_clone}' já existe")
            return False
        
        # Cria o clone
        dados_original = response.data[0]["conteudo"]
        response_insert = supabase.table("sessoes").insert({
            "nome": nome_clone,
            "conteudo": dados_original,
            "data_criacao": datetime.utcnow().isoformat()
        }).execute()
        
        print(f"✅ Sessão clonada: '{nome_original}' → '{nome_clone}'")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao clonar sessão: {e}")
        return False

def backup_sessao(nome_da_sessao, incluir_timestamp=True):
    """
    Cria um backup de uma sessão com timestamp
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") if incluir_timestamp else ""
    nome_backup = f"{nome_da_sessao}_backup_{timestamp}" if timestamp else f"{nome_da_sessao}_backup"
    
    return clonar_sessao(nome_da_sessao, nome_backup)

def validar_sessao(nome_da_sessao):
    """
    Valida se uma sessão pode ser carregada corretamente
    """
    try:
        response = supabase.table("sessoes").select("conteudo").eq("nome", nome_da_sessao).execute()
        
        if not response.data:
            return False, "Sessão não encontrada"
        
        dados = response.data[0]["conteudo"]
        
        # Tenta carregar pools para validação
        pools = carregar_todos_dados()
        
        # Valida estrutura básica
        if not isinstance(dados, dict):
            return False, "Estrutura de dados inválida"
        
        # Conta itens que serão carregados
        total_personagens = 0
        problemas = []
        
        for grupo, lista in dados.items():
            if grupo == "__kits_disponiveis__":
                continue
                
            if not isinstance(lista, list):
                problemas.append(f"Grupo '{grupo}' não é uma lista")
                continue
                
            for i, dados_personagem in enumerate(lista):
                try:
                    deserializar_objeto(dados_personagem, pools)
                    total_personagens += 1
                except Exception as e:
                    problemas.append(f"Erro no personagem {i+1} do grupo '{grupo}': {str(e)}")
        
        if problemas:
            return False, f"Problemas encontrados: {'; '.join(problemas[:3])}"
        
        return True, f"Sessão válida: {total_personagens} personagens em {len([g for g in dados.keys() if g != '__kits_disponiveis__'])} grupos"
        
    except Exception as e:
        return False, f"Erro na validação: {e}"

def status_sessao():
    """
    Mostra o status da sessão atual
    """
    if not GruposDePersonagens:
        print("📭 Nenhuma sessão carregada")
        return
    
    print("📊 STATUS DA SESSÃO ATUAL:")
    print("=" * 50)
    
    total_personagens = 0
    for grupo, lista in GruposDePersonagens.items():
        print(f"👥 {grupo}: {len(lista)} personagens")
        total_personagens += len(lista)
    
    print(f"\n📈 Total: {total_personagens} personagens em {len(GruposDePersonagens)} grupos")
    
    if KitsDisponíveis:
        print(f"📦 {len(KitsDisponíveis)} kits disponíveis")

# === FUNÇÕES AUXILIARES PARA GERENCIAMENTO === #
def renomear_sessao(nome_antigo, nome_novo):
    """
    Renomeia uma sessão existente
    """
    try:
        # Verifica se sessão antiga existe
        response = supabase.table("sessoes").select("*").eq("nome", nome_antigo).execute()
        if not response.data:
            print(f"❌ Sessão '{nome_antigo}' não encontrada")
            return False
        
        # Verifica se novo nome já existe
        response_novo = supabase.table("sessoes").select("nome").eq("nome", nome_novo).execute()
        if response_novo.data:
            print(f"❌ Sessão '{nome_novo}' já existe")
            return False
        
        # Renomeia
        sessao_data = response.data[0]
        supabase.table("sessoes").update({
            "nome": nome_novo,
            "data_atualizacao": datetime.utcnow().isoformat()
        }).eq("nome", nome_antigo).execute()
        
        print(f"✅ Sessão renomeada: '{nome_antigo}' → '{nome_novo}'")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao renomear sessão: {e}")
        return False

def exportar_sessao_json(nome_da_sessao, arquivo_destino=None):
    """
    Exporta uma sessão para um arquivo JSON local
    """
    try:
        response = supabase.table("sessoes").select("*").eq("nome", nome_da_sessao).execute()
        
        if not response.data:
            print(f"❌ Sessão '{nome_da_sessao}' não encontrada")
            return False
        
        import json
        
        if not arquivo_destino:
            arquivo_destino = f"sessao_{nome_da_sessao}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(arquivo_destino, 'w', encoding='utf-8') as f:
            json.dump(response.data[0], f, indent=2, ensure_ascii=False)
        
        print(f"✅ Sessão exportada para: {arquivo_destino}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao exportar sessão: {e}")
        return False
# === SISTEMA DE SESSÕES === #

# === SISTEMA DE KITS === #
def carregar_kits_db():
    """Carrega kits do banco de dados usando o mesmo sistema de deserialização dos personagens"""
    try:
        print("🔄 Carregando kits do banco de dados...")
        
        # Carrega dados das tabelas para deserialização
        print("📋 Carregando dados das tabelas...")
        dados_tabelas = carregar_todos_dados()
        
        # Carrega kits básicos
        response = supabase.table("kits").select("*").execute()
        kits_data = response.data
        kits = {}
        
        if not kits_data:
            print("ℹ️ Nenhum kit encontrado no banco de dados")
            return kits
        
        for kit_data in kits_data:
            nome = kit_data["nome"]
            raridade = kit_data["raridade"]
            kit_id = kit_data["id"]
            
            print(f"🎒 Processando kit: {nome}")
            
            # Cria kit básico
            kit = Kits(nome, raridade)
            kit.id_db = kit_id
            kit.inventario = Inventario()
            
            # Carrega inventário serializado
            try:
                inv_response = supabase.table("kit_inventario").select("*").eq("kit_id", kit_id).execute()
                
                # Procura pelo inventário completo serializado
                for item_inv in inv_response.data:
                    if item_inv["item_nome"] == "__inventario_completo__":
                        item_data = item_inv.get("item_data")
                        if item_data:
                            # Deserializa usando o mesmo sistema dos personagens
                            inventario_deserializado = deserializar_objeto(item_data, dados_tabelas)
                            if inventario_deserializado:
                                kit.inventario = inventario_deserializado
                                print(f"✅ Inventário completo carregado para {nome}")
                                break
                
                # Debug da carga
                itens = kit.inventario.listar_itens() if hasattr(kit.inventario, 'listar_itens') else []
                print(f"📊 Kit {nome}: {len(itens)} tipos de itens carregados")
                        
            except Exception as e:
                print(f"❌ Erro ao carregar inventário do kit '{nome}': {e}")
                import traceback
                traceback.print_exc()
            
            kits[nome] = kit
        
        print(f"✅ Carregados {len(kits)} kits do banco de dados")
        return kits
        
    except Exception as e:
        print(f"❌ Erro crítico ao carregar kits do banco: {e}")
        import traceback
        traceback.print_exc()
        return {}

def salvar_kit_no_banco(kit):
    """Salva um kit no banco de dados usando o mesmo sistema de serialização dos personagens"""
    try:
        print(f"💾 Salvando kit: {kit.nome}")
        
        # Dados básicos do kit
        dados_kit = {
            "nome": kit.nome,
            "raridade": kit.raridade
        }
        
        # Verifica se o kit já existe
        response = supabase.table("kits").select("id").eq("nome", kit.nome).execute()
        
        if response.data:
            # Atualiza kit existente
            kit_id = response.data[0]["id"]
            supabase.table("kits").update(dados_kit).eq("id", kit_id).execute()
            print(f"🔄 Kit existente atualizado")
        else:
            # Insere novo kit
            response = supabase.table("kits").insert(dados_kit).execute()
            kit_id = response.data[0]["id"]
            kit.id_db = kit_id
            print(f"🆕 Novo kit criado")
        
        # Remove inventário existente do banco
        supabase.table("kit_inventario").delete().eq("kit_id", kit_id).execute()
        
        # Serializa e salva o inventário completo
        if kit.inventario and hasattr(kit.inventario, 'itens'):
            inventario_serializado = serializar_objeto(kit.inventario)
            
            dados_inventario = {
                "kit_id": kit_id,
                "item_nome": "__inventario_completo__",
                "item_tipo": "Inventario", 
                "item_data": inventario_serializado,
                "quantidade": 1
            }
            
            supabase.table("kit_inventario").insert(dados_inventario).execute()
            print(f"✅ Inventário completo salvo para o kit")
        
        print(f"✅ Kit '{kit.nome}' salvo com sucesso no banco")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao salvar kit '{kit.nome}': {e}")
        import traceback
        traceback.print_exc()
        return False

def deletar_kit_do_banco(nome_kit):
    """Deleta um kit do banco de dados (inventário deletado automaticamente por CASCADE)"""
    try:
        response = supabase.table("kits").delete().eq("nome", nome_kit).execute()
        
        # Remove também do dicionário em memória
        global KitsDisponíveis
        if nome_kit in KitsDisponíveis:
            del KitsDisponíveis[nome_kit]
        
        print(f"✅ Kit '{nome_kit}' deletado do banco e da memória")
        return True
    except Exception as e:
        print(f"❌ Erro ao deletar kit '{nome_kit}': {e}")
        return False

def listar_kits_banco():
    """Lista todos os kits disponíveis no banco de dados com informações básicas"""
    try:
        response = supabase.table("kits").select("nome, raridade, id").order("nome").execute()
        
        if not response.data:
            print("📦 Nenhum kit encontrado no banco de dados")
            return []
        
        print("📋 KITS NO BANCO DE DADOS:")
        print("=" * 50)
        
        kits_info = []
        for kit_data in response.data:
            nome = kit_data["nome"]
            raridade = kit_data["raridade"]
            kit_id = kit_data["id"]
            
            # Conta itens no inventário
            inv_response = supabase.table("kit_inventario").select("quantidade").eq("kit_id", kit_id).execute()
            total_itens = sum(item.get("quantidade", 0) for item in inv_response.data)
            
            kit_info = {
                "nome": nome,
                "raridade": raridade,
                "total_itens": total_itens,
                "id": kit_id
            }
            kits_info.append(kit_info)
            
            print(f"🎒 {nome} ({raridade}) - {total_itens} itens")
        
        return kits_info
        
    except Exception as e:
        print(f"❌ Erro ao listar kits do banco: {e}")
        return []

def validar_kit_banco(nome_kit):
    """Valida se um kit no banco pode ser carregado corretamente"""
    try:
        # Busca o kit
        response = supabase.table("kits").select("*").eq("nome", nome_kit).execute()
        
        if not response.data:
            return False, "Kit não encontrado no banco"
        
        kit_data = response.data[0]
        kit_id = kit_data["id"]
        
        # Verifica inventário
        inv_response = supabase.table("kit_inventario").select("*").eq("kit_id", kit_id).execute()
        
        if not inv_response.data:
            return True, "Kit válido mas sem itens"
        
        # Tenta carregar dados das tabelas
        dados_tabelas = carregar_todos_dados()
        
        # Tenta deserializar inventário
        for item_inv in inv_response.data:
            if item_inv["item_nome"] == "__inventario_completo__":
                item_data = item_inv.get("item_data")
                if item_data:
                    try:
                        deserializar_objeto(item_data, dados_tabelas)
                        return True, "Kit válido e carregável"
                    except Exception as e:
                        return False, f"Erro na deserialização: {str(e)}"
        
        return True, "Kit válido (formato legado)"
        
    except Exception as e:
        return False, f"Erro na validação: {str(e)}"

def refresh_kits():
    """Recarrega todos os kits do banco de dados"""
    global KitsDisponíveis
    print("🔄 Atualizando kits do banco...")
    KitsDisponíveis = carregar_kits_db()
    print("✅ Kits atualizados com sucesso!")

def filtrar_kits(filtros: Dict[str, Any] = None) -> Dict[str, Kits]:
    """Filtra kits baseado em critérios"""
    if not filtros:
        return KitsDisponíveis
    
    kits_filtrados = {}
    for nome, kit in KitsDisponíveis.items():
        incluir_kit = True
        
        for atributo, valor_filtro in filtros.items():
            if hasattr(kit, atributo):
                valor_kit = getattr(kit, atributo)
                if isinstance(valor_filtro, list):
                    if valor_kit not in valor_filtro:
                        incluir_kit = False
                        break
                elif valor_kit != valor_filtro:
                    incluir_kit = False
                    break
            else:
                incluir_kit = False
                break
                
        if incluir_kit:
            kits_filtrados[nome] = kit
    
    return kits_filtrados

def carregar_kit_por_nome(nome_kit: str) -> Kits:
    """Carrega um kit específico por nome"""
    if nome_kit in KitsDisponíveis:
        return KitsDisponíveis[nome_kit]
    raise ValueError(f"Kit '{nome_kit}' não encontrado.")

def atualizar_kit_especifico(kit_nome: str):
    """Recarrega um kit específico do banco de dados"""
    try:
        print(f"🔄 Atualizando kit: {kit_nome}")
        
        # Carrega dados das tabelas
        dados_tabelas = carregar_todos_dados()
        
        # Busca o kit no banco
        response = supabase.table("kits").select("*").eq("nome", kit_nome).execute()
        
        if not response.data:
            print(f"❌ Kit '{kit_nome}' não encontrado no banco")
            return None
        
        kit_data = response.data[0]
        kit_id = kit_data["id"]
        
        # Cria novo kit
        kit = Kits(kit_data["nome"], kit_data["raridade"])
        kit.id_db = kit_id
        kit.inventario = Inventario()
        
        # Carrega inventário
        inv_response = supabase.table("kit_inventario").select("*").eq("kit_id", kit_id).execute()
        
        for item_inv in inv_response.data:
            if item_inv["item_nome"] == "__inventario_completo__":
                item_data = item_inv.get("item_data")
                if item_data:
                    inventario_deserializado = deserializar_objeto(item_data, dados_tabelas)
                    if inventario_deserializado:
                        kit.inventario = inventario_deserializado
                        break
        
        # Atualiza no dicionário global
        global KitsDisponíveis
        KitsDisponíveis[kit_nome] = kit
        
        print(f"✅ Kit '{kit_nome}' atualizado com sucesso")
        return kit
        
    except Exception as e:
        print(f"❌ Erro ao atualizar kit '{kit_nome}': {e}")
        return None

def debug_kit_inventario_detalhado(kit_nome):
    """Função de debug melhorada para verificar o inventário de um kit"""
    try:
        if kit_nome not in KitsDisponíveis:
            print(f"❌ Kit '{kit_nome}' não encontrado")
            return
        
        kit = KitsDisponíveis[kit_nome]
        print(f"\n🔍 DEBUG DETALHADO - Kit: {kit_nome}")
        print("=" * 60)
        print(f"📋 Raridade: {kit.raridade}")
        print(f"🆔 ID no banco: {getattr(kit, 'id_db', 'Não definido')}")
        
        # Debug do inventário
        if hasattr(kit, 'inventario'):
            inventario = kit.inventario
            print(f"📦 Tipo do inventário: {type(inventario)}")
            print(f"📦 Inventário existe: {inventario is not None}")
            
            if inventario and hasattr(inventario, 'itens'):
                print(f"📝 Lista de itens existe: {hasattr(inventario, 'itens')}")
                print(f"📝 Tipo da lista: {type(inventario.itens)}")
                print(f"📝 Quantidade de itens na lista: {len(inventario.itens) if inventario.itens else 0}")
                
                if inventario.itens:
                    print(f"\n🔬 ANÁLISE DOS ITENS:")
                    for i, item in enumerate(inventario.itens):
                        print(f"  {i+1}. Tipo do container: {type(item)}")
                        
                        # Se é ItemInventario
                        if hasattr(item, 'item') and hasattr(item, 'quantidade'):
                            print(f"     📦 ItemInventario detectado")
                            print(f"     📦 Item interno: {item.item}")
                            print(f"     📦 Tipo do item interno: {type(item.item)}")
                            print(f"     📦 Nome do item: {getattr(item.item, 'nome', 'SEM_NOME')}")
                            print(f"     📦 Classe do item: {item.item.__class__.__name__}")
                            print(f"     📦 Quantidade: {item.quantidade}")
                        else:
                            # Item direto
                            print(f"     📋 Item direto: {item}")
                            print(f"     📋 Tipo: {type(item)}")
                            print(f"     📋 Nome: {getattr(item, 'nome', 'SEM_NOME')}")
                            print(f"     📋 Classe: {item.__class__.__name__}")
                
                # Teste dos métodos do inventário
                print(f"\n🧪 TESTE DOS MÉTODOS:")
                if hasattr(inventario, 'listar_itens'):
                    try:
                        itens_listados = inventario.listar_itens()
                        print(f"✅ listar_itens() funcionou: {len(itens_listados)} itens")
                        for item in itens_listados[:3]:  # Mostra só os 3 primeiros
                            print(f"     - {item}")
                    except Exception as e:
                        print(f"❌ Erro no listar_itens(): {e}")
                
                # Teste do método do kit
                if hasattr(kit, 'listar_itens'):
                    try:
                        itens_kit = kit.listar_itens()
                        print(f"✅ kit.listar_itens() funcionou: {len(itens_kit)} itens")
                        for item in itens_kit[:3]:  # Mostra só os 3 primeiros
                            print(f"     - {item}")
                    except Exception as e:
                        print(f"❌ Erro no kit.listar_itens(): {e}")
            else:
                print("❌ Inventário não tem lista de itens válida")
        else:
            print("❌ Kit não tem inventário")
            
        # Debug direto do banco
        print(f"\n🗄️ DEBUG DO BANCO DE DADOS:")
        if hasattr(kit, 'id_db'):
            try:
                inv_response = supabase.table("kit_inventario").select("*").eq("kit_id", kit.id_db).execute()
                print(f"📊 Itens no banco para este kit: {len(inv_response.data)}")
                
                for i, item_db in enumerate(inv_response.data[:3]):  # Mostra só os 3 primeiros
                    print(f"  {i+1}. Nome: {item_db['item_nome']}")
                    print(f"     Tipo: {item_db.get('item_tipo', 'N/A')}")
                    print(f"     Quantidade: {item_db['quantidade']}")
                    print(f"     Tem dados serializados: {'item_data' in item_db and item_db['item_data'] is not None}")
                    
            except Exception as e:
                print(f"❌ Erro ao consultar banco: {e}")
                    
    except Exception as e:
        print(f"❌ Erro no debug detalhado: {e}")
        import traceback
        traceback.print_exc()

def testar_carregamento_completo():
    """Teste completo do sistema de kits"""
    print("🧪 TESTE COMPLETO DO SISTEMA DE KITS")
    print("=" * 60)
    
    # 1. Recarrega kits
    print("\n1️⃣ RECARREGANDO KITS...")
    kits_carregados = carregar_kits_db()
    
    # 2. Analisa cada kit
    print(f"\n2️⃣ ANÁLISE DETALHADA ({len(kits_carregados)} kits)...")
    for nome, kit in kits_carregados.items():
        debug_kit_inventario_detalhado(nome)
        print("\n" + "-" * 40)
    
    return kits_carregados
# === SISTEMA DE KITS === #

"""
Oque precisa ser feito:

    Carregamento de dados:
        Kits não estão funcionando

    Tela de seleção:
        Os itens nos kits não estão carregando direito
        
    
    Tela de Dados:
        Refazer todas as listas de cada tabela (Uma função e um layout pra cada tabela, mais fácil)
        Prioridade: Kits, Efeitos, Habilidades/Poderes
        Renomear tela
        Corrigir botões de navegação


"""