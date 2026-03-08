### TELA DE COMBATE ###
### TELA DE COMBATE ###
### TELA DE COMBATE ###
class CombatSystemScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(bg='#130f26')
        self.controller = controller
        
        # Inicializar variáveis de grupo como None
        self.grupo_esquerdo = None
        self.grupo_direito = None
        
        self.slot_esquerdo_personagem = None
        self.slot_direito_personagem = None
        
        # Variável para controlar o turno atual
        self.ordem_turno = []
        self.turno_atual_index = 0
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

        self.distancias_mapa: dict = {}
        self.coberturas_mapa: dict = {}

    ### Turnos ###
    def criar_controles_turno(self):
        """Cria os botões de controle de turno"""
        tk.Button(self, text="Passar Turno", bg="#1a0869", fg="white",font=("Arial", 10, "bold"),command=self.passar_turno).place(x=450, y=100, width=100, height=50)
        tk.Button(self, text="Encerrar\nTurno Geral", bg="#4a0030", fg="white",font=("Arial", 10, "bold"),command=self.encerrar_turno_geral).place(x=450, y=150, width=100, height=50)
        tk.Button(self, text="Iniciativa", bg="#1a0869", fg="white",font=("Arial", 10, "bold"),command=self.abrir_popup_iniciativa).place(x=1050, y=150, width=100, height=50)
        tk.Button(self, text="Personagens", bg="#1a0869", fg="white",font=("Arial", 10, "bold"),command=self.abrir_popup_selecao_listas).place(x=1050, y=100, width=100, height=50)
        tk.Button(self, text="🗺 Mapa", bg="#0a3d5c", fg="white", font=("Arial", 10, "bold"), command=self._abrir_mapa).place(x=725, y=205, width=150, height=40)
        tk.Button(self, text="💰 Pilhagem", bg="#4a2200", fg="white", font=("Arial", 10, "bold"),command=self.abrir_popup_pilhagem_central).place(x=880, y=205, width=150, height=40)
        
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
        distâncias do mapa, nível de cobertura e opção de mudá-la."""

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

        # ── distâncias do mapa (do personagem no card para os demais) ────────
        distancias_do_card: dict = {}
        if char_no_card is not None and hasattr(self, "distancias_mapa"):
            distancias_do_card = self.distancias_mapa.get(char_no_card.nome, {})

        # ── cores de cobertura ───────────────────────────────────────────────
        CORES_COB = {
            "Nenhuma": None,
            "Parcial": "#ffcc00",
            "Alta":    "#ff8800",
            "Total":   "#cc0000",
        }
        NIVEIS_COB = ["Nenhuma", "Parcial", "Alta", "Total"]

        # ── linhas de personagem ─────────────────────────────────────────────
        for char in list(data_list):
            eh_destaque = (char_no_card is not None and char is char_no_card)

            # cores de fundo: dourado-escuro se for o personagem do card
            bg_item = "#3a2a00" if eh_destaque else "#220866"

            char_frame = tk.Frame(inner_frame, bg=bg_item, bd=2, relief="solid")
            char_frame.pack(fill="x", padx=5, pady=3)

            # borda destacada via configure (Frame não aceita highlightbackground facilmente)
            if eh_destaque:
                char_frame.configure(highlightbackground="#ffd700",
                                    highlightthickness=2)

            # ── linha principal (ícone + nome + PV) ─────────────────────────
            row_top = tk.Frame(char_frame, bg=bg_item)
            row_top.pack(fill="x")

            if eh_destaque:
                tk.Label(row_top, text="▶", bg=bg_item, fg="#ffd700",
                        font=("Arial", 9, "bold")).pack(side="left", padx=(4, 0))

            nome_fg  = "#ffd700" if eh_destaque else "white"
            nome_fnt = ("Arial", 10, "bold") if eh_destaque else ("Arial", 10)
            info_txt = (f"{char.nome}  •  Nv {char.Nivel}  •  "
                        f"PV {char.VidaAtual}/{char.VidaMax}")

            # ── cobertura atual do personagem ────────────────────────────────
            cobertura_char = getattr(char, "cobertura_mapa", "Nenhuma")
            cor_cob        = CORES_COB.get(cobertura_char)

            # bolinha colorida de cobertura antes do nome
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

            # ── submenu de cobertura ─────────────────────────────────────────
            submenu_cob = tk.Menu(menu, tearoff=0)
            for nivel in NIVEIS_COB:
                cor_n   = CORES_COB.get(nivel)
                icone_n = "●" if cor_n else "○"
                def _setar_cobertura(n=nivel, c=char, cor=cor_n):
                    c.cobertura_mapa = n
                    self._refresh_listas_highlight()
                    self.adicionar_log(
                        f"🛡 Cobertura de {c.nome} → {n}",
                        cor or "gray")
                submenu_cob.add_command(
                    label=f"{icone_n} {nivel}",
                    command=_setar_cobertura)
            menu.add_cascade(label="🛡 Cobertura", menu=submenu_cob)
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

            # ── linha inferior: cobertura (texto) + distância ────────────────
            row_bot = tk.Frame(char_frame, bg=bg_item)
            row_bot.pack(fill="x", padx=8, pady=(0, 4))

            # texto de cobertura
            if cobertura_char and cobertura_char != "Nenhuma":
                tk.Label(row_bot,
                        text=f"🛡 {cobertura_char}",
                        bg=bg_item, fg=cor_cob,
                        font=("Arial", 8, "bold")).pack(side="left")
            else:
                tk.Label(row_bot, text="○ Sem cobertura",
                        bg=bg_item, fg="#555555",
                        font=("Arial", 8, "italic")).pack(side="left")

            # distância em relação ao personagem do card
            if char_no_card is not None and char is not char_no_card:
                dist_val = distancias_do_card.get(char.nome)
                if dist_val is not None:
                    cor_dist = ("#ff4444" if dist_val <= 2
                                else "#ffaa00" if dist_val <= 10
                                else "#00e5ff")
                    tk.Label(row_bot,
                            text=f"↔ {dist_val:.1f} m",
                            bg=bg_item, fg=cor_dist,
                            font=("Arial", 8, "bold")).pack(side="right")
                else:
                    tk.Label(row_bot,
                            text="↔ fora do mapa",
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
                    menu_vazio.add_command(label="👊 Ataque Desarmado", state="disabled")
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
            for h in char.habilidades.listar_habilidades():
                tags = h.tags  if isinstance(h.tags,  list) else [h.tags]
                vals = h.valor if isinstance(h.valor, list) else [h.valor] * len(tags)
                efts = " | ".join(f"{t}:{'+' if v>=0 else ''}{v}" for t, v in zip(tags, vals))
                custo = f"({h.custo}E)" if h.tipo == "ativo" else "(passivo)"
                linhas.append((f"⚔️ {h.nome} {custo}  {efts}", "#90caf9", h.descricao or ""))
            if not linhas: linhas = [("Nenhuma habilidade", "#555555", "")]
            _lista_scroll(linhas, com_tooltip=True)

        def _aba_pods():
            _limpar_aba(); _ativar(btn_pods)
            linhas = []
            for p in char.poderes.listar_poderes():
                tags = p.tags  if isinstance(p.tags,  list) else [p.tags]
                vals = p.valor if isinstance(p.valor, list) else [p.valor] * len(tags)
                efts = " | ".join(f"{t}:{'+' if v>=0 else ''}{v}" for t, v in zip(tags, vals))
                custo = f"({p.custo}E)" if p.tipo == "ativo" else "(passivo)"
                linhas.append((f"🔮 {p.nome} {custo}  {efts}", "#ce93d8", p.descricao or ""))
            if not linhas: linhas = [("Nenhum poder", "#555555", "")]
            _lista_scroll(linhas, com_tooltip=True)

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

                    # Consumir
                    if isinstance(item_obj, CB.Consumivel) and \
                       str(getattr(item_obj, "uso", "")).lower() == "consumir":
                        menu.add_command(
                            label="Consumir",
                            command=lambda i=item_obj: [char.consumir_item(i), _refresh_card_e_inv()])
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

    def _abrir_mapa(self):
        """Abre o mapa de combate."""
        MapaCombate(self, D.GruposDePersonagens if hasattr(D, 'GruposDePersonagens') else {})

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
        popup.configure(bg="#1a1a2e")
        popup.geometry("1050x560")
        popup.resizable(False, False)

        todos = []
        for chave in ("_lista_superior", "_lista_inferior"):
            todos += D.GruposDePersonagens.get(chave, [])
        todos = list({id(p): p for p in todos}.values())  # dedup

        if len(todos) < 2:
            tk.Label(popup, text="São necessários ao menos 2 personagens na cena.",
                     bg="#1a1a2e", fg="red", font=("Arial", 13)).pack(pady=60)
            tk.Button(popup, text="Fechar", command=popup.destroy, bg="#8B0000", fg="white").pack()
            return

        receptor_var = tk.StringVar(value=todos[0].nome)
        alvo_var     = tk.StringVar(value=todos[1].nome if len(todos) > 1 else "")

        # Header seletores
        header = tk.Frame(popup, bg="#1a1a2e")
        header.pack(fill="x", padx=16, pady=10)

        tk.Label(header, text="Receptor:", bg="#1a1a2e", fg="#ffd700", font=("Arial", 11, "bold")).pack(side="left")
        rec_combo = ttk.Combobox(header, textvariable=receptor_var, state="readonly",
                                  values=[p.nome for p in todos], width=20)
        rec_combo.pack(side="left", padx=(4, 20))

        tk.Label(header, text="Alvo (pilhar de):", bg="#1a1a2e", fg="#ff9944", font=("Arial", 11, "bold")).pack(side="left")
        alvo_combo = ttk.Combobox(header, textvariable=alvo_var, state="readonly", width=20)
        alvo_combo.pack(side="left", padx=4)

        # Três paineis
        paineis = tk.Frame(popup, bg="#1a1a2e")
        paineis.pack(fill="both", expand=True, padx=16, pady=(0, 8))

        def _make_painel(parent, titulo, cor_titulo):
            lf = tk.LabelFrame(parent, text=titulo, bg="#130f26", fg=cor_titulo, font=("Arial", 10, "bold"))
            lf.pack(side="left", fill="both", expand=True, padx=4)
            cv = tk.Canvas(lf, bg="#130f26", highlightthickness=0)
            sb = tk.Scrollbar(lf, orient="vertical", command=cv.yview)
            cv.configure(yscrollcommand=sb.set)
            sb.pack(side="right", fill="y"); cv.pack(side="left", fill="both", expand=True)
            inner = tk.Frame(cv, bg="#130f26")
            cv.create_window((0, 0), window=inner, anchor="nw")
            inner.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
            return lf, inner

        lf_rec,  inner_rec  = _make_painel(paineis, "Inventário do Receptor", "#ffd700")
        lf_mid,  inner_mid  = _make_painel(paineis, "Itens do Alvo",          "#ff9944")
        lf_alvo, inner_alvo = _make_painel(paineis, "Inventário do Alvo",     "#aaaaaa")

        def _transferir(item_obj, alvo_obj, receptor_obj, quantidade):
            alvo_obj.inventario.remover_item(item_obj, quantidade)
            receptor_obj.inventario.adicionar_item_objeto(item_obj, quantidade)
            self.refresh(); _atualizar()

        def _pilhar_tudo():
            receptor = next((p for p in todos if p.nome == receptor_var.get()), None)
            alvo     = next((p for p in todos if p.nome == alvo_var.get()),     None)
            if not receptor or not alvo or receptor is alvo: return
            for entrada in list(alvo.inventario.itens):
                item = entrada["item"]; qtd = entrada.get("quantidade", 1)
                alvo.inventario.remover_item(item, qtd)
                receptor.inventario.adicionar_item_objeto(item, qtd)
            self.refresh(); _atualizar()

        def _atualizar(*_):
            for w in inner_rec.winfo_children():  w.destroy()
            for w in inner_mid.winfo_children():  w.destroy()
            for w in inner_alvo.winfo_children(): w.destroy()

            receptor = next((p for p in todos if p.nome == receptor_var.get()), None)
            alvo     = next((p for p in todos if p.nome == alvo_var.get()),     None)

            # Atualizar lista de alvos excluindo receptor
            outros = [p.nome for p in todos if p is not receptor]
            alvo_combo["values"] = outros
            if alvo_var.get() not in outros:
                alvo_var.set(outros[0] if outros else "")
                alvo = next((p for p in todos if p.nome == alvo_var.get()), None)

            lf_rec.config(text=f"Inventário de {receptor.nome}" if receptor else "Receptor")
            lf_alvo.config(text=f"Inventário de {alvo.nome}"    if alvo     else "Alvo")
            lf_mid.config( text=f"Itens de {alvo.nome}"         if alvo     else "Itens do Alvo")

            # Painel esquerdo — inventário do receptor (só leitura)
            if receptor:
                for entrada in receptor.inventario.itens:
                    item = entrada["item"]; qtd = entrada.get("quantidade", 1)
                    nome = getattr(item, "nome", str(item))
                    txt = f"{nome} ×{qtd}" if qtd > 1 else nome
                    tk.Label(inner_rec, text=txt, bg="#130f26", fg="#cccccc",
                             font=("Arial", 10), anchor="w").pack(fill="x", padx=8, pady=1)
                if not receptor.inventario.itens:
                    tk.Label(inner_rec, text="Inventário vazio", bg="#130f26", fg="#555",
                             font=("Arial", 9, "italic")).pack(padx=8, pady=4)

            # Painel central — itens do alvo, clicáveis para transferir
            if alvo and receptor and alvo is not receptor:
                for entrada in list(alvo.inventario.itens):
                    item = entrada["item"]; qtd = entrada.get("quantidade", 1)
                    nome = getattr(item, "nome", str(item))
                    txt = f"{nome} ×{qtd}" if qtd > 1 else nome
                    f = tk.Frame(inner_mid, bg="#1a0f35")
                    f.pack(fill="x", padx=6, pady=2)
                    lbl = tk.Label(f, text=txt, bg="#1a0f35", fg="white",
                                   font=("Arial", 10), anchor="w", cursor="hand2")
                    lbl.pack(fill="x", padx=4, pady=2)
                    lbl.bind("<Button-1>", lambda e, i=item, a=alvo, r=receptor: _transferir(i, a, r, 1))
                    lbl.bind("<Button-3>", lambda e, i=item, a=alvo, r=receptor, q=qtd: _transferir(i, a, r, q))
                    Tooltip(lbl, "Clique esquerdo: 1 item  |  Clique direito: tudo")
                if not alvo.inventario.itens:
                    tk.Label(inner_mid, text="Inventário vazio", bg="#130f26", fg="#555",
                             font=("Arial", 9, "italic")).pack(padx=8, pady=4)

            # Painel direito — inventário completo do alvo (só leitura)
            if alvo:
                for entrada in alvo.inventario.itens:
                    item = entrada["item"]; qtd = entrada.get("quantidade", 1)
                    nome = getattr(item, "nome", str(item))
                    txt = f"{nome} ×{qtd}" if qtd > 1 else nome
                    tk.Label(inner_alvo, text=txt, bg="#130f26", fg="#aaaaaa",
                             font=("Arial", 10), anchor="w").pack(fill="x", padx=8, pady=1)
                if not alvo.inventario.itens:
                    tk.Label(inner_alvo, text="Inventário vazio", bg="#130f26", fg="#555",
                             font=("Arial", 9, "italic")).pack(padx=8, pady=4)

        rec_combo.bind("<<ComboboxSelected>>",  _atualizar)
        alvo_combo.bind("<<ComboboxSelected>>", _atualizar)

        # Rodapé
        rodape = tk.Frame(popup, bg="#1a1a2e")
        rodape.pack(fill="x", padx=16, pady=(0, 10))
        tk.Button(rodape, text="💰 Pilhar Tudo", command=_pilhar_tudo,
                  bg="#7b4a00", fg="white", font=("Arial", 11), width=16).pack(side="left", padx=4)
        tk.Button(rodape, text="Fechar", command=popup.destroy,
                  bg="#3a0a80", fg="white", font=("Arial", 11), width=12).pack(side="right", padx=4)
        tk.Label(rodape, text="Painel central — Esq: 1 item  |  Dir: tudo",
                 bg="#1a1a2e", fg="#666688", font=("Arial", 8)).pack(side="left", padx=8)

        _atualizar()

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

    def abrir_popup_ataque_melee(self, atacante_pre_selecionado, titulo_extra="", arma_pre=None, callback_resultado=None):
        import random
        popup = tk.Toplevel(self)
        titulo_str = f"Ataque Melee — {atacante_pre_selecionado.nome}" + (f" {titulo_extra}" if titulo_extra else "")
        popup.title(titulo_str)
        popup.geometry("500x590")
        popup.configure(bg="#1a1a2e")
        popup.resizable(False, False)
        todos_personagens = self.get_all_personagens()
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
            }
            self.adicionar_log(f"⚔ Melee: {atacante_pre_selecionado.nome} → {alvo.nome}", cor, detalhes=detalhes)
            self.refresh()

        btn_frame = tk.Frame(main_frame, bg="#1a1a2e")
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Confirmar Ataque", command=_confirmar, bg="#38b000", fg="white", font=("Arial", 11), width=16).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Cancelar", command=popup.destroy, bg="#8B0000", fg="white", font=("Arial", 11), width=16).pack(side="left", padx=6)
        _atualizar_armas()

    def abrir_popup_ataque_ranged(self, atacante_pre_selecionado, titulo_extra="", callback_resultado=None):
        import random
        popup = tk.Toplevel(self)
        titulo_str = f"Ataque Ranged — {atacante_pre_selecionado.nome}" + (f" {titulo_extra}" if titulo_extra else "")
        popup.title(titulo_str)
        popup.geometry("520x660")
        popup.configure(bg="#1a1a2e")
        popup.resizable(False, False)
        todos_personagens = self.get_all_personagens()
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
            dist = None
            if hasattr(self, "distancias_mapa"):
                dist = self.distancias_mapa.get(atacante_pre_selecionado.nome, {}).get(alvo_obj.nome)
            if dist is not None:
                distancia_var.set(int(round(dist))); dist_origem_label.config(text="(mapa)")
            else:
                distancia_var.set(1); dist_origem_label.config(text="(manual)")
            cob = getattr(alvo_obj, "cobertura_mapa", None)
            if cob in ("Nenhuma", "Parcial", "Alta", "Total"):
                cobertura_var.set(cob); cob_origem_label.config(text="(mapa)")
            else:
                cobertura_var.set("Nenhuma"); cob_origem_label.config(text="(manual)")

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