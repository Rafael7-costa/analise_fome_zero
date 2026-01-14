import pandas as pd
import numpy as np
import streamlit as st
import folium
import inflection
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from PIL import Image

st.set_page_config(page_title="Página Principal",  page_icon='📊', layout="wide")

# ==============================================================================
# 1. Configurações Iniciais e Dicionários
# ==============================================================================


COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}

def country_name(country_id):
    COUNTRIES = {
        1: 'India', 14: 'Australia', 30: 'Brazil', 37: 'Canada', 94: 'Indonesia',
        148: 'New Zealand', 162: 'Philippines', 166: 'Qatar', 184: 'Singapore',
        189: 'South Africa', 191: 'Sri Lanka', 208: 'Turkey',
        214: 'United Arab Emirates', 215: 'United Kingdom', 216: 'United States'
    }
    return COUNTRIES.get(country_id, "Unknown")

def color_name(color_code):
    return COLORS.get(color_code, "gray")

# ==============================================================================
# 2. Processamento de Dados (Ajustado para 6.929 registros)
# ==============================================================================

def clean_code(df):
    df_processing = df.copy()
    
    # 1. Criação da coluna de Países
    df_processing['Country Name'] = df_processing['Country Code'].apply(country_name)
    
    # 2. Tratamento de Coordenadas (Divisão por 10^10 conforme solicitado)
    # Convertemos para string para garantir que o replace funcione em qualquer formato
    df_processing['Latitude'] = df_processing['Latitude'].astype(str).str.replace('.', '', regex=False).astype(float) / 10**10
    df_processing['Longitude'] = df_processing['Longitude'].astype(str).str.replace('.', '', regex=False).astype(float) / 10**10

    # 3. Limpeza de Strings (Remoção de espaços)
    for col in df_processing.select_dtypes(include=['object']).columns:
        df_processing[col] = df_processing[col].astype(str).str.strip()

    # 4. REMOÇÃO DE DUPLICADAS PELO ID (Essencial para chegar aos 6.929)
    df_processing = df_processing.drop_duplicates(subset='Restaurant ID', keep='first')

    # 5. Conversão de tipos
    binary_columns = ['Has Table booking', 'Has Online delivery', 'Is delivering now', 'Switch to order menu']
    for col in binary_columns:
        if col in df_processing.columns:
            df_processing[col] = df_processing[col].astype(bool)

    df_processing['Price range'] = df_processing['Price range'].astype('category')

    # Resetar o index
    df_final = df_processing.reset_index(drop=True)
    
    return df_final

def get_metrics(df_filtered):
    unique_restaurants = df_filtered['Restaurant ID'].nunique()
    unique_countries = df_filtered['Country Name'].nunique()
    unique_cities = df_filtered['City'].nunique()
    total_votes = df_filtered['Votes'].sum()
    # Tratamento para culinárias (evitando erros com valores vazios)
    unique_cuisine_types = df_filtered['Cuisines'].astype(str).str.split(', ').explode().nunique()
    
    return unique_restaurants, unique_countries, unique_cities, total_votes, unique_cuisine_types

# ==============================================================================
# 3. Função do Mapa Interativo
# ==============================================================================

def create_map(df_map):
    # Localização média para centralizar o mapa
    if not df_map.empty:
        m = folium.Map(location=[df_map['Latitude'].median(), df_map['Longitude'].median()], zoom_start=2)
    else:
        m = folium.Map(location=[0, 0], zoom_start=2)

    marker_cluster = MarkerCluster().add_to(m)

    for _, row in df_map.iterrows():
        icon_color = color_name(row['Rating color'])
        
        popup_content = f"""
            <div style="width: 200px">
                <b>{row['Restaurant Name']}</b><br>
                <i>{row['Cuisines']}</i><br><br>
                <b>Nota:</b> {row['Aggregate rating']} / 5.0<br>
                <b>Preço para dois:</b> {row['Average Cost for two']} ({row['Currency']})
            </div>
        """
        
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon(color=icon_color, icon='utensils', prefix='fa')
        ).add_to(marker_cluster)
    
    return m

# ==============================================================================
# 4. Execução do Dashboard
# ==============================================================================

# Carregamento do arquivo
try:
    # Ajuste o caminho conforme necessário
    df_raw = pd.read_csv('data_set/zomato.csv') 
    df = clean_code(df_raw)
except Exception as e:
    st.error(f"Erro ao carregar os dados. Verifique se o arquivo 'zomato.csv' está na pasta correta. Erro: {e}")
    st.stop()

# --- BARRA LATERAL (SIDEBAR) ---
col1, col2 = st.sidebar.columns([1, 4])
try:
    col1.image(Image.open('logo1.png'), width=100)
except:
    col1.warning("!")
col2.markdown("### Fome Zero")
st.sidebar.markdown("---")
st.sidebar.markdown("### Filtros")

# Filtro de Países
paises_lista = sorted(df['Country Name'].unique().tolist())
countries_selected = st.sidebar.multiselect(
    'Escolha os países para visualizar os restaurantes:',
    options=paises_lista,
    default=paises_lista # Começa com todos selecionados
)

# Filtro aplicado
df_filtered = df[df['Country Name'].isin(countries_selected)]

# Download dos dados tratados (Exatamente os 6.929 ou filtrados)
st.sidebar.markdown("---")
csv = df_filtered.to_csv(index=False).encode('utf-8')
st.sidebar.download_button("📥 Download CSV", data=csv, file_name='dados_tratados.csv', mime='text/csv')

# --- CONTEÚDO PRINCIPAL ---
st.title("📍 Fome Zero!")
st.subheader("O melhor lugar para encontrar seu novo restaurante favorito!")

# Métricas formatadas
res, countries, cities, votes, cuisines = get_metrics(df_filtered)
m1, m2, m3, m4, m5 = st.columns(5)

m1.metric("Restaurantes", f"{res:,}".replace(',', '.'))
m2.metric("Países", countries)
m3.metric("Cidades", cities)
m4.metric("Avaliações", f"{votes:,}".replace(',', '.'))
m5.metric("Culinárias", cuisines)

# MAPA
st.markdown("---")
st.subheader(f"Mapa de Restaurantes ({len(df_filtered)} exibidos)")

with st.container():
    mapa_interativo = create_map(df_filtered)
    folium_static(mapa_interativo, width=1200, height=600)