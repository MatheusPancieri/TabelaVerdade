# Calculadora de Tabela Verdade
## Projeto da disciplina Matemática discreta feita pelos alunos 
### Matheus Pancieri Preza da Silva - ra193282 Fabrício Marques De Souza - ra196892 Ary Correa Coelho - ra194240 

Este projeto é uma calculadora interativa de tabelas verdade para expressões lógicas proposicionais, desenvolvida em Python usando Streamlit.

## Funcionalidades

- Aceita expressões lógicas com operadores:
  - `^` (E)
  - `v` (OU)
  - `->` (Implica)
  - `<->` (Bicondicional)
  - `!` (Negação)
- Gera a tabela verdade da expressão informada.
- Classifica a expressão como Tautologia, Contradição ou Contingência.
- Interface web simples e intuitiva via Streamlit.

## Como usar

### Pré-requisitos

- Python 3.6 ou superior
- Streamlit
- Pandas

### Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/SeuUsuario/SeuRepositorio.git
   cd SeuRepositorio
````

2. Crie e ative um ambiente virtual (recomendado):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

### Executando o app

```bash
streamlit run main.py
```

## Exemplo de expressões válidas

* `(a ^ b) -> c`
* `!(a v b) ^ c`
* `a <-> (b v !c)`
