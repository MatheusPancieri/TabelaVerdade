# 🧠 Calculadora de Tabela Verdade

Uma aplicação web desenvolvida com **Streamlit** para montar e analisar expressões lógicas por meio da tabela verdade.

Permite montar expressões utilizando botões ou digitando diretamente. Suporta negação, conjunção, disjunção, implicação e bicondicional.

---

## ✅ Funcionalidades

* Interface interativa com botões para montar expressões
* Campo de entrada direta com suporte a teclado e mouse
* Geração automática da tabela verdade
* Classificação da expressão como:

  * **Tautologia**
  * **Contradição**
  * **Contingência**

---

## ⚙️ Tecnologias usadas

* Python 3.9+
* Streamlit
* Pandas
* Regex

---

## ▶️ Como executar o projeto

### 1. Clone o repositório

git clone [https://github.com/MatheusPancieri/TabelaVerdade.git](https://github.com/MatheusPancieri/TabelaVerdade.git)
cd TabelaVerdade

### 2. Crie e ative um ambiente virtual

#### Windows

python -m venv venv
venv\Scripts\activate

#### Linux/Mac

python3 -m venv venv
source venv/bin/activate

### 3. Instale as dependências

pip install -r requirements.txt

### 4. Execute o app

streamlit run main.py

> Altere `main.py` se seu arquivo tiver outro nome.

---

## 🧪 Exemplo de expressão para testar

((a ^ b) -> c) <-> (a -> (b v c))

Essa é uma **contingência** — serve como bom teste para as principais operações lógicas.

---

## 📦 Atualizando dependências

Sempre que instalar algo novo com `pip install`, atualize o `requirements.txt` com:

pip freeze > requirements.txt

---

## 📁 Estrutura esperada do projeto

TabelaVerdade/
├── main.py
├── requirements.txt
├── .gitignore
└── README.md

---
