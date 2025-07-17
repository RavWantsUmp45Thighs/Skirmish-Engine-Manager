from Codigos import Personagem, Inventario, SistemaDeProficiencias, Ranged, Melee, Protecao, Item, Consumivel, Explosivo, Municao, Melhoria, Proficiencia, NPC
import json
import os
from supabase import create_client, Client
from typing import Dict, List, Any, Optional, Union
import traceback

url = "https://eozqdonfmtlzmhoyyznn.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVvenFkb25mbXRsem1ob3l5em5uIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg3MTQ0NzQsImV4cCI6MjA2NDI5MDQ3NH0.MQgpQHtzgGaHRwAQPONtFd4z3-sG_zRYNMqPjZ-BU94"
supabase: Client = create_client(url, key)
from datetime import datetime

# === POOLS DE ITEMS === #
def montar_pools_db():
    """Carrega todos os pools de dados do banco de dados"""
    def carregar_tabela_para_pool(nome_tabela, classe, chave="nome"):
        try:
            response = supabase.table(nome_tabela).select("*").execute()
            data = response.data
            pool = {}
            for item in data:
                obj = classe(**item)
                chave_item = item.get(chave)
                if chave_item:
                    pool[chave_item] = obj
            return pool
        except Exception as e:
            print(f"Erro ao carregar tabela {nome_tabela}: {e}")
            return {}

    Pools = {
        "Ranged": carregar_tabela_para_pool("Rangeds", Ranged, chave="nome"),
        "Melee": carregar_tabela_para_pool("Melees", Melee, chave="nome"),
        "Protecao": carregar_tabela_para_pool("Protecoes", Protecao, chave="nome"),
        "Item": carregar_tabela_para_pool("Itens", Item),
        "Consumivel": carregar_tabela_para_pool("Consumiveis", Consumivel),
        "Explosivo": carregar_tabela_para_pool("Explosivos", Explosivo),
        "Municao": carregar_tabela_para_pool("Municoes", Municao),
        "Melhoria": carregar_tabela_para_pool("Melhorias", Melhoria),
    }
    return Pools

def refresh_pools():
    """Recarrega todos os pools do banco de dados"""
    global Pools, Proficiencias
    print("Atualizando dados do banco...")
    Pools = montar_pools_db()
    Proficiencias = carregar_proficiencias_db()
    print("Dados atualizados com sucesso!")

def carregar_item_por_nome(nome_item, Pools):
    """Carrega um item específico por nome"""
    for pool in Pools.values():
        if nome_item in pool:
            return pool[nome_item]
    raise ValueError(f"Item '{nome_item}' não encontrado.")

def filtrar_itens(pool_nome: str, filtros: Dict[str, Any] = None) -> Dict[str, Any]:
    if pool_nome not in Pools:
        return {}
    pool = Pools[pool_nome]
    if not filtros:
        return pool
    itens_filtrados = {}
    for nome, item in pool.items():
        incluir_item = True
        for atributo, valor_filtro in filtros.items():
            if hasattr(item, atributo):
                valor_item = getattr(item, atributo)
                # Se o valor do filtro é uma lista, verifica se o valor do item está na lista
                if isinstance(valor_filtro, list):
                    if valor_item not in valor_filtro:
                        incluir_item = False
                        break
                # Se é string, faz comparação direta
                elif isinstance(valor_filtro, str):
                    if valor_item != valor_filtro:
                        incluir_item = False
                        break
                # Para números, permite comparação direta
                else:
                    if valor_item != valor_filtro:
                        incluir_item = False
                        break
            else:
                # Se o item não tem o atributo, não inclui
                incluir_item = False
                break
        if incluir_item:
            itens_filtrados[nome] = item
    return itens_filtrados

def obter_valores_unicos(pool_nome: str, atributo: str) -> List[Any]:
    if pool_nome not in Pools:
        return []
    valores = set()
    pool = Pools[pool_nome]
    for item in pool.values():
        if hasattr(item, atributo):
            valor = getattr(item, atributo)
            if valor is not None:
                valores.add(valor)
    return sorted(list(valores))

def buscar_itens_por_nome(termo_busca: str, pool_nome: str = None) -> Dict[str, Any]:
    resultados = {}
    pools_para_buscar = [pool_nome] if pool_nome else Pools.keys()
    for pool_key in pools_para_buscar:
        if pool_key in Pools:
            for nome, item in Pools[pool_key].items():
                if termo_busca.lower() in nome.lower():
                    resultados[f"{pool_key}_{nome}"] = item
    return resultados
# === POOLS DE ITEMS === #

# === PERSONAGENS E NPCS === #
def carregar_personagens_db():
    """Carrega personagens do banco de dados e os separa em grupos."""
    try:
        response = supabase.table("personagens").select("*").execute()
        data = response.data

        grupos = {}

        for item in data:
            grupo = item.get("grupo", "SemGrupo") or "SemGrupo"
            dados_json = json.loads(item["dados"]) if isinstance(item["dados"], str) else item["dados"]

            personagem = Personagem.from_dict(dados_json)
            personagem.id_db = item["id"]

            if grupo not in grupos:
                grupos[grupo] = []
            grupos[grupo].append(personagem)

        return grupos

    except Exception as e:
        print(f"Erro ao carregar personagens do banco: {e}")
        traceback.print_exc()

def carregar_tipos_npcs_db():
    """Carrega tipos de NPCs do banco"""
    try:
        response = supabase.table("NPCs").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Erro ao carregar tipos de NPCs: {e}")
        return []

def carregar_tipos_npcs_por_grupo():
    data = carregar_tipos_npcs_db()
    grupos = {}
    for npc in data:
        grupo = npc["grupo"]
        if grupo not in grupos:
            grupos[grupo] = []
        grupos[grupo].append(npc)
    return grupos

def filtrar_npcs(filtros: Dict[str, Any] = None) -> List[Dict]:
    """
    Filtra NPCs baseado em critérios
    
    Args:
        filtros: Dict com critérios (grupo, nivel, etc.)
        
    Returns:
        Lista de NPCs filtrados
    """
    npcs = carregar_tipos_npcs_db()
    
    if not filtros:
        return npcs
    
    npcs_filtrados = []
    
    for npc in npcs:
        incluir_npc = True
        
        for atributo, valor_filtro in filtros.items():
            if atributo in npc:
                if isinstance(valor_filtro, list):
                    if npc[atributo] not in valor_filtro:
                        incluir_npc = False
                        break
                else:
                    if npc[atributo] != valor_filtro:
                        incluir_npc = False
                        break
            else:
                incluir_npc = False
                break
        
        if incluir_npc:
            npcs_filtrados.append(npc)
    
    return npcs_filtrados
# === PERSONAGENS E NPCS === #

# === PROFICIÊNCIAS === #
def carregar_proficiencias_db():
    """Carrega proficiências do banco"""
    try:
        response = supabase.table("Proficiencias").select("*").execute()
        data = response.data
        profs = {}
        for item in data:
            nome = item["nome"]
            profs[nome] = Proficiencia(nome, item["atributo"], item["valor"])
        return profs
    except Exception as e:
        print(f"Erro ao carregar proficiências: {e}")
        return {}

def filtrar_proficiencias(atributo: str = None) -> Dict[str, Proficiencia]:
    """
    Filtra proficiências por atributo
    
    Args:
        atributo: Atributo específico para filtrar
        
    Returns:
        Dict com proficiências filtradas
    """
    if not atributo:
        return Proficiencias
    
    profs_filtradas = {}
    for nome, prof in Proficiencias.items():
        if prof.atributo == atributo:
            profs_filtradas[nome] = prof
    
    return profs_filtradas

Proficiencias = carregar_proficiencias_db()
# === PROFICIÊNCIAS === #

# === SESSÕES === #
GruposDePersonagens = {}
KitsDisponíveis = {}

# === FUNÇÕES PARA KITS ===
def serialize_kit_sessao(kit_data):
    """Serializa um kit para salvar na sessão (apenas índices dos itens)"""
    try:
        kit_serializado = {
            "nome": kit_data.get("nome", ""),
            "descricao": kit_data.get("descricao", ""),
            "itens": []
        }
        
        # Processa os itens do kit
        itens = kit_data.get("itens", [])
        for item in itens:
            if isinstance(item, dict):
                # Se o item já está no formato de índice
                if "nome" in item and "tabela" in item:
                    kit_serializado["itens"].append({
                        "nome": item["nome"],
                        "tabela": item["tabela"],
                        "quantidade": item.get("quantidade", 1)
                    })
                else:
                    # Se é um objeto item, encontra sua tabela
                    nome_item = item.get("nome") or getattr(item, "nome", None)
                    if nome_item:
                        tabela = encontrar_tabela_do_item(nome_item)
                        kit_serializado["itens"].append({
                            "nome": nome_item,
                            "tabela": tabela,
                            "quantidade": item.get("quantidade", 1)
                        })
            else:
                # Se é um objeto item
                nome_item = getattr(item, "nome", None)
                if nome_item:
                    tabela = encontrar_tabela_do_item(nome_item)
                    kit_serializado["itens"].append({
                        "nome": nome_item,
                        "tabela": tabela,
                        "quantidade": 1
                    })
        
        return kit_serializado
        
    except Exception as e:
        print(f"Erro ao serializar kit: {e}")
        return {"nome": "Kit com erro", "descricao": "", "itens": []}

def deserialize_kit_sessao(kit_data):
    """Deserializa um kit carregado da sessão (carrega objetos pelos índices)"""
    try:
        kit_deserializado = {
            "nome": kit_data.get("nome", ""),
            "descricao": kit_data.get("descricao", ""),
            "itens": []
        }
        
        # Processa os itens do kit
        itens = kit_data.get("itens", [])
        for item_index in itens:
            nome_item = item_index.get("nome")
            tabela = item_index.get("tabela")
            quantidade = item_index.get("quantidade", 1)
            
            if nome_item and tabela:
                # Carrega o item do pool correspondente
                item_objeto = carregar_item_de_tabela(nome_item, tabela)
                if item_objeto:
                    kit_deserializado["itens"].append({
                        "nome": nome_item,
                        "tabela": tabela,
                        "quantidade": quantidade,
                        "objeto": item_objeto
                    })
        
        return kit_deserializado
        
    except Exception as e:
        print(f"Erro ao deserializar kit: {e}")
        return {"nome": "Kit com erro", "descricao": "", "itens": []}

def encontrar_tabela_do_item(nome_item):
    """Encontra em qual tabela/pool um item está localizado"""
    mapeamento_pools = {
        "Ranged": "Rangeds",
        "Melee": "Melees", 
        "Protecao": "Protecoes",
        "Item": "Itens",
        "Consumivel": "Consumiveis",
        "Explosivo": "Explosivos",
        "Municao": "Municoes",
        "Melhoria": "Melhorias"
    }
    
    for pool_nome, tabela_nome in mapeamento_pools.items():
        if pool_nome in Pools and nome_item in Pools[pool_nome]:
            return tabela_nome
    
    return "Itens"  # Fallback padrão

def carregar_item_de_tabela(nome_item, tabela):
    """Carrega um item específico de uma tabela pelos pools"""
    mapeamento_tabelas = {
        "Rangeds": "Ranged",
        "Melees": "Melee",
        "Protecoes": "Protecao", 
        "Itens": "Item",
        "Consumiveis": "Consumivel",
        "Explosivos": "Explosivo",
        "Municoes": "Municao",
        "Melhorias": "Melhoria"
    }
    
    pool_nome = mapeamento_tabelas.get(tabela)
    if pool_nome and pool_nome in Pools:
        return Pools[pool_nome].get(nome_item)
    
    return None
# === FUNÇÕES PARA KITS ===
# === SISTEMA DE SESSÕES === #
def listar_sessoes_disponiveis():
    """Lista todas as sessões disponíveis no banco de dados"""
    try:
        response = supabase.table("sessoes").select("nome, data_criacao").order("data_criacao", desc=True).execute()
        
        sessoes = []
        for sessao in response.data:
            sessoes.append({
                "nome": sessao["nome"],
                "data_criacao": sessao["data_criacao"],
                "data_formatada": datetime.fromisoformat(sessao["data_criacao"].replace('Z', '+00:00')).strftime("%d/%m/%Y %H:%M")
            })
        
        return sessoes
    except Exception as e:
        print(f"Erro ao listar sessões: {e}")
        return []

def deletar_sessao_do_supabase(nome_da_sessao):
    """Deleta uma sessão do banco de dados"""
    try:
        response = supabase.table("sessoes").delete().eq("nome", nome_da_sessao).execute()
        print(f"Sessão '{nome_da_sessao}' deletada com sucesso.")
        return True
    except Exception as e:
        print(f"Erro ao deletar sessão: {e}")
        return False
    
def verificar_sessao_existe(nome_da_sessao):
    """Verifica se uma sessão já existe no banco"""
    try:
        response = supabase.table("sessoes").select("nome").eq("nome", nome_da_sessao).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"Erro ao verificar sessão: {e}")
        return False

def salvar_sessao_no_supabase(nome_da_sessao, sobrescrever=False):
    """
    Salva a sessão atual no banco de dados (incluindo kits)
    """
    try:
        # Verifica se a sessão já existe
        if verificar_sessao_existe(nome_da_sessao) and not sobrescrever:
            print(f"Sessão '{nome_da_sessao}' já existe. Use sobrescrever=True para atualizar.")
            return False
        
        def serialize_object(obj):
            """Serializa qualquer objeto para JSON de forma recursiva"""
            if obj is None:
                return None
            
            if isinstance(obj, (str, int, float, bool)):
                return obj
            
            if isinstance(obj, list):
                return [serialize_object(item) for item in obj]
            
            if isinstance(obj, dict):
                return {key: serialize_object(value) for key, value in obj.items()}
            
            if hasattr(obj, 'to_dict'):
                return serialize_object(obj.to_dict())
            
            if hasattr(obj, '__dict__'):
                return serialize_object(vars(obj))
            
            return str(obj)

        def serialize_personagem(personagem):
            """Serializa um personagem para JSON"""
            try:
                if hasattr(personagem, 'to_dict'):
                    data = personagem.to_dict()
                else:
                    data = vars(personagem)
                
                return serialize_object(data)
                
            except Exception as e:
                print(f"Erro ao serializar personagem {getattr(personagem, 'nome', 'sem nome')}: {e}")
                return {
                    "nome": getattr(personagem, 'nome', 'Personagem'),
                    "erro_serializacao": str(e)
                }
        
        # Prepara dados dos personagens
        dados_personagens = {}
        for grupo, lista in GruposDePersonagens.items():
            dados_personagens[grupo] = [serialize_personagem(p) for p in lista]
        
        # Prepara dados dos kits (VERSÃO SIMPLIFICADA)
        dados_kits = {}
        for nome_kit, kit_data in KitsDisponíveis.items():
            dados_kits[nome_kit] = serialize_kit_sessao(kit_data)
        
        # Combina todos os dados
        dados_completos = {
            "personagens": dados_personagens,
            "kits": dados_kits
        }
        
        # Salva no banco
        if verificar_sessao_existe(nome_da_sessao) and sobrescrever:
            response = supabase.table("sessoes").update({
                "data_criacao": datetime.utcnow().isoformat(),
                "conteudo": dados_completos
            }).eq("nome", nome_da_sessao).execute()
        else:
            response = supabase.table("sessoes").insert({
                "nome": nome_da_sessao,
                "data_criacao": datetime.utcnow().isoformat(),
                "conteudo": dados_completos
            }).execute()
        
        print("Sessão (incluindo kits) salva com sucesso no Supabase.")
        return True
        
    except Exception as e:
        print(f"Erro ao salvar sessão: {e}")
        traceback.print_exc()
        return False

def carregar_sessao_do_supabase(nome_da_sessao):
    """Carrega uma sessão específica do banco de dados (incluindo kits)"""
    global GruposDePersonagens, KitsDisponíveis
    try:
        response = supabase.table("sessoes").select("conteudo").eq("nome", nome_da_sessao).order("data_criacao", desc=True).limit(1).execute()
        
        if not response.data:
            print(f"Nenhuma sessão chamada '{nome_da_sessao}' encontrada.")
            return False
        
        dados = response.data[0]["conteudo"]
        
        # Verifica formato da sessão
        if isinstance(dados, dict) and "personagens" in dados:
            dados_personagens = dados.get("personagens", {})
            dados_kits = dados.get("kits", {})
        else:
            dados_personagens = dados
            dados_kits = {}
        
        # Carrega personagens (mantém a lógica existente)
        def deserialize_personagem(data):
            import copy
            data = copy.deepcopy(data)
            
            if 'proficiencias' in data and isinstance(data['proficiencias'], dict):
                if 'proficiencias' in data['proficiencias']:
                    proficiencias_dict = data['proficiencias']['proficiencias']
                else:
                    proficiencias_dict = data['proficiencias']
                
                proficiencias_deserializadas = {}
                for nome, prof_data in proficiencias_dict.items():
                    if hasattr(prof_data, 'atributo') and hasattr(prof_data, 'nivel') and not isinstance(prof_data, dict):
                        proficiencias_deserializadas[nome] = {
                            'nome': getattr(prof_data, 'nome', nome),
                            'atributo': prof_data.atributo,
                            'nivel': prof_data.nivel
                        }
                    elif isinstance(prof_data, dict) and 'atributo' in prof_data and 'nivel' in prof_data:
                        proficiencias_deserializadas[nome] = prof_data
                    elif isinstance(prof_data, dict) and 'atributo' in prof_data and 'valor' in prof_data:
                        proficiencias_deserializadas[nome] = {
                            'nome': nome,
                            'atributo': prof_data['atributo'],
                            'nivel': prof_data['valor']
                        }
                    else:
                        proficiencias_deserializadas[nome] = {
                            'nome': nome,
                            'atributo': None,
                            'nivel': 0
                        }
                
                if 'proficiencias' in data['proficiencias']:
                    data['proficiencias'] = {'proficiencias': proficiencias_deserializadas}
                else:
                    data['proficiencias'] = proficiencias_deserializadas
            
            return Personagem.from_dict(data)
        
        # Carrega personagens
        GruposDePersonagens = {}
        for grupo, lista in dados_personagens.items():
            GruposDePersonagens[grupo] = [deserialize_personagem(p) for p in lista]
        
        # Carrega kits (VERSÃO SIMPLIFICADA)
        KitsDisponíveis = {}
        for nome_kit, kit_data in dados_kits.items():
            KitsDisponíveis[nome_kit] = deserialize_kit_sessao(kit_data)
        
        print(f"Sessão '{nome_da_sessao}' (incluindo kits) carregada com sucesso.")
        return True
        
    except Exception as e:
        print(f"Erro ao carregar sessão: {e}")
        traceback.print_exc()
        return False

def criar_nova_sessao():
    """Cria uma nova sessão vazia (limpa GruposDePersonagens)"""
    global GruposDePersonagens
    GruposDePersonagens = {}
    print("Nova sessão criada (dados limpos).")

def obter_info_sessao_atual():
    """Retorna informações sobre a sessão atual em memória"""
    total_personagens = sum(len(grupo) for grupo in GruposDePersonagens.values())
    grupos_info = {}
    
    for nome_grupo, personagens in GruposDePersonagens.items():
        grupos_info[nome_grupo] = {
            "quantidade": len(personagens),
            "nomes": [p.nome for p in personagens]
        }
    
    return {
        "total_grupos": len(GruposDePersonagens),
        "total_personagens": total_personagens,
        "grupos": grupos_info
    }

def duplicar_sessao(nome_origem, nome_destino):
    """Duplica uma sessão existente com um novo nome"""
    try:
        # Carrega a sessão origem
        response = supabase.table("sessoes").select("conteudo").eq("nome", nome_origem).order("data_criacao", desc=True).limit(1).execute()
        
        if not response.data:
            print(f"Sessão '{nome_origem}' não encontrada.")
            return False
        
        # Verifica se destino já existe
        if verificar_sessao_existe(nome_destino):
            print(f"Sessão '{nome_destino}' já existe.")
            return False
        
        # Cria nova sessão com o mesmo conteúdo
        dados = response.data[0]["conteudo"]
        response = supabase.table("sessoes").insert({
            "nome": nome_destino,
            "data_criacao": datetime.utcnow().isoformat(),
            "conteudo": dados
        }).execute()
        
        print(f"Sessão duplicada: '{nome_origem}' -> '{nome_destino}'")
        return True
        
    except Exception as e:
        print(f"Erro ao duplicar sessão: {e}")
        return False
# === SISTEMA DE SESSÕES ===  #

def obter_categorias_com_filtros():
    """
    Retorna estrutura organizada para uso na interface
    
    Returns:
        Dict com categorias e seus filtros disponíveis
    """
    categorias = {
        "Armas de Fogo": {
            "pool": "Ranged",
            "filtros_disponiveis": {
                "classe": obter_valores_unicos("Ranged", "classe"),
                "raridade": obter_valores_unicos("Ranged", "raridade"),
                "calibre": obter_valores_unicos("Ranged", "calibre"),
                "acao": obter_valores_unicos("Ranged", "acao")
            }
        },
        "Armas Corpo a Corpo": {
            "pool": "Melee",
            "filtros_disponiveis": {
                "classe": obter_valores_unicos("Melee", "classe"),
                "tipo_dano": obter_valores_unicos("Melee", "tipo_dano"),
                "raridade": obter_valores_unicos("Melee", "raridade")
            }
        },
        "Proteções": {
            "pool": "Protecao",
            "filtros_disponiveis": {
                "regiao": obter_valores_unicos("Protecao", "regiao")
            }
        },
        "Melhorias": {
            "pool": "Melhoria",
            "filtros_disponiveis": {
                "tipo": obter_valores_unicos("Melhoria", "tipo"),
                "raridade": obter_valores_unicos("Melhoria", "raridade")
            }
        },
        "Munições": {
            "pool": "Municao",
            "filtros_disponiveis": {
                "calibre": obter_valores_unicos("Municao", "calibre")
            }
        },
        "Consumíveis": {
            "pool": "Consumivel",
            "filtros_disponiveis": {
                "tipo": obter_valores_unicos("Consumivel", "tipo")
            }
        },
        "Explosivos": {
            "pool": "Explosivo",
            "filtros_disponiveis": {
                "tipo_dano": obter_valores_unicos("Explosivo", "tipo_dano")
            }
        },
        "Itens": {
            "pool": "Item",
            "filtros_disponiveis": {
            }
        }
    }
    
    return categorias

# === ALIASES PARA COMPATIBILIDADE ===
# Mantém compatibilidade com código existente
Pools = montar_pools_db()
Rangeds = Pools["Ranged"]
Melees = Pools["Melee"]  
Protecoes = Pools["Protecao"]
Melhorias = Pools["Melhoria"]
Municoes = Pools["Municao"]
Consumiveis = Pools["Consumivel"]
Explosivos = Pools["Explosivo"]
Items = Pools["Item"]