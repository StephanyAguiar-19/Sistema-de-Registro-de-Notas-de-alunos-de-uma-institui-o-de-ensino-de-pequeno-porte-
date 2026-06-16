import sqlite3
from tkinter import *
from tkinter import messagebox, ttk

# --- LÓGICA DE BANCO DE DADOS ---
def conectar():
    return sqlite3.connect("sistema_notas.db")

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            disciplina TEXT NOT NULL,
            nota REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def carregar_alunos_do_arquivo():
    """Carrega os alunos do arquivo_alunos.txt para o banco de dados"""
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # Verificar se há dados na tabela
        cursor.execute("SELECT COUNT(*) FROM alunos")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return  # Se já há dados, não carrega novamente
        
        # Ler arquivo
        with open("arquivo_alunos.txt", "r", encoding="utf-8") as file:
            linhas = file.readlines()
        
        # Pular cabeçalho e processar dados
        for linha in linhas[1:]:
            linha = linha.strip()
            if linha and "," in linha:
                partes = linha.split(",")
                if len(partes) >= 4:
                    try:
                        nome = partes[1].strip()
                        disciplina = partes[2].strip()
                        nota = float(partes[3].strip())
                        
                        cursor.execute("INSERT INTO alunos (nome, disciplina, nota) VALUES (?, ?, ?)",
                                     (nome, disciplina, nota))
                    except (ValueError, IndexError):
                        continue
        
        conn.commit()
        conn.close()
    except FileNotFoundError:
        pass  # Se o arquivo não existir, continua sem carregar

# --- INTERFACE GRÁFICA ---
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Notas")
        self.root.geometry("600x500")
        
        # Paleta de cores - Tema azul e branco minimalista
        self.cor_principal = "#0056B3"      # Azul escuro
        self.cor_secundaria = "#0078D4"     # Azul
        self.cor_fundo = "#F8F9FA"          # Cinza muito claro
        self.cor_texto = "#212529"          # Cinza escuro
        self.cor_branca = "#FFFFFF"         # Branco
        
        self.root.config(bg=self.cor_fundo)
        
        # Configurar estilo do Treeview
        estilo = ttk.Style()
        estilo.theme_use('clam')
        estilo.configure("Treeview",
                        background=self.cor_branca,
                        foreground=self.cor_texto,
                        fieldbackground=self.cor_branca,
                        font=("Arial", 10))
        estilo.configure("Treeview.Heading",
                        background=self.cor_principal,
                        foreground=self.cor_branca,
                        font=("Arial", 10, "bold"))
        estilo.map('Treeview', background=[('selected', self.cor_secundaria)])
        
        # Configurar estilo de Scrollbar
        estilo.configure("Vertical.TScrollbar",
                        background=self.cor_fundo,
                        troughcolor=self.cor_fundo)
        
        # Variáveis
        self.var_nome = StringVar()
        self.var_disciplina = StringVar()
        self.var_nota = StringVar()
        self.id_selecionado = None

        # Header
        header = Frame(self.root, bg=self.cor_principal, height=60)
        header.pack(fill=X)
        Label(header, text="Sistema de Registro de Notas", 
              font=("Arial", 20, "bold"), bg=self.cor_principal, 
              fg=self.cor_branca).pack(pady=15)

        # Layout superior (Formulário)
        frame_form = Frame(self.root, bg=self.cor_fundo)
        frame_form.pack(pady=20, padx=20, fill=X)

        # Nome do Aluno
        Label(frame_form, text="Nome do Aluno:", font=("Arial", 10), 
              bg=self.cor_fundo, fg=self.cor_texto).grid(row=0, column=0, padx=10, pady=10, sticky=W)
        entry_nome = Entry(frame_form, textvariable=self.var_nome, 
                          font=("Arial", 10), width=30, relief="solid", bd=1)
        entry_nome.config(bg=self.cor_branca, fg=self.cor_texto)
        entry_nome.grid(row=0, column=1, padx=10, pady=10)

        # Disciplina
        Label(frame_form, text="Disciplina:", font=("Arial", 10), 
              bg=self.cor_fundo, fg=self.cor_texto).grid(row=1, column=0, padx=10, pady=10, sticky=W)
        entry_disciplina = Entry(frame_form, textvariable=self.var_disciplina, 
                                font=("Arial", 10), width=30, relief="solid", bd=1)
        entry_disciplina.config(bg=self.cor_branca, fg=self.cor_texto)
        entry_disciplina.grid(row=1, column=1, padx=10, pady=10)

        # Nota
        Label(frame_form, text="Nota:", font=("Arial", 10), 
              bg=self.cor_fundo, fg=self.cor_texto).grid(row=2, column=0, padx=10, pady=10, sticky=W)
        entry_nota = Entry(frame_form, textvariable=self.var_nota, 
                          font=("Arial", 10), width=30, relief="solid", bd=1)
        entry_nota.config(bg=self.cor_branca, fg=self.cor_texto)
        entry_nota.grid(row=2, column=1, padx=10, pady=10)

        # Botões
        frame_botoes = Frame(self.root, bg=self.cor_fundo)
        frame_botoes.pack(pady=15)

        Button(frame_botoes, text="Cadastrar", command=self.create, 
               bg=self.cor_principal, fg=self.cor_branca, font=("Arial", 10, "bold"),
               relief="flat", padx=15, pady=8, cursor="hand2").grid(row=0, column=0, padx=5)
        Button(frame_botoes, text="Atualizar", command=self.update, 
               bg=self.cor_secundaria, fg=self.cor_branca, font=("Arial", 10, "bold"),
               relief="flat", padx=15, pady=8, cursor="hand2").grid(row=0, column=1, padx=5)
        Button(frame_botoes, text="Excluir", command=self.delete, 
               bg="#DC3545", fg=self.cor_branca, font=("Arial", 10, "bold"),
               relief="flat", padx=15, pady=8, cursor="hand2").grid(row=0, column=2, padx=5)
        Button(frame_botoes, text="Limpar", command=self.limpar_campos, 
               bg="#6C757D", fg=self.cor_branca, font=("Arial", 10, "bold"),
               relief="flat", padx=15, pady=8, cursor="hand2").grid(row=0, column=3, padx=5)

        # Treeview (Visualização dos Dados)
        frame_tabela = Frame(self.root, bg=self.cor_fundo)
        frame_tabela.pack(pady=20, padx=20, fill=BOTH, expand=True)

        self.tree = ttk.Treeview(frame_tabela, columns=("ID", "Nome", "Disciplina", "Nota"), show="headings", height=12)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Disciplina", text="Disciplina")
        self.tree.heading("Nota", text="Nota")
        self.tree.column("ID", width=40)
        self.tree.column("Nome", width=180)
        self.tree.column("Disciplina", width=150)
        self.tree.column("Nota", width=70)
        self.tree.bind("<<TreeviewSelect>>", self.preencher_campos)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabela, orient=VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.tree.configure(yscroll=scrollbar.set)

        self.read()

    # Operações CRUD
    def create(self):
        if self.var_nome.get() == "" or self.var_disciplina.get() == "" or self.var_nota.get() == "":
            messagebox.showwarning("Erro", "Preencha todos os campos!")
            return
        
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO alunos (nome, disciplina, nota) VALUES (?, ?, ?)", 
                       (self.var_nome.get(), self.var_disciplina.get(), self.var_nota.get()))
        conn.commit()
        conn.close()
        self.read()
        self.limpar_campos()

    def read(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alunos")
        for linha in cursor.fetchall():
            self.tree.insert("", END, values=linha)
        conn.close()

    def update(self):
        if not self.id_selecionado:
            messagebox.showwarning("Erro", "Selecione um aluno na lista!")
            return
        
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE alunos SET nome=?, disciplina=?, nota=? WHERE id=?", 
                       (self.var_nome.get(), self.var_disciplina.get(), self.var_nota.get(), self.id_selecionado))
        conn.commit()
        conn.close()
        self.read()
        self.limpar_campos()

    def delete(self):
        if not self.id_selecionado:
            messagebox.showwarning("Erro", "Selecione um aluno na lista!")
            return
        
        if messagebox.askyesno("Confirmar", "Deseja excluir este registro?"):
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM alunos WHERE id=?", (self.id_selecionado,))
            conn.commit()
            conn.close()
            self.read()
            self.limpar_campos()

    def preencher_campos(self, event):
        item = self.tree.selection()[0]
        valores = self.tree.item(item, "values")
        self.id_selecionado = valores[0]
        self.var_nome.set(valores[1])
        self.var_disciplina.set(valores[2])
        self.var_nota.set(valores[3])

    def limpar_campos(self):
        self.var_nome.set("")
        self.var_disciplina.set("")
        self.var_nota.set("")
        self.id_selecionado = None

if __name__ == "__main__":
    criar_tabela()
    carregar_alunos_do_arquivo()
    root = Tk()
    App(root)
    root.mainloop()
