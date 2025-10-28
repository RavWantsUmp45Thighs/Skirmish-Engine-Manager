import tkinter as tk
from tkinter import ttk, messagebox
import Dados as D
import Codigos as CB
import re, random


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
        btn_salvar = tk.Button(main_container, text="💾 Salvar Sessão Atual", 
                              command=self.salvar_sessao_atual,
                              bg="#1a5f2a", fg="white", font=("Arial", 12, "bold"),
                              relief="raised", bd=2, activebackground="#2a7f3a",
                              height=2)
        btn_salvar.pack(fill="x")
        
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

    def carregar_sessao(self, nome_sessao):
        """Carrega a sessão especificada"""
        try:
            from Dados import carregar_sessao
            
            if carregar_sessao(nome_sessao):
                tk.messagebox.showinfo("Sucesso", f"Sessão '{nome_sessao}' carregada com sucesso!")
                self.nome_sessao_atual = nome_sessao
                # Atualiza outras telas se necessário
                if hasattr(self.controller, 'atualizar_todas_telas'):
                    self.controller.atualizar_todas_telas()
            else:
                tk.messagebox.showerror("Erro", f"Erro ao carregar sessão '{nome_sessao}'")
                
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Erro ao carregar sessão: {e}")

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
            from Dados import salvar_sessao, listar_sessoes
            from tkinter import simpledialog

            # Se não houver sessão carregada, pede nome para criar nova
            if self.nome_sessao_atual:
                # Atualiza sessão existente
                if tk.messagebox.askyesno("Confirmar Atualização",
                                        f"Atualizar a sessão '{self.nome_sessao_atual}'?"):
                    if salvar_sessao(self.nome_sessao_atual, sobrescrever=True):
                        tk.messagebox.showinfo("Sucesso", f"Sessão '{self.nome_sessao_atual}' atualizada com sucesso!")
                        self.atualizar_lista_sessoes()
                    else:
                        tk.messagebox.showerror("Erro", f"Erro ao atualizar sessão '{self.nome_sessao_atual}'")
            else:
                # Cria nova sessão
                nome_novo = simpledialog.askstring("Nova Sessão",
                                                "Digite o nome para a nova sessão:",
                                                parent=self)
                if not nome_novo:
                    return

                nome_novo = nome_novo.strip()
                if not nome_novo:
                    tk.messagebox.showwarning("Aviso", "Digite um nome válido para a sessão.")
                    return

                # Verifica se já existe sessão com o mesmo nome
                sessoes_existentes = listar_sessoes()
                sessao_existe = any(s['nome'] == nome_novo for s in sessoes_existentes)

                if sessao_existe:
                    if tk.messagebox.askyesno("Confirmar Sobrescrita",
                                            f"A sessão '{nome_novo}' já existe.\nDeseja sobrescrever?"):
                        if salvar_sessao(nome_novo, sobrescrever=True):
                            tk.messagebox.showinfo("Sucesso", f"Sessão '{nome_novo}' salva com sucesso!")
                            self.nome_sessao_atual = nome_novo
                            self.atualizar_lista_sessoes()
                        else:
                            tk.messagebox.showerror("Erro", f"Erro ao salvar sessão '{nome_novo}'")
                else:
                    if salvar_sessao(nome_novo):
                        tk.messagebox.showinfo("Sucesso", f"Sessão '{nome_novo}' salva com sucesso!")
                        self.nome_sessao_atual = nome_novo
                        self.atualizar_lista_sessoes()
                    else:
                        tk.messagebox.showerror("Erro", f"Erro ao salvar sessão '{nome_novo}'")

        except Exception as e:
            tk.messagebox.showerror("Erro", f"Erro ao salvar sessão: {e}")

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
        keys = list(self.grupos_personagens.keys())
        valor_inicial = keys[0] if keys else "Sem grupos"
        self.group_var = tk.StringVar(value=valor_inicial)
        
        # Variável para o kit selecionado
        kits_keys = list(D.KitsDisponíveis.keys()) if hasattr(D, 'KitsDisponíveis') and D.KitsDisponíveis else []
        kit_inicial = kits_keys[0] if kits_keys else "Sem kits"
        self.kit_var = tk.StringVar(value=kit_inicial)
        
        self.config(bg='#130f26')

        tk.Button(self, text="Tela inicial", height=2, command=self.TelaInicial, bg="#1a0869", fg="white", font=("Arial", 20)).place(x=20, y=10, width=350, height=75)
        
        tk.Label(self, text="Seleção", fg="white", bg="#1a0869", font=("Arial", 20, "bold"), width=20, height=2).place(x=385, y=10, width=350, height=75)

        tk.Button(self, text="Combate", height=2, command=self.TelaDeCombate, bg="#1a0869", fg="white", font=("Arial", 20)).place(x=870, y=10, width=350, height=75)

        tk.Button(self, text="Informações", height=2, command=self.TelaDeRegrasEItens, bg="#1a0869", fg="white", font=("Arial", 20)).place(x=1235, y=10, width=350, height=75)

        ### --- Grupos (coluna 1) --- ###
        # --- Gerenciamento de Grupos ---
        self.group_management_frame = tk.Frame(self, bg='#1a0869')
        self.group_management_frame.place(x=20, y=120, width=450, height=80)
        self.create_group_management(self.group_management_frame)

        # --- Lista de Grupos ---
        self.group_list_frame = tk.Frame(self, bg='#1a0869')
        self.group_list_frame.place(x=20, y=210, width=450, height=470) 
        self.create_group_list_section(self.group_list_frame)

        ### --- Personagens (coluna 2) --- ###
        # --- Gerenciamento de Personagens ---
        self.char_management_frame = tk.Frame(self, bg='#1a0869')
        self.char_management_frame.place(x=490, y=120, width=450, height=80)
        self.create_char_management(self.char_management_frame)

        # --- Lista de Personagens ---
        self.char_list_frame = tk.Frame(self, bg='#1a0869')
        self.char_list_frame.place(x=490, y=210, width=450, height=470)
        self.create_list_section(self.char_list_frame)

        ### --- Kits (coluna 3) --- ###
        # --- Gerenciamento de Kits ---
        self.kit_management_frame = tk.Frame(self, bg='#1a0869')
        self.kit_management_frame.place(x=960, y=120, width=500, height=80)  # Aumentado de 450 para 500
        self.create_kit_management(self.kit_management_frame)

        # --- Lista de Kits ---
        self.kit_list_frame = tk.Frame(self, bg='#1a0869')
        self.kit_list_frame.place(x=960, y=210, width=500, height=470)
        self.create_kit_list_section(self.kit_list_frame)

### --- Grupos --- ###
    def clear_placeholder(self, event):
        if self.new_group_entry.get() == "Nome do novo grupo...":
            self.new_group_entry.delete(0, tk.END)
            self.new_group_entry.config(fg="black")

    def restore_placeholder(self, event):
        if not self.new_group_entry.get():
            self.new_group_entry.insert(0, "Nome do novo grupo...")
            self.new_group_entry.config(fg="gray")

    def create_group_management(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        # Título
        title_label = tk.Label(frame, text="Grupo de personagens", fg="white", bg="#1a0869", 
                            font=("Arial", 16, "bold"))
        title_label.place(x=10, y=5)

        # Frame para criação de novo grupo
        create_frame = tk.Frame(frame, bg='#1a0869')
        create_frame.place(x=10, y=45, width=350, height=35)

        # Entry para nome do novo grupo
        self.new_group_entry = tk.Entry(create_frame, font=("Arial", 11), bg="white", fg="black")
        self.new_group_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.new_group_entry.insert(0, "Nome do novo grupo...")
        self.new_group_entry.bind("<FocusIn>", self.clear_placeholder)
        self.new_group_entry.bind("<FocusOut>", self.restore_placeholder)

        # Botão de criar grupo
        create_group_btn = tk.Button(create_frame, text="Criar", bg="#006400", fg="white", font=("Arial", 10, "bold"), command=self.create_new_group)
        create_group_btn.pack(side="right", padx=2)

    def create_group_list_section(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        label = tk.Label(frame, text="Grupos", fg="white", bg="#1a0869", font=("Arial", 16, "bold"))
        label.place(x=10, y=10)

        canvas_frame = tk.Frame(frame, bg='#1a0869')
        canvas_frame.place(x=10, y=40, width=430, height=420)

        canvas = tk.Canvas(canvas_frame, bg="#1a0869", highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner_frame = tk.Frame(canvas, bg="#1a0869")
        canvas.create_window((0, 0), window=inner_frame, anchor='nw')
        inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        grupos = list(D.GruposDePersonagens.keys())
        
        if not grupos:
            empty_label = tk.Label(inner_frame, text="Nenhum grupo criado", 
                                fg="gray", bg="#1a0869", font=("Arial", 12, "italic"))
            empty_label.pack(pady=20)
        else:
            for grupo in grupos:
                grupo_frame = tk.Frame(inner_frame, bg="#1a0869", height=60)
                grupo_frame.pack(fill="x", pady=2, padx=5)  # Adicionado padx para espaçamento

                # Contar personagens no grupo
                num_personagens = len(D.GruposDePersonagens.get(grupo, []))
                
                grupo_button = tk.Button(grupo_frame,
                    text=f"{grupo} ({num_personagens} personagens)",
                    bg="#1a0869", fg="white", font=("Arial", 12), anchor="w", justify="left", wraplength=300,
                    command=lambda g=grupo: self.select_group(g), width=35)  # Aumentado width
                grupo_button.pack(side="left", fill="x", expand=True, padx=(0, 5), ipady=8)  # Aumentado ipady

                remove_button = tk.Button(grupo_frame, text="X", bg="red", fg="white", font=("Arial", 12, "bold"),
                    command=lambda g=grupo: self.delete_group(g), width=3)  # Definido width
                remove_button.pack(side="right", padx=5, ipady=8)  # Aumentado ipady

    def select_group(self, group_name):
        """Seleciona um grupo e atualiza a interface"""
        self.group_var.set(group_name)
        # Atualizar a lista de personagens quando um grupo é selecionado
        self.create_list_section(self.char_list_frame)

    def delete_group(self, group_name):
        """Exclui um grupo específico"""
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir o grupo '{group_name}'?\n\nTodos os personagens do grupo serão perdidos!"):
            del D.GruposDePersonagens[group_name]
            
            # Se o grupo excluído era o selecionado, selecionar outro
            if self.group_var.get() == group_name:
                remaining_groups = list(D.GruposDePersonagens.keys())
                if remaining_groups:
                    self.group_var.set(remaining_groups[0])
                else:
                    self.group_var.set("Sem grupos")
            
            self.refresh_all()
            messagebox.showinfo("Sucesso", f"Grupo '{group_name}' excluído com sucesso!")

    def create_new_group(self):
        group_name = self.new_group_entry.get().strip()
        
        if not group_name or group_name == "Nome do novo grupo...":
            messagebox.showwarning("Aviso", "Por favor, digite um nome para o grupo.")
            return
            
        if group_name in D.GruposDePersonagens:
            messagebox.showwarning("Aviso", "Este grupo já existe.")
            return
            
        # Criar novo grupo vazio diretamente em D.GruposDePersonagens
        D.GruposDePersonagens[group_name] = []
        
        # Limpar campo e selecionar novo grupo
        self.new_group_entry.delete(0, tk.END)
        self.new_group_entry.insert(0, "Nome do novo grupo...")
        self.new_group_entry.config(fg="gray")
        self.group_var.set(group_name)
        
        self.refresh_all()
        messagebox.showinfo("Sucesso", f"Grupo '{group_name}' criado com sucesso!")
### --- Grupos --- ###

### --- Personagens --- ###
    def create_char_management(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        # Título
        title_label = tk.Label(frame, text="Personagens", fg="white", bg="#1a0869",font=("Arial", 16, "bold"))
        title_label.place(x=10, y=5)

        # Botão de limpar grupo
        limpar_btn = tk.Button(frame, text="Excluir todos", bg="#8B0000", fg="white", font=("Arial", 12, "bold"), command=self.limpar_grupo_atual)
        limpar_btn.place(x=10, y=45, width=150, height=30)

    def create_list_section(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        # Mostrar grupo selecionado
        grupo_atual = self.group_var.get()
        label = tk.Label(frame, text=f"Grupo: {grupo_atual}", fg="white", bg="#1a0869", font=("Arial", 16, "bold"))
        label.place(x=10, y=10)

        canvas_frame = tk.Frame(frame, bg='#1a0869')
        canvas_frame.place(x=10, y=40, width=430, height=420)

        canvas = tk.Canvas(canvas_frame, bg="#1a0869", highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner_frame = tk.Frame(canvas, bg="#1a0869")
        canvas.create_window((0, 0), window=inner_frame, anchor='nw')
        inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        grupo = self.group_var.get()
        # Buscar no D.GruposDePersonagens
        personagens = D.GruposDePersonagens.get(grupo, [])
        
        if grupo == "Sem grupos":
            empty_label = tk.Label(inner_frame, text="Selecione um grupo para ver os personagens", 
                                fg="gray", bg="#1a0869", font=("Arial", 12, "italic"))
            empty_label.pack(pady=20)
        else:
            # Mostrar personagens existentes
            for char in personagens:
                if isinstance(char, CB.Personagem):
                    char_frame = tk.Frame(inner_frame, bg="#1a0869", height=60)
                    char_frame.pack(fill="x", pady=2, padx=5)  # Adicionado padx

                    char_button = tk.Button(char_frame,
                        text=f"{char.nome} - Nível {char.nivel} - XP:{char.XPAtual}/{char.XPlvlUp} - HP:{char.vidaAtual}/{char.vidaMax}",
                        bg="#1a0869", fg="white", font=("Arial", 12), anchor="w", justify="left", wraplength=300,
                        command=lambda c=char: self.controller.abrir_detalhes(c), width=35)  # Aumentado width
                    char_button.pack(side="left", fill="x", expand=True, padx=(0, 5), ipady=8)  # Aumentado ipady

                    remove_button = tk.Button(char_frame, text="X", bg="red", fg="white", font=("Arial", 12, "bold"),
                        command=lambda c=char: self.remove_specific_character(c), width=3)  # Definido width
                    remove_button.pack(side="right", padx=5, ipady=8)  # Aumentado ipady

            # Adicionar caixa com botões de adicionar/gerar no final (melhorada)
            add_frame = tk.Frame(inner_frame, bg="#2a2647", relief="solid", bd=1, height=80)  # Aumentado height
            add_frame.pack(fill="x", pady=10, padx=5)

            # Botão Adicionar Personagem
            add_char_btn = tk.Button(add_frame, text="Adicionar\nPersonagem", bg="#006400", fg="white", 
                                    font=("Arial", 10, "bold"), command=self.add_character_to_current_group,
                                    width=12, height=2)  # Definido width e height
            add_char_btn.pack(side="left", padx=15, pady=15)

            # Botão Gerar Vários (NOVO)
            generate_multiple_btn = tk.Button(add_frame, text="Gerar\nVários", bg="#8B4513", fg="white", 
                                            font=("Arial", 10, "bold"), command=self.gerar_varios_personagens,
                                            width=12, height=2)  # Definido width e height
            generate_multiple_btn.pack(side="left", padx=15, pady=15)

            # Botão Gerar Personagem
            generate_char_btn = tk.Button(add_frame, text="Gerar\nPersonagem", bg="#0b4f8f", fg="white", 
                                        font=("Arial", 10, "bold"), command=self.gerar_NPC_to_current_group,
                                        width=12, height=2)  # Definido width e height
            generate_char_btn.pack(side="right", padx=15, pady=15)

    def gerar_varios_personagens(self):
        """Gera vários NPCs de forma customizada"""
        # --- Passo 1: Perguntar quantidade ---
        popup_qtd = tk.Toplevel(self)
        popup_qtd.title("Gerar Vários NPCs")
        popup_qtd.geometry("300x150")
        popup_qtd.config(bg="#130f26")

        tk.Label(popup_qtd, text="Quantidade de NPCs", bg="#130f26", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        qtd_entry = tk.Entry(popup_qtd, font=("Arial", 12), justify="center")
        qtd_entry.pack(pady=5)
        qtd_entry.insert(0, "1")

        def confirmar_qtd():
            try:
                qtd = int(qtd_entry.get())
                if qtd <= 0:
                    raise ValueError
                popup_qtd.destroy()
                self._abrir_config_varios_npcs(qtd)
            except ValueError:
                messagebox.showerror("Erro", "Digite um número válido maior que 0.")

        tk.Button(popup_qtd, text="Confirmar", command=confirmar_qtd, bg="#0b8f33", fg="white",
                font=("Arial", 12, "bold")).pack(pady=10)

    def _abrir_config_varios_npcs(self, quantidade):
        """Abre janela para configuração de cada NPC"""
        current_group = self.group_var.get()
        if not current_group or current_group == "Sem grupos":
            messagebox.showwarning("Aviso", "Selecione ou crie um grupo primeiro.")
            return

        popup = tk.Toplevel(self)
        popup.title("Configurar NPCs")
        popup.geometry("700x500")
        popup.config(bg="#130f26")

        # --- Carregar NPCs e kits ---
        npcs_dados = D.carregar_npcs()
        
        # ✅ Usar D.KitsDisponíveis diretamente ao invés de carregar do DB
        if not hasattr(D, 'KitsDisponíveis') or not D.KitsDisponíveis:
            messagebox.showerror("Erro", "Nenhum kit disponível. Carregue os kits primeiro.")
            popup.destroy()
            return
        
        kits_disponiveis = D.KitsDisponíveis

        self.npcs_por_classe = npcs_dados

        # --- Criar Canvas com Scroll ---
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

        # --- Linhas de configuração ---
        self.linhas_npcs = []
        for i in range(quantidade):
            linha_frame = tk.Frame(inner_frame, bg="#2a2647", relief="solid", bd=1)
            linha_frame.pack(fill="x", pady=5)

            # Tipo de NPC
            tipo_var = tk.StringVar()
            tipos = list(self.npcs_por_classe.keys())
            tipo_menu = tk.OptionMenu(linha_frame, tipo_var, *tipos)
            tipo_menu.config(bg="#1a0869", fg="white", font=("Arial", 10), width=15)
            tipo_menu.pack(side="left", padx=5, pady=5)

            # Kit - ✅ Usar os nomes exatos de D.KitsDisponíveis
            kit_var = tk.StringVar()
            kits_opcoes = [""] + list(kits_disponiveis.keys())
            kit_menu = tk.OptionMenu(linha_frame, kit_var, *kits_opcoes)
            kit_menu.config(bg="#1a0869", fg="white", font=("Arial", 10), width=12)
            kit_menu.pack(side="left", padx=5, pady=5)

            # Equip
            equip_var = tk.StringVar(value="basico")
            equip_opcoes = [
                "equipar_tudo",
                "equipar_arma", 
                "equipar_protecoes",
                "basico"
            ]
            equip_menu = tk.OptionMenu(linha_frame, equip_var, *equip_opcoes)
            equip_menu.config(bg="#1a0869", fg="white", font=("Arial", 10), width=25)
            equip_menu.pack(side="left", padx=5, pady=5)

            # Nível
            nivel_entry = tk.Entry(linha_frame, width=5, justify="center")
            nivel_entry.insert(0, "1")
            nivel_entry.pack(side="left", padx=5)

            # Nome
            nome_entry = tk.Entry(linha_frame, width=15)
            nome_entry.pack(side="left", padx=5)

            self.linhas_npcs.append({
                "tipo_var": tipo_var,
                "kit_var": kit_var,
                "modo_var": equip_var,
                "nivel_entry": nivel_entry,
                "nome_entry": nome_entry
            })

        # --- Botão de confirmar ---
        def confirmar_geracao():
            try:
                npcs_criados = 0
                kits_aplicados = 0
                
                for linha in self.linhas_npcs:
                    tipo_npc = linha["tipo_var"].get()
                    kit_nome = linha["kit_var"].get()
                    modo = linha["modo_var"].get()
                    nivel_str = linha["nivel_entry"].get()
                    nome = linha["nome_entry"].get()

                    try:
                        nivel = int(nivel_str)
                    except ValueError:
                        nivel = 1

                    if not tipo_npc:
                        messagebox.showwarning("Aviso", "Selecione um tipo de NPC para todas as linhas.")
                        return

                    if not nome:
                        nome = f"{tipo_npc}_{random.randint(1,1000)}"

                    # --- Buscar NPC base corretamente ---
                    if tipo_npc not in self.npcs_por_classe:
                        messagebox.showwarning("Aviso", f"Tipo de NPC '{tipo_npc}' não encontrado.")
                        continue

                    npc_base = self.npcs_por_classe[tipo_npc]

                    # --- Carregar proficiências padrão ---
                    proficiencias_dados = D.carregar_proficiencias()
                    proficiencias_objetos = {}
                    for nome_prof, dados_prof in proficiencias_dados.items():
                        proficiencias_objetos[nome_prof] = CB.Proficiencia(
                            nome_prof,
                            dados_prof["atributo"],
                            nivel=0
                        )

                    # --- Criar o personagem base ---
                    personagem = CB.NPC(
                        grupo=npc_base["grupo"],
                        classe=npc_base["classe"],
                        forca=npc_base["forca"],
                        agilidade=npc_base["agilidade"],
                        vigor=npc_base["vigor"],
                        inteligencia=npc_base["inteligencia"],
                        presenca=npc_base["presenca"],
                        tatica=npc_base["tatica"]
                    )

                    # --- Gerar o NPC final com nível, nome e proficiências ---
                    personagem = CB.Gerador(
                        npc=personagem,
                        nivel=nivel,
                        nome=nome,
                        proficiencias_base=proficiencias_objetos
                    )

                    # --- Aplicar kit se houver ---
                    if kit_nome and kit_nome != "":
                        # ✅ Buscar diretamente em D.KitsDisponíveis
                        kit_obj = kits_disponiveis.get(kit_nome)
                        
                        if kit_obj:
                            try:
                                relatorio = personagem.receber_kit_avancado(kit_obj, modo)
                                if relatorio.get("sucesso", False):
                                    kits_aplicados += 1
                                else:
                                    print(f"⚠️ Falha ao aplicar kit em {nome}: {relatorio.get('erros', [])}")
                            except Exception as e:
                                print(f"❌ Erro ao aplicar kit em {nome}: {str(e)}")
                                import traceback
                                traceback.print_exc()
                        else:
                            print(f"⚠️ Kit '{kit_nome}' não encontrado")

                    # --- Adicionar NPC ao grupo selecionado ---
                    target_group = self.group_var.get()
                    if target_group not in D.GruposDePersonagens:
                        D.GruposDePersonagens[target_group] = []
                    D.GruposDePersonagens[target_group].append(personagem)
                    npcs_criados += 1

                self.refresh()
                popup.destroy()
                
                # ✅ Feedback mais detalhado
                mensagem = f"✅ {npcs_criados} personagem(ns) gerado(s) com sucesso!"
                if kits_aplicados > 0:
                    mensagem += f"\n🎒 {kits_aplicados} kit(s) aplicado(s)"
                messagebox.showinfo("Sucesso", mensagem)

            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao gerar os NPCs:\n{str(e)}")
                import traceback
                traceback.print_exc()

        tk.Button(popup, text="Confirmar", command=confirmar_geracao,
                bg="#0b8f33", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

    def limpar_grupo_atual(self):
        """Limpa todos os personagens do grupo selecionado"""
        current_group = self.group_var.get()
        
        if current_group and current_group != "Sem grupos":
            # Verificar se o grupo tem personagens
            personagens = D.GruposDePersonagens.get(current_group, [])
            
            if not personagens:
                messagebox.showinfo("Aviso", f"O grupo '{current_group}' já está vazio.")
                return
            
            # Confirmar a ação
            if messagebox.askyesno("Confirmar", 
                                 f"Tem certeza que deseja limpar todos os personagens do grupo '{current_group}'?\n\n"
                                 f"Esta ação irá remover {len(personagens)} personagem(s) e não pode ser desfeita!"):
                # Limpar o grupo
                D.GruposDePersonagens[current_group] = []
                
                # Atualizar a interface
                self.create_list_section(self.char_list_frame)
                messagebox.showinfo("Sucesso", f"Grupo '{current_group}' limpo com sucesso!")
        else:
            messagebox.showwarning("Aviso", "Selecione um grupo primeiro.")

    def add_character_to_current_group(self):
        current_group = self.group_var.get()
        if current_group and current_group != "Sem grupos":
            # Passar o grupo atual diretamente para a função
            self.add_character_with_group(current_group)
        else:
            messagebox.showwarning("Aviso", "Selecione ou crie um grupo primeiro.")

    def gerar_NPC_to_current_group(self):
        current_group = self.group_var.get()
        if current_group and current_group != "Sem grupos":
            # Passar o grupo atual diretamente para a função
            self.gerar_NPC_with_group(current_group)
        else:
            messagebox.showwarning("Aviso", "Selecione ou crie um grupo primeiro.")

    def add_character_with_group(self, target_group):
        """Adiciona personagem diretamente ao grupo especificado sem mostrar seleção de grupo"""
        popup = tk.Toplevel(self)
        popup.title("Criar Novo Personagem")
        popup.geometry("400x600")
        popup.config(bg="#130f26")

        # Mostrar grupo de destino (apenas informativo)
        tk.Label(popup, text=f"Adicionando ao grupo: {target_group}", bg="#130f26", fg="white", 
                font=("Arial", 12, "bold")).pack(pady=10)

        campos = ["Nome", "Nível", "Força", "Agilidade", "Vigor", "Inteligência", "Presença", "Tática"]
        entradas = {}

        for i, campo in enumerate(campos):
            tk.Label(popup, text=campo, bg="#130f26", fg="white", font=("Arial", 12)).pack(pady=(5 if i else 10, 0))
            entrada = tk.Entry(popup, font=("Arial", 12))
            entrada.pack()
            entradas[campo] = entrada

        def confirmar():
            try:
                nome = entradas["Nome"].get()
                nivel = int(entradas["Nível"].get())
                Forca = int(entradas["Força"].get())
                Agilidade = int(entradas["Agilidade"].get())
                Vigor = int(entradas["Vigor"].get())
                Inteligencia = int(entradas["Inteligência"].get())
                Presenca = int(entradas["Presença"].get())
                Tatica = int(entradas["Tática"].get())

                # Cria o personagem com as proficiências padrão usando a nova função
                proficiencias_dados = D.carregar_proficiencias()
                proficiencias_objetos = {}
                for nome_prof, dados_prof in proficiencias_dados.items():
                    proficiencias_objetos[nome_prof] = CB.Proficiencia(
                        nome_prof, 
                        dados_prof["atributo"], 
                        nivel=0  # Nível inicial 0 para todas as proficiências
                    )
                
                novo_personagem = CB.Personagem(nome, nivel, Forca, Agilidade, Vigor, Inteligencia, Presenca, Tatica, proficiencias_base=proficiencias_objetos)

                # Adicionar ao grupo especificado
                if target_group in D.GruposDePersonagens:
                    D.GruposDePersonagens[target_group].append(novo_personagem)

                popup.destroy()
                self.refresh()
            except ValueError:
                messagebox.showerror("Erro", "Preencha todos os campos corretamente!")

        tk.Button(popup, text="Confirmar", command=confirmar, bg="#1a0869", fg="white", font=("Arial", 14), width=20).pack(pady=20)

    def gerar_NPC_with_group(self, target_group):
        """Gera NPC diretamente no grupo especificado sem mostrar seleção de grupo"""

        popup = tk.Toplevel(self)
        popup.title("Gerar NPC")
        popup.geometry("400x400")
        popup.config(bg="#130f26")

        # Mostrar grupo de destino (apenas informativo)
        tk.Label(popup, text=f"Adicionando ao grupo: {target_group}", bg="#130f26", fg="white", 
                font=("Arial", 12, "bold")).pack(pady=10)

        entradas = {}

        # --- Carregar NPCs usando a nova função ---
        npcs_dados = D.carregar_npcs()
        
        if not npcs_dados:
            messagebox.showerror("Erro", "Não foi possível carregar os tipos de NPCs do banco de dados.")
            popup.destroy()
            return

        # Organizar NPCs por grupo (facção)
        npcs_por_grupo = {}
        for classe, npc_data in npcs_dados.items():
            grupo = npc_data.get("grupo", "Sem Grupo")
            if grupo not in npcs_por_grupo:
                npcs_por_grupo[grupo] = []
            npcs_por_grupo[grupo].append(npc_data)

        # --- Grupo (Facção) ---
        tk.Label(popup, text="Grupo (Facção)", bg="#130f26", fg="white", font=("Arial", 12)).pack(pady=(10, 0))
        grupos_npcs = list(npcs_por_grupo.keys())
        grupo_var = tk.StringVar(value=grupos_npcs[0] if grupos_npcs else "")
        grupo_menu = tk.OptionMenu(popup, grupo_var, *grupos_npcs)
        grupo_menu.config(bg="#1a0869", fg="white", font=("Arial", 12), width=30)
        grupo_menu.pack(pady=5)
        entradas["Grupo"] = grupo_var

        # --- Classe do NPC ---
        tk.Label(popup, text="Classe do NPC", bg="#130f26", fg="white", font=("Arial", 12)).pack(pady=(10, 0))
        classe_var = tk.StringVar()
        classe_menu = tk.OptionMenu(popup, classe_var, "")
        classe_menu.config(bg="#1a0869", fg="white", font=("Arial", 12), width=30)
        classe_menu.pack(pady=5)
        entradas["Classe"] = classe_var

        def atualizar_classes(*_):
            grupo_escolhido = grupo_var.get()
            npcs_grupo = npcs_por_grupo.get(grupo_escolhido, [])
            classes = [npc["classe"] for npc in npcs_grupo]
            menu = classe_menu["menu"]
            menu.delete(0, "end")
            if classes:
                classe_var.set(classes[0])
                for c in classes:
                    menu.add_command(label=c, command=lambda value=c: classe_var.set(value))
            else:
                classe_var.set("")

        grupo_var.trace_add("write", atualizar_classes)
        atualizar_classes()

        # --- Nível ---
        tk.Label(popup, text="Nível do NPC", bg="#130f26", fg="white", font=("Arial", 12)).pack(pady=(10, 0))
        nivel_entry = tk.Entry(popup, font=("Arial", 12), width=5, justify="center")
        nivel_entry.insert(0, str(random.randint(1, 1)))
        nivel_entry.pack(pady=5)
        entradas["Nivel"] = nivel_entry

        # --- Nome ---
        tk.Label(popup, text="Nome do NPC (opcional)", bg="#130f26", fg="white", font=("Arial", 12)).pack(pady=(10, 0))
        nome_entry = tk.Entry(popup, font=("Arial", 12), width=25, justify="center")
        nome_entry.pack(pady=5)
        entradas["Nome"] = nome_entry

        # --- Confirmar ---
        def confirmar():
            try:
                grupo = entradas["Grupo"].get()
                classe_nome = entradas["Classe"].get()
                nivel = int(entradas["Nivel"].get())
                nome = entradas["Nome"].get() or f"{classe_nome}_{random.randint(1, 50)}"

                # Buscar NPC base usando a nova estrutura
                npcs_grupo = npcs_por_grupo.get(grupo, [])
                npc_base = next((npc for npc in npcs_grupo if npc["classe"] == classe_nome), None)
                
                if not npc_base:
                    raise ValueError("Classe não encontrada no grupo.")

                # Criar NPC
                npc = CB.NPC(grupo, npc_base["classe"], npc_base["forca"], npc_base["agilidade"],
                        npc_base["vigor"], npc_base["inteligencia"], npc_base["presenca"], npc_base["tatica"])

                # Carregar proficiências usando a nova função
                proficiencias_dados = D.carregar_proficiencias()
                proficiencias_objetos = {}
                for nome_prof, dados_prof in proficiencias_dados.items():
                    proficiencias_objetos[nome_prof] = CB.Proficiencia(
                        nome_prof, 
                        dados_prof["atributo"], 
                        nivel=0  # Nível inicial 0 para todas as proficiências
                    )
                
                # Criar personagem
                personagem = CB.Gerador(npc=npc, nivel=nivel, nome=nome, proficiencias_base=proficiencias_objetos)

                self.carregar_armas_e_armaduras(personagem)
                
                # Adicionar ao grupo especificado
                if target_group in D.GruposDePersonagens:
                    D.GruposDePersonagens[target_group].append(personagem)

                self.refresh()
                popup.destroy()

            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o NPC:\n{e}")

        tk.Button(popup, text="Confirmar", command=confirmar, bg="#0b8f33", fg="white",
                font=("Arial", 12, "bold")).pack(pady=20)

    def remove_specific_character(self, character):
        selected_group = self.group_var.get()
        print(f"Removendo personagem: {character.nome} do grupo {selected_group}")
        
        if selected_group in D.GruposDePersonagens:
            try:
                D.GruposDePersonagens[selected_group].remove(character)
                # Atualizar a interface após remover
                self.create_list_section(self.char_list_frame)
            except ValueError:
                print("Personagem não encontrado no grupo.")
### --- Personagens --- ###

### --- Kits --- ###
    def create_kit_management(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        # Título
        title_label = tk.Label(frame, text="Kits de itens", fg="white", bg="#1a0869", font=("Arial", 16, "bold"))
        title_label.place(x=10, y=5)

        # Botão para refresh dos kits
        refresh_kits_btn = tk.Button(frame, text="Atualizar lista", bg="#0b4f8f", fg="white", font=("Arial", 12, "bold"), command=self.refresh_kits)
        refresh_kits_btn.place(x=10, y=45, width=150, height=30)
        try:
            D.refresh_kits()
        except Exception as e:
            print(f"Erro ao carregar kits automaticamente: {e}")

    def create_kit_list_section(self, frame):
        # Limpa widgets antigos
        for widget in frame.winfo_children():
            widget.destroy()

        # Armazenar referência do frame atual
        self.current_frame = frame

        label = tk.Label(frame, text="Kits Disponíveis", fg="white", bg="#1a0869", font=("Arial", 16, "bold"))
        label.place(x=10, y=10)

        # Frame principal com canvas + scrollbar
        canvas_frame = tk.Frame(frame, bg='#1a0869')
        canvas_frame.place(x=10, y=40, width=480, height=420)

        canvas = tk.Canvas(canvas_frame, bg="#1a0869", highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner_frame = tk.Frame(canvas, bg="#1a0869")
        window = canvas.create_window((0, 0), window=inner_frame, anchor='nw')

        # Faz o inner_frame sempre ocupar a largura visível do canvas
        def resize_inner(event):
            canvas.itemconfig(window, width=event.width)
        canvas.bind("<Configure>", resize_inner)

        # Atualiza scrollregion conforme o conteúdo cresce
        inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Scroll com roda do mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Carregar kits
        kits = D.KitsDisponíveis if hasattr(D, 'KitsDisponíveis') and D.KitsDisponíveis else {}
        
        if not kits:
            empty_label = tk.Label(inner_frame, text="Nenhum kit disponível", 
                                fg="gray", bg="#1a0869", font=("Arial", 12, "italic"))
            empty_label.pack(pady=20)
        else:
            # Organizar kits por raridade
            kits_por_raridade = {}
            for nome, kit in kits.items():
                # Suportar tanto objetos quanto dicionários
                if isinstance(kit, dict):
                    raridade = kit.get('raridade', 'Comum')
                else:
                    raridade = getattr(kit, 'raridade', 'Comum')
                
                kits_por_raridade.setdefault(raridade, []).append((nome, kit))

            # Mostrar por raridade
            for raridade in sorted(kits_por_raridade.keys()):
                # Cabeçalho
                raridade_frame = tk.Frame(inner_frame, bg="#2a2647", relief="solid", bd=1)
                raridade_frame.pack(fill="x", pady=(10, 2), padx=5)
                
                raridade_label = tk.Label(raridade_frame, text=f"Raridade: {raridade}", 
                                        fg="yellow", bg="#2a2647", font=("Arial", 12, "bold"))
                raridade_label.pack(pady=3, anchor="w", padx=5)

                # Kits desta raridade
                for nome_kit, kit_obj in kits_por_raridade[raridade]:
                    kit_frame = tk.Frame(inner_frame, bg="#2a2647")
                    kit_frame.pack(fill="x", pady=2, padx=5)

                    # Contar itens - suportar dict e objeto
                    if isinstance(kit_obj, dict):
                        itens_kit = kit_obj.get('itens', [])
                        if isinstance(itens_kit, dict):
                            total_itens = sum(item.get('quantidade', 0) for item in itens_kit.values())
                            tipos_itens = len(itens_kit)
                        else:
                            total_itens = sum(item.get('quantidade', 0) for item in itens_kit)
                            tipos_itens = len(itens_kit)
                    else:
                        itens_kit = kit_obj.listar_itens()
                        total_itens = sum(item["quantidade"] for item in itens_kit)
                        tipos_itens = len(itens_kit)

                    # Botão principal - agora expande corretamente
                    kit_button = tk.Button(
                        kit_frame,
                        text=f"{nome_kit}\n{tipos_itens} tipos de itens ({total_itens} total)",
                        bg="#1a0869", fg="white", font=("Arial", 11), anchor="w", justify="left",
                        command=lambda k=kit_obj: self.show_kit_contents(k),
                        wraplength=400,
                        height=3
                    )
                    kit_button.pack(side="left", fill="x", expand=True, padx=(0, 5), pady=2)

                    # Botão de apagar - fixo à direita
                    delete_button = tk.Button(
                        kit_frame, text="Apagar", bg="#DC143C", fg="white", 
                        font=("Arial", 9, "bold"), width=10,
                        command=lambda k=nome_kit: self.delete_kit(k)
                    )
                    delete_button.pack(side="right", padx=5)

    def show_kit_contents(self, kit_obj):
        """Mostra popup com conteúdo do kit e opção de dar kit"""
        # Encontrar a janela principal - ajustado para funcionar com diferentes classes
        parent = self
        while hasattr(parent, 'parent') and parent.parent:
            parent = parent.parent
        
        # Se não encontrou parent, usar a própria instância
        if not hasattr(parent, 'winfo_toplevel'):
            parent = self.winfo_toplevel() if hasattr(self, 'winfo_toplevel') else None
        
        popup = tk.Toplevel(parent)
        
        # Suportar dict e objeto para o nome
        if isinstance(kit_obj, dict):
            kit_nome = kit_obj.get('nome', 'Kit sem nome')
            kit_raridade = kit_obj.get('raridade', 'Comum')
        else:
            kit_nome = getattr(kit_obj, 'nome', 'Kit sem nome')
            kit_raridade = getattr(kit_obj, 'raridade', 'Comum')
        
        popup.title(f"Conteúdo do Kit: {kit_nome}")
        popup.geometry("450x600")
        popup.configure(bg="#1a0869")
        popup.resizable(False, False)
        
        # Centralizar o popup
        if parent:
            popup.transient(parent)
        popup.grab_set()
        
        # Título
        title_label = tk.Label(popup, text=f"Kit: {kit_nome}", 
                            fg="white", bg="#1a0869", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Informações do kit
        info_frame = tk.Frame(popup, bg="#2a2647", relief="solid", bd=1)
        info_frame.pack(pady=5, padx=15, fill="x")
        
        kit_info = tk.Label(info_frame, text=f"Raridade: {kit_raridade}", 
                        fg="yellow", bg="#2a2647", font=("Arial", 12, "bold"))
        kit_info.pack(pady=5)
        
        # Frame para o conteúdo com scroll
        content_label = tk.Label(popup, text="Conteúdo do Kit:", 
                                fg="white", bg="#1a0869", font=("Arial", 14, "bold"))
        content_label.pack(pady=(10, 5))
        
        content_frame = tk.Frame(popup, bg="#1a0869")
        content_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        
        canvas = tk.Canvas(content_frame, bg="#1a0869", highlightthickness=0)
        scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        inner_frame = tk.Frame(canvas, bg="#1a0869")
        canvas.create_window((0, 0), window=inner_frame, anchor='nw')
        
        # Mostrar itens do kit - suportar dict e objeto
        if isinstance(kit_obj, dict):
            itens_kit = kit_obj.get('itens', [])
            if isinstance(itens_kit, dict):
                itens_kit = [{'nome': nome, 'quantidade': dados.get('quantidade', 0)} 
                            for nome, dados in itens_kit.items()]
        else:
            itens_kit = kit_obj.listar_itens()
        
        if not itens_kit:
            empty_label = tk.Label(inner_frame, text="Kit vazio", 
                                fg="gray", bg="#1a0869", font=("Arial", 12, "italic"))
            empty_label.pack(pady=20)
        else:
            for i, item in enumerate(itens_kit):
                item_frame = tk.Frame(inner_frame, bg="#2a2647", relief="solid", bd=1)
                item_frame.pack(fill="x", pady=2, padx=5)
                
                item_nome = item.get('nome', 'Item sem nome')
                item_qtd = item.get('quantidade', 0)
                
                item_label = tk.Label(item_frame, 
                                    text=f"• {item_nome} - Quantidade: {item_qtd}", 
                                    fg="white", bg="#2a2647", font=("Arial", 11), anchor="w")
                item_label.pack(pady=8, padx=15, fill="x")
        
        inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Frame para botões na parte inferior
        buttons_frame = tk.Frame(popup, bg="#1a0869")
        buttons_frame.pack(fill="x", padx=15, pady=15)
        
        # Botão "Dar Kit"
        dar_button = tk.Button(buttons_frame, text="Dar Kit aos Personagens", bg="#228B22", fg="white", 
                            font=("Arial", 12, "bold"), height=2,
                            command=lambda: self.show_dar_kit_popup(kit_obj, popup))
        dar_button.pack(fill="x", pady=(0, 10))
        
        # Botão "Fechar"
        close_button = tk.Button(buttons_frame, text="Fechar", bg="#666666", fg="white", 
                            font=("Arial", 11, "bold"), width=15,
                            command=popup.destroy)
        close_button.pack()

    def show_dar_kit_popup(self, kit_obj, parent_popup=None):
        """Mostra popup para dar kit com seleção de grupo, personagens e modo de aplicação"""
        # Fechar popup pai se existir
        if parent_popup:
            parent_popup.destroy()
        
        # Encontrar a janela principal
        parent = self
        while hasattr(parent, 'parent') and parent.parent:
            parent = parent.parent
        
        if not hasattr(parent, 'winfo_toplevel'):
            parent = self.winfo_toplevel() if hasattr(self, 'winfo_toplevel') else None
        
        popup = tk.Toplevel(parent)
        popup.title(f"Dar Kit: {kit_obj.nome}")
        popup.geometry("580x750")  # Aumentei um pouco a altura
        popup.config(bg="#130f26")
        popup.resizable(False, False)
        
        if parent:
            popup.transient(parent)
        popup.grab_set()

        # Título (fixo no topo)
        header_frame = tk.Frame(popup, bg="#130f26")
        header_frame.pack(fill="x", padx=15, pady=(15, 5))
        
        title_label = tk.Label(header_frame, text=f"Dar Kit: {kit_obj.nome}", 
                            fg="white", bg="#130f26", font=("Arial", 16, "bold"))
        title_label.pack()

        kit_info = tk.Label(header_frame, text=f"Raridade: {kit_obj.raridade}", 
                        fg="yellow", bg="#130f26", font=("Arial", 12, "bold"))
        kit_info.pack(pady=5)

        # Frame principal com scroll para todo o conteúdo
        main_canvas_frame = tk.Frame(popup, bg="#130f26")
        main_canvas_frame.pack(fill="both", expand=True, padx=15, pady=5)

        # Canvas e scrollbar principal
        main_canvas = tk.Canvas(main_canvas_frame, bg="#130f26", highlightthickness=0)
        main_scrollbar = tk.Scrollbar(main_canvas_frame, orient="vertical", command=main_canvas.yview)
        main_canvas.configure(yscrollcommand=main_scrollbar.set)

        main_scrollbar.pack(side="right", fill="y")
        main_canvas.pack(side="left", fill="both", expand=True)

        # Frame interno que conterá todo o conteúdo
        scrollable_frame = tk.Frame(main_canvas, bg="#130f26")
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

        # --- Seleção de Grupo ---
        grupo_frame = tk.Frame(scrollable_frame, bg="#1a0869", relief="solid", bd=2)
        grupo_frame.pack(pady=10, padx=5, fill="x")

        tk.Label(grupo_frame, text="1. Selecionar Grupo:", fg="white", bg="#1a0869", 
                font=("Arial", 14, "bold")).pack(pady=8)

        grupos_disponiveis = list(D.GruposDePersonagens.keys())
        if not grupos_disponiveis:
            tk.Label(grupo_frame, text="Nenhum grupo disponível", fg="gray", bg="#1a0869", 
                    font=("Arial", 12, "italic")).pack(pady=10)
            return

        grupo_var = tk.StringVar(value=grupos_disponiveis[0])
        grupo_menu = tk.OptionMenu(grupo_frame, grupo_var, *grupos_disponiveis)
        grupo_menu.config(bg="#2a2647", fg="white", font=("Arial", 12), width=40, relief="solid")
        grupo_menu.pack(pady=8)

        # --- Modo de Aplicação ---
        modo_frame = tk.Frame(scrollable_frame, bg="#1a0869", relief="solid", bd=2)
        modo_frame.pack(pady=10, padx=5, fill="x")

        tk.Label(modo_frame, text="2. Modo de Aplicação:", fg="white", bg="#1a0869", 
                font=("Arial", 14, "bold")).pack(pady=8)

        modo_var = tk.StringVar(value="basico")

        modos = [
            ("basico", "Básico", "Apenas adicionar itens ao inventário"),
            ("equipar_protecoes", "Equipar Proteções", "Adicionar e equipar proteções automaticamente"),
            ("equipar_arma", "Equipar Arma", "Adicionar e equipar uma arma aleatória do kit"),
            ("equipar_tudo", "Equipar Tudo", "Equipar proteções e arma automaticamente")
        ]

        for valor, titulo, descricao in modos:
            modo_item_frame = tk.Frame(modo_frame, bg="#2a2647", relief="solid", bd=1)
            modo_item_frame.pack(fill="x", pady=3, padx=10)
            
            rb = tk.Radiobutton(modo_item_frame, text=titulo, variable=modo_var, value=valor,
                            bg="#2a2647", fg="white", selectcolor="#1a0869", 
                            font=("Arial", 11, "bold"), anchor="w")
            rb.pack(fill="x", padx=10, pady=3)
            
            desc_label = tk.Label(modo_item_frame, text=f"  └ {descricao}", 
                                fg="lightgray", bg="#2a2647", font=("Arial", 9), anchor="w")
            desc_label.pack(fill="x", padx=20, pady=(0, 5))

        # --- Lista de Personagens ---
        personagens_frame = tk.Frame(scrollable_frame, bg="#1a0869", relief="solid", bd=2)
        personagens_frame.pack(pady=10, padx=5, fill="x")

        tk.Label(personagens_frame, text="3. Selecionar Personagens:", fg="white", bg="#1a0869", 
                font=("Arial", 14, "bold")).pack(pady=8)

        # Canvas para lista de personagens (scroll interno para personagens)
        canvas_frame = tk.Frame(personagens_frame, bg='#1a0869')
        canvas_frame.pack(pady=8, padx=10, fill="x")

        # Definir altura fixa para a lista de personagens
        canvas_frame.config(height=200)
        canvas_frame.pack_propagate(False)

        canvas = tk.Canvas(canvas_frame, bg="#1a0869", highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner_frame = tk.Frame(canvas, bg="#1a0869")
        canvas.create_window((0, 0), window=inner_frame, anchor='nw')
        inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Variáveis para checkboxes dos personagens
        personagem_vars = {}

        def atualizar_personagens():
            # Limpar frame
            for widget in inner_frame.winfo_children():
                widget.destroy()
            personagem_vars.clear()

            grupo_selecionado = grupo_var.get()
            personagens = D.GruposDePersonagens.get(grupo_selecionado, [])

            if not personagens:
                tk.Label(inner_frame, text="Nenhum personagem no grupo selecionado", 
                        fg="gray", bg="#1a0869", font=("Arial", 12, "italic")).pack(pady=20)
            else:
                # Botão para selecionar/deselecionar todos
                select_all_frame = tk.Frame(inner_frame, bg="#2a2647", relief="solid", bd=2)
                select_all_frame.pack(fill="x", pady=5, padx=3)

                select_all_var = tk.BooleanVar(value=True)
                
                def toggle_all():
                    valor = select_all_var.get()
                    for var in personagem_vars.values():
                        var.set(valor)

                tk.Checkbutton(select_all_frame, text="Selecionar/Deselecionar Todos", 
                            variable=select_all_var, command=toggle_all,
                            bg="#2a2647", fg="yellow", selectcolor="#1a0869", 
                            font=("Arial", 11, "bold")).pack(pady=5)

                # Lista de personagens
                for char in personagens:
                    if isinstance(char, CB.Personagem):
                        char_frame = tk.Frame(inner_frame, bg="#2a2647", relief="solid", bd=1)
                        char_frame.pack(fill="x", pady=2, padx=3)

                        char_var = tk.BooleanVar(value=True)  # Selecionado por padrão
                        personagem_vars[char] = char_var

                        # Informações do personagem
                        char_info = f"{char.nome} | Nível {char.nivel} | HP: {char.vidaAtual}/{char.vidaMax}"
                        
                        tk.Checkbutton(char_frame, text=char_info, variable=char_var, 
                                    bg="#2a2647", fg="white", selectcolor="#1a0869", 
                                    font=("Arial", 10), anchor="w").pack(fill="x", padx=10, pady=5)

            # Atualizar scroll do canvas de personagens
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
            
            # Atualizar scroll principal
            scrollable_frame.update_idletasks()
            main_canvas.configure(scrollregion=main_canvas.bbox("all"))

        # Atualizar personagens quando o grupo mudar
        grupo_var.trace_add("write", lambda *_: atualizar_personagens())
        atualizar_personagens()

        # Configurar scroll do frame principal
        def configure_scroll(event):
            main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        
        scrollable_frame.bind("<Configure>", configure_scroll)

        # --- Botões de Ação (fixos na parte inferior) ---
        button_frame = tk.Frame(popup, bg="#130f26")
        button_frame.pack(fill="x", padx=15, pady=15)

        def aplicar_kit():
            personagens_selecionados = [char for char, var in personagem_vars.items() if var.get()]
            
            if not personagens_selecionados:
                messagebox.showwarning("Aviso", "Selecione pelo menos um personagem.")
                return

            modo = modo_var.get()
            modo_texto = next(titulo for valor, titulo, _ in modos if valor == modo)
            
            # Confirmar ação
            confirmacao = f"""Confirmar aplicação do kit:

    Kit: {kit_obj.nome}
    Raridade: {kit_obj.raridade}
    Personagens: {len(personagens_selecionados)} selecionado(s)
    Modo: {modo_texto}

    Deseja continuar?"""
            
            if not messagebox.askyesno("Confirmar Aplicação", confirmacao):
                return

            try:
                sucessos = 0
                falhas = []
                detalhes_sucesso = []
                
                for char in personagens_selecionados:
                    try:
                        relatorio = char.receber_kit_avancado(kit_obj, modo)
                        if relatorio["sucesso"]:
                            sucessos += 1
                            if relatorio.get("detalhes"):
                                detalhes_sucesso.append(f"{char.nome}: {relatorio['detalhes']}")
                        else:
                            falhas.append(f"{char.nome}: {', '.join(relatorio.get('erros', ['Erro desconhecido']))}")
                    except Exception as e:
                        falhas.append(f"{char.nome}: {str(e)}")

                # Mostrar resultado detalhado
                if not falhas:
                    resultado = f"✅ Kit '{kit_obj.nome}' aplicado com sucesso!\n\n"
                    resultado += f"Personagens afetados: {sucessos}\n"
                    resultado += f"Modo: {modo_texto}\n\n"
                    if detalhes_sucesso:
                        resultado += "Detalhes:\n" + "\n".join(detalhes_sucesso[:3])
                        if len(detalhes_sucesso) > 3:
                            resultado += f"\n... e mais {len(detalhes_sucesso) - 3} aplicação(ões)"
                            
                    messagebox.showinfo("Sucesso Total", resultado)
                else:
                    resultado = f"Resultado da aplicação do kit '{kit_obj.nome}':\n\n"
                    resultado += f"✅ Sucessos: {sucessos}\n❌ Falhas: {len(falhas)}\n\n"
                    
                    if falhas:
                        resultado += "Detalhes das falhas:\n"
                        resultado += "\n".join(falhas[:3])
                        if len(falhas) > 3:
                            resultado += f"\n... e mais {len(falhas) - 3} falha(s)"
                            
                    messagebox.showwarning("Resultado Parcial", resultado)
                
                popup.destroy()
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro crítico ao aplicar kit:\n{str(e)}")

        # Botões
        tk.Button(button_frame, text="✅ Aplicar Kit", command=aplicar_kit, 
                bg="#228B22", fg="white", font=("Arial", 13, "bold"), 
                width=18, height=2).pack(side="left", padx=10)

        tk.Button(button_frame, text="❌ Cancelar", command=popup.destroy, 
                bg="#8B0000", fg="white", font=("Arial", 13, "bold"), 
                width=18, height=2).pack(side="left", padx=10)

    def refresh_kits(self):
        """Recarrega todos os kits do banco de dados"""
        try:
            D.refresh_kits()  # Chama a função do módulo D para recarregar
            
            # Atualizar a lista de kits na interface
            self.create_kit_list_section(self.current_frame if hasattr(self, 'current_frame') else self.kit_list_frame)
            
            # Atualizar o kit selecionado se existir
            if hasattr(self, 'kit_var'):
                kits_keys = list(D.KitsDisponíveis.keys()) if hasattr(D, 'KitsDisponíveis') and D.KitsDisponíveis else []
                if kits_keys:
                    if self.kit_var.get() not in kits_keys:
                        self.kit_var.set(kits_keys[0])
                else:
                    self.kit_var.set("Sem kits")
                    
            messagebox.showinfo("Sucesso", "Kits atualizados com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar kits: {str(e)}")

    def delete_kit(self, kit_name):
        """Apaga um kit específico"""
        from tkinter import messagebox
        
        result = messagebox.askyesno("Confirmar Exclusão", 
                                f"Tem certeza que deseja apagar o kit '{kit_name}'?\n\n⚠️ Esta ação não pode ser desfeita!")
        
        if result:
            try:
                # Remover o kit do dicionário
                if hasattr(D, 'KitsDisponíveis') and kit_name in D.KitsDisponíveis:
                    del D.KitsDisponíveis[kit_name]
                    
                    # Atualizar a interface
                    frame_to_update = self.current_frame if hasattr(self, 'current_frame') else (
                        self.kit_list_frame if hasattr(self, 'kit_list_frame') else None
                    )
                    
                    if frame_to_update:
                        self.create_kit_list_section(frame_to_update)
                    
                    messagebox.showinfo("Sucesso", f"Kit '{kit_name}' foi apagado com sucesso! 🗑️")
                else:
                    messagebox.showerror("Erro", f"Kit '{kit_name}' não encontrado!")
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao apagar o kit:\n{str(e)}")
### --- Kits --- ###

# --- Refresh --- #
    def refresh_all(self):
        """Atualiza todas as listas"""
        self.create_group_list_section(self.group_list_frame)
        self.create_list_section(self.char_list_frame)
        self.create_kit_management(self.kit_management_frame)
        self.create_kit_list_section(self.kit_list_frame)

    def refresh(self, *args):
        self.refresh_all()
# --- Refresh --- #

    def carregar_armas_e_armaduras(self, personagem):
        for entrada in personagem.inventario.itens:
            item = entrada["item"]
            if isinstance(item, CB.Ranged):
                capacidade_restante = item.capacidade - item.munições  # ou len(item.municoes) se for lista

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

        for item_dict in personagem.inventario.itens[:]:  # cópia para evitar problemas
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
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#130f26')

        self.title_label = tk.Label(self, font=("Arial", 24, "bold"), bg="#1a0869", fg="white")
        self.title_label.place(x=500, y=20, width=600, height=50)

        self.btn_tela_de_selecao = tk.Button(self, text="Seleção", bg="#1a0869", fg="white", font=("Arial", 18), command=self.controller.TelaDeSelecao)
        self.btn_tela_de_selecao.place(x=50, y=20, width=200, height=50)

        self.btn_tela_de_combate = tk.Button(self, text="Tela de Combate", bg="#1a0869", fg="white", font=("Arial", 18), command=self.controller.TelaDeCombate)
        self.btn_tela_de_combate.place(x=1350, y=20, width=200, height=50)

        ## Frame da Vida ##
        self.frame_vida = tk.Frame(self, bg='#1a0869', bd=2, relief='ridge')
        self.frame_vida.place(x=50, y=100, width=200, height=180)
        
        # Vida
        frame_vida_controls = tk.Frame(self.frame_vida, bg='#1a0869')
        frame_vida_controls.pack(pady=2)
        self.label_vida = tk.Label(frame_vida_controls, bg='#1a0869', fg="white", font=("Arial", 16))
        self.label_vida.pack()
        
        frame_vida_input = tk.Frame(self.frame_vida, bg='#1a0869')
        frame_vida_input.pack(pady=2)
        tk.Button(frame_vida_input, text="-", command=lambda: self.alterar_vida(-1), bg="#8c1d1d", fg="white", font=("Arial", 12), width=2).pack(side="left")
        self.entry_vida = tk.Entry(frame_vida_input, width=5, justify="center")
        self.entry_vida.pack(side="left", padx=5)
        tk.Button(frame_vida_input, text="+", command=lambda: self.alterar_vida(1), bg="#115c11", fg="white", font=("Arial", 12), width=2).pack(side="left")
        
        # Energia
        frame_energia_controls = tk.Frame(self.frame_vida, bg='#1a0869')
        frame_energia_controls.pack(pady=2)
        self.label_energia = tk.Label(frame_energia_controls, bg='#1a0869', fg="white", font=("Arial", 16))
        self.label_energia.pack()
        
        frame_energia_input = tk.Frame(self.frame_vida, bg='#1a0869')
        frame_energia_input.pack(pady=2)
        tk.Button(frame_energia_input, text="-", command=lambda: self.alterar_energia(-1), bg="#8c1d1d", fg="white", font=("Arial", 12), width=2).pack(side="left")
        self.entry_energia = tk.Entry(frame_energia_input, width=5, justify="center")
        self.entry_energia.pack(side="left", padx=5)
        tk.Button(frame_energia_input, text="+", command=lambda: self.alterar_energia(1), bg="#115c11", fg="white", font=("Arial", 12), width=2).pack(side="left")
        
        # Mobilidade (sem controles)
        self.label_mobilidade = tk.Label(self.frame_vida, bg='#1a0869', fg="white", font=("Arial", 16))
        self.label_mobilidade.pack(pady=2)
        ## Frame da Vida ##

        ## Frame do XP ##
        self.frame_XP = tk.Frame(self, bg='#1a0869', bd=2, relief='ridge')
        self.frame_XP.place(x=50, y=280, width=200, height=180)
        # XP
        frame_xp_controls = tk.Frame(self.frame_XP, bg='#1a0869')
        frame_xp_controls.pack(pady=2)
        self.label_xp = tk.Label(frame_xp_controls, bg='#1a0869', fg="white", font=("Arial", 16))
        self.label_xp.pack()
        frame_xp_input = tk.Frame(self.frame_XP, bg='#1a0869')
        frame_xp_input.pack(pady=2)
        tk.Button(frame_xp_input, text="-", command=lambda: self.alterar_xp(-1), bg="#8c1d1d", fg="white", font=("Arial", 12), width=2).pack(side="left")
        self.entry_xp = tk.Entry(frame_xp_input, width=5, justify="center")
        self.entry_xp.pack(side="left", padx=5)
        tk.Button(frame_xp_input, text="+", command=lambda: self.alterar_xp(1), bg="#115c11", fg="white", font=("Arial", 12), width=2).pack(side="left")
        
        # Nível
        frame_nivel_controls = tk.Frame(self.frame_XP, bg='#1a0869')
        frame_nivel_controls.pack(pady=2)
        self.label_nivel = tk.Label(frame_nivel_controls, bg='#1a0869', fg="white", font=("Arial", 16))
        self.label_nivel.pack()
        frame_nivel_input = tk.Frame(self.frame_XP, bg='#1a0869')
        frame_nivel_input.pack(pady=2)
        tk.Button(frame_nivel_input, text="-", command=lambda: self.alterar_nivel(-1), bg="#8c1d1d", fg="white", font=("Arial", 12), width=2).pack(side="left", padx=5)
        tk.Button(frame_nivel_input, text="+", command=lambda: self.alterar_nivel(1), bg="#115c11", fg="white", font=("Arial", 12), width=2).pack(side="left", padx=5)
        
        # Carga (sem controles)
        self.label_carga = tk.Label(self.frame_XP, bg='#1a0869', fg="white", font=("Arial", 16))
        self.label_carga.pack(pady=2)
        ## Frame do XP ##

        ## Frame dos Atributos ##
        self.frame_atributos = tk.Frame(self, bg='#1a0869', bd=2, relief='ridge')
        self.frame_atributos.place(x=250, y=100, width=250, height=360)
        self.label_atributos_title = tk.Label(self.frame_atributos, text="Atributos", bg='#1a0869', fg="white", font=("Arial", 18, "bold"))
        self.label_atributos_title.pack(pady=(0, 5))
        self.atributo_frames = {}
        ## Frame dos Atributos ##

        ## Frame da AC ##
        self.frame_AC = tk.Frame(self, bg='#1a0869', bd=2, relief='ridge')
        self.frame_AC.place(x=50, y=460, width=200, height=80)

        self.label_bloqueio= tk.Label(self.frame_AC, bg='#1a0869', fg="white", font=("Arial", 12))
        self.label_bloqueio.pack(pady=2)
        self.label_esquiva= tk.Label(self.frame_AC, bg='#1a0869', fg="white", font=("Arial", 12))
        self.label_esquiva.pack(pady=2)
        self.label_percepcao= tk.Label(self.frame_AC, bg='#1a0869', fg="white", font=("Arial", 12))
        self.label_percepcao.pack(pady=2)
        ## Frame da AC ##

        ## Frame proficiencias ##
        ## Frame proficiencias ##
        self.frame_proficiencias = tk.Frame(self, bg='#1a0869')
        self.frame_proficiencias.place(x=1150, y=100, width=400, height=750)

        self.label_proficiencias_title = tk.Label(self.frame_proficiencias, text="Proficiências", font=("Arial", 18, "bold"), bg="#1a0869", fg="white")
        self.label_proficiencias_title.pack(pady=(10, 5))

        self.container_scroll_prof = tk.Frame(self.frame_proficiencias, bg='#130f26')
        self.container_scroll_prof.pack()

        self.canvas_prof = tk.Canvas(self.container_scroll_prof, bg='#1a0869', highlightthickness=0, width=360, height=700)
        self.scrollbar_prof = tk.Scrollbar(self.container_scroll_prof, orient="vertical", command=self.canvas_prof.yview)

        self.scrollable_frame_prof = tk.Frame(self.canvas_prof, bg='#1a0869')
        self.scrollable_frame_prof.bind("<Configure>", lambda e: self.canvas_prof.configure(scrollregion=self.canvas_prof.bbox("all")))

        self.canvas_prof.create_window((5, 0), window=self.scrollable_frame_prof, anchor="nw")
        self.canvas_prof.configure(yscrollcommand=self.scrollbar_prof.set)

        self.canvas_prof.pack(side="left")
        self.scrollbar_prof.pack(side="right", fill="y")

        self.proficiencia_widgets = []
        ## Frame proficiencias ##
        ## Frame proficiencias ## 

        ## Frame do Inventário ##
        ## Frame do Inventário ##
        self.frame_inventario = tk.Frame(self, bg='#1a0869')
        self.frame_inventario.place(x=530, y=100, width=600, height=350)

        self.header_inventario = tk.Frame(self.frame_inventario, bg="#1a0869")
        self.header_inventario.pack(pady=(10, 5), fill="x", padx=10)

        self.label_inventario_title = tk.Label(self.header_inventario, text="Inventário", font=("Arial", 18, "bold"), bg="#1a0869", fg="white")
        self.label_inventario_title.pack(side="left")
        self.btn_adicionar_item = tk.Button(self.header_inventario, text="Adicionar Item", command=self.abrir_popup_adicionar_item, bg="#1a0869", fg="white", font=("Arial", 12))
        self.btn_adicionar_item.pack(side="right", padx=(10, 0))

        self.container_scroll_inventario = tk.Frame(self.frame_inventario, bg='#130f26', width=600, height=300)
        self.container_scroll_inventario.place(x=10, y=50)

        self.canvas_inventario = tk.Canvas(self.container_scroll_inventario, bg='#1a0869', highlightthickness=0, width=600, height=300)
        self.scrollbar_inventario = tk.Scrollbar(self.container_scroll_inventario, orient="vertical", command=self.canvas_inventario.yview)

        self.scrollable_frame_inventario = tk.Frame(self.canvas_inventario, bg='#1a0869')
        self.scrollable_frame_inventario.bind("<Configure>", lambda e: self.canvas_inventario.configure(scrollregion=self.canvas_inventario.bbox("all")))

        self.canvas_inventario.create_window((0, 0), window=self.scrollable_frame_inventario, anchor="nw")
        self.canvas_inventario.configure(yscrollcommand=self.scrollbar_inventario.set)

        self.canvas_inventario.place(x=0, y=0)
        self.scrollbar_inventario.place(x=570, y=0, height=300)

        self.frame_lista_itens = tk.Frame(self.scrollable_frame_inventario, bg='#1a0869', width=400)
        self.frame_lista_itens.pack()

        self.item_widgets = []
        ## Frame do Inventário ##
        ## Frame do Inventário ##

        ## Frame dos Equipados ##
        self.frame_equipados = tk.Frame(self, bg='#1a0869')
        self.frame_equipados.place(x=530, y=500, width=600, height=350)

        self.header_equipados = tk.Frame(self.frame_equipados, bg="#1a0869")
        self.header_equipados.pack(pady=(10, 5), fill="x", padx=10)
        self.label_equipados_title = tk.Label(self.header_equipados, text="Equipados", font=("Arial", 18, "bold"), bg="#1a0869", fg="white")
        self.label_equipados_title.pack(side="left")


        self.container_scroll_equipados = tk.Frame(self.frame_equipados, bg='#130f26', width=600, height=300)
        self.container_scroll_equipados.place(x=10, y=50)
        self.canvas_equipados = tk.Canvas(self.container_scroll_equipados, bg='#1a0869', highlightthickness=0, width=600, height=300)
        self.scrollbar_equipados = tk.Scrollbar(self.container_scroll_equipados, orient="vertical", command=self.canvas_equipados.yview)
        self.scrollable_frame_equipados = tk.Frame(self.canvas_equipados, bg='#1a0869')
        self.scrollable_frame_equipados.bind("<Configure>", lambda e: self.canvas_equipados.configure(scrollregion=self.canvas_equipados.bbox("all")))

        self.canvas_equipados.create_window((0, 0), window=self.scrollable_frame_equipados, anchor="nw")
        self.canvas_equipados.configure(yscrollcommand=self.scrollbar_equipados.set)
        self.canvas_equipados.place(x=0, y=0)
        self.scrollbar_equipados.place(x=570, y=0, height=300)

        self.frame_lista_equipados = tk.Frame(self.scrollable_frame_equipados, bg='#1a0869', width=400)
        self.frame_lista_equipados.pack()
        ## Frame dos Equipados ##

        ## Frame de Proteções ##
        ## Frame de Proteções ##
        self.frame_protecoes = tk.Frame(self, bg='#1a0869')
        self.frame_protecoes.place(x=50, y=550, width=430, height=300)
        self.label_protecoes_title = tk.Label(self.frame_protecoes, text="Proteções Equipadas",font=("Arial", 18, "bold"), bg="#1a0869", fg="white")
        self.label_protecoes_title.pack(pady=(10, 5))

        self.frame_lista_protecoes = tk.Frame(self.frame_protecoes, bg='#1a0869')
        self.frame_lista_protecoes.pack(fill="both", expand=True)

        self.protecao_widgets = []
        ## Frame de Proteções ##
        ## Frame de Proteções ##

        ## Botões entre Atributos e Proteções ##
        ## Botões entre Atributos e Proteções ##
        self.btn_status_completo = tk.Button(self, text="Rolar dados", command=lambda: self.abrir_popup_rolagem_avancada(), bg="#1a0869", fg="white", font=("Arial", 14))
        self.btn_status_completo.place(x=250, y=340, width=250, height=40)

        self.btn_efeitos = tk.Button(self, text="Efeitos", command=self.abrir_popup_efeitos, bg="#1a0869", fg="white", font=("Arial", 14))
        self.btn_efeitos.place(x=250, y=380, width=250, height=40)

        self.btn_habilidades = tk.Button(self, text="Habilidades", command=self.abrir_popup_habilidades, bg="#1a0869", fg="white", font=("Arial", 14))
        self.btn_habilidades.place(x=250, y=420, width=250, height=40)
        ## Botões entre Atributos e Proteções ##
        ## Botões entre Atributos e Proteções ##
    
    def refresh_info_basica(self):
        """Atualiza informações básicas do personagem"""
        try:
            self.character.calcular_peso_total()
            self.title_label.config(text=f"Detalhes de {self.character.nome}")
            self.label_vida.config(text=f"Vida: {self.character.vidaAtual}/{self.character.vidaMax}")
            self.label_xp.config(text=f"XP: {self.character.XPAtual}/{self.character.XPlvlUp}")
            self.label_nivel.config(text=f"Nível: {self.character.nivel}")
            self.label_carga.config(text=f"Carga: {self.character.cargaAtual:.2f}/{self.character.CargaMax:.2f}")
            self.label_energia.config(text=f"Energia: {self.character.PeAtual}/{self.character.PeMax}")
            self.label_mobilidade.config(text=f"Mobilidade: {self.character.mobilidade}m")
            self.label_bloqueio.config(text=f"Bloqueio: {self.character.bloqueio}")
            self.label_esquiva.config(text=f"Esquiva: {self.character.esquiva}")
            self.label_percepcao.config(text=f"Percepção: {self.character.percepcao}")
        except Exception as e:
            print("Erro no refresh das informações básicas:", e)

    def refresh_atributos(self):
        """Atualiza a seção de atributos"""
        try:
            # Limpa os frames antigos dos atributos
            for frame in self.atributo_frames.values():
                frame.destroy()
            self.atributo_frames.clear()

            atributos = {
                "Força": "Forca",
                "Agilidade": "Agilidade", 
                "Vigor": "Vigor",
                "Inteligência": "Inteligencia",
                "Presença": "Presenca",
                "Tática": "Tatica"
            }
            
            for nome_visivel, nome_real in atributos.items():
                frame = tk.Frame(self.frame_atributos, bg='#1a0869')
                frame.pack(pady=2)
                self.atributo_frames[nome_real] = frame
                
                valor = getattr(self.character, nome_real)
                tk.Label(frame, text=f"{nome_visivel}: {valor}", bg='#1a0869', fg="white", font=("Arial", 14)).pack(side="left")
                tk.Button(frame, text="-", command=lambda nr=nome_real: self.alterar_atributo(nr, -1), bg="#8c1d1d", fg="white", font=("Arial", 10), width=2).pack(side="right", padx=2)
                tk.Button(frame, text="+", command=lambda nr=nome_real: self.alterar_atributo(nr, 1), bg="#115c11", fg="white", font=("Arial", 10), width=2).pack(side="right")
        except Exception as e:
            print("Erro no refresh dos atributos:", e)

    def refresh_proficiencias(self):
        """Atualiza a seção de proficiências"""
        try:
            # Limpa os widgets antigos
            for widget in self.proficiencia_widgets:
                widget.destroy()
            self.proficiencia_widgets.clear()

            # Agrupa proficiências por atributo
            profs_por_atributo = {}
            for nome, prof in self.character.proficiencias.items():
                atributo = prof.atributo
                if atributo not in profs_por_atributo:
                    profs_por_atributo[atributo] = []
                profs_por_atributo[atributo].append(prof)

            # Ordem de exibição dos atributos
            ordem_atributos = ["Força", "Agilidade", "Vigor", "Inteligência", "Presença", "Tática"]

            # Exibe as proficiências organizadas por atributo
            for atributo in ordem_atributos:
                if atributo in profs_por_atributo:
                    # Título separador
                    titulo = tk.Label(self.scrollable_frame_prof, text=atributo, bg="#120447", fg="white", font=("Arial", 14, "bold"), anchor="w")
                    titulo.pack(fill="x", padx=4, pady=(8, 4))
                    self.proficiencia_widgets.append(titulo)

                    for prof in profs_por_atributo[atributo]:
                        frame = tk.Frame(self.scrollable_frame_prof, bg="#1a0869", pady=2)
                        frame.pack(fill='x', padx=2, pady=2)

                        label = tk.Label(frame, text=f"{prof.nome}: {prof.nivel}", bg="#2a0d89", fg="white", font=("Arial", 13), width=27, height=1, anchor='w')
                        label.pack(side="left", padx=2)

                        btn_menos = tk.Button(frame, text="-", font=("Arial", 8), bg="#2a0d89", fg="white", width=4, height=1, command=lambda p=prof: self.decrementar_proficiencia(p))
                        btn_menos.pack(side="left", padx=5)

                        btn_mais = tk.Button(frame, text="+", font=("Arial", 8), bg="#2a0d89", fg="white", width=4, height=1, command=lambda p=prof: self.incrementar_proficiencia(p))
                        btn_mais.pack(side="left", padx=5)

                        self.proficiencia_widgets.append(frame)
        except Exception as e:
            print("Erro no refresh das proficiências:", e)

    def refresh_inventario(self):
        """Atualiza a seção de inventário"""
        try:
            for widget in self.scrollable_frame_inventario.winfo_children():
                widget.destroy()

            for i in self.character.inventario.listar_itens():
                item_obj = i["objeto"]
                item_nome = i["nome"]
                quantidade = i["quantidade"]
                item_id = i["id"]

                frame_item = tk.Frame(self.scrollable_frame_inventario, bg="#1a0869", pady=2)
                frame_item.pack(fill='x', padx=5, pady=2)

                if item_id:
                    texto_item = item_nome
                else:
                    texto_item = f"{item_nome} x {quantidade}"

                btn_item = tk.Button(frame_item, text=texto_item, bg="#2a0d89", fg="white",
                    font=("Arial", 13), anchor='w', relief=tk.FLAT,borderwidth=0, highlightthickness=0, width=35,
                    command=lambda i=item_obj: self.mostrar_popup_detalhes_item(i))
                btn_item.pack(side="left", fill='x', expand=True)

                if item_id:
                    btn_melhorias = tk.Button(frame_item, text="Upgrades", command=lambda i=item_obj: self.abrir_popup_melhorias_item(i), bg="#8B4513", fg="white", font=("Arial", 8), width=8)
                    btn_melhorias.pack(side="right", padx=4)
                    
                    if isinstance(item_obj, (CB.Melee)):
                        btn_equipar = tk.Button(frame_item, text="Equip", command=lambda i=item_obj: self._equipar_item(i), bg="#2a0d89", fg="white", font=("Arial", 8), width=6)
                        btn_equipar.pack(side="right", padx=4)
                        btn_remover = tk.Button(frame_item,text="Discard",command=lambda i=item_obj: self._remover_item_do_inventario(i),bg="#2a0d89",fg="white",font=("Arial", 8))     
                        btn_remover.pack(side="right", padx=4)
                        self.item_widgets.append(btn_equipar)
                    elif isinstance(item_obj, (CB.Ranged)):
                        btn_equipar = tk.Button(frame_item, text="Equip", command=lambda i=item_obj: self._equipar_item(i), bg="#2a0d89", fg="white", font=("Arial", 8), width=6)
                        btn_equipar.pack(side="right", padx=4)
                        btn_unload = tk.Button(frame_item, text="Unload", command=lambda i=item_obj: self.descarregar_municao_ranged(i), bg="#2a0d89", fg="white", font=("Arial", 8), width=6)
                        btn_unload.pack(side="right", padx=4)
                        btn_remover = tk.Button(frame_item,text="Discard",command=lambda i=item_obj: self._remover_item_do_inventario(i),bg="#2a0d89",fg="white",font=("Arial", 8))     
                        btn_remover.pack(side="right", padx=4)
                        self.item_widgets.extend([btn_equipar, btn_unload])
                    elif isinstance(item_obj, (CB.Protecao)):
                        print(f"Item {item_nome} é uma Protecao!")
                        regiao = getattr(item_obj, "regiao", None)
                        if regiao:
                            btn_equipar = tk.Button(frame_item, text="Equip", command=lambda i=item_obj: self._equipar_protecao(i), bg="#2a0d89", fg="white", font=("Arial", 8), width=6)
                            btn_equipar.pack(side="right", padx=4)
                            btn_remover = tk.Button(frame_item,text="Discard",command=lambda i=item_obj: self._remover_item_do_inventario(i),bg="#2a0d89",fg="white",font=("Arial", 8))     
                            btn_remover.pack(side="right", padx=4)
                            self.item_widgets.append(btn_equipar)
                    else:
                        btn_remover = tk.Button(
                            frame_item, text="Discard",
                            command=lambda i=item_obj: self._remover_item_do_inventario(i),
                            bg="#2a0d89", fg="white", font=("Arial", 8)
                        )
                        btn_remover.pack(side="right", padx=5)
                        self.item_widgets.append(btn_remover)
                    
                    # Adicionar o botão de melhorias aos widgets
                    self.item_widgets.append(btn_melhorias)
                else:
                    btn_remover_1 = tk.Button(
                        frame_item, text="-1",
                        command=lambda i=item_obj: self._remover_item_do_inventario(i, 1),
                        bg="#2a0d89", fg="white", font=("Arial", 8), width=3
                    )
                    btn_remover_5 = tk.Button(
                        frame_item, text="-5",
                        command=lambda i=item_obj: self._remover_item_do_inventario(i, 5),
                        bg="#2a0d89", fg="white", font=("Arial", 8), width=3
                    )
                    btn_remover_10 = tk.Button(
                        frame_item, text="-10",
                        command=lambda i=item_obj: self._remover_item_do_inventario(i, 10),
                        bg="#2a0d89", fg="white", font=("Arial", 8), width=3
                    )
                    btn_remover_1.pack(side="right", padx=(2, 0))
                    btn_remover_5.pack(side="right", padx=(5, 0))
                    btn_remover_10.pack(side="right", padx=(7, 0))
                    self.item_widgets.extend([btn_remover_1, btn_remover_10])
        except Exception as e:
            print("Erro ao carregar inventário:", e)

    def refresh_equipados(self):
        """Atualiza a seção de itens equipados"""
        try:
            for widget in self.scrollable_frame_equipados.winfo_children():
                widget.destroy()

            for i in self.character.equipados.listar_itens():
                item_obj = i["objeto"]
                item_nome = i["nome"]
                quantidade = i["quantidade"]
                item_id = i["id"]

                if not item_id:
                    continue
                frame_item = tk.Frame(self.scrollable_frame_equipados, bg="#1a0869", pady=2)
                frame_item.pack(fill='x', padx=5, pady=2)

                texto_item = item_nome

                btn_item = tk.Button(
                    frame_item, text=texto_item, bg="#2a0d89", fg="white", font=("Arial", 14), anchor='w', relief=tk.FLAT,
                    borderwidth=0, highlightthickness=0, width=35, command=lambda i=item_obj: self.mostrar_popup_detalhes_item(i))
                btn_item.pack(side="left", fill='x', expand=True)

                btn_desequipar = tk.Button(frame_item, text="Unequip", command=lambda i=item_obj: self._desequipar_item(i), bg="#2a0d89", fg="white", font=("Arial", 8), width=6)
                btn_desequipar.pack(side="right", padx=5)
                self.item_widgets.append(btn_desequipar)

                if isinstance(item_obj, CB.Ranged):
                    btn_recarregar = tk.Button(frame_item, text="Reload", command=lambda i=item_obj: self.carregar_municao_ranged(i), bg="#2a0d89", fg="white", font=("Arial", 8), width=6)
                    btn_recarregar.pack(side="right", padx=5)
                    btn_disparar = tk.Button(frame_item, text="Shoot", command=lambda i=item_obj: self.disparar_ranged(i), bg="#2a0d89", fg="white", font=("Arial", 8), width=6)
                    btn_disparar.pack(side="right", padx=5)
                    self.item_widgets.append(btn_recarregar)

                self.item_widgets.append(btn_item)
        except Exception as e:
            print("Erro ao carregar itens equipados:", e)

    def refresh_protecoes(self):
        """Atualiza a seção de proteções"""
        try:
            for widget in self.protecao_widgets:
                widget.destroy()
            self.protecao_widgets.clear()

            # Regiões fixas com suas proteções
            regioes = {
                "Cabeça": self.character.Cabeça,
                "Rosto": self.character.Rosto,
                "Torso": self.character.Torso,
                "Braços": self.character.Braços,
                "Pernas": self.character.Pernas
            }

            for regiao, protecao in regioes.items():
                frame_linha = tk.Frame(self.frame_lista_protecoes, bg='#1a0869')
                frame_linha.pack(fill='x', pady=5)
                self.protecao_widgets.append(frame_linha)

                # Obtém o nome da proteção de forma segura
                nome_protecao = self.obter_nome_protecao(protecao)
                label_texto = f"{regiao}: {nome_protecao}"
                label = tk.Label(frame_linha, text=label_texto, font=("Arial", 14), bg='#2a0d89', fg='white', width=25, anchor='w')
                label.pack(side='left', padx=10)

                btn_remover = tk.Button(
                    frame_linha, text="Remover",
                    command=lambda r=regiao: self.remover_protecao(r),
                    bg="#1a0869", fg="white", font=("Arial", 12)
                )
                btn_remover.pack(side='right', padx=5)
        except Exception as e:
            print("Erro no refresh das proteções:", e)

    def refresh(self, character=None):
        """Função principal que chama todos os refreshes"""
        if character is not None:
            self.character = character
        
        # Chama todos os refreshes das seções
        self.refresh_info_basica()
        self.refresh_atributos()
        self.refresh_proficiencias()
        self.refresh_inventario()
        self.refresh_equipados()
        self.refresh_protecoes()

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

    def abrir_popup_adicionar_item(self):
        popup = tk.Toplevel()
        popup.title("Adicionar Item")
        popup.configure(bg="#1a0869")
        popup.geometry("370x500")

        # Carrega os dados das tabelas usando as novas funções
        dados_tabelas = {
            "Armas de Fogo": D.carregar_rangeds(),
            "Armas Corpo a Corpo": D.carregar_melees(),
            "Proteções": D.carregar_protecoes(),
            "Melhorias": D.carregar_melhorias(),
            "Munições": D.carregar_municoes(),
            "Consumíveis": D.carregar_consumiveis(),
            "Explosivos": D.carregar_explosivos(),
            "Itens": D.carregar_itens()
        }

        tk.Label(popup, text="Categoria:", bg="#1a0869", fg="white", font=("Arial", 16)).pack(pady=5)
        categoria_var = tk.StringVar()
        categoria_menu = ttk.Combobox(popup, textvariable=categoria_var, values=list(dados_tabelas.keys()))
        categoria_menu.pack(pady=(0, 10))

        # Área de scroll
        frame_scroll = tk.Frame(popup, bg="#1a0869")
        frame_scroll.pack(expand=True, fill="both", padx=10, pady=10)

        canvas = tk.Canvas(frame_scroll, bg="#1a0869", highlightthickness=0, width=300, height=300)
        scrollbar = tk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a0869")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Botão Voltar
        btn_voltar = tk.Button(popup, text="Voltar", command=popup.destroy, 
                            bg="#a00c0c", fg="white", font=("Arial", 12))
        btn_voltar.pack(pady=10, side="bottom")

        quantidade_widgets = {}

        def exibir_itens(*args):
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
            quantidade_widgets.clear()

            categoria = categoria_var.get()
            if not categoria or categoria not in dados_tabelas:
                return

            # Agora iteramos sobre o dicionário de itens da categoria
            itens_categoria = dados_tabelas[categoria]
            
            for nome_item, item_data in itens_categoria.items():
                frame_item = tk.Frame(scrollable_frame, bg="#1a0869")
                frame_item.pack(fill="x", pady=2)

                # Campo de quantidade para itens stackáveis
                # Verifica se o item não tem "id" (indicando que é stackável)
                if "id" not in item_data:
                    qtd_var = tk.StringVar(value="1")
                    qtd_entry = tk.Entry(frame_item, textvariable=qtd_var, 
                                    width=5, font=("Arial", 12))
                    qtd_entry.pack(side="right", padx=5)
                    quantidade_widgets[nome_item] = qtd_var

                btn_item = tk.Button(frame_item, text=nome_item,
                                bg="#0e3386", fg="white", width=28, font=("Arial", 12),
                                command=lambda n=nome_item: adicionar_item(categoria, n))
                btn_item.pack(side="left", padx=5)

        def adicionar_item(categoria, nome_item):
            try:
                # Pega os dados do item diretamente da categoria carregada
                item_data = dados_tabelas[categoria][nome_item]
                
                # Cria o objeto do item baseado na categoria
                item_obj = criar_item_por_categoria(categoria, item_data)
                
                if item_obj is None:
                    tk.messagebox.showerror("Erro", f"Erro ao criar item '{nome_item}'.")
                    return
                
                quantidade = 1

                # Verifica se é um item stackável (sem ID único)
                if not hasattr(item_obj, "Id"):
                    if nome_item in quantidade_widgets:
                        qtd_str = quantidade_widgets[nome_item].get()
                        try:
                            quantidade = int(qtd_str)
                            if quantidade <= 0:
                                raise ValueError("Quantidade deve ser maior que zero")
                        except ValueError:
                            tk.messagebox.showerror("Erro", "Quantidade inválida.")
                            return

                # Adiciona o item ao inventário
                self.character.inventario.gerenciar_item(item_objeto=item_obj, 
                                                    quantidade=quantidade, 
                                                    operacao="adicionar")
                self.refresh()
                
            except Exception as e:
                tk.messagebox.showerror("Erro", f"Erro ao adicionar item: {str(e)}")

        def criar_item_por_categoria(categoria, item_data):
            """Cria um objeto de item baseado na categoria e dados"""
            try:
                if categoria == "Armas de Fogo":
                    from Codigos import Ranged
                    return Ranged(
                        nome=item_data.get("nome", "Arma de Fogo"),
                        peso=item_data.get("peso", 2.0),
                        classe=item_data.get("classe", "Pistola"),
                        acao=item_data.get("acao", "Semi"),
                        raridade=item_data.get("raridade", "Comum"),
                        calibre=item_data.get("calibre", ".22"),
                        capacidade=item_data.get("capacidade", 10)
                    )
                    
                elif categoria == "Armas Corpo a Corpo":
                    from Codigos import Melee
                    return Melee(
                        nome=item_data.get("nome", "Arma Branca"),
                        peso=item_data.get("peso", 1.0),
                        classe=item_data.get("classe", "Faca"),
                        tipo_dano=item_data.get("tipo_dano", "Cortante"),
                        raridade=item_data.get("raridade", "Comum")
                    )
                    
                elif categoria == "Proteções":
                    from Codigos import Protecao
                    return Protecao(
                        nome=item_data.get("nome", "Proteção"),
                        peso=item_data.get("peso", 1.0),
                        nivelBalistico=item_data.get("nivelBalistico", 1),
                        absorcaoFisica=item_data.get("absorcaoFisica", 1),
                        absorcaoBalistica=item_data.get("absorcaoBalistica", 1),
                        regiao=item_data.get("regiao", "Torso")
                    )
                    
                elif categoria == "Melhorias":
                    from Codigos import Melhoria
                    return Melhoria(
                        nome=item_data.get("nome", "Melhoria"),
                        peso=item_data.get("peso", 0.1),
                        tipo=item_data.get("tipo", "ranged"),
                        modificadores=item_data.get("modificadores", {})
                    )
                    
                elif categoria == "Munições":
                    from Codigos import Municao
                    return Municao(
                        nome=item_data.get("nome", "Munição"),
                        calibre=item_data.get("calibre", ".22"),
                        perfuracao=item_data.get("perfuracao", 1),
                        dano=item_data.get("dano", 5)
                    )
                    
                elif categoria == "Consumíveis":
                    from Codigos import Consumivel
                    return Consumivel(
                        nome=item_data.get("nome", "Consumível"),
                        peso=item_data.get("peso", 1.0),
                        cura=item_data.get("cura", 0),
                        energia=item_data.get("energia", 0)
                    )
                    
                elif categoria == "Explosivos":
                    from Codigos import Explosivo
                    return Explosivo(
                        nome=item_data.get("nome", "Explosivo"),
                        peso=item_data.get("peso", 1.0),
                        raio=item_data.get("raio", 1),
                        dano=item_data.get("dano", 10),
                        tipo_dano=item_data.get("tipo_dano", 1)
                    )
                    
                elif categoria == "Itens":
                    from Codigos import Item
                    return Item(
                        nome=item_data.get("nome", "Item"),
                        peso=item_data.get("peso", 1.0)
                    )
                    
                else:
                    return None
                    
            except Exception as e:
                print(f"❌ Erro ao criar item da categoria {categoria}: {e}")
                return None

        categoria_var.trace_add("write", exibir_itens)

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
            popup.geometry("600x400")  # Diminuído a largura
            popup.resizable(False, False)

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

    def _equipar_item(self, item):
        try:
            sucesso = self.character.equipar_item(item)
            if sucesso:
                self.refresh()
            else:
                print("Item não pôde ser equipado.")
        except Exception as e:
            print("Erro ao equipar item:", e)
    
    def _desequipar_item(self, item):
        try:
            sucesso = self.character.desequipar_item(item)
            if sucesso:
                self.refresh()
            else:
                print("Item não pôde ser equipado.")
        except Exception as e:
            print("Erro ao equipar item:", e)
    
    def _equipar_protecao(self, item):
        self.character.equipar_do_inventario(item.regiao, item.nome)
        self.refresh()
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
    def abrir_popup_rolagem_avancada(self):
        popup = tk.Toplevel(self)
        popup.title("Rolagem Avançada")
        popup.configure(bg="#1a1a2e")
        popup.geometry("560x400")

        tk.Label(popup, text="Escolha o tipo de rolagem:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(pady=5)

        tipo_rolagem = tk.StringVar(value="normal")

        frame_tipos = tk.Frame(popup, bg="#1a1a2e")
        frame_tipos.pack()

        tk.Radiobutton(frame_tipos, text="Fórmula normal", variable=tipo_rolagem, value="normal", bg="#1a1a2e", fg="white").grid(row=0, column=0)
        tk.Radiobutton(frame_tipos, text="Atributo + Proficiência", variable=tipo_rolagem, value="atributo", bg="#1a1a2e", fg="white").grid(row=0, column=1)

        # Fórmula direta
        frame_normal = tk.Frame(popup, bg="#1a1a2e")
        tk.Label(frame_normal, text="Digite a fórmula (ex: 2D6 + 1D10):", bg="#1a1a2e", fg="white").pack()
        formula_var = tk.StringVar()
        tk.Entry(frame_normal, textvariable=formula_var, width=30).pack(pady=5)

        # Atributo + proficiência
        frame_atributo = tk.Frame(popup, bg="#1a1a2e")
        

        tk.Label(frame_atributo, text="Escolha o atributo:", bg="#1a1a2e", fg="white").pack()
        atributos = {
            "Força": self.character.Forca,
            "Agilidade": self.character.Agilidade,
            "Vigor": self.character.Vigor,
            "Inteligência": self.character.Inteligencia,
            "Presença": self.character.Presenca,
            "Tática": self.character.Tatica
            }
        atributo_nomes = list(atributos.keys())
        atributo_var = tk.StringVar(value=atributo_nomes[0])
        ttk.Combobox(frame_atributo, values=atributo_nomes, textvariable=atributo_var, state="readonly").pack(pady=5)

        tk.Label(frame_atributo, text="Escolha a proficiência:", bg="#1a1a2e", fg="white").pack()
        profs = [nome for nome, prof in self.character.proficiencias.items()]
        if profs:
            prof_var = tk.StringVar(value=profs[0])
        else:
            prof_var = tk.StringVar(value="Nenhuma Proficiência")
        ttk.Combobox(frame_atributo, values=profs, textvariable=prof_var).pack(pady=5)

        tk.Label(frame_atributo, text="Modificador extra (buff/debuff):", bg="#1a1a2e", fg="white").pack()
        mod_extra_var = tk.IntVar(value=0)
        tk.Entry(frame_atributo, textvariable=mod_extra_var).pack(pady=5)

        resultado_label = tk.Label(popup, text="", bg="#1a1a2e", fg="white", font=("Arial", 12, "bold"))
        resultado_label.pack(pady=10)

        def atualizar_frames():
            if tipo_rolagem.get() == "normal":
                frame_normal.pack(pady=10)
                frame_atributo.pack_forget()
            else:
                frame_normal.pack_forget()
                frame_atributo.pack(pady=10)

        tipo_rolagem.trace_add("write", lambda *args: atualizar_frames())
        atualizar_frames()

        def rolar_dados():
            if tipo_rolagem.get() == "normal":
                # Rolar com base na fórmula digitada
                formula = formula_var.get()
                try:
                    resultado_total, detalhes = rolar_formula(formula)
                    resultado_label.config(text=f"Rolagem: {resultado_total} ({detalhes})")
                except Exception as e:
                    resultado_label.config(text=f"Erro na fórmula: {e}")
            else:
                # Rolar por atributo + proficiência
                atributo_escolhido = atributo_var.get()
                prof_escolhida = prof_var.get()
                mod_extra = mod_extra_var.get()

                atributos = {
                    "Força": self.character.Forca,
                    "Agilidade": self.character.Agilidade,
                    "Vigor": self.character.Vigor,
                    "Inteligência": self.character.Inteligencia,
                    "Presença": self.character.Presenca,
                    "Tática": self.character.Tatica
                }

                valor_atributo = atributos.get(atributo_escolhido, 0)
                valor_proficiencia = self.character.proficiencias.obter_bonus(prof_escolhida)

                rolagens = [random.randint(1, 20) for _ in range(valor_atributo)]
                melhor_rolagem = max(rolagens) if rolagens else 0

                total = melhor_rolagem + valor_proficiencia + mod_extra

                resultado_label.config(
                    text=(
                        f"Rolagem: {total} "
                        f"(D20s: {rolagens}, Melhor: {melhor_rolagem}, "
                        f"Proficiência: {valor_proficiencia}, Mod: {mod_extra})"
                    )
                )
        def rolar_formula(formula: str):
            padrao = r"(\d*)[dD](\d+)"
            termos = re.findall(padrao, formula)
            soma_total = 0
            detalhes = []

            for quantidade, faces in termos:
                qtd = int(quantidade) if quantidade else 1
                dado = int(faces)
                rolagens = [random.randint(1, dado) for _ in range(qtd)]
                soma = sum(rolagens)
                detalhes.append(f"{qtd}d{dado}: {rolagens} = {soma}")
                soma_total += soma

            return soma_total, " | ".join(detalhes)

            

        rolar_btn = tk.Button(popup, text="Rolar", command=rolar_dados, bg="#4e54c8", fg="white", font=("Arial", 12, "bold"))
        rolar_btn.pack(pady=10)
    
    def abrir_popup_efeitos(self):
        """Abre popup para visualizar e gerenciar buffs/debuffs do personagem"""
        if not hasattr(self, 'character') or not self.character:
            messagebox.showwarning("Aviso", "Nenhum personagem selecionado!")
            return
        
        popup = tk.Toplevel(self)
        popup.title("Buffs e Debuffs")
        popup.geometry("700x600")
        popup.configure(bg='#130f26')
        popup.resizable(False, False)
        
        # Título
        title_label = tk.Label(popup, text="Buffs e Debuffs", font=("Arial", 18, "bold"), bg="#1a0869", fg="white")
        title_label.pack(pady=10, fill="x")
        
        # Frame para adicionar novo efeito
        frame_adicionar = tk.Frame(popup, bg='#1a0869', bd=2, relief='ridge')
        frame_adicionar.pack(pady=10, padx=20, fill="x")
        
        tk.Label(frame_adicionar, text="Adicionar Efeito:", font=("Arial", 12, "bold"), bg='#1a0869', fg="white").pack(anchor="w", padx=5, pady=5)
        
        # Linha 1: Nome e Tipo
        linha1 = tk.Frame(frame_adicionar, bg='#1a0869')
        linha1.pack(fill="x", padx=5, pady=2)
        
        tk.Label(linha1, text="Nome:", bg='#1a0869', fg="white").pack(side="left")
        entry_nome = tk.Entry(linha1, width=25)
        entry_nome.pack(side="left", padx=5)
        
        tk.Label(linha1, text="Tipo:", bg='#1a0869', fg="white").pack(side="left", padx=(20, 0))
        var_tipo = tk.StringVar(value="buff")
        tk.Radiobutton(linha1, text="Buff", variable=var_tipo, value="buff", bg='#1a0869', fg="white", selectcolor='#1a0869').pack(side="left", padx=5)
        tk.Radiobutton(linha1, text="Debuff", variable=var_tipo, value="debuff", bg='#1a0869', fg="white", selectcolor='#1a0869').pack(side="left")
        
        # Linha 2: Duração
        linha2 = tk.Frame(frame_adicionar, bg='#1a0869')
        linha2.pack(fill="x", padx=5, pady=2)
        
        tk.Label(linha2, text="Duração:", bg='#1a0869', fg="white").pack(side="left")
        entry_duracao = tk.Entry(linha2, width=15)
        entry_duracao.pack(side="left", padx=5)
        entry_duracao.insert(0, "1 turno")
        
        var_permanente = tk.BooleanVar(value=False)
        
        def toggle_duracao():
            if var_permanente.get():
                entry_duracao.delete(0, tk.END)
                entry_duracao.insert(0, "permanente")
                entry_duracao.config(state='disabled')
            else:
                entry_duracao.config(state='normal')
                entry_duracao.delete(0, tk.END)
                entry_duracao.insert(0, "1 turno")
        
        tk.Checkbutton(linha2, text="Permanente", variable=var_permanente, bg='#1a0869', fg="white", selectcolor='#1a0869', 
                    command=toggle_duracao).pack(side="left", padx=10)
        
        # Linha 3: Efeito Mecânico
        linha3 = tk.Frame(frame_adicionar, bg='#1a0869')
        linha3.pack(fill="x", padx=5, pady=2)
        
        tk.Label(linha3, text="Efeito:", bg='#1a0869', fg="white").pack(anchor="w")
        entry_efeito = tk.Entry(linha3, width=70)
        entry_efeito.pack(fill="x", pady=2)
        
        # Linha 4: Descrição
        linha4 = tk.Frame(frame_adicionar, bg='#1a0869')
        linha4.pack(fill="x", padx=5, pady=2)
        
        tk.Label(linha4, text="Descrição:", bg='#1a0869', fg="white").pack(anchor="w")
        entry_descricao = tk.Entry(linha4, width=70)
        entry_descricao.pack(fill="x", pady=2)
        
        # Botão adicionar
        def adicionar_efeito():
            nome = entry_nome.get().strip()
            efeito = entry_efeito.get().strip()
            descricao = entry_descricao.get().strip()
            duracao = entry_duracao.get().strip()
            tipo = var_tipo.get()
            
            if not nome or not efeito or not descricao:
                messagebox.showwarning("Aviso", "Nome, efeito e descrição são obrigatórios!")
                return
            
            if not duracao:
                duracao = "1 turno"
            
            self.character.buffs_debuffs.adicionar_efeito(nome, duracao, efeito, descricao, tipo)
            
            # Limpa campos
            entry_nome.delete(0, tk.END)
            entry_efeito.delete(0, tk.END)
            entry_descricao.delete(0, tk.END)
            entry_duracao.delete(0, tk.END)
            entry_duracao.insert(0, "1 turno")
            var_permanente.set(False)
            entry_duracao.config(state='normal')
            
            atualizar_lista()
            self.refresh_info_basica()
        
        tk.Button(frame_adicionar, text="Adicionar", command=adicionar_efeito, bg="#115c11", fg="white", font=("Arial", 10)).pack(pady=5)
        
        # Frame para abas
        frame_abas = tk.Frame(popup, bg='#130f26')
        frame_abas.pack(pady=5)
        
        var_aba = tk.StringVar(value="todos")
        
        tk.Radiobutton(frame_abas, text="Todos", variable=var_aba, value="todos", bg='#130f26', fg="white", selectcolor='#1a0869', command=lambda: atualizar_lista()).pack(side="left", padx=10)
        tk.Radiobutton(frame_abas, text="Buffs", variable=var_aba, value="buffs", bg='#130f26', fg="white", selectcolor='#1a0869', command=lambda: atualizar_lista()).pack(side="left", padx=10)
        tk.Radiobutton(frame_abas, text="Debuffs", variable=var_aba, value="debuffs", bg='#130f26', fg="white", selectcolor='#1a0869', command=lambda: atualizar_lista()).pack(side="left", padx=10)
        tk.Radiobutton(frame_abas, text="Permanentes", variable=var_aba, value="permanentes", bg='#130f26', fg="white", selectcolor='#1a0869', command=lambda: atualizar_lista()).pack(side="left", padx=10)
        tk.Radiobutton(frame_abas, text="Temporários", variable=var_aba, value="temporarios", bg='#130f26', fg="white", selectcolor='#1a0869', command=lambda: atualizar_lista()).pack(side="left", padx=10)
        
        # Frame para lista de efeitos
        frame_lista = tk.Frame(popup, bg='#130f26')
        frame_lista.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Canvas com scrollbar
        canvas = tk.Canvas(frame_lista, bg='#1a0869', highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_lista, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1a0869')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def atualizar_lista():
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
            
            # Obtém efeitos baseado na aba
            aba_atual = var_aba.get()
            if aba_atual == "buffs":
                efeitos = self.character.buffs_debuffs.listar_buffs()
            elif aba_atual == "debuffs":
                efeitos = self.character.buffs_debuffs.listar_debuffs()
            elif aba_atual == "permanentes":
                efeitos = self.character.buffs_debuffs.listar_permanentes()
            elif aba_atual == "temporarios":
                efeitos = self.character.buffs_debuffs.listar_temporarios()
            else:
                efeitos = self.character.buffs_debuffs.listar_efeitos()
            
            if not efeitos:
                tk.Label(scrollable_frame, text="Nenhum efeito", bg='#1a0869', fg="gray", font=("Arial", 12)).pack(pady=20)
                return
            
            for efeito in efeitos:
                frame_efeito = tk.Frame(scrollable_frame, bg='#2a1f4f', bd=1, relief='solid')
                frame_efeito.pack(fill="x", padx=5, pady=2)
                
                cor_tipo = "#115c11" if efeito.tipo == "buff" else "#8c1d1d"
                simbolo = "✨" if efeito.tipo == "buff" else "💀"
                
                # Header
                header = tk.Frame(frame_efeito, bg=cor_tipo)
                header.pack(fill="x")
                
                tk.Label(header, text=f"{simbolo} {efeito.nome}", font=("Arial", 12, "bold"), bg=cor_tipo, fg="white").pack(side="left", padx=5, pady=2)
                
                # Exibe duração como texto descritivo
                duracao_text = str(efeito.duracao)
                tk.Label(header, text=duracao_text, font=("Arial", 10), bg=cor_tipo, fg="white").pack(side="right", padx=5, pady=2)
                
                # Descrição
                tk.Label(frame_efeito, text=f"Descrição: {efeito.descricao}", font=("Arial", 10), bg='#2a1f4f', fg="white", wraplength=600, justify="left").pack(anchor="w", padx=5, pady=2)
                
                # Efeito mecânico
                tk.Label(frame_efeito, text=f"Efeito: {efeito.efeito}", font=("Arial", 10, "bold"), bg='#2a1f4f', fg="#90caf9", wraplength=600, justify="left").pack(anchor="w", padx=5, pady=2)
                
                # Botão remover
                tk.Button(frame_efeito, text="Remover", command=lambda n=efeito.nome: remover_efeito(n), bg="#8c1d1d", fg="white", font=("Arial", 9)).pack(anchor="e", padx=5, pady=2)
        
        def remover_efeito(nome):
            self.character.buffs_debuffs.remover_efeito(nome)
            atualizar_lista()
            self.refresh_info_basica()
        
        # Botões inferiores
        frame_botoes = tk.Frame(popup, bg='#130f26')
        frame_botoes.pack(pady=10)
        
        def limpar_temporarios():
            self.character.buffs_debuffs.limpar_temporarios()
            atualizar_lista()
            self.refresh_info_basica()
        
        def limpar_todos():
            self.character.buffs_debuffs.limpar_efeitos()
            atualizar_lista()
            self.refresh_info_basica()
        
        tk.Button(frame_botoes, text="Limpar Temporários", command=limpar_temporarios, bg="#d97706", fg="white", font=("Arial", 11)).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Limpar Todos", command=limpar_todos, bg="#8c1d1d", fg="white", font=("Arial", 11)).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Fechar", command=popup.destroy, bg="#1a0869", fg="white", font=("Arial", 11)).pack(side="left", padx=5)
        
        atualizar_lista()
        popup.transient(self)
        popup.grab_set()

    def abrir_popup_habilidades(self):
        """Abre popup para visualizar e gerenciar habilidades e poderes do personagem"""
        if not hasattr(self, 'character') or not self.character:
            messagebox.showwarning("Aviso", "Nenhum personagem selecionado!")
            return
        
        popup = tk.Toplevel(self)
        popup.title("Habilidades e Poderes")
        popup.geometry("750x650")
        popup.configure(bg='#130f26')
        popup.resizable(False, False)
        
        # Título
        title_label = tk.Label(popup, text="Habilidades e Poderes", font=("Arial", 18, "bold"), bg="#1a0869", fg="white")
        title_label.pack(pady=10, fill="x")
        
        # Frame para selecionar categoria (Habilidade ou Poder)
        frame_categoria = tk.Frame(popup, bg='#130f26')
        frame_categoria.pack(pady=5)
        
        var_categoria = tk.StringVar(value="habilidade")
        tk.Radiobutton(frame_categoria, text="Habilidade ⚔️", variable=var_categoria, value="habilidade", bg='#130f26', fg="white", selectcolor='#1a0869', font=("Arial", 12), command=lambda: atualizar_lista()).pack(side="left", padx=15)
        tk.Radiobutton(frame_categoria, text="Poder 🔮", variable=var_categoria, value="poder", bg='#130f26', fg="white", selectcolor='#1a0869', font=("Arial", 12), command=lambda: atualizar_lista()).pack(side="left", padx=15)
        
        # Frame para adicionar
        frame_adicionar = tk.Frame(popup, bg='#1a0869', bd=2, relief='ridge')
        frame_adicionar.pack(pady=10, padx=20, fill="x")
        
        tk.Label(frame_adicionar, text="Adicionar:", font=("Arial", 12, "bold"), bg='#1a0869', fg="white").pack(anchor="w", padx=5, pady=5)
        
        # Linha 1: Nome, Tipo e Custo
        linha1 = tk.Frame(frame_adicionar, bg='#1a0869')
        linha1.pack(fill="x", padx=5, pady=2)
        
        tk.Label(linha1, text="Nome:", bg='#1a0869', fg="white").pack(side="left")
        entry_nome = tk.Entry(linha1, width=25)
        entry_nome.pack(side="left", padx=5)
        
        tk.Label(linha1, text="Tipo:", bg='#1a0869', fg="white").pack(side="left", padx=(10, 0))
        var_tipo = tk.StringVar(value="ativo")
        tk.Radiobutton(linha1, text="Ativo", variable=var_tipo, value="ativo", bg='#1a0869', fg="white", selectcolor='#1a0869').pack(side="left", padx=3)
        tk.Radiobutton(linha1, text="Passivo", variable=var_tipo, value="passivo", bg='#1a0869', fg="white", selectcolor='#1a0869').pack(side="left", padx=3)
        
        tk.Label(linha1, text="Custo PE:", bg='#1a0869', fg="white").pack(side="left", padx=(10, 0))
        entry_custo = tk.Entry(linha1, width=5)
        entry_custo.pack(side="left", padx=5)
        entry_custo.insert(0, "0")
        
        # Linha 2: Efeitos
        linha2 = tk.Frame(frame_adicionar, bg='#1a0869')
        linha2.pack(fill="x", padx=5, pady=2)
        
        tk.Label(linha2, text="Efeitos:", bg='#1a0869', fg="white").pack(anchor="w")
        entry_efeitos = tk.Entry(linha2, width=80)
        entry_efeitos.pack(fill="x", pady=2)
        
        # Linha 3: Descrição
        linha3 = tk.Frame(frame_adicionar, bg='#1a0869')
        linha3.pack(fill="x", padx=5, pady=2)
        
        tk.Label(linha3, text="Descrição:", bg='#1a0869', fg="white").pack(anchor="w")
        entry_descricao = tk.Entry(linha3, width=80)
        entry_descricao.pack(fill="x", pady=2)
        
        # Botão adicionar
        def adicionar_item():
            nome = entry_nome.get().strip()
            tipo = var_tipo.get()
            custo_str = entry_custo.get().strip()
            efeitos = entry_efeitos.get().strip()
            descricao = entry_descricao.get().strip()
            categoria = var_categoria.get()
            
            if not nome or not efeitos or not descricao:
                messagebox.showwarning("Aviso", "Nome, efeitos e descrição são obrigatórios!")
                return
            
            try:
                custo = int(custo_str)
                if custo < 0:
                    custo = 0
            except ValueError:
                messagebox.showwarning("Aviso", "Custo deve ser um número inteiro!")
                return
            
            if categoria == "habilidade":
                self.character.habilidades.adicionar_habilidade(nome, tipo, custo, efeitos, descricao)
            else:
                self.character.poderes.adicionar_poder(nome, tipo, custo, efeitos, descricao)
            
            # Limpa campos
            entry_nome.delete(0, tk.END)
            entry_efeitos.delete(0, tk.END)
            entry_descricao.delete(0, tk.END)
            entry_custo.delete(0, tk.END)
            entry_custo.insert(0, "0")
            
            atualizar_lista()
        
        tk.Button(frame_adicionar, text="Adicionar", command=adicionar_item, bg="#115c11", fg="white", font=("Arial", 10)).pack(pady=5)
        
        # Frame para filtros
        frame_filtros = tk.Frame(popup, bg='#130f26')
        frame_filtros.pack(pady=5)
        
        var_filtro = tk.StringVar(value="todos")
        
        tk.Radiobutton(frame_filtros, text="Todos", variable=var_filtro, value="todos", bg='#130f26', fg="white", selectcolor='#1a0869', command=lambda: atualizar_lista()).pack(side="left", padx=8)
        tk.Radiobutton(frame_filtros, text="Ativos", variable=var_filtro, value="ativos", bg='#130f26', fg="white", selectcolor='#1a0869', command=lambda: atualizar_lista()).pack(side="left", padx=8)
        tk.Radiobutton(frame_filtros, text="Passivos", variable=var_filtro, value="passivos", bg='#130f26', fg="white", selectcolor='#1a0869', command=lambda: atualizar_lista()).pack(side="left", padx=8)
        
        # Frame para lista
        frame_lista = tk.Frame(popup, bg='#130f26')
        frame_lista.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Canvas com scrollbar
        canvas = tk.Canvas(frame_lista, bg='#1a0869', highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_lista, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1a0869')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def atualizar_lista():
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
            
            categoria = var_categoria.get()
            filtro = var_filtro.get()
            
            # Obtém itens baseado na categoria e filtro
            if categoria == "habilidade":
                if filtro == "ativos":
                    itens = self.character.habilidades.listar_ativas()
                elif filtro == "passivos":
                    itens = self.character.habilidades.listar_passivas()
                else:
                    itens = self.character.habilidades.listar_habilidades()
                simbolo_categoria = "⚔️"
                cor_base = "#1565c0"
            else:
                if filtro == "ativos":
                    itens = self.character.poderes.listar_ativos()
                elif filtro == "passivos":
                    itens = self.character.poderes.listar_passivos()
                else:
                    itens = self.character.poderes.listar_poderes()
                simbolo_categoria = "🔮"
                cor_base = "#4a148c"
            
            if not itens:
                tk.Label(scrollable_frame, text="Nenhum item", bg='#1a0869', fg="gray", font=("Arial", 12)).pack(pady=20)
                return
            
            for item in itens:
                frame_item = tk.Frame(scrollable_frame, bg='#2a1f4f', bd=1, relief='solid')
                frame_item.pack(fill="x", padx=5, pady=3)
                
                simbolo_tipo = "⚡" if item.tipo == "ativo" else "🛡️"
                
                # Header
                header = tk.Frame(frame_item, bg=cor_base)
                header.pack(fill="x")
                
                tk.Label(header, text=f"{simbolo_categoria}{simbolo_tipo} {item.nome}", font=("Arial", 12, "bold"), bg=cor_base, fg="white").pack(side="left", padx=5, pady=2)
                
                custo_text = f"Custo: {item.custo} PE" if item.custo > 0 else "Passivo"
                tk.Label(header, text=custo_text, font=("Arial", 10), bg=cor_base, fg="white").pack(side="right", padx=5, pady=2)
                
                # Descrição
                tk.Label(frame_item, text=f"Descrição: {item.descricao}", font=("Arial", 10), bg='#2a1f4f', fg="white", wraplength=650, justify="left").pack(anchor="w", padx=5, pady=2)
                
                # Efeitos
                tk.Label(frame_item, text=f"Efeitos: {item.efeitos}", font=("Arial", 10, "bold"), bg='#2a1f4f', fg="#90caf9", wraplength=650, justify="left").pack(anchor="w", padx=5, pady=2)
                
                # Botão remover
                tk.Button(frame_item, text="Remover", command=lambda n=item.nome, c=categoria: remover_item(n, c), bg="#8c1d1d", fg="white", font=("Arial", 9)).pack(anchor="e", padx=5, pady=2)
        
        def remover_item(nome, categoria):
            if categoria == "habilidade":
                self.character.habilidades.remover_habilidade(nome)
            else:
                self.character.poderes.remover_poder(nome)
            atualizar_lista()
        
        # Botões inferiores
        frame_botoes = tk.Frame(popup, bg='#130f26')
        frame_botoes.pack(pady=10)
        
        def limpar_todos():
            categoria = var_categoria.get()
            resultado = messagebox.askyesno("Confirmação", f"Tem certeza que deseja remover todos(as) {'as habilidades' if categoria == 'habilidade' else 'os poderes'}?")
            if resultado:
                if categoria == "habilidade":
                    self.character.habilidades.limpar_habilidades()
                else:
                    self.character.poderes.limpar_poderes()
                atualizar_lista()
        
        tk.Button(frame_botoes, text="Limpar Todos", command=limpar_todos, bg="#8c1d1d", fg="white", font=("Arial", 12)).pack(side="left", padx=10)
        tk.Button(frame_botoes, text="Fechar", command=popup.destroy, bg="#1a0869", fg="white", font=("Arial", 12)).pack(side="left", padx=10)
        
        atualizar_lista()
        popup.transient(self)
        popup.grab_set()

    def alterar_vida(self, multiplicador):
        try:
            valor = int(self.entry_vida.get() or 0)
            if multiplicador > 0:
                self.character.TomarCura(valor)
            else:
                self.character.TomarDano(valor)
            self.entry_vida.delete(0, tk.END)
            self.refresh()
        except ValueError:
            pass

    def alterar_energia(self, multiplicador):
        try:
            valor = int(self.entry_energia.get() or 0)
            if multiplicador > 0:
                self.character.PeAtual = min(self.character.PeAtual + valor, self.character.PeMax)
            else:
                self.character.PeAtual = max(self.character.PeAtual - valor, 0)
            self.entry_energia.delete(0, tk.END)
            self.refresh()
        except ValueError:
            pass

    def alterar_xp(self, multiplicador):
        try:
            valor = int(self.entry_xp.get() or 0)
            if multiplicador > 0:
                self.character.GanharXP(valor)
            else:
                self.character.XPAtual = max(self.character.XPAtual - valor, 0)
            self.entry_xp.delete(0, tk.END)
            self.refresh()
        except ValueError:
            pass

    def alterar_nivel(self, delta):
        if delta > 0:
            self.character.nivel += 1
        else:
            self.character.nivel = max(self.character.nivel - 1, 1)
        self.character.recalcularAtributos()
        self.refresh()

    def alterar_atributo(self, nome_atributo, delta):
        valor_atual = getattr(self.character, nome_atributo)
        novo_valor = max(valor_atual + delta, 0)
        setattr(self.character, nome_atributo, novo_valor)
        self.character.recalcularAtributos()
        self.refresh()
    ## funções dos botões extras ##
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
        
        # Inicializar variáveis de grupo como None
        self.grupo_esquerdo = None
        self.grupo_direito = None
        
        self.slot_esquerdo_personagem = None
        self.slot_direito_personagem = None

        tk.Button(self, text="Tela inicial", height=2, command=self.TelaInicial, bg="#1a0869", fg="white", font=("Arial", 20)).place(x=20, y=10, width=350, height=75)
        
        tk.Button(self, text="Seleção", height=2, command=self.TelaDeSelecao, bg="#1a0869", fg="white", font=("Arial", 20)).place(x=385, y=10, width=350, height=75)

        tk.Label(self, text="Combate", fg="white", bg="#1a0869", font=("Arial", 20, "bold"), width=20, height=2).place(x=870, y=10, width=350, height=75)

        tk.Button(self, text="Informações", height=2, command=self.TelaDeRegrasEItens, bg="#1a0869", fg="white", font=("Arial", 20)).place(x=1235, y=10, width=350, height=75)

        # --- Log de Combate (substituindo o painel central) ---
        self.criar_log_combate()

        # --- Criar seletores de grupos e listas ---
        self.criar_interface_grupos()
    
    def criar_log_combate(self):
        """Cria o log de combate no centro da tela"""
        self.log_frame = tk.Frame(self, bg="#1a0869", relief="solid", bd=2)
        self.log_frame.place(x=500, y=100, width=600, height=600)
        
        # Título do log
        tk.Label(self.log_frame, text="Log de Combate", 
                fg="white", bg="#1a0869", font=("Arial", 18, "bold")).pack(pady=10)
        
        # Frame para o canvas e scrollbar
        canvas_frame = tk.Frame(self.log_frame, bg='#1a0869')
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Canvas para scroll
        self.log_canvas = tk.Canvas(canvas_frame, bg="#130f26", highlightthickness=0)
        log_scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.log_canvas.yview)
        self.log_canvas.configure(yscrollcommand=log_scrollbar.set)
        
        log_scrollbar.pack(side="right", fill="y")
        self.log_canvas.pack(side="left", fill="both", expand=True)
        
        # Frame interno para as mensagens do log
        self.log_inner_frame = tk.Frame(self.log_canvas, bg="#130f26")
        self.log_canvas.create_window((0, 0), window=self.log_inner_frame, anchor='nw')
        self.log_inner_frame.bind("<Configure>", lambda e: self.log_canvas.configure(scrollregion=self.log_canvas.bbox("all")))
        
        # Mensagem inicial
        self.adicionar_log("=== Log de Combate Iniciado ===", cor="yellow")
        self.adicionar_log("Aguardando ações de combate...", cor="gray")

    def adicionar_log(self, mensagem, cor="white"):
        """Adiciona uma mensagem ao log de combate"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        log_entry = tk.Label(self.log_inner_frame, 
                           text=f"[{timestamp}] {mensagem}",
                           bg="#130f26", fg=cor, 
                           font=("Arial", 10),
                           wraplength=550,
                           justify="left",
                           anchor="w")
        log_entry.pack(fill="x", pady=1, padx=5)
        
        # Auto-scroll para o final
        self.log_canvas.update_idletasks()
        self.log_canvas.yview_moveto(1.0)

    def criar_interface_grupos(self):
        """Cria os seletores de grupos e as listas de personagens"""
        # Importar ttk se não estiver importado
        from tkinter import ttk
        
        # Obter lista de grupos disponíveis (baseado no código da tela de seleção)
        grupos_disponiveis = list(D.GruposDePersonagens.keys()) if hasattr(D, 'GruposDePersonagens') and D.GruposDePersonagens else []
        
        # --- Lado Esquerdo ---
        # Seletor de grupo esquerdo
        self.frame_seletor_esquerdo = tk.Frame(self, bg='#1a0869')
        self.frame_seletor_esquerdo.place(x=50, y=100, width=400, height=50)
        
        tk.Label(self.frame_seletor_esquerdo, text="Grupo Esquerdo:", fg="white", bg="#1a0869", font=("Arial", 12, "bold")).pack(side="left", padx=5)
        
        self.combo_grupo_esquerdo = ttk.Combobox(self.frame_seletor_esquerdo, values=grupos_disponiveis, state="readonly", font=("Arial", 10))
        self.combo_grupo_esquerdo.pack(side="right", padx=5)
        
        # Definir valor padrão se houver grupos disponíveis
        if grupos_disponiveis:
            # Priorizar "Players" se existir, senão pegar o primeiro
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
        
        tk.Label(self.frame_seletor_direito, text="Grupo Direito:", fg="white", bg="#1a0869", font=("Arial", 12, "bold")).pack(side="left", padx=5)
        
        self.combo_grupo_direito = ttk.Combobox(self.frame_seletor_direito, values=grupos_disponiveis, state="readonly", font=("Arial", 10))
        self.combo_grupo_direito.pack(side="right", padx=5)
        
        # Definir valor padrão se houver grupos disponíveis
        if grupos_disponiveis:
            # Priorizar "NPCs" se existir, senão pegar um grupo diferente do esquerdo
            if "NPCs" in grupos_disponiveis:
                self.grupo_direito = "NPCs"
            elif len(grupos_disponiveis) > 1:
                # Pegar um grupo diferente do esquerdo
                self.grupo_direito = next((g for g in grupos_disponiveis if g != self.grupo_esquerdo), grupos_disponiveis[0])
            else:
                self.grupo_direito = grupos_disponiveis[0]
            self.combo_grupo_direito.set(self.grupo_direito)
        else:
            self.grupo_direito = "Sem grupos"
        
        self.combo_grupo_direito.bind("<<ComboboxSelected>>", self.atualizar_grupo_direito)
        
        # Criar as listas iniciais
        self.frame_lista_esquerda = self.create_list_section_with_group(self.grupo_esquerdo, x=50, y=150)
        self.frame_lista_direita = self.create_list_section_with_group(self.grupo_direito, x=1150, y=150)

    def create_list_section_with_group(self, grupo_nome, x, y):
        """Cria uma seção de lista para um grupo específico"""
        frame = tk.Frame(self, bg='#1a0869')
        frame.place(x=x, y=y, width=400, height=550)
        
        # Verificar se o grupo existe nos dados (baseado na lógica da tela de seleção)
        if not grupo_nome or grupo_nome == "Sem grupos" or not hasattr(D, 'GruposDePersonagens') or grupo_nome not in D.GruposDePersonagens:
            # Criar frame com mensagem se não há grupo selecionado
            tk.Label(frame, text="Nenhum grupo selecionado" if grupo_nome == "Sem grupos" else f"Grupo '{grupo_nome}' não encontrado", 
                    fg="gray", bg="#1a0869", font=("Arial", 14)).pack(pady=200)
            return frame
        
        data_list = D.GruposDePersonagens[grupo_nome]
        
        label = tk.Label(frame, text=grupo_nome, fg="white", bg="#1a0869", font=("Arial", 16, "bold"))
        label.pack()

        if not data_list:
            # Se o grupo existe mas está vazio
            tk.Label(frame, text="Grupo vazio", fg="gray", bg="#1a0869", font=("Arial", 12)).pack(pady=100)
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
            char_frame = tk.Frame(inner_frame, bg="#220866", bd=2, relief="groove", width=380)
            char_frame.pack(fill="x", padx=5, pady=5)

            # Botão principal com informações do personagem
            info = f"{char.nome} || Nv {char.nivel} || XP: {char.XPAtual}/{char.XPlvlUp}\n"
            info += f"PV: {char.vidaAtual}/{char.vidaMax} || PE: {char.PeAtual}/{char.PeMax}\n"
            info += f"Bloqueio: {char.bloqueio} | Esquiva: {char.esquiva}"
            
            btn_principal = tk.Button(char_frame, text=info, bg="#1a0869", fg="white", font=("Arial", 10), 
                                    justify="left", command=lambda c=char: self.controller.abrir_detalhes(c))
            btn_principal.pack(fill="x", padx=5, pady=2)

            # Linha com botão de ações
            botoes_frame = tk.Frame(char_frame, bg="#220866")
            botoes_frame.pack(pady=2)

            tk.Button(botoes_frame, text="Ações", bg="#3a0a80", fg="white", font=("Arial", 9), 
                    command=lambda c=char: self.abrir_popup_acoes(c)).pack(side="left", padx=5)

            # Controles de dano/cura
            valor_var = tk.IntVar(value=1)
            controle_frame = tk.Frame(char_frame, bg="#220866")
            controle_frame.pack(pady=2)

            entry = tk.Entry(controle_frame, textvariable=valor_var, width=3, font=("Arial", 10))
            entry.grid(row=0, column=2, padx=5)

            # PV
            tk.Button(controle_frame, text="+PV", command=lambda c=char, v=valor_var: self.aplicar_cura(c, v),
                    width=3, font=("Arial", 8)).grid(row=0, column=0)
            tk.Button(controle_frame, text="-PV", command=lambda c=char, v=valor_var: self.aplicar_dano(c, v),
                    width=3, font=("Arial", 8)).grid(row=0, column=1)

            # PE
            tk.Button(controle_frame, text="+PE", command=lambda c=char, v=valor_var: self.aplicar_ganho_energia(c, v),
                    width=3, font=("Arial", 8)).grid(row=0, column=3)
            tk.Button(controle_frame, text="-PE", command=lambda c=char, v=valor_var: self.aplicar_gasto_energia(c, v),
                    width=3, font=("Arial", 8)).grid(row=0, column=4)

        return frame
    
    def get_all_personagens(self):
        """Retorna todos os personagens de todos os grupos"""
        todos_personagens = []
        if D.GruposDePersonagens:
            for grupo in D.GruposDePersonagens.values():
                todos_personagens.extend(grupo)
        return todos_personagens

    def atualizar_grupo_esquerdo(self, event=None):
        """Atualiza o grupo selecionado no lado esquerdo"""
        self.grupo_esquerdo = self.combo_grupo_esquerdo.get()
        # Destruir a lista atual e criar uma nova
        if hasattr(self, 'frame_lista_esquerda'):
            self.frame_lista_esquerda.destroy()
        self.frame_lista_esquerda = self.create_list_section_with_group(self.grupo_esquerdo, x=50, y=150)

    def atualizar_grupo_direito(self, event=None):
        """Atualiza o grupo selecionado no lado direito"""
        self.grupo_direito = self.combo_grupo_direito.get()
        # Destruir a lista atual e criar uma nova
        if hasattr(self, 'frame_lista_direita'):
            self.frame_lista_direita.destroy()
        self.frame_lista_direita = self.create_list_section_with_group(self.grupo_direito, x=1150, y=150)

    def create_list_section_with_group(self, grupo_nome, x, y):
        """Cria uma seção de lista para um grupo específico"""
        if not grupo_nome or grupo_nome not in D.GruposDePersonagens:
            frame = tk.Frame(self, bg='#1a0869')
            frame.place(x=x, y=y, width=400, height=550)
            tk.Label(frame, text="Nenhum grupo selecionado", fg="gray", bg="#1a0869", font=("Arial", 14)).pack(pady=200)
            return frame
        
        data_list = D.GruposDePersonagens[grupo_nome]
        
        frame = tk.Frame(self, bg='#1a0869')
        frame.place(x=x, y=y, width=400, height=550)

        label = tk.Label(frame, text=grupo_nome, fg="white", bg="#1a0869", font=("Arial", 16, "bold"))
        label.pack()

        if not data_list:
            # Se o grupo existe mas está vazio
            tk.Label(frame, text="Grupo vazio", fg="gray", bg="#1a0869", font=("Arial", 12)).pack(pady=100)
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
            char_frame.pack(fill="x", padx=10, pady=5)  # padx=5 para deixar 5px de margem de cada lado
            char_frame.pack_propagate(False)  # Impede que o frame se redimensione baseado no conteúdo
            char_frame.configure(width=360, height=150)

            info = f"{char.nome}   ||  Nv {char.nivel}   ||  XP:  {char.XPAtual}/{char.XPlvlUp}\n"
            info += f"PV: {char.vidaAtual}/{char.vidaMax}    ||   PE: {char.PeAtual}/{char.PeMax}\n"
            info += f"Bloqueio: {char.bloqueio}   |   Esquiva: {char.esquiva}"
            tk.Label(char_frame, text=info, bg="#220866", fg="white", font=("Arial", 12), justify="left").pack(anchor="w", padx=10, pady=5)

            # Linha com dois botões
            botoes_frame = tk.Frame(char_frame, bg="#220866")
            botoes_frame.pack(pady=5)

            tk.Button(botoes_frame, text="Abrir Detalhes", bg="#1a0869", fg="white", font=("Arial", 12), 
                    command=lambda c=char: self.controller.abrir_detalhes(c)).pack(side="left", padx=10)

            tk.Button(botoes_frame, text="Abrir ações", bg="#3a0a80", fg="white", font=("Arial", 12), 
                    command=lambda c=char: self.abrir_popup_acoes(c)).pack(side="left", padx=10)

            valor_var = tk.IntVar(value=1)
            controle_frame = tk.Frame(char_frame, bg="#220866")
            controle_frame.pack(pady=2)

            entry = tk.Entry(controle_frame, textvariable=valor_var, width=3, font=("Arial", 10))
            entry.grid(row=0, column=2, padx=10)

            # PV
            tk.Button(controle_frame, text="+PV", command=lambda c=char, v=valor_var: self.aplicar_cura(c, v),
                    width=4, font=("Arial", 10)).grid(row=0, column=0)
            tk.Button(controle_frame, text="-PV", command=lambda c=char, v=valor_var: self.aplicar_dano(c, v),
                    width=4, font=("Arial", 10)).grid(row=0, column=1)
            # PE
            tk.Button(controle_frame, text="+PE", command=lambda c=char, v=valor_var: self.aplicar_ganho_energia(c, v),
                    width=4, font=("Arial", 10)).grid(row=0, column=3)
            tk.Button(controle_frame, text="-PE", command=lambda c=char, v=valor_var: self.aplicar_gasto_energia(c, v),
                    width=4, font=("Arial", 10)).grid(row=0, column=4)

        return frame

    def create_list_section(self, title, data_list, x, y):
        return self.create_list_section_with_group(title, x, y)

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

    def refresh(self):
        """Atualiza as listas de personagens nas interfaces e as comboboxes de grupos"""
        # Atualizar lista de grupos disponíveis
        grupos_disponiveis = list(D.GruposDePersonagens.keys()) if hasattr(D, 'GruposDePersonagens') and D.GruposDePersonagens else []
        
        # Atualizar valores das comboboxes
        self.combo_grupo_esquerdo['values'] = grupos_disponiveis
        self.combo_grupo_direito['values'] = grupos_disponiveis
        
        # Verificar se os grupos selecionados ainda existem
        if self.grupo_esquerdo not in grupos_disponiveis and grupos_disponiveis:
            # Se o grupo atual não existe mais, selecionar o primeiro disponível
            self.grupo_esquerdo = grupos_disponiveis[0]
            self.combo_grupo_esquerdo.set(self.grupo_esquerdo)
        elif not grupos_disponiveis:
            self.grupo_esquerdo = "Sem grupos"
            self.combo_grupo_esquerdo.set(self.grupo_esquerdo)
        
        if self.grupo_direito not in grupos_disponiveis and grupos_disponiveis:
            # Se o grupo atual não existe mais, selecionar o primeiro disponível (diferente do esquerdo se possível)
            self.grupo_direito = next((g for g in grupos_disponiveis if g != self.grupo_esquerdo), grupos_disponiveis[0])
            self.combo_grupo_direito.set(self.grupo_direito)
        elif not grupos_disponiveis:
            self.grupo_direito = "Sem grupos"
            self.combo_grupo_direito.set(self.grupo_direito)
        
        # Atualizar lista esquerda se existe
        if hasattr(self, 'frame_lista_esquerda') and self.frame_lista_esquerda:
            self.frame_lista_esquerda.destroy()
            self.frame_lista_esquerda = self.create_list_section_with_group(self.grupo_esquerdo, x=50, y=150)
        
        # Atualizar lista direita se existe - COORDENADA CORRIGIDA
        if hasattr(self, 'frame_lista_direita') and self.frame_lista_direita:
            self.frame_lista_direita.destroy()
            self.frame_lista_direita = self.create_list_section_with_group(self.grupo_direito, x=1150 , y=150)

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

    def abrir_popup_tipos_ataque(self, atacante_pre_selecionado):
        """Abre o popup para selecionar o tipo de ataque"""
        popup = tk.Toplevel(self)
        popup.title("Tipos de Ataque")
        popup.configure(bg="#1a1a2e")
        popup.geometry("400x300")
        popup.resizable(False, False)
        
        tk.Label(popup, text="Selecione o tipo de ataque:", 
                bg="#1a1a2e", fg="white", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Frame para os botões de tipo de ataque
        botoes_frame = tk.Frame(popup, bg="#1a1a2e")
        botoes_frame.pack(pady=20)
        
        # Função para abrir ataque melee
        def ataque_melee():
            popup.destroy()
            self.abrir_popup_ataque_melee(atacante_pre_selecionado)
        
        # Função para abrir ataque ranged
        def ataque_ranged():
            popup.destroy()
            self.abrir_popup_ataque_ranged(atacante_pre_selecionado)
        
        
        
        # Botões de tipo de ataque
        tk.Button(botoes_frame, text="Ataque Melee", command=ataque_melee,
                bg="#8B0000", fg="white", font=("Arial", 12), width=20, height=2).pack(pady=5)
        
        tk.Button(botoes_frame, text="Ataque Ranged", command=ataque_ranged,
                bg="#006400", fg="white", font=("Arial", 12), width=20, height=2).pack(pady=5)
        
        tk.Button(botoes_frame, text="Ataque arma especial", command=lambda: print("Funcionalidade não implementada"),
                bg="#FF8C00", fg="white", font=("Arial", 12), width=20, height=2, state="disabled").pack(pady=5)
        
        tk.Button(botoes_frame, text="Ataque de Poder/Magia", command=lambda: print("Funcionalidade não implementada"),
          bg="#800080", fg="white", font=("Arial", 12), width=20, height=2, state="disabled").pack(pady=5)
        
        # Botão de fechar
        tk.Button(popup, text="Fechar", command=popup.destroy, 
                bg="#3a0a80", fg="white", font=("Arial", 12), width=15).pack(pady=20)

    def abrir_popup_ataque_melee(self, atacante_pre_selecionado):
        """Abre o popup de ataque melee com o atacante já pré-selecionado"""
        import random
        popup = tk.Toplevel(self)
        popup.title("Ataque Melee")
        popup.geometry("500x550")
        popup.configure(bg="#1a1a2e")
        popup.resizable(False, False)

        todos_personagens = self.get_all_personagens()
        personagens_names = [p.nome for p in todos_personagens]

        # Frame principal
        main_frame = tk.Frame(popup, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        tk.Label(main_frame, text=f"Ataque Melee - {atacante_pre_selecionado.nome}", 
                bg="#1a1a2e", fg="white", font=("Arial", 14, "bold")).pack(pady=(0, 20))

        # Alvo
        alvo_frame = tk.Frame(main_frame, bg="#1a1a2e")
        alvo_frame.pack(fill="x", pady=5)
        tk.Label(alvo_frame, text="Alvo:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(side="left")
        alvo_var = tk.StringVar()
        alvo_menu = ttk.Combobox(alvo_frame, textvariable=alvo_var, state="readonly", values=personagens_names, width=30)
        alvo_menu.pack(side="right")

        # Arma
        arma_frame = tk.Frame(main_frame, bg="#1a1a2e")
        arma_frame.pack(fill="x", pady=5)
        tk.Label(arma_frame, text="Arma Melee:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(side="right")
        arma_var = tk.StringVar()
        arma_menu = ttk.Combobox(arma_frame, textvariable=arma_var, state="readonly", width=30)
        arma_menu.pack(side="right")

        # Região do corpo
        regiao_frame = tk.Frame(main_frame, bg="#1a1a2e")
        regiao_frame.pack(fill="x", pady=5)
        tk.Label(regiao_frame, text="Região do Corpo:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(side="left")
        regiao_var = tk.StringVar(value="Aleatoria")
        regiao_menu = ttk.Combobox(regiao_frame, textvariable=regiao_var, state="readonly", width=30,
                                values=["Aleatoria", "Cabeça", "Rosto", "Torso", "Pernas", "Braços"])
        regiao_menu.pack(side="right")

        # Tipo de Ataque
        tipo_frame = tk.Frame(main_frame, bg="#1a1a2e")
        tipo_frame.pack(fill="x", pady=5)
        tk.Label(tipo_frame, text="Tipo de Ataque:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(side="left")
        tipo_var = tk.StringVar(value="simples")
        tipo_menu = ttk.Combobox(tipo_frame, textvariable=tipo_var, state="readonly", width=30,
                                values=["simples", "forte", "investida", "arremesso"])
        tipo_menu.pack(side="right")

        # Buff de Acerto
        buff_acerto_frame = tk.Frame(main_frame, bg="#1a1a2e")
        buff_acerto_frame.pack(fill="x", pady=5)
        tk.Label(buff_acerto_frame, text="Buff de Acerto:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(side="left")
        buff_acerto_var = tk.IntVar(value=0)
        tk.Entry(buff_acerto_frame, textvariable=buff_acerto_var, font=("Arial", 12), width=10, justify="center").pack(side="right")

        # Debuff de Acerto
        debuff_acerto_frame = tk.Frame(main_frame, bg="#1a1a2e")
        debuff_acerto_frame.pack(fill="x", pady=5)
        tk.Label(debuff_acerto_frame, text="Debuff de Acerto:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(side="left")
        debuff_acerto_var = tk.IntVar(value=0)
        tk.Entry(debuff_acerto_frame, textvariable=debuff_acerto_var, font=("Arial", 12), width=10, justify="center").pack(side="right")

        # Buff de Dano
        buff_dano_frame = tk.Frame(main_frame, bg="#1a1a2e")
        buff_dano_frame.pack(fill="x", pady=5)
        tk.Label(buff_dano_frame, text="Buff de Dano:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(side="left")
        buff_dano_var = tk.IntVar(value=0)
        tk.Entry(buff_dano_frame, textvariable=buff_dano_var, font=("Arial", 12), width=10, justify="center").pack(side="right")

        # Debuff de Dano
        debuff_dano_frame = tk.Frame(main_frame, bg="#1a1a2e")
        debuff_dano_frame.pack(fill="x", pady=5)
        tk.Label(debuff_dano_frame, text="Debuff de Dano:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(side="left")
        debuff_dano_var = tk.IntVar(value=0)
        tk.Entry(debuff_dano_frame, textvariable=debuff_dano_var, font=("Arial", 12), width=10, justify="center").pack(side="right")

        # Rolagem
        rolagem_frame = tk.Frame(main_frame, bg="#1a1a2e")
        rolagem_frame.pack(fill="x", pady=10)
        tk.Label(rolagem_frame, text="Valor do Dado:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(side="left")
        rolagem_var = tk.IntVar(value=0)
        tk.Entry(rolagem_frame, textvariable=rolagem_var, font=("Arial", 12), width=10, justify="center").pack(side="left", padx=10)
        tk.Button(rolagem_frame, text="Rolar Dado", command=lambda: executar_rolagem_ataque(),
                bg="#0077b6", fg="white", font=("Arial", 11)).pack(side="right")

        # Label de resultado da rolagem
        resultado_rolagem_label = tk.Label(main_frame, text="", bg="#1a1a2e", fg="lightblue", font=("Arial", 10))
        resultado_rolagem_label.pack(pady=5)

        # Label de resultado
        resultado_label = tk.Label(main_frame, text="", bg="#1a1a2e", fg="lightgreen", font=("Arial", 11), wraplength=450)
        resultado_label.pack(pady=10)

        # Inicializar dicionário para mapear armas
        arma_id_por_nome = {}

        def executar_rolagem_ataque():
            atacante = atacante_pre_selecionado
            atributo_base = atacante.Forca
            rolagens = [random.randint(1, 20) for _ in range(max(1, atributo_base // 2))]
            melhor = max(rolagens) if rolagens else 0

            rolagem_var.set(melhor)
            resultado_rolagem_label.config(
                text=f"Rolagem com Força ({atributo_base // 2}x D20): {rolagens} → Melhor: {melhor}"
            )

        # Atualizar armas melee
        def atualizar_armas_melee(*_):
            nonlocal arma_id_por_nome
            arma_id_por_nome = {}
            atacante = atacante_pre_selecionado
            armas_melee = []
            
            # Debug: verificar se existe equipados
            if not hasattr(atacante, 'equipados'):
                resultado_label.config(text="Debug: Atacante não possui atributo 'equipados'", fg="yellow")
                return
                
            # Verificar itens equipados primeiro
            if hasattr(atacante.equipados, 'itens'):
                for i in atacante.equipados.itens:
                    item = i["item"] if isinstance(i, dict) else i
                    if isinstance(item, CB.Melee):
                        entrada = f"{item.nome} (ID: {item.Id})"
                        armas_melee.append(entrada)
                        arma_id_por_nome[entrada] = item.Id
            
            # Se não encontrou em equipados, verificar inventário
            if not armas_melee and hasattr(atacante, 'inventario'):
                if hasattr(atacante.inventario, 'itens'):
                    for i in atacante.inventario.itens:
                        item = i["item"] if isinstance(i, dict) else i
                        if isinstance(item, CB.Melee):
                            entrada = f"{item.nome} (ID: {item.Id})"
                            armas_melee.append(entrada)
                            arma_id_por_nome[entrada] = item.Id

            arma_menu['values'] = armas_melee
            if armas_melee:
                arma_var.set(armas_melee[0])
            else:
                resultado_label.config(text="Nenhuma arma melee encontrada nos equipados ou inventário.", fg="yellow")

        # Confirmar ataque
        def confirmar_ataque_melee():
            try:
                alvo_nome = alvo_var.get().strip()
                entrada_arma = arma_var.get().strip()
                rolagem = rolagem_var.get()
                buff_dano = buff_dano_var.get()
                debuff_dano = debuff_dano_var.get()
                buff_acerto = buff_acerto_var.get()
                debuff_acerto = debuff_acerto_var.get()
                regiao = regiao_var.get()
                tipo = tipo_var.get()

                # Verificações detalhadas com debug
                if not alvo_nome:
                    resultado_label.config(text="Debug: Nenhum alvo selecionado.", fg="red")
                    return
                    
                if not entrada_arma:
                    resultado_label.config(text="Debug: Nenhuma arma selecionada.", fg="red")
                    return

                atacante = atacante_pre_selecionado
                
                # Buscar alvo
                alvo = None
                for p in todos_personagens:
                    if p.nome.strip() == alvo_nome:
                        alvo = p
                        break
                
                if not alvo:
                    resultado_label.config(text=f"Debug: Alvo '{alvo_nome}' não encontrado. Personagens disponíveis: {[p.nome for p in todos_personagens]}", fg="red")
                    return

                # Buscar arma
                arma_id = arma_id_por_nome.get(entrada_arma)
                if not arma_id:
                    resultado_label.config(text=f"Debug: ID da arma '{entrada_arma}' não encontrado. Armas disponíveis: {list(arma_id_por_nome.keys())}", fg="red")
                    return

                # Buscar a arma pelo ID
                arma = None
                
                # Procurar primeiro nos equipados
                if hasattr(atacante, 'equipados') and hasattr(atacante.equipados, 'itens'):
                    for i in atacante.equipados.itens:
                        item = i["item"] if isinstance(i, dict) else i
                        if isinstance(item, CB.Melee) and item.Id == arma_id:
                            arma = item
                            break

                if not arma:
                    resultado_label.config(text=f"Debug: Arma com ID {arma_id} não encontrada no inventário do atacante.", fg="red")
                    return
                
                resultado = CB.acerto_melee(
                    atacante=atacante,
                    alvo=alvo,
                    rolagem=rolagem,
                    id_arma=arma.Id,
                    regiao=regiao,
                    tipo_ataque=tipo,
                    BuffDano=buff_dano,
                    DebuffDano=debuff_dano,
                    BuffAcerto=buff_acerto,
                    DebuffAcerto=debuff_acerto
                )
                

                self.adicionar_log(f"Ataque Melee: {atacante.nome} → {alvo.nome} ({regiao})", "orange")
                self.adicionar_log(f"Resultado: {resultado}", "lightgreen")
                resultado_label.config(text="Ataque executado com sucesso!", fg="lightgreen")
                self.refresh()

            except Exception as e:
                erro_completo = f"Erro detalhado: {str(e)}\nTipo: {type(e).__name__}"
                resultado_label.config(text=erro_completo, fg="red")
                self.adicionar_log(f"ERRO na execução do ataque: {erro_completo}", "red")
                import traceback
                traceback.print_exc()

        # Botões
        botoes_frame = tk.Frame(main_frame, bg="#1a1a2e")
        botoes_frame.pack(pady=20)
        
        tk.Button(botoes_frame, text="Confirmar Ataque", command=confirmar_ataque_melee,
                bg="#38b000", fg="white", font=("Arial", 12), width=15).pack(side="left", padx=5)
        
        tk.Button(botoes_frame, text="Cancelar", command=popup.destroy,
                bg="#8B0000", fg="white", font=("Arial", 12), width=15).pack(side="right", padx=5)

        # Inicializar armas
        atualizar_armas_melee()

    def abrir_popup_ataque_ranged(self, atacante_pre_selecionado):
        """Abre o popup de ataque ranged com o atacante já pré-selecionado"""
        import random
        popup = tk.Toplevel(self)
        popup.title("Ataque Ranged")
        popup.geometry("560x640")
        popup.configure(bg="#1a1a2e")
        popup.resizable(False, False)

        todos_personagens = self.get_all_personagens()
        personagens_names = [p.nome for p in todos_personagens]

        # Frame principal
        main_frame = tk.Frame(popup, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        tk.Label(main_frame, text=f"Ataque Ranged - {atacante_pre_selecionado.nome}", bg="#1a1a2e", fg="white", font=("Arial", 14, "bold")).pack(pady=(0, 20))

        # Alvo
        alvo_frame = tk.Frame(main_frame, bg="#1a1a2e")
        alvo_frame.pack(fill="x", pady=5)
        tk.Label(alvo_frame, text="Alvo:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(side="left")
        alvo_var = tk.StringVar()
        alvo_menu = ttk.Combobox(alvo_frame, textvariable=alvo_var, state="readonly", values=personagens_names, width=34)
        alvo_menu.pack(side="right")

        # Arma
        arma_frame = tk.Frame(main_frame, bg="#1a1a2e")
        arma_frame.pack(fill="x", pady=5)
        tk.Label(arma_frame, text="Arma Ranged:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(side="left")
        arma_var = tk.StringVar()
        arma_menu = ttk.Combobox(arma_frame, textvariable=arma_var, state="readonly", width=34)
        arma_menu.pack(side="right")

        regiao_frame = tk.Frame(main_frame, bg="#1a1a2e")
        regiao_frame.pack(fill="x", pady=5)
        tk.Label(regiao_frame, text="Região do Corpo:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(side="left")
        regiao_var = tk.StringVar(value="Aleatória")
        regiao_menu = ttk.Combobox(regiao_frame, textvariable=regiao_var, state="readonly", width=30,
                        values=["Aleatória", "Cabeça", "Rosto", "Torso", "Pernas", "Braços"])
        regiao_menu.pack(side="right")

        cobertura_frame = tk.Frame(main_frame, bg="#1a1a2e")
        cobertura_frame.pack(fill="x", pady=5)
        tk.Label(cobertura_frame, text="Nível de Cobertura:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(side="left")
        cobertura_var = tk.StringVar(value="Nenhuma")
        cobertura_menu = ttk.Combobox(cobertura_frame, textvariable=cobertura_var, state="readonly", width=30,
                        values=["Nenhuma", "Parcial", "Alta", "Total"])
        cobertura_menu.pack(side="right")

        # Material da cobertura (novo)
        material_frame = tk.Frame(main_frame, bg="#1a1a2e")
        material_frame.pack(fill="x", pady=5)
        tk.Label(material_frame, text="Material da Cobertura:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(side="left")
        material_var = tk.StringVar(value="Madeira")
        material_menu = ttk.Combobox(material_frame, textvariable=material_var, state="readonly", width=30, values=["Nenhum", "Gesso", "Madeira", "Concreto", "Aço"])
        material_menu.pack(side="right")

        # Quantidade de Disparos
        disparos_frame = tk.Frame(main_frame, bg="#1a1a2e")
        disparos_frame.pack(fill="x", pady=5)
        tk.Label(disparos_frame, text="Quantidade de Disparos:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(side="left")
        disparos_var = tk.IntVar(value=1)
        tk.Entry(disparos_frame, textvariable=disparos_var, font=("Arial", 12), width=10, justify="center").pack(side="right")

        # Distância
        distancia_frame = tk.Frame(main_frame, bg="#1a1a2e")
        distancia_frame.pack(fill="x", pady=5)
        tk.Label(distancia_frame, text="Distância até o alvo:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(side="left")
        distancia_var = tk.IntVar(value=1)
        tk.Entry(distancia_frame, textvariable=distancia_var, font=("Arial", 12), width=10, justify="center").pack(side="right")

        # Buff/Debuff de Acerto
        acerto_frame = tk.Frame(main_frame, bg="#1a1a2e")
        acerto_frame.pack(fill="x", pady=5)
        tk.Label(acerto_frame, text="Buff/Debuff de Acerto:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(side="left")
        buff_acerto_var = tk.IntVar(value=0)
        tk.Entry(acerto_frame, textvariable=buff_acerto_var, font=("Arial", 12), width=10, justify="center").pack(side="right")

        # Buff/Debuff de Dano
        dano_frame = tk.Frame(main_frame, bg="#1a1a2e")
        dano_frame.pack(fill="x", pady=5)
        tk.Label(dano_frame, text="Buff/Debuff de Dano:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(side="left")
        buff_dano_var = tk.IntVar(value=0)
        tk.Entry(dano_frame, textvariable=buff_dano_var, font=("Arial", 12), width=10, justify="center").pack(side="right")

        # Rolagem
        rolagem_frame = tk.Frame(main_frame, bg="#1a1a2e")
        rolagem_frame.pack(fill="x", pady=10)
        tk.Label(rolagem_frame, text="Valor do Dado:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(side="left")
        rolagem_var = tk.IntVar(value=0)
        tk.Entry(rolagem_frame, textvariable=rolagem_var, font=("Arial", 12), width=10, justify="center").pack(side="left", padx=10)
        tk.Button(rolagem_frame, text="Rolar Dado", command=lambda: executar_rolagem_ataque(),
                bg="#0077b6", fg="white", font=("Arial", 11)).pack(side="right")

        # Label de resultado da rolagem
        resultado_rolagem_label = tk.Label(main_frame, text="", bg="#1a1a2e", fg="lightblue", font=("Arial", 10))
        resultado_rolagem_label.pack(pady=5)

        def executar_rolagem_ataque():
            atacante = atacante_pre_selecionado
            atributo_base = atacante.Tatica
            rolagens = [random.randint(1, 20) for _ in range(max(1, atributo_base // 2))]
            melhor = max(rolagens) if rolagens else 0

            rolagem_var.set(melhor)
            resultado_rolagem_label.config(
                text=f"Rolagem com Tática ({atributo_base // 2}x D20): {rolagens} → Melhor: {melhor}"
            )

        # Função para determinar região aleatória
        def obter_regiao_final_disparo(regia_escolhida):
            regioes_possiveis = ["Cabeça", "Rosto", "Torso", "Pernas", "Braços"]
            if regia_escolhida != "Aleatória":
                return regia_escolhida
            # aleatoriza a cada disparo
            return random.choice(regioes_possiveis)

        def atualizar_armas_ranged(*_):
            self.arma_id_por_nome = {}
            atacante = atacante_pre_selecionado
            armas_ranged = []
            self.arma_id_por_nome.clear()

            for i in atacante.equipados.itens:
                item = i["item"]
                if isinstance(item, CB.Ranged):
                    entrada = f"{item.nome} (ID: {item.Id})"
                    armas_ranged.append(entrada)
                    self.arma_id_por_nome[entrada] = item.Id

            arma_menu['values'] = armas_ranged
            if armas_ranged:
                arma_var.set(armas_ranged[0])

        # Confirmar ataque
        def confirmar_ataque_ranged():
            alvo_nome = alvo_var.get()
            entrada_arma = arma_var.get()
            rolagem = rolagem_var.get()
            buff_dano = buff_dano_var.get()
            buff_acerto = buff_acerto_var.get()
            regiao_selecionada = regiao_var.get()
            disparos = max(1, disparos_var.get())
            distancia = distancia_var.get()
            cobertura = cobertura_var.get()
            material = material_var.get()

            atacante = atacante_pre_selecionado
            alvo = next((p for p in todos_personagens if p.nome == alvo_nome), None)
            arma_id = self.arma_id_por_nome.get(entrada_arma)
            arma = next((i["item"] for i in atacante.equipados.itens if isinstance(i["item"], CB.Ranged) and i["item"].Id == arma_id), None)

            if not alvo or not arma:
                resultado_label.config(text="Erro: alvo ou arma inválido(s).", fg="red")
                return

            # obter perfuracao da arma (tentativa robusta)
            perfuracao = getattr(arma, "Perfuracao", None)
            if perfuracao is None:
                perfuracao = getattr(arma, "perfuracao", None)
            if perfuracao is None:
                perfuracao = getattr(arma, "Penetration", 0)
            try:
                perfuracao = int(perfuracao)
            except Exception:
                perfuracao = 0

            resultados_disparos = []

            for n in range(disparos):
                regiao_final = obter_regiao_final_disparo(regiao_selecionada)

                res = CB.acerto_ranged(
                    atacante=atacante,
                    alvo=alvo,
                    Rolagem=rolagem,
                    id_arma=arma.Id,
                    distancia=distancia,
                    disparos=1,
                    regiao=regiao_final,
                    BuffDano=buff_dano,
                    BuffAcerto=buff_acerto,
                    DebuffAcerto=0,
                    DebuffDano=0,
                    cobertura=cobertura,
                    material=material
                )

                resultados_disparos.append(f"Tiro {n+1}: {res}")

            # Agregar resultados e adicionar ao log
            texto_log = f"Ataque Ranged: {atacante.nome}, {arma.nome} → {alvo.nome} (Cobertura: {cobertura} / {material}) - {disparos} disparos\n"
            texto_log += "\n".join(resultados_disparos)

            self.adicionar_log(texto_log, "orange")
            # também mostra resumo na label de resultado
            resultado_label.config(text=f"{disparos} disparo(s) processado(s). Veja o log para detalhes.", fg="lightgreen")

            self.refresh()
            popup.destroy()

        # Label de resultado
        resultado_label = tk.Label(main_frame, text="", bg="#1a1a2e", fg="lightgreen", font=("Arial", 11))
        resultado_label.pack(pady=10)

        # Botões
        botoes_frame = tk.Frame(main_frame, bg="#1a1a2e")
        botoes_frame.pack(pady=20)

        tk.Button(botoes_frame, text="Confirmar Ataque", command=confirmar_ataque_ranged,
                bg="#38b000", fg="white", font=("Arial", 12), width=18).pack(side="left", padx=5)

        tk.Button(botoes_frame, text="Cancelar", command=popup.destroy,
                bg="#8B0000", fg="white", font=("Arial", 12), width=18).pack(side="right", padx=5)

        # Inicializar armas
        atualizar_armas_ranged()

    def abrir_popup_loot_com_origem(self, origem_pre_selecionada):
        """Abre o popup de loot com a origem já pré-selecionada"""
        popup = tk.Toplevel(self)
        popup.title("Pilhagem")
        popup.geometry("1000x500")
        popup.configure(bg="#1a1a2e")
        popup.resizable(False, False)

        todos_personagens = self.get_all_personagens()
        personagens = [f"{p.nome}" for p in todos_personagens]

        destino_var = tk.StringVar()
        origem_var = tk.StringVar(value=origem_pre_selecionada.nome)

        # --- Linha de seleção (linha 0) ---
        linha_selecao = tk.Frame(popup, bg="#1a1a2e")
        linha_selecao.pack(pady=10)

        frame_sel_dest = tk.Frame(linha_selecao, bg="#1a1a2e")
        frame_sel_dest.grid(row=0, column=0, padx=30)
        tk.Label(frame_sel_dest, text="Destino (Recebe):", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack()
        ttk.Combobox(frame_sel_dest, textvariable=destino_var, state="readonly", values=personagens).pack()

        frame_central = tk.Frame(linha_selecao, bg="#1a1a2e")
        frame_central.grid(row=0, column=1, padx=30)
        tk.Label(frame_central, text="Transferência", bg="#1a1a2e", fg="white", font=("Arial", 12, "bold")).pack()

        frame_sel_orig = tk.Frame(linha_selecao, bg="#1a1a2e")
        frame_sel_orig.grid(row=0, column=2, padx=30)
        tk.Label(frame_sel_orig, text="Origem (Loot):", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack()
        ttk.Combobox(frame_sel_orig, textvariable=origem_var, state="readonly", values=personagens).pack()

        # --- Linha dos inventários (linha 1) ---
        linha_inventario = tk.Frame(popup, bg="#1a1a2e")
        linha_inventario.pack(fill="both", expand=True, padx=20, pady=(0, 10))

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

        frame_scroll_d = criar_frame_inventario(linha_inventario, "Inventário Destino")
        frame_scroll_o = criar_frame_inventario(linha_inventario, "Inventário Origem")

        # --- Função de transferência ---
        def transferir_item(item, origem, destino, quantidade):
            if quantidade <= 0:
                return
            origem.inventario.remover_item(item, quantidade)
            destino.inventario.adicionar_item_objeto(item, quantidade)
            atualizar_listas()
            self.refresh()

        def atualizar_listas():
            for w in frame_scroll_o.winfo_children(): w.destroy()
            for w in frame_scroll_d.winfo_children(): w.destroy()

            nome_o = origem_var.get()
            nome_d = destino_var.get()

            origem = next((p for p in todos_personagens if p.nome == nome_o), None)
            destino = next((p for p in todos_personagens if p.nome == nome_d), None)

            if not origem or not destino or origem == destino:
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

            for item in origem.inventario.listar_itens():
                criar_item_row(frame_scroll_o, item, origem, destino, "←")

            for item in destino.inventario.listar_itens():
                criar_item_row(frame_scroll_d, item, destino, origem, "→")

        origem_var.trace_add("write", lambda *_: atualizar_listas())
        destino_var.trace_add("write", lambda *_: atualizar_listas())

        tk.Button(popup, text="Fechar", command=popup.destroy, font=("Arial", 12), bg="#004080", fg="white").pack(pady=(0, 10))

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
        
        tk.Label(popup, text="Escolha a arma para recarregar:", 
                bg="#1a0869", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        
        def escolher_arma(arma_selecionada):
            popup.destroy()
            self.abrir_popup_escolher_municao(personagem, arma_selecionada)
        
        # Mostrar armas disponíveis
        for arma in armas_ranged:
            info_texto = f"{arma.nome} - {arma.munições}/{arma.capacidade}"
            tk.Button(popup, text=info_texto, command=lambda a=arma: escolher_arma(a),
                    bg="#006400", fg="white", font=("Arial", 11), width=30, height=2).pack(pady=5)
        
        tk.Button(popup, text="Cancelar", command=popup.destroy, 
                bg="#8B0000", fg="white", font=("Arial", 11)).pack(pady=10)

    def abrir_popup_escolher_municao(self, personagem, arma):
        """Popup para escolher munição e quantidade para recarregar"""
        popup = tk.Toplevel(self)
        popup.title("Escolher Munição")
        popup.configure(bg="#1a0869")
        popup.geometry("400x300")
        popup.resizable(False, False)
        
        tk.Label(popup, text=f"Recarregando: {arma.nome}", 
                bg="#1a0869", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(popup, text=f"Munições atuais: {arma.munições}/{arma.capacidade}",
                bg="#1a0869", fg="white", font=("Arial", 10)).pack(pady=5)
        
        # Buscar munições compatíveis
        itens_inventario = personagem.inventario.listar_itens()
        municoes_compativeis = [
            item for item in itens_inventario
            if isinstance(item["objeto"], CB.Municao) and item["objeto"].calibre == arma.calibre
        ]
        
        if not municoes_compativeis:
            tk.Label(popup, text="Sem munições compatíveis!", 
                    bg="#1a0869", fg="red", font=("Arial", 12)).pack(pady=20)
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
                    self._remover_item_do_inventario(municao_obj, carregado)
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
                        self._remover_item_do_inventario(municao_obj, carregado)
                        popup.destroy()
            except Exception as e:
                print(f"Erro: {e}")
        
        # Botões
        botoes_frame = tk.Frame(popup, bg="#1a0869")
        botoes_frame.pack(pady=20)
        
        tk.Button(botoes_frame, text="Carregar Qtd", command=recarregar_quantidade,
                bg="#006400", fg="white").pack(side="left", padx=10)
        tk.Button(botoes_frame, text="Carregar Tudo", command=recarregar_tudo,
                bg="#004080", fg="white").pack(side="left", padx=10)
        tk.Button(botoes_frame, text="Cancelar", command=popup.destroy,
                bg="#8B0000", fg="white").pack(side="left", padx=10)

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
                armas_vazias = [item["objeto"] for item in itens_equipados 
                            if isinstance(item["objeto"], CB.Ranged)]
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
                tk.Label(popup, text="Nenhuma arma com munição encontrada!", 
                        bg="#1a0869", fg="red", font=("Arial", 12)).pack(pady=50)
                tk.Button(popup, text="OK", command=popup.destroy).pack()
                return
        
        popup = tk.Toplevel(self)
        popup.title(f"Descarregar Arma - {personagem.nome}")
        popup.configure(bg="#1a0869")
        popup.geometry("400x300")
        popup.resizable(False, False)
        
        tk.Label(popup, text="Escolha a arma para descarregar:", 
                bg="#1a0869", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        
        def escolher_arma(arma_selecionada):
            popup.destroy()
            self.abrir_popup_descarregar_quantidade(personagem, arma_selecionada)
        
        # Mostrar armas disponíveis
        for arma in armas_ranged:
            info_texto = f"{arma.nome} - {arma.munições} munições"
            tk.Button(popup, text=info_texto, command=lambda a=arma: escolher_arma(a),
                    bg="#FF8C00", fg="white", font=("Arial", 11), width=30, height=2).pack(pady=5)
        
        tk.Button(popup, text="Cancelar", command=popup.destroy, 
                bg="#8B0000", fg="white", font=("Arial", 11)).pack(pady=10)

    def abrir_popup_descarregar_quantidade(self, personagem, arma):
        """Popup para escolher quantidade a descarregar"""
        popup = tk.Toplevel(self)
        popup.title("Descarregar Munição")
        popup.configure(bg="#1a0869")
        popup.geometry("350x250")
        popup.resizable(False, False)
        
        tk.Label(popup, text=f"Descarregando: {arma.nome}", 
                bg="#1a0869", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(popup, text=f"Munições na arma: {arma.munições}",
                bg="#1a0869", fg="white", font=("Arial", 10)).pack(pady=5)
        
        tk.Label(popup, text="Quantidade a descarregar:", 
                bg="#1a0869", fg="white", font=("Arial", 10)).pack(pady=10)
        
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
                    popup.destroy()
            except Exception as e:
                print(f"Erro: {e}")
        
        def descarregar_tudo():
            try:
                municoes = arma.descarregar_municao(quantidade=arma.munições)
                if municoes:
                    for municao in municoes:
                        personagem.inventario.adicionar_item_objeto(municao)
                    popup.destroy()
            except Exception as e:
                print(f"Erro: {e}")
        
        # Botões
        botoes_frame = tk.Frame(popup, bg="#1a0869")
        botoes_frame.pack(pady=30)
        
        tk.Button(botoes_frame, text="Descarregar Qtd", command=descarregar_quantidade,
                bg="#FF8C00", fg="white").pack(side="left", padx=10)
        tk.Button(botoes_frame, text="Descarregar Tudo", command=descarregar_tudo,
                bg="#8B0000", fg="white").pack(side="left", padx=10)
        tk.Button(botoes_frame, text="Cancelar", command=popup.destroy,
                bg="#006400", fg="white").pack(side="left", padx=10)
    
    def _remover_item_do_inventario(self, item, quantidade=1):
        """Helper function para remover itens do inventário do personagem"""
        try:
            self.character.inventario.remover_item(item, quantidade)
            return True
        except Exception as e:
            print(f"Erro ao remover item do inventário: {e}")
            return False
    
    def TelaInicial(self):
        self.controller.TelaInicial()

    def TelaDeSelecao(self):
        self.controller.TelaDeSelecao()
    
    def TelaDeRegrasEItens(self):
        self.controller.TelaDeRegrasEItens()
### TELA DE COMBATE ###
### TELA DE COMBATE ###
### TELA DE COMBATE ###

### TELA DE DICIONARIOS ###
### TELA DE DICIONARIOS ###
### TELA DE DICIONARIOS ###
class RegrasItensScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.place(x=0, y=0, width=1600, height=900)
        self.config(bg='#130f26')
        
        # Dados atuais selecionados
        self.tabela_atual = None
        self.dados_atuais = {}
        
        # Mapeamento de tabelas para templates
        self.templates_tabelas = {
            "Itens": self.template_itens,
            "Ranged": self.template_ranged,
            "Melee": self.template_melee,
            "Proteção": self.template_protecao,
            "Munições": self.template_municoes,
            "Explosivos": self.template_explosivos,
            "Consumíveis": self.template_consumiveis,
            "Melhorias": self.template_melhorias,
            "Proficiências": self.template_proficiencias,
            "NPCs": self.template_npcs,
            "Kits": self.template_kits,
            "Buffs e Debuffs": self.template_buffs_debuffs,
            "Habilidades": self.template_habilidades,
            "Poderes": self.template_poderes
        }
        
        self.setup_ui()
        self.setup_styles()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("default")
        
        style.configure("CustomCombobox.TCombobox", 
                       foreground="white", 
                       background="#2a1f4a", 
                       fieldbackground="#2a1f4a", 
                       bordercolor="#1a0869", 
                       arrowcolor="white", 
                       font=("Arial", 12))
        
        style.configure("Custom.Treeview",
                       background="#2a1f4a",
                       foreground="white",
                       rowheight=25,
                       fieldbackground="#2a1f4a")
        style.map("Custom.Treeview",
                 background=[('selected', '#1a0869')])

    def setup_ui(self):
        # Botões de navegação
        tk.Button(self, text="Tela inicial", height=2, command=self.TelaInicial, bg="#1a0869", fg="white", font=("Arial", 20)).place(x=20, y=10, width=350, height=75)
        
        tk.Button(self, text="Seleção", height=2, command=self.TelaDeSelecao, bg="#1a0869", fg="white", font=("Arial", 20)).place(x=385, y=10, width=350, height=75)

        tk.Button(self, text="Combate", height=2, command=self.TelaDeCombate, bg="#1a0869", fg="white", font=("Arial", 20)).place(x=870, y=10, width=350, height=75)
        
        tk.Label(self, text="Informações", fg="white", bg="#1a0869", font=("Arial", 20, "bold")).place(x=1235, y=10, width=350, height=75)

        # Seção de seleção de tabela (centralizada)
        tk.Label(self, text="Selecionar Tabela:", fg="white", bg="#130f26",
                font=("Arial", 14, "bold")).place(x=650, y=100)
        
        self.combo_tabelas = ttk.Combobox(self, style="CustomCombobox.TCombobox", values=list(self.templates_tabelas.keys()), state="readonly", font=("Arial", 12))
        self.combo_tabelas.place(x=650, y=130, width=300, height=35)
        self.combo_tabelas.bind('<<ComboboxSelected>>', self.on_tabela_selecionada)

        # Container principal para conteúdo dinâmico (centralizado)
        self.container_conteudo = tk.Frame(self, bg="#130f26")
        self.container_conteudo.place(x=100, y=180, width=1400, height=700)

    def limpar_container(self):
        """Limpa o container de conteúdo"""
        for widget in self.container_conteudo.winfo_children():
            widget.destroy()

    def on_tabela_selecionada(self, event=None):
        """Chamado quando uma tabela é selecionada"""
        self.tabela_atual = self.combo_tabelas.get()
        self.limpar_container()
        
        # Chama o template correspondente
        if self.tabela_atual in self.templates_tabelas:
            self.templates_tabelas[self.tabela_atual]()

    # ==================== TEMPLATES DE TABELAS ==================== #
    # itens #
    def template_itens(self):
        """Template para tabela de Itens"""
        self.limpar_container()

        tk.Label(self.container_conteudo, text="ITENS GENÉRICOS", 
                fg="white", bg="#1a0869", font=("Arial", 18, "bold")
                ).place(x=0, y=0, width=1400, height=50)

        # Frame da Tabela
        tree_frame = tk.Frame(self.container_conteudo, bg="#2a1f4a")
        tree_frame.place(x=0, y=60, width=1400, height=580)

        self.tree_itens = ttk.Treeview(tree_frame, style="Custom.Treeview",
                                    columns=("Nome", "Peso"),
                                    show="headings")
        for col in ("Nome", "Peso"):
            self.tree_itens.heading(col, text=col)
            self.tree_itens.column(col, anchor="center", width=300)
        self.tree_itens.pack(fill="both", expand=True)

        self.carregar_itens_tree()

        # --- Funções internas ---
        def validar_campos(data, editar=False):
            if not data["nome"]:
                messagebox.showwarning("Campo obrigatório", "O campo 'Nome' é obrigatório.")
                return False
            if data["peso"]:
                try:
                    data["peso"] = float(data["peso"])
                except ValueError:
                    messagebox.showwarning("Valor inválido", "O campo 'Peso' deve ser numérico.")
                    return False
            else:
                data["peso"] = None

            if not editar:
                itens = D.carregar_itens()
                if data["nome"] in itens:
                    messagebox.showwarning("Duplicado", f"Já existe um item com o nome '{data['nome']}'.")
                    return False
            return True

        def novo_item():
            popup = tk.Toplevel(self)
            popup.title("Novo Item")
            popup.geometry("400x250")
            popup.config(bg="#1a0869")

            campos = ["Nome", "Peso"]
            entradas = {}
            for i, campo in enumerate(campos):
                tk.Label(popup, text=campo, fg="white", bg="#1a0869",
                        font=("Arial", 12, "bold")).place(x=30, y=30 + i*70)
                entrada = tk.Entry(popup, font=("Arial", 12))
                entrada.place(x=150, y=30 + i*70, width=200)
                entradas[campo] = entrada

            def salvar():
                data = {campo.lower(): entradas[campo].get().strip() for campo in campos}
                if not validar_campos(data):
                    return
                if D.salvar_itens(data):
                    self.carregar_itens_tree()
                    messagebox.showinfo("Sucesso", f"Item '{data['nome']}' criado com sucesso.")
                    popup.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao criar Item.")

            tk.Button(popup, text="Salvar", command=salvar,
                    bg="#0d7377", fg="white", font=("Arial", 14)
                    ).place(x=130, y=160, width=140, height=40)

        def editar_item():
            selected = self.tree_itens.selection()
            if not selected:
                messagebox.showwarning("Nenhum item selecionado", "Selecione um item para editar.")
                return
            item = self.tree_itens.item(selected[0], "values")
            nome_original = item[0]

            popup = tk.Toplevel(self)
            popup.title("Editar Item")
            popup.geometry("400x250")
            popup.config(bg="#1a0869")

            campos = ["Nome", "Peso"]
            entradas = {}
            for i, campo in enumerate(campos):
                tk.Label(popup, text=campo, fg="white", bg="#1a0869",
                        font=("Arial", 12, "bold")).place(x=30, y=30 + i*70)
                entrada = tk.Entry(popup, font=("Arial", 12))
                entrada.place(x=150, y=30 + i*70, width=200)
                entrada.insert(0, item[i])
                entradas[campo] = entrada

            def salvar():
                data = {campo.lower(): entradas[campo].get().strip() for campo in campos}
                if not validar_campos(data, editar=True):
                    return
                if D.editar_itens(nome_original, data):
                    self.carregar_itens_tree()
                    messagebox.showinfo("Sucesso", f"Item '{data['nome']}' atualizado com sucesso.")
                    popup.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao editar Item.")

            tk.Button(popup, text="Salvar", command=salvar,
                    bg="#f39c12", fg="white", font=("Arial", 14)
                    ).place(x=130, y=160, width=140, height=40)

        def remover_item():
            selected = self.tree_itens.selection()
            if not selected:
                messagebox.showwarning("Nenhum item selecionado", "Selecione um item para remover.")
                return
            item = self.tree_itens.item(selected[0], "values")
            nome = item[0]

            confirm = messagebox.askyesno("Confirmar exclusão", f"Tem certeza que deseja remover '{nome}'?")
            if not confirm:
                return

            if D.remover_itens(nome):
                self.carregar_itens_tree()
                messagebox.showinfo("Removido", f"Item '{nome}' foi removido com sucesso.")
            else:
                messagebox.showerror("Erro", f"Erro ao remover Item '{nome}'.")

        # --- Botões ---
        btn_width = 150
        btn_spacing = 150
        total_width = btn_width * 3 + btn_spacing * 2
        start_x = (1000 - total_width) // 2

        tk.Button(self.container_conteudo, text="Novo", bg="#0d7377", fg="white",
                font=("Arial", 14), command=novo_item).place(x=start_x, y=650, width=btn_width, height=40)
        tk.Button(self.container_conteudo, text="Editar", bg="#f39c12", fg="white",
                font=("Arial", 14), command=editar_item).place(x=start_x + btn_spacing, y=650, width=btn_width, height=40)
        tk.Button(self.container_conteudo, text="Remover", bg="#e74c3c", fg="white",
                font=("Arial", 14), command=remover_item).place(x=start_x + btn_spacing * 2, y=650, width=btn_width, height=40)

    def carregar_itens_tree(self):
        """Carrega e exibe todos os itens do banco"""
        if not hasattr(self, "tree_itens"):
            return
        for i in self.tree_itens.get_children():
            self.tree_itens.delete(i)
        try:
            itens = D.carregar_itens()
            for nome, data in itens.items():
                self.tree_itens.insert("", "end", values=(
                    data.get("nome", ""),
                    data.get("peso", "")
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar tabela Itens:\n{e}")
    # itens #

    # municoes #
    def template_municoes(self):
        """Template para tabela de Munições"""
        self.limpar_container()

        tk.Label(self.container_conteudo, text="MUNIÇÕES",
                fg="white", bg="#1a0869", font=("Arial", 18, "bold")
                ).place(x=0, y=0, width=1400, height=50)

        # Frame da Tabela
        tree_frame = tk.Frame(self.container_conteudo, bg="#2a1f4a")
        tree_frame.place(x=0, y=60, width=1400, height=580)

        self.tree_municoes = ttk.Treeview(tree_frame, style="Custom.Treeview",
                                        columns=("Nome", "Calibre", "Dano", "Perfuração"),
                                        show="headings")
        for col in ("Nome", "Calibre", "Dano", "Perfuração"):
            self.tree_municoes.heading(col, text=col)
            self.tree_municoes.column(col, anchor="center", width=200)
        self.tree_municoes.pack(fill="both", expand=True)

        self.carregar_municoes_tree()

        # --- Funções internas ---
        def validar_campos(data, editar=False):
            if not data["nome"]:
                messagebox.showwarning("Campo obrigatório", "O campo 'Nome' é obrigatório.")
                return False

            # Dano
            if data["dano"]:
                try:
                    data["dano"] = int(data["dano"])
                except ValueError:
                    messagebox.showwarning("Valor inválido", "O campo 'Dano' deve ser inteiro.")
                    return False
            else:
                data["dano"] = None

            # Perfuração
            if data["perfuracao"]:
                try:
                    data["perfuracao"] = int(data["perfuracao"])
                except ValueError:
                    messagebox.showwarning("Valor inválido", "O campo 'Perfuração' deve ser inteiro.")
                    return False
            else:
                data["perfuracao"] = None

            # Calibre
            if not data["calibre"]:
                data["calibre"] = None

            if not editar:
                municoes = D.carregar_municoes()
                if data["nome"] in municoes:
                    messagebox.showwarning("Duplicado", f"Já existe uma munição com o nome '{data['nome']}'.")
                    return False

            return True

        def novo_municao():
            popup = tk.Toplevel(self)
            popup.title("Nova Munição")
            popup.geometry("400x350")
            popup.config(bg="#1a0869")

            campos = ["Nome", "Calibre", "Dano", "Perfuração"]
            entradas = {}
            for i, campo in enumerate(campos):
                tk.Label(popup, text=campo, fg="white", bg="#1a0869",
                        font=("Arial", 12, "bold")).place(x=30, y=30 + i*60)
                entrada = tk.Entry(popup, font=("Arial", 12))
                entrada.place(x=150, y=30 + i*60, width=200)
                entradas[campo] = entrada

            def salvar():
                data = {campo.lower().replace(" ", "_"): entradas[campo].get().strip() for campo in campos}
                if not validar_campos(data):
                    return
                if D.salvar_municoes(data):
                    self.carregar_municoes_tree()
                    messagebox.showinfo("Sucesso", f"Munição '{data['nome']}' criada com sucesso.")
                    popup.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao criar Munição.")

            tk.Button(popup, text="Salvar", command=salvar,
                    bg="#0d7377", fg="white", font=("Arial", 14)
                    ).place(x=130, y=280, width=140, height=40)

        def editar_municao():
            selected = self.tree_municoes.selection()
            if not selected:
                messagebox.showwarning("Nenhum item selecionado", "Selecione uma munição para editar.")
                return
            item = self.tree_municoes.item(selected[0], "values")
            nome_original = item[0]

            popup = tk.Toplevel(self)
            popup.title("Editar Munição")
            popup.geometry("400x350")
            popup.config(bg="#1a0869")

            campos = ["Nome", "Calibre", "Dano", "Perfuração"]
            entradas = {}
            for i, campo in enumerate(campos):
                tk.Label(popup, text=campo, fg="white", bg="#1a0869",
                        font=("Arial", 12, "bold")).place(x=30, y=30 + i*60)
                entrada = tk.Entry(popup, font=("Arial", 12))
                entrada.place(x=150, y=30 + i*60, width=200)
                entrada.insert(0, item[i])
                entradas[campo] = entrada

            def salvar():
                data = {campo.lower().replace(" ", "_"): entradas[campo].get().strip() for campo in campos}
                if not validar_campos(data, editar=True):
                    return
                if D.editar_municoes(nome_original, data):
                    self.carregar_municoes_tree()
                    messagebox.showinfo("Sucesso", f"Munição '{data['nome']}' atualizada com sucesso.")
                    popup.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao editar Munição.")

            tk.Button(popup, text="Salvar", command=salvar,
                    bg="#f39c12", fg="white", font=("Arial", 14)
                    ).place(x=130, y=280, width=140, height=40)

        def remover_municao():
            selected = self.tree_municoes.selection()
            if not selected:
                messagebox.showwarning("Nenhum item selecionado", "Selecione uma munição para remover.")
                return
            item = self.tree_municoes.item(selected[0], "values")
            nome = item[0]

            confirm = messagebox.askyesno("Confirmar exclusão", f"Tem certeza que deseja remover '{nome}'?")
            if not confirm:
                return

            if D.remover_municoes(nome):
                self.carregar_municoes_tree()
                messagebox.showinfo("Removido", f"Munição '{nome}' foi removida com sucesso.")
            else:
                messagebox.showerror("Erro", f"Erro ao remover Munição '{nome}'.")

        # --- Botões ---
        btn_width = 150
        btn_spacing = 150
        total_width = btn_width * 3 + btn_spacing * 2
        start_x = (1000 - total_width) // 2

        tk.Button(self.container_conteudo, text="Novo", bg="#0d7377", fg="white",
                font=("Arial", 14), command=novo_municao).place(x=start_x, y=650, width=btn_width, height=40)
        tk.Button(self.container_conteudo, text="Editar", bg="#f39c12", fg="white",
                font=("Arial", 14), command=editar_municao).place(x=start_x + btn_spacing, y=650, width=btn_width, height=40)
        tk.Button(self.container_conteudo, text="Remover", bg="#e74c3c", fg="white",
                font=("Arial", 14), command=remover_municao).place(x=start_x + btn_spacing * 2, y=650, width=btn_width, height=40)

    def carregar_municoes_tree(self):
        """Carrega e exibe todas as munições do banco"""
        if not hasattr(self, "tree_municoes"):
            return
        for i in self.tree_municoes.get_children():
            self.tree_municoes.delete(i)
        try:
            municoes = D.carregar_municoes()
            for nome, data in municoes.items():
                self.tree_municoes.insert("", "end", values=(
                    data.get("nome", ""),
                    data.get("calibre", ""),
                    data.get("dano", ""),
                    data.get("perfuracao", "")
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar tabela Munições:\n{e}")
    # municoes #

    # explosivos #
    def template_explosivos(self):
        """Template para tabela de Explosivos"""
        self.limpar_container()

        tk.Label(self.container_conteudo, text="EXPLOSIVOS",
                fg="white", bg="#1a0869", font=("Arial", 18, "bold")
                ).place(x=0, y=0, width=1400, height=50)

        # Frame da Tabela
        tree_frame = tk.Frame(self.container_conteudo, bg="#2a1f4a")
        tree_frame.place(x=0, y=60, width=1400, height=580)

        self.tree_explosivos = ttk.Treeview(tree_frame, style="Custom.Treeview",
                                            columns=("Nome", "Peso", "Raio", "Dano", "Tipo Dano"),
                                            show="headings")
        for col in ("Nome", "Peso", "Raio", "Dano", "Tipo Dano"):
            self.tree_explosivos.heading(col, text=col)
            self.tree_explosivos.column(col, anchor="center", width=200)
        self.tree_explosivos.pack(fill="both", expand=True)

        self.carregar_explosivos_tree()

        # --- Funções internas ---
        def validar_campos(data, editar=False):
            if not data["nome"]:
                messagebox.showwarning("Campo obrigatório", "O campo 'Nome' é obrigatório.")
                return False

            # Peso
            if data["peso"]:
                try:
                    data["peso"] = float(data["peso"])
                except ValueError:
                    messagebox.showwarning("Valor inválido", "O campo 'Peso' deve ser numérico.")
                    return False
            else:
                data["peso"] = None

            # Raio
            if data["raio"]:
                try:
                    data["raio"] = int(data["raio"])
                except ValueError:
                    messagebox.showwarning("Valor inválido", "O campo 'Raio' deve ser inteiro.")
                    return False
            else:
                data["raio"] = None

            # Dano
            if data["dano"]:
                try:
                    data["dano"] = int(data["dano"])
                except ValueError:
                    messagebox.showwarning("Valor inválido", "O campo 'Dano' deve ser inteiro.")
                    return False
            else:
                data["dano"] = None

            # Tipo de dano
            if not data["tipo_dano"]:
                data["tipo_dano"] = None

            if not editar:
                explosivos = D.carregar_explosivos()
                if data["nome"] in explosivos:
                    messagebox.showwarning("Duplicado", f"Já existe um explosivo com o nome '{data['nome']}'.")
                    return False

            return True

        def novo_explosivo():
            popup = tk.Toplevel(self)
            popup.title("Novo Explosivo")
            popup.geometry("400x400")
            popup.config(bg="#1a0869")

            campos = ["Nome", "Peso", "Raio", "Dano", "Tipo Dano"]
            entradas = {}
            for i, campo in enumerate(campos):
                tk.Label(popup, text=campo, fg="white", bg="#1a0869",
                        font=("Arial", 12, "bold")).place(x=30, y=30 + i*60)
                entrada = tk.Entry(popup, font=("Arial", 12))
                entrada.place(x=150, y=30 + i*60, width=200)
                entradas[campo] = entrada

            def salvar():
                data = {campo.lower().replace(" ", "_"): entradas[campo].get().strip() for campo in campos}
                if not validar_campos(data):
                    return
                if D.salvar_explosivos(data):
                    self.carregar_explosivos_tree()
                    messagebox.showinfo("Sucesso", f"Explosivo '{data['nome']}' criado com sucesso.")
                    popup.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao criar Explosivo.")

            tk.Button(popup, text="Salvar", command=salvar,
                    bg="#0d7377", fg="white", font=("Arial", 14)
                    ).place(x=130, y=320, width=140, height=40)

        def editar_explosivo():
            selected = self.tree_explosivos.selection()
            if not selected:
                messagebox.showwarning("Nenhum item selecionado", "Selecione um explosivo para editar.")
                return
            item = self.tree_explosivos.item(selected[0], "values")
            nome_original = item[0]

            popup = tk.Toplevel(self)
            popup.title("Editar Explosivo")
            popup.geometry("400x400")
            popup.config(bg="#1a0869")

            campos = ["Nome", "Peso", "Raio", "Dano", "Tipo Dano"]
            entradas = {}
            for i, campo in enumerate(campos):
                tk.Label(popup, text=campo, fg="white", bg="#1a0869",
                        font=("Arial", 12, "bold")).place(x=30, y=30 + i*60)
                entrada = tk.Entry(popup, font=("Arial", 12))
                entrada.place(x=150, y=30 + i*60, width=200)
                entrada.insert(0, item[i])
                entradas[campo] = entrada

            def salvar():
                data = {campo.lower().replace(" ", "_"): entradas[campo].get().strip() for campo in campos}
                if not validar_campos(data, editar=True):
                    return
                if D.editar_explosivos(nome_original, data):
                    self.carregar_explosivos_tree()
                    messagebox.showinfo("Sucesso", f"Explosivo '{data['nome']}' atualizado com sucesso.")
                    popup.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao editar Explosivo.")

            tk.Button(popup, text="Salvar", command=salvar,
                    bg="#f39c12", fg="white", font=("Arial", 14)
                    ).place(x=130, y=320, width=140, height=40)

        def remover_explosivo():
            selected = self.tree_explosivos.selection()
            if not selected:
                messagebox.showwarning("Nenhum item selecionado", "Selecione um explosivo para remover.")
                return
            item = self.tree_explosivos.item(selected[0], "values")
            nome = item[0]

            confirm = messagebox.askyesno("Confirmar exclusão", f"Tem certeza que deseja remover '{nome}'?")
            if not confirm:
                return

            if D.remover_explosivos(nome):
                self.carregar_explosivos_tree()
                messagebox.showinfo("Removido", f"Explosivo '{nome}' foi removido com sucesso.")
            else:
                messagebox.showerror("Erro", f"Erro ao remover Explosivo '{nome}'.")

        # --- Botões ---
        btn_width = 150
        btn_spacing = 150
        total_width = btn_width * 3 + btn_spacing * 2
        start_x = (1000 - total_width) // 2

        tk.Button(self.container_conteudo, text="Novo", bg="#0d7377", fg="white",
                font=("Arial", 14), command=novo_explosivo).place(x=start_x, y=650, width=btn_width, height=40)
        tk.Button(self.container_conteudo, text="Editar", bg="#f39c12", fg="white",
                font=("Arial", 14), command=editar_explosivo).place(x=start_x + btn_spacing, y=650, width=btn_width, height=40)
        tk.Button(self.container_conteudo, text="Remover", bg="#e74c3c", fg="white",
                font=("Arial", 14), command=remover_explosivo).place(x=start_x + btn_spacing * 2, y=650, width=btn_width, height=40)

    def carregar_explosivos_tree(self):
        """Carrega e exibe todos os explosivos do banco"""
        if not hasattr(self, "tree_explosivos"):
            return
        for i in self.tree_explosivos.get_children():
            self.tree_explosivos.delete(i)
        try:
            explosivos = D.carregar_explosivos()
            for nome, data in explosivos.items():
                self.tree_explosivos.insert("", "end", values=(
                    data.get("nome", ""),
                    data.get("peso", ""),
                    data.get("raio", ""),
                    data.get("dano", ""),
                    data.get("tipo_dano", "")
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar tabela Explosivos:\n{e}")
    # explosivos #

    # consumiveis #
    def template_consumiveis(self):
        """Template para tabela de Consumíveis"""
        self.limpar_container()

        tk.Label(self.container_conteudo, text="CONSUMÍVEIS",
                fg="white", bg="#1a0869", font=("Arial", 18, "bold")
                ).place(x=0, y=0, width=1400, height=50)

        # Frame da Tabela
        tree_frame = tk.Frame(self.container_conteudo, bg="#2a1f4a")
        tree_frame.place(x=0, y=60, width=1400, height=580)

        self.tree_consumiveis = ttk.Treeview(tree_frame, style="Custom.Treeview",
                                            columns=("Nome", "Peso", "Cura", "Energia"),
                                            show="headings")
        for col in ("Nome", "Peso", "Cura", "Energia"):
            self.tree_consumiveis.heading(col, text=col)
            self.tree_consumiveis.column(col, anchor="center", width=200)
        self.tree_consumiveis.pack(fill="both", expand=True)

        self.carregar_consumiveis_tree()

        # --- Funções internas ---
        def validar_campos(data, editar=False):
            if not data["nome"]:
                messagebox.showwarning("Campo obrigatório", "O campo 'Nome' é obrigatório.")
                return False

            # Peso
            if data["peso"]:
                try:
                    data["peso"] = float(data["peso"])
                except ValueError:
                    messagebox.showwarning("Valor inválido", "O campo 'Peso' deve ser numérico.")
                    return False
            else:
                data["peso"] = None

            # Cura
            if data["cura"]:
                try:
                    data["cura"] = int(data["cura"])
                except ValueError:
                    messagebox.showwarning("Valor inválido", "O campo 'Cura' deve ser inteiro.")
                    return False
            else:
                data["cura"] = None

            # Energia
            if data["energia"]:
                try:
                    data["energia"] = int(data["energia"])
                except ValueError:
                    messagebox.showwarning("Valor inválido", "O campo 'Energia' deve ser inteiro.")
                    return False
            else:
                data["energia"] = None

            if not editar:
                consumiveis = D.carregar_consumiveis()
                if data["nome"] in consumiveis:
                    messagebox.showwarning("Duplicado", f"Já existe um consumível com o nome '{data['nome']}'.")
                    return False

            return True

        def novo_consumivel():
            popup = tk.Toplevel(self)
            popup.title("Novo Consumível")
            popup.geometry("400x350")
            popup.config(bg="#1a0869")

            campos = ["Nome", "Peso", "Cura", "Energia"]
            entradas = {}
            for i, campo in enumerate(campos):
                tk.Label(popup, text=campo, fg="white", bg="#1a0869",
                        font=("Arial", 12, "bold")).place(x=30, y=30 + i*70)
                entrada = tk.Entry(popup, font=("Arial", 12))
                entrada.place(x=150, y=30 + i*70, width=200)
                entradas[campo] = entrada

            def salvar():
                data = {campo.lower(): entradas[campo].get().strip() for campo in campos}
                if not validar_campos(data):
                    return
                if D.salvar_consumiveis(data):
                    self.carregar_consumiveis_tree()
                    messagebox.showinfo("Sucesso", f"Consumível '{data['nome']}' criado com sucesso.")
                    popup.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao criar Consumível.")

            tk.Button(popup, text="Salvar", command=salvar,
                    bg="#0d7377", fg="white", font=("Arial", 14)
                    ).place(x=130, y=260, width=140, height=40)

        def editar_consumivel():
            selected = self.tree_consumiveis.selection()
            if not selected:
                messagebox.showwarning("Nenhum item selecionado", "Selecione um consumível para editar.")
                return
            item = self.tree_consumiveis.item(selected[0], "values")
            nome_original = item[0]

            popup = tk.Toplevel(self)
            popup.title("Editar Consumível")
            popup.geometry("400x350")
            popup.config(bg="#1a0869")

            campos = ["Nome", "Peso", "Cura", "Energia"]
            entradas = {}
            for i, campo in enumerate(campos):
                tk.Label(popup, text=campo, fg="white", bg="#1a0869",
                        font=("Arial", 12, "bold")).place(x=30, y=30 + i*70)
                entrada = tk.Entry(popup, font=("Arial", 12))
                entrada.place(x=150, y=30 + i*70, width=200)
                entrada.insert(0, item[i])
                entradas[campo] = entrada

            def salvar():
                data = {campo.lower(): entradas[campo].get().strip() for campo in campos}
                if not validar_campos(data, editar=True):
                    return
                if D.editar_consumiveis(nome_original, data):
                    self.carregar_consumiveis_tree()
                    messagebox.showinfo("Sucesso", f"Consumível '{data['nome']}' atualizado com sucesso.")
                    popup.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao editar Consumível.")

            tk.Button(popup, text="Salvar", command=salvar,
                    bg="#f39c12", fg="white", font=("Arial", 14)
                    ).place(x=130, y=260, width=140, height=40)

        def remover_consumivel():
            selected = self.tree_consumiveis.selection()
            if not selected:
                messagebox.showwarning("Nenhum item selecionado", "Selecione um consumível para remover.")
                return
            item = self.tree_consumiveis.item(selected[0], "values")
            nome = item[0]

            confirm = messagebox.askyesno("Confirmar exclusão", f"Tem certeza que deseja remover '{nome}'?")
            if not confirm:
                return

            if D.remover_consumiveis(nome):
                self.carregar_consumiveis_tree()
                messagebox.showinfo("Removido", f"Consumível '{nome}' foi removido com sucesso.")
            else:
                messagebox.showerror("Erro", f"Erro ao remover Consumível '{nome}'.")

        # --- Botões ---
        btn_width = 150
        btn_spacing = 150
        total_width = btn_width * 3 + btn_spacing * 2
        start_x = (1000 - total_width) // 2

        tk.Button(self.container_conteudo, text="Novo", bg="#0d7377", fg="white",
                font=("Arial", 14), command=novo_consumivel).place(x=start_x, y=650, width=btn_width, height=40)
        tk.Button(self.container_conteudo, text="Editar", bg="#f39c12", fg="white",
                font=("Arial", 14), command=editar_consumivel).place(x=start_x + btn_spacing, y=650, width=btn_width, height=40)
        tk.Button(self.container_conteudo, text="Remover", bg="#e74c3c", fg="white",
                font=("Arial", 14), command=remover_consumivel).place(x=start_x + btn_spacing * 2, y=650, width=btn_width, height=40)

    def carregar_consumiveis_tree(self):
        """Carrega e exibe todos os consumíveis do banco"""
        if not hasattr(self, "tree_consumiveis"):
            return
        for i in self.tree_consumiveis.get_children():
            self.tree_consumiveis.delete(i)
        try:
            consumiveis = D.carregar_consumiveis()
            for nome, data in consumiveis.items():
                self.tree_consumiveis.insert("", "end", values=(
                    data.get("nome", ""),
                    data.get("peso", ""),
                    data.get("cura", ""),
                    data.get("energia", "")
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar tabela Consumíveis:\n{e}")
    # consumiveis #

    # melhorias #
    def template_melhorias(self):
        """Template para tabela de Melhorias"""
        self.limpar_container()

        tk.Label(self.container_conteudo, text="MELHORIAS",
                fg="white", bg="#1a0869", font=("Arial", 18, "bold")
                ).place(x=0, y=0, width=1400, height=50)

        tree_frame = tk.Frame(self.container_conteudo, bg="#2a1f4a")
        tree_frame.place(x=0, y=60, width=1400, height=580)

        self.tree_melhorias = ttk.Treeview(tree_frame, style="Custom.Treeview",
                                        columns=("Nome", "Peso", "Tipo", "Modificadores"),
                                        show="headings")
        for col in ("Nome", "Peso", "Tipo", "Modificadores"):
            self.tree_melhorias.heading(col, text=col)
            self.tree_melhorias.column(col, anchor="center", width=200)
        self.tree_melhorias.pack(fill="both", expand=True)

        self.carregar_melhorias_tree()

        # --- Funções internas ---
        def validar_campos(data, editar=False):
            if not data["nome"]:
                messagebox.showwarning("Campo obrigatório", "O campo 'Nome' é obrigatório.")
                return False

            if data["peso"]:
                try:
                    data["peso"] = float(data["peso"])
                except ValueError:
                    messagebox.showwarning("Valor inválido", "O campo 'Peso' deve ser numérico.")
                    return False
            else:
                data["peso"] = None

            if not data["tipo"]:
                data["tipo"] = None
            if not data["modificadores"]:
                data["modificadores"] = None

            if not editar:
                melhorias = D.carregar_melhorias()
                if data["nome"] in melhorias:
                    messagebox.showwarning("Duplicado", f"Já existe uma melhoria com o nome '{data['nome']}'.")
                    return False

            return True

        def novo_melhoria():
            popup = tk.Toplevel(self)
            popup.title("Nova Melhoria")
            popup.geometry("400x400")
            popup.config(bg="#1a0869")

            campos = ["Nome", "Peso", "Tipo", "Modificadores"]
            entradas = {}
            for i, campo in enumerate(campos):
                tk.Label(popup, text=campo, fg="white", bg="#1a0869",
                        font=("Arial", 12, "bold")).place(x=30, y=30 + i*60)
                entrada = tk.Entry(popup, font=("Arial", 12))
                entrada.place(x=150, y=30 + i*60, width=200)
                entradas[campo] = entrada

            def salvar():
                data = {campo.lower().replace(" ", "_"): entradas[campo].get().strip() for campo in campos}
                if not validar_campos(data):
                    return
                if D.salvar_melhoria(data):
                    self.carregar_melhorias_tree()
                    messagebox.showinfo("Sucesso", f"Melhoria '{data['nome']}' criada com sucesso.")
                    popup.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao criar Melhoria.")

            tk.Button(popup, text="Salvar", command=salvar,
                    bg="#0d7377", fg="white", font=("Arial", 14)
                    ).place(x=130, y=320, width=140, height=40)

        def editar_melhoria():
            selected = self.tree_melhorias.selection()
            if not selected:
                messagebox.showwarning("Nenhum item selecionado", "Selecione uma melhoria para editar.")
                return
            item = self.tree_melhorias.item(selected[0], "values")
            nome_original = item[0]

            popup = tk.Toplevel(self)
            popup.title("Editar Melhoria")
            popup.geometry("400x400")
            popup.config(bg="#1a0869")

            campos = ["Nome", "Peso", "Tipo", "Modificadores"]
            entradas = {}
            for i, campo in enumerate(campos):
                tk.Label(popup, text=campo, fg="white", bg="#1a0869",
                        font=("Arial", 12, "bold")).place(x=30, y=30 + i*60)
                entrada = tk.Entry(popup, font=("Arial", 12))
                entrada.place(x=150, y=30 + i*60, width=200)
                entrada.insert(0, item[i])
                entradas[campo] = entrada

            def salvar():
                data = {campo.lower().replace(" ", "_"): entradas[campo].get().strip() for campo in campos}
                if not validar_campos(data, editar=True):
                    return
                if D.editar_melhoria(nome_original, data):
                    self.carregar_melhorias_tree()
                    messagebox.showinfo("Sucesso", f"Melhoria '{data['nome']}' atualizada com sucesso.")
                    popup.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao editar Melhoria.")

            tk.Button(popup, text="Salvar", command=salvar,
                    bg="#f39c12", fg="white", font=("Arial", 14)
                    ).place(x=130, y=320, width=140, height=40)

        def remover_melhoria():
            selected = self.tree_melhorias.selection()
            if not selected:
                messagebox.showwarning("Nenhum item selecionado", "Selecione uma melhoria para remover.")
                return
            item = self.tree_melhorias.item(selected[0], "values")
            nome = item[0]

            confirm = messagebox.askyesno("Confirmar exclusão", f"Tem certeza que deseja remover '{nome}'?")
            if not confirm:
                return

            if D.remover_melhoria(nome):
                self.carregar_melhorias_tree()
                messagebox.showinfo("Removido", f"Melhoria '{nome}' foi removida com sucesso.")
            else:
                messagebox.showerror("Erro", f"Erro ao remover Melhoria '{nome}'.")

        # --- Botões ---
        btn_width = 150
        btn_spacing = 150
        total_width = btn_width * 3 + btn_spacing * 2
        start_x = (1000 - total_width) // 2

        tk.Button(self.container_conteudo, text="Novo", bg="#0d7377", fg="white",
                font=("Arial", 14), command=novo_melhoria).place(x=start_x, y=650, width=btn_width, height=40)
        tk.Button(self.container_conteudo, text="Editar", bg="#f39c12", fg="white",
                font=("Arial", 14), command=editar_melhoria).place(x=start_x + btn_spacing, y=650, width=btn_width, height=40)
        tk.Button(self.container_conteudo, text="Remover", bg="#e74c3c", fg="white",
                font=("Arial", 14), command=remover_melhoria).place(x=start_x + btn_spacing * 2, y=650, width=btn_width, height=40)

    def carregar_melhorias_tree(self):
        """Carrega e exibe todas as melhorias do banco"""
        if not hasattr(self, "tree_melhorias"):
            return
        for i in self.tree_melhorias.get_children():
            self.tree_melhorias.delete(i)
        try:
            melhorias = D.carregar_melhorias()
            for nome, data in melhorias.items():
                self.tree_melhorias.insert("", "end", values=(
                    data.get("nome", ""),
                    data.get("peso", ""),
                    data.get("tipo", ""),
                    data.get("modificadores", "")
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar tabela Melhorias:\n{e}")
    # melhorias #
    
    # Ranged #
    def template_ranged(self):
        """Template para tabela de Armas de Fogo"""
        self.limpar_container()

        tk.Label(self.container_conteudo, text="ARMAS DE FOGO",
                fg="white", bg="#1a0869", font=("Arial", 18, "bold")
                ).place(x=0, y=0, width=1400, height=50)

        tree_frame = tk.Frame(self.container_conteudo, bg="#2a1f4a")
        tree_frame.place(x=0, y=60, width=1400, height=580)

        self.tree_ranged = ttk.Treeview(tree_frame, style="Custom.Treeview",
                                        columns=("Nome", "Peso", "Classe", "Ação", "Raridade", "Calibre", "Capacidade"),
                                        show="headings")
        for col in ("Nome", "Peso", "Classe", "Ação", "Raridade", "Calibre", "Capacidade"):
            self.tree_ranged.heading(col, text=col)
            self.tree_ranged.column(col, anchor="center", width=180)
        self.tree_ranged.pack(fill="both", expand=True)

        self.carregar_ranged_tree()

        # --- Funções internas ---
        def validar_campos(data, editar=False):
            if not data["nome"]:
                messagebox.showwarning("Campo obrigatório", "O campo 'Nome' é obrigatório.")
                return False

            if data["peso"]:
                try:
                    data["peso"] = float(data["peso"])
                except ValueError:
                    messagebox.showwarning("Valor inválido", "O campo 'Peso' deve ser numérico.")
                    return False
            else:
                data["peso"] = None

            # Campos opcionais
            for campo in ["classe", "acao", "raridade", "calibre", "capacidade"]:
                if not data[campo]:
                    data[campo] = None

            if not editar:
                rangeds = D.carregar_rangeds()
                if data["nome"] in rangeds:
                    messagebox.showwarning("Duplicado", f"Já existe uma arma de fogo com o nome '{data['nome']}'.")
                    return False

            return True

        def novo_ranged():
            popup = tk.Toplevel(self)
            popup.title("Nova Arma de Fogo")
            popup.geometry("450x450")
            popup.config(bg="#1a0869")

            campos = ["Nome", "Peso", "Classe", "Ação", "Raridade", "Calibre", "Capacidade"]
            entradas = {}
            for i, campo in enumerate(campos):
                tk.Label(popup, text=campo, fg="white", bg="#1a0869",
                        font=("Arial", 12, "bold")).place(x=30, y=30 + i*50)
                entrada = tk.Entry(popup, font=("Arial", 12))
                entrada.place(x=150, y=30 + i*50, width=250)
                entradas[campo] = entrada

            def salvar():
                data = {campo.lower().replace(" ", "_"): entradas[campo].get().strip() for campo in campos}
                if not validar_campos(data):
                    return
                if D.salvar_ranged(data):
                    self.carregar_ranged_tree()
                    messagebox.showinfo("Sucesso", f"Arma '{data['nome']}' criada com sucesso.")
                    popup.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao criar Arma de Fogo.")

            tk.Button(popup, text="Salvar", command=salvar,
                    bg="#0d7377", fg="white", font=("Arial", 14)
                    ).place(x=150, y=370, width=140, height=40)

        def editar_ranged():
            selected = self.tree_ranged.selection()
            if not selected:
                messagebox.showwarning("Nenhum item selecionado", "Selecione uma arma para editar.")
                return
            item = self.tree_ranged.item(selected[0], "values")
            nome_original = item[0]

            popup = tk.Toplevel(self)
            popup.title("Editar Arma de Fogo")
            popup.geometry("450x450")
            popup.config(bg="#1a0869")

            campos = ["Nome", "Peso", "Classe", "Ação", "Raridade", "Calibre", "Capacidade"]
            entradas = {}
            for i, campo in enumerate(campos):
                tk.Label(popup, text=campo, fg="white", bg="#1a0869",
                        font=("Arial", 12, "bold")).place(x=30, y=30 + i*50)
                entrada = tk.Entry(popup, font=("Arial", 12))
                entrada.place(x=150, y=30 + i*50, width=250)
                entrada.insert(0, item[i])
                entradas[campo] = entrada

            def salvar():
                data = {campo.lower().replace(" ", "_"): entradas[campo].get().strip() for campo in campos}
                if not validar_campos(data, editar=True):
                    return
                if D.editar_ranged(nome_original, data):
                    self.carregar_ranged_tree()
                    messagebox.showinfo("Sucesso", f"Arma '{data['nome']}' atualizada com sucesso.")
                    popup.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao editar Arma de Fogo.")

            tk.Button(popup, text="Salvar", command=salvar,
                    bg="#f39c12", fg="white", font=("Arial", 14)
                    ).place(x=150, y=370, width=140, height=40)

        def remover_ranged():
            selected = self.tree_ranged.selection()
            if not selected:
                messagebox.showwarning("Nenhum item selecionado", "Selecione uma arma para remover.")
                return
            item = self.tree_ranged.item(selected[0], "values")
            nome = item[0]

            confirm = messagebox.askyesno("Confirmar exclusão", f"Tem certeza que deseja remover '{nome}'?")
            if not confirm:
                return

            if D.remover_ranged(nome):
                self.carregar_ranged_tree()
                messagebox.showinfo("Removido", f"Arma '{nome}' foi removida com sucesso.")
            else:
                messagebox.showerror("Erro", f"Erro ao remover Arma '{nome}'.")

        # --- Botões ---
        btn_width = 150
        btn_spacing = 150
        total_width = btn_width * 3 + btn_spacing * 2
        start_x = (1000 - total_width) // 2

        tk.Button(self.container_conteudo, text="Novo", bg="#0d7377", fg="white",
                font=("Arial", 14), command=novo_ranged).place(x=start_x, y=650, width=btn_width, height=40)
        tk.Button(self.container_conteudo, text="Editar", bg="#f39c12", fg="white",
                font=("Arial", 14), command=editar_ranged).place(x=start_x + btn_spacing, y=650, width=btn_width, height=40)
        tk.Button(self.container_conteudo, text="Remover", bg="#e74c3c", fg="white",
                font=("Arial", 14), command=remover_ranged).place(x=start_x + btn_spacing * 2, y=650, width=btn_width, height=40)

    def carregar_ranged_tree(self):
        """Carrega e exibe todas as armas de fogo do banco"""
        if not hasattr(self, "tree_ranged"):
            return
        for i in self.tree_ranged.get_children():
            self.tree_ranged.delete(i)
        try:
            rangeds = D.carregar_rangeds()
            for nome, data in rangeds.items():
                self.tree_ranged.insert("", "end", values=(
                    data.get("nome", ""),
                    data.get("peso", ""),
                    data.get("classe", ""),
                    data.get("acao", ""),
                    data.get("raridade", ""),
                    data.get("calibre", ""),
                    data.get("capacidade", "")
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar tabela Armas de Fogo:\n{e}")
    # Ranged #

    # Melees #
    def template_melee(self):
        """Template para tabela de Armas Corpo a Corpo"""
        self.limpar_container()

        tk.Label(self.container_conteudo, text="ARMAS CORPO A CORPO", 
                 fg="white", bg="#1a0869", font=("Arial", 18, "bold")
                 ).place(x=0, y=0, width=1400, height=50)

        # Frame da Tabela
        tree_frame = tk.Frame(self.container_conteudo, bg="#2a1f4a")
        tree_frame.place(x=0, y=60, width=1400, height=580)

        self.tree_melee = ttk.Treeview(tree_frame, style="Custom.Treeview",
                                       columns=("Nome", "Peso", "Classe", "Tipo Dano", "Raridade"),
                                       show="headings")
        for col in ("Nome", "Peso", "Classe", "Tipo Dano", "Raridade"):
            self.tree_melee.heading(col, text=col)
            self.tree_melee.column(col, anchor="center", width=200)
        self.tree_melee.pack(fill="both", expand=True)

        self.carregar_melees_tree()

        # --- Funções internas ---
        def validar_campos(data, editar=False):
            """Valida campos antes de salvar"""
            if not data["nome"]:
                messagebox.showwarning("Campo obrigatório", "O campo 'Nome' é obrigatório.")
                return False

            if data["peso"]:
                try:
                    data["peso"] = float(data["peso"])
                except ValueError:
                    messagebox.showwarning("Valor inválido", "O campo 'Peso' deve ser numérico.")
                    return False
            else:
                data["peso"] = None

            if not editar:
                melees = D.carregar_melees()
                if data["nome"] in melees:
                    messagebox.showwarning("Duplicado", f"Já existe um melee com o nome '{data['nome']}'.")
                    return False

            return True

        def novo_melee():
            popup = tk.Toplevel(self)
            popup.title("Novo Melee")
            popup.geometry("400x400")
            popup.config(bg="#1a0869")

            campos = ["Nome", "Peso", "Classe", "Tipo Dano", "Raridade"]
            entradas = {}

            for i, campo in enumerate(campos):
                tk.Label(popup, text=campo, fg="white", bg="#1a0869",
                         font=("Arial", 12, "bold")).place(x=30, y=30 + i*50)
                entrada = tk.Entry(popup, font=("Arial", 12))
                entrada.place(x=150, y=30 + i*50, width=200)
                entradas[campo] = entrada

            def salvar():
                data = {campo.lower().replace(" ", "_"): entradas[campo].get().strip() for campo in campos}
                if not validar_campos(data):
                    return

                if D.inserir_melee(data):
                    self.carregar_melees_tree()
                    messagebox.showinfo("Sucesso", f"Melee '{data['nome']}' criado com sucesso.")
                    popup.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao criar Melee.")

            tk.Button(popup, text="Salvar", command=salvar,
                      bg="#0d7377", fg="white", font=("Arial", 14)
                      ).place(x=130, y=320, width=140, height=40)

        def editar_melee():
            selected = self.tree_melee.selection()
            if not selected:
                messagebox.showwarning("Nenhum item selecionado", "Selecione um melee para editar.")
                return
            item = self.tree_melee.item(selected[0], "values")
            nome_original = item[0]

            popup = tk.Toplevel(self)
            popup.title("Editar Melee")
            popup.geometry("400x400")
            popup.config(bg="#1a0869")

            campos = ["Nome", "Peso", "Classe", "Tipo Dano", "Raridade"]
            entradas = {}

            for i, campo in enumerate(campos):
                tk.Label(popup, text=campo, fg="white", bg="#1a0869",
                         font=("Arial", 12, "bold")).place(x=30, y=30 + i*50)
                entrada = tk.Entry(popup, font=("Arial", 12))
                entrada.place(x=150, y=30 + i*50, width=200)
                entrada.insert(0, item[i])
                entradas[campo] = entrada

            def salvar():
                data = {campo.lower().replace(" ", "_"): entradas[campo].get().strip() for campo in campos}
                if not validar_campos(data, editar=True):
                    return

                if D.editar_melee(nome_original, data):
                    self.carregar_melees_tree()
                    messagebox.showinfo("Sucesso", f"Melee '{data['nome']}' atualizado com sucesso.")
                    popup.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao editar Melee.")

            tk.Button(popup, text="Salvar", command=salvar,
                      bg="#f39c12", fg="white", font=("Arial", 14)
                      ).place(x=130, y=320, width=140, height=40)

        def remover_melee():
            selected = self.tree_melee.selection()
            if not selected:
                messagebox.showwarning("Nenhum item selecionado", "Selecione um melee para remover.")
                return
            item = self.tree_melee.item(selected[0], "values")
            nome = item[0]

            confirm = messagebox.askyesno("Confirmar exclusão", f"Tem certeza que deseja remover '{nome}'?")
            if not confirm:
                return

            if D.remover_melee(nome):
                self.carregar_melees_tree()
                messagebox.showinfo("Removido", f"Melee '{nome}' foi removido com sucesso.")
            else:
                messagebox.showerror("Erro", f"Erro ao remover Melee '{nome}'.")

        # --- Botões ---
        btn_width = 150
        btn_spacing = 150
        total_width = btn_width * 3 + btn_spacing * 2
        start_x = (1000 - total_width) // 2

        tk.Button(self.container_conteudo, text="Novo", bg="#0d7377", fg="white",
                  font=("Arial", 14), command=novo_melee).place(x=start_x, y=650, width=btn_width, height=40)

        tk.Button(self.container_conteudo, text="Editar", bg="#f39c12", fg="white",
                  font=("Arial", 14), command=editar_melee).place(x=start_x + btn_spacing, y=650, width=btn_width, height=40)

        tk.Button(self.container_conteudo, text="Remover", bg="#e74c3c", fg="white",
                  font=("Arial", 14), command=remover_melee).place(x=start_x + btn_spacing * 2, y=650, width=btn_width, height=40)
    
    def carregar_melees_tree(self):
        """Carrega e exibe todas as armas melee do banco"""
        if not hasattr(self, "tree_melee"):
            return

        for i in self.tree_melee.get_children():
            self.tree_melee.delete(i)

        try:
            melees = D.carregar_melees()
            for nome, data in melees.items():
                self.tree_melee.insert("", "end", values=(
                    data.get("nome", ""),
                    data.get("peso", ""),
                    data.get("classe", ""),
                    data.get("tipo_dano", ""),
                    data.get("raridade", "")
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar tabela Melee:\n{e}")
    # Melees #
    
    # protecao #
    def template_protecao(self):
        """Template para tabela de Proteções"""
        self.limpar_container()

        tk.Label(self.container_conteudo, text="PROTEÇÕES",
                fg="white", bg="#1a0869", font=("Arial", 18, "bold")
                ).place(x=0, y=0, width=1400, height=50)

        tree_frame = tk.Frame(self.container_conteudo, bg="#2a1f4a")
        tree_frame.place(x=0, y=60, width=1400, height=580)

        self.tree_protecao = ttk.Treeview(tree_frame, style="Custom.Treeview",
                                        columns=("Nome", "Peso", "Nível Balístico", "Abs. Física", "Abs. Balística", "Região"),
                                        show="headings")
        for col in ("Nome", "Peso", "Nível Balístico", "Abs. Física", "Abs. Balística", "Região"):
            self.tree_protecao.heading(col, text=col)
            self.tree_protecao.column(col, anchor="center", width=180)
        self.tree_protecao.pack(fill="both", expand=True)

        self.carregar_protecao_tree()

        # --- Funções internas ---
        def validar_campos(data, editar=False):
            if not data["nome"]:
                messagebox.showwarning("Campo obrigatório", "O campo 'Nome' é obrigatório.")
                return False

            # Conversão de valores numéricos
            for campo in ["peso", "nivel_balistico", "absorcao_fisica", "absorcao_balistica"]:
                if data[campo]:
                    try:
                        data[campo] = float(data[campo])
                    except ValueError:
                        messagebox.showwarning("Valor inválido", f"O campo '{campo}' deve ser numérico.")
                        return False
                else:
                    data[campo] = None

            if not data["regiao"]:
                data["regiao"] = None

            if not editar:
                protecoes = D.carregar_protecoes()
                if data["nome"] in protecoes:
                    messagebox.showwarning("Duplicado", f"Já existe uma proteção com o nome '{data['nome']}'.")
                    return False

            return True

        def novo_protecao():
            popup = tk.Toplevel(self)
            popup.title("Nova Proteção")
            popup.geometry("450x450")
            popup.config(bg="#1a0869")

            campos = ["Nome", "Peso", "Nível Balístico", "Abs. Física", "Abs. Balística", "Região"]
            entradas = {}
            for i, campo in enumerate(campos):
                tk.Label(popup, text=campo, fg="white", bg="#1a0869",
                        font=("Arial", 12, "bold")).place(x=30, y=30 + i*50)
                entrada = tk.Entry(popup, font=("Arial", 12))
                entrada.place(x=180, y=30 + i*50, width=200)
                entradas[campo] = entrada

            def salvar():
                data = {
                    "nome": entradas["Nome"].get().strip(),
                    "peso": entradas["Peso"].get().strip(),
                    "nivel_balistico": entradas["Nível Balístico"].get().strip(),
                    "absorcao_fisica": entradas["Abs. Física"].get().strip(),
                    "absorcao_balistica": entradas["Abs. Balística"].get().strip(),
                    "regiao": entradas["Região"].get().strip()
                }
                if not validar_campos(data):
                    return
                if D.salvar_protecao(data):
                    self.carregar_protecao_tree()
                    messagebox.showinfo("Sucesso", f"Proteção '{data['nome']}' criada com sucesso.")
                    popup.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao criar Proteção.")

            tk.Button(popup, text="Salvar", command=salvar,
                    bg="#0d7377", fg="white", font=("Arial", 14)
                    ).place(x=150, y=370, width=140, height=40)

        def editar_protecao():
            selected = self.tree_protecao.selection()
            if not selected:
                messagebox.showwarning("Nenhum item selecionado", "Selecione uma proteção para editar.")
                return
            item = self.tree_protecao.item(selected[0], "values")
            nome_original = item[0]

            popup = tk.Toplevel(self)
            popup.title("Editar Proteção")
            popup.geometry("450x450")
            popup.config(bg="#1a0869")

            campos = ["Nome", "Peso", "Nível Balístico", "Abs. Física", "Abs. Balística", "Região"]
            entradas = {}
            for i, campo in enumerate(campos):
                tk.Label(popup, text=campo, fg="white", bg="#1a0869",
                        font=("Arial", 12, "bold")).place(x=30, y=30 + i*50)
                entrada = tk.Entry(popup, font=("Arial", 12))
                entrada.place(x=180, y=30 + i*50, width=200)
                entrada.insert(0, item[i])
                entradas[campo] = entrada

            def salvar():
                data = {
                    "nome": entradas["Nome"].get().strip(),
                    "peso": entradas["Peso"].get().strip(),
                    "nivel_balistico": entradas["Nível Balístico"].get().strip(),
                    "absorcao_fisica": entradas["Abs. Física"].get().strip(),
                    "absorcao_balistica": entradas["Abs. Balística"].get().strip(),
                    "regiao": entradas["Região"].get().strip()
                }
                if not validar_campos(data, editar=True):
                    return
                if D.editar_protecao(nome_original, data):
                    self.carregar_protecao_tree()
                    messagebox.showinfo("Sucesso", f"Proteção '{data['nome']}' atualizada com sucesso.")
                    popup.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao editar Proteção.")

            tk.Button(popup, text="Salvar", command=salvar,
                    bg="#f39c12", fg="white", font=("Arial", 14)
                    ).place(x=150, y=370, width=140, height=40)

        def remover_protecao():
            selected = self.tree_protecao.selection()
            if not selected:
                messagebox.showwarning("Nenhum item selecionado", "Selecione uma proteção para remover.")
                return
            item = self.tree_protecao.item(selected[0], "values")
            nome = item[0]

            confirm = messagebox.askyesno("Confirmar exclusão", f"Tem certeza que deseja remover '{nome}'?")
            if not confirm:
                return

            if D.remover_protecao(nome):
                self.carregar_protecao_tree()
                messagebox.showinfo("Removido", f"Proteção '{nome}' foi removida com sucesso.")
            else:
                messagebox.showerror("Erro", f"Erro ao remover Proteção '{nome}'.")

        # --- Botões ---
        btn_width = 150
        btn_spacing = 150
        total_width = btn_width * 3 + btn_spacing * 2
        start_x = (1000 - total_width) // 2

        tk.Button(self.container_conteudo, text="Novo", bg="#0d7377", fg="white",
                font=("Arial", 14), command=novo_protecao).place(x=start_x, y=650, width=btn_width, height=40)
        tk.Button(self.container_conteudo, text="Editar", bg="#f39c12", fg="white",
                font=("Arial", 14), command=editar_protecao).place(x=start_x + btn_spacing, y=650, width=btn_width, height=40)
        tk.Button(self.container_conteudo, text="Remover", bg="#e74c3c", fg="white",
                font=("Arial", 14), command=remover_protecao).place(x=start_x + btn_spacing * 2, y=650, width=btn_width, height=40)

    def carregar_protecao_tree(self):
        """Carrega e exibe todas as proteções do banco"""
        if not hasattr(self, "tree_protecao"):
            return
        for i in self.tree_protecao.get_children():
            self.tree_protecao.delete(i)
        try:
            protecoes = D.carregar_protecoes()
            for nome, data in protecoes.items():
                self.tree_protecao.insert("", "end", values=(
                    data.get("nome", ""),
                    data.get("peso", ""),
                    data.get("nivel_balistico", ""),
                    data.get("absorcao_fisica", ""),
                    data.get("absorcao_balistica", ""),
                    data.get("regiao", "")
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar tabela Proteções:\n{e}")
    # protecao #

    # npcs - não tá pronto #
    def template_npcs(self):
        """Template para tabela de NPCs"""
        tk.Label(self.container_conteudo, text="NPCs", 
                fg="white", bg="#1a0869", font=("Arial", 18, "bold")).place(x=0, y=0, width=1400, height=50)
        
        tree_frame = tk.Frame(self.container_conteudo, bg="#2a1f4a")
        tree_frame.place(x=0, y=60, width=1400, height=580)
        
        tree = ttk.Treeview(tree_frame, style="Custom.Treeview", columns=("Grupo", "Classe", "FOR", "AGI", "VIG", "INT", "TAT", "PRE"), show="headings")
        for col in ("Grupo", "Classe", "FOR", "AGI", "VIG", "INT", "TAT", "PRE"):
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True)
        
        # Botões centralizados
        btn_width = 150
        btn_spacing = 150
        total_width = btn_width * 3 + btn_spacing * 2
        start_x = (1000 - total_width) // 2
        
        tk.Button(self.container_conteudo, text="Novo", bg="#0d7377", fg="white", 
                 font=("Arial", 14)).place(x=start_x, y=650, width=btn_width, height=40)
        tk.Button(self.container_conteudo, text="Editar", bg="#f39c12", fg="white", 
                 font=("Arial", 14)).place(x=start_x + btn_spacing, y=650, width=btn_width, height=40)
        tk.Button(self.container_conteudo, text="Remover", bg="#e74c3c", fg="white", 
                 font=("Arial", 14)).place(x=start_x + btn_spacing * 2, y=650, width=btn_width, height=40)
    # npcs - não tá pronto #
    
    # kits #
    def template_kits(self):
        """Template para tabela de Kits com integração ao banco de dados"""
        tk.Label(self.container_conteudo, text="KITS", fg="white", bg="#1a0869", 
                font=("Arial", 18, "bold")).place(x=0, y=0, width=1400, height=50)
        
        # Frame para a Treeview
        tree_frame = tk.Frame(self.container_conteudo, bg="#2a1f4a")
        tree_frame.place(x=0, y=60, width=1400, height=530)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Treeview para lista de kits
        self.tree_kits = ttk.Treeview(tree_frame, style="Custom.Treeview", 
                                    columns=("Nome", "Raridade", "Conteúdo"), 
                                    show="headings", yscrollcommand=scrollbar.set)
        
        self.tree_kits.heading("Nome", text="Nome do Kit")
        self.tree_kits.heading("Raridade", text="Raridade")
        self.tree_kits.heading("Conteúdo", text="Conteúdo")
        
        # Larguras das colunas
        self.tree_kits.column("Nome", width=250, anchor="w")
        self.tree_kits.column("Raridade", width=150, anchor="center")
        self.tree_kits.column("Conteúdo", width=950, anchor="w")
        
        scrollbar.config(command=self.tree_kits.yview)
        self.tree_kits.pack(fill="both", expand=True)
        
        # Carrega os kits do banco
        self.carregar_kits_na_tree()
        
        # Botões de ação
        btn_width = 150
        btn_spacing = 20
        total_width = btn_width * 3 + btn_spacing * 2
        start_x = (1400 - total_width) // 2
        
        tk.Button(self.container_conteudo, text="Novo Kit", bg="#0d7377", fg="white", 
                font=("Arial", 14), command=self.novo_kit).place(
                x=start_x, y=600, width=btn_width, height=40)
        
        tk.Button(self.container_conteudo, text="Editar Kit", bg="#f39c12", fg="white", 
                font=("Arial", 14), command=self.editar_kit).place(
                x=start_x + btn_width + btn_spacing, y=600, width=btn_width, height=40)
        
        tk.Button(self.container_conteudo, text="Remover Kit", bg="#e74c3c", fg="white", 
                font=("Arial", 14), command=self.remover_kit).place(
                x=start_x + (btn_width + btn_spacing) * 2, y=600, width=btn_width, height=40)
        
        # Botão de atualizar
        tk.Button(self.container_conteudo, text="🔄 Atualizar", bg="#3498db", fg="white", 
                font=("Arial", 12), command=self.carregar_kits_na_tree).place(
                x=1250, y=605, width=120, height=30)

    def carregar_kits_na_tree(self):
        """Carrega os kits do banco de dados e exibe na Treeview"""
        # Limpa a tree
        for item in self.tree_kits.get_children():
            self.tree_kits.delete(item)
        
        try:
            # Importa as funções necessárias do módulo Dados
            from Dados import KitsDisponíveis, carregar_kits_db
            
            # Recarrega os kits do banco
            kits = carregar_kits_db()
            
            # Popula a tree
            for nome_kit, kit in kits.items():
                raridade = kit.raridade
                
                # Monta a string de conteúdo
                conteudo_str = self.montar_string_conteudo(kit)
                
                self.tree_kits.insert("", "end", values=(nome_kit, raridade, conteudo_str))
            
            print(f"✅ {len(kits)} kits carregados na interface")
            
        except Exception as e:
            print(f"❌ Erro ao carregar kits: {e}")
            import traceback
            traceback.print_exc()

    def carregar_itens_kit_na_tree(self, tree, kit):
        """Carrega os itens do kit na Treeview"""
        # Limpa a tree
        for item in tree.get_children():
            tree.delete(item)
        
        try:
            if not hasattr(kit, 'inventario') or not kit.inventario:
                return
            
            inventario = kit.inventario
            
            # Verifica se tem o método listar_itens
            if hasattr(inventario, 'listar_itens'):
                itens = inventario.listar_itens()
                
                for item_info in itens:
                    if isinstance(item_info, dict):
                        nome = item_info.get('nome', 'Item Desconhecido')
                        qtd = item_info.get('quantidade', 1)
                        tree.insert("", "end", values=(nome, qtd))
                    else:
                        # Fallback para formato alternativo
                        nome = str(item_info)
                        tree.insert("", "end", values=(nome, 1))
            
            # Fallback: acesso direto aos itens
            elif hasattr(inventario, 'itens') and inventario.itens:
                for item_container in inventario.itens:
                    # Verifica se é ItemInventario (com quantidade)
                    if hasattr(item_container, 'item') and hasattr(item_container, 'quantidade'):
                        item_obj = item_container.item
                        qtd = item_container.quantidade
                        nome = getattr(item_obj, 'nome', 'Item Desconhecido')
                        tree.insert("", "end", values=(nome, qtd))
                    else:
                        # Item direto
                        nome = getattr(item_container, 'nome', str(item_container))
                        tree.insert("", "end", values=(nome, 1))
                        
        except Exception as e:
            print(f"Erro ao carregar itens do kit: {e}")
            import traceback
            traceback.print_exc()

    def remover_item_do_kit(self, tree, kit, popup):
        """Remove item selecionado do kit (passando o objeto real do inventário)"""
        selecionado = tree.selection()
        
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para remover", parent=popup)
            return
        
        item_tree = tree.item(selecionado[0])
        nome_item = item_tree['values'][0]
        
        confirma = messagebox.askyesno(
            "Confirmar Remoção",
            f"Deseja remover '{nome_item}' do kit?",
            parent=popup
        )
        if not confirma:
            return

        try:
            if hasattr(kit, 'inventario') and kit.inventario:
                inventario = kit.inventario
                item_objeto = None

                # 🔎 Primeiro tenta achar o objeto pelo nome
                for container in getattr(inventario, "itens", []):
                    if hasattr(container, "item"):
                        obj = container.item
                        if getattr(obj, "nome", None) == nome_item:
                            item_objeto = obj
                            break
                    elif hasattr(container, "nome"):
                        if container.nome == nome_item:
                            item_objeto = container
                            break
                    elif isinstance(container, dict):
                        if container.get("nome") == nome_item:
                            from Dados import carregar_item_por_nome
                            item_objeto = carregar_item_por_nome(nome_item)
                            break
                    elif isinstance(container, str):
                        from Dados import carregar_item_por_nome
                        if container == nome_item:
                            item_objeto = carregar_item_por_nome(nome_item)
                            break
                
                if not item_objeto:
                    messagebox.showerror("Erro", f"Item '{nome_item}' não encontrado no inventário", parent=popup)
                    return

                # ✅ Remove agora com segurança
                inventario.remover_item(item_objeto)

                from Dados import salvar_kit_no_banco
                if salvar_kit_no_banco(kit):
                    messagebox.showinfo("Sucesso", f"Item '{nome_item}' removido com sucesso!", parent=popup)
                    self.carregar_itens_kit_na_tree(tree, kit)
                    self.carregar_kits_na_tree()
                else:
                    messagebox.showerror("Erro", "Não foi possível salvar as alterações", parent=popup)
                    
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover item: {str(e)}", parent=popup)
            print(f"Erro ao remover item do kit: {e}")
            import traceback
            traceback.print_exc()

    def montar_string_conteudo(self, kit):
        """Monta uma string resumida do conteúdo do kit"""
        try:
            if not hasattr(kit, 'inventario') or not kit.inventario:
                return "Vazio"
            
            inventario = kit.inventario
            
            # Se o inventário tem o método listar_itens
            if hasattr(inventario, 'listar_itens'):
                itens = inventario.listar_itens()
                
                if not itens:
                    return "Vazio"
                
                # Cria resumo dos itens
                resumo_itens = []
                for item_info in itens[:5]:  # Mostra no máximo 5 itens
                    if isinstance(item_info, dict):
                        nome = item_info.get('nome', 'Item')
                        qtd = item_info.get('quantidade', 1)
                        resumo_itens.append(f"{nome} ({qtd}x)")
                    else:
                        resumo_itens.append(str(item_info))
                
                total_itens = len(itens)
                texto = ", ".join(resumo_itens)
                
                if total_itens > 5:
                    texto += f" ... +{total_itens - 5} itens"
                
                return texto
            
            # Fallback: conta itens direto
            elif hasattr(inventario, 'itens') and inventario.itens:
                total = len(inventario.itens)
                return f"{total} item(ns)"
            
            return "Vazio"
            
        except Exception as e:
            print(f"⚠️ Erro ao montar conteúdo: {e}")
            return "Erro ao carregar"

    def novo_kit(self):
        """Abre janela para criar novo kit"""
        popup = tk.Toplevel(self)
        popup.title("Novo Kit")
        popup.geometry("400x250")
        popup.configure(bg="#130f26")
        popup.transient(self)
        popup.grab_set()
        
        # Título
        tk.Label(popup, text="CRIAR NOVO KIT", fg="white", bg="#1a0869",
                font=("Arial", 16, "bold")).pack(fill="x", pady=(0, 10))
        
        # Nome do kit
        tk.Label(popup, text="Nome do Kit:", bg="#130f26", fg="white",
                font=("Arial", 12)).pack(anchor="w", padx=20, pady=(10, 0))
        nome_var = tk.StringVar()
        tk.Entry(popup, textvariable=nome_var, font=("Arial", 12)).pack(fill="x", padx=20, pady=5)
        
        # Raridade
        tk.Label(popup, text="Raridade:", bg="#130f26", fg="white",
                font=("Arial", 12)).pack(anchor="w", padx=20, pady=(10, 0))
        raridade_var = tk.StringVar()
        raridades = ["Comum", "Incomum", "Raro", "Épico", "Lendário"]
        raridade_combo = ttk.Combobox(popup, textvariable=raridade_var, values=raridades, state="readonly")
        raridade_combo.pack(fill="x", padx=20, pady=5)
        raridade_combo.current(0)  # Default = Comum
        
        def salvar_novo_kit():
            nome = nome_var.get().strip()
            raridade = raridade_var.get()
            
            if not nome:
                messagebox.showwarning("Aviso", "Digite um nome para o kit", parent=popup)
                return
            
            try:
                from Codigos import Kits
                from Dados import salvar_kit_no_banco
                
                # Cria objeto Kit
                kit = Kits(nome=nome, raridade=raridade)
                
                # Salva no banco
                if salvar_kit_no_banco(kit):
                    messagebox.showinfo("Sucesso", f"Kit '{nome}' criado com sucesso!", parent=popup)
                    self.carregar_kits_na_tree()  # Atualiza a tree
                    popup.destroy()
                else:
                    messagebox.showerror("Erro", "Não foi possível salvar o kit", parent=popup)
            
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao criar kit: {str(e)}", parent=popup)
                print(f"❌ Erro ao criar kit: {e}")
                import traceback
                traceback.print_exc()
        
        # Botões
        frame_botoes = tk.Frame(popup, bg="#130f26")
        frame_botoes.pack(fill="x", pady=15)
        
        tk.Button(frame_botoes, text="Cancelar", bg="#a00c0c", fg="white",
                font=("Arial", 12), command=popup.destroy).pack(side="left", padx=20)
        tk.Button(frame_botoes, text="Criar Kit", bg="#0d7377", fg="white",
                font=("Arial", 12), command=salvar_novo_kit).pack(side="right", padx=20)

    def editar_kit(self):
        """Abre janela para editar kit selecionado"""
        selecionado = self.tree_kits.selection()
        
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um kit para editar")
            return
        
        item = self.tree_kits.item(selecionado[0])
        nome_kit = item['values'][0]
        
        try:
            # Recarrega os kits do banco para garantir sincronização
            from Dados import carregar_kits_db
            kits_atualizados = carregar_kits_db()
            
            if nome_kit not in kits_atualizados:
                messagebox.showerror("Erro", f"Kit '{nome_kit}' não encontrado")
                return
            
            kit = kits_atualizados[nome_kit]
            
            # Cria popup de edição
            self.abrir_popup_edicao_kit(kit)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar kit: {str(e)}")
            print(f"❌ Erro ao editar kit: {e}")
            import traceback
            traceback.print_exc()

    def remover_kit(self):
        """Remove kit selecionado"""
        selecionado = self.tree_kits.selection()
        
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um kit para remover")
            return
        
        item = self.tree_kits.item(selecionado[0])
        nome_kit = item['values'][0]
        
        # Confirma remoção
        confirma = messagebox.askyesno("Confirmar Remoção", 
                                        f"Deseja realmente remover o kit '{nome_kit}'?")
        
        if confirma:
            try:
                from Dados import deletar_kit_do_banco
                
                if deletar_kit_do_banco(nome_kit):
                    messagebox.showinfo("Sucesso", f"Kit '{nome_kit}' removido com sucesso!")
                    self.carregar_kits_na_tree()  # Atualiza a lista
                else:
                    messagebox.showerror("Erro", f"Não foi possível remover o kit '{nome_kit}'")
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover kit: {str(e)}")
                print(f"❌ Erro: {e}")
                import traceback
                traceback.print_exc()

    def abrir_popup_edicao_kit(self, kit):
        """Abre popup com a lista de itens do kit para edição"""
        popup = tk.Toplevel(self)
        popup.title(f"Editar Kit: {kit.nome}")
        popup.geometry("800x600")
        popup.config(bg="#130f26")
        popup.transient(self)
        popup.grab_set()
        
        # Título
        tk.Label(popup, text=f"EDITANDO: {kit.nome}", fg="white", bg="#1a0869", 
                font=("Arial", 16, "bold")).pack(fill="x", pady=(0, 10))
        
        # Frame para a lista de itens
        frame_lista = tk.Frame(popup, bg="#2a1f4a")
        frame_lista.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side="right", fill="y")
        
        # Treeview para itens do kit
        tree_itens = ttk.Treeview(frame_lista, style="Custom.Treeview",
                                columns=("Nome", "Quantidade"),
                                show="headings", yscrollcommand=scrollbar.set)
        
        tree_itens.heading("Nome", text="Item")
        tree_itens.heading("Quantidade", text="Quantidade")
        
        tree_itens.column("Nome", width=500, anchor="w")
        tree_itens.column("Quantidade", width=150, anchor="center")
        
        scrollbar.config(command=tree_itens.yview)
        tree_itens.pack(fill="both", expand=True)
        
        # Carrega itens do kit
        self.carregar_itens_kit_na_tree(tree_itens, kit)
        
        # Frame para botões
        frame_botoes = tk.Frame(popup, bg="#130f26")
        frame_botoes.pack(fill="x", padx=20, pady=10)
        
        # Botão Adicionar (sem funcionalidade)
        tk.Button(frame_botoes, text="Adicionar Item", bg="#0d7377", fg="white", font=("Arial", 12), 
        command=lambda: self.abrir_popup_adicionar_item_kit(kit, tree_itens, popup)).pack(side="left", padx=5)
        
        # Botão Remover
        tk.Button(frame_botoes, text="Remover Item", bg="#e74c3c", fg="white",
                font=("Arial", 12), 
                command=lambda: self.remover_item_do_kit(tree_itens, kit, popup)).pack(side="left", padx=5)
        
        # Botão Fechar
        tk.Button(frame_botoes, text="Fechar", bg="#95a5a6", fg="white",
                font=("Arial", 12), command=popup.destroy).pack(side="right", padx=5)
    
    def abrir_popup_adicionar_item_kit(self, kit, tree_itens, popup_pai):
        """Abre popup para adicionar item ao kit"""
        popup = tk.Toplevel(popup_pai)
        popup.title("Adicionar Item ao Kit")
        popup.configure(bg="#130f26")
        popup.geometry("1400x700")
        popup.transient(popup_pai)
        popup.grab_set()

        # Carrega os dados das tabelas
        import Dados as D
        dados_tabelas = {
            "Armas de Fogo": D.carregar_rangeds(),
            "Armas Corpo a Corpo": D.carregar_melees(),
            "Proteções": D.carregar_protecoes(),
            "Melhorias": D.carregar_melhorias(),
            "Munições": D.carregar_municoes(),
            "Consumíveis": D.carregar_consumiveis(),
            "Explosivos": D.carregar_explosivos(),
            "Itens": D.carregar_itens()
        }

        # Título
        tk.Label(popup, text="ADICIONAR ITEM AO KIT", bg="#1a0869", fg="white", 
                font=("Arial", 18, "bold")).pack(fill="x", pady=(0, 10))

        # Frame principal com scroll
        main_frame = tk.Frame(popup, bg="#130f26")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = tk.Canvas(main_frame, bg="#130f26", highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#130f26")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        quantidade_widgets = {}

        # Frame para as três colunas
        frame_colunas = tk.Frame(scrollable_frame, bg="#130f26")
        frame_colunas.pack(fill="both", expand=True, padx=10)

        # Dividir categorias em três colunas
        categorias_lista = list(dados_tabelas.items())
        terco = (len(categorias_lista) + 2) // 3
        
        # Coluna esquerda
        coluna_esquerda = tk.Frame(frame_colunas, bg="#130f26")
        coluna_esquerda.pack(side="left", fill="both", expand=True, padx=3)
        
        # Coluna central
        coluna_central = tk.Frame(frame_colunas, bg="#130f26")
        coluna_central.pack(side="left", fill="both", expand=True, padx=3)
        
        # Coluna direita
        coluna_direita = tk.Frame(frame_colunas, bg="#130f26")
        coluna_direita.pack(side="left", fill="both", expand=True, padx=3)

        # Cria uma seção para cada categoria
        for idx, (categoria, itens_dict) in enumerate(categorias_lista):
            if not itens_dict:
                continue
            
            # Escolhe a coluna (distribuindo em 3 colunas)
            if idx < terco:
                parent_frame = coluna_esquerda
            elif idx < terco * 2:
                parent_frame = coluna_central
            else:
                parent_frame = coluna_direita
                
            # Frame da categoria
            frame_categoria = tk.Frame(parent_frame, bg="#1a0869", relief="raised", bd=2)
            frame_categoria.pack(fill="both", expand=True, pady=5)
            
            # Header da categoria
            tk.Label(frame_categoria, text=categoria, bg="#0e3386", fg="white", 
                    font=("Arial", 12, "bold")).pack(fill="x", pady=3)
            
            # Frame com canvas e scrollbar para a lista de itens
            frame_lista = tk.Frame(frame_categoria, bg="#1a0869")
            frame_lista.pack(fill="both", expand=True, padx=5, pady=5)
            
            # Canvas e scrollbar
            canvas_lista = tk.Canvas(frame_lista, bg="#1a0869", highlightthickness=0, height=150)
            scrollbar_lista = tk.Scrollbar(frame_lista, orient="vertical", command=canvas_lista.yview)
            frame_itens_scroll = tk.Frame(canvas_lista, bg="#1a0869")
            
            frame_itens_scroll.bind("<Configure>", 
                                lambda e, c=canvas_lista: c.configure(scrollregion=c.bbox("all")))
            canvas_lista.create_window((0, 0), window=frame_itens_scroll, anchor="nw")
            canvas_lista.configure(yscrollcommand=scrollbar_lista.set)
            
            canvas_lista.pack(side="left", fill="both", expand=True)
            scrollbar_lista.pack(side="right", fill="y")
            
            # Exibe os itens da categoria na lista com scroll
            for nome_item, item_data in itens_dict.items():
                frame_item = tk.Frame(frame_itens_scroll, bg="#1a0869")
                frame_item.pack(fill="x", pady=1)

                # Botão do item
                btn_item = tk.Button(frame_item, text=nome_item,
                                bg="#0d7377", fg="white", width=20, font=("Arial", 9),
                                anchor="w", padx=5,
                                command=lambda c=categoria, n=nome_item: adicionar_item(c, n))
                btn_item.pack(side="left", padx=2)

                # Campo de quantidade para itens stackáveis
                if "id" not in item_data:
                    qtd_var = tk.StringVar(value="1")
                    tk.Label(frame_item, text="Qtd:", bg="#1a0869", fg="white",
                            font=("Arial", 8)).pack(side="left", padx=(5, 2))
                    qtd_entry = tk.Entry(frame_item, textvariable=qtd_var, 
                                    width=4, font=("Arial", 9))
                    qtd_entry.pack(side="left", padx=2)
                    quantidade_widgets[nome_item] = qtd_var

        def adicionar_item(categoria, nome_item):
            try:
                item_data = dados_tabelas[categoria][nome_item]
                
                # Cria o objeto do item baseado na categoria
                item_obj = criar_item_por_categoria(categoria, item_data)
                
                if item_obj is None:
                    messagebox.showerror("Erro", f"Erro ao criar item '{nome_item}'.", parent=popup)
                    return
                
                quantidade = 1

                # Verifica se é um item stackável (sem ID único)
                if not hasattr(item_obj, "Id"):
                    if nome_item in quantidade_widgets:
                        qtd_str = quantidade_widgets[nome_item].get()
                        try:
                            quantidade = int(qtd_str)
                            if quantidade <= 0:
                                raise ValueError("Quantidade deve ser maior que zero")
                        except ValueError:
                            messagebox.showerror("Erro", "Quantidade inválida.", parent=popup)
                            return

                # Adiciona o item ao inventário do kit
                if hasattr(kit, 'inventario') and kit.inventario:
                    kit.inventario.gerenciar_item(item_objeto=item_obj, 
                                                quantidade=quantidade, 
                                                operacao="adicionar")
                    
                    # Salva no banco
                    from Dados import salvar_kit_no_banco
                    
                    if salvar_kit_no_banco(kit):
                        # Atualiza a tree do popup de edição
                        self.carregar_itens_kit_na_tree(tree_itens, kit)
                        
                        # Atualiza a tree principal
                        self.carregar_kits_na_tree()
                        
                        # Reseta o campo de quantidade se for stackável
                        if nome_item in quantidade_widgets:
                            quantidade_widgets[nome_item].set("1")
                    else:
                        messagebox.showerror("Erro", "Não foi possível salvar as alterações", parent=popup)
                else:
                    messagebox.showerror("Erro", "Kit não possui inventário válido", parent=popup)
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar item: {str(e)}", parent=popup)
                print(f"❌ Erro: {e}")
                import traceback
                traceback.print_exc()

        def criar_item_por_categoria(categoria, item_data):
            """Cria um objeto de item baseado na categoria e dados"""
            try:
                if categoria == "Armas de Fogo":
                    from Codigos import Ranged
                    return Ranged(
                        nome=item_data.get("nome", "Arma de Fogo"),
                        peso=item_data.get("peso", 2.0),
                        classe=item_data.get("classe", "Pistola"),
                        acao=item_data.get("acao", "Semi"),
                        raridade=item_data.get("raridade", "Comum"),
                        calibre=item_data.get("calibre", ".22"),
                        capacidade=item_data.get("capacidade", 10)
                    )
                    
                elif categoria == "Armas Corpo a Corpo":
                    from Codigos import Melee
                    return Melee(
                        nome=item_data.get("nome", "Arma Branca"),
                        peso=item_data.get("peso", 1.0),
                        classe=item_data.get("classe", "Faca"),
                        tipo_dano=item_data.get("tipo_dano", "Cortante"),
                        raridade=item_data.get("raridade", "Comum")
                    )
                    
                elif categoria == "Proteções":
                    from Codigos import Protecao
                    return Protecao(
                        nome=item_data.get("nome", "Proteção"),
                        peso=item_data.get("peso", 1.0),
                        nivelBalistico=item_data.get("nivelBalistico", 1),
                        absorcaoFisica=item_data.get("absorcaoFisica", 1),
                        absorcaoBalistica=item_data.get("absorcaoBalistica", 1),
                        regiao=item_data.get("regiao", "Torso")
                    )
                    
                elif categoria == "Melhorias":
                    from Codigos import Melhoria
                    return Melhoria(
                        nome=item_data.get("nome", "Melhoria"),
                        peso=item_data.get("peso", 0.1),
                        tipo=item_data.get("tipo", "ranged"),
                        modificadores=item_data.get("modificadores", {})
                    )
                    
                elif categoria == "Munições":
                    from Codigos import Municao
                    return Municao(
                        nome=item_data.get("nome", "Munição"),
                        calibre=item_data.get("calibre", ".22"),
                        perfuracao=item_data.get("perfuracao", 1),
                        dano=item_data.get("dano", 5)
                    )
                    
                elif categoria == "Consumíveis":
                    from Codigos import Consumivel
                    return Consumivel(
                        nome=item_data.get("nome", "Consumível"),
                        peso=item_data.get("peso", 1.0),
                        cura=item_data.get("cura", 0),
                        energia=item_data.get("energia", 0)
                    )
                    
                elif categoria == "Explosivos":
                    from Codigos import Explosivo
                    return Explosivo(
                        nome=item_data.get("nome", "Explosivo"),
                        peso=item_data.get("peso", 1.0),
                        raio=item_data.get("raio", 1),
                        dano=item_data.get("dano", 10),
                        tipo_dano=item_data.get("tipo_dano", 1)
                    )
                    
                elif categoria == "Itens":
                    from Codigos import Item
                    return Item(
                        nome=item_data.get("nome", "Item"),
                        peso=item_data.get("peso", 1.0)
                    )
                    
                else:
                    return None
                    
            except Exception as e:
                print(f"❌ Erro ao criar item da categoria {categoria}: {e}")
                return None

        # Botão Fechar
        tk.Button(popup, text="Fechar", command=popup.destroy, 
                bg="#95a5a6", fg="white", font=("Arial", 14), 
                width=20).pack(pady=10)
    # kits #

    # buffs e debuffs #
    def template_buffs_debuffs(self):
        """Template para tabela de Buffs e Debuffs"""
        self.limpar_container()

        tk.Label(self.container_conteudo, text="BUFFS E DEBUFFS", 
                fg="white", bg="#1a0869", font=("Arial", 18, "bold")
                ).place(x=0, y=0, width=1400, height=50)

        # --- Tabela ---
        tree_frame = tk.Frame(self.container_conteudo, bg="#2a1f4a")
        tree_frame.place(x=0, y=60, width=1400, height=580)

        self.tree_buffs = ttk.Treeview(tree_frame, style="Custom.Treeview",
                                    columns=("Nome", "Tipo", "Duração", "Descrição"),
                                    show="headings")
        for col in ("Nome", "Tipo", "Duração", "Descrição"):
            self.tree_buffs.heading(col, text=col)
            self.tree_buffs.column(col, anchor="center", width=300)
        self.tree_buffs.pack(fill="both", expand=True)

        self.carregar_buffs_tree()

        # --- Funções internas ---
        def validar_campos(data, editar=False):
            if not data["nome"]:
                messagebox.showwarning("Campo obrigatório", "O campo 'Nome' é obrigatório.")
                return False
            if not data["tipo"]:
                messagebox.showwarning("Campo obrigatório", "O campo 'Tipo' é obrigatório.")
                return False
            if data["duração"]:
                try:
                    data["duração"] = int(data["duração"])
                except ValueError:
                    messagebox.showwarning("Valor inválido", "O campo 'Duração' deve ser numérico.")
                    return False
            else:
                data["duração"] = None
            if not editar:
                buffs = D.carregar_buffs_debuffs()
                if data["nome"] in buffs:
                    messagebox.showwarning("Duplicado", f"Já existe um efeito chamado '{data['nome']}'.")
                    return False
            return True

        def novo_buff():
            popup = tk.Toplevel(self)
            popup.title("Novo Buff/Debuff")
            popup.geometry("450x400")
            popup.config(bg="#1a0869")

            campos = ["Nome", "Tipo", "Duração", "Descrição"]
            entradas = {}
            for i, campo in enumerate(campos):
                tk.Label(popup, text=campo, fg="white", bg="#1a0869", font=("Arial", 12, "bold")).place(x=30, y=30 + i*70)
                entrada = tk.Entry(popup, font=("Arial", 12))
                entrada.place(x=150, y=30 + i*70, width=250)
                entradas[campo] = entrada

            def salvar():
                data = {campo.lower(): entradas[campo].get().strip() for campo in campos}
                if not validar_campos(data):
                    return
                if D.salvar_buff_debuff(data):
                    self.carregar_buffs_tree()
                    messagebox.showinfo("Sucesso", f"Efeito '{data['nome']}' criado com sucesso.")
                    popup.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao criar Buff/Debuff.")

            tk.Button(popup, text="Salvar", command=salvar,
                    bg="#0d7377", fg="white", font=("Arial", 14)).place(x=150, y=320, width=140, height=40)

        def editar_buff():
            selected = self.tree_buffs.selection()
            if not selected:
                messagebox.showwarning("Nenhum selecionado", "Selecione um efeito para editar.")
                return
            item = self.tree_buffs.item(selected[0], "values")
            nome_original = item[0]

            popup = tk.Toplevel(self)
            popup.title("Editar Buff/Debuff")
            popup.geometry("450x400")
            popup.config(bg="#1a0869")

            campos = ["Nome", "Tipo", "Duração", "Descrição"]
            entradas = {}
            for i, campo in enumerate(campos):
                tk.Label(popup, text=campo, fg="white", bg="#1a0869", font=("Arial", 12, "bold")).place(x=30, y=30 + i*70)
                entrada = tk.Entry(popup, font=("Arial", 12))
                entrada.place(x=150, y=30 + i*70, width=250)
                entrada.insert(0, item[i])
                entradas[campo] = entrada

            def salvar():
                data = {campo.lower(): entradas[campo].get().strip() for campo in campos}
                if not validar_campos(data, editar=True):
                    return
                if D.editar_buff_debuff(nome_original, data):
                    self.carregar_buffs_tree()
                    messagebox.showinfo("Sucesso", f"Efeito '{data['nome']}' atualizado com sucesso.")
                    popup.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao editar Buff/Debuff.")

            tk.Button(popup, text="Salvar", command=salvar,
                    bg="#f39c12", fg="white", font=("Arial", 14)).place(x=150, y=320, width=140, height=40)

        def remover_buff():
            selected = self.tree_buffs.selection()
            if not selected:
                messagebox.showwarning("Nenhum selecionado", "Selecione um efeito para remover.")
                return
            item = self.tree_buffs.item(selected[0], "values")
            nome = item[0]
            if not messagebox.askyesno("Confirmar exclusão", f"Remover '{nome}'?"):
                return
            if D.remover_buff_debuff(nome):
                self.carregar_buffs_tree()
                messagebox.showinfo("Removido", f"'{nome}' removido com sucesso.")
            else:
                messagebox.showerror("Erro", "Erro ao remover Buff/Debuff.")

        # --- Botões ---
        btn_width = 150
        btn_spacing = 150
        total_width = btn_width * 3 + btn_spacing * 2
        start_x = (1000 - total_width) // 2

        tk.Button(self.container_conteudo, text="Novo", bg="#0d7377", fg="white",
                font=("Arial", 14), command=novo_buff).place(x=start_x, y=650, width=btn_width, height=40)
        tk.Button(self.container_conteudo, text="Editar", bg="#f39c12", fg="white",
                font=("Arial", 14), command=editar_buff).place(x=start_x + btn_spacing, y=650, width=btn_width, height=40)
        tk.Button(self.container_conteudo, text="Remover", bg="#e74c3c", fg="white",
                font=("Arial", 14), command=remover_buff).place(x=start_x + btn_spacing * 2, y=650, width=btn_width, height=40)

    def carregar_buffs_tree(self):
        if not hasattr(self, "tree_buffs"):
            return
        for i in self.tree_buffs.get_children():
            self.tree_buffs.delete(i)
        try:
            buffs = D.carregar_buffs_debuffs()
            for nome, data in buffs.items():
                self.tree_buffs.insert("", "end", values=(
                    data.get("nome", ""),
                    data.get("tipo", ""),
                    data.get("duração", ""),
                    data.get("descrição", "")
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar Buffs/Debuffs:\n{e}")
    # buffs e debuffs #

    # habilidades #
    def template_habilidades(self):
        """Template para tabela de Habilidades"""
        self.limpar_container()

        tk.Label(self.container_conteudo, text="HABILIDADES",
                fg="white", bg="#1a0869", font=("Arial", 18, "bold")
                ).place(x=0, y=0, width=1400, height=50)

        # Frame da Tabela
        tree_frame = tk.Frame(self.container_conteudo, bg="#2a1f4a")
        tree_frame.place(x=0, y=60, width=1400, height=580)

        self.tree_habilidades = ttk.Treeview(tree_frame, style="Custom.Treeview",
                                        columns=("Nome", "Descrição", "Categoria"),
                                        show="headings")
        for col in ("Nome", "Descrição", "Categoria"):
            self.tree_habilidades.heading(col, text=col)
            self.tree_habilidades.column(col, anchor="center", width=400)
        self.tree_habilidades.pack(fill="both", expand=True)

        self.carregar_habilidades_tree()

        # --- Funções internas ---
        def validar_campos(data, editar=False):
            if not data["nome"]:
                messagebox.showwarning("Campo obrigatório", "O campo 'Nome' é obrigatório.")
                return False
            if not editar:
                habilidades = D.carregar_habilidades()
                if data["nome"] in habilidades:
                    messagebox.showwarning("Duplicado", f"Já existe uma habilidade com o nome '{data['nome']}'.")
                    return False
            return True

        def nova_habilidade():
            popup = tk.Toplevel(self)
            popup.title("Nova Habilidade")
            popup.geometry("500x350")
            popup.config(bg="#1a0869")

            campos = ["Nome", "Descrição", "Categoria"]
            entradas = {}
            for i, campo in enumerate(campos):
                tk.Label(popup, text=campo, fg="white", bg="#1a0869",
                        font=("Arial", 12, "bold")).place(x=30, y=30 + i*90)
                entrada = tk.Entry(popup, font=("Arial", 12))
                entrada.place(x=150, y=30 + i*90, width=300)
                entradas[campo] = entrada

            def salvar():
                data = {campo.lower(): entradas[campo].get().strip() for campo in campos}
                if not validar_campos(data):
                    return
                if D.salvar_habilidades(data):
                    self.carregar_habilidades_tree()
                    messagebox.showinfo("Sucesso", f"Habilidade '{data['nome']}' criada com sucesso.")
                    popup.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao criar Habilidade.")

            tk.Button(popup, text="Salvar", command=salvar,
                    bg="#0d7377", fg="white", font=("Arial", 14)
                    ).place(x=180, y=280, width=140, height=40)

        def editar_habilidade():
            selected = self.tree_habilidades.selection()
            if not selected:
                messagebox.showwarning("Nenhuma habilidade selecionada", "Selecione uma habilidade para editar.")
                return
            item = self.tree_habilidades.item(selected[0], "values")
            nome_original = item[0]

            popup = tk.Toplevel(self)
            popup.title("Editar Habilidade")
            popup.geometry("500x350")
            popup.config(bg="#1a0869")

            campos = ["Nome", "Descrição", "Categoria"]
            entradas = {}
            for i, campo in enumerate(campos):
                tk.Label(popup, text=campo, fg="white", bg="#1a0869",
                        font=("Arial", 12, "bold")).place(x=30, y=30 + i*90)
                entrada = tk.Entry(popup, font=("Arial", 12))
                entrada.place(x=150, y=30 + i*90, width=300)
                entrada.insert(0, item[i])
                entradas[campo] = entrada

            def salvar():
                data = {campo.lower(): entradas[campo].get().strip() for campo in campos}
                if not validar_campos(data, editar=True):
                    return
                if D.editar_habilidades(nome_original, data):
                    self.carregar_habilidades_tree()
                    messagebox.showinfo("Sucesso", f"Habilidade '{data['nome']}' atualizada com sucesso.")
                    popup.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao editar Habilidade.")

            tk.Button(popup, text="Salvar", command=salvar,
                    bg="#f39c12", fg="white", font=("Arial", 14)
                    ).place(x=180, y=280, width=140, height=40)

        def remover_habilidade():
            selected = self.tree_habilidades.selection()
            if not selected:
                messagebox.showwarning("Nenhuma habilidade selecionada", "Selecione uma habilidade para remover.")
                return
            item = self.tree_habilidades.item(selected[0], "values")
            nome = item[0]

            confirm = messagebox.askyesno("Confirmar exclusão", f"Tem certeza que deseja remover '{nome}'?")
            if not confirm:
                return

            if D.remover_habilidades(nome):
                self.carregar_habilidades_tree()
                messagebox.showinfo("Removida", f"Habilidade '{nome}' removida com sucesso.")
            else:
                messagebox.showerror("Erro", f"Erro ao remover habilidade '{nome}'.")

        # --- Botões ---
        btn_width = 150
        btn_spacing = 150
        total_width = btn_width * 3 + btn_spacing * 2
        start_x = (1000 - total_width) // 2

        tk.Button(self.container_conteudo, text="Novo", bg="#0d7377", fg="white",
                font=("Arial", 14), command=nova_habilidade).place(x=start_x, y=650, width=btn_width, height=40)
        tk.Button(self.container_conteudo, text="Editar", bg="#f39c12", fg="white",
                font=("Arial", 14), command=editar_habilidade).place(x=start_x + btn_spacing, y=650, width=btn_width, height=40)
        tk.Button(self.container_conteudo, text="Remover", bg="#e74c3c", fg="white",
                font=("Arial", 14), command=remover_habilidade).place(x=start_x + btn_spacing * 2, y=650, width=btn_width, height=40)

    def carregar_habilidades_tree(self):
        """Carrega e exibe todas as habilidades do banco"""
        if not hasattr(self, "tree_habilidades"):
            return
        for i in self.tree_habilidades.get_children():
            self.tree_habilidades.delete(i)
        try:
            habilidades = D.carregar_habilidades()
            for nome, data in habilidades.items():
                self.tree_habilidades.insert("", "end", values=(
                    data.get("nome", ""),
                    data.get("descrição", ""),
                    data.get("categoria", "")
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar tabela Habilidades:\n{e}")
    # habilidades #

    # poderes #
    def template_poderes(self):
        """Template para tabela de Poderes"""
        self.limpar_container()

        tk.Label(self.container_conteudo, text="PODERES",
                fg="white", bg="#1a0869", font=("Arial", 18, "bold")
                ).place(x=0, y=0, width=1400, height=50)

        # Frame da Tabela
        tree_frame = tk.Frame(self.container_conteudo, bg="#2a1f4a")
        tree_frame.place(x=0, y=60, width=1400, height=580)

        self.tree_poderes = ttk.Treeview(tree_frame, style="Custom.Treeview",
                                        columns=("Nome", "Custo", "Descrição"),
                                        show="headings")
        for col in ("Nome", "Custo", "Descrição"):
            self.tree_poderes.heading(col, text=col)
            self.tree_poderes.column(col, anchor="center", width=400)
        self.tree_poderes.pack(fill="both", expand=True)

        self.carregar_poderes_tree()

        # --- Funções internas ---
        def validar_campos(data, editar=False):
            if not data["nome"]:
                messagebox.showwarning("Campo obrigatório", "O campo 'Nome' é obrigatório.")
                return False
            if data["custo"]:
                try:
                    data["custo"] = int(data["custo"])
                except ValueError:
                    messagebox.showwarning("Valor inválido", "O campo 'Custo' deve ser numérico.")
                    return False
            else:
                data["custo"] = None

            if not editar:
                poderes = D.carregar_poderes()
                if data["nome"] in poderes:
                    messagebox.showwarning("Duplicado", f"Já existe um poder com o nome '{data['nome']}'.")
                    return False
            return True

        def novo_poder():
            popup = tk.Toplevel(self)
            popup.title("Novo Poder")
            popup.geometry("500x350")
            popup.config(bg="#1a0869")

            campos = ["Nome", "Custo", "Descrição"]
            entradas = {}
            for i, campo in enumerate(campos):
                tk.Label(popup, text=campo, fg="white", bg="#1a0869",
                        font=("Arial", 12, "bold")).place(x=30, y=30 + i*90)
                entrada = tk.Entry(popup, font=("Arial", 12))
                entrada.place(x=150, y=30 + i*90, width=300)
                entradas[campo] = entrada

            def salvar():
                data = {campo.lower(): entradas[campo].get().strip() for campo in campos}
                if not validar_campos(data):
                    return
                if D.salvar_poderes(data):
                    self.carregar_poderes_tree()
                    messagebox.showinfo("Sucesso", f"Poder '{data['nome']}' criado com sucesso.")
                    popup.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao criar Poder.")

            tk.Button(popup, text="Salvar", command=salvar,
                    bg="#0d7377", fg="white", font=("Arial", 14)
                    ).place(x=180, y=280, width=140, height=40)

        def editar_poder():
            selected = self.tree_poderes.selection()
            if not selected:
                messagebox.showwarning("Nenhum poder selecionado", "Selecione um poder para editar.")
                return
            item = self.tree_poderes.item(selected[0], "values")
            nome_original = item[0]

            popup = tk.Toplevel(self)
            popup.title("Editar Poder")
            popup.geometry("500x350")
            popup.config(bg="#1a0869")

            campos = ["Nome", "Custo", "Descrição"]
            entradas = {}
            for i, campo in enumerate(campos):
                tk.Label(popup, text=campo, fg="white", bg="#1a0869",
                        font=("Arial", 12, "bold")).place(x=30, y=30 + i*90)
                entrada = tk.Entry(popup, font=("Arial", 12))
                entrada.place(x=150, y=30 + i*90, width=300)
                entrada.insert(0, item[i])
                entradas[campo] = entrada

            def salvar():
                data = {campo.lower(): entradas[campo].get().strip() for campo in campos}
                if not validar_campos(data, editar=True):
                    return
                if D.editar_poderes(nome_original, data):
                    self.carregar_poderes_tree()
                    messagebox.showinfo("Sucesso", f"Poder '{data['nome']}' atualizado com sucesso.")
                    popup.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao editar Poder.")

            tk.Button(popup, text="Salvar", command=salvar,
                    bg="#f39c12", fg="white", font=("Arial", 14)
                    ).place(x=180, y=280, width=140, height=40)

        def remover_poder():
            selected = self.tree_poderes.selection()
            if not selected:
                messagebox.showwarning("Nenhum poder selecionado", "Selecione um poder para remover.")
                return
            item = self.tree_poderes.item(selected[0], "values")
            nome = item[0]

            confirm = messagebox.askyesno("Confirmar exclusão", f"Tem certeza que deseja remover '{nome}'?")
            if not confirm:
                return

            if D.remover_poderes(nome):
                self.carregar_poderes_tree()
                messagebox.showinfo("Removido", f"Poder '{nome}' removido com sucesso.")
            else:
                messagebox.showerror("Erro", f"Erro ao remover Poder '{nome}'.")

        # --- Botões ---
        btn_width = 150
        btn_spacing = 150
        total_width = btn_width * 3 + btn_spacing * 2
        start_x = (1000 - total_width) // 2

        tk.Button(self.container_conteudo, text="Novo", bg="#0d7377", fg="white",
                font=("Arial", 14), command=novo_poder).place(x=start_x, y=650, width=btn_width, height=40)
        tk.Button(self.container_conteudo, text="Editar", bg="#f39c12", fg="white",
                font=("Arial", 14), command=editar_poder).place(x=start_x + btn_spacing, y=650, width=btn_width, height=40)
        tk.Button(self.container_conteudo, text="Remover", bg="#e74c3c", fg="white",
                font=("Arial", 14), command=remover_poder).place(x=start_x + btn_spacing * 2, y=650, width=btn_width, height=40)

    def carregar_poderes_tree(self):
        """Carrega e exibe todos os poderes do banco"""
        if not hasattr(self, "tree_poderes"):
            return
        for i in self.tree_poderes.get_children():
            self.tree_poderes.delete(i)
        try:
            poderes = D.carregar_poderes()
            for nome, data in poderes.items():
                self.tree_poderes.insert("", "end", values=(
                    data.get("nome", ""),
                    data.get("custo", ""),
                    data.get("descrição", "")
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar tabela Poderes:\n{e}")
    # poderes #

    def template_proficiencias(self):
        """Template para tabela de Proficiências"""
        tk.Label(self.container_conteudo, text="PROFICIÊNCIAS", fg="white", bg="#1a0869", font=("Arial", 18, "bold")).place(x=0, y=0, width=1400, height=50)
        
        tree_frame = tk.Frame(self.container_conteudo, bg="#2a1f4a")
        tree_frame.place(x=0, y=60, width=1400, height=580)
        
        tree = ttk.Treeview(tree_frame, style="Custom.Treeview", columns=("Nome", "Atributo", "Nível"), show="headings")
        for col in ("Nome", "Atributo", "Nível"):
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True)
        
        # Botões centralizados
        btn_width = 150
        btn_spacing = 150
        total_width = btn_width * 3 + btn_spacing * 2
        start_x = (1000 - total_width) // 2
        
        tk.Button(self.container_conteudo, text="Novo", bg="#0d7377", fg="white", 
                 font=("Arial", 14)).place(x=start_x, y=650, width=btn_width, height=40)
        tk.Button(self.container_conteudo, text="Editar", bg="#f39c12", fg="white", 
                 font=("Arial", 14)).place(x=start_x + btn_spacing, y=650, width=btn_width, height=40)
        tk.Button(self.container_conteudo, text="Remover", bg="#e74c3c", fg="white", 
                 font=("Arial", 14)).place(x=start_x + btn_spacing * 2, y=650, width=btn_width, height=40)

    def TelaInicial(self):
        self.controller.TelaInicial()

    def TelaDeSelecao(self):
        self.controller.TelaDeSelecao()

    def TelaDeCombate(self):
        self.controller.TelaDeCombate()
### TELA DE DICIONARIOS ###
### TELA DE DICIONARIOS ###
### TELA DE DICIONARIOS ###

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1600x900")
        self.title("Skirmish Engine Manager")
        #self.resizable(False,False)

        self.frames = {}

        # Configura o layout da janela principal para expandir corretamente
        self.grid_rowconfigure(0, weight=1)  
        self.grid_columnconfigure(0, weight=1)

        for F in (MainScreen, CharacterSelectScreen, CharacterDetailsScreen, CombatSystemScreen, RegrasItensScreen):
            frame = F(self, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.grid_remove()

        self.show_frame(MainScreen)

    def show_frame(self, cont, **kwargs):
        for frame in self.frames.values():
            frame.grid_remove()

        frame = self.frames[cont]
        if hasattr(frame, 'refresh'):
            frame.refresh(**kwargs)
        frame.grid()

        # Configura para ocupar todo o espaço
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

# Executar o App
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

