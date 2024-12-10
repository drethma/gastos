import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import calendar
from db import criar_tabela, adicionar_transacao, visualizar_transacoes, editar_transacao

# Inicializa o banco de dados
criar_tabela()

# Função auxiliar para filtrar dados por mês e ano
def filtrar_por_mes_ano(df, mes, ano):
    if mes != "Nenhum":
        # Converte o nome do mês para número (ex: 'Jan' -> 1)
        mes_numero = list(calendar.month_abbr).index(mes)
        df = df[df['Data'].dt.month == mes_numero]
    if ano != "Nenhum":
        df = df[df['Data'].dt.year == int(ano)]
    return df

# Função de cadastro
def cadastrar_transacao():
    st.header("➕ Cadastrar Transação")
    
    descricao = st.text_input("📝 Descrição")
    tipo = st.selectbox("🔄 Tipo", ["Entrada", "Saída"])
    categoria = st.text_input("📂 Categoria")
    valor = st.number_input("💰 Valor", min_value=0.0, step=0.01)
    data = st.date_input("📅 Data")
    
    if st.button("✅ Salvar"):
        if descricao and tipo and categoria and valor > 0:
            adicionar_transacao(descricao, tipo, categoria, valor, data)
            st.success("✅ Transação adicionada com sucesso!")
        else:
            st.error("⚠️ Por favor, preencha todos os campos.")

# Função de visualização com filtro
def visualizar_transacoes_func():
    st.header("📊 Visualizar Transações")
    dados = visualizar_transacoes()

    if dados:
        df = pd.DataFrame(dados, columns=["ID", "Descrição", "Tipo", "Categoria", "Valor", "Data"])
        df['Data'] = pd.to_datetime(df['Data'])

        # Filtros de mês e ano
        meses = ["Nenhum"] + list(calendar.month_abbr[1:])
        anos = ["Nenhum"] + sorted(df['Data'].dt.year.unique().astype(str))

        mes = st.selectbox("📅 Filtrar por Mês", meses)
        ano = st.selectbox("📆 Filtrar por Ano", anos)

        df_filtrado = filtrar_por_mes_ano(df, mes, ano)

        st.dataframe(df_filtrado)
    else:
        st.warning("⚠️ Nenhuma transação encontrada.")

# Função de gráfico com filtro
def grafico_entradas_saidas_mes():
    st.header("📈 Comparação de Entradas vs Saídas por Mês")
    dados = visualizar_transacoes()

    if dados:
        df = pd.DataFrame(dados, columns=["ID", "Descrição", "Tipo", "Categoria", "Valor", "Data"])
        df['Data'] = pd.to_datetime(df['Data'])
        df['Mês'] = df['Data'].dt.strftime("%b")
        df['Ano'] = df['Data'].dt.year

        # Filtros de mês e ano
        meses = ["Nenhum"] + list(df['Mês'].unique())
        anos = ["Nenhum"] + sorted(df['Ano'].astype(str).unique())

        mes = st.selectbox("📅 Filtrar por Mês", meses)
        ano = st.selectbox("📆 Filtrar por Ano", anos)

        df_filtrado = filtrar_por_mes_ano(df, mes, ano)

        if not df_filtrado.empty:
            resumo = df_filtrado.groupby(["Mês", "Tipo"])["Valor"].sum().unstack(fill_value=0)

            # Garantindo que os valores sejam listas para evitar erros
            entradas = resumo.get('Entrada', pd.Series(0, index=resumo.index)).tolist()
            saidas = resumo.get('Saída', pd.Series(0, index=resumo.index)).tolist()

            fig = go.Figure(data=[
                go.Bar(name='Entradas', x=resumo.index, y=entradas, marker_color='green'),
                go.Bar(name='Saídas', x=resumo.index, y=saidas, marker_color='red')
            ])

            fig.update_layout(
                title="Comparação de Entradas e Saídas por Mês",
                xaxis_title="Mês",
                yaxis_title="Valor (R$)",
                barmode='group'
            )

            st.plotly_chart(fig)
        else:
            st.warning("⚠️ Nenhuma transação encontrada para os filtros selecionados.")
    else:
        st.warning("⚠️ Nenhuma transação encontrada.")

# Função de edição de transações
def editar_transacoes():
    st.header("✏️ Editar Transações")
    
    # Carrega as transações para edição
    dados = visualizar_transacoes()

    if dados:
        df = pd.DataFrame(dados, columns=["ID", "Descrição", "Tipo", "Categoria", "Valor", "Data"])
        df['Data'] = pd.to_datetime(df['Data'])

        # Filtros de mês e ano
        meses = ["Nenhum"] + list(calendar.month_abbr[1:])
        anos = ["Nenhum"] + sorted(df['Data'].dt.year.unique().astype(str))

        mes = st.selectbox("📅 Filtrar por Mês", meses)
        ano = st.selectbox("📆 Filtrar por Ano", anos)

        df_filtrado = filtrar_por_mes_ano(df, mes, ano)

        # Seleção da transação a ser editada
        transacao_id = st.selectbox("📝 Selecione a transação para editar", df_filtrado["ID"].tolist())

        # Carrega a transação selecionada
        transacao = df_filtrado[df_filtrado["ID"] == transacao_id].iloc[0]

        descricao = st.text_input("📝 Descrição", transacao["Descrição"])
        tipo = st.selectbox("🔄 Tipo", ["Entrada", "Saída"], index=["Entrada", "Saída"].index(transacao["Tipo"]))
        categoria = st.text_input("📂 Categoria", transacao["Categoria"])
        valor = st.number_input("💰 Valor", min_value=0.0, step=0.01, value=transacao["Valor"])
        data = st.date_input("📅 Data", value=transacao["Data"])

        if st.button("✅ Atualizar"):
            editar_transacao(transacao_id, descricao, tipo, categoria, valor, data)
            st.success("✅ Transação atualizada com sucesso!")
        else:
            st.warning("⚠️ Não foram feitas alterações.")
    else:
        st.warning("⚠️ Nenhuma transação encontrada.")

# Sidebar com menu suspenso
st.sidebar.title("💼 Menu")
menu = st.sidebar.selectbox(
    "Escolha uma opção:",
    ["🏠 Home", "➕ Cadastrar Transação", "📊 Visualizar Transações", "✏️ Editar Transações", "📈 Gráfico Entradas vs Saídas por Mês"]
)

# Exibição de acordo com a opção selecionada na sidebar
if menu == "🏠 Home":
    st.title("🏠 Bem-vindo ao Controle de Gastos")
elif menu == "➕ Cadastrar Transação":
    cadastrar_transacao()
elif menu == "📊 Visualizar Transações":
    visualizar_transacoes_func()
elif menu == "✏️ Editar Transações":
    editar_transacoes()
elif menu == "📈 Gráfico Entradas vs Saídas por Mês":
    grafico_entradas_saidas_mes()
