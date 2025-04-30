import streamlit as st
import pandas as pd
import os
from datetime import date

# 📁 Arquivos dos módulos
ARQUIVOS = {
    'produtos': 'produtos.csv',
    'clientes': 'clientes.csv',
    'vendas': 'vendas.csv',
    'financeiro': 'financeiro.csv'
}

# 🧰 Funções utilitárias
def inicializar_arquivos():
    if not os.path.exists(ARQUIVOS['produtos']):
        pd.DataFrame(columns=['ID', 'Nome', 'Categoria', 'Preço', 'Estoque']).to_csv(ARQUIVOS['produtos'], index=False)
    if not os.path.exists(ARQUIVOS['clientes']):
        pd.DataFrame(columns=['ID', 'Nome', 'Email', 'Telefone']).to_csv(ARQUIVOS['clientes'], index=False)
    if not os.path.exists(ARQUIVOS['vendas']):
        pd.DataFrame(columns=['ID', 'Cliente', 'Produto', 'Data', 'Valor']).to_csv(ARQUIVOS['vendas'], index=False)
    if not os.path.exists(ARQUIVOS['financeiro']):
        pd.DataFrame(columns=['ID', 'Tipo', 'Descrição', 'Data', 'Valor']).to_csv(ARQUIVOS['financeiro'], index=False)

def carregar_dados(tipo):
    return pd.read_csv(ARQUIVOS[tipo])

def salvar_dados(tipo, df):
    df.to_csv(ARQUIVOS[tipo], index=False)

def gerar_id(df):
    if df.empty:
        return 1
    return int(df['ID'].max()) + 1

# 🧱 Módulos
def modulo_produtos():
    st.subheader("📦 Gestão de Produtos")
    df = carregar_dados('produtos')

    with st.expander("➕ Adicionar Produto"):
        nome = st.text_input("Nome do Produto")
        categoria = st.text_input("Categoria")
        preco = st.number_input("Preço", min_value=0.0)
        estoque = st.number_input("Estoque", min_value=0)
        if st.button("Salvar Produto"):
            novo = pd.DataFrame([{
                'ID': gerar_id(df),
                'Nome': nome,
                'Categoria': categoria,
                'Preço': preco,
                'Estoque': estoque
            }])
            df = pd.concat([df, novo], ignore_index=True)
            salvar_dados('produtos', df)
            st.success("✅ Produto cadastrado.")

    st.write("📋 Produtos cadastrados:")
    st.dataframe(df, use_container_width=True)

def modulo_clientes():
    st.subheader("👤 Cadastro de Clientes")
    df = carregar_dados('clientes')

    with st.expander("➕ Adicionar Cliente"):
        nome = st.text_input("Nome completo")
        email = st.text_input("Email")
        telefone = st.text_input("Telefone")
        if st.button("Salvar Cliente"):
            novo = pd.DataFrame([{
                'ID': gerar_id(df),
                'Nome': nome,
                'Email': email,
                'Telefone': telefone
            }])
            df = pd.concat([df, novo], ignore_index=True)
            salvar_dados('clientes', df)
            st.success("✅ Cliente cadastrado.")

    st.write("📋 Clientes:")
    st.dataframe(df, use_container_width=True)

def modulo_vendas():
    st.subheader("🛒 Registro de Vendas")
    produtos = carregar_dados('produtos')
    clientes = carregar_dados('clientes')
    vendas = carregar_dados('vendas')

    with st.expander("➕ Registrar Venda"):
        cliente = st.selectbox("Cliente", clientes['Nome'] if not clientes.empty else [])
        produto = st.selectbox("Produto", produtos['Nome'] if not produtos.empty else [])
        valor = st.number_input("Valor da venda", min_value=0.0)
        data_venda = st.date_input("Data da venda", value=date.today())
        if st.button("Registrar Venda"):
            nova = pd.DataFrame([{
                'ID': gerar_id(vendas),
                'Cliente': cliente,
                'Produto': produto,
                'Data': data_venda,
                'Valor': valor
            }])
            vendas = pd.concat([vendas, nova], ignore_index=True)
            salvar_dados('vendas', vendas)
            st.success("✅ Venda registrada.")

    st.write("📋 Vendas realizadas:")
    st.dataframe(vendas, use_container_width=True)

def modulo_financeiro():
    st.subheader("💰 Controle Financeiro")
    df = carregar_dados('financeiro')

    with st.expander("➕ Nova Transação"):
        tipo = st.selectbox("Tipo", ["Entrada", "Saída"])
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor", min_value=0.0)
        data_trans = st.date_input("Data", value=date.today())
        if st.button("Salvar Transação"):
            nova = pd.DataFrame([{
                'ID': gerar_id(df),
                'Tipo': tipo,
                'Descrição': descricao,
                'Data': data_trans,
                'Valor': valor
            }])
            df = pd.concat([df, nova], ignore_index=True)
            salvar_dados('financeiro', df)
            st.success("✅ Transação salva.")

    st.write("📋 Registro Financeiro:")
    st.dataframe(df, use_container_width=True)

def modulo_dashboard():
    st.subheader("📈 Dashboard")
    vendas = carregar_dados('vendas')
    financeiro = carregar_dados('financeiro')

    total_vendas = vendas['Valor'].sum() if not vendas.empty else 0
    entradas = financeiro[financeiro['Tipo'] == 'Entrada']['Valor'].sum() if not financeiro.empty else 0
    saidas = financeiro[financeiro['Tipo'] == 'Saída']['Valor'].sum() if not financeiro.empty else 0
    saldo = entradas - saidas

    col1, col2, col3 = st.columns(3)
    col1.metric("🛒 Total em Vendas", f"R$ {total_vendas:,.2f}")
    col2.metric("💰 Entradas", f"R$ {entradas:,.2f}")
    col3.metric("💸 Saídas", f"R$ {saidas:,.2f}")

    st.info(f"📊 **Saldo atual:** R$ {saldo:,.2f}")

# 🚀 App principal
def main():
    st.set_page_config(page_title="ERP Streamlit", layout="wide")
    st.title("🧩 Mini ERP - Gestão Empresarial Integrada")
    inicializar_arquivos()

    menu = st.sidebar.selectbox("Módulos", [
        "📦 Produtos",
        "👤 Clientes",
        "🛒 Vendas",
        "💰 Financeiro",
        "📈 Dashboard"
    ])

    if menu == "📦 Produtos":
        modulo_produtos()
    elif menu == "👤 Clientes":
        modulo_clientes()
    elif menu == "🛒 Vendas":
        modulo_vendas()
    elif menu == "💰 Financeiro":
        modulo_financeiro()
    elif menu == "📈 Dashboard":
        modulo_dashboard()

if __name__ == "__main__":
    main()
