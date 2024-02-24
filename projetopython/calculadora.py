import tkinter as tk

def calcular():
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        operacao = operacoes.get()
        
        if operacao == "+":
            resultado.set(round(num1 + num2))
        elif operacao == "-":
            resultado.set(round(num1 - num2))
        elif operacao == "*":
            resultado.set(round(num1 * num2))
        elif operacao == "/":
            if num2 == 0:
                resultado.set("Erro: Divisão por zero")
            else:
                resultado.set(round(num1 / num2))
    except ValueError:
        resultado.set("Erro: Valores inválidos")

# Configurar a janela principal
root = tk.Tk()
root.title("Calculadora")


# Entradas para os números e menu suspenso para operações
entry_num1 = tk.Entry(root)
entry_num2 = tk.Entry(root)
operacoes = tk.StringVar()
operacoes.set("+")  # Padrão: adição

# Variáveis para armazenar os números e o resultado
resultado = tk.StringVar()
resultado.set("Resultado")

# Botão de cálculo
botao_calcular = tk.Button(root, text="Calcular", command=calcular)

# Exibição do resultado
label_resultado = tk.Label(root, textvariable=resultado)

# Layout dos widgets na janela
entry_num1.pack()
entry_num2.pack()
botao_calcular.pack()
label_resultado.pack()
tk.OptionMenu(root, operacoes, "+", "-", "*", "/").pack()

# Iniciar a interface gráfica
root.mainloop()

