import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Visão Países", page_icon='🌎', layout="wide")

# ==============================================================================
# Funções de Processamento
# ==============================================================================

def country_name(country_id):
    COUNTRIES = {
        1: 'India', 14: 'Australia', 30: 'Brazil', 37: 'Canada', 94: 'Indonesia',
        148: 'New Zealand', 162: 'Philippines', 166: 'Qatar', 184: 'Singapore',
        189: 'South Africa', 191: 'Sri Lanka', 208: 'Turkey',
        214: 'United Arab Emirates', 215: 'United Kingdom', 216: 'United States'
    }
    return COUNTRIES.get(country_id)

def clean_code(df):
    df['Country Name'] = df['Country Code'].apply(country_name)
    df = df.dropna().copy()
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
    binary_columns = ['Has Table booking', 'Has Online delivery', 'Is delivering now', 'Switch to order menu']
    for col in binary_columns:
        df[col] = df[col].astype(bool)
    df = df.drop_duplicates()
    return df

# ==============================================================================
# Funções de Visualização (Otimização)
# ==============================================================================

def create_bar_chart(df, x_val, y_val, title, color, text_format='.2s'):
    """Cria um gráfico de barras padronizado para o dashboard."""
    fig = px.bar(
        df, x=x_val, y=y_val, text=y_val,
        labels={x_val: 'País', y_val: title},
        color_discrete_sequence=[color]
    )
    fig.update_traces(textposition='outside', texttemplate='%{text:' + text_format + '}')
    fig.update_layout(xaxis_title=None, yaxis_title=None, showlegend=False, margin=dict(t=30, b=0))
    return fig

# ==============================================================================
# Processamento de Dados
# ==============================================================================
try:
    df_raw = pd.read_csv('data_set/zomato.csv')
    df = clean_code(df_raw)
except FileNotFoundError:
    st.error("Arquivo 'zomato.csv' não encontrado.")
    st.stop()

# --- Sidebar ---
col1, col2 = st.sidebar.columns([1, 4])
try:
    col1.image(Image.open('logo1.png'), width=100)
except:
    col1.warning("!")
col2.markdown("### Fome Zero")

st.sidebar.markdown("## Filtros")
paises_lista = df['Country Name'].unique().tolist()
countries_selected = st.sidebar.multiselect('Escolha os países que deseja visualizar os restaurantes', options=paises_lista, default=['Brazil', 'Canada', 'Australia', 'Qatar'])
df_filtered = df[df['Country Name'].isin(countries_selected)]

# ... (Mantenha suas funções de processamento e visualização iguais)

# ==============================================================================
# Layout Principal
# ==============================================================================
st.title("🌎 Visão Países")
tab1, tab2 = st.tabs(["Visão Geral", "Avaliações & Preços"])

with tab1:
    # 1. Cidades
    st.subheader("Cidades Registradas por País")
    df_aux = df_filtered.groupby('Country Name')['City'].nunique().sort_values(ascending=False).reset_index()
    st.plotly_chart(create_bar_chart(df_aux, 'Country Name', 'City', 'Cidades', '#2C3E50', '.0f'), use_container_width=True)
    if not df_aux.empty:
        st.info(f"📍 **Destaque:** {df_aux.iloc[0]['Country Name']} possui a maior capilaridade com {df_aux.iloc[0]['City']} cidades registradas.")

    # 2. Restaurantes
    st.subheader("Restaurantes Registrados por País")
    df_rest = df_filtered.groupby('Country Name')['Restaurant ID'].nunique().sort_values(ascending=False).reset_index()
    st.plotly_chart(create_bar_chart(df_rest, 'Country Name', 'Restaurant ID', 'Restaurantes', '#E67E22', '.0f'), use_container_width=True)
    if not df_rest.empty:
        st.success(f"🍴 **Presença:** {df_rest.iloc[0]['Country Name']} lidera em volume com {df_rest.iloc[0]['Restaurant ID']:,} estabelecimentos cadastrados.")

    # 3. Serviços Lado a Lado
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.write("### Restaurantes que Entregam Agora")
        df_del = df_filtered[df_filtered['Is delivering now']].groupby('Country Name')['Restaurant ID'].nunique().sort_values(ascending=False).reset_index()
        st.plotly_chart(create_bar_chart(df_del, 'Country Name', 'Restaurant ID', 'Entrega', '#E74C3C', '.0f'), use_container_width=True)
        if not df_del.empty:
            st.info(f"🚀 {df_del.iloc[0]['Country Name']} tem a frota mais ativa ({df_del.iloc[0]['Restaurant ID']} entregando).")
    
    with c2:
        st.write("### Restaurantes com Reserva de Mesa")
        df_res = df_filtered[df_filtered['Has Table booking']].groupby('Country Name')['Restaurant ID'].nunique().sort_values(ascending=False).reset_index()
        st.plotly_chart(create_bar_chart(df_res, 'Country Name', 'Restaurant ID', 'Reserva', '#8E44AD', '.0f'), use_container_width=True)
        if not df_res.empty:
            st.info(f"📅 {df_res.iloc[0]['Country Name']} é o melhor para planejar ({df_res.iloc[0]['Restaurant ID']} aceitam reserva).")

    # 4. Culinárias
    st.subheader("Tipos de Culinária por País")
    df_cui_dist = df_filtered.copy()
    df_cui_dist['Cuisines'] = df_cui_dist['Cuisines'].str.split(', ')
    df_cui_dist = df_cui_dist.explode('Cuisines').groupby('Country Name')['Cuisines'].nunique().sort_values(ascending=False).reset_index()
    st.plotly_chart(create_bar_chart(df_cui_dist, 'Country Name', 'Cuisines', 'Culinárias', '#27AE60', '.0f'), use_container_width=True)
    if not df_cui_dist.empty:
        st.success(f"🍲 **Diversidade:** {df_cui_dist.iloc[0]['Country Name']} oferece a maior variedade gastronômica ({df_cui_dist.iloc[0]['Cuisines']} tipos).")

with tab2:
    # 1. Votos
    st.subheader("Total de Avaliações por País")
    df_votes = df_filtered.groupby('Country Name')['Votes'].sum().sort_values(ascending=False).reset_index()
    st.plotly_chart(create_bar_chart(df_votes, 'Country Name', 'Votes', 'Votos', '#3498DB', '.2s'), use_container_width=True)
    if not df_votes.empty:
        st.info(f"🗳️ **Engajamento:** {df_votes.iloc[0]['Country Name']} é o país mais avaliado pelos usuários ({df_votes.iloc[0]['Votes']:,} votos).")

    # 2. Notas Lado a Lado
    st.markdown("---")
    col_nota1, col_nota2 = st.columns(2)
    df_rate_base = df_filtered.groupby('Country Name')['Aggregate rating'].mean().reset_index()
    
    with col_nota1:
        st.write("### Top Maiores Avaliações Médias")
        df_top = df_rate_base.sort_values('Aggregate rating', ascending=False).head(10)
        st.plotly_chart(create_bar_chart(df_top, 'Country Name', 'Aggregate rating', 'Nota', '#27AE60', '.2f'), use_container_width=True)
        if not df_top.empty:
            st.success(f"🥇 **Campeão de Qualidade:** {df_top.iloc[0]['Country Name']} ({df_top.iloc[0]['Aggregate rating']:.2f})")

    with col_nota2:
        st.write("### Top Menores Avaliações Médias")
        df_low = df_rate_base.sort_values('Aggregate rating', ascending=True).head(10)
        st.plotly_chart(create_bar_chart(df_low, 'Country Name', 'Aggregate rating', 'Nota', '#C0392B', '.2f'), use_container_width=True)
        if not df_low.empty:
            st.error(f"⚠️ **Ponto de Atenção:** {df_low.iloc[0]['Country Name']} ({df_low.iloc[0]['Aggregate rating']:.2f})")

    # 3. Economia Lado a Lado
    st.markdown("---")
    st.subheader("Preço por País")
    ce1, ce2 = st.columns(2)
    with ce1:
        st.write("### Qtd. de Restaurantes Luxo (Nível 4)")
        df_p4 = df_filtered[df_filtered['Price range'] == 4].groupby('Country Name')['Restaurant ID'].nunique().sort_values(ascending=False).reset_index()
        st.plotly_chart(create_bar_chart(df_p4, 'Country Name', 'Restaurant ID', 'Qtd.', '#1ABC9C', '.0f'), use_container_width=True)
        if not df_p4.empty:
            st.info(f"💎 {df_p4.iloc[0]['Country Name']} lidera o mercado de alto padrão ({df_p4.iloc[0]['Restaurant ID']} opções).")
            
    with ce2:
        st.write("### Média de Preço para Dois")
        df_cost = df_filtered.groupby('Country Name')['Average Cost for two'].mean().sort_values(ascending=False).reset_index()
        st.plotly_chart(create_bar_chart(df_cost, 'Country Name', 'Average Cost for two', 'Preço', '#34495E', '.2f'), use_container_width=True)
        if not df_cost.empty:
            st.warning(f"💸 **Custo Médio:** {df_cost.iloc[0]['Country Name']} possui o prato para dois mais caro ({df_cost.iloc[0]['Average Cost for two']:.2f}).")














