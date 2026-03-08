import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import Dados as D
import Codigos as CB
import re, random, json
import traceback
import math
try:
    from PIL import Image, ImageTk, ImageDraw, ImageFont
    PIL_DISPONIVEL = True
except ImportError:
    PIL_DISPONIVEL = False

# CONSTANTES VISUAIS
COR_BG          = "#0d0d1a"
COR_PAINEL      = "#130f26"
COR_ACENTO      = "#2d0a8c"
COR_ACENTO2     = "#4a1aac"
COR_BORDA       = "#3a1a6e"
COR_TEXTO       = "#e0d8ff"
COR_TEXTO_DIM   = "#7a6a9a"
COR_SELECIONADO = "#00e5ff"
COR_LINHA_DIST  = "#00e5ff"
COR_LINHA_MOV   = "#00ff88"
COR_AVISO       = "#ff6b35"

RAIO_TOKEN      = 20
FONTE_NOME      = ("Consolas", 9, "bold")
FONTE_LABEL     = ("Consolas", 10)
FONTE_TITULO    = ("Consolas", 13, "bold")
FONTE_DIST      = ("Consolas", 12, "bold")

CORES_GRUPO = {
    "_lista_superior": "#00ccff",
    "_lista_inferior": "#ff4444",
    "default":         "#aaaaff",
}

NIVEIS_COBERTURA = ["Nenhuma", "Parcial", "Alta", "Total"]
CORES_COBERTURA  = {
    "Nenhuma": None,
    "Parcial": "#ffcc00",
    "Alta":    "#ff8800",
    "Total":   "#cc0000",
}


### Funções universais ###
class Tooltip:
    def __init__(self, widget, texto, delay=300):
        self.widget = widget; self.texto = texto; self.delay = delay; self.tip = None; self.after_id = None
        widget.bind("<Enter>", self._schedule); widget.bind("<Leave>", self._hide); widget.bind("<Button>", self._hide)

    def _schedule(self, e=None): self.after_id = self.widget.after(self.delay, self._show)

    def _show(self):
        if self.tip or not self.texto: return
        x, y = self.widget.winfo_pointerx()+12, self.widget.winfo_pointery()+10
        self.tip = tk.Toplevel(self.widget); self.tip.overrideredirect(True); self.tip.configure(bg="#1a0869")
        tk.Label(self.tip, text=self.texto, bg="#1a0869", fg="white", font=("Arial", 10), wraplength=420, justify="left", padx=8, pady=4).pack()
        self.tip.geometry(f"+{x}+{y}")

    def _hide(self, e=None):
        if self.after_id: self.widget.after_cancel(self.after_id); self.after_id = None
        if self.tip: self.tip.destroy(); self.tip = None

# adicionar item #
ORDEM_CLASSES = [
    "Pistola", "Revolver", "Submetralhadora", "Escopeta", "Espingarda",
    "Carabina", "Fuzil de assalto", "Fuzil de batalha", "DMR",
    "Fuzil de precisão", "Metralhadora leve", "Metralhadora média",
    "Metralhadora pesada", "Fuzil antimaterial"
]
ORDEM_RARIDADES = ["Comum", "Incomum", "Rara", "Épica", "Exótica", "Lendária"]
PAGINAS = [
    ["Armas de Fogo", "Munições"],            # página 0 — especial
    ["Armas Corpo a Corpo", "Proteções"],
    ["Melhorias", "Equipamentos"],
    ["Itens", "Consumiveis"],
]

def abrir_popup_adicionar_item(master, personagem, on_finish=None):
    if not personagem: return

    popup = tk.Toplevel(master)
    popup.title("Adicionar Item")
    popup.configure(bg="#1a0869")
    popup.geometry("760x580")

    tabelas = {
        "Armas de Fogo": "Rangeds",
        "Armas Corpo a Corpo": "Melees",
        "Proteções": "Protecoes",
        "Melhorias": "Melhorias",
        "Munições": "Municoes",
        "Itens": "Itens",
        "Consumiveis": "Consumiveis",
        "Equipamentos": "Equipamentos",
    }

    pagina_atual = {"valor": 0}
    total_paginas = len(PAGINAS)

    tk.Label(popup, text="Categorias", bg="#1a0869", fg="white", font=("Arial", 18)).pack(pady=5)

    nav_frame = tk.Frame(popup, bg="#1a0869")
    nav_frame.pack(pady=5)

    frame_listas = tk.Frame(popup, bg="#1a0869")
    frame_listas.pack(expand=True)

    lista_frames = []

    def criar_lista(parent):
        container = tk.Frame(parent, bg="#1a0869")
        container.pack(side="left", padx=30)

        titulo = tk.Label(container, text="", bg="#1a0869", fg="white", font=("Arial", 14))
        titulo.pack(pady=5)

        canvas = tk.Canvas(container, bg="#1a0869", highlightthickness=0, width=300, height=400)
        lista = tk.Frame(canvas, bg="#1a0869")

        canvas.create_window((0, 0), window=lista, anchor="nw")
        lista.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.pack()

        _scroll_alvo = {"y": None}

        def _animar_scroll():
            atual = canvas.yview()[0]
            alvo  = _scroll_alvo["y"]
            if alvo is None:
                return
            diff = alvo - atual
            if abs(diff) < 0.001:
                canvas.yview_moveto(alvo)
                _scroll_alvo["y"] = None
                return
            canvas.yview_moveto(atual + diff * 0.15)
            canvas.after(16, _animar_scroll)

        def _scroll_suave(ev):
            total = canvas.bbox("all")
            if not total:
                return
            conteudo_h = total[3]
            view_h     = canvas.winfo_height()
            if conteudo_h <= view_h:
                return
            delta    = -1 if ev.delta > 0 else 1
            passo    = (view_h * 0.18) / conteudo_h
            atual    = _scroll_alvo["y"] if _scroll_alvo["y"] is not None else canvas.yview()[0]
            novo     = max(0.0, min(1.0, atual + delta * passo))
            iniciando = _scroll_alvo["y"] is None
            _scroll_alvo["y"] = novo
            if iniciando:
                _animar_scroll()

        def _bind_scroll_recursivo(widget):
            widget.bind("<MouseWheel>", _scroll_suave)
            for filho in widget.winfo_children():
                _bind_scroll_recursivo(filho)

        container._bind_scroll = _bind_scroll_recursivo
        container._canvas = canvas

        return titulo, lista

    lista_frames.append(criar_lista(frame_listas))
    lista_frames.append(criar_lista(frame_listas))

    # ── helpers de ordenação ──────────────────────────────────────────────────

    def _chave_ranged(item_tuple):
        nome, obj = item_tuple
        classe   = getattr(obj, "classe",   "") if hasattr(obj, "classe")   else ""
        raridade = getattr(obj, "raridade", "") if hasattr(obj, "raridade") else ""
        ci = ORDEM_CLASSES.index(classe)   if classe   in ORDEM_CLASSES   else 999
        ri = ORDEM_RARIDADES.index(raridade) if raridade in ORDEM_RARIDADES else 999
        return (ci, ri, nome)

    def _label_ranged(obj):
        """Retorna uma string extra com classe/raridade/modos/calibre/cap."""
        if not hasattr(obj, "classe"):
            return ""
        modos = "/".join(getattr(obj, "acoes_disparo", []))
        return (
            f"  {obj.classe} · {obj.raridade}\n"
            f"  {modos} | {obj.calibre} | {obj.capacidade} proj."
        )

    # ── renderização de listas ────────────────────────────────────────────────

    def _renderizar_lista(lista_widget, cat):
        """Preenche um frame de lista para a categoria dada."""
        for w in lista_widget.winfo_children():
            w.destroy()

        dados = D.carregar_tabela_especifica(tabelas[cat])

        if cat == "Armas de Fogo":
            itens = sorted(dados.items(), key=_chave_ranged)
        else:
            itens = list(dados.items())

        for nome, obj in itens:
            f = tk.Frame(lista_widget, bg="#1a0869")
            f.pack(fill="x", pady=2)

            if not hasattr(obj, "Id"):
                v = tk.StringVar(value="1")
                tk.Entry(f, textvariable=v, width=4).pack(side="right", padx=4)
            else:
                v = None

            if cat == "Armas de Fogo":
                extra = _label_ranged(obj)
                btn_text = f"{nome}\n{extra}".strip()
                btn = tk.Button(
                    f, text=btn_text, bg="#0e3386", fg="white",
                    width=28, font=("Arial", 10), justify="left",
                    anchor="w", wraplength=240,
                    command=lambda n=nome, o=obj, q=v, c=cat: adicionar(c, n, o, q)
                )
            else:
                btn = tk.Button(
                    f, text=nome, bg="#0e3386", fg="white",
                    width=26, font=("Arial", 11),
                    command=lambda n=nome, o=obj, q=v, c=cat: adicionar(c, n, o, q)
                )
            for container_frame, _ in lista_frames:
                # sobe até o container que tem _bind_scroll
                parent = lista_widget.master.master  # Frame > Canvas > container
                if hasattr(parent, "_bind_scroll"):
                    parent._bind_scroll(lista_widget)

            btn.pack(side="left", padx=4, pady=5)

    def atualizar_listas():
        pag = PAGINAS[pagina_atual["valor"]]
        for idx in range(2):
            titulo, lista = lista_frames[idx]
            if idx < len(pag):
                cat = pag[idx]
                titulo.config(text=cat)
                _renderizar_lista(lista, cat)
            else:
                titulo.config(text="")
                for w in lista.winfo_children():
                    w.destroy()

        pagina_label.config(text=f"Página {pagina_atual['valor']+1} / {total_paginas}")

    # ── adicionar item ────────────────────────────────────────────────────────

    def adicionar(cat, nome, data, qtd_var=None):
        try:
            qtd = int(qtd_var.get()) if qtd_var else 1
            item = D.reconstruct_item_from_data(data)
            personagem.inventario.gerenciar_item(item_objeto=item, quantidade=qtd, operacao="adicionar")
            if on_finish:
                on_finish()
        except Exception:
            import traceback; traceback.print_exc()

    # ── navegação ─────────────────────────────────────────────────────────────

    def proxima():
        if pagina_atual["valor"] + 1 < total_paginas:
            pagina_atual["valor"] += 1
            atualizar_listas()

    def anterior():
        if pagina_atual["valor"] > 0:
            pagina_atual["valor"] -= 1
            atualizar_listas()

    tk.Button(nav_frame, text="<< Anterior", command=anterior, bg="#0e3386", fg="white").pack(side="left", padx=10)
    pagina_label = tk.Label(nav_frame, text="", bg="#1a0869", fg="white", font=("Arial", 12))
    pagina_label.pack(side="left", padx=10)
    tk.Button(nav_frame, text="Próxima >>", command=proxima, bg="#0e3386", fg="white").pack(side="left", padx=10)

    atualizar_listas()

    tk.Button(popup, text="Fechar", bg="#a00c0c", fg="white", font=("Arial", 12), command=popup.destroy).pack(pady=8)
# adicionar item #

def abrir_popup_loot(master, personagem, D, on_finish=None):
    """
    Popup de Loot — aleatoriza itens de tabelas e adiciona ao inventário.

    Modos disponíveis:
      1. Item único aleatório de uma tabela
      2. Item aleatório com quantidade fixa X
      3. Item aleatório com quantidade entre MIN e MAX
      4. Múltiplos itens aleatórios (com quantidade fixa ou aleatória)
    """
    if not personagem:
        return

    # ── Paleta ────────────────────────────────────────────────────────────────
    BG      = "#130f26"
    BG2     = "#1a0869"
    BG3     = "#220866"
    BG_CARD = "#0d0824"
    FG      = "white"
    FG_DIM  = "#888899"
    ACC     = "#7c5cfc"
    GRN     = "#1f7a1f"
    RED     = "#7a1f1f"
    ENT     = "#0b0926"
    GOLD    = "#ffd700"

    # ── Janela ────────────────────────────────────────────────────────────────
    popup = tk.Toplevel(master)
    popup.title(f"💰 Loot — {personagem.nome}")
    popup.configure(bg=BG)
    popup.geometry("820x680")
    popup.resizable(True, True)
    popup.minsize(700, 560)

    tabelas = {
        "Armas de Fogo":       "Rangeds",
        "Armas Corpo a Corpo": "Melees",
        "Proteções":           "Protecoes",
        "Melhorias":           "Melhorias",
        "Munições":            "Municoes",
        "Itens":               "Itens",
        "Consumíveis":         "Consumiveis",
        "Equipamentos":        "Equipamentos",
    }
    nomes_tabelas = list(tabelas.keys())

    # ── HEADER ────────────────────────────────────────────────────────────────
    hdr = tk.Frame(popup, bg="#090720", height=52)
    hdr.pack(fill="x")
    hdr.pack_propagate(False)
    tk.Label(
        hdr, text="💰  LOOT",
        font=("Consolas", 15, "bold"), bg="#090720", fg=GOLD
    ).pack(side="left", padx=18, pady=12)
    tk.Label(
        hdr, text=f"→  {personagem.nome}",
        font=("Arial", 11), bg="#090720", fg=FG_DIM
    ).pack(side="left", padx=4)

    # ── LAYOUT PRINCIPAL ──────────────────────────────────────────────────────
    body = tk.Frame(popup, bg=BG)
    body.pack(fill="both", expand=True, padx=12, pady=8)

    # Coluna esquerda: configuração
    col_cfg = tk.Frame(body, bg=BG, width=380)
    col_cfg.pack(side="left", fill="both", expand=False, padx=(0, 8))
    col_cfg.pack_propagate(False)

    # Coluna direita: resultado / histórico
    col_res = tk.Frame(body, bg=BG2, bd=1, relief="solid")
    col_res.pack(side="left", fill="both", expand=True)

    # ════════════════════════════════════════════════════════════════════════
    # COLUNA ESQUERDA — Configuração
    # ════════════════════════════════════════════════════════════════════════

    def _section(parent, titulo):
        f = tk.Frame(parent, bg="#1a1640", bd=0)
        f.pack(fill="x", pady=(8, 2))
        tk.Label(f, text=titulo, bg="#1a1640", fg="#9988dd",
                 font=("Consolas", 9, "bold"), padx=8, pady=4).pack(anchor="w")
        body_sec = tk.Frame(f, bg=BG3)
        body_sec.pack(fill="x", padx=4, pady=(0, 6))
        return body_sec

    def _row_cfg(parent, label, widget_factory, hint=""):
        r = tk.Frame(parent, bg=BG3); r.pack(fill="x", padx=10, pady=4)
        tk.Label(r, text=label, bg=BG3, fg="#8899cc",
                 font=("Arial", 10), width=20, anchor="w").pack(side="left")
        w = widget_factory(r); w.pack(side="left", fill="x", expand=True, padx=(4, 0))
        if hint:
            tk.Label(r, text=hint, bg=BG3, fg="#556688",
                     font=("Arial", 8, "italic")).pack(side="left", padx=4)
        return w

    def _entry(parent, var, width=8):
        return tk.Entry(parent, textvariable=var, width=width,
                        bg=ENT, fg=FG, insertbackground=FG,
                        relief="flat", highlightthickness=1,
                        highlightbackground="#2a1f6a", highlightcolor=ACC,
                        font=("Arial", 10), justify="center")

    # ── Seção 1: Tabela ──────────────────────────────────────────────────────
    s_tab = _section(col_cfg, "  TABELA DE ORIGEM")

    tabela_var = tk.StringVar(value=nomes_tabelas[0])
    combo_tab = _row_cfg(
        s_tab, "Tabela:",
        lambda p: ttk.Combobox(p, textvariable=tabela_var,
                               state="readonly", values=nomes_tabelas, width=22)
    )

    # Prévia dos itens da tabela selecionada
    lbl_preview = tk.Label(s_tab, text="", bg=BG3, fg=FG_DIM,
                           font=("Arial", 8, "italic"), anchor="w", padx=14)
    lbl_preview.pack(fill="x")

    def _atualizar_preview(*_):
        chave = tabelas.get(tabela_var.get(), "")
        try:
            dados = D.carregar_tabela_especifica(chave)
            n = len(dados)
            amostra = list(dados.keys())[:4]
            texto = f"{n} item(ns) disponível(is)  •  ex: {', '.join(amostra)}"
            if n > 4:
                texto += f"  +{n-4} mais…"
            lbl_preview.config(text=texto)
        except Exception:
            lbl_preview.config(text="(tabela indisponível)")

    combo_tab.bind("<<ComboboxSelected>>", _atualizar_preview)
    _atualizar_preview()

    # ── Seção 2: Modo de quantidade ──────────────────────────────────────────
    s_qtd = _section(col_cfg, "  QUANTIDADE DO ITEM")

    modo_qtd_var = tk.StringVar(value="unico")

    def _radio(parent, texto, valor, var):
        r = tk.Frame(parent, bg=BG3); r.pack(fill="x", padx=10, pady=2)
        tk.Radiobutton(
            r, text=texto, variable=var, value=valor,
            bg=BG3, fg=FG, selectcolor="#24195e",
            activebackground=BG3, activeforeground=FG,
            indicatoron=1, font=("Arial", 10)
        ).pack(side="left")
        return r

    _radio(s_qtd, "Item único (quantidade 1)", "unico", modo_qtd_var)
    r_fixo = _radio(s_qtd, "Quantidade fixa:", "fixo", modo_qtd_var)
    var_qtd_fixa = tk.IntVar(value=5)
    _entry(r_fixo, var_qtd_fixa, 6).pack(side="left", padx=8)

    r_range = _radio(s_qtd, "Quantidade aleatória:", "range", modo_qtd_var)
    var_qtd_min = tk.IntVar(value=1)
    var_qtd_max = tk.IntVar(value=10)
    tk.Label(r_range, text="mín", bg=BG3, fg=FG_DIM,
             font=("Arial", 9)).pack(side="left", padx=(8, 2))
    _entry(r_range, var_qtd_min, 5).pack(side="left")
    tk.Label(r_range, text="máx", bg=BG3, fg=FG_DIM,
             font=("Arial", 9)).pack(side="left", padx=(6, 2))
    _entry(r_range, var_qtd_max, 5).pack(side="left")

    # ── Seção 3: Múltiplos itens ─────────────────────────────────────────────
    s_mult = _section(col_cfg, "  MÚLTIPLOS ITENS DIFERENTES")

    mult_var = tk.BooleanVar(value=False)
    r_mult = tk.Frame(s_mult, bg=BG3); r_mult.pack(fill="x", padx=10, pady=4)
    tk.Checkbutton(
        r_mult, text="Sortear vários itens distintos",
        variable=mult_var,
        bg=BG3, fg=FG, selectcolor="#24195e",
        activebackground=BG3, activeforeground=FG,
        font=("Arial", 10)
    ).pack(side="left")

    var_n_itens = tk.IntVar(value=3)
    r_n = tk.Frame(s_mult, bg=BG3); r_n.pack(fill="x", padx=10, pady=4)
    tk.Label(r_n, text="Quantidade de itens distintos:",
             bg=BG3, fg="#8899cc", font=("Arial", 10)).pack(side="left")
    _entry(r_n, var_n_itens, 5).pack(side="left", padx=8)
    tk.Label(r_n, text="(cada um pode ter qtd. própria acima)",
             bg=BG3, fg=FG_DIM, font=("Arial", 8, "italic")).pack(side="left")

    # ── Seção 4: Repetição permitida ─────────────────────────────────────────
    s_rep = _section(col_cfg, "  OPÇÕES EXTRAS")
    repeticao_var = tk.BooleanVar(value=True)
    tk.Checkbutton(
        s_rep, text="Permitir repetir o mesmo item (em sorteios múltiplos)",
        variable=repeticao_var,
        bg=BG3, fg=FG, selectcolor="#24195e",
        activebackground=BG3, activeforeground=FG,
        font=("Arial", 9)
    ).pack(anchor="w", padx=10, pady=4)

    adicionar_auto_var = tk.BooleanVar(value=True)
    tk.Checkbutton(
        s_rep, text="Adicionar automaticamente ao inventário",
        variable=adicionar_auto_var,
        bg=BG3, fg=FG, selectcolor="#24195e",
        activebackground=BG3, activeforeground=FG,
        font=("Arial", 9)
    ).pack(anchor="w", padx=10, pady=2)

    # ════════════════════════════════════════════════════════════════════════
    # COLUNA DIREITA — Resultado
    # ════════════════════════════════════════════════════════════════════════
    res_hdr = tk.Frame(col_res, bg="#0d0824")
    res_hdr.pack(fill="x")
    tk.Label(res_hdr, text="🎲 Resultado do Sorteio",
             bg="#0d0824", fg=GOLD, font=("Arial", 11, "bold")).pack(
                 side="left", padx=10, pady=8)

    lbl_contagem = tk.Label(res_hdr, text="", bg="#0d0824", fg=FG_DIM,
                            font=("Arial", 9))
    lbl_contagem.pack(side="right", padx=10)

    # Canvas scrollável para os itens sorteados
    res_outer = tk.Frame(col_res, bg=BG2)
    res_outer.pack(fill="both", expand=True)
    res_canvas = tk.Canvas(res_outer, bg=BG2, highlightthickness=0)
    res_sb = tk.Scrollbar(res_outer, orient="vertical", command=res_canvas.yview)
    res_canvas.configure(yscrollcommand=res_sb.set)
    res_sb.pack(side="right", fill="y")
    res_canvas.pack(side="left", fill="both", expand=True)
    res_inner = tk.Frame(res_canvas, bg=BG2)
    res_win = res_canvas.create_window((0, 0), window=res_inner, anchor="nw")
    res_inner.bind("<Configure>",
                   lambda e: res_canvas.configure(scrollregion=res_canvas.bbox("all")))
    res_canvas.bind("<Configure>",
                    lambda e: res_canvas.itemconfig(res_win, width=e.width))
    res_canvas.bind("<Enter>",
                    lambda e: res_canvas.bind_all(
                        "<MouseWheel>",
                        lambda ev: res_canvas.yview_scroll(int(ev.delta / -90), "units")))
    res_canvas.bind("<Leave>",
                    lambda e: res_canvas.unbind_all("<MouseWheel>"))

    # Estado: lista de (nome_item, objeto_item, quantidade)
    resultado_atual: list[dict] = []

    def _limpar_resultado():
        resultado_atual.clear()
        for w in res_inner.winfo_children():
            w.destroy()
        lbl_contagem.config(text="")

    def _adicionar_linha_resultado(nome, obj, qtd):
        resultado_atual.append({"nome": nome, "obj": obj, "qtd": qtd})
        idx = len(resultado_atual) - 1

        bg_ln = "#1a0f3a" if idx % 2 == 0 else "#220d52"
        row = tk.Frame(res_inner, bg=bg_ln, bd=1, relief="solid")
        row.pack(fill="x", padx=4, pady=2)

        # Ícone de tipo
        tipo_icone = "📦"
        nm = nome.lower()
        if any(k in nm for k in ("pistola","rifle","espingarda","smg","sniper","lmg","shotgun")):
            tipo_icone = "🔫"
        elif any(k in nm for k in ("faca","espada","machado","lança","marreta","bastão","porrete")):
            tipo_icone = "⚔"
        elif any(k in nm for k in ("colete","elmo","capacete","armadura","escudo")):
            tipo_icone = "🛡"
        elif any(k in nm for k in ("bala","munição","cartucho","projétil","9mm","7.62",".308",".45","5.56")):
            tipo_icone = "🔸"
        elif any(k in nm for k in ("poção","bandagem","kit","seringa","remédio")):
            tipo_icone = "🧪"

        # Quantidade (editável)
        var_qtd_item = tk.IntVar(value=qtd)
        resultado_atual[idx]["var_qtd"] = var_qtd_item

        tk.Label(row, text=tipo_icone, bg=bg_ln, fg=FG,
                 font=("Arial", 10)).pack(side="left", padx=(6, 2))
        tk.Label(row, text=nome, bg=bg_ln, fg=FG,
                 font=("Arial", 10, "bold"), anchor="w").pack(
                     side="left", fill="x", expand=True, padx=4, pady=6)
        tk.Label(row, text="×", bg=bg_ln, fg=FG_DIM,
                 font=("Arial", 9)).pack(side="left")
        entry_qtd = tk.Entry(row, textvariable=var_qtd_item, width=5,
                              bg=ENT, fg=GOLD, insertbackground=FG,
                              relief="flat", font=("Arial", 10), justify="center")
        entry_qtd.pack(side="left", padx=(2, 6))

        # Botão remover desta linha
        def _remover(i=idx):
            resultado_atual[i]["removido"] = True
            row.destroy()
            _atualizar_contagem()

        tk.Button(row, text="✕", command=_remover,
                  bg=bg_ln, fg="#cc4444",
                  font=("Arial", 9), relief="flat", cursor="hand2",
                  activebackground="#2a0a0a").pack(side="left", padx=4)

    def _atualizar_contagem():
        vivos = [r for r in resultado_atual if not r.get("removido")]
        total_qtd = sum(r["var_qtd"].get() if "var_qtd" in r else r["qtd"]
                        for r in vivos)
        lbl_contagem.config(
            text=f"{len(vivos)} item(ns) sorteado(s)  •  {total_qtd} unidade(s) total"
        )

    # ────────────────────────────────────────────────────────────────────────
    # Lógica de sorteio
    # ────────────────────────────────────────────────────────────────────────
    def _calcular_quantidade():
        modo = modo_qtd_var.get()
        if modo == "unico":
            return 1
        elif modo == "fixo":
            return max(1, var_qtd_fixa.get())
        else:  # range
            mn = max(1, var_qtd_min.get())
            mx = max(mn, var_qtd_max.get())
            return random.randint(mn, mx)

    def _sortear():
        chave_tab = tabelas.get(tabela_var.get(), "")
        try:
            dados = D.carregar_tabela_especifica(chave_tab)
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Não foi possível carregar a tabela:\n{e}",
                                    parent=popup)
            return

        if not dados:
            tk.messagebox.showwarning("Tabela vazia",
                                      "A tabela selecionada não possui itens.",
                                      parent=popup)
            return

        nomes_disponiveis = list(dados.keys())
        _limpar_resultado()

        if mult_var.get():
            # ── Múltiplos itens distintos ──────────────────────────────────
            n = max(1, var_n_itens.get())
            if not repeticao_var.get():
                n = min(n, len(nomes_disponiveis))
                sorteados = random.sample(nomes_disponiveis, n)
            else:
                sorteados = [random.choice(nomes_disponiveis) for _ in range(n)]

            for nome_item in sorteados:
                qtd = _calcular_quantidade()
                obj_data = dados[nome_item]
                _adicionar_linha_resultado(nome_item, obj_data, qtd)
        else:
            # ── Item único ────────────────────────────────────────────────
            nome_item = random.choice(nomes_disponiveis)
            qtd = _calcular_quantidade()
            obj_data = dados[nome_item]
            _adicionar_linha_resultado(nome_item, obj_data, qtd)

        _atualizar_contagem()

    # ────────────────────────────────────────────────────────────────────────
    # Confirmar: adicionar ao inventário
    # ────────────────────────────────────────────────────────────────────────
    def _confirmar():
        vivos = [r for r in resultado_atual if not r.get("removido")]
        if not vivos:
            tk.messagebox.showwarning("Sem itens",
                                      "Nenhum item para adicionar.\nSorteie primeiro!",
                                      parent=popup)
            return

        adicionados = []
        erros = []
        for entrada in vivos:
            try:
                qtd = entrada["var_qtd"].get() if "var_qtd" in entrada else entrada["qtd"]
                qtd = max(1, qtd)
                item_obj = D.reconstruct_item_from_data(entrada["obj"])
                personagem.inventario.gerenciar_item(
                    item_objeto=item_obj, quantidade=qtd, operacao="adicionar"
                )
                adicionados.append(f"{entrada['nome']} ×{qtd}")
            except Exception as e:
                erros.append(f"{entrada['nome']}: {e}")

        if erros:
            tk.messagebox.showerror(
                "Erros ao adicionar",
                "Alguns itens falharam:\n" + "\n".join(erros),
                parent=popup
            )

        if adicionados:
            _limpar_resultado()
            if on_finish:
                on_finish()
            tk.messagebox.showinfo(
                "✅ Loot adicionado!",
                f"Adicionados ao inventário de {personagem.nome}:\n\n"
                + "\n".join(f"  • {a}" for a in adicionados),
                parent=popup
            )

    def _sortear_e_confirmar():
        """Sorteio rápido: sorteia e já adiciona ao inventário sem confirmação manual."""
        chave_tab = tabelas.get(tabela_var.get(), "")
        try:
            dados = D.carregar_tabela_especifica(chave_tab)
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Tabela indisponível:\n{e}", parent=popup)
            return

        if not dados:
            return

        nomes_disponiveis = list(dados.keys())
        sorteios = []

        if mult_var.get():
            n = max(1, var_n_itens.get())
            if not repeticao_var.get():
                n = min(n, len(nomes_disponiveis))
                sorteados = random.sample(nomes_disponiveis, n)
            else:
                sorteados = [random.choice(nomes_disponiveis) for _ in range(n)]
            for nome_item in sorteados:
                sorteios.append((nome_item, dados[nome_item], _calcular_quantidade()))
        else:
            nome_item = random.choice(nomes_disponiveis)
            sorteios.append((nome_item, dados[nome_item], _calcular_quantidade()))

        adicionados = []
        for nome_item, obj_data, qtd in sorteios:
            try:
                item_obj = D.reconstruct_item_from_data(obj_data)
                personagem.inventario.gerenciar_item(
                    item_objeto=item_obj, quantidade=qtd, operacao="adicionar"
                )
                adicionados.append(f"{nome_item} ×{qtd}")
            except Exception as e:
                print(f"Erro ao adicionar {nome_item}: {e}")

        if adicionados and on_finish:
            on_finish()

        # Mostra resultado brevemente na coluna direita
        _limpar_resultado()
        for nome_item, obj_data, qtd in sorteios:
            _adicionar_linha_resultado(nome_item, obj_data, qtd)
        _atualizar_contagem()

        if adicionados:
            tk.messagebox.showinfo(
                "✅ Loot adicionado!",
                f"Adicionados ao inventário de {personagem.nome}:\n\n"
                + "\n".join(f"  • {a}" for a in adicionados),
                parent=popup
            )

    # ════════════════════════════════════════════════════════════════════════
    # BARRA DE BOTÕES
    # ════════════════════════════════════════════════════════════════════════
    bbar = tk.Frame(popup, bg="#090720", height=56)
    bbar.pack(fill="x", side="bottom")
    bbar.pack_propagate(False)

    tk.Button(
        bbar, text="  ✕  Fechar  ",
        command=popup.destroy,
        bg=RED, fg=FG, relief="flat",
        font=("Arial", 10, "bold"), cursor="hand2", pady=6
    ).pack(side="right", padx=10, pady=8)

    tk.Button(
        bbar, text="  ✅  Adicionar ao Inventário  ",
        command=_confirmar,
        bg=GRN, fg=FG, relief="flat",
        font=("Arial", 10, "bold"), cursor="hand2", pady=6
    ).pack(side="right", padx=(0, 6), pady=8)

    tk.Button(
        bbar, text="  ⚡  Sortear e Adicionar  ",
        command=_sortear_e_confirmar,
        bg="#4a2080", fg=FG, relief="flat",
        font=("Arial", 10, "bold"), cursor="hand2", pady=6
    ).pack(side="right", padx=(0, 6), pady=8)

    tk.Button(
        bbar, text="  🎲  Sortear  ",
        command=_sortear,
        bg="#0a3d5c", fg=FG, relief="flat",
        font=("Arial", 10, "bold"), cursor="hand2", pady=6
    ).pack(side="left", padx=10, pady=8)

    tk.Button(
        bbar, text="  🗑  Limpar  ",
        command=_limpar_resultado,
        bg="#2a1a00", fg=FG, relief="flat",
        font=("Arial", 10, "bold"), cursor="hand2", pady=6
    ).pack(side="left", padx=(0, 6), pady=8)

    popup.transient(master)
    popup.grab_set()

def aplicar_efeitos_item(efeitos: list, alvo, mult_chance: float = 1.0):
    """
    Aplica efeitos de um item (Melee, Ranged/Municao, Consumivel) ao alvo.
    Cada efeito deve ter: {"nome": str, "duracao": int, "chance": int (0-100)}

    O nome é buscado no banco de D.carregar_buffs_debuffs() para obter
    a mecânica completa (efeito de tags, tipo, descricao).
    Se não encontrado no banco, aplica como marcador de status vazio.

    mult_chance: multiplicador de chance (usado para falloff em área, 0.0-1.0).
    Retorna lista de nomes dos efeitos aplicados.
    """
    if not efeitos:
        return []

    banco = D.carregar_buffs_debuffs()
    aplicados = []

    for ef in efeitos:
        if not isinstance(ef, dict):
            continue

        nome    = ef.get("nome", "")
        chance  = ef.get("chance", 100)
        duracao = ef.get("duracao", 1)

        if not nome:
            continue

        chance_final = max(1, min(100, int(chance * mult_chance)))
        roll = random.randint(1, 100)
        if roll > chance_final:
            continue

        dados_banco = banco.get(nome, {})
        bb = CB.BuffDebuff(
            nome     = nome,
            duracao  = duracao,
            efeito   = dados_banco.get("efeito", []),
            descricao= dados_banco.get("descricao", ""),
            tipo     = dados_banco.get("tipo", "debuff"),
        )
        alvo.buffs_debuffs.adicionar_efeito_objeto(bb)
        aplicados.append(nome)

    return aplicados

def equipar_item(self, item, nome_slot=None, forcar=False):
    # 🔹 Armas
    if self._eh_arma_melee(item) or self._eh_arma_ranged(item):

        usa_duas = getattr(item, "requer_duas_maos", False)

        # =========================================================
        # 🔥 CASO 1 — Slot NÃO informado → modo automático
        # =========================================================
        if nome_slot is None:

            maos_livres = [s for s in self.slots.values() if s.tipo == "mao" and s.item is None]

            # Arma 2 mãos
            if usa_duas and not forcar:
                if len(maos_livres) < 2:
                    return False

                if not self._remover_do_inventario_generico(item):
                    return False

                for s in maos_livres[:2]:
                    s.item = item
                return True

            # Arma 1 mão
            if maos_livres:
                if not self._remover_do_inventario_generico(item):
                    return False
                maos_livres[0].item = item
                return True

            return False

        # =========================================================
        # 🔥 CASO 2 — Slot informado manualmente
        # =========================================================
        slot = self.slots.get(nome_slot)
        if not slot or slot.tipo != "mao":
            return False

        if usa_duas and not forcar:
            outro_nome = "mao_esquerda" if nome_slot == "mao_direita" else "mao_direita"
            outro_slot = self.slots.get(outro_nome)

            if slot.item or (outro_slot and outro_slot.item):
                return False

            if not self._remover_do_inventario_generico(item):
                return False

            slot.item = item
            if outro_slot:
                outro_slot.item = item
            return True

        # Uma mão ou forçado
        if slot.item and not forcar:
            return False

        if not self._remover_do_inventario_generico(item):
            return False

        slot.item = item
        return True

    # 🔹 Proteções continuam iguais
    if self._eh_protecao(item):
        return self._equipar_protecao(item)

    return False

# rolagem #
ATRIBUTOS_SIMPLES = [
    "iniciativa", "sorte",
    "força", "agilidade", "vigor",
    "inteligencia", "presença", "tática", "poder",
]
ATRIB_CAMPO = {
    "força":       "Forca",
    "agilidade":   "Agilidade",
    "vigor":       "Vigor",
    "inteligencia":"Inteligencia",
    "presença":    "Presenca",
    "tática":      "Tatica",
    "poder":       "Poder",
}
GRUPO_PARA_ATRIBS = {
    "físico":  ["força", "agilidade", "vigor"],
    "mental":  ["inteligencia", "poder", "tática"],
    "vocal":   ["presença"],
}
BG      = "#1a1a2e"
BG2     = "#0d0b1e"
BG_CARD = "#1a0869"
FG      = "white"
FG_DIM  = "#aaaaaa"
ENT     = "#0b0926"
ACC     = "#7c5cfc"
GRN     = "#1f7a1f"
RED     = "#7a1f1f"
CYAN    = "#00bcd4"
YELLOW  = "#f1c40f"
def _rolar_formula(formula: str):
    """
    Interpreta fórmulas como '2d20 + 5', '1d100 + 1d10 - 3', '1d10 x 10'.
    Retorna (total: int, detalhes: str).
    """
    formula = formula.strip().lower()
    if not formula:
        return 0, "fórmula vazia"

    # ── multiplicador: "1d10 x 10" ou "1d10 * 10" ──
    mult_match = re.match(r'^(.+?)\s*[x\*]\s*(\d+)$', formula)
    if mult_match:
        base_formula = mult_match.group(1).strip()
        multiplicador = int(mult_match.group(2))
        base_total, base_det = _rolar_formula(base_formula)
        total = base_total * multiplicador
        return total, f"({base_det}) × {multiplicador} = {total}"

    total = 0
    detalhes_partes = []

    # separa em tokens com sinal: ["+2d6", "-3", "+1d100", "+5"]
    tokens = re.findall(r'[+-]?\s*\d*[d]?\d+', formula.replace(" ", ""))

    for token in tokens:
        token = token.replace(" ", "")
        if not token:
            continue

        # detecta sinal
        if token.startswith("-"):
            sinal = -1
            token = token[1:]
        elif token.startswith("+"):
            sinal = 1
            token = token[1:]
        else:
            sinal = 1

        if "d" in token:
            partes = token.split("d")
            qtd  = int(partes[0]) if partes[0] else 1
            face = int(partes[1])
            qtd  = max(1, qtd)
            rolagens = [random.randint(1, face) for _ in range(qtd)]
            soma = sum(rolagens)
            total += sinal * soma
            sinal_txt = "+" if sinal == 1 else "-"
            detalhes_partes.append(
                f"{sinal_txt}{qtd}d{face}{rolagens}={sinal*soma}"
            )
        else:
            val = int(token)
            total += sinal * val
            sinal_txt = "+" if sinal == 1 else "-"
            detalhes_partes.append(f"{sinal_txt}{val}")

    detalhes = "  ".join(detalhes_partes)
    return total, detalhes

def _obter_mod_teste(personagem, teste_nome: str) -> int:
    """Soma mod_testes + bonus_testes para o nome fornecido (case-insensitive)."""
    nome = teste_nome.lower()
    mod   = getattr(personagem, "mod_testes",   {}).get(nome, 0)
    bonus = getattr(personagem, "bonus_testes",  {}).get(nome, 0)
    return mod + bonus

def _obter_mod_atributo(personagem, atrib_nome: str) -> int:
    """Retorna bonus_atributos para o atributo (case-insensitive)."""
    nome = atrib_nome.lower()
    return getattr(personagem, "bonus_atributos", {}).get(nome, 0)

def _valor_atributo(personagem, atrib_nome: str) -> int:
    """Retorna o valor base do atributo no personagem."""
    campo = ATRIB_CAMPO.get(atrib_nome.lower())
    if campo:
        return getattr(personagem, campo, 0)
    return 0

def _melhor_de_n(n: int, faces: int = 20):
    """Rola n d{faces} e retorna (melhor, lista_completa)."""
    n = max(1, n)
    rolls = [random.randint(1, faces) for _ in range(n)]
    return max(rolls), rolls

def _dados_por_atributo(valor_atrib: int) -> int:
    """Converte valor do atributo em número de d20 a rolar."""
    return max(1, valor_atrib // 2)

def _coletar_mods_para_teste(personagem, atrib_nome: str):
    """
    Retorna lista de (fonte, valor, tipo) relevantes para o teste do atributo.
    tipo ∈ {'mod_teste', 'bonus_atrib', 'efeito', 'prof'}
    """
    mods = []
    atrib_l = atrib_nome.lower()

    # 1. mod_testes direto
    v = getattr(personagem, "mod_testes", {}).get(atrib_l, 0)
    if v: mods.append(("Modificador de Teste", v, "mod_teste"))

    # 2. bonus_testes direto
    v = getattr(personagem, "bonus_testes", {}).get(atrib_l, 0)
    if v: mods.append(("Bônus de Teste", v, "bonus_teste"))

    # 3. bonus_atributos
    v = getattr(personagem, "bonus_atributos", {}).get(atrib_l, 0)
    if v: mods.append(("Bônus de Atributo", v, "bonus_atrib"))

    # 4. Buffs/debuffs ativos
    gbb = getattr(personagem, "buffs_debuffs", None)
    if gbb:
        for efeito in gbb.listar_efeitos():
            ef_list = efeito.efeito if isinstance(efeito.efeito, list) else [efeito.efeito]
            for entrada in ef_list:
                if not isinstance(entrada, dict): continue
                # suporta formato novo {"tags": [...]} e antigo {"atributo": "..."}
                tags = entrada.get("tags") or []
                if not tags and "atributo" in entrada:
                    tags = [entrada["atributo"]]
                valor = entrada.get("valor", 0)
                for tag in tags:
                    tag_l = tag.lower()
                    if tag_l == atrib_l:
                        mods.append((f"Efeito: {efeito.nome}", valor, "efeito"))
                    elif tag_l == "qualquer teste" and atrib_l not in ("sorte", "iniciativa"):
                        mods.append((f"Efeito (qualquer): {efeito.nome}", valor, "efeito"))

    # 5. Habilidades passivas
    hab_g = getattr(personagem, "habilidades", None)
    if hab_g:
        for h in hab_g.listar_habilidades():
            if h.tipo != "passivo": continue
            tags = h.tags if isinstance(h.tags, list) else [h.tags]
            vals = h.valor if isinstance(h.valor, list) else [h.valor] * len(tags)
            for t, v in zip(tags, vals):
                if t.lower() == atrib_l and v:
                    mods.append((f"Habilidade: {h.nome}", v, "efeito"))

    # 6. Poderes passivos
    pod_g = getattr(personagem, "poderes", None)
    if pod_g:
        for p in pod_g.listar_poderes():
            if p.tipo != "passivo": continue
            tags = p.tags if isinstance(p.tags, list) else [p.tags]
            vals = p.valor if isinstance(p.valor, list) else [p.valor] * len(tags)
            for t, v in zip(tags, vals):
                if t.lower() == atrib_l and v:
                    mods.append((f"Poder: {p.nome}", v, "efeito"))

    return mods

def _coletar_profs_para_atributo(personagem, atrib_nome: str):
    """
    Retorna lista de proficiências cujo atributo-pai corresponde ao atributo dado.
    Cada item: (Proficiencia_obj,)
    """
    atrib_l = atrib_nome.lower()
    # mapeamento display → campo Personagem → label para comparação
    MAP = {
        "força":       "Força",
        "agilidade":   "Agilidade",
        "vigor":       "Vigor",
        "inteligencia":"Inteligência",
        "presença":    "Presença",
        "tática":      "Tática",
        "poder":       "Poder",
    }
    nome_display = MAP.get(atrib_l)

    prof_g = getattr(personagem, "proficiencias", None)
    if not prof_g: return []

    resultado = []
    for prof in prof_g.proficiencias.values():
        if prof.atributo == nome_display:
            resultado.append(prof)
    return resultado

def abrir_popup_rolagem_personagem(parent_widget, personagem, log_callback=None):
    """
    Abre popup de rolagem para um personagem específico.
    log_callback(mensagem, cor, detalhes=dict) — opcional (para tela de combate).
    """
    popup = tk.Toplevel(parent_widget)
    popup.title(f"🎲 Rolagem — {personagem.nome}")
    popup.configure(bg=BG)
    popup.geometry("650x650")
    popup.resizable(True, True)
    popup.transient(parent_widget)
    popup.grab_set()

    _construir_interface_rolagem(popup, [personagem], log_callback, multi=False)

def abrir_popup_rolagem_grupo(parent_widget, lista_personagens, log_callback=None):
    """
    Abre popup de rolagem para múltiplos personagens (tela de combate).
    """
    if not lista_personagens:
        return

    popup = tk.Toplevel(parent_widget)
    popup.title("🎲 Rolagem em Grupo")
    popup.configure(bg=BG)
    popup.geometry("700x650")
    popup.resizable(True, True)
    popup.transient(parent_widget)
    popup.grab_set()

    _construir_interface_rolagem(popup, lista_personagens, log_callback, multi=True)

def _construir_interface_rolagem(popup, personagens, log_callback, multi: bool):
    BG_H = "#090720"

    # ── HEADER ───────────────────────────────────────────────────────────────
    hdr = tk.Frame(popup, bg=BG_H, height=52)
    hdr.pack(fill="x")
    hdr.pack_propagate(False)
    titulo = "Rolagem em Grupo" if multi else f"Rolagem — {personagens[0].nome}"
    tk.Label(hdr, text=f"🎲 {titulo}",font=("Consolas", 13, "bold"), bg=BG_H, fg="#a88fff").pack(side="left", padx=16, pady=12)

    # ── SCROLL PRINCIPAL ──────────────────────────────────────────────────────
    outer = tk.Frame(popup, bg=BG)
    outer.pack(fill="both", expand=True)
    cv = tk.Canvas(outer, bg=BG, highlightthickness=0)
    sb = tk.Scrollbar(outer, orient="vertical", command=cv.yview)
    inner = tk.Frame(cv, bg=BG)
    inner.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
    cv.create_window((0, 0), window=inner, anchor="nw")
    cv.configure(yscrollcommand=sb.set)
    cv.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")
    cv.bind("<Enter>",  lambda e: cv.bind_all("<MouseWheel>",
            lambda ev: cv.yview_scroll(int(ev.delta / -90), "units")))
    cv.bind("<Leave>",  lambda e: cv.unbind_all("<MouseWheel>"))

    # ── SELEÇÃO DE PERSONAGENS (apenas multi) ─────────────────────────────────
    personagens_sel = list(personagens)  # cópia mutável

    if multi:
        sec_pers = _section(inner, "  PERSONAGENS")
        vars_pers = {}
        for p in personagens:
            var = tk.BooleanVar(value=True)
            vars_pers[p] = var
            tk.Checkbutton(sec_pers, text=p.nome, variable=var,bg="#1a1640", fg=FG, selectcolor="#1a1640",activebackground="#ffffff", activeforeground=FG,font=("Arial", 10)).pack(anchor="w", padx=12, pady=1)

        def _get_sel():
            return [p for p, v in vars_pers.items() if v.get()]
    else:
        def _get_sel():
            return personagens_sel

    # ── MODO ──────────────────────────────────────────────────────────────────
    sec_modo = _section(inner, "  MODO DE ROLAGEM")
    modo_var = tk.StringVar(value="formula")
    tk.Radiobutton(sec_modo, text="Fórmula livre  (ex: 2d20 + 5)",variable=modo_var, value="formula",bg="#1a1640", fg=FG, selectcolor="#24195e",activebackground="#1a1640", font=("Arial", 10),command=lambda: _toggle_modo()).pack(anchor="w", padx=12, pady=2)
    tk.Radiobutton(sec_modo, text="Teste de Atributo / Proficiência",variable=modo_var, value="atributo",bg="#1a1640", fg=FG, selectcolor="#24195e",activebackground="#1a1640", font=("Arial", 10),command=lambda: _toggle_modo()).pack(anchor="w", padx=12, pady=2)

    # ── FRAME FÓRMULA ─────────────────────────────────────────────────────────
    frame_formula = tk.Frame(inner, bg=BG)

    sec_f = _section(frame_formula, "  FÓRMULA")
    tk.Label(sec_f, text="Digite a fórmula:",bg="#1a1640", fg=FG_DIM, font=("Arial", 9)).pack(anchor="w", padx=12)
    formula_var = tk.StringVar(value="1d20")
    entry_f = tk.Entry(sec_f, textvariable=formula_var, width=32,bg=ENT, fg=FG, insertbackground=FG,font=("Consolas", 13), relief="flat",highlightthickness=1, highlightbackground="#2a1f6a",highlightcolor=ACC)
    entry_f.pack(padx=12, pady=6, fill="x")

    # exemplos clicáveis
    ex_frame = tk.Frame(sec_f, bg="#1a1640")
    ex_frame.pack(fill="x", padx=10, pady=(0, 6))
    tk.Label(ex_frame, text="Exemplos:", bg="#1a1640", fg=FG_DIM,font=("Arial", 8)).pack(side="left")
    for ex in ("1d4", "1d6", "1d8", "1d12", "1d20","1d10 x 10", "1d100"):
        tk.Button(ex_frame, text=ex, bg="#2a1f5e", fg="#ccbbff",font=("Arial", 8), relief="flat", cursor="hand2",command=lambda v=ex: formula_var.set(v)).pack(side="left", padx=3)

    # ── FRAME ATRIBUTO ────────────────────────────────────────────────────────
    frame_atrib = tk.Frame(inner, bg=BG)

    sec_at = _section(frame_atrib, "  ATRIBUTO / TESTE")

    atrib_var = tk.StringVar(value="força")
    tk.Label(sec_at, text="Escolha o teste:", bg="#1a1640", fg=FG_DIM,font=("Arial", 9)).pack(anchor="w", padx=12)
    combo_atrib = ttk.Combobox(sec_at, textvariable=atrib_var,values=ATRIBUTOS_SIMPLES, state="readonly", width=22)
    combo_atrib.pack(padx=12, pady=4, anchor="w")

    # informação de mecânica
    lbl_mecanica = tk.Label(sec_at, text="", bg="#1a1640", fg=CYAN,font=("Arial", 8, "italic"), wraplength=500, justify="left")
    lbl_mecanica.pack(anchor="w", padx=12)

    # ── Proficiência ──────────────────────────────────────────────────────────
    sec_prof = _section(frame_atrib, "  PROFICIÊNCIA (opcional)")

    usar_prof_var = tk.BooleanVar(value=False)
    prof_frame_inner = tk.Frame(sec_prof, bg="#1a1640")
    prof_frame_inner.pack(fill="x", padx=10)

    tk.Checkbutton(prof_frame_inner, text="Usar pontos de proficiência",
                   variable=usar_prof_var, bg="#1a1640", fg=FG,
                   selectcolor="#24195e", activebackground="#1a1640",
                   font=("Arial", 10),
                   command=lambda: _atualizar_profs()).pack(anchor="w")

    combo_prof_var = tk.StringVar()
    combo_prof     = ttk.Combobox(prof_frame_inner, textvariable=combo_prof_var,
                                  state="readonly", width=30)
    combo_prof.pack(anchor="w", pady=2)
    combo_prof.pack_forget()

    lbl_prof_val = tk.Label(prof_frame_inner, text="", bg="#1a1640",
                            fg="#7ec8e3", font=("Arial", 9, "italic"))
    lbl_prof_val.pack(anchor="w")
    lbl_prof_val.pack_forget()

    # ── Modificadores Ativos ──────────────────────────────────────────────────
    sec_mods = _section(frame_atrib, "  MODIFICADORES ATIVOS (do personagem)")

    lbl_mods_info = tk.Label(sec_mods, text="Selecione o personagem e o atributo acima para ver os mods.",
                             bg="#1a1640", fg=FG_DIM, font=("Arial", 8, "italic"), wraplength=520)
    lbl_mods_info.pack(anchor="w", padx=12, pady=4)

    frame_mods_lista = tk.Frame(sec_mods, bg="#1a1640")
    frame_mods_lista.pack(fill="x", padx=10, pady=4)

    # (os checkboxes de mods serão gerados dinamicamente)
    mods_vars: list = []  # lista de (descrição, valor, BooleanVar)

    # ── Buff / Debuff manual ──────────────────────────────────────────────────
    sec_bd = _section(frame_atrib, "  BUFF / DEBUFF MANUAL")
    row_bd = tk.Frame(sec_bd, bg="#1a1640"); row_bd.pack(fill="x", padx=10, pady=4)
    tk.Label(row_bd, text="Buff:", bg="#1a1640", fg="#90ee90",
             font=("Arial", 10)).pack(side="left")
    buff_var = tk.IntVar(value=0)
    tk.Entry(row_bd, textvariable=buff_var, width=6, bg=ENT, fg="#90ee90",
             font=("Arial", 10), justify="center").pack(side="left", padx=4)
    tk.Label(row_bd, text="   Debuff:", bg="#1a1640", fg="#ff9999",
             font=("Arial", 10)).pack(side="left")
    debuff_var = tk.IntVar(value=0)
    tk.Entry(row_bd, textvariable=debuff_var, width=6, bg=ENT, fg="#ff9999",
             font=("Arial", 10), justify="center").pack(side="left", padx=4)

    # ─────────────────────────────────────────────────────────────────────────
    # RESULTADO
    # ─────────────────────────────────────────────────────────────────────────
    sec_res = _section(inner, "  RESULTADO")
    frame_resultados = tk.Frame(sec_res, bg="#0d0b1e")
    frame_resultados.pack(fill="x", padx=6, pady=4)

    # ─────────────────────────────────────────────────────────────────────────
    # CALLBACKS INTERNOS
    # ─────────────────────────────────────────────────────────────────────────

    def _toggle_modo():
        modo = modo_var.get()
        if modo == "formula":
            frame_atrib.pack_forget()
            frame_formula.pack(fill="x", after=sec_modo)
        else:
            frame_formula.pack_forget()
            frame_atrib.pack(fill="x", after=sec_modo)
        _limpar_resultados()

    def _atualizar_mecanica(*_):
        nome = atrib_var.get().lower()
        if nome in ("iniciativa", "sorte"):
            lbl_mecanica.config(
                text="▸ 1d20 fixo  (sem escala por atributo)")
        else:
            campo = ATRIB_CAMPO.get(nome)
            val   = getattr(personagens[0], campo, 0) if campo else 0
            n     = _dados_por_atributo(val)
            lbl_mecanica.config(
                text=f"▸ Valor do atributo: {val}  →  {n}×d20, fica com o maior")
        _atualizar_mods_lista()
        _atualizar_profs()

    combo_atrib.bind("<<ComboboxSelected>>", _atualizar_mecanica)

    def _atualizar_profs():
        combo_prof.pack_forget()
        lbl_prof_val.pack_forget()
        if not usar_prof_var.get():
            return

        # usa primeiro personagem como referência
        p = _get_sel()[0] if _get_sel() else (personagens[0] if personagens else None)
        if not p:
            return

        nome = atrib_var.get().lower()
        profs = _coletar_profs_para_atributo(p, nome)
        if not profs:
            lbl_prof_val.config(text="Nenhuma proficiência neste atributo.")
            lbl_prof_val.pack(anchor="w")
            return

        nomes = [f"{pr.nome}  (nível {pr.nivel})" for pr in profs]
        combo_prof["values"] = nomes
        if nomes:
            combo_prof_var.set(nomes[0])
        combo_prof.pack(anchor="w", pady=2)

        def _on_prof(*_):
            idx  = combo_prof["values"].index(combo_prof_var.get())
            prof = profs[idx]
            lbl_prof_val.config(
                text=f"Bônus de proficiência: +{prof.nivel}")
        combo_prof.bind("<<ComboboxSelected>>", _on_prof)
        _on_prof()
        lbl_prof_val.pack(anchor="w")

    def _atualizar_mods_lista():
        for w in frame_mods_lista.winfo_children():
            w.destroy()
        mods_vars.clear()

        nome = atrib_var.get().lower()
        sels = _get_sel()
        p = sels[0] if sels else (personagens[0] if personagens else None)
        if not p:
            return

        mods = _coletar_mods_para_teste(p, nome)

        if not mods:
            tk.Label(frame_mods_lista, text="Nenhum modificador encontrado.",
                     bg="#1a1640", fg=FG_DIM, font=("Arial", 8, "italic")).pack(anchor="w")
            lbl_mods_info.config(text="")
            return

        lbl_mods_info.config(text=f"Modificadores detectados para «{nome}»:")

        total_auto = 0
        for (fonte, valor, tipo) in mods:
            var_m = tk.BooleanVar(value=True)
            total_auto += valor
            sinal = "+" if valor >= 0 else ""
            cor   = "#90ee90" if valor >= 0 else "#ff9999"
            row_m = tk.Frame(frame_mods_lista, bg="#1a1640")
            row_m.pack(fill="x", pady=1)
            tk.Checkbutton(row_m, variable=var_m,
                           bg="#1a1640", selectcolor="#24195e",
                           activebackground="#1a1640").pack(side="left")
            tk.Label(row_m, text=f"{sinal}{valor}",
                     bg="#1a1640", fg=cor,
                     font=("Arial", 10, "bold"), width=5).pack(side="left")
            tk.Label(row_m, text=fonte, bg="#1a1640", fg=FG_DIM,
                     font=("Arial", 9)).pack(side="left", padx=4)
            mods_vars.append((fonte, valor, var_m))

    def _limpar_resultados():
        for w in frame_resultados.winfo_children():
            w.destroy()

    def _exibir_resultado_bloco(personagem, total, detalhes, mods_aplicados,
                                 prof_bonus, buff, debuff):
        """Cria um bloco de resultado para um personagem."""
        cor_total = YELLOW if total >= 15 else (CYAN if total >= 8 else "#ff7777")
        bloco = tk.Frame(frame_resultados, bg="#12103a", bd=1, relief="ridge")
        bloco.pack(fill="x", padx=4, pady=4)
        # nome
        tk.Label(bloco, text=personagem.nome, bg="#12103a", fg="#b79cff",
                 font=("Arial", 10, "bold")).pack(anchor="w", padx=8, pady=(4, 0))
        # total
        tk.Label(bloco, text=f"Total: {total}",
                 bg="#12103a", fg=cor_total,
                 font=("Consolas", 16, "bold")).pack(anchor="w", padx=12)
        # detalhes linha a linha
        tk.Label(bloco, text=detalhes, bg="#12103a", fg=FG_DIM,
                 font=("Arial", 8), wraplength=550, justify="left").pack(
            anchor="w", padx=12, pady=(0, 4))
        if mods_aplicados:
            tk.Label(bloco,
                     text="Mods: " + "  ".join(
                         (f"+{v}" if v >= 0 else str(v)) + f" ({n})"
                         for n, v, _ in mods_aplicados),
                     bg="#12103a", fg="#aaaaee",
                     font=("Arial", 8)).pack(anchor="w", padx=12)
        if prof_bonus:
            tk.Label(bloco, text=f"Proficiência: +{prof_bonus}",
                     bg="#12103a", fg="#7ec8e3",
                     font=("Arial", 8)).pack(anchor="w", padx=12)
        if buff or debuff:
            tk.Label(bloco,
                     text=f"Buff manual: +{buff}   Debuff manual: -{debuff}",
                     bg="#12103a", fg=FG_DIM, font=("Arial", 8)).pack(anchor="w", padx=12)
        tk.Frame(bloco, bg="#2a1f6a", height=1).pack(fill="x", padx=8, pady=4)

    # ─────────────────────────────────────────────────────────────────────────
    # ROLAR
    # ─────────────────────────────────────────────────────────────────────────

    def _rolar():
        _limpar_resultados()
        sels = _get_sel()
        if not sels:
            tk.Label(frame_resultados, text="Selecione ao menos um personagem.",
                     bg="#0d0b1e", fg="red", font=("Arial", 10)).pack()
            return

        modo = modo_var.get()
        log_entradas = []

        for p in sels:
            if modo == "formula":
                total, detalhes = _rolar_formula(formula_var.get())
                _exibir_resultado_bloco(p, total, detalhes, [], 0, 0, 0)
                log_entradas.append({p.nome: f"Total {total}  ({detalhes})"})

            else:  # modo atributo
                nome = atrib_var.get().lower()

                # ── decide quantos dados ──
                if nome in ("iniciativa", "sorte"):
                    melhor, rolls = _melhor_de_n(1, 20)
                    detalhes_base = f"1d20{rolls} = {melhor}"
                else:
                    campo = ATRIB_CAMPO.get(nome)
                    val   = getattr(p, campo, 0) if campo else 0
                    n     = _dados_por_atributo(val)
                    melhor, rolls = _melhor_de_n(n, 20)
                    detalhes_base = f"{n}d20{rolls} → melhor={melhor}  (atrib={val})"

                # ── mods selecionados ──
                mods_ativos = [(s, v, bv) for s, v, bv in mods_vars if bv.get()]
                soma_mods   = sum(v for _, v, _ in mods_ativos)

                # ── proficiência ──
                prof_bonus = 0
                if usar_prof_var.get() and combo_prof["values"]:
                    try:
                        idx  = combo_prof["values"].index(combo_prof_var.get())
                        profs = _coletar_profs_para_atributo(p, nome)
                        if 0 <= idx < len(profs):
                            prof_bonus = profs[idx].nivel
                    except (ValueError, IndexError):
                        pass

                # ── buff / debuff manual ──
                b  = buff_var.get()
                db = debuff_var.get()

                total = melhor + soma_mods + prof_bonus + b - db
                detalhes = detalhes_base
                if soma_mods: detalhes += f"  mods={soma_mods:+d}"
                if prof_bonus: detalhes += f"  prof=+{prof_bonus}"
                if b:  detalhes += f"  buff=+{b}"
                if db: detalhes += f"  debuff=-{db}"

                _exibir_resultado_bloco(p, total, detalhes,
                                        mods_ativos, prof_bonus, b, db)
                log_entradas.append({p.nome: f"[{nome}] Total {total}  ({detalhes})"})

        # ── log de combate ──
        if log_callback:
            atrib_txt = (formula_var.get() if modo == "formula"
                         else atrib_var.get())
            nomes = ", ".join(p.nome for p in sels)
            detalhes_log = {
                entry_k: entry_v
                for d in log_entradas
                for entry_k, entry_v in d.items()
            }
            log_callback(
                f"🎲 Rolagem «{atrib_txt}» — {nomes}",
                CYAN,
                detalhes=detalhes_log
            )

    # ── inicialização ──────────────────────────────────────────────────────────
    _toggle_modo()      # mostra frame fórmula por padrão
    _atualizar_mecanica()

    # ── BARRA DE BOTÕES ───────────────────────────────────────────────────────
    bbar = tk.Frame(popup, bg=BG_H, height=52)
    bbar.pack(fill="x", side="bottom")
    bbar.pack_propagate(False)

    tk.Button(bbar, text="  ✕  Fechar  ",
              command=popup.destroy,
              bg=RED, fg=FG, relief="flat",
              font=("Arial", 10, "bold"), cursor="hand2").pack(
        side="right", padx=10, pady=10)

    tk.Button(bbar, text="  🎲  Rolar  ",
              command=_rolar,
              bg=GRN, fg=FG, relief="flat",
              font=("Arial", 10, "bold"), cursor="hand2").pack(
        side="right", padx=(0, 6), pady=10)

def _section(parent, title):
    f = tk.Frame(parent, bg="#12103a", bd=0)
    f.pack(fill="x", padx=14, pady=(10, 2))
    tk.Label(f, text=title, bg="#12103a", fg="#9988dd",
             font=("Consolas", 9, "bold"), padx=8, pady=4).pack(anchor="w")
    body = tk.Frame(f, bg="#1a1640")
    body.pack(fill="x", padx=4, pady=(0, 6))
    return body
# rolagem #
### Funções universais ###

### TELA PRINCIPAL ###
### TELA PRINCIPAL ###
### TELA PRINCIPAL ###
class MainScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#130f26")

        self.nome_sessao_atual = None

        # Título da tela com tamanho reduzido
        title_frame = tk.Frame(self, bg="#1a0869", relief="raised", bd=3)
        title_frame.place(width=700, height=90, x=450, y=100)
        
        label = tk.Label(title_frame, text="- Skirmish Engine -", 
                        font=("Arial", 32, "bold"), fg="#ffffff", bg="#1a0869")
        label.pack(expand=True)

        # Barra de navegação superior
        nav_frame = tk.Frame(self, bg="#130f26")
        nav_frame.place(x=20, y=10, width=1565, height=85)
        
        tk.Label(self, text="Tela inicial", fg="white", bg="#1a0869", font=("Arial", 20, "bold"), width=20, height=2).place(x=20, y=10, width=350, height=75)
        
        tk.Button(self, text="Seleção", height=2, command=self.TelaDeSelecao, bg="#1a0869", fg="white", font=("Arial", 20)).place(x=385, y=10, width=350, height=75)

        tk.Button(self, text="Combate", height=2, command=self.TelaDeCombate, bg="#1a0869", fg="white", font=("Arial", 20)).place(x=870, y=10, width=350, height=75)

        tk.Button(self, text="Informações", height=2, command=self.TelaDeRegrasEItens, bg="#1a0869", fg="white", font=("Arial", 20)).place(x=1235, y=10, width=350, height=75)
        
        # === SEÇÃO DE GERENCIAMENTO DE SESSÕES (CENTRALIZADA E AUMENTADA) ===
        sessao_frame = tk.Frame(self, bg="#1a0869", relief="raised", bd=3)
        sessao_frame.place(x=300, y=220, width=600, height=550)
        
        # Título da seção com estilo aprimorado
        title_bg = tk.Frame(sessao_frame, bg="#2a1f3d", height=50)
        title_bg.pack(fill="x")
        tk.Label(title_bg, text="🎮 Gerenciamento de Sessões", 
                font=("Arial", 18, "bold"), fg="#ffffff", bg="#2a1f3d").pack(pady=12)
        
        # Container principal
        main_container = tk.Frame(sessao_frame, bg="#1a0869")
        main_container.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Frame para a lista de sessões com canvas e scrollbar
        lista_container = tk.Frame(main_container, bg="#2a1f3d", relief="sunken", bd=2)
        lista_container.pack(fill="both", expand=True, pady=(0, 15))
        
        # Canvas para scroll
        canvas = tk.Canvas(lista_container, bg="#2a1f3d", highlightthickness=0)
        scrollbar = tk.Scrollbar(lista_container, orient="vertical", command=canvas.yview,
                                bg="#2a1f3d", troughcolor="#130f26", activebackground="#4a3f5d")
        
        self.sessoes_frame = tk.Frame(canvas, bg="#2a1f3d")
        
        self.sessoes_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.sessoes_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botão de salvar sessão atual
        btn_frame = tk.Frame(main_container, bg="#1a0869")
        btn_frame.pack(fill="x", pady=(0, 0))

        btn_salvar_atual = tk.Button(btn_frame, text="💾 Salvar Atual",command=self.salvar_sessao_atual,
                                    bg="#1a5f2a", fg="white", font=("Arial", 11, "bold"),
                                    relief="raised", bd=2, activebackground="#2a7f3a",height=2)
        btn_salvar_atual.pack(side="left", fill="x", expand=True, padx=(0, 3))

        btn_salvar_novo = tk.Button(btn_frame, text="📋 Salvar Novo",command=self.salvar_sessao_nova,
                                    bg="#1a4f7a", fg="white", font=("Arial", 11, "bold"),
                                    relief="raised", bd=2, activebackground="#2a6f9a",height=2)
        btn_salvar_novo.pack(side="left", fill="x", expand=True, padx=(3, 3))

        btn_nova_sessao = tk.Button(btn_frame, text="🆕 Nova Sessão",command=self.nova_sessao,
                                    bg="#6a3f00", fg="white", font=("Arial", 11, "bold"),
                                    relief="raised", bd=2, activebackground="#8a5f10",height=2)
        btn_nova_sessao.pack(side="left", fill="x", expand=True, padx=(3, 0))
        
        # === INFORMAÇÕES DO APLICATIVO (LADO DIREITO E AUMENTADA) ===
        sobre_frame = tk.Frame(self, bg="#1a0869", relief="raised", bd=3)
        sobre_frame.place(x=950, y=220, width=500, height=550)

        # Título da seção sobre
        sobre_title_bg = tk.Frame(sobre_frame, bg="#2a1f3d", height=50)
        sobre_title_bg.pack(fill="x")
        tk.Label(sobre_title_bg, text="ℹ️ Sobre o Aplicativo", 
                font=("Arial", 18, "bold"), fg="#ffffff", bg="#2a1f3d").pack(pady=12)

        # Conteúdo sobre
        sobre_content = tk.Frame(sobre_frame, bg="#1a0869")
        sobre_content.pack(fill="both", expand=True, padx=20, pady=15)

        sobre_o_app = """🎯 Versão 1.4.0

👨‍💻 Desenvolvido por:
    Lucas Henrique Gonzaga Santos

🐍 Linguagem:
    Python

🖼️ Interface:
    Tkinter

💻 Editor:
    Visual Studio Code

🎮 Sistema de combate tático
    para RPGs de mesa"""

        sobre_label = tk.Label(sobre_content, text=sobre_o_app, 
                             font=("Arial", 13), fg="white", bg="#1a0869", 
                             justify="left", anchor="nw")
        sobre_label.pack(fill="both", expand=True)

        # Botão de shutdown reduzido
        shutdown_frame = tk.Frame(self, bg="#130f26")
        shutdown_frame.place(x=700, y=810, width=200, height=70)
        
        btn_sair = tk.Button(shutdown_frame, text="🔴 SHUTDOWN", 
                           font=("Arial", 18, "bold"), fg="white", bg="#8b1538",
                           command=controller.quit, relief="raised", bd=4,
                           activebackground="#a61e42", activeforeground="white")
        btn_sair.pack(fill="both", expand=True)
        
        # Carrega a lista de sessões na inicialização
        self.atualizar_lista_sessoes()

    def atualizar_lista_sessoes(self):
        """Atualiza a lista de sessões com botões individuais"""
        try:
            # Limpa frame
            for widget in self.sessoes_frame.winfo_children():
                widget.destroy()
            
            # Importa a função correta do módulo D
            from Dados import listar_sessoes
            sessoes = listar_sessoes()
            
            if not sessoes:
                # Mensagem quando não há sessões
                msg_frame = tk.Frame(self.sessoes_frame, bg="#2a1f3d")
                msg_frame.pack(fill="x", padx=10, pady=20)
                tk.Label(msg_frame, text="📭 Nenhuma sessão salva", 
                        font=("Arial", 12, "italic"), fg="#888888", bg="#2a1f3d").pack()
                return
            
            for idx, sessao in enumerate(sessoes):
                # Frame para cada sessão
                sessao_item = tk.Frame(self.sessoes_frame, bg="#1a0869" if idx % 2 == 0 else "#2a1f3d", 
                                      relief="solid", bd=1)
                sessao_item.pack(fill="x", padx=5, pady=3)
                
                # Frame esquerdo - Info da sessão
                info_frame = tk.Frame(sessao_item, bg=sessao_item['bg'])
                info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)
                
                # Nome da sessão
                nome_label = tk.Label(info_frame, 
                                     text=f"📂 {sessao['nome']}", 
                                     font=("Arial", 13, "bold"), 
                                     fg="#ffffff", bg=info_frame['bg'],
                                     anchor="w")
                nome_label.pack(fill="x")
                
                # Info adicional
                info_text = f"👥 {sessao['total_personagens']} personagens em {sessao['total_grupos']} grupos"
                info_label = tk.Label(info_frame, 
                                     text=info_text, 
                                     font=("Arial", 10), 
                                     fg="#cccccc", bg=info_frame['bg'],
                                     anchor="w")
                info_label.pack(fill="x")
                
                # Frame direito - Botões de ação
                botoes_frame = tk.Frame(sessao_item, bg=sessao_item['bg'])
                botoes_frame.pack(side="right", padx=10, pady=8)
                
                # Botão Carregar
                btn_carregar = tk.Button(botoes_frame, text="Carregar", 
                                        command=lambda n=sessao['nome']: self.carregar_sessao(n),
                                        bg="#2a1f3d", fg="white", font=("Arial", 11, "bold"),
                                        width=10, relief="raised", bd=2,
                                        activebackground="#4a3f5d")
                btn_carregar.pack(side="left", padx=3)
                
                # Botão Renomear
                btn_renomear = tk.Button(botoes_frame, text="Renomear", 
                                        command=lambda n=sessao['nome']: self.renomear_sessao(n),
                                        bg="#2a1f3d", fg="white", font=("Arial", 11, "bold"),
                                        width=10, relief="raised", bd=2,
                                        activebackground="#4a3f5d")
                btn_renomear.pack(side="left", padx=3)
                
                # Botão Deletar
                btn_deletar = tk.Button(botoes_frame, text="Apagar", 
                                       command=lambda n=sessao['nome']: self.deletar_sessao(n),
                                       bg="#8b1538", fg="white", font=("Arial", 11, "bold"),
                                       width=8, relief="raised", bd=2,
                                       activebackground="#a61e42")
                btn_deletar.pack(side="left", padx=3)
                
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Erro ao carregar lista de sessões: {e}")

    def _restaurar_log_combate(self, combat_screen):
        """Recria os widgets de log a partir do log_historico salvo."""
        try:
            # Limpa widgets existentes
            for w in combat_screen.log_inner_frame.winfo_children():
                w.destroy()

            # Recria cada entrada
            for entrada in combat_screen.log_historico:
                ts  = entrada.get("timestamp", "")
                msg = entrada.get("mensagem", "")
                cor = entrada.get("cor", "white")
                det = entrada.get("detalhes")

                # Usa o mesmo método, mas evita duplicar no histórico
                _original = combat_screen.log_historico
                combat_screen.log_historico = None  # flag temporária

                combat_screen.adicionar_log(msg, cor=cor, detalhes=det)

                combat_screen.log_historico = _original  # restaura

        except Exception as e:
            print(f"⚠️ Erro ao restaurar log: {e}")

    def deletar_sessao(self, nome_sessao):
        """Deleta a sessão especificada"""
        try:
            # Confirma a exclusão
            if tk.messagebox.askyesno("Confirmar Exclusão", 
                                    f"Tem certeza que deseja deletar a sessão '{nome_sessao}'?\n\nEsta ação não pode ser desfeita."):
                from Dados import deletar_sessao
                
                if deletar_sessao(nome_sessao):
                    tk.messagebox.showinfo("Sucesso", f"Sessão '{nome_sessao}' deletada com sucesso!")
                    self.atualizar_lista_sessoes()
                else:
                    tk.messagebox.showerror("Erro", f"Erro ao deletar sessão '{nome_sessao}'")
                    
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Erro ao deletar sessão: {e}")

    def renomear_sessao(self, nome_antigo):
        """Renomeia a sessão especificada"""
        try:
            # Dialog para pedir novo nome
            from tkinter import simpledialog
            nome_novo = simpledialog.askstring("Renomear Sessão", 
                                              f"Digite o novo nome para '{nome_antigo}':",
                                              parent=self)
            
            if not nome_novo:
                return
            
            nome_novo = nome_novo.strip()
            
            if nome_antigo == nome_novo:
                tk.messagebox.showwarning("Aviso", "O novo nome deve ser diferente do nome atual.")
                return
            
            # Confirma a renomeação
            if tk.messagebox.askyesno("Confirmar Renomeação", 
                                    f"Renomear sessão de:\n'{nome_antigo}'\npara:\n'{nome_novo}'?"):
                from Dados import clonar_sessao, deletar_sessao
                
                # Como não há função renomear_sessao, usa clone + delete
                if clonar_sessao(nome_antigo, nome_novo):
                    if deletar_sessao(nome_antigo):
                        tk.messagebox.showinfo("Sucesso", f"Sessão renomeada com sucesso:\n'{nome_antigo}' → '{nome_novo}'")
                        self.atualizar_lista_sessoes()
                    else:
                        tk.messagebox.showerror("Erro", "Sessão clonada, mas erro ao deletar a original.")
                        self.atualizar_lista_sessoes()
                else:
                    tk.messagebox.showerror("Erro", f"Erro ao renomear sessão. Verifique se o novo nome já existe.")
                    
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Erro ao renomear sessão: {e}")

    def salvar_sessao_atual(self):
        """Salva a sessão atual - cria nova se não houver sessão carregada"""
        try:
            import Dados as D
            from tkinter import simpledialog

            # ── Captura estado da tela de combate ─────────────────────────
            combat_screen = self.controller.frames.get(CombatSystemScreen)
            if combat_screen:
                # Estado de combate
                nomes_ordem = [p.nome for p in combat_screen.ordem_turno]
                
                # ✅ NOVO: Captura iniciativas de todos os personagens em combate
                iniciativas = {}
                for chave in ("_lista_superior", "_lista_inferior"):
                    lista = D.GruposDePersonagens.get(chave, [])
                    for personagem in lista:
                        iniciativas[personagem.nome] = getattr(personagem, 'iniciativa_atual', None)
                
                D.EstadoCombate.clear()
                D.EstadoCombate.update({
                    "ordem_turno_nomes":  nomes_ordem,
                    "turno_atual_index":  combat_screen.turno_atual_index,
                    "grupo_esquerdo":     combat_screen.grupo_esquerdo,
                    "grupo_direito":      combat_screen.grupo_direito,
                    "iniciativas":        iniciativas,  # ✅ NOVO: armazenar iniciativas
                })

                # Log de combate
                D.LogCombate.clear()
                D.LogCombate.extend(getattr(combat_screen, 'log_historico', []))

                # Estado do mapa (sem img_original — não serializável)
                D.EstadoMapa.clear()
                estado_mapa = dict(combat_screen._estado_mapa)
                estado_mapa.pop("img_original", None)
                D.EstadoMapa.update(estado_mapa)

            # ── Lógica de nome / sobrescrever ────────────────────────────
            if self.nome_sessao_atual:
                if tk.messagebox.askyesno("Confirmar Atualização",
                                        f"Atualizar a sessão '{self.nome_sessao_atual}'?"):
                    if D.salvar_sessao(self.nome_sessao_atual, sobrescrever=True):
                        tk.messagebox.showinfo("Sucesso", f"Sessão '{self.nome_sessao_atual}' atualizada!")
                        self.atualizar_lista_sessoes()
                    else:
                        tk.messagebox.showerror("Erro", f"Erro ao atualizar sessão '{self.nome_sessao_atual}'")
            else:
                nome_novo = simpledialog.askstring("Nova Sessão",
                                                "Digite o nome para a nova sessão:",
                                                parent=self)
                if not nome_novo:
                    return
                nome_novo = nome_novo.strip()
                if not nome_novo:
                    tk.messagebox.showwarning("Aviso", "Digite um nome válido para a sessão.")
                    return

                sessoes_existentes = D.listar_sessoes()
                sessao_existe = any(s['nome'] == nome_novo for s in sessoes_existentes)

                if sessao_existe:
                    if tk.messagebox.askyesno("Confirmar Sobrescrita",
                                            f"A sessão '{nome_novo}' já existe.\nDeseja sobrescrever?"):
                        if D.salvar_sessao(nome_novo, sobrescrever=True):
                            tk.messagebox.showinfo("Sucesso", f"Sessão '{nome_novo}' salva!")
                            self.nome_sessao_atual = nome_novo
                            self.atualizar_lista_sessoes()
                        else:
                            tk.messagebox.showerror("Erro", f"Erro ao salvar sessão '{nome_novo}'")
                else:
                    if D.salvar_sessao(nome_novo):
                        tk.messagebox.showinfo("Sucesso", f"Sessão '{nome_novo}' salva!")
                        self.nome_sessao_atual = nome_novo
                        self.atualizar_lista_sessoes()
                    else:
                        tk.messagebox.showerror("Erro", f"Erro ao salvar sessão '{nome_novo}'")

        except Exception as e:
            tk.messagebox.showerror("Erro", f"Erro ao salvar sessão: {e}")
            import traceback; traceback.print_exc()
    
    def salvar_sessao_nova(self):
        """Sempre pede um novo nome e salva como sessão nova"""
        try:
            import Dados as D
            from tkinter import simpledialog

            # Captura estado da tela de combate (igual ao salvar_sessao_atual)
            combat_screen = self.controller.frames.get(CombatSystemScreen)
            if combat_screen:
                nomes_ordem = [p.nome for p in combat_screen.ordem_turno]
                iniciativas = {}
                for chave in ("_lista_superior", "_lista_inferior"):
                    lista = D.GruposDePersonagens.get(chave, [])
                    for personagem in lista:
                        iniciativas[personagem.nome] = getattr(personagem, 'iniciativa_atual', None)

                D.EstadoCombate.clear()
                D.EstadoCombate.update({
                    "ordem_turno_nomes":  nomes_ordem,
                    "turno_atual_index":  combat_screen.turno_atual_index,
                    "grupo_esquerdo":     combat_screen.grupo_esquerdo,
                    "grupo_direito":      combat_screen.grupo_direito,
                    "iniciativas":        iniciativas,
                })
                D.LogCombate.clear()
                D.LogCombate.extend(getattr(combat_screen, 'log_historico', []))
                D.EstadoMapa.clear()
                estado_mapa = dict(combat_screen._estado_mapa)
                estado_mapa.pop("img_original", None)
                D.EstadoMapa.update(estado_mapa)

            nome_novo = simpledialog.askstring("Salvar Como Nova Sessão",
                                            "Digite o nome para a nova sessão:",
                                            parent=self)
            if not nome_novo:
                return
            nome_novo = nome_novo.strip()
            if not nome_novo:
                tk.messagebox.showwarning("Aviso", "Digite um nome válido.")
                return

            sessoes_existentes = D.listar_sessoes()
            sessao_existe = any(s['nome'] == nome_novo for s in sessoes_existentes)

            if sessao_existe:
                if not tk.messagebox.askyesno("Confirmar Sobrescrita",
                                            f"A sessão '{nome_novo}' já existe.\nDeseja sobrescrever?"):
                    return
                ok = D.salvar_sessao(nome_novo, sobrescrever=True)
            else:
                ok = D.salvar_sessao(nome_novo)

            if ok:
                tk.messagebox.showinfo("Sucesso", f"Sessão '{nome_novo}' salva!")
                self.nome_sessao_atual = nome_novo
                self.atualizar_lista_sessoes()
            else:
                tk.messagebox.showerror("Erro", f"Erro ao salvar sessão '{nome_novo}'")

        except Exception as e:
            tk.messagebox.showerror("Erro", f"Erro ao salvar nova sessão: {e}")
            import traceback; traceback.print_exc()

    def nova_sessao(self):
        """Limpa todos os dados para começar uma sessão do zero"""
        try:
            if not tk.messagebox.askyesno("Nova Sessão",
                                        "Isso irá apagar todos os dados não salvos.\n\nDeseja continuar?"):
                return

            import Dados as D

            # Limpa todos os dados globais
            D.GruposDePersonagens.clear()
            D.KitsDisponíveis.clear()
            D.EstadoCombate.clear()
            D.LogCombate.clear()
            D.EstadoMapa.clear()

            # Reseta o nome da sessão atual
            self.nome_sessao_atual = None

            # Reseta a tela de combate se existir
            combat_screen = self.controller.frames.get(CombatSystemScreen)
            if combat_screen:
                combat_screen.ordem_turno = []
                combat_screen.turno_atual_index = 0
                combat_screen.grupo_esquerdo = None
                combat_screen.grupo_direito = None
                combat_screen.log_historico = []
                combat_screen._estado_mapa.clear()
                try:
                    combat_screen.atualizar_fila_turno()
                    combat_screen.atualizar_card_turno_atual()
                except Exception:
                    pass
                try:
                    for w in combat_screen.log_inner_frame.winfo_children():
                        w.destroy()
                except Exception:
                    pass

            # Atualiza todas as telas
            if hasattr(self.controller, 'atualizar_todas_telas'):
                self.controller.atualizar_todas_telas()

            tk.messagebox.showinfo("Nova Sessão", "✅ Sessão limpa! Pronto para começar.")

        except Exception as e:
            tk.messagebox.showerror("Erro", f"Erro ao criar nova sessão: {e}")
            import traceback; traceback.print_exc()

    def carregar_sessao(self, nome_sessao):
        """Carrega a sessão especificada e restaura o estado de combate"""
        try:
            import Dados as D

            if D.carregar_sessao(nome_sessao):
                self.nome_sessao_atual = nome_sessao

                # ── Restaura tela de combate ──────────────────────────────
                combat_screen = self.controller.frames.get(CombatSystemScreen)
                if combat_screen and D.EstadoCombate:
                    ec = D.EstadoCombate

                    # Grupos selecionados
                    combat_screen.grupo_esquerdo = ec.get("grupo_esquerdo")
                    combat_screen.grupo_direito  = ec.get("grupo_direito")

                    # Ordem de turno — reconstrói lista de objetos a partir dos nomes
                    nomes = ec.get("ordem_turno_nomes", [])
                    todos = [p for lista in D.GruposDePersonagens.values() for p in lista]
                    mapa_nomes = {p.nome: p for p in todos}
                    combat_screen.ordem_turno = [mapa_nomes[n] for n in nomes if n in mapa_nomes]
                    combat_screen.turno_atual_index = ec.get("turno_atual_index", 0)

                    # ✅ NOVO: Restaura iniciativas de cada personagem
                    iniciativas_salvas = ec.get("iniciativas", {})
                    for nome_pers, init_valor in iniciativas_salvas.items():
                        pers = mapa_nomes.get(nome_pers)
                        if pers and init_valor is not None:
                            pers.iniciativa_atual = init_valor

                    # Mapa
                    combat_screen._estado_mapa.clear()
                    combat_screen._estado_mapa.update(D.EstadoMapa)

                    # Log — limpa widgets e redesenha a partir do histórico
                    combat_screen.log_historico = list(D.LogCombate)
                    self._restaurar_log_combate(combat_screen)

                    # Atualiza UI da tela de combate
                    combat_screen.atualizar_fila_turno()
                    combat_screen.atualizar_card_turno_atual()

                # Atualiza outras telas
                if hasattr(self.controller, 'atualizar_todas_telas'):
                    self.controller.atualizar_todas_telas()

                tk.messagebox.showinfo("Sucesso", f"Sessão '{nome_sessao}' carregada com sucesso!")
            else:
                tk.messagebox.showerror("Erro", f"Erro ao carregar sessão '{nome_sessao}'")

        except Exception as e:
            tk.messagebox.showerror("Erro", f"Erro ao carregar sessão: {e}")
            import traceback; traceback.print_exc()

    def TelaDeSelecao(self):
        self.controller.TelaDeSelecao()

    def TelaDeCombate(self):
        self.controller.TelaDeCombate()

    def TelaDeRegrasEItens(self):
        self.controller.TelaDeRegrasEItens()
### TELA PRINCIPAL ###
### TELA PRINCIPAL ###
### TELA PRINCIPAL ###

### TELA DE SELEÇÃO ###
### TELA DE SELEÇÃO ###
### TELA DE SELEÇÃO ###
class CharacterSelectScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.grupos_personagens = D.GruposDePersonagens
        
        # ✅ Filtra grupos ocultos (que começam com _lista_)
        keys = [g for g in self.grupos_personagens.keys() if not g.startswith("_lista_")]
        valor_inicial = keys[0] if keys else "Sem grupos"
        self.group_var = tk.StringVar(value=valor_inicial)
        self.config(bg='#130f26')

        tk.Button(self, text="Tela inicial", command=self.TelaInicial, bg="#1a0869", fg="white", font=("Arial", 20)).place(x=20, y=10, width=350, height=75)
        tk.Label(self, text="Seleção", fg="white", bg="#1a0869", font=("Arial", 20, "bold")).place(x=385, y=10, width=350, height=75)
        tk.Button(self, text="Combate", command=self.TelaDeCombate, bg="#1a0869", fg="white", font=("Arial", 20)).place(x=870, y=10, width=350, height=75)
        tk.Button(self, text="Informações", command=self.TelaDeRegrasEItens, bg="#1a0869", fg="white", font=("Arial", 20)).place(x=1235, y=10, width=350, height=75)
        tk.Frame(self, bg="#2a1a79", height=2).place(x=0, y=95, relwidth=1)

        self.group_management_frame = tk.Frame(self, bg='#1a0869')
        self.group_management_frame.place(x=20, y=110, width=590, height=90)
        self.create_group_management(self.group_management_frame)
        self.group_list_frame = tk.Frame(self, bg='#1a0869')
        self.group_list_frame.place(x=20, y=210, width=590, height=545)
        self.create_group_list_section(self.group_list_frame)

        self.char_management_frame = tk.Frame(self, bg='#1a0869')
        self.char_management_frame.place(x=650, y=110, width=590, height=90)
        self.create_char_management(self.char_management_frame)
        self.char_list_frame = tk.Frame(self, bg='#1a0869')
        self.char_list_frame.place(x=650, y=210, width=590, height=545)
        self.create_list_section(self.char_list_frame)
        self.refresh_all()
        self.after(50,lambda:self.focus_set())

### --- Grupos --- ###
    def clear_placeholder(self, event):
        if self.new_group_entry.get() == "Nome do novo grupo...":
            self.new_group_entry.delete(0, tk.END)
            self.new_group_entry.config(fg="white")

    def restore_placeholder(self, event):
        if not self.new_group_entry.get():
            self.new_group_entry.insert(0, "Nome do novo grupo...")
            self.new_group_entry.config(fg="#4a4470")

    def create_group_management(self,frame):
        for widget in frame.winfo_children(): widget.destroy()
        tk.Label(frame,text="Grupos de Personagens",fg="white",bg="#1a0869",font=("Arial",15,"bold")).pack(anchor="w")
        tk.Button(frame,text="+ Novo Grupo",bg="#411f9c", fg="white", font=("Arial", 11, "bold"),relief="flat", cursor="hand2",activebackground="#411f9c",command=self.abrir_popup_novo_grupo).pack(pady=(10,0),ipadx=12,ipady=8,anchor="w")

    def create_group_list_section(self, frame):
        """Mostra apenas grupos visíveis (exclui _lista_superior e _lista_inferior)"""
        for widget in frame.winfo_children(): 
            widget.destroy()
        
        tk.Frame(frame,bg="#2a1a79",height=2).pack(fill="x",side="top")
        tk.Frame(frame,bg="#2a1a79",width=2).pack(fill="y",side="left")
        tk.Frame(frame,bg="#2a1a79",width=2).pack(fill="y",side="right")

        header=tk.Frame(frame,bg="#1a0869",height=42)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Frame(header,bg="#2a1a79",width=4).pack(side="left",fill="y")
        
        # ✅ NOVO: Filtra grupos ocultos
        grupos_visiveis = [g for g in D.GruposDePersonagens.keys() 
                        if not g.startswith("_lista_")]
        
        tk.Label(header,text="  Grupos",fg="white",bg="#1a0869",font=("Arial",13,"bold")).pack(side="left",pady=10)
        tk.Label(header,text=f"{len(grupos_visiveis)} grupo(s)",fg="#4a4470",bg="#1a0869",font=("Arial",10)).pack(side="right",padx=14)

        tk.Frame(frame,bg="#2a1a79",height=1).pack(fill="x")

        canvas_frame=tk.Frame(frame,bg="#1a0869")
        canvas_frame.pack(fill="both",expand=True)

        canvas=tk.Canvas(canvas_frame,bg="#0f0a1f",highlightthickness=0)
        scrollbar=tk.Scrollbar(canvas_frame,orient="vertical",command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right",fill="y")
        canvas.pack(side="left",fill="both",expand=True)

        inner_frame=tk.Frame(canvas,bg="#0f0a1f")
        window_id=canvas.create_window((0,0),window=inner_frame,anchor="nw")

        inner_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>",lambda e: canvas.itemconfig(window_id,width=e.width))

        # ✅ USA APENAS GRUPOS VISÍVEIS
        grupos = grupos_visiveis

        if not grupos:
            tk.Label(inner_frame,text="Nenhum grupo criado ainda.",fg="#4a4470",bg="#0f0a1f",font=("Arial",12,"italic")).pack(pady=40)
            return

        for grupo in grupos:
            num_personagens=len(D.GruposDePersonagens.get(grupo,[]))
            is_selected=self.group_var.get()==grupo
            row_bg="#2a1a79" if is_selected else "#1a0869"
            accent="#411f9c" if is_selected else "#2a1a79"

            row=tk.Frame(inner_frame,bg=row_bg)
            row.pack(fill="x",pady=2)

            tk.Frame(row,bg=accent,width=4).pack(side="left",fill="y")

            tk.Button(row,text=f"  {grupo}",bg=row_bg,fg="white",font=("Arial",12,"bold" if is_selected else "normal"),anchor="w",relief="flat",activebackground="#411f9c",cursor="hand2",command=lambda g=grupo:self.select_group(g)).pack(side="left",fill="x",expand=True,ipady=13)

            tk.Label(row,text=f"{num_personagens}p",fg="#4a4470",bg=row_bg,font=("Arial",12)).pack(side="left",padx=4)

            tk.Button(row,text="✎",bg=row_bg,fg="white",font=("Arial",11),relief="flat",activebackground="#411f9c",cursor="hand2",width=2,command=lambda g=grupo:self.renomear_grupo(g)).pack(side="left",padx=2,ipady=8)

            tk.Button(row,text="✕",bg=row_bg,fg="#ff6b6b",font=("Arial",11,"bold"),relief="flat",activebackground="#5a1010",cursor="hand2",width=2,command=lambda g=grupo:self.delete_group(g)).pack(side="right",padx=6,ipady=8)

    def renomear_grupo(self, group_name):
        """Renomeia um grupo"""
        # ✅ NOVO: Impede renomear grupos ocultos
        if group_name.startswith("_lista_"):
            messagebox.showwarning("Aviso", "Não é possível renomear grupos de combate.")
            return
        
        popup = tk.Toplevel(self)
        popup.title("Renomear Grupo")
        popup.geometry("360x160")
        popup.config(bg="#130f26")
        popup.resizable(False, False)
        tk.Label(popup, text=f"Renomear: {group_name}", bg="#130f26", fg="white", font=("Arial", 12, "bold")).pack(pady=14)
        entry = tk.Entry(popup, font=("Arial", 13), bg="#2a1a79", fg="white", insertbackground="white", relief="flat", justify="center")
        entry.pack(padx=20, fill="x", ipady=8)
        entry.insert(0, group_name)
        entry.select_range(0, tk.END)
        entry.focus_set()
        
        def confirmar(*_):
            novo_nome = entry.get().strip()
            if not novo_nome:
                messagebox.showwarning("Aviso", "Digite um nome válido.", parent=popup)
                return
            if novo_nome == group_name:
                popup.destroy()
                return
            if novo_nome in D.GruposDePersonagens:
                messagebox.showwarning("Aviso", "Já existe um grupo com esse nome.", parent=popup)
                return
            D.GruposDePersonagens[novo_nome] = D.GruposDePersonagens.pop(group_name)
            if self.group_var.get() == group_name:
                self.group_var.set(novo_nome)
            popup.destroy()
            self.refresh_all()
        
        entry.bind("<Return>", confirmar)
        tk.Button(popup, text="Confirmar", command=confirmar, bg="#411f9c", fg="white", font=("Arial", 12, "bold"), relief="flat", cursor="hand2").pack(pady=14, ipadx=20, ipady=6)

    def select_group(self, group_name):
        """Seleciona um grupo, mas bloqueia grupos ocultos"""
        # ✅ NOVO: Bloqueia grupos que começam com _lista_
        if group_name.startswith("_lista_"):
            return  # Ignora silenciosamente
        
        self.group_var.set(group_name)
        self.create_group_list_section(self.group_list_frame)
        self.create_list_section(self.char_list_frame)

    def delete_group(self, group_name):
        """Deleta um grupo"""
        # ✅ NOVO: Impede deletar grupos ocultos
        if group_name.startswith("_lista_"):
            messagebox.showwarning("Aviso", "Não é possível deletar grupos de combate.")
            return
        
        if messagebox.askyesno("Confirmar", f"Excluir o grupo '{group_name}'?\n\nTodos os personagens serão perdidos!"):
            del D.GruposDePersonagens[group_name]
            if self.group_var.get() == group_name:
                # ✅ NOVO: Usa apenas grupos visíveis
                remaining = [g for g in D.GruposDePersonagens.keys() if not g.startswith("_lista_")]
                self.group_var.set(remaining[0] if remaining else "Sem grupos")
            self.refresh_all()

    def abrir_popup_novo_grupo(self):
        popup=tk.Toplevel(self)
        popup.title("Novo Grupo")
        popup.geometry("360x160")
        popup.config(bg="#130f26")
        popup.resizable(False,False)

        tk.Label(popup,text="Nome do novo grupo",bg="#130f26",fg="white",font=("Arial",12,"bold")).pack(pady=14)

        entry=tk.Entry(popup,font=("Arial",13),bg="#2a1a79",fg="white",insertbackground="white",relief="flat",justify="center")
        entry.pack(padx=20,fill="x",ipady=8)
        entry.focus_set()

        def confirmar(*_):
            nome=entry.get().strip()
            if not nome:
                messagebox.showwarning("Aviso","Digite um nome válido.",parent=popup); return
            if nome in D.GruposDePersonagens:
                messagebox.showwarning("Aviso","Já existe um grupo com esse nome.",parent=popup); return
            D.GruposDePersonagens[nome]=[]
            self.group_var.set(nome)
            popup.destroy()
            self.refresh_all()

        entry.bind("<Return>",confirmar)

        tk.Button(popup,text="Confirmar",command=confirmar,bg="#411f9c",fg="white",font=("Arial",12,"bold"),relief="flat",cursor="hand2").pack(pady=14,ipadx=20,ipady=6)
### --- Grupos --- ###

### --- Personagens --- ###
    def create_char_management(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        tk.Label(frame, text="Personagens", fg="white", bg="#1a0869", font=("Arial", 15, "bold")).pack(anchor="w")
        tk.Button(frame, text="Excluir todos",bg="#411f9c", fg="white", font=("Arial", 11, "bold"),relief="flat", cursor="hand2",activebackground="#411f9c", command=self.limpar_grupo_atual).pack(pady=(10,0),ipadx=12,ipady=8,anchor="w")

    def create_list_section(self, frame):
        for widget in frame.winfo_children(): widget.destroy()

        grupo_atual=self.group_var.get()
        personagens=D.GruposDePersonagens.get(grupo_atual,[])

        tk.Frame(frame,bg="#2a1a79",height=2).pack(fill="x",side="top")
        tk.Frame(frame,bg="#2a1a79",width=2).pack(fill="y",side="left")
        tk.Frame(frame,bg="#2a1a79",width=2).pack(fill="y",side="right")

        header=tk.Frame(frame,bg="#1a0869",height=42)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Frame(header,bg="#2a1a79",width=4).pack(side="left",fill="y")
        tk.Label(header,text=f"  {grupo_atual}",fg="white",bg="#1a0869",font=("Arial",13,"bold")).pack(side="left",pady=10)
        tk.Label(header,text=f"{len(personagens)} pers.",fg="#4a4470",bg="#1a0869",font=("Arial",10)).pack(side="right",padx=14)

        tk.Frame(frame,bg="#2a1a79",height=1).pack(fill="x")

        canvas_frame=tk.Frame(frame,bg="#1a0869")
        canvas_frame.pack(fill="both",expand=True)

        canvas=tk.Canvas(canvas_frame,bg="#0f0a1f",highlightthickness=0)
        scrollbar=tk.Scrollbar(canvas_frame,orient="vertical",command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right",fill="y")
        canvas.pack(side="left",fill="both",expand=True)

        inner_frame=tk.Frame(canvas,bg="#0f0a1f")
        window_id=canvas.create_window((0,0),window=inner_frame,anchor="nw")

        inner_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>",lambda e: canvas.itemconfig(window_id,width=e.width))

        if grupo_atual=="Sem grupos":
            tk.Label(inner_frame,text="Selecione um grupo para ver os personagens.",fg="#4a4470",bg="#0f0a1f",font=("Arial",12,"italic")).pack(pady=40)
            return

        if not personagens:
            tk.Label(inner_frame,text="Nenhum personagem neste grupo.",fg="#4a4470",bg="#0f0a1f",font=("Arial",12,"italic")).pack(pady=40)

        for char in personagens:
            if isinstance(char,CB.Personagem):
                hp_ratio=char.VidaAtual/char.VidaMax if char.VidaMax>0 else 0
                hp_color="#2a1a79" if hp_ratio>0.5 else ("#8f6b10" if hp_ratio>0.2 else "#6e2a2a")

                row=tk.Frame(inner_frame,bg="#1a0869")
                row.pack(fill="x",pady=2)

                tk.Frame(row,bg=hp_color,width=4).pack(side="left",fill="y")

                info_frame=tk.Frame(row,bg="#1a0869")
                info_frame.pack(side="left",fill="x",expand=True,padx=8,pady=8)

                tk.Label(info_frame,text=char.nome,fg="white",bg="#1a0869",font=("Arial",14,"bold"),anchor="w").pack(fill="x")
                tk.Label(info_frame,text=f"Nv.{char.Nivel}  •  XP {char.XPAtual}/{char.XPlvlUp}  •  HP {char.VidaAtual}/{char.VidaMax}",fg="#4a4470",bg="#1a0869",font=("Arial",11),anchor="w").pack(fill="x")

                btn_frame=tk.Frame(row,bg="#1a0869")
                btn_frame.pack(side="right",padx=6)

                tk.Button(btn_frame,text="↗",bg="#1a0869",fg="white",font=("Arial",13),relief="flat",activebackground="#2a1a79",cursor="hand2",width=2,command=lambda c=char:self.controller.abrir_detalhes(c)).pack(pady=(4,2))
                tk.Button(btn_frame,text="⇄",bg="#1a0869",fg="white",font=("Arial",13),relief="flat",activebackground="#2a1a79",cursor="hand2",width=2,command=lambda c=char:self.transferir_personagem(c)).pack(pady=2)
                tk.Button(btn_frame,text="✕",bg="#1a0869",fg="#ff6b6b",font=("Arial",12,"bold"),relief="flat",activebackground="#5a1010",cursor="hand2",width=2,command=lambda c=char:self.remove_specific_character(c)).pack(pady=(2,4))

        action_frame=tk.Frame(inner_frame,bg="#0f0a1f")
        action_frame.pack(fill="x",pady=10)

        tk.Frame(action_frame,bg="#2a1a79",height=1).pack(fill="x",pady=(0,10))

        btn_row=tk.Frame(action_frame,bg="#0f0a1f")
        btn_row.pack(fill="x")

        tk.Button(btn_row,text="+ Adicionar",bg="#1a0869",fg="white",font=("Arial",11,"bold"),relief="flat",cursor="hand2",activebackground="#411f9c",command=self.add_character_to_current_group).pack(side="left",ipadx=14,ipady=8)
        tk.Button(btn_row,text="Gerar Vários",bg="#1a0869",fg="white",font=("Arial",11,"bold"),relief="flat",cursor="hand2",activebackground="#411f9c",command=self.gerar_varios_personagens).pack(side="left",padx=10,ipadx=14,ipady=8)
        tk.Button(btn_row,text="Gerar NPC",bg="#1a0869",fg="white",font=("Arial",11,"bold"),relief="flat",cursor="hand2",activebackground="#411f9c",command=self.gerar_NPC_to_current_group).pack(side="right",ipadx=14,ipady=8)

    def transferir_personagem(self, character):
        grupo_atual = self.group_var.get()
        outros_grupos = [g for g in D.GruposDePersonagens.keys() if g != grupo_atual]
        if not outros_grupos:
            messagebox.showinfo("Aviso", "Não há outros grupos para transferir.")
            return
        popup = tk.Toplevel(self)
        popup.title("Transferir Personagem")
        popup.geometry("360x200")
        popup.config(bg="#130f26")
        popup.resizable(False, False)
        tk.Label(popup, text=f"Transferir: {character.nome}", bg="#130f26", fg="white", font=("Arial", 12, "bold")).pack(pady=14)
        tk.Label(popup, text="Selecione o grupo de destino:", bg="#130f26", fg="white", font=("Arial", 11)).pack()
        destino_var = tk.StringVar(value=outros_grupos[0])
        destino_menu = tk.OptionMenu(popup, destino_var, *outros_grupos)
        destino_menu.config(bg="#1a0869", fg="white", font=("Arial", 12), width=28, relief="flat")
        destino_menu.pack(pady=10)
        def confirmar():
            destino = destino_var.get()
            try:
                D.GruposDePersonagens[grupo_atual].remove(character)
            except ValueError:
                pass
            D.GruposDePersonagens.setdefault(destino, []).append(character)
            popup.destroy()
            self.refresh_all()
        tk.Button(popup, text="Transferir", command=confirmar, bg="#411f9c", fg="white", font=("Arial", 12, "bold"), relief="flat", cursor="hand2").pack(ipadx=20, ipady=6)

    def gerar_varios_personagens(self):
        popup_qtd = tk.Toplevel(self)
        popup_qtd.title("Gerar Vários NPCs")
        popup_qtd.geometry("300x150")
        popup_qtd.config(bg="#130f26")
        tk.Label(popup_qtd, text="Quantidade de NPCs", bg="#130f26", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        qtd_entry = tk.Entry(popup_qtd, font=("Arial", 12), justify="center", bg="#2a1a79", fg="white", insertbackground="white")
        qtd_entry.pack(pady=5)
        qtd_entry.insert(0, "1")
        def confirmar_qtd():
            try:
                qtd = int(qtd_entry.get())
                if qtd <= 0: raise ValueError
                popup_qtd.destroy()
                self._abrir_config_varios_npcs(qtd)
            except ValueError:
                messagebox.showerror("Erro", "Digite um número válido maior que 0.")
        tk.Button(popup_qtd, text="Confirmar", command=confirmar_qtd, bg="#411f9c", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

    def _abrir_config_varios_npcs(self, quantidade):
        current_group = self.group_var.get()
        if not current_group or current_group == "Sem grupos":
            messagebox.showwarning("Aviso", "Selecione ou crie um grupo primeiro.")
            return
        popup = tk.Toplevel(self)
        popup.title("Configurar NPCs")
        popup.geometry("700x500")
        popup.config(bg="#130f26")
        npcs_dados = D.carregar_npcs()
        if not npcs_dados:
            messagebox.showerror("Erro", "Não foi possível carregar os tipos de NPCs.")
            popup.destroy()
            return
        npcs_por_grupo = {}
        for classe, npc_data in npcs_dados.items():
            grp = npc_data.get("grupo", "Sem Grupo")
            npcs_por_grupo.setdefault(grp, []).append(npc_data)
        canvas_frame = tk.Frame(popup, bg='#130f26')
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        canvas = tk.Canvas(canvas_frame, bg="#130f26", highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        inner_frame = tk.Frame(canvas, bg="#130f26")
        canvas.create_window((0, 0), window=inner_frame, anchor='nw')
        inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        self.linhas_npcs = []
        grupos_npcs = list(npcs_por_grupo.keys())
        for i in range(quantidade):
            linha_frame = tk.Frame(inner_frame, bg="#1a0869")
            linha_frame.pack(fill="x", pady=4, padx=4)
            grupo_var = tk.StringVar(value=grupos_npcs[0] if grupos_npcs else "")
            grupo_menu = tk.OptionMenu(linha_frame, grupo_var, *grupos_npcs)
            grupo_menu.config(bg="#2a1a79", fg="white", font=("Arial", 10), width=18)
            grupo_menu.pack(side="left", padx=5, pady=5)
            classe_var = tk.StringVar()
            classe_menu = tk.OptionMenu(linha_frame, classe_var, "")
            classe_menu.config(bg="#2a1a79", fg="white", font=("Arial", 10), width=18)
            classe_menu.pack(side="left", padx=5, pady=5)
            def atualizar_classes_linha(g_var=grupo_var, c_var=classe_var, c_menu=classe_menu, *_):
                npcs_grp = npcs_por_grupo.get(g_var.get(), [])
                classes = [n.get("Classe", n.get("classe", "")) for n in npcs_grp]
                menu = c_menu["menu"]
                menu.delete(0, "end")
                if classes:
                    c_var.set(classes[0])
                    for c in classes:
                        menu.add_command(label=c, command=lambda v=c, cv=c_var: cv.set(v))
                else:
                    c_var.set("")
            grupo_var.trace_add("write", lambda *a, gv=grupo_var, cv=classe_var, cm=classe_menu: atualizar_classes_linha(gv, cv, cm))
            atualizar_classes_linha(grupo_var, classe_var, classe_menu)
            nivel_entry = tk.Entry(linha_frame, width=5, justify="center", bg="#2a1a79", fg="white", insertbackground="white")
            nivel_entry.insert(0, "1")
            nivel_entry.pack(side="left", padx=5)
            nome_entry = tk.Entry(linha_frame, width=20, bg="#2a1a79", fg="white", insertbackground="white")
            nome_entry.pack(side="left", padx=5)
            self.linhas_npcs.append({"grupo_var": grupo_var, "classe_var": classe_var, "nivel_entry": nivel_entry, "nome_entry": nome_entry, "npcs_por_grupo": npcs_por_grupo})
        def confirmar_geracao():
            try:
                npcs_criados = 0
                for linha in self.linhas_npcs:
                    grupo_npc = linha["grupo_var"].get()
                    classe_npc = linha["classe_var"].get()
                    nivel_str = linha["nivel_entry"].get()
                    nome = linha["nome_entry"].get()
                    try:
                        nivel = int(nivel_str)
                    except ValueError:
                        nivel = 1
                    if not classe_npc:
                        messagebox.showwarning("Aviso", "Selecione um tipo de NPC para todas as linhas.")
                        return
                    if not nome:
                        nome = f"{classe_npc}_{random.randint(1, 1000)}"
                    npcs_grp = linha["npcs_por_grupo"].get(grupo_npc, [])
                    npc_base = next((n for n in npcs_grp if n.get("Classe", n.get("classe", "")) == classe_npc), None)
                    if not npc_base:
                        messagebox.showwarning("Aviso", f"Classe '{classe_npc}' não encontrada.")
                        continue
                    proficiencias_dados = D.carregar_proficiencias()
                    proficiencias_objetos = {np_: CB.Proficiencia(np_, dp["atributo"], nivel=0) for np_, dp in proficiencias_dados.items()}
                    npc = CB.NPC(
                        nome=nome, nivel=nivel,
                        classe=npc_base.get("Classe", npc_base.get("classe")),
                        grupo=npc_base.get("grupo"),
                        Forca=int(npc_base.get("Forca", npc_base.get("forca", 1))),
                        Agilidade=int(npc_base.get("Agilidade", npc_base.get("agilidade", 1))),
                        Vigor=int(npc_base.get("Vigor", npc_base.get("vigor", 1))),
                        Inteligencia=int(npc_base.get("Inteligencia", npc_base.get("inteligencia", 1))),
                        Presenca=int(npc_base.get("Presenca", npc_base.get("presenca", 1))),
                        Tatica=int(npc_base.get("Tatica", npc_base.get("tatica", 1))),
                        Poder=int(npc_base.get("Poder", npc_base.get("poder", 1))),
                        proficiencias_base=proficiencias_objetos,
                    )
                    personagem = npc.gerar()
                    personagem.preencher_recursos_ao_maximo()
                    target_group = self.group_var.get()
                    if target_group not in D.GruposDePersonagens:
                        D.GruposDePersonagens[target_group] = []
                    D.GruposDePersonagens[target_group].append(personagem)
                    npcs_criados += 1
                self.refresh()
                popup.destroy()
                messagebox.showinfo("Sucesso", f"{npcs_criados} personagem(ns) gerado(s)!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao gerar os NPCs:\n{str(e)}")
                import traceback; traceback.print_exc()
        tk.Button(popup, text="Confirmar", command=confirmar_geracao, bg="#411f9c", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

    def limpar_grupo_atual(self):
        current_group = self.group_var.get()
        if not current_group or current_group == "Sem grupos":
            messagebox.showwarning("Aviso", "Selecione um grupo primeiro.")
            return
        personagens = D.GruposDePersonagens.get(current_group, [])
        if not personagens:
            messagebox.showinfo("Aviso", f"O grupo '{current_group}' já está vazio.")
            return
        if messagebox.askyesno("Confirmar", f"Limpar '{current_group}'?\n{len(personagens)} personagem(s) serão removidos!"):
            D.GruposDePersonagens[current_group] = []
            self.create_list_section(self.char_list_frame)

    def add_character_to_current_group(self):
        current_group = self.group_var.get()
        if current_group and current_group != "Sem grupos":
            self.add_character_with_group(current_group)
        else:
            messagebox.showwarning("Aviso", "Selecione ou crie um grupo primeiro.")

    def gerar_NPC_to_current_group(self):
        current_group = self.group_var.get()
        if current_group and current_group != "Sem grupos":
            self.gerar_NPC_with_group(current_group)
        else:
            messagebox.showwarning("Aviso", "Selecione ou crie um grupo primeiro.")

    def add_character_with_group(self, target_group):
        popup = tk.Toplevel(self)
        popup.title("Criar Novo Personagem")
        popup.geometry("400x600")
        popup.config(bg="#130f26")
        tk.Label(popup, text=f"Adicionando ao grupo: {target_group}", bg="#130f26", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        campos = ["Nome", "Nível", "Força", "Agilidade", "Vigor", "Inteligência", "Presença", "Tática", "Poder"]
        entradas = {}
        for campo in campos:
            tk.Label(popup, text=campo, bg="#130f26", fg="white", font=("Arial", 12)).pack(pady=(5, 0))
            entrada = tk.Entry(popup, font=("Arial", 12), bg="#2a1a79", fg="white", insertbackground="white")
            entrada.pack()
            entradas[campo] = entrada
        def confirmar():
            def get_int(entry, padrao=1):
                v = entry.get().strip()
                return int(v) if v else padrao
            try:
                nome = entradas["Nome"].get().strip()
                nivel = get_int(entradas["Nível"])
                proficiencias_dados = D.carregar_proficiencias()
                proficiencias_objetos = {n: CB.Proficiencia(n, d["atributo"], nivel=0) for n, d in proficiencias_dados.items()}
                novo_personagem = CB.Personagem(
                    nome, nivel,
                    get_int(entradas["Força"]), get_int(entradas["Agilidade"]),
                    get_int(entradas["Vigor"]), get_int(entradas["Inteligência"]),
                    get_int(entradas["Presença"]), get_int(entradas["Tática"]),
                    get_int(entradas["Poder"]), proficiencias_base=proficiencias_objetos
                )
                if target_group in D.GruposDePersonagens:
                    D.GruposDePersonagens[target_group].append(novo_personagem)
                popup.destroy()
                self.refresh()
            except ValueError:
                messagebox.showerror("Erro", "Preencha todos os campos corretamente!")
        tk.Button(popup, text="Confirmar", command=confirmar, bg="#411f9c", fg="white", font=("Arial", 14), width=20).pack(pady=20)

    def gerar_NPC_with_group(self, target_group):
        popup = tk.Toplevel(self); popup.title("Gerar NPC"); popup.geometry("420x420"); popup.config(bg="#130f26")
        tk.Label(popup, text=f"Adicionando ao grupo: {target_group}", bg="#130f26", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        npcs_dados = D.carregar_npcs()
        if not npcs_dados: messagebox.showerror("Erro", "Não foi possível carregar os tipos de NPCs."); popup.destroy(); return
        npcs_por_grupo = {}
        for _, npc_obj in npcs_dados.items(): grp = getattr(npc_obj, "grupo", "Sem Grupo"); npcs_por_grupo.setdefault(grp, []).append(npc_obj)
        tk.Label(popup, text="Grupo (Facção)", bg="#130f26", fg="white", font=("Arial", 12)).pack(pady=(10, 0))
        grupos_npcs = list(npcs_por_grupo.keys()); grupo_var = tk.StringVar(value=grupos_npcs[0] if grupos_npcs else "")
        grupo_menu = tk.OptionMenu(popup, grupo_var, *grupos_npcs); grupo_menu.config(bg="#1a0869", fg="white", font=("Arial", 12), width=30); grupo_menu.pack(pady=5)
        tk.Label(popup, text="Classe do NPC", bg="#130f26", fg="white", font=("Arial", 12)).pack(pady=(10, 0))
        classe_var = tk.StringVar(); classe_menu = tk.OptionMenu(popup, classe_var, ""); classe_menu.config(bg="#1a0869", fg="white", font=("Arial", 12), width=30); classe_menu.pack(pady=5)
        def atualizar_classes(*_):
            npcs_grp = npcs_por_grupo.get(grupo_var.get(), []); classes = [n.classe for n in npcs_grp]; menu = classe_menu["menu"]; menu.delete(0, "end")
            if classes: classe_var.set(classes[0]); [menu.add_command(label=c, command=lambda v=c: classe_var.set(v)) for c in classes]
            else: classe_var.set("")
        grupo_var.trace_add("write", atualizar_classes); atualizar_classes()
        tk.Label(popup, text="Nível do NPC", bg="#130f26", fg="white", font=("Arial", 12)).pack(pady=(10, 0))
        nivel_entry = tk.Entry(popup, font=("Arial", 12), width=5, justify="center", bg="#2a1a79", fg="white", insertbackground="white"); nivel_entry.insert(0, "1"); nivel_entry.pack(pady=5)
        tk.Label(popup, text="Nome do NPC (opcional)", bg="#130f26", fg="white", font=("Arial", 12)).pack(pady=(10, 0))
        nome_entry = tk.Entry(popup, font=("Arial", 12), width=25, justify="center", bg="#2a1a79", fg="white", insertbackground="white"); nome_entry.pack(pady=5)
        def confirmar():
            try:
                grupo_npc = grupo_var.get(); classe_nome = classe_var.get(); nivel = int(nivel_entry.get()); nome = nome_entry.get().strip()
                npcs_grp = npcs_por_grupo.get(grupo_npc, []); npc_base = next((n for n in npcs_grp if n.classe == classe_nome), None)
                if not npc_base: raise ValueError("Classe não encontrada no grupo.")
                proficiencias_dados = D.carregar_proficiencias(); proficiencias_objetos = {n: CB.Proficiencia(n, d["atributo"], nivel=0) for n, d in proficiencias_dados.items()}
                for nome_prof, prof in npc_base.proficiencias_base.items():
                    if nome_prof in proficiencias_objetos: proficiencias_objetos[nome_prof].nivel = prof.nivel
                    else: proficiencias_objetos[nome_prof] = CB.Proficiencia(nome_prof, prof.atributo, nivel=prof.nivel)
                npc_novo = CB.NPC(nome=nome if nome else f"{classe_nome}_{random.randint(1,50)}", nivel=nivel, classe=npc_base.classe, grupo=npc_base.grupo, Forca=npc_base.atributos["Forca"], Agilidade=npc_base.atributos["Agilidade"], Vigor=npc_base.atributos["Vigor"], Inteligencia=npc_base.atributos["Inteligencia"], Presenca=npc_base.atributos["Presenca"], Tatica=npc_base.atributos["Tatica"], Poder=npc_base.atributos["Poder"], proficiencias_base=proficiencias_objetos, poder_inicial=npc_base.poder_inicial, habilidade_inicial=npc_base.habilidade_inicial, kits=npc_base.kits, kit_fixo=npc_base.kit_fixo, resistencias_base=npc_base.resistencias_base)
                personagem = npc_novo.gerar(); personagem.preencher_recursos_ao_maximo(); target_group not in D.GruposDePersonagens and D.GruposDePersonagens.setdefault(target_group, []); D.GruposDePersonagens[target_group].append(personagem); self.refresh(); popup.destroy()
            except Exception as e: import traceback; traceback.print_exc(); messagebox.showerror("Erro", str(e))
        tk.Button(popup, text="Confirmar", command=confirmar, bg="#411f9c", fg="white", font=("Arial", 12, "bold")).pack(pady=20)

    def remove_specific_character(self, character):
        selected_group = self.group_var.get()
        if selected_group in D.GruposDePersonagens:
            try:
                D.GruposDePersonagens[selected_group].remove(character)
                self.create_list_section(self.char_list_frame)
            except ValueError:
                print("Personagem não encontrado no grupo.")
### --- Personagens --- ###

# --- Refresh --- #
    def refresh_all(self):
        self.create_group_list_section(self.group_list_frame)
        self.create_list_section(self.char_list_frame)

    def refresh(self, *args):
        self.refresh_all()
# --- Refresh --- #

    def carregar_armas_e_armaduras(self, personagem):
        for entrada in personagem.inventario.itens:
            item = entrada["item"]
            if isinstance(item, CB.Ranged):
                capacidade_restante = item.capacidade - item.munições
                if capacidade_restante <= 0:
                    continue
                for municao_entrada in personagem.inventario.itens:
                    municao = municao_entrada["item"]
                    quantidade_disponivel = municao_entrada["quantidade"]
                    if isinstance(municao, CB.Municao) and municao.calibre == item.calibre:
                        quantidade_a_carregar = min(quantidade_disponivel, capacidade_restante)
                        carregado = item.carregar_municao(municao, quantidade_a_carregar)
                        if carregado > 0:
                            personagem.inventario.remover_item(municao, carregado)
                        else:
                            print(f"Falha ao carregar {item.nome} com {municao.nome}")
                        break
        for item_dict in personagem.inventario.itens[:]:
            item = item_dict["item"]
            if hasattr(item, "regiao"):
                sucesso = personagem.equipar_do_inventario(item.regiao, item.nome)
                if not sucesso:
                    print(f"[AVISO] Não foi possível equipar {item.nome} na região {item.regiao}")

    def TelaInicial(self):
        self.controller.TelaInicial()

    def TelaDeCombate(self):
        self.controller.TelaDeCombate()

    def TelaDeRegrasEItens(self):
        self.controller.TelaDeRegrasEItens()
### TELA DE SELEÇÃO ###
### TELA DE SELEÇÃO ###
### TELA DE SELEÇÃO ###

### TELA DE DETALHES ###
### TELA DE DETALHES ###
### TELA DE DETALHES ###
class CharacterDetailsScreen(tk.Frame):
    # init e refresh #
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#130f26')

        self.proficiencia_widgets = []
        self.item_widgets         = []

        # ══ CANVAS PRINCIPAL ══
        self.main_canvas    = tk.Canvas(self, bg='#130f26', highlightthickness=0)
        self.main_scrollbar = tk.Scrollbar(self, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_main_frame = tk.Frame(self.main_canvas, bg='#130f26')
        self.canvas_window = self.main_canvas.create_window((0, 0), window=self.scrollable_main_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.main_scrollbar.set)
        self.scrollable_main_frame.bind("<Configure>", lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all")))
        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.main_scrollbar.pack(side="right", fill="y")
        self.main_scrollbar.bind("<Enter>", self._bind_mousewheel)
        self.main_scrollbar.bind("<Leave>", self._unbind_mousewheel)

        # ══ CABEÇALHO ══
        self.title_label = tk.Label(self.scrollable_main_frame, font=("Arial", 24, "bold"), bg="#1a0869", fg="white")
        self.title_label.place(x=500, y=20, width=600, height=50)
        self.btn_tela_de_selecao = tk.Button(self.scrollable_main_frame, text="Seleção", bg="#1a0869", fg="white", font=("Arial", 18), command=self.controller.TelaDeSelecao)
        self.btn_tela_de_selecao.place(x=50, y=20, width=200, height=50)
        self.btn_tela_de_combate = tk.Button(self.scrollable_main_frame, text="Tela de Combate", bg="#1a0869", fg="white", font=("Arial", 18), command=self.controller.TelaDeCombate)
        self.btn_tela_de_combate.place(x=1350, y=20, width=200, height=50)
        
        tk.Button(self.scrollable_main_frame, text="Rolagem", bg="#1a0869", fg="white",font=("Arial", 18), command=self._abrir_popup_rolagem).place(x=1150, y=20, width=160, height=50)
        tk.Button(self.scrollable_main_frame, text="Loot", bg="#1a0869", fg="white",font=("Arial", 18),command=lambda: abrir_popup_loot(self, self.character, D, on_finish=self.refresh)).place(x=290, y=20, width=160, height=50)
        
        # ══ STATS & ATRIBUTOS ══ #
        self.frame_stats_unificado = tk.Frame(self.scrollable_main_frame, bg='#1a0869', bd=2)
        self.frame_stats_unificado.place(x=50, y=100, width=300, height=750)
        tk.Label(self.frame_stats_unificado, text="Status do Personagem", font=("Arial", 18, "bold"), bg="#1a0869", fg="white").pack(pady=(10, 15))

        # ── Canvas scrollável interno ── #
        self._stats_canvas = tk.Canvas(self.frame_stats_unificado, bg='#1a0869', highlightthickness=0)
        self._stats_inner  = tk.Frame(self._stats_canvas, bg='#1a0869')
        self._stats_canvas_window = self._stats_canvas.create_window((0, 0), window=self._stats_inner, anchor="nw")
        self._stats_inner.bind("<Configure>", lambda e: self._stats_canvas.configure(scrollregion=self._stats_canvas.bbox("all")))
        self._stats_canvas.bind("<Configure>", lambda e: self._stats_canvas.itemconfig(self._stats_canvas_window, width=e.width))  # <-- isso
        self._stats_canvas.pack(fill="both", expand=True)
        self._stats_canvas.bind("<Enter>", lambda e: self._stats_canvas.bind_all("<MouseWheel>", lambda ev: self._stats_canvas.yview_scroll(int(ev.delta / -90), "units")))
        self._stats_canvas.bind("<Leave>", lambda e: self._stats_canvas.unbind_all("<MouseWheel>"))
        # ── Canvas scrollável interno ── #

        # ── Recursos ── #
        frame_recursos = tk.Frame(self._stats_inner, bg='#2a1a79', bd=2, relief='flat')
        frame_recursos.pack(pady=10, padx=10, fill="x")
        self.label_vida = tk.Label(frame_recursos, text="Vida", bg='#2a1a79', fg="white", font=("Arial", 12, "bold"))
        self.label_vida.pack(anchor="w", padx=10)
        self.barra_vida = tk.Canvas(frame_recursos, height=20, bg="#111111", highlightthickness=0, cursor="hand2")
        self.barra_vida.pack(fill="x", padx=10, pady=3)
        self.barra_vida.bind("<Button-1>",  lambda e: self.setar_barra_por_clique("VidaAtual", "VidaMax", e))
        self.barra_vida.bind("<B1-Motion>", lambda e: self.setar_barra_por_clique("VidaAtual", "VidaMax", e))
        self.label_energia = tk.Label(frame_recursos, text="Energia", bg='#2a1a79', fg="white", font=("Arial", 12, "bold"))
        self.label_energia.pack(anchor="w", padx=10)
        self.barra_energia = tk.Canvas(frame_recursos, height=20, bg="#111111", highlightthickness=0, cursor="hand2")
        self.barra_energia.pack(fill="x", padx=10, pady=3)
        self.barra_energia.bind("<Button-1>",  lambda e: self.setar_barra_por_clique("EnergiaAtual", "EnergiaMax", e))
        self.barra_energia.bind("<B1-Motion>", lambda e: self.setar_barra_por_clique("EnergiaAtual", "EnergiaMax", e))
        self.label_mana = tk.Label(frame_recursos, text="Mana", bg='#2a1a79', fg="white", font=("Arial", 12, "bold"))
        self.label_mana.pack(anchor="w", padx=10)
        self.barra_mana = tk.Canvas(frame_recursos, height=20, bg="#111111", highlightthickness=0, cursor="hand2")
        self.barra_mana.pack(fill="x", padx=10, pady=3)
        self.barra_mana.bind("<Button-1>",  lambda e: self.setar_barra_por_clique("ManaAtual", "ManaMax", e))
        self.barra_mana.bind("<B1-Motion>", lambda e: self.setar_barra_por_clique("ManaAtual", "ManaMax", e))
        # ── Recursos ── #
        # ── Progressão ── #
        frame_prog = tk.Frame(self._stats_inner, bg='#2a1a79', bd=2, relief='flat')
        frame_prog.pack(pady=10, padx=10, fill="x")
        frame_nivel_row = tk.Frame(frame_prog, bg='#2a1a79')
        frame_nivel_row.pack(pady=(4, 2))
        tk.Button(frame_nivel_row, text="-", font=("Arial", 10), bg="#8c1d1d", fg="white", width=2,command=lambda: [self.character.modificar_nivel(-1), self.refresh()]).pack(side="left", padx=4)
        self.label_nivel = tk.Label(frame_nivel_row, bg='#2a1a79', fg="white", font=("Arial", 14, "bold"), width=12)
        self.label_nivel.pack(side="left")
        tk.Button(frame_nivel_row, text="+", font=("Arial", 10), bg="#115c11", fg="white", width=2,command=lambda: [self.character.modificar_nivel(1), self.refresh()]).pack(side="left", padx=4)
        self.barra_xp = tk.Canvas(frame_prog, height=20, bg="#111111", highlightthickness=0, cursor="hand2")
        self.barra_xp.pack(fill="x", padx=10, pady=5)
        self.barra_xp.bind("<Button-1>",  lambda e: self.setar_barra_por_clique("XPAtual", "XPlvlUp", e))
        self.barra_xp.bind("<B1-Motion>", lambda e: self.setar_barra_por_clique("XPAtual", "XPlvlUp", e))
        # ── Progressão ── #
        # ── Defesas & Movimento ── #
        frame_def = tk.Frame(self._stats_inner, bg='#2a1a79', bd=2, relief='flat')
        frame_def.pack(pady=10, padx=10, fill="x")

        self.label_bloqueio  = tk.Frame(frame_def, bg='#2a1a79'); self.label_bloqueio.pack(pady=2, fill="x", padx=6)
        self.label_esquiva   = tk.Frame(frame_def, bg='#2a1a79'); self.label_esquiva.pack(pady=2, fill="x", padx=6)
        self.label_percepcao = tk.Frame(frame_def, bg='#2a1a79'); self.label_percepcao.pack(pady=2, fill="x", padx=6)
        self.label_movimento = tk.Frame(frame_def, bg='#2a1a79'); self.label_movimento.pack(pady=2, fill="x", padx=6)
        self.label_disparada = tk.Frame(frame_def, bg='#2a1a79'); self.label_disparada.pack(pady=2, fill="x", padx=6)

        self.label_carga_status = tk.Label(frame_def, bg='#2a1a79', fg="white", font=("Arial", 11, "bold"), anchor="w", wraplength=260)
        self.label_carga_status.pack(pady=2, fill="x", padx=6)
        # ── Defesas & Movimento ── #
        # ── Atributos ── #
        frame_atributos_container = tk.Frame(self._stats_inner, bg='#2a1a79', bd=2, relief='flat')
        frame_atributos_container.pack(pady=10, padx=10, fill="x")
        tk.Label(frame_atributos_container, text="Atributos", bg='#2a1a79', fg="white", font=("Arial", 14, "bold")).pack(pady=5)
        self.frame_atributos = tk.Frame(frame_atributos_container, bg='#2a1a79')
        self.frame_atributos.pack(pady=(0, 8), padx=5, fill="x")
        self.atributo_frames = {}
        # ── Atributos ── #
        # ══ STATS & ATRIBUTOS ══ #

        # ══ INVENTÁRIO ══ #
        self.frame_inventario = tk.Frame(self.scrollable_main_frame, bg='#1a0869')
        self.frame_inventario.place(x=395, y=100, width=350, height=370)
        self.header_inventario = tk.Frame(self.frame_inventario, bg="#1a0869")
        self.header_inventario.pack(pady=(10, 5), fill="x", padx=10)
        self.label_inventario_title = tk.Label(self.header_inventario, text="Inventário", font=("Arial", 16, "bold"), bg="#1a0869", fg="white")
        self.label_inventario_title.pack(side="left")
        self.btn_adicionar_item = tk.Button(self.header_inventario, text="Adicionar Item", command=lambda: abrir_popup_adicionar_item(self, self.character, on_finish=self.refresh), bg="#1a0869", fg="white", font=("Arial", 12))
        self.btn_adicionar_item.pack(side="right", padx=(10, 0))
        self.container_scroll_inventario = tk.Frame(self.frame_inventario, bg='#130f26')
        self.container_scroll_inventario.pack(fill="both", expand=True, padx=10, pady=(5,10))
        self.canvas_inventario = tk.Canvas(self.container_scroll_inventario, bg='#1a0869', highlightthickness=0)
        self.scrollable_frame_inventario = tk.Frame(self.canvas_inventario, bg='#1a0869')
        self.scrollable_frame_inventario.bind("<Configure>", lambda e: self.canvas_inventario.configure(scrollregion=self.canvas_inventario.bbox("all")))
        self.canvas_inventario.create_window((0, 0), window=self.scrollable_frame_inventario, anchor="nw")
        self.canvas_inventario.pack(fill="both", expand=True)
        self.canvas_inventario.bind("<Enter>", lambda e: self.canvas_inventario.bind_all("<MouseWheel>", lambda ev: self.canvas_inventario.yview_scroll(int(ev.delta/-90), "units")))
        self.canvas_inventario.bind("<Leave>", lambda e: self.canvas_inventario.unbind_all("<MouseWheel>"))

        # ══ EQUIPADOS ══ #
        self.frame_equipados = tk.Frame(self.scrollable_main_frame, bg='#1a0869')
        self.frame_equipados.place(x=395, y=475, width=350, height=370)
        header_equipados = tk.Frame(self.frame_equipados, bg="#1a0869"); header_equipados.pack(pady=(10, 5), fill="x", padx=10)
        tk.Label(header_equipados, text="Equipados", font=("Arial", 16, "bold"), bg="#1a0869", fg="white").pack(side="left")
        self.container_scroll_equipados = tk.Frame(self.frame_equipados, bg='#130f26')
        self.container_scroll_equipados.pack(fill="both", expand=True, padx=10, pady=(5,10))
        self.canvas_equipados = tk.Canvas(self.container_scroll_equipados, bg='#1a0869', highlightthickness=0)
        self.frame_lista_equipados = tk.Frame(self.canvas_equipados, bg='#1a0869')
        self.frame_lista_equipados.bind("<Configure>", lambda e: self.canvas_equipados.configure(scrollregion=self.canvas_equipados.bbox("all")))
        self.canvas_equipados.create_window((0, 0), window=self.frame_lista_equipados, anchor="nw")
        self.canvas_equipados.pack(fill="both", expand=True)
        self.canvas_equipados.bind("<Enter>", lambda e: self.canvas_equipados.bind_all("<MouseWheel>", lambda ev: self.canvas_equipados.yview_scroll(int(ev.delta/-90), "units")))
        self.canvas_equipados.bind("<Leave>", lambda e: self.canvas_equipados.unbind_all("<MouseWheel>"))

        # ══ BUFFS / DEBUFFS ══ #
        self.frame_efeitos = tk.Frame(self.scrollable_main_frame, bg='#1a0869')
        self.frame_efeitos.place(x=770, y=100, width=350, height=370)
        header_efeitos = tk.Frame(self.frame_efeitos, bg="#1a0869"); header_efeitos.pack(pady=(10,5), fill="x", padx=10)
        tk.Label(header_efeitos, text="Buffs/Debuffs", font=("Arial",16,"bold"), bg="#1a0869", fg="white").pack(side="left")
        self.btn_adicionar_efeito = tk.Button(header_efeitos, text="Adicionar Efeito", command=lambda:self.abrir_popup_efeito(), bg="#1a0869", fg="white", font=("Arial",12))
        self.btn_adicionar_efeito.pack(side="right", padx=(10,0))
        self.container_scroll_efeitos = tk.Frame(self.frame_efeitos, bg='#130f26')
        self.container_scroll_efeitos.pack(fill="both", expand=True, padx=10, pady=(5,10))
        self.canvas_efeitos = tk.Canvas(self.container_scroll_efeitos, bg='#1a0869', highlightthickness=0)
        self.scrollable_frame_efeitos = tk.Frame(self.canvas_efeitos, bg='#1a0869')
        self.scrollable_frame_efeitos.bind("<Configure>", lambda e:self.canvas_efeitos.configure(scrollregion=self.canvas_efeitos.bbox("all")))
        self.canvas_efeitos.create_window((0,0), window=self.scrollable_frame_efeitos, anchor="nw")
        self.canvas_efeitos.pack(fill="both", expand=True)
        self.canvas_efeitos.bind("<Enter>", lambda e:self.canvas_efeitos.bind_all("<MouseWheel>", lambda ev:self.canvas_efeitos.yview_scroll(int(ev.delta/-90),"units")))
        self.canvas_efeitos.bind("<Leave>", lambda e:self.canvas_efeitos.unbind_all("<MouseWheel>"))

        # ══ HABILIDADES ══ #
        self.frame_habilidades = tk.Frame(self.scrollable_main_frame, bg='#1a0869')
        self.frame_habilidades.place(x=770, y=475, width=350, height=370)
        header_habilidades = tk.Frame(self.frame_habilidades, bg="#1a0869")
        header_habilidades.pack(pady=(10,5), fill="x", padx=10)
        tk.Label(header_habilidades, text="Habilidades/Poderes", font=("Arial",16,"bold"), bg="#1a0869", fg="white").pack(side="left")
        self.btn_adicionar_habilidade = tk.Button(header_habilidades, text="Adicionar",command=lambda: self.abrir_popup_habilidade(None, "habilidade"),bg="#1a0869", fg="white", font=("Arial",12))
        self.btn_adicionar_habilidade.pack(side="right", padx=(10,0))
        self.container_scroll_habilidades = tk.Frame(self.frame_habilidades, bg='#130f26')
        self.container_scroll_habilidades.pack(fill="both", expand=True, padx=10, pady=(5,10))
        self.canvas_habilidades = tk.Canvas(self.container_scroll_habilidades, bg='#1a0869', highlightthickness=0)
        self._scrollbar_habilidades = tk.Scrollbar(self.container_scroll_habilidades, orient="vertical", command=self.canvas_habilidades.yview)
        self.canvas_habilidades.configure(yscrollcommand=self._scrollbar_habilidades.set)
        self.scrollable_frame_habilidades = tk.Frame(self.canvas_habilidades, bg='#1a0869')
        self._win_habilidades = self.canvas_habilidades.create_window((0,0), window=self.scrollable_frame_habilidades, anchor="nw")
        self.scrollable_frame_habilidades.bind("<Configure>",lambda e: self.canvas_habilidades.configure(scrollregion=self.canvas_habilidades.bbox("all")))
        self.canvas_habilidades.bind("<Configure>",lambda e: self.canvas_habilidades.itemconfig(self._win_habilidades, width=e.width))
        self.canvas_habilidades.pack(side="left", fill="both", expand=True)
        self._scrollbar_habilidades.pack(side="right", fill="y")
        self.canvas_habilidades.bind("<Enter>", lambda e: self.canvas_habilidades.bind_all("<MouseWheel>", lambda ev: self.canvas_habilidades.yview_scroll(int(ev.delta / -90), "units")))
        self.canvas_habilidades.bind("<Leave>", lambda e: self.canvas_habilidades.unbind_all("<MouseWheel>"))

        # ══ PROFICIÊNCIAS ══
        self.frame_proficiencias = tk.Frame(self.scrollable_main_frame, bg='#1a0869')
        self.frame_proficiencias.place(x=1160, y=100, width=390, height=750)
        header_prof = tk.Frame(self.frame_proficiencias, bg="#1a0869"); header_prof.pack(pady=(10, 5), fill="x", padx=10)
        tk.Label(header_prof, text="Proficiências", font=("Arial", 16, "bold"), bg="#1a0869", fg="white").pack(side="left")
        self.container_scroll_prof = tk.Frame(self.frame_proficiencias, bg='#130f26')
        self.container_scroll_prof.pack(fill="both", expand=True, padx=10, pady=(5,10))
        self.canvas_prof = tk.Canvas(self.container_scroll_prof, bg='#1a0869', highlightthickness=0, width=380, height=850)
        self.scrollable_frame_prof = tk.Frame(self.canvas_prof, bg='#1a0869')
        self.scrollable_frame_prof.bind("<Configure>", lambda e: self.canvas_prof.configure(scrollregion=self.canvas_prof.bbox("all")))
        self.canvas_prof.create_window((5, 0), window=self.scrollable_frame_prof, anchor="nw")
        self.canvas_prof.pack(side="left")
        self.canvas_prof.bind("<Enter>", lambda e: self.canvas_prof.bind_all("<MouseWheel>", lambda ev: self.canvas_prof.yview_scroll(int(ev.delta/-90), "units")))
        self.canvas_prof.bind("<Leave>", lambda e: self.canvas_prof.unbind_all("<MouseWheel>"))

        self.scrollable_main_frame.configure(width=2000, height=1300)
    
    def _bind_mousewheel(self, event):
        self.main_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        self.main_canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def refresh_info_basica(self):
        try:
            self.character.calcular_peso_total()
            self.title_label.config(text=f"Detalhes de {self.character.nome}")

            # ===== FUNÇÃO PADRÃO DE BARRA ===== #
            def atualizar_barra(canvas,atual,maximo,cor,altura=18,texto_extra=""):
                canvas.delete("all")
                largura=canvas.winfo_width()
                if largura<=1: largura=400
                proporcao=0 if maximo==0 else atual/maximo
                if proporcao<0: proporcao=0
                if proporcao>1: proporcao=1
                preenchido=int(largura*proporcao)
                canvas.create_rectangle(0,0,preenchido,altura,fill=cor,width=0)
                canvas.create_text(largura//2,altura//2,text=f"{atual}/{maximo}{texto_extra}",fill="white",font=("Arial",9,"bold"))

            # ===== RECURSOS ===== #
            atualizar_barra(self.barra_vida,self.character.VidaAtual,self.character.VidaMax,"#b22222",20)
            atualizar_barra(self.barra_energia,self.character.EnergiaAtual,self.character.EnergiaMax,"#1e90ff",20)
            atualizar_barra(self.barra_mana,self.character.ManaAtual,self.character.ManaMax,"#7b3fe4",20)

            # ===== PROGRESSÃO ===== #
            self.label_nivel.config(text=f"Nível: {self.character.Nivel}")
            atualizar_barra(self.barra_xp,self.character.XPAtual,self.character.XPlvlUp,"#f1c40f",20," XP")

            # ===== DEFESAS BASE + BONUS ===== #
            def linha_status(label_frame, atributo, nome_exibicao=None, sufixo=""):
                base, bonus_prof, mod, final = self.character.breakdown(atributo)
                nome = nome_exibicao if nome_exibicao else atributo.capitalize()
                atributo_lower = atributo.lower()

                # Coleta fontes de mod (buffs/debuffs/poderes/habilidades)
                fontes_mod = []
                for efeito in self.character.buffs_debuffs.listar_efeitos():
                    for entrada in efeito.efeito:
                        tags = entrada.get("tags", []) if isinstance(entrada, dict) else []
                        if atributo_lower in [t.lower() for t in tags]:
                            fontes_mod.append((efeito.nome, entrada.get("valor", 0), "buff"))

                for hab in self.character.habilidades.listar_habilidades():
                    tags = hab.tags if isinstance(hab.tags, list) else [hab.tags]
                    vals = hab.valor if isinstance(hab.valor, list) else [hab.valor] * len(tags)
                    for t, v in zip(tags, vals):
                        if t.lower() == atributo_lower:
                            fontes_mod.append((hab.nome, v, "hab"))

                for poder in self.character.poderes.listar_poderes():
                    tags = poder.tags if isinstance(poder.tags, list) else [poder.tags]
                    vals = poder.valor if isinstance(poder.valor, list) else [poder.valor] * len(tags)
                    for t, v in zip(tags, vals):
                        if t.lower() == atributo_lower:
                            fontes_mod.append((poder.nome, v, "poder"))

                # Monta qual proficiência dá o bonus_prof
                prof_map = {
                    "bloqueio":"Luta",
                    "esquiva":"Reflexo",
                    "percepcao":"Percepção",
                    "movimento":"Atletismo",
                    "disparada":"Atletismo",
                    "vida":"Vitalidade",
                    "mana":"Mana",
                    "carga":"Carga"
                }
                nome_prof = prof_map.get(atributo_lower, "")
                nivel_prof = self.character.proficiencias.obter_proficiencias(nome_prof).get(nome_prof, 0) if nome_prof else 0

                # Limpa o frame antes de redesenhar
                for widget in label_frame.winfo_children():
                    widget.destroy()

                FG = "white"
                BG = label_frame.cget("bg")

                # ── Nome ──
                tk.Label(label_frame, text=f"{nome}", bg=BG, fg=FG,
                        font=("Arial", 10, "bold")).pack(side="left")

                # ── Base ──
                tk.Label(label_frame, text=f"  {base}", bg=BG, fg="#aaaaaa",
                        font=("Arial", 10)).pack(side="left")

                # ── Bônus de Proficiência ──
                if bonus_prof != 0:
                    sinal = "+" if bonus_prof >= 0 else ""
                    lbl_prof = tk.Label(label_frame, text=f"  {sinal}{bonus_prof}",bg=BG, fg="#7ec8e3", font=("Arial", 10, "bold"),cursor="hand2")
                    lbl_prof.pack(side="left")
                    tip_prof = f"Proficiência: {nome_prof} (nível {nivel_prof})"
                    if atributo_lower in ("bloqueio", "esquiva"):tip_prof += f"\n({nome_prof} // 2 = {bonus_prof})"
                    Tooltip(lbl_prof, tip_prof)

                # ── Bônus de Efeitos ──
                if mod != 0:
                    sinal = "+" if mod >= 0 else ""
                    lbl_mod = tk.Label(label_frame, text=f"  {sinal}{mod}",bg=BG, fg="#f0a500", font=("Arial", 10, "bold"),cursor="hand2")
                    lbl_mod.pack(side="left")
                    linhas = []
                    for nome_fonte, valor, tipo in fontes_mod:
                        icone = {"buff": "⚡", "hab": "⚔️", "poder": "🔮"}.get(tipo, "•")
                        s = "+" if valor >= 0 else ""
                        linhas.append(f"{icone} {nome_fonte}: {s}{valor}")
                    Tooltip(lbl_mod, "\n".join(linhas) if linhas else "Efeitos ativos")

                # ── Total ──
                tk.Label(label_frame, text=f"  = {final}{sufixo}", bg=BG, fg=FG,
                        font=("Arial", 10, "bold")).pack(side="left")

            linha_status(self.label_bloqueio,"bloqueio","Bloqueio")
            linha_status(self.label_esquiva,"esquiva","Esquiva")
            linha_status(self.label_percepcao,"percepcao","Percepção")

            linha_status(self.label_movimento,"movimento","Movimento","m")
            linha_status(self.label_disparada,"disparada","Disparada","m")

            # ===== CARGA ===== #
            atual=self.character.CargaAtual
            maximo=self.character.CargaMax
            sobrecarregado=atual>maximo
            cor="#ff4444" if sobrecarregado else "white"
            texto=f"Carga: {atual}/{maximo}"
            if sobrecarregado: texto+="  ⚠ SOBRECARGA"
            self.label_carga_status.config(text=texto,fg=cor)

        except Exception as e:
            print("Erro no refresh:",e)

    def refresh_atributos(self):
        try:
            for frame in self.atributo_frames.values(): frame.destroy()
            self.atributo_frames.clear()

            atributos=[("Força","Forca"),("Agilidade","Agilidade"),("Vigor","Vigor"),("Inteligência","Inteligencia"),("Presença","Presenca"),("Tática","Tatica"),("Poder","Poder")]

            for i,(nome_visivel,nome_real) in enumerate(atributos):
                frame=tk.Frame(self.frame_atributos,bg='#2a1a79')
                frame.grid(row=i,column=0,padx=10,pady=4,sticky="w")
                self.atributo_frames[nome_real]=frame

                valor=getattr(self.character,nome_real)

                tk.Label(frame,text=f"{nome_visivel}:",bg='#2a1a79',fg="white",font=("Arial",12,"bold"),width=12,anchor="w").pack(side="left")
                tk.Label(frame,text=str(valor),bg='#2a1a79',fg="white",font=("Arial",12),width=3).pack(side="left",padx=(0,6))
                tk.Button(frame,text="-",command=lambda nr=nome_real:self.alterar_atributo(nr,-1),bg="#8c1d1d",fg="white",font=("Arial",10),width=2).pack(side="left",padx=2)
                tk.Button(frame,text="+",command=lambda nr=nome_real:self.alterar_atributo(nr,1),bg="#115c11",fg="white",font=("Arial",10),width=2).pack(side="left")

            self.frame_atributos.grid_columnconfigure(0,weight=1)

        except Exception as e:
            print("Erro no refresh atributos:",e)

    def refresh_resistencias(self):
        """Seção de resistências NATURAIS (base) - resumo compacto com popup de edição"""
        if hasattr(self, "_frame_res") and self._frame_res.winfo_exists(): self._frame_res.destroy()
        self._frame_res = tk.Frame(self._stats_inner, bg='#2a1a79', bd=2, relief='flat'); self._frame_res.pack(pady=10, padx=10, fill="x")
        tk.Label(self._frame_res, text="Resistências Naturais (Base)", bg='#2a1a79', fg="white", font=("Arial", 13, "bold")).pack(pady=(6, 4))
        c = self.character
        def abrir_popup_resistencia(tipo, valor_atual):
            popup = tk.Toplevel(self); popup.title(f"Editar {tipo.capitalize()}"); popup.geometry("300x150"); popup.configure(bg="#1a0869"); popup.resizable(False, False)
            tk.Label(popup, text=f"{tipo.capitalize()}", font=("Arial", 14, "bold"), bg="#1a0869", fg="white").pack(pady=10)
            frame_edit = tk.Frame(popup, bg="#1a0869"); frame_edit.pack(pady=10)
            tk.Label(frame_edit, text="Valor:", bg="#1a0869", fg="white").pack(side="left", padx=5)
            entry = tk.Entry(frame_edit, width=10, font=("Arial", 12), justify="center"); entry.insert(0, f"{valor_atual:+d}"); entry.pack(side="left", padx=5)
            def salvar(): 
                try: novo = int(entry.get()); c.resistencias_base[tipo] = max(-100, min(100, novo)); self.refresh_resistencias(); self.refresh_modificadores(); popup.destroy()
                except: entry.delete(0, tk.END); entry.insert(0, f"{valor_atual:+d}")
            tk.Button(popup, text="Salvar", command=salvar, bg="#115c11", fg="white", font=("Arial", 11), width=20).pack(pady=10)
            entry.focus_set(); entry.select_range(0, tk.END)
        frame_res = tk.Frame(self._frame_res, bg='#2a1a79'); frame_res.pack(fill="x", padx=4, pady=4)
        for tipo in sorted(c.resistencias_base.keys()):
            base = c.resistencias_base[tipo]
            if base >= 100: label_txt = f"{tipo.capitalize()}: Imune"; cor = "#4ae34a"
            elif base > 0: label_txt = f"{tipo.capitalize()}: {base}% de resistência"; cor = "#3eb6e6"
            elif base < 0: label_txt = f"{tipo.capitalize()}: {abs(base)}% de vulnerabilidade"; cor = "#f05a5a"
            else: label_txt = f"{tipo.capitalize()}: Normal"; cor = "#ffffff"
            btn = tk.Button(frame_res, text=label_txt, bg="#2a1a79", fg=cor, font=("Arial", 10, "bold"), relief="raised", anchor="w", command=lambda t=tipo, v=base: abrir_popup_resistencia(t, v))
            btn.pack(fill="x", pady=3)

    def refresh_modificadores(self):
        if hasattr(self, "_frame_mods") and self._frame_mods.winfo_exists(): self._frame_mods.destroy()
        self._frame_mods = tk.Frame(self._stats_inner, bg='#2a1a79', bd=2, relief='flat'); self._frame_mods.pack(pady=10, padx=10, fill="x")
        tk.Label(self._frame_mods, text="Modificações Ativas (Efeitos)", bg='#2a1a79', fg="white", font=("Arial", 13, "bold")).pack(pady=(6, 4))
        c = self.character
        testes_combinados = {}
        for k in set(list(c.bonus_testes.keys()) + list(c.mod_testes.keys())):
            total = c.bonus_testes.get(k, 0) + c.mod_testes.get(k, 0)
            if total != 0: testes_combinados[k] = total
        if testes_combinados:
            btn_testes = tk.Label(self._frame_mods, text=f"🎲 Testes ({len(testes_combinados)})", bg='#1a3060', fg="white", font=("Arial", 11, "bold"), cursor="hand2", relief="flat", padx=6, pady=3)
            btn_testes.pack(fill="x", padx=8, pady=2)
            txt = "\n".join(f"  {k.capitalize()}: {'+' if v > 0 else ''}{v}" for k, v in sorted(testes_combinados.items()))
            Tooltip(btn_testes, txt)
        atribs_ativos = {k: v for k, v in c.bonus_atributos.items() if v != 0}
        if atribs_ativos:
            btn_atribs = tk.Label(self._frame_mods, text=f"⚡ Atributos ({len(atribs_ativos)})", bg='#1a3060', fg="white", font=("Arial", 11, "bold"), cursor="hand2", relief="flat", padx=6, pady=3)
            btn_atribs.pack(fill="x", padx=8, pady=2)
            txt = "\n".join(f"  {k.capitalize()}: {'+' if v > 0 else ''}{v}" for k, v in sorted(atribs_ativos.items()))
            Tooltip(btn_atribs, txt)
        efeitos_ativos = {k: v for k, v in c.mod_efeitos.items() if v != 0}
        if efeitos_ativos:
            btn_ef = tk.Label(self._frame_mods, text=f"✨ Efeitos ({len(efeitos_ativos)})", bg='#1a3060', fg="white", font=("Arial", 11, "bold"), cursor="hand2", relief="flat", padx=6, pady=3)
            btn_ef.pack(fill="x", padx=8, pady=2)
            txt = "\n".join(f"  {k.capitalize()}: {'+' if v > 0 else ''}{v}" for k, v in sorted(efeitos_ativos.items()))
            Tooltip(btn_ef, txt)
        res_mod_ativos = {k: v for k, v in c.resistencias_mod.items() if v != 0}
        if res_mod_ativos:
            btn_res = tk.Label(self._frame_mods, text=f"🛡️ Resistências ({len(res_mod_ativos)})", bg='#1a4060', fg="#7ec8e3", font=("Arial", 11, "bold"), cursor="hand2", relief="flat", padx=6, pady=3)
            btn_res.pack(fill="x", padx=8, pady=2)
            txt = "\n".join(f"  {k.capitalize()}: {'+' if v > 0 else ''}{v}%" for k, v in sorted(res_mod_ativos.items()))
            Tooltip(btn_res, txt)
        imun_mod_ativas = [t for t in c.imunidades_mod]
        if imun_mod_ativas:
            btn_imun = tk.Label(self._frame_mods, text=f"⚪ Imunidades ({len(imun_mod_ativas)})", bg='#1a4a2a', fg="#4ae34a", font=("Arial", 11, "bold"), cursor="hand2", relief="flat", padx=6, pady=3)
            btn_imun.pack(fill="x", padx=8, pady=2)
            txt = "\n".join(f"  {i.capitalize()}" for i in sorted(imun_mod_ativas))
            Tooltip(btn_imun, txt)
        if not any([testes_combinados, atribs_ativos, efeitos_ativos, res_mod_ativos, imun_mod_ativas]):
            tk.Label(self._frame_mods, text="Nenhuma modificação ativa", bg='#2a1a79', fg="#888888", font=("Arial", 10, "italic")).pack(pady=4)

    def refresh_proficiencias(self):
        try:
            scroll_pos = self.canvas_prof.yview()[0]

            for widget in self.proficiencia_widgets:
                widget.destroy()
            self.proficiencia_widgets.clear()

            profs_por_atributo = {}
            for prof in self.character.proficiencias.proficiencias.values():
                profs_por_atributo.setdefault(prof.atributo, []).append(prof)

            ordem_atributos = ["Força", "Agilidade", "Vigor", "Inteligência", "Presença", "Tática", "Poder"]

            for atributo in ordem_atributos:
                if atributo not in profs_por_atributo:
                    continue

                titulo = tk.Label(self.scrollable_frame_prof, text=atributo, bg="#120447", fg="white", font=("Arial", 14, "bold"), anchor="w")
                titulo.pack(fill="x", padx=4, pady=(8, 4))
                self.proficiencia_widgets.append(titulo)

                for prof in profs_por_atributo[atributo]:
                    frame = tk.Frame(self.scrollable_frame_prof, bg="#1a0869", pady=2)
                    frame.pack(fill="x", padx=2, pady=2)

                    tk.Label(frame, text=f"{prof.nome}: {prof.nivel}", bg="#2a0d89", fg="white", font=("Arial", 13), width=30, anchor="w").pack(side="left", padx=2)
                    tk.Button(frame, text="-", font=("Arial", 8), bg="#2a0d89", fg="white", width=4, command=lambda p=prof: self.decrementar_proficiencia(p)).pack(side="left", padx=5)
                    tk.Button(frame, text="+", font=("Arial", 8), bg="#2a0d89", fg="white", width=4, command=lambda p=prof: self.incrementar_proficiencia(p)).pack(side="left", padx=5)

                    self.proficiencia_widgets.append(frame)

            self.canvas_prof.update_idletasks()
            self.canvas_prof.yview_moveto(scroll_pos)

        except Exception as e:
            print("Erro no refresh das proficiências:", e)

    def refresh_inventario(self):
        """Atualiza a seção de inventário com menu direto no botão do item"""
        try:
            if not self.character: return
            for widget in self.scrollable_frame_inventario.winfo_children():
                widget.destroy()
            self.item_widgets.clear()

            def atualizar():
                self.refresh_inventario()
                self.refresh_info_basica()

            def _eh_item_complexo(item_obj):
                return isinstance(
                    item_obj,
                    (CB.Melee, CB.Ranged, CB.Municao, CB.Equipamento, CB.Melhoria)
                ) or self.character._eh_protecao(item_obj) or isinstance(item_obj, CB.Consumivel)

            def _eh_consumivel_area(item_obj):
                if not isinstance(item_obj, CB.Consumivel):
                    return False

                # Formato antigo: raio no próprio objeto
                if getattr(item_obj, "raio", None):
                    return True

                # Campo 'uso' indica arremesso ou detonação
                uso = str(getattr(item_obj, "uso", "")).lower()
                if any(k in uso for k in ("arremess", "detonac", "detonaç", "area", "área")):
                    return True

                # Novo formato: efeito dano_area na lista de efeitos
                for ef in getattr(item_obj, "efeitos", []):
                    if isinstance(ef, dict) and ef.get("tipo") == "dano_area":
                        return True

                return False

            for i in self.character.inventario.listar_itens():
                item_obj  = i["objeto"]
                item_nome = i["nome"]
                quantidade = i["quantidade"]

                texto_item = f"{item_nome}  (x{quantidade})" if quantidade > 1 else item_nome

                frame_item = tk.Frame(
                    self.scrollable_frame_inventario,
                    bg="#1a0869", width=300, height=30
                )
                frame_item.pack(fill='x', padx=10, pady=4)
                frame_item.pack_propagate(False)

                btn_item = tk.Button(
                    frame_item,
                    text=texto_item,
                    bg="#2a0d89", fg="white",
                    font=("Arial", 12),
                    anchor='w', relief=tk.FLAT,
                    borderwidth=0, highlightthickness=0
                )
                btn_item.pack(fill='x', ipady=4, ipadx=10)

                Tooltip(btn_item, self._gerar_texto_tooltip_item(item_obj))

                # Shift+Clique → popup de detalhes para itens complexos
                if _eh_item_complexo(item_obj):
                    btn_item.bind(
                        "<Shift-Button-1>",
                        lambda e, i=item_obj: self.mostrar_popup_detalhes_item(i)
                    )

                menu = tk.Menu(btn_item, tearoff=0)

                # ── Armas / Proteções / Equipamentos ─────────────────────────
                if isinstance(item_obj, (CB.Melee, CB.Ranged)) \
                        or self.character._eh_protecao(item_obj) \
                        or isinstance(item_obj, CB.Equipamento):
                    menu.add_command(
                        label="Equipar Direto",
                        command=lambda i=item_obj: [self._equipar_item(i), atualizar()]
                    )
                    menu.add_command(
                        label="Equipar Popup",
                        command=lambda i=item_obj: self.abrir_popup_escolher_slot(i)
                    )
                    if isinstance(item_obj, CB.Ranged):
                        menu.add_command(
                            label="Carregar",
                            command=lambda i=item_obj: self.carregar_municao_ranged(i)
                        )
                        menu.add_command(
                            label="Descarregar",
                            command=lambda i=item_obj: [
                                self.descarregar_municao_ranged(i), atualizar()
                            ]
                        )
                        if len(item_obj.acoes_disparo) > 1:
                            menu.add_command(
                                label=f"Trocar Modo ({item_obj.modo_disparo_atual})",
                                command=lambda i=item_obj: [i.trocar_modo_disparo(), atualizar()]
                            )
                    menu.add_separator()

                # ── Detalhes ──────────────────────────────────────────────────
                if _eh_item_complexo(item_obj):
                    menu.add_command(
                        label="Ver detalhes completos",
                        command=lambda i=item_obj: self.mostrar_popup_detalhes_item(i)
                    )
                    menu.add_separator()

                # ── Consumíveis ───────────────────────────────────────────────
                if isinstance(item_obj, CB.Consumivel):
                    if _eh_consumivel_area(item_obj):
                        menu.add_command(label="💥 Usar em Área...",command=lambda i=item_obj: self.abrir_popup_usar_area(i))
                    else:
                        def _usar_consumivel(i=item_obj):
                            # 1. Aplica cura / dano via sistema de combate
                            CB.usar_consumivel(i, self.character, alvo=self.character, aplicar=True)
                            # 2. Aplica buffs/debuffs que estejam na lista de efeitos
                            efeitos_bb = [ef for ef in getattr(i, "efeitos", [])if isinstance(ef, dict) and ef.get("tipo") in ("buff", "debuff")]
                            if efeitos_bb:
                                aplicar_efeitos_item(efeitos_bb, self.character)
                            atualizar()
                        menu.add_command(label="✅ Usar", command=_usar_consumivel)
                    menu.add_separator()

                # ── Descartar ─────────────────────────────────────────────────
                if quantidade > 1:
                    if quantidade >= 1:
                        menu.add_command(
                            label="Descartar 1",
                            command=lambda i=item_obj: [
                                self._remover_item_do_inventario(i, 1), atualizar()
                            ]
                        )
                    if quantidade >= 5:
                        menu.add_command(
                            label="Descartar 5",
                            command=lambda i=item_obj: [
                                self._remover_item_do_inventario(i, 5), atualizar()
                            ]
                        )
                    if quantidade >= 10:
                        menu.add_command(
                            label="Descartar 10",
                            command=lambda i=item_obj: [
                                self._remover_item_do_inventario(i, 10), atualizar()
                            ]
                        )
                    menu.add_separator()
                    menu.add_command(
                        label="Descartar Tudo",
                        command=lambda i=item_obj: [
                            self._remover_item_do_inventario(i, quantidade), atualizar()
                        ]
                    )
                else:
                    menu.add_command(
                        label="Descartar",
                        command=lambda i=item_obj: [
                            self._remover_item_do_inventario(i, 1), atualizar()
                        ]
                    )

                btn_item.config(
                    command=lambda m=menu, b=btn_item: m.tk_popup(
                        b.winfo_rootx(), b.winfo_rooty() + b.winfo_height()
                    )
                )

        except Exception as e:
            print("Erro ao carregar inventário:", e)

    def refresh_equipados(self):
        if not self.character: return
        for w in self.frame_lista_equipados.winfo_children(): w.destroy()
        def atualizar(): self.refresh_inventario(); self.refresh_equipados(); self.refresh_info_basica()
        sep=lambda: tk.Frame(self.frame_lista_equipados,bg="#130f26",height=3,width=300).pack(fill="x",pady=8)

        def linha_slot(slot_nome,item_obj=None):
            frame=tk.Frame(self.frame_lista_equipados,bg="#2a0d89", width=300, height=30); frame.pack(fill="x",pady=3,padx=6); frame.pack_propagate(False)
            texto=f"{slot_nome}: {item_obj.nome}" if item_obj else f"{slot_nome}: —"
            lbl=tk.Button(frame,text=texto,bg="#2a0d89",fg="white",font=("Arial",12),anchor="w",relief=tk.FLAT,activebackground="#2a0d89",width=300,height=30)
            lbl.pack(fill="x",ipady=4),lbl.pack_propagate(False)
            if item_obj:
                menu=tk.Menu(lbl,tearoff=0)
                if isinstance(item_obj, CB.Ranged):
                    menu.add_command(label="Disparar", command=lambda i=item_obj: self.disparar_ranged(i))
                    menu.add_command(label="Carregar", command=lambda i=item_obj: self.carregar_municao_ranged(i))
                    menu.add_command(label="Descarregar", command=lambda i=item_obj: self.descarregar_municao_ranged(i))
                    if len(item_obj.acoes_disparo) > 1:
                        menu.add_command(label=f"Trocar Modo ({item_obj.modo_disparo_atual})", command=lambda i=item_obj: [i.trocar_modo_disparo(), atualizar()])
                    menu.add_separator()
                menu.add_command(label="Desequipar",command=lambda i=item_obj:[self.character.desequipar_item_generico(i),atualizar()])
                lbl.config(command=lambda m=menu,b=lbl:m.tk_popup(b.winfo_rootx(),b.winfo_rooty()+b.winfo_height()))

        for regiao,item in self.character.regioes_corpo.items(): linha_slot(regiao,item)

        if self.character.equipamentos_slots:
            sep()
            for eq in self.character.equipamentos_slots: linha_slot("Equipamento",eq)
        sep()
        for s in self.character.slots.values(): linha_slot(s.nome,s.item)

    def refresh_efeitos(self):
        for w in self.scrollable_frame_efeitos.winfo_children(): w.destroy()
        if not self.character: return
        def atualizar(): self.refresh_efeitos(); self.refresh_info_basica()

        for e in self.character.buffs_debuffs.listar_efeitos():
            cor="#00630C" if str(e.tipo).lower()=="buff" else "#630000"
            frame=tk.Frame(self.scrollable_frame_efeitos,bg=cor,width=300,height=30); frame.pack(fill="x",padx=8,pady=4); frame.pack_propagate(False)
            if e.eh_permanente():
                duracao_texto = "Permanente"
            elif e.turnos_restantes == 0:
                duracao_texto = "Imediato"
            else:
                duracao_texto = f"{e.turnos_restantes} turno{'s' if e.turnos_restantes != 1 else ''}"
            texto=f"{e.nome}  •  {duracao_texto}"
            btn=tk.Button(frame,text=texto,bg=cor,fg="white",font=("Arial",12,"bold"),anchor="w",relief=tk.FLAT,activebackground="#2a0d89")
            btn.pack(fill="x",ipady=6,ipadx=10)

            tooltip_text=f"Nome: {e.nome}\nDuração: {duracao_texto}\nDescrição: {e.descricao}\nEfeito: {e.efeito}"
            Tooltip(btn,tooltip_text)

            menu=tk.Menu(btn,tearoff=0)

            if not e.eh_permanente():
                menu.add_command(label="Aumentar duração (+1)",command=lambda ee=e:[setattr(ee,"turnos_restantes",int(ee.turnos_restantes)+1),atualizar()])
                menu.add_command(label="Diminuir duração (-1)",command=lambda ee=e:[setattr(ee,"turnos_restantes",int(ee.turnos_restantes)-1),self.character.buffs_debuffs.remover_efeito(ee.nome) if int(ee.turnos_restantes)<=0 else None,atualizar()])
                menu.add_separator()

            menu.add_command(label="Remover efeito",command=lambda n=e.nome:[self.character.buffs_debuffs.remover_efeito(n),atualizar()])

            btn.config(command=lambda m=menu,b=btn:m.tk_popup(b.winfo_rootx(),b.winfo_rooty()+b.winfo_height()))

    def refresh_habilidades(self):
        for w in self.scrollable_frame_habilidades.winfo_children(): w.destroy()
        if not self.character: return
        def atualizar(): self.refresh_habilidades(); self.refresh_info_basica()
        COR_HAB="#2a0d89"; COR_HAB_O="#2a0d89"; COR_POD="#2a0d89"; COR_POD_O="#2a0d89"; COR_BORDA="#120447"
        BADGE={"habilidade_antigo":("Habilidade"),"habilidade_ofensivo":("Habilidade de ataque"),"poder_antigo":("Poder"),"poder_ofensivo":("Poder de ataque")}
        FUNDO={"habilidade_antigo":COR_HAB,"habilidade_ofensivo":COR_HAB_O,"poder_antigo":COR_POD,"poder_ofensivo":COR_POD_O}
        itens=[]
        for h in self.character.habilidades.listar_habilidades(): itens.append(("habilidade_antigo",h))
        for h in self.character.habilidades.listar_habilidades_ofensivas(): itens.append(("habilidade_ofensivo",h))
        for p in self.character.poderes.listar_poderes(): itens.append(("poder_antigo",p))
        for p in self.character.poderes.listar_poderes_ofensivos(): itens.append(("poder_ofensivo",p))
        if not itens:
            tk.Label(self.scrollable_frame_habilidades,text="Nenhuma habilidade ou poder.",bg="#1a0869",fg="#FFFFFF",font=("Arial",10,"italic")).pack(pady=12)
            return
        for tipo,item in itens:
            bg=FUNDO[tipo]; badge_txt=BADGE[tipo]
            if "antigo" in tipo:
                tipo_txt="Passivo" if item.custo==0 else "Ativo"
                custo_txt="" if item.custo==0 else f"{item.custo} Energia"
            else:
                custos=[]
                if getattr(item,"custo_energia",0): custos.append(f"{item.custo_energia} Energia")
                if getattr(item,"custo_mana",0): custos.append(f"{item.custo_mana} Mana")
                tipo_txt="Ofensivo"
                custo_txt=" + ".join(custos) if custos else "Grátis"
            texto=f"{item.nome} | {badge_txt} | {tipo_txt}"
            if custo_txt: texto+=f" | {custo_txt}"
            def _make_menu(tipo_item,item_obj):
                m=tk.Menu(self.scrollable_frame_habilidades,tearoff=0,bg="#1a0c3a",fg="white",activebackground="#120447",activeforeground="white",font=("Arial",10))
                if "antigo" in tipo_item and item_obj.custo>0:
                    m.add_command(label="▶  Usar",command=lambda:self._usar_habilidade_poder_antigo(item_obj,atualizar)); m.add_separator()
                elif "ofensivo" in tipo_item:
                    m.add_command(label="▶  Usar (Tela de Combate)",command=lambda:self.controller.TelaDeCombate()); m.add_separator()
                m.add_command(label="🔍  Detalhes",command=lambda:_popup_detalhes(item_obj,tipo_item))
                categoria="habilidade" if "habilidade" in tipo_item else "poder"
                m.add_command(label="✏️  Editar",command=lambda:self.abrir_popup_habilidade(item_obj,categoria))
                def _remover():
                    if "habilidade" in tipo_item:
                        if "ofensivo" in tipo_item: self.character.habilidades.remover_habilidade_ofensiva(item_obj.nome)
                        else: self.character.habilidades.remover_habilidade(item_obj.nome)
                    else:
                        if "ofensivo" in tipo_item: self.character.poderes.remover_poder_ofensivo(item_obj.nome)
                        else: self.character.poderes.remover_poder(item_obj.nome)
                    atualizar()
                m.add_separator(); m.add_command(label="❌ Remover",command=_remover)
                return m
            menu_obj=_make_menu(tipo,item)
            btn=tk.Button(self.scrollable_frame_habilidades,text=texto,bg=bg,fg="white",font=("Arial",10,"bold"),height=2,relief="flat",bd=1,highlightthickness=1,highlightbackground=COR_BORDA,anchor="w",cursor="hand2",activebackground="#120447",activeforeground="white",command=lambda m=menu_obj,bg=bg: m.tk_popup(self.scrollable_frame_habilidades.winfo_pointerx(),self.scrollable_frame_habilidades.winfo_pointery()))
            btn.pack(fill="x",padx=5,pady=5)
            Tooltip(btn,getattr(item,"descricao","") or "—")
        def _popup_detalhes(item_obj,tipo_item):
            pop=tk.Toplevel(); pop.title(f"Detalhes — {item_obj.nome}"); pop.configure(bg="#130f26"); pop.geometry("420x380"); pop.resizable(False,False)
            tk.Label(pop,text=item_obj.nome,bg="#0a0433",fg="#b79cff",font=("Arial",15,"bold")).pack(fill="x",pady=10)
            frame=tk.Frame(pop,bg="#1a0869",bd=1,relief="flat"); frame.pack(fill="both",expand=True,padx=12,pady=6)
            def linha(chave,valor,cor_val="white"):
                r=tk.Frame(frame,bg="#1a0869"); r.pack(fill="x",padx=8,pady=2)
                tk.Label(r,text=f"{chave}:",bg="#1a0869",fg="#8899cc",font=("Arial",10,"bold"),width=18,anchor="w").pack(side="left")
                tk.Label(r,text=str(valor),bg="#1a0869",fg=cor_val,font=("Arial",10),anchor="w",wraplength=220,justify="left").pack(side="left")
            if "antigo" in tipo_item:
                tipo_label="Passivo" if item_obj.custo==0 else "Ativo"
                linha("Tipo",tipo_label)
                if item_obj.custo: linha("Custo",f"{item_obj.custo} Energia","#0fbcd3")
                tags_str = ", ".join(item_obj.tags) if isinstance(item_obj.tags, list) else str(item_obj.tags)
                linha("Tags",tags_str if tags_str else "—")
                valor_str = str(item_obj.valor)
                linha("Valor",valor_str)
                if item_obj.duracao: linha("Duração",f"{item_obj.duracao} turno(s)")
                linha("Descrição",item_obj.descricao or "—")
            else:
                linha("Tipo","Ataque Ofensivo")
                custos=[]
                if getattr(item_obj,"custo_energia",0): custos.append(f"{item_obj.custo_energia} Energia")
                if getattr(item_obj,"custo_mana",0): custos.append(f"{item_obj.custo_mana} Mana")
                linha("Custo",", ".join(custos) if custos else "Grátis")
                if getattr(item_obj,"dano",None): 
                    dano_str = ", ".join(f"{d['valor']} {d['tipo']}" for d in item_obj.dano)
                    linha("Dano",dano_str,"#ff9966")
                if getattr(item_obj,"efeitos",None): 
                    efeitos_str = ", ".join(e.get("nome","?") for e in item_obj.efeitos)
                    linha("Efeitos",efeitos_str,"#88eecc")
                if getattr(item_obj,"ignora_resistencias",False):
                    linha("Ignora Resistências","Sim","#ffaa00")
                linha("Descrição",item_obj.descricao or "—")
            tk.Button(pop,text="Fechar",command=pop.destroy,bg="#004080",fg="white",font=("Arial",11)).pack(pady=10)

    def refresh(self, character=None):
        """Função principal que chama todos os refreshes"""
        if character is not None:
            self.character = character
        
        # Chama todos os refreshes das seções
        self.refresh_info_basica()
        self.refresh_atributos()
        self.refresh_resistencias()
        self.refresh_modificadores()
        self.refresh_proficiencias()
        self.refresh_inventario()
        self.refresh_equipados()
        self.refresh_efeitos()
        self.refresh_habilidades()

    def setar_barra_por_clique(self,atributo_atual,atributo_max,event):
        try:
            largura=event.widget.winfo_width()
            if largura<=1: return

            proporcao=event.x/largura
            if proporcao<0: proporcao=0
            if proporcao>1: proporcao=1

            maximo=getattr(self.character,atributo_max)
            novo_valor=int(maximo*proporcao)

            setattr(self.character,atributo_atual,novo_valor)
            self.refresh_info_basica()

        except Exception as e:
            print("Erro ao setar barra:",e)
    # init e refresh #
    
    # proficiencias #
    def incrementar_proficiencia(self, prof):
        prof.nivel += 1
        self.character.recalcularAtributos()
        self.refresh_info_basica()
        self.refresh_proficiencias()
    
    def decrementar_proficiencia(self, prof):
        prof.nivel -= 1
        self.character.recalcularAtributos()
        self.refresh_info_basica()
        self.refresh_proficiencias()
    # proficiencias #
    
    # inventário #
    def _remover_item_do_inventario(self, item, quantidade=1):
        try:
            self.character.inventario.remover_item(item, quantidade)
            self.refresh()

        except Exception as e:
            print("Erro ao remover item do inventário:", e)

    def remover_protecao(self, regiao):
        try:
            # Acessa a proteção atual do personagem naquela região
            protecao_atual = getattr(self.character, regiao, None)

            if not protecao_atual:
                return

            # Retorna o item ao inventário do personagem
            self.character.inventario.gerenciar_item(item_objeto=protecao_atual, quantidade=1, operacao="adicionar")

            # Remove a proteção da região
            setattr(self.character, regiao, None)

            # Recalcula peso e atualiza interface
            self.character.calcular_peso_total()
            self.refresh()

        except Exception as e:
            print("Erro ao remover proteção:", e)

    def mostrar_popup_detalhes_item(self, item_obj):
        try:
            stats = item_obj.stats()
            tipo = item_obj.__class__.__name__

            # Ajustando o tamanho horizontal do popup
            popup = tk.Toplevel(self)
            popup.title(f"Detalhes do Item: {stats.get('Nome', 'Desconhecido')}")
            popup.configure(bg="#1a0869")
            popup.geometry("600x400")
            popup.resizable()

            lbl_titulo = tk.Label(
                popup,
                text=f"{stats.get('Nome', 'Item Sem Nome')} ({tipo})",
                font=("Arial", 16, "bold"),
                bg="#1a0869",
                fg="white"
            )
            lbl_titulo.pack(pady=(20, 10))

            # Frame que contém o canvas com scroll
            frame_scroll = tk.Frame(popup, bg="#1a0869", height=250)  # Diminuído o tamanho vertical
            frame_scroll.pack(pady=10, padx=20, fill='both', expand=True)

            canvas = tk.Canvas(frame_scroll, bg="#130f26", highlightthickness=0)
            scrollbar = tk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
            scroll_frame = tk.Frame(canvas, bg="#130f26")

            scroll_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            self.scroll_frame_item_detalhes = scroll_frame
            self.item_detalhes_atual = item_obj

            canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            for chave, valor in stats.items():
                linha = tk.Frame(scroll_frame, bg="#130f26")
                linha.pack(anchor='w', pady=2, padx=10)
                tk.Label(linha, text=f"{chave}:", font=("Arial", 12, "bold"), fg="white", bg="#130f26").pack(side="left")
                tk.Label(linha, text=f" {valor}", font=("Arial", 12), fg="white", bg="#130f26").pack(side="left")

            # Botão Fechar (removido o frame de ações e botão equipar)
            btn_fechar = tk.Button(popup, text="Fechar", command=popup.destroy, bg="#004080", fg="white", font=("Arial", 12))
            btn_fechar.pack(side="right", padx=(0, 30), pady=20)

        except Exception as e:
            print("Erro ao mostrar detalhes do item:", e)

    def abrir_popup_melhorias_item(self, item_obj):
        try:
            def obter_melhorias(item):
                for nome in ["Acessorios", "Melhorias", "melhorias_equipadas"]:
                    if hasattr(item, nome):
                        return getattr(item, nome)
                return []

            def ao_clicar_em_melhoria(melhoria, arma, personagem):
                melhorias_aplicadas = obter_melhorias(arma)
                if melhoria in melhorias_aplicadas:
                    melhoria.remover(arma)
                    if melhoria in melhorias_aplicadas:
                        melhorias_aplicadas.remove(melhoria)
                    arma.recalcular_atributos()
                    personagem.inventario.adicionar_item_objeto(melhoria, 1)
                elif any(melhoria is item["objeto"] for item in personagem.inventario.listar_itens()):
                    sucesso = melhoria.aplicar(arma)
                    if sucesso:
                        personagem.inventario.remover_item(melhoria, 1)
                atualizar_listas()
                self.refresh()

            popup = tk.Toplevel(self)
            popup.title(f"Gerenciar Melhorias - {item_obj.nome}")
            popup.configure(bg="#1a0869")
            popup.geometry("900x550")

            tk.Label(popup, text=f"Melhorias para: {item_obj.nome}", font=("Arial", 12, "bold"), bg="#1a0869", fg="white").pack(pady=(10, 5))

            frame_geral = tk.Frame(popup, bg="#1a0869")
            frame_geral.pack(fill="both", expand=True, padx=20, pady=10)

            # ====== MELHORIAS EQUIPADAS ======
            frame_equipadas = tk.Frame(frame_geral, bg="#1a0869")
            frame_equipadas.pack(side="left", fill="both", expand=True, padx=10)

            tk.Label(frame_equipadas, text="Melhorias Equipadas", font=("Arial", 12, "bold"), bg="#1a0869", fg="white").pack(pady=5)

            canvas_eq = tk.Canvas(frame_equipadas, bg="#130f26", highlightthickness=0)
            scrollbar_eq = tk.Scrollbar(frame_equipadas, orient="vertical", command=canvas_eq.yview)
            frame_scroll_eq = tk.Frame(canvas_eq, bg="#130f26")

            canvas_eq.create_window((0, 0), window=frame_scroll_eq, anchor="nw")
            canvas_eq.configure(yscrollcommand=scrollbar_eq.set)

            canvas_eq.pack(side="left", fill="both", expand=True)
            scrollbar_eq.pack(side="right", fill="y")

            # ====== MELHORIAS NO INVENTÁRIO ======
            frame_inventario = tk.Frame(frame_geral, bg="#1a0869")
            frame_inventario.pack(side="right", fill="both", expand=True, padx=10)

            tk.Label(frame_inventario, text="Melhorias no Inventário", font=("Arial", 12, "bold"), bg="#1a0869", fg="white").pack(pady=5)

            canvas_inv = tk.Canvas(frame_inventario, bg="#130f26", highlightthickness=0)
            scrollbar_inv = tk.Scrollbar(frame_inventario, orient="vertical", command=canvas_inv.yview)
            frame_scroll_inv = tk.Frame(canvas_inv, bg="#130f26")

            canvas_inv.create_window((0, 0), window=frame_scroll_inv, anchor="nw")
            canvas_inv.configure(yscrollcommand=scrollbar_inv.set)

            canvas_inv.pack(side="left", fill="both", expand=True)
            scrollbar_inv.pack(side="right", fill="y")

            def atualizar_listas():
                for w in frame_scroll_eq.winfo_children(): w.destroy()
                for w in frame_scroll_inv.winfo_children(): w.destroy()

                melhorias_equipadas = obter_melhorias(item_obj)

                for melhoria in melhorias_equipadas:
                    frame = tk.Frame(frame_scroll_eq, bg="#130f26")
                    frame.pack(fill="x", pady=2, padx=4)
                    tk.Label(frame, text=melhoria.nome, font=("Arial", 11), bg="#130f26", fg="white").pack(side="left")
                    tk.Button(frame, text="Remover", command=lambda m=melhoria: ao_clicar_em_melhoria(m, item_obj, self.character)).pack(side="right", padx=4)

                for item in self.character.inventario.listar_itens():
                    obj = item["objeto"]
                    if isinstance(obj, CB.Melhoria):
                        if (obj.tipo == "ranged" and isinstance(item_obj, CB.Ranged)) or \
                        (obj.tipo == "melee" and isinstance(item_obj, CB.Melee)) or \
                        (obj.tipo == "protecao" and isinstance(item_obj, CB.Protecao)):
                            frame = tk.Frame(frame_scroll_inv, bg="#130f26")
                            frame.pack(fill="x", pady=2, padx=4)
                            tk.Label(frame, text=obj.nome, font=("Arial", 11), bg="#130f26", fg="white").pack(side="left")
                            tk.Button(frame, text="Equipar", command=lambda m=obj: ao_clicar_em_melhoria(m, item_obj, self.character)).pack(side="right", padx=4)

            atualizar_listas()

            tk.Button(popup, text="Fechar", command=popup.destroy, font=("Arial", 12), bg="#004080", fg="white").pack(pady=10)

        except Exception as e:
            print("Erro ao abrir popup de melhorias:", e)

    def atualizar_popup_detalhes(self, item_obj, scroll_frame):
            for widget in scroll_frame.winfo_children():
                widget.destroy()

            stats_atualizadas = item_obj.stats()
            for chave, valor in stats_atualizadas.items():
                linha = tk.Frame(scroll_frame, bg="#130f26")
                linha.pack(anchor='w', pady=2, padx=10)
                tk.Label(linha, text=f"{chave}:", font=("Arial", 12, "bold"), fg="white", bg="#130f26").pack(side="left")
                tk.Label(linha, text=f" {valor}", font=("Arial", 12), fg="white", bg="#130f26").pack(side="left")
    
    def obter_nome_protecao(self, protecao):
        """Obtém o nome da proteção de forma segura"""
        if not protecao:
            return "Nenhuma"
        
        # Se é um dicionário, pega o nome diretamente
        if isinstance(protecao, dict):
            return protecao.get("nome", "Desconhecida")
        
        # Se é um objeto, pega o atributo nome
        if hasattr(protecao, 'nome'):
            return protecao.nome
        
        # Fallback
        return str(protecao)
  
    def _equipar_item(self,item):
        try:
            sucesso=False
            if self.character._eh_protecao(item):
                regiao=item.regiao_indicada.lower() if item.regiao_indicada else None
                if not regiao or regiao not in self.character.regioes_corpo: raise Exception(f"Região inválida para proteção: {regiao}")
                self.character._equipar_protecao_obj_em_regiao(item,regiao); sucesso=True
            else:
                sucesso=self.character.equipar_item(item)
            if sucesso: self.refresh()
            else: print("Equipar falhou:",item)
        except Exception as e:
            print("Erro ao equipar item:",e)

    def abrir_popup_escolher_slot(self,item_obj):
        try:
            popup=tk.Toplevel(self); popup.title(f"Escolher slot para: {getattr(item_obj,'nome','Item')}"); popup.configure(bg="#1a0869"); popup.geometry("400x350")
            tk.Label(popup,text=f"{getattr(item_obj,'nome','Item')}",font=("Arial",12,"bold"),bg="#1a0869",fg="white").pack(pady=10)

            if self.character._eh_protecao(item_obj):
                regioes_validas=self.character.obter_regioes_compativeis(item_obj)
                for r in regioes_validas:
                    tk.Button(popup,text=r.capitalize(),command=lambda reg=r:[self.character._equipar_protecao_obj_em_regiao(item_obj,reg),self.refresh_inventario(),self.refresh_equipados(),popup.destroy()],bg="#2a0d89",fg="white",font=("Arial",10)).pack(fill="x",padx=20,pady=5)

            elif self.character._eh_arma_melee(item_obj) or self.character._eh_arma_ranged(item_obj):
                maos_item=getattr(item_obj,"maos",1)
                slots_mao=[(k,s) for k,s in self.character.slots.items() if s.tipo=="mao"]
                slots_suporte=[(k,s) for k,s in self.character.slots.items() if s.tipo=="suporte"]

                for chave,slot in slots_mao:
                    tk.Button(popup,text=f"Equipar em {slot.nome}",command=lambda key=chave:self._equipar_popup(item_obj,key,popup),bg="#2a0d89",fg="white",font=("Arial",10)).pack(fill="x",padx=20,pady=5)

                if maos_item==2 and len(slots_mao)>=2:
                    tk.Button(popup,text="Equipar usando 2 mãos",command=lambda:self._popup_escolher_duas_maos(item_obj,popup),bg="#5a0d89",fg="white",font=("Arial",10,"bold")).pack(fill="x",padx=20,pady=10)

                for chave,slot in slots_suporte:
                    aceita=getattr(slot,"aceita",[])
                    requer=getattr(slot,"requer_maos",1)
                    classe=item_obj.__class__.__name__
                    if classe in aceita and maos_item==requer:
                        tk.Button(popup,text=f"Guardar em {slot.nome}",command=lambda key=chave:self._equipar_popup(item_obj,key,popup),bg="#0d5a89",fg="white",font=("Arial",10)).pack(fill="x",padx=20,pady=5)

            elif isinstance(item_obj,CB.Equipamento):
                tk.Button(popup,text="Equipar Equipamento",command=lambda:[self.character.equipar_equipamento_slot(item_obj),self.refresh_inventario(),self.refresh_equipados(),popup.destroy()],bg="#2a0d89",fg="white",font=("Arial",10)).pack(fill="x",padx=20,pady=5)

            else:
                tk.Label(popup,text="Não há slots disponíveis para este item.",bg="#1a0869",fg="white").pack(pady=20)

        except Exception as e:
            print("Erro no popup de escolher slot:",e)
    
    def _equipar_popup(self,item_obj,nome_slot,popup):
        sucesso=self.character._equipar_arma(item_obj,nome_slot=nome_slot,forcar=True,usar_duas_maos=False)
        if sucesso: self.refresh(); popup.destroy()
        else: print("Falha ao equipar no slot:",nome_slot)
   
    def _popup_escolher_duas_maos(self,item_obj,popup_pai):
        popup2=tk.Toplevel(self); popup2.title("Escolher 2 Mãos"); popup2.configure(bg="#1a0869"); popup2.geometry("300x250")
        maos=[(k,s) for k,s in self.character.slots.items() if s.tipo=="mao"]
        for i in range(len(maos)):
            for j in range(i+1,len(maos)):
                k1,s1=maos[i]; k2,s2=maos[j]
                texto=f"{s1.nome} + {s2.nome}"
                tk.Button(popup2,text=texto,command=lambda a=k1,b=k2:self._equipar_dupla_especifica(item_obj,a,b,popup_pai,popup2),bg="#5a0d89",fg="white").pack(fill="x",padx=15,pady=5)

    def _equipar_dupla_especifica(self,item_obj,slot1,slot2,popup1,popup2):
        sucesso=self.character._equipar_arma(item_obj,nome_slot=slot1,forcar=True,usar_duas_maos=True)
        if sucesso: self.refresh(); popup2.destroy(); popup1.destroy()
        else: print("Falha ao equipar nas duas mãos específicas")
    # inventário #

    # funções de items #
    def disparar_ranged(self, arma):
        if not isinstance(arma, CB.Ranged):
            print("Esse item não é uma arma de fogo.")
            return

        popup = tk.Toplevel(self)
        popup.title("Disparo")
        popup.configure(bg="#1a0869")
        popup.geometry("400x200")
        popup.resizable(False, False)

        label_municoes = tk.Label(
            popup,
            text=f"Munições disponíveis: {arma.munições if arma.municao else 0}",
            bg="#1a0869", fg="white", font=("Arial", 12)
        )
        label_municoes.pack(pady=(10, 5))

        tk.Label(
            popup, text="Quantidade de disparos:",
            bg="#1a0869", fg="white", font=("Arial", 12)
        ).pack(pady=(10, 5))

        spinbox_qtd = tk.Spinbox(
            popup,
            from_=1,
            to=arma.munições if arma.munições > 0 else 1,
            width=5,
            justify="center"
        )
        spinbox_qtd.delete(0, tk.END)
        spinbox_qtd.insert(0, "1")
        spinbox_qtd.pack()

        mensagem_label = tk.Label(popup, text="", bg="#1a0869", fg="lightgreen", font=("Arial", 10))
        mensagem_label.pack(pady=(5, 10))

        def confirmar_disparo():
            try:
                qtd = int(spinbox_qtd.get())

                if arma.municao is None or arma.munições == 0:
                    mensagem_label.config(text="Click Click Click... (arma descarregada)", fg="red")
                    return

                arma.disparar(qtd)
                self.refresh()
                popup.destroy()
            except Exception as e:
                mensagem_label.config(text=f"Erro ao disparar: {e}", fg="red")

        def cancelar():
            popup.destroy()

        botoes_frame = tk.Frame(popup, bg="#1a0869")
        botoes_frame.pack(pady=10)

        tk.Button(
            botoes_frame, text="Cancelar", command=cancelar,
            bg="#800000", fg="white", width=10
        ).pack(side="left", padx=10)

        tk.Button(
            botoes_frame, text="Confirmar", command=confirmar_disparo,
            bg="#004080", fg="white", width=10
        ).pack(side="right", padx=10)
    
    def carregar_municao_ranged(self, arma):
        try:
            popup = tk.Toplevel(self)
            popup.title("Carregar Munição")
            popup.configure(bg="#1a0869")
            popup.geometry("400x250")
            popup.resizable(False, False)

            tk.Label(popup, text="Escolha a Munição:", bg="#1a0869", fg="white", font=("Arial", 12)).pack(pady=(10, 5))

            # Buscar munições compatíveis no inventário do personagem
            try:
                itens_inventario = self.character.inventario.listar_itens()
            except Exception as e:
                print("Erro ao acessar inventário do personagem:", e)
                popup.destroy()
                return

            municoes_compativeis = [
                item for item in itens_inventario
                if isinstance(item["objeto"], CB.Municao) and item["objeto"].calibre == arma.calibre
            ]

            if not municoes_compativeis:
                tk.Label(popup, text="Sem munições compatíveis com esta arma.", bg="#1a0869", fg="red").pack(pady=20)
                return

            # Mostrar nomes das munições compatíveis
            nomes_municoes = [f"{item['objeto'].nome} (x{item['quantidade']})" for item in municoes_compativeis]
            municao_var = tk.StringVar(value=nomes_municoes[0])
            dropdown = tk.OptionMenu(popup, municao_var, *nomes_municoes)
            dropdown.config(font=("Arial", 10))
            dropdown.pack(pady=5)

            tk.Label(popup, text="Quantidade:", bg="#1a0869", fg="white", font=("Arial", 12)).pack(pady=(10, 5))
            quantidade_spinbox = tk.Spinbox(popup, from_=1, to=100, width=5)
            quantidade_spinbox.pack()

            mensagem_label = tk.Label(popup, text="", bg="#1a0869", fg="lightgreen", font=("Arial", 10))
            mensagem_label.pack()

            def confirmar_carregamento():
                index = nomes_municoes.index(municao_var.get())
                item_escolhido = municoes_compativeis[index]
                municao_obj = item_escolhido["objeto"]
                quantidade = int(quantidade_spinbox.get())

                carregado = arma.carregar_municao(municao_obj, quantidade)

                if carregado > 0:
                    self._remover_item_do_inventario(municao_obj, carregado)
                    mensagem_label.config(text=f"{carregado} munições carregadas.")
                    self.refresh()
                    popup.destroy()
                else:
                    mensagem_label.config(text="Não foi possível carregar a munição.", fg="red")
            def recarregar_tudo():
                index = nomes_municoes.index(municao_var.get())
                item_escolhido = municoes_compativeis[index]
                municao_obj = item_escolhido["objeto"]
                quantidade_disponivel = item_escolhido["quantidade"]

                espaco_restante = arma.capacidade - arma.munições  # Ajuste os nomes se forem diferentes
                quantidade_a_carregar = min(espaco_restante, quantidade_disponivel)

                if quantidade_a_carregar <= 0:
                    mensagem_label.config(text="A arma já está cheia ou não há munição.", fg="red")
                    return

                carregado = arma.carregar_municao(municao_obj, quantidade_a_carregar)

                if carregado > 0:
                    self._remover_item_do_inventario(municao_obj, carregado)
                    mensagem_label.config(text=f"{carregado} munições carregadas.")
                    self.refresh()
                    popup.destroy()
                else:
                    mensagem_label.config(text="Não foi possível carregar a munição.", fg="red")
            
            # Frame para botões lado a lado
            botoes_frame = tk.Frame(popup, bg="#1a0869")
            botoes_frame.pack(pady=20)

            btn_confirmar = tk.Button(
                botoes_frame, text="Confirmar",
                command=confirmar_carregamento, bg="#004080", fg="white", width=12
            )
            btn_confirmar.pack(side="left", padx=10)

            btn_recarregar_tudo = tk.Button(
                botoes_frame, text="Recarregar Tudo",
                command=recarregar_tudo, bg="#008000", fg="white", width=15
            )
            btn_recarregar_tudo.pack(side="left", padx=10)

        except Exception as e:
            print("Erro ao carregar munição:", e)

    def descarregar_municao_ranged(self, arma):
        if not isinstance(arma, CB.Ranged):
            print("Esse item não é uma arma de fogo.")
            return

        if arma.munições == 0:
            print("A arma já está descarregada.")
            return

        popup = tk.Toplevel(self)
        popup.title("Descarregar Munição")
        popup.configure(bg="#1a0869")
        popup.geometry("400x200")
        popup.resizable(False, False)

        tk.Label(popup, text=f"Munições na arma ({arma.municao.nome}): {arma.munições}",
                bg="#1a0869", fg="white", font=("Arial", 12)).pack(pady=(10, 5))

        tk.Label(popup, text="Quantidade a descarregar:", bg="#1a0869", fg="white", font=("Arial", 12)).pack(pady=(10, 5))
        spinbox_qtd = tk.Spinbox(popup, from_=1, to=arma.munições, width=5)
        spinbox_qtd.pack()

        mensagem_label = tk.Label(popup, text="", bg="#1a0869", fg="lightgreen", font=("Arial", 10))
        mensagem_label.pack()

        def confirmar_descarregamento():
            try:
                qtd = int(spinbox_qtd.get())
                municoes = arma.descarregar_municao(quantidade=qtd)

                if municoes:
                    for municao in municoes:
                        self.character.inventario.adicionar_item_objeto(municao)
                    mensagem_label.config(text=f"{len(municoes)} munições devolvidas ao inventário.")
                    self.refresh()
                    popup.destroy()
                else:
                    mensagem_label.config(text="Nada foi descarregado.", fg="orange")
            except Exception as e:
                mensagem_label.config(text=f"Erro: {e}", fg="red")

        def descarregar_tudo():
            try:
                qtd_total = arma.munições
                municoes = arma.descarregar_municao(quantidade=qtd_total)

                if municoes:
                    for municao in municoes:
                        self.character.inventario.adicionar_item_objeto(municao)
                    mensagem_label.config(text=f"{len(municoes)} munições devolvidas ao inventário.")
                    self.refresh()
                    popup.destroy()
                else:
                    mensagem_label.config(text="Nada foi descarregado.", fg="orange")
            except Exception as e:
                mensagem_label.config(text=f"Erro: {e}", fg="red")

        # Frame para os botões lado a lado
        botoes_frame = tk.Frame(popup, bg="#1a0869")
        botoes_frame.pack(pady=20)

        btn_confirmar = tk.Button(
            botoes_frame, text="Confirmar",
            command=confirmar_descarregamento, bg="#004080", fg="white", width=12
        )
        btn_confirmar.pack(side="left", padx=10)

        btn_tudo = tk.Button(
            botoes_frame, text="Descarregar Tudo",
            command=descarregar_tudo, bg="#8B0000", fg="white", width=15
        )
        btn_tudo.pack(side="left", padx=10)

    def abrir_popup_equipar_protecao(self, protecao, popup_detalhes):
        popup = tk.Toplevel(self)
        popup.title("Escolha a região para equipar")
        popup.configure(bg='#1a0869')
        popup.grab_set()

        label = tk.Label(popup, text="Escolha a região do corpo:", font=("Arial", 14), bg='#1a0869', fg='white')
        label.pack(pady=10)

        regioes = ["Cabeça", "Rosto", "Torso", "Braços", "Pernas"]

        for regiao in regioes:
            botao = tk.Button(
                popup, text=regiao,
                command=lambda r=regiao: self.equipar_na_regiao(r, protecao, popup, popup_detalhes),
                bg='#2a0d89', fg='white', font=("Arial", 12), width=20
            )
            botao.pack(pady=5)

    def equipar_na_regiao(self, regiao, protecao, popup, popup_detalhes):
        self.character.equipar_do_inventario(regiao, protecao.nome)  # Usa a função da classe Personagem
        popup.destroy()
        popup_detalhes.destroy()
        self.refresh()
    
    def abrir_popup_transferencia(self):
        popup = tk.Toplevel(self)
        popup.title("Transferência de Itens")
        popup.geometry("900x500")
        popup.configure(bg="#1a1a2e")
        popup.resizable(False, False)

        personagem_origem = self.character

        # Lista todos os personagens de todos os grupos, exceto o personagem de origem
        todos_personagens = sum(D.GruposDePersonagens.values(), [])
        personagens_destino = [p for p in todos_personagens if p != personagem_origem]

        destino_var = tk.StringVar()
        destino_nomes = [f"{p.nome} ({grupo})"
                        for grupo, lista in D.GruposDePersonagens.items()
                        for p in lista if p != personagem_origem]

        # --- Linha de seleção ---
        linha_selecao = tk.Frame(popup, bg="#1a1a2e")
        linha_selecao.pack(pady=10)

        tk.Label(linha_selecao, text=f"Origem: {personagem_origem.nome}", bg="#1a1a2e", fg="white", font=("Arial", 12)).grid(row=0, column=0, padx=30)

        tk.Label(linha_selecao, text="Destino:", bg="#1a1a2e", fg="white", font=("Arial", 12)).grid(row=0, column=1, padx=10)
        ttk.Combobox(linha_selecao, textvariable=destino_var, state="readonly", values=destino_nomes).grid(row=0, column=2)

        # --- Linha dos inventários ---
        linha_inventario = tk.Frame(popup, bg="#1a1a2e")
        linha_inventario.pack(fill="both", expand=True, padx=20, pady=(10, 10))

        def criar_frame_inventario(parent, titulo):
            frame = tk.Frame(parent, bg="#130f26")
            frame.pack(side="left", fill="both", expand=True, padx=10)
            tk.Label(frame, text=titulo, font=("Arial", 12, "bold"), bg="#130f26", fg="white").pack()
            canvas = tk.Canvas(frame, bg="#130f26", highlightthickness=0)
            scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
            frame_scroll = tk.Frame(canvas, bg="#130f26")
            canvas.create_window((0, 0), window=frame_scroll, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            return frame_scroll

        frame_scroll_o = criar_frame_inventario(linha_inventario, "Inventário de Origem")
        frame_scroll_d = criar_frame_inventario(linha_inventario, "Inventário de Destino")

        def transferir_item(item, origem, destino, quantidade):
            if quantidade <= 0: return
            origem.inventario.remover_item(item, quantidade)
            destino.inventario.adicionar_item_objeto(item, quantidade)
            atualizar_listas()

        def atualizar_listas():
            for w in frame_scroll_o.winfo_children(): w.destroy()
            for w in frame_scroll_d.winfo_children(): w.destroy()

            nome_destino_formatado = destino_var.get()
            nome_destino = nome_destino_formatado.split(" (")[0] if " (" in nome_destino_formatado else nome_destino_formatado

            destino = next((p for p in todos_personagens if p.nome == nome_destino), None)
            if not destino:
                return

            def criar_item_row(parent_frame, item_data, de, para, direcao):
                nome = item_data["nome"]
                obj = item_data["objeto"]
                qtd = item_data["quantidade"]
                is_stackable = item_data["id"] is None

                frame = tk.Frame(parent_frame, bg="#130f26")
                frame.pack(fill="x", pady=2, padx=5)

                tk.Label(frame, text=f"{nome} x{qtd}" if is_stackable else nome,
                        bg="#130f26", fg="white", font=("Arial", 11)).pack(side="left")

                if is_stackable:
                    qtd_var = tk.IntVar(value=1)
                    tk.Entry(frame, textvariable=qtd_var, width=4, font=("Arial", 10), justify="center").pack(side="right", padx=(2, 0))

                    btn = tk.Button(frame, text=direcao, font=("Arial", 10, "bold"), bg="#2a0d89", fg="white",
                                    command=lambda: transferir_item(obj, de, para, qtd_var.get()))
                    btn.pack(side="right", padx=(2, 4))
                else:
                    btn = tk.Button(frame, text=direcao, font=("Arial", 10, "bold"), bg="#2a0d89", fg="white",
                                    command=lambda: transferir_item(obj, de, para, 1))
                    btn.pack(side="right", padx=4)

            for item in personagem_origem.inventario.listar_itens():
                criar_item_row(frame_scroll_o, item, personagem_origem, destino, "→")

            for item in destino.inventario.listar_itens():
                criar_item_row(frame_scroll_d, item, destino, personagem_origem, "←")

            self.refresh()

        destino_var.trace_add("write", lambda *_: atualizar_listas())

        tk.Button(popup, text="Fechar", command=popup.destroy, font=("Arial", 12), bg="#004080", fg="white").pack(pady=(0, 10))
    
    def abrir_popup_melhorias(self):
        try:
            def obter_melhorias(item):
                for nome in ["Acessorios", "Melhorias", "melhorias_equipadas"]:
                    if hasattr(item, nome):
                        return getattr(item, nome)
                return []

            def ao_clicar_em_melhoria(melhoria, arma, personagem):
                melhorias_aplicadas = obter_melhorias(arma)
                if melhoria in melhorias_aplicadas:
                    melhoria.remover(arma)
                    if melhoria in melhorias_aplicadas:
                        melhorias_aplicadas.remove(melhoria)
                    arma.recalcular_atributos()
                    personagem.inventario.adicionar_item_objeto(melhoria, 1)
                elif any(melhoria is item["objeto"] for item in personagem.inventario.listar_itens()):
                    sucesso = melhoria.aplicar(arma)
                    if sucesso:
                        personagem.inventario.remover_item(melhoria, 1)
                atualizar_listas()
                self.refresh()

            popup = tk.Toplevel(self)
            popup.title("Gerenciar Melhorias")
            popup.configure(bg="#1a0869")
            popup.geometry("900x550")

            tk.Label(popup, text="Escolha o item para gerenciar melhorias:", font=("Arial", 12, "bold"), bg="#1a0869", fg="white").pack(pady=(10, 5))

            # ============ COMBOBOX DE ITENS ============
            todos_itens_validos = []

            for item in self.character.inventario.listar_itens():
                if isinstance(item["objeto"], (CB.Ranged, CB.Melee, CB.Protecao)):
                    todos_itens_validos.append(item["objeto"])
            for slot in self.character.equipados.listar_itens():
                if isinstance(slot, (CB.Ranged, CB.Melee)):
                    todos_itens_validos.append(slot)
            regioes = {
                "Cabeça": self.character.Cabeça,
                "Rosto": self.character.Rosto,
                "Torso": self.character.Torso,
                "Braços": self.character.Braços,
                "Pernas": self.character.Pernas
            }
            for protecao in regioes.values():
                if isinstance(protecao, CB.Protecao):
                    todos_itens_validos.append(protecao)

            item_selecionado = tk.StringVar()
            combobox = ttk.Combobox(popup, textvariable=item_selecionado, values=[i.nome for i in todos_itens_validos], state="readonly")
            combobox.pack(pady=5)

            frame_geral = tk.Frame(popup, bg="#1a0869")
            frame_geral.pack(fill="both", expand=True, padx=20, pady=10)

            # ====== MELHORIAS EQUIPADAS ======
            frame_equipadas = tk.Frame(frame_geral, bg="#1a0869")
            frame_equipadas.pack(side="left", fill="both", expand=True, padx=10)

            tk.Label(frame_equipadas, text="Melhorias Equipadas", font=("Arial", 12, "bold"), bg="#1a0869", fg="white").pack(pady=5)

            canvas_eq = tk.Canvas(frame_equipadas, bg="#130f26", highlightthickness=0)
            scrollbar_eq = tk.Scrollbar(frame_equipadas, orient="vertical", command=canvas_eq.yview)
            frame_scroll_eq = tk.Frame(canvas_eq, bg="#130f26")

            canvas_eq.create_window((0, 0), window=frame_scroll_eq, anchor="nw")
            canvas_eq.configure(yscrollcommand=scrollbar_eq.set)

            canvas_eq.pack(side="left", fill="both", expand=True)
            scrollbar_eq.pack(side="right", fill="y")

            # ====== MELHORIAS NO INVENTÁRIO ======
            frame_inventario = tk.Frame(frame_geral, bg="#1a0869")
            frame_inventario.pack(side="right", fill="both", expand=True, padx=10)

            tk.Label(frame_inventario, text="Melhorias no Inventário", font=("Arial", 12, "bold"), bg="#1a0869", fg="white").pack(pady=5)

            canvas_inv = tk.Canvas(frame_inventario, bg="#130f26", highlightthickness=0)
            scrollbar_inv = tk.Scrollbar(frame_inventario, orient="vertical", command=canvas_inv.yview)
            frame_scroll_inv = tk.Frame(canvas_inv, bg="#130f26")

            canvas_inv.create_window((0, 0), window=frame_scroll_inv, anchor="nw")
            canvas_inv.configure(yscrollcommand=scrollbar_inv.set)

            canvas_inv.pack(side="left", fill="both", expand=True)
            scrollbar_inv.pack(side="right", fill="y")

            def atualizar_listas():
                for w in frame_scroll_eq.winfo_children(): w.destroy()
                for w in frame_scroll_inv.winfo_children(): w.destroy()

                nome = item_selecionado.get()
                item_obj = next((i for i in todos_itens_validos if i.nome == nome), None)
                if not item_obj: return

                melhorias_equipadas = obter_melhorias(item_obj)

                for melhoria in melhorias_equipadas:
                    frame = tk.Frame(frame_scroll_eq, bg="#130f26")
                    frame.pack(fill="x", pady=2, padx=4)
                    tk.Label(frame, text=melhoria.nome, font=("Arial", 11), bg="#130f26", fg="white").pack(side="left")
                    tk.Button(frame, text="Remover", command=lambda m=melhoria: ao_clicar_em_melhoria(m, item_obj, self.character)).pack(side="right", padx=4)

                for item in self.character.inventario.listar_itens():
                    obj = item["objeto"]
                    if isinstance(obj, CB.Melhoria):
                        if (obj.tipo == "ranged" and isinstance(item_obj, CB.Ranged)) or \
                        (obj.tipo == "melee" and isinstance(item_obj, CB.Melee)) or \
                        (obj.tipo == "protecao" and isinstance(item_obj, CB.Protecao)):
                            frame = tk.Frame(frame_scroll_inv, bg="#130f26")
                            frame.pack(fill="x", pady=2, padx=4)
                            tk.Label(frame, text=obj.nome, font=("Arial", 11), bg="#130f26", fg="white").pack(side="left")
                            tk.Button(frame, text="Equipar", command=lambda m=obj: ao_clicar_em_melhoria(m, item_obj, self.character)).pack(side="right", padx=4)

            # Atualiza lista ao selecionar item
            combobox.bind("<<ComboboxSelected>>", lambda e: atualizar_listas())

            tk.Button(popup, text="Fechar", command=popup.destroy, font=("Arial", 12), bg="#004080", fg="white").pack(pady=10)

        except Exception as e:
            print("Erro ao abrir popup de melhorias:", e)
    ## funções de items ##

    ## funções dos botões extras ##
    def abrir_popup_habilidade(self, item=None, categoria="habilidade"):
        if not self.character:
            return

        editando    = item is not None
        eh_ofensivo = isinstance(item, (CB.PoderOfensivo, CB.HabilidadeOfensiva)) if editando else False

        # ── Categorias de tags (uso exclusivo deste popup) ────────────────────
        TIPOS_DANO   = ["contundente","concussivo","cortante","perfurante","balístico",
                        "rasgante","explosivo","incendiário","congelante","envenenante",
                        "eletrocutante","mental"]
        TIPOS_TESTE  = ["iniciativa","sorte","força","agilidade","vigor","inteligencia",
                        "presença","tática","poder","físico","mental","vocal","qualquer teste"]
        PALAVRAS     = ["vida","energia","mana","vidaMax","energiaMax","manaMax",
                        "movimentação","bloqueio","esquiva","carga","percepção"]
        RESISTENCIAS = [f"resistencia_{t}" for t in TIPOS_DANO]
        DESARMADO    = ["desarmado_dano", "desarmado_crit_mult", "desarmado_crit_valor"]  # ← NOVO
        CATEGORIAS   = ["Tipos de Dano", "Tipos de Teste", "Palavras-chave", "Resistências", "Desarmado"]  # ← NOVO

        def opcoes_cat(cat):
            return {"Tipos de Dano": TIPOS_DANO, "Tipos de Teste": TIPOS_TESTE,
                    "Palavras-chave": PALAVRAS, "Resistências": RESISTENCIAS,
                    "Desarmado": DESARMADO}.get(cat, TIPOS_TESTE)  # ← NOVO

        def detectar_cat(tag):
            if tag in TIPOS_DANO:   return "Tipos de Dano"
            if tag in TIPOS_TESTE:  return "Tipos de Teste"
            if tag in RESISTENCIAS: return "Resistências"
            if tag in DESARMADO:    return "Desarmado"  # ← NOVO
            return "Palavras-chave"

        # ── janela ────────────────────────────────────────────────────────────
        popup = tk.Toplevel(self)
        popup.title("Editar" if editando else "Novo Poder / Habilidade")
        popup.geometry("680x820")
        popup.configure(bg="#0d0a1e")
        popup.resizable(False, True)

        BG = "#0d0a1e"; PANEL = "#12103a"; CARD = "#1a1640"
        ENT = "#0b0926"; FG = "#e8e0ff"; ACC = "#7c5cfc"
        GRN = "#1f7a1f"; RED = "#7a1f1f"

        # ── header ────────────────────────────────────────────────────────────
        hdr = tk.Frame(popup, bg="#090720", height=52)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr,
                 text=("✦ EDITAR" if editando else "✦ NOVO") + "  PODER / HABILIDADE",
                 font=("Consolas", 14, "bold"), bg="#090720", fg="#a88fff"
                 ).pack(side="left", padx=18, pady=12)

        # ── scroll principal ──────────────────────────────────────────────────
        outer = tk.Frame(popup, bg=BG)
        outer.pack(fill="both", expand=True)
        cv = tk.Canvas(outer, bg=BG, highlightthickness=0)
        sb_main = tk.Scrollbar(outer, orient="vertical", command=cv.yview)
        inner = tk.Frame(cv, bg=BG)
        inner.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
        cv.create_window((0, 0), window=inner, anchor="nw")
        cv.configure(yscrollcommand=sb_main.set)
        cv.pack(side="left", fill="both", expand=True)
        sb_main.pack(side="right", fill="y")
        cv.bind("<Enter>",
                lambda e: cv.bind_all("<MouseWheel>",
                                      lambda ev: cv.yview_scroll(int(ev.delta / -90), "units")))
        cv.bind("<Leave>", lambda e: cv.unbind_all("<MouseWheel>"))

        # ── helpers de layout ─────────────────────────────────────────────────
        def section(parent, title):
            f = tk.Frame(parent, bg=PANEL)
            f.pack(fill="x", padx=14, pady=(10, 2))
            tk.Label(f, text=title, bg=PANEL, fg="#9988dd",
                     font=("Consolas", 9, "bold"), padx=8, pady=4).pack(anchor="w")
            body = tk.Frame(f, bg=CARD)
            body.pack(fill="x", padx=4, pady=(0, 6))
            return body

        def lbl_entry(parent, label, width=28, hint=""):
            r = tk.Frame(parent, bg=CARD)
            r.pack(fill="x", padx=10, pady=4)
            tk.Label(r, text=label, bg=CARD, fg="#8899cc",
                     font=("Arial", 10), width=20, anchor="w").pack(side="left")
            e = tk.Entry(r, width=width, bg=ENT, fg=FG, insertbackground=FG,
                         relief="flat", highlightthickness=1,
                         highlightbackground="#2a1f6a", highlightcolor=ACC,
                         font=("Arial", 10))
            e.pack(side="left", fill="x", expand=True, padx=(4, 0))
            if hint:
                tk.Label(r, text=hint, bg=CARD, fg="#556688",
                         font=("Arial", 8, "italic")).pack(side="left", padx=6)
            return e

        # ═══════════════  SEÇÃO 1 – IDENTIDADE  ══════════════════════════════
        s_id = section(inner, "  IDENTIDADE")

        # Categoria: Habilidade ou Poder
        var_cat = tk.StringVar(value=categoria)
        r_cat = tk.Frame(s_id, bg=CARD)
        r_cat.pack(fill="x", padx=10, pady=4)
        tk.Label(r_cat, text="Categoria", bg=CARD, fg="#8899cc",
                 font=("Arial", 10), width=20, anchor="w").pack(side="left")
        for val, txt in [("habilidade", "Habilidade"), ("poder", "Poder")]:
            tk.Radiobutton(r_cat, text=txt, variable=var_cat, value=val,
                           bg=CARD, fg=FG, selectcolor="#24195e",
                           activebackground=CARD, activeforeground=FG,
                           indicatoron=0, width=14, bd=1, relief="ridge",
                           font=("Arial", 9)).pack(side="left", padx=3)

        # Subtipo: Padrão (passivo/ativo) ou Ofensivo
        var_subtipo = tk.StringVar(value="ofensivo" if eh_ofensivo else "padrao")
        r_sub = tk.Frame(s_id, bg=CARD)
        r_sub.pack(fill="x", padx=10, pady=4)
        tk.Label(r_sub, text="Subtipo", bg=CARD, fg="#8899cc",
                 font=("Arial", 10), width=20, anchor="w").pack(side="left")
        for val, txt in [("padrao", "Padrão  (passivo / ativo)"),
                         ("ofensivo", "Ofensivo  (dano / ataque)")]:
            tk.Radiobutton(r_sub, text=txt, variable=var_subtipo, value=val,
                           bg=CARD, fg=FG, selectcolor="#24195e",
                           activebackground=CARD, activeforeground=FG,
                           indicatoron=0, width=22, bd=1, relief="ridge",
                           font=("Arial", 9)).pack(side="left", padx=3)

        ent_nome = lbl_entry(s_id, "Nome")
        ent_desc = lbl_entry(s_id, "Descrição")

        # ══════════════════════════════════════════════════════════════════════
        #  FRAME PADRÃO  (passivo ↔ ativo, determinado pelo custo)
        # ══════════════════════════════════════════════════════════════════════
        frame_padrao = tk.Frame(inner, bg=BG)

        # ── Custo ─────────────────────────────────────────────────────────────
        s_custo = section(frame_padrao, "  CUSTO  (0 = passivo)")
        r_custo = tk.Frame(s_custo, bg=CARD)
        r_custo.pack(fill="x", padx=10, pady=4)
        tk.Label(r_custo, text="Energia", bg=CARD, fg="#8899cc",
                 font=("Arial", 10), width=10, anchor="w").pack(side="left")
        ent_energia = tk.Entry(r_custo, width=6, bg=ENT, fg=FG,
                               insertbackground=FG, relief="flat",
                               highlightthickness=1, highlightbackground="#2a1f6a",
                               highlightcolor=ACC, font=("Arial", 10))
        ent_energia.pack(side="left", padx=(4, 20))
        tk.Label(r_custo, text="Mana", bg=CARD, fg="#8899cc",
                 font=("Arial", 10), width=8, anchor="w").pack(side="left")
        ent_mana_pad = tk.Entry(r_custo, width=6, bg=ENT, fg=FG,
                                insertbackground=FG, relief="flat",
                                highlightthickness=1, highlightbackground="#2a1f6a",
                                highlightcolor=ACC, font=("Arial", 10))
        ent_mana_pad.pack(side="left", padx=(4, 0))

        lbl_modo = tk.Label(s_custo, text="▶ MODO: PASSIVO",
                            bg=CARD, fg="#55cc88", font=("Consolas", 9, "bold"))
        lbl_modo.pack(anchor="w", padx=14, pady=(0, 4))

        # ── Sub-frame PASSIVO ─────────────────────────────────────────────────
        frame_passivo = tk.Frame(frame_padrao, bg=BG)

        s_pass = section(frame_passivo, "  MODIFICADORES PASSIVOS")
        linhas_passivo = []

        def _rebuild_passivo():
            for w in s_pass.winfo_children():
                w.destroy()
            for idx, ln in enumerate(linhas_passivo):
                bloco = tk.Frame(s_pass, bg="#0f0d2e", relief="ridge", bd=1)
                bloco.pack(fill="x", padx=6, pady=3)

                row1 = tk.Frame(bloco, bg="#0f0d2e")
                row1.pack(fill="x", padx=8, pady=(5, 2))
                tk.Label(row1, text="Categoria", fg="#8899cc", bg="#0f0d2e",
                         font=("Arial", 9)).pack(side="left", padx=(0, 6))
                cat_cb = ttk.Combobox(row1, textvariable=ln["cat"],
                                      values=CATEGORIAS, state="readonly",
                                      font=("Arial", 9), width=18)
                cat_cb.pack(side="left", padx=(0, 10))

                def _rem_p(i=idx):
                    linhas_passivo.pop(i); _rebuild_passivo()

                tk.Button(row1, text="✕ Remover", fg="#ff6666", bg="#0f0d2e",
                          bd=0, font=("Arial", 9, "bold"), cursor="hand2",
                          command=_rem_p, activebackground="#1a1040",
                          activeforeground="#ff6666").pack(side="right", padx=4)

                row2 = tk.Frame(bloco, bg="#0f0d2e")
                row2.pack(fill="x", padx=8, pady=(2, 6))
                tk.Label(row2, text="Tag", fg="#8899cc", bg="#0f0d2e",
                         font=("Arial", 9)).pack(side="left", padx=(0, 6))
                opcoes = opcoes_cat(ln["cat"].get())
                tag_cb = ttk.Combobox(row2, textvariable=ln["tag"],
                                      values=opcoes, state="readonly",
                                      font=("Arial", 9), width=22)
                tag_cb.pack(side="left", padx=(0, 14))
                tk.Label(row2, text="Valor", fg="#8899cc", bg="#0f0d2e",
                         font=("Arial", 9)).pack(side="left", padx=(0, 4))
                tk.Entry(row2, textvariable=ln["val"], bg=ENT, fg=FG,
                         insertbackground=FG, relief="flat",
                         font=("Arial", 9), width=8).pack(side="left")
                tk.Label(row2, text="(ex: -3, 10)", fg="#445566", bg="#0f0d2e",
                         font=("Arial", 8, "italic")).pack(side="left", padx=6)

                def _cat_ch(evt, l=ln, cb=tag_cb):
                    novas = opcoes_cat(l["cat"].get())
                    cb["values"] = novas
                    if l["tag"].get() not in novas:
                        l["tag"].set(novas[0] if novas else "")
                cat_cb.bind("<<ComboboxSelected>>", _cat_ch)

        def _add_passivo(cat="Tipos de Teste", tag=None, val="0"):
            ops = opcoes_cat(cat)
            tag_v = tag if tag in ops else (ops[0] if ops else "")
            linhas_passivo.append({"cat": tk.StringVar(value=cat),
                                   "tag": tk.StringVar(value=tag_v),
                                   "val": tk.StringVar(value=str(val))})
            _rebuild_passivo()

        tk.Button(frame_passivo, text="＋  Adicionar Modificador",
                  command=_add_passivo, bg="#1f4a2a", fg="white",
                  relief="flat", padx=10, pady=4, font=("Arial", 9),
                  cursor="hand2").pack(anchor="w", padx=18, pady=(2, 8))

        # ── Sub-frame ATIVO ───────────────────────────────────────────────────
        frame_ativo = tk.Frame(frame_padrao, bg=BG)

        s_dur_pad = section(frame_ativo, "  DURAÇÃO DO EFEITO")
        ent_duracao_pad = lbl_entry(s_dur_pad, "Turnos de duração",
                                    width=8, hint="vazio = instantâneo")

        s_dano_pad = section(frame_ativo, "  DANO  (opcional)")
        linhas_dano_pad = []

        def _rebuild_dano_pad():
            for w in s_dano_pad.winfo_children():
                w.destroy()
            for idx, ln in enumerate(linhas_dano_pad):
                lf = tk.Frame(s_dano_pad, bg="#0f0d2e", relief="ridge", bd=1)
                lf.pack(fill="x", padx=6, pady=3)
                row = tk.Frame(lf, bg="#0f0d2e")
                row.pack(fill="x", padx=8, pady=5)
                tk.Label(row, text="Tipo", fg="#8899cc", bg="#0f0d2e",
                         font=("Arial", 9)).pack(side="left", padx=(0, 4))
                ttk.Combobox(row, textvariable=ln["tipo"], values=TIPOS_DANO,
                             state="readonly", font=("Arial", 9),
                             width=16).pack(side="left", padx=(0, 12))
                tk.Label(row, text="Valor", fg="#8899cc", bg="#0f0d2e",
                         font=("Arial", 9)).pack(side="left", padx=(0, 4))
                tk.Entry(row, textvariable=ln["val"], bg=ENT, fg=FG,
                         insertbackground=FG, relief="flat",
                         font=("Arial", 9), width=8).pack(side="left")

                def _rem_dp(i=idx):
                    linhas_dano_pad.pop(i); _rebuild_dano_pad()

                tk.Button(row, text="✕", command=_rem_dp, bg=RED, fg=FG,
                          relief="flat", width=3,
                          font=("Arial", 8)).pack(side="right", padx=4)

        def _add_dano_pad(tipo="contundente", val="0"):
            linhas_dano_pad.append({"tipo": tk.StringVar(value=tipo),
                                    "val":  tk.StringVar(value=str(val))})
            _rebuild_dano_pad()

        tk.Button(frame_ativo, text="＋  Adicionar Dano", command=_add_dano_pad,
                  bg="#1f3a6a", fg="white", relief="flat", padx=10, pady=4,
                  font=("Arial", 9), cursor="hand2").pack(anchor="w", padx=18, pady=(2, 4))

        s_ef_pad = section(frame_ativo, "  EFEITOS COM CHANCE  (buff/debuff do dicionário)")
        linhas_ef_pad = []

        def _nomes_buffs():
            try:    return list(D.carregar_buffs_debuffs_raw().keys()) or ["—"]
            except: return ["—"]

        def _rebuild_ef_pad():
            for w in s_ef_pad.winfo_children():
                w.destroy()
            nomes_buff = _nomes_buffs()
            for idx, ln in enumerate(linhas_ef_pad):
                lf = tk.Frame(s_ef_pad, bg="#0f0d2e", relief="ridge", bd=1)
                lf.pack(fill="x", padx=6, pady=3)
                row = tk.Frame(lf, bg="#0f0d2e")
                row.pack(fill="x", padx=8, pady=5)
                tk.Label(row, text="Efeito", fg="#8899cc", bg="#0f0d2e",
                         font=("Arial", 9)).pack(side="left", padx=(0, 4))
                if ln["nome"].get() not in nomes_buff and nomes_buff:
                    ln["nome"].set(nomes_buff[0])
                ttk.Combobox(row, textvariable=ln["nome"], values=nomes_buff,
                             font=("Arial", 9), width=18).pack(side="left", padx=(0, 10))
                tk.Label(row, text="Chance%", fg="#8899cc", bg="#0f0d2e",
                         font=("Arial", 9)).pack(side="left", padx=(0, 4))
                tk.Entry(row, textvariable=ln["chance"], bg=ENT, fg=FG,
                         insertbackground=FG, relief="flat",
                         font=("Arial", 9), width=5).pack(side="left", padx=(0, 10))
                tk.Label(row, text="Turnos", fg="#8899cc", bg="#0f0d2e",
                         font=("Arial", 9)).pack(side="left", padx=(0, 4))
                tk.Entry(row, textvariable=ln["duracao"], bg=ENT, fg=FG,
                         insertbackground=FG, relief="flat",
                         font=("Arial", 9), width=5).pack(side="left")

                def _rem_ep(i=idx):
                    linhas_ef_pad.pop(i); _rebuild_ef_pad()

                tk.Button(row, text="✕", command=_rem_ep, bg=RED, fg=FG,
                          relief="flat", width=3,
                          font=("Arial", 8)).pack(side="right", padx=4)

        def _add_ef_pad(nome="", chance=100, duracao=1):
            nomes = _nomes_buffs()
            nome_v = nome if nome in nomes else (nomes[0] if nomes else "")
            linhas_ef_pad.append({"nome":    tk.StringVar(value=nome_v),
                                  "chance":  tk.StringVar(value=str(chance)),
                                  "duracao": tk.StringVar(value=str(duracao))})
            _rebuild_ef_pad()

        tk.Button(frame_ativo, text="＋  Adicionar Efeito", command=_add_ef_pad,
                  bg="#4a2a6a", fg="white", relief="flat", padx=10, pady=4,
                  font=("Arial", 9), cursor="hand2").pack(anchor="w", padx=18, pady=(2, 4))

        s_opt_pad = section(frame_ativo, "  OPÇÕES")
        var_ign_pad = tk.BooleanVar(value=False)
        r_opt_pad = tk.Frame(s_opt_pad, bg=CARD)
        r_opt_pad.pack(fill="x", padx=10, pady=4)
        tk.Checkbutton(r_opt_pad, text="Ignora Resistências", variable=var_ign_pad,
                       bg=CARD, fg=FG, selectcolor="#24195e",
                       activebackground=CARD, activeforeground=FG,
                       font=("Arial", 10)).pack(side="left")

        # ── Lógica passivo ↔ ativo dentro do frame padrão ─────────────────────
        def _atualizar_modo(*_):
            try:    en = int(ent_energia.get() or "0")
            except: en = 0
            try:    mn = int(ent_mana_pad.get() or "0")
            except: mn = 0
            if en == 0 and mn == 0:
                lbl_modo.config(text="▶ MODO: PASSIVO  (modificador permanente)",
                                fg="#55cc88")
                frame_ativo.pack_forget()
                frame_passivo.pack(fill="x")
            else:
                lbl_modo.config(text="▶ MODO: ATIVO  (gasta recurso, causa efeito)",
                                fg="#cc8855")
                frame_passivo.pack_forget()
                frame_ativo.pack(fill="x")

        ent_energia.bind("<KeyRelease>", _atualizar_modo)
        ent_mana_pad.bind("<KeyRelease>", _atualizar_modo)

        # ══════════════════════════════════════════════════════════════════════
        #  FRAME OFENSIVO  (PoderOfensivo / HabilidadeOfensiva)
        # ══════════════════════════════════════════════════════════════════════
        frame_ofensivo = tk.Frame(inner, bg=BG)

        s_custo_of = section(frame_ofensivo, "  CUSTO")
        r_custo_of = tk.Frame(s_custo_of, bg=CARD)
        r_custo_of.pack(fill="x", padx=10, pady=4)
        tk.Label(r_custo_of, text="Energia", bg=CARD, fg="#8899cc",
                 font=("Arial", 10), width=10, anchor="w").pack(side="left")
        ent_energia_of = tk.Entry(r_custo_of, width=6, bg=ENT, fg=FG,
                                  insertbackground=FG, relief="flat",
                                  highlightthickness=1, highlightbackground="#2a1f6a",
                                  highlightcolor=ACC, font=("Arial", 10))
        ent_energia_of.pack(side="left", padx=(4, 20))
        tk.Label(r_custo_of, text="Mana", bg=CARD, fg="#8899cc",
                 font=("Arial", 10), width=8, anchor="w").pack(side="left")
        ent_mana_of = tk.Entry(r_custo_of, width=6, bg=ENT, fg=FG,
                               insertbackground=FG, relief="flat",
                               highlightthickness=1, highlightbackground="#2a1f6a",
                               highlightcolor=ACC, font=("Arial", 10))
        ent_mana_of.pack(side="left", padx=(4, 0))

        s_dano_of = section(frame_ofensivo, "  DANO")
        linhas_dano_of = []

        def _rebuild_dano_of():
            for w in s_dano_of.winfo_children():
                w.destroy()
            for idx, ln in enumerate(linhas_dano_of):
                lf = tk.Frame(s_dano_of, bg="#0f0d2e", relief="ridge", bd=1)
                lf.pack(fill="x", padx=6, pady=3)
                row = tk.Frame(lf, bg="#0f0d2e")
                row.pack(fill="x", padx=8, pady=5)
                tk.Label(row, text="Tipo", fg="#8899cc", bg="#0f0d2e",
                         font=("Arial", 9)).pack(side="left", padx=(0, 4))
                ttk.Combobox(row, textvariable=ln["tipo"], values=TIPOS_DANO,
                             state="readonly", font=("Arial", 9),
                             width=16).pack(side="left", padx=(0, 12))
                tk.Label(row, text="Valor", fg="#8899cc", bg="#0f0d2e",
                         font=("Arial", 9)).pack(side="left", padx=(0, 4))
                tk.Entry(row, textvariable=ln["val"], bg=ENT, fg=FG,
                         insertbackground=FG, relief="flat",
                         font=("Arial", 9), width=8).pack(side="left")
                tk.Label(row, text="de dano", fg="#445566", bg="#0f0d2e",
                         font=("Arial", 8)).pack(side="left", padx=4)

                def _rem_do(i=idx):
                    linhas_dano_of.pop(i); _rebuild_dano_of()

                tk.Button(row, text="✕", command=_rem_do, bg=RED, fg=FG,
                          relief="flat", width=3,
                          font=("Arial", 8)).pack(side="right", padx=4)

        def _add_dano_of(tipo="contundente", val="0"):
            linhas_dano_of.append({"tipo": tk.StringVar(value=tipo),
                                   "val":  tk.StringVar(value=str(val))})
            _rebuild_dano_of()

        tk.Button(frame_ofensivo, text="＋  Adicionar Dano", command=_add_dano_of,
                  bg="#1f3a6a", fg="white", relief="flat", padx=10, pady=4,
                  font=("Arial", 9), cursor="hand2").pack(anchor="w", padx=18, pady=(2, 4))

        s_ef_of = section(frame_ofensivo, "  EFEITOS ADICIONAIS  (buff/debuff do dicionário)")
        linhas_ef_of = []

        def _rebuild_ef_of():
            for w in s_ef_of.winfo_children():
                w.destroy()
            nomes_buff = _nomes_buffs()
            for idx, ln in enumerate(linhas_ef_of):
                lf = tk.Frame(s_ef_of, bg="#0f0d2e", relief="ridge", bd=1)
                lf.pack(fill="x", padx=6, pady=3)
                row = tk.Frame(lf, bg="#0f0d2e")
                row.pack(fill="x", padx=8, pady=5)
                tk.Label(row, text="Efeito", fg="#8899cc", bg="#0f0d2e",
                         font=("Arial", 9)).pack(side="left", padx=(0, 4))
                if ln["nome"].get() not in nomes_buff and nomes_buff:
                    ln["nome"].set(nomes_buff[0])
                ttk.Combobox(row, textvariable=ln["nome"], values=nomes_buff,
                             font=("Arial", 9), width=18).pack(side="left", padx=(0, 10))
                tk.Label(row, text="Chance%", fg="#8899cc", bg="#0f0d2e",
                         font=("Arial", 9)).pack(side="left", padx=(0, 4))
                tk.Entry(row, textvariable=ln["chance"], bg=ENT, fg=FG,
                         insertbackground=FG, relief="flat",
                         font=("Arial", 9), width=5).pack(side="left", padx=(0, 10))
                tk.Label(row, text="Turnos", fg="#8899cc", bg="#0f0d2e",
                         font=("Arial", 9)).pack(side="left", padx=(0, 4))
                tk.Entry(row, textvariable=ln["duracao"], bg=ENT, fg=FG,
                         insertbackground=FG, relief="flat",
                         font=("Arial", 9), width=5).pack(side="left")

                def _rem_eo(i=idx):
                    linhas_ef_of.pop(i); _rebuild_ef_of()

                tk.Button(row, text="✕", command=_rem_eo, bg=RED, fg=FG,
                          relief="flat", width=3,
                          font=("Arial", 8)).pack(side="right", padx=4)

        def _add_ef_of(nome="", chance=100, duracao=1):
            nomes = _nomes_buffs()
            nome_v = nome if nome in nomes else (nomes[0] if nomes else "")
            linhas_ef_of.append({"nome":    tk.StringVar(value=nome_v),
                                 "chance":  tk.StringVar(value=str(chance)),
                                 "duracao": tk.StringVar(value=str(duracao))})
            _rebuild_ef_of()

        tk.Button(frame_ofensivo, text="＋  Adicionar Efeito", command=_add_ef_of,
                  bg="#4a2a6a", fg="white", relief="flat", padx=10, pady=4,
                  font=("Arial", 9), cursor="hand2").pack(anchor="w", padx=18, pady=(2, 4))

        s_opt_of = section(frame_ofensivo, "  OPÇÕES")
        var_ign_of = tk.BooleanVar(value=False)
        r_opt_of = tk.Frame(s_opt_of, bg=CARD)
        r_opt_of.pack(fill="x", padx=10, pady=4)
        tk.Checkbutton(r_opt_of, text="Ignora Resistências", variable=var_ign_of,
                       bg=CARD, fg=FG, selectcolor="#24195e",
                       activebackground=CARD, activeforeground=FG,
                       font=("Arial", 10)).pack(side="left")

        # ══════════════════════════════════════════════════════════════════════
        #  LÓGICA DE VISIBILIDADE  padrão ↔ ofensivo
        # ══════════════════════════════════════════════════════════════════════
        def _toggle_subtipo(*_):
            if var_subtipo.get() == "ofensivo":
                frame_padrao.pack_forget()
                frame_ofensivo.pack(fill="x")
            else:
                frame_ofensivo.pack_forget()
                frame_padrao.pack(fill="x")
                _atualizar_modo()

        var_subtipo.trace_add("write", _toggle_subtipo)

        # ══════════════════════════════════════════════════════════════════════
        #  PREENCHER se editando
        # ══════════════════════════════════════════════════════════════════════
        if editando:
            ent_nome.insert(0, item.nome)
            ent_desc.insert(0, getattr(item, "descricao", ""))

            if eh_ofensivo:
                # PoderOfensivo / HabilidadeOfensiva
                ent_energia_of.insert(0, str(item.custo_energia))
                ent_mana_of.insert(0, str(item.custo_mana))
                for d in item.dano:
                    _add_dano_of(d.get("tipo", "contundente"), d.get("valor", 0))
                for ef in item.efeitos:
                    _add_ef_of(ef.get("nome", ""), ef.get("chance", 100), ef.get("duracao", 1))
                var_ign_of.set(item.ignora_resistencias)
            else:
                # Poder / Habilidade  (passivo ou ativo)
                ent_energia.insert(0, str(item.custo))
                ent_mana_pad.insert(0, str(getattr(item, "custo_mana", 0)))
                if item.tipo == "passivo":
                    tags = item.tags if isinstance(item.tags, list) else [item.tags]
                    vals = item.valor if isinstance(item.valor, list) else [item.valor] * len(tags)
                    for t, v in zip(tags, vals):
                        _add_passivo(cat=detectar_cat(t), tag=t, val=str(v))
                else:
                    if getattr(item, "duracao", None):
                        ent_duracao_pad.insert(0, str(item.duracao))
                    for d in getattr(item, "dano", []):
                        _add_dano_pad(d.get("tipo", "contundente"), d.get("valor", 0))
                    for ef in getattr(item, "efeitos_ativos", []):
                        _add_ef_pad(ef.get("nome", ""), ef.get("chance", 100), ef.get("duracao", 1))
                    var_ign_pad.set(getattr(item, "ignora_resistencias", False))
        else:
            _add_passivo()      # novo padrão começa com 1 modificador em branco
            _add_dano_of()      # novo ofensivo começa com 1 dano em branco

        # Estado inicial dos frames
        _toggle_subtipo()
        _atualizar_modo()

        # ══════════════════════════════════════════════════════════════════════
        #  SALVAR
        # ══════════════════════════════════════════════════════════════════════
        def salvar():
            nome = ent_nome.get().strip()
            if not nome:
                messagebox.showwarning("Erro", "Nome é obrigatório.", parent=popup)
                return

            desc    = ent_desc.get().strip()
            cat     = var_cat.get()
            ofensivo = var_subtipo.get() == "ofensivo"

            # Remove item antigo se editando
            if editando:
                if eh_ofensivo:
                    if cat == "habilidade":
                        self.character.habilidades.remover_habilidade_ofensiva(item.nome)
                    else:
                        self.character.poderes.remover_poder_ofensivo(item.nome)
                else:
                    if cat == "habilidade":
                        self.character.habilidades.remover_habilidade(item.nome)
                    else:
                        self.character.poderes.remover_poder(item.nome)

            # ── Salvar OFENSIVO ───────────────────────────────────────────────
            if ofensivo:
                try:    en = int(ent_energia_of.get() or "0")
                except: en = 0
                try:    mn = int(ent_mana_of.get() or "0")
                except: mn = 0

                if not linhas_dano_of:
                    messagebox.showwarning("Erro", "Adicione ao menos um tipo de dano.",
                                           parent=popup)
                    return

                danos = []
                for ln in linhas_dano_of:
                    try:    v = int(ln["val"].get())
                    except: v = 0
                    danos.append({"tipo": ln["tipo"].get(), "valor": v})

                efeitos = []
                for ln in linhas_ef_of:
                    n_ef = ln["nome"].get().strip()
                    if not n_ef or n_ef == "—": continue
                    try:    ch = int(ln["chance"].get())
                    except: ch = 100
                    try:    d_ef = int(ln["duracao"].get())
                    except: d_ef = 1
                    efeitos.append({"nome": n_ef, "chance": ch, "duracao": d_ef})

                kwargs = dict(nome=nome, descricao=desc, custo_energia=en,
                              custo_mana=mn, dano=danos, efeitos=efeitos,
                              ignora_resistencias=var_ign_of.get())
                if cat == "habilidade":
                    self.character.habilidades.adicionar_habilidade_ofensiva(
                        CB.HabilidadeOfensiva(**kwargs))
                else:
                    self.character.poderes.adicionar_poder_ofensivo(
                        CB.PoderOfensivo(**kwargs))

            # ── Salvar PADRÃO (passivo / ativo) ───────────────────────────────
            else:
                try:    en = int(ent_energia.get() or "0")
                except: en = 0
                try:    mn = int(ent_mana_pad.get() or "0")
                except: mn = 0
                passivo = (en == 0 and mn == 0)

                if passivo:
                    if not linhas_passivo:
                        messagebox.showwarning("Erro", "Adicione ao menos um modificador.",
                                               parent=popup)
                        return
                    tags_lista, valor_lista = [], []
                    for ln in linhas_passivo:
                        t = ln["tag"].get().strip()
                        if not t:
                            messagebox.showwarning("Erro",
                                                   "Selecione uma tag em todos os modificadores.",
                                                   parent=popup)
                            return
                        try:    v = int(ln["val"].get())
                        except:
                            try:    v = float(ln["val"].get())
                            except:
                                messagebox.showwarning("Erro",
                                                       f"Valor inválido na tag '{t}'.",
                                                       parent=popup)
                                return
                        tags_lista.append(t)
                        valor_lista.append(v)

                    if cat == "habilidade":
                        self.character.habilidades.adicionar_habilidade(
                            nome, "passivo", 0, tags_lista, valor_lista, False, None, desc)
                    else:
                        self.character.poderes.adicionar_poder(
                            nome, "passivo", 0, tags_lista, valor_lista, False, None, desc)

                else:  # ativo
                    try:    dur = int(ent_duracao_pad.get()) if ent_duracao_pad.get().strip() else None
                    except: dur = None

                    danos = []
                    for ln in linhas_dano_pad:
                        try:    v = int(ln["val"].get())
                        except: v = 0
                        danos.append({"tipo": ln["tipo"].get(), "valor": v})

                    efeitos = []
                    for ln in linhas_ef_pad:
                        n_ef = ln["nome"].get().strip()
                        if not n_ef or n_ef == "—": continue
                        try:    ch = int(ln["chance"].get())
                        except: ch = 100
                        try:    d_ef = int(ln["duracao"].get())
                        except: d_ef = 1
                        efeitos.append({"nome": n_ef, "chance": ch, "duracao": d_ef})

                    if cat == "habilidade":
                        obj = CB.Habilidade(
                            nome=nome, tipo="ativo", custo=en, custo_mana=mn,
                            tags=[], valor=0, descricao=desc, duracao=dur,
                            dano=danos, efeitos_ativos=efeitos,
                            ignora_resistencias=var_ign_pad.get())
                        self.character.habilidades.adicionar_habilidade_objeto(obj)
                    else:
                        obj = CB.Poder(
                            nome=nome, tipo="ativo", custo=en, custo_mana=mn,
                            tags=[], valor=0, descricao=desc, duracao=dur,
                            dano=danos, efeitos_ativos=efeitos,
                            ignora_resistencias=var_ign_pad.get())
                        self.character.poderes.adicionar_poder_objeto(obj)

            self.refresh_habilidades()
            popup.destroy()

        # ── barra de botões ───────────────────────────────────────────────────
        bbar = tk.Frame(popup, bg="#090720", height=52)
        bbar.pack(fill="x", side="bottom")
        bbar.pack_propagate(False)
        tk.Button(bbar, text="  ✕  Cancelar  ", command=popup.destroy,
                  bg=RED, fg="white", relief="flat",
                  font=("Arial", 10, "bold"), cursor="hand2",
                  pady=6).pack(side="right", padx=10, pady=8)
        tk.Button(bbar, text="  ✦  Salvar  ", command=salvar,
                  bg=GRN, fg="white", relief="flat",
                  font=("Arial", 10, "bold"), cursor="hand2",
                  pady=6).pack(side="right", padx=(0, 6), pady=8)

        ent_nome.focus_set()
        popup.transient(self)
        popup.grab_set()

    def _abrir_popup_rolagem(self):
            abrir_popup_rolagem_personagem(self, self.character)
    
    def _abrir_popup_loot_combate(self):
        char = self.personagem_no_card
        if not char:
            self.adicionar_log("Selecione um personagem no card primeiro.", "gray")
            return
        abrir_popup_loot(self, char, D, on_finish=self.refresh)

    def abrir_popup_efeito(self, efeito=None):
        if not self.character: return
        editando=efeito is not None
        popup=tk.Toplevel(self); popup.title("Editar Efeito" if editando else "Adicionar Efeito"); popup.geometry("520x360"); popup.configure(bg="#130f26"); popup.resizable(False,False)
        tk.Label(popup,text="Efeito" if not editando else f"Editar: {efeito.nome}",font=("Arial",18,"bold"),bg="#1a0869",fg="white").pack(fill="x",pady=10)
        frame=tk.Frame(popup,bg="#1a0869"); frame.pack(padx=15,pady=10,fill="both",expand=True)

        buffs_debuffs_disponiveis=D.carregar_buffs_debuffs()
        nomes_buffs=list(buffs_debuffs_disponiveis.keys())
        tk.Label(frame,text="Escolha um Efeito",bg="#1a0869",fg="white").pack(anchor="w")
        var_efeito=tk.StringVar(value=efeito.nome if editando else (nomes_buffs[0] if nomes_buffs else ""))
        efeito_menu=tk.OptionMenu(frame,var_efeito,*nomes_buffs); efeito_menu.configure(bg="#1a0869",fg="white"); efeito_menu["menu"].configure(bg="#2a1f4a",fg="white"); efeito_menu.pack(fill="x")

        tk.Label(frame,text="Duração (turnos, 0 = imediato, 'permanente')",bg="#1a0869",fg="white").pack(anchor="w")
        entry_duracao=tk.Entry(frame,width=20); entry_duracao.pack()
        if editando: entry_duracao.insert(0,efeito.duracao)

        def salvar():
            nome_escolhido=var_efeito.get().strip()
            if not nome_escolhido: return
            duracao_raw=entry_duracao.get().strip() or "0"
            if duracao_raw.lower()=="permanente": duracao="permanente"
            else:
                try: duracao_int=int(duracao_raw); duracao=duracao_int if duracao_int>0 else 0
                except: duracao=1

            dados_efeito=buffs_debuffs_disponiveis.get(nome_escolhido)
            if not dados_efeito: return

            if editando: self.character.buffs_debuffs.remover_efeito(efeito.nome)

            self.character.buffs_debuffs.adicionar_efeito(
                nome_escolhido,
                duracao,
                dados_efeito.get("efeito"),
                dados_efeito.get("descricao"),
                dados_efeito.get("tipo")
            )

            self.refresh_efeitos(); self.refresh_info_basica(); popup.destroy()

        tk.Button(frame,text="Salvar",command=salvar,bg="#115c11",fg="white").pack(pady=10)
        popup.transient(self); popup.grab_set()

    def abrir_popup_usar_area(self, item_obj):
        popup = tk.Toplevel(self)
        popup.title(f"Usar em Área — {item_obj.nome}")
        popup.geometry("560x600")
        popup.configure(bg="#130f26")
        popup.resizable(False, False)

        BG, FG, ENT = "#1a0869", "white", "#0d0730"

        tk.Label(
            popup, text=f"💥 {item_obj.nome}",
            font=("Arial", 16, "bold"), bg="#0a0433", fg="#b79cff"
        ).pack(fill="x", pady=10)

        # ── Info de área: suporta formato antigo (atributos) e novo (efeitos) ──
        # Coleta todos os efeitos dano_area presentes
        efeitos_area = []
        for ef in getattr(item_obj, "efeitos", []):
            if isinstance(ef, dict) and ef.get("tipo") == "dano_area":
                efeitos_area.append(ef)

        # Formato antigo: raio no próprio objeto
        raio_antigo     = getattr(item_obj, "raio",       None)
        letal_antigo    = getattr(item_obj, "raio_letal", None)
        falloff_antigo  = getattr(item_obj, "falloff",    "linear")
        perf_antigo     = getattr(item_obj, "perfuracao", 0)

        if efeitos_area:
            # Novo formato: exibe info do primeiro efeito de área
            ef0 = efeitos_area[0]
            raio    = ef0.get("raio", 0)
            letal   = ef0.get("raio_letal") or round(raio * 0.3, 1)
            falloff = ef0.get("falloff", "linear")
            perf    = ef0.get("perfuracao", 0)

            if len(efeitos_area) == 1:
                info_txt = (
                    f"Raio: {raio}m  |  Letal: {letal}m  |  "
                    f"Falloff: {falloff}  |  Perf.: {perf}"
                )
            else:
                partes = [
                    f"Efeito {i+1}: raio {e.get('raio',0)}m / "
                    f"{e.get('subtipo','?')} {e.get('valor',0)}"
                    for i, e in enumerate(efeitos_area)
                ]
                info_txt = "  |  ".join(partes)
        elif raio_antigo:
            # Formato antigo
            raio    = raio_antigo
            letal   = letal_antigo or round(raio * 0.3, 1)
            falloff = falloff_antigo
            perf    = perf_antigo
            info_txt = (
                f"Raio: {raio}m  |  Letal: {letal}m  |  "
                f"Falloff: {falloff}  |  Perf.: {perf}"
            )
        else:
            info_txt = "Efeito de área (sem dados de raio)"

        tk.Label(
            popup, text=info_txt,
            bg="#130f26", fg="#aaaaaa", font=("Arial", 9)
        ).pack()

        # ── Efeitos de buff/debuff que serão aplicados junto ──────────────────
        efeitos_buff = [
            ef for ef in getattr(item_obj, "efeitos", [])
            if isinstance(ef, dict) and ef.get("tipo") in ("buff", "debuff")
        ]
        if efeitos_buff:
            nomes_buffs = ", ".join(
                f"{ef.get('nome','?')} ({ef.get('chance',100)}% / {ef.get('duracao',1)}t)"
                for ef in efeitos_buff
            )
            tk.Label(
                popup,
                text=f"Efeitos adicionais: {nomes_buffs}",
                bg="#130f26", fg="#a0d4a0", font=("Arial", 8, "italic"),
                wraplength=530
            ).pack(pady=(0, 4))

        frame = tk.Frame(popup, bg=BG, bd=2, relief="ridge")
        frame.pack(padx=12, pady=6, fill="both", expand=True)

        # ── Cobertura ─────────────────────────────────────────────────────────
        row_cob = tk.Frame(frame, bg=BG)
        row_cob.pack(fill="x", pady=6, padx=8)
        tk.Label(
            row_cob, text="Cobertura dos alvos:",
            bg=BG, fg=FG, width=20, anchor="w"
        ).pack(side="left")
        var_cob = tk.StringVar(value="Nenhuma")
        for op in ("Nenhuma", "Parcial", "Alta", "Total"):
            tk.Radiobutton(
                row_cob, text=op, variable=var_cob, value=op,
                bg=BG, fg=FG, selectcolor="#24195e",
                activebackground=BG, activeforeground=FG,
                indicatoron=0, width=8, bd=1, relief="ridge"
            ).pack(side="left", padx=2)

        # ── Buff/Debuff de dano ───────────────────────────────────────────────
        row_mod = tk.Frame(frame, bg=BG)
        row_mod.pack(fill="x", pady=4, padx=8)
        tk.Label(row_mod, text="Buff de dano:", bg=BG, fg=FG, width=14, anchor="w").pack(side="left")
        entry_buff = tk.Entry(row_mod, width=6, bg=ENT, fg=FG, insertbackground=FG)
        entry_buff.insert(0, "0")
        entry_buff.pack(side="left", padx=4)
        tk.Label(row_mod, text="Debuff de dano:", bg=BG, fg=FG).pack(side="left", padx=(12, 4))
        entry_debuff = tk.Entry(row_mod, width=6, bg=ENT, fg=FG, insertbackground=FG)
        entry_debuff.insert(0, "0")
        entry_debuff.pack(side="left")

        # ── Alvos ─────────────────────────────────────────────────────────────
        tk.Frame(frame, bg="#2a1f6a", height=1).pack(fill="x", pady=8)
        tk.Label(
            frame, text="Alvos e distâncias (metros):",
            bg=BG, fg=FG, font=("Arial", 11, "bold")
        ).pack(anchor="w", padx=8)

        todos_personagens = [p for lista in D.GruposDePersonagens.values() for p in lista]

        linhas_alvos = []
        frame_alvos = tk.Frame(frame, bg="#150b52", bd=1, relief="ridge")
        frame_alvos.pack(fill="x", padx=8, pady=4)

        def adicionar_linha_alvo(personagem=None, dist="0"):
            lf = tk.Frame(frame_alvos, bg="#150b52")
            lf.pack(fill="x", pady=3, padx=4)
            var_alvo = tk.StringVar(
                value=personagem.nome if personagem
                else (todos_personagens[0].nome if todos_personagens else "")
            )
            nomes = [p.nome for p in todos_personagens]
            om = tk.OptionMenu(lf, var_alvo, *nomes)
            om.config(bg="#2a1f6a", fg=FG, width=20, relief="flat")
            om["menu"].config(bg="#2a1f4a", fg=FG)
            om.pack(side="left", padx=(0, 6))
            ev = tk.Entry(lf, width=6, bg=ENT, fg=FG, insertbackground=FG)
            ev.insert(0, str(dist))
            ev.pack(side="left", padx=(0, 4))
            tk.Label(lf, text="m", bg="#150b52", fg="#888888", font=("Arial", 9)).pack(side="left")
            entrada = (var_alvo, ev, lf)

            def remover():
                linhas_alvos.remove(entrada)
                lf.destroy()

            tk.Button(
                lf, text="✕", command=remover,
                bg="#5c1111", fg=FG, relief="ridge", bd=1, width=3
            ).pack(side="left", padx=(8, 0))
            linhas_alvos.append(entrada)

        tk.Button(
            frame, text="＋ Adicionar alvo",
            command=adicionar_linha_alvo,
            bg="#1f5c1f", fg="white", relief="ridge", bd=1, padx=8
        ).pack(anchor="w", padx=8)

        if todos_personagens:
            adicionar_linha_alvo(todos_personagens[0], "0")

        # ── Resultado ─────────────────────────────────────────────────────────
        tk.Frame(frame, bg="#2a1f6a", height=1).pack(fill="x", pady=8)
        label_resultado = tk.Label(
            frame, text="",
            bg=BG, fg="#90caf9", font=("Arial", 9),
            wraplength=500, justify="left"
        )
        label_resultado.pack(anchor="w", padx=8)

        # ── Simular / Usar ────────────────────────────────────────────────────
        def simular(aplicar: bool):
            try:
                buff_val   = int(entry_buff.get().strip()   or 0)
                debuff_val = int(entry_debuff.get().strip() or 0)
            except:
                buff_val = debuff_val = 0

            mapa = {p.nome: p for p in todos_personagens}
            alvos_dist = []
            for var_a, ev_d, _ in linhas_alvos:
                p = mapa.get(var_a.get())
                if not p:
                    continue
                try:
                    d = float(ev_d.get().strip())
                except:
                    d = 0.0
                alvos_dist.append((p, d))

            if not alvos_dist:
                label_resultado.config(
                    text="Adicione ao menos um alvo.", fg="#ff9999"
                )
                return

            # ── Chama o sistema de combate para o dano em área ────────────────
            res = CB.usar_consumivel(
                item_obj, self.character,
                alvos_distancias=alvos_dist,
                cobertura=var_cob.get(),
                BuffDano=buff_val,
                DebuffDano=debuff_val,
                aplicar=aplicar
            )

            linhas_log = list(res.get("log", []))

            if res.get("resultado_area"):
                for entrada in res["resultado_area"].get("alvos", []):
                    if entrada.get("regioes"):
                        linhas_log.append(
                            "  " + " | ".join(
                                f"{r['regiao']}: {r['dano_final']}"
                                for r in entrada["regioes"]
                            )
                        )

            # ── Aplica buffs/debuffs do consumível em cada alvo atingido ──────
            if aplicar and efeitos_buff:
                for alvo_obj, distancia in alvos_dist:
                    # Calcula mult_chance por falloff/raio se disponível
                    mult = 1.0
                    if efeitos_area:
                        ef0 = efeitos_area[0]
                        raio_ef    = ef0.get("raio", 0)
                        raio_letal = ef0.get("raio_letal") or round(raio_ef * 0.3, 1)
                        falloff_ef = ef0.get("falloff", "linear")

                        if raio_ef > 0 and distancia > raio_letal:
                            proporcao = max(
                                0.0,
                                1.0 - (distancia - raio_letal) / max(raio_ef - raio_letal, 1)
                            )
                            if falloff_ef == "quadratico":
                                mult = proporcao ** 2
                            elif falloff_ef == "linear":
                                mult = proporcao
                            # "nenhum" → mult permanece 1.0

                    aplicados = aplicar_efeitos_item(efeitos_buff, alvo_obj, mult_chance=mult)
                    if aplicados:
                        linhas_log.append(
                            f"  {alvo_obj.nome} ← {', '.join(aplicados)}"
                        )

            label_resultado.config(
                text="\n".join(linhas_log) if linhas_log else "Sem log.",
                fg="#90caf9"
            )

            if aplicar:
                self.refresh()
                popup.destroy()

        btn_frame = tk.Frame(popup, bg="#130f26")
        btn_frame.pack(pady=8)
        tk.Button(
            btn_frame, text="🔍 Simular (sem aplicar)",
            command=lambda: simular(False),
            bg="#1a3060", fg="white", font=("Arial", 11), padx=10
        ).pack(side="left", padx=8)
        tk.Button(
            btn_frame, text="💥 Usar!",
            command=lambda: simular(True),
            bg="#6b1a1a", fg="white", font=("Arial", 11, "bold"), padx=14
        ).pack(side="left", padx=8)

        popup.transient(self)
        popup.grab_set()

    def alterar_nivel(self, delta):
        if delta > 0:
            self.character.Nivel += 1
        else:
            self.character.Nivel = max(self.character.Nivel - 1, 1)
        self.character.recalcularAtributos()
        self.refresh()

    def alterar_atributo(self, nome_atributo, delta):
        valor_atual = getattr(self.character, nome_atributo)
        novo_valor = max(valor_atual + delta, 0)
        setattr(self.character, nome_atributo, novo_valor)
        self.character.recalcularAtributos()
        self.refresh()
    ## funções dos botões extras ##
    
    def _gerar_texto_tooltip_item(self, item):
        linhas = [f"✦ {getattr(item, 'nome', 'Desconhecido')}"]

        if isinstance(item, CB.Melee):
            linhas += [f"Tipo: Melee | Raridade: {item.raridade}", f"Dano: {item.dano}  |  Crítico: {item.valor_critico}+ (x{item.critico_multiplicador})", f"Alcance: {item.alcance}  |  Mãos: {item.maos}  |  Peso: {item.peso}", f"Tags: {', '.join(sorted(item.tags)) or '—'}"]
            if item.tipo_dano: linhas.append(f"Tipo de Dano: {item.tipo_dano}")
            if item.ignora_armadura: linhas.append(f"Ignora Armadura: {item.ignora_armadura}")
            linhas.append("\n[Clique → menu]  [Shift+Clique → detalhes completos]")

        elif isinstance(item, CB.Ranged):
            linhas += [f"Tipo: {item.classe} | Raridade: {item.raridade}", f"Dano: {item.dano}  |  Calibre: {item.calibre}  |  Peso: {item.peso}", f"Munições: {item.munições}/{item.capacidade}  ({item.municao.nome if item.municao else 'Descarregada'})", f"Alcance: {item.MinRange}–{item.MaxRange}m  |  Recuo: {item.recuo}", f"Crítico: Curto {item.ShortCrit}+  Médio {item.MediumCrit}+  Longo {item.LongCrit}+"]
            linhas.append("\n[Clique → menu]  [Shift+Clique → detalhes completos]")

        elif self.character._eh_protecao(item):
            linhas += [f"Tipo: Proteção  |  Peso: {item.peso}", f"Regiões: {', '.join(item.regioes_cobertas)}", f"Nível Balístico: {item.nivelBalistico}  |  Durabilidade: {item.durabilidade}/{item.durabilidadeMax}"]
            abs_resumo = "  ".join(f"{k}: {v}" for k, v in item.absorcoes.items())
            if abs_resumo: linhas.append(f"Absorções: {abs_resumo}")
            linhas.append("\n[Clique → menu]  [Shift+Clique → detalhes completos]")

        elif isinstance(item, CB.Consumivel):
            linhas.append(f"Tipo: Consumível  |  Peso: {getattr(item, 'peso', '—')}")
            if hasattr(item, 'descricao') and item.descricao: linhas.append(item.descricao)
            if item.eh_area():
                linhas.append(f"💥 Área: raio {item.raio}m  |  letal {item.raio_letal or round(item.raio * 0.3, 1)}m  |  falloff: {item.falloff}")
                linhas.append("[Clique → menu]  [Shift+Clique → detalhes completos]")
            else:
                efeitos_resumo = []
                for e in item.efeitos:
                    tipo = e.get("tipo", "")
                    if tipo == "cura": efeitos_resumo.append(f"Cura: +{e.get('valor', 0)}")
                    elif tipo == "energia": efeitos_resumo.append(f"Energia: +{e.get('valor', 0)}")
                    elif tipo == "mana": efeitos_resumo.append(f"Mana: +{e.get('valor', 0)}")
                    elif tipo == "dano": efeitos_resumo.append(f"Dano ({e.get('subtipo','?')}): {e.get('valor', 0)}")
                    elif tipo in ("buff", "debuff"): efeitos_resumo.append(f"{tipo.capitalize()}: {e.get('nome','')}")
                if efeitos_resumo: linhas.append("Efeitos: " + "  |  ".join(efeitos_resumo))

        elif isinstance(item, CB.Municao):
            linhas += [f"Tipo: Munição  |  Calibre: {item.calibre}", f"Dano Extra: {item.dano}  |  Tipo: {item.tipo_dano}  |  Perfuração: {item.perfuracao}"]
            if item.efeitos: linhas.append(f"Efeitos: {', '.join(str(e) for e in item.efeitos)}")

        elif isinstance(item, CB.Melhoria):
            linhas += [f"Tipo: Melhoria ({item.tipo})  |  Peso: {item.peso}"]
            mods_resumo = "  ".join(f"{k}: {'+' if v > 0 else ''}{v}" for k, v in item.modificadores.items() if k not in ("add_tags", "remove_tags") and v != 0)
            if mods_resumo: linhas.append(f"Mods: {mods_resumo}")
            if item.modificadores.get("add_tags"): linhas.append(f"Adiciona Tags: {', '.join(item.modificadores['add_tags'])}")
            if item.modificadores.get("remove_tags"): linhas.append(f"Remove Tags: {', '.join(item.modificadores['remove_tags'])}")

        elif isinstance(item, CB.Equipamento):
            linhas.append(f"Tipo: Equipamento  |  Peso: {item.peso}")
            if item.slots_criados: linhas.append(f"Slots criados: {len(item.slots_criados)}")

        else:
            if hasattr(item, 'descricao') and item.descricao: linhas.append(item.descricao)
            if hasattr(item, 'peso'): linhas.append(f"Peso: {item.peso}")

        return "\n".join(linhas)
### TELA DE DETALHES ###
### TELA DE DETALHES ###
### TELA DE DETALHES ###

### TELA DE COMBATE ###
### TELA DE COMBATE ###
### TELA DE COMBATE ###
class CombatSystemScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(bg='#130f26')
        self.controller = controller
        self._estado_mapa: dict = {}
        self.distancias_mapa: dict = {}
        self.coberturas_mapa: dict = {}
        
        # Inicializar variáveis de grupo como None
        self.grupo_esquerdo = None
        self.grupo_direito = None
        
        self.slot_esquerdo_personagem = None
        self.slot_direito_personagem = None
        
        # Variável para controlar o turno atual
        self.ordem_turno = []
        self.turno_atual_index = 0
        self.log_historico = []
        self.personagem_no_card = None

        tk.Button(self, text="Tela inicial", height=2, command=self.TelaInicial, bg="#1a0869", fg="white", font=("Arial", 20)).place(x=20, y=10, width=350, height=75)
        
        tk.Button(self, text="Seleção", height=2, command=self.TelaDeSelecao, bg="#1a0869", fg="white", font=("Arial", 20)).place(x=385, y=10, width=350, height=75)

        tk.Label(self, text="Combate", fg="white", bg="#1a0869", font=("Arial", 20, "bold"), width=20, height=2).place(x=870, y=10, width=350, height=75)

        tk.Button(self, text="Informações", height=2, command=self.TelaDeRegrasEItens, bg="#1a0869", fg="white", font=("Arial", 20)).place(x=1235, y=10, width=350, height=75)

        # --- Controles de Turno (NOVO) ---
        self.criar_controles_turno()
        
        # --- Fila de Ordem de Turno (NOVO) ---
        self.criar_fila_turno()

        # --- Log de Combate ---
        self.criar_log_combate()

        # --- Criar seletores de grupos e listas ---
        self.criar_interface_grupos()

    ### Turnos ###
    def criar_controles_turno(self):
        """Cria os botões de controle de turno"""
        tk.Button(self, text="Passar Turno", bg="#1a0869", fg="white",font=("Arial", 10, "bold"),command=self.passar_turno).place(x=450, y=100, width=100, height=50)
        tk.Button(self, text="Encerrar\nTurno Geral", bg="#4a0030", fg="white",font=("Arial", 10, "bold"),command=self.encerrar_turno_geral).place(x=450, y=150, width=100, height=50)
        tk.Button(self, text="Iniciativa", bg="#1a0869", fg="white",font=("Arial", 10, "bold"),command=self.abrir_popup_iniciativa).place(x=1050, y=150, width=100, height=50)
        tk.Button(self, text="Personagens", bg="#1a0869", fg="white",font=("Arial", 10, "bold"),command=self.abrir_popup_selecao_listas).place(x=1050, y=100, width=100, height=50)
        tk.Button(self, text="🎲 Rolagem ", bg="#1a0869", fg="white",font=("Arial", 10, "bold"),command=self._abrir_popup_rolagem_grupo).place(x=450, y=205, width=110, height=40)
        tk.Button(self, text="Vida/Energia/Mana", bg="#5a189a", fg="white", font=("Arial", 10, "bold"), command=self.abrir_popup_ajuste_global).place(x=565, y=205, width=150, height=40)
        tk.Button(self, text="Mapa", bg="#0a3d5c", fg="white",font=("Arial", 10, "bold"),command=self._ir_para_mapa).place(x=720, y=205, width=80, height=40)
        tk.Button(self, text="Pilhagem", bg="#4a2200", fg="white", font=("Arial", 10, "bold"),command=self.abrir_popup_pilhagem_central).place(x=805, y=205, width=110, height=40)
        tk.Button(self, text="💰 Loot", bg="#4a2200", fg="white",font=("Arial", 10, "bold"),command=self._abrir_popup_loot_combate).place(x=920, y=205, width=80, height=40)
        
    def criar_fila_turno(self):
        """Cria a fila de ordem de turno no centro superior"""
        # Frame principal da fila com borda amarela
        self.fila_frame = tk.Frame(self, bg="#1a0869", relief="solid", bd=3)
        self.fila_frame.place(x=550, y=100, width=500, height=100)
        
        # Frame interno (fundo escuro)
        fila_inner = tk.Frame(self.fila_frame, bg="#1a0869")
        fila_inner.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Label do título
        tk.Label(fila_inner, text="Fila de ordem e turno atual", bg="#1a0869", fg="white", font=("Arial", 12, "bold")).pack()
        
        # Frame para o canvas com scroll horizontal
        canvas_frame = tk.Frame(fila_inner, bg='#1a0869')
        canvas_frame.pack(fill="both", expand=True, padx=3, pady=(0, 3))
        
        # Canvas para scroll horizontal
        self.fila_canvas = tk.Canvas(canvas_frame, bg="#130f26", highlightthickness=0, height=20)
        self.fila_canvas.pack(fill="both", expand=True)
        
        # Frame interno para os cards de personagens
        self.fila_inner_frame = tk.Frame(self.fila_canvas, bg="#130f26")
        self.fila_canvas.create_window((0, 0), window=self.fila_inner_frame, anchor='nw')
        self.fila_inner_frame.bind("<Configure>", lambda e: self.fila_canvas.configure(scrollregion=self.fila_canvas.bbox("all")))
        
        # Inicializar fila vazia
        self.atualizar_fila_turno()

    def atualizar_fila_turno(self):
        """Atualiza a exibição da fila de turno. Cards são botões clicáveis."""
        for widget in self.fila_inner_frame.winfo_children():
            widget.destroy()
        if not self.ordem_turno:
            tk.Label(self.fila_inner_frame, text="Aguardando iniciativa...",bg="#130f26", fg="gray", font=("Arial", 9)).pack(side="left", padx=5)
            return
        for idx, personagem in enumerate(self.ordem_turno):
            is_atual = (idx == self.turno_atual_index)
            bg_color = "#2d0a8c" if is_atual else "#1a0869"
            fg_color = "yellow" if is_atual else "white"
            indicador = "▶ " if is_atual else ""
            iniciativa = getattr(personagem, "iniciativa_atual", "?")

            card = tk.Frame(self.fila_inner_frame, bg=bg_color,relief="solid", bd=2 if is_atual else 1)
            card.pack(side="left", padx=4, pady=4)

            btn = tk.Button(card,text=f"{indicador}{personagem.nome} ({iniciativa})",bg=bg_color, fg=fg_color, font=("Arial", 9, "bold"),relief="flat", cursor="hand2",activebackground="#4a1aac", activeforeground="white",command=lambda p=personagem: self._mostrar_personagem_no_card(p))
            btn.pack(padx=6, pady=4)

            if idx < len(self.ordem_turno) - 1:
                tk.Label(self.fila_inner_frame, text="→",bg="#130f26", fg="gray",font=("Arial", 12, "bold")).pack(side="left", padx=2)
    
    def passar_turno(self):
        """Avança para o próximo personagem da fila. Se for o último, encerra o turno geral."""
        if not self.ordem_turno:
            self.adicionar_log("Nenhuma ordem de turno definida.", "gray")
            return

        eh_ultimo = (self.turno_atual_index >= len(self.ordem_turno) - 1)

        if eh_ultimo:
            self.encerrar_turno_geral()
        else:
            personagem_atual = self.ordem_turno[self.turno_atual_index]
            self.turno_atual_index += 1
            proximo = self.ordem_turno[self.turno_atual_index]

            self.adicionar_log(f"Turno de {personagem_atual.nome} encerrado.", "gray")
            self.adicionar_log(f"▶ Vez de {proximo.nome} (Iniciativa: {getattr(proximo, 'iniciativa_atual', '?')})", "yellow")

            self.atualizar_fila_turno()
            self.atualizar_card_turno_atual()

    def encerrar_turno_geral(self):
        """Encerra o turno geral e volta para o primeiro personagem da fila."""
        if not self.ordem_turno:
            self.adicionar_log("Nenhuma ordem de turno definida.", "gray")
            return

        # Processar turno de todos os personagens da fila
        for personagem in self.ordem_turno:
            expirados = personagem.processar_turno()
            if expirados:
                for nome_efeito in expirados:
                    self.adicionar_log(f"  ⏱ Efeito '{nome_efeito}' expirou em {personagem.nome}.", "orange")

        self.turno_atual_index = 0
        primeiro = self.ordem_turno[0]

        self.adicionar_log("═══════ TURNO GERAL ENCERRADO ═══════", "cyan")
        self.adicionar_log(f"▶ Novo turno começa! Vez de {primeiro.nome} (Iniciativa: {getattr(primeiro, 'iniciativa_atual', '?')})", "yellow")

        self.atualizar_fila_turno()
        self.atualizar_card_turno_atual()
        self.refresh()
    ### Turnos ###

    ### Log ###    
    def criar_log_combate(self):
        """Cria o log de combate no centro da tela"""
        self.log_frame = tk.Frame(self, bg="#1a0869", relief="solid", bd=2)
        self.log_frame.place(x=450, y=250, width=700, height=500)
        tk.Label(self.log_frame, text="Log de Combate", fg="white", bg="#1a0869", font=("Arial", 18, "bold")).pack(pady=10)
        canvas_frame = tk.Frame(self.log_frame, bg='#1a0869')
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.log_canvas = tk.Canvas(canvas_frame, bg="#130f26", highlightthickness=0)
        log_scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.log_canvas.yview)
        self.log_canvas.configure(yscrollcommand=log_scrollbar.set)
        log_scrollbar.pack(side="right", fill="y")
        self.log_canvas.pack(side="left", fill="both", expand=True)
        self.log_inner_frame = tk.Frame(self.log_canvas, bg="#130f26")
        self.log_canvas.create_window((0, 0), window=self.log_inner_frame, anchor='nw')
        self.log_inner_frame.bind("<Configure>", lambda e: self.log_canvas.configure(scrollregion=self.log_canvas.bbox("all")))
        self.log_canvas.bind("<Enter>", lambda e: self.log_canvas.bind_all("<MouseWheel>", lambda ev: self.log_canvas.yview_scroll(int(ev.delta / -90), "units")))
        self.log_canvas.bind("<Leave>", lambda e: self.log_canvas.unbind_all("<MouseWheel>"))
        self.adicionar_log("=== Log de Combate Iniciado ===", cor="yellow")
        self.adicionar_log("Aguardando ações de combate...", cor="gray")

    def adicionar_log(self, mensagem, cor="white", detalhes=None):
        """
        Adiciona entrada no log.
        - Se detalhes=None: linha de texto simples.
        - Se detalhes=dict ou str: botão clicável que abre popup com informações completas.
        detalhes pode ser:
            str  → exibido como texto no popup
            dict → chaves são seções, valores são conteúdo (str ou list de str)
        """
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        D.LogCombate.append({
            "timestamp": timestamp,
            "mensagem":  mensagem,
            "cor":       cor,
            "detalhes":  detalhes if isinstance(detalhes, (str, dict, type(None))) else str(detalhes)
        })

        if detalhes is None:
            # ── ENTRADA SIMPLES ─────────────────────────────────────────────────
            lbl = tk.Label(self.log_inner_frame, text=f"[{timestamp}] {mensagem}", bg="#130f26", fg=cor, font=("Arial", 10), wraplength=550, justify="left", anchor="w")
            lbl.pack(fill="x", pady=1, padx=5)
        else:
            # ── ENTRADA DETALHADA (botão) ────────────────────────────────────────
            row = tk.Frame(self.log_inner_frame, bg="#130f26")
            row.pack(fill="x", pady=1, padx=5)

            # Ícone indicador de "tem detalhes"
            tk.Label(row, text="📋", bg="#130f26", fg=cor, font=("Arial", 9)).pack(side="left")

            btn = tk.Button(row, text=f"[{timestamp}] {mensagem}", bg="#130f26", fg=cor, font=("Arial", 10), anchor="w", relief="flat", cursor="hand2", activebackground="#1e1450", activeforeground="white", wraplength=490)
            btn.pack(side="left", fill="x", expand=True)

            # Captura detalhes e mensagem para o popup
            btn.config(command=lambda m=mensagem, d=detalhes, t=timestamp, c=cor: self._abrir_popup_log(m, d, t, c))

            # Tooltip rápida com preview
            preview = detalhes if isinstance(detalhes, str) else "\n".join(f"{k}: {v if isinstance(v, str) else ', '.join(str(x) for x in v)}" for k, v in list(detalhes.items())[:4])
            Tooltip(btn, preview[:300])

        # Auto-scroll para o final
        self.log_canvas.update_idletasks()
        self.log_canvas.yview_moveto(1.0)

    def _abrir_popup_log(self, mensagem, detalhes, timestamp, cor):
        """Abre popup com os detalhes completos de uma entrada do log."""
        popup = tk.Toplevel(self)
        popup.title("Detalhes da Ação")
        popup.configure(bg="#1a1a2e")
        popup.geometry("520x480")
        popup.resizable(False, False)

        # ── Cabeçalho ───────────────────────────────────────────────────────────
        header = tk.Frame(popup, bg="#2d0a8c")
        header.pack(fill="x")
        tk.Label(header, text=mensagem, bg="#2d0a8c", fg=cor if cor not in ("white", "gray") else "white", font=("Arial", 13, "bold"), wraplength=480, justify="left").pack(side="left", padx=12, pady=8)
        tk.Label(header, text=timestamp, bg="#2d0a8c", fg="#aaaaaa", font=("Arial", 9)).pack(side="right", padx=12)

        # ── Conteúdo scrollável ──────────────────────────────────────────────────
        outer = tk.Frame(popup, bg="#1a1a2e")
        outer.pack(fill="both", expand=True, padx=10, pady=10)
        canvas = tk.Canvas(outer, bg="#130f26", highlightthickness=0)
        sb = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        inner = tk.Frame(canvas, bg="#130f26")
        win = canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win, width=e.width))
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", lambda ev: canvas.yview_scroll(int(ev.delta / -90), "units")))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        # ── Renderizar detalhes ──────────────────────────────────────────────────
        if isinstance(detalhes, str):
            tk.Label(inner, text=detalhes, bg="#130f26", fg="white", font=("Arial", 11), wraplength=460, justify="left", anchor="w").pack(fill="x", padx=10, pady=6)

        elif isinstance(detalhes, dict):
            for secao, conteudo in detalhes.items():
                # Título da seção
                sec_frame = tk.Frame(inner, bg="#220866")
                sec_frame.pack(fill="x", padx=6, pady=(6, 1))
                tk.Label(sec_frame, text=secao, bg="#220866", fg="yellow", font=("Arial", 10, "bold")).pack(anchor="w", padx=8, pady=3)

                # Conteúdo da seção
                if isinstance(conteudo, list):
                    for linha in conteudo:
                        tk.Label(inner, text=f"  {linha}", bg="#130f26", fg="white", font=("Arial", 10), anchor="w", wraplength=460, justify="left").pack(fill="x", padx=14, pady=1)
                else:
                    tk.Label(inner, text=f"  {conteudo}", bg="#130f26", fg="white", font=("Arial", 10), anchor="w", wraplength=460, justify="left").pack(fill="x", padx=14, pady=1)

                tk.Frame(inner, bg="#2d0a8c", height=1).pack(fill="x", padx=6, pady=(2, 0))

        tk.Button(popup, text="Fechar", command=popup.destroy, bg="#3a0a80", fg="white", font=("Arial", 11), width=12).pack(pady=10)
    ### Log ### 

    ### Listas de personagens ###
    def criar_interface_grupos(self):
        """Cria os seletores de grupos e as listas de personagens"""
        
        # --- Card do turno atual (Esquerda) ---
        self.criar_card_turno_atual()
        
        # Inicializar grupos padrão para as listas
        grupos_disponiveis = list(D.GruposDePersonagens.keys()) if hasattr(D, 'GruposDePersonagens') and D.GruposDePersonagens else []
        
        if grupos_disponiveis:
            self.grupo_lista_superior = grupos_disponiveis[0] if len(grupos_disponiveis) > 0 else None
            self.grupo_lista_inferior = grupos_disponiveis[1] if len(grupos_disponiveis) > 1 else grupos_disponiveis[0]
        else:
            self.grupo_lista_superior = None
            self.grupo_lista_inferior = None
        
        # Criar as duas listas simplificadas na direita (divididas verticalmente)
        # Lista superior
        self.frame_lista_direita_1 = self.create_simple_list(self.grupo_lista_superior, x=1185, y=100, height=300)
        # Lista inferior
        self.frame_lista_direita_2 = self.create_simple_list(self.grupo_lista_inferior, x=1185, y=410, height=300)
    
    def abrir_popup_selecao_listas(self):
        """Abre popup para selecionar personagens para as listas superior e inferior"""
        popup = tk.Toplevel(self)
        popup.title("Selecionar Personagens para Listas")
        popup.configure(bg="#1a0869")
        popup.geometry("1400x600")
        popup.resizable(False, False)
        
        # Listas temporárias para armazenar seleções
        self.temp_lista_inferior = []
        self.temp_lista_superior = []
        
        # Título
        tk.Label(popup, text="Organize os Personagens nas Listas", bg="#1a0869", fg="white", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Frame principal com 3 colunas
        main_frame = tk.Frame(popup, bg="#1a0869")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # --- Coluna Esquerda (Lista Inferior) ---
        left_frame = tk.LabelFrame(main_frame, text="Lista Inferior", 
                                bg="#1a0869", fg="white", font=("Arial", 12, "bold"))
        left_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        left_canvas = tk.Canvas(left_frame, bg="#130f26", highlightthickness=0)
        left_scroll = tk.Scrollbar(left_frame, orient="vertical", command=left_canvas.yview)
        left_inner = tk.Frame(left_canvas, bg="#130f26")
        left_canvas.create_window((0, 0), window=left_inner, anchor='nw')
        left_canvas.configure(yscrollcommand=left_scroll.set)
        left_scroll.pack(side="right", fill="y")
        left_canvas.pack(side="left", fill="both", expand=True)
        left_inner.bind("<Configure>", lambda e: left_canvas.configure(scrollregion=left_canvas.bbox("all")))
        
        # --- Coluna Central (Todos os Personagens) ---
        center_frame = tk.LabelFrame(main_frame, text="Todos os Personagens", bg="#1a0869", fg="white", font=("Arial", 12, "bold"))
        center_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        # Combobox para selecionar grupo
        grupos_disponiveis = list(D.GruposDePersonagens.keys()) if hasattr(D, 'GruposDePersonagens') and D.GruposDePersonagens else ["Vazio"]
        grupo_var = tk.StringVar(value=grupos_disponiveis[0] if grupos_disponiveis else "")
        
        combo_frame = tk.Frame(center_frame, bg="#1a0869")
        combo_frame.pack(pady=5)
        tk.Label(combo_frame, text="Grupo:", bg="#1a0869", fg="white", font=("Arial", 10)).pack(side="left", padx=5)
        grupo_combo = ttk.Combobox(combo_frame, textvariable=grupo_var, state="readonly", values=grupos_disponiveis, width=15)
        grupo_combo.pack(side="left")
        
        center_canvas = tk.Canvas(center_frame, bg="#130f26", highlightthickness=0)
        center_scroll = tk.Scrollbar(center_frame, orient="vertical", command=center_canvas.yview)
        center_inner = tk.Frame(center_canvas, bg="#130f26")
        center_canvas.create_window((0, 0), window=center_inner, anchor='nw')
        center_canvas.configure(yscrollcommand=center_scroll.set)
        center_scroll.pack(side="right", fill="y")
        center_canvas.pack(side="left", fill="both", expand=True)
        center_inner.bind("<Configure>", lambda e: center_canvas.configure(scrollregion=center_canvas.bbox("all")))
        
        # --- Coluna Direita (Lista Superior) ---
        right_frame = tk.LabelFrame(main_frame, text="Lista Superior", bg="#1a0869", fg="white", font=("Arial", 12, "bold"))
        right_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        right_canvas = tk.Canvas(right_frame, bg="#130f26", highlightthickness=0)
        right_scroll = tk.Scrollbar(right_frame, orient="vertical", command=right_canvas.yview)
        right_inner = tk.Frame(right_canvas, bg="#130f26")
        right_canvas.create_window((0, 0), window=right_inner, anchor='nw')
        right_canvas.configure(yscrollcommand=right_scroll.set)
        right_scroll.pack(side="right", fill="y")
        right_canvas.pack(side="left", fill="both", expand=True)
        right_inner.bind("<Configure>", lambda e: right_canvas.configure(scrollregion=right_canvas.bbox("all")))
        
        def atualizar_listas():
            """Atualiza as três listas"""
            # Limpar listas
            for widget in left_inner.winfo_children():
                widget.destroy()
            for widget in center_inner.winfo_children():
                widget.destroy()
            for widget in right_inner.winfo_children():
                widget.destroy()
            
            # Lista Inferior
            for personagem in self.temp_lista_inferior:
                frame = tk.Frame(left_inner, bg="#220866", bd=1, relief="solid")
                frame.pack(fill="x", padx=5, pady=2)
                tk.Label(frame, text=personagem.nome, bg="#220866", fg="white", font=("Arial", 10)).pack(side="left", padx=5)
                tk.Button(frame, text="✕", command=lambda p=personagem: remover_de_inferior(p), bg="#8B0000", fg="white", width=3).pack(side="right", padx=2)
            
            # Lista Central - personagens do grupo selecionado que não estão em nenhuma lista
            grupo_nome = grupo_var.get()
            if grupo_nome and grupo_nome in D.GruposDePersonagens:
                for personagem in D.GruposDePersonagens[grupo_nome]:
                    if personagem not in self.temp_lista_inferior and personagem not in self.temp_lista_superior:
                        frame = tk.Frame(center_inner, bg="#220866", bd=1, relief="solid")
                        frame.pack(fill="x", padx=5, pady=2)
                        
                        tk.Label(frame, text=personagem.nome, bg="#220866", fg="white", font=("Arial", 10)).pack(side="left", padx=5)
                        # Botões de seta
                        tk.Button(frame, text="←", command=lambda p=personagem: adicionar_a_inferior(p), bg="#006400", fg="white", width=3).pack(side="right", padx=2)
                        tk.Button(frame, text="→", command=lambda p=personagem: adicionar_a_superior(p), bg="#004080", fg="white", width=3).pack(side="right", padx=2)
            
            # Lista Superior
            for personagem in self.temp_lista_superior:
                frame = tk.Frame(right_inner, bg="#220866", bd=1, relief="solid")
                frame.pack(fill="x", padx=5, pady=2)
                
                tk.Label(frame, text=personagem.nome, bg="#220866", fg="white", font=("Arial", 10)).pack(side="left", padx=5)
                
                tk.Button(frame, text="✕", command=lambda p=personagem: remover_de_superior(p), bg="#8B0000", fg="white", width=3).pack(side="right", padx=2)
        
        def adicionar_a_inferior(personagem):
            if personagem not in self.temp_lista_inferior:
                self.temp_lista_inferior.append(personagem)
                atualizar_listas()
        
        def adicionar_a_superior(personagem):
            if personagem not in self.temp_lista_superior:
                self.temp_lista_superior.append(personagem)
                atualizar_listas()
        
        def remover_de_inferior(personagem):
            if personagem in self.temp_lista_inferior:
                self.temp_lista_inferior.remove(personagem)
                atualizar_listas()
        
        def remover_de_superior(personagem):
            if personagem in self.temp_lista_superior:
                self.temp_lista_superior.remove(personagem)
                atualizar_listas()
        
        def confirmar_selecao():
            """Aplica as seleções e fecha o popup"""
            # Criar grupos temporários com os personagens selecionados
            if not hasattr(D, 'GruposDePersonagens'):
                D.GruposDePersonagens = {}
            
            # Atualizar grupos com nomes especiais
            D.GruposDePersonagens["_lista_inferior"] = self.temp_lista_inferior.copy()
            D.GruposDePersonagens["_lista_superior"] = self.temp_lista_superior.copy()
            
            # Atualizar as variáveis de grupo
            self.grupo_lista_inferior = "_lista_inferior"
            self.grupo_lista_superior = "_lista_superior"
            
            # Recriar as listas
            self.frame_lista_direita_2.destroy()
            self.frame_lista_direita_1.destroy()
            
            self.frame_lista_direita_1 = self.create_simple_list(self.grupo_lista_superior, x=1185, y=100, height=300)
            self.frame_lista_direita_2 = self.create_simple_list(self.grupo_lista_inferior, x=1185, y=410, height=300)
            
            popup.destroy()
        
        # Vincular atualização ao combobox
        grupo_combo.bind("<<ComboboxSelected>>", lambda e: atualizar_listas())
        
        # Botões de ação
        botoes_frame = tk.Frame(popup, bg="#1a0869")
        botoes_frame.pack(pady=10)
        
        tk.Button(botoes_frame, text="Confirmar", command=confirmar_selecao, bg="#38b000", fg="white", font=("Arial", 12), width=15).pack(side="left", padx=10)
        tk.Button(botoes_frame, text="Cancelar", command=popup.destroy,bg="#8B0000", fg="white", font=("Arial", 12), width=15).pack(side="left", padx=10)
        
        # Inicializar listas
        atualizar_listas()
    
    def abrir_popup_iniciativa(self):
        """Abre popup para gerenciar iniciativa dos personagens em combate"""
        import random
        popup = tk.Toplevel(self)
        popup.title("Gerenciar Iniciativa")
        popup.configure(bg="#1a1a2e")
        popup.geometry("900x600")
        popup.resizable(False, False)
        
        # Título
        tk.Label(popup, text="Gerenciamento de Iniciativa", bg="#1a1a2e", fg="white", font=("Arial", 16, "bold")).pack(pady=15)
    
        # Frame principal com 2 colunas
        main_frame = tk.Frame(popup, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # --- Coluna Esquerda: Personagens em Combate ---
        left_frame = tk.LabelFrame(main_frame, text="Personagens em Combate", bg="#1a1a2e", fg="white", font=("Arial", 12, "bold"))
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Botão de rolar iniciativa para todos
        tk.Button(left_frame, text="🎲 Rolar Iniciativa para Todos", command=lambda: rolar_todos(),
                bg="#0077b6", fg="white", font=("Arial", 11, "bold")).pack(pady=10)
        
        # Canvas para lista de personagens
        left_canvas = tk.Canvas(left_frame, bg="#130f26", highlightthickness=0)
        left_scroll = tk.Scrollbar(left_frame, orient="vertical", command=left_canvas.yview)
        left_inner = tk.Frame(left_canvas, bg="#130f26")
        left_canvas.create_window((0, 0), window=left_inner, anchor='nw')
        left_canvas.configure(yscrollcommand=left_scroll.set)
        left_scroll.pack(side="right", fill="y")
        left_canvas.pack(side="left", fill="both", expand=True)
        left_inner.bind("<Configure>", lambda e: left_canvas.configure(scrollregion=left_canvas.bbox("all")))
        
        # --- Coluna Direita: Ordem de Turnos ---
        right_frame = tk.LabelFrame(main_frame, text="Ordem de Turnos", bg="#1a1a2e", fg="white", font=("Arial", 12, "bold"))
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Canvas para ordem de turnos
        right_canvas = tk.Canvas(right_frame, bg="#130f26", highlightthickness=0)
        right_scroll = tk.Scrollbar(right_frame, orient="vertical", command=right_canvas.yview)
        right_inner = tk.Frame(right_canvas, bg="#130f26")
        right_canvas.create_window((0, 0), window=right_inner, anchor='nw')
        right_canvas.configure(yscrollcommand=right_scroll.set)
        right_scroll.pack(side="right", fill="y")
        right_canvas.pack(side="left", fill="both", expand=True)
        right_inner.bind("<Configure>", lambda e: right_canvas.configure(scrollregion=right_canvas.bbox("all")))
        
        # Dicionário para armazenar variáveis de iniciativa
        iniciativa_vars = {}
        
        # Coletar todos os personagens em combate (listas superior e inferior)
        personagens_combate = []
        if hasattr(D, 'GruposDePersonagens'):
            if "_lista_superior" in D.GruposDePersonagens:
                personagens_combate.extend(D.GruposDePersonagens["_lista_superior"])
            if "_lista_inferior" in D.GruposDePersonagens:
                personagens_combate.extend(D.GruposDePersonagens["_lista_inferior"])
        
        def criar_linha_personagem(personagem):
            """Cria uma linha para cada personagem com nome e seletor de iniciativa"""
            frame = tk.Frame(left_inner, bg="#220866", bd=1, relief="solid")
            frame.pack(fill="x", padx=5, pady=3)
            
            # Nome do personagem
            tk.Label(frame, text=personagem.nome, bg="#220866", fg="white", font=("Arial", 11, "bold")).pack(side="left", padx=10)
            
            # Frame para controles de iniciativa
            controls_frame = tk.Frame(frame, bg="#220866")
            controls_frame.pack(side="right", padx=10)
            
            # Variável para armazenar valor da iniciativa
            iniciativa_var = tk.StringVar(value=getattr(personagem, 'iniciativa_atual', 'Sem iniciativa'))
            iniciativa_vars[personagem.nome] = iniciativa_var
            
            # Label de iniciativa atual
            tk.Label(controls_frame, text="Iniciativa:", bg="#220866", fg="lightblue", font=("Arial", 9)).pack(side="left", padx=5)
            
            # Combobox para valores de iniciativa
            valores = ["Sem iniciativa", "Incapacitado"] + [str(i) for i in range(1, 21)]
            combo = ttk.Combobox(controls_frame, textvariable=iniciativa_var, values=valores, state="readonly", width=15)
            combo.pack(side="left", padx=5)
            
            # Botão para rolar iniciativa individual
            def rolar_individual():
                rolagem = random.randint(1, 20)
                iniciativa_var.set(str(rolagem))
                atualizar_ordem()
            
            tk.Button(controls_frame, text="🎲", command=rolar_individual, bg="#006400", fg="white", width=3).pack(side="left", padx=2)
        
        def rolar_todos():
            """Rola iniciativa para todos os personagens"""
            for personagem in personagens_combate:
                if personagem.nome in iniciativa_vars:
                    rolagem = random.randint(1, 20)
                    iniciativa_vars[personagem.nome].set(str(rolagem))
            atualizar_ordem()
        
        def atualizar_ordem():
            """Atualiza a lista de ordem de turnos baseada nas iniciativas"""
            # Limpar lista atual
            for widget in right_inner.winfo_children():
                widget.destroy()
            
            # Criar lista de (personagem, iniciativa_valor)
            ordem = []
            for personagem in personagens_combate:
                if personagem.nome in iniciativa_vars:
                    valor_str = iniciativa_vars[personagem.nome].get()
                    
                    # Determinar valor numérico para ordenação
                    if valor_str == "Sem iniciativa":
                        valor_num = -1
                    elif valor_str == "Incapacitado":
                        valor_num = -2
                    else:
                        valor_num = int(valor_str)
                    
                    ordem.append((personagem, valor_str, valor_num))
            
            # Ordenar por valor numérico (maior para menor), excluindo valores negativos da ordem principal
            ordem_valida = [(p, v_str, v_num) for p, v_str, v_num in ordem if v_num > 0]
            ordem_invalida = [(p, v_str, v_num) for p, v_str, v_num in ordem if v_num <= 0]
            
            ordem_valida.sort(key=lambda x: x[2], reverse=True)
            
            # Mostrar ordem válida
            for idx, (personagem, valor_str, _) in enumerate(ordem_valida, 1):
                frame = tk.Frame(right_inner, bg="#220866", bd=1, relief="solid")
                frame.pack(fill="x", padx=5, pady=2)
                
                tk.Label(frame, text=f"{idx}º", bg="#220866", fg="yellow", font=("Arial", 10, "bold"), width=4).pack(side="left", padx=5)
                tk.Label(frame, text=personagem.nome, bg="#220866", fg="white", font=("Arial", 10)).pack(side="left", padx=5)
                tk.Label(frame, text=f"[{valor_str}]", bg="#220866", fg="lightgreen", font=("Arial", 9)).pack(side="right", padx=10)
            
            # Separador se houver personagens inválidos
            if ordem_invalida:
                tk.Frame(right_inner, bg="gray", height=2).pack(fill="x", padx=5, pady=5)
            
            # Mostrar personagens sem iniciativa ou incapacitados
            for personagem, valor_str, _ in ordem_invalida:
                frame = tk.Frame(right_inner, bg="#3a1a1a", bd=1, relief="solid")
                frame.pack(fill="x", padx=5, pady=2)
                
                tk.Label(frame, text="—", bg="#3a1a1a", fg="gray", font=("Arial", 10), width=4).pack(side="left", padx=5)
                tk.Label(frame, text=personagem.nome, bg="#3a1a1a", fg="gray", font=("Arial", 10)).pack(side="left", padx=5)
                tk.Label(frame, text=f"[{valor_str}]", bg="#3a1a1a", fg="red", font=("Arial", 9)).pack(side="right", padx=10)
        
        def confirmar_iniciativa():
            """Confirma a ordem de iniciativa e atualiza a tela de combate"""
            # Criar lista ordenada apenas com personagens que têm iniciativa válida
            ordem_final = []
            for personagem in personagens_combate:
                if personagem.nome in iniciativa_vars:
                    valor_str = iniciativa_vars[personagem.nome].get()
                    
                    if valor_str not in ["Sem iniciativa", "Incapacitado"]:
                        try:
                            valor_num = int(valor_str)
                            personagem.iniciativa_atual = valor_num
                            ordem_final.append((personagem, valor_num))
                        except ValueError:
                            pass
            
            # Ordenar por iniciativa (maior para menor)
            ordem_final.sort(key=lambda x: x[1], reverse=True)
            
            # Atualizar ordem de turno na tela principal
            self.ordem_turno = [p for p, _ in ordem_final]
            self.turno_atual_index = 0
            
            # Atualizar displays
            self.atualizar_fila_turno()
            self.atualizar_card_turno_atual()
            
            # Log
            if self.ordem_turno:
                self.adicionar_log("=== Ordem de Iniciativa Definida ===", "yellow")
                for idx, personagem in enumerate(self.ordem_turno, 1):
                    self.adicionar_log(f"{idx}º - {personagem.nome} (Iniciativa: {personagem.iniciativa_atual})", "lightgreen")
            
            popup.destroy()
        
        # Criar linhas para cada personagem
        for personagem in personagens_combate:
            criar_linha_personagem(personagem)
        
        # Atualizar ordem inicial
        atualizar_ordem()
        
        # Botões de ação
        botoes_frame = tk.Frame(popup, bg="#1a1a2e")
        botoes_frame.pack(pady=15)
        
        tk.Button(botoes_frame, text="Confirmar Ordem", command=confirmar_iniciativa,
                bg="#38b000", fg="white", font=("Arial", 12, "bold"), width=18).pack(side="left", padx=10)
        
        tk.Button(botoes_frame, text="Cancelar", command=popup.destroy,
                bg="#8B0000", fg="white", font=("Arial", 12, "bold"), width=18).pack(side="left", padx=10)

    def get_all_personagens(self):
        """Retorna todos os personagens de todos os grupos"""
        todos_personagens = []
        if D.GruposDePersonagens:
            for grupo in D.GruposDePersonagens.values():
                todos_personagens.extend(grupo)
        return todos_personagens

    def create_simple_list(self, grupo_nome, x, y, height):
        """Lista simplificada com destaque do personagem no card,
        distâncias do mapa, nível de cobertura e material de cobertura."""

        frame = tk.Frame(self, bg="#1a0869")
        frame.place(x=x, y=y, width=400, height=height)

        if not grupo_nome or grupo_nome not in D.GruposDePersonagens:
            tk.Label(frame, text="Nenhum grupo selecionado",
                    fg="gray", bg="#1a0869", font=("Arial", 14)).pack(pady=100)
            return frame

        data_list = D.GruposDePersonagens[grupo_nome]

        # ── título + botão renomear ──────────────────────────────────────────
        header = tk.Frame(frame, bg="#1a0869")
        header.pack(fill="x", padx=6, pady=(4, 2))

        chave_apelido = f"_apelido_{grupo_nome}"
        if grupo_nome == "_lista_inferior":
            nome_padrao = "Lista Inferior"
        elif grupo_nome == "_lista_superior":
            nome_padrao = "Lista Superior"
        else:
            nome_padrao = grupo_nome
        titulo_atual = getattr(D, chave_apelido, nome_padrao)

        lbl_titulo = tk.Label(header, text=titulo_atual,
                            fg="white", bg="#1a0869", font=("Arial", 13, "bold"))
        lbl_titulo.pack(side="left")

        def _renomear():
            popup = tk.Toplevel(frame)
            popup.title("Renomear lista")
            popup.configure(bg="#1a0869")
            popup.geometry("320x130")
            popup.resizable(False, False)
            tk.Label(popup, text="Novo nome:", bg="#1a0869", fg="white",
                    font=("Arial", 11)).pack(pady=(14, 4))
            var = tk.StringVar(value=lbl_titulo.cget("text"))
            entry = tk.Entry(popup, textvariable=var, font=("Arial", 11),
                            width=28, justify="center")
            entry.pack()
            entry.select_range(0, tk.END)
            entry.focus_set()
            def _confirmar(ev=None):
                novo = var.get().strip()
                if novo:
                    setattr(D, chave_apelido, novo)
                    lbl_titulo.config(text=novo)
                popup.destroy()
            tk.Button(popup, text="Confirmar", command=_confirmar,
                    bg="#38b000", fg="white", font=("Arial", 10),
                    width=12).pack(pady=10)
            entry.bind("<Return>", _confirmar)

        tk.Button(header, text="✏", command=_renomear,
                bg="#1a0869", fg="#aaaaaa", font=("Arial", 10),
                relief="flat", cursor="hand2").pack(side="left", padx=(6, 0))

        if not data_list:
            tk.Label(frame, text="Lista vazia",
                    fg="gray", bg="#1a0869", font=("Arial", 12)).pack(pady=50)
            return frame

        # ── canvas com scroll ────────────────────────────────────────────────
        canvas_frame = tk.Frame(frame, bg="#1a0869")
        canvas_frame.pack(fill="both", expand=True)
        canvas = tk.Canvas(canvas_frame, bg="#1a0869", highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical",
                                command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        inner_frame = tk.Frame(canvas, bg="#1a0869")
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        inner_frame.bind("<Configure>",
                        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # ── personagem atualmente no card ────────────────────────────────────
        char_no_card = getattr(self, "personagem_no_card", None)

        # ── distâncias do mapa ───────────────────────────────────────────────
        distancias_do_card: dict = {}
        if char_no_card is not None and hasattr(self, "distancias_mapa"):
            distancias_do_card = self.distancias_mapa.get(char_no_card.nome, {})

        # ── constantes de cobertura e material ───────────────────────────────
        CORES_COB = {
            "Nenhuma": None,
            "Parcial": "#ffcc00",
            "Alta":    "#ff8800",
            "Total":   "#cc0000",
        }
        NIVEIS_COB = ["Nenhuma", "Parcial", "Alta", "Total"]

        NIVEIS_MAT = ["Nenhum", "Gesso", "Madeira", "Veiculo", "Concreto", "Aço"]
        CORES_MAT  = {
            "Nenhum":   None,
            "Gesso":    "#ddddcc",
            "Madeira":  "#cc9944",
            "Veiculo":  "#88aacc",
            "Concreto": "#aaaaaa",
            "Aço":      "#99ddff",
        }

        # ── linhas de personagem ─────────────────────────────────────────────
        for char in list(data_list):
            eh_destaque = (char_no_card is not None and char is char_no_card)
            bg_item = "#3a2a00" if eh_destaque else "#220866"

            char_frame = tk.Frame(inner_frame, bg=bg_item, bd=2, relief="solid")
            char_frame.pack(fill="x", padx=5, pady=3)

            if eh_destaque:
                char_frame.configure(highlightbackground="#ffd700",
                                    highlightthickness=2)

            # ── linha principal ──────────────────────────────────────────────
            row_top = tk.Frame(char_frame, bg=bg_item)
            row_top.pack(fill="x")

            if eh_destaque:
                tk.Label(row_top, text="▶", bg=bg_item, fg="#ffd700",
                        font=("Arial", 9, "bold")).pack(side="left", padx=(4, 0))

            nome_fg  = "#ffd700" if eh_destaque else "white"
            nome_fnt = ("Arial", 10, "bold") if eh_destaque else ("Arial", 10)
            info_txt = (f"{char.nome}  •  Nv {char.Nivel}  •  "
                        f"PV {char.VidaAtual}/{char.VidaMax}")

            cobertura_char = getattr(char, "cobertura_mapa", "Nenhuma")
            material_char  = getattr(char, "material_mapa",  "Nenhum")
            cor_cob        = CORES_COB.get(cobertura_char)
            cor_mat        = CORES_MAT.get(material_char)

            # bolinha de cobertura
            if cor_cob:
                cv_cob = tk.Canvas(row_top, width=10, height=10,
                                bg=bg_item, highlightthickness=0)
                cv_cob.create_oval(1, 1, 9, 9, fill=cor_cob, outline="")
                cv_cob.pack(side="left", padx=(4, 0), pady=4)

            # ── menu de contexto ─────────────────────────────────────────────
            menu = tk.Menu(char_frame, tearoff=0)
            menu.add_command(
                label="👁 Escolher",
                command=lambda p=char: self._mostrar_personagem_no_card(p))
            menu.add_command(
                label="📋 Detalhes",
                command=lambda p=char: self.controller.abrir_detalhes(p))
            menu.add_separator()

            # submenu cobertura
            submenu_cob = tk.Menu(menu, tearoff=0)
            for nivel in NIVEIS_COB:
                cor_n   = CORES_COB.get(nivel)
                icone_n = "●" if cor_n else "○"
                def _setar_cobertura(n=nivel, c=char, cor=cor_n):
                    c.cobertura_mapa = n
                    self._refresh_listas_highlight()
                    self.adicionar_log(f"🛡 Cobertura de {c.nome} → {n}", cor or "gray")
                submenu_cob.add_command(label=f"{icone_n} {nivel}",
                                        command=_setar_cobertura)
            menu.add_cascade(label="🛡 Cobertura", menu=submenu_cob)

            # submenu material
            submenu_mat = tk.Menu(menu, tearoff=0)
            for mat in NIVEIS_MAT:
                cor_m   = CORES_MAT.get(mat)
                icone_m = "■" if cor_m else "□"
                def _setar_material(m=mat, c=char, cor=cor_m):
                    c.material_mapa = m
                    self._refresh_listas_highlight()
                    self.adicionar_log(f"🧱 Material de {c.nome} → {m}", cor or "gray")
                submenu_mat.add_command(label=f"{icone_m} {mat}",
                                        command=_setar_material)
            menu.add_cascade(label="🧱 Material", menu=submenu_mat)
            menu.add_separator()

            menu.add_command(
                label="✕ Remover do combate",
                command=lambda p=char, gn=grupo_nome: [
                    self._remover_do_combate(p),
                    self.frame_lista_direita_1.destroy(),
                    self.frame_lista_direita_2.destroy(),
                    setattr(self, "frame_lista_direita_1",
                            self.create_simple_list(self.grupo_lista_superior,
                                                x=1150, y=250, height=295)),
                    setattr(self, "frame_lista_direita_2",
                            self.create_simple_list(self.grupo_lista_inferior,
                                                x=1150, y=555, height=295)),
                ])

            btn = tk.Button(row_top, text=info_txt,
                            bg=bg_item, fg=nome_fg, font=nome_fnt,
                            anchor="w", relief=tk.FLAT, cursor="hand2",
                            activebackground="#4a2a10" if eh_destaque else "#3a1a9e")
            btn.config(command=lambda m=menu, b=btn:
                    m.tk_popup(b.winfo_rootx(),
                                b.winfo_rooty() + b.winfo_height()))
            btn.pack(side="left", fill="x", expand=True, padx=8, pady=3)

            # ── linha inferior: cobertura + material + distância ─────────────
            row_bot = tk.Frame(char_frame, bg=bg_item)
            row_bot.pack(fill="x", padx=8, pady=(0, 4))

            # cobertura
            if cobertura_char and cobertura_char != "Nenhuma":
                tk.Label(row_bot, text=f"🛡 {cobertura_char}",
                        bg=bg_item, fg=cor_cob,
                        font=("Arial", 8, "bold")).pack(side="left")
            else:
                tk.Label(row_bot, text="○ Sem cobertura",
                        bg=bg_item, fg="#555555",
                        font=("Arial", 8, "italic")).pack(side="left")

            # material (só exibe quando definido)
            if material_char and material_char != "Nenhum":
                tk.Label(row_bot, text=f"  🧱 {material_char}",
                        bg=bg_item, fg=cor_mat or "#88ccff",
                        font=("Arial", 8)).pack(side="left")

            # distância
            if char_no_card is not None and char is not char_no_card:
                dist_val = distancias_do_card.get(char.nome)
                if dist_val is not None:
                    cor_dist = ("#ff4444" if dist_val <= 2
                                else "#ffaa00" if dist_val <= 10
                                else "#00e5ff")
                    tk.Label(row_bot, text=f"↔ {dist_val:.1f} m",
                            bg=bg_item, fg=cor_dist,
                            font=("Arial", 8, "bold")).pack(side="right")
                else:
                    tk.Label(row_bot, text="↔ fora do mapa",
                            bg=bg_item, fg="#444466",
                            font=("Arial", 8, "italic")).pack(side="right")
            elif char_no_card is not None and char is char_no_card:
                tk.Label(row_bot, text="◉ selecionado",
                        bg=bg_item, fg="#ffd700",
                        font=("Arial", 8, "italic")).pack(side="right")

        return frame
    
    def _refresh_listas_highlight(self):
        """Reconstrói as listas laterais para refletir o personagem destacado."""
        if hasattr(self, 'frame_lista_direita_1'):
            self.frame_lista_direita_1.destroy()
            self.frame_lista_direita_1 = self.create_simple_list(
                self.grupo_lista_superior, x=1185, y=100, height=300)
        if hasattr(self, 'frame_lista_direita_2'):
            self.frame_lista_direita_2.destroy()
            self.frame_lista_direita_2 = self.create_simple_list(
                self.grupo_lista_inferior, x=1185, y=410, height=300)
    ### Listas de personagens ###

    ### Card personagem ###
    def criar_card_turno_atual(self):
        """Cria o card do personagem do turno atual no lado esquerdo"""
        # Frame principal para o card do turno atual
        self.frame_turno_atual = tk.Frame(self, bg='#1a0869')
        self.frame_turno_atual.place(x=20, y=100, width=400, height=700)
        
        tk.Label(self.frame_turno_atual, text="Turno Atual", fg="white", bg="#1a0869", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Aqui ficará o card do personagem
        self.atualizar_card_turno_atual()

    def atualizar_card_turno_atual(self):
        """Mostra o personagem do turno real no card."""
        if not self.ordem_turno:
            self._limpar_card()
            tk.Label(self.frame_turno_atual, text="Aguardando iniciativa...",fg="gray", bg="#1a0869", font=("Arial", 12)).pack(pady=100)
            self.personagem_no_card = None
            self._refresh_listas_highlight()
            return
        p = self.ordem_turno[self.turno_atual_index]
        self.personagem_no_card = p
        self._construir_conteudo_card(p)
        self._refresh_listas_highlight()

    def _mostrar_personagem_no_card(self, personagem):
        """Exibe qualquer personagem no card sem alterar o turno real."""
        self.personagem_no_card = personagem
        self._construir_conteudo_card(personagem)
        self._refresh_listas_highlight()

    def _limpar_card(self):
        """Remove tudo do frame_turno_atual exceto o título fixo."""
        for widget in self.frame_turno_atual.winfo_children():
            if not (isinstance(widget, tk.Label) and widget.cget("text") == "Turno Atual"):
                widget.destroy()
        if not any(isinstance(w, tk.Label) and w.cget("text") == "Turno Atual"
                   for w in self.frame_turno_atual.winfo_children()):
            tk.Label(self.frame_turno_atual, text="Turno Atual",
                     fg="white", bg="#1a0869", font=("Arial", 16, "bold")).pack(pady=10)

    def _construir_conteudo_card(self, char):
        """Constrói todo o conteúdo visual do card para 'char'."""
        self._limpar_card()

        # ── container scrollável ─────────────────────────────────────────────
        outer = tk.Frame(self.frame_turno_atual, bg="#1a0869")
        outer.pack(fill="both", expand=True, padx=4, pady=(0, 4))
        main_canvas = tk.Canvas(outer, bg="#1a0869", highlightthickness=0)
        main_scroll = tk.Scrollbar(outer, orient="vertical", command=main_canvas.yview)
        main_canvas.configure(yscrollcommand=main_scroll.set)
        main_scroll.pack(side="right", fill="y")
        main_canvas.pack(side="left", fill="both", expand=True)
        char_frame  = tk.Frame(main_canvas, bg="#220866")
        card_window = main_canvas.create_window((0, 0), window=char_frame, anchor="nw")
        char_frame.bind("<Configure>", lambda e: (
            main_canvas.configure(scrollregion=main_canvas.bbox("all")),
            main_canvas.itemconfig(card_window, width=main_canvas.winfo_width())))
        main_canvas.bind("<Configure>", lambda e: main_canvas.itemconfig(card_window, width=e.width))
        main_canvas.bind("<Enter>", lambda e: main_canvas.bind_all("<MouseWheel>", lambda ev: main_canvas.yview_scroll(int(ev.delta / -90), "units")))
        main_canvas.bind("<Leave>", lambda e: main_canvas.unbind_all("<MouseWheel>"))

        # ── HEADER ──────────────────────────────────────────────────────────
        header = tk.Frame(char_frame, bg="#2d0a8c")
        header.pack(fill="x", pady=(6, 2))
        tk.Label(header, text=f"▶ {char.nome}", bg="#2d0a8c", fg="yellow", font=("Arial", 14, "bold")).pack(side="left", padx=10)
        tk.Label(header, text=f"Nv {char.Nivel}  |  Init {getattr(char, 'iniciativa_atual', '?')}", bg="#2d0a8c", fg="white", font=("Arial", 10)).pack(side="right", padx=10)

        # ── BARRAS CLICÁVEIS ─────────────────────────────────────────────────
        def _barra_clicavel(parent, label_txt, attr_atual, attr_max, cor):
            row = tk.Frame(parent, bg="#220866")
            row.pack(fill="x", padx=12, pady=3)
            tk.Label(row, text=label_txt, bg="#220866", fg="#cccccc", font=("Arial", 9, "bold"), width=7, anchor="w").pack(side="left")
            lbl_val = tk.Label(row, text=f"{getattr(char, attr_atual)}/{getattr(char, attr_max)}", bg="#220866", fg="white", font=("Arial", 9, "bold"), width=9, anchor="w")
            lbl_val.pack(side="left")
            c = tk.Canvas(row, height=14, bg="#111111", highlightthickness=0, cursor="hand2")
            c.pack(side="left", fill="x", expand=True, padx=(4, 0))
            c._cor = cor; c._label_ref = lbl_val
            def _redraw(ev=None):
                self._redesenhar_barra(c, getattr(char, attr_atual), getattr(char, attr_max), cor)
                lbl_val.config(text=f"{getattr(char, attr_atual)}/{getattr(char, attr_max)}")
            c.bind("<Map>",       lambda e: c.after(50, _redraw))
            c.bind("<Button-1>",  lambda e: [self._setar_barra_combate(char, attr_atual, attr_max, c, e), _redraw()])
            c.bind("<B1-Motion>", lambda e: [self._setar_barra_combate(char, attr_atual, attr_max, c, e), _redraw()])

        barras_frame = tk.Frame(char_frame, bg="#220866")
        barras_frame.pack(fill="x", padx=4, pady=4)
        _barra_clicavel(barras_frame, "Vida",    "VidaAtual",    "VidaMax",    "#b22222")
        _barra_clicavel(barras_frame, "Energia", "EnergiaAtual", "EnergiaMax", "#1e90ff")
        _barra_clicavel(barras_frame, "Mana",    "ManaAtual",    "ManaMax",    "#7b3fe4")

        # ── INFO RÁPIDA ──────────────────────────────────────────────────────
        info_frame = tk.Frame(char_frame, bg="#1b1240")
        info_frame.pack(fill="x", padx=12, pady=4)
        tk.Label(info_frame, text=f"Mov {char.Movimento}m  |  Disp {char.Disparada}m  |  Carga {char.CargaAtual}/{char.CargaMax}kg", bg="#1b1240", fg="lightgreen", font=("Arial", 9)).pack(anchor="w")
        tk.Label(info_frame, text=f"Percepção {char.Percepcao}  |  Bloqueio {char.Bloqueio}  |  Esquiva {char.Esquiva}", bg="#1b1240", fg="#e8665d", font=("Arial", 9)).pack(anchor="w")

        # ── MÃOS + SUPORTE ───────────────────────────────────────────────────
        maos_frame = tk.Frame(char_frame, bg="#2a0d5c")
        maos_frame.pack(fill="x", padx=12, pady=4)
        tk.Label(maos_frame, text="Armas em Mãos", bg="#2a0d5c", fg="yellow", font=("Arial", 10, "bold")).pack(anchor="w")

        def _linha_slot(parent, slot_key, slot_label, bg_frame="#2a0d5c"):
            slot = char.slots.get(slot_key)
            item = slot.item if slot else None
            row  = tk.Frame(parent, bg=bg_frame)
            row.pack(fill="x", pady=1)
            tk.Label(row, text=f"{slot_label}:", bg=bg_frame, fg="#cccccc", font=("Arial", 9), width=10, anchor="w").pack(side="left")

            if item:
                eh_ranged = isinstance(item, CB.Ranged)
                menu = tk.Menu(row, tearoff=0)

                # --- Opção Atacar ---
                def _atacar_slot(c=char):
                    armas_unicas = {}
                    for k, s in c.slots.items():
                        if s.tipo == "mao" and s.item:
                            armas_unicas[id(s.item)] = s.item
                    armas = list(armas_unicas.values())
                    if len(armas) == 2 and all(getattr(a, "maos", 1) == 1 for a in armas):
                        self._iniciar_dual_wield(c, [(None, a) for a in armas])
                    elif len(armas) == 1:
                        arma = armas[0]
                        if isinstance(arma, CB.Ranged):
                            self.abrir_popup_ataque_ranged(c)
                        else:
                            self.abrir_popup_ataque_melee(c, arma_pre=arma)

                menu.add_command(label="⚔ Atacar", command=_atacar_slot)
                menu.add_separator()

                if eh_ranged:
                    menu.add_command(label="🔫 Disparar", command=lambda c=char, i=item: self.abrir_popup_ataque_ranged(c, callback_resultado=lambda r: self.refresh()))
                    menu.add_command(label="🔄 Recarregar", command=lambda c=char, i=item: [self.abrir_popup_escolher_municao(c, i)])
                    menu.add_command(label="📤 Descarregar", command=lambda c=char, i=item: [self.abrir_popup_descarregar_quantidade(c, i)])
                    if len(item.acoes_disparo) > 1:
                        menu.add_command(label=f"🔁 Modo: {item.modo_disparo_atual}", command=lambda i=item: [i.trocar_modo_disparo(), self.refresh()])
                    menu.add_separator()

                menu.add_command(label="↕ Trocar  (suporte ↔ mão)", command=lambda k=slot_key: [self._trocar_arma_slot(char, k), self.refresh()])
                menu.add_command(label="📦 Guardar  (→ inventário)", command=lambda k=slot_key: [self._guardar_arma_slot(char, k), self.refresh()])

                btn_txt = f"{item.nome}  [{getattr(item,'munições','?')}/{getattr(item,'capacidade','?')}]" if eh_ranged else item.nome
                btn = tk.Button(row, text=btn_txt, bg="#3d1a6e", fg="white", font=("Arial", 9),relief="flat", anchor="w", cursor="hand2", activebackground="#5a2a9e")
                btn.config(command=lambda m=menu, b=btn: m.tk_popup(b.winfo_rootx(), b.winfo_rooty() + b.winfo_height()))
                btn.pack(side="left", fill="x", expand=True)
                Tooltip(btn, self._tooltip_arma(item))

            else:
                # Mão vazia — menu com opções
                is_mao = "mao" in slot_key
                if is_mao:
                    menu_vazio = tk.Menu(row, tearoff=0)
                    menu_vazio.add_command(label="👊 Ataque Desarmado", command=lambda c=char: self.abrir_popup_ataque_desarmado(c))
                    menu_vazio.add_command(label="💰 Pilhar",command=lambda c=char: self.abrir_popup_pilhagem_card(c))
                    btn_vazio = tk.Button(row, text="👊 Mão Vazia", bg="#1a0f35", fg="#666666",font=("Arial", 9, "italic"), relief="flat", anchor="w",cursor="hand2", activebackground="#2a1a45")
                    btn_vazio.config(command=lambda m=menu_vazio, b=btn_vazio:m.tk_popup(b.winfo_rootx(), b.winfo_rooty() + b.winfo_height()))
                    btn_vazio.pack(side="left", fill="x", expand=True)
                else:
                    btn_vazio = tk.Button(row, text="— vazio —", bg="#1a0f35", fg="#555555",font=("Arial", 9, "italic"), relief="flat", anchor="w")
                    btn_vazio.pack(side="left", fill="x", expand=True)

        for slot_key, slot_label in [("mao_direita", "Mão Dir"), ("mao_esquerda", "Mão Esq")]:
            _linha_slot(maos_frame, slot_key, slot_label)

        slots_suporte = [(k, s) for k, s in char.slots.items() if s.tipo == "suporte"]
        if slots_suporte:
            tk.Frame(maos_frame, bg="#3d1a6e", height=1).pack(fill="x", padx=4, pady=(4, 2))
            tk.Label(maos_frame, text="Suporte", bg="#2a0d5c", fg="#aaaaaa", font=("Arial", 8, "italic")).pack(anchor="w")
            for slot_key, slot_obj in slots_suporte:
                label = getattr(slot_obj, "nome", slot_key.replace("_", " ").capitalize())
                _linha_slot(maos_frame, slot_key, label)

        # ── PROTEÇÕES ────────────────────────────────────────────────────────
        prot_frame = tk.Frame(char_frame, bg="#1f0b3f")
        prot_frame.pack(fill="x", padx=12, pady=(2, 4))
        def _tooltip_protecoes():
            linhas = []
            for regiao, item in char.regioes_corpo.items():
                if item:
                    defesa = getattr(item, "defesa", None) or getattr(item, "Defesa", None)
                    extra  = f"  (def {defesa})" if defesa is not None else ""
                    linhas.append(f"✅ {regiao.capitalize()}: {item.nome}{extra}")
                else:
                    linhas.append(f"○  {regiao.capitalize()}: —")
            return "\n".join(linhas) if linhas else "Nenhuma proteção equipada"
        equipadas = [v for v in char.regioes_corpo.values() if v]
        lbl_prot = tk.Label(prot_frame, text=f"🛡 Proteções  {len(equipadas)}/{len(char.regioes_corpo)}", bg="#1f0b3f", fg="#90caf9", font=("Arial", 9, "bold"), cursor="hand2", anchor="w")
        lbl_prot.pack(fill="x")
        Tooltip(lbl_prot, _tooltip_protecoes())

        # ── PAINEL DE ABAS ───────────────────────────────────────────────────
        abas_container = tk.Frame(char_frame, bg="#130f26", relief="solid", bd=1)
        abas_container.pack(fill="x", padx=8, pady=6)
        abas_bar = tk.Frame(abas_container, bg="#0d0824")
        abas_bar.pack(fill="x")
        conteudo_frame = tk.Frame(abas_container, bg="#1a0f35", height=120)
        conteudo_frame.pack(fill="x")
        conteudo_frame.pack_propagate(False)
        COR_ATIVA = "#2d0a8c"; COR_INATIVA = "#0d0824"
        aba_ativa = {"btn": None}

        def _limpar_aba():
            if not conteudo_frame.winfo_exists(): return
            for w in conteudo_frame.winfo_children(): w.destroy()

        def _ativar(btn):
            if aba_ativa["btn"]: aba_ativa["btn"].config(bg=COR_INATIVA)
            btn.config(bg=COR_ATIVA); aba_ativa["btn"] = btn

        def _lista_scroll(linhas, com_tooltip=False):
            cv = tk.Canvas(conteudo_frame, bg="#1a0f35", highlightthickness=0)
            sb = tk.Scrollbar(conteudo_frame, orient="vertical", command=cv.yview)
            cv.configure(yscrollcommand=sb.set)
            sb.pack(side="right", fill="y"); cv.pack(side="left", fill="both", expand=True)
            inner = tk.Frame(cv, bg="#1a0f35")
            win = cv.create_window((0, 0), window=inner, anchor="nw")
            inner.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
            cv.bind("<Configure>", lambda e: cv.itemconfig(win, width=e.width))
            cv.bind("<Enter>", lambda e: cv.bind_all("<MouseWheel>", lambda ev: cv.yview_scroll(int(ev.delta / -90), "units")))
            cv.bind("<Leave>", lambda e: cv.unbind_all("<MouseWheel>"))
            for item in linhas:
                texto, cor = item[0], item[1]
                tip = item[2] if com_tooltip and len(item) > 2 else ""
                lbl = tk.Label(inner, text=texto, bg="#1a0f35", fg=cor, font=("Arial", 9), anchor="w", wraplength=310, justify="left")
                lbl.pack(fill="x", padx=6, pady=1)
                if tip: Tooltip(lbl, tip)

        def _aba_mods():
            _limpar_aba(); _ativar(btn_mods)
            linhas = []
            testes = {k: char.bonus_testes.get(k, 0) + char.mod_testes.get(k, 0)
                      for k in set(list(char.bonus_testes) + list(char.mod_testes))}
            for k, v in testes.items():
                if v: linhas.append((f"🎲 {k.capitalize()}: {'+' if v>0 else ''}{v}", "#90caf9"))
            for k, v in char.bonus_atributos.items():
                if v: linhas.append((f"⚡ {k.capitalize()}: {'+' if v>0 else ''}{v}", "#ffd54f"))
            for k, v in char.mod_efeitos.items():
                if v: linhas.append((f"✨ {k.capitalize()}: {'+' if v>0 else ''}{v}", "#ce93d8"))
            if not linhas: linhas = [("Nenhum modificador ativo", "#555555")]
            _lista_scroll(linhas)

        def _aba_buffs():
            _limpar_aba(); _ativar(btn_buffs)
            linhas = []
            for e in char.buffs_debuffs.listar_efeitos():
                cor   = "#66bb6a" if str(e.tipo).lower() == "buff" else "#ef5350"
                icone = "⬆" if str(e.tipo).lower() == "buff" else "⬇"
                dur   = "∞" if e.eh_permanente() else ("imediato" if e.turnos_restantes == 0 else f"{e.turnos_restantes}t")
                linhas.append((f"{icone} {e.nome}  [{dur}]", cor, e.descricao or ""))
            if not linhas: linhas = [("Nenhum efeito ativo", "#555555", "")]
            _lista_scroll(linhas, com_tooltip=True)

        def _aba_habs():
            _limpar_aba(); _ativar(btn_habs)
            linhas = []

            # ── Habilidades padrão (antigas) ──────────────────────────────────────
            for h in char.habilidades.listar_habilidades():
                tags = h.tags  if isinstance(h.tags,  list) else [h.tags]
                vals = h.valor if isinstance(h.valor, list) else [h.valor] * len(tags)
                efts = " | ".join(f"{t}:{'+' if v>=0 else ''}{v}" for t, v in zip(tags, vals))
                custo = f"({h.custo}E)" if h.tipo == "ativo" else "(passivo)"
                linhas.append(("hab_antigo", h, f"⚔️ {h.nome} {custo}  {efts}", "#90caf9", h.descricao or ""))

            # ── Habilidades ofensivas ─────────────────────────────────────────────
            for h in char.habilidades.listar_habilidades_ofensivas():
                custos = []
                if h.custo_energia: custos.append(f"{h.custo_energia}E")
                if h.custo_mana:    custos.append(f"{h.custo_mana}M")
                custo = f"({'+ '.join(custos)})" if custos else "(grátis)"
                linhas.append(("hab_ofensivo", h, f"⚔️ {h.nome} {custo}", "#f4a261", h.descricao or ""))

            if not linhas:
                cv = tk.Canvas(conteudo_frame, bg="#1a0f35", highlightthickness=0)
                cv.pack(fill="both", expand=True)
                tk.Label(cv, text="Nenhuma habilidade", bg="#1a0f35", fg="#555555", font=("Arial", 9)).pack(pady=8)
                return

            cv = tk.Canvas(conteudo_frame, bg="#1a0f35", highlightthickness=0)
            sb = tk.Scrollbar(conteudo_frame, orient="vertical", command=cv.yview)
            cv.configure(yscrollcommand=sb.set)
            sb.pack(side="right", fill="y"); cv.pack(side="left", fill="both", expand=True)
            inner = tk.Frame(cv, bg="#1a0f35")
            win = cv.create_window((0, 0), window=inner, anchor="nw")
            inner.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
            cv.bind("<Configure>", lambda e: cv.itemconfig(win, width=e.width))
            cv.bind("<Enter>", lambda e: cv.bind_all("<MouseWheel>", lambda ev: cv.yview_scroll(int(ev.delta / -90), "units")))
            cv.bind("<Leave>", lambda e: cv.unbind_all("<MouseWheel>"))

            for tipo_item, item_obj, texto, cor, desc in linhas:
                btn = tk.Button(inner, text=texto, bg="#1a0f35", fg=cor,
                                font=("Arial", 9), anchor="w", relief="flat",
                                cursor="hand2", activebackground="#2a1f55",
                                activeforeground="white")
                btn.pack(fill="x", padx=6, pady=1)
                if desc: Tooltip(btn, desc)

                menu = tk.Menu(inner, tearoff=0)

                if tipo_item == "hab_antigo":
                    if item_obj.tipo == "ativo":
                        def _usar_hab(h=item_obj):
                            if char.EnergiaAtual < h.custo:
                                self.adicionar_log(f"❌ {char.nome} sem energia para '{h.nome}'.", "red"); return
                            char.ModificarEnergia(-h.custo)
                            tags = h.tags  if isinstance(h.tags,  list) else [h.tags]
                            vals = h.valor if isinstance(h.valor, list) else [h.valor] * len(tags)
                            if h.duracao:
                                from_efeito = [{"tags": [t], "valor": v, "por_turno": h.por_turno} for t, v in zip(tags, vals)]
                                efeito_temp = CB.BuffDebuff(nome=h.nome, duracao=h.duracao, efeito=from_efeito, descricao=h.descricao, tipo="buff")
                                char.buffs_debuffs.adicionar_efeito_objeto(efeito_temp)
                                self.adicionar_log(f"⚔️ {char.nome} usou '{h.nome}' ({h.duracao}t)", "#90caf9")
                            else:
                                for t, v in zip(tags, vals):
                                    char.aplicar_modificador_generico(tags=[t], valor=v)
                                self.adicionar_log(f"⚔️ {char.nome} usou '{h.nome}' (imediato)", "#90caf9")
                            self.refresh()
                        menu.add_command(label="▶ Usar", command=_usar_hab)
                    else:
                        menu.add_command(label="▶ Passivo (sempre ativo)", state="disabled")

                elif tipo_item == "hab_ofensivo":
                    def _usar_hab_ofensivo(h=item_obj):
                        self._rotear_ofensivo(char, h)
                    menu.add_command(label="▶ Usar", command=_usar_hab_ofensivo)

                def _detalhes_hab(h=item_obj, ti=tipo_item):
                    self._popup_detalhes_hab_pod(char, h, ti)
                menu.add_command(label="🔍 Detalhes", command=_detalhes_hab)

                btn.config(command=lambda m=menu, b=btn: m.tk_popup(b.winfo_rootx(), b.winfo_rooty() + b.winfo_height()))

        def _aba_pods():
            _limpar_aba(); _ativar(btn_pods)
            linhas = []

            # ── Poderes padrão (antigos) ──────────────────────────────────────────
            for p in char.poderes.listar_poderes():
                tags = p.tags  if isinstance(p.tags,  list) else [p.tags]
                vals = p.valor if isinstance(p.valor, list) else [p.valor] * len(tags)
                efts = " | ".join(f"{t}:{'+' if v>=0 else ''}{v}" for t, v in zip(tags, vals))
                custo = f"({p.custo}E)" if p.tipo == "ativo" else "(passivo)"
                linhas.append(("pod_antigo", p, f"🔮 {p.nome} {custo}  {efts}", "#ce93d8", p.descricao or ""))

            # ── Poderes ofensivos ─────────────────────────────────────────────────
            for p in char.poderes.listar_poderes_ofensivos():
                custos = []
                if p.custo_energia: custos.append(f"{p.custo_energia}E")
                if p.custo_mana:    custos.append(f"{p.custo_mana}M")
                custo = f"({'+ '.join(custos)})" if custos else "(grátis)"
                linhas.append(("pod_ofensivo", p, f"🔮 {p.nome} {custo}", "#f77f00", p.descricao or ""))

            if not linhas:
                cv = tk.Canvas(conteudo_frame, bg="#1a0f35", highlightthickness=0)
                cv.pack(fill="both", expand=True)
                tk.Label(cv, text="Nenhum poder", bg="#1a0f35", fg="#555555", font=("Arial", 9)).pack(pady=8)
                return

            cv = tk.Canvas(conteudo_frame, bg="#1a0f35", highlightthickness=0)
            sb = tk.Scrollbar(conteudo_frame, orient="vertical", command=cv.yview)
            cv.configure(yscrollcommand=sb.set)
            sb.pack(side="right", fill="y"); cv.pack(side="left", fill="both", expand=True)
            inner = tk.Frame(cv, bg="#1a0f35")
            win = cv.create_window((0, 0), window=inner, anchor="nw")
            inner.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
            cv.bind("<Configure>", lambda e: cv.itemconfig(win, width=e.width))
            cv.bind("<Enter>", lambda e: cv.bind_all("<MouseWheel>", lambda ev: cv.yview_scroll(int(ev.delta / -90), "units")))
            cv.bind("<Leave>", lambda e: cv.unbind_all("<MouseWheel>"))

            for tipo_item, item_obj, texto, cor, desc in linhas:
                btn = tk.Button(inner, text=texto, bg="#1a0f35", fg=cor,
                                font=("Arial", 9), anchor="w", relief="flat",
                                cursor="hand2", activebackground="#2a1f55",
                                activeforeground="white")
                btn.pack(fill="x", padx=6, pady=1)
                if desc: Tooltip(btn, desc)

                menu = tk.Menu(inner, tearoff=0)

                if tipo_item == "pod_antigo":
                    if item_obj.tipo == "ativo":
                        def _usar_pod(p=item_obj):
                            if char.EnergiaAtual < p.custo:
                                self.adicionar_log(f"❌ {char.nome} sem energia para '{p.nome}'.", "red"); return
                            p.usar(char)
                            self.adicionar_log(f"🔮 {char.nome} usou '{p.nome}'", "#ce93d8")
                            self.refresh()
                        menu.add_command(label="▶ Usar", command=_usar_pod)
                    else:
                        menu.add_command(label="▶ Passivo (sempre ativo)", state="disabled")

                elif tipo_item == "pod_ofensivo":
                    def _usar_pod_ofensivo(p=item_obj):
                        self._rotear_ofensivo(char, p)
                    menu.add_command(label="▶ Usar", command=_usar_pod_ofensivo)

                def _detalhes_pod(p=item_obj, ti=tipo_item):
                    self._popup_detalhes_hab_pod(char, p, ti)
                menu.add_command(label="🔍 Detalhes", command=_detalhes_pod)

                btn.config(command=lambda m=menu, b=btn: m.tk_popup(b.winfo_rootx(), b.winfo_rooty() + b.winfo_height()))

        def _aba_inv():
            _limpar_aba(); _ativar(btn_inv)
            cv = tk.Canvas(conteudo_frame, bg="#1a0f35", highlightthickness=0)
            sb = tk.Scrollbar(conteudo_frame, orient="vertical", command=cv.yview)
            cv.configure(yscrollcommand=sb.set)
            sb.pack(side="right", fill="y"); cv.pack(side="left", fill="both", expand=True)
            inner = tk.Frame(cv, bg="#1a0f35")
            win = cv.create_window((0, 0), window=inner, anchor="nw")
            inner.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
            cv.bind("<Configure>", lambda e: cv.itemconfig(win, width=e.width))
            cv.bind("<Enter>", lambda e: cv.bind_all("<MouseWheel>", lambda ev: cv.yview_scroll(int(ev.delta / -90), "units")))
            cv.bind("<Leave>", lambda e: cv.unbind_all("<MouseWheel>"))

            def _atualizar_inv():
                for w in inner.winfo_children(): w.destroy()
                itens = char.inventario.listar_itens()
                if not itens:
                    tk.Label(inner, text="Inventário vazio", bg="#1a0f35", fg="#555555",
                             font=("Arial", 9, "italic")).pack(padx=6, pady=4)
                    return

                def _refresh_card_e_inv():self.atualizar_card_turno_atual()

                for entrada in itens:
                    item_obj  = entrada["objeto"]
                    item_nome = entrada["nome"]
                    quantidade = entrada["quantidade"]
                    texto = f"{item_nome}  (×{quantidade})" if quantidade > 1 else item_nome

                    f = tk.Frame(inner, bg="#220840", relief="flat")
                    f.pack(fill="x", padx=4, pady=2)

                    btn = tk.Button(f, text=texto, bg="#2a0d50", fg="white", font=("Arial", 9),
                                    anchor="w", relief=tk.FLAT, borderwidth=0)
                    btn.pack(fill="x", ipady=3, ipadx=6)
                    Tooltip(btn, self._gerar_texto_tooltip_item(item_obj))

                    menu = tk.Menu(btn, tearoff=0)

                    # Equipar
                    if isinstance(item_obj, (CB.Melee, CB.Ranged)) or \
                       char._eh_protecao(item_obj) or isinstance(item_obj, CB.Equipamento):
                        menu.add_command(
                            label="Equipar Direto",
                            command=lambda i=item_obj: [self._equipar_item_combate(char, i), _refresh_card_e_inv()])
                        menu.add_command(
                            label="Equipar (slot)",
                            command=lambda i=item_obj: self._abrir_popup_slot_combate(char, i, _refresh_card_e_inv))
                        if isinstance(item_obj, CB.Ranged):
                            menu.add_command(
                                label="Descarregar",
                                command=lambda i=item_obj: [self.abrir_popup_descarregar_quantidade(char, i), _refresh_card_e_inv()])
                        menu.add_separator()

                    if isinstance(item_obj, CB.Consumivel):
                        if self._consumivel_eh_area(item_obj):
                            menu.add_command(
                                label="💥 Usar em Área",
                                command=lambda i=item_obj, p=char: self._usar_consumivel_area(i, p),
                                background="#1a0869",
                                foreground="#ff8844"
                            )
                        else:
                            menu.add_command(
                                label="🧪 Usar Agora",
                                command=lambda i=item_obj, p=char: self._usar_consumivel_simples(i, p),
                                background="#1a0869",
                                foreground="#90caf9"
                            )
                        menu.add_separator()

                    # Descartar
                    if quantidade > 1:
                        menu.add_command(label="Descartar 1",
                            command=lambda i=item_obj: [char.inventario.remover_item(i, 1), _refresh_card_e_inv()])
                        if quantidade >= 5:
                            menu.add_command(label="Descartar 5",
                                command=lambda i=item_obj: [char.inventario.remover_item(i, 5), _refresh_card_e_inv()])
                        if quantidade >= 10:
                            menu.add_command(label="Descartar 10",
                                command=lambda i=item_obj: [char.inventario.remover_item(i, 10), _refresh_card_e_inv()])
                        menu.add_separator()
                        menu.add_command(label="Descartar Tudo",
                            command=lambda i=item_obj, q=quantidade: [char.inventario.remover_item(i, q), _refresh_card_e_inv()])
                    else:
                        menu.add_command(label="Descartar",
                            command=lambda i=item_obj: [char.inventario.remover_item(i, 1), _refresh_card_e_inv()])

                    btn.config(command=lambda m=menu, b=btn:
                               m.tk_popup(b.winfo_rootx(), b.winfo_rooty() + b.winfo_height()))

            _atualizar_inv()

        btn_mods  = tk.Button(abas_bar, text="Mods",        bg=COR_INATIVA, fg="white", font=("Arial", 9, "bold"), relief="flat", padx=4, pady=3, activebackground=COR_ATIVA, activeforeground="white", command=_aba_mods)
        btn_buffs = tk.Button(abas_bar, text="Buffs",       bg=COR_INATIVA, fg="white", font=("Arial", 9, "bold"), relief="flat", padx=4, pady=3, activebackground=COR_ATIVA, activeforeground="white", command=_aba_buffs)
        btn_habs  = tk.Button(abas_bar, text="Habilidades", bg=COR_INATIVA, fg="white", font=("Arial", 9, "bold"), relief="flat", padx=4, pady=3, activebackground=COR_ATIVA, activeforeground="white", command=_aba_habs)
        btn_pods  = tk.Button(abas_bar, text="Poderes",     bg=COR_INATIVA, fg="white", font=("Arial", 9, "bold"), relief="flat", padx=4, pady=3, activebackground=COR_ATIVA, activeforeground="white", command=_aba_pods)
        btn_inv   = tk.Button(abas_bar, text="Inventário",  bg=COR_INATIVA, fg="white", font=("Arial", 9, "bold"), relief="flat", padx=4, pady=3, activebackground=COR_ATIVA, activeforeground="white", command=_aba_inv)
        for b in (btn_mods, btn_buffs, btn_habs, btn_pods, btn_inv):
            b.pack(side="left", fill="x", expand=True)
        _aba_buffs()

        # ── AÇÕES RÁPIDAS ─────────────────────────────────────────────────────
        acoes_frame = tk.Frame(char_frame, bg="#220866")
        acoes_frame.pack(fill="x", pady=(6, 10))
        tk.Button(acoes_frame, text="⚔️ Ações",   bg="#7b2cbf", fg="white", font=("Arial", 11, "bold"), command=lambda c=char: self.abrir_popup_acoes(c)).pack(fill="x", padx=20, pady=3)
        tk.Button(acoes_frame, text="🎲 Rolagem", bg="#0a3d5c", fg="white",command=lambda c=char: abrir_popup_rolagem_personagem(self, c, self.adicionar_log)).pack(fill="x", padx=20, pady=3)
        tk.Button(acoes_frame, text="📋 Detalhes", bg="#1a0869", fg="white", font=("Arial", 10), command=lambda c=char: self.controller.abrir_detalhes(c)).pack(fill="x", padx=20, pady=3)

        # ── TURNO INFO ────────────────────────────────────────────────────────
        turno_info = tk.Frame(char_frame, bg="#130f26")
        turno_info.pack(fill="x", padx=12, pady=(0, 8))
        tk.Label(turno_info, text="Ações Restantes: 2", bg="#130f26", fg="lightgreen", font=("Arial", 10, "bold")).pack(anchor="w")
        tk.Label(turno_info, text="Reação: Disponível",  bg="#130f26", fg="orange",     font=("Arial", 9)).pack(anchor="w")

    def _renderizar_card(self, char):
        """Limpa frame_turno_atual e renderiza o card de 'char'."""
        for widget in self.frame_turno_atual.winfo_children():
            if not (isinstance(widget, tk.Label) and widget.cget("text") == "Turno Atual"):
                widget.destroy()
        if not any(isinstance(w, tk.Label) and w.cget("text") == "Turno Atual"
                   for w in self.frame_turno_atual.winfo_children()):
            tk.Label(self.frame_turno_atual, text="Turno Atual",fg="white", bg="#1a0869", font=("Arial", 16, "bold")).pack(pady=10)
        self._construir_conteudo_card(char)
    ### Card personagem ###

    ### Barras ###
    def _setar_barra_combate(self, personagem, atributo_atual, atributo_max,canvas_widget, event):
        """Clique / arrasto nas barras do card de combate."""
        try:
            largura = canvas_widget.winfo_width()
            if largura <= 1:
                return
            proporcao = max(0.0, min(1.0, event.x / largura))
            maximo    = getattr(personagem, atributo_max)
            setattr(personagem, atributo_atual, int(maximo * proporcao))
            self._redesenhar_barra(canvas_widget,getattr(personagem, atributo_atual),maximo,canvas_widget._cor)
            if hasattr(canvas_widget, "_label_ref"):
                canvas_widget._label_ref.config(
                    text=f"{getattr(personagem, atributo_atual)}/{maximo}")
        except Exception as e:
            print("Erro ao setar barra combate:", e)

    def _redesenhar_barra(self, canvas_widget, atual, maximo, cor):
        """Redesenha o conteúdo de um canvas-barra."""
        canvas_widget.delete("all")
        w = canvas_widget.winfo_width()
        if w <= 1: w = 340
        h = int(canvas_widget.cget("height"))
        prop = 0 if maximo == 0 else max(0, min(1, atual / maximo))
        canvas_widget.create_rectangle(0, 0, int(w * prop), h, fill=cor, width=0)
        canvas_widget.create_text(w // 2, h // 2,text=f"{atual}/{maximo}",fill="white", font=("Arial", 8, "bold"))
    ### Barras ###

    ### Funções para armas ###
    def _trocar_arma_slot(self, char, slot_origem_key):
        try:
            slot_origem = char.slots.get(slot_origem_key)
            if not slot_origem or not slot_origem.item:
                return
            arma_origem = slot_origem.item
            eh_mao = slot_origem.tipo == "mao"
            if eh_mao:
                # ── mão → suporte ────────────────────────────────────────────
                slots_destino = [(k, s) for k, s in char.slots.items() if s.tipo == "suporte"]
            else:
                # ── suporte → mão ────────────────────────────────────────────
                slots_destino = [(k, s) for k, s in char.slots.items() if s.tipo == "mao"]
            if not slots_destino:
                return
            # prefere slot com item para fazer swap; senão usa slot vazio
            slot_com_item = next(((k, s) for k, s in slots_destino if s.item),  None)
            slot_sem_item = next(((k, s) for k, s in slots_destino if not s.item), None)
            alvo_key, slot_alvo = slot_com_item or slot_sem_item
            arma_alvo = slot_alvo.item   # pode ser None
            # 1. Devolve arma de origem ao inventário
            char.desequipar_item_generico(arma_origem)
            # 2. Se havia arma no destino, devolve ela também
            if arma_alvo:
                char.desequipar_item_generico(arma_alvo)
            # 3. Equipa arma_origem no destino
            char.equipar_item(arma_origem, nome_slot=alvo_key, forcar=True)
            # 4. Se havia arma no destino, equipa ela na origem
            if arma_alvo:
                char.equipar_item(arma_alvo, nome_slot=slot_origem_key, forcar=True)
            self.atualizar_card_turno_atual()
        except Exception as e:
            print("Erro ao trocar arma de slot:", e)
            import traceback; traceback.print_exc()

    def _guardar_arma_slot(self, char, slot_key):
        """Desequipa a arma do slot e devolve ao inventário."""
        try:
            slot = char.slots.get(slot_key)
            if not slot or not slot.item:
                return
            char.inventario.adicionar_item_objeto(slot.item, 1)
            slot.item = None
            self.atualizar_card_turno_atual()
        except Exception as e:
            print("Erro ao guardar arma:", e)
    
    def _tooltip_arma(self, item):
        """Retorna string de tooltip com os detalhes relevantes da arma."""
        if item is None: return "Slot vazio"
        linhas = [item.nome]
        # dano
        dano = getattr(item, "dano", None) or getattr(item, "Dano", None)
        if dano: linhas.append(f"Dano: {dano}")
        # tipo de arma
        tipo = getattr(item, "tipo", None) or getattr(item, "Tipo", None)
        if tipo: linhas.append(f"Tipo: {tipo}")
        # ranged-específico
        muns = getattr(item, "munições",  None)
        cap  = getattr(item, "capacidade", None)
        if muns is not None and cap is not None: linhas.append(f"Munição: {muns}/{cap}")
        modo = getattr(item, "modo_disparo", None) or getattr(item, "ModoDisparo", None)
        if modo: linhas.append(f"Modo: {modo}")
        # tenta descobrir o tipo de munição carregada
        mun_obj = getattr(item, "municao_carregada", None) or getattr(item, "municao", None)
        if mun_obj:
            nome_mun = getattr(mun_obj, "nome", str(mun_obj))
            linhas.append(f"Munição carregada: {nome_mun}")
        elif hasattr(item, "calibre"): linhas.append(f"Calibre: {item.calibre}")
        return "\n".join(linhas)
    ### Funções para armas ###

    def abrir_popup_ajuste_global(self):
        popup = tk.Toplevel(self)
        popup.title("Ajuste Global de Recursos")
        popup.configure(bg="#1a1a2e")
        popup.geometry("600x700")
        popup.resizable(False, False)

        tk.Label(popup, text="⚙ Ajuste Global de Vida, Energia e Mana", bg="#1a1a2e", fg="white", font=("Arial", 14, "bold")).pack(pady=15)

        main = tk.Frame(popup, bg="#1a1a2e")
        main.pack(fill="both", expand=True, padx=20)

        # ---------------- ALVO ----------------
        alvo_frame = tk.LabelFrame(main, text="Alvo", bg="#1a1a2e", fg="white", font=("Arial", 11, "bold"))
        alvo_frame.pack(fill="x", pady=10)

        alvo_var = tk.StringVar(value="superior")

        tk.Radiobutton(alvo_frame, text="Lista Superior", variable=alvo_var, value="superior", bg="#1a1a2e", fg="white", selectcolor="#2d0a8c").pack(anchor="w")
        tk.Radiobutton(alvo_frame, text="Lista Inferior", variable=alvo_var, value="inferior", bg="#1a1a2e", fg="white", selectcolor="#2d0a8c").pack(anchor="w")
        tk.Radiobutton(alvo_frame, text="Ambos", variable=alvo_var, value="ambos", bg="#1a1a2e", fg="white", selectcolor="#2d0a8c").pack(anchor="w")

        # ---------------- ATRIBUTOS ----------------
        attr_frame = tk.LabelFrame(main, text="Recursos", bg="#1a1a2e", fg="white", font=("Arial", 11, "bold"))
        attr_frame.pack(fill="x", pady=10)

        vida_var = tk.BooleanVar()
        energia_var = tk.BooleanVar()
        mana_var = tk.BooleanVar()

        tk.Checkbutton(attr_frame, text="Vida", variable=vida_var, bg="#1a1a2e", fg="white", selectcolor="#2d0a8c").pack(anchor="w")
        tk.Checkbutton(attr_frame, text="Energia", variable=energia_var, bg="#1a1a2e", fg="white", selectcolor="#2d0a8c").pack(anchor="w")
        tk.Checkbutton(attr_frame, text="Mana", variable=mana_var, bg="#1a1a2e", fg="white", selectcolor="#2d0a8c").pack(anchor="w")

        # ---------------- TIPO ----------------
        tipo_frame = tk.LabelFrame(main, text="Tipo de Modificação", bg="#1a1a2e", fg="white", font=("Arial", 11, "bold"))
        tipo_frame.pack(fill="x", pady=10)

        tipo_var = tk.StringVar(value="somar")

        tk.Radiobutton(tipo_frame, text="Somar", variable=tipo_var, value="somar", bg="#1a1a2e", fg="white", selectcolor="#2d0a8c").pack(anchor="w")
        tk.Radiobutton(tipo_frame, text="Subtrair", variable=tipo_var, value="subtrair", bg="#1a1a2e", fg="white", selectcolor="#2d0a8c").pack(anchor="w")
        tk.Radiobutton(tipo_frame, text="Definir valor fixo", variable=tipo_var, value="fixar", bg="#1a1a2e", fg="white", selectcolor="#2d0a8c").pack(anchor="w")
        tk.Radiobutton(tipo_frame, text="Restaurar para máximo", variable=tipo_var, value="maximo", bg="#1a1a2e", fg="white", selectcolor="#2d0a8c").pack(anchor="w")

        valor_frame = tk.Frame(main, bg="#1a1a2e")
        valor_frame.pack(pady=5)

        tk.Label(valor_frame, text="Valor:", bg="#1a1a2e", fg="white").pack(side="left", padx=5)
        valor_entry = tk.Entry(valor_frame, width=10)
        valor_entry.pack(side="left")

        # ---------------- OPÇÕES EXTRA ----------------
        extra_frame = tk.LabelFrame(main, text="Opções", bg="#1a1a2e", fg="white", font=("Arial", 11, "bold"))
        extra_frame.pack(fill="x", pady=10)

        permitir_ultrapassar = tk.BooleanVar()
        permitir_negativo = tk.BooleanVar()

        tk.Checkbutton(extra_frame, text="Permitir ultrapassar máximo", variable=permitir_ultrapassar, bg="#1a1a2e", fg="white", selectcolor="#2d0a8c").pack(anchor="w")
        tk.Checkbutton(extra_frame, text="Permitir ficar abaixo de 0", variable=permitir_negativo, bg="#1a1a2e", fg="white", selectcolor="#2d0a8c").pack(anchor="w")

        # ---------------- APLICAR ----------------
        def aplicar():
            try:
                valor = int(valor_entry.get()) if valor_entry.get() else 0
            except:
                self.adicionar_log("Valor inválido para ajuste global.", "red")
                return

            grupos = []
            if alvo_var.get() == "superior":
                grupos = D.GruposDePersonagens.get("_lista_superior", [])
            elif alvo_var.get() == "inferior":
                grupos = D.GruposDePersonagens.get("_lista_inferior", [])
            else:
                grupos = D.GruposDePersonagens.get("_lista_superior", []) + D.GruposDePersonagens.get("_lista_inferior", [])

            if not grupos:
                self.adicionar_log("Nenhum personagem encontrado para ajuste.", "gray")
                return

            atributos = []
            if vida_var.get(): atributos.append(("VidaAtual", "VidaMax", "❤ Vida"))
            if energia_var.get(): atributos.append(("EnergiaAtual", "EnergiaMax", "⚡ Energia"))
            if mana_var.get(): atributos.append(("ManaAtual", "ManaMax", "🔮 Mana"))

            if not atributos:
                self.adicionar_log("Nenhum recurso selecionado para ajuste.", "gray")
                return

            for personagem in grupos:
                for atual, maximo, _ in atributos:
                    valor_atual = getattr(personagem, atual)
                    valor_max = getattr(personagem, maximo)

                    if tipo_var.get() == "somar":
                        novo = valor_atual + valor
                    elif tipo_var.get() == "subtrair":
                        novo = valor_atual - valor
                    elif tipo_var.get() == "fixar":
                        novo = valor
                    elif tipo_var.get() == "maximo":
                        novo = valor_max
                    else:
                        novo = valor_atual

                    if not permitir_ultrapassar.get():
                        novo = min(novo, valor_max)
                    if not permitir_negativo.get():
                        novo = max(novo, 0)

                    setattr(personagem, atual, novo)

            resumo_attr = ", ".join([a[2] for a in atributos])
            self.adicionar_log(f"⚙ Ajuste Global aplicado em {len(grupos)} personagem(ns): {resumo_attr}", "cyan")

            self._refresh_listas_highlight()
            self.atualizar_card_turno_atual()
            popup.destroy()

        botoes = tk.Frame(popup, bg="#1a1a2e")
        botoes.pack(pady=15)

        tk.Button(botoes, text="Confirmar", command=aplicar, bg="#38b000", fg="white", font=("Arial", 12, "bold"), width=15).pack(side="left", padx=10)
        tk.Button(botoes, text="Cancelar", command=popup.destroy, bg="#8B0000", fg="white", font=("Arial", 12, "bold"), width=15).pack(side="left", padx=10)

    def _remover_do_combate(self, personagem):
        """Remove o personagem da fila de turno e das listas superiores/inferiores."""
        # fila de turno
        if personagem in self.ordem_turno:
            idx = self.ordem_turno.index(personagem)
            self.ordem_turno.remove(personagem)
            if self.turno_atual_index >= len(self.ordem_turno) and self.ordem_turno:
                self.turno_atual_index = 0
            elif idx < self.turno_atual_index:
                self.turno_atual_index = max(0, self.turno_atual_index - 1)

        # listas de combate
        for chave in ("_lista_superior", "_lista_inferior"):
            lista = D.GruposDePersonagens.get(chave, [])
            if personagem in lista:
                lista.remove(personagem)

        self.atualizar_fila_turno()
        self.atualizar_card_turno_atual()
        self.refresh()
    
    # Funções do card #
    def abrir_popup_pilhagem_card(self, receptor):
        popup = tk.Toplevel(self)
        popup.title(f"Pilhagem — {receptor.nome}")
        popup.configure(bg="#1a1a2e")
        popup.geometry("900x520")
        popup.resizable(False, False)

        # Personagens disponíveis para pilhar (listas de combate, excluindo receptor)
        todos = []
        for chave in ("_lista_superior", "_lista_inferior"):
            todos += D.GruposDePersonagens.get(chave, [])
        alvos = [p for p in todos if p is not receptor]

        if not alvos:
            tk.Label(popup, text="Nenhum alvo disponível na cena.", bg="#1a1a2e", fg="red",
                     font=("Arial", 13)).pack(pady=60)
            tk.Button(popup, text="Fechar", command=popup.destroy, bg="#8B0000", fg="white").pack()
            return

        alvo_var = tk.StringVar(value=alvos[0].nome)

        # Header
        header = tk.Frame(popup, bg="#1a1a2e")
        header.pack(fill="x", padx=16, pady=10)
        tk.Label(header, text=f"Receptor: {receptor.nome}", bg="#1a1a2e", fg="#ffd700",
                 font=("Arial", 12, "bold")).pack(side="left")
        tk.Label(header, text="Pilhar de:", bg="#1a1a2e", fg="white", font=("Arial", 11)).pack(side="left", padx=(30, 6))
        alvo_combo = ttk.Combobox(header, textvariable=alvo_var, state="readonly",
                                   values=[p.nome for p in alvos], width=22)
        alvo_combo.pack(side="left")

        # Paineis
        paineis = tk.Frame(popup, bg="#1a1a2e")
        paineis.pack(fill="both", expand=True, padx=16, pady=(0, 8))

        # Painel receptor (esquerda) — só exibe, não permite transferir de volta
        frame_rec = tk.LabelFrame(paineis, text=f"Inventário de {receptor.nome}",
                                   bg="#130f26", fg="#ffd700", font=("Arial", 10, "bold"))
        frame_rec.pack(side="left", fill="both", expand=True, padx=(0, 6))
        canvas_rec = tk.Canvas(frame_rec, bg="#130f26", highlightthickness=0)
        sb_rec = tk.Scrollbar(frame_rec, orient="vertical", command=canvas_rec.yview)
        canvas_rec.configure(yscrollcommand=sb_rec.set)
        sb_rec.pack(side="right", fill="y"); canvas_rec.pack(side="left", fill="both", expand=True)
        inner_rec = tk.Frame(canvas_rec, bg="#130f26")
        canvas_rec.create_window((0, 0), window=inner_rec, anchor="nw")
        inner_rec.bind("<Configure>", lambda e: canvas_rec.configure(scrollregion=canvas_rec.bbox("all")))

        # Painel alvo (direita) — itens clicáveis para transferir
        frame_alvo = tk.LabelFrame(paineis, text="Alvo",
                                    bg="#130f26", fg="#ff9944", font=("Arial", 10, "bold"))
        frame_alvo.pack(side="left", fill="both", expand=True, padx=(6, 0))
        canvas_alvo = tk.Canvas(frame_alvo, bg="#130f26", highlightthickness=0)
        sb_alvo = tk.Scrollbar(frame_alvo, orient="vertical", command=canvas_alvo.yview)
        canvas_alvo.configure(yscrollcommand=sb_alvo.set)
        sb_alvo.pack(side="right", fill="y"); canvas_alvo.pack(side="left", fill="both", expand=True)
        inner_alvo = tk.Frame(canvas_alvo, bg="#130f26")
        canvas_alvo.create_window((0, 0), window=inner_alvo, anchor="nw")
        inner_alvo.bind("<Configure>", lambda e: canvas_alvo.configure(scrollregion=canvas_alvo.bbox("all")))

        def _transferir(item_obj, alvo_obj, quantidade):
            alvo_obj.inventario.remover_item(item_obj, quantidade)
            receptor.inventario.adicionar_item_objeto(item_obj, quantidade)
            self.refresh()
            _atualizar()

        def _pilhar_tudo():
            alvo = next((p for p in alvos if p.nome == alvo_var.get()), None)
            if not alvo: return
            for entrada in list(alvo.inventario.itens):
                item = entrada["item"]; qtd = entrada.get("quantidade", 1)
                alvo.inventario.remover_item(item, qtd)
                receptor.inventario.adicionar_item_objeto(item, qtd)
            self.refresh(); _atualizar()

        def _atualizar(*_):
            for w in inner_rec.winfo_children(): w.destroy()
            for w in inner_alvo.winfo_children(): w.destroy()

            alvo = next((p for p in alvos if p.nome == alvo_var.get()), None)
            frame_alvo.config(text=f"Inventário de {alvo.nome}" if alvo else "Alvo")

            # Receptor — só exibição
            for entrada in receptor.inventario.itens:
                item = entrada["item"]; qtd = entrada.get("quantidade", 1)
                nome = getattr(item, "nome", str(item))
                txt = f"{nome} ×{qtd}" if qtd > 1 else nome
                tk.Label(inner_rec, text=txt, bg="#130f26", fg="#cccccc",
                         font=("Arial", 10), anchor="w").pack(fill="x", padx=8, pady=1)

            if not receptor.inventario.itens:
                tk.Label(inner_rec, text="Inventário vazio", bg="#130f26", fg="#555",
                         font=("Arial", 9, "italic")).pack(padx=8, pady=4)

            # Alvo — clicável
            if alvo:
                for entrada in list(alvo.inventario.itens):
                    item = entrada["item"]; qtd = entrada.get("quantidade", 1)
                    nome = getattr(item, "nome", str(item))
                    txt = f"{nome} ×{qtd}" if qtd > 1 else nome
                    f = tk.Frame(inner_alvo, bg="#1a0f35")
                    f.pack(fill="x", padx=6, pady=2)
                    lbl = tk.Label(f, text=txt, bg="#1a0f35", fg="white",font=("Arial", 10), anchor="w", cursor="hand2")
                    lbl.pack(fill="x", padx=4, pady=2)
                    lbl.bind("<Button-1>",  lambda e, i=item, a=alvo: _transferir(i, a, 1))
                    lbl.bind("<Button-3>",  lambda e, i=item, a=alvo, q=qtd: _transferir(i, a, q))
                    Tooltip(lbl, "Clique esquerdo: 1 item  |  Clique direito: tudo")
                if not alvo.inventario.itens:
                    tk.Label(inner_alvo, text="Inventário vazio", bg="#130f26", fg="#555",font=("Arial", 9, "italic")).pack(padx=8, pady=4)

        alvo_combo.bind("<<ComboboxSelected>>", _atualizar)

        # Rodapé
        rodape = tk.Frame(popup, bg="#1a1a2e")
        rodape.pack(fill="x", padx=16, pady=(0, 10))
        tk.Button(rodape, text="💰 Pilhar Tudo", command=_pilhar_tudo,bg="#7b4a00", fg="white", font=("Arial", 11), width=16).pack(side="left", padx=4)
        tk.Button(rodape, text="Fechar", command=popup.destroy,bg="#3a0a80", fg="white", font=("Arial", 11), width=12).pack(side="right", padx=4)
        tk.Label(rodape, text="Esq: 1 item  |  Dir: tudo", bg="#1a1a2e", fg="#666688",font=("Arial", 8)).pack(side="left", padx=8)

        _atualizar()

    def abrir_popup_pilhagem_central(self):
        popup = tk.Toplevel(self)
        popup.title("Pilhagem")
        popup.configure(bg="#130f26")
        popup.geometry("1300x680")
        popup.resizable(True, True)

        BG      = "#130f26"
        BG2     = "#1a0869"
        BG3     = "#220866"
        FG      = "white"
        FG_DIM  = "#888899"
        SEL_BG  = "#3d1080"

        mundo = CB.InventarioMundo.get()

        # ── helpers ──────────────────────────────────────────────────────────
        def _make_scrollable_frame(parent, bg=BG):
            cv = tk.Canvas(parent, bg=bg, highlightthickness=0)
            sb = tk.Scrollbar(parent, orient="vertical", command=cv.yview)
            cv.configure(yscrollcommand=sb.set)
            sb.pack(side="right", fill="y")
            cv.pack(side="left", fill="both", expand=True)
            inner = tk.Frame(cv, bg=bg)
            win = cv.create_window((0, 0), window=inner, anchor="nw")
            inner.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
            cv.bind("<Configure>", lambda e: cv.itemconfig(win, width=e.width))
            cv.bind("<Enter>", lambda e: cv.bind_all("<MouseWheel>", lambda ev: cv.yview_scroll(int(ev.delta / -90), "units")))
            cv.bind("<Leave>", lambda e: cv.unbind_all("<MouseWheel>"))
            return inner

        def _nome_item(item, qtd=1):
            n = getattr(item, "nome", str(item))
            return f"{n} ×{qtd}" if qtd > 1 else n

        def _get_itens_completos(personagem):
            """Retorna todos os itens deduplicated: inventário + slots + regiões + equipamentos.
            Usa dupla chave: id() do objeto Python E item.Id (UUID), para cobrir casos onde
            o mesmo item foi deserializado em objetos Python distintos mas tem o mesmo Id."""
            vistos_py  = {}   # id(objeto_python) -> chave_canonica
            vistos_can = {}   # chave_canonica    -> entrada_dict

            def _chave_can(item):
                item_id = getattr(item, "Id", None)
                return f"Id:{item_id}" if item_id else f"py:{id(item)}"

            def _recalc(entrada):
                origens = entrada["origens"]
                slots_ = [o.split(":", 1)[1] for o in origens if o.startswith("slot:")]
                corpo_ = [o.split(":", 1)[1] for o in origens if o.startswith("corpo:")]
                if slots_:
                    entrada["origem"] = "slot:" + "+".join(slots_)
                elif corpo_:
                    entrada["origem"] = "corpo:" + "+".join(corpo_)

            def _add(item, qtd, origem):
                py_key  = id(item)
                can_key = _chave_can(item)

                # já visto por id() Python
                if py_key in vistos_py:
                    can = vistos_py[py_key]
                    e   = vistos_can[can]
                    if origem not in e["origens"]:
                        e["origens"].append(origem)
                        _recalc(e)
                    return

                # já visto pela chave canônica (mesmo Id UUID, objeto diferente)
                if can_key in vistos_can:
                    vistos_py[py_key] = can_key
                    e = vistos_can[can_key]
                    if origem not in e["origens"]:
                        e["origens"].append(origem)
                        _recalc(e)
                    return

                # novo
                vistos_py[py_key]  = can_key
                vistos_can[can_key] = {
                    "item": item, "qtd": qtd,
                    "origem": origem, "origens": [origem]
                }

            # inventário
            for e in personagem.inventario.listar_itens():
                item = e.get("objeto") or e.get("item")
                if item:
                    _add(item, e.get("quantidade", 1), "inventário")

            # slots (armas)
            for slot in personagem.slots.values():
                if slot.item:
                    _add(slot.item, 1, f"slot:{slot.nome}")

            # regiões do corpo (proteções)
            for regiao, prot in getattr(personagem, "regioes_corpo", {}).items():
                if prot:
                    _add(prot, 1, f"corpo:{regiao}")

            # equipamentos_slots
            for eq in getattr(personagem, "equipamentos_slots", []):
                if eq:
                    _add(eq, 1, "slot:equipamento")

            return list(vistos_can.values())

        def _transferir_para_inventario(item, qtd, personagem_origem, origem_tipo):
            """Remove item de TODOS os slots/regiões onde ele estiver equipado."""
            for slot in personagem_origem.slots.values():
                if slot.item is item:
                    slot.item = None
            if hasattr(personagem_origem, "regioes_corpo"):
                for regiao, prot in list(personagem_origem.regioes_corpo.items()):
                    if prot is item:
                        personagem_origem.regioes_corpo[regiao] = None
            return True

        # ── estado de seleção ─────────────────────────────────────────────────
        sel_esq = {"pers": None, "btn": None}
        sel_dir = {"pers": None, "btn": None}

        grupos_disponiveis = [k for k in D.GruposDePersonagens.keys()
                               if not k.startswith("_") or k in ("_lista_superior", "_lista_inferior")]

        # fallback para nomes amigáveis
        def _nome_grupo(k):
            mapa = {"_lista_superior": "Lista Superior", "_lista_inferior": "Lista Inferior"}
            return mapa.get(k, k)

        nomes_grupos = [_nome_grupo(k) for k in grupos_disponiveis]
        chave_por_nome = {_nome_grupo(k): k for k in grupos_disponiveis}

        # ── LAYOUT PRINCIPAL (5 colunas) ──────────────────────────────────────
        main = tk.Frame(popup, bg=BG)
        main.pack(fill="both", expand=True, padx=8, pady=8)

        # configurar pesos das colunas para distribuição uniforme
        for i in range(5):
            main.columnconfigure(i, weight=1, uniform="col")
        main.rowconfigure(0, weight=0)
        main.rowconfigure(1, weight=1)

        # ── CABEÇALHOS ────────────────────────────────────────────────────────
        titulos = [
            ("👥 Grupo 1",          "#3a1080"),
            ("🎒 Inventário / Equip.", "#1a3d6e"),
            ("🌍 Mundo",            "#2a4a0a"),
            ("🎒 Inventário / Equip.", "#1a3d6e"),
            ("👥 Grupo 2",          "#3a1080"),
        ]
        for col, (txt, bg_hdr) in enumerate(titulos):
            tk.Label(main, text=txt, bg=bg_hdr, fg=FG,
                     font=("Arial", 10, "bold"), anchor="center",
                     relief="flat", pady=6).grid(row=0, column=col, sticky="ew", padx=3, pady=(0, 4))

        # ── FRAMES DAS COLUNAS ────────────────────────────────────────────────
        def _col_frame(col, bg=BG2):
            f = tk.Frame(main, bg=bg, bd=1, relief="solid")
            f.grid(row=1, column=col, sticky="nsew", padx=3)
            return f

        frm_g1   = _col_frame(0, "#110830")
        frm_inv1 = _col_frame(1, "#0d1e38")
        frm_mundo = _col_frame(2, "#0d1f0a")
        frm_inv2 = _col_frame(3, "#0d1e38")
        frm_g2   = _col_frame(4, "#110830")

        # ═══════════════════════════════════════════════════════════════════════
        # COLUNA 1 — Grupo Esquerdo
        # ═══════════════════════════════════════════════════════════════════════
        var_grupo_esq = tk.StringVar(value=nomes_grupos[0] if nomes_grupos else "")

        top_g1 = tk.Frame(frm_g1, bg="#110830")
        top_g1.pack(fill="x", padx=6, pady=(6, 2))
        tk.Label(top_g1, text="Grupo:", bg="#110830", fg=FG_DIM, font=("Arial", 8)).pack(side="left")
        combo_g1 = ttk.Combobox(top_g1, textvariable=var_grupo_esq, state="readonly",
                                  values=nomes_grupos, width=14)
        combo_g1.pack(side="left", padx=4)

        inner_g1 = _make_scrollable_frame(frm_g1, bg="#110830")

        def _render_grupo_esq(*_):
            for w in inner_g1.winfo_children(): w.destroy()
            chave = chave_por_nome.get(var_grupo_esq.get())
            if not chave: return
            for pers in D.GruposDePersonagens.get(chave, []):
                eh_sel    = sel_esq["pers"] is pers
                bloqueado = sel_dir["pers"] is pers  # já selecionado no lado direito
                if bloqueado:
                    bg_btn = "#2a1a1a"
                elif eh_sel:
                    bg_btn = SEL_BG
                else:
                    bg_btn = "#1a0869"
                border = 2 if eh_sel else 1
                f = tk.Frame(inner_g1, bg=bg_btn, bd=border, relief="solid",
                             highlightbackground="#9966ff" if eh_sel else ("#553333" if bloqueado else "#333366"),
                             highlightthickness=1)
                f.pack(fill="x", padx=4, pady=2)
                pv_txt = f"❤ {pers.VidaAtual}/{pers.VidaMax}"
                indicador = "▶ " if eh_sel else ("🚫 " if bloqueado else "  ")
                fg_cor = "#ffd700" if eh_sel else ("#555566" if bloqueado else FG)
                btn = tk.Button(f, text=f"{indicador}{pers.nome}\n{pv_txt}",
                                bg=bg_btn, fg=fg_cor,
                                font=("Arial", 9, "bold" if eh_sel else "normal"),
                                relief="flat", anchor="w", justify="left",
                                cursor="arrow" if bloqueado else "hand2",
                                activebackground=bg_btn,
                                state="disabled" if bloqueado else "normal")
                btn.pack(fill="x", padx=4, pady=3)

                if not bloqueado:
                    def _sel_esq(p=pers):
                        sel_esq["pers"] = p
                        _render_grupo_esq()
                        _render_grupo_dir()
                        _render_inv_esq()
                    btn.config(command=_sel_esq)

        combo_g1.bind("<<ComboboxSelected>>", _render_grupo_esq)

        # ═══════════════════════════════════════════════════════════════════════
        # COLUNA 2 — Inventário do personagem selecionado do Grupo 1
        # ═══════════════════════════════════════════════════════════════════════
        lbl_inv1_titulo = tk.Label(frm_inv1, text="— nenhum selecionado —",
                                    bg="#0d1e38", fg="#88aaff",
                                    font=("Arial", 9, "italic"))
        lbl_inv1_titulo.pack(fill="x", padx=6, pady=(6, 2))

        inner_inv1 = _make_scrollable_frame(frm_inv1, bg="#0d1e38")

        def _render_inv_esq():
            for w in inner_inv1.winfo_children(): w.destroy()
            pers = sel_esq["pers"]
            if not pers:
                tk.Label(inner_inv1, text="Selecione um personagem →",
                         bg="#0d1e38", fg=FG_DIM, font=("Arial", 9, "italic")).pack(pady=20)
                lbl_inv1_titulo.config(text="— nenhum selecionado —")
                return
            lbl_inv1_titulo.config(text=f"🎒 {pers.nome}")
            itens = _get_itens_completos(pers)
            if not itens:
                tk.Label(inner_inv1, text="Vazio", bg="#0d1e38", fg=FG_DIM,
                         font=("Arial", 9, "italic")).pack(pady=10)
                return
            for entrada in itens:
                item  = entrada["item"]
                qtd   = entrada["qtd"]
                orig  = entrada["origem"]
                origens = entrada.get("origens", [orig])
                nome  = _nome_item(item, qtd)
                icone = "🛡" if orig.startswith("corpo") else ("⚔" if orig.startswith("slot") else "📦")
                # label de origem legível (ex: "Mão Dir+Mão Esq" ou "peito+costas")
                partes = [o.split(":", 1)[1] for o in origens if ":" in o]
                orig_label = "+".join(partes) if partes else orig
                f = tk.Frame(inner_inv1, bg="#122040", bd=1, relief="solid")
                f.pack(fill="x", padx=4, pady=1)
                info = tk.Frame(f, bg="#122040")
                info.pack(side="left", fill="x", expand=True, padx=6, pady=3)
                tk.Label(info, text=f"{icone} {nome}", bg="#122040", fg=FG,
                         font=("Arial", 9, "bold"), anchor="w").pack(anchor="w")
                if orig_label and orig_label != "inventário":
                    tk.Label(info, text=orig_label, bg="#122040", fg="#6688bb",
                             font=("Arial", 7, "italic"), anchor="w").pack(anchor="w")
                # Seta → mundo
                def _para_mundo(i=item, q=qtd, p=pers, o=orig):
                    if o == "inventário":
                        p.inventario.remover_item(i, q)
                    else:
                        _transferir_para_inventario(i, q, p, o)
                    mundo.adicionar(i, origem=p.nome, local="campo")
                    _render_inv_esq(); _render_mundo()
                tk.Button(f, text="→🌍", command=_para_mundo,
                          bg="#1e4a0a", fg="#aaffaa", font=("Arial", 8),
                          relief="flat", cursor="hand2").pack(side="right", padx=2)

        # ═══════════════════════════════════════════════════════════════════════
        # COLUNA 3 — Inventário do Mundo
        # ═══════════════════════════════════════════════════════════════════════
        tk.Label(frm_mundo, text="Itens no Cenário", bg="#0d1f0a", fg="#88dd88",
                 font=("Arial", 9, "italic")).pack(fill="x", padx=6, pady=(6, 2))

        btn_limpar_mundo = tk.Button(frm_mundo, text="🗑 Limpar tudo",
                                      bg="#2a0a0a", fg="#ff8888",
                                      font=("Arial", 8), relief="flat", cursor="hand2")
        btn_limpar_mundo.pack(fill="x", padx=6, pady=(0, 2))

        inner_mundo = _make_scrollable_frame(frm_mundo, bg="#0d1f0a")

        def _render_mundo():
            for w in inner_mundo.winfo_children(): w.destroy()
            itens_m = mundo.listar()
            if not itens_m:
                tk.Label(inner_mundo, text="Mundo vazio", bg="#0d1f0a", fg=FG_DIM,
                         font=("Arial", 9, "italic")).pack(pady=20)
                return
            for entrada in itens_m:
                item   = entrada["item"]
                origem = entrada.get("origem", "?")
                nome   = getattr(item, "nome", str(item))
                f = tk.Frame(inner_mundo, bg="#152010", bd=1, relief="solid")
                f.pack(fill="x", padx=4, pady=2)
                # nome + origem
                info_f = tk.Frame(f, bg="#152010")
                info_f.pack(fill="x", padx=4, pady=(3, 0))
                tk.Label(info_f, text=f"📦 {nome}", bg="#152010", fg="#ccffcc",
                         font=("Arial", 9, "bold"), anchor="w").pack(side="left")
                tk.Label(info_f, text=f"  (de: {origem})", bg="#152010", fg=FG_DIM,
                         font=("Arial", 8), anchor="w").pack(side="left")
                # botões ← e →
                btn_f = tk.Frame(f, bg="#152010")
                btn_f.pack(fill="x", padx=4, pady=(1, 3))

                def _mundo_para_esq(i=item, e=entrada):
                    pers = sel_esq["pers"]
                    if not pers:
                        return
                    mundo.remover(i)
                    pers.inventario.adicionar_item_objeto(i, 1)
                    _render_mundo(); _render_inv_esq()

                def _mundo_para_dir(i=item, e=entrada):
                    pers = sel_dir["pers"]
                    if not pers:
                        return
                    mundo.remover(i)
                    pers.inventario.adicionar_item_objeto(i, 1)
                    _render_mundo(); _render_inv_dir()

                tk.Button(btn_f, text="←G1", command=_mundo_para_esq,
                          bg="#1a1060", fg="#aaaaff", font=("Arial", 8),
                          relief="flat", cursor="hand2").pack(side="left", padx=2)
                tk.Button(btn_f, text="G2→", command=_mundo_para_dir,
                          bg="#1a1060", fg="#aaaaff", font=("Arial", 8),
                          relief="flat", cursor="hand2").pack(side="left", padx=2)

                def _remover_mundo(i=item):
                    mundo.remover(i)
                    _render_mundo()

                tk.Button(btn_f, text="✕", command=_remover_mundo,
                          bg="#152010", fg="#ff6666", font=("Arial", 8),
                          relief="flat", cursor="hand2").pack(side="right", padx=2)

        def _limpar_mundo():
            mundo.limpar()
            _render_mundo()

        btn_limpar_mundo.config(command=_limpar_mundo)

        # ═══════════════════════════════════════════════════════════════════════
        # COLUNA 4 — Inventário do personagem selecionado do Grupo 2
        # ═══════════════════════════════════════════════════════════════════════
        lbl_inv2_titulo = tk.Label(frm_inv2, text="— nenhum selecionado —",
                                    bg="#0d1e38", fg="#88aaff",
                                    font=("Arial", 9, "italic"))
        lbl_inv2_titulo.pack(fill="x", padx=6, pady=(6, 2))

        inner_inv2 = _make_scrollable_frame(frm_inv2, bg="#0d1e38")

        def _render_inv_dir():
            for w in inner_inv2.winfo_children(): w.destroy()
            pers = sel_dir["pers"]
            if not pers:
                tk.Label(inner_inv2, text="← Selecione um personagem",
                         bg="#0d1e38", fg=FG_DIM, font=("Arial", 9, "italic")).pack(pady=20)
                lbl_inv2_titulo.config(text="— nenhum selecionado —")
                return
            lbl_inv2_titulo.config(text=f"🎒 {pers.nome}")
            itens = _get_itens_completos(pers)
            if not itens:
                tk.Label(inner_inv2, text="Vazio", bg="#0d1e38", fg=FG_DIM,
                         font=("Arial", 9, "italic")).pack(pady=10)
                return
            for entrada in itens:
                item  = entrada["item"]
                qtd   = entrada["qtd"]
                orig  = entrada["origem"]
                origens = entrada.get("origens", [orig])
                nome  = _nome_item(item, qtd)
                icone = "🛡" if orig.startswith("corpo") else ("⚔" if orig.startswith("slot") else "📦")
                partes = [o.split(":", 1)[1] for o in origens if ":" in o]
                orig_label = "+".join(partes) if partes else orig
                f = tk.Frame(inner_inv2, bg="#122040", bd=1, relief="solid")
                f.pack(fill="x", padx=4, pady=1)
                # Seta → mundo
                def _para_mundo_dir(i=item, q=qtd, p=pers, o=orig):
                    if o == "inventário":
                        p.inventario.remover_item(i, q)
                    else:
                        _transferir_para_inventario(i, q, p, o)
                    mundo.adicionar(i, origem=p.nome, local="campo")
                    _render_inv_dir(); _render_mundo()
                tk.Button(f, text="🌍←", command=_para_mundo_dir,
                          bg="#1e4a0a", fg="#aaffaa", font=("Arial", 8),
                          relief="flat", cursor="hand2").pack(side="left", padx=2)
                info = tk.Frame(f, bg="#122040")
                info.pack(side="left", fill="x", expand=True, padx=6, pady=3)
                tk.Label(info, text=f"{icone} {nome}", bg="#122040", fg=FG,
                         font=("Arial", 9, "bold"), anchor="w").pack(anchor="w")
                if orig_label and orig_label != "inventário":
                    tk.Label(info, text=orig_label, bg="#122040", fg="#6688bb",
                             font=("Arial", 7, "italic"), anchor="w").pack(anchor="w")

        # ═══════════════════════════════════════════════════════════════════════
        # COLUNA 5 — Grupo Direito
        # ═══════════════════════════════════════════════════════════════════════
        var_grupo_dir = tk.StringVar(value=nomes_grupos[1] if len(nomes_grupos) > 1 else (nomes_grupos[0] if nomes_grupos else ""))

        top_g2 = tk.Frame(frm_g2, bg="#110830")
        top_g2.pack(fill="x", padx=6, pady=(6, 2))
        tk.Label(top_g2, text="Grupo:", bg="#110830", fg=FG_DIM, font=("Arial", 8)).pack(side="left")
        combo_g2 = ttk.Combobox(top_g2, textvariable=var_grupo_dir, state="readonly",
                                  values=nomes_grupos, width=14)
        combo_g2.pack(side="left", padx=4)

        inner_g2 = _make_scrollable_frame(frm_g2, bg="#110830")

        def _render_grupo_dir(*_):
            for w in inner_g2.winfo_children(): w.destroy()
            chave = chave_por_nome.get(var_grupo_dir.get())
            if not chave: return
            for pers in D.GruposDePersonagens.get(chave, []):
                eh_sel    = sel_dir["pers"] is pers
                bloqueado = sel_esq["pers"] is pers  # já selecionado no lado esquerdo
                if bloqueado:
                    bg_btn = "#2a1a1a"
                elif eh_sel:
                    bg_btn = SEL_BG
                else:
                    bg_btn = "#1a0869"
                border = 2 if eh_sel else 1
                f = tk.Frame(inner_g2, bg=bg_btn, bd=border, relief="solid",
                             highlightbackground="#9966ff" if eh_sel else ("#553333" if bloqueado else "#333366"),
                             highlightthickness=1)
                f.pack(fill="x", padx=4, pady=2)
                pv_txt = f"❤ {pers.VidaAtual}/{pers.VidaMax}"
                indicador = "▶ " if eh_sel else ("🚫 " if bloqueado else "  ")
                fg_cor = "#ffd700" if eh_sel else ("#555566" if bloqueado else FG)
                btn = tk.Button(f, text=f"{indicador}{pers.nome}\n{pv_txt}",
                                bg=bg_btn, fg=fg_cor,
                                font=("Arial", 9, "bold" if eh_sel else "normal"),
                                relief="flat", anchor="w", justify="left",
                                cursor="arrow" if bloqueado else "hand2",
                                activebackground=bg_btn,
                                state="disabled" if bloqueado else "normal")
                btn.pack(fill="x", padx=4, pady=3)

                if not bloqueado:
                    def _sel_dir(p=pers):
                        sel_dir["pers"] = p
                        _render_grupo_dir()
                        _render_grupo_esq()
                        _render_inv_dir()
                    btn.config(command=_sel_dir)

        combo_g2.bind("<<ComboboxSelected>>", _render_grupo_dir)

        # ═══════════════════════════════════════════════════════════════════════
        # RODAPÉ
        # ═══════════════════════════════════════════════════════════════════════
        rodape = tk.Frame(popup, bg="#0a0620")
        rodape.pack(fill="x", padx=8, pady=(0, 8))

        tk.Label(rodape,
                 text="Clique em um personagem para ver seus itens  •  Use os botões para mover itens entre inventários e o mundo",
                 bg="#0a0620", fg=FG_DIM, font=("Arial", 8)).pack(side="left", padx=8)

        tk.Button(rodape, text="Fechar", command=popup.destroy,
                  bg="#3a0a80", fg=FG, font=("Arial", 11), width=10).pack(side="right", padx=8, pady=4)

        # ── renderização inicial ──────────────────────────────────────────────
        _render_grupo_esq()
        _render_grupo_dir()
        _render_mundo()

    def aplicar_ganho_energia(self, personagem, valor_var):
        valor = valor_var.get()
        if isinstance(valor, int) and valor > 0:
            personagem.GanharEnergia(valor)
            self.refresh()
    
    def abrir_popup_acoes(self, personagem):
        popup = tk.Toplevel(self)
        popup.title(f"Ações - {personagem.nome}")
        popup.configure(bg="#1a0869")
        popup.geometry("350x500")  # Aumentado a altura
        popup.resizable(False, False)
        
        tk.Label(popup, text=f"Ações disponíveis para {personagem.nome}", 
                bg="#1a0869", fg="white", font=("Arial", 14, "bold")).pack(pady=15)
        
        # Frame para os botões de ação
        botoes_frame = tk.Frame(popup, bg="#1a0869")
        botoes_frame.pack(pady=20)
        
        # Função para abrir menu de tipos de ataque
        def abrir_menu_ataque():
            popup.destroy()
            self.abrir_popup_tipos_ataque(personagem)
        
        # Função para abrir popup de pilhagem com personagem pré-selecionado
        def pilhar():
            popup.destroy()
            self.abrir_popup_loot_com_origem(personagem)
        
        # Função para trocar arma
        def trocar_arma():
            popup.destroy()
            self.abrir_popup_trocar_arma(personagem)
        
        # Função para recarregar arma
        def recarregar_arma():
            popup.destroy()
            self.abrir_popup_recarregar_arma(personagem)
        
        # Função para descarregar arma
        def descarregar_arma():
            popup.destroy()
            self.abrir_popup_descarregar_arma(personagem)
        
        # Botões de ação
        tk.Button(botoes_frame, text="Atacar", command=abrir_menu_ataque, 
                bg="#8B0000", fg="white", font=("Arial", 12), width=15, height=2).pack(pady=5)
        
        tk.Button(botoes_frame, text="Pilhar", command=pilhar,
                bg="#4B0082", fg="white", font=("Arial", 12), width=15, height=2).pack(pady=5)
        
        tk.Button(botoes_frame, text="Recarregar", command=recarregar_arma,
                bg="#006400", fg="white", font=("Arial", 12), width=15, height=2).pack(pady=5)
        
        tk.Button(botoes_frame, text="Descarregar", command=descarregar_arma,
                bg="#FF8C00", fg="white", font=("Arial", 12), width=15, height=2).pack(pady=5)
        
        tk.Button(botoes_frame, text="Trocar Arma", command=trocar_arma,
                bg="#2F4F4F", fg="white", font=("Arial", 12), width=15, height=2).pack(pady=5)
        
        # Botão de fechar
        tk.Button(popup, text="Fechar", command=popup.destroy, 
                bg="#3a0a80", fg="white", font=("Arial", 12), width=15).pack(pady=20)

    def _abrir_popup_loot_combate(self):
        char = self.personagem_no_card
        if not char:
            self.adicionar_log("Selecione um personagem no card primeiro.", "gray")
            return
        abrir_popup_loot(self, char, D, on_finish=self.refresh)

    def abrir_popup_tipos_ataque(self, atacante):
        """Detecta armas equipadas e decide o fluxo: simples ou dual wield."""
        armas = []
        itens_vistos = set()
        for slot_key in ("mao_direita", "mao_esquerda"):
            slot = atacante.slots.get(slot_key)
            if slot and slot.item and id(slot.item) not in itens_vistos:
                armas.append((slot_key, slot.item))
                itens_vistos.add(id(slot.item))

        # Sem armas: só melee desarmado (não implementado) ou cancela
        if not armas:
            self.abrir_popup_ataque_melee(atacante); return

        # Uma arma: abre o popup certo direto
        if len(armas) == 1:
            _, item = armas[0]
            if isinstance(item, CB.Ranged):
                self.abrir_popup_ataque_ranged(atacante)
            else:
                self.abrir_popup_ataque_melee(atacante)
            return

        # Duas armas: pergunta se é dual wield ou usa só uma
        popup = tk.Toplevel(self)
        popup.title("Tipo de Ataque")
        popup.configure(bg="#1a1a2e")
        popup.geometry("380x280")
        popup.resizable(False, False)

        tk.Label(popup, text=f"Armas de {atacante.nome}", bg="#1a1a2e",
                 fg="white", font=("Arial", 13, "bold")).pack(pady=12)

        for slot_key, item in armas:
            tipo_txt = "Ranged" if isinstance(item, CB.Ranged) else "Melee"
            slot_txt = "Mão Dir" if slot_key == "mao_direita" else "Mão Esq"
            tk.Label(popup, text=f"{slot_txt}: {item.nome} ({tipo_txt})",
                     bg="#1a1a2e", fg="#aaaaff", font=("Arial", 10)).pack()

        tk.Frame(popup, bg="#333", height=1).pack(fill="x", padx=20, pady=8)

        def _dual():
            popup.destroy()
            self._iniciar_dual_wield(atacante, armas)

        def _escolher():
            popup.destroy()
            self._escolher_arma_unica(atacante, armas)

        tk.Button(popup, text="⚔⚔ Dual Wield (as duas)", command=_dual,
                  bg="#7b2cbf", fg="white", font=("Arial", 11), width=24).pack(pady=4)
        tk.Button(popup, text="⚔ Usar só uma arma", command=_escolher,
                  bg="#1a0869", fg="white", font=("Arial", 11), width=24).pack(pady=4)
        tk.Button(popup, text="Cancelar", command=popup.destroy,
                  bg="#8B0000", fg="white", font=("Arial", 10), width=24).pack(pady=4)

    def _escolher_arma_unica(self, atacante, armas):
        """Popup para escolher qual das duas armas usar."""
        popup = tk.Toplevel(self)
        popup.title("Escolher Arma")
        popup.configure(bg="#1a1a2e")
        popup.geometry("340x200")
        popup.resizable(False, False)

        tk.Label(popup, text="Qual arma usar?", bg="#1a1a2e",
                 fg="white", font=("Arial", 12, "bold")).pack(pady=14)

        for slot_key, item in armas:
            slot_txt = "Mão Dir" if slot_key == "mao_direita" else "Mão Esq"
            tipo_txt = "Ranged" if isinstance(item, CB.Ranged) else "Melee"
            def _usar(i=item):
                popup.destroy()
                if isinstance(i, CB.Ranged):
                    self.abrir_popup_ataque_ranged(atacante)
                else:
                    self.abrir_popup_ataque_melee(atacante)
            tk.Button(popup, text=f"{slot_txt}: {item.nome} ({tipo_txt})",
                      command=_usar, bg="#1a0869", fg="white",
                      font=("Arial", 11), width=28).pack(pady=5)

        tk.Button(popup, text="Cancelar", command=popup.destroy,
                  bg="#8B0000", fg="white", font=("Arial", 10)).pack(pady=6)

    def _iniciar_dual_wield(self, atacante, armas):
        """
        Abre os popups de ataque em sequência para cada arma.
        Armazena os resultados e ao fim do segundo exibe o log combinado.
        """
        self._dw_resultados = []
        self._dw_armas = armas
        self._dw_atacante = atacante
        self._dw_index = 0
        self._dw_abrir_proximo()

    def _dw_abrir_proximo(self):
        """Abre o popup da próxima arma do dual wield."""
        if self._dw_index >= len(self._dw_armas):
            self._dw_finalizar(); return

        slot_key, item = self._dw_armas[self._dw_index]
        slot_txt = "Mão Dir" if slot_key == "mao_direita" else "Mão Esq"

        if isinstance(item, CB.Ranged):
            self.abrir_popup_ataque_ranged(
                self._dw_atacante,
                titulo_extra=f"[Dual Wield — {slot_txt}]",
                callback_resultado=self._dw_receber_resultado)
        else:
            self.abrir_popup_ataque_melee(
                self._dw_atacante,
                titulo_extra=f"[Dual Wield — {slot_txt}]",
                arma_pre=item,
                callback_resultado=self._dw_receber_resultado)

    def _dw_receber_resultado(self, res: dict):
        """Callback chamado pelo popup ao confirmar. Avança para o próximo."""
        self._dw_resultados.append(res)
        self._dw_index += 1
        self._dw_abrir_proximo()

    def _dw_finalizar(self):
        """Exibe log combinado dos dois ataques no log de combate."""
        atacante = self._dw_atacante
        linhas = []
        dano_total = 0
        for i, res in enumerate(self._dw_resultados):
            slot_txt = "Mão Dir" if i == 0 else "Mão Esq"
            if "por_disparo" in res:          # ranged
                acertos = sum(1 for t in res["por_disparo"] if t["acertou"])
                dano = sum(t["dano_final"] for t in res["por_disparo"] if t["acertou"])
                linhas += [f"[{slot_txt}] {l}" for l in res["log"]]
            else:                             # melee
                acertos = 1 if res["acertou"] else 0
                dano = res["dano_final"] if res["acertou"] else 0
                linhas += [f"[{slot_txt}] {l}" for l in res["log"]]
            dano_total += dano

        titulo = f"⚔⚔ Dual Wield: {atacante.nome}"
        detalhes = {"Dano Total": str(dano_total), "Por arma": linhas}
        cor = "lightgreen" if any(
            (r.get("acertou") or r.get("acertou_algum")) for r in self._dw_resultados
        ) else "orange"
        self.adicionar_log(titulo, cor, detalhes=detalhes)
        self.refresh()

    def _equipar_item_combate(self, char, item):
        try:
            if char._eh_protecao(item):
                regiao = item.regiao_indicada.lower() if item.regiao_indicada else None
                if regiao and regiao in char.regioes_corpo:
                    char._equipar_protecao_obj_em_regiao(item, regiao)
            else:
                char.equipar_item(item)
        except Exception as e:
            print("Erro ao equipar item (combate):", e)

    def _abrir_popup_slot_combate(self, char, item_obj, on_finish):
        """Reusa a lógica de escolha de slot adaptada para o contexto de combate."""
        try:
            popup = tk.Toplevel(self)
            popup.title(f"Slot — {getattr(item_obj,'nome','Item')}")
            popup.configure(bg="#1a0869")
            popup.geometry("380x320")

            tk.Label(popup, text=getattr(item_obj, 'nome', 'Item'),
                     font=("Arial", 12, "bold"), bg="#1a0869", fg="white").pack(pady=10)

            def _equipar_e_fechar(fn):
                fn(); popup.destroy(); on_finish()

            if char._eh_protecao(item_obj):
                for r in char.obter_regioes_compativeis(item_obj):
                    tk.Button(popup, text=r.capitalize(),
                              command=lambda reg=r: _equipar_e_fechar(
                                  lambda: char._equipar_protecao_obj_em_regiao(item_obj, reg)),
                              bg="#2a0d89", fg="white", font=("Arial", 10)).pack(fill="x", padx=20, pady=4)

            elif char._eh_arma_melee(item_obj) or char._eh_arma_ranged(item_obj):
                for chave, slot in [(k, s) for k, s in char.slots.items() if s.tipo == "mao"]:
                    tk.Button(popup, text=f"Equipar em {slot.nome}",
                              command=lambda k=chave: _equipar_e_fechar(
                                  lambda: char._equipar_arma(item_obj, nome_slot=k, forcar=True)),
                              bg="#2a0d89", fg="white", font=("Arial", 10)).pack(fill="x", padx=20, pady=4)

            elif isinstance(item_obj, CB.Equipamento):
                tk.Button(popup, text="Equipar",
                          command=lambda: _equipar_e_fechar(
                              lambda: char.equipar_equipamento_slot(item_obj)),
                          bg="#2a0d89", fg="white", font=("Arial", 10)).pack(fill="x", padx=20, pady=10)
            else:
                tk.Label(popup, text="Sem slot disponível.", bg="#1a0869", fg="white").pack(pady=20)

            tk.Button(popup, text="Cancelar", command=popup.destroy,
                      bg="#8B0000", fg="white", font=("Arial", 10)).pack(pady=8)
        except Exception as e:
            print("Erro popup slot combate:", e)
     
    # Armas #
    def abrir_popup_trocar_arma(self, personagem):
        """Abre popup para trocar armas entre equipadas e inventário"""
        popup = tk.Toplevel(self)
        popup.title(f"Trocar Arma - {personagem.nome}")
        popup.configure(bg="#1a0869")
        popup.geometry("600x400")
        popup.resizable(False, False)
        
        # Frame principal dividido em duas colunas
        main_frame = tk.Frame(popup, bg="#1a0869")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Coluna esquerda - Armas Equipadas
        equipadas_frame = tk.LabelFrame(main_frame, text="Armas Equipadas", 
                                    bg="#1a0869", fg="white", font=("Arial", 12, "bold"))
        equipadas_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        # Coluna direita - Armas no Inventário
        inventario_frame = tk.LabelFrame(main_frame, text="Armas no Inventário", 
                                        bg="#1a0869", fg="white", font=("Arial", 12, "bold"))
        inventario_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        def atualizar_listas():
            # Limpar frames
            for widget in equipadas_frame.winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.destroy()
            for widget in inventario_frame.winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.destroy()
            
            # Armas equipadas - usar listar_itens() do equipados
            try:
                itens_equipados = personagem.equipados.listar_itens()
                armas_equipadas = [item for item in itens_equipados 
                                if isinstance(item["objeto"], (CB.Ranged, CB.Melee))]
                
                for item in armas_equipadas:
                    arma = item["objeto"]
                    item_frame = tk.Frame(equipadas_frame, bg="#220866", bd=1, relief="solid")
                    item_frame.pack(fill="x", padx=5, pady=2)
                    
                    tk.Label(item_frame, text=arma.nome, bg="#220866", fg="white", 
                            font=("Arial", 10)).pack(side="left", padx=5)
                    
                    tk.Button(item_frame, text="→", command=lambda a=arma: mover_para_inventario(a),
                            bg="#8B0000", fg="white", width=3).pack(side="right", padx=2)
            except Exception as e:
                print(f"Erro ao listar armas equipadas: {e}")
            
            # Armas no inventário
            try:
                itens_inventario = personagem.inventario.listar_itens()
                armas_inventario = [item for item in itens_inventario 
                                if isinstance(item["objeto"], (CB.Ranged, CB.Melee))]
                
                for item in armas_inventario:
                    arma = item["objeto"]
                    quantidade = item["quantidade"]
                    
                    item_frame = tk.Frame(inventario_frame, bg="#220866", bd=1, relief="solid")
                    item_frame.pack(fill="x", padx=5, pady=2)
                    
                    texto = f"{arma.nome} ({quantidade}x)" if quantidade > 1 else arma.nome
                    tk.Label(item_frame, text=texto, bg="#220866", fg="white", 
                            font=("Arial", 10)).pack(side="left", padx=5)
                    
                    tk.Button(item_frame, text="←", command=lambda a=arma: mover_para_equipados(a),
                            bg="#006400", fg="white", width=3).pack(side="right", padx=2)
            except Exception as e:
                print(f"Erro ao listar armas do inventário: {e}")
        
        def mover_para_inventario(arma):
            try:
                sucesso = personagem.desequipar_item(arma)
                if sucesso:
                    atualizar_listas()
                else:
                    print("Não foi possível desequipar a arma.")
            except Exception as e:
                print(f"Erro ao desequipar arma: {e}")
        
        def mover_para_equipados(arma):
            try:
                sucesso = personagem.equipar_item(arma)
                if sucesso:
                    atualizar_listas()
                else:
                    print("Não foi possível equipar a arma.")
            except Exception as e:
                print(f"Erro ao equipar arma: {e}")
        
        # Inicializar listas
        atualizar_listas()
        
        # Botão fechar
        tk.Button(popup, text="Fechar", command=popup.destroy, 
                bg="#3a0a80", fg="white", font=("Arial", 12)).pack(pady=10)

    def abrir_popup_recarregar_arma(self, personagem):
        """Abre popup para recarregar armas Ranged"""
        # Verificar se há armas Ranged equipadas
        try:
            itens_equipados = personagem.equipados.listar_itens()
            armas_ranged = [item["objeto"] for item in itens_equipados 
                        if isinstance(item["objeto"], CB.Ranged)]
        except Exception as e:
            print(f"Erro ao listar armas equipadas: {e}")
            armas_ranged = []
        
        if not armas_ranged:
            # Abrir popup de trocar arma se não houver armas ranged equipadas
            self.abrir_popup_trocar_arma(personagem)
            return
        
        popup = tk.Toplevel(self)
        popup.title(f"Recarregar Arma - {personagem.nome}")
        popup.configure(bg="#1a0869")
        popup.geometry("400x300")
        popup.resizable(False, False)
        
        tk.Label(popup, text="Escolha a arma para recarregar:", bg="#1a0869", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        
        def escolher_arma(arma_selecionada):
            popup.destroy()
            self.abrir_popup_escolher_municao(personagem, arma_selecionada)
        
        # Mostrar armas disponíveis
        for arma in armas_ranged:
            info_texto = f"{arma.nome} - {arma.munições}/{arma.capacidade}"
            tk.Button(popup, text=info_texto, command=lambda a=arma: escolher_arma(a), bg="#006400", fg="white", font=("Arial", 11), width=30, height=2).pack(pady=5)
        
        tk.Button(popup, text="Cancelar", command=popup.destroy, 
                bg="#8B0000", fg="white", font=("Arial", 11)).pack(pady=10)

    def abrir_popup_escolher_municao(self, personagem, arma):
        """Popup para escolher munição e quantidade para recarregar"""
        popup = tk.Toplevel(self)
        popup.title("Escolher Munição")
        popup.configure(bg="#1a0869")
        popup.geometry("400x300")
        popup.resizable(False, False)
        
        tk.Label(popup, text=f"Recarregando: {arma.nome}", bg="#1a0869", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(popup, text=f"Munições atuais: {arma.munições}/{arma.capacidade}", bg="#1a0869", fg="white", font=("Arial", 10)).pack(pady=5)
        
        # Buscar munições compatíveis
        itens_inventario = personagem.inventario.listar_itens()
        municoes_compativeis = [item for item in itens_inventario if isinstance(item["objeto"], CB.Municao) and item["objeto"].calibre == arma.calibre]
        
        if not municoes_compativeis:
            tk.Label(popup, text="Sem munições compatíveis!", bg="#1a0869", fg="red", font=("Arial", 12)).pack(pady=20)
            tk.Button(popup, text="Fechar", command=popup.destroy).pack()
            return
        
        tk.Label(popup, text="Escolha a munição:", bg="#1a0869", fg="white", font=("Arial", 10)).pack()
        
        # Dropdown de munições
        nomes_municoes = [f"{item['objeto'].nome} (x{item['quantidade']})" for item in municoes_compativeis]
        municao_var = tk.StringVar(value=nomes_municoes[0])
        dropdown = tk.OptionMenu(popup, municao_var, *nomes_municoes)
        dropdown.pack(pady=5)
        
        # Quantidade
        tk.Label(popup, text="Quantidade:", bg="#1a0869", fg="white", font=("Arial", 10)).pack()
        quantidade_var = tk.IntVar(value=1)
        spinbox = tk.Spinbox(popup, from_=1, to=100, textvariable=quantidade_var, width=5)
        spinbox.pack()
        
        def recarregar_quantidade():
            try:
                index = nomes_municoes.index(municao_var.get())
                item_escolhido = municoes_compativeis[index]
                municao_obj = item_escolhido["objeto"]
                quantidade = quantidade_var.get()
                
                carregado = arma.carregar_municao(municao_obj, quantidade)
                if carregado > 0:
                    self._remover_item_do_inventario(personagem, municao_obj, carregado)
                    self.refresh()
                    popup.destroy()
                else:
                    tk.Label(popup, text="Erro ao carregar!", fg="red").pack()
            except Exception as e:
                print(f"Erro: {e}")
        
        def recarregar_tudo():
            try:
                index = nomes_municoes.index(municao_var.get())
                item_escolhido = municoes_compativeis[index]
                municao_obj = item_escolhido["objeto"]
                
                espaco_restante = arma.capacidade - arma.munições
                quantidade_disponivel = item_escolhido["quantidade"]
                quantidade_a_carregar = min(espaco_restante, quantidade_disponivel)
                
                if quantidade_a_carregar > 0:
                    carregado = arma.carregar_municao(municao_obj, quantidade_a_carregar)
                    if carregado > 0:
                        self._remover_item_do_inventario(personagem, municao_obj, carregado)
                        self.refresh()
                        popup.destroy()
            except Exception as e:
                print(f"Erro: {e}")
        
        # Botões
        botoes_frame = tk.Frame(popup, bg="#1a0869")
        botoes_frame.pack(pady=20)
        
        tk.Button(botoes_frame, text="Carregar Qtd", command=recarregar_quantidade, bg="#006400", fg="white").pack(side="left", padx=10)
        tk.Button(botoes_frame, text="Carregar Tudo", command=recarregar_tudo, bg="#004080", fg="white").pack(side="left", padx=10)
        tk.Button(botoes_frame, text="Cancelar", command=popup.destroy, bg="#8B0000", fg="white").pack(side="left", padx=10)

    def abrir_popup_descarregar_arma(self, personagem):
        """Abre popup para descarregar armas Ranged"""
        # Verificar se há armas Ranged equipadas com munição
        try:
            itens_equipados = personagem.equipados.listar_itens()
            armas_ranged = [item["objeto"] for item in itens_equipados 
                        if isinstance(item["objeto"], CB.Ranged) and item["objeto"].munições > 0]
        except Exception as e:
            print(f"Erro ao listar armas equipadas: {e}")
            armas_ranged = []
        
        if not armas_ranged:
            # Verificar se há armas ranged equipadas mas vazias
            try:
                armas_vazias = [item["objeto"] for item in itens_equipados if isinstance(item["objeto"], CB.Ranged)]
            except:
                armas_vazias = []
                
            if not armas_vazias:
                self.abrir_popup_trocar_arma(personagem)
                return
            else:
                popup = tk.Toplevel(self)
                popup.title("Aviso")
                popup.configure(bg="#1a0869")
                popup.geometry("300x150")
                tk.Label(popup, text="Nenhuma arma com munição encontrada!", bg="#1a0869", fg="red", font=("Arial", 12)).pack(pady=50)
                tk.Button(popup, text="OK", command=popup.destroy).pack()
                return
        
        popup = tk.Toplevel(self)
        popup.title(f"Descarregar Arma - {personagem.nome}")
        popup.configure(bg="#1a0869")
        popup.geometry("400x300")
        popup.resizable(False, False)
        
        tk.Label(popup, text="Escolha a arma para descarregar:", bg="#1a0869", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        
        def escolher_arma(arma_selecionada):
            popup.destroy()
            self.abrir_popup_descarregar_quantidade(personagem, arma_selecionada)
        
        # Mostrar armas disponíveis
        for arma in armas_ranged:
            info_texto = f"{arma.nome} - {arma.munições} munições"
            tk.Button(popup, text=info_texto, command=lambda a=arma: escolher_arma(a), bg="#FF8C00", fg="white", font=("Arial", 11), width=30, height=2).pack(pady=5)
        
        tk.Button(popup, text="Cancelar", command=popup.destroy, bg="#8B0000", fg="white", font=("Arial", 11)).pack(pady=10)

    def abrir_popup_descarregar_quantidade(self, personagem, arma):
        """Popup para escolher quantidade a descarregar"""
        popup = tk.Toplevel(self)
        popup.title("Descarregar Munição")
        popup.configure(bg="#1a0869")
        popup.geometry("350x250")
        popup.resizable(False, False)
        
        tk.Label(popup, text=f"Descarregando: {arma.nome}", bg="#1a0869", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(popup, text=f"Munições na arma: {arma.munições}", bg="#1a0869", fg="white", font=("Arial", 10)).pack(pady=5)
        
        tk.Label(popup, text="Quantidade a descarregar:", bg="#1a0869", fg="white", font=("Arial", 10)).pack(pady=10)
        
        quantidade_var = tk.IntVar(value=1)
        spinbox = tk.Spinbox(popup, from_=1, to=arma.munições, textvariable=quantidade_var, width=5)
        spinbox.pack()
        
        def descarregar_quantidade():
            try:
                quantidade = quantidade_var.get()
                municoes = arma.descarregar_municao(quantidade=quantidade)
                if municoes:
                    for municao in municoes:
                        personagem.inventario.adicionar_item_objeto(municao)
                    self.refresh()
                    popup.destroy()
            except Exception as e:
                print(f"Erro: {e}")
        
        def descarregar_tudo():
            try:
                municoes = arma.descarregar_municao(quantidade=arma.munições)
                if municoes:
                    for municao in municoes:
                        personagem.inventario.adicionar_item_objeto(municao)
                    self.refresh()
                    popup.destroy()
            except Exception as e:
                print(f"Erro: {e}")
        
        # Botões
        botoes_frame = tk.Frame(popup, bg="#1a0869")
        botoes_frame.pack(pady=30)
        
        tk.Button(botoes_frame, text="Descarregar Qtd", command=descarregar_quantidade, bg="#FF8C00", fg="white").pack(side="left", padx=10)
        tk.Button(botoes_frame, text="Descarregar Tudo", command=descarregar_tudo, bg="#8B0000", fg="white").pack(side="left", padx=10)
        tk.Button(botoes_frame, text="Cancelar", command=popup.destroy, bg="#006400", fg="white").pack(side="left", padx=10)
    
    def _remover_item_do_inventario(self, personagem, item, quantidade=1):
        try:
            personagem.inventario.remover_item(item, quantidade)
            return True
        except Exception as e:
            print(f"Erro ao remover item do inventário: {e}")
            return False
    
    def texto_armas_maos(self, char):
        maos = [s for s in char.slots.values() if s.tipo == "mao" and s.item]
        if not maos: return "Nenhuma arma equipada"
        linhas = []
        for s in maos:
            i = s.item
            linhas.append(f"{s.nome}: {i.nome}\nDano: {getattr(i,'dano','—')} | Tipo: {getattr(i,'tipo','—')}")
        return "\n\n".join(linhas)
    # Armas #

    # Consumiveis #
    @staticmethod
    def _consumivel_eh_area(item_obj):
        """
        Detecta se um Consumivel tem efeito de área.
        Suporta formato antigo (item_obj.raio) e novo (efeitos[*].tipo == 'dano_area').
        """
        if getattr(item_obj, "raio", None):
            return True
        uso = str(getattr(item_obj, "uso", "")).lower()
        if any(k in uso for k in ("arremess", "detonac", "detonaç", "area", "área")):
            return True
        for ef in getattr(item_obj, "efeitos", []):
            if isinstance(ef, dict) and ef.get("tipo") == "dano_area":
                return True
        return False

    @staticmethod
    def _dados_area_consumivel(item_obj):
        """
        Retorna (raio, raio_letal, falloff, perfuracao) independente do formato.
        Prioriza novo formato (primeiro efeito dano_area); cai para atributos diretos.
        Retorna (0, 0, 'linear', 0) se não encontrar nada.
        """
        for ef in getattr(item_obj, "efeitos", []):
            if isinstance(ef, dict) and ef.get("tipo") == "dano_area":
                raio    = ef.get("raio", 0)
                letal   = ef.get("raio_letal") or round(raio * 0.3, 1)
                falloff = ef.get("falloff", "linear")
                perf    = ef.get("perfuracao", 0)
                return raio, letal, falloff, perf

        # formato antigo
        raio = getattr(item_obj, "raio", 0) or 0
        letal = getattr(item_obj, "raio_letal", None) or round(raio * 0.3, 1)
        falloff = getattr(item_obj, "falloff", "linear") or "linear"
        perf = getattr(item_obj, "perfuracao", 0) or 0
        return raio, letal, falloff, perf
    
    def _usar_consumivel_simples(self, item, personagem):
        CB.usar_consumivel(item, personagem, alvo=personagem, aplicar=True)
        efeitos_bb = [
            ef for ef in getattr(item, "efeitos", [])
            if isinstance(ef, dict) and ef.get("tipo") in ("buff", "debuff")
        ]
        if efeitos_bb:
            aplicar_efeitos_item(efeitos_bb, personagem)
        self.refresh()

    def _usar_consumivel_area(self, item, personagem):
        """Abre o popup de consumível em área (inputs manuais + integração com mapa)."""
        self.abrir_popup_consumivel_area(item, personagem)

    def _abrir_menu_consumiveis(self, personagem):
        itens = personagem.inventario.listar_itens()
        consumiveis = [i for i in itens if isinstance(i["objeto"], CB.Consumivel)]

        menu = tk.Menu(self, tearoff=0)

        for entrada in consumiveis:
            item = entrada["objeto"]

            if self._consumivel_eh_area(item):
                menu.add_command(
                    label=f"💥 {item.nome}",
                    command=lambda i=item, p=personagem:
                        self.mapa_instancia.abrir_popup_usar_consumivel_area(i, p)
                )
            else:
                def _usar(i=item, p=personagem):
                    CB.usar_consumivel(i, p, alvo=p, aplicar=True)
                    efeitos_bb = [
                        ef for ef in getattr(i, "efeitos", [])
                        if isinstance(ef, dict) and ef.get("tipo") in ("buff", "debuff")
                    ]
                    if efeitos_bb:
                        aplicar_efeitos_item(efeitos_bb, p)

                menu.add_command(label=f"🧪 {item.nome}", command=_usar)

        menu.tk_popup(self.winfo_pointerx(), self.winfo_pointery())
    # Consumiveis #

    # ataques #
    def abrir_popup_consumivel_area(self, item_consumivel, personagem_usuario):
        """
        Popup de usar consumível em área.
        Suporta formato antigo (raio/falloff como atributos) e
        novo formato (efeitos[*].tipo == 'dano_area').
        """
        popup = tk.Toplevel(self)
        popup.title(f"Usar em Área — {item_consumivel.nome}")
        popup.configure(bg="#130f26")
        popup.geometry("860x720")
        popup.resizable(True, True)

        BG     = "#1a0869"
        BG2    = "#220866"
        BGDARK = "#130f26"
        FG     = "white"
        FG_DIM = "#aaaaaa"
        ENT    = "#0d0730"

        # ── Dados de área (independente do formato) ────────────────────────────
        raio, raio_letal, falloff, perfuracao = self._dados_area_consumivel(item_consumivel)

        # Efeitos de área para exibição (pode haver múltiplos no novo formato)
        efeitos_area = [
            ef for ef in getattr(item_consumivel, "efeitos", [])
            if isinstance(ef, dict) and ef.get("tipo") == "dano_area"
        ]

        # Buffs/debuffs que serão aplicados junto
        efeitos_buff = [
            ef for ef in getattr(item_consumivel, "efeitos", [])
            if isinstance(ef, dict) and ef.get("tipo") in ("buff", "debuff")
        ]

        # ── estado interno ─────────────────────────────────────────────────────
        alvos_data: list[dict] = []

        # ── HEADER ────────────────────────────────────────────────────────────
        header = tk.Frame(popup, bg="#0a0433", height=56)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(
            header, text=f"💥 {item_consumivel.nome}",
            font=("Arial", 15, "bold"), bg="#0a0433", fg="#b79cff"
        ).pack(side="left", padx=14, pady=10)

        if efeitos_area:
            if len(efeitos_area) == 1:
                ef0 = efeitos_area[0]
                info_txt = (
                    f"Raio: {ef0.get('raio', raio)}m  |  "
                    f"Raio letal: {ef0.get('raio_letal') or round(ef0.get('raio', raio) * 0.3, 1)}m  |  "
                    f"Falloff: {ef0.get('falloff', falloff)}  |  "
                    f"Perf.: {ef0.get('perfuracao', perfuracao)}"
                )
            else:
                partes = [
                    f"Ef{i+1}: {e.get('subtipo','?')} {e.get('valor',0)} "
                    f"r{e.get('raio', raio)}m"
                    for i, e in enumerate(efeitos_area)
                ]
                info_txt = "  |  ".join(partes)
        else:
            # formato antigo
            info_txt = (
                f"Raio: {raio}m  |  Raio letal: {raio_letal}m  |  "
                f"Falloff: {falloff}  |  Perf.: {perfuracao}"
            )

        tk.Label(
            header, text=info_txt,
            bg="#0a0433", fg=FG_DIM, font=("Arial", 9)
        ).pack(side="left", padx=14)

        # Linha de buffs/debuffs adicionais (novo formato)
        if efeitos_buff:
            nomes_bb = ", ".join(
                f"{ef.get('nome','?')} ({ef.get('chance',100)}% / {ef.get('duracao',1)}t)"
                for ef in efeitos_buff
            )
            tk.Label(
                popup, text=f"Efeitos adicionais: {nomes_bb}",
                bg="#130f26", fg="#a0d4a0",
                font=("Arial", 8, "italic"), wraplength=830
            ).pack(fill="x", padx=14, pady=(0, 2))

        # ── PAINEL UNIVERSAL ──────────────────────────────────────────────────
        univ_frame = tk.LabelFrame(
            popup, text="Modificadores Universais",
            bg=BG, fg="yellow", font=("Arial", 10, "bold")
        )
        univ_frame.pack(fill="x", padx=12, pady=(8, 4))

        univ_inner = tk.Frame(univ_frame, bg=BG)
        univ_inner.pack(fill="x", padx=8, pady=6)

        def _lbl_entry(parent, label, var, width=7):
            tk.Label(parent, text=label, bg=BG, fg=FG,
                     font=("Arial", 9)).pack(side="left", padx=(8, 2))
            tk.Entry(parent, textvariable=var, width=width,
                     bg=ENT, fg=FG, font=("Arial", 9),
                     justify="center", insertbackground=FG).pack(side="left", padx=(0, 6))

        var_ubuff   = tk.IntVar(value=0)
        var_udebuff = tk.IntVar(value=0)
        _lbl_entry(univ_inner, "Buff dano (todos):",   var_ubuff)
        _lbl_entry(univ_inner, "Debuff dano (todos):", var_udebuff)
        tk.Label(
            univ_inner, text="(somado ao individual de cada alvo)",
            bg=BG, fg=FG_DIM, font=("Arial", 8, "italic")
        ).pack(side="left", padx=6)

        # ── ADICIONAR ALVO ────────────────────────────────────────────────────
        add_frame = tk.LabelFrame(
            popup, text="Adicionar Alvo",
            bg=BG, fg="lightblue", font=("Arial", 10, "bold")
        )
        add_frame.pack(fill="x", padx=12, pady=4)

        add_inner = tk.Frame(add_frame, bg=BG)
        add_inner.pack(fill="x", padx=8, pady=6)

        todos_combate = []
        for chave in ("_lista_superior", "_lista_inferior"):
            todos_combate += D.GruposDePersonagens.get(chave, [])
        todos_combate = list({id(p): p for p in todos_combate}.values())

        var_alvo_sel = tk.StringVar(value=todos_combate[0].nome if todos_combate else "")
        var_dist_add = tk.DoubleVar(value=1.0)
        var_cob_add  = tk.StringVar(value="Nenhuma")
        var_mat_add  = tk.StringVar(value="Nenhum")

        tk.Label(add_inner, text="Personagem:", bg=BG, fg=FG,
                 font=("Arial", 9)).pack(side="left", padx=(0, 2))
        ttk.Combobox(
            add_inner, textvariable=var_alvo_sel, state="readonly",
            values=[p.nome for p in todos_combate], width=18
        ).pack(side="left", padx=(0, 10))

        _lbl_entry(add_inner, "Dist (m):", var_dist_add, width=6)

        tk.Label(add_inner, text="Cobertura:", bg=BG, fg=FG,
                 font=("Arial", 9)).pack(side="left", padx=(8, 2))
        ttk.Combobox(
            add_inner, textvariable=var_cob_add, state="readonly",
            values=["Nenhuma", "Parcial", "Alta", "Total"], width=10
        ).pack(side="left", padx=(0, 10))

        tk.Label(add_inner, text="Material:", bg=BG, fg=FG,
                 font=("Arial", 9)).pack(side="left", padx=(0, 2))
        ttk.Combobox(
            add_inner, textvariable=var_mat_add, state="readonly",
            values=["Nenhum", "Gesso", "Madeira", "Veiculo", "Concreto", "Aço"], width=10
        ).pack(side="left", padx=(0, 10))

        def _adicionar_alvo_manual():
            pers = next((p for p in todos_combate if p.nome == var_alvo_sel.get()), None)
            if not pers:
                return
            if any(d["pers"] is pers for d in alvos_data):
                return

            # preencher cobertura e material do mapa se disponíveis
            cob_auto = getattr(pers, "cobertura_mapa", None)
            cob = cob_auto if cob_auto in ("Nenhuma", "Parcial", "Alta", "Total") \
                else var_cob_add.get()

            mat_auto = getattr(pers, "material_mapa", None)
            mat = mat_auto if mat_auto in ("Nenhum", "Gesso", "Madeira", "Veiculo", "Concreto", "Aço") \
                else var_mat_add.get()

            _append_alvo(pers, var_dist_add.get(), cob, mat)

        tk.Button(
            add_inner, text="+ Adicionar", command=_adicionar_alvo_manual,
            bg="#1a5c1a", fg=FG, font=("Arial", 9, "bold"),
            relief="flat", cursor="hand2"
        ).pack(side="left", padx=6)

        lbl_mapa_status = tk.Label(add_inner, text="", bg=BG, fg="#90caf9",
                                   font=("Arial", 8, "italic"))
        lbl_mapa_status.pack(side="right", padx=6)

        def _abrir_mapa_epicentro():
            estado = getattr(self, "_estado_mapa", {})
            if not estado.get("tokens_dados"):
                tk.messagebox.showwarning(
                    "Mapa vazio",
                    "Abra o mapa de combate, posicione os personagens e volte.",
                    parent=popup)
                return
            _popup_selecionar_epicentro(popup, estado, item_consumivel, raio_letal,
                                        _callback_epicentro)

        def _callback_epicentro(epicentro_wx, epicentro_wy, alvos_detectados):
            alvos_data.clear()
            _rebuild_lista_alvos()
            for pers, dist_m, cob in alvos_detectados:
                mat_auto = getattr(pers, "material_mapa", None)
                mat = mat_auto if mat_auto in (
                    "Nenhum", "Gesso", "Madeira", "Veiculo", "Concreto", "Aço"
                ) else "Nenhum"
                _append_alvo(pers, round(dist_m, 1), cob, mat)
            lbl_mapa_status.config(
                text=f"✓ Epicentro ({epicentro_wx:.0f},{epicentro_wy:.0f}) — "
                     f"{len(alvos_detectados)} alvo(s) importados"
            )

        tk.Button(
            add_inner, text="🗺 Abrir no Mapa",
            command=_abrir_mapa_epicentro,
            bg="#0a3d5c", fg=FG, font=("Arial", 9, "bold"),
            relief="flat", cursor="hand2"
        ).pack(side="right", padx=4)

        # ── LISTA DE ALVOS ────────────────────────────────────────────────────
        lista_frame = tk.LabelFrame(
            popup, text="Alvos no Raio",
            bg=BG, fg="orange", font=("Arial", 10, "bold")
        )
        lista_frame.pack(fill="both", expand=True, padx=12, pady=4)

        cab = tk.Frame(lista_frame, bg="#0d0824")
        cab.pack(fill="x", padx=4, pady=(4, 0))
        for txt, w in [("Personagem", 16), ("Dist(m)", 7), ("Cobertura", 10),
                       ("Material", 10), ("Buff", 5), ("Debuff", 6), ("", 4)]:
            tk.Label(
                cab, text=txt, bg="#0d0824", fg=FG_DIM,
                font=("Arial", 8, "bold"), width=w, anchor="w"
            ).pack(side="left", padx=2)

        cv_lista = tk.Canvas(lista_frame, bg=BG, highlightthickness=0)
        sb_lista = tk.Scrollbar(lista_frame, orient="vertical", command=cv_lista.yview)
        cv_lista.configure(yscrollcommand=sb_lista.set)
        sb_lista.pack(side="right", fill="y")
        cv_lista.pack(side="left", fill="both", expand=True, padx=4)

        frame_linhas = tk.Frame(cv_lista, bg=BG)
        cv_lista.create_window((0, 0), window=frame_linhas, anchor="nw")
        frame_linhas.bind(
            "<Configure>",
            lambda e: cv_lista.configure(scrollregion=cv_lista.bbox("all"))
        )
        cv_lista.bind("<Enter>", lambda e: cv_lista.bind_all(
            "<MouseWheel>",
            lambda ev: cv_lista.yview_scroll(int(ev.delta / -90), "units")))
        cv_lista.bind("<Leave>", lambda e: cv_lista.unbind_all("<MouseWheel>"))

        def _rebuild_lista_alvos():
            for w in frame_linhas.winfo_children():
                w.destroy()
            for idx, d in enumerate(alvos_data):
                _criar_linha_alvo(idx, d)

        def _criar_linha_alvo(idx, d):
            zona_letal = d["dist"].get() <= raio_letal
            bg_ln = "#2a0800" if zona_letal else BG2
            row = tk.Frame(frame_linhas, bg=bg_ln, bd=1, relief="solid")
            row.pack(fill="x", padx=2, pady=2)

            icone = "💥" if zona_letal else "⚡"
            tk.Label(row, text=icone, bg=bg_ln, fg="yellow",
                     font=("Arial", 9)).pack(side="left", padx=(4, 2))
            tk.Label(
                row, text=d["pers"].nome, bg=bg_ln, fg=FG,
                font=("Arial", 9, "bold"), width=16, anchor="w"
            ).pack(side="left", padx=2)
            tk.Entry(
                row, textvariable=d["dist"], width=7,
                bg=ENT, fg=FG, font=("Arial", 9),
                justify="center", insertbackground=FG
            ).pack(side="left", padx=2)
            ttk.Combobox(
                row, textvariable=d["cob"], state="readonly",
                values=["Nenhuma", "Parcial", "Alta", "Total"], width=10
            ).pack(side="left", padx=2)
            ttk.Combobox(
                row, textvariable=d["mat"], state="readonly",
                values=["Nenhum", "Gesso", "Madeira", "Veiculo", "Concreto", "Aço"], width=10
            ).pack(side="left", padx=2)
            tk.Entry(
                row, textvariable=d["buff"], width=5,
                bg=ENT, fg="#90ee90", font=("Arial", 9),
                justify="center", insertbackground=FG
            ).pack(side="left", padx=2)
            tk.Entry(
                row, textvariable=d["debuff"], width=5,
                bg=ENT, fg="#ff9999", font=("Arial", 9),
                justify="center", insertbackground=FG
            ).pack(side="left", padx=2)
            tk.Button(
                row, text="✕",
                command=lambda i=idx: _remover_alvo(i),
                bg=bg_ln, fg="#cc4444",
                font=("Arial", 9), relief="flat", cursor="hand2"
            ).pack(side="left", padx=4)

        def _append_alvo(pers, dist_m, cob, mat):
            d = {
                "pers":   pers,
                "dist":   tk.DoubleVar(value=dist_m),
                "cob":    tk.StringVar(value=cob),
                "mat":    tk.StringVar(value=mat),
                "buff":   tk.IntVar(value=0),
                "debuff": tk.IntVar(value=0),
            }
            alvos_data.append(d)
            _rebuild_lista_alvos()

        def _remover_alvo(idx):
            if 0 <= idx < len(alvos_data):
                alvos_data.pop(idx)
                _rebuild_lista_alvos()

        # ── RESULTADO ────────────────────────────────────────────────────────
        res_frame = tk.Frame(popup, bg=BG, bd=1, relief="ridge", height=70)
        res_frame.pack(fill="x", padx=12, pady=(4, 2))
        res_frame.pack_propagate(False)
        lbl_resultado = tk.Label(
            res_frame, text="", bg=BG, fg="#90caf9",
            font=("Arial", 9), wraplength=800, justify="left", anchor="nw"
        )
        lbl_resultado.pack(fill="both", expand=True, padx=8, pady=4)

        # ── PROCESSAR ────────────────────────────────────────────────────────
        def _processar(aplicar=False):
            """
            Delega o cálculo para CB.calcular_dano_explosao, que já trata:
              - falloff correto
              - regiões expostas (cobertura bloqueia fatias de dano)
              - penetração de material vs fragmentação
              - armadura do alvo por região
            """
            if not alvos_data:
                lbl_resultado.config(text="❌ Nenhum alvo adicionado.", fg="#ff9999")
                return

            try:
                log_total  = []
                dano_total = 0

                for d in alvos_data:
                    buff_ef   = d["buff"].get()   + var_ubuff.get()
                    debuff_ef = d["debuff"].get() + var_udebuff.get()

                    # calcular_dano_explosao espera lista de (alvo, distancia)
                    # mas cada entrada pode ter cobertura e material diferentes,
                    # então chamamos uma vez por alvo
                    res = CB.calcular_dano_explosao(
                        item=item_consumivel,
                        atacante=personagem_usuario,
                        alvos_distancias=[(d["pers"], d["dist"].get())],
                        cobertura=d["cob"].get(),
                        material=d["mat"].get(),
                        BuffDano=buff_ef,
                        DebuffDano=debuff_ef,
                        aplicar=aplicar,
                    )

                    entrada_alvo = res["alvos"][0] if res["alvos"] else {}
                    dano_alvo    = entrada_alvo.get("dano_total", 0)
                    atingido     = entrada_alvo.get("atingido", False)
                    mult_falloff = entrada_alvo.get("mult_falloff", 0.0)

                    dano_total += dano_alvo

                    if not atingido:
                        log_total.append(
                            f"  → {d['pers'].nome}: fora do raio ({d['dist'].get():.1f}m)"
                        )
                    else:
                        detalhe_regioes = "  ".join(
                            f"{r['regiao']}:{r['dano_final']}"
                            for r in entrada_alvo.get("regioes", [])
                        )
                        pen_txt = ""
                        if entrada_alvo.get("regioes"):
                            pen = entrada_alvo["regioes"][0].get("mult_penetracao_cobertura", 1.0)
                            if pen != 1.0:
                                pen_txt = f" | pen×{pen:.2f}"

                        log_total.append(
                            f"  → {d['pers'].nome} ({d['cob'].get()}/{d['mat'].get()}) "
                            f"dist {d['dist'].get():.1f}m | falloff×{mult_falloff:.2f}{pen_txt} "
                            f"— Dano total: {dano_alvo}  [{detalhe_regioes}]"
                        )

                        # Buffs/debuffs de status (não são tratados por calcular_dano_explosao)
                        if aplicar and atingido:
                            efeitos_bb = [
                                ef for ef in getattr(item_consumivel, "efeitos", [])
                                if isinstance(ef, dict) and ef.get("tipo") in ("buff", "debuff")
                            ]
                            if efeitos_bb:
                                aplicados = aplicar_efeitos_item(
                                    efeitos_bb, d["pers"], mult_chance=mult_falloff
                                )
                                if aplicados:
                                    log_total.append(
                                        f"    ✨ Efeitos em {d['pers'].nome}: "
                                        f"{', '.join(aplicados)}"
                                    )

                # ── Consumir item ──────────────────────────────────────────────
                if aplicar:
                    if personagem_usuario.inventario.remover_item(item_consumivel, 1):
                        log_total.append(
                            f"\n✓ {personagem_usuario.nome} consumiu {item_consumivel.nome}."
                        )
                    else:
                        log_total.append(
                            f"\n⚠ [ERRO] Falha ao consumir {item_consumivel.nome}."
                        )

                cor = "#90caf9" if aplicar else "#aaaaaa"
                lbl_resultado.config(
                    text="\n".join(log_total) if log_total else "Sem log",
                    fg=cor
                )

                if aplicar:
                    self.adicionar_log(
                        f"💥 Área: {item_consumivel.nome} por "
                        f"{personagem_usuario.nome} ({len(alvos_data)} alvo(s)) "
                        f"— {dano_total} dano total",
                        "orange",
                        detalhes={"Log": log_total}
                    )
                    popup.destroy()
                    self.refresh()

            except Exception as e:
                lbl_resultado.config(text=f"❌ Erro: {e}", fg="#ff9999")
                import traceback
                traceback.print_exc()

        # ── BOTÕES RODAPÉ ─────────────────────────────────────────────────────
        rodape = tk.Frame(popup, bg=BGDARK)
        rodape.pack(fill="x", padx=12, pady=8)

        tk.Button(
            rodape, text="🔍 Simular",
            command=lambda: _processar(aplicar=False),
            bg="#1a3060", fg=FG, font=("Arial", 11), padx=12
        ).pack(side="left", padx=6)

        tk.Button(
            rodape, text="💥 USAR AGORA!",
            command=lambda: _processar(aplicar=True),
            bg="#6b1a1a", fg=FG, font=("Arial", 12, "bold"), padx=16
        ).pack(side="left", padx=6)

        tk.Button(
            rodape, text="Cancelar", command=popup.destroy,
            bg="#3a0a80", fg=FG, font=("Arial", 10)
        ).pack(side="right", padx=6)

        popup.transient(self)
        popup.grab_set()

    def abrir_popup_ataque_melee(self, atacante_pre_selecionado, titulo_extra="", arma_pre=None, callback_resultado=None):
        import random
        popup = tk.Toplevel(self)
        titulo_str = f"Ataque Melee — {atacante_pre_selecionado.nome}" + (f" {titulo_extra}" if titulo_extra else "")
        popup.title(titulo_str)
        popup.geometry("500x590")
        popup.configure(bg="#1a1a2e")
        popup.resizable(False, False)
        todos_personagens = self._get_alvos_unicos()
        personagens_names = [p.nome for p in todos_personagens]
        main_frame = tk.Frame(popup, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=12)
        tk.Label(main_frame, text=titulo_str, bg="#1a1a2e", fg="white", font=("Arial", 12, "bold")).pack(pady=(0, 10))

        def _row(label, widget_factory):
            f = tk.Frame(main_frame, bg="#1a1a2e")
            f.pack(fill="x", pady=2)
            tk.Label(f, text=label, bg="#1a1a2e", fg="white", font=("Arial", 10), width=22, anchor="w").pack(side="left")
            w = widget_factory(f)
            w.pack(side="right")
            return w

        alvo_var = tk.StringVar()
        _row("Alvo:", lambda f: ttk.Combobox(f, textvariable=alvo_var, state="readonly", values=personagens_names, width=28))
        arma_var = tk.StringVar()
        arma_combo = _row("Arma Melee:", lambda f: ttk.Combobox(f, textvariable=arma_var, state="readonly", width=28))
        arma_info_label = tk.Label(main_frame, text="", bg="#1a1a2e", fg="#aaaaaa", font=("Arial", 9))
        arma_info_label.pack(anchor="e", padx=4)
        regiao_var = tk.StringVar(value="aleatoria")
        _row("Região:", lambda f: ttk.Combobox(f, textvariable=regiao_var, state="readonly", width=28,
             values=["aleatoria", "cabeça", "rosto", "pescoço", "peito", "costas", "abdômen", "braços", "pernas"]))
        furtivo_var = tk.BooleanVar(value=False)
        _row("Furtivo:", lambda f: tk.Checkbutton(f, variable=furtivo_var, bg="#1a1a2e", activebackground="#1a1a2e"))

        # Arremesso — sempre visível, avisa se não tem tag
        arremesso_var = tk.BooleanVar(value=False)
        arremesso_frame = tk.Frame(main_frame, bg="#1a1a2e")
        arremesso_frame.pack(fill="x", pady=2)
        tk.Label(arremesso_frame, text="Arremessar:", bg="#1a1a2e", fg="white", font=("Arial", 10), width=22, anchor="w").pack(side="left")
        arremesso_aviso = tk.Label(arremesso_frame, text="", bg="#1a1a2e", fg="#ff9944", font=("Arial", 8))
        arremesso_aviso.pack(side="right", padx=4)
        tk.Checkbutton(arremesso_frame, variable=arremesso_var, bg="#1a1a2e", activebackground="#1a1a2e").pack(side="right")

        buff_acerto_var   = tk.IntVar(value=0)
        debuff_acerto_var = tk.IntVar(value=0)
        buff_dano_var     = tk.IntVar(value=0)
        debuff_dano_var   = tk.IntVar(value=0)
        _row("Buff Acerto:",   lambda f: tk.Entry(f, textvariable=buff_acerto_var,   width=8, font=("Arial", 10), justify="center"))
        _row("Debuff Acerto:", lambda f: tk.Entry(f, textvariable=debuff_acerto_var, width=8, font=("Arial", 10), justify="center"))
        _row("Buff Dano:",     lambda f: tk.Entry(f, textvariable=buff_dano_var,     width=8, font=("Arial", 10), justify="center"))
        _row("Debuff Dano:",   lambda f: tk.Entry(f, textvariable=debuff_dano_var,   width=8, font=("Arial", 10), justify="center"))

        rolagem_var = tk.IntVar(value=0)
        f_rol = tk.Frame(main_frame, bg="#1a1a2e")
        f_rol.pack(fill="x", pady=6)
        tk.Label(f_rol, text="Valor do Dado:", bg="#1a1a2e", fg="white", font=("Arial", 10), width=22, anchor="w").pack(side="left")
        tk.Entry(f_rol, textvariable=rolagem_var, width=7, font=("Arial", 10), justify="center").pack(side="left", padx=6)
        rolagem_info = tk.Label(f_rol, text="", bg="#1a1a2e", fg="lightblue", font=("Arial", 8))
        rolagem_info.pack(side="left")

        def _rolar():
            n = max(1, atacante_pre_selecionado.Forca // 2)
            rolls = [random.randint(1, 20) for _ in range(n)]
            best = max(rolls)
            rolagem_var.set(best)
            rolagem_info.config(text=f"Força ({n}×D20): {rolls} → {best}")

        tk.Button(f_rol, text="🎲 Rolar", command=_rolar, bg="#0077b6", fg="white", font=("Arial", 9)).pack(side="right")

        resultado_label = tk.Label(main_frame, text="", bg="#1a1a2e", fg="lightgreen", font=("Arial", 9), wraplength=450)
        resultado_label.pack(pady=4)

        arma_map: dict = {}

        def _atualizar_info_arma(*_):
            arma = arma_map.get(arma_var.get())
            if not arma:
                arma_info_label.config(text=""); arremesso_aviso.config(text=""); return
            tags_txt = ", ".join(sorted(arma.tags)) if arma.tags else "—"
            arma_info_label.config(text=f"Tags: {tags_txt} | Dano: {arma.dano} | Crit: {arma.valor_critico}+")
            arremesso_aviso.config(text="✔ dano completo" if "arremessavel" in arma.tags else "⚠ sem tag — ¼ dano")

        arma_combo.bind("<<ComboboxSelected>>", _atualizar_info_arma)

        def _atualizar_armas():
            arma_map.clear()
            for slot in atacante_pre_selecionado.slots.values():
                if slot.item and isinstance(slot.item, CB.Melee):
                    arma_map[f"{slot.item.nome} [{slot.nome}]"] = slot.item
            for entrada in atacante_pre_selecionado.inventario.itens:
                item = entrada["item"] if isinstance(entrada, dict) else entrada
                if isinstance(item, CB.Melee):
                    arma_map[f"{item.nome} [inv]"] = item
            arma_combo["values"] = list(arma_map.keys())
            if arma_pre:
                chave = next((k for k, v in arma_map.items() if v is arma_pre), None)
                arma_var.set(chave if chave else (list(arma_map.keys())[0] if arma_map else ""))
            elif arma_map:
                arma_var.set(list(arma_map.keys())[0])
            _atualizar_info_arma()

        def _confirmar():
            alvo = next((p for p in todos_personagens if p.nome == alvo_var.get()), None)
            arma = arma_map.get(arma_var.get())
            if not alvo or not arma:
                resultado_label.config(text="Selecione alvo e arma.", fg="red"); return
            res = CB.acerto_melee(
                atacante=atacante_pre_selecionado, alvo=alvo,
                rolagem=rolagem_var.get(), id_arma=arma.Id,
                regiao=regiao_var.get(), furtivo=furtivo_var.get(),
                arremesso=arremesso_var.get(),
                BuffDano=buff_dano_var.get(), DebuffDano=debuff_dano_var.get(),
                BuffAcerto=buff_acerto_var.get(), DebuffAcerto=debuff_acerto_var.get()
            )
            if res["acertou"]:
                efeitos_aplicados = aplicar_efeitos_item(getattr(arma, "efeitos", []), alvo)
                if efeitos_aplicados:
                    res["log"].append(f"Efeitos: {', '.join(efeitos_aplicados)}")
            if callback_resultado:
                callback_resultado(res); popup.destroy(); return
            cor = "lightgreen" if res["acertou"] else "orange"
            resultado_label.config(text=" | ".join(res["log"]), fg=cor)
            detalhes = {
                "Resultado": ("✅ ACERTO" + (" 💥 CRÍTICO" if res["critico"] else "")) if res["acertou"] else "❌ ERRO",
                "Região": res["regiao"] or "—",
                "Dano": f"{res['dano_final']} (bruto {res['dano_bruto']} | abs {res['absorcao']})",
                "Tipo de Dano": res["tipo_dano"] or "—",
                "Efeito Crítico": res["efeito_critico"] or "—",
                "Arremesso": "Sim — ficou com o alvo" if res.get("arremesso") and res["acertou"] else ("Sim — caiu no campo" if res.get("arma_perdida") else "Não"),
                "Efeitos Aplicados": ", ".join(res["log"][-1:]) if res["acertou"] and getattr(arma, "efeitos", []) else "—",
            }
            self.adicionar_log(f"⚔ Melee: {atacante_pre_selecionado.nome} → {alvo.nome}", cor, detalhes=detalhes)
            self.refresh()

        btn_frame = tk.Frame(main_frame, bg="#1a1a2e")
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Confirmar Ataque", command=_confirmar, bg="#38b000", fg="white", font=("Arial", 11), width=16).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Cancelar", command=popup.destroy, bg="#8B0000", fg="white", font=("Arial", 11), width=16).pack(side="left", padx=6)
        _atualizar_armas()

    def abrir_popup_ataque_desarmado(self, atacante):
        BG = "#1a1a2e"; CARD = "#12102e"; ENT = "#0b0926"; FG = "white"
        ACC = "#38b000"; RED = "#8B0000"

        popup = tk.Toplevel(self)
        popup.title(f"Ataque Desarmado — {atacante.nome}")
        popup.configure(bg=BG)
        popup.resizable(True, True)

        todos = self._get_alvos_unicos()
        nomes = [p.nome for p in todos]

        # ── header ───────────────────────────────────────────────────────────
        hdr = tk.Frame(popup, bg="#090720", height=46)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        params = atacante.calcular_ataque_desarmado()
        info_txt = (f"👊 {atacante.nome}  |  "
                    f"Dano: {params['dano_base']} + {params['dano_mod']:+}  "
                    f"Crit: ×{params['crit_mult']}  em {params['crit_valor']}+  "
                    f"(Prof. Luta: {params['prof_luta']})")
        tk.Label(hdr, text=info_txt, bg="#090720", fg="#a88fff",
                font=("Consolas", 9, "bold")).pack(side="left", padx=12, pady=10)

        # ── scroll principal ─────────────────────────────────────────────────
        outer = tk.Frame(popup, bg=BG)
        outer.pack(fill="both", expand=True)
        cv = tk.Canvas(outer, bg=BG, highlightthickness=0, width=540)
        sb = tk.Scrollbar(outer, orient="vertical", command=cv.yview)
        inner = tk.Frame(cv, bg=BG)
        inner.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
        cv.create_window((0, 0), window=inner, anchor="nw")
        cv.configure(yscrollcommand=sb.set)
        cv.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        cv.bind("<Enter>",  lambda e: cv.bind_all("<MouseWheel>",   lambda ev: cv.yview_scroll(int(ev.delta / -90), "units")))
        cv.bind("<Leave>",  lambda e: cv.unbind_all("<MouseWheel>"))

        def sep():
            tk.Frame(inner, bg="#2a1f6a", height=1).pack(fill="x", padx=10, pady=4)

        def lbl_entry(parent, label, var, width=6):
            f = tk.Frame(parent, bg=CARD)
            f.pack(side="left", padx=4)
            tk.Label(f, text=label, bg=CARD, fg="#8899cc",
                    font=("Arial", 9)).pack(side="left", padx=(0, 3))
            tk.Entry(f, textvariable=var, width=width, bg=ENT, fg=FG,
                    insertbackground=FG, relief="flat",
                    font=("Arial", 9), justify="center").pack(side="left")
            return f

        # ── Buffs/Debuffs globais ─────────────────────────────────────────────
        sec_global = tk.Frame(inner, bg=CARD, relief="ridge", bd=1)
        sec_global.pack(fill="x", padx=10, pady=(10, 2))
        tk.Label(sec_global, text="Modificadores Gerais", bg=CARD, fg="#9988dd",
                font=("Consolas", 9, "bold"), padx=8, pady=4).pack(anchor="w")

        row_global = tk.Frame(sec_global, bg=CARD)
        row_global.pack(fill="x", padx=8, pady=(0, 8))
        g_buff_dano    = tk.IntVar(value=0)
        g_debuff_dano  = tk.IntVar(value=0)
        g_buff_ac      = tk.IntVar(value=0)
        g_debuff_ac    = tk.IntVar(value=0)
        lbl_entry(row_global, "Buff Dano:",    g_buff_dano)
        lbl_entry(row_global, "Debuff Dano:",  g_debuff_dano)
        lbl_entry(row_global, "Buff Acerto:",  g_buff_ac)
        lbl_entry(row_global, "Debuff Acerto:", g_debuff_ac)

        # ── Botão "Rolar para todos" ──────────────────────────────────────────
        def _rolar_todos():
            import random
            n = max(1, atacante.Forca // 2)
            for alvo_data in linhas_alvos:
                rolls = [random.randint(1, 20) for _ in range(n)]
                alvo_data["rol_var"].set(max(rolls))
                alvo_data["rol_info"].config(
                    text=f"Força ({n}×D20): {rolls} → {max(rolls)}")

        tk.Button(inner, text="🎲 Rolar Acerto para Todos",
                command=_rolar_todos, bg="#0077b6", fg=FG,
                font=("Arial", 10, "bold"), relief="flat",
                pady=5, cursor="hand2").pack(fill="x", padx=10, pady=(4, 2))

        sep()

        # ── Lista de alvos ────────────────────────────────────────────────────
        tk.Label(inner, text="Alvos", bg=BG, fg="#9988dd",
                font=("Consolas", 9, "bold")).pack(anchor="w", padx=12)

        frame_alvos = tk.Frame(inner, bg=BG)
        frame_alvos.pack(fill="x", padx=10)

        linhas_alvos = []   # cada item: dict com vars e widgets

        def _rebuild_alvos():
            for w in frame_alvos.winfo_children():
                w.destroy()
            for idx, d in enumerate(linhas_alvos):
                bloco = tk.Frame(frame_alvos, bg=CARD, relief="ridge", bd=1)
                bloco.pack(fill="x", pady=4)

                # ── Linha 1: Alvo | Ataques | Rolagem | [Remover] ────────────
                row1 = tk.Frame(bloco, bg=CARD)
                row1.pack(fill="x", padx=8, pady=(6, 2))

                tk.Label(row1, text="Alvo:", bg=CARD, fg="#8899cc",
                        font=("Arial", 9)).pack(side="left", padx=(0, 3))
                alvo_cb = ttk.Combobox(row1, textvariable=d["alvo_var"],
                                    values=nomes, state="readonly",
                                    font=("Arial", 9), width=16)
                alvo_cb.pack(side="left", padx=(0, 8))

                tk.Label(row1, text="Ataques:", bg=CARD, fg="#8899cc",
                        font=("Arial", 9)).pack(side="left", padx=(0, 3))
                tk.Entry(row1, textvariable=d["ataques_var"], width=3,
                        bg=ENT, fg=FG, insertbackground=FG,
                        relief="flat", font=("Arial", 9),
                        justify="center").pack(side="left", padx=(0, 8))

                tk.Label(row1, text="Rolagem:", bg=CARD, fg="#8899cc",
                        font=("Arial", 9)).pack(side="left", padx=(0, 3))
                tk.Entry(row1, textvariable=d["rol_var"], width=5,
                        bg=ENT, fg=FG, insertbackground=FG,
                        relief="flat", font=("Arial", 9),
                        justify="center").pack(side="left", padx=(0, 4))

                def _rolar_este(data=d):
                    import random
                    n = max(1, atacante.Forca // 2)
                    rolls = [random.randint(1, 20) for _ in range(n)]
                    best = max(rolls)
                    data["rol_var"].set(best)
                    data["rol_info"].config(
                        text=f"({n}×D20): {rolls} → {best}")

                tk.Button(row1, text="🎲", command=_rolar_este,
                        bg="#0077b6", fg=FG, font=("Arial", 9),
                        relief="flat", cursor="hand2",
                        padx=4).pack(side="left", padx=(0, 6))

                rol_info = tk.Label(row1, text="", bg=CARD, fg="lightblue",
                                    font=("Arial", 8))
                rol_info.pack(side="left")
                d["rol_info"] = rol_info  # guarda ref para _rolar_todos

                def _remover(i=idx):
                    linhas_alvos.pop(i)
                    _rebuild_alvos()

                tk.Button(row1, text="✕ Remover", command=_remover,
                        bg="#3a0000", fg="#ff6666", font=("Arial", 8, "bold"),
                        relief="flat", cursor="hand2",
                        bd=0).pack(side="right", padx=4)

                # ── Linha 2: Buff/Debuff individuais ─────────────────────────
                row2 = tk.Frame(bloco, bg=CARD)
                row2.pack(fill="x", padx=8, pady=(2, 6))
                lbl_entry(row2, "Buff Dano:",    d["buff_dano"])
                lbl_entry(row2, "Debuff Dano:",  d["debuff_dano"])
                lbl_entry(row2, "Buff Acerto:",  d["buff_ac"])
                lbl_entry(row2, "Debuff Acerto:", d["debuff_ac"])

        def _add_alvo():
            linhas_alvos.append({
                "alvo_var":   tk.StringVar(value=nomes[0] if nomes else ""),
                "ataques_var": tk.IntVar(value=1),
                "rol_var":    tk.IntVar(value=0),
                "rol_info":   None,
                "buff_dano":  tk.IntVar(value=0),
                "debuff_dano": tk.IntVar(value=0),
                "buff_ac":    tk.IntVar(value=0),
                "debuff_ac":  tk.IntVar(value=0),
            })
            _rebuild_alvos()

        _add_alvo()  # começa com 1 alvo

        sep()

        tk.Button(inner, text="＋  Adicionar Alvo", command=_add_alvo,
                bg="#1f4a2a", fg=FG, font=("Arial", 10),
                relief="flat", pady=4, padx=10,
                cursor="hand2").pack(anchor="w", padx=10, pady=(0, 6))

        # ── resultado ─────────────────────────────────────────────────────────
        resultado_label = tk.Label(inner, text="", bg=BG, fg="lightgreen",
                                font=("Arial", 9), wraplength=500,
                                justify="left")
        resultado_label.pack(padx=10, pady=4)

        # ── Confirmar ─────────────────────────────────────────────────────────
        def _confirmar():
            if not linhas_alvos:
                resultado_label.config(text="Adicione ao menos um alvo.", fg="red")
                return

            log_total = []
            erro = False

            for d in linhas_alvos:
                alvo_obj = next((p for p in todos if p.nome == d["alvo_var"].get()), None)
                if not alvo_obj:
                    resultado_label.config(text="Selecione um alvo válido.", fg="red")
                    erro = True; break

                n_ataques = max(1, d["ataques_var"].get())
                rolagem   = d["rol_var"].get()
                b_dano  = d["buff_dano"].get()  + g_buff_dano.get()
                db_dano = d["debuff_dano"].get() + g_debuff_dano.get()
                b_ac    = d["buff_ac"].get()    + g_buff_ac.get()
                db_ac   = d["debuff_ac"].get()  + g_debuff_ac.get()

                for i in range(n_ataques):
                    res = CB.acerto_desarmado(
                        atacante=atacante, alvo=alvo_obj,
                        rolagem=rolagem,
                        BuffDano=b_dano, DebuffDano=db_dano,
                        BuffAcerto=b_ac, DebuffAcerto=db_ac,
                    )
                    cor = "lightgreen" if res["acertou"] else "orange"
                    prefixo = f"[Ataque {i+1}/{n_ataques}] " if n_ataques > 1 else ""
                    detalhes = {
                        "Resultado": ("✅ ACERTO" + (" 💥 CRÍTICO" if res["critico"] else "")) if res["acertou"] else "❌ ERRO",
                        "Região":    res["regiao"] or "—",
                        "Dano":      f"{res['dano_final']} (bruto {res['dano_bruto']} | abs {res['absorcao']})",
                        "Tipo":      res["tipo_dano"],
                        "Efeito Crítico": res["efeito_critico"] or "—",
                    }
                    self.adicionar_log(
                        f"👊 {prefixo}{atacante.nome} → {alvo_obj.nome}: " + " | ".join(res["log"]),
                        cor, detalhes=detalhes)
                    log_total.append(f"{alvo_obj.nome}: " + " | ".join(res["log"]))

            if not erro:
                resultado_label.config(text="\n".join(log_total),
                                    fg="lightgreen" if log_total else "orange")
                self.refresh()

        # ── barra de botões ───────────────────────────────────────────────────
        bbar = tk.Frame(popup, bg="#090720", height=50)
        bbar.pack(fill="x", side="bottom")
        bbar.pack_propagate(False)
        tk.Button(bbar, text="  ✕  Cancelar  ", command=popup.destroy,
                bg=RED, fg=FG, relief="flat",
                font=("Arial", 10, "bold"), cursor="hand2",
                pady=6).pack(side="right", padx=10, pady=8)
        tk.Button(bbar, text="  👊  Confirmar  ", command=_confirmar,
                bg=ACC, fg=FG, relief="flat",
                font=("Arial", 10, "bold"), cursor="hand2",
                pady=6).pack(side="right", padx=(0, 6), pady=8)

        popup.transient(self)
        popup.grab_set()

    def abrir_popup_ataque_ranged(self, atacante_pre_selecionado, titulo_extra="", callback_resultado=None):
        import random
        popup = tk.Toplevel(self)
        titulo_str = f"Ataque Ranged — {atacante_pre_selecionado.nome}" + (f" {titulo_extra}" if titulo_extra else "")
        popup.title(titulo_str)
        popup.geometry("520x660")
        popup.configure(bg="#1a1a2e")
        popup.resizable(False, False)
        todos_personagens = self._get_alvos_unicos()
        personagens_names = [p.nome for p in todos_personagens]
        main_frame = tk.Frame(popup, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=12)
        tk.Label(main_frame, text=titulo_str, bg="#1a1a2e", fg="white", font=("Arial", 12, "bold")).pack(pady=(0, 10))

        def _row(label, widget_factory):
            f = tk.Frame(main_frame, bg="#1a1a2e")
            f.pack(fill="x", pady=2)
            tk.Label(f, text=label, bg="#1a1a2e", fg="white", font=("Arial", 10), width=22, anchor="w").pack(side="left")
            w = widget_factory(f)
            w.pack(side="right")
            return w

        alvo_var = tk.StringVar()
        alvo_combo = _row("Alvo:", lambda f: ttk.Combobox(f, textvariable=alvo_var, state="readonly", values=personagens_names, width=28))
        arma_var = tk.StringVar()
        arma_combo = _row("Arma Ranged:", lambda f: ttk.Combobox(f, textvariable=arma_var, state="readonly", width=28))
        arma_info_label = tk.Label(main_frame, text="", bg="#1a1a2e", fg="#aaaaaa", font=("Arial", 9))
        arma_info_label.pack(anchor="e", padx=4)
        regiao_var = tk.StringVar(value="aleatoria")
        _row("Região:", lambda f: ttk.Combobox(f, textvariable=regiao_var, state="readonly", width=28,
             values=["aleatoria", "cabeça", "rosto", "pescoço", "peito", "costas", "abdômen", "braços", "pernas"]))

        distancia_var = tk.IntVar(value=1)
        f_dist = tk.Frame(main_frame, bg="#1a1a2e")
        f_dist.pack(fill="x", pady=2)
        tk.Label(f_dist, text="Distância (m):", bg="#1a1a2e", fg="white", font=("Arial", 10), width=22, anchor="w").pack(side="left")
        dist_origem_label = tk.Label(f_dist, text="", bg="#1a1a2e", fg="#666688", font=("Arial", 8))
        dist_origem_label.pack(side="right", padx=4)
        tk.Entry(f_dist, textvariable=distancia_var, width=10, font=("Arial", 10), justify="center").pack(side="right")

        cobertura_var = tk.StringVar(value="Nenhuma")
        cob_frame = tk.Frame(main_frame, bg="#1a1a2e")
        cob_frame.pack(fill="x", pady=2)
        tk.Label(cob_frame, text="Cobertura do Alvo:", bg="#1a1a2e", fg="white", font=("Arial", 10), width=22, anchor="w").pack(side="left")
        cob_origem_label = tk.Label(cob_frame, text="", bg="#1a1a2e", fg="#666688", font=("Arial", 8))
        cob_origem_label.pack(side="right", padx=2)
        ttk.Combobox(cob_frame, textvariable=cobertura_var, state="readonly", width=16, values=["Nenhuma", "Parcial", "Alta", "Total"]).pack(side="right")

        material_var = tk.StringVar(value="Nenhum")
        _row("Material Cobertura:", lambda f: ttk.Combobox(f, textvariable=material_var, state="readonly", width=28,
             values=["Nenhum", "Gesso", "Madeira", "Veiculo", "Concreto", "Aço"]))

        disparos_var = tk.IntVar(value=1)
        f_disp = tk.Frame(main_frame, bg="#1a1a2e")
        f_disp.pack(fill="x", pady=2)
        tk.Label(f_disp, text="Disparos:", bg="#1a1a2e", fg="white", font=("Arial", 10), width=22, anchor="w").pack(side="left")
        tk.Entry(f_disp, textvariable=disparos_var, width=7, font=("Arial", 10), justify="center").pack(side="right")

        f_disp_btns = tk.Frame(main_frame, bg="#1a1a2e")
        f_disp_btns.pack(fill="x", pady=1)
        tempo_info_label = tk.Label(f_disp_btns, text="", bg="#1a1a2e", fg="#aaaaaa", font=("Arial", 8))
        tempo_info_label.pack(side="left")

        arma_map: dict = {}

        def _arma_atual():
            return arma_map.get(arma_var.get())

        def _tudo():
            arma = _arma_atual()
            if arma:
                disparos_var.set(arma.munições); tempo_info_label.config(text=f"Tudo: {arma.munições} tiro(s)")

        def _randomizar_tempo():
            arma = _arma_atual()
            if not arma or arma.TPM <= 0:
                tempo_info_label.config(text="TPM inválido."); return
            seg = round(random.uniform(0.05, 2.0), 2)
            qtd = CB.calcular_disparos_por_tempo(arma.TPM, arma.capacidade, arma.munições, seg)
            disparos_var.set(qtd)
            tempo_info_label.config(text=f"{seg:.2f}s × {arma.TPM} TPM = {qtd} tiro(s) (max {arma.munições})")

        tk.Button(f_disp_btns, text="🎲 Randomizar tempo", command=_randomizar_tempo, bg="#0077b6", fg="white", font=("Arial", 9), padx=4).pack(side="right", padx=2)
        tk.Button(f_disp_btns, text="📦 Tudo", command=_tudo, bg="#444", fg="white", font=("Arial", 9), padx=4).pack(side="right", padx=2)

        buff_acerto_var   = tk.IntVar(value=0)
        debuff_acerto_var = tk.IntVar(value=0)
        buff_dano_var     = tk.IntVar(value=0)
        debuff_dano_var   = tk.IntVar(value=0)
        _row("Buff Acerto:",   lambda f: tk.Entry(f, textvariable=buff_acerto_var,   width=8, font=("Arial", 10), justify="center"))
        _row("Debuff Acerto:", lambda f: tk.Entry(f, textvariable=debuff_acerto_var, width=8, font=("Arial", 10), justify="center"))
        _row("Buff Dano:",     lambda f: tk.Entry(f, textvariable=buff_dano_var,     width=8, font=("Arial", 10), justify="center"))
        _row("Debuff Dano:",   lambda f: tk.Entry(f, textvariable=debuff_dano_var,   width=8, font=("Arial", 10), justify="center"))

        rolagem_var = tk.IntVar(value=0)
        f_rol = tk.Frame(main_frame, bg="#1a1a2e")
        f_rol.pack(fill="x", pady=6)
        tk.Label(f_rol, text="Valor do Dado:", bg="#1a1a2e", fg="white", font=("Arial", 10), width=22, anchor="w").pack(side="left")
        tk.Entry(f_rol, textvariable=rolagem_var, width=7, font=("Arial", 10), justify="center").pack(side="left", padx=6)
        rolagem_info = tk.Label(f_rol, text="", bg="#1a1a2e", fg="lightblue", font=("Arial", 8))
        rolagem_info.pack(side="left")

        def _rolar():
            n = max(1, atacante_pre_selecionado.Tatica // 2)
            rolls = [random.randint(1, 20) for _ in range(n)]
            best = max(rolls)
            rolagem_var.set(best)
            rolagem_info.config(text=f"Tática ({n}×D20): {rolls} → {best}")

        tk.Button(f_rol, text="🎲 Rolar", command=_rolar, bg="#0077b6", fg="white", font=("Arial", 9)).pack(side="right")

        resultado_label = tk.Label(main_frame, text="", bg="#1a1a2e", fg="lightgreen", font=("Arial", 9), wraplength=460)
        resultado_label.pack(pady=4)

        def _preencher_do_mapa(alvo_obj):
            # ── distância ────────────────────────────────────────────────────
            dist = None
            if hasattr(self, "distancias_mapa"):
                dist = self.distancias_mapa.get(
                    atacante_pre_selecionado.nome, {}
                ).get(alvo_obj.nome)
            if dist is not None:
                distancia_var.set(int(round(dist)))
                dist_origem_label.config(text="(mapa)")
            else:
                distancia_var.set(1)
                dist_origem_label.config(text="(manual)")

            # ── cobertura ─────────────────────────────────────────────────────
            cob = getattr(alvo_obj, "cobertura_mapa", None)
            if cob in ("Nenhuma", "Parcial", "Alta", "Total"):
                cobertura_var.set(cob)
                cob_origem_label.config(text="(mapa)")
            else:
                cobertura_var.set("Nenhuma")
                cob_origem_label.config(text="(manual)")

            # ── material ──────────────────────────────────────────────────────
            mat = getattr(alvo_obj, "material_mapa", None)
            if mat in ("Nenhum", "Gesso", "Madeira", "Veiculo", "Concreto", "Aço"):
                material_var.set(mat)
            else:
                material_var.set("Nenhum")

        def _on_alvo_change(*_):
            alvo_obj = next((p for p in todos_personagens if p.nome == alvo_var.get()), None)
            if alvo_obj: _preencher_do_mapa(alvo_obj)

        alvo_combo.bind("<<ComboboxSelected>>", _on_alvo_change)

        def _atualizar_info_arma(*_):
            arma = _arma_atual()
            if arma:
                arma_info_label.config(text=f"Modo: {arma.modo_disparo_atual} | Munição: {arma.munições}/{arma.capacidade} | TPM: {arma.TPM}")

        arma_combo.bind("<<ComboboxSelected>>", _atualizar_info_arma)

        def _atualizar_armas():
            arma_map.clear()
            for slot in atacante_pre_selecionado.slots.values():
                if slot.item and isinstance(slot.item, CB.Ranged):
                    arma_map[f"{slot.item.nome} [{slot.nome}]"] = slot.item
            arma_combo["values"] = list(arma_map.keys())
            if arma_map:
                arma_var.set(list(arma_map.keys())[0]); _atualizar_info_arma()

        def _confirmar():
            alvo = next((p for p in todos_personagens if p.nome == alvo_var.get()), None)
            arma = _arma_atual()
            if not alvo or not arma:
                resultado_label.config(text="Selecione alvo e arma.", fg="red"); return
            if arma.munições <= 0:
                resultado_label.config(text="Sem munição.", fg="red"); return
            res = CB.acerto_ranged(
                atacante=atacante_pre_selecionado, alvo=alvo,
                rolagem=rolagem_var.get(), id_arma=arma.Id,
                distancia=distancia_var.get(), disparos=disparos_var.get(),
                regiao=regiao_var.get(), cobertura=cobertura_var.get(),
                material=material_var.get(),
                BuffAcerto=buff_acerto_var.get(), DebuffAcerto=debuff_acerto_var.get(),
                BuffDano=buff_dano_var.get(), DebuffDano=debuff_dano_var.get()
            )
            for tiro in res["por_disparo"]:
                if tiro["acertou"]:
                    efeitos_arma = getattr(arma, "efeitos", [])
                    efeitos_municao = getattr(arma.municao, "efeitos", []) if arma.municao else []
                    efeitos_aplicados = aplicar_efeitos_item(efeitos_arma + efeitos_municao, alvo)
                    tiro["efeitos_aplicados"].extend(efeitos_aplicados)
            if callback_resultado:
                callback_resultado(res); popup.destroy(); return
            acertos = sum(1 for t in res["por_disparo"] if t["acertou"])
            dano_total = sum(t["dano_final"] for t in res["por_disparo"] if t["acertou"])
            cor = "lightgreen" if res["acertou_algum"] else "orange"
            resultado_label.config(text=f"{res['disparos_realizados']} tiro(s) | {acertos} acerto(s) | Dano total: {dano_total}", fg=cor)
            detalhes = {
                "Arma": f"{arma.nome} | Modo: {res['modo_disparo']} | Munição: {res['municao_nome']}",
                "Distância": f"{distancia_var.get()}m | Cobertura: {cobertura_var.get()} ({material_var.get()})",
                "Disparos": f"{res['disparos_realizados']} tiro(s) | {acertos} acerto(s) | Dano total: {dano_total}",
                "Por tiro": res["log"],
            }
            self.adicionar_log(f"🔫 Ranged: {atacante_pre_selecionado.nome} [{arma.nome} / {res['modo_disparo']}] → {alvo.nome}", cor, detalhes=detalhes)
            self.refresh()
            _atualizar_info_arma()

        btn_frame = tk.Frame(main_frame, bg="#1a1a2e")
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Confirmar Ataque", command=_confirmar, bg="#38b000", fg="white", font=("Arial", 11), width=16).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Cancelar", command=popup.destroy, bg="#8B0000", fg="white", font=("Arial", 11), width=16).pack(side="left", padx=6)
        _atualizar_armas()

    def _usar_hab_poder_ofensivo(self, char, item_ofensivo):
        """
        Popup único para PoderOfensivo / HabilidadeOfensiva.
        Sem rolagem, sem distância, sem cobertura.
        Seleciona um ou mais alvos + região, aplica dano e efeitos.
        """
        import tkinter as tk
        from tkinter import ttk

        BG = "#1a1a2e"; FG = "white"

        popup = tk.Toplevel(self)
        popup.title(f"{item_ofensivo.nome}")
        popup.geometry("480x480")
        popup.configure(bg=BG)
        popup.resizable(False, False)

        # ── Banner ────────────────────────────────────────────────────────────────
        self._banner_poder(popup, item_ofensivo, BG)  # ✅ CORRETO: com self

        main = tk.Frame(popup, bg=BG)
        main.pack(fill="both", expand=True, padx=20, pady=8)

        def _row(lbl, factory):
            f = tk.Frame(main, bg=BG); f.pack(fill="x", pady=3)
            tk.Label(f, text=lbl, bg=BG, fg=FG, font=("Arial",10),
                    width=18, anchor="w").pack(side="left")
            w = factory(f); w.pack(side="right"); return w

        todos = self._get_alvos_unicos()
        nomes = [p.nome for p in todos]

        # ── Seleção de alvos (Listbox multi-select) ───────────────────────────────
        tk.Label(main, text="Alvos:", bg=BG, fg=FG, font=("Arial",10)).pack(anchor="w")

        frm_lb = tk.Frame(main, bg=BG); frm_lb.pack(fill="x", pady=2)
        lb = tk.Listbox(frm_lb, selectmode="multiple", bg="#0d0730", fg=FG,
                        font=("Arial",10), height=5, highlightthickness=0,
                        selectbackground="#5a3fbf", activestyle="none")
        for n in nomes: lb.insert("end", n)
        sb_lb = tk.Scrollbar(frm_lb, orient="vertical", command=lb.yview)
        lb.configure(yscrollcommand=sb_lb.set)
        lb.pack(side="left", fill="x", expand=True)
        sb_lb.pack(side="right", fill="y")

        # ── Região ────────────────────────────────────────────────────────────────
        regiao_var = tk.StringVar(value="aleatoria")
        _row("Região:", lambda f: ttk.Combobox(
            f, textvariable=regiao_var, state="readonly", width=24,
            values=["aleatoria","cabeça","rosto","pescoço","peito",
                    "costas","abdômen","braços","pernas"]))

        # ── Buff / Debuff Dano ────────────────────────────────────────────────────
        buff_dn_var   = tk.IntVar(value=0)
        debuff_dn_var = tk.IntVar(value=0)
        _row("Buff Dano:",   lambda f: tk.Entry(f, textvariable=buff_dn_var,
                                                width=8, font=("Arial",10), justify="center"))
        _row("Debuff Dano:", lambda f: tk.Entry(f, textvariable=debuff_dn_var,
                                                width=8, font=("Arial",10), justify="center"))

        # ── Resultado ─────────────────────────────────────────────────────────────
        res_label = tk.Label(main, text="", bg=BG, fg="lightgreen",
                            font=("Arial",9), wraplength=420)
        res_label.pack(pady=6)

        def _confirmar():
            indices = lb.curselection()
            if not indices:
                res_label.config(text="Selecione pelo menos um alvo.", fg="red"); return

            alvos_sel = [todos[i] for i in indices]

            res = CB.acerto_poder_habilidade(
                ph=item_ofensivo,
                usuario=char,
                alvos=alvos_sel,
                regiao=regiao_var.get(),
                BuffDano=buff_dn_var.get(),
                DebuffDano=debuff_dn_var.get(),
            )

            if not res.get("sucesso"):
                res_label.config(text=res.get("log", ["Erro"])[0], fg="red"); return

            res_label.config(text=" | ".join(res.get("log", [])), fg="lightgreen")

            detalhes = {"Poder/Habilidade": item_ofensivo.nome}
            for entrada in res.get("alvos", []):
                detalhes[entrada["alvo"]] = (
                    f"({entrada['regiao']}) "
                    f"Dano: {entrada['dano']} | Abs: {entrada['absorcao']}"
                    + (f" | Efeitos: {', '.join(entrada['efeitos'])}" if entrada["efeitos"] else "")
                )

            self.adicionar_log(
                f"🔮 {item_ofensivo.nome}: {char.nome} → "
                f"{', '.join(e['alvo'] for e in res.get('alvos', []))}",
                "lightgreen", detalhes=detalhes)
            self.refresh()
            popup.destroy()

        btn_f = tk.Frame(main, bg=BG); btn_f.pack(pady=8)
        tk.Button(btn_f, text="✅ Confirmar", command=_confirmar,
                bg="#38b000", fg=FG, font=("Arial",11), width=14).pack(side="left", padx=6)
        tk.Button(btn_f, text="Cancelar", command=popup.destroy,
                bg="#8B0000", fg=FG, font=("Arial",11), width=14).pack(side="left", padx=6)

    def _rotear_ofensivo(self, char, item_ofensivo):
        pode, erro = item_ofensivo.pode_usar(char)
        if not pode:
            self.adicionar_log(f"❌ {erro}", "red")
            return
        self._usar_hab_poder_ofensivo(char, item_ofensivo)

    def _banner_poder(self, popup, item_ofensivo, bg):
        """Cria um banner colorido com informações do poder no topo do popup."""
        import tkinter as tk
        banner = tk.Frame(popup, bg="#0a0433", height=44)
        banner.pack(fill="x"); banner.pack_propagate(False)
        tk.Label(banner, text=f"🔮 {item_ofensivo.nome}",
                font=("Arial", 13, "bold"), bg="#0a0433", fg="#b79cff").pack(
                    side="left", padx=10, pady=8)
        dano_txt = (", ".join(f"{d['valor']}({d['tipo'][:3]})"
                            for d in item_ofensivo.dano)
                    if item_ofensivo.dano else "sem dano direto")
        custos = []
        if getattr(item_ofensivo, "custo_energia", 0):
            custos.append(f"{item_ofensivo.custo_energia}E")
        if getattr(item_ofensivo, "custo_mana", 0):
            custos.append(f"{item_ofensivo.custo_mana}M")
        custo_txt = "+".join(custos) if custos else "grátis"
        
        # ✅ REMOVIDO: tipo_ataque não existe mais
        tk.Label(banner,
                text=f"Dano: {dano_txt}  |  Custo: {custo_txt}",
                bg="#0a0433", fg="#aaaaaa", font=("Arial", 8)).pack(
                    side="left", padx=6)

    def _aplicar_efeitos_ph_ui(self, item_ofensivo, alvo):
        """
        Aplica os efeitos do poder/habilidade ao alvo (helper para callbacks).
        Retorna lista de nomes dos efeitos aplicados.
        Importa BuffDebuff do escopo global (CB).
        """
        import random
        aplicados = []
        for ef in getattr(item_ofensivo, "efeitos", []):
            chance = ef.get("chance", 100)
            if random.randint(1, 100) <= chance:
                try:
                    bb = CB.BuffDebuff(
                        nome=ef.get("nome", "Efeito"),
                        duracao=ef.get("duracao", 1),
                        efeito=ef.get("efeito", []),
                        descricao=ef.get("descricao", ""),
                        tipo=ef.get("tipo", "debuff"),
                    )
                    alvo.buffs_debuffs.adicionar_efeito_objeto(bb)
                    aplicados.append(ef.get("nome", "Efeito"))
                except Exception:
                    pass
        return aplicados
    # ataques #

    def _popup_detalhes_hab_pod(self, char, item_obj, tipo_item):
        """Popup de detalhes para habilidades e poderes no card de combate."""
        pop = tk.Toplevel(self)
        pop.title(f"Detalhes — {item_obj.nome}")
        pop.configure(bg="#130f26")
        pop.geometry("420x360")
        pop.resizable(False, False)

        tk.Label(pop, text=item_obj.nome, bg="#0a0433", fg="#b79cff",
                font=("Arial", 15, "bold")).pack(fill="x", pady=10)

        frame = tk.Frame(pop, bg="#1a0869", bd=1, relief="flat")
        frame.pack(fill="both", expand=True, padx=12, pady=6)

        def linha(chave, valor, cor_val="white"):
            r = tk.Frame(frame, bg="#1a0869"); r.pack(fill="x", padx=8, pady=2)
            tk.Label(r, text=f"{chave}:", bg="#1a0869", fg="#8899cc",
                    font=("Arial", 10, "bold"), width=18, anchor="w").pack(side="left")
            tk.Label(r, text=str(valor), bg="#1a0869", fg=cor_val,
                    font=("Arial", 10), anchor="w", wraplength=220,
                    justify="left").pack(side="left")

        is_ofensivo = "ofensivo" in tipo_item

        if not is_ofensivo:
            tipo_label = "Passivo" if item_obj.custo == 0 else "Ativo"
            linha("Categoria", "Habilidade" if "hab" in tipo_item else "Poder")
            linha("Tipo", tipo_label)
            if item_obj.custo: linha("Custo", f"{item_obj.custo} Energia", "#0fbcd3")
            tags = item_obj.tags  if isinstance(item_obj.tags,  list) else [item_obj.tags]
            vals = item_obj.valor if isinstance(item_obj.valor, list) else [item_obj.valor] * len(tags)
            linha("Efeitos", "  |  ".join(f"{t}: {'+' if v>=0 else ''}{v}" for t, v in zip(tags, vals)))
            if item_obj.duracao: linha("Duração", f"{item_obj.duracao} turno(s)")
        else:
            linha("Categoria", "Habilidade Ofensiva" if "hab" in tipo_item else "Poder Ofensivo")
            linha("Tipo de Ataque", item_obj.tipo_ataque.upper())
            custos = []
            if getattr(item_obj, "custo_energia", 0): custos.append(f"{item_obj.custo_energia} Energia")
            if getattr(item_obj, "custo_mana",    0): custos.append(f"{item_obj.custo_mana} Mana")
            linha("Custo", ", ".join(custos) if custos else "Grátis", "#0fbcd3")
            if item_obj.dano:
                linha("Dano", "  |  ".join(f"{d['valor']} {d['tipo']}" for d in item_obj.dano), "#ff9966")
            if item_obj.raio:       linha("Raio",    f"{item_obj.raio}m")
            if item_obj.alcance_max: linha("Alcance", f"{item_obj.alcance_min}–{item_obj.alcance_max}m")
            if item_obj.efeitos:
                linha("Efeitos", ", ".join(e.get("nome", "?") for e in item_obj.efeitos), "#88eecc")
            if item_obj.ignora_resistencias: linha("Ignora Res.", "SIM", "#ff9999")

        linha("Descrição", item_obj.descricao or "—")

        tk.Button(pop, text="Fechar", command=pop.destroy,
                bg="#004080", fg="white", font=("Arial", 11)).pack(pady=10)

    def _gerar_texto_tooltip_item(self, item):
        linhas = [f"Nome: {getattr(item, 'nome', 'Desconhecido')}"]
        if hasattr(item,'descricao'): linhas.append(f"\n{item.descricao}")
        if hasattr(item,'dano'): linhas.append(f"\nDano: {item.dano}")
        if hasattr(item,'defesa'): linhas.append(f"\nDefesa: {item.defesa}")
        if hasattr(item,'peso'): linhas.append(f"\nPeso: {item.peso}")
        if hasattr(item,'regiao'): linhas.append(f"\nRegião: {item.regiao}")
        if hasattr(item,'Id'): linhas.append(f"\nID: {item.Id}")
        return "\n".join(linhas)
    
    # Funções do card #
    def _abrir_popup_rolagem_grupo(self):
        todos = []
        for chave in ("_lista_superior", "_lista_inferior"):
            todos += D.GruposDePersonagens.get(chave, [])
        todos = list({id(p): p for p in todos}.values())
        abrir_popup_rolagem_grupo(self, todos, log_callback=self.adicionar_log)

    def _get_alvos_unicos(self):
        """Retorna lista única de personagens sem duplicatas."""
        todos = self.get_all_personagens()
        unicos_dict = {id(p): p for p in todos}
        return list(unicos_dict.values())

    def _ir_para_mapa(self):
        """Navega para a tela de mapa (Frame próprio), preservando estado."""
        self.controller.abrir_mapa(
            grupos=D.GruposDePersonagens if hasattr(D, "GruposDePersonagens") else {},
            estado_salvo=self._estado_mapa,
            callback_estado=self._receber_estado_mapa,
        )

    def _receber_estado_mapa(self, novo_estado: dict):
        """Chamado pela tela do mapa ao sair, para salvar o estado aqui."""
        self._estado_mapa = novo_estado
        # Também atualiza distâncias e coberturas usadas no card/listas
        self.distancias_mapa = novo_estado.get("distancias_calculadas", {})

    def refresh(self):
        """Atualiza as listas de personagens e o card do turno atual"""
        # Atualizar card do turno atual
        self.atualizar_card_turno_atual()
        
        # Atualizar listas direita - SEM atualizar combobox
        if hasattr(self, 'frame_lista_direita_1'):
            self.frame_lista_direita_1.destroy()
            self.frame_lista_direita_1 = self.create_simple_list(self.grupo_lista_superior, x=1185, y=100, height=300)
        
        if hasattr(self, 'frame_lista_direita_2'):
            self.frame_lista_direita_2.destroy()
            self.frame_lista_direita_2 = self.create_simple_list(self.grupo_lista_inferior, x=1185, y=410, height=300)

    def TelaInicial(self):
        self.controller.TelaInicial()

    def TelaDeSelecao(self):
        self.controller.TelaDeSelecao()
    
    def TelaDeRegrasEItens(self):
        self.controller.TelaDeRegrasEItens()
### TELA DE COMBATE ###
### TELA DE COMBATE ###
### TELA DE COMBATE ###

### MAPA DE COMBATE ###
### MAPA DE COMBATE ###
### MAPA DE COMBATE ###
# CLASSE TOKEN
class Token:
    def __init__(self, personagem, wx, wy, grupo="default"):
        self.personagem = personagem
        self.wx    = wx
        self.wy    = wy
        self.grupo = grupo
        self.cobertura = getattr(personagem, "cobertura_mapa", "Nenhuma")
        self.material  = getattr(personagem, "material_mapa",   "Nenhum")

    def tela(self, ox, oy, zoom):
        return self.wx * zoom + ox, self.wy * zoom + oy

    def salvar_cobertura(self):
        self.personagem.cobertura_mapa = self.cobertura
        self.personagem.material_mapa  = self.material

def _popup_selecionar_epicentro(parent_popup, estado_mapa: dict,
                                item_consumivel, raio_letal: float,
                                callback):
    import math

    tokens_dados     = estado_mapa.get("tokens_dados", [])
    escala_m_px      = estado_mapa.get("escala_m_por_px", 0.05)
    img_original     = estado_mapa.get("img_original", None)

    # ── Extrai raio/raio_letal independente do formato ────────────────────
    # Novo formato: pega do primeiro efeito dano_area
    raio = 0
    for ef in getattr(item_consumivel, "efeitos", []):
        if isinstance(ef, dict) and ef.get("tipo") == "dano_area":
            raio = ef.get("raio", 0) or 0
            # raio_letal pode ter sido passado como argumento; se for 0, recalcula
            if not raio_letal:
                raio_letal = ef.get("raio_letal") or round(raio * 0.3, 1)
            break

    # Formato antigo: fallback para atributo direto
    if not raio:
        raio = getattr(item_consumivel, "raio", 0) or 0
    if not raio_letal:
        raio_letal = getattr(item_consumivel, "raio_letal", None) or round(raio * 0.3, 1)

    # Garante que nunca chegue None nas contas
    raio       = raio       or 0
    raio_letal = raio_letal or 0

    # ── view state ────────────────────────────────────────────────────────
    view = {
        "zoom":     1.0,
        "ox":       40,
        "oy":       40,
        "pan":      False,
        "pan_sx":   0,
        "pan_sy":   0,
        "epi_wx":   None,
        "epi_wy":   None,
        "alvos":    [],
        "cursor_x": None,
        "cursor_y": None,
        "img_tk":   None,
    }
    ESCALA_BASE = 2.0

    pop = tk.Toplevel(parent_popup)
    pop.title(f"Escolher Epicentro — {item_consumivel.nome}")
    pop.configure(bg="#1a1430")
    pop.geometry("980x700")
    pop.resizable(True, True)
    pop.grab_set()

    tk.Label(pop,
             text=(f"Clique para epicentro  |  Raio: {raio}m  "
                   f"(vermelho = zona letal {raio_letal}m)  |  "
                   "Scroll: zoom  •  Botão do meio: pan"),
             bg="#1a1430", fg="#aaaaaa", font=("Arial", 9)).pack(pady=(6, 2))

    canvas = tk.Canvas(pop, bg="#1a1430", highlightthickness=0, cursor="crosshair")
    canvas.pack(fill="both", expand=True, padx=8, pady=(0, 4))

    lbl_info = tk.Label(pop, text="Nenhum epicentro definido",
                        bg="#1a1430", fg="#aaaaaa", font=("Arial", 9))
    lbl_info.pack(pady=(0, 4))

    # ── helpers de coordenadas ────────────────────────────────────────────
    def world_to_screen(wx, wy):
        z = view["zoom"] * ESCALA_BASE
        return view["ox"] + wx * z, view["oy"] + wy * z

    def screen_to_world(sx, sy):
        z = view["zoom"] * ESCALA_BASE
        return (sx - view["ox"]) / z, (sy - view["oy"]) / z

    def raio_em_tela(metros):
        if not metros:
            return 0
        return metros / escala_m_px * view["zoom"] * ESCALA_BASE

    # ── redesenho ─────────────────────────────────────────────────────────
    def _redesenhar():
        canvas.delete("all")
        w = canvas.winfo_width()  or 960
        h = canvas.winfo_height() or 640

        if img_original and PIL_DISPONIVEL:
            try:
                z = view["zoom"] * ESCALA_BASE
                nw = max(1, int(img_original.width  * z))
                nh = max(1, int(img_original.height * z))
                img_r = img_original.resize((nw, nh), Image.LANCZOS)
                view["img_tk"] = ImageTk.PhotoImage(img_r)
                canvas.create_image(view["ox"], view["oy"],
                                    anchor="nw", image=view["img_tk"])
            except Exception:
                pass
        else:
            canvas.create_rectangle(0, 0, w, h, fill="#1a1430", outline="")

        cx = cy = None
        if view["cursor_x"] is not None:
            cx, cy = view["cursor_x"], view["cursor_y"]
        elif view["epi_wx"] is not None:
            cx, cy = world_to_screen(view["epi_wx"], view["epi_wy"])

        rv  = raio_em_tela(raio)        # usa variável local, nunca None
        rlv = raio_em_tela(raio_letal)

        if cx is not None:
            canvas.create_oval(cx-rv,  cy-rv,  cx+rv,  cy+rv,
                               outline="#ffaa00", width=2,
                               fill="#ffaa00", stipple="gray12")
            canvas.create_oval(cx-rlv, cy-rlv, cx+rlv, cy+rlv,
                               outline="#ff3333", width=2,
                               fill="#ff3333", stipple="gray25",
                               dash=(5, 4))
            canvas.create_line(cx-14, cy, cx+14, cy, fill="#ffffff", width=1)
            canvas.create_line(cx, cy-14, cx, cy+14, fill="#ffffff", width=1)

        for td in tokens_dados:
            tx, ty = world_to_screen(td["wx"], td["wy"])
            r = max(10, int(14 * view["zoom"]))

            cor_borda = "#7b3fe4"
            if cx is not None:
                dist_px = math.hypot(tx - cx, ty - cy)
                dist_m  = dist_px / (view["zoom"] * ESCALA_BASE) * escala_m_px
                if dist_m <= raio_letal:
                    cor_borda = "#ff3333"
                elif dist_m <= raio:          # usa variável local
                    cor_borda = "#ffaa00"
                else:
                    cor_borda = "#444466"

            canvas.create_oval(tx-r, ty-r, tx+r, ty+r,
                               fill="#2a0d89", outline=cor_borda, width=2)
            fs = max(7, int(r * 0.65))
            canvas.create_text(tx, ty,
                               text=td["personagem_nome"][0].upper(),
                               fill="white", font=("Consolas", fs, "bold"))
            canvas.create_text(tx, ty + r + 6,
                               text=td["personagem_nome"],
                               fill="#cccccc", font=("Consolas", 7), anchor="n")

    # ── eventos de mouse ──────────────────────────────────────────────────
    def _on_motion(e):
        view["cursor_x"] = e.x
        view["cursor_y"] = e.y
        _redesenhar()

    def _on_leave(e):
        view["cursor_x"] = None
        view["cursor_y"] = None
        _redesenhar()

    def _on_click(e):
        wx, wy = screen_to_world(e.x, e.y)
        view["epi_wx"] = wx
        view["epi_wy"] = wy

        alvos = []
        todos_pers = {}
        for lista in D.GruposDePersonagens.values():
            for p in lista:
                todos_pers[p.nome] = p

        for td in tokens_dados:
            p = todos_pers.get(td["personagem_nome"])
            if p is None:
                continue
            dist_px = math.hypot(td["wx"] - wx, td["wy"] - wy)
            dist_m  = dist_px * escala_m_px
            if dist_m <= raio:              # usa variável local
                alvos.append((p, dist_m, td.get("cobertura", "Nenhuma")))

        view["alvos"]    = alvos
        view["cursor_x"] = None
        view["cursor_y"] = None
        _redesenhar()

        lbl_info.config(
            text=(f"Epicentro: ({wx:.1f}, {wy:.1f})  |  "
                  f"{len(alvos)} alvo(s) no raio  —  clique CONFIRMAR para importar"),
            fg="#90caf9")

    # ── pan ───────────────────────────────────────────────────────────────
    def _pan_start(e):
        view["pan"]    = True
        view["pan_sx"] = e.x
        view["pan_sy"] = e.y
        canvas.config(cursor="fleur")

    def _pan_move(e):
        if not view["pan"]:
            return
        view["ox"] += e.x - view["pan_sx"]
        view["oy"] += e.y - view["pan_sy"]
        view["pan_sx"] = e.x
        view["pan_sy"] = e.y
        _redesenhar()

    def _pan_end(e):
        view["pan"] = False
        canvas.config(cursor="crosshair")

    # ── zoom ──────────────────────────────────────────────────────────────
    def _on_scroll(e):
        fator = 1.15 if e.delta > 0 else 1 / 1.15
        novo  = max(0.1, min(8.0, view["zoom"] * fator))
        mx, my = e.x, e.y
        view["ox"] = mx - (mx - view["ox"]) * (novo / view["zoom"])
        view["oy"] = my - (my - view["oy"]) * (novo / view["zoom"])
        view["zoom"] = novo
        _redesenhar()

    canvas.bind("<Motion>",           _on_motion)
    canvas.bind("<Leave>",            _on_leave)
    canvas.bind("<Button-1>",         _on_click)
    canvas.bind("<ButtonPress-2>",    _pan_start)
    canvas.bind("<B2-Motion>",        _pan_move)
    canvas.bind("<ButtonRelease-2>",  _pan_end)
    canvas.bind("<MouseWheel>",       _on_scroll)
    canvas.bind("<Button-4>",  lambda e: _on_scroll(type("E", (), {"delta":1,  "x":e.x,"y":e.y})()))
    canvas.bind("<Button-5>",  lambda e: _on_scroll(type("E", (), {"delta":-1, "x":e.x,"y":e.y})()))
    canvas.bind("<Configure>", lambda e: _redesenhar())

    # ── botões ────────────────────────────────────────────────────────────
    rod = tk.Frame(pop, bg="#1a1430")
    rod.pack(fill="x", padx=10, pady=6)

    def _confirmar():
        if view["epi_wx"] is None:
            tk.messagebox.showwarning("Sem epicentro",
                                      "Clique no mapa para definir o epicentro.",
                                      parent=pop)
            return
        pop.destroy()
        callback(view["epi_wx"], view["epi_wy"], view["alvos"])

    tk.Button(rod, text="✓ Confirmar e importar alvos",
              command=_confirmar,
              bg="#38b000", fg="white", font=("Arial", 11, "bold"),
              padx=14).pack(side="left", padx=6)

    tk.Button(rod, text="Cancelar", command=pop.destroy,
              bg="#8B0000", fg="white", font=("Arial", 10)).pack(side="right", padx=6)

    pop.after(80, _redesenhar)

# POPUP PRINCIPAL #
class MapaCombateScreen(tk.Frame):
    """
    Tela própria do mapa de combate.
    Substitui o Toplevel; é gerenciada pela controller como qualquer outra tela.

    A controller deve:
      1. Instanciar uma vez e guardar em self._mapa_screen.
      2. Chamar show(grupos, estado_salvo, callback_estado) para exibir.
      3. Ao voltar, chamar a callback com o estado atual.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(bg=COR_BG)
        self.controller      = controller
        self._callback_estado = None
        self._grupos          = {}

        # ── estado persistido entre visitas ──────────────────────────────────
        self.zoom            = 0.5
        self.zoom_min        = 0.15
        self.zoom_max        = 5.0
        self.offset_x        = 0
        self.offset_y        = 0
        self._pan_ativo      = False
        self._pan_ox         = 0
        self._pan_oy         = 0
        self.img_original    = None
        self.img_tk          = None
        self.tokens: list    = []          # lista de Token
        self.token_focado    = None
        self.token_em_mov    = None
        self.escala_m_por_px = 0.05
        self.mostrar_grade   = False
        self.tamanho_grade   = 50
        self.raio_token      = RAIO_TOKEN
        self.distancias: dict = {}

        self._construir_ui()

    # ── API pública ──────────────────────────────────────────────────────────
    def show(self, grupos: dict, estado_salvo: dict, callback_estado):
        """Chamado pela controller ao navegar para cá."""
        self._grupos          = grupos
        self._callback_estado = callback_estado
        self._restaurar_estado(estado_salvo)
        self._atualizar_lista_lateral()
        self.after(80, self._redesenhar)

    def _voltar(self):
        estado = self._coletar_estado()
        if self._callback_estado:
            self._callback_estado(estado)
        self.controller.TelaDeCombate()   # ajuste ao nome real do método na controller

    # ── CONSTRUÇÃO DA UI ────────────────────────────────────────────────────
    def _construir_ui(self):
        self._construir_toolbar()
        area = tk.Frame(self, bg=COR_BG)
        area.pack(fill="both", expand=True, padx=6, pady=(0, 6))
        self._construir_canvas(area)
        self._construir_painel_lateral(area)
        self._construir_statusbar()

    def _construir_toolbar(self):
        tb = tk.Frame(self, bg=COR_ACENTO, height=46)
        tb.pack(fill="x")
        tb.pack_propagate(False)

        # botão VOLTAR (destaque)
        tk.Button(tb, text="← Voltar ao Combate",
                  command=self._voltar,
                  bg="#4a0030", fg="white",
                  font=("Consolas", 10, "bold"),
                  relief="flat", cursor="hand2",
                  activebackground="#7a0050", padx=12
                  ).pack(side="left", padx=(6, 12), pady=6)

        tk.Frame(tb, bg="#5a2acc", width=2).pack(
            side="left", fill="y", pady=8, padx=4)

        def _btn(text, cmd, cor=COR_ACENTO2):
            b = tk.Button(tb, text=text, command=cmd, bg=cor, fg=COR_TEXTO,
                          font=("Consolas", 10, "bold"), relief="flat",
                          cursor="hand2", activebackground="#6a2acc",
                          activeforeground="white", padx=10)
            b.pack(side="left", padx=3, pady=6)
            return b

        def _sep():
            tk.Frame(tb, bg="#5a2acc", width=2).pack(
                side="left", fill="y", pady=8, padx=4)

        _btn("📂 Carregar Mapa", self._carregar_mapa)
        _btn("🗑 Remover Mapa",  self._remover_mapa)
        _sep()
        _btn("🔍+",     lambda: self._aplicar_zoom(1.2))
        _btn("🔍−",     lambda: self._aplicar_zoom(1/1.2))
        _btn("⌂ Reset", self._reset_view)
        _sep()
        self.btn_grade = tk.Button(
            tb, text="⊞ Grade OFF",
            command=self._toggle_grade,
            bg=COR_ACENTO, fg=COR_TEXTO_DIM,
            font=("Consolas", 10, "bold"), relief="flat",
            cursor="hand2", activebackground=COR_ACENTO2, padx=10)
        self.btn_grade.pack(side="left", padx=3, pady=6)
        _sep()
        _btn("✕ Limpar Seleção", self._limpar_selecao)
        _sep()
        tk.Label(tb, text="Token:", bg=COR_ACENTO, fg=COR_TEXTO_DIM,
                 font=("Consolas", 9)).pack(side="left", padx=(4, 0))
        _btn("▲", self._token_maior)
        _btn("▼", self._token_menor)

        tk.Frame(tb, bg="#5a2acc", width=2).pack(
            side="right", fill="y", pady=8, padx=4)
        tk.Label(tb, text="m/px:", bg=COR_ACENTO, fg=COR_TEXTO_DIM,
                 font=("Consolas", 10)).pack(side="right", padx=(0, 4))
        self.entry_escala = tk.Entry(
            tb, width=6, font=("Consolas", 10),
            bg="#1a0f35", fg=COR_TEXTO,
            insertbackground=COR_TEXTO, relief="flat", justify="center")
        self.entry_escala.insert(0, str(self.escala_m_por_px))
        self.entry_escala.pack(side="right", padx=3, pady=8)
        self.entry_escala.bind("<Return>",   self._atualizar_escala)
        self.entry_escala.bind("<FocusOut>", self._atualizar_escala)

    def _construir_canvas(self, parent):
        wrap = tk.Frame(parent, bg=COR_BG)
        wrap.pack(side="left", fill="both", expand=True)

        self.canvas = tk.Canvas(wrap, bg="#1a1430",
                                highlightthickness=0, cursor="crosshair")
        sx = tk.Scrollbar(wrap, orient="horizontal", command=self.canvas.xview)
        sy = tk.Scrollbar(wrap, orient="vertical",   command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=sx.set, yscrollcommand=sy.set)
        sy.pack(side="right",  fill="y")
        sx.pack(side="bottom", fill="x")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<ButtonPress-2>",   self._pan_start)
        self.canvas.bind("<B2-Motion>",       self._pan_move)
        self.canvas.bind("<ButtonRelease-2>", self._pan_end)
        self.canvas.bind("<MouseWheel>",      self._on_scroll)
        self.canvas.bind("<Button-4>",  lambda e: self._aplicar_zoom(1.15, e))
        self.canvas.bind("<Button-5>",  lambda e: self._aplicar_zoom(1/1.15, e))
        self.canvas.bind("<Configure>", self._on_resize)
        self.canvas.bind("<ButtonPress-1>", self._canvas_clique_esq)
        self.canvas.bind("<ButtonPress-3>", self._canvas_clique_dir)
        self.canvas.bind("<Motion>",        self._on_mouse_move)

    def _construir_painel_lateral(self, parent):
        self.painel = tk.Frame(parent, bg=COR_PAINEL, width=280)
        self.painel.pack(side="right", fill="y", padx=(6, 0))
        self.painel.pack_propagate(False)

        tk.Label(self.painel, text="PERSONAGENS", bg=COR_PAINEL,
                 fg=COR_TEXTO_DIM, font=("Consolas", 9, "bold")).pack(pady=(10, 2))

        fl = tk.Frame(self.painel, bg=COR_PAINEL)
        fl.pack(fill="both", expand=True, padx=6)
        self.canvas_lista = tk.Canvas(fl, bg=COR_PAINEL, highlightthickness=0)
        sb = tk.Scrollbar(fl, orient="vertical", command=self.canvas_lista.yview)
        self.canvas_lista.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.canvas_lista.pack(side="left", fill="both", expand=True)
        self.frame_lista_inner = tk.Frame(self.canvas_lista, bg=COR_PAINEL)
        self.canvas_lista.create_window(
            (0, 0), window=self.frame_lista_inner, anchor="nw")
        self.frame_lista_inner.bind("<Configure>",
            lambda e: self.canvas_lista.configure(
                scrollregion=self.canvas_lista.bbox("all")))

        tk.Frame(self.painel, bg=COR_BORDA, height=1).pack(fill="x", padx=6, pady=4)
        tk.Label(self.painel, text="DISTÂNCIAS", bg=COR_PAINEL,
                 fg=COR_TEXTO_DIM, font=("Consolas", 9, "bold")).pack()
        self.lbl_token_focado = tk.Label(
            self.painel, text="Clique esq. em um token →",
            bg=COR_PAINEL, fg=COR_TEXTO_DIM, font=("Consolas", 8, "italic"))
        self.lbl_token_focado.pack(pady=(2, 4))

        fd = tk.Frame(self.painel, bg=COR_PAINEL, height=150)
        fd.pack(fill="x", padx=6, pady=(0, 4))
        fd.pack_propagate(False)
        self.canvas_dist = tk.Canvas(fd, bg=COR_PAINEL, highlightthickness=0)
        sb2 = tk.Scrollbar(fd, orient="vertical", command=self.canvas_dist.yview)
        self.canvas_dist.configure(yscrollcommand=sb2.set)
        sb2.pack(side="right", fill="y")
        self.canvas_dist.pack(side="left", fill="both", expand=True)
        self.frame_dist_inner = tk.Frame(self.canvas_dist, bg=COR_PAINEL)
        self.canvas_dist.create_window(
            (0, 0), window=self.frame_dist_inner, anchor="nw")
        self.frame_dist_inner.bind("<Configure>",
            lambda e: self.canvas_dist.configure(
                scrollregion=self.canvas_dist.bbox("all")))

    def _construir_statusbar(self):
        sb = tk.Frame(self, bg="#0a0818", height=24)
        sb.pack(fill="x", side="bottom")
        sb.pack_propagate(False)
        self.lbl_status = tk.Label(
            sb,
            text="Esq: selecionar/distâncias  •  Dir: mover token  •  Meio: pan  •  Scroll: zoom  •  ← Voltar para salvar",
            bg="#0a0818", fg=COR_TEXTO_DIM, font=("Consolas", 8))
        self.lbl_status.pack(side="left", padx=8)
        self.lbl_cursor = tk.Label(sb, text="", bg="#0a0818",
                                   fg=COR_TEXTO_DIM, font=("Consolas", 8))
        self.lbl_cursor.pack(side="right", padx=8)

    # ── ESTADO ──────────────────────────────────────────────────────────────
    def _restaurar_estado(self, estado: dict):
        if not estado:
            return
        self.zoom            = estado.get("zoom",            self.zoom)
        self.offset_x        = estado.get("offset_x",        self.offset_x)
        self.offset_y        = estado.get("offset_y",        self.offset_y)
        self.escala_m_por_px = estado.get("escala_m_por_px", self.escala_m_por_px)
        self.mostrar_grade   = estado.get("mostrar_grade",   self.mostrar_grade)
        self.raio_token      = estado.get("raio_token",      self.raio_token)
        self.img_original    = estado.get("img_original",    self.img_original)
        self.entry_escala.delete(0, "end")
        self.entry_escala.insert(0, str(self.escala_m_por_px))
        self.btn_grade.config(
            text="⊞ Grade ON"  if self.mostrar_grade else "⊞ Grade OFF",
            fg=COR_TEXTO       if self.mostrar_grade else COR_TEXTO_DIM)

        # reconstruir tokens a partir dos dados salvos
        self.tokens.clear()
        self.token_focado = None
        self.token_em_mov = None
        todos_pers = {}
        for personagens in self._grupos.values():
            for p in personagens:
                todos_pers[p.nome] = p

        for td in estado.get("tokens_dados", []):
            p = todos_pers.get(td["personagem_nome"])
            if p is None:
                continue
            t = Token(p, td["wx"], td["wy"], td["grupo"])
            t.cobertura = td["cobertura"]
            t.material  = td.get("material", "Nenhum")
            t.salvar_cobertura()
            self.tokens.append(t)

        self._atualizar_distancias()

    def _coletar_estado(self) -> dict:
        tokens_dados = []
        for t in self.tokens:
            tokens_dados.append({
                "personagem_nome": t.personagem.nome,
                "grupo":           t.grupo,
                "wx":              t.wx,
                "wy":              t.wy,
                "cobertura":       t.cobertura,
                "material":        t.material,
            })
        return {
            "zoom":              self.zoom,
            "offset_x":         self.offset_x,
            "offset_y":         self.offset_y,
            "escala_m_por_px":  self.escala_m_por_px,
            "mostrar_grade":    self.mostrar_grade,
            "raio_token":       self.raio_token,
            "img_original":     self.img_original,
            "tokens_dados":     tokens_dados,
            "distancias_calculadas": dict(self.distancias),
        }

    # ── ZOOM / PAN (idêntico ao original) ───────────────────────────────────
    def _aplicar_zoom(self, fator, event=None):
        novo = max(self.zoom_min, min(self.zoom_max, self.zoom * fator))
        if novo == self.zoom: return
        if event:
            mx = self.canvas.canvasx(event.x)
            my = self.canvas.canvasy(event.y)
            self.offset_x = mx - (mx - self.offset_x) * (novo / self.zoom)
            self.offset_y = my - (my - self.offset_y) * (novo / self.zoom)
        else:
            w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
            self.offset_x = w/2 - (w/2 - self.offset_x) * (novo / self.zoom)
            self.offset_y = h/2 - (h/2 - self.offset_y) * (novo / self.zoom)
        self.zoom = novo
        self._redesenhar()

    def _on_scroll(self, e):
        self._aplicar_zoom(1.15 if e.delta > 0 else 1/1.15, e)

    def _pan_start(self, e):
        self._pan_ativo = True; self._pan_ox = e.x; self._pan_oy = e.y
        self.canvas.config(cursor="fleur")

    def _pan_move(self, e):
        if not self._pan_ativo: return
        self.offset_x += e.x - self._pan_ox; self._pan_ox = e.x
        self.offset_y += e.y - self._pan_oy; self._pan_oy = e.y
        self._redesenhar()

    def _pan_end(self, e):
        self._pan_ativo = False; self.canvas.config(cursor="crosshair")

    def _on_resize(self, e): self._redesenhar()

    # ── REDESENHO (idêntico ao original) ────────────────────────────────────
    def _redesenhar(self):
        self.canvas.delete("all")
        self._desenhar_fundo()
        if self.mostrar_grade: self._desenhar_grade()
        if self.token_focado and self.token_focado in self.tokens:
            self._desenhar_linhas_distancia()
        for t in self.tokens:
            self._desenhar_token(t)

    def _desenhar_fundo(self):
        if self.img_original and PIL_DISPONIVEL:
            nw = max(1, int(self.img_original.width  * self.zoom))
            nh = max(1, int(self.img_original.height * self.zoom))
            try:   img = self.img_original.resize((nw, nh), Image.LANCZOS)
            except: img = self.img_original.resize((nw, nh))
            self.img_tk = ImageTk.PhotoImage(img)
            self.canvas.create_image(self.offset_x, self.offset_y,
                                     anchor="nw", image=self.img_tk)
        else:
            w = self.canvas.winfo_width(); h = self.canvas.winfo_height()
            self.canvas.create_rectangle(0, 0, w, h, fill="#1a1430", outline="")
            step = max(20, int(40 * self.zoom)); ox = int(self.offset_x % step)
            oy   = int(self.offset_y % step)
            for x in range(ox, w+step, step):
                for y in range(oy, h+step, step):
                    self.canvas.create_oval(x-1, y-1, x+1, y+1,
                                            fill="#2a1f4a", outline="")

    def _desenhar_grade(self):
        w = self.canvas.winfo_width(); h = self.canvas.winfo_height()
        gs = int(self.tamanho_grade * self.zoom)
        if gs < 8: return
        ox = int(self.offset_x % gs); oy = int(self.offset_y % gs)
        for x in range(ox, w+gs, gs):
            self.canvas.create_line(x, 0, x, h, fill="#2a1f4a", width=1)
        for y in range(oy, h+gs, gs):
            self.canvas.create_line(0, y, w, y, fill="#2a1f4a", width=1)

    def _desenhar_linhas_distancia(self):
        tf = self.token_focado
        x1, y1 = tf.tela(self.offset_x, self.offset_y, self.zoom)
        for other in self.tokens:
            if other is tf: continue
            x2, y2 = other.tela(self.offset_x, self.offset_y, self.zoom)
            dm = self._dist_metros(tf, other)
            self.canvas.create_line(x1,y1,x2,y2, fill="#2244aa",width=1,dash=(6,4))
            mx, my = (x1+x2)/2, (y1+y2)/2
            self.canvas.create_rectangle(mx-28,my-10,mx+28,my+10,
                                         fill="#001020",outline="#2244aa")
            self.canvas.create_text(mx, my, text=f"{dm:.1f} m",
                                    fill=COR_LINHA_DIST,
                                    font=("Consolas", 8, "bold"))

    def _desenhar_token(self, token):
        cx, cy = token.tela(self.offset_x, self.offset_y, self.zoom)
        r = self.raio_token
        cor_g     = CORES_GRUPO.get(token.grupo, CORES_GRUPO["default"])
        eh_foc    = token is self.token_focado
        eh_mov    = token is self.token_em_mov
        cor_borda = (COR_LINHA_MOV   if eh_mov  else
                     COR_SELECIONADO if eh_foc  else cor_g)
        esp       = 4 if eh_mov else (3 if eh_foc else 2)
        tag       = f"tok_{id(token)}"

        self.canvas.create_oval(cx-r+3,cy-r+3,cx+r+3,cy+r+3,
                                fill="#000000",outline="",stipple="gray50",
                                tags=("token_sombra", tag))
        self.canvas.create_oval(cx-r,cy-r,cx+r,cy+r,
                                fill="#1a0f35",outline=cor_borda,width=esp,
                                tags=("token", tag))
        if eh_foc or eh_mov:
            self.canvas.create_oval(cx-r-6,cy-r-6,cx+r+6,cy+r+6,
                                    fill="",outline=COR_LINHA_MOV if eh_mov else COR_SELECIONADO,
                                    width=1,dash=(4,4),tags=(tag,))
        cor_cob = CORES_COBERTURA.get(token.cobertura)
        if cor_cob:
            self.canvas.create_arc(cx-r,cy-r,cx+r,cy+r,
                                   start=45,extent=90,
                                   outline=cor_cob,width=4,
                                   style="arc",tags=(tag,))
        fs = max(8, int(r*0.65))
        if token.material and token.material != "Nenhum":
            self.canvas.create_text(
                cx, cy - r - 8,
                text=token.material,
                fill="#88ccff",
                font=("Consolas", 7),
                anchor="s",
                tags=(tag,))
        self.canvas.create_text(cx,cy,
                                text=token.personagem.nome[0].upper(),
                                fill=cor_g,font=("Consolas",fs,"bold"),
                                tags=(tag,))
        self.canvas.create_text(cx,cy+r+10,
                                text=token.personagem.nome,
                                fill=COR_TEXTO,font=FONTE_NOME,anchor="n",
                                tags=(tag,))
        bw,bh = r*2,4; bx,by = cx-r,cy+r+22
        prop = token.personagem.VidaAtual / max(1, token.personagem.VidaMax)
        cor_v = "#00cc44" if prop>.5 else "#ffcc00" if prop>.25 else "#ff3333"
        self.canvas.create_rectangle(bx,by,bx+bw,by+bh,fill="#111111",outline="")
        self.canvas.create_rectangle(bx,by,bx+int(bw*prop),by+bh,
                                     fill=cor_v,outline="")

        self.canvas.tag_bind(tag,"<ButtonPress-1>",
                             lambda e,t=token: self._token_clique_esq(e,t))
        self.canvas.tag_bind(tag,"<ButtonPress-3>",
                             lambda e,t=token: self._token_clique_dir(e,t))
        self.canvas.tag_bind(tag,"<Enter>",
                             lambda e,t=token: self._token_hover(e,t,True))
        self.canvas.tag_bind(tag,"<Leave>",
                             lambda e,t=token: self._token_hover(e,t,False))

    # ── CLIQUES ─────────────────────────────────────────────────────────────
    def _canvas_clique_esq(self, e):
        items = self.canvas.find_overlapping(e.x-4,e.y-4,e.x+4,e.y+4)
        if any("token" in (self.canvas.gettags(i) or ()) for i in items): return
        self._limpar_selecao()

    def _canvas_clique_dir(self, e):
        items = self.canvas.find_overlapping(e.x-4,e.y-4,e.x+4,e.y+4)
        if any("token" in (self.canvas.gettags(i) or ()) for i in items): return
        if self.token_em_mov:
            wx = (e.x - self.offset_x) / self.zoom
            wy = (e.y - self.offset_y) / self.zoom
            self.token_em_mov.wx = wx
            self.token_em_mov.wy = wy
            nome = self.token_em_mov.personagem.nome
            self.token_em_mov = None
            self.canvas.config(cursor="crosshair")
            self.lbl_status.config(text=f"{nome} movido!")
            self._atualizar_distancias()
            if self.token_focado: self._atualizar_painel_distancias()
            self._redesenhar(); self._atualizar_lista_lateral()

    def _token_clique_esq(self, e, token):
        if self.token_focado is token:
            self.token_focado = None
            self.lbl_token_focado.config(text="Clique esq. em um token →")
            self._limpar_painel_distancias()
        else:
            self.token_focado = token
            self.lbl_token_focado.config(text=f"► {token.personagem.nome}")
            self._atualizar_painel_distancias()
        self.after(0, self._redesenhar)
        self.after(0, self._atualizar_lista_lateral)
        return "break"

    def _token_clique_dir(self, e, token):
        if self.token_em_mov is token:
            self.token_em_mov = None
            self.canvas.config(cursor="crosshair")
            self.lbl_status.config(
                text="Esq: selecionar  •  Dir: mover  •  Meio: pan  •  Scroll: zoom")
        else:
            self.token_em_mov = token
            self.lbl_status.config(
                text=f"▶ {token.personagem.nome} — clique DIR no destino  •  Dir no token: cancelar")
        self.after(0, self._redesenhar)
        self.after(0, self._atualizar_lista_lateral)
        return "break"

    def _token_hover(self, e, token, entrando):
        if entrando:
            pv  = f"PV {token.personagem.VidaAtual}/{token.personagem.VidaMax}"
            cob = f"Cob: {token.cobertura}"
            self.lbl_status.config(
                text=f"{token.personagem.nome}  •  {pv}  •  {cob}")
        else:
            self.lbl_status.config(
                text="Esq: selecionar/distâncias  •  Dir: mover  •  Meio: pan  •  Scroll: zoom")

    def _limpar_selecao(self):
        self.token_focado = None; self.token_em_mov = None
        self.canvas.config(cursor="crosshair")
        self.lbl_token_focado.config(text="Clique esq. em um token →")
        self._limpar_painel_distancias()
        self.lbl_status.config(
            text="Esq: selecionar/distâncias  •  Dir: mover  •  Meio: pan  •  Scroll: zoom")
        self._redesenhar(); self._atualizar_lista_lateral()

    # ── PAINEL DISTÂNCIAS ────────────────────────────────────────────────────
    def _limpar_painel_distancias(self):
        for w in self.frame_dist_inner.winfo_children(): w.destroy()

    def _atualizar_painel_distancias(self):
        self._limpar_painel_distancias()
        tf = self.token_focado
        if not tf or tf not in self.tokens: return
        outros = sorted([(t, self._dist_metros(tf,t))
                         for t in self.tokens if t is not tf], key=lambda x:x[1])
        for other, dm in outros:
            cor_g = CORES_GRUPO.get(other.grupo, CORES_GRUPO["default"])
            row = tk.Frame(self.frame_dist_inner, bg=COR_PAINEL)
            row.pack(fill="x", pady=1, padx=4)
            cv = tk.Canvas(row, width=10, height=10,
                           bg=COR_PAINEL, highlightthickness=0)
            cv.create_oval(1,1,9,9,fill=cor_g,outline="")
            cv.pack(side="left",padx=(2,4))
            tk.Label(row, text=other.personagem.nome, bg=COR_PAINEL,
                     fg=COR_TEXTO, font=("Consolas",9),
                     anchor="w", width=11).pack(side="left")
            cor_d = "#ff4444" if dm<=2 else "#ffaa00" if dm<=10 else COR_LINHA_DIST
            tk.Label(row, text=f"{dm:.1f} m", bg=COR_PAINEL,
                     fg=cor_d, font=("Consolas",9,"bold")).pack(side="right",padx=4)

    # ── LISTA LATERAL ────────────────────────────────────────────────────────
    def _atualizar_lista_lateral(self):
        for w in self.frame_lista_inner.winfo_children(): w.destroy()

        for token in self.tokens:
            cor_g  = CORES_GRUPO.get(token.grupo, CORES_GRUPO["default"])
            eh_foc = token is self.token_focado
            eh_mov = token is self.token_em_mov
            bg_row = ("#1e1040" if eh_foc else "#0d2a0d" if eh_mov else COR_PAINEL)
            row = tk.Frame(self.frame_lista_inner, bg=bg_row,
                           relief="solid" if (eh_foc or eh_mov) else "flat",
                           bd=1 if (eh_foc or eh_mov) else 0)
            row.pack(fill="x", pady=2, padx=4)
            cv = tk.Canvas(row, width=10, height=10, bg=bg_row, highlightthickness=0)
            cv.create_oval(1, 1, 9, 9, fill=cor_g, outline="")
            cv.pack(side="left", padx=(4, 2), pady=5)
            fg_n = COR_SELECIONADO if eh_foc else COR_LINHA_MOV if eh_mov else COR_TEXTO
            lbl  = tk.Label(row, text=token.personagem.nome,
                            bg=bg_row, fg=fg_n,
                            font=("Consolas", 9, "bold" if (eh_foc or eh_mov) else "normal"),
                            anchor="w", cursor="hand2")
            lbl.pack(side="left", fill="x", expand=True)
            lbl.bind("<ButtonPress-1>", lambda e, t=token: self._token_clique_esq(e, t))

            # ── bolinha de cobertura ──────────────────────────────────────────
            cor_cob = CORES_COBERTURA.get(token.cobertura)
            if cor_cob:
                cv2 = tk.Canvas(row, width=8, height=8, bg=bg_row, highlightthickness=0)
                cv2.create_oval(1, 1, 7, 7, fill=cor_cob, outline="")
                cv2.pack(side="left", padx=(0, 2))

            # ── label de material (quando definido) ───────────────────────────
            mat = getattr(token, "material", "Nenhum")
            if mat and mat != "Nenhum":
                tk.Label(row, text=mat,
                         bg=bg_row, fg="#88ccff",
                         font=("Consolas", 7)).pack(side="left", padx=(0, 3))

            # ── botão 🛡 abre popup cobertura+material ────────────────────────
            tk.Button(row, text="🛡", bg=bg_row, fg=COR_TEXTO_DIM,
                      font=("Consolas", 9), relief="flat", cursor="hand2",
                      activebackground=COR_ACENTO,
                      command=lambda t=token: self._popup_cobertura(t)
                      ).pack(side="left", padx=1)

            txt_m = "✕mov" if eh_mov else "↖"
            fg_m  = COR_LINHA_MOV if eh_mov else COR_TEXTO_DIM
            bm = tk.Label(row, text=txt_m, bg=bg_row, fg=fg_m,
                          font=("Consolas", 8), cursor="hand2")
            bm.pack(side="left", padx=2)
            bm.bind("<ButtonPress-1>", lambda e, t=token: self._token_clique_dir(e, t))

            tk.Button(row, text="✕", bg=bg_row, fg="#aa4444",
                      font=("Consolas", 8), relief="flat", cursor="hand2",
                      command=lambda t=token: self._remover_token(t)
                      ).pack(side="right", padx=4)

        tk.Frame(self.frame_lista_inner, bg=COR_BORDA, height=1).pack(fill="x", pady=4)
        tk.Button(self.frame_lista_inner, text="+ Adicionar Personagem",
                  bg=COR_ACENTO, fg=COR_TEXTO, font=("Consolas", 9, "bold"),
                  relief="flat", cursor="hand2",
                  command=self._popup_adicionar_token
                  ).pack(fill="x", padx=4, pady=2)
    
    # ── POPUP COBERTURA ──────────────────────────────────────────────────────
    def _popup_cobertura(self, token):
        NIVEIS_MATERIAL = ["Nenhum", "Gesso", "Madeira", "Veiculo", "Concreto", "Aço"]
        CORES_MATERIAL  = {
            "Nenhum":   COR_TEXTO_DIM,
            "Gesso":    "#ddddcc",
            "Madeira":  "#cc9944",
            "Veiculo":  "#88aacc",
            "Concreto": "#aaaaaa",
            "Aço":      "#99ddff",
        }

        pop = tk.Toplevel(self)
        pop.title(f"Cobertura — {token.personagem.nome}")
        pop.configure(bg=COR_PAINEL)
        pop.geometry("300x420")
        pop.resizable(False, False)
        pop.grab_set()

        tk.Label(pop, text=f"Cobertura de {token.personagem.nome}",
                 bg=COR_PAINEL, fg=COR_TEXTO,
                 font=("Consolas", 10, "bold")).pack(pady=(14, 4))

        # ── Nível de cobertura ────────────────────────────────────────────────
        tk.Frame(pop, bg=COR_BORDA, height=1).pack(fill="x", padx=14, pady=(4, 6))
        tk.Label(pop, text="Nível de cobertura:",
                 bg=COR_PAINEL, fg=COR_TEXTO_DIM,
                 font=("Consolas", 9, "bold")).pack(anchor="w", padx=18)

        var_cob = tk.StringVar(value=token.cobertura)
        for nivel in NIVEIS_COBERTURA:
            cor = CORES_COBERTURA.get(nivel) or COR_TEXTO_DIM
            tk.Radiobutton(
                pop, text=nivel, variable=var_cob, value=nivel,
                bg=COR_PAINEL, fg=cor, selectcolor="#2a0060",
                activebackground=COR_PAINEL,
                font=("Consolas", 10, "bold"), cursor="hand2"
            ).pack(anchor="w", padx=30, pady=1)

        # ── Material de cobertura ─────────────────────────────────────────────
        tk.Frame(pop, bg=COR_BORDA, height=1).pack(fill="x", padx=14, pady=(8, 6))
        tk.Label(pop, text="Material da cobertura:",
                 bg=COR_PAINEL, fg=COR_TEXTO_DIM,
                 font=("Consolas", 9, "bold")).pack(anchor="w", padx=18)

        var_mat = tk.StringVar(value=token.material)

        mat_frame = tk.Frame(pop, bg=COR_PAINEL)
        mat_frame.pack(fill="x", padx=18, pady=(0, 4))

        for mat in NIVEIS_MATERIAL:
            cor = CORES_MATERIAL.get(mat, COR_TEXTO_DIM)
            tk.Radiobutton(
                mat_frame, text=mat, variable=var_mat, value=mat,
                bg=COR_PAINEL, fg=cor, selectcolor="#2a0060",
                activebackground=COR_PAINEL,
                font=("Consolas", 9), cursor="hand2"
            ).pack(anchor="w", padx=12, pady=1)

        # ── Botão confirmar ────────────────────────────────────────────────────
        tk.Frame(pop, bg=COR_BORDA, height=1).pack(fill="x", padx=14, pady=(6, 4))

        def _conf():
            token.cobertura = var_cob.get()
            token.material  = var_mat.get()
            token.salvar_cobertura()           # persiste ambos no personagem
            pop.destroy()
            self._atualizar_lista_lateral()
            self._redesenhar()

        tk.Button(pop, text="Confirmar", command=_conf,
                  bg="#38b000", fg="white",
                  font=("Consolas", 10, "bold")).pack(pady=8)

    # ── TOKENS ───────────────────────────────────────────────────────────────
    def _remover_token(self, token):
        if self.token_focado is token:
            self.token_focado = None
            self.lbl_token_focado.config(text="Clique esq. em um token →")
            self._limpar_painel_distancias()
        if self.token_em_mov is token:
            self.token_em_mov = None
            self.canvas.config(cursor="crosshair")
        self.tokens.remove(token)
        self._atualizar_distancias()
        self._atualizar_lista_lateral()
        self._redesenhar()

    def _popup_adicionar_token(self):
        pop = tk.Toplevel(self)
        pop.title("Adicionar Personagens ao Mapa")
        pop.configure(bg=COR_PAINEL)
        pop.geometry("380x500")
        pop.resizable(False, False)
        
        # ── CABEÇALHO ───────────────────────────────────────────────────────────
        tk.Label(pop, text="Adicionar Personagens",
                bg=COR_PAINEL, fg=COR_TEXTO,
                font=("Consolas", 11, "bold")).pack(pady=(14, 8))
        
        # ── SELETOR DE GRUPO ────────────────────────────────────────────────────
        frame_grupo = tk.Frame(pop, bg=COR_PAINEL)
        frame_grupo.pack(fill="x", padx=14, pady=(0, 8))
        
        tk.Label(frame_grupo, text="Grupo:", bg=COR_PAINEL, fg=COR_TEXTO_DIM,
                font=("Consolas", 9)).pack(side="left", padx=(0, 6))
        
        # Listar todos os grupos disponíveis
        grupos_disponiveis = list(self._grupos.keys()) if self._grupos else []
        grupo_var = tk.StringVar(
            value=grupos_disponiveis[0] if grupos_disponiveis else ""
        )
        
        # Canvas com scroll
        cs = tk.Canvas(pop, bg=COR_PAINEL, highlightthickness=0)
        sbs = tk.Scrollbar(pop, orient="vertical", command=cs.yview)
        cs.configure(yscrollcommand=sbs.set)
        
        # Packer order: precisa fazer pack ANTES de usar before=
        cs.pack(fill="both", expand=True, padx=10, pady=(0, 56))
        sbs.pack(side="right", fill="y", before=cs, pady=(0, 56))
        
        inner = tk.Frame(cs, bg=COR_PAINEL)
        cs.create_window((0, 0), window=inner, anchor="nw")
        
        def _atualizar_scroll():
            inner.bind("<Configure>",
                    lambda e: cs.configure(scrollregion=cs.bbox("all")))
        
        # ── FUNÇÃO INTERNA: ATUALIZAR LISTA ─────────────────────────────────────
        def _atualizar_lista_personagens():
            """Atualiza a lista de personagens do grupo selecionado."""
            # Limpar lista anterior
            for widget in inner.winfo_children():
                widget.destroy()
            
            grupo_selecionado = grupo_var.get()
            if not grupo_selecionado or grupo_selecionado not in self._grupos:
                tk.Label(inner, text="Nenhum grupo selecionado.",
                        bg=COR_PAINEL, fg=COR_TEXTO_DIM,
                        font=("Consolas", 9, "italic")).pack(padx=6, pady=4)
                return
            
            personagens = self._grupos[grupo_selecionado]
            if not personagens:
                tk.Label(inner, text="Nenhum personagem neste grupo.",
                        bg=COR_PAINEL, fg=COR_TEXTO_DIM,
                        font=("Consolas", 9, "italic")).pack(padx=6, pady=4)
                return
            
            # ✅ NOVO: Rastrear quais personagens já estão no mapa (por ID do objeto)
            ids_no_mapa = {id(t.personagem) for t in self.tokens}
            
            # Listar cada personagem uma única vez
            for p in personagens:
                ja_no_mapa = id(p) in ids_no_mapa
                
                # ── Linha do personagem ─────────────────────────────────────────
                row = tk.Frame(inner, bg="#1a0f35" if not ja_no_mapa else "#2a1a2a")
                row.pack(fill="x", padx=4, pady=1)
                
                # Label com nome
                cor_nome = COR_TEXTO if not ja_no_mapa else COR_TEXTO_DIM
                font_nome = ("Consolas", 9) if not ja_no_mapa else ("Consolas", 9, "italic")
                texto_nome = p.nome if not ja_no_mapa else f"{p.nome} (no mapa)"
                
                tk.Label(row, text=texto_nome, bg="#1a0f35" if not ja_no_mapa else "#2a1a2a",
                        fg=cor_nome, font=font_nome, anchor="w").pack(
                            side="left", padx=8, pady=4, fill="x", expand=True)
                
                # ✅ NOVO: Botão Adicionar (SEMPRE desabilitado se já está no mapa)
                if ja_no_mapa:
                    tk.Button(
                        row, text="✓ No mapa", bg="#2a1a2a", fg="#88aa88",
                        font=("Consolas", 8), relief="flat",
                        state="disabled"
                    ).pack(side="right", padx=4, pady=2)
                else:
                    # ✅ NOVO: Adicionar com verificação de duplicata
                    def _adicionar_com_verificacao(ps=p, gp=grupo_selecionado):
                        # Verificar NOVAMENTE se não foi adicionado enquanto popup estava aberto
                        ids_atuais = {id(t.personagem) for t in self.tokens}
                        if id(ps) not in ids_atuais:
                            self._adicionar_token(ps, gp)
                            _atualizar_lista_personagens()  # Atualizar lista
                        else:
                            # Aviso: já foi adicionado por outro lado
                            pass
                    
                    tk.Button(
                        row, text="Adicionar", bg=COR_ACENTO, fg=COR_TEXTO,
                        font=("Consolas", 8), relief="flat", cursor="hand2",
                        activebackground=COR_ACENTO2,
                        command=_adicionar_com_verificacao
                    ).pack(side="right", padx=4, pady=2)
                
                _atualizar_scroll()
        
        # ── SELETOR DE GRUPO (DEPOIS de definir _atualizar_lista_personagens) ───
        combo_grupo = tk.OptionMenu(
            frame_grupo, grupo_var, *grupos_disponiveis,
            command=lambda _: _atualizar_lista_personagens()
        )
        combo_grupo.config(
            bg="#1a0f35", fg=COR_TEXTO,
            font=("Consolas", 9),
            activebackground=COR_ACENTO,
            activeforeground="white",
            highlightthickness=0
        )
        combo_grupo["menu"].config(bg="#1a0f35", fg=COR_TEXTO,
                                    font=("Consolas", 9),
                                    activebackground=COR_ACENTO,
                                    activeforeground="white")
        combo_grupo.pack(side="left", fill="x", expand=True)
        
        # ── BOTÕES DE AÇÃO (RODAPÉ) ─────────────────────────────────────────────
        frame_botoes = tk.Frame(pop, bg=COR_PAINEL)
        frame_botoes.pack(fill="x", side="bottom", padx=10, pady=10)
        
        tk.Button(frame_botoes, text="Fechar",
                command=pop.destroy,
                bg="#3a0a80", fg=COR_TEXTO,
                font=("Consolas", 10, "bold"),
                relief="flat", cursor="hand2",
                activebackground="#5a1aa0").pack(side="right", padx=4)
        
        tk.Button(frame_botoes, text="↻ Atualizar",
                command=_atualizar_lista_personagens,
                bg=COR_ACENTO2, fg=COR_TEXTO,
                font=("Consolas", 10),
                relief="flat", cursor="hand2",
                activebackground=COR_ACENTO).pack(side="right", padx=4)
        
        # Inicializar lista
        _atualizar_lista_personagens()

    def _adicionar_token(self, personagem, grupo):
        # ── Calcular posição inicial (espaçamento inteligente) ──────────────────
        w = max(self.canvas.winfo_width(), 400)
        h = max(self.canvas.winfo_height(), 300)
        
        # Posicionar em grid: 6 personagens por linha
        col = len(self.tokens) % 6
        row = len(self.tokens) // 6
        
        cx = w // 2 + col * 80 - 200
        cy = h // 2 + row * 100 - 100
        
        # Converter coordenadas de tela para mundo
        wx = (cx - self.offset_x) / self.zoom
        wy = (cy - self.offset_y) / self.zoom
        
        # ── Criar token ─────────────────────────────────────────────────────────
        t = Token(personagem, wx, wy, grupo)
        self.tokens.append(t)
        
        # ── Atualizar mapa e painel lateral ─────────────────────────────────────
        self._atualizar_distancias()
        self._atualizar_lista_lateral()
        self._redesenhar()
        
        # ── Feedback ao usuário ─────────────────────────────────────────────────
        self.lbl_status.config(
            text=f"✓ {personagem.nome} adicionado ao mapa! (Grupo: {grupo})"
        )

    # ── DISTÂNCIAS ────────────────────────────────────────────────────────────
    def _dist_metros(self, t1, t2):
        import math
        return math.hypot(t2.wx-t1.wx, t2.wy-t1.wy) * self.escala_m_por_px

    def _atualizar_distancias(self):
        self.distancias.clear()
        for t1 in self.tokens:
            n1 = t1.personagem.nome
            self.distancias.setdefault(n1, {})
            for t2 in self.tokens:
                if t1 is t2: continue
                self.distancias[n1][t2.personagem.nome] = round(
                    self._dist_metros(t1,t2), 2)
        # sincroniza com CombatSystemScreen
        if hasattr(self.controller, "_tela_combate"):
            tela = self.controller._tela_combate
            if hasattr(tela, "distancias_mapa"):
                tela.distancias_mapa = dict(self.distancias)

    # ── HELPERS ───────────────────────────────────────────────────────────────
    def _carregar_mapa(self):
        if not PIL_DISPONIVEL:
            tk.messagebox.showerror("Pillow ausente",
                "pip install Pillow  para usar imagens de fundo.")
            return
        path = filedialog.askopenfilename(
            title="Escolher imagem",
            filetypes=[("Imagens","*.png *.jpg *.jpeg *.webp *.bmp"),("Todos","*.*")])
        if not path: return
        try:
            self.img_original = Image.open(path).convert("RGBA")
            self._reset_view()
        except Exception as e:
            tk.messagebox.showerror("Erro", str(e))

    def _remover_mapa(self):
        self.img_original = None; self.img_tk = None; self._redesenhar()

    def _reset_view(self):
        self.zoom=1.0; self.offset_x=0; self.offset_y=0; self._redesenhar()

    def _toggle_grade(self):
        self.mostrar_grade = not self.mostrar_grade
        self.btn_grade.config(
            text="⊞ Grade ON"  if self.mostrar_grade else "⊞ Grade OFF",
            fg=COR_TEXTO       if self.mostrar_grade else COR_TEXTO_DIM)
        self._redesenhar()

    def _atualizar_escala(self, event=None):
        try:
            val = float(self.entry_escala.get())
            if val > 0:
                self.escala_m_por_px = val
                self._atualizar_distancias()
                if self.token_focado: self._atualizar_painel_distancias()
                self._redesenhar()
        except ValueError:
            self.entry_escala.delete(0,"end")
            self.entry_escala.insert(0,str(self.escala_m_por_px))

    def _token_maior(self):
        self.raio_token = min(60, self.raio_token+4); self._redesenhar()

    def _token_menor(self):
        self.raio_token = max(10, self.raio_token-4); self._redesenhar()

    def _on_mouse_move(self, e):
        wx = (e.x - self.offset_x) / self.zoom
        wy = (e.y - self.offset_y) / self.zoom
        self.lbl_cursor.config(
            text=f"x:{wx:.0f}  y:{wy:.0f}  zoom:{self.zoom:.2f}×")
        if self.token_em_mov:
            self._redesenhar()
            r=10; cx,cy = e.x, e.y
            self.canvas.create_line(cx-r,cy,cx+r,cy,fill=COR_LINHA_MOV,width=2)
            self.canvas.create_line(cx,cy-r,cx,cy+r,fill=COR_LINHA_MOV,width=2)
            self.canvas.create_oval(cx-r,cy-r,cx+r,cy+r,
                                    outline=COR_LINHA_MOV,width=1)
### MAPA DE COMBATE ###
### MAPA DE COMBATE ###
### MAPA DE COMBATE ###

### TELA DE COMBATE 2 ###
### TELA DE COMBATE 2 ###
### TELA DE COMBATE 2 ###
'''
class CombatSystemScreen2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(bg='#130f26')
        self.controller = controller
        
        # Inicializar variáveis de grupo como None
        self.grupo_esquerdo = None
        self.grupo_direito = None
        
        # Botões de navegação
        tk.Button(self, text="Tela inicial", height=2, command=self.TelaInicial, 
                 bg="#1a0869", fg="white", font=("Arial", 20)).place(x=20, y=10, width=350, height=75)
        
        tk.Button(self, text="Seleção", height=2, command=self.TelaDeSelecao, 
                 bg="#1a0869", fg="white", font=("Arial", 20)).place(x=385, y=10, width=350, height=75)

        tk.Label(self, text="Combate 2", fg="white", bg="#1a0869", 
                font=("Arial", 20, "bold"), width=20, height=2).place(x=870, y=10, width=350, height=75)

        tk.Button(self, text="Informações", height=2, command=self.TelaDeRegrasEItens, 
                 bg="#1a0869", fg="white", font=("Arial", 20)).place(x=1235, y=10, width=350, height=75)

        # Criar interface de grupos
        self.criar_interface_grupos()

    def criar_interface_grupos(self):
        """Cria os seletores de grupos e as listas de personagens"""
        grupos_disponiveis = list(D.GruposDePersonagens.keys()) if hasattr(D, 'GruposDePersonagens') and D.GruposDePersonagens else []
        
        # --- Lado Esquerdo ---
        # Seletor de grupo esquerdo
        self.frame_seletor_esquerdo = tk.Frame(self, bg='#1a0869')
        self.frame_seletor_esquerdo.place(x=50, y=100, width=400, height=50)
        
        tk.Label(self.frame_seletor_esquerdo, text="Grupo Esquerdo:", 
                fg="white", bg="#1a0869", font=("Arial", 12, "bold")).pack(side="left", padx=5)
        
        self.combo_grupo_esquerdo = ttk.Combobox(self.frame_seletor_esquerdo, 
                                                values=grupos_disponiveis, 
                                                state="readonly", font=("Arial", 10))
        self.combo_grupo_esquerdo.pack(side="right", padx=5)
        
        # Definir valor padrão
        if grupos_disponiveis:
            if "Players" in grupos_disponiveis:
                self.grupo_esquerdo = "Players"
            else:
                self.grupo_esquerdo = grupos_disponiveis[0]
            self.combo_grupo_esquerdo.set(self.grupo_esquerdo)
        else:
            self.grupo_esquerdo = "Sem grupos"
        
        self.combo_grupo_esquerdo.bind("<<ComboboxSelected>>", self.atualizar_grupo_esquerdo)
        
        # --- Lado Direito ---
        # Seletor de grupo direito
        self.frame_seletor_direito = tk.Frame(self, bg='#1a0869')
        self.frame_seletor_direito.place(x=1150, y=100, width=400, height=50)
        
        tk.Label(self.frame_seletor_direito, text="Grupo Direito:", 
                fg="white", bg="#1a0869", font=("Arial", 12, "bold")).pack(side="left", padx=5)
        
        self.combo_grupo_direito = ttk.Combobox(self.frame_seletor_direito, 
                                               values=grupos_disponiveis, 
                                               state="readonly", font=("Arial", 10))
        self.combo_grupo_direito.pack(side="right", padx=5)
        
        # Definir valor padrão
        if grupos_disponiveis:
            if "NPCs" in grupos_disponiveis:
                self.grupo_direito = "NPCs"
            elif len(grupos_disponiveis) > 1:
                self.grupo_direito = next((g for g in grupos_disponiveis if g != self.grupo_esquerdo), grupos_disponiveis[0])
            else:
                self.grupo_direito = grupos_disponiveis[0]
            self.combo_grupo_direito.set(self.grupo_direito)
        else:
            self.grupo_direito = "Sem grupos"
        
        self.combo_grupo_direito.bind("<<ComboboxSelected>>", self.atualizar_grupo_direito)
        
        # Criar as listas iniciais
        self.frame_lista_esquerda = self.create_list_section_with_group(self.grupo_esquerdo, x=50, y=160)
        self.frame_lista_direita = self.create_list_section_with_group(self.grupo_direito, x=1150, y=160)

    def atualizar_grupo_esquerdo(self, event=None):
        """Atualiza o grupo selecionado no lado esquerdo"""
        self.grupo_esquerdo = self.combo_grupo_esquerdo.get()
        if hasattr(self, 'frame_lista_esquerda'):
            self.frame_lista_esquerda.destroy()
        self.frame_lista_esquerda = self.create_list_section_with_group(self.grupo_esquerdo, x=50, y=160)

    def atualizar_grupo_direito(self, event=None):
        """Atualiza o grupo selecionado no lado direito"""
        self.grupo_direito = self.combo_grupo_direito.get()
        if hasattr(self, 'frame_lista_direita'):
            self.frame_lista_direita.destroy()
        self.frame_lista_direita = self.create_list_section_with_group(self.grupo_direito, x=1150, y=160)

    def create_list_section_with_group(self, grupo_nome, x, y):
        """Cria uma seção de lista para um grupo específico"""  
        if not grupo_nome or grupo_nome not in D.GruposDePersonagens:
            frame = tk.Frame(self, bg='#1a0869')
            frame.place(x=x, y=y, width=400, height=690)
            tk.Label(frame, text="Nenhum grupo selecionado", 
                    fg="gray", bg="#1a0869", font=("Arial", 14)).pack(pady=300)
            return frame
        
        data_list = D.GruposDePersonagens[grupo_nome]
        
        frame = tk.Frame(self, bg='#1a0869')
        frame.place(x=x, y=y, width=400, height=690)

        label = tk.Label(frame, text=grupo_nome, fg="white", bg="#1a0869", font=("Arial", 16, "bold"))
        label.pack()

        if not data_list:
            tk.Label(frame, text="Grupo vazio", fg="gray", bg="#1a0869", 
                    font=("Arial", 12)).pack(pady=100)
            return frame

        canvas_frame = tk.Frame(frame, bg='#1a0869')
        canvas_frame.pack(fill="both", expand=True)
        canvas = tk.Canvas(canvas_frame, bg="#1a0869", highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        inner_frame = tk.Frame(canvas, bg="#1a0869")
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        for char in data_list:
            char_frame = tk.Frame(inner_frame, bg="#220866", bd=2, relief="groove")
            char_frame.pack(fill="x", padx=10, pady=5)
            char_frame.pack_propagate(False)
            char_frame.configure(width=370, height=200)

            info = f"{char.nome}    ||   Nv {char.Nivel}   ||   XP:  {char.XPAtual}/{char.XPlvlUp}\n"
            info += f"PV: {char.VidaAtual}/{char.VidaMax}  || Energia: {char.EnergiaAtual}/{char.EnergiaMax} || Mana:{char.ManaAtual}/{char.ManaMax}\n"
            info += f"Bloqueio: {char.Bloqueio}   |   Esquiva: {char.Esquiva}"
            tk.Label(char_frame, text=info, bg="#220866", fg="white", 
                    font=("Arial", 12), justify="left").pack(anchor="w", padx=10, pady=5)
            
            lbl_armas = tk.Label(char_frame, text="🗡 Armas equipadas", bg="#220866", 
                               fg="#90caf9", font=("Arial", 10, "underline"), cursor="hand2")
            lbl_armas.pack(anchor="w", padx=12)
            Tooltip(lbl_armas, self.texto_armas_maos(char))

            # Linha com dois botões
            botoes_frame = tk.Frame(char_frame, bg="#220866")
            botoes_frame.pack(pady=5)

            tk.Button(botoes_frame, text="Abrir Detalhes", bg="#1a0869", fg="white", 
                     font=("Arial", 12), 
                     command=lambda c=char: self.controller.abrir_detalhes(c)).pack(side="left", padx=10)

            tk.Button(botoes_frame, text="Abrir ações", bg="#3a0a80", fg="white", 
                     font=("Arial", 12), 
                     command=lambda c=char: print(f"Ações de {c.nome}")).pack(side="left", padx=10)

            # Controles de vida/energia/mana
            valor_var = tk.IntVar(value=1)
            controle_frame = tk.Frame(char_frame, bg="#220866")
            controle_frame.pack(pady=2)

            entry = tk.Entry(controle_frame, textvariable=valor_var, width=3, font=("Arial", 10))
            entry.grid(row=0, column=2, padx=10)

            # Vida
            tk.Button(controle_frame, text="+Vida", 
                     command=lambda c=char, v=valor_var: self.aplicar_cura(c, v), 
                     width=5, font=("Arial", 8)).grid(row=0, column=0)
            tk.Button(controle_frame, text="-Vida", 
                     command=lambda c=char, v=valor_var: self.aplicar_dano(c, v), 
                     width=5, font=("Arial", 8)).grid(row=0, column=1)

            # Energia
            tk.Button(controle_frame, text="+Energia", 
                     command=lambda c=char, v=valor_var: self.aplicar_ganho_energia(c, v), 
                     width=7, font=("Arial", 8)).grid(row=0, column=3)
            tk.Button(controle_frame, text="-Energia", 
                     command=lambda c=char, v=valor_var: self.aplicar_gasto_energia(c, v), 
                     width=7, font=("Arial", 8)).grid(row=0, column=4)

            # Mana
            tk.Button(controle_frame, text="+Mana", 
                     command=lambda c=char, v=valor_var: self.aplicar_ganho_mana(c, v), 
                     width=6, font=("Arial", 8)).grid(row=0, column=5)
            tk.Button(controle_frame, text="-Mana", 
                     command=lambda c=char, v=valor_var: self.aplicar_gasto_mana(c, v), 
                     width=6, font=("Arial", 8)).grid(row=0, column=6)

        return frame

    def aplicar_dano(self, personagem, valor_var):
        valor = valor_var.get()
        if isinstance(valor, int) and valor > 0:
            personagem.TomarDano(valor)
            self.refresh()
    
    def aplicar_gasto_energia(self, personagem, valor_var):
        valor = valor_var.get()
        if isinstance(valor, int) and valor > 0:
            personagem.GastarEnergia(valor)
            self.refresh()

    def aplicar_cura(self, personagem, valor_var):
        valor = valor_var.get()
        if isinstance(valor, int) and valor > 0:
            personagem.TomarCura(valor)
            self.refresh()

    def aplicar_ganho_energia(self, personagem, valor_var):
        valor = valor_var.get()
        if isinstance(valor, int) and valor > 0:
            personagem.GanharEnergia(valor)
            self.refresh()
    
    def aplicar_ganho_mana(self, personagem, valor_var):
        valor = valor_var.get()
        if isinstance(valor, int) and valor > 0:
            personagem.GanharMana(valor)
            self.refresh()
    
    def aplicar_gasto_mana(self, personagem, valor_var):
        valor = valor_var.get()
        if isinstance(valor, int) and valor > 0:
            personagem.GastarMana(valor)
            self.refresh()

    def refresh(self):
        """Atualiza as listas de personagens"""   
        grupos_disponiveis = list(D.GruposDePersonagens.keys()) if hasattr(D, 'GruposDePersonagens') and D.GruposDePersonagens else []
        
        # Atualizar valores das comboboxes
        self.combo_grupo_esquerdo['values'] = grupos_disponiveis
        self.combo_grupo_direito['values'] = grupos_disponiveis
        
        # Verificar se os grupos selecionados ainda existem
        if self.grupo_esquerdo not in grupos_disponiveis and grupos_disponiveis:
            self.grupo_esquerdo = grupos_disponiveis[0]
            self.combo_grupo_esquerdo.set(self.grupo_esquerdo)
        elif not grupos_disponiveis:
            self.grupo_esquerdo = "Sem grupos"
            self.combo_grupo_esquerdo.set(self.grupo_esquerdo)
        
        if self.grupo_direito not in grupos_disponiveis and grupos_disponiveis:
            self.grupo_direito = next((g for g in grupos_disponiveis if g != self.grupo_esquerdo), grupos_disponiveis[0])
            self.combo_grupo_direito.set(self.grupo_direito)
        elif not grupos_disponiveis:
            self.grupo_direito = "Sem grupos"
            self.combo_grupo_direito.set(self.grupo_direito)
        
        # Atualizar listas
        if hasattr(self, 'frame_lista_esquerda') and self.frame_lista_esquerda:
            self.frame_lista_esquerda.destroy()
            self.frame_lista_esquerda = self.create_list_section_with_group(self.grupo_esquerdo, x=50, y=160)
        
        if hasattr(self, 'frame_lista_direita') and self.frame_lista_direita:
            self.frame_lista_direita.destroy()
            self.frame_lista_direita = self.create_list_section_with_group(self.grupo_direito, x=1150, y=160)

    def texto_armas_maos(self, char):
        """Retorna texto descritivo das armas nas mãos"""
        maos = [s for s in char.slots.values() if s.tipo == "mao" and s.item]
        if not maos: 
            return "Nenhuma arma equipada"
        linhas = []
        for s in maos:
            i = s.item
            linhas.append(f"{s.nome}: {i.nome}\nDano: {getattr(i,'dano','—')} | Tipo: {getattr(i,'tipo','—')}")
        return "\n\n".join(linhas)

    def TelaInicial(self):
        self.controller.TelaInicial()

    def TelaDeSelecao(self):
        self.controller.TelaDeSelecao()
    
    def TelaDeRegrasEItens(self):
        self.controller.TelaDeRegrasEItens()
'''
### TELA DE COMBATE 2 ###
### TELA DE COMBATE 2 ###
### TELA DE COMBATE 2 ###

### TELA DE DICIONARIOS ###
C = {
    "bg_dark":    "#0d0b1e",   # fundo principal
    "bg_mid":     "#1a1535",   # painéis internos
    "bg_card":    "#221d3a",   # cards / frames de tabela
    "accent":     "#7c3aed",   # roxo principal
    "accent2":    "#5b21b6",   # roxo mais escuro
    "accent_hi":  "#a855f7",   # roxo claro (hover / destaque)
    "gold":       "#f59e0b",   # amarelo/ouro (editar)
    "red":        "#ef4444",   # vermelho (remover)
    "green":      "#10b981",   # verde (novo/salvar)
    "blue":       "#3b82f6",   # azul (info / atualizar)
    "text":       "#e2e8f0",   # texto principal
    "text_dim":   "#94a3b8",   # texto secundário
    "border":     "#3b1f6e",   # borda sutil
    "row_alt":    "#1e1840",   # linha alternada da tree
    "nav_bg":     "#130f26",   # barra de navegação
    "nav_btn":    "#2d1b69",   # botão de navegação
    "sep":        "#4c1d95",   # separador
}


class RegrasItensScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.place(x=0, y=0, width=1600, height=900)
        self.config(bg=C["bg_dark"])

        self.tabela_atual = None

        self.templates_tabelas = {
            "Itens":           self.template_itens,
            "Ranged":          self.template_ranged,
            "Melee":           self.template_melees,
            "Proteção":        self.template_protecao,
            "Munições":        self.template_municoes,
            "Consumíveis":     self.template_consumiveis,
            "Melhorias":       self.template_melhorias,
            "NPCs":            self.template_npcs,
            "Kits":            self.template_kits,
            "Buffs e Debuffs": self.template_buffs_debuffs,
            "Habilidades":     self.template_habilidades,
            "Poderes":         self.template_poderes,
        }

        self.setup_styles()
        self.setup_ui()
        
    # =========================================================================
    # HELPERS DE UI  (todos como métodos da classe)
    # =========================================================================
    def make_label(self, parent, text, x, y, w=None, h=30,
                   font_size=11, bold=False, anchor="w", bg=None):
        style = ("Segoe UI", font_size, "bold") if bold else ("Segoe UI", font_size)
        lbl = tk.Label(parent, text=text, fg=C["text"],
                       bg=bg or C["bg_mid"], font=style, anchor=anchor)
        if w:
            lbl.place(x=x, y=y, width=w, height=h)
        else:
            lbl.place(x=x, y=y, height=h)
        return lbl

    def make_entry(self, parent, x, y, w=250, h=30):
        e = tk.Entry(parent, font=("Segoe UI", 11),
                     bg=C["bg_card"], fg=C["text"],
                     insertbackground=C["text"], relief="flat",
                     highlightthickness=1,
                     highlightbackground=C["border"],
                     highlightcolor=C["accent_hi"])
        e.place(x=x, y=y, width=w, height=h)
        return e

    def make_combobox(self, parent, values, x, y, w=250, h=30, state="readonly"):
        cb = ttk.Combobox(parent, values=values, state=state,
                          font=("Segoe UI", 11))
        cb.place(x=x, y=y, width=w, height=h)
        return cb

    def make_text(self, parent, x, y, w=250, h=80):
        t = tk.Text(parent, font=("Segoe UI", 10),
                    bg=C["bg_card"], fg=C["text"],
                    insertbackground=C["text"], relief="flat",
                    highlightthickness=1,
                    highlightbackground=C["border"],
                    highlightcolor=C["accent_hi"], wrap="word")
        t.place(x=x, y=y, width=w, height=h)
        return t

    def make_btn(self, parent, text, cmd, x, y, w=140, h=36, color=None):
        color = color or C["green"]
        btn = tk.Button(parent, text=text, command=cmd,
                        bg=color, fg="white",
                        font=("Segoe UI", 11, "bold"),
                        relief="flat", cursor="hand2",
                        activebackground=C["accent_hi"],
                        activeforeground="white")
        btn.place(x=x, y=y, width=w, height=h)
        return btn

    def section_title(self, parent, text, y=0):
        """Faixa de título de seção."""
        frm = tk.Frame(parent, bg=C["accent2"])
        frm.place(x=0, y=y, width=1600, height=48)
        tk.Label(frm, text=text, fg="white", bg=C["accent2"],
                 font=("Segoe UI", 16, "bold")).place(x=20, y=8)
        tk.Frame(frm, bg=C["accent_hi"]).place(x=0, y=46, width=1600, height=2)

    def build_popup(self, title, w=500, h=480):
        """Cria Toplevel estilizado com barra de título."""
        popup = tk.Toplevel(self)
        popup.title(title)
        popup.geometry(f"{w}x{h}")
        popup.config(bg=C["bg_mid"])
        popup.resizable(False, False)
        popup.transient(self)
        popup.grab_set()
        tk.Frame(popup, bg=C["accent2"]).place(x=0, y=0, width=w, height=44)
        tk.Label(popup, text=title, fg="white", bg=C["accent2"],
                 font=("Segoe UI", 13, "bold")).place(x=16, y=10)
        return popup

    def _make_tree(self, parent, cols, col_widths=None):
        """Treeview com scrollbar vertical e zebra striping."""
        frm = tk.Frame(parent, bg=C["bg_card"],
                       highlightthickness=1,
                       highlightbackground=C["border"])
        frm.pack(fill="both", expand=True)

        sb = ttk.Scrollbar(frm, orient="vertical")
        sb.pack(side="right", fill="y")

        tree = ttk.Treeview(frm, style="Custom.Treeview",
                            columns=cols, show="headings",
                            yscrollcommand=sb.set)
        sb.config(command=tree.yview)

        for i, col in enumerate(cols):
            w = col_widths[i] if col_widths else 200
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=w, minwidth=60)

        tree.tag_configure("odd",  background=C["bg_card"])
        tree.tag_configure("even", background=C["row_alt"])
        tree.pack(fill="both", expand=True)
        return tree

    def _insert_tree(self, tree, values):
        tag = "even" if len(tree.get_children()) % 2 == 0 else "odd"
        return tree.insert("", "end", values=values, tags=(tag,))

    def _btn_bar(self, parent, cmd_novo, cmd_editar, cmd_remover, y=700):
        """Três botões de ação centralizados."""
        cx = 700
        self.make_btn(parent, "＋  Novo",   cmd_novo,    cx - 220, y, 180, 38, C["green"])
        self.make_btn(parent, "✎  Editar",  cmd_editar,  cx -  10, y, 180, 38, C["gold"])
        self.make_btn(parent, "✕  Remover", cmd_remover, cx + 200, y, 180, 38, C["red"])
    # =========================================================================
    # ESTILOS ttk
    # =========================================================================
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure("CustomCombobox.TCombobox",
                        foreground=C["text"], background=C["bg_card"],
                        fieldbackground=C["bg_card"], bordercolor=C["border"],
                        arrowcolor=C["accent_hi"], font=("Segoe UI", 11))

        style.configure("Custom.Treeview",
                        background=C["bg_card"], foreground=C["text"],
                        rowheight=28, fieldbackground=C["bg_card"],
                        font=("Segoe UI", 10))
        style.configure("Custom.Treeview.Heading",
                        background=C["accent2"], foreground="white",
                        font=("Segoe UI", 10, "bold"), relief="flat")
        style.map("Custom.Treeview",
                  background=[("selected", C["accent"])],
                  foreground=[("selected", "white")])

        style.configure("Sel.TCombobox",
                        foreground=C["text"], background=C["bg_card"],
                        fieldbackground=C["bg_card"], bordercolor=C["border"],
                        arrowcolor=C["accent_hi"], font=("Segoe UI", 12))
    # =========================================================================
    # LAYOUT BASE
    # =========================================================================
    def setup_ui(self):
        # ── Barra de navegação — estilo original do projeto ──────────────────
        tk.Button(self, text="Tela inicial", height=2, command=self.TelaInicial, bg="#1a0869", fg="white", font=("Arial", 20)).place(x=20, y=10, width=350, height=75)

        tk.Button(self, text="Seleção", height=2, command=self.TelaDeSelecao, bg="#1a0869", fg="white", font=("Arial", 20)).place(x=385, y=10, width=350, height=75)

        tk.Button(self, text="Combate", height=2, command=self.TelaDeCombate, bg="#1a0869", fg="white", font=("Arial", 20)).place(x=870, y=10, width=350, height=75)

        tk.Label(self, text="Informações",fg="white", bg="#1a0869", font=("Arial", 20, "bold"), width=20, height=2).place(x=1235, y=10, width=350, height=75)

        # ── Barra de seleção de tabela ────────────────────────────────────────
        sel_bar = tk.Frame(self, bg=C["bg_mid"])
        sel_bar.place(x=0, y=90, width=1600, height=56)
        tk.Frame(sel_bar, bg=C["border"]).place(x=0, y=55, width=1600, height=1)

        tk.Label(sel_bar, text="Tabela:", fg=C["text_dim"],bg=C["bg_mid"], font=("Segoe UI", 11)).place(x=20, y=16)

        self.combo_tabelas = ttk.Combobox(sel_bar, style="Sel.TCombobox",values=list(self.templates_tabelas.keys()),state="readonly", font=("Segoe UI", 12))
        self.combo_tabelas.place(x=90, y=10, width=280, height=36)
        self.combo_tabelas.bind("<<ComboboxSelected>>", self.on_tabela_selecionada)

        self._hint = tk.Label(sel_bar,text="← Selecione uma tabela para começar",fg=C["text_dim"], bg=C["bg_mid"],font=("Segoe UI", 10, "italic"))
        self._hint.place(x=390, y=18)

        # ── Container de conteúdo ─────────────────────────────────────────────
        self.container_conteudo = tk.Frame(self, bg=C["bg_dark"])
        self.container_conteudo.place(x=0, y=146, width=1600, height=754)

    def limpar_container(self):
        for w in self.container_conteudo.winfo_children():
            w.destroy()
        if hasattr(self, "_hint"):
            self._hint.config(text="")

    def on_tabela_selecionada(self, event=None):
        self.tabela_atual = self.combo_tabelas.get()
        self.limpar_container()
        if self.tabela_atual in self.templates_tabelas:
            self.templates_tabelas[self.tabela_atual]()

    def resumir_texto(self, valor, limite=35):
        if not valor:
            return ""
        texto = (", ".join(map(str, valor))
                 if isinstance(valor, (list, tuple)) else str(valor))
        return texto if len(texto) <= limite else texto[:limite] + "…"
    # =========================================================================
    # ITENS GENÉRICOS
    # =========================================================================
    def template_itens(self):
        self.limpar_container()
        self._descricoes_itens = {}
        c = self.container_conteudo

        self.section_title(c, "📦  ITENS GENÉRICOS")

        frm = tk.Frame(c, bg=C["bg_dark"])
        frm.place(x=20, y=58, width=1560, height=580)

        cols = ("Nome", "Peso", "Uso", "Descrição")
        self.tree_itens = self._make_tree(frm, cols, [400, 120, 200, 820])

        self.carregar_itens_tree()

        # ── Novo ─────────────────────────────────────────────
        def novo_item():
            p = self.build_popup("Novo Item", 480, 420)
            LX, EX, EW = 20, 170, 270

            self.make_label(p,"Nome",LX,60,bg=C["bg_mid"])
            self.make_label(p,"Peso",LX,100,bg=C["bg_mid"])
            self.make_label(p,"Uso",LX,140,bg=C["bg_mid"])
            self.make_label(p,"Descrição",LX,180,bg=C["bg_mid"])

            e_nome = self.make_entry(p,EX,60,EW)
            e_peso = self.make_entry(p,EX,100,EW)
            e_uso  = self.make_entry(p,EX,140,EW)
            e_desc = self.make_text(p,EX,180,EW,100)

            def salvar():
                nome = e_nome.get().strip()
                if not nome:
                    messagebox.showwarning("Erro","Nome obrigatório.",parent=p); return

                peso_s = e_peso.get().strip()
                try: peso = float(peso_s) if peso_s else None
                except: messagebox.showwarning("Erro","Peso inválido.",parent=p); return

                dados = D.carregar_itens_raw()

                if nome in dados:
                    messagebox.showwarning("Duplicado","Já existe.",parent=p); return

                dados[nome] = {
                    "nome":nome,
                    "peso":peso,
                    "uso":e_uso.get().strip() or None,
                    "descricao":e_desc.get("1.0","end").strip() or None
                }

                D.salvar_itens_raw(dados)
                self.carregar_itens_tree()
                p.destroy()

            self.make_btn(p,"💾  Salvar",salvar,170,360,140,38,C["green"])

        # ── Editar ───────────────────────────────────────────
        def editar_item():
            sel = self.tree_itens.selection()
            if not sel:
                messagebox.showwarning("Aviso","Selecione um item."); return

            nome_orig = self.tree_itens.item(sel[0],"values")[0]

            dados = D.carregar_itens_raw()
            data  = dados.get(nome_orig)

            if not data: return

            p = self.build_popup("Editar Item",480,420)
            LX, EX, EW = 20,170,270

            self.make_label(p,"Nome",LX,60,bg=C["bg_mid"])
            self.make_label(p,"Peso",LX,100,bg=C["bg_mid"])
            self.make_label(p,"Uso",LX,140,bg=C["bg_mid"])
            self.make_label(p,"Descrição",LX,180,bg=C["bg_mid"])

            e_nome = self.make_entry(p,EX,60,EW); e_nome.insert(0,data.get("nome",""))
            e_peso = self.make_entry(p,EX,100,EW); e_peso.insert(0,str(data.get("peso","") or ""))
            e_uso  = self.make_entry(p,EX,140,EW); e_uso.insert(0,data.get("uso","") or "")

            e_desc = self.make_text(p,EX,180,EW,100)
            e_desc.insert("1.0",data.get("descricao","") or "")

            def salvar():
                nome = e_nome.get().strip()
                if not nome:
                    messagebox.showwarning("Erro","Nome obrigatório.",parent=p); return

                peso_s = e_peso.get().strip()
                try: peso = float(peso_s) if peso_s else None
                except: messagebox.showwarning("Erro","Peso inválido.",parent=p); return

                if nome_orig != nome:
                    dados.pop(nome_orig,None)

                dados[nome] = {
                    "nome":nome,
                    "peso":peso,
                    "uso":e_uso.get().strip() or None,
                    "descricao":e_desc.get("1.0","end").strip() or None
                }

                D.salvar_itens_raw(dados)
                self.carregar_itens_tree()
                p.destroy()

            self.make_btn(p,"💾  Salvar",salvar,170,360,140,38,C["gold"])

        # ── Remover ──────────────────────────────────────────
        def remover_item():
            sel = self.tree_itens.selection()
            if not sel: return

            nome = self.tree_itens.item(sel[0],"values")[0]

            if messagebox.askyesno("Confirmar",f"Remover '{nome}'?"):
                D.remover_item_raw(nome)
                self.carregar_itens_tree()

        self._btn_bar(c,novo_item,editar_item,remover_item,y=648)

    def carregar_itens_tree(self):
        if not hasattr(self,"tree_itens"): return

        self.tree_itens.delete(*self.tree_itens.get_children())
        self._descricoes_itens.clear()

        try:
            for nome,data in D.carregar_itens_raw().items():

                descricao = data.get("descricao","")

                iid = self._insert_tree(
                    self.tree_itens,
                    (
                        data.get("nome",""),
                        data.get("peso",""),
                        data.get("uso",""),
                        self.resumir_texto(descricao)
                    )
                )

                if descricao:
                    Tooltip(self.tree_itens,descricao)

                self._descricoes_itens[iid] = descricao

        except Exception:
            traceback.print_exc()
    # =========================================================================
    # RANGED
    # =========================================================================
    CLASSES_RANGED = ["Pistola","Revolver","Submetralhadora","Escopeta","Espingarda","Carabina","Fuzil de assalto","Fuzil de batalha","DMR","Fuzil de precisão","Metralhadora leve","Metralhadora média","Metralhadora pesada","Fuzil antimaterial",]
    RARIDADES = ["Comum","Incomum","Rara","Épica","Exótica","Lendária"]
    MODOS_DE_DISPARO = []

    def template_ranged(self):
        self.limpar_container()
        c = self.container_conteudo
        self.section_title(c, "🔫  ARMAS DE FOGO")

        frm = tk.Frame(c, bg=C["bg_dark"])
        frm.place(x=20, y=58, width=1560, height=580)

        cols = ("Nome","Peso","Classe","Ações","Modo Padrão","Raridade","Calibre","Capacidade","TPM","Ruído")
        self.tree_ranged = self._make_tree(frm, cols, [220,70,160,200,120,100,100,110,70,70])
        self.carregar_ranged_tree()

        def _popup_ranged(titulo, data=None):
            p = self.build_popup(titulo, 520, 690)
            LX, EX, EW = 20, 200, 290
            y = 58; fields = {}
            for label, key in [
                ("Nome","nome"), ("Peso","peso"), ("Calibre","calibre"),
                ("Capacidade","cap"), ("TPM","tpm"), ("Ruído","ruido"),
                ("Tipo de Dano","tipo_dano"),("Descrição","descricao"),
            ]:
                self.make_label(p, label, LX, y, bg=C["bg_mid"])
                fields[key] = self.make_entry(p, EX, y, EW); y += 42
            self.make_label(p, "Classe",   LX, y, bg=C["bg_mid"])
            fields["classe"]   = self.make_combobox(p, self.CLASSES_RANGED, EX, y, EW); y += 42
            self.make_label(p, "Ações (vírgula)", LX, y, bg=C["bg_mid"])
            fields["acoes"]    = self.make_entry(p, EX, y, EW); y += 42
            self.make_label(p, "Modo padrão", LX, y, bg=C["bg_mid"])
            fields["modo_padrao"] = self.make_combobox(p, [], EX, y, EW); y += 42
            self.make_label(p, "Empunhadura", LX, y, bg=C["bg_mid"])
            fields["maos"] = self.make_combobox(p, ["1 mão", "2 mãos"], EX, y, EW); y += 42
            self.make_label(p, "Raridade", LX, y, bg=C["bg_mid"])
            fields["raridade"] = self.make_combobox(p, self.RARIDADES, EX, y, EW)

            def _atualizar_modos(*_):
                modos = [a.strip() for a in fields["acoes"].get().split(",") if a.strip()]
                fields["modo_padrao"]["values"] = modos
                if modos and fields["modo_padrao"].get() not in modos:
                    fields["modo_padrao"].set(modos[0])

            fields["acoes"].bind("<KeyRelease>", _atualizar_modos)

            if data:
                fields["nome"].insert(0, data.get("nome",""))
                fields["peso"].insert(0, str(data.get("peso","")))
                fields["calibre"].insert(0, data.get("calibre",""))
                fields["cap"].insert(0, str(data.get("capacidade","")))
                fields["tpm"].insert(0, str(data.get("TPM","")))
                fields["ruido"].insert(0, str(data.get("ruido","")))
                fields["tipo_dano"].insert(0, data.get("tipo_dano","balístico"))
                fields["descricao"].insert(0, data.get("descricao",""))
                fields["classe"].set(data.get("classe",""))
                fields["acoes"].insert(0, ", ".join(data.get("acoes_disparo",[])))
                _atualizar_modos()
                fields["modo_padrao"].set(data.get("modo_disparo_atual", ""))

                # ✅ FIX: suporta "requer_duas_maos" (bool) e "maos" (int legado)
                requer_duas = data.get("requer_duas_maos", None)
                if requer_duas is None:
                    requer_duas = data.get("maos", 1) == 2
                fields["maos"].set("2 mãos" if requer_duas else "1 mão")

                fields["raridade"].set(data.get("raridade","Comum"))
            else:
                fields["tipo_dano"].insert(0, "balístico")
                fields["maos"].set("1 mão")
            return p, fields

        def novo_ranged():
            p, fields = _popup_ranged("Nova Arma de Fogo")
            def salvar():
                nome = fields["nome"].get().strip()
                if not nome: messagebox.showwarning("Erro","Nome obrigatório.",parent=p); return
                try:
                    peso=float(fields["peso"].get()); cap=int(fields["cap"].get())
                    tpm=int(fields["tpm"].get());     ruido=int(fields["ruido"].get())
                except: messagebox.showwarning("Erro","Peso/Cap/TPM/Ruído devem ser numéricos.",parent=p); return
                dados = D.carregar_rangeds_raw()
                if nome in dados: messagebox.showwarning("Duplicado","Já existe.",parent=p); return
                acoes = [a.strip() for a in fields["acoes"].get().split(",") if a.strip()]
                dados[nome] = {
                    "nome":nome,"peso":peso,"classe":fields["classe"].get(),
                    "acoes_disparo":acoes,
                    "modo_disparo_atual":fields["modo_padrao"].get() or (acoes[0] if acoes else ""),
                    "raridade":fields["raridade"].get(),"calibre":fields["calibre"].get().strip(),
                    "capacidade":cap,"TPM":tpm,"ruido":ruido,
                    "tipo_dano":fields["tipo_dano"].get().strip(),"requer_duas_maos": fields["maos"].get() == "2 mãos",
                    "descricao": fields["descricao"].get().strip(),
                }
                D.salvar_rangeds_raw(dados); self.carregar_ranged_tree(); p.destroy()
            self.make_btn(p,"💾  Salvar",salvar,185,610,150,38,C["green"])

        def editar_ranged():
            sel = self.tree_ranged.selection()
            if not sel: messagebox.showwarning("Aviso","Selecione uma arma."); return
            nome_orig = self.tree_ranged.item(sel[0],"values")[0]
            dados = D.carregar_rangeds_raw(); data = dados.get(nome_orig)
            if not data: return
            p, fields = _popup_ranged("Editar Arma de Fogo", data)
            def salvar():
                nome = fields["nome"].get().strip()
                if not nome: messagebox.showwarning("Erro","Nome obrigatório.",parent=p); return
                try:
                    peso=float(fields["peso"].get()); cap=int(fields["cap"].get())
                    tpm=int(fields["tpm"].get());     ruido=int(fields["ruido"].get())
                except: messagebox.showwarning("Erro","Valores inválidos.",parent=p); return
                if nome_orig != nome: dados.pop(nome_orig, None)
                acoes = [a.strip() for a in fields["acoes"].get().split(",") if a.strip()]
                dados[nome] = {
                    "nome":nome,"peso":peso,"classe":fields["classe"].get(),
                    "acoes_disparo":acoes,
                    "modo_disparo_atual":fields["modo_padrao"].get() or (acoes[0] if acoes else ""),
                    "raridade":fields["raridade"].get(),"calibre":fields["calibre"].get().strip(),
                    "capacidade":cap,"TPM":tpm,"ruido":ruido,
                    "tipo_dano":fields["tipo_dano"].get().strip(),"requer_duas_maos": fields["maos"].get() == "2 mãos",
                    "descricao": fields["descricao"].get().strip(),
                }
                D.salvar_rangeds_raw(dados); self.carregar_ranged_tree(); p.destroy()
            self.make_btn(p,"💾  Salvar",salvar,185,610,150,38,C["gold"])

        def remover_ranged():
            sel = self.tree_ranged.selection()
            if not sel: return
            nome = self.tree_ranged.item(sel[0],"values")[0]
            if messagebox.askyesno("Confirmar",f"Remover '{nome}'?"):
                D.remover_ranged_raw(nome); self.carregar_ranged_tree()

        self._btn_bar(c, novo_ranged, editar_ranged, remover_ranged, y=648)

    def carregar_ranged_tree(self):
        if not hasattr(self, "tree_ranged"): return
        self.tree_ranged.delete(*self.tree_ranged.get_children())

        ORDEM_CLASSES = [
            "Pistola","Revolver","Submetralhadora","Escopeta","Espingarda",
            "Carabina","Fuzil de assalto","Fuzil de batalha","DMR",
            "Fuzil de precisão","Metralhadora leve","Metralhadora média",
            "Metralhadora pesada","Fuzil antimaterial"
        ]
        ORDEM_RARIDADES = ["Comum","Incomum","Rara","Épica","Exótica","Lendária"]

        def _chave_ranged(item_tuple):
            nome, d = item_tuple
            if isinstance(d, dict):
                classe   = d.get("classe", "")
                raridade = d.get("raridade", "")
            else:
                classe   = getattr(d, "classe", "")
                raridade = getattr(d, "raridade", "")
            ci = ORDEM_CLASSES.index(classe)     if classe   in ORDEM_CLASSES   else 999
            ri = ORDEM_RARIDADES.index(raridade) if raridade in ORDEM_RARIDADES else 999
            return (ci, ri, nome)

        try:
            itens = sorted(D.carregar_rangeds().items(), key=_chave_ranged)
            for nome, d in itens:
                if isinstance(d, dict):
                    nome_v   = d.get("nome", "")
                    peso_v   = d.get("peso", "")
                    classe_v = d.get("classe", "")
                    acoes_v  = ", ".join(d.get("acoes_disparo", []))
                    modo_v   = d.get("modo_disparo_atual", "")
                    rar_v    = d.get("raridade", "")
                    cal_v    = d.get("calibre", "")
                    cap_v    = d.get("capacidade", "")
                    tpm_v    = d.get("TPM", "")
                    ruido_v  = d.get("ruido", "")
                else:
                    nome_v   = getattr(d, "nome", "")
                    peso_v   = getattr(d, "pesoBase", getattr(d, "peso", ""))
                    classe_v = getattr(d, "classe", "")
                    acoes_v  = ", ".join(getattr(d, "acoes_disparo", []))
                    modo_v   = getattr(d, "modo_disparo_atual", "")
                    rar_v    = getattr(d, "raridade", "")
                    cal_v    = getattr(d, "calibre", "")
                    cap_v    = getattr(d, "capacidadeBase", getattr(d, "capacidade", ""))
                    tpm_v    = getattr(d, "TPM", "")
                    ruido_v  = getattr(d, "ruido", "")

                self._insert_tree(self.tree_ranged, (
                    nome_v, peso_v, classe_v, acoes_v,
                    modo_v, rar_v, cal_v, cap_v, tpm_v, ruido_v,
                ))
        except Exception:
            traceback.print_exc()
    # =========================================================================
    # MELEE
    # =========================================================================
    TAGS_MELEE_LIST = ["Perfurante","Cortante","Contundente","Leve","Pesada","Duas Mãos","Alcance","Arremessável","Não Letal"]

    def template_melees(self):
        self.limpar_container()
        c = self.container_conteudo
        self.section_title(c, "⚔  ARMAS MELEE")

        frm = tk.Frame(c, bg=C["bg_dark"])
        frm.place(x=20, y=58, width=1560, height=750)

        cols = ("Nome","Peso","Dano Base","Mult Crítico","Valor Crítico","Raridade","Tags")
        self.tree_melees = self._make_tree(frm, cols, [260,80,110,130,130,120,710])
        self.carregar_melees_tree()

        def _popup_melee(titulo, data=None):
            # Grupos de tags mutuamente exclusivos (só 1 por grupo)
            GRUPOS_TAGS = {
                "Tipo de Dano":  ["cortante", "perfurante", "concussivo"],
                "Peso":          ["leve", "balanceada", "pesada"],
                "Empunhadura":   ["uma_mao", "duas_maos"],
                "Alcance":       ["alcance_curto", "alcance_medio", "alcance_longo"],
            }
            # Tags livres (não exclusivas entre si)
            TAGS_LIVRES = ["sofisticada", "arremessavel", "furtiva", "nao_letal"]

            p = self.build_popup(titulo, 560, 750)
            LX, EX, EW = 20, 190, 340
            y = 58; fields = {}
            for label, key in [
                ("Nome","nome"),("Peso","peso"),("Dano Base","dano_base"),
                ("Mult. Crítico","crit_mult"),("Valor Crítico","crit_valor"),
                ("Descrição","descricao"),
            ]:
                self.make_label(p, label, LX, y, bg=C["bg_mid"])
                fields[key] = self.make_entry(p, EX, y, EW); y += 42
            self.make_label(p, "Raridade", LX, y, bg=C["bg_mid"])
            fields["raridade"] = self.make_combobox(p, self.RARIDADES, EX, y, EW); y += 42

            # --- Tags com grupos exclusivos via Radiobutton + livres via Checkbutton ---
            self.make_label(p, "Tags", LX, y, bg=C["bg_mid"])
            tags_frm = tk.Frame(p, bg=C["bg_card"])
            tags_frm.place(x=EX, y=y, width=EW, height=300)

            tags_vars  = {}   # tag -> BooleanVar  (para livres e leitura final)
            radio_vars = {}   # grupo -> StringVar (para exclusivos; "" = nenhuma)

            row_i = 0
            for grupo, opcoes in GRUPOS_TAGS.items():
                tk.Label(tags_frm, text=grupo+":", bg=C["bg_card"], fg=C["accent_hi"],
                        font=("Segoe UI", 8, "bold")).grid(
                    row=row_i, column=0, columnspan=len(opcoes)+1, sticky="w", padx=4, pady=(4,0))
                row_i += 1
                rvar = tk.StringVar(value="")
                radio_vars[grupo] = rvar
                for col_i, tag in enumerate(opcoes):
                    tk.Radiobutton(
                        tags_frm, text=tag, variable=rvar, value=tag,
                        bg=C["bg_card"], fg=C["text"], selectcolor=C["accent2"],
                        activebackground=C["bg_card"], activeforeground=C["accent_hi"],
                        font=("Segoe UI", 9),
                    ).grid(row=row_i, column=col_i, sticky="w", padx=4, pady=1)
                row_i += 1

            # Separador visual
            tk.Frame(tags_frm, bg=C["accent2"], height=1).grid(
                row=row_i, column=0, columnspan=4, sticky="ew", padx=4, pady=4)
            row_i += 1

            # Tags livres
            tk.Label(tags_frm, text="Especiais:", bg=C["bg_card"], fg=C["accent_hi"],
                    font=("Segoe UI", 8, "bold")).grid(
                row=row_i, column=0, columnspan=4, sticky="w", padx=4)
            row_i += 1

            cols_por_linha = 2  # Coloca 2 tags por linha
            for idx, tag in enumerate(TAGS_LIVRES):
                var = tk.BooleanVar()
                tags_vars[tag] = var
                col_i = idx % cols_por_linha
                tk.Checkbutton(
                    tags_frm, text=tag, variable=var,
                    bg=C["bg_card"], fg=C["text"], selectcolor=C["accent2"],
                    activebackground=C["bg_card"], activeforeground=C["accent_hi"],
                    font=("Segoe UI", 9),
                ).grid(row=row_i, column=col_i, sticky="w", padx=4, pady=1)
                if col_i == cols_por_linha - 1:
                    row_i += 1

            def _get_tags_selecionadas():
                """Lê radio + checkbuttons e retorna lista final de tags."""
                resultado = []
                for rvar in radio_vars.values():
                    v = rvar.get()
                    if v: resultado.append(v)
                for tag, bvar in tags_vars.items():
                    if bvar.get(): resultado.append(tag)
                return resultado

            # Pré-preencher ao editar
            if data:
                fields["nome"].insert(0, data.get("nome",""))
                fields["peso"].insert(0, str(data.get("peso","")))
                fields["dano_base"].insert(0, str(data.get("dano_base","")))
                fields["crit_mult"].insert(0, str(data.get("crit_mult","")))
                fields["crit_valor"].insert(0, str(data.get("crit_valor","")))
                fields["raridade"].set(data.get("raridade","Comum"))
                fields["descricao"].insert(0, data.get("descricao",""))
                tags_salvas = set(data.get("tags", []))
                for grupo, opcoes in GRUPOS_TAGS.items():
                    for tag in opcoes:
                        if tag in tags_salvas:
                            radio_vars[grupo].set(tag)
                            break
                for tag in TAGS_LIVRES:
                    if tag in tags_salvas:
                        tags_vars[tag].set(True)

            # Expõe helper para os blocos salvar
            fields["_get_tags"] = _get_tags_selecionadas
            return p, fields, tags_vars

        def novo_melee():
            p, fields, tags_vars = _popup_melee("Nova Arma Melee")
            def salvar():
                nome = fields["nome"].get().strip()
                if not nome: messagebox.showwarning("Erro","Nome obrigatório.",parent=p); return
                try:
                    peso=float(fields["peso"].get()); db=int(fields["dano_base"].get())
                    cm=int(fields["crit_mult"].get()); cv=int(fields["crit_valor"].get())
                except: messagebox.showwarning("Erro","Valores inválidos.",parent=p); return
                dados = D.carregar_melees_raw()
                if nome in dados: messagebox.showwarning("Duplicado","Já existe.",parent=p); return
                dados[nome] = {
                    "nome":nome,"peso":peso,"dano_base":db,"crit_mult":cm,
                    "crit_valor":cv,"raridade":fields["raridade"].get(),
                    "tags": fields["_get_tags"](),"Melhorias":[],
                    "descricao": fields["descricao"].get().strip(),
                }
                D.salvar_melees_raw(dados); self.carregar_melees_tree(); p.destroy()
            self.make_btn(p,"💾  Salvar",salvar,200,670,160,38,C["green"])

        def editar_melee():
            sel = self.tree_melees.selection()
            if not sel: messagebox.showwarning("Aviso","Selecione uma arma."); return
            nome_orig = self.tree_melees.item(sel[0],"values")[0]
            dados = D.carregar_melees_raw(); data = dados.get(nome_orig)
            if not data: return
            p, fields, tags_vars = _popup_melee("Editar Arma Melee", data)
            def salvar():
                nome = fields["nome"].get().strip()
                if not nome: messagebox.showwarning("Erro","Nome obrigatório.",parent=p); return
                try:
                    peso=float(fields["peso"].get()); db=int(fields["dano_base"].get())
                    cm=int(fields["crit_mult"].get()); cv=int(fields["crit_valor"].get())
                except: messagebox.showwarning("Erro","Valores inválidos.",parent=p); return
                if nome_orig != nome: dados.pop(nome_orig, None)
                dados[nome] = {
                    "nome":nome,"peso":peso,"dano_base":db,"crit_mult":cm,
                    "crit_valor":cv,"raridade":fields["raridade"].get(),
                    "tags": fields["_get_tags"](),
                    "Melhorias":data.get("Melhorias",[]),
                    "descricao": fields["descricao"].get().strip(),
                }
                D.salvar_melees_raw(dados); self.carregar_melees_tree(); p.destroy()
            self.make_btn(p,"💾  Salvar",salvar,200,670,160,38,C["gold"])

        def remover_melee():
            sel = self.tree_melees.selection()
            if not sel: return
            nome = self.tree_melees.item(sel[0],"values")[0]
            if messagebox.askyesno("Confirmar",f"Remover '{nome}'?"):
                D.remover_melee_raw(nome); self.carregar_melees_tree()

        self._btn_bar(c, novo_melee, editar_melee, remover_melee, y=648)

    def carregar_melees_tree(self):
        if not hasattr(self,"tree_melees"): return
        self.tree_melees.delete(*self.tree_melees.get_children())
        try:
            for nome, d in D.carregar_melees_raw().items():
                self._insert_tree(self.tree_melees,(
                    d.get("nome",""),d.get("peso",""),d.get("dano_base",""),
                    d.get("crit_mult",""),d.get("crit_valor",""),
                    d.get("raridade",""),", ".join(d.get("tags",[])),
                ))
        except Exception: traceback.print_exc()
    # =========================================================================
    # PROTEÇÃO
    # =========================================================================
    def template_protecao(self):
        self.limpar_container()
        c = self.container_conteudo
        self.section_title(c, "🛡  PROTEÇÕES")

        frm = tk.Frame(c, bg=C["bg_dark"])
        frm.place(x=20, y=58, width=1560, height=580)

        cols = ("Nome","Peso","Nível Balístico","Durabilidade","Regiões","Região Indicada","Absorções")
        self.tree_protecao = self._make_tree(frm, cols, [220,70,130,100,250,150,610])
        self.carregar_protecao_tree()

        def _popup_prot(titulo, data=None):
            p = self.build_popup(titulo, 540, 700)
            LX, EX, EW = 20, 210, 300
            y = 58; fields = {}

            # Campos simples
            for label, key in [
                ("Nome","nome"), ("Peso","peso"),
                ("Nível Balístico","nivelBalistico"), ("Durabilidade Máx","durabilidadeMax"),
            ]:
                self.make_label(p, label, LX, y, bg=C["bg_mid"])
                fields[key] = self.make_entry(p, EX, y, EW); y += 42

            # Regiões e região indicada
            self.make_label(p, "Regiões (vírgula)", LX, y, bg=C["bg_mid"])
            fields["regioes"] = self.make_entry(p, EX, y, EW); y += 42

            self.make_label(p, "Região Indicada", LX, y, bg=C["bg_mid"])
            fields["regiao_indicada"] = self.make_combobox(p, [], EX, y, EW); y += 42

            def _atualizar_regioes(*_):
                regioes = [r.strip() for r in fields["regioes"].get().split(",") if r.strip()]
                fields["regiao_indicada"]["values"] = regioes
                if regioes and fields["regiao_indicada"].get() not in regioes:
                    fields["regiao_indicada"].set(regioes[0])

            fields["regioes"].bind("<KeyRelease>", _atualizar_regioes)

            # Absorções (cada tipo numa linha) — COM SCROLL
            self.make_label(p, "Absorções", LX, y, bg=C["bg_mid"]); y += 28

            # Frame container com altura fixa
            abs_container = tk.Frame(p, bg=C["bg_mid"], bd=1, relief="sunken")
            abs_container.place(x=LX, y=y, width=EX + 85, height=180)

            canvas_abs = tk.Canvas(abs_container, bg=C["bg_mid"], highlightthickness=0)
            scrollbar_abs = tk.Scrollbar(abs_container, orient="vertical", command=canvas_abs.yview)
            scroll_frame = tk.Frame(canvas_abs, bg=C["bg_mid"])

            scroll_frame.bind(
                "<Configure>",
                lambda e: canvas_abs.configure(scrollregion=canvas_abs.bbox("all"))
            )

            canvas_abs.create_window((0, 0), window=scroll_frame, anchor="nw")
            canvas_abs.configure(yscrollcommand=scrollbar_abs.set)

            canvas_abs.pack(side="left", fill="both", expand=True)
            scrollbar_abs.pack(side="right", fill="y")

            # Bind mousewheel
            def _on_mousewheel(event):
                canvas_abs.yview_scroll(int(-1 * (event.delta / 120)), "units")
            canvas_abs.bind("<MouseWheel>", _on_mousewheel)
            scroll_frame.bind("<MouseWheel>", _on_mousewheel)

            TIPOS_ABS = CB.tipos_de_dano
            fields["absorcoes"] = {}
            for tipo in TIPOS_ABS:
                row = tk.Frame(scroll_frame, bg=C["bg_mid"])
                row.pack(fill="x", padx=4, pady=2)
                tk.Label(row, text=f"  {tipo.capitalize()}", bg=C["bg_mid"], fg="white",
                        width=18, anchor="w").pack(side="left")
                entry = tk.Entry(row, width=8)
                entry.insert(0, "0")
                entry.pack(side="left")
                entry.bind("<MouseWheel>", _on_mousewheel)
                fields["absorcoes"][tipo] = entry

            y += 190

            # Descrição
            self.make_label(p, "Descrição", LX, y, bg=C["bg_mid"])
            fields["descricao"] = self.make_entry(p, EX, y, EW)

            if data:
                abs_ = data.get("absorcoes", {})
                fields["nome"].insert(0, data.get("nome",""))
                fields["peso"].insert(0, str(data.get("peso","")))
                fields["nivelBalistico"].insert(0, str(data.get("nivelBalistico","")))
                fields["durabilidadeMax"].insert(0, str(data.get("durabilidadeMax", 100)))
                fields["regioes"].insert(0, ", ".join(data.get("regioes_cobertas",[])))
                _atualizar_regioes()
                fields["regiao_indicada"].set(data.get("regiao_indicada",""))
                for tipo in TIPOS_ABS:
                    fields["absorcoes"][tipo].delete(0, "end")
                    fields["absorcoes"][tipo].insert(0, str(abs_.get(tipo, 0)))
                fields["descricao"].insert(0, data.get("descricao",""))

            return p, fields, TIPOS_ABS

        def _coletar_dados(fields, TIPOS_ABS):
            nome = fields["nome"].get().strip()
            try:
                peso   = float(fields["peso"].get() or 0)
                nb     = float(fields["nivelBalistico"].get() or 0)
                durmax = int(fields["durabilidadeMax"].get() or 100)
            except:
                return None, "Peso/Nível Balístico/Durabilidade devem ser numéricos."
            regioes = [r.strip().lower() for r in fields["regioes"].get().split(",") if r.strip()]
            abs_ = {}
            for tipo in TIPOS_ABS:
                try:
                    val = int(fields["absorcoes"][tipo].get() or 0)
                    if val != 0:
                        abs_[tipo] = val
                except:
                    pass
            descricao = fields["descricao"].get().strip()
            reg_ind   = fields["regiao_indicada"].get().strip().lower()
            return {
                "nome": nome, "peso": peso, "nivelBalistico": nb,
                "absorcoes": abs_, "regioes_cobertas": regioes,
                "regiao_indicada": reg_ind or (regioes[0] if regioes else ""),
                "durabilidade": durmax, "durabilidadeMax": durmax,
                "descricao": descricao, "Melhorias": [],
            }, None

        def novo_protecao():
            p, fields, TIPOS_ABS = _popup_prot("Nova Proteção")
            def salvar():
                nome = fields["nome"].get().strip()
                if not nome: messagebox.showwarning("Erro","Nome obrigatório.",parent=p); return
                obj, err = _coletar_dados(fields, TIPOS_ABS)
                if err: messagebox.showwarning("Erro", err, parent=p); return
                dados = D.carregar_protecoes_raw()
                if nome in dados: messagebox.showwarning("Duplicado","Já existe.",parent=p); return
                dados[nome] = obj
                D.salvar_protecoes_raw(dados); self.carregar_protecao_tree(); p.destroy()
            self.make_btn(p,"💾  Salvar",salvar,195,620,150,38,C["green"])

        def editar_protecao():
            sel = self.tree_protecao.selection()
            if not sel: messagebox.showwarning("Aviso","Selecione."); return
            nome_orig = self.tree_protecao.item(sel[0],"values")[0]
            dados = D.carregar_protecoes_raw(); data = dados.get(nome_orig)
            if not data: return
            p, fields, TIPOS_ABS = _popup_prot("Editar Proteção", data)
            def salvar():
                nome = fields["nome"].get().strip()
                if not nome: messagebox.showwarning("Erro","Nome obrigatório.",parent=p); return
                obj, err = _coletar_dados(fields, TIPOS_ABS)
                if err: messagebox.showwarning("Erro", err, parent=p); return
                if nome_orig != nome: dados.pop(nome_orig, None)
                obj["durabilidade"] = data.get("durabilidade", obj["durabilidadeMax"])
                dados[nome] = obj
                D.salvar_protecoes_raw(dados); self.carregar_protecao_tree(); p.destroy()
            self.make_btn(p,"💾  Salvar",salvar,195,620,150,38,C["gold"])

        def remover_protecao():
            sel = self.tree_protecao.selection()
            if not sel: return
            nome = self.tree_protecao.item(sel[0],"values")[0]
            if messagebox.askyesno("Confirmar",f"Remover '{nome}'?"):
                D.remover_protecao_raw(nome); self.carregar_protecao_tree()

        self._btn_bar(c, novo_protecao, editar_protecao, remover_protecao, y=648)

    def carregar_protecao_tree(self):
        if not hasattr(self,"tree_protecao"): return
        self.tree_protecao.delete(*self.tree_protecao.get_children())
        try:
            for nome, d in sorted(D.carregar_protecoes_raw().items(), key=lambda x: x[0].lower()):
                abs_ = d.get("absorcoes",{})
                abs_str = ", ".join(f"{k}:{v}" for k,v in abs_.items())
                self._insert_tree(self.tree_protecao,(
                    d.get("nome",""),
                    d.get("peso",""),
                    d.get("nivelBalistico",""),
                    f"{d.get('durabilidade', d.get('durabilidadeMax',100))}/{d.get('durabilidadeMax',100)}",
                    ", ".join(d.get("regioes_cobertas",[])),
                    d.get("regiao_indicada",""),
                    abs_str,
                ))
        except Exception: traceback.print_exc()
    # =========================================================================
    # MUNIÇÕES  (substitua o método template_municoes e carregar_municoes_tree)
    # =========================================================================
    def template_municoes(self):
        self.limpar_container()
        c = self.container_conteudo
        self.section_title(c, "🔴  MUNIÇÕES")

        frm = tk.Frame(c, bg=C["bg_dark"])
        frm.place(x=20, y=58, width=1560, height=580)

        cols = ("Nome", "Calibre", "Dano", "Tipo de Dano", "Perfuração", "Efeitos")
        self.tree_municoes = self._make_tree(frm, cols, [280, 160, 80, 160, 120, 740])
        self.carregar_municoes_tree()

        def _popup_mun(titulo, data=None):
            p = self.build_popup(titulo, 560, 720)
            LX, EX, EW = 20, 185, 340
            y = 58
            fields = {}

            # ── Campos simples ────────────────────────────────────────────────
            for label, key in [
                ("Nome",         "nome"),
                ("Calibre",      "calibre"),
                ("Dano",         "dano"),
                ("Tipo de Dano", "tipo_dano"),
                ("Perfuração",   "perfuracao"),
            ]:
                self.make_label(p, label, LX, y, bg=C["bg_mid"])
                fields[key] = self.make_entry(p, EX, y, EW)
                y += 42

            # ── Descrição ─────────────────────────────────────────────────────
            self.make_label(p, "Descrição", LX, y, bg=C["bg_mid"])
            fields["descricao"] = self.make_text(p, EX, y, EW, 80)
            y += 90

            # ── Pré-preencher campos simples ──────────────────────────────────
            if data:
                fields["nome"].insert(0, data.get("nome", ""))
                fields["calibre"].insert(0, data.get("calibre", ""))
                fields["dano"].insert(0, str(data.get("dano", "")))
                fields["tipo_dano"].insert(0, data.get("tipo_dano", "balístico"))
                fields["perfuracao"].insert(0, str(data.get("perfuracao", 0)))
                fields["descricao"].insert("1.0", data.get("descricao", "") or "")
            else:
                fields["tipo_dano"].insert(0, "balístico")

            # ── Seção de Efeitos ──────────────────────────────────────────────
            self.make_label(p, "Efeitos", LX, y, bg=C["bg_mid"])
            y += 28

            # Container com borda
            efeitos_container = tk.Frame(p, bg=C["bg_card"],
                                         highlightthickness=1,
                                         highlightbackground=C["border"])
            efeitos_container.place(x=LX, y=y, width=510, height=200)

            # Canvas + Scrollbar para a lista de efeitos
            canvas_ef = tk.Canvas(efeitos_container, bg=C["bg_card"], highlightthickness=0)
            sb_ef = tk.Scrollbar(efeitos_container, orient="vertical", command=canvas_ef.yview)
            lista_frame = tk.Frame(canvas_ef, bg=C["bg_card"])

            lista_frame.bind(
                "<Configure>",
                lambda e: canvas_ef.configure(scrollregion=canvas_ef.bbox("all"))
            )
            canvas_ef.create_window((0, 0), window=lista_frame, anchor="nw")
            canvas_ef.configure(yscrollcommand=sb_ef.set)

            canvas_ef.pack(side="left", fill="both", expand=True)
            sb_ef.pack(side="right", fill="y")

            canvas_ef.bind(
                "<Enter>",
                lambda e: canvas_ef.bind_all(
                    "<MouseWheel>",
                    lambda ev: canvas_ef.yview_scroll(int(-1 * (ev.delta / 120)), "units")
                )
            )
            canvas_ef.bind("<Leave>", lambda e: canvas_ef.unbind_all("<MouseWheel>"))

            # Estado interno da lista de efeitos
            efeitos_state = []  # lista de dicts: {"nome": str, "duracao": int/None, "chance": int}

            # Carregar efeitos salvos (suporta formato antigo e novo)
            if data:
                raw = data.get("efeitos", [])
                for ef in raw:
                    if isinstance(ef, dict):
                        efeitos_state.append({
                            "nome":    str(ef.get("nome", ef.get("name", ""))),
                            "duracao": ef.get("duracao", ef.get("duration", "")),
                            "chance":  ef.get("chance", 100),
                        })
                    elif isinstance(ef, str):
                        # formato legado: só nome
                        efeitos_state.append({"nome": ef, "duracao": "", "chance": 100})

            def rebuild_lista():
                for w in lista_frame.winfo_children():
                    w.destroy()

                if not efeitos_state:
                    tk.Label(
                        lista_frame,
                        text="Nenhum efeito adicionado.",
                        fg=C["text_dim"], bg=C["bg_card"],
                        font=("Segoe UI", 9, "italic")
                    ).pack(pady=8, padx=8, anchor="w")
                    return

                # Cabeçalho
                hdr = tk.Frame(lista_frame, bg=C["accent2"])
                hdr.pack(fill="x", padx=4, pady=(4, 2))
                for txt, w in [("Nome do Efeito", 180), ("Duração", 70), ("Chance %", 70), ("", 36)]:
                    tk.Label(hdr, text=txt, fg="white", bg=C["accent2"],
                             font=("Segoe UI", 8, "bold"), width=w // 8,
                             anchor="w").pack(side="left", padx=4)

                for i, ef in enumerate(efeitos_state):
                    row = tk.Frame(lista_frame,
                                   bg=C["bg_card"] if i % 2 == 0 else C["row_alt"])
                    row.pack(fill="x", padx=4, pady=1)

                    # Nome
                    e_nome = tk.Entry(row, font=("Segoe UI", 9),
                                      bg=C["bg_mid"], fg=C["text"],
                                      insertbackground=C["text"],
                                      relief="flat", width=22)
                    e_nome.insert(0, ef["nome"])
                    e_nome.pack(side="left", padx=4, pady=3)

                    # Duração
                    e_dur = tk.Entry(row, font=("Segoe UI", 9),
                                     bg=C["bg_mid"], fg=C["text"],
                                     insertbackground=C["text"],
                                     relief="flat", width=8)
                    e_dur.insert(0, str(ef["duracao"]) if ef["duracao"] != "" else "")
                    e_dur.pack(side="left", padx=4, pady=3)

                    # Chance
                    e_chance = tk.Entry(row, font=("Segoe UI", 9),
                                        bg=C["bg_mid"], fg=C["text"],
                                        insertbackground=C["text"],
                                        relief="flat", width=8)
                    e_chance.insert(0, str(ef.get("chance", 100)))
                    e_chance.pack(side="left", padx=4, pady=3)

                    # Botão remover
                    def _remover(idx=i):
                        efeitos_state.pop(idx)
                        rebuild_lista()

                    tk.Button(row, text="✕", font=("Segoe UI", 8, "bold"),
                              bg=C["red"], fg="white", width=3, relief="flat",
                              cursor="hand2", command=_remover).pack(side="left", padx=4)

                    # Bind para salvar mudanças em tempo real ao sair do campo
                    def _sync(event=None, idx=i, en=e_nome, ed=e_dur, ec=e_chance):
                        efeitos_state[idx]["nome"]    = en.get().strip()
                        efeitos_state[idx]["duracao"] = ed.get().strip()
                        efeitos_state[idx]["chance"]  = ec.get().strip()

                    e_nome.bind("<FocusOut>", _sync)
                    e_dur.bind("<FocusOut>",  _sync)
                    e_chance.bind("<FocusOut>", _sync)

                canvas_ef.configure(scrollregion=canvas_ef.bbox("all"))

            rebuild_lista()

            # ── Botão "＋ Adicionar Efeito" ───────────────────────────────────
            y_btn = y + 208
            def adicionar_efeito():
                efeitos_state.append({"nome": "", "duracao": "", "chance": 100})
                rebuild_lista()
                # Rolar para o final
                canvas_ef.after(50, lambda: canvas_ef.yview_moveto(1.0))

            self.make_btn(p, "＋  Efeito", adicionar_efeito,
                          LX, y_btn, 140, 30, C["blue"])

            # ── Helper para coletar efeitos validados ─────────────────────────
            def _get_efeitos_validados(parent_popup):
                # Sincroniza campos ainda focados
                parent_popup.focus()

                resultado = []
                for ef in efeitos_state:
                    nome_ef = str(ef["nome"]).strip()
                    if not nome_ef:
                        continue  # ignora linhas vazias

                    dur_s = str(ef["duracao"]).strip()
                    try:
                        duracao = int(dur_s) if dur_s else None
                    except ValueError:
                        messagebox.showwarning(
                            "Erro",
                            f"Duração inválida no efeito '{nome_ef}'.",
                            parent=parent_popup
                        )
                        return None

                    chance_s = str(ef["chance"]).strip()
                    try:
                        chance = int(chance_s) if chance_s else 100
                        if not (0 <= chance <= 100):
                            raise ValueError
                    except ValueError:
                        messagebox.showwarning(
                            "Erro",
                            f"Chance inválida no efeito '{nome_ef}' (0–100).",
                            parent=parent_popup
                        )
                        return None

                    resultado.append({
                        "nome":    nome_ef,
                        "duracao": duracao,
                        "chance":  chance,
                    })
                return resultado

            fields["_get_efeitos"] = _get_efeitos_validados
            return p, fields

        # ── Novo ─────────────────────────────────────────────────────────────
        def novo_mun():
            p, fields = _popup_mun("Nova Munição")

            def salvar():
                nome = fields["nome"].get().strip()
                if not nome:
                    messagebox.showwarning("Erro", "Nome obrigatório.", parent=p)
                    return
                if not fields["calibre"].get().strip():
                    messagebox.showwarning("Erro", "Calibre obrigatório.", parent=p)
                    return
                try:
                    dano = int(fields["dano"].get() or 0)
                    perf = int(fields["perfuracao"].get() or 0)
                except:
                    messagebox.showwarning("Erro", "Dano/Perfuração devem ser inteiros.", parent=p)
                    return

                efeitos = fields["_get_efeitos"](p)
                if efeitos is None:
                    return

                dados = D.carregar_municoes_raw()
                if nome in dados:
                    messagebox.showwarning("Duplicado", "Já existe.", parent=p)
                    return

                dados[nome] = {
                    "nome":      nome,
                    "calibre":   fields["calibre"].get().strip(),
                    "dano":      dano,
                    "tipo_dano": fields["tipo_dano"].get().strip(),
                    "perfuracao": perf,
                    "efeitos":   efeitos,
                    "descricao": fields["descricao"].get("1.0", "end").strip(),
                }
                D.salvar_municoes_raw(dados)
                self.carregar_municoes_tree()
                p.destroy()

            self.make_btn(p, "💾  Salvar", salvar, 200, 668, 150, 38, C["green"])

        # ── Editar ────────────────────────────────────────────────────────────
        def editar_mun():
            sel = self.tree_municoes.selection()
            if not sel:
                messagebox.showwarning("Aviso", "Selecione.")
                return
            nome_orig = self.tree_municoes.item(sel[0], "values")[0]
            dados = D.carregar_municoes_raw()
            data = dados.get(nome_orig)
            if not data:
                return

            p, fields = _popup_mun("Editar Munição", data)

            def salvar():
                nome = fields["nome"].get().strip()
                if not nome:
                    messagebox.showwarning("Erro", "Nome obrigatório.", parent=p)
                    return
                try:
                    dano = int(fields["dano"].get() or 0)
                    perf = int(fields["perfuracao"].get() or 0)
                except:
                    messagebox.showwarning("Erro", "Dano/Perfuração inválidos.", parent=p)
                    return

                efeitos = fields["_get_efeitos"](p)
                if efeitos is None:
                    return

                if nome_orig != nome:
                    dados.pop(nome_orig, None)

                dados[nome] = {
                    "nome":      nome,
                    "calibre":   fields["calibre"].get().strip(),
                    "dano":      dano,
                    "tipo_dano": fields["tipo_dano"].get().strip(),
                    "perfuracao": perf,
                    "efeitos":   efeitos,
                    "descricao": fields["descricao"].get("1.0", "end").strip(),
                }
                D.salvar_municoes_raw(dados)
                self.carregar_municoes_tree()
                p.destroy()

            self.make_btn(p, "💾  Salvar", salvar, 200, 668, 150, 38, C["gold"])

        # ── Remover ───────────────────────────────────────────────────────────
        def remover_mun():
            sel = self.tree_municoes.selection()
            if not sel:
                return
            nome = self.tree_municoes.item(sel[0], "values")[0]
            if messagebox.askyesno("Confirmar", f"Remover '{nome}'?"):
                D.remover_municao_raw(nome)
                self.carregar_municoes_tree()

        self._btn_bar(c, novo_mun, editar_mun, remover_mun, y=648)

    def carregar_municoes_tree(self):
        if not hasattr(self, "tree_municoes"):
            return
        self.tree_municoes.delete(*self.tree_municoes.get_children())
        try:
            for nome, d in D.carregar_municoes_raw().items():
                efeitos = d.get("efeitos", [])
                # Formatar efeitos para exibição na tree
                if efeitos and isinstance(efeitos[0], dict):
                    ef_str = ", ".join(
                        f"{e['nome']} ({e.get('chance', 100)}%"
                        + (f" / {e['duracao']}t" if e.get('duracao') else "")
                        + ")"
                        for e in efeitos
                    )
                else:
                    ef_str = ", ".join(str(e) for e in efeitos)

                self._insert_tree(self.tree_municoes, (
                    d.get("nome", ""),
                    d.get("calibre", ""),
                    d.get("dano", ""),
                    d.get("tipo_dano", ""),
                    d.get("perfuracao", ""),
                    self.resumir_texto(ef_str, 80),
                ))
        except Exception:
            traceback.print_exc()
    # =========================================================================
    # CONSUMÍVEIS
    # =========================================================================
    _TIPOS_DANO_CONS = CB.tipos_de_dano

    def template_consumiveis(self):
        self.limpar_container()
        c = self.container_conteudo
        self.section_title(c, "💊  CONSUMÍVEIS")

        frm = tk.Frame(c, bg=C["bg_dark"])
        frm.place(x=20, y=58, width=1560, height=580)

        cols = ("Nome", "Peso", "Uso", "Efeitos")
        self.tree_consumiveis = self._make_tree(frm, cols, [300, 80, 160, 1000])
        self.carregar_consumiveis_tree()

        def novo_cons():
            self._popup_cons("Novo Consumível", None)

        def editar_cons():
            sel = self.tree_consumiveis.selection()
            if not sel:
                messagebox.showwarning("Aviso", "Selecione um consumível.")
                return
            nome_orig = self.tree_consumiveis.item(sel[0], "values")[0]
            dados = D.carregar_consumiveis_raw()
            data  = dados.get(nome_orig)
            if not data:
                return
            self._popup_cons("Editar Consumível", data, nome_orig=nome_orig)

        def remover_cons():
            sel = self.tree_consumiveis.selection()
            if not sel:
                return
            nome = self.tree_consumiveis.item(sel[0], "values")[0]
            if messagebox.askyesno("Confirmar", f"Remover '{nome}'?"):
                D.remover_consumiveis_raw(nome)
                self.carregar_consumiveis_tree()

        self._btn_bar(c, novo_cons, editar_cons, remover_cons, y=648)

    def _popup_cons(self, titulo, data, nome_orig=None):
        """
        Popup para criar/editar consumível.

        Tipos de efeito e campos:
          cura      → valor
          energia   → valor
          mana      → valor
          dano      → subtipo, valor
          dano_area → subtipo, valor, raio, raio_letal, falloff, perfuracao
          buff      → nome, duracao, chance
          debuff    → nome, duracao, chance
        """
        TIPOS_EFEITO = ["cura", "energia", "mana", "dano", "dano_area", "buff", "debuff"]
        FALLOFF_OPS  = ["nenhum", "linear", "quadratico"]

        p = self.build_popup(titulo, 620, 780)
        LX, EX, EW = 20, 190, 390
        fields = {}
        y = 58

        # ── Nome ──────────────────────────────────────────────────────────────
        self.make_label(p, "Nome", LX, y, bg=C["bg_mid"])
        fields["nome"] = self.make_entry(p, EX, y, EW)
        y += 42

        # ── Peso ──────────────────────────────────────────────────────────────
        self.make_label(p, "Peso", LX, y, bg=C["bg_mid"])
        fields["peso"] = self.make_entry(p, EX, y, EW)
        y += 42

        # ── Uso ───────────────────────────────────────────────────────────────
        self.make_label(p, "Uso", LX, y, bg=C["bg_mid"])
        fields["uso"] = self.make_combobox(p, ["Consumivel", "Arremessavel"], EX, y, EW)
        y += 42

        # ── Separador ─────────────────────────────────────────────────────────
        tk.Frame(p, bg=C["accent2"]).place(x=LX, y=y, width=570, height=2)
        y += 8
        tk.Label(p, text="Efeitos", fg=C["accent_hi"], bg=C["bg_mid"],
                 font=("Segoe UI", 10, "bold")).place(x=LX, y=y)
        y += 26

        # ── Container com scroll para os efeitos ──────────────────────────────
        ef_container = tk.Frame(p, bg=C["bg_card"],
                                highlightthickness=1,
                                highlightbackground=C["border"])
        ef_container.place(x=LX, y=y, width=576, height=320)

        canvas_ef = tk.Canvas(ef_container, bg=C["bg_card"], highlightthickness=0)
        sb_ef     = tk.Scrollbar(ef_container, orient="vertical", command=canvas_ef.yview)
        lista_frm = tk.Frame(canvas_ef, bg=C["bg_card"])

        lista_frm.bind("<Configure>",
                       lambda e: canvas_ef.configure(scrollregion=canvas_ef.bbox("all")))
        canvas_ef.create_window((0, 0), window=lista_frm, anchor="nw")
        canvas_ef.configure(yscrollcommand=sb_ef.set)
        canvas_ef.pack(side="left", fill="both", expand=True)
        sb_ef.pack(side="right", fill="y")

        canvas_ef.bind("<Enter>",
            lambda e: canvas_ef.bind_all(
                "<MouseWheel>",
                lambda ev: canvas_ef.yview_scroll(int(-1*(ev.delta/120)), "units")))
        canvas_ef.bind("<Leave>",
            lambda e: canvas_ef.unbind_all("<MouseWheel>"))

        # Estado: lista de dicts com dados brutos de cada efeito
        efeitos_state = []

        # Carregar efeitos existentes
        if data:
            for ef in data.get("efeitos", []):
                if isinstance(ef, dict):
                    efeitos_state.append(dict(ef))

        # ─────────────────────────────────────────────────────────────────────
        # Mapa: idx -> dict de widgets do efeito
        _widgets_map = {}

        def _make_efeito_frame(parent, idx):
            ef_data    = efeitos_state[idx]
            tipo_atual = ef_data.get("tipo", "cura")

            outer = tk.Frame(parent, bg=C["bg_mid"],
                             highlightthickness=1,
                             highlightbackground=C["border"])
            outer.pack(fill="x", padx=6, pady=4)

            # ── cabeçalho ─────────────────────────────────────────────────────
            hdr = tk.Frame(outer, bg=C["accent2"])
            hdr.pack(fill="x")

            tk.Label(hdr, text=f"  Efeito {idx+1}",
                     fg="white", bg=C["accent2"],
                     font=("Segoe UI", 9, "bold")).pack(side="left", padx=4, pady=3)

            cb_tipo = ttk.Combobox(hdr, values=TIPOS_EFEITO,
                                   state="readonly",
                                   font=("Segoe UI", 9), width=12)
            cb_tipo.set(tipo_atual)
            cb_tipo.pack(side="left", padx=6, pady=3)

            def _remover(i=idx):
                efeitos_state.pop(i)
                _rebuild_lista()

            tk.Button(hdr, text="✕ Remover",
                      font=("Segoe UI", 8, "bold"),
                      bg=C["red"], fg="white", relief="flat",
                      cursor="hand2", command=_remover).pack(
                          side="right", padx=6, pady=3)

            # ── corpo com sub-campos ──────────────────────────────────────────
            body = tk.Frame(outer, bg=C["bg_mid"])
            body.pack(fill="x", padx=8, pady=6)

            wids = {}  # chave -> widget

            def _linha(lbl, key, default="", w=10):
                row = tk.Frame(body, bg=C["bg_mid"])
                row.pack(fill="x", pady=2)
                tk.Label(row, text=lbl, fg=C["text_dim"], bg=C["bg_mid"],
                         font=("Segoe UI", 9), width=18,
                         anchor="w").pack(side="left", padx=4)
                e = tk.Entry(row, font=("Segoe UI", 10),
                             bg=C["bg_card"], fg=C["text"],
                             insertbackground=C["text"],
                             relief="flat", width=w)
                e.insert(0, str(ef_data.get(key, default)))
                e.pack(side="left", padx=4)
                wids[key] = e

            def _combo(lbl, key, opcoes, default=""):
                row = tk.Frame(body, bg=C["bg_mid"])
                row.pack(fill="x", pady=2)
                tk.Label(row, text=lbl, fg=C["text_dim"], bg=C["bg_mid"],
                         font=("Segoe UI", 9), width=18,
                         anchor="w").pack(side="left", padx=4)
                cb = ttk.Combobox(row, values=opcoes, state="readonly",
                                  font=("Segoe UI", 9), width=18)
                cb.set(str(ef_data.get(key, default) or default))
                cb.pack(side="left", padx=4)
                wids[key] = cb

            def _rebuild_body(event=None):
                for w in body.winfo_children():
                    w.destroy()
                wids.clear()

                tp = cb_tipo.get()

                if tp in ("cura", "energia", "mana"):
                    _linha("Valor", "valor", 0)

                elif tp == "dano":
                    _combo("Subtipo de dano", "subtipo",
                           self._TIPOS_DANO_CONS, "balístico")
                    _linha("Valor", "valor", 0)

                elif tp == "dano_area":
                    _combo("Subtipo de dano", "subtipo",
                           self._TIPOS_DANO_CONS, "explosivo")
                    _linha("Valor do dano",    "valor",      0)
                    _linha("Raio (m)",          "raio",       3)
                    _linha("Raio letal (m)",    "raio_letal", "")
                    _combo("Falloff",           "falloff",
                           FALLOFF_OPS, "linear")
                    _linha("Perfuração",        "perfuracao", 0)

                elif tp in ("buff", "debuff"):
                    _linha("Nome do efeito", "nome",    "", w=22)
                    _linha("Duração (turnos)", "duracao", 1)
                    _linha("Chance (0-100)", "chance",  100)

                canvas_ef.after(30, lambda: canvas_ef.configure(
                    scrollregion=canvas_ef.bbox("all")))

            cb_tipo.bind("<<ComboboxSelected>>", _rebuild_body)
            _rebuild_body()

            _widgets_map[idx] = (wids, cb_tipo)

        # ─────────────────────────────────────────────────────────────────────
        def _rebuild_lista():
            for w in lista_frm.winfo_children():
                w.destroy()
            _widgets_map.clear()

            if not efeitos_state:
                tk.Label(lista_frm,
                         text="Nenhum efeito. Clique em ＋ Efeito.",
                         fg=C["text_dim"], bg=C["bg_card"],
                         font=("Segoe UI", 9, "italic")).pack(
                             pady=12, padx=8, anchor="w")
                canvas_ef.configure(scrollregion=canvas_ef.bbox("all"))
                return

            for i in range(len(efeitos_state)):
                _make_efeito_frame(lista_frm, i)

            canvas_ef.after(30, lambda: canvas_ef.configure(
                scrollregion=canvas_ef.bbox("all")))

        _rebuild_lista()

        # ── Botão ＋ Efeito ────────────────────────────────────────────────────
        y_btn = y + 328
        def _adicionar():
            efeitos_state.append({"tipo": "cura"})
            _rebuild_lista()
            canvas_ef.after(60, lambda: canvas_ef.yview_moveto(1.0))

        self.make_btn(p, "＋  Efeito", _adicionar, LX, y_btn, 140, 30, C["blue"])

        # ── Descrição ─────────────────────────────────────────────────────────
        y_desc = y_btn + 40
        self.make_label(p, "Descrição", LX, y_desc, bg=C["bg_mid"])
        fields["descricao"] = self.make_text(p, EX, y_desc, EW, 80)

        # ── Pré-preencher campos fixos ────────────────────────────────────────
        if data:
            fields["nome"].insert(0, data.get("nome", ""))
            fields["peso"].insert(0, str(data.get("peso", "") or ""))
            fields["uso"].set(data.get("uso", "Consumivel"))
            fields["descricao"].insert("1.0", data.get("descricao", "") or "")

        # ── Coletar e validar efeitos ─────────────────────────────────────────
        def _coletar_efeitos():
            resultado = []
            for i, (wids, cb_tp) in _widgets_map.items():
                tp = cb_tp.get()
                ef = {"tipo": tp}

                def _int(key, label, minval=None):
                    raw = wids[key].get().strip() if key in wids else "0"
                    if not raw:
                        return 0, True
                    try:
                        v = int(raw)
                        if minval is not None and v < minval:
                            raise ValueError
                        return v, True
                    except ValueError:
                        msg = f"Efeito {i+1}: '{label}' deve ser inteiro"
                        if minval is not None:
                            msg += f" ≥ {minval}"
                        messagebox.showwarning("Erro", msg + ".", parent=p)
                        return None, False

                # ── Cura / Energia / Mana ─────────────────────────────────────
                if tp in ("cura", "energia", "mana"):
                    val, ok = _int("valor", "Valor")
                    if not ok:
                        return None
                    ef["valor"] = val
                    # alvo explícito para o Personagem.aplicar_efeito_com_chance
                    if tp == "cura":
                        ef["alvo"] = "vida"
                        ef["tipo"] = "cura"
                    elif tp == "energia":
                        ef["alvo"] = "energia"
                        ef["tipo"] = "cura"      # reutiliza o branch "cura" + alvo
                    else:
                        ef["alvo"] = "mana"
                        ef["tipo"] = "cura"

                # ── Dano direto ───────────────────────────────────────────────
                elif tp == "dano":
                    ef["subtipo"] = wids["subtipo"].get() if "subtipo" in wids else ""
                    val, ok = _int("valor", "Valor")
                    if not ok:
                        return None
                    ef["valor"] = val

                # ── Dano em área ──────────────────────────────────────────────
                elif tp == "dano_area":
                    ef["subtipo"] = wids["subtipo"].get() if "subtipo" in wids else ""
                    val, ok = _int("valor", "Valor do dano")
                    if not ok:
                        return None
                    ef["valor"] = val

                    raio, ok2 = _int("raio", "Raio", minval=1)
                    if not ok2:
                        return None
                    ef["raio"] = raio

                    # Raio letal: opcional (vazio = None)
                    rl_raw = wids["raio_letal"].get().strip() if "raio_letal" in wids else ""
                    if rl_raw:
                        try:
                            ef["raio_letal"] = int(rl_raw)
                        except ValueError:
                            messagebox.showwarning(
                                "Erro",
                                f"Efeito {i+1}: 'Raio letal' deve ser inteiro.",
                                parent=p)
                            return None
                    else:
                        ef["raio_letal"] = None

                    ef["falloff"]    = wids["falloff"].get() if "falloff" in wids else "linear"
                    perf, ok3 = _int("perfuracao", "Perfuração")
                    if not ok3:
                        return None
                    ef["perfuracao"] = perf

                # ── Buff / Debuff ─────────────────────────────────────────────
                elif tp in ("buff", "debuff"):
                    nome_ef = wids["nome"].get().strip() if "nome" in wids else ""
                    if not nome_ef:
                        messagebox.showwarning(
                            "Erro",
                            f"Efeito {i+1}: Nome do efeito é obrigatório.",
                            parent=p)
                        return None
                    ef["nome"] = nome_ef

                    dur, ok = _int("duracao", "Duração", minval=1)
                    if not ok:
                        return None
                    ef["duracao"] = dur

                    chance, ok2 = _int("chance", "Chance")
                    if not ok2:
                        return None
                    if not (0 <= chance <= 100):
                        messagebox.showwarning(
                            "Erro",
                            f"Efeito {i+1}: Chance deve ser entre 0 e 100.",
                            parent=p)
                        return None
                    ef["chance"] = chance

                resultado.append(ef)
            return resultado

        # ── Salvar ────────────────────────────────────────────────────────────
        def _salvar():
            nome = fields["nome"].get().strip()
            if not nome:
                messagebox.showwarning("Erro", "Nome obrigatório.", parent=p)
                return

            peso_s = fields["peso"].get().strip()
            try:
                peso = float(peso_s) if peso_s else None
            except ValueError:
                messagebox.showwarning("Erro", "Peso inválido.", parent=p)
                return

            efeitos = _coletar_efeitos()
            if efeitos is None:
                return

            dados = D.carregar_consumiveis_raw()

            if nome_orig is None and nome in dados:
                messagebox.showwarning("Duplicado", "Já existe.", parent=p)
                return

            if nome_orig and nome_orig != nome:
                dados.pop(nome_orig, None)

            dados[nome] = {
                "nome":      nome,
                "peso":      peso,
                "uso":       fields["uso"].get(),
                "efeitos":   efeitos,
                "descricao": fields["descricao"].get("1.0", "end").strip(),
            }

            D.salvar_consumiveis_raw(dados)
            self.carregar_consumiveis_tree()
            p.destroy()

        cor_btn = C["gold"] if nome_orig else C["green"]
        self.make_btn(p, "💾  Salvar", _salvar,
                      220, y_desc + 92, 160, 38, cor_btn)

    def carregar_consumiveis_tree(self):
        if not hasattr(self, "tree_consumiveis"):
            return
        self.tree_consumiveis.delete(*self.tree_consumiveis.get_children())
        try:
            for nome, d in D.carregar_consumiveis_raw().items():
                partes = []
                for ef in d.get("efeitos", []):
                    if not isinstance(ef, dict):
                        partes.append(str(ef))
                        continue
                    tp = ef.get("tipo", "")

                    if tp == "cura":
                        alvo = ef.get("alvo", "vida")
                        partes.append(f"Cura {alvo} +{ef.get('valor', 0)}")

                    elif tp in ("energia", "mana"):
                        partes.append(f"{tp.capitalize()} +{ef.get('valor', 0)}")

                    elif tp == "dano":
                        partes.append(
                            f"Dano {ef.get('subtipo','?')} {ef.get('valor',0)}")

                    elif tp == "dano_area":
                        partes.append(
                            f"Área {ef.get('subtipo','?')} {ef.get('valor',0)}"
                            f" r{ef.get('raio','?')}m")

                    elif tp in ("buff", "debuff"):
                        partes.append(
                            f"{tp.capitalize()} '{ef.get('nome','?')}'"
                            f" {ef.get('duracao',1)}t"
                            f" {ef.get('chance',100)}%")

                    else:
                        partes.append(tp)

                ef_str = " | ".join(partes) if partes else "—"

                self._insert_tree(self.tree_consumiveis, (
                    d.get("nome", ""),
                    d.get("peso", ""),
                    d.get("uso", ""),
                    self.resumir_texto(ef_str, 120),
                ))
        except Exception:
            traceback.print_exc()
    # =========================================================================
    # MELHORIAS
    # =========================================================================
    TIPOS_MELHORIA = ["melee", "ranged", "protecao"]
    ATRIBUTOS_MELHORIA = {
        "melee": ["dano", "critico_multiplicador", "valor_critico", "peso", "mod_acerto", "ignora_armadura", "maos"],
        "ranged": ["dano", "recuo", "MaxRange", "MinRange", "ShortCrit", "MediumCrit", "LongCrit", "capacidade", "peso", "ruido", "TPM"],
        "protecao": ["nivelBalistico", "peso", "durabilidade", "absorcao_extra"]
    }

    def _criar_campos_modificadores(self, parent, tipo, mods_existentes=None):
        """Cria campos de modificadores com layout melhorado"""
        campos = {}
        atributos = self.ATRIBUTOS_MELHORIA.get(tipo.lower(), [])
        
        if not atributos:
            tk.Label(parent, text="Nenhum atributo disponível", 
                    fg=C["text_dim"], bg=C["bg_card"],
                    font=("Segoe UI", 9)).pack(pady=10)
            return campos
        
        for atr in atributos:
            # Frame para cada linha
            row = tk.Frame(parent, bg=C["bg_card"])
            row.pack(fill="x", padx=4, pady=3)
            
            # Label do atributo (esquerda)
            tk.Label(row, text=atr, fg=C["text"], bg=C["bg_card"], 
                    font=("Segoe UI", 9), width=22, anchor="w").pack(side="left", padx=4)
            
            # Entry (direita)
            e = tk.Entry(row, font=("Segoe UI", 10), bg=C["bg_mid"], 
                        fg=C["text"], bd=1, relief="flat", 
                        insertbackground=C["text"], width=12)
            e.pack(side="left", padx=4, fill="x", expand=True)
            
            # Preencher com valor existente
            if mods_existentes and atr in mods_existentes:
                e.insert(0, str(mods_existentes[atr]))
            
            campos[atr] = e
        
        return campos

    def _criar_campos_absorcoes(self, parent, mods_existentes=None):
        """Cria campos de absorção para proteção com layout melhorado"""
        campos = {}
        tipos_dano = sorted(CB.tipos_de_dano) if hasattr(CB, 'tipos_de_dano') else [
            "balístico", "congelante", "cortante", "explosivo", 
            "incendiário", "mental", "perfurante"
        ]
        
        for tipo in tipos_dano:
            # Frame para cada linha
            row = tk.Frame(parent, bg=C["bg_card"])
            row.pack(fill="x", padx=4, pady=3)
            
            # Label do tipo de dano (esquerda)
            tk.Label(row, text=tipo.capitalize(), fg=C["text"], bg=C["bg_card"],
                    font=("Segoe UI", 9), width=22, anchor="w").pack(side="left", padx=4)
            
            # Entry (direita)
            e = tk.Entry(row, font=("Segoe UI", 10), bg=C["bg_mid"],
                        fg=C["text"], bd=1, relief="flat",
                        insertbackground=C["text"], width=12)
            e.pack(side="left", padx=4, fill="x", expand=True)
            e.insert(0, "0")
            
            # Preencher com valor existente
            if mods_existentes and tipo in mods_existentes:
                e.delete(0, tk.END)
                e.insert(0, str(mods_existentes[tipo]))
            
            campos[tipo] = e
        
        return campos

    def template_melhorias(self):
        """Template principal da seção de melhorias"""
        self.limpar_container()
        c = self.container_conteudo
        self.section_title(c, "🔧  MELHORIAS")
        frm = tk.Frame(c, bg=C["bg_dark"])
        frm.place(x=20, y=58, width=1560, height=580)
        cols = ("Nome", "Peso", "Tipo", "Modificadores")
        self.tree_melhorias = self._make_tree(frm, cols, [300, 100, 160, 980])
        self.carregar_melhorias_tree()

        def _load():
            return D.carregar_melhorias_raw() if hasattr(D, "carregar_melhorias_raw") else {}
        
        def _save(d):
            if hasattr(D, "salvar_melhorias_raw"):
                D.salvar_melhorias_raw(d)

        def _popup_mel(titulo, data=None):
            """Popup para criar/editar melhorias com scroll CORRIGIDO"""
            p = self.build_popup(titulo, 560, 620)
            LX, EX, EW = 20, 200, 320
            y = 58
            fields = {}
            
            # ── Campo Nome ────────────────────────────────────────────────────
            self.make_label(p, "Nome", LX, y, bg=C["bg_mid"])
            fields["nome"] = self.make_entry(p, EX, y, EW)
            y += 42
            
            # ── Campo Peso ────────────────────────────────────────────────────
            self.make_label(p, "Peso", LX, y, bg=C["bg_mid"])
            fields["peso"] = self.make_entry(p, EX, y, EW)
            y += 42
            
            # ── Campo Tipo ────────────────────────────────────────────────────
            self.make_label(p, "Tipo", LX, y, bg=C["bg_mid"])
            fields["tipo"] = self.make_combobox(p, self.TIPOS_MELHORIA, EX, y, EW)
            y += 42
            
            # ── Título Modificadores ──────────────────────────────────────────
            self.make_label(p, "Modificadores", LX, y, bg=C["bg_mid"])
            y += 28
            
            # ── Frame container com borda e scroll ─────────────────────────────
            container = tk.Frame(p, bg=C["bg_card"], bd=1, relief="sunken")
            container.place(x=EX, y=y, width=EW, height=280)
            
            # Canvas + Scrollbar
            canvas = tk.Canvas(container, bg=C["bg_card"], highlightthickness=0)
            scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
            scroll_frame = tk.Frame(canvas, bg=C["bg_card"])
            
            # Configurar o canvas
            canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Atualizar scroll region quando o conteúdo mudar
            def on_frame_configure(event):
                canvas.configure(scrollregion=canvas.bbox("all"))
            
            scroll_frame.bind("<Configure>", on_frame_configure)
            
            # Pack
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # ── Mousewheel support ────────────────────────────────────────────
            def on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            
            def bind_mousewheel(e):
                canvas.bind_all("<MouseWheel>", on_mousewheel)
            
            def unbind_mousewheel(e):
                canvas.unbind_all("<MouseWheel>")
            
            container.bind("<Enter>", bind_mousewheel)
            container.bind("<Leave>", unbind_mousewheel)
            
            fields["mod_campos"] = {}

            def atualizar_tipo(event=None):
                # Limpar campos anteriores
                for w in scroll_frame.winfo_children():
                    w.destroy()
                fields["mod_campos"] = {}
                
                # Pegar tipo selecionado
                tipo = fields["tipo"].get() or "melee"
                mods_exist = data.get("modificadores", {}) if data else {}
                
                # Criar campos apropriados para o tipo
                if tipo.lower() == "protecao":
                    campos = self._criar_campos_absorcoes(scroll_frame, mods_exist)
                else:
                    campos = self._criar_campos_modificadores(scroll_frame, tipo, mods_exist)
                
                fields["mod_campos"] = campos
                
                # Forçar atualização do scroll region
                scroll_frame.update_idletasks()
                canvas.configure(scrollregion=canvas.bbox("all"))

            # Bind do combobox
            fields["tipo"].bind("<<ComboboxSelected>>", atualizar_tipo)
            
            # Preencher dados se estiver editando
            if data:
                fields["nome"].insert(0, data.get("nome", ""))
                fields["peso"].insert(0, str(data.get("peso", "")))
                fields["tipo"].set(data.get("tipo", "melee"))
            
            # Atualizar tipo inicial
            atualizar_tipo()
            
            return p, fields

        def novo_mel():
            p, fields = _popup_mel("Nova Melhoria")
            def salvar():
                nome = fields["nome"].get().strip()
                if not nome:
                    messagebox.showwarning("Erro", "Nome obrigatório.", parent=p)
                    return
                peso_s = fields["peso"].get().strip()
                try:
                    peso = float(peso_s) if peso_s else None
                except:
                    messagebox.showwarning("Erro", "Peso inválido.", parent=p)
                    return
                mods = {}
                for atr, entry in fields["mod_campos"].items():
                    v = entry.get().strip()
                    if v:
                        try:
                            mods[atr] = float(v)
                        except:
                            mods[atr] = v
                dados = _load()
                if nome in dados:
                    messagebox.showwarning("Duplicado", "Já existe.", parent=p)
                    return
                dados[nome] = {"nome": nome, "peso": peso, "tipo": fields["tipo"].get(), "modificadores": mods}
                _save(dados)
                self.carregar_melhorias_tree()
                p.destroy()
            self.make_btn(p, "💾  Salvar", salvar, 200, 545, 150, 38, C["green"])

        def editar_mel():
            sel = self.tree_melhorias.selection()
            if not sel:
                messagebox.showwarning("Aviso", "Selecione uma melhoria.")
                return
            item = self.tree_melhorias.item(sel[0])
            nome_orig = item["values"][0] if item["values"] else None
            if not nome_orig:
                messagebox.showwarning("Erro", "Não foi possível obter o nome.")
                return
            dados = _load()
            data = dados.get(nome_orig)
            if not data:
                messagebox.showwarning("Erro", "Melhoria não encontrada.")
                return
            p, fields = _popup_mel("Editar Melhoria", data)
            def salvar():
                nome = fields["nome"].get().strip()
                if not nome:
                    messagebox.showwarning("Erro", "Nome obrigatório.", parent=p)
                    return
                peso_s = fields["peso"].get().strip()
                try:
                    peso = float(peso_s) if peso_s else None
                except:
                    messagebox.showwarning("Erro", "Peso inválido.", parent=p)
                    return
                mods = {}
                for atr, entry in fields["mod_campos"].items():
                    v = entry.get().strip()
                    if v:
                        try:
                            mods[atr] = float(v)
                        except:
                            mods[atr] = v
                if nome_orig != nome:
                    dados.pop(nome_orig, None)
                dados[nome] = {"nome": nome, "peso": peso, "tipo": fields["tipo"].get(), "modificadores": mods}
                _save(dados)
                self.carregar_melhorias_tree()
                p.destroy()
            self.make_btn(p, "💾  Salvar", salvar, 200, 545, 150, 38, C["gold"])

        def remover_mel():
            sel = self.tree_melhorias.selection()
            if not sel:
                messagebox.showwarning("Aviso", "Selecione uma melhoria.")
                return
            item = self.tree_melhorias.item(sel[0])
            nome = item["values"][0] if item["values"] else None
            if not nome:
                messagebox.showwarning("Erro", "Não foi possível obter o nome.")
                return
            if messagebox.askyesno("Confirmar", f"Remover '{nome}'?"):
                dados = _load()
                if nome in dados:
                    del dados[nome]
                    _save(dados)
                self.carregar_melhorias_tree()

        self._btn_bar(c, novo_mel, editar_mel, remover_mel, y=648)

    def carregar_melhorias_tree(self):
        """Carrega melhorias na tree"""
        if not hasattr(self, "tree_melhorias"):
            return
        self.tree_melhorias.delete(*self.tree_melhorias.get_children())
        try:
            if not hasattr(D, "carregar_melhorias_raw"):
                return
            fonte = D.carregar_melhorias_raw()
            if not fonte:
                return
            for nome, d in fonte.items():
                nome_v = d.get("nome", "")
                peso_v = d.get("peso", "")
                tipo_v = d.get("tipo", "")
                mods = d.get("modificadores", {})
                mods_str = self._formatar_mods_resumido(mods, tipo_v)
                self._insert_tree(self.tree_melhorias, (nome_v, peso_v, tipo_v, self.resumir_texto(mods_str, 60)))
        except Exception as e:
            print(f"Erro: {e}")

    def _formatar_mods_resumido(self, mods, tipo):
        """Formata modificadores resumidos"""
        if not mods:
            return "—"
        partes = []
        if tipo.lower() == "melee":
            if mods.get("dano"): partes.append(f"Dano +{mods['dano']}")
            if mods.get("critico_multiplicador"): partes.append(f"CritM ×{mods['critico_multiplicador']}")
            if mods.get("valor_critico"): partes.append(f"CritV +{mods['valor_critico']}")
            if mods.get("mod_acerto"): partes.append(f"Acerto +{mods['mod_acerto']}")
            if mods.get("ignora_armadura"): partes.append(f"IgnArm +{mods['ignora_armadura']}")
            if mods.get("peso"): partes.append(f"Peso {mods['peso']}")
            if mods.get("maos"): partes.append(f"Mãos +{mods['maos']}")
        elif tipo.lower() == "ranged":
            if mods.get("dano"): partes.append(f"Dano +{mods['dano']}")
            if mods.get("recuo"): partes.append(f"Recuo +{mods['recuo']}")
            if mods.get("MaxRange"): partes.append(f"MaxR +{mods['MaxRange']}")
            if mods.get("MinRange"): partes.append(f"MinR +{mods['MinRange']}")
            if mods.get("ShortCrit"): partes.append(f"SC +{mods['ShortCrit']}")
            if mods.get("MediumCrit"): partes.append(f"MC +{mods['MediumCrit']}")
            if mods.get("LongCrit"): partes.append(f"LC +{mods['LongCrit']}")
            if mods.get("capacidade"): partes.append(f"Cap +{mods['capacidade']}")
            if mods.get("peso"): partes.append(f"Peso {mods['peso']}")
        elif tipo.lower() == "protecao":
            if mods.get("nivelBalistico"): partes.append(f"NB +{mods['nivelBalistico']}")
            if mods.get("durabilidade"): partes.append(f"Dur +{mods['durabilidade']}")
            if mods.get("peso"): partes.append(f"Peso {mods['peso']}")
        return " | ".join(partes) if partes else "—"
    # =========================================================================
    # BUFFS E DEBUFFS
    # =========================================================================
    BUFF_TIPOS_DANO = [
        "contundente", "concussivo", "cortante", "perfurante", "balístico",
        "rasgante", "explosivo", "incendiário", "congelante", "envenenante",
        "eletrocutante", "mental",
    ]
    BUFF_TIPOS_TESTE = [
        "iniciativa", "sorte", "força", "agilidade", "vigor", "inteligencia",
        "presença", "tática", "poder", "físico", "mental", "vocal", "qualquer teste",
    ]
    BUFF_PALAVRAS_CHAVE = [
        "vida", "energia", "mana",
        "vidaMax", "energiaMax", "manaMax",
        "movimentação", "bloqueio", "esquiva", "carga", "percepção",
    ]
    BUFF_RESISTENCIAS = [
        f"resistencia_{t}" for t in [
            "contundente", "concussivo", "cortante", "perfurante", "balístico",
            "rasgante", "explosivo", "incendiário", "congelante", "envenenante",
            "eletrocutante", "mental",
        ]
    ]
    BUFF_DESARMADO = ["desarmado_dano", "desarmado_crit_mult", "desarmado_crit_valor"]
    BUFF_CATEGORIAS = ["Tipos de Dano", "Tipos de Teste", "Palavras-chave", "Resistências", "Desarmado"]

    def _opcoes_para_categoria(self, cat):
        if cat == "Tipos de Dano":
            return self.BUFF_TIPOS_DANO
        if cat == "Tipos de Teste":
            return self.BUFF_TIPOS_TESTE
        if cat == "Palavras-chave":
            return self.BUFF_PALAVRAS_CHAVE
        if cat == "Resistências":
            return self.BUFF_RESISTENCIAS
        if cat == "Desarmado":
            return self.BUFF_DESARMADO
        return []

    def _detectar_categoria(self, tag):
        if tag in self.BUFF_TIPOS_DANO:
            return "Tipos de Dano"
        if tag in self.BUFF_TIPOS_TESTE:
            return "Tipos de Teste"
        if tag in self.BUFF_RESISTENCIAS:
            return "Resistências"
        if tag in self.BUFF_DESARMADO:
            return "Desarmado"
        return "Palavras-chave"

    def template_buffs_debuffs(self):
        self.limpar_container()
        c = self.container_conteudo
        self.section_title(c, "✨  BUFFS E DEBUFFS")

        frm = tk.Frame(c, bg=C["bg_dark"])
        frm.place(x=20, y=58, width=1560, height=580)

        cols = ("Nome", "Tipo", "Efeitos", "Descrição")
        self.tree_buffs = self._make_tree(frm, cols, [220, 100, 440, 780])
        self.carregar_buffs_tree()

        # ── Popup compartilhado ───────────────────────────────────────────────
        def _popup_buff(titulo, data=None):
            p = self.build_popup(titulo, 620, 680)
            p.resizable(False, True)
            LX, EX, EW = 20, 190, 390
            y = 58

            # ── Nome ─────────────────────────────────────────────────────────
            self.make_label(p, "Nome", LX, y, bg=C["bg_mid"])
            f_nome = self.make_entry(p, EX, y, EW)
            y += 42

            # ── Tipo ─────────────────────────────────────────────────────────
            self.make_label(p, "Tipo", LX, y, bg=C["bg_mid"])
            f_tipo = self.make_combobox(p, ["buff", "debuff"], EX, y, EW)
            y += 42

            # ── Separador + título Efeitos ────────────────────────────────────
            tk.Frame(p, bg=C["accent2"]).place(x=LX, y=y, width=580, height=2)
            y += 10
            tk.Label(p, text="Efeitos", fg=C["accent_hi"], bg=C["bg_mid"],
                     font=("Segoe UI", 10, "bold")).place(x=LX, y=y)
            y += 32

            # ── Frame scrollável para lista de efeitos ────────────────────────
            frame_efeitos_outer = tk.Frame(p, bg=C["bg_mid"], bd=1, relief="sunken")
            frame_efeitos_outer.place(x=LX, y=y, width=580, height=340)

            canvas_ef = tk.Canvas(frame_efeitos_outer, bg=C["bg_mid"],
                                  highlightthickness=0)
            sb_ef = ttk.Scrollbar(frame_efeitos_outer, orient="vertical",
                                  command=canvas_ef.yview)
            canvas_ef.configure(yscrollcommand=sb_ef.set)
            sb_ef.pack(side="right", fill="y")
            canvas_ef.pack(side="left", fill="both", expand=True)

            frame_lista = tk.Frame(canvas_ef, bg=C["bg_mid"])
            canvas_win = canvas_ef.create_window((0, 0), window=frame_lista,
                                                 anchor="nw")

            def _on_resize(evt):
                canvas_ef.itemconfig(canvas_win, width=evt.width)
            canvas_ef.bind("<Configure>", _on_resize)

            def _scroll_update(*_):
                frame_lista.update_idletasks()
                canvas_ef.configure(scrollregion=canvas_ef.bbox("all"))
            frame_lista.bind("<Configure>", _scroll_update)

            # Mousewheel
            def _mw(evt):
                canvas_ef.yview_scroll(int(-1 * (evt.delta / 120)), "units")
            canvas_ef.bind_all("<MouseWheel>", _mw)
            p.bind("<Destroy>", lambda e: canvas_ef.unbind_all("<MouseWheel>"))

            # ── Estado: lista de linhas de efeito ─────────────────────────────
            linhas_efeito = []   # cada item: {"cat": StringVar, "tag": StringVar, "val": StringVar, "frame": Frame}

            def _rebuild_efeitos():
                """Redesenha todos os blocos de efeito no frame_lista."""
                for w in frame_lista.winfo_children():
                    w.destroy()

                for idx, linha in enumerate(linhas_efeito):
                    bloco = tk.Frame(frame_lista, bg=C["bg_dark"],
                                     relief="ridge", bd=1)
                    bloco.pack(fill="x", padx=6, pady=4)
                    linha["frame"] = bloco

                    # Linha 1: Categoria + botão remover
                    row1 = tk.Frame(bloco, bg=C["bg_dark"])
                    row1.pack(fill="x", padx=8, pady=(6, 2))

                    tk.Label(row1, text="Categoria", fg=C["text_dim"],
                             bg=C["bg_dark"],
                             font=("Segoe UI", 9)).pack(side="left", padx=(0, 6))

                    cat_cb = ttk.Combobox(row1, textvariable=linha["cat"],
                                         values=self.BUFF_CATEGORIAS,
                                         state="readonly",
                                         font=("Segoe UI", 10), width=18)
                    cat_cb.pack(side="left", padx=(0, 10))

                    # Botão remover (captura idx por closure)
                    def _remover(i=idx):
                        linhas_efeito.pop(i)
                        _rebuild_efeitos()

                    tk.Button(row1, text="✕ Remover", fg=C["red"],
                              bg=C["bg_dark"], activebackground=C["bg_mid"],
                              activeforeground=C["red"], bd=0,
                              font=("Segoe UI", 9, "bold"),
                              cursor="hand2",
                              command=_remover).pack(side="right", padx=4)

                    # Linha 2: Efeito (tag) + Valor
                    row2 = tk.Frame(bloco, bg=C["bg_dark"])
                    row2.pack(fill="x", padx=8, pady=(2, 6))

                    tk.Label(row2, text="Efeito", fg=C["text_dim"],
                             bg=C["bg_dark"],
                             font=("Segoe UI", 9)).pack(side="left", padx=(0, 6))

                    opcoes_ini = self._opcoes_para_categoria(linha["cat"].get())
                    tag_cb = ttk.Combobox(row2, textvariable=linha["tag"],
                                         values=opcoes_ini,
                                         state="readonly",
                                         font=("Segoe UI", 10), width=22)
                    tag_cb.pack(side="left", padx=(0, 14))

                    tk.Label(row2, text="Valor", fg=C["text_dim"],
                             bg=C["bg_dark"],
                             font=("Segoe UI", 9)).pack(side="left", padx=(0, 4))

                    val_entry = tk.Entry(row2, textvariable=linha["val"],
                                        bg=C["bg_input"], fg=C["text"],
                                        insertbackground=C["text"],
                                        font=("Segoe UI", 10), width=8,
                                        relief="flat")
                    val_entry.pack(side="left")

                    tk.Label(row2, text="(ex: -3, 10)", fg=C["text_dim"],
                             bg=C["bg_dark"],
                             font=("Segoe UI", 8, "italic")).pack(side="left",
                                                                   padx=6)

                    # Atualiza tags ao trocar categoria
                    def _cat_changed(evt, l=linha, cb=tag_cb):
                        novas = self._opcoes_para_categoria(l["cat"].get())
                        cb["values"] = novas
                        if l["tag"].get() not in novas:
                            l["tag"].set(novas[0] if novas else "")
                    cat_cb.bind("<<ComboboxSelected>>", _cat_changed)

                _scroll_update()

            def _adicionar_linha(cat="Tipos de Teste", tag=None, val="0"):
                opcoes = self._opcoes_para_categoria(cat)
                tag_val = tag if tag in opcoes else (opcoes[0] if opcoes else "")
                linhas_efeito.append({
                    "cat": tk.StringVar(value=cat),
                    "tag": tk.StringVar(value=tag_val),
                    "val": tk.StringVar(value=str(val)),
                    "frame": None,
                })
                _rebuild_efeitos()

            # ── Botão "+ Adicionar Efeito" ────────────────────────────────────
            y_btn_add = y + 348
            tk.Button(p, text="＋  Adicionar Efeito",
                      fg=C["accent_hi"], bg=C["bg_mid"],
                      activebackground=C["bg_dark"],
                      activeforeground=C["accent_hi"],
                      bd=0, font=("Segoe UI", 10, "bold"),
                      cursor="hand2",
                      command=_adicionar_linha).place(x=LX, y=y_btn_add,
                                                      width=200, height=30)

            # ── Descrição ─────────────────────────────────────────────────────
            y_desc = y_btn_add + 38
            self.make_label(p, "Descrição", LX, y_desc, bg=C["bg_mid"])
            f_desc = self.make_text(p, EX, y_desc, EW, 80)

            # ── Pré-preencher ao editar ───────────────────────────────────────
            if data:
                f_nome.insert(0, data.get("nome", ""))
                f_tipo.set(data.get("tipo", "buff"))
                f_desc.insert("1.0", data.get("descricao", "") or "")

                efeitos_raw = data.get("efeito", [])
                # Compatibilidade: dict único → lista
                if isinstance(efeitos_raw, dict):
                    efeitos_raw = [efeitos_raw]
                # Formato antigo com "atributo" → converte para "tags"
                for ef in efeitos_raw:
                    if isinstance(ef, dict):
                        tag_salva = ef.get("tags", [ef.get("atributo", "")])
                        if isinstance(tag_salva, list):
                            tag_salva = tag_salva[0] if tag_salva else ""
                        cat_salva = self._detectar_categoria(tag_salva)
                        val_salvo = ef.get("valor", 0)
                        _adicionar_linha(cat=cat_salva, tag=tag_salva,
                                         val=str(val_salvo))
            else:
                _adicionar_linha()  # Começa com 1 linha em branco

            return p, f_nome, f_tipo, f_desc, linhas_efeito

        # ── Coletar e validar dados do popup ──────────────────────────────────
        def _coletar(p, f_nome, f_tipo, f_desc, linhas_efeito):
            nome = f_nome.get().strip()
            if not nome:
                messagebox.showwarning("Erro", "Nome obrigatório.", parent=p)
                return None

            tipo = f_tipo.get()
            if tipo not in ("buff", "debuff"):
                messagebox.showwarning("Erro", "Tipo deve ser 'buff' ou 'debuff'.",
                                       parent=p)
                return None

            if not linhas_efeito:
                messagebox.showwarning("Erro", "Adicione ao menos um efeito.",
                                       parent=p)
                return None

            efeitos_out = []
            for i, linha in enumerate(linhas_efeito, 1):
                tag = linha["tag"].get().strip()
                if not tag:
                    messagebox.showwarning(
                        "Erro", f"Efeito #{i}: selecione um atributo.", parent=p)
                    return None
                val_s = linha["val"].get().strip()
                try:
                    val = int(val_s) if val_s else 0
                except ValueError:
                    try:
                        val = float(val_s)
                    except ValueError:
                        messagebox.showwarning(
                            "Erro",
                            f"Efeito #{i}: valor inválido '{val_s}'.", parent=p)
                        return None
                efeitos_out.append({"tags": [tag], "valor": val})

            descricao = f_desc.get("1.0", "end").strip()

            return {
                "nome":      nome,
                "tipo":      tipo,
                "efeito":    efeitos_out,
                "descricao": descricao,
            }

        # ── Novo ─────────────────────────────────────────────────────────────
        def novo_buff():
            p, f_nome, f_tipo, f_desc, linhas = _popup_buff("Novo Buff/Debuff")

            def salvar():
                obj = _coletar(p, f_nome, f_tipo, f_desc, linhas)
                if obj is None:
                    return
                dados = D.carregar_buffs_debuffs_raw()
                if obj["nome"] in dados:
                    messagebox.showwarning("Duplicado", "Já existe um buff/debuff com esse nome.", parent=p)
                    return
                dados[obj["nome"]] = obj
                D.salvar_buffs_debuffs_raw(dados)
                self.carregar_buffs_tree()
                p.destroy()

            self.make_btn(p, "💾  Salvar", salvar, 200, 630, 160, 38, C["green"])

        # ── Editar ────────────────────────────────────────────────────────────
        def editar_buff():
            sel = self.tree_buffs.selection()
            if not sel:
                messagebox.showwarning("Aviso", "Selecione um buff/debuff.")
                return
            nome_orig = self.tree_buffs.item(sel[0], "values")[0]
            dados = D.carregar_buffs_debuffs_raw()
            data = dados.get(nome_orig)
            if not data:
                return

            p, f_nome, f_tipo, f_desc, linhas = _popup_buff("Editar Buff/Debuff", data)

            def salvar():
                obj = _coletar(p, f_nome, f_tipo, f_desc, linhas)
                if obj is None:
                    return
                if nome_orig != obj["nome"]:
                    dados.pop(nome_orig, None)
                dados[obj["nome"]] = obj
                D.salvar_buffs_debuffs_raw(dados)
                self.carregar_buffs_tree()
                p.destroy()

            self.make_btn(p, "💾  Salvar", salvar, 200, 630, 160, 38, C["gold"])

        # ── Remover ───────────────────────────────────────────────────────────
        def remover_buff():
            sel = self.tree_buffs.selection()
            if not sel:
                return
            nome = self.tree_buffs.item(sel[0], "values")[0]
            if messagebox.askyesno("Confirmar", f"Remover '{nome}'?"):
                if D.remover_buff_debuff_raw(nome):
                    self.carregar_buffs_tree()

        self._btn_bar(c, novo_buff, editar_buff, remover_buff, y=648)

    def carregar_buffs_tree(self):
        if not hasattr(self, "tree_buffs"):
            return
        self.tree_buffs.delete(*self.tree_buffs.get_children())
        try:
            for nome, d in D.carregar_buffs_debuffs_raw().items():
                efeito_raw = d.get("efeito", [])
                # Normaliza para lista
                if isinstance(efeito_raw, dict):
                    efeito_raw = [efeito_raw]

                partes = []
                for ef in efeito_raw:
                    if not isinstance(ef, dict):
                        continue
                    tags = ef.get("tags", [ef.get("atributo", "?")])
                    tag_str = tags[0] if isinstance(tags, list) and tags else str(tags)
                    val = ef.get("valor", "")
                    val_str = f"{val:+}" if isinstance(val, (int, float)) else str(val)
                    partes.append(f"{tag_str} {val_str}")

                efeitos_str = " | ".join(partes) if partes else "—"

                self._insert_tree(self.tree_buffs, (
                    d.get("nome", ""),
                    d.get("tipo", ""),
                    efeitos_str,
                    self.resumir_texto(d.get("descricao", ""), 80),
                ))
        except Exception:
            traceback.print_exc()
    # =========================================================================
    # HABILIDADES
    # =========================================================================
    def template_habilidades(self):
        self.limpar_container()
        c = self.container_conteudo
        self.section_title(c, "💡  HABILIDADES")

        frm = tk.Frame(c, bg=C["bg_dark"])
        frm.place(x=20, y=58, width=1560, height=580)

        cols = ("Nome", "Tipo", "Custo", "Tags", "Descrição")
        self.tree_habilidades = self._make_tree(frm, cols, [250, 120, 100, 350, 730])
        self.carregar_habilidades_tree()

        def _popup_hab(titulo, data=None):
            p = self.build_popup(titulo, 560, 620)
            LX, EX, EW = 20, 190, 340
            y = 58
            fields = {}

            # ── Nome ──────────────────────────────────────────────────────────
            self.make_label(p, "Nome", LX, y, bg=C["bg_mid"])
            fields["nome"] = self.make_entry(p, EX, y, EW)
            y += 42

            # ── Tipo ──────────────────────────────────────────────────────────
            self.make_label(p, "Tipo", LX, y, bg=C["bg_mid"])
            fields["tipo"] = self.make_combobox(p, ["passivo", "ativo"], EX, y, EW)
            y += 42

            # ── Custo ─────────────────────────────────────────────────────────
            self.make_label(p, "Custo Energia", LX, y, bg=C["bg_mid"])
            fields["custo"] = self.make_entry(p, EX, y, EW)
            y += 42

            # ── Tags ──────────────────────────────────────────────────────────
            self.make_label(p, "Tags (vírgula)", LX, y, bg=C["bg_mid"])
            fields["tags"] = self.make_entry(p, EX, y, EW)
            y += 42

            # ── Valor ─────────────────────────────────────────────────────────
            self.make_label(p, "Valor", LX, y, bg=C["bg_mid"])
            fields["valor"] = self.make_entry(p, EX, y, EW)
            y += 42

            # ── Duração ───────────────────────────────────────────────────────
            self.make_label(p, "Duração (turnos)", LX, y, bg=C["bg_mid"])
            fields["duracao"] = self.make_entry(p, EX, y, EW)
            y += 42

            # ── Por Turno ─────────────────────────────────────────────────────
            self.make_label(p, "Por Turno", LX, y, bg=C["bg_mid"])
            fields["por_turno"] = self.make_combobox(p, ["true", "false"], EX, y, EW)
            y += 42

            # ── Descrição ─────────────────────────────────────────────────────
            self.make_label(p, "Descrição", LX, y, bg=C["bg_mid"])
            fields["descricao"] = self.make_text(p, EX, y, EW, 100)

            # ── Preencher dados se editando ───────────────────────────────────
            if data:
                fields["nome"].insert(0, data.get("nome", ""))
                fields["tipo"].set(data.get("tipo", "passivo"))
                fields["custo"].insert(0, str(data.get("custo", 0)))
                tags = data.get("tags", [])
                tags_str = ", ".join(tags) if isinstance(tags, list) else str(tags or "")
                fields["tags"].insert(0, tags_str)
                valor = data.get("valor", 0)
                valor_str = ", ".join(str(v) for v in valor) if isinstance(valor, list) else str(valor or "")
                fields["valor"].insert(0, valor_str)
                fields["duracao"].insert(0, str(data.get("duracao", 0)))
                fields["por_turno"].set(str(data.get("por_turno", False)).lower())
                fields["descricao"].insert("1.0", data.get("descricao", ""))

            return p, fields

        def novo_hab():
            p, fields = _popup_hab("Nova Habilidade")

            def salvar():
                nome = fields["nome"].get().strip()
                if not nome:
                    messagebox.showwarning("Erro", "Nome obrigatório.", parent=p)
                    return

                tipo = fields["tipo"].get()
                try:
                    custo = int(fields["custo"].get() or 0)
                except:
                    messagebox.showwarning("Erro", "Custo deve ser inteiro.", parent=p)
                    return

                tags = [t.strip() for t in fields["tags"].get().split(",") if t.strip()]
                
                try:
                    valor_str = fields["valor"].get().strip()
                    if "," in valor_str:
                        valor = [int(v.strip()) for v in valor_str.split(",")]
                    else:
                        valor = int(valor_str) if valor_str else 0
                except:
                    messagebox.showwarning("Erro", "Valor inválido.", parent=p)
                    return

                try:
                    duracao = int(fields["duracao"].get() or 0)
                except:
                    messagebox.showwarning("Erro", "Duração deve ser inteiro.", parent=p)
                    return

                por_turno = fields["por_turno"].get().lower() == "true"

                dados = D.carregar_habilidades_raw()
                if nome in dados:
                    messagebox.showwarning("Duplicado", "Já existe.", parent=p)
                    return

                dados[nome] = {
                    "nome": nome,
                    "tipo": tipo,
                    "custo": custo,
                    "tags": tags,
                    "valor": valor,
                    "duracao": duracao,
                    "por_turno": por_turno,
                    "descricao": fields["descricao"].get("1.0", "end").strip()
                }

                D.salvar_habilidades_raw(dados)
                self.carregar_habilidades_tree()
                p.destroy()

            self.make_btn(p, "💾  Salvar", salvar, 200, 545, 160, 38, C["green"])

        def editar_hab():
            sel = self.tree_habilidades.selection()
            if not sel:
                messagebox.showwarning("Aviso", "Selecione uma habilidade.")
                return

            nome_orig = self.tree_habilidades.item(sel[0])["values"][0]
            dados = D.carregar_habilidades_raw()
            data = dados.get(nome_orig)

            if not data:
                return

            p, fields = _popup_hab("Editar Habilidade", data)

            def salvar():
                nome = fields["nome"].get().strip()
                if not nome:
                    messagebox.showwarning("Erro", "Nome obrigatório.", parent=p)
                    return

                try:
                    custo = int(fields["custo"].get() or 0)
                except:
                    messagebox.showwarning("Erro", "Custo deve ser inteiro.", parent=p)
                    return

                tags = [t.strip() for t in fields["tags"].get().split(",") if t.strip()]
                
                try:
                    valor_str = fields["valor"].get().strip()
                    if "," in valor_str:
                        valor = [int(v.strip()) for v in valor_str.split(",")]
                    else:
                        valor = int(valor_str) if valor_str else 0
                except:
                    messagebox.showwarning("Erro", "Valor inválido.", parent=p)
                    return

                try:
                    duracao = int(fields["duracao"].get() or 0)
                except:
                    messagebox.showwarning("Erro", "Duração deve ser inteiro.", parent=p)
                    return

                por_turno = fields["por_turno"].get().lower() == "true"

                if nome_orig != nome:
                    dados.pop(nome_orig, None)

                dados[nome] = {
                    "nome": nome,
                    "tipo": fields["tipo"].get(),
                    "custo": custo,
                    "tags": tags,
                    "valor": valor,
                    "duracao": duracao,
                    "por_turno": por_turno,
                    "descricao": fields["descricao"].get("1.0", "end").strip()
                }

                D.salvar_habilidades_raw(dados)
                self.carregar_habilidades_tree()
                p.destroy()

            self.make_btn(p, "💾  Salvar", salvar, 200, 545, 160, 38, C["gold"])

        def remover_hab():
            sel = self.tree_habilidades.selection()
            if not sel:
                return

            nome = self.tree_habilidades.item(sel[0])["values"][0]

            if messagebox.askyesno("Confirmar", f"Remover '{nome}'?"):
                D.remover_habilidade_raw(nome)
                self.carregar_habilidades_tree()

        self._btn_bar(c, novo_hab, editar_hab, remover_hab, y=648)

    def carregar_habilidades_tree(self):
        if not hasattr(self, "tree_habilidades"):
            return

        self.tree_habilidades.delete(*self.tree_habilidades.get_children())

        try:
            for nome, d in D.carregar_habilidades_raw().items():
                tipo = d.get("tipo", "passivo")
                custo = d.get("custo", 0)
                tags = d.get("tags", [])
                tags_str = ", ".join(tags) if isinstance(tags, list) else str(tags or "")

                self._insert_tree(self.tree_habilidades, (
                    d.get("nome", ""),
                    tipo,
                    custo,
                    tags_str,
                    self.resumir_texto(d.get("descricao", ""), 70)
                ))
        except Exception:
            traceback.print_exc()
    # =========================================================================
    # PODERES
    # =========================================================================
    def template_poderes(self):
        self.limpar_container()
        c = self.container_conteudo
        self.section_title(c, "⚡  PODERES")

        frm = tk.Frame(c, bg=C["bg_dark"])
        frm.place(x=20, y=58, width=1560, height=580)

        cols = ("Nome", "Tipo", "Custo Energia", "Custo Mana", "Dano", "Descrição")
        self.tree_poderes = self._make_tree(frm, cols, [220, 120, 140, 140, 200, 720])
        self.carregar_poderes_tree()

        def _popup_pod(titulo, data=None):
            p = self.build_popup(titulo, 580, 680)
            LX, EX, EW = 20, 210, 330
            y = 58
            fields = {}

            # ── Nome ──────────────────────────────────────────────────────────
            self.make_label(p, "Nome", LX, y, bg=C["bg_mid"])
            fields["nome"] = self.make_entry(p, EX, y, EW)
            y += 42

            # ── Tipo ──────────────────────────────────────────────────────────
            self.make_label(p, "Tipo", LX, y, bg=C["bg_mid"])
            fields["tipo"] = self.make_combobox(p, ["passivo", "ativo", "ofensivo"], EX, y, EW)
            y += 42

            # ── Custo Energia ─────────────────────────────────────────────────
            self.make_label(p, "Custo Energia", LX, y, bg=C["bg_mid"])
            fields["custo_energia"] = self.make_entry(p, EX, y, EW)
            y += 42

            # ── Custo Mana ───────────────────────────────────────────────────
            self.make_label(p, "Custo Mana", LX, y, bg=C["bg_mid"])
            fields["custo_mana"] = self.make_entry(p, EX, y, EW)
            y += 42

            # ── Dano (tipo valor, tipo valor) ─────────────────────────────────
            self.make_label(p, "Dano (tipo:valor,tipo:valor)", LX, y, bg=C["bg_mid"])
            fields["dano"] = self.make_entry(p, EX, y, EW)
            y += 42

            # ── Efeitos (nome chance duração) ─────────────────────────────────
            self.make_label(p, "Efeitos (vírgula separados)", LX, y, bg=C["bg_mid"])
            fields["efeitos"] = self.make_entry(p, EX, y, EW)
            y += 42

            # ── Ignora Resistências ───────────────────────────────────────────
            self.make_label(p, "Ignora Resistências", LX, y, bg=C["bg_mid"])
            fields["ignora_resistencias"] = self.make_combobox(p, ["true", "false"], EX, y, EW)
            y += 42

            # ── Descrição ─────────────────────────────────────────────────────
            self.make_label(p, "Descrição", LX, y, bg=C["bg_mid"])
            fields["descricao"] = self.make_text(p, EX, y, EW, 120)

            # ── Preencher dados se editando ───────────────────────────────────
            if data:
                fields["nome"].insert(0, data.get("nome", ""))
                fields["tipo"].set(data.get("tipo", "ativo"))
                fields["custo_energia"].insert(0, str(data.get("custo_energia", 0)))
                fields["custo_mana"].insert(0, str(data.get("custo_mana", 0)))
                
                dano = data.get("dano", [])
                dano_str = ", ".join(f"{d.get('tipo', '')}:{d.get('valor', '')}" for d in dano) if isinstance(dano, list) else ""
                fields["dano"].insert(0, dano_str)
                
                efeitos = data.get("efeitos", [])
                efeitos_str = ", ".join(str(e) for e in efeitos) if isinstance(efeitos, list) else str(efeitos or "")
                fields["efeitos"].insert(0, efeitos_str)
                
                fields["ignora_resistencias"].set(str(data.get("ignora_resistencias", False)).lower())
                fields["descricao"].insert("1.0", data.get("descricao", ""))

            return p, fields

        def novo_pod():
            p, fields = _popup_pod("Novo Poder")

            def salvar():
                nome = fields["nome"].get().strip()
                if not nome:
                    messagebox.showwarning("Erro", "Nome obrigatório.", parent=p)
                    return

                tipo = fields["tipo"].get()

                try:
                    custo_e = int(fields["custo_energia"].get() or 0)
                    custo_m = int(fields["custo_mana"].get() or 0)
                except:
                    messagebox.showwarning("Erro", "Custos devem ser inteiros.", parent=p)
                    return

                # Parse dano: "fisico:10, fogo:5"
                dano_list = []
                dano_str = fields["dano"].get().strip()
                if dano_str:
                    try:
                        for par in dano_str.split(","):
                            tipo_d, valor_d = par.split(":")
                            dano_list.append({"tipo": tipo_d.strip(), "valor": int(valor_d.strip())})
                    except:
                        messagebox.showwarning("Erro", "Dano inválido (use: tipo:valor,tipo:valor).", parent=p)
                        return

                efeitos_list = [e.strip() for e in fields["efeitos"].get().split(",") if e.strip()]

                ignora_res = fields["ignora_resistencias"].get().lower() == "true"

                dados = D.carregar_poderes_raw()
                if nome in dados:
                    messagebox.showwarning("Duplicado", "Já existe.", parent=p)
                    return

                dados[nome] = {
                    "nome": nome,
                    "tipo": tipo,
                    "custo_energia": custo_e,
                    "custo_mana": custo_m,
                    "dano": dano_list,
                    "efeitos": efeitos_list,
                    "ignora_resistencias": ignora_res,
                    "descricao": fields["descricao"].get("1.0", "end").strip()
                }

                D.salvar_poderes_raw(dados)
                self.carregar_poderes_tree()
                p.destroy()

            self.make_btn(p, "💾  Salvar", salvar, 215, 600, 160, 38, C["green"])

        def editar_pod():
            sel = self.tree_poderes.selection()
            if not sel:
                messagebox.showwarning("Aviso", "Selecione um poder.")
                return

            nome_orig = self.tree_poderes.item(sel[0])["values"][0]
            dados = D.carregar_poderes_raw()
            data = dados.get(nome_orig)

            if not data:
                return

            p, fields = _popup_pod("Editar Poder", data)

            def salvar():
                nome = fields["nome"].get().strip()
                if not nome:
                    messagebox.showwarning("Erro", "Nome obrigatório.", parent=p)
                    return

                try:
                    custo_e = int(fields["custo_energia"].get() or 0)
                    custo_m = int(fields["custo_mana"].get() or 0)
                except:
                    messagebox.showwarning("Erro", "Custos devem ser inteiros.", parent=p)
                    return

                dano_list = []
                dano_str = fields["dano"].get().strip()
                if dano_str:
                    try:
                        for par in dano_str.split(","):
                            tipo_d, valor_d = par.split(":")
                            dano_list.append({"tipo": tipo_d.strip(), "valor": int(valor_d.strip())})
                    except:
                        messagebox.showwarning("Erro", "Dano inválido.", parent=p)
                        return

                efeitos_list = [e.strip() for e in fields["efeitos"].get().split(",") if e.strip()]

                ignora_res = fields["ignora_resistencias"].get().lower() == "true"

                if nome_orig != nome:
                    dados.pop(nome_orig, None)

                dados[nome] = {
                    "nome": nome,
                    "tipo": fields["tipo"].get(),
                    "custo_energia": custo_e,
                    "custo_mana": custo_m,
                    "dano": dano_list,
                    "efeitos": efeitos_list,
                    "ignora_resistencias": ignora_res,
                    "descricao": fields["descricao"].get("1.0", "end").strip()
                }

                D.salvar_poderes_raw(dados)
                self.carregar_poderes_tree()
                p.destroy()

            self.make_btn(p, "💾  Salvar", salvar, 215, 600, 160, 38, C["gold"])

        def remover_pod():
            sel = self.tree_poderes.selection()
            if not sel:
                return

            nome = self.tree_poderes.item(sel[0])["values"][0]

            if messagebox.askyesno("Confirmar", f"Remover '{nome}'?"):
                D.remover_poder_raw(nome)
                self.carregar_poderes_tree()

        self._btn_bar(c, novo_pod, editar_pod, remover_pod, y=648)

    def carregar_poderes_tree(self):
        if not hasattr(self, "tree_poderes"):
            return

        self.tree_poderes.delete(*self.tree_poderes.get_children())

        try:
            for nome, d in D.carregar_poderes_raw().items():
                tipo = d.get("tipo", "ativo")
                custo_e = d.get("custo_energia", 0)
                custo_m = d.get("custo_mana", 0)
                
                dano = d.get("dano", [])
                dano_str = ", ".join(f"{dmg.get('tipo', '')}:{dmg.get('valor', '')}" for dmg in dano) if isinstance(dano, list) else ""

                self._insert_tree(self.tree_poderes, (
                    d.get("nome", ""),
                    tipo,
                    custo_e,
                    custo_m,
                    dano_str,
                    self.resumir_texto(d.get("descricao", ""), 60)
                ))
        except Exception:
            traceback.print_exc()
    # =========================================================================
    # NPCs
    # =========================================================================
    ATRIBS_NPC = ["Forca","Agilidade","Vigor","Inteligencia","Tatica","Presenca","Poder"]
    ATRIBS_LABEL = {"Forca":"FOR","Agilidade":"AGI","Vigor":"VIG","Inteligencia":"INT","Tatica":"TAT","Presenca":"PRE","Poder":"POD"}
    TIPOS_DANO = ["contundente","concussivo","cortante","perfurante","balístico","rasgante","explosivo","incendiário","congelante","envenenante","eletrocutante","mental"]

    def template_npcs(self):
        self.limpar_container()
        c = self.container_conteudo
        self.section_title(c, "🧟  NPCs")

        frm = tk.Frame(c, bg=C["bg_dark"])
        frm.place(x=20, y=58, width=1560, height=580)

        cols = ("Nome","Nível","Classe","Grupo","FOR","AGI","VIG","INT","TAT","PRE","POD")
        self.tree_npcs = self._make_tree(frm, cols, [200,60,140,140,60,60,60,60,60,60,60])
        self.carregar_npcs_tree()

        def novo_npc():  self._popup_npc_completo("Novo NPC", None)
        def editar_npc():
            sel = self.tree_npcs.selection()
            if not sel: messagebox.showwarning("Aviso","Selecione um NPC."); return
            nome = self.tree_npcs.item(sel[0],"values")[0]
            dados = D.carregar_npcs_raw()
            self._popup_npc_completo("Editar NPC", dados.get(nome), nome_orig=nome)

        def remover_npc():
            sel = self.tree_npcs.selection()
            if not sel: return
            nome = self.tree_npcs.item(sel[0],"values")[0]
            if messagebox.askyesno("Confirmar", f"Remover '{nome}'?"):
                D.remover_npc_raw(nome); self.carregar_npcs_tree()

        self._btn_bar(c, novo_npc, editar_npc, remover_npc, y=648)

    def _popup_npc_completo(self, titulo, data, nome_orig=None):
        try: 
            kits_disponiveis = D.carregar_kits()
            nomes_kits = sorted(kits_disponiveis.keys())
        except:
            kits_disponiveis = {}
            nomes_kits = []
        d = data or {}
        kits_state = list(d.get("kits", []))
        kit_fixo_state = d.get("kit_fixo")
        profs_state = dict(d.get("proficiencias_base", {}))
        res_base_state = dict(d.get("resistencias_base", {}))
        for t in self.TIPOS_DANO: res_base_state.setdefault(t, 0)

        # ── Converte habilidade_inicial / poder_inicial para lista de dicts ──
        def _norm_entry(e, categoria):
            if isinstance(e, str):
                return {"nome": e, "descricao": "", "categoria": categoria,
                        "subtipo": "padrao", "tipo": "passivo",
                        "custo": 0, "custo_mana": 0, "tags": [], "valor": []}
            out = dict(e)
            out.setdefault("categoria", categoria)
            out.setdefault("subtipo", "padrao")
            return out

        npc_habs_state = [_norm_entry(x, "habilidade") for x in d.get("habilidade_inicial", [])]
        npc_habs_state += [_norm_entry(x, "poder")      for x in d.get("poder_inicial",     [])]

        p = tk.Toplevel(self)
        p.title(titulo)
        p.geometry("1600x780")
        p.config(bg=C["bg_mid"])
        p.resizable(False, False)
        p.transient(self)
        p.grab_set()

        tk.Frame(p, bg=C["accent2"]).place(x=0, y=0, width=1600, height=44)
        tk.Label(p, text=titulo, fg="white", bg=C["accent2"], font=("Segoe UI", 13, "bold")).place(x=16, y=10)

        CONTENT_Y = 54
        COL_W = 280
        COL_GAP = 10
        COL_H = 690
        BG_COL = C["bg_card"]
        col_xs = [10 + i*(COL_W+COL_GAP) for i in range(5)]

        def col_frame(idx):
            f = tk.Frame(p, bg=BG_COL, highlightthickness=1, highlightbackground=C["border"])
            f.place(x=col_xs[idx], y=CONTENT_Y, width=COL_W, height=COL_H)
            return f

        col_info  = col_frame(0)
        col_prof  = col_frame(1)
        col_hab   = col_frame(2)
        col_res   = col_frame(3)
        col_kits  = col_frame(4)

        def col_title(parent, text):
            tk.Label(parent, text=text, fg="white", bg=C["accent2"],
                     font=("Segoe UI", 11, "bold")).pack(fill="x", pady=(0,8), ipady=4)

        # ══════════════════════════════════════════════════════════════════════
        #  COL 0 — Info & Atributos
        # ══════════════════════════════════════════════════════════════════════
        col_title(col_info, "📋  Info & Atributos")
        LX, EX, EW = 8, 110, 150
        fields = {}
        y = 8
        for label, key in [("Nome","nome"),("Nível","nivel"),("Classe","classe"),("Grupo","grupo")]:
            tk.Label(col_info, text=label, fg=C["text_dim"], bg=BG_COL,
                     font=("Segoe UI", 9)).place(x=LX, y=y+34, height=24)
            e = tk.Entry(col_info, font=("Segoe UI", 10), bg=C["bg_mid"], fg=C["text"],
                         insertbackground=C["text"], relief="flat", highlightthickness=1,
                         highlightbackground=C["border"], highlightcolor=C["accent_hi"])
            e.place(x=EX, y=y+34, width=EW, height=26)
            fields[key] = e
            y += 38

        if d:
            fields["nome"].insert(0, d.get("nome",""))
            fields["nivel"].insert(0, str(d.get("nivel",1)))
            fields["classe"].insert(0, d.get("classe","") or "")
            fields["grupo"].insert(0, d.get("grupo","") or "")

        y += 46
        tk.Frame(col_info, bg=C["border"]).place(x=8, y=y, width=COL_W-16, height=1)
        y += 8
        tk.Label(col_info, text="Atributos", fg="white", bg=BG_COL,
                 font=("Segoe UI", 10, "bold")).place(x=8, y=y)
        y += 24
        attr_vars = {}
        for attr in self.ATRIBS_NPC:
            val = int(d.get(attr, 1)) if d else 1
            var = tk.IntVar(value=val)
            attr_vars[attr] = var
            row = tk.Frame(col_info, bg=BG_COL)
            row.place(x=8, y=y, width=COL_W-16, height=30)
            tk.Label(row, text=self.ATRIBS_LABEL[attr], fg=C["text_dim"], bg=BG_COL,
                     font=("Segoe UI", 9), width=4).pack(side="left")
            tk.Button(row, text="−", font=("Segoe UI", 9), bg="#8c1d1d", fg="white", width=2,
                      relief="flat", cursor="hand2",
                      command=lambda v=var: v.set(max(1, v.get()-1))).pack(side="left", padx=2)
            tk.Label(row, textvariable=var, fg="white", bg=BG_COL,
                     font=("Segoe UI", 10, "bold"), width=3).pack(side="left")
            tk.Button(row, text="+", font=("Segoe UI", 9), bg="#115c11", fg="white", width=2,
                      relief="flat", cursor="hand2",
                      command=lambda v=var: v.set(v.get()+1)).pack(side="left", padx=2)
            y += 32

        # ══════════════════════════════════════════════════════════════════════
        #  COL 1 — Proficiências
        # ══════════════════════════════════════════════════════════════════════
        col_title(col_prof, "📖  Proficiências")
        canvas_prof = tk.Canvas(col_prof, bg=BG_COL, highlightthickness=0)
        sb_prof = ttk.Scrollbar(col_prof, orient="vertical", command=canvas_prof.yview)
        frm_prof = tk.Frame(canvas_prof, bg=BG_COL)
        frm_prof.bind("<Configure>", lambda e: canvas_prof.configure(scrollregion=canvas_prof.bbox("all")))
        canvas_prof.create_window((0,0), window=frm_prof, anchor="nw")
        canvas_prof.configure(yscrollcommand=sb_prof.set)
        sb_prof.pack(side="right", fill="y")
        canvas_prof.pack(fill="both", expand=True)
        canvas_prof.bind("<Enter>", lambda e: canvas_prof.bind_all("<MouseWheel>", lambda ev: canvas_prof.yview_scroll(int(ev.delta/-90),"units")))
        canvas_prof.bind("<Leave>", lambda e: canvas_prof.unbind_all("<MouseWheel>"))

        try: todas_profs = list(D.carregar_proficiencias().keys())
        except Exception: todas_profs = list(profs_state.keys()) or []
        for pr in todas_profs: profs_state.setdefault(pr, 0)
        prof_vars = {}

        def rebuild_prof():
            for w in frm_prof.winfo_children(): w.destroy()
            for pr in sorted(profs_state.keys()):
                nivel = profs_state[pr]
                var = tk.IntVar(value=nivel)
                prof_vars[pr] = var
                row = tk.Frame(frm_prof, bg=BG_COL)
                row.pack(fill="x", padx=6, pady=2)
                tk.Label(row, text=pr, fg=C["text"], bg=BG_COL,
                         font=("Segoe UI", 9), width=14, anchor="w").pack(side="left")
                tk.Button(row, text="−", font=("Segoe UI", 8), bg="#8c1d1d", fg="white",
                          width=2, relief="flat", cursor="hand2",
                          command=lambda p2=pr: (profs_state.update({p2: max(0, profs_state[p2]-1)}), rebuild_prof())).pack(side="left", padx=1)
                tk.Label(row, text=str(nivel), fg="white", bg=BG_COL,
                         font=("Segoe UI", 10, "bold"), width=3).pack(side="left")
                tk.Button(row, text="+", font=("Segoe UI", 8), bg="#115c11", fg="white",
                          width=2, relief="flat", cursor="hand2",
                          command=lambda p2=pr: (profs_state.update({p2: profs_state[p2]+1}), rebuild_prof())).pack(side="left", padx=1)
        rebuild_prof()

        # ══════════════════════════════════════════════════════════════════════
        #  COL 2 — Habilidades / Poderes  (popup completo integrado)
        # ══════════════════════════════════════════════════════════════════════
        col_title(col_hab, "⚔  Habilidades / Poderes")

        # Constantes do popup interno (mesmo esquema de abrir_popup_habilidade)
        TIPOS_DANO_NPC   = ["contundente","concussivo","cortante","perfurante","balístico",
                            "rasgante","explosivo","incendiário","congelante","envenenante",
                            "eletrocutante","mental"]
        TIPOS_TESTE_NPC  = ["iniciativa","sorte","força","agilidade","vigor","inteligencia",
                            "presença","tática","poder","físico","mental","vocal","qualquer teste"]
        PALAVRAS_NPC     = ["vida","energia","mana","vidaMax","energiaMax","manaMax",
                            "movimentação","bloqueio","esquiva","carga","percepção"]
        RESISTENCIAS_NPC = [f"resistencia_{t}" for t in TIPOS_DANO_NPC]
        DESARMADO_NPC    = ["desarmado_dano","desarmado_crit_mult","desarmado_crit_valor"]
        CATEGORIAS_NPC   = ["Tipos de Dano","Tipos de Teste","Palavras-chave","Resistências","Desarmado"]

        def _opcoes_cat_npc(cat):
            return {"Tipos de Dano": TIPOS_DANO_NPC,
                    "Tipos de Teste": TIPOS_TESTE_NPC,
                    "Palavras-chave": PALAVRAS_NPC,
                    "Resistências":   RESISTENCIAS_NPC,
                    "Desarmado":      DESARMADO_NPC}.get(cat, TIPOS_TESTE_NPC)

        def _detectar_cat_npc(tag):
            if tag in TIPOS_DANO_NPC:   return "Tipos de Dano"
            if tag in TIPOS_TESTE_NPC:  return "Tipos de Teste"
            if tag in RESISTENCIAS_NPC: return "Resistências"
            if tag in DESARMADO_NPC:    return "Desarmado"
            return "Palavras-chave"

        def _nomes_buffs_npc():
            try:    return list(D.carregar_buffs_debuffs_raw().keys()) or ["—"]
            except: return ["—"]

        # Canvas scrollável da coluna
        canvas_hab = tk.Canvas(col_hab, bg=BG_COL, highlightthickness=0)
        sb_hab = ttk.Scrollbar(col_hab, orient="vertical", command=canvas_hab.yview)
        frm_hab = tk.Frame(canvas_hab, bg=BG_COL)
        frm_hab.bind("<Configure>", lambda e: canvas_hab.configure(scrollregion=canvas_hab.bbox("all")))
        canvas_hab.create_window((0,0), window=frm_hab, anchor="nw")
        canvas_hab.configure(yscrollcommand=sb_hab.set)
        sb_hab.pack(side="right", fill="y")
        canvas_hab.pack(fill="both", expand=True)
        canvas_hab.bind("<Enter>", lambda e: canvas_hab.bind_all("<MouseWheel>", lambda ev: canvas_hab.yview_scroll(int(ev.delta/-90),"units")))
        canvas_hab.bind("<Leave>", lambda e: canvas_hab.unbind_all("<MouseWheel>"))

        # ── Lista principal ───────────────────────────────────────────────
        def rebuild_hab():
            for w in frm_hab.winfo_children():
                w.destroy()

            for idx, entry in enumerate(npc_habs_state):
                cat_txt   = entry.get("categoria", "habilidade").capitalize()
                sub_txt   = "Ofensivo" if entry.get("subtipo") == "ofensivo" else (
                            "Passivo"  if entry.get("tipo") == "passivo" else "Ativo")
                cor_badge = "#0a5c2a" if entry.get("categoria") == "habilidade" else "#3b0a5c"

                row = tk.Frame(frm_hab, bg=C["bg_mid"], relief="ridge", bd=1)
                row.pack(fill="x", padx=4, pady=3)

                header_row = tk.Frame(row, bg=C["bg_mid"])
                header_row.pack(fill="x", padx=6, pady=(5,2))
                tk.Label(header_row, text=f"[{cat_txt}]", bg=cor_badge, fg="white",
                         font=("Segoe UI", 8, "bold"), padx=4).pack(side="left")
                tk.Label(header_row, text=f"  {entry.get('nome','?')}  •  {sub_txt}",
                         bg=C["bg_mid"], fg=C["text"],
                         font=("Segoe UI", 9, "bold"), anchor="w").pack(side="left", fill="x", expand=True)

                desc = entry.get("descricao", "")
                if desc:
                    tk.Label(row, text=desc, bg=C["bg_mid"], fg=C["text_dim"],
                             font=("Segoe UI", 8, "italic"),
                             wraplength=220, anchor="w", justify="left").pack(fill="x", padx=8, pady=(0,3))

                btn_row = tk.Frame(row, bg=C["bg_mid"])
                btn_row.pack(fill="x", padx=6, pady=(0,5))
                tk.Button(btn_row, text="✏ Editar", font=("Segoe UI", 8),
                          bg=C["accent2"], fg="white", relief="flat", cursor="hand2",
                          command=lambda i=idx: _abrir_popup_hab_npc(i)).pack(side="left", padx=(0,4))
                tk.Button(btn_row, text="✕", font=("Segoe UI", 8),
                          bg=C.get("red","#7a1f1f"), fg="white", width=3,
                          relief="flat", cursor="hand2",
                          command=lambda i=idx: _remover_hab(i)).pack(side="left")

            # Separador + botões de adicionar
            tk.Frame(frm_hab, bg=C["border"], height=1).pack(fill="x", padx=6, pady=6)
            add_row = tk.Frame(frm_hab, bg=BG_COL)
            add_row.pack(fill="x", padx=4, pady=(0,6))
            tk.Button(add_row, text="＋ Nova Habilidade", font=("Segoe UI", 9),
                      bg=C.get("green","#1f7a1f"), fg="white", relief="flat", cursor="hand2",
                      command=lambda: _abrir_popup_hab_npc(None, "habilidade")).pack(fill="x", pady=2)
            tk.Button(add_row, text="＋ Novo Poder", font=("Segoe UI", 9),
                      bg="#3b0a5c", fg="white", relief="flat", cursor="hand2",
                      command=lambda: _abrir_popup_hab_npc(None, "poder")).pack(fill="x", pady=2)

        def _remover_hab(idx):
            npc_habs_state.pop(idx)
            rebuild_hab()

        # ── Popup de criação/edição (mesmo layout de abrir_popup_habilidade) ─
        def _abrir_popup_hab_npc(idx_editar, categoria_default="habilidade"):
            editando      = idx_editar is not None
            data_edit     = npc_habs_state[idx_editar] if editando else {}
            eh_ofensivo_e = data_edit.get("subtipo") == "ofensivo" if editando else False

            pop2 = tk.Toplevel(p)
            pop2.title("Editar Habilidade/Poder NPC" if editando else "Nova Habilidade/Poder NPC")
            pop2.geometry("680x820")
            pop2.configure(bg="#0d0a1e")
            pop2.resizable(False, True)
            pop2.transient(p)
            pop2.grab_set()

            PBG  = "#0d0a1e"; PPANEL = "#12103a"; PCARD = "#1a1640"
            PENT = "#0b0926"; PFG   = "#e8e0ff"; PACC  = "#7c5cfc"
            PGRN = "#1f7a1f"; PRED  = "#7a1f1f"

            # header
            hdr = tk.Frame(pop2, bg="#090720", height=52)
            hdr.pack(fill="x"); hdr.pack_propagate(False)
            tk.Label(hdr,
                     text=("✦ EDITAR" if editando else "✦ NOVO") + "  PODER / HABILIDADE  [NPC]",
                     font=("Consolas", 13, "bold"), bg="#090720", fg="#a88fff"
                     ).pack(side="left", padx=18, pady=12)

            # scroll principal
            outer = tk.Frame(pop2, bg=PBG); outer.pack(fill="both", expand=True)
            cv2   = tk.Canvas(outer, bg=PBG, highlightthickness=0)
            sb2   = tk.Scrollbar(outer, orient="vertical", command=cv2.yview)
            inn2  = tk.Frame(cv2, bg=PBG)
            inn2.bind("<Configure>", lambda e: cv2.configure(scrollregion=cv2.bbox("all")))
            cv2.create_window((0,0), window=inn2, anchor="nw")
            cv2.configure(yscrollcommand=sb2.set)
            cv2.pack(side="left", fill="both", expand=True); sb2.pack(side="right", fill="y")
            cv2.bind("<Enter>",  lambda e: cv2.bind_all("<MouseWheel>",   lambda ev: cv2.yview_scroll(int(ev.delta/-90),"units")))
            cv2.bind("<Leave>",  lambda e: cv2.unbind_all("<MouseWheel>"))

            # helpers
            def psection(parent, title):
                f = tk.Frame(parent, bg=PPANEL); f.pack(fill="x", padx=14, pady=(10,2))
                tk.Label(f, text=title, bg=PPANEL, fg="#9988dd",
                         font=("Consolas", 9, "bold"), padx=8, pady=4).pack(anchor="w")
                body = tk.Frame(f, bg=PCARD); body.pack(fill="x", padx=4, pady=(0,6))
                return body

            def plbl_entry(parent, label, width=28, hint=""):
                r = tk.Frame(parent, bg=PCARD); r.pack(fill="x", padx=10, pady=4)
                tk.Label(r, text=label, bg=PCARD, fg="#8899cc",
                         font=("Arial", 10), width=20, anchor="w").pack(side="left")
                e = tk.Entry(r, width=width, bg=PENT, fg=PFG, insertbackground=PFG,
                             relief="flat", highlightthickness=1,
                             highlightbackground="#2a1f6a", highlightcolor=PACC,
                             font=("Arial", 10))
                e.pack(side="left", fill="x", expand=True, padx=(4,0))
                if hint:
                    tk.Label(r, text=hint, bg=PCARD, fg="#556688",
                             font=("Arial", 8, "italic")).pack(side="left", padx=6)
                return e

            # ── IDENTIDADE ────────────────────────────────────────────────
            s_id = psection(inn2, "  IDENTIDADE")

            var_cat = tk.StringVar(
                value=data_edit.get("categoria", categoria_default) if editando else categoria_default)
            r_cat = tk.Frame(s_id, bg=PCARD); r_cat.pack(fill="x", padx=10, pady=4)
            tk.Label(r_cat, text="Categoria", bg=PCARD, fg="#8899cc",
                     font=("Arial", 10), width=20, anchor="w").pack(side="left")
            for val, txt in [("habilidade","Habilidade"),("poder","Poder")]:
                tk.Radiobutton(r_cat, text=txt, variable=var_cat, value=val,
                               bg=PCARD, fg=PFG, selectcolor="#24195e",
                               activebackground=PCARD, activeforeground=PFG,
                               indicatoron=0, width=14, bd=1, relief="ridge",
                               font=("Arial", 9)).pack(side="left", padx=3)

            var_subtipo = tk.StringVar(value="ofensivo" if eh_ofensivo_e else "padrao")
            r_sub = tk.Frame(s_id, bg=PCARD); r_sub.pack(fill="x", padx=10, pady=4)
            tk.Label(r_sub, text="Subtipo", bg=PCARD, fg="#8899cc",
                     font=("Arial", 10), width=20, anchor="w").pack(side="left")
            for val, txt in [("padrao","Padrão  (passivo / ativo)"),
                             ("ofensivo","Ofensivo  (dano / ataque)")]:
                tk.Radiobutton(r_sub, text=txt, variable=var_subtipo, value=val,
                               bg=PCARD, fg=PFG, selectcolor="#24195e",
                               activebackground=PCARD, activeforeground=PFG,
                               indicatoron=0, width=22, bd=1, relief="ridge",
                               font=("Arial", 9)).pack(side="left", padx=3)

            ent_nome = plbl_entry(s_id, "Nome")
            ent_desc = plbl_entry(s_id, "Descrição")

            # ── FRAME PADRÃO ──────────────────────────────────────────────
            frame_padrao = tk.Frame(inn2, bg=PBG)

            s_custo = psection(frame_padrao, "  CUSTO  (0 = passivo)")
            r_custo = tk.Frame(s_custo, bg=PCARD); r_custo.pack(fill="x", padx=10, pady=4)
            tk.Label(r_custo, text="Energia", bg=PCARD, fg="#8899cc",
                     font=("Arial", 10), width=10, anchor="w").pack(side="left")
            ent_energia = tk.Entry(r_custo, width=6, bg=PENT, fg=PFG, insertbackground=PFG,
                                   relief="flat", highlightthickness=1,
                                   highlightbackground="#2a1f6a", highlightcolor=PACC,
                                   font=("Arial", 10))
            ent_energia.pack(side="left", padx=(4,20))
            tk.Label(r_custo, text="Mana", bg=PCARD, fg="#8899cc",
                     font=("Arial", 10), width=8, anchor="w").pack(side="left")
            ent_mana_pad = tk.Entry(r_custo, width=6, bg=PENT, fg=PFG, insertbackground=PFG,
                                    relief="flat", highlightthickness=1,
                                    highlightbackground="#2a1f6a", highlightcolor=PACC,
                                    font=("Arial", 10))
            ent_mana_pad.pack(side="left", padx=(4,0))

            lbl_modo = tk.Label(s_custo, text="▶ MODO: PASSIVO",
                                bg=PCARD, fg="#55cc88", font=("Consolas", 9, "bold"))
            lbl_modo.pack(anchor="w", padx=14, pady=(0,4))

            # sub-frame PASSIVO
            frame_passivo  = tk.Frame(frame_padrao, bg=PBG)
            s_pass         = psection(frame_passivo, "  MODIFICADORES PASSIVOS")
            linhas_passivo = []

            def _rebuild_passivo():
                for w in s_pass.winfo_children(): w.destroy()
                for idx2, ln in enumerate(linhas_passivo):
                    bloco = tk.Frame(s_pass, bg="#0f0d2e", relief="ridge", bd=1)
                    bloco.pack(fill="x", padx=6, pady=3)
                    row1 = tk.Frame(bloco, bg="#0f0d2e"); row1.pack(fill="x", padx=8, pady=(5,2))
                    tk.Label(row1, text="Categoria", fg="#8899cc", bg="#0f0d2e",
                             font=("Arial", 9)).pack(side="left", padx=(0,6))
                    cat_cb = ttk.Combobox(row1, textvariable=ln["cat"],
                                         values=CATEGORIAS_NPC, state="readonly",
                                         font=("Arial", 9), width=18)
                    cat_cb.pack(side="left", padx=(0,10))
                    def _rem_p(i=idx2): linhas_passivo.pop(i); _rebuild_passivo()
                    tk.Button(row1, text="✕ Remover", fg="#ff6666", bg="#0f0d2e",
                              bd=0, font=("Arial", 9, "bold"), cursor="hand2",
                              command=_rem_p,
                              activebackground="#1a1040", activeforeground="#ff6666"
                              ).pack(side="right", padx=4)
                    row2 = tk.Frame(bloco, bg="#0f0d2e"); row2.pack(fill="x", padx=8, pady=(2,6))
                    tk.Label(row2, text="Tag", fg="#8899cc", bg="#0f0d2e",
                             font=("Arial", 9)).pack(side="left", padx=(0,6))
                    opcoes = _opcoes_cat_npc(ln["cat"].get())
                    tag_cb = ttk.Combobox(row2, textvariable=ln["tag"],
                                         values=opcoes, state="readonly",
                                         font=("Arial", 9), width=22)
                    tag_cb.pack(side="left", padx=(0,14))
                    tk.Label(row2, text="Valor", fg="#8899cc", bg="#0f0d2e",
                             font=("Arial", 9)).pack(side="left", padx=(0,4))
                    tk.Entry(row2, textvariable=ln["val"], bg=PENT, fg=PFG,
                             insertbackground=PFG, relief="flat",
                             font=("Arial", 9), width=8).pack(side="left")
                    tk.Label(row2, text="(ex: -3, 10)", fg="#445566", bg="#0f0d2e",
                             font=("Arial", 8, "italic")).pack(side="left", padx=6)
                    def _cat_ch(evt, l=ln, cb=tag_cb):
                        novas = _opcoes_cat_npc(l["cat"].get())
                        cb["values"] = novas
                        if l["tag"].get() not in novas:
                            l["tag"].set(novas[0] if novas else "")
                    cat_cb.bind("<<ComboboxSelected>>", _cat_ch)

            def _add_passivo(cat="Tipos de Teste", tag=None, val="0"):
                ops   = _opcoes_cat_npc(cat)
                tag_v = tag if (tag and tag in ops) else (ops[0] if ops else "")
                linhas_passivo.append({"cat": tk.StringVar(value=cat),
                                       "tag": tk.StringVar(value=tag_v),
                                       "val": tk.StringVar(value=str(val))})
                _rebuild_passivo()

            tk.Button(frame_passivo, text="＋  Adicionar Modificador",
                      command=_add_passivo, bg="#1f4a2a", fg="white",
                      relief="flat", padx=10, pady=4, font=("Arial", 9),
                      cursor="hand2").pack(anchor="w", padx=18, pady=(2,8))

            # sub-frame ATIVO
            frame_ativo    = tk.Frame(frame_padrao, bg=PBG)
            s_dur_pad      = psection(frame_ativo, "  DURAÇÃO DO EFEITO")
            ent_duracao_pad = plbl_entry(s_dur_pad, "Turnos de duração",
                                        width=8, hint="vazio = instantâneo")
            s_dano_pad      = psection(frame_ativo, "  DANO  (opcional)")
            linhas_dano_pad = []

            def _rebuild_dano_pad():
                for w in s_dano_pad.winfo_children(): w.destroy()
                for idx2, ln in enumerate(linhas_dano_pad):
                    lf = tk.Frame(s_dano_pad, bg="#0f0d2e", relief="ridge", bd=1)
                    lf.pack(fill="x", padx=6, pady=3)
                    row = tk.Frame(lf, bg="#0f0d2e"); row.pack(fill="x", padx=8, pady=5)
                    tk.Label(row, text="Tipo", fg="#8899cc", bg="#0f0d2e",
                             font=("Arial", 9)).pack(side="left", padx=(0,4))
                    ttk.Combobox(row, textvariable=ln["tipo"], values=TIPOS_DANO_NPC,
                                 state="readonly", font=("Arial", 9),
                                 width=16).pack(side="left", padx=(0,12))
                    tk.Label(row, text="Valor", fg="#8899cc", bg="#0f0d2e",
                             font=("Arial", 9)).pack(side="left", padx=(0,4))
                    tk.Entry(row, textvariable=ln["val"], bg=PENT, fg=PFG,
                             insertbackground=PFG, relief="flat",
                             font=("Arial", 9), width=8).pack(side="left")
                    def _rem_dp(i=idx2): linhas_dano_pad.pop(i); _rebuild_dano_pad()
                    tk.Button(row, text="✕", command=_rem_dp, bg=PRED, fg=PFG,
                              relief="flat", width=3, font=("Arial", 8)).pack(side="right", padx=4)

            def _add_dano_pad(tipo="contundente", val="0"):
                linhas_dano_pad.append({"tipo": tk.StringVar(value=tipo),
                                        "val":  tk.StringVar(value=str(val))})
                _rebuild_dano_pad()

            tk.Button(frame_ativo, text="＋  Adicionar Dano", command=_add_dano_pad,
                      bg="#1f3a6a", fg="white", relief="flat", padx=10, pady=4,
                      font=("Arial", 9), cursor="hand2").pack(anchor="w", padx=18, pady=(2,4))

            s_ef_pad       = psection(frame_ativo, "  EFEITOS COM CHANCE")
            linhas_ef_pad  = []

            def _rebuild_ef_pad():
                for w in s_ef_pad.winfo_children(): w.destroy()
                nomes_buff = _nomes_buffs_npc()
                for idx2, ln in enumerate(linhas_ef_pad):
                    lf = tk.Frame(s_ef_pad, bg="#0f0d2e", relief="ridge", bd=1)
                    lf.pack(fill="x", padx=6, pady=3)
                    row = tk.Frame(lf, bg="#0f0d2e"); row.pack(fill="x", padx=8, pady=5)
                    tk.Label(row, text="Efeito", fg="#8899cc", bg="#0f0d2e",
                             font=("Arial", 9)).pack(side="left", padx=(0,4))
                    if ln["nome"].get() not in nomes_buff and nomes_buff:
                        ln["nome"].set(nomes_buff[0])
                    ttk.Combobox(row, textvariable=ln["nome"], values=nomes_buff,
                                 font=("Arial", 9), width=18).pack(side="left", padx=(0,10))
                    tk.Label(row, text="Chance%", fg="#8899cc", bg="#0f0d2e",
                             font=("Arial", 9)).pack(side="left", padx=(0,4))
                    tk.Entry(row, textvariable=ln["chance"], bg=PENT, fg=PFG,
                             insertbackground=PFG, relief="flat",
                             font=("Arial", 9), width=5).pack(side="left", padx=(0,10))
                    tk.Label(row, text="Turnos", fg="#8899cc", bg="#0f0d2e",
                             font=("Arial", 9)).pack(side="left", padx=(0,4))
                    tk.Entry(row, textvariable=ln["duracao"], bg=PENT, fg=PFG,
                             insertbackground=PFG, relief="flat",
                             font=("Arial", 9), width=5).pack(side="left")
                    def _rem_ep(i=idx2): linhas_ef_pad.pop(i); _rebuild_ef_pad()
                    tk.Button(row, text="✕", command=_rem_ep, bg=PRED, fg=PFG,
                              relief="flat", width=3, font=("Arial", 8)).pack(side="right", padx=4)

            def _add_ef_pad(nome="", chance=100, duracao=1):
                nomes  = _nomes_buffs_npc()
                nome_v = nome if nome in nomes else (nomes[0] if nomes else "")
                linhas_ef_pad.append({"nome":    tk.StringVar(value=nome_v),
                                      "chance":  tk.StringVar(value=str(chance)),
                                      "duracao": tk.StringVar(value=str(duracao))})
                _rebuild_ef_pad()

            tk.Button(frame_ativo, text="＋  Adicionar Efeito", command=_add_ef_pad,
                      bg="#4a2a6a", fg="white", relief="flat", padx=10, pady=4,
                      font=("Arial", 9), cursor="hand2").pack(anchor="w", padx=18, pady=(2,4))

            s_opt_pad   = psection(frame_ativo, "  OPÇÕES")
            var_ign_pad = tk.BooleanVar(value=False)
            r_opt_pad   = tk.Frame(s_opt_pad, bg=PCARD); r_opt_pad.pack(fill="x", padx=10, pady=4)
            tk.Checkbutton(r_opt_pad, text="Ignora Resistências", variable=var_ign_pad,
                           bg=PCARD, fg=PFG, selectcolor="#24195e",
                           activebackground=PCARD, activeforeground=PFG,
                           font=("Arial", 10)).pack(side="left")

            def _atualizar_modo(*_):
                try:    en = int(ent_energia.get() or "0")
                except: en = 0
                try:    mn = int(ent_mana_pad.get() or "0")
                except: mn = 0
                if en == 0 and mn == 0:
                    lbl_modo.config(text="▶ MODO: PASSIVO  (modificador permanente)", fg="#55cc88")
                    frame_ativo.pack_forget(); frame_passivo.pack(fill="x")
                else:
                    lbl_modo.config(text="▶ MODO: ATIVO  (gasta recurso, causa efeito)", fg="#cc8855")
                    frame_passivo.pack_forget(); frame_ativo.pack(fill="x")

            ent_energia.bind("<KeyRelease>", _atualizar_modo)
            ent_mana_pad.bind("<KeyRelease>", _atualizar_modo)

            # ── FRAME OFENSIVO ────────────────────────────────────────────
            frame_ofensivo = tk.Frame(inn2, bg=PBG)

            s_custo_of = psection(frame_ofensivo, "  CUSTO")
            r_custo_of = tk.Frame(s_custo_of, bg=PCARD); r_custo_of.pack(fill="x", padx=10, pady=4)
            tk.Label(r_custo_of, text="Energia", bg=PCARD, fg="#8899cc",
                     font=("Arial", 10), width=10, anchor="w").pack(side="left")
            ent_energia_of = tk.Entry(r_custo_of, width=6, bg=PENT, fg=PFG, insertbackground=PFG,
                                      relief="flat", highlightthickness=1,
                                      highlightbackground="#2a1f6a", highlightcolor=PACC,
                                      font=("Arial", 10))
            ent_energia_of.pack(side="left", padx=(4,20))
            tk.Label(r_custo_of, text="Mana", bg=PCARD, fg="#8899cc",
                     font=("Arial", 10), width=8, anchor="w").pack(side="left")
            ent_mana_of = tk.Entry(r_custo_of, width=6, bg=PENT, fg=PFG, insertbackground=PFG,
                                   relief="flat", highlightthickness=1,
                                   highlightbackground="#2a1f6a", highlightcolor=PACC,
                                   font=("Arial", 10))
            ent_mana_of.pack(side="left", padx=(4,0))

            s_dano_of      = psection(frame_ofensivo, "  DANO")
            linhas_dano_of = []

            def _rebuild_dano_of():
                for w in s_dano_of.winfo_children(): w.destroy()
                for idx2, ln in enumerate(linhas_dano_of):
                    lf = tk.Frame(s_dano_of, bg="#0f0d2e", relief="ridge", bd=1)
                    lf.pack(fill="x", padx=6, pady=3)
                    row = tk.Frame(lf, bg="#0f0d2e"); row.pack(fill="x", padx=8, pady=5)
                    tk.Label(row, text="Tipo", fg="#8899cc", bg="#0f0d2e",
                             font=("Arial", 9)).pack(side="left", padx=(0,4))
                    ttk.Combobox(row, textvariable=ln["tipo"], values=TIPOS_DANO_NPC,
                                 state="readonly", font=("Arial", 9),
                                 width=16).pack(side="left", padx=(0,12))
                    tk.Label(row, text="Valor", fg="#8899cc", bg="#0f0d2e",
                             font=("Arial", 9)).pack(side="left", padx=(0,4))
                    tk.Entry(row, textvariable=ln["val"], bg=PENT, fg=PFG,
                             insertbackground=PFG, relief="flat",
                             font=("Arial", 9), width=8).pack(side="left")
                    def _rem_do(i=idx2): linhas_dano_of.pop(i); _rebuild_dano_of()
                    tk.Button(row, text="✕", command=_rem_do, bg=PRED, fg=PFG,
                              relief="flat", width=3, font=("Arial", 8)).pack(side="right", padx=4)

            def _add_dano_of(tipo="contundente", val="0"):
                linhas_dano_of.append({"tipo": tk.StringVar(value=tipo),
                                       "val":  tk.StringVar(value=str(val))})
                _rebuild_dano_of()

            tk.Button(frame_ofensivo, text="＋  Adicionar Dano", command=_add_dano_of,
                      bg="#1f3a6a", fg="white", relief="flat", padx=10, pady=4,
                      font=("Arial", 9), cursor="hand2").pack(anchor="w", padx=18, pady=(2,4))

            s_ef_of       = psection(frame_ofensivo, "  EFEITOS ADICIONAIS")
            linhas_ef_of  = []

            def _rebuild_ef_of():
                for w in s_ef_of.winfo_children(): w.destroy()
                nomes_buff = _nomes_buffs_npc()
                for idx2, ln in enumerate(linhas_ef_of):
                    lf = tk.Frame(s_ef_of, bg="#0f0d2e", relief="ridge", bd=1)
                    lf.pack(fill="x", padx=6, pady=3)
                    row = tk.Frame(lf, bg="#0f0d2e"); row.pack(fill="x", padx=8, pady=5)
                    tk.Label(row, text="Efeito", fg="#8899cc", bg="#0f0d2e",
                             font=("Arial", 9)).pack(side="left", padx=(0,4))
                    if ln["nome"].get() not in nomes_buff and nomes_buff:
                        ln["nome"].set(nomes_buff[0])
                    ttk.Combobox(row, textvariable=ln["nome"], values=nomes_buff,
                                 font=("Arial", 9), width=18).pack(side="left", padx=(0,10))
                    tk.Label(row, text="Chance%", fg="#8899cc", bg="#0f0d2e",
                             font=("Arial", 9)).pack(side="left", padx=(0,4))
                    tk.Entry(row, textvariable=ln["chance"], bg=PENT, fg=PFG,
                             insertbackground=PFG, relief="flat",
                             font=("Arial", 9), width=5).pack(side="left", padx=(0,10))
                    tk.Label(row, text="Turnos", fg="#8899cc", bg="#0f0d2e",
                             font=("Arial", 9)).pack(side="left", padx=(0,4))
                    tk.Entry(row, textvariable=ln["duracao"], bg=PENT, fg=PFG,
                             insertbackground=PFG, relief="flat",
                             font=("Arial", 9), width=5).pack(side="left")
                    def _rem_eo(i=idx2): linhas_ef_of.pop(i); _rebuild_ef_of()
                    tk.Button(row, text="✕", command=_rem_eo, bg=PRED, fg=PFG,
                              relief="flat", width=3, font=("Arial", 8)).pack(side="right", padx=4)

            def _add_ef_of(nome="", chance=100, duracao=1):
                nomes  = _nomes_buffs_npc()
                nome_v = nome if nome in nomes else (nomes[0] if nomes else "")
                linhas_ef_of.append({"nome":    tk.StringVar(value=nome_v),
                                     "chance":  tk.StringVar(value=str(chance)),
                                     "duracao": tk.StringVar(value=str(duracao))})
                _rebuild_ef_of()

            tk.Button(frame_ofensivo, text="＋  Adicionar Efeito", command=_add_ef_of,
                      bg="#4a2a6a", fg="white", relief="flat", padx=10, pady=4,
                      font=("Arial", 9), cursor="hand2").pack(anchor="w", padx=18, pady=(2,4))

            s_opt_of   = psection(frame_ofensivo, "  OPÇÕES")
            var_ign_of = tk.BooleanVar(value=False)
            r_opt_of   = tk.Frame(s_opt_of, bg=PCARD); r_opt_of.pack(fill="x", padx=10, pady=4)
            tk.Checkbutton(r_opt_of, text="Ignora Resistências", variable=var_ign_of,
                           bg=PCARD, fg=PFG, selectcolor="#24195e",
                           activebackground=PCARD, activeforeground=PFG,
                           font=("Arial", 10)).pack(side="left")

            # toggle padrão ↔ ofensivo
            def _toggle_subtipo(*_):
                if var_subtipo.get() == "ofensivo":
                    frame_padrao.pack_forget(); frame_ofensivo.pack(fill="x")
                else:
                    frame_ofensivo.pack_forget(); frame_padrao.pack(fill="x")
                    _atualizar_modo()
            var_subtipo.trace_add("write", _toggle_subtipo)

            # preencher se editando
            if editando:
                ent_nome.insert(0, data_edit.get("nome", ""))
                ent_desc.insert(0, data_edit.get("descricao", ""))
                if eh_ofensivo_e:
                    ent_energia_of.insert(0, str(data_edit.get("custo_energia", 0)))
                    ent_mana_of.insert(0,    str(data_edit.get("custo_mana", 0)))
                    for d2 in data_edit.get("dano", []):
                        _add_dano_of(d2.get("tipo","contundente"), d2.get("valor", 0))
                    for ef in data_edit.get("efeitos", []):
                        _add_ef_of(ef.get("nome",""), ef.get("chance",100), ef.get("duracao",1))
                    var_ign_of.set(data_edit.get("ignora_resistencias", False))
                else:
                    ent_energia.insert(0, str(data_edit.get("custo", 0)))
                    ent_mana_pad.insert(0, str(data_edit.get("custo_mana", 0)))
                    tipo_e = data_edit.get("tipo", "passivo")
                    if tipo_e == "passivo":
                        tags = data_edit.get("tags", [])
                        vals = data_edit.get("valor", [])
                        if not isinstance(tags, list): tags = [tags]
                        if not isinstance(vals, list): vals = [vals]*len(tags)
                        for t, v in zip(tags, vals):
                            _add_passivo(cat=_detectar_cat_npc(t), tag=t, val=str(v))
                    else:
                        if data_edit.get("duracao"):
                            ent_duracao_pad.insert(0, str(data_edit["duracao"]))
                        for d2 in data_edit.get("dano", []):
                            _add_dano_pad(d2.get("tipo","contundente"), d2.get("valor",0))
                        for ef in data_edit.get("efeitos_ativos", []):
                            _add_ef_pad(ef.get("nome",""), ef.get("chance",100), ef.get("duracao",1))
                        var_ign_pad.set(data_edit.get("ignora_resistencias", False))
            else:
                _add_passivo()
                _add_dano_of()

            _toggle_subtipo()
            _atualizar_modo()

            # ── SALVAR ────────────────────────────────────────────────────
            def _salvar_hab_npc():
                nome_hab = ent_nome.get().strip()
                if not nome_hab:
                    messagebox.showwarning("Erro", "Nome é obrigatório.", parent=pop2)
                    return
                desc_hab = ent_desc.get().strip()
                cat_hab  = var_cat.get()
                ofensivo = var_subtipo.get() == "ofensivo"

                if ofensivo:
                    try:    en = int(ent_energia_of.get() or "0")
                    except: en = 0
                    try:    mn = int(ent_mana_of.get() or "0")
                    except: mn = 0
                    if not linhas_dano_of:
                        messagebox.showwarning("Erro", "Adicione ao menos um tipo de dano.", parent=pop2)
                        return
                    danos = []
                    for ln in linhas_dano_of:
                        try:    v = int(ln["val"].get())
                        except: v = 0
                        danos.append({"tipo": ln["tipo"].get(), "valor": v})
                    efeitos = []
                    for ln in linhas_ef_of:
                        n_ef = ln["nome"].get().strip()
                        if not n_ef or n_ef == "—": continue
                        try:    ch = int(ln["chance"].get())
                        except: ch = 100
                        try:    d_ef = int(ln["duracao"].get())
                        except: d_ef = 1
                        efeitos.append({"nome": n_ef, "chance": ch, "duracao": d_ef})
                    entry_dict = {
                        "nome": nome_hab, "descricao": desc_hab,
                        "categoria": cat_hab, "subtipo": "ofensivo",
                        "custo_energia": en, "custo_mana": mn,
                        "dano": danos, "efeitos": efeitos,
                        "ignora_resistencias": var_ign_of.get()
                    }
                else:
                    try:    en = int(ent_energia.get() or "0")
                    except: en = 0
                    try:    mn = int(ent_mana_pad.get() or "0")
                    except: mn = 0
                    passivo = (en == 0 and mn == 0)
                    if passivo:
                        if not linhas_passivo:
                            messagebox.showwarning("Erro", "Adicione ao menos um modificador.", parent=pop2)
                            return
                        tags_lista, valor_lista = [], []
                        for ln in linhas_passivo:
                            t = ln["tag"].get().strip()
                            if not t:
                                messagebox.showwarning("Erro", "Selecione uma tag.", parent=pop2)
                                return
                            try:    v = int(ln["val"].get())
                            except:
                                try:    v = float(ln["val"].get())
                                except:
                                    messagebox.showwarning("Erro", f"Valor inválido na tag '{t}'.", parent=pop2)
                                    return
                            tags_lista.append(t); valor_lista.append(v)
                        entry_dict = {
                            "nome": nome_hab, "descricao": desc_hab,
                            "categoria": cat_hab, "subtipo": "padrao",
                            "tipo": "passivo", "custo": 0, "custo_mana": 0,
                            "tags": tags_lista, "valor": valor_lista
                        }
                    else:
                        try:    dur = int(ent_duracao_pad.get()) if ent_duracao_pad.get().strip() else None
                        except: dur = None
                        danos = []
                        for ln in linhas_dano_pad:
                            try:    v = int(ln["val"].get())
                            except: v = 0
                            danos.append({"tipo": ln["tipo"].get(), "valor": v})
                        efeitos = []
                        for ln in linhas_ef_pad:
                            n_ef = ln["nome"].get().strip()
                            if not n_ef or n_ef == "—": continue
                            try:    ch = int(ln["chance"].get())
                            except: ch = 100
                            try:    d_ef = int(ln["duracao"].get())
                            except: d_ef = 1
                            efeitos.append({"nome": n_ef, "chance": ch, "duracao": d_ef})
                        entry_dict = {
                            "nome": nome_hab, "descricao": desc_hab,
                            "categoria": cat_hab, "subtipo": "padrao",
                            "tipo": "ativo", "custo": en, "custo_mana": mn,
                            "duracao": dur, "dano": danos, "efeitos_ativos": efeitos,
                            "ignora_resistencias": var_ign_pad.get(),
                            "tags": [], "valor": 0
                        }

                if editando:
                    npc_habs_state[idx_editar] = entry_dict
                else:
                    npc_habs_state.append(entry_dict)

                rebuild_hab()
                pop2.destroy()

            # barra de botões
            bbar = tk.Frame(pop2, bg="#090720", height=52)
            bbar.pack(fill="x", side="bottom"); bbar.pack_propagate(False)
            tk.Button(bbar, text="  ✕  Cancelar  ", command=pop2.destroy,
                      bg=PRED, fg="white", relief="flat",
                      font=("Arial", 10, "bold"), cursor="hand2",
                      pady=6).pack(side="right", padx=10, pady=8)
            tk.Button(bbar, text="  ✦  Salvar  ", command=_salvar_hab_npc,
                      bg=PGRN, fg="white", relief="flat",
                      font=("Arial", 10, "bold"), cursor="hand2",
                      pady=6).pack(side="right", padx=(0,6), pady=8)

            ent_nome.focus_set()

        # Renderiza lista inicial da coluna
        rebuild_hab()

        # ══════════════════════════════════════════════════════════════════════
        #  COL 3 — Resistências Naturais (Base)
        # ══════════════════════════════════════════════════════════════════════
        col_title(col_res, "🛡  Resistências Naturais (Base)")
        canvas_res = tk.Canvas(col_res, bg=BG_COL, highlightthickness=0)
        sb_res = ttk.Scrollbar(col_res, orient="vertical", command=canvas_res.yview)
        frm_res = tk.Frame(canvas_res, bg=BG_COL)
        frm_res.bind("<Configure>", lambda e: canvas_res.configure(scrollregion=canvas_res.bbox("all")))
        canvas_res.create_window((0,0), window=frm_res, anchor="nw")
        canvas_res.configure(yscrollcommand=sb_res.set)
        sb_res.pack(side="right", fill="y")
        canvas_res.pack(fill="both", expand=True)
        canvas_res.bind("<Enter>", lambda e: canvas_res.bind_all("<MouseWheel>", lambda ev: canvas_res.yview_scroll(int(ev.delta/-90),"units")))
        canvas_res.bind("<Leave>", lambda e: canvas_res.unbind_all("<MouseWheel>"))

        def abrir_popup_resistencia(tipo, valor_atual):
            pop = tk.Toplevel(p)
            pop.title(f"Editar {tipo.capitalize()}")
            pop.geometry("280x140")
            pop.config(bg=C["bg_mid"])
            pop.resizable(False, False)
            pop.transient(p)
            pop.grab_set()
            tk.Label(pop, text=f"{tipo.capitalize()}", font=("Segoe UI", 12, "bold"),
                     bg=C["bg_mid"], fg="white").pack(pady=10)
            frm_ed = tk.Frame(pop, bg=C["bg_mid"]); frm_ed.pack(pady=10)
            tk.Label(frm_ed, text="Valor:", bg=C["bg_mid"], fg=C["text"]).pack(side="left", padx=5)
            entry = tk.Entry(frm_ed, width=8, font=("Segoe UI", 12), justify="center",
                             bg=C["bg_card"], fg="white", insertbackground="white")
            entry.insert(0, f"{valor_atual:+d}"); entry.pack(side="left", padx=5)
            def salvar():
                try:
                    novo = int(entry.get())
                    res_base_state[tipo] = max(-100, min(100, novo))
                    rebuild_res()
                    pop.destroy()
                except:
                    entry.delete(0, tk.END); entry.insert(0, f"{valor_atual:+d}")
            tk.Button(pop, text="Salvar", command=salvar, bg=C["green"], fg="white",
                      font=("Segoe UI", 11, "bold"), relief="flat", cursor="hand2",
                      width=20).pack(pady=10)
            entry.focus_set(); entry.select_range(0, tk.END)

        def rebuild_res():
            for w in frm_res.winfo_children(): w.destroy()
            for tipo in self.TIPOS_DANO:
                base = res_base_state[tipo]
                if base >= 100:   label_txt = f"{tipo.capitalize()}: Imune";                       cor = "#4ae34a"
                elif base > 0:    label_txt = f"{tipo.capitalize()}: {base}% de resistência";      cor = "#7ec8e3"
                elif base < 0:    label_txt = f"{tipo.capitalize()}: {abs(base)}% de vulnerabilidade"; cor = "#ff9999"
                else:             label_txt = f"{tipo.capitalize()}: Normal";                       cor = C["text_dim"]
                btn = tk.Button(frm_res, text=label_txt, bg=C["bg_card"], fg=cor,
                                font=("Segoe UI", 9, "bold"), relief="raised", anchor="w",
                                cursor="hand2",
                                command=lambda t=tipo, v=base: abrir_popup_resistencia(t, v))
                btn.pack(fill="x", padx=4, pady=2)
        rebuild_res()

        # ══════════════════════════════════════════════════════════════════════
        #  COL 4 — Kits
        # ══════════════════════════════════════════════════════════════════════
        col_title(col_kits, "🎒  Kits")
        canvas_kits = tk.Canvas(col_kits, bg=BG_COL, highlightthickness=0)
        sb_kits = ttk.Scrollbar(col_kits, orient="vertical", command=canvas_kits.yview)
        frm_kits = tk.Frame(canvas_kits, bg=BG_COL)
        frm_kits.bind("<Configure>", lambda e: canvas_kits.configure(scrollregion=canvas_kits.bbox("all")))
        canvas_kits.create_window((0,0), window=frm_kits, anchor="nw")
        canvas_kits.configure(yscrollcommand=sb_kits.set)
        sb_kits.pack(side="right", fill="y")
        canvas_kits.pack(fill="both", expand=True)
        canvas_kits.bind("<Enter>", lambda e: canvas_kits.bind_all("<MouseWheel>", lambda ev: canvas_kits.yview_scroll(int(ev.delta/-90),"units")))
        canvas_kits.bind("<Leave>", lambda e: canvas_kits.unbind_all("<MouseWheel>"))

        def definir_fixo(nome):
            nonlocal kit_fixo_state
            kit_fixo_state = None if kit_fixo_state == nome else nome
            rebuild_kits()

        def rebuild_kits():
            for w in frm_kits.winfo_children(): w.destroy()
            for nome_kit in list(kits_state):
                row = tk.Frame(frm_kits, bg=C["bg_mid"]); row.pack(fill="x", padx=6, pady=2)
                texto = f"🎒 {nome_kit}"
                if nome_kit == kit_fixo_state: texto += " (Fixo)"
                tk.Label(row, text=texto, fg=C["text"], bg=C["bg_mid"],
                         font=("Segoe UI", 9)).pack(side="left", fill="x", expand=True)
                tk.Button(row, text="F", bg=C["gold"], fg="black", width=2,
                          relief="flat", cursor="hand2",
                          command=lambda n=nome_kit: definir_fixo(n)).pack(side="right", padx=2)
                tk.Button(row, text="✕", bg=C["red"], fg="white", width=2,
                          relief="flat", cursor="hand2",
                          command=lambda n=nome_kit: (kits_state.remove(n), rebuild_kits())).pack(side="right", padx=2)
            if nomes_kits:
                add_row = tk.Frame(frm_kits, bg=BG_COL); add_row.pack(fill="x", padx=6, pady=(4,6))
                cb_kit = ttk.Combobox(add_row, values=[k for k in nomes_kits if k not in kits_state],
                                      state="readonly", font=("Segoe UI", 9))
                cb_kit.pack(side="left", fill="x", expand=True)
                tk.Button(add_row, text="＋", font=("Segoe UI", 9), bg=C["green"], fg="white",
                          width=3, relief="flat", cursor="hand2",
                          command=lambda: (cb_kit.get() and cb_kit.get() not in kits_state
                                          and (kits_state.append(cb_kit.get()), rebuild_kits()))
                          ).pack(side="right", padx=2)
        rebuild_kits()

        # ══════════════════════════════════════════════════════════════════════
        #  SALVAR NPC
        # ══════════════════════════════════════════════════════════════════════
        def salvar_npc():
            nome = fields["nome"].get().strip()
            if not nome:
                messagebox.showwarning("Erro", "Nome obrigatório.", parent=p); return
            try: nivel = int(fields["nivel"].get() or 1)
            except: messagebox.showwarning("Erro", "Nível inválido.", parent=p); return

            atribs = {}
            [atribs.update({attr: var.get()}) for attr, var in attr_vars.items()]

            dados = D.carregar_npcs_raw()
            if nome_orig and nome_orig != nome: dados.pop(nome_orig, None)
            base = dict(dados.get(nome_orig or nome, {}))

            profs_save   = {k: v for k, v in profs_state.items() if v != 0}
            res_base_save = {k: v for k, v in res_base_state.items() if v != 0}

            if kit_fixo_state and kit_fixo_state not in kits_state:
                kit_fixo_final = None
            else:
                kit_fixo_final = kit_fixo_state

            # Separa habilidades e poderes de volta (salvos como dicts completos)
            habs_save    = [e for e in npc_habs_state if e.get("categoria") == "habilidade"]
            poderes_save = [e for e in npc_habs_state if e.get("categoria") == "poder"]

            dados[nome] = {
                **base,
                "nome":               nome,
                "nivel":              nivel,
                "classe":             fields["classe"].get().strip(),
                "grupo":              fields["grupo"].get().strip(),
                "proficiencias_base": profs_save,
                "habilidade_inicial": habs_save,
                "poder_inicial":      poderes_save,
                "kits":               list(kits_state),
                "kit_fixo":           kit_fixo_final,
                "resistencias_base":  res_base_save,
                "__class__":          "NPC",
                **atribs
            }
            D.salvar_npcs_raw(dados)
            self.carregar_npcs_tree()
            p.destroy()

        btn_color = C["gold"] if nome_orig else C["green"]
        tk.Button(p, text="💾  Salvar NPC", command=salvar_npc,
                  bg=btn_color, fg="white", font=("Segoe UI", 12, "bold"),
                  relief="flat", cursor="hand2", activebackground=C["accent_hi"]
                  ).place(x=650, y=CONTENT_Y + COL_H + 10, width=300, height=42)
    
    def carregar_npcs_tree(self):
        if not hasattr(self,"tree_npcs"): return
        self.tree_npcs.delete(*self.tree_npcs.get_children())
        try:
            for nome,d in D.carregar_npcs_raw().items():
                self._insert_tree(self.tree_npcs,(
                    d.get("nome",""),d.get("nivel",""),d.get("classe",""),d.get("grupo",""),
                    d.get("Forca",""),d.get("Agilidade",""),d.get("Vigor",""),
                    d.get("Inteligencia",""),d.get("Tatica",""),d.get("Presenca",""),d.get("Poder",""),
                ))
        except Exception: traceback.print_exc()
    
    # =========================================================================
    # KITS
    # =========================================================================
    def template_kits(self):
        self.limpar_container()
        c = self.container_conteudo
        self.section_title(c, "🎒  KITS DE EQUIPAMENTO")

        frm = tk.Frame(c, bg=C["bg_dark"])
        frm.place(x=20, y=58, width=1560, height=560)

        cols = ("Nome","Raridade","Conteúdo")
        self.tree_kits = self._make_tree(frm, cols, [280,140,1120])
        self.carregar_kits_na_tree()

        self.make_btn(c,"🔄",self.carregar_kits_na_tree, 1390, 630, 50, 36, C["blue"])
        self._btn_bar(c, self.novo_kit, self.editar_kit, self.remover_kit, y=630)

    def carregar_kits_na_tree(self):
        if not hasattr(self,"tree_kits"): return
        self.tree_kits.delete(*self.tree_kits.get_children())
        try:
            from Dados import carregar_kits
            kits = carregar_kits()
            for nome_kit, kit in kits.items():
                raridade = getattr(kit, "raridade", "?")
                conteudo = self.montar_string_conteudo(kit)
                self._insert_tree(self.tree_kits, (nome_kit, raridade, conteudo))
        except Exception as e:
            print(f"Erro: {e}")
            import traceback
            traceback.print_exc()

    def montar_string_conteudo(self, kit):
        """✅ CORRIGIDO: Usa listar_itens() do kit."""
        try:
            itens = kit.listar_itens()  # ✅ NOVO
            if not itens:
                return "Vazio"
            resumo = [f"{i.get('nome','?')}" for i in itens[:6]]
            txt = ", ".join(resumo)
            if len(itens) > 6:
                txt += f" +{len(itens)-6}…"
            return txt
        except:
            return "Erro"

    def novo_kit(self):
        p = self.build_popup("Novo Kit", 420, 220)
        self.make_label(p, "Nome do Kit", 20, 60, bg=C["bg_mid"])
        e_nome = self.make_entry(p, 170, 60, 220)
        self.make_label(p, "Raridade", 20, 104, bg=C["bg_mid"])
        e_rar = self.make_combobox(p, ["Comum", "Incomum", "Rara", "Épica", "Exótica", "Lendária"], 170, 104, 220)
        e_rar.current(0)
        
        def salvar():
            nome = e_nome.get().strip()
            if not nome:
                messagebox.showwarning("Erro", "Nome obrigatório.", parent=p)
                return
            try:
                from Codigos import KitEquipamento
                from Dados import salvar_kit_no_banco
                
                kit = KitEquipamento(nome=nome, itens=[], raridade=e_rar.get())  # ✅ itens=[] inicializado
                
                if salvar_kit_no_banco(kit):
                    self.carregar_kits_na_tree()
                    p.destroy()
                else:
                    messagebox.showerror("Erro", "Não foi possível salvar.", parent=p)
            except Exception as ex:
                messagebox.showerror("Erro", str(ex), parent=p)
        
        self.make_btn(p, "💾  Criar", salvar, 140, 158, 140, 36, C["green"])

    def editar_kit(self):
        sel = self.tree_kits.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um kit.")
            return
        nome_kit = self.tree_kits.item(sel[0])["values"][0]
        try:
            from Dados import carregar_kits
            kits = carregar_kits()
            if nome_kit not in kits:
                return
            self.abrir_popup_edicao_kit(kits[nome_kit])
        except Exception:
            import traceback
            traceback.print_exc()

    def remover_kit(self):
        sel = self.tree_kits.selection()
        if not sel:
            return
        nome_kit = self.tree_kits.item(sel[0])["values"][0]
        if messagebox.askyesno("Confirmar", f"Remover '{nome_kit}'?"):
            try:
                from Dados import deletar_kit_do_banco
                if deletar_kit_do_banco(nome_kit):
                    self.carregar_kits_na_tree()
            except Exception:
                import traceback
                traceback.print_exc()

    def abrir_popup_edicao_kit(self, kit):
        popup = tk.Toplevel(self)
        popup.title(f"Editar Kit: {kit.nome}")
        popup.geometry("960x680")
        popup.config(bg=C["bg_mid"])
        popup.transient(self)
        popup.grab_set()

        # ── Cabeçalho ────────────────────────────────────────────────────
        tk.Frame(popup, bg=C["accent2"]).place(x=0,y=0,width=960,height=70)

        tk.Label(popup,text="Nome:",fg="white",bg=C["accent2"],font=("Segoe UI",10,"bold")).place(x=16,y=10)
        e_nome = tk.Entry(popup,font=("Segoe UI",10))
        e_nome.insert(0,kit.nome)
        e_nome.place(x=70,y=10,width=260)

        tk.Label(popup,text="Raridade:",fg="white",bg=C["accent2"],font=("Segoe UI",10,"bold")).place(x=350,y=10)

        e_rar = ttk.Combobox(popup,values=kit.RARIDADES,state="readonly",font=("Segoe UI",10))
        e_rar.set(kit.raridade)
        e_rar.place(x=430,y=10,width=180)

        titulo_label = tk.Label(popup,text=f"🎒  {kit.nome}",fg="white",bg=C["accent2"],font=("Segoe UI",12,"bold"))
        titulo_label.place(x=16,y=38)

        # ── Área de lista com scroll ──────────────────────────────────────
        frm = tk.Frame(popup, bg=C["bg_card"])
        frm.place(x=10,y=80,width=940,height=454)

        canvas = tk.Canvas(frm, bg=C["bg_card"], highlightthickness=0)
        scrollbar = tk.Scrollbar(frm, orient="vertical", command=canvas.yview)
        items_frame = tk.Frame(canvas, bg=C["bg_card"])

        canvas.create_window((0,0), window=items_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        items_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.bind("<Enter>", lambda e: canvas.bind("<MouseWheel>", lambda ev: canvas.yview_scroll(int(-1*(ev.delta/120)), "units")))
        canvas.bind("<Leave>", lambda e: canvas.unbind("<MouseWheel>"))

        # ── Função que redesenha a lista ──────────────────────────────────
        def atualizar_arvore():
            for w in items_frame.winfo_children():
                w.destroy()

            if not kit.itens:
                tk.Label(items_frame,text="Kit vazio.",fg=C["text_dim"],bg=C["bg_card"],font=("Segoe UI",11)).pack(pady=20)
                return

            for idx, entrada in enumerate(kit.itens):
                item = entrada.get("item")
                if not item:
                    continue

                tem_id = hasattr(item,"Id") and item.Id
                unico  = bool(tem_id)
                nome   = getattr(item,"nome","Desconhecido")
                tipo   = item.__class__.__name__
                qtd    = 1 if unico else entrada.get("quantidade",1)

                row = tk.Frame(items_frame,bg=C["bg_mid"],relief="flat",bd=1)
                row.pack(fill="x",padx=4,pady=3)

                left = tk.Frame(row,bg=C["bg_mid"])
                left.pack(side="left",fill="x",expand=True,padx=8,pady=6)

                texto_nome = nome if unico else f"{nome}  x{qtd}"
                tk.Label(left,text=texto_nome,fg=C["text"],bg=C["bg_mid"],font=("Segoe UI",11),anchor="w").pack(side="left")

                label_tipo = f"({tipo}) [Único]" if unico else f"({tipo})"
                tk.Label(left,text=label_tipo,fg="#ffaa00" if unico else C["text_dim"],bg=C["bg_mid"],font=("Segoe UI",9,"bold" if unico else "normal"),anchor="e").pack(side="left",padx=6)

                right = tk.Frame(row,bg=C["bg_mid"])
                right.pack(side="right",padx=8,pady=4)

                if unico:

                    def _remover_unico(i=idx):
                        kit.remover_item(indice=i)
                        atualizar_arvore()

                    tk.Button(right,text="✕ Remover",bg=C["red"],fg="white",font=("Segoe UI",9,"bold"),relief="flat",cursor="hand2",command=_remover_unico).pack(side="left",padx=2)

                else:

                    def _diminuir(i=idx):
                        if 0<=i<len(kit.itens):
                            qtd_atual = kit.itens[i].get("quantidade",1)
                            if qtd_atual<=1:
                                kit.remover_item(indice=i)
                            else:
                                kit.itens[i]["quantidade"] = qtd_atual-1
                        atualizar_arvore()

                    tk.Button(right,text="−",width=2,font=("Arial",12,"bold"),bg=C["accent2"],fg=C["text"],relief="flat",cursor="hand2",command=_diminuir).pack(side="left",padx=1)

                    tk.Label(right,text=str(qtd),fg=C["accent_hi"],bg=C["bg_dark"],font=("Arial",11,"bold"),width=4,anchor="center").pack(side="left",padx=2)

                    def _aumentar(i=idx):
                        if 0<=i<len(kit.itens):
                            kit.itens[i]["quantidade"] = kit.itens[i].get("quantidade",1)+1
                        atualizar_arvore()

                    tk.Button(right,text="+",width=2,font=("Arial",12,"bold"),bg=C["accent2"],fg=C["text"],relief="flat",cursor="hand2",command=_aumentar).pack(side="left",padx=1)

                    def _remover_tudo(i=idx):
                        kit.remover_item(indice=i)
                        atualizar_arvore()

                    tk.Button(right,text="✕",bg=C["red"],fg="white",font=("Segoe UI",9,"bold"),relief="flat",cursor="hand2",command=_remover_tudo).pack(side="left",padx=(6,2))

        atualizar_arvore()

        # ── Barra de botões ───────────────────────────────────────────────
        btn_frame = tk.Frame(popup, bg=C["bg_mid"])
        btn_frame.place(x=10,y=544,width=940,height=56)

        self.make_btn(btn_frame,"＋ Adicionar Item",lambda: self.abrir_popup_adicionar_item_kit(kit,atualizar_arvore),10,10,180,36,C["green"])

        def salvar_kit():
            try:
                novo_nome = e_nome.get().strip()
                nova_raridade = e_rar.get()

                if not novo_nome:
                    messagebox.showwarning("Erro","Nome obrigatório.",parent=popup)
                    return

                kit.nome = novo_nome
                kit.raridade = nova_raridade
                titulo_label.config(text=f"🎒  {kit.nome}")

                from Dados import salvar_kit_no_banco
                salvar_kit_no_banco(kit)

                messagebox.showinfo("Sucesso","Kit salvo com sucesso!",parent=popup)
                self.carregar_kits_na_tree()
                popup.destroy()

            except Exception as e:
                messagebox.showerror("Erro",str(e),parent=popup)

        self.make_btn(btn_frame,"💾 Salvar",salvar_kit,810,10,120,36,C["blue"])

    def abrir_popup_adicionar_item_kit(self, kit, on_finish=None):
        if not kit:
            return

        import Dados as D

        popup = tk.Toplevel(self)
        popup.title(f"Adicionar Item ao Kit: {kit.nome}")
        popup.configure(bg="#1a0869")
        popup.geometry("900x600")

        tabelas = {
            "Armas de Fogo": "Rangeds",
            "Armas Corpo a Corpo": "Melees",
            "Proteções": "Protecoes",
            "Melhorias": "Melhorias",
            "Munições": "Municoes",
            "Itens": "Itens",
            "Consumíveis": "Consumiveis",
            "Equipamentos": "Equipamentos"
        }
        categorias = list(tabelas.keys())
        pagina_atual = {"valor": 0}

        tk.Label(
            popup,
            text=f"📦 Adicionar Itens ao Kit: {kit.nome}",
            bg="#1a0869", fg="white",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        nav_frame = tk.Frame(popup, bg="#1a0869")
        nav_frame.pack(pady=5)

        frame_listas = tk.Frame(popup, bg="#1a0869")
        frame_listas.pack(expand=True, fill="both", padx=10, pady=10)

        lista_frames = []
        qty_vars = {}

        def criar_lista(parent):
            container = tk.Frame(parent, bg="#1a0869")
            container.pack(side="left", padx=15, expand=True, fill="both")

            titulo = tk.Label(container, text="", bg="#1a0869", fg="white", font=("Arial", 12, "bold"))
            titulo.pack(pady=5)

            canvas = tk.Canvas(container, bg="#1a0869", highlightthickness=0, width=320, height=420)
            scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
            lista = tk.Frame(canvas, bg="#1a0869")

            canvas.create_window((0, 0), window=lista, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            lista.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            canvas.bind("<Enter>", lambda e: canvas.bind("<MouseWheel>", lambda ev: canvas.yview_scroll(int(-1*(ev.delta/120)), "units")))
            canvas.bind("<Leave>", lambda e: canvas.unbind("<MouseWheel>"))

            return titulo, lista

        lista_frames.append(criar_lista(frame_listas))
        lista_frames.append(criar_lista(frame_listas))

        # ── helpers para Armas de Fogo (mesmo padrão do popup universal) ──────────

        def _chave_ranged(item_tuple):
            nome, obj = item_tuple
            classe   = getattr(obj, "classe",   "")
            raridade = getattr(obj, "raridade", "")
            ci = ORDEM_CLASSES.index(classe)     if classe   in ORDEM_CLASSES   else 999
            ri = ORDEM_RARIDADES.index(raridade) if raridade in ORDEM_RARIDADES else 999
            return (ci, ri, nome)

        def _label_ranged(obj):
            if not hasattr(obj, "classe"):
                return ""
            modos = "/".join(getattr(obj, "acoes_disparo", []))
            return (
                f"  {obj.classe} · {obj.raridade}\n"
                f"  {modos} | {obj.calibre} | {obj.capacidade} proj."
            )

        # ── renderização por categoria ────────────────────────────────────────────

        def _renderizar_lista(lista_widget, cat):
            for w in lista_widget.winfo_children():
                w.destroy()

            try:
                dados = D.carregar_tabela_especifica(tabelas[cat])
            except Exception as e:
                print(f"Erro ao carregar {cat}: {e}")
                dados = {}

            if cat == "Armas de Fogo":
                itens = sorted(dados.items(), key=_chave_ranged)
            else:
                itens = list(dados.items())

            for nome, obj in itens:
                f = tk.Frame(lista_widget, bg="#1a0869")
                f.pack(fill="x", pady=3, padx=2)

                tem_id   = hasattr(obj, "Id") and obj.Id
                tipo_item = obj.__class__.__name__

                if cat == "Armas de Fogo":
                    # ✅ Botão rico igual ao popup universal (sem spinner — ranged são únicos)
                    extra    = _label_ranged(obj)
                    btn_text = f"{nome}\n{extra}".strip()
                    tk.Button(
                        f,
                        text=btn_text,
                        bg="#0e3386", fg="white",
                        width=28, font=("Arial", 10),
                        justify="left", anchor="w", wraplength=240,
                        command=lambda n=nome, o=obj, c=cat: adicionar_ao_kit(c, n, o)
                    ).pack(side="left", padx=2, pady=2)

                elif not tem_id:
                    # Stackável: botão + spinner
                    tk.Button(
                        f,
                        text=nome,
                        bg="#0e3386", fg="white",
                        width=24, font=("Arial", 10),
                        command=lambda n=nome, o=obj, c=cat: adicionar_ao_kit(c, n, o)
                    ).pack(side="left", padx=2, pady=2)

                    tk.Label(f, text=f"({tipo_item})", fg="#aaa", bg="#1a0869", font=("Arial", 8)).pack(side="left", padx=2)

                    spinner_f = tk.Frame(f, bg="#1a0869")
                    spinner_f.pack(side="right", padx=4)

                    def diminuir_popup(nome_item=nome):
                        if nome_item in qty_vars:
                            try:
                                qtd = int(qty_vars[nome_item].get())
                                if qtd > 1:
                                    qty_vars[nome_item].set(str(qtd - 1))
                            except: pass

                    tk.Button(spinner_f, text="−", width=2, font=("Arial", 10, "bold"),
                            bg="#05103a", fg="#00ff00", relief="flat",
                            command=diminuir_popup, cursor="hand2").pack(side="left", padx=1)

                    qtd_var = tk.StringVar(value="1")
                    qty_vars[nome] = qtd_var
                    tk.Entry(spinner_f, textvariable=qtd_var, width=3, font=("Arial", 9, "bold"),
                            bg="#05103a", fg="#00ff00", insertbackground="#00ff00",
                            justify="center", relief="flat", borderwidth=0).pack(side="left", padx=2)

                    def aumentar_popup(nome_item=nome):
                        if nome_item in qty_vars:
                            try:
                                qtd = int(qty_vars[nome_item].get())
                                qty_vars[nome_item].set(str(qtd + 1))
                            except: pass

                    tk.Button(spinner_f, text="+", width=2, font=("Arial", 10, "bold"),
                            bg="#05103a", fg="#00ff00", relief="flat",
                            command=aumentar_popup, cursor="hand2").pack(side="left", padx=1)

                else:
                    # Único (com ID, não-ranged): botão simples + label [Único]
                    tk.Button(
                        f,
                        text=nome,
                        bg="#0e3386", fg="white",
                        width=24, font=("Arial", 10),
                        command=lambda n=nome, o=obj, c=cat: adicionar_ao_kit(c, n, o)
                    ).pack(side="left", padx=2, pady=2)

                    tk.Label(f, text=f"({tipo_item}) [Único]", fg="#ffaa00", bg="#1a0869",
                            font=("Arial", 8, "bold")).pack(side="left", padx=2)

        def atualizar_listas():
            for idx in range(2):
                titulo, lista = lista_frames[idx]
                cat_index = pagina_atual["valor"] * 2 + idx
                if cat_index >= len(categorias):
                    titulo.config(text="")
                    for w in lista.winfo_children():
                        w.destroy()
                    continue
                cat = categorias[cat_index]
                titulo.config(text=f"📌 {cat}")
                _renderizar_lista(lista, cat)

            num_paginas = ((len(categorias) - 1) // 2) + 1
            pagina_label.config(text=f"Página {pagina_atual['valor'] + 1} / {num_paginas}")

        def adicionar_ao_kit(categoria, nome, data):
            try:
                slot_padrao = {
                    "Armas de Fogo": "mao_direita",
                    "Armas Corpo a Corpo": "mao_direita",
                    "Proteções": "peito",
                    "Melhorias": "inventario",
                    "Munições": "inventario",
                    "Itens": "inventario",
                    "Consumíveis": "inventario",
                    "Equipamentos": "inventario"
                }
                slot = slot_padrao.get(categoria, "inventario")
                item = D.reconstruct_item_from_data(data)

                tem_id = hasattr(item, "Id") and item.Id
                if not tem_id and nome in qty_vars:
                    try:
                        qtd = max(1, int(qty_vars[nome].get()))
                    except:
                        qtd = 1
                else:
                    qtd = 1

                kit.adicionar_item(item, slot, qtd)

                if nome in qty_vars:
                    qty_vars[nome].set("1")

                if on_finish:
                    on_finish()

            except Exception as e:
                print(f"❌ Erro: {e}")
                import traceback
                traceback.print_exc()

        def proxima():
            if (pagina_atual["valor"] + 1) * 2 < len(categorias):
                pagina_atual["valor"] += 1
                atualizar_listas()

        def anterior():
            if pagina_atual["valor"] > 0:
                pagina_atual["valor"] -= 1
                atualizar_listas()

        tk.Button(nav_frame, text="<< Anterior", command=anterior, bg="#0e3386", fg="white", font=("Arial", 11)).pack(side="left", padx=10)
        pagina_label = tk.Label(nav_frame, text="", bg="#1a0869", fg="white", font=("Arial", 11))
        pagina_label.pack(side="left", padx=10)
        tk.Button(nav_frame, text="Próxima >>", command=proxima, bg="#0e3386", fg="white", font=("Arial", 11)).pack(side="left", padx=10)

        atualizar_listas()

        tk.Button(popup, text="Fechar", bg="#a00c0c", fg="white", font=("Arial", 12, "bold"), command=popup.destroy).pack(pady=10)

        popup.transient(self)
        popup.grab_set()

    # =========================================================================
    # NAVEGAÇÃO
    # =========================================================================
    def TelaInicial(self):   self.controller.TelaInicial()
    def TelaDeSelecao(self): self.controller.TelaDeSelecao()
    def TelaDeCombate(self): self.controller.TelaDeCombate()
### TELA DE DICIONARIOS ###

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1600x900")
        self.title("Skirmish Engine Manager")

        self.frames = {}

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        for F in (MainScreen, CharacterSelectScreen, CharacterDetailsScreen,
                  CombatSystemScreen, MapaCombateScreen, RegrasItensScreen):
            frame = F(self, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.grid_remove()

        self.show_frame(MainScreen)
        self.after(1, self._force_draw)

    def _force_draw(self):
        self.update_idletasks(); self.update()

    def show_frame(self, cont, **kwargs):
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[cont]
        if hasattr(frame, 'refresh'):
            frame.refresh(**kwargs)
        frame.grid()
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

    def TelaInicial(self):
        self.show_frame(MainScreen)

    def TelaDeSelecao(self):
        self.show_frame(CharacterSelectScreen)

    def TelaDeCombate(self):
        self.show_frame(CombatSystemScreen)

    def TelaDeRegrasEItens(self):
        self.show_frame(RegrasItensScreen)

    def abrir_detalhes(self, character):
        self.show_frame(CharacterDetailsScreen, character=character)

    def abrir_mapa(self, grupos: dict, estado_salvo: dict, callback_estado):
        # Guarda referência à tela de combate para sincronizar distâncias
        self._tela_combate = self.frames[CombatSystemScreen]
        tela_mapa = self.frames[MapaCombateScreen]
        tela_mapa.show(grupos, estado_salvo, callback_estado)
        self.show_frame(MapaCombateScreen)

# Executar o App
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()


'''
Tela de combate:
- Botão de Regras (não essencial)

Tela de mapa de combate:
- Controle de turnos/fila/card como na tela de combate (não essencial)
- Card de personagem como na tela de combate (não essencial)
- (talvez) Direção de cobertura (não essencial)


Tela de Dados:
- Buffs/Debuffs(50%): Melhorar escolha de atributos/alvo/etc
- NPC(80%): Falta Habilidades e Poder
- Equipamento(0%): Falta tudo
'''
