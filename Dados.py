from Codigos import Personagem, Inventario, SistemaDeProficiencias, Ranged, Melee, Protecao, Item, Consumivel, Explosivo, Municao, Melhoria, Proficiencia, Kits, NPC, gerar_id, Habilidade,Poder, BuffDebuff
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

def carregar_poderes():
    """Carrega todos os poderes da tabela Poderes"""
    try:
        response = supabase.table("Poderes").select("*").execute()
        return {item["nome"]: item for item in response.data}
    except Exception as e:
        print(f"Erro ao carregar Poderes: {e}")
        return {}

def carregar_habilidades():
    """Carrega todas as habilidades da tabela Habilidades"""
    try:
        response = supabase.table("Habilidades").select("*").execute()
        return {item["nome"]: item for item in response.data}
    except Exception as e:
        print(f"Erro ao carregar Habilidades: {e}")
        return {}

def carregar_buffs_debuffs():
    """Carrega todos os buffs/debuffs da tabela BuffsDebuffs"""
    try:
        response = supabase.table("BuffsDebuffs").select("*").execute()
        return {item["nome"]: item for item in response.data}
    except Exception as e:
        print(f"Erro ao carregar BuffsDebuffs: {e}")
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
        "Poderes": carregar_poderes(),
        "Habilidades": carregar_habilidades(),
        "BuffsDebuffs": carregar_buffs_debuffs(),
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
        "Poderes": carregar_poderes,
        "Habilidades": carregar_habilidades,
        "BuffsDebuffs": carregar_buffs_debuffs,
        "Npcs": carregar_npcs
    }
    
    if nome_tabela in tabelas_disponiveis:
        return tabelas_disponiveis[nome_tabela]()
    else:
        print(f"Tabela '{nome_tabela}' não encontrada.")
        return {}

_processing_items = set()

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
        
        nome_item_lower = nome_item.lower()
        
        for tabela_nome, (funcao_carregar, class_name) in tabelas_itens.items():
            dados_tabela = funcao_carregar()
            for chave, item_data in dados_tabela.items():
                if chave.lower() == nome_item_lower:
                    print(f"✅ Item '{nome_item}' encontrado na tabela {tabela_nome} como '{chave}'")
                    return reconstruct_item_from_data(item_data, class_name)
        
        print(f"❌ Item '{nome_item}' não encontrado em nenhuma tabela")
        return None
        
    finally:
        _processing_items.remove(db_id)
# === FUNÇÕES DE CARREGAMENTO SUPABASE === #

# === FUNÇÕES DE SALVAMENTO E EDIÇÃO SUPABASE === #
def salvar_item(dados_item):
    try:
        response = supabase.table("Itens").insert(dados_item).execute()
        if response.data:
            print(f"✅ Item '{dados_item.get('nome')}' salvo com sucesso.")
            return response.data[0]
        else:
            print("⚠️ Nenhum dado retornado ao salvar o item.")
            return None
    except Exception as e:
        print(f"❌ Erro ao salvar item '{dados_item.get('nome', 'Sem nome')}': {e}")
        return None

def editar_item(nome_item, novos_dados):
    try:
        response = supabase.table("Itens").update(novos_dados).eq("nome", nome_item).execute()
        if response.data:
            print(f"✅ Item '{nome_item}' atualizado com sucesso.")
            return response.data[0]
        else:
            print(f"⚠️ Nenhum item encontrado com nome '{nome_item}'.")
            return None
    except Exception as e:
        print(f"❌ Erro ao editar item '{nome_item}': {e}")
        return None

def remover_item(nome):
    try:
        supabase.table("Itens").delete().eq("nome", nome).execute()
        print(f"🗑️ Item '{nome}' removido com sucesso.")
        return True
    except Exception as e:
        print(f"❌ Erro ao remover item '{nome}': {e}")
        return False


def salvar_consumivel(dados_consumivel):
    try:
        response = supabase.table("Consumiveis").insert(dados_consumivel).execute()
        if response.data:
            print(f"✅ Consumível '{dados_consumivel.get('nome')}' salvo com sucesso.")
            return response.data[0]
        else:
            print("⚠️ Nenhum dado retornado ao salvar o consumível.")
            return None
    except Exception as e:
        print(f"❌ Erro ao salvar consumível '{dados_consumivel.get('nome', 'Sem nome')}': {e}")
        return None

def editar_consumivel(nome_consumivel, novos_dados):
    try:
        response = supabase.table("Consumiveis").update(novos_dados).eq("nome", nome_consumivel).execute()
        if response.data:
            print(f"✅ Consumível '{nome_consumivel}' atualizado com sucesso.")
            return response.data[0]
        else:
            print(f"⚠️ Nenhum consumível encontrado com nome '{nome_consumivel}'.")
            return None
    except Exception as e:
        print(f"❌ Erro ao editar consumível '{nome_consumivel}': {e}")
        return None

def remover_consumivel(nome):
    try:
        supabase.table("Consumiveis").delete().eq("nome", nome).execute()
        print(f"🗑️ Consumível '{nome}' removido com sucesso.")
        return True
    except Exception as e:
        print(f"❌ Erro ao remover consumível '{nome}': {e}")
        return False


def salvar_explosivo(dados_explosivo):
    try:
        response = supabase.table("Explosivos").insert(dados_explosivo).execute()
        if response.data:
            print(f"✅ Explosivo '{dados_explosivo.get('nome')}' salvo com sucesso.")
            return response.data[0]
        else:
            print("⚠️ Nenhum dado retornado ao salvar o explosivo.")
            return None
    except Exception as e:
        print(f"❌ Erro ao salvar explosivo '{dados_explosivo.get('nome', 'Sem nome')}': {e}")
        return None

def editar_explosivo(nome_explosivo, novos_dados):
    try:
        response = supabase.table("Explosivos").update(novos_dados).eq("nome", nome_explosivo).execute()
        if response.data:
            print(f"✅ Explosivo '{nome_explosivo}' atualizado com sucesso.")
            return response.data[0]
        else:
            print(f"⚠️ Nenhum explosivo encontrado com nome '{nome_explosivo}'.")
            return None
    except Exception as e:
        print(f"❌ Erro ao editar explosivo '{nome_explosivo}': {e}")
        return None

def remover_explosivo(nome):
    try:
        supabase.table("Explosivos").delete().eq("nome", nome).execute()
        print(f"🗑️ Explosivo '{nome}' removido com sucesso.")
        return True
    except Exception as e:
        print(f"❌ Erro ao remover explosivo '{nome}': {e}")
        return False


def salvar_municao(dados_municao):
    try:
        response = supabase.table("Municoes").insert(dados_municao).execute()
        if response.data:
            print(f"✅ Munição '{dados_municao.get('nome')}' salva com sucesso.")
            return response.data[0]
        else:
            print("⚠️ Nenhum dado retornado ao salvar a munição.")
            return None
    except Exception as e:
        print(f"❌ Erro ao salvar munição '{dados_municao.get('nome', 'Sem nome')}': {e}")
        return None

def editar_municao(nome_municao, novos_dados):
    try:
        response = supabase.table("Municoes").update(novos_dados).eq("nome", nome_municao).execute()
        if response.data:
            print(f"✅ Munição '{nome_municao}' atualizada com sucesso.")
            return response.data[0]
        else:
            print(f"⚠️ Nenhuma munição encontrada com nome '{nome_municao}'.")
            return None
    except Exception as e:
        print(f"❌ Erro ao editar munição '{nome_municao}': {e}")
        return None

def remover_municao(nome):
    try:
        supabase.table("Municoes").delete().eq("nome", nome).execute()
        print(f"🗑️ Munição '{nome}' removida com sucesso.")
        return True
    except Exception as e:
        print(f"❌ Erro ao remover munição '{nome}': {e}")
        return False


def salvar_melhoria(dados_melhoria):
    try:
        response = supabase.table("Melhorias").insert(dados_melhoria).execute()
        if response.data:
            print(f"✅ Melhoria '{dados_melhoria.get('nome')}' salva com sucesso.")
            return response.data[0]
        else:
            print("⚠️ Nenhum dado retornado ao salvar a melhoria.")
            return None
    except Exception as e:
        print(f"❌ Erro ao salvar melhoria '{dados_melhoria.get('nome', 'Sem nome')}': {e}")
        return None

def editar_melhoria(nome_melhoria, novos_dados):
    try:
        response = supabase.table("Melhorias").update(novos_dados).eq("nome", nome_melhoria).execute()
        if response.data:
            print(f"✅ Melhoria '{nome_melhoria}' atualizada com sucesso.")
            return response.data[0]
        else:
            print(f"⚠️ Nenhuma melhoria encontrada com nome '{nome_melhoria}'.")
            return None
    except Exception as e:
        print(f"❌ Erro ao editar melhoria '{nome_melhoria}': {e}")
        return None

def remover_melhoria(nome):
    try:
        supabase.table("Melhorias").delete().eq("nome", nome).execute()
        print(f"🗑️ Melhoria '{nome}' removida com sucesso.")
        return True
    except Exception as e:
        print(f"❌ Erro ao remover melhoria '{nome}': {e}")
        return False


def salvar_melee(dados_melee):
    try:
        response = supabase.table("Melees").insert(dados_melee).execute()
        if response.data:
            print(f"✅ Melee '{dados_melee.get('nome')}' salvo com sucesso.")
            return response.data[0]
        else:
            print("⚠️ Nenhum dado retornado ao salvar o melee.")
            return None
    except Exception as e:
        print(f"❌ Erro ao salvar melee '{dados_melee.get('nome', 'Sem nome')}': {e}")
        return None

def editar_melee(nome_melee, novos_dados):
    try:
        response = supabase.table("Melees").update(novos_dados).eq("nome", nome_melee).execute()
        if response.data:
            print(f"✅ Melee '{nome_melee}' atualizado com sucesso.")
            return response.data[0]
        else:
            print(f"⚠️ Nenhum melee encontrado com nome '{nome_melee}'.")
            return None
    except Exception as e:
        print(f"❌ Erro ao editar melee '{nome_melee}': {e}")
        return None

def remover_melee(nome):
    """Remove uma arma melee pelo nome."""
    try:
        supabase.table("Melees").delete().eq("nome", nome).execute()
        return True
    except Exception as e:
        print(f"Erro ao remover Melee: {e}")
        return False


def salvar_ranged(dados_ranged):
    try:
        response = supabase.table("Rangeds").insert(dados_ranged).execute()
        if response.data:
            print(f"✅ Ranged '{dados_ranged.get('nome')}' salvo com sucesso.")
            return response.data[0]
        else:
            print("⚠️ Nenhum dado retornado ao salvar o ranged.")
            return None
    except Exception as e:
        print(f"❌ Erro ao salvar ranged '{dados_ranged.get('nome', 'Sem nome')}': {e}")
        return None

def editar_ranged(nome_ranged, novos_dados):
    try:
        response = supabase.table("Rangeds").update(novos_dados).eq("nome", nome_ranged).execute()
        if response.data:
            print(f"✅ Ranged '{nome_ranged}' atualizado com sucesso.")
            return response.data[0]
        else:
            print(f"⚠️ Nenhum ranged encontrado com nome '{nome_ranged}'.")
            return None
    except Exception as e:
        print(f"❌ Erro ao editar ranged '{nome_ranged}': {e}")
        return None

def remover_ranged(nome):
    try:
        supabase.table("Rangeds").delete().eq("nome", nome).execute()
        print(f"🗑️ Ranged '{nome}' removido com sucesso.")
        return True
    except Exception as e:
        print(f"❌ Erro ao remover ranged '{nome}': {e}")
        return False
    

def salvar_protecao(dados_protecao):
    try:
        response = supabase.table("Protecoes").insert(dados_protecao).execute()
        if response.data:
            print(f"✅ Proteção '{dados_protecao.get('nome')}' salva com sucesso.")
            return response.data[0]
        else:
            print("⚠️ Nenhum dado retornado ao salvar a proteção.")
            return None
    except Exception as e:
        print(f"❌ Erro ao salvar proteção '{dados_protecao.get('nome', 'Sem nome')}': {e}")
        return None

def editar_protecao(nome_protecao, novos_dados):
    try:
        response = supabase.table("Protecoes").update(novos_dados).eq("nome", nome_protecao).execute()
        if response.data:
            print(f"✅ Proteção '{nome_protecao}' atualizada com sucesso.")
            return response.data[0]
        else:
            print(f"⚠️ Nenhuma proteção encontrada com nome '{nome_protecao}'.")
            return None
    except Exception as e:
        print(f"❌ Erro ao editar proteção '{nome_protecao}': {e}")
        return None

def remover_protecao(nome):
    try:
        supabase.table("Protecoes").delete().eq("nome", nome).execute()
        print(f"🗑️ Proteção '{nome}' removida com sucesso.")
        return True
    except Exception as e:
        print(f"❌ Erro ao remover proteção '{nome}': {e}")
        return False


def salvar_npc(dados_npc):
    try:
        response = supabase.table("NPCs").insert(dados_npc).execute()
        if response.data:
            print(f"✅ NPC '{dados_npc.get('classe')}' salvo com sucesso.")
            return response.data[0]
        else:
            print("⚠️ Nenhum dado retornado ao salvar o NPC.")
            return None
    except Exception as e:
        print(f"❌ Erro ao salvar NPC '{dados_npc.get('classe', 'Sem classe')}': {e}")
        return None

def editar_npc(classe_npc, novos_dados):
    try:
        response = supabase.table("NPCs").update(novos_dados).eq("classe", classe_npc).execute()
        if response.data:
            print(f"✅ NPC '{classe_npc}' atualizado com sucesso.")
            return response.data[0]
        else:
            print(f"⚠️ Nenhum NPC encontrado com classe '{classe_npc}'.")
            return None
    except Exception as e:
        print(f"❌ Erro ao editar NPC '{classe_npc}': {e}")
        return None

def remover_npc(classe):
    try:
        supabase.table("NPCs").delete().eq("classe", classe).execute()
        print(f"🗑️ NPC '{classe}' removido com sucesso.")
        return True
    except Exception as e:
        print(f"❌ Erro ao remover NPC '{classe}': {e}")
        return False


def salvar_buff_debuff(dados):
    try:
        response = supabase.table("BuffsDebuffs").insert(dados).execute()
        if response.data:
            print(f"✅ Buff/Debuff '{dados.get('nome')}' salvo com sucesso.")
            return response.data[0]
        return None
    except Exception as e:
        print(f"❌ Erro ao salvar Buff/Debuff '{dados.get('nome', 'Sem nome')}': {e}")
        return None

def editar_buff_debuff(nome, novos_dados):
    try:
        response = supabase.table("BuffsDebuffs").update(novos_dados).eq("nome", nome).execute()
        if response.data:
            print(f"✅ Buff/Debuff '{nome}' atualizado com sucesso.")
            return response.data[0]
        return None
    except Exception as e:
        print(f"❌ Erro ao editar Buff/Debuff '{nome}': {e}")
        return None

def remover_buff_debuff(nome):
    try:
        supabase.table("BuffsDebuffs").delete().eq("nome", nome).execute()
        print(f"🗑️ Buff/Debuff '{nome}' removido com sucesso.")
        return True
    except Exception as e:
        print(f"❌ Erro ao remover Buff/Debuff '{nome}': {e}")
        return False


def salvar_habilidade(dados):
    try:
        response = supabase.table("Habilidades").insert(dados).execute()
        if response.data:
            print(f"✅ Habilidade '{dados.get('nome')}' salva com sucesso.")
            return response.data[0]
        return None
    except Exception as e:
        print(f"❌ Erro ao salvar habilidade '{dados.get('nome', 'Sem nome')}': {e}")
        return None

def editar_habilidade(nome, novos_dados):
    try:
        response = supabase.table("Habilidades").update(novos_dados).eq("nome", nome).execute()
        if response.data:
            print(f"✅ Habilidade '{nome}' atualizada com sucesso.")
            return response.data[0]
        return None
    except Exception as e:
        print(f"❌ Erro ao editar habilidade '{nome}': {e}")
        return None

def remover_habilidade(nome):
    try:
        supabase.table("Habilidades").delete().eq("nome", nome).execute()
        print(f"🗑️ Habilidade '{nome}' removida com sucesso.")
        return True
    except Exception as e:
        print(f"❌ Erro ao remover habilidade '{nome}': {e}")
        return False


def salvar_poder(dados):
    try:
        response = supabase.table("Poderes").insert(dados).execute()
        if response.data:
            print(f"✅ Poder '{dados.get('nome')}' salvo com sucesso.")
            return response.data[0]
        return None
    except Exception as e:
        print(f"❌ Erro ao salvar poder '{dados.get('nome', 'Sem nome')}': {e}")
        return None

def editar_poder(nome, novos_dados):
    try:
        response = supabase.table("Poderes").update(novos_dados).eq("nome", nome).execute()
        if response.data:
            print(f"✅ Poder '{nome}' atualizado com sucesso.")
            return response.data[0]
        return None
    except Exception as e:
        print(f"❌ Erro ao editar poder '{nome}': {e}")
        return None

def remover_poder(nome):
    try:
        supabase.table("Poderes").delete().eq("nome", nome).execute()
        print(f"🗑️ Poder '{nome}' removido com sucesso.")
        return True
    except Exception as e:
        print(f"❌ Erro ao remover poder '{nome}': {e}")
        return False
# === FUNÇÕES DE SALVAMENTO E EDIÇÃO SUPABASE === #

# === DESERIALIZAÇÃO DE ITENS === #
def deserialize_object_with_class(obj, _visited_objects=None, _processing_items=None):
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
        return obj
    if obj_id:
        _visited_objects.add(obj_id)

    try:
        if obj is None or isinstance(obj, (str, int, float, bool)):
            return obj

        if isinstance(obj, list):
            return [deserialize_object_with_class(item, _visited_objects, _processing_items) for item in obj]

        if isinstance(obj, dict):
            # Proficiencia simples → retorna como está
            if "nome" in obj and "atributo" in obj and ("nivel" in obj or "valor" in obj) and "__class__" not in obj:
                return obj

            if "__class__" in obj:
                class_name = obj["__class__"]
                item_identifier = f"{class_name}_{obj.get('nome', 'unknown')}_{obj.get('Id', id(obj))}"

                if item_identifier in _processing_items:
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
                        return safe_data

                    elif class_name == "Inventario":
                        try:
                            if hasattr(Inventario, 'from_dict'):
                                return Inventario.from_dict(safe_data)
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
                            return inventario
                        except Exception as e:
                            return safe_data

                    elif class_name in ["Ranged", "Melee", "Protecao", "Consumivel", "Explosivo", "Municao", "Melhoria", "Item"]:
                        return reconstruct_item_from_data(safe_data, class_name, _processing_items)

                    else:
                        try:
                            class_obj = globals().get(class_name)
                            if class_obj and hasattr(class_obj, 'from_dict'):
                                return class_obj.from_dict(safe_data)
                            else:
                                return safe_data
                        except Exception as e:
                            return safe_data

                finally:
                    _processing_items.discard(item_identifier)

            else:
                # Dicionário comum → processa recursivamente
                return {key: deserialize_object_with_class(value, _visited_objects, _processing_items) for key, value in obj.items()}

        return obj

    finally:
        if obj_id and obj_id in _visited_objects:
            _visited_objects.remove(obj_id)

def serializar_item(item):
    """Serializa um item para dicionário"""
    if item is None:
        return None
    if hasattr(item, 'to_dict'):
        item_dict = item.to_dict()
        item_dict["__class__"] = item.__class__.__name__
        return item_dict
    return None

def serializar_item_com_melhorias(item):
    """
    Serializa itens Ranged, Melee ou Protecao removendo temporariamente as melhorias
    VERSÃO CORRIGIDA - Evita loops na serialização
    """
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
    
    return data

def deserializar_item(data):
    """Deserializa um item de dicionário para objeto"""
    if data is None:
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
                return class_obj.from_dict(item_data)
        except Exception as e:
            pass
    
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
    try:
        if _processing_items is None:
            _processing_items = set()
            
        # Se item_data já é um objeto (não é dict), retorna como está
        if not isinstance(item_data, dict):
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
        
        # Tenta carregar do banco primeiro (se o nome existir)
        if "nome" in item_data:
            try:
                item_do_banco = carregar_item_por_nome(item_data["nome"])
                if item_do_banco:
                    return item_do_banco
            except Exception as e:
                pass
        
        # Reconstrói baseado na classe específica
        if class_name == "Ranged":
            return reconstruct_ranged(item_data, _processing_items)
        elif class_name == "Melee":
            return reconstruct_melee(item_data, _processing_items)
        elif class_name == "Protecao":
            return reconstruct_protecao(item_data, _processing_items)
        elif class_name == "Municao":
            return reconstruct_municao(item_data)
        elif class_name == "Explosivo":
            return reconstruct_explosivo(item_data)
        elif class_name == "Consumivel":
            return reconstruct_consumivel(item_data)
        elif class_name == "Melhoria":
            return reconstruct_melhoria(item_data)
        elif class_name == "Item":
            return reconstruct_item(item_data)
        else:
            return item_data
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return item_data

def reconstruct_item(item_data):
    """Reconstrói um Item básico"""
    from Codigos import Item
    
    return Item(
        nome=item_data.get("nome", "Item"),
        peso=item_data.get("peso")
    )

def reconstruct_consumivel(item_data):
    """Reconstrói um Consumível"""
    from Codigos import Consumivel
    
    return Consumivel(
        nome=item_data.get("nome", "Consumível"),
        peso=item_data.get("peso", 1.0),
        cura=item_data.get("cura", 0),
        energia=item_data.get("energia", 0)
    )

def reconstruct_explosivo(item_data):
    """Reconstrói um Explosivo"""
    from Codigos import Explosivo
    
    return Explosivo(
        nome=item_data.get("nome", "Explosivo"),
        peso=item_data.get("peso", 1.0),
        raio=item_data.get("raio", 1),
        dano=item_data.get("dano", 10),
        tipo_dano=item_data.get("tipo_dano", 1)
    )

def reconstruct_municao(item_data):
    """Reconstrói uma Munição"""
    from Codigos import Municao
    
    return Municao(
        nome=item_data.get("nome", "Munição"),
        calibre=item_data.get("calibre", ".22"),
        perfuracao=item_data.get("perfuracao", 1),
        dano=item_data.get("dano", 5)
    )

def reconstruct_melhoria(item_data):
    """Reconstrói uma Melhoria"""
    from Codigos import Melhoria
    
    return Melhoria(
        nome=item_data.get("nome", "Melhoria"),
        peso=item_data.get("peso", 0.1),
        tipo=item_data.get("tipo", "ranged"),
        modificadores=item_data.get("modificadores", {})
    )

def reconstruct_ranged(item_data, _processing_items=None):
    """Reconstrói uma arma Ranged com proteção contra loops - reconstruindo melhorias separadamente"""
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
                return item_data
        
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
                                pass
                    else:
                        acessorios_reconstruidos.append(acessorio_data)
                except Exception as e:
                    continue
            
            # Agora equipa todas as melhorias no item usando o método oficial
            for acessorio in acessorios_reconstruidos:
                try:
                    item.adicionar_acessorio(acessorio)
                except Exception as e:
                    pass
        
        return item
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return item_data

def reconstruct_melee(item_data, _processing_items=None):
    """Reconstrói uma arma Melee com proteção contra loops - reconstruindo melhorias separadamente"""
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
                return item_data
        
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
                                pass
                    else:
                        melhorias_reconstruidas.append(melhoria_data)
                except Exception as e:
                    continue
            
            # Agora equipa todas as melhorias no item usando o método oficial
            for melhoria in melhorias_reconstruidas:
                try:
                    item.adicionar_melhoria(melhoria)
                except Exception as e:
                    pass
        
        return item
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return item_data

def reconstruct_protecao(item_data, _processing_items=None):
    """Reconstrói uma proteção com proteção contra loops - reconstruindo melhorias separadamente"""
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
                return item_data
        
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
                                pass
                    else:
                        melhorias_reconstruidas.append(melhoria_data)
                except Exception as e:
                    continue
            
            # Agora equipa todas as melhorias no item usando o método oficial
            for melhoria in melhorias_reconstruidas:
                try:
                    item.adicionar_melhoria(melhoria)
                except Exception as e:
                    pass
        
        return item
        
    except Exception as e:
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
    VERSÃO CORRIGIDA - Trata proteções equipadas em personagens
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
        
        # Para itens com nome, retorna uma referência que pode ser resolvida depois
        if hasattr(obj, 'nome'):
            return {
                "__circular_ref__": True,
                "__class__": obj_type,
                "__nome__": obj.nome,  # Permite buscar no banco depois
                "__id__": obj_id,
                "__path__": _path
            }
        
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

def serializar_objeto(obj, _visited_objects=None, _path="root"):
    """
    Serializa qualquer objeto preservando informação de classe e prevenindo loops infinitos
    VERSÃO CORRIGIDA - Trata proteções equipadas em personagens
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
        
        # Para itens com nome, retorna uma referência que pode ser resolvida depois
        if hasattr(obj, 'nome'):
            return {
                "__circular_ref__": True,
                "__class__": obj_type,
                "__nome__": obj.nome,  # Permite buscar no banco depois
                "__id__": obj_id,
                "__path__": _path
            }
        
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

def deserializar_objeto(obj, pools=None, _objetos_resolvidos=None):
    """
    Deserializa objeto e re-equipa melhorias se necessário
    VERSÃO CORRIGIDA - Resolve referências circulares e proteções
    """
    # Inicializa cache de objetos resolvidos
    if _objetos_resolvidos is None:
        _objetos_resolvidos = {}
        print(f"🔄 Iniciando deserialização")
    
    # Detecta referências circulares
    if isinstance(obj, dict) and obj.get("__circular_ref__"):
        class_name = obj.get("__class__", "Unknown")
        obj_id = obj.get("__id__", "unknown")
        nome = obj.get("__nome__")
        path = obj.get("__path__", "unknown")
        
        print(f"  ⚠️  Referência circular detectada: {class_name} (id={obj_id}) em {path}")
        
        # Se já resolvemos este objeto antes, retorna a referência
        if obj_id in _objetos_resolvidos:
            print(f"    ✅ Objeto já resolvido anteriormente")
            return _objetos_resolvidos[obj_id]
        
        # Se tem nome, tenta buscar do banco
        if nome:
            print(f"    🔍 Tentando carregar '{nome}' do banco")
            try:
                item_do_banco = carregar_item_por_nome(nome)
                if item_do_banco:
                    print(f"      ✅ '{nome}' carregado do banco")
                    _objetos_resolvidos[obj_id] = item_do_banco
                    return item_do_banco
            except Exception as e:
                print(f"      ⚠️  Erro ao carregar do banco: {e}")
        
        # Se não conseguiu resolver, retorna None
        print(f"    ⚠️  Não foi possível resolver referência circular")
        return None
    
    # Casos base
    if not isinstance(obj, dict):
        return obj
    
    # Primeiro deserializa o objeto base
    resultado = deserialize_object_with_class(obj)
    
    # Guarda no cache
    if isinstance(obj, dict) and "__id__" in obj:
        _objetos_resolvidos[obj["__id__"]] = resultado
    
    # Se é um dict com dados serializados de melhorias, processa separadamente
    if isinstance(obj, dict) and obj.get("__class__") in ['Ranged', 'Melee', 'Protecao']:
        class_name = obj.get("__class__")
        print(f"  ➡️  Deserializando {class_name} com melhorias")
        
        # Processa melhorias serializadas
        if "__melhorias_serializadas__" in obj:
            melhorias_data = obj["__melhorias_serializadas__"]
            print(f"    🛠  Reequipando {len(melhorias_data)} melhorias")
            
            for i, melhoria_data in enumerate(melhorias_data):
                try:
                    # Deserializa recursivamente (com cache)
                    melhoria = deserializar_objeto(melhoria_data, pools, _objetos_resolvidos)
                    
                    if melhoria:
                        if class_name == 'Ranged':
                            resultado.adicionar_acessorio(melhoria)
                            print(f"        ✅ Acessório {i+1} adicionado")
                        else:
                            resultado.adicionar_melhoria(melhoria)
                            print(f"        ✅ Melhoria {i+1} adicionada")
                except Exception as e:
                    print(f"      ⚠️  Erro ao reequipar melhoria {i}: {e}")
        
        # Processa acessórios serializados
        if "__acessorios_serializados__" in obj:
            acessorios_data = obj["__acessorios_serializados__"]
            print(f"    🛠  Reequipando {len(acessorios_data)} acessórios")
            
            for i, acessorio_data in enumerate(acessorios_data):
                try:
                    # Deserializa recursivamente (com cache)
                    acessorio = deserializar_objeto(acessorio_data, pools, _objetos_resolvidos)
                    
                    if acessorio:
                        resultado.adicionar_acessorio(acessorio)
                        print(f"        ✅ Acessório {i+1} adicionado")
                except Exception as e:
                    print(f"      ⚠️  Erro ao reequipar acessório {i}: {e}")
    
    print(f"✅ Deserialização concluída")
    return resultado

def deserializar_item(item_data):
    """
    Deserializa um item que pode vir como dict ou objeto já instanciado
    VERSÃO CORRIGIDA - Trata objetos já instanciados e referências circulares
    """
    # Se é None, retorna None
    if item_data is None:
        return None
    
    # NOVO: Se já é uma instância de classe (não é dict), retorna direto
    if not isinstance(item_data, dict):
        # Verifica se é realmente um objeto (tem __class__ mas não é tipo primitivo)
        if hasattr(item_data, '__class__') and not isinstance(item_data, (str, int, float, bool, list)):
            classe_nome = item_data.__class__.__name__
            print(f"  ✅ Item já instanciado: {classe_nome}")
            if hasattr(item_data, 'nome'):
                print(f"     Nome: {item_data.nome}")
            return item_data
        # Se não é objeto customizado, retorna como está
        return item_data
    
    # NOVO: Trata referências circulares
    if item_data.get("__circular_ref__"):
        classe = item_data.get("__class__", "Unknown")
        nome = item_data.get("__nome__")
        print(f"  🔄 Resolvendo referência circular: {classe}")
        
        if nome:
            try:
                print(f"     Buscando '{nome}' no banco...")
                item = carregar_item_por_nome(nome)
                if item:
                    print(f"     ✅ '{nome}' carregado do banco")
                    return item
            except Exception as e:
                print(f"     ⚠️  Erro ao carregar: {e}")
        
        print(f"     ⚠️  Não foi possível resolver referência")
        return None
    
    # Se é um dict com dados de item, processa normalmente
    nome_classe = item_data.get("__class__")
    
    if not nome_classe:
        # Tenta detectar o tipo pela estrutura
        if "dano" in item_data or "Dano" in item_data:
            if "alcance" in item_data or "Alcance" in item_data:
                nome_classe = "Ranged"
            else:
                nome_classe = "Melee"
        elif "protecao" in item_data or "Protecao" in item_data:
            nome_classe = "Protecao"
    
    # Importa as classes necessárias
    try:
        if nome_classe == "Ranged":
            from Codigos import Ranged
            if hasattr(Ranged, 'from_dict'):
                return Ranged.from_dict(item_data)
            else:
                item = Ranged()
                for key, value in item_data.items():
                    if not key.startswith('__'):
                        setattr(item, key, value)
                return item
        
        elif nome_classe == "Melee":
            from Codigos import Melee
            if hasattr(Melee, 'from_dict'):
                return Melee.from_dict(item_data)
            else:
                item = Melee()
                for key, value in item_data.items():
                    if not key.startswith('__'):
                        setattr(item, key, value)
                return item
        
        elif nome_classe == "Protecao":
            from Codigos import Protecao
            if hasattr(Protecao, 'from_dict'):
                return Protecao.from_dict(item_data)
            else:
                item = Protecao()
                for key, value in item_data.items():
                    if not key.startswith('__'):
                        setattr(item, key, value)
                return item
        
        else:
            print(f"  ⚠️  Classe desconhecida: {nome_classe}")
            return None
            
    except Exception as e:
        print(f"  ❌ Erro ao deserializar item: {e}")
        import traceback
        traceback.print_exc()
        return None

def deserialize_object_with_class(obj):
    """
    Deserializa objeto baseado no campo __class__
    VERSÃO CORRIGIDA - Compatível com objetos já instanciados
    """
    # Se não é dict, retorna como está
    if not isinstance(obj, dict):
        return obj
    
    # Se não tem classe especificada, retorna o dict
    if "__class__" not in obj:
        return obj
    
    classe_nome = obj.get("__class__")
    
    # Remove metadados antes de criar o objeto
    dados_limpos = {k: v for k, v in obj.items() if not k.startswith('__')}
    
    try:
        # Tenta importar e instanciar a classe
        if classe_nome == "Personagem":
            from Codigos import Personagem
            if hasattr(Personagem, 'from_dict'):
                return Personagem.from_dict(obj)
            else:
                personagem = Personagem()
                for key, value in dados_limpos.items():
                    setattr(personagem, key, value)
                return personagem
        
        elif classe_nome in ["Ranged", "Melee", "Protecao"]:
            # Usa deserializar_item para estes casos
            return deserializar_item(obj)
        
        else:
            # Para outras classes, retorna o dict
            return dados_limpos
            
    except Exception as e:
        print(f"⚠️  Erro ao instanciar {classe_nome}: {e}")
        return dados_limpos

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
    VERSÃO CORRIGIDA - Trata personagens com proteções equipadas
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
        
        print("🔄 Reconstruindo personagens e equipamentos...")
        
        # Reconstrói os grupos de personagens
        GruposDePersonagens = {}
        personagens_carregados = 0
        personagens_com_erro = 0
        
        for grupo, lista_personagens in dados_sessao.items():
            # Ignora dados especiais dos kits
            if grupo == "__kits_disponiveis__":
                try:
                    KitsDisponíveis = deserializar_objeto(lista_personagens, pools)
                    print(f"📦 {len(KitsDisponíveis)} kits carregados")
                except Exception as e:
                    print(f"⚠️ Erro ao carregar kits: {e}")
                continue
            
            GruposDePersonagens[grupo] = []
            print(f"\n📂 Processando grupo '{grupo}'...")
            
            for idx, dados_personagem in enumerate(lista_personagens):
                try:
                    print(f"  👤 Carregando personagem {idx+1}...")
                    
                    # Deserializa recursivamente para reconstituir objetos
                    dados_deserializados = deserializar_objeto(dados_personagem, pools)
                    
                    # Reconstrói o personagem
                    if hasattr(Personagem, 'from_dict'):
                        personagem = Personagem.from_dict(dados_deserializados)
                    else:
                        personagem = Personagem()
                        for attr, valor in dados_deserializados.items():
                            if not attr.startswith('__'):  # Ignora metadados
                                setattr(personagem, attr, valor)
                    
                    GruposDePersonagens[grupo].append(personagem)
                    personagens_carregados += 1
                    
                    # Mostra info do personagem carregado
                    nome_personagem = getattr(personagem, 'nome', 'Sem nome')
                    tem_protecao = hasattr(personagem, 'Protecao') and personagem.Protecao is not None
                    print(f"    ✅ {nome_personagem} carregado {'(com proteção)' if tem_protecao else ''}")
                    
                except Exception as e:
                    print(f"    ❌ Erro ao carregar personagem {idx+1}: {e}")
                    personagens_com_erro += 1
                    import traceback
                    traceback.print_exc()
                    continue
        
        print(f"\n{'='*60}")
        print(f"✅ Sessão carregada:")
        print(f"   • {len(GruposDePersonagens)} grupos")
        print(f"   • {personagens_carregados} personagens carregados")
        if personagens_com_erro > 0:
            print(f"   ⚠️  {personagens_com_erro} personagens com erro")
        print(f"{'='*60}\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao carregar sessão: {e}")
        import traceback
        traceback.print_exc()
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

# === SISTEMA DE SESSÕES === #

# === SISTEMA DE KITS === #
def carregar_kits_db():
    """Carrega kits do banco de dados usando apenas o campo inventario_dados"""
    try:
        print("🔄 Carregando kits do banco de dados...")
        
        dados_tabelas = carregar_todos_dados()
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
            
            kit = Kits(nome, raridade)
            kit.id_db = kit_id
            kit.inventario = Inventario()

            inventario_serializado = kit_data.get("inventario_dados")
            if inventario_serializado:
                try:
                    inventario_deserializado = deserializar_objeto(inventario_serializado, dados_tabelas)
                    
                    if inventario_deserializado:
                        if isinstance(inventario_deserializado, list):
                            kit.inventario = Inventario.from_dict({"itens": inventario_deserializado})
                        elif isinstance(inventario_deserializado, Inventario):
                            kit.inventario = inventario_deserializado
                        else:
                            print(f"⚠️ Inventário de {nome} veio em formato inesperado: {type(inventario_deserializado)}")
                    
                        print(f"✅ Inventário carregado ({len(kit.inventario.itens)} itens)")
                except Exception as e:
                    print(f"❌ Erro ao deserializar inventário de {nome}: {e}")
            
            kits[nome] = kit
        
        print(f"✅ Carregados {len(kits)} kits do banco de dados")
        return kits
        
    except Exception as e:
        print(f"❌ Erro crítico ao carregar kits do banco: {e}")
        import traceback
        traceback.print_exc()
        return {}

def salvar_kit_no_banco(kit):
    try:
        print(f"💾 Salvando kit: {kit.nome}")
        
        inventario_serializado = None
        if kit.inventario and hasattr(kit.inventario, 'itens'):
            inventario_serializado = serializar_objeto(kit.inventario)
        
        dados_kit = {
            "nome": kit.nome,
            "raridade": kit.raridade,
            "inventario_dados": inventario_serializado
        }
        
        # Busca se já existe
        response = supabase.table("kits").select("id").eq("nome", kit.nome).execute()
        
        if response.data:
            kit_id = response.data[0]["id"]
            supabase.table("kits").update(dados_kit).eq("id", kit_id).execute()
            kit.id_db = kit_id
            print(f"🔄 Kit existente atualizado")
        else:
            response = supabase.table("kits").insert(dados_kit).execute()
            kit_id = response.data[0]["id"]
            kit.id_db = kit_id
            print(f"🆕 Novo kit criado")
        
        print(f"✅ Kit '{kit.nome}' salvo com sucesso no banco")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao salvar kit '{kit.nome}': {e}")
        import traceback
        traceback.print_exc()
        return False

def deletar_kit_do_banco(nome_kit):
    """Deleta um kit do banco de dados"""
    try:
        supabase.table("kits").delete().eq("nome", nome_kit).execute()
        
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
        response = supabase.table("kits").select("nome, raridade, id, inventario_dados").order("nome").execute()
        
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
            inventario_serializado = kit_data.get("inventario_dados")
            
            total_itens = 0
            if inventario_serializado:
                try:
                    inventario = deserializar_objeto(inventario_serializado, carregar_todos_dados())
                    if inventario and hasattr(inventario, "itens"):
                        total_itens = len(inventario.itens)
                except:
                    total_itens = 0
            
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
        response = supabase.table("kits").select("*").eq("nome", nome_kit).execute()
        
        if not response.data:
            return False, "Kit não encontrado no banco"
        
        kit_data = response.data[0]
        inventario_serializado = kit_data.get("inventario_dados")
        
        if not inventario_serializado:
            return True, "Kit válido mas sem itens"
        
        try:
            deserializar_objeto(inventario_serializado, carregar_todos_dados())
            return True, "Kit válido e carregável"
        except Exception as e:
            return False, f"Erro na deserialização: {str(e)}"
        
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
        
        dados_tabelas = carregar_todos_dados()
        response = supabase.table("kits").select("*").eq("nome", kit_nome).execute()
        
        if not response.data:
            print(f"❌ Kit '{kit_nome}' não encontrado no banco")
            return None
        
        kit_data = response.data[0]
        kit_id = kit_data["id"]
        
        kit = Kits(kit_data["nome"], kit_data["raridade"])
        kit.id_db = kit_id
        kit.inventario = Inventario()
        
        inventario_serializado = kit_data.get("inventario_dados")
        if inventario_serializado:
            inventario_deserializado = deserializar_objeto(inventario_serializado, dados_tabelas)
            if isinstance(inventario_deserializado, list):
                kit.inventario = Inventario.from_dict({"itens": inventario_deserializado})
            elif isinstance(inventario_deserializado, Inventario):
                kit.inventario = inventario_deserializado
        
        global KitsDisponíveis
        KitsDisponíveis[kit_nome] = kit
        
        print(f"✅ Kit '{kit_nome}' atualizado com sucesso")
        return kit
        
    except Exception as e:
        print(f"❌ Erro ao atualizar kit '{kit_nome}': {e}")
        return None

def debug_kit_inventario_detalhado(kit_nome):
    """Função de debug para verificar o inventário de um kit"""
    try:
        if kit_nome not in KitsDisponíveis:
            print(f"❌ Kit '{kit_nome}' não encontrado")
            return
        
        kit = KitsDisponíveis[kit_nome]
        print(f"\n🔍 DEBUG DETALHADO - Kit: {kit_nome}")
        print("=" * 60)
        print(f"📋 Raridade: {kit.raridade}")
        print(f"🆔 ID no banco: {getattr(kit, 'id_db', 'Não definido')}")
        
        if hasattr(kit, 'inventario'):
            inventario = kit.inventario
            print(f"📦 Tipo do inventário: {type(inventario)}")
            print(f"📦 Quantidade de itens: {len(inventario.itens) if hasattr(inventario, 'itens') else 0}")
            
            if hasattr(inventario, 'itens') and inventario.itens:
                print(f"\n🔬 ITENS:")
                for i, item in enumerate(inventario.itens[:5]):  # Mostra só os 5 primeiros
                    nome_item = getattr(item.item, 'nome', 'SEM_NOME') if hasattr(item, 'item') else getattr(item, 'nome', 'SEM_NOME')
                    print(f"  {i+1}. {nome_item} (quantidade: {getattr(item, 'quantidade', '?')})")
        else:
            print("❌ Kit não tem inventário")
                    
    except Exception as e:
        print(f"❌ Erro no debug detalhado: {e}")

def testar_carregamento_completo():
    """Teste completo do sistema de kits"""
    print("🧪 TESTE COMPLETO DO SISTEMA DE KITS")
    print("=" * 60)
    
    kits_carregados = carregar_kits_db()
    
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