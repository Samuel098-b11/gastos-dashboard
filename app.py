import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Análise de Gastos Pessoais", layout="wide")

st.title("💸 Análise de Gastos Pessoais")

st.markdown("""
Faça upload de um arquivo `.csv` com os seus gastos.  
O arquivo deve conter as colunas: **Data, Categoria, Descrição, Valor**
""")

# Upload do arquivo
uploaded_file = st.file_uploader("Escolha seu arquivo CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=['Data'])
    df['AnoMes'] = df['Data'].dt.to_period('M').astype(str)

    st.subheader("📊 Tabela de Gastos")
    st.dataframe(df)

    # Filtros
    categorias = df['Categoria'].unique()
    categoria_selecionada = st.multiselect("Filtrar por Categoria", categorias, default=categorias)
    df_filtrado = df[df['Categoria'].isin(categoria_selecionada)]

    st.subheader("💰 Gastos por Categoria")
    gasto_categoria = df_filtrado.groupby('Categoria')['Valor'].sum().reset_index()
    fig_pizza = px.pie(gasto_categoria, names='Categoria', values='Valor', title='Distribuição dos Gastos')
    st.plotly_chart(fig_pizza, use_container_width=True)

    st.subheader("📈 Evolução Mensal dos Gastos")
    gasto_mes = df_filtrado.groupby('AnoMes')['Valor'].sum().reset_index()
    fig_linha = px.line(gasto_mes, x='AnoMes', y='Valor', markers=True, title='Gastos por Mês')
    st.plotly_chart(fig_linha, use_container_width=True)

    st.subheader("📌 Resumo Rápido")
    total = df_filtrado['Valor'].sum()
    media = df_filtrado.groupby('AnoMes')['Valor'].sum().mean()
    maior_categoria = gasto_categoria.sort_values(by='Valor', ascending=False).iloc[0]

    st.markdown(f"""
    - **Total gasto:** R$ {total:.2f}  
    - **Média mensal:** R$ {media:.2f}  
    - **Categoria com maior gasto:** {maior_categoria['Categoria']} (R$ {maior_categoria['Valor']:.2f})
    """)
else:
    st.info("Envie um arquivo CSV para começar.")
