import re
import streamlit as st
import pandas as pd

# ------------------------------------------------------------
# CSS PARA DEIXAR OS BOTÕES COM VISUAL "PREENCHIDO"
# ------------------------------------------------------------
# Você pode ajustar cores, bordas e etc. conforme desejar.
st.markdown(
    """
    <style>
    /* Ajusta a cor e estilo básico dos botões gerados por st.button */
    button[data-baseweb="button"] {
        background-color: #007aff !important; /* Azul estilo Apple */
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        padding: 0.6em 1em !important;
        margin: 0.2em !important;
    }

    /* Ajusta o container dos botões para que fiquem mais próximos uns dos outros */
    .css-1ea4gb4.e1ewe7hr3 {
        gap: 0.2rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

class myStack:
    def __init__(self):
        self.stack = []

    def push(self, x):
        self.stack.append(x)

    def size(self):
        return len(self.stack)

    def empty(self):
        return self.size() == 0

    def top(self):
        return self.stack[-1]

    def pop(self):
        res = self.top()
        self.stack.pop()
        return res

def Priority(c: str):
    if c == '(':
        return 0
    elif c in ['>', '~']:  # -> ou <-> (convertidos em > e ~)
        return 1
    elif c in ['v', '^']:  # ou (v) e e (^)
        return 2
    else:
        assert c == '!'
        return 3

def Oper(x: int, y: int, oper: str):
    if oper == 'v':  # OR
        return x | y
    elif oper == '^':  # AND
        return x & y
    elif oper == '>':  # IMPLICAÇÃO
        return ((1 ^ x) | y)
    else:
        assert oper == '~'  # BICONDICIONAL
        return 1 if (x == y) else 0

def preprocess(expression: str):
    expression = re.sub(' ', '', expression)
    expression = re.sub('<->', '~', expression)  # <-> para ~
    expression = re.sub('->', '>', expression)   # -> para >
    expression = re.sub('-', '!', expression)    # - para !
    expression = re.sub(r'\+', 'v', expression)  # + para v
    expression = re.sub('\.', '^', expression)   # . para ^
    # Remove !! (dupla negação)
    while re.search('!!', expression):
        expression = re.sub('!!', '', expression)
    return expression

def GetVariable(expression: str):
    SetVar = set()
    ListVar = []
    for c in expression:
        if 'a' <= c <= 'z' and c != 'v':
            if c not in SetVar:
                SetVar.add(c)
                ListVar.append(c)
    return ListVar

def GetRPN(expression: str):
    stack = myStack()
    RPN = myStack()
    for c in expression:
        if c == '(':
            stack.push(c)
        elif c == ')':
            while True:
                x = stack.pop()
                if x == '(':
                    break
                RPN.push(x)
        elif c in ['v', '^', '>', '~', '!']:
            while (not stack.empty()) and Priority(c) <= Priority(stack.top()):
                RPN.push(stack.pop())
            stack.push(c)
        else:
            # 0, 1 ou variável (a, b, c, etc.)
            RPN.push(c)
    while not stack.empty():
        RPN.push(stack.pop())
    return RPN

def Calculate(RPN: myStack, VariableValue: dict):
    res = myStack()
    for c in RPN.stack:
        if c in ['0', '1'] or ('a' <= c <= 'z' and c != 'v'):
            res.push(VariableValue[c])
        elif c == '!':  # NOT
            val = res.pop()
            res.push(1 ^ val)
        else:  # ^, v, >, ~
            x = res.pop()
            y = res.pop()
            res.push(Oper(y, x, c))
    assert res.size() == 1
    return res.pop()

def Solve(expression: str):
    """Retorna (DataFrame da Tabela Verdade, Classificação)."""
    # Prepara a expressão e extrai variáveis
    list_var = GetVariable(expression)
    expr_label = expression

    expression = preprocess(expression)
    RPN = GetRPN(expression)

    # Monta colunas para o DF
    colunas = list_var + [expr_label]
    resultados = []

    n = len(list_var)
    for mask in range(2 ** n):
        VariableValue = {'0': 0, '1': 1}
        linha = []
        for i in range(n):
            VariableValue[list_var[i]] = (mask >> (n - i - 1)) & 1
            linha.append(VariableValue[list_var[i]])
        valor_expr = Calculate(RPN, VariableValue)
        linha.append(valor_expr)
        resultados.append(linha)

    valores_finais = [row[-1] for row in resultados]
    if all(v == 1 for v in valores_finais):
        classificacao = "Tautologia"
    elif all(v == 0 for v in valores_finais):
        classificacao = "Contradição"
    else:
        classificacao = "Contingência"

    df = pd.DataFrame(resultados, columns=colunas)
    return df, classificacao


# ------------------------------------------------------------
# INTERFACE DE "CALCULADORA LÓGICA" EM STREAMLIT
# ------------------------------------------------------------
def main():
    st.title("Calculadora de Tabela Verdade")

    st.markdown("""
    **Monte a expressão booleana clicando nos botões abaixo**  
    Operadores suportados:
    - `^` (E / AND)
    - `v` (OU / OR)
    - `->` (IMPLICAÇÃO)
    - `<->` (BICONDICIONAL)
    - `!` (NÃO / NOT)

    **Exemplo**: (a ^ b) -> c
    """)

    # Sessão para armazenar a expressão atual
    if "expression" not in st.session_state:
        st.session_state["expression"] = ""

    def add_symbol(symbol: str):
        st.session_state["expression"] += symbol

    # Mostra a expressão no topo, como se fosse o display da “calculadora”
    st.subheader("Expressão Atual")
    st.code(st.session_state["expression"], language="plaintext")

    # Primeira linha
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("("):
            add_symbol("(")
    with c2:
        if st.button(")"):
            add_symbol(")")
    with c3:
        if st.button("Limpar"):
            st.session_state["expression"] = ""
    with c4:
        if st.button("←"):  # Apagar último caractere
            st.session_state["expression"] = st.session_state["expression"][:-1]

    # Segunda linha
    c5, c6, c7, c8 = st.columns(4)
    with c5:
        if st.button("a"):
            add_symbol("a")
    with c6:
        if st.button("b"):
            add_symbol("b")
    with c7:
        if st.button("c"):
            add_symbol("c")
    with c8:
        if st.button("!"):  # NOT
            add_symbol("!")

    # Terceira linha
    c9, c10, c11, c12 = st.columns(4)
    with c9:
        if st.button("->"):
            add_symbol("->")
    with c10:
        if st.button("<->"):
            add_symbol("<->")
    with c11:
        if st.button("^"):  # AND
            add_symbol("^")
    with c12:
        if st.button("v"):  # OR
            add_symbol("v")

    # Quarta linha
    c13, c14, c15, c16 = st.columns(4)
    with c13:
        if st.button("1"):
            add_symbol("1")
    with c14:
        if st.button("0"):
            add_symbol("0")
    # Deixamos c15 vazio (ou poderíamos pôr outro botão).
    with c15:
        st.write("")  # Espaço em branco
    with c16:
        # Botão para gerar a tabela
        if st.button("Gerar Tabela"):
            expr = st.session_state["expression"]
            if expr.strip():
                df, classificacao = Solve(expr)
                st.subheader("Tabela Verdade")
                st.table(df)
                st.write(f"**Classificação**: {classificacao}")
            else:
                st.warning("A expressão está vazia. Monte algo antes de gerar a tabela.")

if __name__ == "__main__":
    main()
