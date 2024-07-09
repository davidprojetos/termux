import tkinter as tk
from tkinter import messagebox
import time


class ComputadorInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Computador Interface")
        self.geometry("400x300")

        self.computador = None

        self.create_widgets()

    def create_widgets(self):
        self.label_status = tk.Label(self, text="Estado: Desligado")
        self.label_status.pack()

        self.button_ligar = tk.Button(self, text="Ligar", command=self.ligar_computador)
        self.button_ligar.pack()

        self.button_desligar = tk.Button(self, text="Desligar", command=self.desligar_computador, state=tk.DISABLED)
        self.button_desligar.pack()

        self.button_adicionar_arquivo = tk.Button(self, text="Adicionar Arquivo", command=self.adicionar_arquivo, state=tk.DISABLED)
        self.button_adicionar_arquivo.pack()

        self.button_listar_arquivos = tk.Button(self, text="Listar Arquivos", command=self.listar_arquivos, state=tk.DISABLED)
        self.button_listar_arquivos.pack()

        self.button_deletar_arquivo = tk.Button(self, text="Deletar Arquivo", command=self.deletar_arquivo, state=tk.DISABLED)
        self.button_deletar_arquivo.pack()

    def ligar_computador(self):
        self.computador = computador()
        self.computador.modelo = "Inpirion 3360"
        self.computador.marca = "Dell"
        self.computador.cpu = "I5"
        self.computador.memoria_ram_max = "8GB"
        self.computador.capacidade_hd_max = 1000 
        self.computador.ligar()
        self.label_status.config(text="Estado: Ligado")
        self.button_ligar.config(state=tk.DISABLED)
        self.button_desligar.config(state=tk.NORMAL)
        self.button_adicionar_arquivo.config(state=tk.NORMAL)
        self.button_listar_arquivos.config(state=tk.NORMAL)
        self.button_deletar_arquivo.config(state=tk.NORMAL)
        self.countdown_timer(6)

    def desligar_computador(self):
        self.computador.desligar()
        self.label_status.config(text="Estado: Desligado")
        self.button_ligar.config(state=tk.NORMAL)
        self.button_desligar.config(state=tk.DISABLED)
        self.button_adicionar_arquivo.config(state=tk.DISABLED)
        self.button_listar_arquivos.config(state=tk.DISABLED)
        self.button_deletar_arquivo.config(state=tk.DISABLED)

    def adicionar_arquivo(self):
        nome = tk.simpledialog.askstring("Adicionar Arquivo", "Digite o nome do arquivo:")
        if nome:
            tamanho = tk.simpledialog.askinteger("Adicionar Arquivo", "Digite o tamanho do arquivo em GB:")
            if tamanho is not None:
                self.computador.criar_arquivo(nome, tamanho)

    def listar_arquivos(self):
        messagebox.showinfo("Arquivos", self.computador.listar_arquivos())

    def deletar_arquivo(self):
        nome = tk.simpledialog.askstring("Deletar Arquivo", "Digite o nome do arquivo a ser deletado:")
        if nome:
            messagebox.showinfo("Deletar Arquivo", self.computador.deletar_arquivo(nome))

    def countdown_timer(self, seconds):
        for i in range(seconds, 0, -1):
            self.label_status.config(text=f"Ligando aguarde: {i} segundos")
            self.update()
            time.sleep(1)


class computador:
    modelo = None
    marca = None
    cpu = None
    memoria_atual = 0
    memoria_ram_max = None
    capacidade_hd = 0
    capacidade_hd_max = None
    arquivos = {}
    quantidade_arquivos = 0
    estado = 'desligado'

    def ligar(self):
        self.estado = 'ligado'

    def desligar(self):
        self.estado = 'desligado'

    def criar_arquivo(self, nome_arquivo, tamanho):
        if self.estado == 'ligado':
            if self.capacidade_hd_max - tamanho > 0:
                self.capacidade_hd_max -= tamanho
                self.arquivos[self.quantidade_arquivos] = (nome_arquivo, tamanho)
                self.quantidade_arquivos += 1
                print(f"Arquivo de {tamanho} GB adicionado no HD.")
            else:
                print("Memoria Cheia!")
        else:
            print("Computador Desligado!")

    def listar_arquivos(self):
        if self.estado == 'ligado':
            arquivos_info = ""
            for x in range(0, self.quantidade_arquivos):
                arquivos_info += f"Nome: {self.arquivos[x][0]} | Tamanho: {self.arquivos[x][1]} GB\n"
            return arquivos_info
        else:
            return "Computador Desligado!"

    def deletar_arquivo(self, nome_arquivo):
        if self.estado == 'ligado':
            quantidade = 0
            for x in range(self.quantidade_arquivos):
                if self.arquivos[x][0] == nome_arquivo:
                    quantidade += 1
            if quantidade >= 2:
                opcao = tk.messagebox.askyesno("Deletar Arquivo", f"Exite mais de um arquivo com o nome '{nome_arquivo}'. Deseja apagar todos?")
                if opcao:
                    for x in range(self.quantidade_arquivos):
                        if self.arquivos[x][0] == nome_arquivo:
                            self.capacidade_hd_max += self.arquivos[x][1]
                            self.quantidade_arquivos -= 1
                            self.arquivos.update(x=(None, None))
                    return "Arquivos apagados com sucesso!"
                else:
                    return "Operação cancelada!"
            elif quantidade == 1:
                for x in range(self.quantidade_arquivos):
                    if self.arquivos[x][0] == nome_arquivo:
                        self.capacidade_hd_max += self.arquivos[x][1]
                        self.quantidade_arquivos -= 1
                        self.arquivos.update(x=(None, None))
                return "Arquivo apagado com sucesso!"
            else:
                return f"Arquivo '{nome_arquivo}' não encontrado!"
        else:
            return "Computador Desligado!"


app = ComputadorInterface()
app.mainloop()

