import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import Dados as D
import Codigos as CB
import re
import random
import os

### TELA PRINCIPAL ###
### TELA PRINCIPAL ###
### TELA PRINCIPAL ###
class MainScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#130f26")

        # Título da tela
        label = tk.Label(text="- Skirmish Engine -", width=25, height=3, font=("Arial", 40, "bold"), fg="white", bg="#1a0869")
        label.place(width=800,height=100,x=400, y=120)

        tk.Label(self, text="Tela inicial", fg="white", bg="#1a0869",
                font=("Arial", 20, "bold"), width=20, height=2).place(x=20, y=10, width=350, height=75)
        
        tk.Button(self, text="Seleção", height=2, command=self.TelaDeSelecao,
                bg="#1a0869", fg="white", font=("Arial", 20)).place(x=385, y=10, width=350, height=75)
        
        tk.Button(self, text="Combate", height=2, command=self.TelaDeCombate,
                bg="#1a0869", fg="white", font=("Arial", 20)).place(x=870, y=10, width=350, height=75)

        tk.Button(self, text="Informações", height=2, command=self.TelaDeRegrasEItens,
                bg="#1a0869", fg="white", font=("Arial", 20)).place(x=1235, y=10, width=350, height=75)
        
        # === SEÇÃO DE GERENCIAMENTO DE SESSÕES ===
        # Frame para controles de sessão
        sessao_frame = tk.Frame(self, bg="#1a0869")
        sessao_frame.place(x=50, y=250, width=450, height=400)
        
        # Título da seção
        tk.Label(sessao_frame, text="Gerenciamento de Sessões", 
                font=("Arial", 16, "bold"), fg="white", bg="#1a0869").pack(pady=10)
        
        # Frame para listbox e scrollbar
        lista_frame = tk.Frame(sessao_frame, bg="#1a0869")
        lista_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Listbox para mostrar sessões disponíveis
        self.sessoes_listbox = tk.Listbox(lista_frame, font=("Arial", 12), bg="#2a1f3d", fg="white", 
                                         selectbackground="#4a3f5d", height=8)
        self.sessoes_listbox.pack(side="left", fill="both", expand=True)
        
        # Scrollbar para a listbox
        scrollbar = tk.Scrollbar(lista_frame, orient="vertical", command=self.sessoes_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.sessoes_listbox.config(yscrollcommand=scrollbar.set)
        
        # Frame para botões de sessão
        botoes_sessao_frame = tk.Frame(sessao_frame, bg="#1a0869")
        botoes_sessao_frame.pack(fill="x", padx=10, pady=5)
        
        # Botões para gerenciar sessões
        tk.Button(botoes_sessao_frame, text="Atualizar Lista", command=self.atualizar_lista_sessoes,
                bg="#2a1f3d", fg="white", font=("Arial", 10)).pack(side="left", padx=2)
        
        tk.Button(botoes_sessao_frame, text="Carregar", command=self.carregar_sessao_selecionada,
                bg="#2a1f3d", fg="white", font=("Arial", 10)).pack(side="left", padx=2)
        
        tk.Button(botoes_sessao_frame, text="Deletar", command=self.deletar_sessao_selecionada,
                bg="#2a1f3d", fg="white", font=("Arial", 10)).pack(side="left", padx=2)
        
        # Frame para criar/salvar sessão
        criar_frame = tk.Frame(sessao_frame, bg="#1a0869")
        criar_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(criar_frame, text="Nome da sessão:", fg="white", bg="#1a0869", font=("Arial", 10)).pack(anchor="w")
        
        self.nome_sessao_entry = tk.Entry(criar_frame, font=("Arial", 12), bg="#2a1f3d", fg="white")
        self.nome_sessao_entry.pack(fill="x", pady=2)
        
        # Frame para botões criar/salvar
        botoes_criar_frame = tk.Frame(criar_frame, bg="#1a0869")
        botoes_criar_frame.pack(fill="x", pady=5)
        
        tk.Button(botoes_criar_frame, text="Nova Sessão", command=self.criar_nova_sessao,
                bg="#2a1f3d", fg="white", font=("Arial", 10)).pack(side="left", padx=2)
        
        tk.Button(botoes_criar_frame, text="Salvar Atual", command=self.salvar_sessao_atual,
                bg="#2a1f3d", fg="white", font=("Arial", 10)).pack(side="left", padx=2)
        
        tk.Button(botoes_criar_frame, text="Duplicar", command=self.duplicar_sessao_selecionada,
                bg="#2a1f3d", fg="white", font=("Arial", 10)).pack(side="left", padx=2)
        
        # === INFORMAÇÕES DA SESSÃO ATUAL ===
        info_frame = tk.Frame(self, bg="black")
        info_frame.place(x=550, y=250, width=500, height=300)
        
        tk.Label(info_frame, text="Sessão Atual", font=("Arial", 14, "bold"), fg="white", bg="black").pack(pady=5)
        
        self.info_sessao_label = tk.Label(info_frame, text="Nenhuma sessão carregada", 
                                         font=("Arial", 12), fg="white", bg="black", justify="left")
        self.info_sessao_label.pack(fill="both", expand=True, padx=10, pady=5)
        
        # === INFORMAÇÕES DO APLICATIVO ===
        sobre_frame = tk.Frame(self, bg="black")
        sobre_frame.place(x=1100, y=250, width=500, height=300)

        sobre_o_app = """
Versão 1.4.0

Feito por Lucas Henrique Gonzaga Santos

Linguagem de programação usada: Python

Biblioteca de interface usada: Tkinter

Programa usado: Visual Studio Code """

        sobre_label = tk.Label(sobre_frame, text=sobre_o_app, font=("Arial", 14), fg="white", bg="black", justify="left")
        sobre_label.pack(fill="both", expand=True, padx=10, pady=10)

        btn_sair = tk.Button(text="Shutdown", width=15, height=2, font=("Arial", 30, "bold"), fg="white", bg="#1a0869", command=controller.quit)
        btn_sair.place(width=300,height=100, x=650, y=800)
        
        # Carrega a lista de sessões na inicialização
        self.atualizar_lista_sessoes()
        self.atualizar_info_sessao_atual()

    def atualizar_lista_sessoes(self):
        """Atualiza a listbox com as sessões disponíveis"""
        try:
            from Dados import listar_sessoes_disponiveis
            self.sessoes_listbox.delete(0, tk.END)
            
            sessoes = listar_sessoes_disponiveis()
            for sessao in sessoes:
                # Formato: "Nome - DD/MM/YYYY HH:MM"
                item = f"{sessao['nome']} - {sessao['data_formatada']}"
                self.sessoes_listbox.insert(tk.END, item)
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Erro ao carregar lista de sessões: {e}")

    def carregar_sessao_selecionada(self):
        """Carrega a sessão selecionada na listbox"""
        try:
            selection = self.sessoes_listbox.curselection()
            if not selection:
                tk.messagebox.showwarning("Aviso", "Selecione uma sessão para carregar.")
                return
            
            # Pega o nome da sessão (antes do " - ")
            item_text = self.sessoes_listbox.get(selection[0])
            nome_sessao = item_text.split(" - ")[0]
            
            from Dados import carregar_sessao_do_supabase
            if carregar_sessao_do_supabase(nome_sessao):
                tk.messagebox.showinfo("Sucesso", f"Sessão '{nome_sessao}' carregada com sucesso!")
                self.atualizar_info_sessao_atual()
            else:
                tk.messagebox.showerror("Erro", f"Erro ao carregar sessão '{nome_sessao}'")
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Erro ao carregar sessão: {e}")

    def deletar_sessao_selecionada(self):
        """Deleta a sessão selecionada"""
        try:
            selection = self.sessoes_listbox.curselection()
            if not selection:
                tk.messagebox.showwarning("Aviso", "Selecione uma sessão para deletar.")
                return
            
            item_text = self.sessoes_listbox.get(selection[0])
            nome_sessao = item_text.split(" - ")[0]
            
            # Confirma a exclusão
            if tk.messagebox.askyesno("Confirmar", f"Deletar sessão '{nome_sessao}'?"):
                from Dados import deletar_sessao_do_supabase
                if deletar_sessao_do_supabase(nome_sessao):
                    tk.messagebox.showinfo("Sucesso", f"Sessão '{nome_sessao}' deletada!")
                    self.atualizar_lista_sessoes()
                else:
                    tk.messagebox.showerror("Erro", f"Erro ao deletar sessão '{nome_sessao}'")
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Erro ao deletar sessão: {e}")

    def criar_nova_sessao(self):
        """Cria uma nova sessão vazia"""
        try:
            from Dados import criar_nova_sessao
            criar_nova_sessao()
            tk.messagebox.showinfo("Sucesso", "Nova sessão criada (dados limpos)!")
            self.atualizar_info_sessao_atual()
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Erro ao criar nova sessão: {e}")

    def salvar_sessao_atual(self):
        """Salva a sessão atual com o nome especificado"""
        try:
            nome_sessao = self.nome_sessao_entry.get().strip()
            if not nome_sessao:
                tk.messagebox.showwarning("Aviso", "Digite um nome para a sessão.")
                return
            
            from Dados import salvar_sessao_no_supabase, verificar_sessao_existe
            
            # Verifica se já existe
            if verificar_sessao_existe(nome_sessao):
                if tk.messagebox.askyesno("Confirmar", f"Sessão '{nome_sessao}' já existe. Sobrescrever?"):
                    if salvar_sessao_no_supabase(nome_sessao, sobrescrever=True):
                        tk.messagebox.showinfo("Sucesso", f"Sessão '{nome_sessao}' atualizada!")
                        self.atualizar_lista_sessoes()
                        self.nome_sessao_entry.delete(0, tk.END)
                    else:
                        tk.messagebox.showerror("Erro", f"Erro ao salvar sessão '{nome_sessao}'")
            else:
                if salvar_sessao_no_supabase(nome_sessao):
                    tk.messagebox.showinfo("Sucesso", f"Sessão '{nome_sessao}' salva!")
                    self.atualizar_lista_sessoes()
                    self.nome_sessao_entry.delete(0, tk.END)
                else:
                    tk.messagebox.showerror("Erro", f"Erro ao salvar sessão '{nome_sessao}'")
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Erro ao salvar sessão: {e}")

    def duplicar_sessao_selecionada(self):
        """Duplica a sessão selecionada"""
        try:
            selection = self.sessoes_listbox.curselection()
            if not selection:
                tk.messagebox.showwarning("Aviso", "Selecione uma sessão para duplicar.")
                return
            
            nome_novo = self.nome_sessao_entry.get().strip()
            if not nome_novo:
                tk.messagebox.showwarning("Aviso", "Digite um nome para a nova sessão.")
                return
            
            item_text = self.sessoes_listbox.get(selection[0])
            nome_origem = item_text.split(" - ")[0]
            
            from Dados import duplicar_sessao
            if duplicar_sessao(nome_origem, nome_novo):
                tk.messagebox.showinfo("Sucesso", f"Sessão duplicada: '{nome_origem}' -> '{nome_novo}'")
                self.atualizar_lista_sessoes()
                self.nome_sessao_entry.delete(0, tk.END)
            else:
                tk.messagebox.showerror("Erro", f"Erro ao duplicar sessão")
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Erro ao duplicar sessão: {e}")

    def atualizar_info_sessao_atual(self):
        """Atualiza as informações da sessão atual"""
        try:
            from Dados import obter_info_sessao_atual
            info = obter_info_sessao_atual()
            
            if info['total_personagens'] == 0:
                texto = "Nenhuma sessão carregada"
            else:
                texto = f"Grupos: {info['total_grupos']}\n"
                texto += f"Personagens: {info['total_personagens']}\n\n"
                
                for nome_grupo, grupo_info in info['grupos'].items():
                    texto += f"• {nome_grupo}: {grupo_info['quantidade']} personagens\n"
                    for nome in grupo_info['nomes']:
                        texto += f"  - {nome}\n"
            
            self.info_sessao_label.config(text=texto)
        except Exception as e:
            self.info_sessao_label.config(text=f"Erro ao carregar informações: {e}")

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

        # --- Navegação ---
        tk.Button(self, text="Tela inicial", height=2, command=self.Voltar,
                bg="#1a0869", fg="white", font=("Arial", 20)).place(x=20, y=10, width=350, height=75)

        tk.Label(self, text="Seleção", fg="white", bg="#1a0869",
                font=("Arial", 20, "bold"), width=20, height=2).place(x=385, y=10, width=350, height=75)

        tk.Button(self, text="Combate", height=2, command=self.TelaDeCombate,
                bg="#1a0869", fg="white", font=("Arial", 20)).place(x=870, y=10, width=350, height=75)

        tk.Button(self, text="Informações", height=2, command=self.TelaDeRegrasEItens,
                bg="#1a0869", fg="white", font=("Arial", 20)).place(x=1235, y=10, width=350, height=75)

        ### --- Grupos --- ###
        # --- Gerenciamento de Grupos (coluna 1) ---
        self.group_management_frame = tk.Frame(self, bg='#1a0869')
        self.group_management_frame.place(x=20, y=120, width=350, height=80)
        self.create_group_management(self.group_management_frame)

        # --- Lista de Grupos (coluna 1) ---
        self.group_list_frame = tk.Frame(self, bg='#1a0869')
        self.group_list_frame.place(x=20, y=210, width=350, height=470)
        self.create_group_list_section(self.group_list_frame)
        ### --- Grupos --- ###

        ### --- Personagens --- ###
        # --- Gerenciamento de Personagens (coluna 2) ---
        self.char_management_frame = tk.Frame(self, bg='#1a0869')
        self.char_management_frame.place(x=420, y=120, width=350, height=80)
        self.create_char_management(self.char_management_frame)

        # --- Lista de Personagens (coluna 2) ---
        self.char_list_frame = tk.Frame(self, bg='#1a0869')
        self.char_list_frame.place(x=420, y=210, width=350, height=470)
        self.create_list_section(self.char_list_frame)

        # --- Gerenciamento de Kits (coluna 3) ---
        self.kit_management_frame = tk.Frame(self, bg='#1a0869')
        self.kit_management_frame.place(x=820, y=120, width=350, height=80)
        self.create_kit_management(self.kit_management_frame)

        # --- Lista de Kits (coluna 3) ---
        self.kit_list_frame = tk.Frame(self, bg='#1a0869')
        self.kit_list_frame.place(x=820, y=210, width=350, height=470)
        self.create_kit_list_section(self.kit_list_frame)

        # --- Gerenciamento de Items (coluna 4) ---
        self.item_management_frame = tk.Frame(self, bg='#1a0869')
        self.item_management_frame.place(x=1220, y=120, width=350, height=80)

        self.create_item_management(self.item_management_frame)

        # --- Lista de Items (coluna 4) ---
        self.item_list_frame = tk.Frame(self, bg='#1a0869')
        self.item_list_frame.place(x=1220, y=210, width=350, height=470)

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
        title_label = tk.Label(frame, text="Gerenciar Grupos", fg="white", bg="#1a0869", 
                            font=("Arial", 16, "bold"))
        title_label.place(x=10, y=5)

        # Frame para criação de novo grupo
        create_frame = tk.Frame(frame, bg='#1a0869')
        create_frame.place(x=10, y=35, width=330, height=35)

        # Entry para nome do novo grupo
        self.new_group_entry = tk.Entry(create_frame, font=("Arial", 11), bg="white", fg="black")
        self.new_group_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.new_group_entry.insert(0, "Nome do novo grupo...")
        self.new_group_entry.bind("<FocusIn>", self.clear_placeholder)
        self.new_group_entry.bind("<FocusOut>", self.restore_placeholder)

        # Botão de criar grupo
        create_group_btn = tk.Button(create_frame, text="Criar", bg="#006400", fg="white", 
                                    font=("Arial", 10, "bold"), command=self.create_new_group)
        create_group_btn.pack(side="right", padx=2)

    def create_group_list_section(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        label = tk.Label(frame, text="Grupos", fg="white", bg="#1a0869", font=("Arial", 16, "bold"))
        label.place(x=10, y=10)

        canvas_frame = tk.Frame(frame, bg='#1a0869')
        canvas_frame.place(x=10, y=40, width=330, height=420)

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
                grupo_frame.pack(fill="x", pady=2)

                # Contar personagens no grupo
                num_personagens = len(D.GruposDePersonagens.get(grupo, []))
                
                grupo_button = tk.Button(grupo_frame,
                    text=f"{grupo} ({num_personagens} personagens)",
                    bg="#1a0869", fg="white", font=("Arial", 12), anchor="w", justify="left", wraplength=240,
                    command=lambda g=grupo: self.select_group(g), width=28)
                grupo_button.pack(side="left", fill="x", expand=True, padx=(0, 5), ipady=5)

                remove_button = tk.Button(grupo_frame, text="X", bg="red", fg="white", font=("Arial", 12, "bold"),
                    command=lambda g=grupo: self.delete_group(g))
                remove_button.pack(side="right", padx=5, ipady=5)

    def create_list_section(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        # Mostrar grupo selecionado
        grupo_atual = self.group_var.get()
        label = tk.Label(frame, text=f"Personagens - {grupo_atual}", fg="white", bg="#1a0869", font=("Arial", 16, "bold"))
        label.place(x=10, y=10)

        canvas_frame = tk.Frame(frame, bg='#1a0869')
        canvas_frame.place(x=10, y=40, width=330, height=420)

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
                    char_frame.pack(fill="x", pady=2)

                    char_button = tk.Button(char_frame,
                        text=f"{char.nome} - Nível {char.nivel} - XP:{char.XPAtual}/{char.XPlvlUp} - HP:{char.vidaAtual}/{char.vidaMax}",
                        bg="#1a0869", fg="white", font=("Arial", 12), anchor="w", justify="left", wraplength=240,
                        command=lambda c=char: self.controller.abrir_detalhes(c), width=28)
                    char_button.pack(side="left", fill="x", expand=True, padx=(0, 5), ipady=5)

                    remove_button = tk.Button(char_frame, text="X", bg="red", fg="white", font=("Arial", 12, "bold"),
                        command=lambda c=char: self.remove_specific_character(c))
                    remove_button.pack(side="right", padx=5, ipady=5)

            # Adicionar caixa com botões de adicionar/gerar no final
            add_frame = tk.Frame(inner_frame, bg="#2a2647", relief="solid", bd=1, height=60)
            add_frame.pack(fill="x", pady=10)

            add_char_btn = tk.Button(add_frame, text="Adicionar\nPersonagem", bg="#006400", fg="white", 
                                    font=("Arial", 10, "bold"), command=self.add_character_to_current_group)
            add_char_btn.pack(side="left", padx=10, pady=10)

            generate_char_btn = tk.Button(add_frame, text="Gerar\nPersonagem", bg="#0b4f8f", fg="white", 
                                        font=("Arial", 10, "bold"), command=self.gerar_NPC_to_current_group)
            generate_char_btn.pack(side="right", padx=10, pady=10)

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
            title_label = tk.Label(frame, text="Gerenciar Personagens", fg="white", bg="#1a0869", 
                                font=("Arial", 16, "bold"))
            title_label.place(x=10, y=5)

            # Botão de gerar vários
            gerar_varios_btn = tk.Button(frame, text="Gerar vários", bg="#1a0869", fg="white", 
                                        font=("Arial", 12, "bold"), command=self.gerar_grupo_NPCs_to_current_group)
            gerar_varios_btn.place(x=10, y=35, width=100, height=30)

            # Botão de dar kits
            dar_kits_btn = tk.Button(frame, text="Dar kits", bg="#8B4513", fg="white", 
                                    font=("Arial", 12, "bold"), command=self.dar_kits_to_current_group)
            dar_kits_btn.place(x=120, y=35, width=100, height=30)

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

    def gerar_grupo_NPCs_to_current_group(self):
        current_group = self.group_var.get()
        if current_group and current_group != "Sem grupos":
            # Passar o grupo atual diretamente para a função
            self.gerar_grupo_NPCs_with_group(current_group)
        else:
            messagebox.showwarning("Aviso", "Selecione ou crie um grupo primeiro.")

    def add_character_with_group(self, target_group):
        """Adiciona personagem diretamente ao grupo especificado sem mostrar seleção de grupo"""
        popup = tk.Toplevel(self)
        popup.title("Criar Novo Personagem")
        popup.geometry("400x500")
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

                # Cria o personagem com as proficiências padrão
                novo_personagem = CB.Personagem(nome, nivel, Forca, Agilidade, Vigor, Inteligencia, Presenca, Tatica, proficiencias_base=D.Proficiencias)

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
        import random
        from Dados import carregar_tipos_npcs_por_grupo, filtrar_proficiencias

        popup = tk.Toplevel(self)
        popup.title("Gerar NPC")
        popup.geometry("400x300")
        popup.config(bg="#130f26")

        # Mostrar grupo de destino (apenas informativo)
        tk.Label(popup, text=f"Adicionando ao grupo: {target_group}", bg="#130f26", fg="white", 
                font=("Arial", 12, "bold")).pack(pady=10)

        entradas = {}

        # --- Carregar e organizar NPCs por grupo ---
        npcs_por_grupo = carregar_tipos_npcs_por_grupo()
        
        if not npcs_por_grupo:
            messagebox.showerror("Erro", "Não foi possível carregar os tipos de NPCs do banco de dados.")
            popup.destroy()
            return

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
        nivel_entry.insert(0, str(random.randint(1, 5)))
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

                # Buscar NPC base
                npcs_grupo = npcs_por_grupo.get(grupo, [])
                npc_base = next((npc for npc in npcs_grupo if npc["classe"] == classe_nome), None)
                
                if not npc_base:
                    raise ValueError("Classe não encontrada no grupo.")

                # Criar NPC
                npc = CB.NPC(grupo, npc_base["classe"], npc_base["forca"], npc_base["agilidade"],
                        npc_base["vigor"], npc_base["inteligencia"], npc_base["presenca"], npc_base["tatica"])

                # Carregar proficiências
                proficiencias = filtrar_proficiencias()
                
                # Criar personagem
                personagem = CB.Gerador(npc=npc, nivel=nivel, nome=nome, proficiencias_base=proficiencias)

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

    def gerar_grupo_NPCs_with_group(self, target_group):
        """Gera grupo de NPCs diretamente no grupo especificado sem mostrar seleção de grupo"""
        import random

        # Carrega dados dos NPCs
        dados_npcs = D.ler_dados_npcs()
        npcs_por_faccao = {}
        for npc in dados_npcs:
            faccao = npc["grupo"]
            classe = npc["classe"]
            atributos = (
                classe,
                npc["forca"],
                npc["agilidade"],
                npc["vigor"],
                npc["inteligencia"],
                npc["presenca"],
                npc["tatica"]
            )
            if faccao not in npcs_por_faccao:
                npcs_por_faccao[faccao] = []
            npcs_por_faccao[faccao].append(atributos)

        popup = tk.Toplevel()
        popup.title("Gerar Grupo de NPCs")
        popup.configure(bg="#130f26")
        popup.geometry("500x550")

        entradas = {}

        # Cabeçalho com opções iniciais
        header_frame = tk.Frame(popup, bg="#130f26")
        header_frame.pack(pady=10)

        # Mostrar grupo de destino (apenas informativo)
        tk.Label(header_frame, text=f"Adicionando ao grupo: {target_group}", bg="#130f26", fg="white", 
                font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=4, pady=5)

        # Facção
        tk.Label(header_frame, text="Facção:", bg="#130f26", fg="white").grid(row=1, column=0, padx=5, sticky="e")
        faccao_var = tk.StringVar(value=list(npcs_por_faccao.keys())[0])
        faccao_menu = ttk.Combobox(header_frame, textvariable=faccao_var, state="readonly", values=list(npcs_por_faccao.keys()), width=20)
        faccao_menu.grid(row=1, column=1, padx=5)
        entradas["Facção"] = faccao_var

        # Quantidade
        tk.Label(header_frame, text="Quantidade:", bg="#130f26", fg="white").grid(row=1, column=2, padx=5, sticky="e")
        qtd_var = tk.StringVar(value="3")
        qtd_entry = tk.Entry(header_frame, textvariable=qtd_var, width=5, justify="center")
        qtd_entry.grid(row=1, column=3, padx=5)

        # Área scrollável
        canvas_frame = tk.Frame(popup, bg="#130f26")
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame, bg="#130f26", highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#130f26")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        slots = []

        def gerar_slots(npcs_por_faccao=npcs_por_faccao):
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
            slots.clear()

            faccao = faccao_var.get()
            classes_disponiveis = [c[0] for c in npcs_por_faccao.get(faccao, [])]

            try:
                qtd = int(qtd_var.get())
            except:
                tk.messagebox.showerror("Erro", "Valores inválidos.")
                return

            if not classes_disponiveis:
                tk.messagebox.showerror("Erro", f"Nenhuma classe disponível para a facção '{faccao}'.")
                return

            for i in range(qtd):
                slot = {}
                frame = tk.Frame(scrollable_frame, bg="#1f1b3a", bd=1, relief="solid", padx=5, pady=5)
                frame.pack(padx=5, pady=5, fill="x")

                tk.Label(frame, text=f"NPC {i+1}", bg="#1f1b3a", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=6, pady=(0, 5), sticky="w")

                # Classe
                tk.Label(frame, text="Classe", bg="#1f1b3a", fg="white").grid(row=1, column=0, padx=2, sticky="e")
                classe_var = tk.StringVar(value=classes_disponiveis[0])
                classe_menu = ttk.Combobox(frame, textvariable=classe_var, state="readonly", values=classes_disponiveis, width=20)
                classe_menu.grid(row=1, column=1, padx=2)

                # Nível
                tk.Label(frame, text="Nível", bg="#1f1b3a", fg="white").grid(row=1, column=2, padx=2, sticky="e")
                nivel_var = tk.StringVar(value="1")
                nivel_entry = tk.Entry(frame, textvariable=nivel_var, width=5, justify="center")
                nivel_entry.grid(row=1, column=3, padx=2)

                # Nome (opcional)
                tk.Label(frame, text="Nome (opcional)", bg="#1f1b3a", fg="white").grid(row=1, column=4, padx=2, sticky="e")
                nome_var = tk.StringVar(value="")
                nome_entry = tk.Entry(frame, textvariable=nome_var, width=15, justify="center")
                nome_entry.grid(row=1, column=5, padx=2)

                slot.update({
                    "Classe": classe_var,
                    "Nivel": nivel_var,
                    "Nome": nome_var
                })

                slots.append(slot)

        # Atualizar slots automaticamente ao trocar facção
        faccao_var.trace_add("write", lambda *args: gerar_slots(npcs_por_faccao))

        # Botões
        tk.Button(popup, text="Gerar Slots", command=lambda:gerar_slots(npcs_por_faccao), font=("Arial", 11), bg="#0b4f8f", fg="white").pack(pady=(10, 10))
        tk.Button(popup, text="Confirmar Geração", command=lambda: self.confirmar_geracao_with_group(slots, entradas, npcs_por_faccao, target_group), font=("Arial", 11), bg="#1a7837", fg="white").pack(pady=(0, 10))

    def confirmar_geracao_with_group(self, slots, entradas, npcs_por_faccao, target_group):
        """Confirma a geração de NPCs para um grupo específico"""
        import random
        try:
            faccao = entradas["Facção"].get()

            # Carregar os NPCs do JSON
            npcs_disponiveis = D.carregar_npcs_json()

            for i, slot in enumerate(slots):
                classe_nome = slot["Classe"].get()
                nivel = int(slot["Nivel"].get())
                nome_customizado = slot["Nome"].get().strip()

                # Buscar NPC correspondente pela facção e classe
                npc_dict = next((n for n in npcs_disponiveis if n['faccao'] == faccao and n['classe'] == classe_nome), None)
                if not npc_dict:
                    raise ValueError(f"Classe '{classe_nome}' não encontrada na facção '{faccao}'.")

                npc_base = CB.NPC(
                    faccao=npc_dict['faccao'],
                    classe=npc_dict['classe'],
                    forca=int(npc_dict['forca']),
                    agilidade=int(npc_dict['agilidade']),
                    vigor=int(npc_dict['vigor']),
                    inteligencia=int(npc_dict['inteligencia']),
                    presenca=int(npc_dict['presenca']),
                    tatica=int(npc_dict['tatica'])
                )

                # Definir nome
                nome = nome_customizado if nome_customizado else f"{classe_nome}_{random.randint(1, 99)}"

                # Criar personagem
                personagem = CB.Gerador(npc=npc_base, kit=None, nivel=nivel, nome=nome, proficiencias_base=D.Proficiencias)

                # Pós-processamento
                self.carregar_armas_e_armaduras(personagem)

                # Adicionar ao grupo especificado
                if target_group in D.GruposDePersonagens:
                    D.GruposDePersonagens[target_group].append(personagem)
                else:
                    raise ValueError(f"Grupo de destino '{target_group}' não encontrado.")

            self.refresh()
            tk.messagebox.showinfo("Sucesso", "NPCs gerados com sucesso!")

        except Exception as e:
            tk.messagebox.showerror("Erro", f"Ocorreu um erro ao gerar os NPCs:\n{e}")

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
    def clear_kit_placeholder(self, event):
        if self.new_kit_entry.get() == "Nome do novo kit...":
            self.new_kit_entry.delete(0, tk.END)
            self.new_kit_entry.config(fg="black")

    def restore_kit_placeholder(self, event):
        if not self.new_kit_entry.get():
            self.new_kit_entry.insert(0, "Nome do novo kit...")
            self.new_kit_entry.config(fg="gray")

    def create_kit_management(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        # Título
        title_label = tk.Label(frame, text="Gerenciar Kits", fg="white", bg="#1a0869", 
                            font=("Arial", 16, "bold"))
        title_label.place(x=10, y=5)

        # Frame para criação de novo kit
        create_frame = tk.Frame(frame, bg='#1a0869')
        create_frame.place(x=10, y=35, width=330, height=35)

        # Entry para nome do novo kit
        self.new_kit_entry = tk.Entry(create_frame, font=("Arial", 11), bg="white", fg="black")
        self.new_kit_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.new_kit_entry.insert(0, "Nome do novo kit...")
        self.new_kit_entry.bind("<FocusIn>", self.clear_kit_placeholder)
        self.new_kit_entry.bind("<FocusOut>", self.restore_kit_placeholder)

        # Botão de criar kit
        create_kit_btn = tk.Button(create_frame, text="Criar", bg="#006400", fg="white", 
                                  font=("Arial", 10, "bold"), command=self.create_new_kit)
        create_kit_btn.pack(side="right", padx=2)

        #info_label = tk.Label(frame, text="Kits pré-definidos do sistema", fg="gray", bg="#1a0869", 
        #                font=("Arial", 12, "italic"))
        #info_label.place(x=10, y=35)

    def create_kit_list_section(self, frame):
        """Versão atualizada que mostra resumo dos kits"""
        for widget in frame.winfo_children():
            widget.destroy()

        label = tk.Label(frame, text="Kits", fg="white", bg="#1a0869", font=("Arial", 16, "bold"))
        label.place(x=10, y=10)

        canvas_frame = tk.Frame(frame, bg='#1a0869')
        canvas_frame.place(x=10, y=40, width=330, height=420)

        canvas = tk.Canvas(canvas_frame, bg="#1a0869", highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner_frame = tk.Frame(canvas, bg="#1a0869")
        canvas.create_window((0, 0), window=inner_frame, anchor='nw')
        inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        if not hasattr(D, 'KitsDisponíveis'):
            D.KitsDisponíveis = {}
        
        kits = list(D.KitsDisponíveis.keys())
        
        if not kits:
            empty_label = tk.Label(inner_frame, text="Nenhum kit disponível", 
                                fg="gray", bg="#1a0869", font=("Arial", 12, "italic"))
            empty_label.pack(pady=20)
        else:
            for kit in kits:
                kit_frame = tk.Frame(inner_frame, bg="#1a0869", height=60)
                kit_frame.pack(fill="x", pady=2)
                
                kit_button = tk.Button(kit_frame,
                    text=kit,
                    bg="#1a0869", fg="white", font=("Arial", 12), anchor="w", justify="left", wraplength=240,
                    command=lambda k=kit: self.select_kit(k), width=28)
                kit_button.pack(side="left", fill="x", expand=True, padx=(0, 5), ipady=5)

                # Botão de excluir
                remove_button = tk.Button(kit_frame, text="X", bg="red", fg="white", font=("Arial", 12, "bold"),
                    command=lambda k=kit: self.delete_kit(k))
                remove_button.pack(side="right", padx=5, ipady=5)

    def select_kit(self, kit_name):
        """Seleciona um kit e atualiza a interface"""
        self.kit_var.set(kit_name)
        self.refresh_items()

    def delete_kit(self, kit_name):
        """Exclui um kit específico"""
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir o kit '{kit_name}'?\n\nTodos os items do kit serão perdidos!"):
            # Remover kit do dicionário local
            if hasattr(D, 'KitsDisponíveis') and kit_name in D.KitsDisponíveis:
                del D.KitsDisponíveis[kit_name]
                
                # Se o kit excluído era o selecionado, selecionar outro
                if self.kit_var.get() == kit_name:
                    remaining_kits = list(D.KitsDisponíveis.keys()) if D.KitsDisponíveis else []
                    if remaining_kits:
                        self.kit_var.set(remaining_kits[0])
                    else:
                        self.kit_var.set("Sem kits")
                
                self.refresh_kits()
                messagebox.showinfo("Sucesso", f"Kit '{kit_name}' excluído com sucesso!")
            else:
                messagebox.showerror("Erro", "Erro ao excluir o kit.")

    def create_new_kit(self):
        """Cria um novo kit vazio"""
        kit_name = self.new_kit_entry.get().strip()
        
        # Validar nome do kit
        if not kit_name or kit_name == "Nome do novo kit...":
            messagebox.showwarning("Aviso", "Por favor, digite um nome para o kit.")
            return
        
        # Verificar se D.KitsDisponíveis existe, senão criar
        if not hasattr(D, 'KitsDisponíveis'):
            D.KitsDisponíveis = {}
        
        # Verificar se o kit já existe
        if kit_name in D.KitsDisponíveis:
            messagebox.showwarning("Aviso", "Este kit já existe.")
            return
        
        # Criar kit vazio com estrutura padrão
        D.KitsDisponíveis[kit_name] = {
            "Armas Brancas": [],
            "Armas de Fogo": [],
            "Proteções": [],
            "Itens": [],
            "Consumíveis": [],
            "Explosivos": [],
            "Munições": [],
            "Melhorias": []
        }
        
        # Limpar campo de entrada
        self.new_kit_entry.delete(0, tk.END)
        self.new_kit_entry.insert(0, "Nome do novo kit...")
        self.new_kit_entry.config(fg="gray")
        
        # Selecionar o novo kit
        self.kit_var.set(kit_name)
        
        # Atualizar interface
        self.refresh_kits()
        
        messagebox.showinfo("Sucesso", f"Kit '{kit_name}' criado com sucesso!")

    def clear_all_items_from_kit(self):
        """Remove todos os itens do kit selecionado"""
        current_kit = self.kit_var.get()
        
        if current_kit == "Sem kits":
            messagebox.showwarning("Aviso", "Selecione um kit primeiro.")
            return
        
        if not hasattr(D, 'KitsDisponíveis') or current_kit not in D.KitsDisponíveis:
            messagebox.showwarning("Aviso", "Kit não encontrado.")
            return
        
        # Contar total de itens
        total_itens = sum(len(categoria) for categoria in D.KitsDisponíveis[current_kit].values())
        
        if total_itens == 0:
            messagebox.showinfo("Info", "O kit já está vazio.")
            return
        
        # Confirmar ação
        if messagebox.askyesno("Confirmar", 
                            f"Tem certeza que deseja excluir todos os {total_itens} itens do kit '{current_kit}'?\n\n"
                            "Esta ação não pode ser desfeita!"):
            # Limpar todas as categorias
            for categoria in D.KitsDisponíveis[current_kit].keys():
                D.KitsDisponíveis[current_kit][categoria].clear()
            
            self.refresh_items()
            messagebox.showinfo("Sucesso", f"Todos os itens foram removidos do kit '{current_kit}'!")

    def validate_kit_name(self, kit_name):
        """Valida se o nome do kit é válido"""
        if not kit_name or kit_name.isspace():
            return False, "Nome do kit não pode estar vazio."
        
        if len(kit_name) > 50:
            return False, "Nome do kit muito longo (máximo 50 caracteres)."
        
        # Caracteres proibidos
        forbidden_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        if any(char in kit_name for char in forbidden_chars):
            return False, "Nome do kit contém caracteres inválidos."
        
        return True, ""

    def refresh_kits(self):
        """Atualiza a lista de kits"""
        self.create_kit_list_section(self.kit_list_frame)
        self.create_item_list_section(self.item_list_frame)

    def dar_kits_to_current_group(self):
        current_group = self.group_var.get()
        if current_group and current_group != "Sem grupos":
            self.show_dar_kits_popup(current_group)
        else:
            messagebox.showwarning("Aviso", "Selecione um grupo primeiro.")

    def show_dar_kits_popup(self, group_name):
        """Mostra popup para dar kits aos personagens do grupo"""
        # Verificar se há personagens no grupo
        personagens = D.GruposDePersonagens.get(group_name, [])
        if not personagens:
            messagebox.showinfo("Info", "Não há personagens neste grupo.")
            return

        # Verificar se há kits disponíveis
        if not hasattr(D, 'KitsDisponíveis') or not D.KitsDisponíveis:
            messagebox.showwarning("Aviso", "Não há kits disponíveis no sistema.")
            return

        popup = tk.Toplevel(self)
        popup.title(f"Dar Kits - Grupo: {group_name}")
        popup.geometry("600x500")
        popup.config(bg="#130f26")
        popup.grab_set()  # Torna o popup modal

        # --- HEADER ---
        header_frame = tk.Frame(popup, bg="#130f26")
        header_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(header_frame, text=f"Dar Kits aos Personagens - {group_name}", 
                fg="white", bg="#130f26", font=("Arial", 16, "bold")).pack()

        # --- ÁREA SCROLLÁVEL ---
        canvas_frame = tk.Frame(popup, bg="#130f26")
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = tk.Canvas(canvas_frame, bg="#1a0869", highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a0869")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Lista de kits disponíveis
        kits_disponiveis = ["Nenhum"] + list(D.KitsDisponíveis.keys())
        
        # Dicionário para armazenar as seleções de kit para cada personagem
        kit_selections = {}

        # Criar uma linha para cada personagem
        for i, personagem in enumerate(personagens):
            if isinstance(personagem, CB.Personagem):
                char_frame = tk.Frame(scrollable_frame, bg="#2a2647", relief="solid", bd=1)
                char_frame.pack(fill="x", pady=5, padx=10)

                # Nome do personagem
                name_frame = tk.Frame(char_frame, bg="#2a2647")
                name_frame.pack(fill="x", padx=10, pady=5)

                tk.Label(name_frame, text=f"{personagem.nome} - Nível {personagem.nivel}", 
                        fg="white", bg="#2a2647", font=("Arial", 12, "bold")).pack(side="left")

                # Seleção de kit
                kit_frame = tk.Frame(char_frame, bg="#2a2647")
                kit_frame.pack(fill="x", padx=10, pady=(0, 10))

                tk.Label(kit_frame, text="Kit:", fg="white", bg="#2a2647", 
                        font=("Arial", 11)).pack(side="left", padx=(0, 10))

                kit_var = tk.StringVar(value="Nenhum")
                kit_menu = ttk.Combobox(kit_frame, textvariable=kit_var, 
                                    state="readonly", values=kits_disponiveis, width=25)
                kit_menu.pack(side="left")

                kit_selections[personagem] = kit_var

        def confirmar_kits():
            """Confirma e aplica os kits selecionados"""
            try:
                kits_aplicados = 0
                kits_com_erro = 0
                relatorio_detalhado = []
                
                for personagem, kit_var in kit_selections.items():
                    kit_selecionado = kit_var.get()
                    
                    if kit_selecionado != "Nenhum":
                        # Entregar o kit
                        if self.entregar_kit_para_personagem(kit_selecionado, personagem):
                            kits_aplicados += 1
                            # Contar itens do kit
                            kit_data = D.KitsDisponíveis[kit_selecionado]
                            total_itens = sum(sum(item.get('quantidade', 1) for item in categoria) for categoria in kit_data.values())
                            relatorio_detalhado.append(f"✅ {personagem.nome}: Kit '{kit_selecionado}' entregue ({total_itens} itens)")
                        else:
                            relatorio_detalhado.append(f"❌ {personagem.nome}: Erro ao entregar kit '{kit_selecionado}'")
                            kits_com_erro += 1
                
                popup.destroy()
                
                # Montar mensagem final
                if kits_aplicados > 0 or kits_com_erro > 0:
                    mensagem_final = f"RELATÓRIO DE ENTREGA DE KITS\n\n"
                    mensagem_final += f"✅ Kits entregues com sucesso: {kits_aplicados}\n"
                    if kits_com_erro > 0:
                        mensagem_final += f"❌ Kits com erro: {kits_com_erro}\n"
                    mensagem_final += "\nDetalhes:\n"
                    mensagem_final += "\n".join(relatorio_detalhado)
                    
                    if kits_aplicados > 0:
                        messagebox.showinfo("Relatório de Entrega", mensagem_final)
                        self.refresh()  # Atualizar a interface
                    else:
                        messagebox.showwarning("Relatório de Entrega", mensagem_final)
                else:
                    messagebox.showinfo("Info", "Nenhum kit foi selecionado para entrega.")
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao processar kits:\n{e}")

        # --- BOTÕES ---
        button_frame = tk.Frame(popup, bg="#130f26")
        button_frame.pack(fill="x", padx=10, pady=10)

        tk.Button(button_frame, text="Cancelar", command=popup.destroy, 
                bg="#8B0000", fg="white", font=("Arial", 12), width=15).pack(side="left")

        tk.Button(button_frame, text="Confirmar", command=confirmar_kits, 
                bg="#006400", fg="white", font=("Arial", 12), width=15).pack(side="right")

    def entregar_kit_para_personagem(self, kit_name, personagem):
        """Entrega um kit para um personagem, criando novos itens no inventário baseado nos índices"""
        try:
            if kit_name not in D.KitsDisponíveis:
                print(f"Kit '{kit_name}' não encontrado")
                return False
            
            kit_data = D.KitsDisponíveis[kit_name]
            
            # Mapeamento das tabelas para os pools de dados
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
            
            # Processar cada categoria do kit
            for categoria, itens_indices in kit_data.items():
                for item_indice in itens_indices:
                    nome_item = item_indice.get('nome')
                    tabela = item_indice.get('tabela')
                    quantidade = item_indice.get('quantidade', 1)
                    
                    if not nome_item or not tabela:
                        print(f"Índice inválido encontrado: {item_indice}")
                        continue
                    
                    # Verificar se a tabela existe no mapeamento
                    if tabela not in mapeamento_tabelas:
                        print(f"Tabela '{tabela}' não encontrada no mapeamento")
                        continue
                    
                    pool_nome = mapeamento_tabelas[tabela]
                    
                    # Verificar se o pool existe
                    if not hasattr(D, 'Pools') or pool_nome not in D.Pools:
                        print(f"Pool '{pool_nome}' não encontrado")
                        continue
                    
                    pool_items = D.Pools[pool_nome]
                    
                    # Verificar se o item existe no pool
                    if nome_item not in pool_items:
                        print(f"Item '{nome_item}' não encontrado no pool '{pool_nome}'")
                        continue
                    
                    # Obter o item do pool e criar nova instância
                    item_template = pool_items[nome_item]
                    
                    # Criar nova instância do item
                    if callable(item_template):
                        item_obj = item_template()
                    else:
                        # Se não é callable, criar nova instância baseada na classe
                        item_obj = item_template.__class__()
                        # Copiar atributos do template
                        for attr_name, attr_value in item_template.__dict__.items():
                            setattr(item_obj, attr_name, attr_value)
                    
                    # Adicionar ao inventário do personagem
                    personagem.inventario.gerenciar_item(
                        item_objeto=item_obj, 
                        quantidade=quantidade, 
                        operacao="adicionar"
                    )
            
            return True
            
        except Exception as e:
            print(f"Erro ao entregar kit '{kit_name}': {e}")

    def recriar_item_do_indice(self, nome_item, classe_item):
            """Recria um item a partir do nome e classe, procurando nos pools"""
            try:
                # Procurar o item nos pools
                for pool_name, pool_items in D.Pools.items():
                    if nome_item in pool_items:
                        item_original = pool_items[nome_item]
                        # Verificar se a classe confere
                        if item_original.__class__.__name__ == classe_item:
                            # Retornar uma nova instância do item
                            return item_original.__class__(**item_original.__dict__)
                
                return None
                
            except Exception as e:
                print(f"Erro ao recriar item {nome_item}: {e}")
                return None
### --- Kits --- ###

### --- Itens --- ###
    def create_item_list_section(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        # Mostrar kit selecionado
        kit_atual = self.kit_var.get()
        label = tk.Label(frame, text=f"Items - {kit_atual}", fg="white", bg="#1a0869", font=("Arial", 16, "bold"))
        label.place(x=10, y=10)

        canvas_frame = tk.Frame(frame, bg='#1a0869')
        canvas_frame.place(x=10, y=40, width=330, height=420)

        canvas = tk.Canvas(canvas_frame, bg="#1a0869", highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner_frame = tk.Frame(canvas, bg="#1a0869")
        canvas.create_window((0, 0), window=inner_frame, anchor='nw')
        inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Verificar se D.KitsDisponíveis existe
        if not hasattr(D, 'KitsDisponíveis'):
            D.KitsDisponíveis = {}

        kit = self.kit_var.get()
        
        if kit == "Sem kits":
            empty_label = tk.Label(inner_frame, text="Selecione um kit para ver os items", 
                                fg="gray", bg="#1a0869", font=("Arial", 12, "italic"))
            empty_label.pack(pady=20)
        else:
            # Obter itens do kit como índices
            kit_data = D.KitsDisponíveis.get(kit, {})
            
            if not kit_data:
                empty_label = tk.Label(inner_frame, text="Este kit está vazio", 
                                    fg="gray", bg="#1a0869", font=("Arial", 12, "italic"))
                empty_label.pack(pady=20)
            else:
                # Mostrar items por categoria
                for categoria, itens in kit_data.items():
                    if itens:  # Só mostra categorias com itens
                        # Título da categoria
                        categoria_label = tk.Label(inner_frame, text=f"=== {categoria} ===", 
                                                fg="yellow", bg="#1a0869", font=("Arial", 12, "bold"))
                        categoria_label.pack(pady=(10, 5))
                        
                        # Itens da categoria (como índices)
                        for item_indice in itens:
                            item_frame = tk.Frame(inner_frame, bg="#1a0869", height=60)
                            item_frame.pack(fill="x", pady=2)

                            # Exibir apenas nome e quantidade (simplificado)
                            nome = item_indice.get('nome', 'Item desconhecido')
                            quantidade = item_indice.get('quantidade', 1)
                            
                            item_text = f"{nome} (x{quantidade})"

                            item_label = tk.Label(item_frame,
                                text=item_text,
                                bg="#1a0869", fg="white", font=("Arial", 12), anchor="w", justify="left")
                            item_label.pack(side="left", fill="x", expand=True, padx=(0, 5), ipady=5)

                            # Adicionar botão de remover
                            remove_button = tk.Button(item_frame, text="X", bg="red", fg="white", font=("Arial", 12, "bold"),
                                command=lambda i=item_indice, cat=categoria: self.remove_item_from_kit(i, cat))
                            remove_button.pack(side="right", padx=5, ipady=5)

            # Adicionar caixa com botão de adicionar item no final
            add_frame = tk.Frame(inner_frame, bg="#2a2647", relief="solid", bd=1, height=60)
            add_frame.pack(fill="x", pady=10)

            add_item_btn = tk.Button(add_frame, text="Adicionar\nItem", bg="#006400", fg="white", 
                                    font=("Arial", 10, "bold"), command=self.add_item_to_current_kit)
            add_item_btn.pack(side="left", padx=10, pady=10)

    def create_item_management(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        # Título
        title_label = tk.Label(frame, text="Gerenciar Items", fg="white", bg="#1a0869", 
                            font=("Arial", 16, "bold"))
        title_label.place(x=10, y=5)

        # Botão de excluir todos os items
        clear_all_btn = tk.Button(frame, text="Excluir Todos", bg="#8B0000", fg="white", 
                                font=("Arial", 12, "bold"), command=self.clear_all_items_from_kit)
        clear_all_btn.place(x=10, y=35, width=120, height=30)

        #info_label = tk.Label(frame, text="Visualização dos itens do kit", fg="gray", bg="#1a0869", 
        #                font=("Arial", 12, "italic"))
        #info_label.place(x=10, y=35)

    def clear_all_items_from_kit(self):
        """Remove todos os itens do kit selecionado"""
        current_kit = self.kit_var.get()
        
        if current_kit == "Sem kits":
            messagebox.showwarning("Aviso", "Selecione um kit primeiro.")
            return
        
        if not hasattr(D, 'KitsDisponíveis') or current_kit not in D.KitsDisponíveis:
            messagebox.showwarning("Aviso", "Kit não encontrado.")
            return
        
        # Contar total de itens
        total_itens = sum(len(categoria) for categoria in D.KitsDisponíveis[current_kit].values())
        
        if total_itens == 0:
            messagebox.showinfo("Info", "O kit já está vazio.")
            return
        
        # Confirmar ação
        if messagebox.askyesno("Confirmar", 
                            f"Tem certeza que deseja excluir todos os {total_itens} itens do kit '{current_kit}'?\n\n"
                            "Esta ação não pode ser desfeita!"):
            # Limpar todas as categorias
            for categoria in D.KitsDisponíveis[current_kit].keys():
                D.KitsDisponíveis[current_kit][categoria].clear()
            
            # Salvar no banco
            D.salvar_kits_no_supabase()
            
            self.refresh_items()
            messagebox.showinfo("Sucesso", f"Todos os itens foram removidos do kit '{current_kit}'!")

    def show_item_selection_popup(self, kit_name):
        """Mostra popup para seleção de item"""
        popup = tk.Toplevel(self)
        popup.title("Adicionar Item ao Kit")
        popup.geometry("600x700")
        popup.config(bg="#130f26")
        popup.grab_set()  # Torna o popup modal

        # Carrega os pools de dados
        if not hasattr(D, 'Pools') or not D.Pools:
            messagebox.showerror("Erro", "Pools de dados não carregados!")
            popup.destroy()
            return

        # Variáveis de controle
        selected_item = {"item": None, "pool": None}
        
        # --- HEADER ---
        header_frame = tk.Frame(popup, bg="#130f26")
        header_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(header_frame, text=f"Adicionar Item ao Kit: {kit_name}", 
                fg="white", bg="#130f26", font=("Arial", 16, "bold")).pack()

        # --- SELEÇÃO DE CATEGORIA ---
        category_frame = tk.Frame(popup, bg="#130f26")
        category_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(category_frame, text="Categoria:", fg="white", bg="#130f26", 
                font=("Arial", 12)).pack(side="left")

        categories = list(D.Pools.keys())
        category_var = tk.StringVar(value=categories[0] if categories else "")
        category_menu = ttk.Combobox(category_frame, textvariable=category_var, 
                                state="readonly", values=categories, width=20)
        category_menu.pack(side="left", padx=10)

        # --- BUSCA ---
        search_frame = tk.Frame(popup, bg="#130f26")
        search_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(search_frame, text="Buscar:", fg="white", bg="#130f26", 
                font=("Arial", 12)).pack(side="left")

        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, width=30)
        search_entry.pack(side="left", padx=10)

        # --- LISTA DE ITENS ---
        list_frame = tk.Frame(popup, bg="#130f26")
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Canvas com scrollbar
        canvas = tk.Canvas(list_frame, bg="#1a0869", highlightthickness=0)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a0869")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- QUANTIDADE ---
        quantity_frame = tk.Frame(popup, bg="#130f26")
        quantity_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(quantity_frame, text="Quantidade:", fg="white", bg="#130f26", 
                font=("Arial", 12)).pack(side="left")

        quantity_var = tk.StringVar(value="1")
        quantity_entry = tk.Entry(quantity_frame, textvariable=quantity_var, width=10)
        quantity_entry.pack(side="left", padx=10)

        def update_item_list():
            """Atualiza a lista de itens baseada na categoria e busca"""
            for widget in scrollable_frame.winfo_children():
                widget.destroy()

            category = category_var.get()
            search_term = search_var.get().lower()

            if not category or category not in D.Pools:
                return

            items = D.Pools[category]
            
            # Filtrar por termo de busca se fornecido
            if search_term:
                items = {name: item for name, item in items.items() 
                        if search_term in name.lower()}

            if not items:
                no_items_label = tk.Label(scrollable_frame, text="Nenhum item encontrado", 
                                        fg="gray", bg="#1a0869", font=("Arial", 12))
                no_items_label.pack(pady=20)
                return

            # Criar botões para cada item
            for item_name, item_obj in items.items():
                item_frame = tk.Frame(scrollable_frame, bg="#1a0869", relief="solid", bd=1)
                item_frame.pack(fill="x", pady=2, padx=5)

                # Informações do item
                info_text = item_name
                if hasattr(item_obj, 'dano'):
                    info_text += f" | Dano: {item_obj.dano}"
                if hasattr(item_obj, 'protecao'):
                    info_text += f" | Proteção: {item_obj.protecao}"
                if hasattr(item_obj, 'preco'):
                    info_text += f" | Preço: {item_obj.preco}"

                item_button = tk.Button(item_frame, text=info_text, 
                                    bg="#2a2647", fg="white", font=("Arial", 11),
                                    anchor="w", justify="left",
                                    command=lambda name=item_name, obj=item_obj, pool=category: 
                                    select_item(name, obj, pool))
                item_button.pack(fill="x", padx=5, pady=2)

        def select_item(item_name, item_obj, pool_name):
            """Seleciona um item"""
            selected_item["item"] = item_obj
            selected_item["pool"] = pool_name
            selected_item["name"] = item_name

            # Atualizar interface para mostrar seleção
            for widget in scrollable_frame.winfo_children():
                for child in widget.winfo_children():
                    if isinstance(child, tk.Button):
                        if child.cget("text").startswith(item_name):
                            child.config(bg="#006400")  # Verde para selecionado
                        else:
                            child.config(bg="#2a2647")  # Cor normal

        def confirm_add(self):
            """Confirma a adição do item ao kit - função dentro do popup"""
            if not selected_item["item"]:
                messagebox.showwarning("Aviso", "Selecione um item primeiro!")
                return

            # Validar quantidade
            try:
                quantidade = int(quantity_var.get())
                if quantidade <= 0:
                    messagebox.showwarning("Aviso", "Quantidade deve ser maior que 0!")
                    return
            except ValueError:
                messagebox.showwarning("Aviso", "Quantidade deve ser um número válido!")
                return

            # Determinar categoria do item baseado no pool
            categoria_map = {
                "Ranged": "Armas de Fogo",
                "Melee": "Armas Brancas", 
                "Protecao": "Proteções",
                "Item": "Itens",
                "Consumivel": "Consumíveis",
                "Explosivo": "Explosivos",
                "Municao": "Munições",
                "Melhoria": "Melhorias"
            }
            
            categoria = categoria_map.get(selected_item["pool"], "Itens")
            
            # Mapear pool para tabela
            tabela_map = {
                "Ranged": "Rangeds",
                "Melee": "Melees",
                "Protecao": "Protecoes", 
                "Item": "Itens",
                "Consumivel": "Consumiveis",
                "Explosivo": "Explosivos",
                "Municao": "Municoes",
                "Melhoria": "Melhorias"
            }
            
            tabela = tabela_map.get(selected_item["pool"], "Itens")
            
            # Criar índice do item (apenas nome, tabela e quantidade)
            item_indice = {
                "nome": selected_item["name"],
                "tabela": tabela,
                "quantidade": quantidade
            }
            
            # Verificar se o kit existe
            if kit_name not in D.KitsDisponíveis:
                messagebox.showerror("Erro", "Kit não encontrado!")
                return
            
            # Verificar se a categoria existe no kit
            if categoria not in D.KitsDisponíveis[kit_name]:
                D.KitsDisponíveis[kit_name][categoria] = []
            
            # Verificar se o item já existe no kit (mesmo nome e tabela)
            item_existente = None
            for item in D.KitsDisponíveis[kit_name][categoria]:
                if item.get("nome") == selected_item["name"] and item.get("tabela") == tabela:
                    item_existente = item
                    break
            
            if item_existente:
                # Se já existe, aumentar a quantidade
                item_existente["quantidade"] = item_existente.get("quantidade", 1) + quantidade
                mensagem = f"Quantidade de '{selected_item['name']}' aumentada para {item_existente['quantidade']}!"
            else:
                # Se não existe, adicionar novo índice
                D.KitsDisponíveis[kit_name][categoria].append(item_indice)
                mensagem = f"{quantidade}x '{selected_item['name']}' adicionado(s) ao kit na categoria '{categoria}'!"
            
            messagebox.showinfo("Sucesso", mensagem)
            
            # Limpar seleção
            selected_item["item"] = None
            selected_item["pool"] = None
            selected_item["name"] = None
            quantity_var.set("1")
            
            # Resetar cores dos botões
            for widget in scrollable_frame.winfo_children():
                for child in widget.winfo_children():
                    if isinstance(child, tk.Button):
                        child.config(bg="#2a2647")
                        
            self.refresh_items()

        # --- BOTÕES ---
        button_frame = tk.Frame(popup, bg="#130f26")
        button_frame.pack(fill="x", padx=10, pady=10)

        tk.Button(button_frame, text="Cancelar", command=popup.destroy, 
                bg="#8B0000", fg="white", font=("Arial", 12), width=15).pack(side="left")

        tk.Button(button_frame, text="Adicionar ao Kit", command=confirm_add, 
                bg="#006400", fg="white", font=("Arial", 12), width=15).pack(side="right")

        # --- BIND EVENTS ---
        category_var.trace("w", lambda *args: update_item_list())
        search_var.trace("w", lambda *args: update_item_list())

        # Inicializar lista
        update_item_list()

    def add_item_to_current_kit(self):
        """Adiciona um item ao kit atualmente selecionado"""
        current_kit = self.kit_var.get()
        
        if current_kit == "Sem kits":
            messagebox.showwarning("Aviso", "Selecione um kit primeiro.")
            return
        
        if not hasattr(D, 'KitsDisponíveis') or current_kit not in D.KitsDisponíveis:
            messagebox.showwarning("Aviso", "Kit não encontrado.")
            return
        
        # Mostrar popup de seleção de item
        self.show_item_selection_popup(current_kit)

    def remove_item_from_kit(self, item_indice, categoria):
        """Remove um item específico do kit"""
        selected_kit = self.kit_var.get()
        
        if selected_kit not in D.KitsDisponíveis:
            return
        
        if categoria not in D.KitsDisponíveis[selected_kit]:
            return
        
        # Remover o item índice da lista
        try:
            D.KitsDisponíveis[selected_kit][categoria].remove(item_indice)
            self.refresh_items()
        except ValueError:
            pass

    def view_item_details(self, item_indice):
        """Visualizar detalhes do item índice"""
        nome = item_indice.get('nome', 'Desconhecido')
        classe = item_indice.get('classe', 'Desconhecida')
        quantidade = item_indice.get('quantidade', 1)
        
        details = f"Item: {nome}\n"
        details += f"Classe: {classe}\n"
        details += f"Quantidade: {quantidade}\n"
        
        messagebox.showinfo("Detalhes do Item", details)

    def refresh_items(self, *args):
        """Atualiza apenas a lista de items"""
        self.create_item_list_section(self.item_list_frame)
### --- Itens --- ###

# --- Refresh --- #
    def refresh_all(self):
        """Atualiza todas as listas"""
        self.create_group_list_section(self.group_list_frame)
        self.create_list_section(self.char_list_frame)
        self.create_kit_list_section(self.kit_list_frame)
        self.create_item_management(self.item_management_frame)
        self.create_item_list_section(self.item_list_frame)

    def refresh(self, *args):
        self.refresh_all()
# --- Refresh --- #

# --- Criação e Geração de personagens --- #
    def add_character(self, title):
        # Verificar se existem grupos disponíveis
        grupos_disponiveis = list(D.GruposDePersonagens.keys())
        
        if not grupos_disponiveis:
            messagebox.showwarning("Aviso", "Nenhum grupo disponível!\n\nCrie um grupo primeiro antes de adicionar personagens.")
            return
        
        popup = tk.Toplevel(self)
        popup.title("Criar Novo Personagem")
        popup.geometry("400x550")
        popup.config(bg="#130f26")

        # Usar self.group_var ao invés de criar uma nova variável local
        tk.Label(popup, text="Inserir em:", bg="#130f26", fg="white", font=("Arial", 12)).pack(pady=(10, 0))

        # Modificando o Combobox para usar self.group_var e valores corretos
        lista_menu = ttk.Combobox(popup, textvariable=self.group_var, state="readonly", 
                                values=grupos_disponiveis, font=("Arial", 11))
        lista_menu.pack(pady=(0, 10))

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

                # Cria o personagem com as proficiências padrão (todas com valor 0)
                novo_personagem = CB.Personagem(nome, nivel, Forca, Agilidade, Vigor, Inteligencia, Presenca, Tatica, proficiencias_base=D.Proficiencias)

                destino = self.group_var.get()
                if destino in D.GruposDePersonagens:
                    D.GruposDePersonagens[destino].append(novo_personagem)

                popup.destroy()
                self.refresh()
            except ValueError:
                messagebox.showerror("Erro", "Preencha todos os campos corretamente!")

        tk.Button(popup, text="Confirmar", command=confirmar, bg="#1a0869", fg="white", font=("Arial", 14), width=20).pack(pady=20)

    def remove_specific_character(self, character):
        selected_group = self.group_var.get()
        print(f"Removendo personagem: {character.nome} do grupo {selected_group}")
        
        if selected_group in D.GruposDePersonagens:
            try:
                D.GruposDePersonagens[selected_group].remove(character)
            except ValueError:
                print("Personagem não encontrado no grupo.")
        
        self.refresh()

    def gerar_NPC(self, title):
        import random
        import tkinter as tk
        from tkinter import ttk, messagebox
        from Dados import carregar_tipos_npcs_por_grupo, filtrar_proficiencias, GruposDePersonagens

        # Verificar se existem grupos disponíveis em D.GruposDePersonagens
        grupos_disponiveis = list(D.GruposDePersonagens.keys())
        
        if not grupos_disponiveis:
            messagebox.showwarning("Aviso", "Nenhum grupo disponível!\n\nCrie um grupo primeiro antes de gerar NPCs.")
            return

        popup = tk.Toplevel(self)
        popup.title("Gerar NPC")
        popup.geometry("400x350")
        popup.config(bg="#130f26")

        entradas = {}

        # --- Carregar e organizar NPCs por grupo (usando banco de dados) ---
        npcs_por_grupo = carregar_tipos_npcs_por_grupo()
        
        if not npcs_por_grupo:
            messagebox.showerror("Erro", "Não foi possível carregar os tipos de NPCs do banco de dados.")
            popup.destroy()
            return

        # --- Grupo de Destino (usar D.GruposDePersonagens) ---
        tk.Label(popup, text="Inserir em:", bg="#130f26", fg="white", font=("Arial", 12)).pack(pady=(10, 0))
        grupo_destino_var = tk.StringVar(value=grupos_disponiveis[0])
        grupo_destino_menu = ttk.Combobox(popup, textvariable=grupo_destino_var, state="readonly",
                                        values=grupos_disponiveis, font=("Arial", 11))
        grupo_destino_menu.pack(pady=(0, 10))
        entradas["GrupoDestino"] = grupo_destino_var

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
            classes = [npc["classe"] for npc in npcs_grupo]  # Agora é dict, não objeto
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
        nivel_entry.insert(0, str(random.randint(1, 5)))
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
                destino = entradas["GrupoDestino"].get()
                nome = entradas["Nome"].get() or f"{classe_nome}_{random.randint(1, 50)}"

                # Buscar NPC base (agora é dict do banco de dados)
                npcs_grupo = npcs_por_grupo.get(grupo, [])
                npc_base = next((npc for npc in npcs_grupo if npc["classe"] == classe_nome), None)
                
                if not npc_base:
                    raise ValueError("Classe não encontrada no grupo.")

                # Criar NPC usando dados do banco (assumindo que as chaves são as mesmas)
                npc = CB.NPC(grupo, npc_base["classe"], npc_base["forca"], npc_base["agilidade"],
                        npc_base["vigor"], npc_base["inteligencia"], npc_base["presenca"], npc_base["tatica"])

                # Carregar proficiências do banco de dados
                proficiencias = filtrar_proficiencias()  # Carrega todas as proficiências
                
                # Criar personagem sem kit
                personagem = CB.Gerador(npc=npc, nivel=nivel, nome=nome, proficiencias_base=proficiencias)

                self.carregar_armas_e_armaduras(personagem)
                # Usar D.GruposDePersonagens
                if destino in D.GruposDePersonagens:
                    D.GruposDePersonagens[destino].append(personagem)

                self.refresh()
                popup.destroy()

            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o NPC:\n{e}")

        tk.Button(popup, text="Confirmar", command=confirmar, bg="#0b8f33", fg="white",
                font=("Arial", 12, "bold")).pack(pady=20)

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

    def gerar_grupo_NPCs(self, title):
        import random

        grupos_disponiveis = list(D.GruposDePersonagens.keys())
        
        if not grupos_disponiveis:
            messagebox.showwarning("Aviso", "Nenhum grupo disponível!\n\nCrie um grupo primeiro antes de gerar grupos de NPCs.")
            return

        # Carrega dados dos NPCs
        dados_npcs = D.ler_dados_npcs()
        npcs_por_faccao = {}
        for npc in dados_npcs:
            faccao = npc["grupo"]
            classe = npc["classe"]
            atributos = (
                classe,
                npc["forca"],
                npc["agilidade"],
                npc["vigor"],
                npc["inteligencia"],
                npc["presenca"],
                npc["tatica"]
            )
            if faccao not in npcs_por_faccao:
                npcs_por_faccao[faccao] = []
            npcs_por_faccao[faccao].append(atributos)

        popup = tk.Toplevel()
        popup.title("Gerar Grupo de NPCs")
        popup.configure(bg="#130f26")
        popup.geometry("500x550")

        entradas = {}

        # Cabeçalho com opções iniciais
        header_frame = tk.Frame(popup, bg="#130f26")
        header_frame.pack(pady=10)

        # Grupo de destino
        tk.Label(header_frame, text="Inserir em:", bg="#130f26", fg="white").grid(row=0, column=0, padx=5, sticky="e")
        destino_var = tk.StringVar(value=grupos_disponiveis[0])
        destino_menu = ttk.Combobox(header_frame, textvariable=destino_var, state="readonly", values=grupos_disponiveis, width=20)
        destino_menu.grid(row=0, column=1, padx=5)
        entradas["Destino"] = destino_var

        # Facção
        tk.Label(header_frame, text="Facção:", bg="#130f26", fg="white").grid(row=0, column=2, padx=5, sticky="e")
        faccao_var = tk.StringVar(value=list(npcs_por_faccao.keys())[0])
        faccao_menu = ttk.Combobox(header_frame, textvariable=faccao_var, state="readonly", values=list(npcs_por_faccao.keys()), width=20)
        faccao_menu.grid(row=0, column=3, padx=5)
        entradas["Facção"] = faccao_var

        # Quantidade
        tk.Label(header_frame, text="Quantidade:", bg="#130f26", fg="white").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        qtd_var = tk.StringVar(value="3")
        qtd_entry = tk.Entry(header_frame, textvariable=qtd_var, width=5, justify="center")
        qtd_entry.grid(row=1, column=1, padx=5, pady=5)

        # Área scrollável
        canvas_frame = tk.Frame(popup, bg="#130f26")
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame, bg="#130f26", highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#130f26")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        slots = []

        def gerar_slots(npcs_por_faccao=npcs_por_faccao):
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
            slots.clear()

            faccao = faccao_var.get()
            classes_disponiveis = [c[0] for c in npcs_por_faccao.get(faccao, [])]

            try:
                qtd = int(qtd_var.get())
            except:
                tk.messagebox.showerror("Erro", "Valores inválidos.")
                return

            if not classes_disponiveis:
                tk.messagebox.showerror("Erro", f"Nenhuma classe disponível para a facção '{faccao}'.")
                return

            for i in range(qtd):
                slot = {}
                frame = tk.Frame(scrollable_frame, bg="#1f1b3a", bd=1, relief="solid", padx=5, pady=5)
                frame.pack(padx=5, pady=5, fill="x")

                tk.Label(frame, text=f"NPC {i+1}", bg="#1f1b3a", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=6, pady=(0, 5), sticky="w")

                # Classe
                tk.Label(frame, text="Classe", bg="#1f1b3a", fg="white").grid(row=1, column=0, padx=2, sticky="e")
                classe_var = tk.StringVar(value=classes_disponiveis[0])
                classe_menu = ttk.Combobox(frame, textvariable=classe_var, state="readonly", values=classes_disponiveis, width=20)
                classe_menu.grid(row=1, column=1, padx=2)

                # Nível
                tk.Label(frame, text="Nível", bg="#1f1b3a", fg="white").grid(row=1, column=2, padx=2, sticky="e")
                nivel_var = tk.StringVar(value="1")
                nivel_entry = tk.Entry(frame, textvariable=nivel_var, width=5, justify="center")
                nivel_entry.grid(row=1, column=3, padx=2)

                # Nome (opcional)
                tk.Label(frame, text="Nome (opcional)", bg="#1f1b3a", fg="white").grid(row=1, column=4, padx=2, sticky="e")
                nome_var = tk.StringVar(value="")
                nome_entry = tk.Entry(frame, textvariable=nome_var, width=15, justify="center")
                nome_entry.grid(row=1, column=5, padx=2)

                slot.update({
                    "Classe": classe_var,
                    "Nivel": nivel_var,
                    "Nome": nome_var
                })

                slots.append(slot)

        # Atualizar slots automaticamente ao trocar facção
        faccao_var.trace_add("write", lambda *args: gerar_slots(npcs_por_faccao))

        # Botões
        tk.Button(popup, text="Gerar Slots", command=lambda:gerar_slots(npcs_por_faccao), font=("Arial", 11), bg="#0b4f8f", fg="white").pack(pady=(10, 10))
        tk.Button(popup, text="Confirmar Geração", command=lambda: self.confirmar_geracao(slots, entradas, npcs_por_faccao), font=("Arial", 11), bg="#1a7837", fg="white").pack(pady=(0, 10))

    def confirmar_geracao(self, slots, entradas, npcs_por_faccao):
        import random
        try:
            faccao = entradas["Facção"].get()
            destino = entradas["Destino"].get()

            # Carregar os NPCs do JSON
            npcs_disponiveis = D.carregar_npcs_json()

            for i, slot in enumerate(slots):
                classe_nome = slot["Classe"].get()
                nivel = int(slot["Nivel"].get())
                nome_customizado = slot["Nome"].get().strip()

                # Buscar NPC correspondente pela facção e classe
                npc_dict = next((n for n in npcs_disponiveis if n['faccao'] == faccao and n['classe'] == classe_nome), None)
                if not npc_dict:
                    raise ValueError(f"Classe '{classe_nome}' não encontrada na facção '{faccao}'.")

                npc_base = CB.NPC(
                    faccao=npc_dict['faccao'],
                    classe=npc_dict['classe'],
                    forca=int(npc_dict['forca']),
                    agilidade=int(npc_dict['agilidade']),
                    vigor=int(npc_dict['vigor']),
                    inteligencia=int(npc_dict['inteligencia']),
                    presenca=int(npc_dict['presenca']),
                    tatica=int(npc_dict['tatica'])
                )

                # Definir nome (usar customizado ou gerar automaticamente)
                nome = nome_customizado if nome_customizado else f"{classe_nome}_{random.randint(1, 99)}"

                # Criar personagem sem kit
                personagem = CB.Gerador(npc=npc_base, kit=None, nivel=nivel, nome=nome, proficiencias_base=D.Proficiencias)

                # Pós-processamento
                self.carregar_armas_e_armaduras(personagem)

                # Adicionar ao grupo
                if destino in D.GruposDePersonagens:
                    D.GruposDePersonagens[destino].append(personagem)
                else:
                    raise ValueError(f"Grupo de destino '{destino}' não encontrado.")

            self.refresh()
            tk.messagebox.showinfo("Sucesso", "NPCs gerados com sucesso!")

        except Exception as e:
            tk.messagebox.showerror("Erro", f"Ocorreu um erro ao gerar os NPCs:\n{e}")
# --- Criação e Geração de personagens --- #

    def Voltar(self):
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

        self.label_bloqueio= tk.Label(self.frame_AC, bg='#1a0869', fg="white", font=("Arial", 16))
        self.label_bloqueio.pack(pady=2)
        self.label_esquiva= tk.Label(self.frame_AC, bg='#1a0869', fg="white", font=("Arial", 16))
        self.label_esquiva.pack(pady=2)
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
                    texto_item = f"{item_nome} x{quantidade}"

                btn_item = tk.Button(frame_item, text=texto_item, bg="#2a0d89", fg="white",
                    font=("Arial", 13), anchor='w', relief=tk.FLAT,borderwidth=0, highlightthickness=0, width=35,
                    command=lambda i=item_obj: self.mostrar_popup_detalhes_item(i))
                btn_item.pack(side="left", fill='x', expand=True)

                if item_id:
                    # Botão de melhorias para todos os itens com ID
                    btn_melhorias = tk.Button(frame_item, text="Upgrades", command=lambda i=item_obj: self.abrir_popup_melhorias_item(i), bg="#8B4513", fg="white", font=("Arial", 8), width=8)
                    btn_melhorias.pack(side="right", padx=5)
                    
                    if isinstance(item_obj, (CB.Melee)):
                        btn_equipar = tk.Button(frame_item, text="Equip", command=lambda i=item_obj: self._equipar_item(i), bg="#2a0d89", fg="white", font=("Arial", 8), width=6)
                        btn_equipar.pack(side="right", padx=5)
                        btn_remover = tk.Button(frame_item,text="Discard",command=lambda i=item_obj: self._remover_item_do_inventario(i),bg="#2a0d89",fg="white",font=("Arial", 8))     
                        btn_remover.pack(side="right", padx=5)
                        self.item_widgets.append(btn_equipar)
                    elif isinstance(item_obj, (CB.Ranged)):
                        btn_equipar = tk.Button(frame_item, text="Equip", command=lambda i=item_obj: self._equipar_item(i), bg="#2a0d89", fg="white", font=("Arial", 8), width=6)
                        btn_equipar.pack(side="right", padx=5)
                        btn_unload = tk.Button(frame_item, text="Unload", command=lambda i=item_obj: self.descarregar_municao_ranged(i), bg="#2a0d89", fg="white", font=("Arial", 8), width=6)
                        btn_unload.pack(side="right", padx=5)
                        btn_remover = tk.Button(frame_item,text="Discard",command=lambda i=item_obj: self._remover_item_do_inventario(i),bg="#2a0d89",fg="white",font=("Arial", 8))     
                        btn_remover.pack(side="right", padx=5)
                        self.item_widgets.extend([btn_equipar, btn_unload])
                    elif isinstance(item_obj, (CB.Protecao)):
                        print(f"Item {item_nome} é uma Protecao!")
                        regiao = getattr(item_obj, "regiao", None)
                        if regiao:
                            btn_equipar = tk.Button(frame_item, text="Equip", command=lambda i=item_obj: self._equipar_protecao(i), bg="#2a0d89", fg="white", font=("Arial", 8), width=6)
                            btn_equipar.pack(side="right", padx=5)
                            btn_remover = tk.Button(frame_item,text="Discard",command=lambda i=item_obj: self._remover_item_do_inventario(i),bg="#2a0d89",fg="white",font=("Arial", 8))     
                            btn_remover.pack(side="right", padx=5)
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
                "Pernas": self.character.Pernas}

            for regiao, protecao in regioes.items():
                frame_linha = tk.Frame(self.frame_lista_protecoes, bg='#1a0869')
                frame_linha.pack(fill='x', pady=5)
                self.protecao_widgets.append(frame_linha)

                nome_protecao = protecao.nome if protecao else "Nenhuma"
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
        self.refresh()
    
    def decrementar_proficiencia(self, prof):
        prof.nivel -= 1
        self.refresh()
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

        categorias = {
            "Armas de Fogo": D.Rangeds,
            "Armas Corpo a Corpo": D.Melees,
            "Proteções": D.Protecoes,
            "Melhorias": D.Melhorias,
            "Munições": D.Municoes,
            "Consumíveis": D.Consumiveis,
            "Explosivos": D.Explosivos,
            "Itens": D.Items
        }

        tk.Label(popup, text="Categoria:", bg="#1a0869", fg="white", font=("Arial", 16)).pack(pady=5)
        categoria_var = tk.StringVar()
        categoria_menu = ttk.Combobox(popup, textvariable=categoria_var, values=list(categorias.keys()))
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
        btn_voltar = tk.Button( popup, text="Voltar", command=popup.destroy, bg="#a00c0c", fg="white", font=("Arial", 12))
        btn_voltar.pack(pady=10, side="bottom")

        quantidade_widgets = {}

        def exibir_itens(*args):
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
            quantidade_widgets.clear()

            categoria = categoria_var.get()
            if not categoria:
                return

            for nome_item, item_func in categorias[categoria].items():
                item_obj = item_func() if callable(item_func) else item_func

                frame_item = tk.Frame(scrollable_frame, bg="#1a0869")
                frame_item.pack(fill="x", pady=2)

                # Campo de quantidade se for stackável
                if not hasattr(item_obj, "Id"):
                    qtd_var = tk.StringVar(value="1")
                    qtd_entry = tk.Entry(frame_item, textvariable=qtd_var, width=5, font=("Arial", 12))
                    qtd_entry.pack(side="right", padx=5)
                    quantidade_widgets[nome_item] = qtd_var

                btn_item = tk.Button( frame_item, text=nome_item,
                    bg="#0e3386", fg="white", width=28, font=("Arial", 12),
                    command=lambda n=nome_item: adicionar_item(categoria, n))
                btn_item.pack(side="left", padx=5)

        def adicionar_item(categoria, nome_item):
            item_obj = categorias[categoria][nome_item]
            item_obj = item_obj() if callable(item_obj) else item_obj
            quantidade = 1

            if not hasattr(item_obj, "Id"):
                qtd_str = quantidade_widgets.get(nome_item).get()
                try:
                    quantidade = int(qtd_str)
                    if quantidade <= 0:
                        raise ValueError
                except ValueError:
                    tk.messagebox.showerror("Erro", "Quantidade inválida.")
                    return

            self.character.inventario.gerenciar_item(item_objeto=item_obj, quantidade=quantidade, operacao="adicionar")
            self.refresh()

        categoria_var.trace_add("write", exibir_itens)
    
    def remover_protecao(self, regiao):
        try:
            # Acessa a proteção atual do personagem naquela região
            protecao_atual = getattr(self.character, regiao, None)

            if not protecao_atual:
                print(f"Nenhuma proteção equipada na região: {regiao}")
                return

            # Retorna o item ao inventário do personagem
            self.character.inventario.gerenciar_item(item_objeto=protecao_atual, quantidade=1, operacao="adicionar")

            # Remove a proteção da região
            setattr(self.character, regiao, None)

            # Recalcula peso e atualiza interface
            self.character.calcular_peso_total()
            self.refresh()
            print(f"Proteção removida da região: {regiao}")

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
        """Abre popup para visualizar e gerenciar efeitos do personagem"""
        if not hasattr(self, 'character') or not self.character:
            messagebox.showwarning("Aviso", "Nenhum personagem selecionado!")
            return
        
        popup = tk.Toplevel(self)
        popup.title("Efeitos do Personagem")
        popup.geometry("600x500")
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
        entry_nome = tk.Entry(linha1, width=20)
        entry_nome.pack(side="left", padx=5)
        
        tk.Label(linha1, text="Tipo:", bg='#1a0869', fg="white").pack(side="left", padx=(20, 0))
        var_tipo = tk.StringVar(value="buff")
        tk.Radiobutton(linha1, text="Buff", variable=var_tipo, value="buff", bg='#1a0869', fg="white", selectcolor='#1a0869').pack(side="left", padx=5)
        tk.Radiobutton(linha1, text="Debuff", variable=var_tipo, value="debuff", bg='#1a0869', fg="white", selectcolor='#1a0869').pack(side="left")
        
        # Linha 2: Valor
        linha2 = tk.Frame(frame_adicionar, bg='#1a0869')
        linha2.pack(fill="x", padx=5, pady=2)
        
        tk.Label(linha2, text="Valor:", bg='#1a0869', fg="white").pack(side="left")
        entry_valor = tk.Entry(linha2, width=10)
        entry_valor.pack(side="left", padx=5)
        
        # Linha 3: Descrição
        linha3 = tk.Frame(frame_adicionar, bg='#1a0869')
        linha3.pack(fill="x", padx=5, pady=2)
        
        tk.Label(linha3, text="Descrição:", bg='#1a0869', fg="white").pack(anchor="w")
        entry_descricao = tk.Entry(linha3, width=60)
        entry_descricao.pack(fill="x", pady=2)
        
        # Botão adicionar
        def adicionar_efeito():
            nome = entry_nome.get().strip()
            descricao = entry_descricao.get().strip()
            valor = entry_valor.get().strip()
            tipo = var_tipo.get()
            
            if not nome or not descricao:
                messagebox.showwarning("Aviso", "Nome e descrição são obrigatórios!")
                return
            
            # Tenta converter valor para número, se não conseguir mantém como string
            try:
                valor = float(valor) if '.' in valor else int(valor)
            except ValueError:
                if not valor:
                    valor = 0
            
            self.character.efeitos.adicionar_efeito(nome, descricao, valor, tipo)
            
            # Limpa campos
            entry_nome.delete(0, tk.END)
            entry_descricao.delete(0, tk.END)
            entry_valor.delete(0, tk.END)
            
            # Atualiza lista
            atualizar_lista()
            
            # Atualiza a tela principal se os efeitos afetarem stats
            self.refresh_info_basica()
        
        tk.Button(frame_adicionar, text="Adicionar", command=adicionar_efeito, bg="#115c11", fg="white", font=("Arial", 10)).pack(pady=5)
        
        # Frame para lista de efeitos
        frame_lista = tk.Frame(popup, bg='#130f26')
        frame_lista.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Canvas com scrollbar para lista
        canvas = tk.Canvas(frame_lista, bg='#1a0869', highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_lista, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1a0869')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def atualizar_lista():
            # Limpa lista atual
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
            
            # Adiciona efeitos
            efeitos = self.character.efeitos.listar_efeitos()
            if not efeitos:
                tk.Label(scrollable_frame, text="Nenhum efeito ativo", bg='#1a0869', fg="gray", font=("Arial", 12)).pack(pady=20)
                return
            
            for efeito in efeitos:
                # Frame para cada efeito
                frame_efeito = tk.Frame(scrollable_frame, bg='#2a1f4f', bd=1, relief='solid')
                frame_efeito.pack(fill="x", padx=5, pady=2)
                
                # Cor baseada no tipo
                cor_tipo = "#115c11" if efeito.tipo == "buff" else "#8c1d1d"
                simbolo = "+" if efeito.tipo == "buff" else "-"
                
                # Header do efeito
                header = tk.Frame(frame_efeito, bg=cor_tipo)
                header.pack(fill="x")
                
                tk.Label(header, text=f"[{simbolo}] {efeito.nome}", font=("Arial", 12, "bold"), bg=cor_tipo, fg="white").pack(side="left", padx=5, pady=2)
                tk.Label(header, text=f"Valor: {efeito.valor}", font=("Arial", 10), bg=cor_tipo, fg="white").pack(side="right", padx=5, pady=2)
                
                # Descrição
                tk.Label(frame_efeito, text=efeito.descricao, font=("Arial", 10), bg='#2a1f4f', fg="white", wraplength=500, justify="left").pack(anchor="w", padx=5, pady=2)
                
                # Botão remover
                tk.Button(frame_efeito, text="Remover", command=lambda n=efeito.nome: remover_efeito(n), bg="#8c1d1d", fg="white", font=("Arial", 9)).pack(anchor="e", padx=5, pady=2)
        
        def remover_efeito(nome):
            self.character.efeitos.remover_efeito(nome)
            atualizar_lista()
            # Atualiza a tela principal se os efeitos afetarem stats
            self.refresh_info_basica()
        
        # Botão para limpar todos os efeitos
        frame_botoes = tk.Frame(popup, bg='#130f26')
        frame_botoes.pack(pady=10)
        
        def limpar_todos():
            self.character.efeitos.limpar_efeitos()
            atualizar_lista()
            # Atualiza a tela principal se os efeitos afetarem stats
            self.refresh_info_basica()
        
        tk.Button(frame_botoes, text="Limpar Todos", command=limpar_todos, bg="#8c1d1d", fg="white", font=("Arial", 12)).pack(side="left", padx=10)
        tk.Button(frame_botoes, text="Fechar", command=popup.destroy, bg="#1a0869", fg="white", font=("Arial", 12)).pack(side="left", padx=10)
        
        # Carrega lista inicial
        atualizar_lista()
        
        # Centraliza popup
        popup.transient(self)
        popup.grab_set()

    def abrir_popup_habilidades(self):
        """Abre popup para visualizar e gerenciar habilidades/poderes do personagem"""
        if not hasattr(self, 'character') or not self.character:
            messagebox.showwarning("Aviso", "Nenhum personagem selecionado!")
            return
        
        popup = tk.Toplevel(self)
        popup.title("Habilidades e Poderes")
        popup.geometry("650x600")
        popup.configure(bg='#130f26')
        popup.resizable(False, False)
        
        # Título
        title_label = tk.Label(popup, text="Habilidades e Poderes", font=("Arial", 18, "bold"), bg="#1a0869", fg="white")
        title_label.pack(pady=10, fill="x")
        
        # Frame para adicionar nova habilidade
        frame_adicionar = tk.Frame(popup, bg='#1a0869', bd=2, relief='ridge')
        frame_adicionar.pack(pady=10, padx=20, fill="x")
        
        tk.Label(frame_adicionar, text="Adicionar Habilidade:", font=("Arial", 12, "bold"), bg='#1a0869', fg="white").pack(anchor="w", padx=5, pady=5)
        
        # Linha 1: Nome e Gasto de Energia
        linha1 = tk.Frame(frame_adicionar, bg='#1a0869')
        linha1.pack(fill="x", padx=5, pady=2)
        
        tk.Label(linha1, text="Nome:", bg='#1a0869', fg="white").pack(side="left")
        entry_nome = tk.Entry(linha1, width=25)
        entry_nome.pack(side="left", padx=5)
        
        tk.Label(linha1, text="Custo Energia:", bg='#1a0869', fg="white").pack(side="left", padx=(20, 0))
        entry_energia = tk.Entry(linha1, width=5)
        entry_energia.pack(side="left", padx=5)
        entry_energia.insert(0, "0")
        
        # Linha 2: Descrição
        linha2 = tk.Frame(frame_adicionar, bg='#1a0869')
        linha2.pack(fill="x", padx=5, pady=2)
        
        tk.Label(linha2, text="Descrição:", bg='#1a0869', fg="white").pack(anchor="w")
        entry_descricao = tk.Entry(linha2, width=70)
        entry_descricao.pack(fill="x", pady=2)
        
        # Linha 3: Efeito
        linha3 = tk.Frame(frame_adicionar, bg='#1a0869')
        linha3.pack(fill="x", padx=5, pady=2)
        
        tk.Label(linha3, text="Efeito:", bg='#1a0869', fg="white").pack(anchor="w")
        entry_efeito = tk.Entry(linha3, width=70)
        entry_efeito.pack(fill="x", pady=2)
        
        # Botão adicionar
        def adicionar_habilidade():
            nome = entry_nome.get().strip()
            descricao = entry_descricao.get().strip()
            efeito = entry_efeito.get().strip()
            energia = entry_energia.get().strip()
            
            if not nome or not descricao or not efeito:
                messagebox.showwarning("Aviso", "Nome, descrição e efeito são obrigatórios!")
                return
            
            # Tenta converter energia para número
            try:
                energia = int(energia)
            except ValueError:
                energia = 0
            
            if energia < 0:
                energia = 0
            
            self.character.habilidades.adicionar_habilidade(nome, descricao, efeito, energia)
            
            # Limpa campos
            entry_nome.delete(0, tk.END)
            entry_descricao.delete(0, tk.END)
            entry_efeito.delete(0, tk.END)
            entry_energia.delete(0, tk.END)
            entry_energia.insert(0, "0")
            
            # Atualiza lista
            atualizar_lista()
        
        tk.Button(frame_adicionar, text="Adicionar", command=adicionar_habilidade, bg="#115c11", fg="white", font=("Arial", 10)).pack(pady=5)
        
        # Frame para abas (Todas, Ativas, Passivas)
        frame_abas = tk.Frame(popup, bg='#130f26')
        frame_abas.pack(pady=5)
        
        var_aba = tk.StringVar(value="todas")
        
        tk.Radiobutton(frame_abas, text="Todas", variable=var_aba, value="todas", bg='#130f26', fg="white", selectcolor='#1a0869', command=lambda: atualizar_lista()).pack(side="left", padx=10)
        tk.Radiobutton(frame_abas, text="Ativas", variable=var_aba, value="ativas", bg='#130f26', fg="white", selectcolor='#1a0869', command=lambda: atualizar_lista()).pack(side="left", padx=10)
        tk.Radiobutton(frame_abas, text="Passivas", variable=var_aba, value="passivas", bg='#130f26', fg="white", selectcolor='#1a0869', command=lambda: atualizar_lista()).pack(side="left", padx=10)
        
        # Frame para lista de habilidades
        frame_lista = tk.Frame(popup, bg='#130f26')
        frame_lista.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Canvas com scrollbar para lista
        canvas = tk.Canvas(frame_lista, bg='#1a0869', highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_lista, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1a0869')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def atualizar_lista():
            # Limpa lista atual
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
            
            # Obtém habilidades baseado na aba selecionada
            aba_atual = var_aba.get()
            if aba_atual == "ativas":
                habilidades = self.character.habilidades.listar_ativas()
            elif aba_atual == "passivas":
                habilidades = self.character.habilidades.listar_passivas()
            else:
                habilidades = self.character.habilidades.listar_habilidades()
            
            if not habilidades:
                texto = "Nenhuma habilidade cadastrada"
                if aba_atual == "ativas":
                    texto = "Nenhuma habilidade ativa cadastrada"
                elif aba_atual == "passivas":
                    texto = "Nenhuma habilidade passiva cadastrada"
                
                tk.Label(scrollable_frame, text=texto, bg='#1a0869', fg="gray", font=("Arial", 12)).pack(pady=20)
                return
            
            for habilidade in habilidades:
                # Frame para cada habilidade
                frame_habilidade = tk.Frame(scrollable_frame, bg='#2a1f4f', bd=1, relief='solid')
                frame_habilidade.pack(fill="x", padx=5, pady=3)
                
                # Cor baseada no tipo
                cor_tipo = "#4a148c" if habilidade.tipo == "passivo" else "#1565c0"
                simbolo = "🔮" if habilidade.tipo == "passivo" else "⚡"
                
                # Header da habilidade
                header = tk.Frame(frame_habilidade, bg=cor_tipo)
                header.pack(fill="x")
                
                tk.Label(header, text=f"{simbolo} {habilidade.nome}", font=("Arial", 12, "bold"), bg=cor_tipo, fg="white").pack(side="left", padx=5, pady=2)
                
                custo_text = "Passivo" if habilidade.gasto_energia == 0 else f"Custo: {habilidade.gasto_energia} PE"
                tk.Label(header, text=custo_text, font=("Arial", 10), bg=cor_tipo, fg="white").pack(side="right", padx=5, pady=2)
                
                # Descrição
                tk.Label(frame_habilidade, text=f"Descrição: {habilidade.descricao}", font=("Arial", 10), bg='#2a1f4f', fg="white", wraplength=550, justify="left").pack(anchor="w", padx=5, pady=2)
                
                # Efeito
                tk.Label(frame_habilidade, text=f"Efeito: {habilidade.efeito}", font=("Arial", 10, "bold"), bg='#2a1f4f', fg="#90caf9", wraplength=550, justify="left").pack(anchor="w", padx=5, pady=2)
                
                # Botão remover
                tk.Button(frame_habilidade, text="Remover", command=lambda n=habilidade.nome: remover_habilidade(n), bg="#8c1d1d", fg="white", font=("Arial", 9)).pack(anchor="e", padx=5, pady=2)
        
        def remover_habilidade(nome):
            self.character.habilidades.remover_habilidade(nome)
            atualizar_lista()
        
        # Botão para limpar todas as habilidades
        frame_botoes = tk.Frame(popup, bg='#130f26')
        frame_botoes.pack(pady=10)
        
        def limpar_todas():
            resultado = messagebox.askyesno("Confirmação", "Tem certeza que deseja remover todas as habilidades?")
            if resultado:
                self.character.habilidades.limpar_habilidades()
                atualizar_lista()
        
        tk.Button(frame_botoes, text="Limpar Todas", command=limpar_todas, bg="#8c1d1d", fg="white", font=("Arial", 12)).pack(side="left", padx=10)
        tk.Button(frame_botoes, text="Fechar", command=popup.destroy, bg="#1a0869", fg="white", font=("Arial", 12)).pack(side="left", padx=10)
        
        # Carrega lista inicial
        atualizar_lista()
        
        # Centraliza popup
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
            # Criar frame vazio se não há grupo selecionado
            frame = tk.Frame(self, bg='#1a0869')
            frame.place(x=x, y=y, width=350, height=550)
            tk.Label(frame, text="Nenhum grupo selecionado", fg="gray", bg="#1a0869", font=("Arial", 14)).pack(pady=200)
            return frame
        
        data_list = D.GruposDePersonagens[grupo_nome]
        
        frame = tk.Frame(self, bg='#1a0869')
        frame.place(x=x, y=y, width=350, height=550)

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
            char_frame = tk.Frame(inner_frame, bg="#220866", bd=2, relief="groove", width=400)
            char_frame.pack(fill="x", padx=5, pady=5)

            info = f"{char.nome} || Nv {char.nivel} || XP: {char.XPAtual}/{char.XPlvlUp}\n"
            info += f"PV: {char.vidaAtual}/{char.vidaMax} || PE: {char.PeAtual}/{char.PeMax}\n"
            info += f"Bloqueio: {char.bloqueio} | Esquiva: {char.esquiva}"
            tk.Label(char_frame, text=info, bg="#220866", fg="white", font=("Arial", 10), justify="left").pack(anchor="w", padx=5, pady=2)

            # Linha com dois botões
            botoes_frame = tk.Frame(char_frame, bg="#220866")
            botoes_frame.pack(pady=2)

            tk.Button(botoes_frame, text="Abrir Detalhes", bg="#1a0869", fg="white", font=("Arial", 9),command=lambda c=char: self.controller.abrir_detalhes(c)).pack(side="left", padx=5)

            tk.Button(botoes_frame, text="Abrir ações", bg="#3a0a80", fg="white", font=("Arial", 9), command=lambda c=char: self.abrir_popup_acoes(c)).pack(side="left", padx=5)

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
        
        # Atualizar lista direita se existe
        if hasattr(self, 'frame_lista_direita') and self.frame_lista_direita:
            self.frame_lista_direita.destroy()
            self.frame_lista_direita = self.create_list_section_with_group(self.grupo_direito, x=1150, y=150)

    def abrir_popup_acoes(self, personagem):
        popup = tk.Toplevel(self)
        popup.title(f"Ações - {personagem.nome}")
        popup.configure(bg="#1a0869")
        popup.geometry("350x400")
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
        
        # Botões de ação
        tk.Button(botoes_frame, text="Atacar", command=abrir_menu_ataque, 
                bg="#8B0000", fg="white", font=("Arial", 12), width=15, height=2).pack(pady=5)
        
        tk.Button(botoes_frame, text="Pilhar", command=pilhar,
                bg="#4B0082", fg="white", font=("Arial", 12), width=15, height=2).pack(pady=5)
        
        tk.Button(botoes_frame, text="Recarregar", command=lambda: print(f"Recarregar - {personagem.nome}"),
                bg="#006400", fg="white", font=("Arial", 12), width=15, height=2).pack(pady=5)
        
        tk.Button(botoes_frame, text="Descarregar", command=lambda: print(f"Descarregar - {personagem.nome}"),
                bg="#FF8C00", fg="white", font=("Arial", 12), width=15, height=2).pack(pady=5)
        
        tk.Button(botoes_frame, text="Trocar Arma", command=lambda: print(f"Trocar Arma - {personagem.nome}"),
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
        
        tk.Button(botoes_frame, text="Ataque Explosivo", command=lambda: print("Funcionalidade não implementada"),
                bg="#FF8C00", fg="white", font=("Arial", 12), width=20, height=2, state="disabled").pack(pady=5)
        
        tk.Button(botoes_frame, text="Ataque Mágico", command=lambda: print("Funcionalidade não implementada"),
                bg="#4B0082", fg="white", font=("Arial", 12), width=20, height=2, state="disabled").pack(pady=5)
        
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
        tk.Label(arma_frame, text="Arma Melee:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(side="left")
        arma_var = tk.StringVar()
        arma_menu = ttk.Combobox(arma_frame, textvariable=arma_var, state="readonly", width=30)
        arma_menu.pack(side="right")

        # Região do corpo
        regiao_frame = tk.Frame(main_frame, bg="#1a1a2e")
        regiao_frame.pack(fill="x", pady=5)
        tk.Label(regiao_frame, text="Região do Corpo:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(side="left")
        regiao_var = tk.StringVar(value="Aleatório")
        regiao_menu = ttk.Combobox(regiao_frame, textvariable=regiao_var, state="readonly", width=30,
                                  values=["Aleatório", "Cabeça", "Rosto", "Torso", "Pernas", "Braços"])
        regiao_menu.pack(side="right")

        # Tipo de Ataque
        tipo_frame = tk.Frame(main_frame, bg="#1a1a2e")
        tipo_frame.pack(fill="x", pady=5)
        tk.Label(tipo_frame, text="Tipo de Ataque:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(side="left")
        tipo_var = tk.StringVar(value="simples")
        tipo_menu = ttk.Combobox(tipo_frame, textvariable=tipo_var, state="readonly", width=30,
                                values=["simples", "forte", "investida", "arremesso"])
        tipo_menu.pack(side="right")

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
            atributo_base = atacante.Forca
            rolagens = [random.randint(1, 20) for _ in range(max(1, atributo_base // 2))]
            melhor = max(rolagens) if rolagens else 0

            rolagem_var.set(melhor)
            resultado_rolagem_label.config(
                text=f"Rolagem com Força ({atributo_base // 2}x D20): {rolagens} → Melhor: {melhor}"
            )

        # Função para determinar região aleatória
        def obter_regiao_final():
            if regiao_var.get() == "Aleatório":
                rand = random.randint(1, 100)
                if rand <= 10:
                    return "Cabeça"
                elif rand <= 30:
                    return "Torso"
                elif rand <= 50:
                    return "Pernas"
                else:
                    return "Braços"
            return regiao_var.get()

        # Atualizar armas melee
        def atualizar_armas_melee(*_):
            self.arma_id_por_nome = {}
            atacante = atacante_pre_selecionado
            armas_melee = []
            self.arma_id_por_nome.clear()
            
            for i in atacante.equipados.itens:
                item = i["item"]
                if isinstance(item, CB.Melee):
                    entrada = f"{item.nome} (ID: {item.Id})"
                    armas_melee.append(entrada)
                    self.arma_id_por_nome[entrada] = item.Id

            arma_menu['values'] = armas_melee
            if armas_melee:
                arma_var.set(armas_melee[0])

        # Confirmar ataque
        def confirmar_ataque_melee():
            alvo_nome = alvo_var.get()
            entrada_arma = arma_var.get()
            rolagem = rolagem_var.get()
            buff_dano = buff_dano_var.get()
            buff_acerto = buff_acerto_var.get()
            regiao = obter_regiao_final()
            tipo = tipo_var.get()

            atacante = atacante_pre_selecionado
            alvo = next((p for p in todos_personagens if p.nome == alvo_nome), None)
            arma_id = self.arma_id_por_nome.get(entrada_arma)
            arma = next((i["item"] for i in atacante.inventario.itens if isinstance(i["item"], CB.Melee) and i["item"].Id == arma_id), None)

            if not alvo or not arma:
                resultado_label.config(text="Erro: alvo ou arma inválido(s).", fg="red")
                return

            resultado = CB.acerto_melee(
                atacante=atacante,
                alvo=alvo,
                rolagem=rolagem,
                id_arma=arma.Id,
                regiao=regiao,
                debuff=buff_dano,
                tipo_ataque=tipo
            )
            
            # Adicionar ao log
            self.adicionar_log(f"Ataque Melee: {atacante.nome} → {alvo.nome} ({regiao})", "orange")
            self.adicionar_log(resultado, "lightgreen")
            
            self.refresh()
            popup.destroy()

        # Label de resultado
        resultado_label = tk.Label(main_frame, text="", bg="#1a1a2e", fg="lightgreen", font=("Arial", 11))
        resultado_label.pack(pady=10)

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
        popup.geometry("500x550")
        popup.configure(bg="#1a1a2e")
        popup.resizable(False, False)

        todos_personagens = self.get_all_personagens()
        personagens_names = [p.nome for p in todos_personagens]

        # Frame principal
        main_frame = tk.Frame(popup, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        tk.Label(main_frame, text=f"Ataque Ranged - {atacante_pre_selecionado.nome}", 
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
        tk.Label(arma_frame, text="Arma Ranged:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(side="left")
        arma_var = tk.StringVar()
        arma_menu = ttk.Combobox(arma_frame, textvariable=arma_var, state="readonly", width=30)
        arma_menu.pack(side="right")

        # Região do corpo
        regiao_frame = tk.Frame(main_frame, bg="#1a1a2e")
        regiao_frame.pack(fill="x", pady=5)
        tk.Label(regiao_frame, text="Região do Corpo:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(side="left")
        regiao_var = tk.StringVar(value="Aleatório")
        regiao_menu = ttk.Combobox(regiao_frame, textvariable=regiao_var, state="readonly", width=30,
                                  values=["Aleatório", "Cabeça", "Rosto", "Torso", "Pernas", "Braços"])
        regiao_menu.pack(side="right")

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
        distancia_var = tk.IntVar(value=10)
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
        def obter_regiao_final():
            if regiao_var.get() == "Aleatório":
                rand = random.randint(1, 100)
                if rand <= 10:
                    return "Cabeça"
                elif rand <= 30:
                    return "Torso"
                elif rand <= 50:
                    return "Pernas"
                else:
                    return "Braços"
            return regiao_var.get()

        # Atualizar armas ranged
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
            regiao = obter_regiao_final()
            disparos = disparos_var.get()
            distancia = distancia_var.get()

            atacante = atacante_pre_selecionado
            alvo = next((p for p in todos_personagens if p.nome == alvo_nome), None)
            arma_id = self.arma_id_por_nome.get(entrada_arma)
            arma = next((i["item"] for i in atacante.inventario.itens if isinstance(i["item"], CB.Ranged) and i["item"].Id == arma_id), None)

            if not alvo or not arma:
                resultado_label.config(text="Erro: alvo ou arma inválido(s).", fg="red")
                return

            resultado = CB.acerto_ranged(
                atacante=atacante,
                alvo=alvo,
                rolagem=rolagem,
                id_arma=arma.Id,
                regiao=regiao,
                buff=buff_dano,
                disparos=disparos,
                distancia=distancia
            )
            
            # Adicionar ao log
            self.adicionar_log(f"Ataque Ranged: {atacante.nome} → {alvo.nome} ({regiao}) - {disparos} disparos", "orange")
            self.adicionar_log(resultado, "lightgreen")
            
            self.refresh()
            popup.destroy()

        # Label de resultado
        resultado_label = tk.Label(main_frame, text="", bg="#1a1a2e", fg="lightgreen", font=("Arial", 11))
        resultado_label.pack(pady=10)

        # Botões
        botoes_frame = tk.Frame(main_frame, bg="#1a1a2e")
        botoes_frame.pack(pady=20)
        
        tk.Button(botoes_frame, text="Confirmar Ataque", command=confirmar_ataque_ranged,
                 bg="#38b000", fg="white", font=("Arial", 12), width=15).pack(side="left", padx=5)
        
        tk.Button(botoes_frame, text="Cancelar", command=popup.destroy,
                 bg="#8B0000", fg="white", font=("Arial", 12), width=15).pack(side="right", padx=5)

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

    def abrir_popup_ataque_com_atacante(self, atacante_pre_selecionado):
        """Abre o popup de ataque com o atacante já pré-selecionado"""
        import random
        popup = tk.Toplevel(self)
        popup.title("Ataque")
        popup.geometry("700x550")
        popup.configure(bg="#1a1a2e")
        popup.resizable(False,False)

        todos_personagens = self.get_all_personagens()
        personagens_names = [p.nome for p in todos_personagens]

        y = 10

        # Atacante (pré-selecionado)
        tk.Label(popup, text="Atacante:", bg="#1a1a2e", fg="white", font=("Arial", 12)).place(x=20, y=y)
        atacante_var = tk.StringVar(value=atacante_pre_selecionado.nome)
        atacante_menu = ttk.Combobox(popup, textvariabile=atacante_var, state="readonly", values=personagens_names)
        y += 25
        atacante_menu.place(x=20, y=y, width=200)

        # Alvo
        y += 35
        tk.Label(popup, text="Alvo:", bg="#1a1a2e", fg="white", font=("Arial", 12)).place(x=20, y=y)
        alvo_var = tk.StringVar()
        y += 25
        alvo_menu = ttk.Combobox(popup, textvariable=alvo_var, state="readonly", values=personagens_names)
        alvo_menu.place(x=20, y=y, width=200)

        # Arma
        y += 35
        tk.Label(popup, text="Arma:", bg="#1a1a2e", fg="white", font=("Arial", 12)).place(x=20, y=y)
        arma_var = tk.StringVar()
        y += 25
        arma_menu = ttk.Combobox(popup, textvariable=arma_var, state="readonly")
        arma_menu.place(x=20, y=y, width=200)

        arma_tipo_label = tk.Label(popup, text="", bg="#1a1a2e", fg="#bbbbbb", font=("Arial", 10, "italic"))
        y += 30
        arma_tipo_label.place(x=20, y=y)

        # Buff/Debuff
        y += 30
        tk.Label(popup, text="Debuff/Buff(+ para debuff / - para buff):", bg="#1a1a2e", fg="white", font=("Arial", 12)).place(x=20, y=y)
        buff_var = tk.IntVar(value=0)
        y += 25
        tk.Entry(popup, textvariable=buff_var, font=("Arial", 12), width=10, justify="center").place(x=20, y=y)

        # Região do corpo
        y_regiao = y + 40
        regiao_frame = tk.Frame(popup, bg="#1a1a2e")
        tk.Label(regiao_frame, text="Região do Corpo:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack()
        regiao_var = tk.StringVar(value="Torso")
        ttk.Combobox(regiao_frame, textvariable=regiao_var, state="readonly",
                    values=["Cabeça", "Rosto", "Torso", "Pernas", "Braços"]).pack()
        regiao_frame.place(x=20, y=y_regiao)
        regiao_frame.place_forget()

        # Corpo a Corpo
        y_corpo = y_regiao + 50
        corpo_a_corpo_frame = tk.Frame(popup, bg="#1a1a2e")
        tk.Label(corpo_a_corpo_frame, text="Tipo de Ataque:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack()
        tipo_var = tk.StringVar(value="simples")
        ttk.Combobox(corpo_a_corpo_frame, textvariable=tipo_var, state="readonly",
                    values=["simples", "forte", "investida", "arremesso"]).pack()
        corpo_a_corpo_frame.place(x=20, y=y_corpo)
        corpo_a_corpo_frame.place_forget()

        # Ranged
        y_ranged = y_regiao + 50
        ranged_frame = tk.Frame(popup, bg="#1a1a2e")
        tk.Label(ranged_frame, text="Disparos:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack()
        disparos_var = tk.IntVar(value=1)
        tk.Entry(ranged_frame, textvariable=disparos_var, font=("Arial", 12), width=10, justify="center").pack()

        tk.Label(ranged_frame, text="Distância até o alvo:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(pady=(10, 0))
        distancia_var = tk.IntVar(value=10)
        tk.Entry(ranged_frame, textvariable=distancia_var, font=("Arial", 12), width=10, justify="center").pack()
        ranged_frame.place(x=20, y=y_ranged)
        ranged_frame.place_forget()

        # Lógica do ataque — DEFINIDA ANTES do botão
        def confirmar_ataque():
            atacante_nome = atacante_var.get()
            alvo_nome = alvo_var.get()
            entrada_arma = arma_var.get()
            rolagem = rolagem_var.get()
            buff = buff_var.get()
            regiao = regiao_var.get()
            disparos = disparos_var.get()
            distancia = distancia_var.get()
            tipo = tipo_var.get()

            atacante = next((p for p in todos_personagens if p.nome == atacante_nome), None)
            alvo = next((p for p in todos_personagens if p.nome == alvo_nome), None)
            arma_id = self.arma_id_por_nome.get(entrada_arma)
            arma = next((i["item"] for i in atacante.inventario.itens if isinstance(i["item"], (CB.Melee, CB.Ranged)) and i["item"].Id == arma_id), None)

            if not atacante or not alvo or not arma:
                resultado_label.config(text="Erro: atacante, alvo ou arma inválido(s).", fg="red")
                return

            if isinstance(arma, CB.Melee):
                resultado = CB.acerto_melee(
                    atacante=atacante,
                    alvo=alvo,
                    rolagem=rolagem,
                    id_arma=arma.Id,
                    regiao=regiao,
                    debuff=buff,
                    tipo_ataque=tipo
                )
            elif isinstance(arma, CB.Ranged):
                resultado = CB.acerto_ranged(
                    atacante=atacante,
                    alvo=alvo,
                    rolagem=rolagem,
                    id_arma=arma.Id,
                    regiao=regiao,
                    buff=buff,
                    disparos=disparos,
                    distancia=distancia
                )
            else:
                resultado = "Tipo de arma inválido."
            self.refresh()
            resultado_label.config(text=resultado, fg="lightgreen")

        # Arma listener
        def atualizar_armas(*_):
            self.arma_id_por_nome = {}
            nome_atacante = atacante_var.get()
            atacante = next((p for p in todos_personagens if p.nome == nome_atacante), None)
            if not atacante:
                arma_menu['values'] = []
                return

            armas_validas = []
            self.arma_id_por_nome.clear()
            for i in atacante.inventario.itens:
                item = i["item"]
                if isinstance(item, CB.Melee) or isinstance(item, CB.Ranged):
                    entrada = f"{item.nome} (ID: {item.Id})"
                    armas_validas.append(entrada)
                    self.arma_id_por_nome[entrada] = item.Id

            arma_menu['values'] = armas_validas
            if armas_validas:
                arma_var.set(armas_validas[0])
                verificar_arma()

        def verificar_arma(*_):
            nome_atacante = atacante_var.get()
            atacante = next((p for p in todos_personagens if p.nome == nome_atacante), None)
            entrada_arma = arma_var.get()
            if not atacante or entrada_arma not in self.arma_id_por_nome:
                return

            arma_id = self.arma_id_por_nome[entrada_arma]
            arma = next((i["item"] for i in atacante.inventario.itens if isinstance(i["item"], (CB.Melee, CB.Ranged)) and i["item"].Id == arma_id), None)

            corpo_a_corpo_frame.place_forget()
            ranged_frame.place_forget()
            regiao_frame.place_forget()

            if arma:
                if isinstance(arma, CB.Melee):
                    arma_tipo_label.config(text="Tipo da arma: Corpo a Corpo")
                    regiao_frame.place(x=20, y=y_regiao)
                    corpo_a_corpo_frame.place(x=20, y=y_corpo)
                elif isinstance(arma, CB.Ranged):
                    arma_tipo_label.config(text="Tipo da arma: À Distância")
                    regiao_frame.place(x=20, y=y_regiao)
                    ranged_frame.place(x=20, y=y_ranged)
                else:
                    arma_tipo_label.config(text="Tipo de item inválido")

        atacante_var.trace_add("write", atualizar_armas)
        arma_var.trace_add("write", verificar_arma)

        # Rolagem
        y_rolagem = y_ranged + 120
        acao_frame = tk.Frame(popup, bg="#1a1a2e")
        acao_frame.place(x=20, y=y_rolagem)

        tk.Label(acao_frame, text="Valor do Dado:", bg="#1a1a2e", fg="white", font=("Arial", 12)).grid(row=0, column=0, padx=5)
        rolagem_var = tk.IntVar(value=0)
        tk.Entry(acao_frame, textvariable=rolagem_var, font=("Arial", 12), width=6, justify="center").grid(row=0, column=1, padx=5)

        def executar_rolagem_ataque():
            nome_atacante = atacante_var.get()
            atacante = next((p for p in todos_personagens if p.nome == nome_atacante), None)
            entrada_arma = arma_var.get()
            if not hasattr(self, "arma_id_por_nome") or entrada_arma not in self.arma_id_por_nome:
                return
            arma_id = self.arma_id_por_nome.get(entrada_arma)
            arma = next((i["item"] for i in atacante.inventario.itens if isinstance(i["item"], (CB.Melee, CB.Ranged)) and i["item"].Id == arma_id), None)

            if not atacante or not arma:
                resultado_label.config(text="Erro ao localizar atacante ou arma.")
                return

            if isinstance(arma, CB.Melee):
                atributo_base = atacante.Forca
                texto_attr = "Força"
            elif isinstance(arma, CB.Ranged):
                atributo_base = atacante.Tatica
                texto_attr = "Tática"
            else:
                resultado_label.config(text="Tipo de arma inválido.")
                return

            rolagens = [random.randint(1, 20) for _ in range(max(1, atributo_base // 2))]
            melhor = max(rolagens) if rolagens else 0

            rolagem_var.set(melhor)
            resultado_label.config(
                text=f"Rolagem com {texto_attr} ({atributo_base // 2}x D20):\n"
                    f"{rolagens} → Melhor: {melhor}"
            )

        tk.Button(acao_frame, text="Rolar Dado", command=executar_rolagem_ataque,
                bg="#0077b6", fg="white", font=("Arial", 11)).grid(row=0, column=2, padx=10)

        resultado_label = tk.Label(popup, text="", bg="#1a1a2e", fg="lightgreen", font=("Arial", 11))
        resultado_label.place(x=300, y=20)

        # Confirmar
        y_rolagem += 60
        tk.Button(popup, text="Confirmar Ataque", command=confirmar_ataque,
                bg="#38b000", fg="white", font=("Arial", 12), width=20).place(x=100, y=y_rolagem)

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

        style = ttk.Style()
        style.theme_use("default")
        style.configure("CustomCombobox.TCombobox", foreground="black", background="black", fieldbackground="black", bordercolor="black", arrowcolor="black", font=("Arial", 14), padding=6, borderwidth=2, relief="flat")

        # Título
        tk.Button(self, text="Tela inicial", height=2, command=self.TelaInicial,
                bg="#1a0869", fg="white", font=("Arial", 20)).place(x=20, y=10, width=350, height=75)
        
        tk.Button(self, text="Seleção", height=2, command=self.TelaDeSelecao,
                bg="#1a0869", fg="white", font=("Arial", 20)).place(x=385, y=10, width=350, height=75)

        tk.Button(self, text="Combate", height=2, command=self.TelaDeCombate,
                bg="#1a0869", fg="white", font=("Arial", 20)).place(x=870, y=10, width=350, height=75)
        
        tk.Label(self, text="Informações", fg="white", bg="#1a0869",
                font=("Arial", 20, "bold"), width=20, height=2).place(x=1235, y=10, width=350, height=75)

        # Lista de dados #
        tk.Label(self, text="Lista de Conteúdo", bg="#3d0586", fg="white", font=("Arial", 18, "bold"), width=30).place(x=50, y=100)
        self.lista_tipo_var = tk.StringVar(value="NPCs")
        tipo_combobox = ttk.Combobox(self, textvariable=self.lista_tipo_var, values=["NPCs", "Itens", "Kits", "Proficiências"], state="readonly", width=79, style="CustomCombobox.TCombobox")
        tipo_combobox.place(x=50, y=145)
        self.lista_tipo_var.trace_add("write", self.atualizar_lista_conteudo)

        lista_canvas_frame = tk.Frame(self, bg="#130f26")
        lista_canvas_frame.place(x=50, y=180, width=500, height=650)

        self.lista_canvas = tk.Canvas(lista_canvas_frame, bg="#14014a", highlightbackground="#4e00b3", highlightthickness=2)
        lista_scrollbar = tk.Scrollbar(lista_canvas_frame, orient="vertical", command=self.lista_canvas.yview)
        self.lista_canvas.configure(yscrollcommand=lista_scrollbar.set)

        lista_scrollbar.pack(side="right", fill="y")
        self.lista_canvas.pack(side="left", fill="both", expand=True)

        self.lista_inner_frame = tk.Frame(self.lista_canvas, bg="#14014a")
        self.lista_canvas.create_window((0, 0), window=self.lista_inner_frame, anchor="nw")
        self.lista_inner_frame.bind("<Configure>", lambda e: self.lista_canvas.configure(scrollregion=self.lista_canvas.bbox("all")))
        # Lista de dados #

    def TelaInicial(self):
        self.controller.TelaInicial()

    def TelaDeSelecao(self):
        self.controller.TelaDeSelecao()

    def TelaDeCombate(self):
        self.controller.TelaDeCombate()

    def mostrar_topico(self, *args):
        texto = D.Topicos.get(self.topico_var.get(), "Tópico não encontrado.")
        self.texto_label.config(text=texto)

    def carregar_lista_dados(self, tipo):
        for widget in self.lista_inner_frame.winfo_children():
            widget.destroy()

        tipo = tipo or self.lista_tipo_var.get()

        if tipo == "NPCs":
            grupo = self.npc_grupo_var.get() if hasattr(self, 'npc_grupo_var') else None
            if not grupo or grupo not in D.NPCs_predefinidos:
                return
            npcs = D.NPCs_predefinidos[grupo]

            for nome, f, a, v, i, p, t in npcs:
                npc = CB.NPC(grupo, nome, f, a, v, i, p, t)

                def mostrar_info(n=npc):
                    popup = tk.Toplevel(self)
                    popup.title(f"{n.classe} ({n.grupo})")
                    popup.configure(bg="#1a1a2e")
                    popup.geometry("300x300")

                    tk.Label(popup, text=f"Classe: {n.classe}", bg="#1a1a2e", fg="white", font=("Arial", 14, "bold")).pack(pady=(10, 5))

                    atributos = {
                        "Força": n.forca,
                        "Agilidade": n.agilidade,
                        "Vigor": n.vigor,
                        "Inteligência": n.inteligencia,
                        "Presença": n.presenca,
                        "Tática": n.tatica
                    }

                    for nome, valor in atributos.items():
                        tk.Label(popup, text=f"{nome}: {valor}", bg="#1a1a2e", fg="lightgreen", font=("Arial", 12)).pack(anchor="w", padx=20)

                    tk.Button(popup, text="Fechar", command=popup.destroy, bg="#4e00b3", fg="white", font=("Arial", 11)).pack(pady=15)

                btn = tk.Button(self.lista_inner_frame, text=nome, font=("Arial", 12, "bold"),
                                bg="#3d0586", fg="white", relief="flat", command=mostrar_info)
                btn.pack(fill="x", padx=10, pady=5)

        elif tipo == "Proficiências":
            filtro = self.prof_filtro_var.get() if hasattr(self, 'prof_filtro_var') else "Geral"
            grupos = {
                "Força": D.Força,
                "Agilidade": D.Agilidade,
                "Vigor": D.Vigor,
                "Inteligência": D.Inteligencia,
                "Presença": D.Presença,
                "Tática": D.Tática
            }
            todas = D.Proficiencias if filtro == "Geral" or filtro not in grupos else grupos[filtro]

            for nome in todas:
                tk.Label(self.lista_inner_frame, text=nome, bg="#14014a", fg="white", font=("Arial", 12, "bold"), anchor="w").pack(fill="x", padx=10, pady=3)

        elif tipo == "Itens":
            tipo_item = self.tipo_item_var.get() if hasattr(self, 'tipo_item_var') else None
            tipos_dict = {
                "Item": D.Items,
                "Consumíveis": D.Consumiveis,
                "Explosivos": D.Explosivos,
                "Municao": D.Munições,
                "Melee": D.Melees,
                "Ranged": D.Rangeds,
                "Protecao": D.Protecoes,
                "Melhoria": D.Melhorias
            }

            if tipo_item not in tipos_dict:
                return
            pool = tipos_dict[tipo_item]

            for nome, construtor in pool.items():
                def abrir_popup(n=nome, c=construtor):
                    item = c()
                    popup = tk.Toplevel(self)
                    popup.title(n)
                    popup.geometry("300x200")
                    popup.configure(bg="#1a1a2e")

                    tk.Label(popup, text=f"Nome: {item.nome}", fg="white", bg="#1a1a2e", font=("Arial", 12, "bold")).pack(pady=10)
                    peso = getattr(item, "peso", "N/A")
                    tk.Label(popup, text=f"Peso: {peso}", fg="lightgreen", bg="#1a1a2e", font=("Arial", 11)).pack()

                    for attr in vars(item):
                        if attr not in ("nome", "peso"):
                            valor = getattr(item, attr)
                            tk.Label(popup, text=f"{attr.capitalize()}: {valor}", fg="white", bg="#1a1a2e", font=("Arial", 10)).pack(anchor="w", padx=15)

                    tk.Button(popup, text="Fechar", command=popup.destroy, bg="#4e00b3", fg="white").pack(pady=15)

                btn = tk.Button(self.lista_inner_frame, text=nome, font=("Arial", 12, "bold"), bg="#3d0586", fg="white", command=abrir_popup)
                btn.pack(fill="x", padx=5, pady=2)

        elif tipo == "Kits":
            nome_kit = self.kit_var.get() if hasattr(self, 'kit_var') else None
            if nome_kit not in D.kits_por_nome:
                return

            kit = D.kits_por_nome[nome_kit]
            contagem = {}
            for item in kit.itens:
                nome = getattr(item, "nome", str(item))
                contagem[nome] = contagem.get(nome, 0) + 1

            for nome, qtd in contagem.items():
                texto = f"{nome} x{qtd}"
                tk.Label(self.lista_inner_frame, text=texto, bg="#14014a", fg="white", font=("Arial", 12, "bold"), anchor="w").pack(fill="x", padx=10, pady=3)

        self.lista_canvas.configure(scrollregion=self.lista_canvas.bbox("all"))

    def atualizar_lista_conteudo(self, *args):
        # Limpa o conteúdo anterior
        for widget in self.lista_inner_frame.winfo_children():
            widget.destroy()

        tipo = self.lista_tipo_var.get()

        if tipo == "NPCs":
            for grupo, npcs in D.NPCs_predefinidos.items():
                lbl_grupo = tk.Label(self.lista_inner_frame, text=f"[{grupo}]", bg="#14014a", fg="#c5c5ff", font=("Arial", 12, "bold"))
                lbl_grupo.pack(anchor="w", padx=10, pady=(8, 2))

                for nome, f, a, v, i, p, t in npcs:
                    def mostrar(n=nome, g=grupo, ff=f, aa=a, vv=v, ii=i, pp=p, tt=t):
                        npc = CB.NPC(g, n, ff, aa, vv, ii, pp, tt)
                        self.mostrar_popup_npc(npc)
                    btn = tk.Button(self.lista_inner_frame, text=nome, bg="#3d0586", fg="white", font=("Arial", 11), command=mostrar)
                    btn.pack(fill="x", padx=20, pady=2)

        elif tipo == "Itens":
            pools_nomeados = [
                ("Itens Gerais", D.Items),
                ("Consumíveis", D.Consumiveis),
                ("Explosivos", D.Explosivos),
                ("Munições", D.Munições),
                ("Armas Corpo-a-Corpo", D.Melees),
                ("Armas de Fogo", D.Rangeds),
                ("Proteções", D.Protecoes),
                ("Melhorias", D.Melhorias)
            ]
            for titulo, pool in pools_nomeados:
                if not pool:
                    continue

                lbl_titulo = tk.Label(self.lista_inner_frame, text=titulo, bg="#14014a", fg="#c5c5ff", font=("Arial", 12, "bold"))
                lbl_titulo.pack(anchor="w", padx=10, pady=(10, 2))

                for nome, construtor in sorted(pool.items()):
                    def abrir(n=nome, c=construtor):
                        item = c()
                        self.mostrar_popup_detalhes_item(item)
                    btn = tk.Button(self.lista_inner_frame, text=nome, bg="#3d0586", fg="white", font=("Arial", 11), command=abrir)
                    btn.pack(fill="x", padx=20, pady=2)

        elif tipo == "Kits":
            for nome, kit in D.kits_por_nome.items():
                def abrir(n=nome, k=kit):
                    self.mostrar_popup_kit(n, k)
                btn = tk.Button(self.lista_inner_frame, text=nome, bg="#3d0586", fg="white", font=("Arial", 11), command=abrir)
                btn.pack(fill="x", padx=20, pady=2)

        elif tipo == "Proficiências":
            for nome in D.Proficiencias:
                lbl = tk.Label(self.lista_inner_frame, text=nome, bg="#14014a", fg="white", font=("Arial", 12, "bold"), anchor="w")
                lbl.pack(fill="x", padx=10, pady=3)

        self.lista_canvas.configure(scrollregion=self.lista_canvas.bbox("all"))

    def mostrar_popup_npc(self, npc):
        try:
            stats = npc.__repr__()  # usa o dicionário personalizado do NPC
            nome = stats.get("Grupo", "NPC Sem Grupo")
            tipo = stats.get("Classe", npc.__class__.__name__)

            popup = tk.Toplevel(self)
            popup.title(f"Detalhes do NPC: {tipo}")
            popup.configure(bg="#1a0869")
            popup.geometry("500x420")
            popup.resizable(False, False)

            tk.Label( popup, text=f"{tipo} (Grupo: {nome})", font=("Arial", 16, "bold"), bg="#1a0869", fg="white").pack(pady=(20, 10))

            frame_scroll = tk.Frame(popup, bg="#1a0869", height=250)
            frame_scroll.pack(pady=10, padx=20, fill='both', expand=True)

            canvas = tk.Canvas(frame_scroll, bg="#130f26", highlightthickness=0)
            scrollbar = tk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
            scroll_frame = tk.Frame(canvas, bg="#130f26")

            scroll_frame.bind( "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            for chave, valor in stats.items():
                linha = tk.Frame(scroll_frame, bg="#130f26")
                linha.pack(anchor='w', pady=2, padx=10)
                tk.Label(linha, text=f"{chave}:", font=("Arial", 12, "bold"), fg="white", bg="#130f26").pack(side="left")
                tk.Label(linha, text=f" {valor}", font=("Arial", 12), fg="white", bg="#130f26").pack(side="left")

            btn_fechar = tk.Button(popup, text="Fechar", command=popup.destroy, bg="#004080", fg="white", font=("Arial", 12),width=10, height=10)
            btn_fechar.pack(pady=20)

        except Exception as e:
            print("Erro ao mostrar detalhes do NPC:", e)

    def mostrar_popup_detalhes_item(self, item_obj):
        try:
            stats = item_obj.stats()
            tipo = item_obj.__class__.__name__

            popup = tk.Toplevel(self)
            popup.title(f"Detalhes do Item: {stats.get('Nome', 'Desconhecido')}")
            popup.configure(bg="#1a0869")
            popup.geometry("600x400")
            popup.resizable(False, False)

            lbl_titulo = tk.Label(
                popup,
                text=f"{stats.get('Nome', 'Item Sem Nome')} ({tipo})",
                font=("Arial", 16, "bold"),
                bg="#1a0869",
                fg="white"
            )
            lbl_titulo.pack(pady=(20, 10))

            frame_scroll = tk.Frame(popup, bg="#1a0869", height=250)
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

            frame_acoes = tk.Frame(popup, bg="#1a0869", height=60)
            frame_acoes.pack(pady=(10, 0), fill='x')

            if tipo == "Protecao":
                btn_equipar = tk.Button(
                    frame_acoes,
                    text="Equipar", 
                    command=lambda p=popup: self.abrir_popup_equipar_protecao(item_obj, p),
                    bg="#004080", fg="white", font=("Arial", 10), width=10
                )
                btn_equipar.pack(side="left", padx=(10, 10))

            btn_fechar = tk.Button(popup, text="Fechar", command=popup.destroy, bg="#004080", fg="white", font=("Arial", 12))
            btn_fechar.pack(side="right", padx=(0, 30), pady=20)

        except Exception as e:
            print("Erro ao mostrar detalhes do item:", e)

    def mostrar_popup_kit(self, nome, kit):
        popup = tk.Toplevel(self)
        popup.title(f"Kit: {nome}")
        popup.configure(bg="#1a0869")
        popup.geometry("400x400")
        popup.resizable(False, False)

        tk.Label(
            popup,
            text=nome,
            font=("Arial", 16, "bold"),
            bg="#1a0869",
            fg="white"
        ).pack(pady=(20, 10))

        # Frame com scroll para os itens do kit
        frame_scroll = tk.Frame(popup, bg="#1a0869")
        frame_scroll.pack(padx=20, pady=10, fill='both', expand=True)

        canvas = tk.Canvas(frame_scroll, bg="#130f26", highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#130f26")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Agrupa os itens por nome
        contagem = {}
        for item in kit.itens:
            item_nome = getattr(item, "nome", str(item))
            contagem[item_nome] = contagem.get(item_nome, 0) + 1

        for item_nome, qtd in contagem.items():
            linha = tk.Frame(scroll_frame, bg="#130f26")
            linha.pack(anchor="w", pady=2, padx=10)
            tk.Label(linha, text=f"{item_nome}:", font=("Arial", 12, "bold"), fg="white", bg="#130f26").pack(side="left")
            tk.Label(linha, text=f" x{qtd}", font=("Arial", 12), fg="white", bg="#130f26").pack(side="left")

        # Botão Fechar
        btn_fechar = tk.Button(popup, text="Fechar", command=popup.destroy, bg="#004080", fg="white", font=("Arial", 12))
        btn_fechar.pack(pady=10)
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