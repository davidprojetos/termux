import csv
from openpyxl import Workbook, load_workbook
from openpyxl.utils.exceptions import InvalidFileException
from openpyxl.utils import get_column_letter
from operator import itemgetter

# Função para criar um novo arquivo Excel
def criar_arquivo_excel(nome_arquivo):
    try:
        workbook = Workbook()
        workbook.save(filename=nome_arquivo)
        print("Arquivo Excel criado com sucesso!")
    except Exception as e:
        print(f"Erro ao criar arquivo Excel: {e}")

# Função para adicionar uma nova planilha
def adicionar_planilha(arquivo, nome_planilha):
    try:
        workbook = load_workbook(arquivo)
        workbook.create_sheet(title=nome_planilha)
        workbook.save(arquivo)
        print("Planilha adicionada com sucesso!")
    except Exception as e:
        print(f"Erro ao adicionar planilha: {e}")
        
# Função para adicionar dados a uma planilha
def adicionar_dados(arquivo, planilha, novos_dados):
    try:
        workbook = load_workbook(arquivo)
        sheet = workbook[planilha]
        sheet.append(novos_dados)
        workbook.save(arquivo)
        print("Dados adicionados com sucesso!")
    except KeyError:
        print(f"A planilha '{planilha}' não foi encontrada.")
    except Exception as e:
        print(f"Erro ao adicionar dados: {e}")
# Função para ler dados de uma planilha
def ler_dados(arquivo, planilha):
    try:
        workbook = load_workbook(arquivo)
        sheet = workbook[planilha]
        dados = []
        for row in sheet.iter_rows(values_only=True):
            dados.append(row)
        return dados
    except KeyError:
        print(f"A planilha '{planilha}' não foi encontrada.")
        return []
    except Exception as e:
        print(f"Erro ao ler dados: {e}")
        return []

# Função para listar todas as planilhas no arquivo Excel
def listar_planilhas(arquivo):
    try:
        workbook = load_workbook(arquivo)
        return workbook.sheetnames
    except InvalidFileException:
        print("Arquivo Excel inválido.")
        return []
    except Exception as e:
        print(f"Erro ao listar planilhas: {e}")
        return []

# Função para exibir dados de forma formatada
def exibir_dados_formatados(dados):
    if dados:
        for linha in dados:
            print(" | ".join(str(col) for col in linha))
    else:
        print("Nenhum dado encontrado.")

# Função para atualizar nome da planilha
def atualizar_nome_planilha(arquivo, nome_antigo, novo_nome):
    try:
        workbook = load_workbook(arquivo)
        workbook[nome_antigo].title = novo_nome
        workbook.save(arquivo)
        print("Nome da planilha atualizado com sucesso!")
    except KeyError:
        print(f"A planilha '{nome_antigo}' não foi encontrada.")
    except Exception as e:
        print(f"Erro ao atualizar nome da planilha: {e}")

# Função para excluir planilha
def excluir_planilha(arquivo, nome_planilha):
    try:
        workbook = load_workbook(arquivo)
        del workbook[nome_planilha]
        workbook.save(arquivo)
        print("Planilha excluída com sucesso!")
    except KeyError:
        print(f"A planilha '{nome_planilha}' não foi encontrada.")
    except Exception as e:
        print(f"Erro ao excluir planilha: {e}")

# Função para ordenar dados
def ordenar_dados(arquivo, planilha, coluna):
    try:
        workbook = load_workbook(arquivo)
        sheet = workbook[planilha]
        dados = list(sheet.iter_rows(values_only=True))
        cabecalho = dados[0]
        dados_ordenados = [cabecalho] + sorted(dados[1:], key=itemgetter(coluna))
        return dados_ordenados
    except KeyError:
        print(f"A planilha '{planilha}' não foi encontrada.")
        return []
    except Exception as e:
        print(f"Erro ao ordenar dados: {e}")
        return []

# Função para buscar dados
def buscar_dados(arquivo, planilha, coluna, valor):
    try:
        workbook = load_workbook(arquivo)
        sheet = workbook[planilha]
        dados_encontrados = [linha for linha in sheet.iter_rows(values_only=True) if linha[coluna - 1] == valor]
        return dados_encontrados
    except KeyError:
        print(f"A planilha '{planilha}' não foi encontrada.")
        return []
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        return []

# Função para exportar dados para CSV
def exportar_para_csv(arquivo_excel, planilha, arquivo_csv):
    try:
        workbook = load_workbook(arquivo_excel)
        sheet = workbook[planilha]
        with open(arquivo_csv, 'w', newline='') as file:
            writer = csv.writer(file)
            for row in sheet.iter_rows(values_only=True):
                writer.writerow(row)
        print(f"Dados exportados para '{arquivo_csv}' com sucesso!")
    except FileNotFoundError:
        print("Arquivo Excel não encontrado.")
    except KeyError:
        print(f"A planilha '{planilha}' não foi encontrada.")
    except Exception as e:
        print(f"Erro ao exportar dados para CSV: {e}")

# Função para importar dados de CSV
def importar_de_csv(arquivo_excel, planilha, arquivo_csv):
    try:
        workbook = load_workbook(arquivo_excel)
        sheet = workbook[planilha]
        with open(arquivo_csv, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                sheet.append(row)
        workbook.save(arquivo_excel)
        print(f"Dados importados de '{arquivo_csv}' para '{planilha}' com sucesso!")
    except FileNotFoundError:
        print("Arquivo Excel não encontrado.")
    except KeyError:
        print(f"A planilha '{planilha}' não foi encontrada.")
    except Exception as e:
        print(f"Erro ao importar dados de CSV: {e}")

# Função para calcular estatísticas
def calcular_estatisticas(arquivo, planilha, coluna):
    try:
        workbook = load_workbook(arquivo)
        sheet = workbook[planilha]
        dados = [linha[coluna - 1] for linha in sheet.iter_rows(values_only=True)][1:]  # Ignorar cabeçalho
        dados_numericos = [float(valor) for valor in dados if isinstance(valor, (int, float))]
        if dados_numericos:
            print("Estatísticas:")
            print(f"Média: {sum(dados_numericos) / len(dados_numericos)}")
            print(f"Mínimo: {min(dados_numericos)}")
            print(f"Máximo: {max(dados_numericos)}")
        else:
            print("Não há dados numéricos na coluna selecionada.")
    except KeyError:
        print(f"A planilha '{planilha}' não foi encontrada.")
    except Exception as e:
        print(f"Erro ao calcular estatísticas: {e}")

# Função principal
def main():
    arquivo_excel = 'dados.xlsx'

    while True:
        print("\nSelecione uma opção:")
        print("1. Criar novo arquivo Excel")
        print("2. Adicionar planilha")
        print("3. Listar planilhas")
        print("4. Adicionar dados")
        print("5. Ler dados")
        print("6. Atualizar nome da planilha")
        print("7. Excluir planilha")
        print("8. Ordenar dados")
        print("9. Buscar dados")
        print("10. Exportar para CSV")
        print("11. Importar de CSV")
        print("12. Calcular estatísticas")
        print("13. Sair")

        opcao = input("Opção: ")

        if opcao == '1':
            criar_arquivo_excel(arquivo_excel)

        elif opcao == '2':
            nome_planilha = input("Digite o nome da nova planilha: ")
            adicionar_planilha(arquivo_excel, nome_planilha)

        elif opcao == '3':
            planilhas = listar_planilhas(arquivo_excel)
            if planilhas:
                print("Planilhas disponíveis:")
                for planilha in planilhas:
                    print(planilha)

        elif opcao == '4':
            planilha = input("Digite o nome da planilha: ")
            dados = input("Digite os dados a serem adicionados separados por vírgula: ").split(',')
            adicionar_dados(arquivo_excel, planilha, dados)

        elif opcao == '5':
            planilha = input("Digite o nome da planilha: ")
            dados = ler_dados(arquivo_excel, planilha)
            exibir_dados_formatados(dados)

        elif opcao == '6':
            nome_antigo = input("Digite o nome da planilha que deseja atualizar: ")
            novo_nome = input("Digite o novo nome da planilha: ")
            atualizar_nome_planilha(arquivo_excel, nome_antigo, novo_nome)

        elif opcao == '7':
            nome_planilha = input("Digite o nome da planilha que deseja excluir: ")
            excluir_planilha(arquivo_excel, nome_planilha)

        elif opcao == '8':
            planilha = input("Digite o nome da planilha: ")
            coluna = int(input("Digite o número da coluna para ordenar: "))
            dados_ordenados = ordenar_dados(arquivo_excel, planilha, coluna)
            exibir_dados_formatados(dados_ordenados)

        elif opcao == '9':
            planilha = input("Digite o nome da planilha: ")
            coluna = int(input("Digite o número da coluna para buscar: "))
            valor = input("Digite o valor a ser buscado: ")
            dados_encontrados = buscar_dados(arquivo_excel, planilha, coluna, valor)
            exibir_dados_formatados(dados_encontrados)

        elif opcao == '10':
            planilha = input("Digite o nome da planilha: ")
            arquivo_csv = input("Digite o nome do arquivo CSV para exportar: ")
            exportar_para_csv(arquivo_excel, planilha, arquivo_csv)

        elif opcao == '11':
            planilha = input("Digite o nome da planilha: ")
            arquivo_csv = input("Digite o nome do arquivo CSV para importar: ")
            importar_de_csv(arquivo_excel, planilha, arquivo_csv)

        elif opcao == '12':
            planilha = input("Digite o nome da planilha: ")
            coluna = int(input("Digite o número da coluna para calcular estatísticas: "))
            calcular_estatisticas(arquivo_excel, planilha, coluna)

        elif opcao == '13':
            print("Saindo...")
            break

        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
