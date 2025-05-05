import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import Dados as D
import Codigos as CB
import re
import random

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
        
        tk.Button(self, text="Tela de seleção", height=2, command=self.TelaDeSelecao,
                bg="#1a0869", fg="white", font=("Arial", 20)).place(x=385, y=10, width=350, height=75)
        
        tk.Button(self, text="Combate", height=2, command=self.TelaDeCombate,
                bg="#1a0869", fg="white", font=("Arial", 20)).place(x=870, y=10, width=350, height=75)

        tk.Button(self, text="Informações", height=2, command=self.TelaDeRegrasEItens,
                bg="#1a0869", fg="white", font=("Arial", 20)).place(x=1235, y=10, width=350, height=75)
        

        # Frame para o texto sobre o aplicativo, com fundo preto
        sobre_frame = tk.Frame(self, bg="black")
        sobre_frame.place(x=550, y=250, width=500, height=300)

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
        self.characters = D.GruposDePersonagens["Players"] + D.GruposDePersonagens["NPCs"]
        self.config(bg='#130f26')

        # --- Botões de Navegação ---
        tk.Button(self, text="Tela inicial", height=2, command=self.Voltar,
                bg="#1a0869", fg="white", font=("Arial", 20)).place(x=20, y=10, width=350, height=75)

        tk.Label(self, text="Seleção de Personagem", fg="white", bg="#1a0869",
                font=("Arial", 20, "bold"), width=20, height=2).place(x=385, y=10, width=350, height=75)

        tk.Button(self, text="Combate", height=2, command=self.TelaDeCombate,
                bg="#1a0869", fg="white", font=("Arial", 20)).place(x=870, y=10, width=350, height=75)

        tk.Button(self, text="Informações", height=2, command=self.TelaDeRegrasEItens,
                bg="#1a0869", fg="white", font=("Arial", 20)).place(x=1235, y=10, width=350, height=75)

        # --- Lista de Personagens ---
        self.char_list_frame = self.create_list_section(self, self.characters)
        self.char_list_frame.place(x=20, y=120, width=350, height=600)

        # --- Botões de Criação ---
        self.create_controls(self).place(x=420, y=120)

        self.group_var.trace("w", self.refresh)

    def create_list_section(self, parent, data_list):
        frame = tk.Frame(parent, bg='#1a0869')

        # --- Combobox de Seleção de Grupo ---
        self.group_var = tk.StringVar(value="Players")
        self.group_var.trace("w", self.refresh)
        group_menu = ttk.Combobox(frame, textvariable=self.group_var, state="readonly", values=["Players", "NPCs"], font=("Arial", 12))
        group_menu.place(x=10, y=10, width=320, height=30)

        # --- Título da seção de personagens ---
        label = tk.Label(frame, text="Personagens", fg="white", bg="#1a0869", font=("Arial", 18, "bold"))
        label.place(x=10, y=50)

        # --- Frame e Canvas para Scroll da Lista de Personagens ---
        canvas_frame = tk.Frame(frame, bg='#1a0869')
        canvas_frame.place(x=10, y=90, width=320, height=350)

        canvas = tk.Canvas(canvas_frame, bg="#1a0869", highlightthickness=0, width=300, height=350)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview, width=20)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Colocando a barra de rolagem ao lado direito do canvas
        scrollbar.place(x=300, y=0, height=350)

        canvas.place(x=0, y=0, width=300, height=350)

        inner_frame = tk.Frame(canvas, bg="#1a0869")
        canvas.create_window((0, 0), window=inner_frame, anchor='nw')
        inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # --- Criação dos Botões de Personagens ---
        y_offset = 0  # Controle de deslocamento vertical para os botões
        for char in data_list:
            if isinstance(char, CB.Personagem):
                char_frame = tk.Frame(inner_frame, bg="#1a0869")
                char_frame.place(x=0, y=y_offset, width=300, height=60)

                # Botão principal do personagem
                char_button = tk.Button(char_frame, text=f"{char.nome} - Nível {char.nivel} - XP:{char.XPAtual}/{char.XPlvlUp} - HP:{char.vidaAtual}/{char.vidaMax}", bg="#1a0869", fg="white", font=("Arial", 12),
                                        anchor="w", justify="left", height=2, wraplength=250, width=34, command=lambda c=char: self.controller.abrir_detalhes(c))
                char_button.place(x=0, y=0, width=250, height=50)

                # Botão de remover
                remove_button = tk.Button(char_frame, text="X", bg="red", fg="white", font=("Arial", 12, "bold"), width=3, command=lambda c=char: self.remove_specific_character(c))
                remove_button.place(x=230, y=0, width=30, height=50)

                y_offset += 60
        return frame

    def create_controls(self, parent):
        frame = tk.Frame(parent, bg="#1a0869")

        add_button = tk.Button(frame, text="Adicionar", command=lambda: self.add_character("Personagens"), width=20, height=1, bg="#1a0869", fg="white", font=("Arial", 15))
        add_button.pack(pady=5)

        random_button = tk.Button(frame, text="Gerar NPC", command=lambda: self.gerar_NPC("Personagens"), width=20, height=1, bg="#1a0869", fg="white", font=("Arial", 15))
        random_button.pack(pady=5)

        group_button = tk.Button(frame, text="Gerar Grupo de NPC", command=lambda: self.gerar_grupo_NPCs("Personagens"), width=20, height=1, bg="#1a0869", fg="white", font=("Arial", 15))
        group_button.pack(pady=5)

        return frame
    
    def refresh(self, *args):
        for widget in self.char_list_frame.winfo_children():
            widget.destroy()

        selected_group = self.group_var.get()

        if selected_group in D.GruposDePersonagens:
            self.char_list_frame = self.create_list_section(self, D.GruposDePersonagens[selected_group])

        self.char_list_frame.place(x=20, y=120, width=350, height=600)

    def remove_specific_character(self, character):
        selected_group = self.group_var.get()
        print(f"Removendo personagem: {character.nome} do grupo {selected_group}")
        
        if selected_group in D.GruposDePersonagens:
            try:
                D.GruposDePersonagens[selected_group].remove(character)
            except ValueError:
                print("Personagem não encontrado no grupo.")
        
        self.refresh()
    
    def add_character(self, title):
        popup = tk.Toplevel(self)
        popup.title("Criar Novo Personagem")
        popup.geometry("400x550")
        popup.config(bg="#130f26")

        # Usar self.group_var ao invés de criar uma nova variável local
        tk.Label(popup, text="Inserir em:", bg="#130f26", fg="white", font=("Arial", 12)).pack(pady=(10, 0))

        # Modificando o Combobox para usar self.group_var e valores corretos
        lista_menu = ttk.Combobox(popup, textvariable=self.group_var, state="readonly", 
                                values=list(D.GruposDePersonagens.keys()), font=("Arial", 11))
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
                novo_personagem = CB.Personagem( nome, nivel, Forca, Agilidade, Vigor, Inteligencia, Presenca, Tatica, proficiencias_base=D.Proficiencias)

                destino = self.group_var.get()
                if destino in D.GruposDePersonagens:
                    D.GruposDePersonagens[destino].append(novo_personagem)

                popup.destroy()
                self.refresh()
            except ValueError:
                tk.messagebox.showerror("Erro", "Preencha todos os campos corretamente!")

        tk.Button(popup, text="Confirmar", command=confirmar, bg="#1a0869", fg="white", font=("Arial", 14), width=20).pack(pady=20)
    
    def gerar_NPC(self, title):
        import random
        popup = tk.Toplevel(self)
        popup.title("Gerar NPC")
        popup.geometry("400x550")
        popup.config(bg="#130f26")

        entradas = {}

        # --- Grupo de Destino (GruposDePersonagens) ---
        tk.Label(popup, text="Inserir em:", bg="#130f26", fg="white", font=("Arial", 12)).pack(pady=(10, 0))
        grupo_destino_var = tk.StringVar(value=list(D.GruposDePersonagens.keys())[0])
        grupo_destino_menu = ttk.Combobox(popup, textvariable=grupo_destino_var, state="readonly",
                                        values=list(D.GruposDePersonagens.keys()), font=("Arial", 11))
        grupo_destino_menu.pack(pady=(0, 10))
        entradas["GrupoDestino"] = grupo_destino_var

        # --- Grupo NPC (Facção) ---
        tk.Label(popup, text="Grupo (Facção)", bg="#130f26", fg="white", font=("Arial", 12)).pack(pady=(10, 0))
        grupo_var = tk.StringVar(value=list(D.NPCs_predefinidos.keys())[0])
        grupo_menu = tk.OptionMenu(popup, grupo_var, *D.NPCs_predefinidos.keys())
        grupo_menu.config(bg="#1a0869", fg="white", font=("Arial", 12), width=30)
        grupo_menu.pack(pady=5)
        entradas["Grupo"] = grupo_var

        # --- Classe NPC ---
        tk.Label(popup, text="Classe do NPC", bg="#130f26", fg="white", font=("Arial", 12)).pack(pady=(10, 0))
        classe_var = tk.StringVar()
        classe_menu = tk.OptionMenu(popup, classe_var, "")
        classe_menu.config(bg="#1a0869", fg="white", font=("Arial", 12), width=30)
        classe_menu.pack(pady=5)
        entradas["Classe"] = classe_var

        def atualizar_classes(*_):
            grupo_escolhido = grupo_var.get()
            classes = [c[0] for c in D.NPCs_predefinidos.get(grupo_escolhido, [])]
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

        # --- Kits ---
        tk.Label(popup, text="Kit", bg="#130f26", fg="white", font=("Arial", 12)).pack(pady=(10, 0))
        kit_var = tk.StringVar(value=list(D.kits_por_nome.keys())[0])
        kit_menu = tk.OptionMenu(popup, kit_var, *D.kits_por_nome.keys())
        kit_menu.config(bg="#1a0869", fg="white", font=("Arial", 12), width=30)
        kit_menu.pack(pady=5)
        entradas["Kit"] = kit_var

        # --- Nível ---
        tk.Label(popup, text="Nível do NPC", bg="#130f26", fg="white", font=("Arial", 12)).pack(pady=(10, 0))
        nivel_entry = tk.Entry(popup, font=("Arial", 12), width=5, justify="center")
        nivel_entry.insert(0, str(random.randint(1, 5)))
        nivel_entry.pack(pady=5)
        entradas["Nivel"] = nivel_entry

        # --- Nome ---
        tk.Label(popup, text="Nome do NPC", bg="#130f26", fg="white", font=("Arial", 12)).pack(pady=(10, 0))
        nome_entry = tk.Entry(popup, font=("Arial", 12), width=25, justify="center")
        nome_entry.pack(pady=5)
        entradas["Nome"] = nome_entry

        # --- Confirmar ---
        def confirmar():
            try:
                grupo = entradas["Grupo"].get()
                classe = entradas["Classe"].get()
                kit_key = entradas["Kit"].get()
                nivel = int(entradas["Nivel"].get())
                destino = entradas["GrupoDestino"].get()

                # Pega a tupla do NPC
                tupla_npc = next((t for t in D.NPCs_predefinidos[grupo] if t[0] == classe), None)
                if not tupla_npc:
                    raise ValueError("Classe selecionada não encontrada no grupo escolhido.")

                # Nome
                nome = entradas["Nome"].get() or f"{classe}_{random.randint(1, 50)}"

                # Cria o NPC base
                classe, Forca, Agilidade, Vigor, Inteligencia, Presenca, Tatica = tupla_npc
                npc = CB.NPC(grupo, classe, int(Forca), int(Agilidade), int(Vigor),
                            int(Inteligencia), int(Presenca), int(Tatica))

                # Recupera kit e chama Gerador
                kit = D.kits_por_nome[kit_key]
                personagem = CB.Gerador(npc=npc, kit=kit, nivel=nivel, nome=nome, proficiencias_base=D.Proficiencias)

                # Pós-processamento
                self.carregar_armas_e_armaduras(personagem)

                if destino in D.GruposDePersonagens:
                    D.GruposDePersonagens[destino].append(personagem)

                self.refresh()
                popup.destroy()

            except Exception as e:
                tk.messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o personagem:\n{e}")

        botao_confirmar = tk.Button(popup, text="Confirmar", command=confirmar, bg="#0b8f33", fg="white", font=("Arial", 12, "bold"))
        botao_confirmar.pack(pady=20)

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

        popup = tk.Toplevel()
        popup.title("Gerar Grupo de NPCs")
        popup.configure(bg="#130f26")
        popup.geometry("550x600")

        entradas = {}

        # Cabeçalho com opções iniciais
        header_frame = tk.Frame(popup, bg="#130f26")
        header_frame.pack(pady=10)

        # Grupo de destino
        tk.Label(header_frame, text="Inserir em:", bg="#130f26", fg="white").grid(row=0, column=0, padx=5, sticky="e")
        destino_var = tk.StringVar(value=list(D.GruposDePersonagens.keys())[0])
        destino_menu = ttk.Combobox(header_frame, textvariable=destino_var, state="readonly", values=list(D.GruposDePersonagens.keys()), width=20)
        destino_menu.grid(row=0, column=1, padx=5)
        entradas["Destino"] = destino_var

        # Facção (grupo de NPCs)
        tk.Label(header_frame, text="Facção:", bg="#130f26", fg="white").grid(row=0, column=2, padx=5, sticky="e")
        faccao_var = tk.StringVar(value=list(D.NPCs_predefinidos.keys())[0])
        faccao_menu = ttk.Combobox(header_frame, textvariable=faccao_var, state="readonly", values=list(D.NPCs_predefinidos.keys()), width=20)
        faccao_menu.grid(row=0, column=3, padx=5)
        entradas["Facção"] = faccao_var

        # Quantidade
        tk.Label(header_frame, text="Quantidade:", bg="#130f26", fg="white").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        qtd_var = tk.StringVar(value="3")
        qtd_entry = tk.Entry(header_frame, textvariable=qtd_var, width=5, justify="center")
        qtd_entry.grid(row=1, column=1, padx=5, pady=5)

        # Área scrollável para os NPCs
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

        def gerar_slots():
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
            slots.clear()

            try:
                qtd = int(qtd_var.get())
            except:
                tk.messagebox.showerror("Erro", "Valores inválidos.")
                return

            faccao = faccao_var.get()
            classes_disponiveis = [c[0] for c in D.NPCs_predefinidos.get(faccao, [])]

            for i in range(qtd):
                slot = {}
                frame = tk.Frame(scrollable_frame, bg="#1f1b3a", bd=1, relief="solid", padx=5, pady=5)
                frame.pack(padx=5, pady=5, fill="x")

                # Título
                tk.Label(frame, text=f"NPC {i+1}", bg="#1f1b3a", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=6, pady=(0, 5), sticky="w")

                # Classe
                tk.Label(frame, text="Classe", bg="#1f1b3a", fg="white").grid(row=1, column=0, padx=2, sticky="e")
                classe_var = tk.StringVar(value=classes_disponiveis[0] if classes_disponiveis else "")
                classe_menu = ttk.Combobox(frame, textvariable=classe_var, state="readonly", values=classes_disponiveis, width=25)
                classe_menu.grid(row=1, column=1, padx=2)

                # Kit
                tk.Label(frame, text="Kit", bg="#1f1b3a", fg="white").grid(row=1, column=2, padx=2, sticky="e")
                kit_var = tk.StringVar(value=list(D.kits_por_nome.keys())[0])
                kit_menu = ttk.Combobox(frame, textvariable=kit_var, state="readonly", values=list(D.kits_por_nome.keys()), width=25)
                kit_menu.grid(row=1, column=3, padx=2)

                # Nível individual (inicializa com o padrão)
                tk.Label(frame, text="Nível", bg="#1f1b3a", fg="white").grid(row=1, column=4, padx=2, sticky="e")
                nivel_var = tk.StringVar(value="1")
                nivel_entry = tk.Entry(frame, textvariable=nivel_var, width=5, justify="center")
                nivel_entry.grid(row=1, column=5, padx=2)

                # Adiciona ao slot
                slot.update({
                    "Classe": classe_var,
                    "Kit": kit_var,
                    "Nivel": nivel_var
                })

                slots.append(slot)

        # Botão para gerar os slots com base nos valores acima
        tk.Button(popup, text="Gerar Slots", command=gerar_slots, font=("Arial", 11), bg="#0b4f8f", fg="white").pack(pady=(10, 10))
        tk.Button(popup, text="Confirmar Geração", command=lambda: self.confirmar_geracao(slots, entradas), font=("Arial", 11), bg="#1a7837", fg="white").pack(pady=(0, 10))

    def confirmar_geracao(self, slots, entradas):
        import random
        try:
            faccao = entradas["Facção"].get()
            destino = entradas["Destino"].get()

            for i, slot in enumerate(slots):
                classe_nome = slot["Classe"].get()
                kit_nome = slot["Kit"].get()
                nivel = int(slot["Nivel"].get())

                # Buscar a tupla da classe
                tupla_npc = next((t for t in D.NPCs_predefinidos[faccao] if t[0] == classe_nome), None)
                if not tupla_npc:
                    raise ValueError(f"Classe '{classe_nome}' não encontrada na facção '{faccao}'.")

                classe, Forca, Agilidade, Vigor, Inteligencia, Presenca, Tatica = tupla_npc
                npc_base = CB.NPC(faccao, classe, int(Forca), int(Agilidade), int(Vigor),
                                int(Inteligencia), int(Presenca), int(Tatica))

                # Criar personagem
                kit = D.kits_por_nome[kit_nome]
                nome = f"{classe}_{random.randint(1, 99)}"
                personagem = CB.Gerador(npc=npc_base, kit=kit, nivel=nivel, nome=nome, proficiencias_base=D.Proficiencias)

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
        self.frame_vida.place(x=50, y=100, width=200, height=120)
        self.label_vida = tk.Label(self.frame_vida, bg='#1a0869', fg="white", font=("Arial", 16))
        self.label_vida.pack(pady=2)
        self.label_energia = tk.Label(self.frame_vida, bg='#1a0869', fg="white", font=("Arial", 16))
        self.label_energia.pack(pady=2)
        self.label_mobilidade = tk.Label(self.frame_vida, bg='#1a0869', fg="white", font=("Arial", 16))
        self.label_mobilidade.pack(pady=2)
        ## Frame da Vida ##

        ## Frame do XP ##
        self.frame_XP = tk.Frame(self, bg='#1a0869', bd=2, relief='ridge')
        self.frame_XP.place(x=50, y=220, width=200, height=120)
        self.label_xp = tk.Label(self.frame_XP, bg='#1a0869', fg="white", font=("Arial", 16))
        self.label_xp.pack(pady=2)
        self.label_nivel = tk.Label(self.frame_XP, bg='#1a0869', fg="white", font=("Arial", 16))
        self.label_nivel.pack(pady=2)
        self.label_carga = tk.Label(self.frame_XP, bg='#1a0869', fg="white", font=("Arial", 16))
        self.label_carga.pack(pady=2)
        ## Frame do XP ##

        ## Frame dos Atributos ##
        self.frame_atributos = tk.Frame(self, bg='#1a0869', bd=2, relief='ridge')
        self.frame_atributos.place(x=250, y=100, width=250, height=240)
        self.label_atributos_title = tk.Label(self.frame_atributos, text="Atributos", bg='#1a0869', fg="white", font=("Arial", 18, "bold"))
        self.label_atributos_title.pack(pady=(0, 5))
        self.atributo_labels = []
        ## Frame dos Atributos ##

        ## Frame da AC ##
        self.frame_AC = tk.Frame(self, bg='#1a0869', bd=2, relief='ridge')
        self.frame_AC.place(x=50, y=340, width=200, height=80)

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
        self.btn_status_completo = tk.Button(self, text="Change Stats", command=self.abrir_popup_status_completo, bg="#1a0869", fg="white", font=("Arial", 14))
        self.btn_status_completo.place(x=250, y=340, width=250, height=40)

        self.btn_rolagem = tk.Button(self, text="Dice Roll", command=lambda: self.abrir_popup_rolagem_avancada(), bg="#1a0869", fg="white", font=("Arial", 14))
        self.btn_rolagem.place(x=250, y=380, width=250, height=40)

        self.btn_rolagem = tk.Button(self, text="Looting/Sharing", command=lambda: self.abrir_popup_transferencia(), bg="#1a0869", fg="white", font=("Arial", 14))
        self.btn_rolagem.place(x=250, y=420, width=250, height=40)

        self.btn_rolagem = tk.Button(self, text="Item upgrades", command=lambda: self.abrir_popup_melhorias(), bg="#1a0869", fg="white", font=("Arial", 14))
        self.btn_rolagem.place(x=250, y=460, width=250, height=40)
        ## Botões entre Atributos e Proteções ##
        ## Botões entre Atributos e Proteções ##
    
    def refresh(self, character=None):
        if character is not None:
            self.character = character
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


            for lbl in self.atributo_labels:
                lbl.destroy()
            self.atributo_labels.clear()

            atributos = {
                "Força": self.character.Forca,
                "Agilidade": self.character.Agilidade,
                "Vigor": self.character.Vigor,
                "Inteligência": self.character.Inteligencia,
                "Presença": self.character.Presenca,
                "Tática": self.character.Tatica
            }
            for atributo, valor in atributos.items():
                lbl = tk.Label(self.frame_atributos, text=f"{atributo}: {valor}", bg='#1a0869', fg="white", font=("Arial", 14))
                lbl.pack()
                self.atributo_labels.append(lbl)

        except Exception as e:
            print("Erro no refresh da tela de detalhes:", e)

        ## Atualização das proficiências ##
        ## Atualização das proficiências ##
        for widget in self.proficiencia_widgets:
            widget.destroy()
        self.proficiencia_widgets.clear()

        for nome, prof in self.character.proficiencias.items():
            frame = tk.Frame(self.scrollable_frame_prof, bg="#1a0869", pady=2)
            frame.pack(fill='x', padx=2, pady=2)

            label = tk.Label(frame, text=f"{prof.nome}: {prof.nivel}", bg="#2a0d89", fg="white", font=("Arial", 13), width=27, height=1, anchor='w')
            label.pack(side="left", padx=2)

            btn_menos = tk.Button(frame, text="-", font=("Arial", 8), bg="#2a0d89", fg="white", width= 4, height= 1, command=lambda p=prof: self.decrementar_proficiencia(p))
            btn_menos.pack(side="left", padx=5)

            btn_mais = tk.Button(frame, text="+", font=("Arial", 8), bg="#2a0d89", fg="white",width= 4, height= 1, command=lambda p=prof: self.incrementar_proficiencia(p))
            btn_mais.pack(side="left", padx=5)

            self.proficiencia_widgets.append(frame)
        ## Atualização das proficiências ##
        ## Atualização das proficiências ##

        ## Atualização do inventário ##
        ## Atualização do inventário ##
        for widget in self.scrollable_frame_inventario.winfo_children():
            widget.destroy()

        try:
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
                    font=("Arial", 14), anchor='w', relief=tk.FLAT,borderwidth=0, highlightthickness=0, width=35,
                    command=lambda i=item_obj: self.mostrar_popup_detalhes_item(i))
                btn_item.pack(side="left", fill='x', expand=True)

                if item_id:
                    if isinstance(item_obj, (CB.Melee)):
                        btn_equipar = tk.Button(frame_item, text="Equip", command=lambda i=item_obj: self._equipar_item(i), bg="#2a0d89", fg="white", font=("Arial", 8), width=6)
                        btn_equipar.pack(side="right", padx=5)
                        btn_remover = tk.Button(frame_item,text="Discard",command=lambda i=item_obj: self._remover_item_do_inventario(i),bg="#2a0d89",fg="white",font=("Arial", 8))     
                        btn_remover.pack(side="right", padx=5)
                        self.item_widgets.append(btn_equipar)
                    elif isinstance(item_obj, (CB.Ranged)):
                        btn_equipar = tk.Button(frame_item, text="Equip", command=lambda i=item_obj: self._equipar_item(i), bg="#2a0d89", fg="white", font=("Arial", 8), width=6)
                        btn_equipar.pack(side="right", padx=5)
                        btn_equipar = tk.Button(frame_item, text="Unload", command=lambda i=item_obj: self.descarregar_municao_ranged(i), bg="#2a0d89", fg="white", font=("Arial", 8), width=6)
                        btn_equipar.pack(side="right", padx=5)
                        btn_remover = tk.Button(frame_item,text="Discard",command=lambda i=item_obj: self._remover_item_do_inventario(i),bg="#2a0d89",fg="white",font=("Arial", 8))     
                        btn_remover.pack(side="right", padx=5)
                        self.item_widgets.append(btn_equipar)
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
        ## Atualização do inventário ##
        ## Atualização do inventário ##

        ## Atualização do equipados ##
        ## Atualização do equipados ##
        for widget in self.scrollable_frame_equipados.winfo_children():
            widget.destroy()

        try:
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
        ## Atualização do equipados ##
        ## Atualização do equipados ##

        ## Atualização das proteções ##
        ## Atualização das proteções ##
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
        ## Atualização das proteções ##
        ## Atualização das proteções ##

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
            "Munições": D.Munições,
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

            # Frame para botões de ação (embaixo, lado a lado)
            frame_acoes = tk.Frame(popup, bg="#1a0869", height=60)
            frame_acoes.pack(pady=(10, 0), fill='x')

            def criar_botao(texto, comando=None, largura=140):
                btn = tk.Button(frame_acoes, text=texto, command=comando, bg="#004080", fg="white", font=("Arial", 10), width=int(largura / 10))
                btn.pack(side="left", padx=(10, 0), pady=10)

            if tipo == "Protecao":
                # Botão Equipar ao lado do "Fechar"
                btn_equipar = tk.Button(
                    frame_acoes,
                    text="Equipar", 
                    command=lambda p=popup: self.abrir_popup_equipar_protecao(item_obj, p),
                    bg="#004080", fg="white", font=("Arial", 10), width=10
                )
                btn_equipar.pack(side="left", padx=(10, 10))

            # Botão Fechar
            btn_fechar = tk.Button(popup, text="Fechar", command=popup.destroy, bg="#004080", fg="white", font=("Arial", 12))
            btn_fechar.pack(side="right", padx=(0, 30), pady=20)

        except Exception as e:
            print("Erro ao mostrar detalhes do item:", e)

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
    
    def abrir_popup_status_completo(self):
        popup = tk.Toplevel(self)
        popup.title("Status do Personagem")
        popup.configure(bg="#1e1b3a")
        popup.geometry("540x200")

        personagem = self.character  # Referência ao personagem

        # Função auxiliar
        def tratar_valor(entrada):
            try:
                return int(entrada.get())
            except ValueError:
                return None

        # --- Seção Vida/Energia ---
        frame_vida_energia = tk.Frame(popup, bg="#1e1b3a")
        frame_vida_energia.grid(row=0, column=0, padx=15, pady=10)

        tk.Label(frame_vida_energia, text=f"Vida: {personagem.vidaAtual}/{personagem.vidaMax}",
                bg="#1e1b3a", fg="white", font=("Arial", 12)).grid(row=0, column=0, columnspan=2)
        entrada_vida = tk.Entry(frame_vida_energia, justify="center")
        entrada_vida.grid(row=1, column=0, columnspan=2, pady=5)

        tk.Button(frame_vida_energia, text="Curar", command=lambda: (personagem.TomarCura(tratar_valor(entrada_vida) or 0), self.refresh(character=personagem), popup.destroy(), self.abrir_popup_status_completo()), bg="#115c11", fg="white").grid(row=2, column=0, pady=2)
        tk.Button(frame_vida_energia, text="Dano", command=lambda: (personagem.TomarDano(tratar_valor(entrada_vida) or 0), self.refresh(character=personagem), popup.destroy(), self.abrir_popup_status_completo()), bg="#8c1d1d", fg="white").grid(row=2, column=1, pady=2)

        tk.Label(frame_vida_energia, text=f"Energia: {personagem.PeAtual}/{personagem.PeMax}",
                bg="#1e1b3a", fg="white", font=("Arial", 12)).grid(row=3, column=0, columnspan=2)
        entrada_energia = tk.Entry(frame_vida_energia, justify="center")
        entrada_energia.grid(row=4, column=0, columnspan=2, pady=5)

        tk.Button(frame_vida_energia, text="Recuperar", command=lambda: (setattr(personagem, 'PeAtual', min(personagem.PeAtual + (tratar_valor(entrada_energia) or 0), personagem.PeMax)), self.refresh(character=personagem), popup.destroy(), self.abrir_popup_status_completo()), bg="#115c11", fg="white").grid(row=5, column=0, pady=2)
        tk.Button(frame_vida_energia, text="Gastar", command=lambda: (setattr(personagem, 'PeAtual', max(personagem.PeAtual - (tratar_valor(entrada_energia) or 0), 0)), self.refresh(character=personagem), popup.destroy(), self.abrir_popup_status_completo()), bg="#8c1d1d", fg="white").grid(row=5, column=1, pady=2)

        # --- Seção XP/Nível ---
        frame_xp = tk.Frame(popup, bg="#1e1b3a")
        frame_xp.grid(row=0, column=1, padx=15, pady=10)

        tk.Label(frame_xp, text=f"XP: {personagem.XPAtual}/{personagem.XPlvlUp}",
                bg="#1e1b3a", fg="white", font=("Arial", 12)).grid(row=0, column=0, columnspan=2)
        entrada_xp = tk.Entry(frame_xp, justify="center")
        entrada_xp.grid(row=1, column=0, columnspan=2, pady=5)

        tk.Button(frame_xp, text="Ganhar XP", command=lambda: (personagem.GanharXP(tratar_valor(entrada_xp) or 0), self.refresh(character=personagem), popup.destroy(), self.abrir_popup_status_completo()), bg="#115c11", fg="white").grid(row=2, column=0, pady=2)
        tk.Button(frame_xp, text="Remover XP", command=lambda: (setattr(personagem, 'XPAtual', max(personagem.XPAtual - (tratar_valor(entrada_xp) or 0), 0)), self.refresh(character=personagem), popup.destroy(), self.abrir_popup_status_completo()), bg="#8c1d1d", fg="white").grid(row=2, column=1, pady=2)

        tk.Label(frame_xp, text=f"Nível: {personagem.nivel}",
                bg="#1e1b3a", fg="white", font=("Arial", 12)).grid(row=3, column=0, columnspan=2, pady=5)

        tk.Button(frame_xp, text="+", command=lambda: (setattr(personagem, 'nivel', personagem.nivel + 1), personagem.recalcularAtributos(), self.refresh(character=personagem), popup.destroy(), self.abrir_popup_status_completo()), bg="#115c11", fg="white", width=4).grid(row=4, column=0, padx=5)
        tk.Button(frame_xp, text="-", command=lambda: (setattr(personagem, 'nivel', max(personagem.nivel - 1, 1)), personagem.recalcularAtributos(), self.refresh(character=personagem), popup.destroy(), self.abrir_popup_status_completo()), bg="#8c1d1d", fg="white", width=4).grid(row=4, column=1, padx=5)

        # --- Seção Atributos ---
        frame_atributos = tk.Frame(popup, bg="#1e1b3a")
        frame_atributos.grid(row=0, column=2, padx=15, pady=10)

        atributos = {
            "Força": "Forca",
            "Agilidade": "Agilidade",
            "Vigor": "Vigor",
            "Presença": "Presenca",
            "Inteligência": "Inteligencia",
            "Tática": "Tatica"
        }

        for idx, (nome_visivel, nome_real) in enumerate(atributos.items()):
            tk.Label(frame_atributos, text=f"{nome_visivel}: {getattr(personagem, nome_real)}",
                    bg="#1e1b3a", fg="white", font=("Arial", 12)).grid(row=idx, column=0, sticky="w", pady=2)
            tk.Button(frame_atributos, text="+", command=lambda nv=nome_real: (setattr(personagem, nv, getattr(personagem, nv) + 1), personagem.recalcularAtributos(), self.refresh(character=personagem), popup.destroy(), self.abrir_popup_status_completo()), bg="#115c11", fg="white", width=3).grid(row=idx, column=1, padx=2)
            tk.Button(frame_atributos, text="-", command=lambda nv=nome_real: (setattr(personagem, nv, max(getattr(personagem, nv) - 1, 0)), personagem.recalcularAtributos(), self.refresh(character=personagem), popup.destroy(), self.abrir_popup_status_completo()), bg="#8c1d1d", fg="white", width=3).grid(row=idx, column=2, padx=2)
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
        self.players = D.GruposDePersonagens["Players"]
        self.npcs = D.GruposDePersonagens["NPCs"]

        tk.Button(self, text="Tela inicial", height=2, command=self.TelaInicial,
                bg="#1a0869", fg="white", font=("Arial", 20)).place(x=20, y=10, width=350, height=75)
        
        tk.Button(self, text="Tela de seleção", height=2, command=self.TelaDeSelecao,
                bg="#1a0869", fg="white", font=("Arial", 20)).place(x=385, y=10, width=350, height=75)

        tk.Label(self, text="Combate", fg="white", bg="#1a0869",
                font=("Arial", 20, "bold"), width=20, height=2).place(x=870, y=10, width=350, height=75)

        tk.Button(self, text="Informações", height=2, command=self.TelaDeRegrasEItens,
                bg="#1a0869", fg="white", font=("Arial", 20)).place(x=1235, y=10, width=350, height=75)

        # Frame de botões centrais
        action_buttons_frame = tk.Frame(self, bg='#130f26', width= 25, height= 4)
        action_buttons_frame.place(x=685, y=170)

        btn_cfg = {"width": 15, "height": 2, "font": ("Arial", 18, "bold"), "bg": "#7a3cff", "fg": "white"}
        tk.Button(action_buttons_frame, text="Ataque", command=self.abrir_popup_ataque, **btn_cfg).pack(pady=5)
        tk.Button(action_buttons_frame, text="Pilhar", command=self.abrir_popup_loot, **btn_cfg).pack(pady=5)

        # Painéis laterais (Players e NPCs)
        self.players_frame = self.create_list_section("Players", self.players, x=50, y=100)
        self.npcs_frame = self.create_list_section("NPCs", self.npcs, x=1050, y=100)

    def create_list_section(self, title, data_list, x, y, anchor="nw"):
        frame = tk.Frame(self, bg='#1a0869')
        frame.place(x=x, y=y, width=500, height=600, anchor=anchor)

        label = tk.Label(frame, text=title, fg="white", bg="#1a0869", font=("Arial", 18, "bold"))
        label.pack()

        canvas_frame = tk.Frame(frame, bg='#1a0869')
        canvas_frame.pack(fill="both", expand=True)
        canvas = tk.Canvas(canvas_frame, bg="#1a0869", highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        inner_frame = tk.Frame(canvas, bg="#1a0869")
        canvas.create_window((0, 0), window=inner_frame, anchor=anchor)

        inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        for char in data_list:
            char_frame = tk.Frame(inner_frame, bg="#1a0869")
            char_frame.pack(fill="x", pady=2)

            # Botão principal com informações do personagem
            char_button = tk.Button(
                char_frame,
                text=f"{char.nome} - Nível {char.nivel} - XP:{char.XPAtual}/{char.XPlvlUp} - HP:{char.vidaAtual}/{char.vidaMax}",
                bg="#1a0869", fg="white", font=("Arial", 11), anchor="w", justify="left",
                width=38, height=2,
                command=lambda c=char: self.controller.abrir_detalhes(c)
            )
            char_button.pack(side=tk.LEFT, fill="x", expand=True)

            # Campo de entrada para o valor de dano/cura
            valor_var = tk.IntVar(value=1)
            valor_entry = tk.Entry(char_frame, textvariable=valor_var, font=("Arial", 9), width=4, justify="center")
            valor_entry.pack(side=tk.RIGHT, padx=2)

            # Botão de Cura
            cura_btn = tk.Button(
                char_frame, text="Cura", fg="white", bg="#006400", font=("Arial", 10, "bold"),
                width=4, height=1, command=lambda c=char, v=valor_var: self.aplicar_cura(c, v)
            )
            cura_btn.pack(side=tk.RIGHT, padx=2)

            # Botão de Dano
            dano_btn = tk.Button(
                char_frame, text="Dano", fg="white", bg="#8b0000", font=("Arial", 10, "bold"),
                width=4, height=1, command=lambda c=char, v=valor_var: self.aplicar_dano(c, v)
            )
            dano_btn.pack(side=tk.RIGHT, padx=2)

        return frame

    def aplicar_dano(self, personagem, valor_var):
        valor = valor_var.get()
        if isinstance(valor, int) and valor > 0:
            personagem.TomarDano(valor)
            self.refresh()

    def aplicar_cura(self, personagem, valor_var):
        valor = valor_var.get()
        if isinstance(valor, int) and valor > 0:
            personagem.TomarCura(valor)
            self.refresh()

    def refresh(self):
        self.players_frame.destroy()
        self.npcs_frame.destroy()

        self.players_frame = self.create_list_section("Players", self.players, x=50, y=100)
        self.npcs_frame = self.create_list_section("NPCs", self.npcs, x=1050, y=100)

## função mais importante do sistema inteiro ##
    def abrir_popup_ataque(self):
        import random
        popup = tk.Toplevel(self)
        popup.title("Ataque")
        popup.geometry("700x550")
        popup.configure(bg="#1a1a2e")
        popup.resizable(False,False)

        y = 10

        # Atacante
        tk.Label(popup, text="Atacante:", bg="#1a1a2e", fg="white", font=("Arial", 12)).place(x=20, y=y)
        atacante_var = tk.StringVar()
        atacante_menu = ttk.Combobox(popup, textvariable=atacante_var, state="readonly",
            values=[f"Player: {p.nome}" for p in self.players] + ["────────────"] + [f"NPC: {n.nome}" for n in self.npcs])
        y += 25
        atacante_menu.place(x=20, y=y, width=200)

        # Alvo
        y += 35
        tk.Label(popup, text="Alvo:", bg="#1a1a2e", fg="white", font=("Arial", 12)).place(x=20, y=y)
        alvo_var = tk.StringVar()
        y += 25
        alvo_menu = ttk.Combobox(popup, textvariable=alvo_var, state="readonly",
            values=[f"Player: {p.nome}" for p in self.players] + ["────────────"] + [f"NPC: {n.nome}" for n in self.npcs])
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
            atacante_nome = atacante_var.get().replace("Player: ", "").replace("NPC: ", "")
            alvo_nome = alvo_var.get().replace("Player: ", "").replace("NPC: ", "")
            entrada_arma = arma_var.get()
            rolagem = rolagem_var.get()
            buff = buff_var.get()
            regiao = regiao_var.get()
            disparos = disparos_var.get()
            distancia = distancia_var.get()
            tipo = tipo_var.get()

            atacante = next((p for p in self.players + self.npcs if p.nome == atacante_nome), None)
            alvo = next((p for p in self.players + self.npcs if p.nome == alvo_nome), None)
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
            nome_atacante = atacante_var.get().replace("Player: ", "").replace("NPC: ", "")
            atacante = next((p for p in self.players + self.npcs if p.nome == nome_atacante), None)
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
            nome_atacante = atacante_var.get().replace("Player: ", "").replace("NPC: ", "")
            atacante = next((p for p in self.players + self.npcs if p.nome == nome_atacante), None)
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
            nome_atacante = atacante_var.get().replace("Player: ", "").replace("NPC: ", "")
            atacante = next((p for p in self.players + self.npcs if p.nome == nome_atacante), None)
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
## função mais importante do sistema inteiro ##

    def abrir_popup_loot(self):
        popup = tk.Toplevel(self)
        popup.title("Pilhagem")
        popup.geometry("1000x500")
        popup.configure(bg="#1a1a2e")
        popup.resizable(False, False)

        personagens = [f"Player: {p.nome}" for p in self.players] + [f"NPC: {n.nome}" for n in self.npcs]

        destino_var = tk.StringVar()
        origem_var = tk.StringVar()

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

            nome_o = origem_var.get().replace("Player: ", "").replace("NPC: ", "")
            nome_d = destino_var.get().replace("Player: ", "").replace("NPC: ", "")

            origem = next((p for p in self.players + self.npcs if p.nome == nome_o), None)
            destino = next((p for p in self.players + self.npcs if p.nome == nome_d), None)

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
    def __init__(self, parent, controller):  # controller = MainApp
        super().__init__(parent)
        self.controller = controller
        self.place(x=0, y=0, width=1600, height=900)
        self.config(bg='#130f26')

        style = ttk.Style()
        style.theme_use("default")
        style.configure("CustomCombobox.TCombobox", foreground="black", background="black", fieldbackground="black", bordercolor="black", arrowcolor="black", font=("Arial", 14), padding=6, borderwidth=2, relief="flat")

        # Título
        tk.Label(self, text="Regras e Itens", font=("Arial", 25, "bold"), bg="#3d0586", fg="white", width=20, height=1).place(x=600, y=10)

        self.topico_var = tk.StringVar()
        self.topico_var.trace_add("write", self.mostrar_topico)  # Atualiza o texto ao mudar

        ttk.Combobox(self, textvariable=self.topico_var, values=list(D.Topicos.keys()), state="readonly", width=53, style="CustomCombobox.TCombobox" ).place(x=625, y=110)
        # Frame externo que segura o canvas + scrollbar
        texto_frame = tk.Frame(self, bg="#130f26")
        texto_frame.place(x=450, y=150, width=700, height=650)
        # Canvas central
        self.texto_canvas = tk.Canvas(texto_frame, bg="black", highlightbackground="#4e00b3", highlightthickness=2)
        self.texto_canvas.pack(side="left", fill="both", expand=True)
        # Scrollbar vertical
        texto_scrollbar = tk.Scrollbar(texto_frame, orient="vertical", command=self.texto_canvas.yview)
        texto_scrollbar.pack(side="right", fill="y")
        self.texto_canvas.configure(yscrollcommand=texto_scrollbar.set)
        # Frame interno onde o texto será colocado
        self.texto_inner_frame = tk.Frame(self.texto_canvas, bg="black", )
        self.texto_canvas.create_window((0, 0), window=self.texto_inner_frame, anchor="nw")
        # Atualiza o scroll sempre que o conteúdo mudar
        self.texto_inner_frame.bind("<Configure>", lambda e: self.texto_canvas.configure(scrollregion=self.texto_canvas.bbox("all")))
        # Label de texto (inicial)
        self.texto_label = tk.Label(
            self.texto_inner_frame,
            text="Selecione um tópico acima para exibir o conteúdo.",
            fg="white", bg="black", font=("Arial", 14),
            justify="left", wraplength=665
        )
        self.texto_label.pack(padx=10, pady=10, anchor="nw")

        tk.Button(self, font=("Arial", 14, "bold"), text="Voltar ao início", bg="#3d0586", fg="white", command=self.Voltar, width=20, height= 1).place(x=400, y=850)
        tk.Button(self, font=("Arial", 14, "bold"), text="Tela de seleção", bg="#3d0586", fg="white", command=self.TelaDeSelecao, width=20, height= 1).place(x=680, y=850)
        tk.Button(self, font=("Arial", 14, "bold"), text="Tela de Combate", bg="#3d0586", fg="white", command=self.TelaDeCombate, width=20, height= 1).place(x=960, y=850)

        # Lado esquerdo — NPCs
        tk.Label(self, text="Tipos de NPCs", bg="#3d0586", fg="white",
                font=("Arial", 18, "bold"), width=20, height=1).place(x=50, y=10)

        self.npc_grupo_var = tk.StringVar()
        npc_combobox = ttk.Combobox(self, textvariable=self.npc_grupo_var,
            values=list(D.NPCs_predefinidos.keys()), state="readonly",
            width=46, style="CustomCombobox.TCombobox")
        npc_combobox.place(x=50, y=45)
        npc_combobox.bind("<<ComboboxSelected>>", self.carregar_npcs)

        npc_canvas_frame = tk.Frame(self, bg="#130f26")
        npc_canvas_frame.place(x=50, y=85, width=300, height=350)

        self.npc_canvas = tk.Canvas(npc_canvas_frame, bg="#14014a", highlightbackground="#4e00b3", highlightthickness=2)
        npc_scrollbar = tk.Scrollbar(npc_canvas_frame, orient="vertical", command=self.npc_canvas.yview)
        self.npc_canvas.configure(yscrollcommand=npc_scrollbar.set)

        npc_scrollbar.pack(side="right", fill="y")
        self.npc_canvas.pack(side="left", fill="both", expand=True)

        self.npc_inner_frame = tk.Frame(self.npc_canvas, bg="#14014a")
        self.npc_canvas.create_window((0, 0), window=self.npc_inner_frame, anchor="nw")
        self.npc_inner_frame.bind("<Configure>", lambda e: self.npc_canvas.configure(scrollregion=self.npc_canvas.bbox("all")))

        # Lado esquerdo — Proficiências
        tk.Label(self, text="Proficiências", bg="#3d0586", fg="white", font=("Arial", 18, "bold"), width=20, height=1).place(x=50, y=450)

        self.prof_filtro_var = tk.StringVar(value="Geral")
        prof_combobox = ttk.Combobox(self, textvariable=self.prof_filtro_var, values=["Geral", "Força", "Agilidade", "Vigor", "Inteligência", "Presença", "Tática"], state="readonly", width=46, style="CustomCombobox.TCombobox")
        prof_combobox.place(x=50, y=485)
        self.prof_filtro_var.trace_add("write", self.carregar_proficiencias)

        prof_canvas_frame = tk.Frame(self, bg="#130f26")
        prof_canvas_frame.place(x=50, y=525, width=300, height=350)
        self.prof_canvas = tk.Canvas(prof_canvas_frame, bg="#14014a", highlightbackground="#4e00b3", highlightthickness=2)
        scrollbar = tk.Scrollbar(prof_canvas_frame, orient="vertical", command=self.prof_canvas.yview)
        self.prof_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.prof_canvas.pack(side="left", fill="both", expand=True)
        self.prof_inner_frame = tk.Frame(self.prof_canvas, bg="#14014a")
        self.prof_canvas.create_window((0, 0), window=self.prof_inner_frame, anchor='nw')
        self.prof_inner_frame.bind("<Configure>", lambda e: self.prof_canvas.configure(scrollregion=self.prof_canvas.bbox("all")))

        # Lado direito - Tipo de Item
        tk.Label(self, text="Itens", bg="#3d0586", fg="white", font=("Arial", 18, "bold"), width=20, height=1).place(x=1240, y=10)

        self.tipo_item_var = tk.StringVar()
        self.tipo_item_var.trace_add("write", self.carregar_itens)

        item_combobox = ttk.Combobox(
            self,
            textvariable=self.tipo_item_var,
            values=["Item", "Municao", "Melee", "Ranged", "Protecao", "Melhoria"],
            state="readonly", width=46, style="CustomCombobox.TCombobox"
        )
        item_combobox.place(x=1240, y=45)
        item_combobox.bind("<<ComboboxSelected>>", self.carregar_itens)

        item_canvas_frame = tk.Frame(self, bg="#130f26")
        item_canvas_frame.place(x=1240, y=85, width=300, height=350)

        self.tipo_item_canvas = tk.Canvas(item_canvas_frame, bg="#14014a", highlightbackground="#4e00b3", highlightthickness=2)
        item_scrollbar = tk.Scrollbar(item_canvas_frame, orient="vertical", command=self.tipo_item_canvas.yview)
        self.tipo_item_canvas.configure(yscrollcommand=item_scrollbar.set)

        item_scrollbar.pack(side="right", fill="y")
        self.tipo_item_canvas.pack(side="left", fill="both", expand=True)

        self.item_inner_frame = tk.Frame(self.tipo_item_canvas, bg="#14014a")
        self.tipo_item_canvas.create_window((0, 0), window=self.item_inner_frame, anchor="nw")
        self.item_inner_frame.bind("<Configure>", lambda e: self.tipo_item_canvas.configure(scrollregion=self.tipo_item_canvas.bbox("all")))

        # Lado direito - Kit
        tk.Label(self, text="Kits ", bg="#3d0586", fg="white", font=("Arial", 18, "bold"), width=20, height=1).place(x=1240, y=450)

        self.kit_var = tk.StringVar()
        self.kit_var.trace_add("write", self.carregar_kit)

        kit_combobox = ttk.Combobox(self, textvariable=self.kit_var, values=list(D.kits_por_nome.keys()), state="readonly", width=46, style="CustomCombobox.TCombobox")
        kit_combobox.place(x=1240, y=485)

        kit_canvas_frame = tk.Frame(self, bg="#130f26")
        kit_canvas_frame.place(x=1240, y=525, width=300, height=350)

        self.kit_canvas = tk.Canvas(kit_canvas_frame, bg="#14014a", highlightbackground="#4e00b3", highlightthickness=2)
        kit_scrollbar = tk.Scrollbar(kit_canvas_frame, orient="vertical", command=self.kit_canvas.yview)
        self.kit_canvas.configure(yscrollcommand=kit_scrollbar.set)

        kit_scrollbar.pack(side="right", fill="y")
        self.kit_canvas.pack(side="left", fill="both", expand=True)

        self.kit_inner_frame = tk.Frame(self.kit_canvas, bg="#14014a")
        self.kit_canvas.create_window((0, 0), window=self.kit_inner_frame, anchor="nw")
        self.kit_inner_frame.bind("<Configure>", lambda e: self.kit_canvas.configure(scrollregion=self.kit_canvas.bbox("all")))

    def Voltar(self):
        self.controller.voltar()

    def TelaDeSelecao(self):
        self.controller.TelaDeSelecao()

    def TelaDeCombate(self):
        self.controller.TelaDeCombate()

    def mostrar_topico(self, *args):
        texto = D.Topicos.get(self.topico_var.get(), "Tópico não encontrado.")
        self.texto_label.config(text=texto)

    def carregar_npcs(self, event=None):
        grupo = self.npc_grupo_var.get()

        for widget in self.npc_inner_frame.winfo_children():
            widget.destroy()

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

            btn = tk.Button(self.npc_inner_frame, text=nome, font=("Arial", 12, "bold"),
                            bg="#3d0586", fg="white", relief="flat", command=mostrar_info)
            btn.pack(fill="x", padx=10, pady=5)

    def carregar_proficiencias(self, *args):
        for widget in self.prof_inner_frame.winfo_children():
            widget.destroy()

        filtro = self.prof_filtro_var.get()

        grupos = {
            "Força": D.Força,
            "Agilidade": D.Agilidade,
            "Vigor": D.Vigor,
            "Inteligência": D.Inteligencia,
            "Presença": D.Presença,
            "Tática": D.Tática
        }

        if filtro == "Geral" or filtro not in grupos:
            todas = D.Proficiencias
        else:
            todas = grupos[filtro]

        for nome in todas:
            tk.Label(self.prof_inner_frame, text=nome, bg="#14014a", fg="white", font=("Arial", 12, "bold"), anchor="w").pack(fill="x", padx=10, pady=3)

    def carregar_itens(self, *args):
        # Limpar itens antigos
        for widget in self.item_inner_frame.winfo_children():
            widget.destroy()

        tipo = self.tipo_item_var.get()

        tipos_dict = {
            "Item": D.Items,
            "Municao": D.Munições,
            "Melee": D.Melees,
            "Ranged": D.Rangeds,
            "Protecao": D.Protecoes,
            "Melhoria": D.Melhorias
        }

        if tipo not in tipos_dict:
            return

        pool = tipos_dict[tipo]

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

            # Cria botão real com scroll funcionando
            btn = tk.Button(self.item_inner_frame, text=nome, font=("Arial", 12, "bold"), bg="#3d0586", fg="white", command=abrir_popup)
            btn.pack(fill="x", padx=5, pady=2)

        # Força atualização do scroll
        self.tipo_item_canvas.configure(scrollregion=self.tipo_item_canvas.bbox("all"))

    def carregar_kit(self, *args):
        for widget in self.kit_inner_frame.winfo_children():
            widget.destroy()

        nome_kit = self.kit_var.get()
        if nome_kit not in D.kits_por_nome:
            return

        kit = D.kits_por_nome[nome_kit]

        contagem = {}
        for item in kit.itens:
            nome = getattr(item, "nome", str(item))
            contagem[nome] = contagem.get(nome, 0) + 1

        for nome, qtd in contagem.items():
            texto = f"{nome} x{qtd}"
            tk.Label(
                self.kit_inner_frame,
                text=texto,
                bg="#14014a",
                fg="white",
                font=("Arial", 12, "bold"),
                anchor="w"
            ).pack(fill="x", padx=10, pady=3)
### TELA DE DICIONARIOS ###
### TELA DE DICIONARIOS ###
### TELA DE DICIONARIOS ###

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1600x900")
        self.title("BALLISTIC_Nexus")
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