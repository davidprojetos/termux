"""

1) Crie uma lista com números inteiros de 1 a 10. Em seguida, use um loop para encontrar a soma 
de todos os números pares dessa lista.

"""
lista = []
soma = 0
for x in range(1,11):
  lista.append(x)
  if x%2==0:
    soma += x
print(f"Lista: {lista}")
print(f"Soma dos pares: {soma}")