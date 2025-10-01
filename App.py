import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import Dados as D
import Codigos as CB
import re, random, os, json, traceback


### TELA PRINCIPAL ###
### TELA PRINCIPAL ###
### TELA PRINCIPAL ###
class MainScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#130f26")

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
        
        # Frame para listbox com visual melhorado
        lista_frame = tk.Frame(main_container, bg="#1a0869")
        lista_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Listbox estilizada
        self.sessoes_listbox = tk.Listbox(lista_frame, font=("Arial", 12, "bold"), 
                                         bg="#2a1f3d", fg="#ffffff", 
                                         selectbackground="#4a3f5d", 
                                         selectforeground="#ffffff",
                                         relief="sunken", bd=2,
                                         height=12, activestyle="dotbox")
        self.sessoes_listbox.pack(side="left", fill="both", expand=True)
        
        # Scrollbar estilizada
        scrollbar = tk.Scrollbar(lista_frame, orient="vertical", 
                               command=self.sessoes_listbox.yview,
                               bg="#2a1f3d", troughcolor="#130f26",
                               activebackground="#4a3f5d")
        scrollbar.pack(side="right", fill="y")
        self.sessoes_listbox.config(yscrollcommand=scrollbar.set)
        
        # Frame para controles - primeira linha
        controles1_frame = tk.Frame(main_container, bg="#1a0869")
        controles1_frame.pack(fill="x", pady=(0, 10))
        
        tk.Button(controles1_frame, text="🔄 Atualizar", command=self.atualizar_lista_sessoes,
                bg="#2a1f3d", fg="white", font=("Arial", 11, "bold"), 
                relief="raised", bd=2, activebackground="#4a3f5d",
                width=12).pack(side="left", padx=5)
        
        tk.Button(controles1_frame, text="📂 Carregar", command=self.carregar_sessao_selecionada,
                bg="#2a1f3d", fg="white", font=("Arial", 11, "bold"),
                relief="raised", bd=2, activebackground="#4a3f5d",
                width=12).pack(side="left", padx=5)
        
        tk.Button(controles1_frame, text="🗑️ Deletar", command=self.deletar_sessao_selecionada,
                bg="#8b1538", fg="white", font=("Arial", 11, "bold"),
                relief="raised", bd=2, activebackground="#a61e42",
                width=12).pack(side="left", padx=5)
        
        # Separador visual
        separator = tk.Frame(main_container, bg="#4a3f5d", height=2)
        separator.pack(fill="x", pady=10)
        
        # Frame para entrada de texto
        entrada_frame = tk.Frame(main_container, bg="#1a0869")
        entrada_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(entrada_frame, text="💾 Nome da sessão:", 
                fg="white", bg="#1a0869", font=("Arial", 12, "bold")).pack(anchor="w")
        
        self.nome_sessao_entry = tk.Entry(entrada_frame, font=("Arial", 12), 
                                        bg="#2a1f3d", fg="white", relief="sunken", bd=2,
                                        insertbackground="white")
        self.nome_sessao_entry.pack(fill="x", pady=5)
        
        # Frame para controles - segunda linha
        controles2_frame = tk.Frame(main_container, bg="#1a0869")
        controles2_frame.pack(fill="x")
        
        tk.Button(controles2_frame, text="➕ Nova Sessão", command=self.criar_nova_sessao,
                bg="#2a1f3d", fg="white", font=("Arial", 11, "bold"),
                relief="raised", bd=2, activebackground="#4a3f5d",
                width=15).pack(side="left", padx=5)
        
        tk.Button(controles2_frame, text="💾 Salvar Atual", command=self.salvar_sessao_atual,
                bg="#1a5f2a", fg="white", font=("Arial", 11, "bold"),
                relief="raised", bd=2, activebackground="#2a7f3a",
                width=15).pack(side="left", padx=5)
        
        tk.Button(controles2_frame, text="✏️ Renomear", command=self.renomear_sessao_selecionada,
                bg="#2a1f3d", fg="white", font=("Arial", 11, "bold"),
                relief="raised", bd=2, activebackground="#4a3f5d",
                width=15).pack(side="left", padx=5)
        
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
        """Atualiza a listbox com as sessões disponíveis"""
        try:
            self.sessoes_listbox.delete(0, tk.END)
            
            # Importa a função correta do módulo D
            from Dados import listar_sessoes
            sessoes = listar_sessoes()
            
            for sessao in sessoes:
                # Formato: "Nome - Data Atualização (X personagens em Y grupos)"
                status_icon = "🔄" if sessao.get('modificada', False) else "✨"
                item = f"{status_icon} {sessao['nome']} - ({sessao['total_personagens']} chars em {sessao['total_grupos']} grupos)"
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
            
            # Extrai o nome da sessão (após o emoji e antes do " - ")
            item_text = self.sessoes_listbox.get(selection[0])
            # Remove emoji e pega o nome até o primeiro " - "
            nome_sessao = item_text.split(" ", 1)[1].split(" - ")[0]
            
            # Importa a função correta do módulo D
            from Dados import carregar_sessao
            
            if carregar_sessao(nome_sessao):
                tk.messagebox.showinfo("Sucesso", f"Sessão '{nome_sessao}' carregada com sucesso!")
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
            
            # Extrai o nome da sessão
            item_text = self.sessoes_listbox.get(selection[0])
            nome_sessao = item_text.split(" ", 1)[1].split(" - ")[0]
            
            # Confirma a exclusão
            if tk.messagebox.askyesno("Confirmar Exclusão", 
                                    f"Tem certeza que deseja deletar a sessão '{nome_sessao}'?\n\nEsta ação não pode ser desfeita."):
                # Importa a função correta do módulo D
                from Dados import deletar_sessao
                
                if deletar_sessao(nome_sessao):
                    tk.messagebox.showinfo("Sucesso", f"Sessão '{nome_sessao}' deletada com sucesso!")
                    self.atualizar_lista_sessoes()
                else:
                    tk.messagebox.showerror("Erro", f"Erro ao deletar sessão '{nome_sessao}'")
                    
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Erro ao deletar sessão: {e}")

    def criar_nova_sessao(self):
        """Cria uma nova sessão vazia"""
        try:
            # Importa a função correta do módulo D
            from Dados import limpar_sessao_atual
            
            # Confirma se o usuário quer limpar a sessão atual
            if tk.messagebox.askyesno("Confirmar Nova Sessão", 
                                    "Criar uma nova sessão irá limpar todos os dados atuais.\n\nDeseja continuar?"):
                limpar_sessao_atual()
                tk.messagebox.showinfo("Sucesso", "Nova sessão criada! Todos os dados foram limpos da memória.")
                # Atualiza outras telas se necessário
                self.controller.atualizar_todas_telas()
                
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Erro ao criar nova sessão: {e}")

    def salvar_sessao_atual(self):
        """Salva a sessão atual com o nome especificado"""
        try:
            nome_sessao = self.nome_sessao_entry.get().strip()
            if not nome_sessao:
                tk.messagebox.showwarning("Aviso", "Digite um nome para a sessão.")
                return
            
            # Importa as funções corretas do módulo D
            from Dados import salvar_sessao, listar_sessoes
            
            # Verifica se já existe uma sessão com esse nome
            sessoes_existentes = listar_sessoes()
            sessao_existe = any(s['nome'] == nome_sessao for s in sessoes_existentes)
            
            if sessao_existe:
                if tk.messagebox.askyesno("Confirmar Sobrescrita", 
                                        f"A sessão '{nome_sessao}' já existe.\n\nDeseja sobrescrever?"):
                    if salvar_sessao(nome_sessao, sobrescrever=True):
                        tk.messagebox.showinfo("Sucesso", f"Sessão '{nome_sessao}' atualizada com sucesso!")
                        self.atualizar_lista_sessoes()
                        self.nome_sessao_entry.delete(0, tk.END)
                    else:
                        tk.messagebox.showerror("Erro", f"Erro ao atualizar sessão '{nome_sessao}'")
            else:
                if salvar_sessao(nome_sessao):
                    tk.messagebox.showinfo("Sucesso", f"Sessão '{nome_sessao}' salva com sucesso!")
                    self.atualizar_lista_sessoes()
                    self.nome_sessao_entry.delete(0, tk.END)
                else:
                    tk.messagebox.showerror("Erro", f"Erro ao salvar sessão '{nome_sessao}'")
                    
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Erro ao salvar sessão: {e}")

    def renomear_sessao_selecionada(self):
        """Renomeia a sessão selecionada"""
        try:
            selection = self.sessoes_listbox.curselection()
            if not selection:
                tk.messagebox.showwarning("Aviso", "Selecione uma sessão para renomear.")
                return
            
            nome_novo = self.nome_sessao_entry.get().strip()
            if not nome_novo:
                tk.messagebox.showwarning("Aviso", "Digite o novo nome para a sessão.")
                return
            
            # Extrai o nome atual da sessão
            item_text = self.sessoes_listbox.get(selection[0])
            nome_antigo = item_text.split(" ", 1)[1].split(" - ")[0]
            
            if nome_antigo == nome_novo:
                tk.messagebox.showwarning("Aviso", "O novo nome deve ser diferente do nome atual.")
                return
            
            # Confirma a renomeação
            if tk.messagebox.askyesno("Confirmar Renomeação", 
                                    f"Renomear sessão de:\n'{nome_antigo}'\npara:\n'{nome_novo}'?"):
                # Importa a função correta do módulo D
                from Dados import clonar_sessao, deletar_sessao
                
                # Como não há função renomear_sessao, usa clone + delete
                if clonar_sessao(nome_antigo, nome_novo):
                    if deletar_sessao(nome_antigo):
                        tk.messagebox.showinfo("Sucesso", f"Sessão renomeada com sucesso:\n'{nome_antigo}' → '{nome_novo}'")
                        self.atualizar_lista_sessoes()
                        self.nome_sessao_entry.delete(0, tk.END)
                    else:
                        tk.messagebox.showerror("Erro", "Sessão clonada, mas erro ao deletar a original.")
                        self.atualizar_lista_sessoes()
                else:
                    tk.messagebox.showerror("Erro", f"Erro ao renomear sessão. Verifique se o novo nome já existe.")
                    
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Erro ao renomear sessão: {e}")

    def validar_sessao_selecionada(self):
        """Valida a sessão selecionada"""
        try:
            selection = self.sessoes_listbox.curselection()
            if not selection:
                tk.messagebox.showwarning("Aviso", "Selecione uma sessão para validar.")
                return
            
            # Extrai o nome da sessão
            item_text = self.sessoes_listbox.get(selection[0])
            nome_sessao = item_text.split(" ", 1)[1].split(" - ")[0]
            
            # Importa a função de validação
            from Dados import validar_sessao
            
            valida, resultado = validar_sessao(nome_sessao)
            
            if valida:
                tk.messagebox.showinfo("Validação", f"✅ Sessão '{nome_sessao}' válida!\n\n{resultado}")
            else:
                tk.messagebox.showerror("Validação", f"❌ Problemas na sessão '{nome_sessao}':\n\n{resultado}")
                
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Erro ao validar sessão: {e}")

    def mostrar_status_sessao_atual(self):
        """Mostra o status da sessão atual carregada na memória"""
        try:
            from Dados import GruposDePersonagens, KitsDisponíveis
            
            if not GruposDePersonagens:
                tk.messagebox.showinfo("Status da Sessão", "📭 Nenhuma sessão carregada na memória")
                return
            
            # Calcula estatísticas
            total_personagens = 0
            detalhes_grupos = []
            
            for grupo, lista in GruposDePersonagens.items():
                total_personagens += len(lista)
                detalhes_grupos.append(f"👥 {grupo}: {len(lista)} personagens")
            
            status_text = f"📊 SESSÃO ATUAL CARREGADA:\n\n"
            status_text += "\n".join(detalhes_grupos)
            status_text += f"\n\n📈 Total: {total_personagens} personagens em {len(GruposDePersonagens)} grupos"
            
            if KitsDisponíveis:
                status_text += f"\n📦 {len(KitsDisponíveis)} kits disponíveis"
            
            tk.messagebox.showinfo("Status da Sessão", status_text)
            
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Erro ao verificar status da sessão: {e}")

    def TelaDeSelecao(self):
        self.controller.TelaDeSelecao()

    def TelaDeCombate(self):
        self.controller.TelaDeCombate()

    def TelaDeRegrasEItens(self):
        self.controller.TelaDeRegrasEItens()### TELA PRINCIPAL ###
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
        self.kit_management_frame.place(x=960, y=120, width=450, height=80)
        self.create_kit_management(self.kit_management_frame)

        # --- Lista de Kits ---
        self.kit_list_frame = tk.Frame(self, bg='#1a0869')
        self.kit_list_frame.place(x=960, y=210, width=450, height=470)
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
        """Função placeholder para gerar vários personagens - sem funcionalidade ainda"""
        messagebox.showinfo("Em desenvolvimento", "Funcionalidade 'Gerar Vários' ainda não implementada.")

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

    def create_kit_list_section(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        # Armazenar referência do frame atual para uso em outros métodos
        self.current_frame = frame

        label = tk.Label(frame, text="Kits Disponíveis", fg="white", bg="#1a0869", font=("Arial", 16, "bold"))
        label.place(x=10, y=10)

        canvas_frame = tk.Frame(frame, bg='#1a0869')
        canvas_frame.place(x=10, y=40, width=460, height=420)

        canvas = tk.Canvas(canvas_frame, bg="#1a0869", highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner_frame = tk.Frame(canvas, bg="#1a0869")
        canvas.create_window((0, 0), window=inner_frame, anchor='nw')
        inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Carregar kits disponíveis
        kits = D.KitsDisponíveis if hasattr(D, 'KitsDisponíveis') and D.KitsDisponíveis else {}
        
        if not kits:
            empty_label = tk.Label(inner_frame, text="Nenhum kit disponível", 
                                fg="gray", bg="#1a0869", font=("Arial", 12, "italic"))
            empty_label.pack(pady=20)
        else:
            # Organizar kits por raridade
            kits_por_raridade = {}
            for nome, kit in kits.items():
                raridade = kit.raridade
                if raridade not in kits_por_raridade:
                    kits_por_raridade[raridade] = []
                kits_por_raridade[raridade].append((nome, kit))

            # Mostrar kits organizados por raridade
            for raridade in sorted(kits_por_raridade.keys()):
                # Cabeçalho da raridade
                raridade_frame = tk.Frame(inner_frame, bg="#2a2647", relief="solid", bd=1)
                raridade_frame.pack(fill="x", pady=(10, 2), padx=5)
                
                raridade_label = tk.Label(raridade_frame, text=f"Raridade: {raridade}", 
                                        fg="yellow", bg="#2a2647", font=("Arial", 12, "bold"))
                raridade_label.pack(pady=3)

                # Kits desta raridade
                for nome_kit, kit_obj in kits_por_raridade[raridade]:
                    kit_frame = tk.Frame(inner_frame, bg="#1a0869", height=80)
                    kit_frame.pack(fill="x", pady=2, padx=5)

                    # Contar itens no kit
                    itens_kit = kit_obj.listar_itens()
                    total_itens = sum(item["quantidade"] for item in itens_kit)
                    tipos_itens = len(itens_kit)

                    # Botão principal do kit - abre o popup de visualização
                    kit_button = tk.Button(kit_frame,
                        text=f"{nome_kit}\n{tipos_itens} tipos de itens ({total_itens} total)",
                        bg="#1a0869", fg="white", font=("Arial", 11), anchor="w", justify="left",
                        command=lambda k=kit_obj: self.show_kit_contents(k), wraplength=210, height=3)
                    kit_button.pack(side="left", fill="x", expand=True, padx=(0, 5), pady=2)

                    # Frame para botão de ação
                    actions_frame = tk.Frame(kit_frame, bg="#1a0869")
                    actions_frame.pack(side="right", padx=5)

                    # Botão de apagar kit
                    delete_button = tk.Button(actions_frame, text="Apagar", bg="#DC143C", fg="white", 
                                        font=("Arial", 9, "bold"), width=9,
                                        command=lambda k=nome_kit: self.delete_kit(k))
                    delete_button.pack(pady=1)

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
        popup.title(f"Conteúdo do Kit: {kit_obj.nome}")
        popup.geometry("450x600")
        popup.configure(bg="#1a0869")
        popup.resizable(False, False)
        
        # Centralizar o popup
        if parent:
            popup.transient(parent)
        popup.grab_set()
        
        # Título
        title_label = tk.Label(popup, text=f"Kit: {kit_obj.nome}", 
                            fg="white", bg="#1a0869", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Informações do kit
        info_frame = tk.Frame(popup, bg="#2a2647", relief="solid", bd=1)
        info_frame.pack(pady=5, padx=15, fill="x")
        
        kit_info = tk.Label(info_frame, text=f"Raridade: {kit_obj.raridade}", 
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
        
        # Mostrar itens do kit
        itens_kit = kit_obj.listar_itens()
        if not itens_kit:
            empty_label = tk.Label(inner_frame, text="Kit vazio", 
                                fg="gray", bg="#1a0869", font=("Arial", 12, "italic"))
            empty_label.pack(pady=20)
        else:
            for i, item in enumerate(itens_kit):
                item_frame = tk.Frame(inner_frame, bg="#2a2647", relief="solid", bd=1)
                item_frame.pack(fill="x", pady=2, padx=5)
                
                item_label = tk.Label(item_frame, 
                                    text=f"• {item['nome']} - Quantidade: {item['quantidade']}", 
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
                
                # Feedback para o usuário
                tk.messagebox.showinfo("Sucesso", f"'{nome_item}' adicionado ao inventário!")
                
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

    ### CORREÇÃO DO MÉTODO REFRESH (adicionar antes dos outros métodos)

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
        regiao_var = tk.StringVar(value="Aleatória")
        regiao_menu = ttk.Combobox(regiao_frame, textvariable=regiao_var, state="readonly", width=30,
                          values=["Aleatória", "Cabeça", "Rosto", "Torso", "Pernas", "Braços"])
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
        def obter_regiao_final():
            if regiao_var.get() == "Aleatória":
                return "Aleatorio"
            return regiao_var.get()

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
            arma = next((i["item"] for i in atacante.equipados.itens if isinstance(i["item"], CB.Ranged) and i["item"].Id == arma_id), None)

            if not alvo or not arma:
                resultado_label.config(text="Erro: alvo ou arma inválido(s).", fg="red")
                return

            resultado = CB.acerto_ranged(
                atacante=atacante,
                alvo=alvo,
                Rolagem=rolagem,
                id_arma=arma.Id,
                distancia=distancia,
                disparos=disparos,
                regiao=regiao,
                BuffDano=buff_dano,
                BuffAcerto=buff_acerto
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
        self.item_selecionado = None
        
        # Mapeamento de tabelas para suas configurações
        self.configuracoes_tabelas = {
            "Itens": {
                "tabela_db": "Itens",
                "classe": CB.Item,
                "campos": ["nome", "peso"]
            },
            "Ranged": {
                "tabela_db": "Rangeds", 
                "classe": CB.Ranged,
                "campos": ["nome", "peso", "classe", "acao", "raridade", "calibre", "capacidade"]
            },
            "Melee": {
                "tabela_db": "Melees",
                "classe": CB.Melee, 
                "campos": ["nome", "peso", "classe", "tipo_dano", "raridade"]
            },
            "Proteção": {
                "tabela_db": "Protecoes",
                "classe": CB.Protecao,
                "campos": ["nome", "peso", "nivelBalistico", "absorcaoFisica", "absorcaoBalistica", "regiao"]
            },
            "Munições": {
                "tabela_db": "Municoes",
                "classe": CB.Municao,
                "campos": ["nome", "calibre", "dano", "perfuracao"]
            },
            "Explosivos": {
                "tabela_db": "Explosivos", 
                "classe": CB.Explosivo,
                "campos": ["nome", "peso", "raio", "dano", "tipo_dano"]
            },
            "Consumíveis": {
                "tabela_db": "Consumiveis",
                "classe": CB.Consumivel, 
                "campos": ["nome", "peso", "cura", "energia"]
            },
            "Melhorias": {
                "tabela_db": "Melhorias",
                "classe": CB.Melhoria,
                "campos": ["nome", "peso", "tipo", "modificadores"]
            },
            "Proficiências": {
                "tabela_db": "Proficiencias",
                "classe": CB.Proficiencia,
                "campos": ["nome", "atributo", "nivel"]
            },
            "NPCs": {
                "tabela_db": "NPCs", 
                "classe": dict,
                "campos": ["grupo", "classe", "forca", "agilidade", "vigor", "inteligencia", "tatica", "presenca"]
            },
            # Tabelas não implementadas ainda
            "Kits": {
            "tabela_db": "kits",
            "classe": CB.Kits,
            "campos": ["nome", "raridade", "inventario_resumo"]  # Campo especial para mostrar resumo do inventário
            },
            "Efeitos": {
                "tabela_db": "Efeitos",
                "classe": None,
                "campos": []  # TODO: Implementar quando a tabela existir
            },
            "Habilidades": {
                "tabela_db": "Habilidades",
                "classe": None,
                "campos": []  # TODO: Implementar quando a tabela existir
            }
        }
        
        self.setup_ui()
        self.setup_styles()

    def carregar_dados_kits(self):
        """Carrega dados específicos para kits"""
        kits_dict = D.carregar_kits_db()  # D é o módulo de dados
        data = []
        
        for nome, kit in kits_dict.items():
            # Garante que o inventário seja carregado corretamente
            try:
                # Força o carregamento do inventário se não estiver carregado
                if not hasattr(kit, 'inventario') or kit.inventario is None:
                    # Tenta recarregar o kit completo do banco
                    kit_completo = D.carregar_kit_completo_db(nome)  # Função que deve existir no módulo D
                    if kit_completo and hasattr(kit_completo, 'inventario'):
                        kit = kit_completo
                
                inventario_resumo = self.gerar_resumo_inventario(kit)
            except Exception as e:
                print(f"Erro ao carregar inventário do kit {nome}: {e}")
                inventario_resumo = "Erro ao carregar inventário"
            
            data.append({
                "nome": nome,
                "raridade": kit.raridade,
                "inventario_resumo": inventario_resumo,
                "_kit_objeto": kit,  # Armazena referência ao objeto completo
                "_dados_completos": {
                    "nome": kit.nome,
                    "raridade": kit.raridade,
                    "Id": getattr(kit, 'Id', None),
                    "inventario": self.inventario_para_dict(kit.inventario) if hasattr(kit, 'inventario') and kit.inventario else {}
                }
            })
        
        return data

    def gerar_resumo_inventario(self, kit):
        """Gera um resumo textual do inventário do kit"""
        if not hasattr(kit, 'inventario') or not kit.inventario:
            return "Inventário vazio"
        
        try:
            # Se o inventário tem método listar_itens, usa ele
            if hasattr(kit, 'listar_itens'):
                itens_info = kit.listar_itens()
                if not itens_info:
                    return "Inventário vazio"
                
                # Gera resumo mais detalhado
                tipos_count = {}
                total_itens = 0
                
                for item_info in itens_info:
                    total_itens += item_info.get('quantidade', 1)
                    
                    # Obtém o tipo real do objeto, não do campo 'tipo'
                    item_obj = item_info.get('objeto')
                    if item_obj:
                        # Determina o tipo baseado na classe do objeto
                        if isinstance(item_obj, CB.Melee):
                            tipo_display = 'Arma C.a.C.'
                        elif isinstance(item_obj, CB.Ranged):
                            tipo_display = 'Arma de Fogo'
                        elif isinstance(item_obj, CB.Protecao):
                            tipo_display = 'Proteção'
                        elif isinstance(item_obj, CB.Consumivel):
                            tipo_display = 'Consumível'
                        elif isinstance(item_obj, CB.Explosivo):
                            tipo_display = 'Explosivo'
                        elif isinstance(item_obj, CB.Municao):
                            tipo_display = 'Munição'
                        elif isinstance(item_obj, CB.Melhoria):
                            tipo_display = 'Melhoria'
                        else:
                            tipo_display = 'Item'
                    else:
                        tipo_display = 'Item'
                    
                    tipos_count[tipo_display] = tipos_count.get(tipo_display, 0) + item_info.get('quantidade', 1)
                
                # Cria resumo baseado nos tipos
                if len(tipos_count) == 1:
                    tipo, qtd = next(iter(tipos_count.items()))
                    return f"{qtd} {tipo}{'s' if qtd > 1 else ''}"
                else:
                    resumo_parts = []
                    for tipo, qtd in tipos_count.items():
                        resumo_parts.append(f"{qtd} {tipo}{'s' if qtd > 1 else ''}")
                    return ", ".join(resumo_parts)
            
            # Fallback: tenta contar itens diretamente
            elif hasattr(kit.inventario, 'itens'):
                total_itens = len(kit.inventario.itens)
                return f"{total_itens} item(s) no inventário"
            
            # Se tem slots
            elif hasattr(kit.inventario, 'slots'):
                slots_ocupados = sum(1 for slot in kit.inventario.slots.values() 
                                if hasattr(slot, 'item') and slot.item)
                return f"{slots_ocupados} slot(s) ocupado(s)"
            
            else:
                return "Inventário presente"
                
        except Exception as e:
            print(f"Erro ao gerar resumo do inventário: {e}")
            return "Erro ao ler inventário"

    def inventario_para_dict(self, inventario):
        """Converte inventário para dicionário para visualização"""
        if not inventario:
            return {}
        
        try:
            # Se tem método listar_itens, usa ele para gerar estrutura limpa
            if hasattr(inventario, 'listar_itens'):
                # Precisa usar o kit para chamar listar_itens
                kit = self.get_kit_atual()
                if kit and hasattr(kit, 'listar_itens'):
                    itens_info = kit.listar_itens()
                    inventario_dict = {}
                    for i, item_info in enumerate(itens_info):
                        item_obj = item_info.get("objeto")
                        
                        # Determina se tem ID baseado no objeto real
                        tem_id = hasattr(item_obj, 'Id') and item_obj.Id is not None
                        
                        # Determina o tipo real do objeto
                        if isinstance(item_obj, CB.Melee):
                            tipo = 'melee'
                        elif isinstance(item_obj, CB.Ranged):
                            tipo = 'ranged'
                        elif isinstance(item_obj, CB.Protecao):
                            tipo = 'protecao'
                        elif isinstance(item_obj, CB.Consumivel):
                            tipo = 'consumivel'
                        elif isinstance(item_obj, CB.Explosivo):
                            tipo = 'explosivo'
                        elif isinstance(item_obj, CB.Municao):
                            tipo = 'municao'
                        elif isinstance(item_obj, CB.Melhoria):
                            tipo = 'melhoria'
                        else:
                            tipo = 'item'
                        
                        inventario_dict[f"item_{i+1}"] = {
                            "nome": item_info.get("nome", ""),
                            "quantidade": item_info.get("quantidade", 1),
                            "tipo": tipo,
                            "tem_id": tem_id
                        }
                    return inventario_dict
            
            # Fallback: usa to_dict se disponível
            elif hasattr(inventario, 'to_dict'):
                return inventario.to_dict()
            
            # Último recurso: converte __dict__
            else:
                return vars(inventario)
                
        except Exception as e:
            print(f"Erro ao converter inventário para dict: {e}")
            return {"erro": str(e)}

    def atualizar_visualizacao_inventario(self):
        """Atualiza a visualização do inventário no campo de texto"""
        if "inventario" not in self.campos_entrada:
            return
        
        kit = self.get_kit_atual()
        if not kit:
            return
        
        text_widget = self.campos_entrada["inventario"]
        text_widget.delete("1.0", "end")
        
        try:
            # Agora o inventário vem do banco, então mostra os dados atuais
            if hasattr(kit, 'inventario') and kit.inventario:
                # Usa o método listar_itens se disponível para uma visualização mais limpa
                if hasattr(kit, 'listar_itens'):
                    itens_info = kit.listar_itens()
                    if itens_info:
                        inventario_texto = "=== INVENTÁRIO DO KIT ===\n\n"
                        for i, item_info in enumerate(itens_info, 1):
                            nome = item_info.get('nome', 'Item sem nome')
                            quantidade = item_info.get('quantidade', 1)
                            item_obj = item_info.get('objeto')
                            
                            # Determina o tipo real e se tem ID baseado no objeto
                            tem_id = hasattr(item_obj, 'Id') and item_obj.Id is not None
                            
                            if isinstance(item_obj, CB.Melee):
                                tipo = 'melee'
                            elif isinstance(item_obj, CB.Ranged):
                                tipo = 'ranged'
                            elif isinstance(item_obj, CB.Protecao):
                                tipo = 'protecao'
                            elif isinstance(item_obj, CB.Consumivel):
                                tipo = 'consumivel'
                            elif isinstance(item_obj, CB.Explosivo):
                                tipo = 'explosivo'
                            elif isinstance(item_obj, CB.Municao):
                                tipo = 'municao'
                            elif isinstance(item_obj, CB.Melhoria):
                                tipo = 'melhoria'
                            else:
                                tipo = 'item'
                            
                            inventario_texto += f"{i}. {nome}\n"
                            inventario_texto += f"   Quantidade: {quantidade}\n"
                            inventario_texto += f"   Tipo: {tipo.capitalize()}\n"
                            
                            if tem_id:
                                inventario_texto += f"   Item único (ID: {item_obj.Id})\n"
                            
                            # Informações específicas por tipo usando o objeto real
                            if isinstance(item_obj, CB.Melee):
                                if hasattr(item_obj, 'peso'):
                                    inventario_texto += f"   Peso: {item_obj.peso}\n"
                                if hasattr(item_obj, 'tipo_dano'):
                                    inventario_texto += f"   Tipo de Dano: {item_obj.tipo_dano}\n"
                                if hasattr(item_obj, 'classe'):
                                    inventario_texto += f"   Classe: {item_obj.classe}\n"
                                if hasattr(item_obj, 'raridade'):
                                    inventario_texto += f"   Raridade: {item_obj.raridade}\n"
                                if hasattr(item_obj, 'dano_simples'):
                                    inventario_texto += f"   Dano Simples: {item_obj.dano_simples}\n"
                                    
                            elif isinstance(item_obj, CB.Ranged):
                                if hasattr(item_obj, 'peso'):
                                    inventario_texto += f"   Peso: {item_obj.peso}\n"
                                if hasattr(item_obj, 'calibre'):
                                    inventario_texto += f"   Calibre: {item_obj.calibre}\n"
                                if hasattr(item_obj, 'acao'):
                                    inventario_texto += f"   Ação: {item_obj.acao}\n"
                                if hasattr(item_obj, 'capacidade'):
                                    inventario_texto += f"   Capacidade: {item_obj.capacidade}\n"
                                if hasattr(item_obj, 'raridade'):
                                    inventario_texto += f"   Raridade: {item_obj.raridade}\n"
                                    
                            elif isinstance(item_obj, CB.Protecao):
                                if hasattr(item_obj, 'peso'):
                                    inventario_texto += f"   Peso: {item_obj.peso}\n"
                                if hasattr(item_obj, 'nivelBalistico'):
                                    inventario_texto += f"   Nível Balístico: {item_obj.nivelBalistico}\n"
                                if hasattr(item_obj, 'regiao'):
                                    inventario_texto += f"   Região: {item_obj.regiao}\n"
                                if hasattr(item_obj, 'absorcaoFisica'):
                                    inventario_texto += f"   Absorção Física: {item_obj.absorcaoFisica}\n"
                                if hasattr(item_obj, 'absorcaoBalistica'):
                                    inventario_texto += f"   Absorção Balística: {item_obj.absorcaoBalistica}\n"
                                    
                            elif isinstance(item_obj, CB.Consumivel):
                                if hasattr(item_obj, 'peso'):
                                    inventario_texto += f"   Peso: {item_obj.peso}\n"
                                if hasattr(item_obj, 'cura'):
                                    inventario_texto += f"   Cura: {item_obj.cura}\n"
                                if hasattr(item_obj, 'energia'):
                                    inventario_texto += f"   Energia: {item_obj.energia}\n"
                                    
                            elif isinstance(item_obj, CB.Municao):
                                if hasattr(item_obj, 'calibre'):
                                    inventario_texto += f"   Calibre: {item_obj.calibre}\n"
                                if hasattr(item_obj, 'dano'):
                                    inventario_texto += f"   Dano: {item_obj.dano}\n"
                                if hasattr(item_obj, 'perfuracao'):
                                    inventario_texto += f"   Perfuração: {item_obj.perfuracao}\n"
                            
                            elif isinstance(item_obj, CB.Explosivo):
                                if hasattr(item_obj, 'peso'):
                                    inventario_texto += f"   Peso: {item_obj.peso}\n"
                                if hasattr(item_obj, 'raio'):
                                    inventario_texto += f"   Raio: {item_obj.raio}\n"
                                if hasattr(item_obj, 'dano'):
                                    inventario_texto += f"   Dano: {item_obj.dano}\n"
                                if hasattr(item_obj, 'tipo_dano'):
                                    inventario_texto += f"   Tipo de Dano: {item_obj.tipo_dano}\n"
                            
                            elif isinstance(item_obj, CB.Melhoria):
                                if hasattr(item_obj, 'peso'):
                                    inventario_texto += f"   Peso: {item_obj.peso}\n"
                                if hasattr(item_obj, 'tipo'):
                                    inventario_texto += f"   Tipo: {item_obj.tipo}\n"
                                if hasattr(item_obj, 'modificadores'):
                                    inventario_texto += f"   Modificadores: {item_obj.modificadores}\n"
                            
                            else:
                                # Item genérico
                                if hasattr(item_obj, 'peso'):
                                    inventario_texto += f"   Peso: {item_obj.peso}\n"
                            
                            inventario_texto += "\n"
                        
                        text_widget.insert("1.0", inventario_texto)
                    else:
                        text_widget.insert("1.0", "Inventário vazio")
                else:
                    # Fallback: mostra como JSON mas com dados mais detalhados
                    inventario_dict = self.inventario_para_dict(kit.inventario)
                    inventario_str = json.dumps(inventario_dict, indent=2, ensure_ascii=False)
                    text_widget.insert("1.0", inventario_str)
            else:
                text_widget.insert("1.0", "Inventário não inicializado")
                
        except Exception as e:
            text_widget.insert("1.0", f"Erro ao carregar inventário: {e}")
            print(f"Erro na visualização do inventário: {e}")
            import traceback
            print(f"Traceback completo: {traceback.format_exc()}")

    def get_kit_atual(self):
        """Obtém o kit atualmente selecionado"""
        if not self.item_selecionado or self.item_selecionado not in self.dados_atuais:
            return None
        
        dados_item = self.dados_atuais[self.item_selecionado]
        return dados_item.get("_kit_objeto")

    def abrir_popup_adicionar_item_kit(self):
        """Abre popup para adicionar item ao kit"""
        kit = self.get_kit_atual()
        if not kit:
            messagebox.showwarning("Aviso", "Nenhum kit selecionado!")
            return
        
        popup = tk.Toplevel()
        popup.title("Adicionar Item ao Kit")
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
        btn_voltar = tk.Button(popup, text="Voltar", command=popup.destroy, 
                            bg="#a00c0c", fg="white", font=("Arial", 12))
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

                btn_item = tk.Button(frame_item, text=nome_item,
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
                    messagebox.showerror("Erro", "Quantidade inválida.")
                    return

            try:
                # Adiciona o item ao inventário
                kit.inventario.gerenciar_item(item_objeto=item_obj, quantidade=quantidade, operacao="adicionar")
                
                # Salva o kit atualizado no banco (agora com inventário)
                if D.salvar_kit_no_banco(kit):
                    self.atualizar_visualizacao_inventario()
                    # Atualiza os dados locais
                    D.refresh_kits()
                    messagebox.showinfo("Sucesso", f"Item '{nome_item}' adicionado ao kit e salvo no banco!")
                else:
                    messagebox.showerror("Erro", "Item adicionado mas falha ao salvar no banco!")
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar item: {e}")

        categoria_var.trace_add("write", exibir_itens)

    def abrir_popup_remover_item_kit(self):
        """Abre popup para remover item do kit"""
        kit = self.get_kit_atual()
        if not kit:
            messagebox.showwarning("Aviso", "Nenhum kit selecionado!")
            return
        
        # Obter lista de itens no inventário
        try:
            itens_info = kit.listar_itens() if hasattr(kit, 'listar_itens') else []
        except:
            itens_info = []
            
        if not itens_info:
            messagebox.showinfo("Info", "O inventário do kit está vazio!")
            return
        
        popup = tk.Toplevel()
        popup.title("Remover Item do Kit")
        popup.configure(bg="#1a0869")
        popup.geometry("400x500")

        tk.Label(popup, text="Itens no Kit:", bg="#1a0869", fg="white", font=("Arial", 16)).pack(pady=10)

        # Área de scroll
        frame_scroll = tk.Frame(popup, bg="#1a0869")
        frame_scroll.pack(expand=True, fill="both", padx=10, pady=10)

        canvas = tk.Canvas(frame_scroll, bg="#1a0869", highlightthickness=0, width=350, height=350)
        scrollbar = tk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a0869")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        quantidade_widgets = {}

        def remover_item(nome_item, tem_id):
            try:
                if tem_id:
                    # Item único - remover diretamente
                    quantidade = 1
                else:
                    # Item stackável - obter quantidade
                    qtd_str = quantidade_widgets[nome_item].get()
                    try:
                        quantidade = int(qtd_str)
                        if quantidade <= 0:
                            raise ValueError
                    except ValueError:
                        messagebox.showerror("Erro", "Quantidade inválida.")
                        return

                # Encontrar o objeto do item no inventário
                item_obj = None
                if hasattr(kit.inventario, 'slots'):
                    for slot in kit.inventario.slots.values():
                        if hasattr(slot, 'item') and slot.item and slot.item.nome == nome_item:
                            item_obj = slot.item
                            break
                elif hasattr(kit.inventario, 'itens'):
                    for item in kit.inventario.itens:
                        if hasattr(item, 'nome') and item.nome == nome_item:
                            item_obj = item
                            break

                if item_obj:
                    kit.inventario.gerenciar_item(item_objeto=item_obj, quantidade=quantidade, operacao="remover")
                    
                    # Salva o kit atualizado no banco
                    if D.salvar_kit_no_banco(kit):
                        self.atualizar_visualizacao_inventario()
                        # Atualiza os dados locais
                        D.refresh_kits()
                        messagebox.showinfo("Sucesso", f"Item '{nome_item}' removido do kit e salvo no banco!")
                        popup.destroy()
                        # Reabrir popup atualizado se ainda há itens
                        self.abrir_popup_remover_item_kit()
                    else:
                        messagebox.showerror("Erro", "Item removido mas falha ao salvar no banco!")
                else:
                    messagebox.showerror("Erro", f"Item '{nome_item}' não encontrado no inventário!")
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover item: {e}")

        # Exibir itens
        for item_info in itens_info:
            nome = item_info["nome"]
            quantidade_atual = item_info["quantidade"]
            tem_id = item_info.get("tem_id", False)

            frame_item = tk.Frame(scrollable_frame, bg="#1a0869")
            frame_item.pack(fill="x", pady=2)

            # Mostrar nome e quantidade atual
            info_text = f"{nome} (Qtd: {quantidade_atual})"
            tk.Label(frame_item, text=info_text, bg="#1a0869", fg="white", 
                    font=("Arial", 10)).pack(side="left", padx=5)

            if not tem_id:
                # Campo para quantidade a remover
                qtd_var = tk.StringVar(value="1")
                qtd_entry = tk.Entry(frame_item, textvariable=qtd_var, width=5, font=("Arial", 10))
                qtd_entry.pack(side="right", padx=5)
                quantidade_widgets[nome] = qtd_var

            # Botão remover
            btn_remover = tk.Button(frame_item, text="Remover",
                bg="#e74c3c", fg="white", font=("Arial", 10),
                command=lambda n=nome, t=tem_id: remover_item(n, t))
            btn_remover.pack(side="right", padx=5)

        # Botão Voltar
        btn_voltar = tk.Button(popup, text="Voltar", command=popup.destroy, 
                            bg="#a00c0c", fg="white", font=("Arial", 12))
        btn_voltar.pack(pady=10, side="bottom")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("default")
        
        # Configurações para Combobox
        style.configure("CustomCombobox.TCombobox", 
                       foreground="white", 
                       background="#2a1f4a", 
                       fieldbackground="#2a1f4a", 
                       bordercolor="#1a0869", 
                       arrowcolor="white", 
                       font=("Arial", 12))
        
        # Configurações para Treeview
        style.configure("Custom.Treeview",
                       background="#2a1f4a",
                       foreground="white",
                       rowheight=25,
                       fieldbackground="#2a1f4a")
        style.map("Custom.Treeview",
                 background=[('selected', '#1a0869')])
        
        # Configurações para Entry
        style.configure("Custom.TEntry",
                       fieldbackground="#2a1f4a",
                       bordercolor="#1a0869",
                       foreground="white")

    def setup_ui(self):
        # Botões de navegação
        tk.Button(self, text="Tela inicial", height=2, command=self.TelaInicial,
                bg="#1a0869", fg="white", font=("Arial", 16)).place(x=20, y=10, width=250, height=50)
        
        tk.Button(self, text="Seleção", height=2, command=self.TelaDeSelecao,
                bg="#1a0869", fg="white", font=("Arial", 16)).place(x=280, y=10, width=250, height=50)

        tk.Button(self, text="Combate", height=2, command=self.TelaDeCombate,
                bg="#1a0869", fg="white", font=("Arial", 16)).place(x=540, y=10, width=250, height=50)
        
        tk.Label(self, text="Administração de Dados", fg="white", bg="#1a0869",
                font=("Arial", 16, "bold")).place(x=800, y=10, width=250, height=50)

        # Seção de seleção de tabela
        tk.Label(self, text="Selecionar Tabela:", fg="white", bg="#130f26",
                font=("Arial", 14, "bold")).place(x=20, y=80)
        
        self.combo_tabelas = ttk.Combobox(self, style="CustomCombobox.TCombobox", 
                                         values=list(self.configuracoes_tabelas.keys()),
                                         state="readonly", font=("Arial", 12))
        self.combo_tabelas.place(x=20, y=110, width=300, height=35)
        self.combo_tabelas.bind('<<ComboboxSelected>>', self.on_tabela_selecionada)

        # Botão para atualizar dados
        tk.Button(self, text="Atualizar Dados", command=self.atualizar_dados,
                bg="#2a1f4a", fg="white", font=("Arial", 12)).place(x=340, y=110, width=150, height=35)

        # Lista de itens
        tk.Label(self, text="Itens da Tabela:", fg="white", bg="#130f26",
                font=("Arial", 14, "bold")).place(x=20, y=160)

        # Frame para Treeview com scrollbars
        tree_frame = tk.Frame(self, bg="#130f26")
        tree_frame.place(x=20, y=190, width=800, height=400)

        # Treeview
        self.tree = ttk.Treeview(tree_frame, style="Custom.Treeview")
        self.tree.bind('<<TreeviewSelect>>', self.on_item_selecionado)

        # Scrollbars
        v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        # Grid do Treeview
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Botões de ação
        tk.Button(self, text="Novo Item", command=self.novo_item,
                bg="#0d7377", fg="white", font=("Arial", 14)).place(x=20, y=610, width=150, height=40)
        
        tk.Button(self, text="Editar Item", command=self.editar_item,
                bg="#f39c12", fg="white", font=("Arial", 14)).place(x=180, y=610, width=150, height=40)
        
        tk.Button(self, text="Remover Item", command=self.remover_item,
                bg="#e74c3c", fg="white", font=("Arial", 14)).place(x=340, y=610, width=150, height=40)

        # Seção de edição/criação
        tk.Label(self, text="Detalhes do Item:", fg="white", bg="#130f26",
                font=("Arial", 14, "bold")).place(x=850, y=160)

        # Frame scrollável para campos
        self.canvas_campos = tk.Canvas(self, bg="#2a1f4a", width=720, height=430)
        self.canvas_campos.place(x=850, y=190)

        self.frame_campos = tk.Frame(self.canvas_campos, bg="#2a1f4a")
        self.scrollbar_campos = ttk.Scrollbar(self, orient="vertical", command=self.canvas_campos.yview)
        self.canvas_campos.configure(yscrollcommand=self.scrollbar_campos.set)

        self.scrollbar_campos.place(x=1570, y=190, height=430)
        self.canvas_campos.create_window((0, 0), window=self.frame_campos, anchor="nw")

        # Botões de ação para edição
        tk.Button(self, text="Salvar", command=self.salvar_item,
                bg="#27ae60", fg="white", font=("Arial", 14)).place(x=850, y=640, width=150, height=40)
        
        tk.Button(self, text="Cancelar", command=self.cancelar_edicao,
                bg="#95a5a6", fg="white", font=("Arial", 14)).place(x=1010, y=640, width=150, height=40)

        # Dicionário para armazenar os widgets de entrada
        self.campos_entrada = {}

    def atualizar_dados(self):
        """Atualiza os dados da tabela atual"""
        if not self.tabela_atual:
            messagebox.showwarning("Aviso", "Selecione uma tabela primeiro!")
            return
        
        # Recarrega os dados da tabela atual
        self.carregar_dados_tabela()
        messagebox.showinfo("Sucesso", f"Dados da tabela '{self.tabela_atual}' atualizados!")

    def on_tabela_selecionada(self, event=None):
        """Chamado quando uma tabela é selecionada no combobox"""
        self.tabela_atual = self.combo_tabelas.get()
        self.carregar_dados_tabela()
        self.limpar_campos_edicao()

    def carregar_dados_tabela(self):
        """Carrega os dados da tabela selecionada"""
        if not self.tabela_atual:
            return
        
        try:
            config = self.configuracoes_tabelas[self.tabela_atual]
            
            # Verifica se a tabela está implementada
            if not config["campos"]:
                messagebox.showwarning("Aviso", f"Tabela '{self.tabela_atual}' ainda não implementada!")
                self.dados_atuais = {}
                self.atualizar_treeview()
                return
            

            if self.tabela_atual == "NPCs":
                data = D.carregar_tipos_npcs_db()
            elif self.tabela_atual == "Proficiências":
                profs_dict = D.carregar_proficiencias_db()
                data = []
                for nome, prof in profs_dict.items():
                    data.append({
                        "nome": nome,
                        "atributo": prof.atributo,
                        "nivel": prof.nivel
                    })
            elif self.tabela_atual == "Kits":
                data = self.carregar_dados_kits()
            else:
                # Para outras tabelas, usa função genérica
                data = D.carregar_dados_tabela_generica(config["tabela_db"])
            
            self.dados_atuais = {}
            
            # Processamento especial para diferentes tipos de tabelas
            if self.tabela_atual == "NPCs":
                # Para NPCs, a chave primária é 'classe'
                for item in data:
                    chave = item.get("classe", f"npc_{item.get('grupo', 'sem_grupo')}")
                    self.dados_atuais[chave] = item
            
            elif self.tabela_atual == "Kits":
                # Para kits, processa os dados carregados
                for item in data:
                    nome = item.get("nome")
                    if nome:
                        self.dados_atuais[nome] = item
                    
            elif self.tabela_atual == "Proficiências":
                for item in data:
                    nome = item["nome"]
                    self.dados_atuais[nome] = item
                    
            else:
                # Para outras tabelas, usa 'nome' como chave
                for item in data:
                    nome = item.get("nome")
                    if nome:
                        self.dados_atuais[nome] = item
            
            self.atualizar_treeview()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")
            print(f"Erro detalhado: {traceback.format_exc()}")

    def atualizar_treeview(self):
        """Atualiza o Treeview com os dados atuais"""
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not self.tabela_atual or not self.dados_atuais:
            return
        
        config = self.configuracoes_tabelas[self.tabela_atual]
        campos = config["campos"]
        
        # Configurar colunas
        self.tree["columns"] = campos
        self.tree["show"] = "headings"
        
        for campo in campos:
            self.tree.heading(campo, text=campo.title())
            self.tree.column(campo, width=100, minwidth=50)
        
        # Adicionar dados
        for chave, dados in self.dados_atuais.items():
            valores = []
            for campo in campos:
                valor = dados.get(campo, "")
                if isinstance(valor, (dict, list)):
                    valor = json.dumps(valor)
                valores.append(str(valor))
            self.tree.insert("", "end", values=valores, tags=(chave,))

    def on_item_selecionado(self, event=None):
        """Chamado quando um item é selecionado no Treeview"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        tags = item.get("tags", [])
        if tags:
            self.item_selecionado = tags[0]
            self.carregar_item_para_edicao()

    def criar_campos_edicao(self, dados=None):
        """Cria os campos de edição baseados na tabela selecionada"""
        # Limpar campos existentes
        for widget in self.frame_campos.winfo_children():
            widget.destroy()
        self.campos_entrada.clear()

        
        if self.tabela_atual == "Kits":
            # Campo Nome
            tk.Label(self.frame_campos, text="Nome:", 
                    fg="white", bg="#2a1f4a", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
            entry_nome = tk.Entry(self.frame_campos, bg="#130f26", fg="white", 
                                font=("Arial", 12), width=50)
            entry_nome.grid(row=0, column=1, padx=5, pady=5)
            if dados and "nome" in dados:
                entry_nome.insert(0, str(dados["nome"]))
            self.campos_entrada["nome"] = entry_nome
            
            # Campo Raridade
            tk.Label(self.frame_campos, text="Raridade:", 
                    fg="white", bg="#2a1f4a", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
            combo_raridade = ttk.Combobox(self.frame_campos, values=["Comum", "Incomum", "Raro", "Épico", "Lendário"],
                                        state="readonly", font=("Arial", 12), width=47)
            combo_raridade.grid(row=1, column=1, padx=5, pady=5)
            if dados and "raridade" in dados:
                combo_raridade.set(dados["raridade"])
            self.campos_entrada["raridade"] = combo_raridade
            
            # Botões de gerenciamento de inventário
            frame_botoes = tk.Frame(self.frame_campos, bg="#2a1f4a")
            frame_botoes.grid(row=2, column=0, columnspan=2, pady=10)
            
            tk.Button(frame_botoes, text="Adicionar Item", command=self.abrir_popup_adicionar_item_kit,
                    bg="#0d7377", fg="white", font=("Arial", 12)).pack(side="left", padx=5)
            
            tk.Button(frame_botoes, text="Remover Item", command=self.abrir_popup_remover_item_kit,
                    bg="#e74c3c", fg="white", font=("Arial", 12)).pack(side="left", padx=5)
            
            # Campo Inventário (apenas visualização)
            tk.Label(self.frame_campos, text="Inventário:", 
                    fg="white", bg="#2a1f4a", font=("Arial", 12)).grid(row=3, column=0, sticky="nw", padx=5, pady=5)
            text_inventario = scrolledtext.ScrolledText(self.frame_campos, height=10, width=50, 
                                                    bg="#130f26", fg="white", font=("Arial", 10))
            text_inventario.grid(row=3, column=1, padx=5, pady=5)
            
            if dados and "inventario" in dados:
                # Mostra o inventário de forma legível
                inventario_str = json.dumps(dados["inventario"], indent=2, ensure_ascii=False)
                text_inventario.insert("1.0", inventario_str)
            else:
                text_inventario.insert("1.0", "{}")
            
            self.campos_entrada["inventario"] = text_inventario
            if dados and self.item_selecionado:
                # Usa um after para garantir que a interface esteja pronta
                self.after(100, self.atualizar_visualizacao_inventario)
            
            # Aviso sobre edição de inventário
            tk.Label(self.frame_campos, 
                    text="Use os botões acima para adicionar/remover itens do inventário.",
                    fg="yellow", bg="#2a1f4a", font=("Arial", 10), wraplength=400, justify="left").grid(
                    row=4, column=0, columnspan=2, padx=5, pady=5)
            
            # Atualizar scroll region
            self.frame_campos.update_idletasks()
            self.canvas_campos.configure(scrollregion=self.canvas_campos.bbox("all"))
            return
        
        if not self.tabela_atual:
            return
        
        config = self.configuracoes_tabelas[self.tabela_atual]
        campos = config["campos"]
        
        row = 0
        for campo in campos:
            # Label
            tk.Label(self.frame_campos, text=f"{campo.title()}:", 
                    fg="white", bg="#2a1f4a", font=("Arial", 12)).grid(row=row, column=0, sticky="w", padx=5, pady=5)
            
            # Campo de entrada
            if campo in ["descricao", "efeito"]:  # Campos de texto longo
                text_widget = scrolledtext.ScrolledText(self.frame_campos, height=3, width=50, 
                                                       bg="#130f26", fg="white", font=("Arial", 10))
                text_widget.grid(row=row, column=1, padx=5, pady=5)
                if dados and campo in dados:
                    text_widget.insert("1.0", str(dados[campo]))
                self.campos_entrada[campo] = text_widget
            else:  # Campos de texto simples
                entry = tk.Entry(self.frame_campos, bg="#130f26", fg="white", 
                               font=("Arial", 12), width=50)
                entry.grid(row=row, column=1, padx=5, pady=5)
                if dados and campo in dados:
                    entry.insert(0, str(dados[campo]))
                self.campos_entrada[campo] = entry
            
            row += 1
        
        # Atualizar scroll region
        self.frame_campos.update_idletasks()
        self.canvas_campos.configure(scrollregion=self.canvas_campos.bbox("all"))

    def novo_item(self):
        """Cria um novo item"""
        if not self.tabela_atual:
            messagebox.showwarning("Aviso", "Selecione uma tabela primeiro!")
            return
        
        config = self.configuracoes_tabelas[self.tabela_atual]
        if not config["campos"]:
            messagebox.showwarning("Aviso", f"Tabela '{self.tabela_atual}' ainda não implementada!")
            return
        
        self.item_selecionado = None
        self.criar_campos_edicao()

    def editar_item(self):
        """Edita o item selecionado"""
        if not self.item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para editar!")
            return
        
        self.carregar_item_para_edicao()

    def remover_item(self):
        """Remove o item selecionado"""
        if not self.item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para remover!")
            return
        
        # Confirmar remoção
        resposta = messagebox.askyesno("Confirmar", 
                                     f"Tem certeza que deseja remover o item '{self.item_selecionado}'?")
        if not resposta:
            return
        
        if self.tabela_atual == "Kits":
            if D.deletar_kit_do_banco(self.item_selecionado):
                messagebox.showinfo("Sucesso", f"Kit '{self.item_selecionado}' removido com sucesso!")
                
                # Remove dos dados locais
                if self.item_selecionado in self.dados_atuais:
                    del self.dados_atuais[self.item_selecionado]
                
                # Atualiza a interface
                self.atualizar_treeview()
                self.limpar_campos_edicao()
            else:
                messagebox.showerror("Erro", "Erro ao remover kit do banco de dados!")
            return
        
        try:
            config = self.configuracoes_tabelas[self.tabela_atual]
            
            # Remove do banco de dados
            D.deletar_item_do_banco(config["tabela_db"], self.item_selecionado)
            
            # Remove dos dados locais
            if self.item_selecionado in self.dados_atuais:
                del self.dados_atuais[self.item_selecionado]
            
            # Atualiza a interface
            self.atualizar_treeview()
            self.limpar_campos_edicao()
            
            messagebox.showinfo("Sucesso", f"Item '{self.item_selecionado}' removido com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover item: {e}")
            print(f"Erro detalhado: {traceback.format_exc()}")
   
    def carregar_item_para_edicao(self):
        """Carrega os dados do item selecionado nos campos de edição"""
        if not self.item_selecionado or self.item_selecionado not in self.dados_atuais:
            return
        
        dados_item = self.dados_atuais[self.item_selecionado]
        
        # Para kits, usa os dados completos
        if self.tabela_atual == "Kits" and "_dados_completos" in dados_item:
            dados_para_edicao = dados_item["_dados_completos"]
            
            # Se for kit, força o carregamento correto do inventário
            kit_objeto = dados_item.get("_kit_objeto")
            if kit_objeto:
                # Tenta recarregar o kit do banco para garantir inventário atualizado
                try:
                    kit_atualizado = D.carregar_kit_completo_db(kit_objeto.nome)
                    if kit_atualizado and hasattr(kit_atualizado, 'inventario'):
                        dados_item["_kit_objeto"] = kit_atualizado
                        dados_para_edicao["inventario"] = self.inventario_para_dict(kit_atualizado.inventario)
                except Exception as e:
                    print(f"Erro ao recarregar kit: {e}")
        else:
            dados_para_edicao = dados_item
        
        self.criar_campos_edicao(dados_para_edicao)
        
        # Se for kit, força atualização da visualização do inventário
        if self.tabela_atual == "Kits":
            self.atualizar_visualizacao_inventario()

    def salvar_item(self):
        """Salva ou atualiza o item atual"""
        if not self.tabela_atual:
            messagebox.showwarning("Aviso", "Selecione uma tabela primeiro!")
            return
        
        config = self.configuracoes_tabelas[self.tabela_atual]
        if not config["campos"]:
            messagebox.showwarning("Aviso", f"Tabela '{self.tabela_atual}' ainda não implementada!")
            return
        
        if self.tabela_atual == "Kits":
            nome = self.campos_entrada["nome"].get().strip()
            raridade = self.campos_entrada["raridade"].get()
            
            if not nome:
                messagebox.showwarning("Aviso", "O campo 'nome' é obrigatório!")
                return
            
            if not raridade:
                messagebox.showwarning("Aviso", "O campo 'raridade' é obrigatório!")
                return
            
            try:
                # Se é edição, pega o kit existente e preserva o inventário
                if self.item_selecionado and self.item_selecionado in self.dados_atuais:
                    kit_existente = self.dados_atuais[self.item_selecionado].get("_kit_objeto")
                    if kit_existente:
                        # Atualiza apenas nome e raridade, preserva inventário
                        kit_existente.nome = nome
                        kit_existente.raridade = raridade
                        kit_para_salvar = kit_existente
                    else:
                        # Cria novo kit se não encontrou objeto existente
                        kit_para_salvar = CB.Kits(nome, raridade)
                else:
                    # Novo kit
                    kit_para_salvar = CB.Kits(nome, raridade)
                    # Garante que o novo kit tenha um inventário vazio
                    if not hasattr(kit_para_salvar, 'inventario') or kit_para_salvar.inventario is None:
                        # Assumindo que existe uma classe Inventario
                        kit_para_salvar.inventario = CB.Inventario()  # ou a classe correta do inventário
                
                # Usar a função específica para kits que agora salva o inventário também
                if D.salvar_kit_no_banco(kit_para_salvar):
                    if self.item_selecionado and self.item_selecionado in self.dados_atuais:
                        messagebox.showinfo("Sucesso", f"Kit '{nome}' atualizado com sucesso!")
                    else:
                        messagebox.showinfo("Sucesso", f"Kit '{nome}' salvo com sucesso!")
                    
                    # Recarrega os dados para atualizar a interface
                    self.carregar_dados_tabela()
                    self.limpar_campos_edicao()
                    
                    # Atualiza os kits em memória
                    D.refresh_kits()  # Função que recarrega os kits do banco
                    
                else:
                    messagebox.showerror("Erro", "Erro ao salvar kit no banco de dados!")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar kit no banco de dados: {e}")
                print(f"Erro detalhado: {traceback.format_exc()}")
            
            return
        
        try:
            # Coletar dados dos campos
            dados_item = {}
            for campo, widget in self.campos_entrada.items():
                if isinstance(widget, scrolledtext.ScrolledText):
                    valor = widget.get("1.0", "end-1c")
                else:
                    valor = widget.get()
                
                # Converter tipos apropriados
                if campo in ["peso", "dano", "perfuracao", "cura", "energia", "raio", "valor", 
                           "capacidade", "nivelBalistico", "absorcaoFisica", "absorcaoBalistica",
                           "forca", "agilidade", "vigor", "inteligencia", "tatica", "presenca"]:
                    try:
                        valor = float(valor) if valor else 0.0
                    except ValueError:
                        valor = 0.0
                elif campo in ["calibre"]:
                    # Calibre pode ser string
                    pass
                
                dados_item[campo] = valor
            
            # Validar campos obrigatórios
            if not dados_item.get("nome", "").strip():
                messagebox.showwarning("Aviso", "O campo 'nome' é obrigatório!")
                return
            
            nome_item = dados_item["nome"]
            
            # Verificar se é novo item ou edição
            if self.item_selecionado and self.item_selecionado in self.dados_atuais:
                # Atualizando item existente
                D.atualizar_item_no_banco(config["tabela_db"], self.item_selecionado, dados_item)
                
                # Se o nome mudou, precisa remover a entrada antiga
                if self.item_selecionado != nome_item:
                    if self.item_selecionado in self.dados_atuais:
                        del self.dados_atuais[self.item_selecionado]
                
                messagebox.showinfo("Sucesso", f"Item '{nome_item}' atualizado com sucesso!")
            else:
                # Novo item
                if nome_item in self.dados_atuais:
                    resposta = messagebox.askyesno("Item Existente", 
                                                 f"Item '{nome_item}' já existe. Deseja substituir?")
                    if not resposta:
                        return
                
                D.salvar_item_no_banco(config["tabela_db"], dados_item)
                messagebox.showinfo("Sucesso", f"Item '{nome_item}' salvo com sucesso!")
            
            # Atualizar dados locais
            self.dados_atuais[nome_item] = dados_item
            
            # Atualizar interface
            self.atualizar_treeview()
            self.limpar_campos_edicao()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar item: {e}")
            print(f"Erro detalhado: {traceback.format_exc()}")

    def cancelar_edicao(self):
        """Cancela a edição atual"""
        self.limpar_campos_edicao()

    def limpar_campos_edicao(self):
        """Limpa os campos de edição"""
        self.item_selecionado = None
        for widget in self.frame_campos.winfo_children():
            widget.destroy()
        self.campos_entrada.clear()

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

