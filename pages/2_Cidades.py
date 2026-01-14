import pandas as pd
import streamlit as st
from PIL import Image
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Visão Cidades", page_icon='🏙️', layout="wide")

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

def create_bar_chart(df, x_val, y_val, label_y, text_format='.2s', color_col='Country Name'):
    """
    Cria um gráfico de barras com legenda por país.
    """
    fig = px.bar(
        df, 
        x=x_val, 
        y=y_val, 
        color=color_col, 
        text=y_val,
        labels={x_val: 'Cidade', y_val: label_y, color_col: 'País'},
        color_discrete_sequence=px.colors.qualitative.Safe 
    )
    
    fig.update_traces(textposition='outside', texttemplate='%{text:' + text_format + '}')
    fig.update_layout(
        xaxis_title=None, 
        yaxis_title=None, 
        legend_title_text='País',
        margin=dict(t=30, b=0)
    )
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

# ==============================================================================
# Layout Principal
# ==============================================================================
st.title("🏙️ Visão Cidades")

# --- BLOCO 1: Volume Geral ---
st.subheader("Top 10 Cidades com Mais Restaurantes")
df_city_rest = (df_filtered.groupby(['City', 'Country Name'])['Restaurant ID']
                           .nunique().sort_values(ascending=False).reset_index().head(10))

st.plotly_chart(create_bar_chart(df_city_rest, 'City', 'Restaurant ID', 'Qtd Restaurantes', '.0f'), use_container_width=True)

if not df_city_rest.empty:
    top = df_city_rest.iloc[0]
    st.info(f"🏙️ **Destaque de Volume:** A cidade de **{top['City']} ({top['Country Name']})** é o maior polo gastronômico atual com **{top['Restaurant ID']}** estabelecimentos.")

# --- BLOCO 2: Qualidade (Lado a Lado) ---
st.markdown("---")
st.subheader("Cidades em Destaque: Qualidade das Avaliações")
col1, col2 = st.columns(2)

with col1:
    st.write("### Cidades com Notas Altas (> 4)")
    df_high = (df_filtered[df_filtered['Aggregate rating'] > 4]
               .groupby(['City', 'Country Name'])['Restaurant ID']
               .nunique().sort_values(ascending=False).reset_index().head(10))
    st.plotly_chart(create_bar_chart(df_high, 'City', 'Restaurant ID', 'Restaurantes > 4', '.0f'), use_container_width=True)
    if not df_high.empty:
        st.success(f"🌟 **Excelência:** **{df_high.iloc[0]['City']}** lidera o ranking de qualidade com **{df_high.iloc[0]['Restaurant ID']}** restaurantes nota 4+.")

with col2:
    st.write("### Cidades com Notas Baixas (< 2.5)")
    df_low = (df_filtered[df_filtered['Aggregate rating'] < 2.5]
              .groupby(['City', 'Country Name'])['Restaurant ID']
              .nunique().sort_values(ascending=False).reset_index().head(10))
    st.plotly_chart(create_bar_chart(df_low, 'City', 'Restaurant ID', 'Restaurantes < 2.5', '.0f'), use_container_width=True)
    if not df_low.empty:
        st.error(f"⚠️ **Atenção:** **{df_low.iloc[0]['City']}** possui a maior concentração de avaliações críticas (**{df_low.iloc[0]['Restaurant ID']}** locais).")

# --- BLOCO 3: Financeiro e Diversidade ---
st.markdown("---")
st.subheader("Diversidade e Serviços por Cidade")        
col3, col4 = st.columns(2)

with col3:
    st.write("### Cidades com Maior Preço Médio (Prato para dois)")
    df_price = (df_filtered.groupby(['City', 'Country Name'])['Average Cost for two']
                .mean().sort_values(ascending=False).reset_index().head(10))
    st.plotly_chart(create_bar_chart(df_price, 'City', 'Average Cost for two', 'Preço Médio', '.2f'), use_container_width=True)
    if not df_price.empty:
        st.warning(f"💰 **Mercado de Luxo:** **{df_price.iloc[0]['City']}** apresenta o maior ticket médio: **{df_price.iloc[0]['Average Cost for two']:.2f}** (moeda local).")

with col4:
    st.write("### Cidades com Maior Diversidade Culinária")
    df_diverse = df_filtered.copy()
    df_diverse['Cuisines'] = df_diverse['Cuisines'].str.split(', ')
    df_diverse = df_diverse.explode('Cuisines').groupby(['City', 'Country Name'])['Cuisines'].nunique().sort_values(ascending=False).reset_index().head(10)
    st.plotly_chart(create_bar_chart(df_diverse, 'City', 'Cuisines', 'Tipos de Culinária', '.0f'), use_container_width=True)
    if not df_diverse.empty:
        st.info(f"🎨 **Mix Gastronômico:** **{df_diverse.iloc[0]['City']}** é a mais diversa, oferecendo **{df_diverse.iloc[0]['Cuisines']}** tipos diferentes de culinária.")

# --- BLOCO 4: Logística e Serviços (Três Colunas) ---
st.markdown("---")
st.subheader("Logística e Serviços por Cidade")

col_serv1, col_serv2, col_serv3 = st.columns(3)

with col_serv1:
    st.write("### Cidades com Entregas Ativas")
    df_deliv_now = (df_filtered[df_filtered['Is delivering now']]
                    .groupby(['City', 'Country Name'])['Restaurant ID']
                    .nunique().sort_values(ascending=False).reset_index().head(7))
    st.plotly_chart(create_bar_chart(df_deliv_now, 'City', 'Restaurant ID', 'Entregas', '.0f'), use_container_width=True)
    if not df_deliv_now.empty:
        st.caption(f"🚀 **{df_deliv_now.iloc[0]['City']}** é a mais ágil em delivery.")

with col_serv2:
    st.write("### Cidades com Pedidos Online")
    df_online = (df_filtered[df_filtered['Has Online delivery']]
                 .groupby(['City', 'Country Name'])['Restaurant ID']
                 .nunique().sort_values(ascending=False).reset_index().head(7))
    st.plotly_chart(create_bar_chart(df_online, 'City', 'Restaurant ID', 'Online', '.0f'), use_container_width=True)
    if not df_online.empty:
        st.caption(f"📱 **{df_online.iloc[0]['City']}** lidera pedidos via App.")

with col_serv3:
    st.write("### Cidades com Reservas de Mesa")
    df_book = (df_filtered[df_filtered['Has Table booking']]
               .groupby(['City', 'Country Name'])['Restaurant ID']
               .nunique().sort_values(ascending=False).reset_index().head(7))
    st.plotly_chart(create_bar_chart(df_book, 'City', 'Restaurant ID', 'Reservas', '.0f'), use_container_width=True)
    if not df_book.empty:
        st.caption(f"📅 **{df_book.iloc[0]['City']}** tem mais opções de reserva.")

# Insight Final Consolidado
st.markdown("---")
if not df_deliv_now.empty and not df_online.empty and not df_book.empty:
    st.info(f"💡 **Conclusão:** Observamos que **{df_deliv_now.iloc[0]['City']}** domina a logística de entregas, enquanto **{df_diverse.iloc[0]['City']}** se destaca pela variedade de sabores disponível.")









