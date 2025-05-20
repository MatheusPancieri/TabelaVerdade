import re
import streamlit as st
import pandas as pd

class myStack:
    def __init__(self):
        self.stack = []

    def push(self, x):
        self.stack.append(x)

    def size(self):
        return len(self.stack)

    def empty(self):
        return not self.stack

    def top(self):
        return self.stack[-1]

    def pop(self):
        return self.stack.pop()

def Priority(c: str):
    return {'(': 0, '>': 1, '~': 1, 'v': 2, '^': 2, '!': 3}.get(c, -1)

def Oper(x: int, y: int, oper: str):
    if oper == 'v': return x | y
    if oper == '^': return x & y
    if oper == '>': return (1 ^ x) | y
    if oper == '~': return int(x == y)
    raise ValueError("Operador inválido")

def preprocess(expression: str):
    expression = re.sub(r'\s+', '', expression)
    expression = expression.replace('<->', '~').replace('->', '>')
    expression = expression.replace('-', '!').replace('+', 'v').replace('.', '^')
    while '!!' in expression:
        expression = expression.replace('!!', '')
    return expression

def GetVariable(expression: str):
    return sorted({c for c in expression if 'a' <= c <= 'z' and c != 'v'})

def GetRPN(expression: str):
    stack, RPN = myStack(), myStack()
    for c in expression:
        if c == '(':
            stack.push(c)
        elif c == ')':
            while stack.top() != '(':
                RPN.push(stack.pop())
            stack.pop()
        elif c in ['v', '^', '>', '~', '!']:
            while not stack.empty() and Priority(c) <= Priority(stack.top()):
                RPN.push(stack.pop())
            stack.push(c)
        else:
            RPN.push(c)
    while not stack.empty():
        RPN.push(stack.pop())
    return RPN

def Calculate(RPN: myStack, VariableValue: dict):
    res = myStack()
    for c in RPN.stack:
        if c in VariableValue:
            res.push(VariableValue[c])
        elif c == '!':
            res.push(1 ^ res.pop())
        else:
            x, y = res.pop(), res.pop()
            res.push(Oper(y, x, c))
    return res.pop()

def Solve(expression: str):
    expr_label = expression
    expression = preprocess(expression)
    vars_list = GetVariable(expression)
    RPN = GetRPN(expression)
    n = len(vars_list)

    results = []
    for mask in range(2 ** n):
        values = {vars_list[i]: (mask >> (n - i - 1)) & 1 for i in range(n)}
        values.update({'0': 0, '1': 1})
        row = list(values[var] for var in vars_list)
        row.append(Calculate(RPN, values))
        results.append(row)

    final_vals = [r[-1] for r in results]
    if all(v == 1 for v in final_vals):
        classificacao = "Tautologia"
    elif all(v == 0 for v in final_vals):
        classificacao = "Contradição"
    else:
        classificacao = "Contingência"

    df = pd.DataFrame(results, columns=vars_list + [expr_label])
    return df, classificacao

# INTERFASSE
def main():
    st.title("Calculadora de Tabela Verdade")

    st.markdown("""
    Monte sua expressão lógica usando os botões ou digite diretamente abaixo.  
    Operadores suportados:
    - `^` (E)
    - `v` (OU)
    - `->` (Implica)
    - `<->` (Bicondicional)
    - `!` (Negação)

    **Exemplo**: (a ^ b) -> c
    """)

    # Inicializa estados
    if "expression" not in st.session_state:
        st.session_state["expression"] = ""
    if "output_df" not in st.session_state:
        st.session_state["output_df"] = None
    if "output_classificacao" not in st.session_state:
        st.session_state["output_classificacao"] = None
    if "output_error" not in st.session_state:
        st.session_state["output_error"] = None

    # Campo de entrada editável com teclado/mouse
    st.subheader("Expressão Atual")
    expression_input = st.text_input("Digite ou use os botões abaixo:", st.session_state["expression"])
    st.session_state["expression"] = expression_input  # sincroniza com o campo

    # Lógica para adicionar símbolos
    def add_symbol(symbol):
        st.session_state["expression"] += symbol

    # Geração da tabela
    def generate_table():
        expr = st.session_state["expression"]
        st.session_state["output_error"] = None
        if expr.strip():
            try:
                df, classificacao = Solve(expr)
                st.session_state["output_df"] = df
                st.session_state["output_classificacao"] = classificacao
            except Exception as e:
                st.session_state["output_error"] = str(e)
        else:
            st.warning("A expressão está vazia.")

    # Criação de linhas de botões
    def create_button_row(symbols):
        cols = st.columns(len(symbols))
        for i, symbol in enumerate(symbols):
            with cols[i]:
                if symbol == "Limpar":
                    st.button("Limpar", on_click=lambda: st.session_state.update({"expression": ""}))
                elif symbol == "←":
                    st.button("←", on_click=lambda: st.session_state.update({"expression": st.session_state["expression"][:-1]}))
                elif symbol == "Gerar Tabela":
                    st.button("Gerar Tabela", key="generate", on_click=generate_table)
                elif symbol:
                    st.button(symbol, on_click=add_symbol, args=(symbol,))

    # Botões
    create_button_row(["(", ")", "Limpar", "←"])
    create_button_row(["a", "b", "c", "!"])
    create_button_row(["->", "<->", "^", "v"])
    create_button_row(["1", "0", "", "Gerar Tabela"])

    # Resultados
    if st.session_state["output_df"] is not None:
        st.subheader("Tabela Verdade")
        st.table(st.session_state["output_df"])
        st.success(f"**Classificação**: {st.session_state['output_classificacao']}")

    if st.session_state["output_error"]:
        st.error(f"Erro ao processar a expressão: {st.session_state['output_error']}")

if __name__ == "__main__":
    main()
