import streamlit as st
import pandas as pd
import plotly.express as px
from db import init_db, inserir_transacao, obter_transacoes, atualizar_transacao, obter_transacao_por_id

# Inicializa o banco de dados
init_db()

# Menu lateral
menu = st.sidebar.selectbox("Menu", ["Cadastro", "Visualização", "Edição", "Gráficos"])

# Cadastro de transações
if menu == "Cadastro":
    st.header("Cadastro de Transações")
    with st.form("form_cadastro"):
        data = st.date_input("Data")
        categoria = st.text_input("Categoria")
        descricao = st.text_input("Descrição")
        tipo = st.selectbox("Tipo", ["Entrada", "Saída"])
        valor = st.number_input("Valor", format="%.2f")
        submit = st.form_submit_button("Salvar")
        
        if submit:
            inserir_transacao(data, categoria, descricao, tipo, valor)
            st.success("Transação cadastrada com sucesso!")

# Visualização de transações
elif menu == "Visualização":
    st.header("Transações Cadastradas")
    transacoes = obter_transacoes()
    if transacoes:
        df = pd.DataFrame(transacoes, columns=["ID", "Data", "Categoria", "Descrição", "Tipo", "Valor"])
        st.dataframe(df)
    else:
        st.warning("Nenhuma transação cadastrada.")

# Edição de transações
elif menu == "Edição":
    st.header("Editar Transações")
    transacoes = obter_transacoes()
    if transacoes:
        df = pd.DataFrame(transacoes, columns=["ID", "Data", "Categoria", "Descrição", "Tipo", "Valor"])
        transacao_id = st.selectbox("Selecione a transação para editar", df["ID"])
        transacao = obter_transacao_por_id(transacao_id)
        if transacao:
            with st.form("form_edicao"):
                data = st.date_input("Data", value=pd.to_datetime(transacao[1]))
                categoria = st.text_input("Categoria", value=transacao[2])
                descricao = st.text_input("Descrição", value=transacao[3])
                tipo = st.selectbox("Tipo", ["Entrada", "Saída"], index=0 if transacao[4] == "Entrada" else 1)
                valor = st.number_input("Valor", format="%.2f", value=transacao[5])
                submit = st.form_submit_button("Atualizar")

                if submit:
                    atualizar_transacao(transacao_id, data, categoria, descricao, tipo, valor)
                    st.success("Transação atualizada com sucesso!")
    else:
        st.warning("Nenhuma transação disponível para editar.")

# Gráficos
elif menu == "Gráficos":
    st.header("Gráficos de Gastos por Mês")
    transacoes = obter_transacoes()
    if transacoes:
        # Convertendo os dados para um DataFrame
        df = pd.DataFrame(transacoes, columns=["ID", "Data", "Categoria", "Descrição", "Tipo", "Valor"])
        
        # Transformando a coluna Data para datetime e extraindo o mês
        df['Data'] = pd.to_datetime(df['Data'])
        
        # Extraindo o nome do mês abreviado (Jan, Fev, Mar, etc.)
        df['Mês'] = df['Data'].dt.strftime('%b')  # Nome abreviado do mês
        
        # Adicionando uma coluna para indicar o tipo de transação (Entrada ou Saída)
        df_entrada = df[df['Tipo'] == "Entrada"]
        df_saida = df[df['Tipo'] == "Saída"]

        # Agrupando por mês e somando os valores
        df_entrada = df_entrada.groupby('Mês').agg({'Valor': 'sum'}).reset_index()
        df_entrada['Tipo'] = 'Entrada'
        
        df_saida = df_saida.groupby('Mês').agg({'Valor': 'sum'}).reset_index()
        df_saida['Tipo'] = 'Saída'
        
        # Unindo os dois DataFrames (Entrada e Saída)
        df_grafico = pd.concat([df_entrada, df_saida], ignore_index=True)
        
        # Calculando os totais de Entradas e Saídas
        total_entrada = df_entrada['Valor'].sum()
        total_saida = df_saida['Valor'].sum()

        # Exibindo os cartões de Entradas e Saídas com os totais
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
                <div style="background-color: green; padding: 10px; border-radius: 10px; color: white;">
                    <h3>Entradas</h3>
                    <p>R$ {total_entrada:,.2f}</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style="background-color: darkred; padding: 10px; border-radius: 10px; color: white;">
                    <h3>Saídas</h3>
                    <p>R$ {total_saida:,.2f}</p>
                </div>
            """, unsafe_allow_html=True)

        # Criando o gráfico com Plotly
        fig = px.bar(
            df_grafico,
            x="Mês",
            y="Valor",
            color="Tipo",
            barmode="group",  # Usando 'group' para separar as barras
            color_discrete_map={"Entrada": "green", "Saída": "darkred"},
            title="Gastos por Mês",
            labels={"Valor": "Valor (R$)", "Mês": "Mês"}
        )
        
        # Formatando os valores no eixo Y para o formato em reais (R$)
        fig.update_layout(
            yaxis_tickformat="R$,.2f",  # Formato em Reais (R$)
            xaxis_title="Mês",
            yaxis_title="Valor (R$)"
        )
        
        # Adicionando rótulos nas colunas do gráfico
        fig.update_traces(texttemplate='%{y:$.2f}', textposition='outside', showlegend=False)
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Nenhuma transação cadastrada para gerar gráficos.")
