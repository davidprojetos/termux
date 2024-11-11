"""

3) Escreva um programa que receba uma lista de números e retorne outra lista com os números 
elevados ao quadrado. Por exemplo, dado `[2, 3, 4]`, o código deve retornar `[4, 9, 16]`.

"""

lista = []
lista_quadrado = []

for x in range(0,5):
  while True:
    try:
      num = int(input("Digite um número inteiro: "))
      lista.append(x)
      lista_quadrado.append(x**2)
      break
    except ValueError:
      print("Entrada inválida! Digite um número valido.")
    
    
print(lista)
print(lista_quadrado)