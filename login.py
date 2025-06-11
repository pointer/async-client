import tkinter as tk
from tkinter import messagebox

def registrar():
    nome = entry_nome.get()
    senha = entry_senha.get()

    if nome and senha:
        usuarios[nome] = senha
        messagebox.showinfo('Registrado', 'Sua conta foi criada com sucesso')

        # Limpar o formulário
        entry_nome.delete(0, tk.END)
        entry_senha.delete(0, tk.END)

    else:
        messagebox.showerror('Falha', 'Insira usuário e senha desejados')

def login():
    nome = entry_nome.get()
    senha = entry_senha.get()

    if usuarios.get(nome) == senha:
        messagebox.showinfo('Logado', f'Bem vindo, {nome}')
    else:
        messagebox.showerror('Falha', 'Credenciais inválidas')

    # Limpar o formulário
    entry_nome.delete(0, tk.END)
    entry_senha.delete(0, tk.END)

# Dicionário para guardar os usuários
usuarios = {}

# Criar a janela
janela = tk.Tk()
janela.title('Login')
janela.geometry('360x360')

# Fontes
fonte_padrao = ('Arial', 14)
fonte_menor = ('Arial', 12)

frame_principal = tk.Frame(janela)
frame_principal.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Create labels and entry fields
label_nome = tk.Label(frame_principal, text='Usuário:', font=fonte_padrao,
    padx=5, pady=5)
label_nome.pack()
entry_nome = tk.Entry(frame_principal, font=fonte_menor)
entry_nome.pack()

label_senha = tk.Label(frame_principal, text='Password:', font=fonte_padrao,
    padx=5, pady=5)
label_senha.pack()
entry_senha = tk.Entry(frame_principal, show='*', font=fonte_menor)
entry_senha.pack()

frame_botoes = tk.Frame(frame_principal)
frame_botoes.pack(padx=15, pady=15)

# botão de registrar
botao_registrar = tk.Button(frame_botoes, text='Registrar', 
    font=fonte_menor, command=registrar)
botao_registrar.grid(row=0, column=0, padx=15, ipadx=2, ipady=2)

# botão de login
botao_login = tk.Button(frame_botoes, text='Login', 
    font=fonte_menor, command=login)
botao_login.grid(row=0, column=1, padx=15, ipadx=2, ipady=2)

# Run the application
janela.mainloop()
