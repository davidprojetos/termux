# 📘 FII Provisor — Guia de Comandos

Sistema de controle e projeção de rendimentos com Fundos Imobiliários (FIIs) utilizando Python + SQLite.

---

## ✅ Inicialização

```bash
python fiiprovisor.py init
```
> Inicializa o banco de dados e importa a carteira inicial fixa.

---

## ➕ Cadastro

### 1. Adicionar fundo manualmente

```bash
python fiiprovisor.py add_fundo <ticker> <quantidade> <total_investido>
```

**Exemplo:**
```bash
python fiiprovisor.py add_fundo MXRF11 100 1050.00
```

---

### 2. Adicionar provento (dividendo) manualmente

```bash
python fiiprovisor.py add_provento <ticker> <ano> <mes> <valor_cota>
```

**Exemplo:**
```bash
python fiiprovisor.py add_provento MXRF11 2025 5 0.10
```

---

### 3. Importar proventos de 2 meses atrás (completos)

```bash
python fiiprovisor.py fetch_two_months_complete
```
> Importa proventos pesquisados para todos os fundos da carteira (preenche com 0.00 os que não tiverem valor).

---

## 📊 Relatórios

### 1. Relatório consolidado da carteira

```bash
python fiiprovisor.py report_all
```
Mostra:
- Total investido
- Rendimento mensal estimado
- Projeção anual
- Rendimento percentual médio

---

### 2. Relatório individual por fundo

```bash
python fiiprovisor.py report_ind <ticker>
```

**Exemplo:**
```bash
python fiiprovisor.py report_ind MXRF11
```

Mostra:
- Quantidade de cotas
- Rendimento mensal estimado
- Rendimento percentual
- Tempo estimado para recuperar investimento

---

## 📈 Projeções

### 1. Projeção com reinvestimento (sem aporte)

```bash
python fiiprovisor.py project <meta_mensal>
```

**Exemplo:**
```bash
python fiiprovisor.py project 300
```

> Simula reinvestimento dos rendimentos até atingir R$300/mês de proventos.

---

### 2. Projeção com reinvestimento + aporte mensal fixo

```bash
python fiiprovisor.py project_aporte <meta_mensal> <aporte_mensal>
```

**Exemplo:**
```bash
python fiiprovisor.py project_aporte 500 250
```

> Simula crescimento com reinvestimento + aportes mensais.

---

### 3. Projeção investindo sempre nos FIIs mais rentáveis

```bash
python fiiprovisor.py project_melhor <meta_mensal> <aporte_mensal>
```

**Exemplo:**
```bash
python fiiprovisor.py project_melhor 500 300
```

> Investe priorizando os fundos com melhor rendimento relativo (dividendo / preço).

---

## 📂 Extras

Se quiser:

- Exportar relatórios para CSV
- Gerar gráfico da projeção de crescimento
- Importar proventos automaticamente de APIs públicas

Fale comigo e posso adicionar as funcionalidades.

---

## 🛠️ Requisitos

- Python 3.9+
- SQLite3 (já incluído na maioria das distribuições Python)
- Pode rodar em Termux (Android), Linux, Windows, macOS