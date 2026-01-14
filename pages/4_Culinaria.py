import pandas as pd
import streamlit as st
from PIL import Image
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Visão Culinária", page_icon='👨‍🍳',layout="wide")

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

def get_processed_cuisines(df):
    """Separa as culinárias por vírgula e cria uma linha individual para cada uma 🔪"""
    df_exploded = df.copy()
    df_exploded['Cuisines'] = df_exploded['Cuisines'].str.split(', ')
    df_exploded = df_exploded.explode('Cuisines')
    return df_exploded

# ==============================================================================
# Funções de Visualização
# ==============================================================================

def get_extreme_metrics_by_cuisine(df, cuisine_name):
    """Função genérica para extrair melhor/pior restaurante por tipo de culinária"""
    # Usamos o df_filtered original aqui pois o filtro de texto resolve
    df_c = df[df['Cuisines'].str.contains(cuisine_name, case=False, na=False)].copy()
    if df_c.empty:
        return None, None
    best = df_c.sort_values(by='Aggregate rating', ascending=False).iloc[0]
    df_low = df_c[df_c['Votes'] > 0]
    worst = df_low.sort_values(by='Aggregate rating', ascending=True).iloc[0] if not df_low.empty else None
    return best, worst

def plot_expensive_cuisines(df):
    """Gera gráfico das 10 culinárias individuais com maior custo médio 💰"""
    df_cuisines = get_processed_cuisines(df)
    df_price = (df_cuisines.groupby('Cuisines')['Average Cost for two']
                          .mean().sort_values(ascending=False).reset_index().head(10))
    
    if df_price.empty: return None

    fig = px.bar(df_price, x='Average Cost for two', y='Cuisines', orientation='h',
                 text='Average Cost for two', title="Top 10 Culinárias mais Caras para Duas Pessoas",
                 labels={'Average Cost for two': 'Custo Médio', 'Cuisines': 'Culinária'},
                 color='Average Cost for two', color_continuous_scale='Reds')
    
    fig.update_traces(texttemplate='%{text:,.2f}', textposition='outside')
    fig.update_layout(yaxis={'categoryorder': 'total ascending'}, xaxis_title="Custo Médio (Moeda Local)", yaxis_title=None)
    return fig

def plot_cuisine_ratings(df, top=True):
    """Gera gráfico vertical das 10 melhores ou piores culinárias individuais ⭐"""
    df_cuisines = get_processed_cuisines(df)
    
    # Filtro de relevância: apenas culinárias com mais de 5 restaurantes
    counts = df_cuisines['Cuisines'].value_counts()
    valid = counts[counts > 5].index
    df_cuisines = df_cuisines[df_cuisines['Cuisines'].isin(valid)]
    
    if not top:
        df_cuisines = df_cuisines[df_cuisines['Votes'] > 0]

    df_plot = (df_cuisines.groupby('Cuisines')['Aggregate rating']
                          .mean().sort_values(ascending=not top).reset_index().head(10))
    
    if df_plot.empty: return None

    color_scale = 'Viridis' if top else 'Reds_r'
    title = "Top 10 Culinárias com Melhores Notas" if top else "Top 10 Culinárias com Menores Notas"

    fig = px.bar(df_plot, x='Cuisines', y='Aggregate rating', text='Aggregate rating',
                 title=title, labels={'Aggregate rating': 'Nota Média', 'Cuisines': 'Culinária'},
                 color='Aggregate rating', color_continuous_scale=color_scale)
    
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(xaxis_tickangle=-45, yaxis_range=[0, 5.5], xaxis_title=None, showlegend=False)
    return fig


def plot_online_delivery_cuisines(df):
    """Gera gráfico das culinárias com maior volume de entrega online ativa 🚚"""
    # 1. Filtro inicial: Aceita pedido online E está entregando agora
    df_delivery = df[(df['Has Online delivery'] == True) & (df['Is delivering now'] == True)].copy()
    
    if df_delivery.empty:
        return None

    # 2. Processamento das culinárias individuais (Explode)
    df_exploded = get_processed_cuisines(df_delivery)
    
    # 3. Contagem por tipo de culinária
    df_counts = (df_exploded['Cuisines'].value_counts()
                                        .reset_index()
                                        .rename(columns={'count': 'Quantidade'})
                                        .head(10))
    
    # 4. Criação do Gráfico
    fig = px.bar(
        df_counts,
        x='Quantidade',
        y='Cuisines',
        orientation='h',
        text='Quantidade',
        title="Top 10 Culinárias com Maior Disponibilidade de Entrega Online",
        labels={'Quantidade': 'Número de Restaurantes', 'Cuisines': 'Culinária'},
        color='Quantidade',
        color_continuous_scale='GnBu' # Tons de verde/azul para serviço
    )
    
    fig.update_traces(textposition='outside')
    fig.update_layout(yaxis={'categoryorder': 'total ascending'}, showlegend=False)
    
    return fig

# 1. Preparar a lista de culinárias únicas (com cache para não pesar o app)
@st.cache_data
def get_cuisines(df):
    return sorted(df['Cuisines'].str.split(', ').explode().dropna().unique().tolist())
# ==============================================================================
# Processamento de Dados
# ==============================================================================
try:
    df_raw = pd.read_csv('data_set/zomato.csv')
    df = clean_code(df_raw)
except FileNotFoundError:
    st.error("Arquivo 'zomato.csv' não encontrado.")
    st.stop()


# --- BLOCO DA SIDEBAR ---
# Filtro de Países (o que você já tinha)
col1, col2 = st.sidebar.columns([1, 4])
try:
    col1.image(Image.open('logo1.png'), width=100)
except:
    col1.warning("!")
col2.markdown("### Fome Zero")

st.sidebar.markdown("## Filtros")
st.sidebar.markdown("---")
paises_lista = df['Country Name'].unique().tolist()
countries_selected = st.sidebar.multiselect(
    'Escolha os países que deseja visualizar os restaurantes', 
    options=paises_lista, 
    default=['Brazil', 'Canada', 'Australia', 'Qatar']
)

# Filtro de Culinárias (Novo)
st.sidebar.markdown("---")
culinarias_lista = get_cuisines(df)
cuisines_selected = st.sidebar.multiselect(
    'Escolha os tipos de culinária que deseja visualizar', 
    options=culinarias_lista,
    default=[ 'Italian','American', 'Arabian','Japanese','Home-made','BBQ','Brazilian'] # Começa vazio ou coloque as culinárias padrão
)

# --- APLICAÇÃO DOS FILTROS ---
# Primeiro filtra por país
df_filtered = df[df['Country Name'].isin(countries_selected)]

# Depois filtra por culinária (se houver alguma selecionada)
if cuisines_selected:
    search_set = set(cuisines_selected)
    df_filtered = df_filtered[df_filtered['Cuisines'].apply(
        lambda x: bool(search_set.intersection(set(x.split(', ')))) if isinstance(x, str) else False
    )]

# ==============================================================================
# Layout Principal 
# ==============================================================================
st.title("🔪🧂🍳🔥Visão Culinária")
tab_aval, tab_preco = st.tabs(["⭐ Avaliações por Culinária", "📊Visão Geral"])

# --- ABA 1: AVALIAÇÃO ---
with tab_aval:
    # Destaques em Cards (Utilizando função genérica para simplificar)
    cuisines_destaque = {
        "Italian": "🍝", "American": "🍔", "Arabian": "🥙", 
        "Japanese": "🍣", "Home-made": "🏠"
    }

    for name, emoji in cuisines_destaque.items():
        st.markdown(f"### {emoji} Performance: Culinária {name}")
        best, worst = get_extreme_metrics_by_cuisine(df_filtered, name)
        
        if best is not None:
            c1, c2 = st.columns(2)
            with c1:
                st.metric(f"🏆 Melhor {name}", best['Restaurant Name'], f"{best['Aggregate rating']}/5.0")
                st.caption(f"📍 {best['City']}, {best['Country Name']} | 💰 {best['Average Cost for two']:,} ({best['Currency']})")
            with c2:
                if worst is not None:
                    st.metric(f"📉 Menor Nota", worst['Restaurant Name'], f"{worst['Aggregate rating']}/5.0", delta_color="inverse")
                    st.caption(f"📍 {worst['City']}, {worst['Country Name']} | 💰 {worst['Average Cost for two']:,} ({worst['Currency']})")
        else:
            st.warning(f"Sem dados para {name} nos filtros selecionados.")
        st.markdown("---")

# --- ABA 2: PREÇO E RANKINGS ---
with tab_preco:
    # 1. Gráfico de Custos
    st.subheader("💰 Análise de Custo por Tipo de Cozinha")
    fig_price = plot_expensive_cuisines(df_filtered)
    if fig_price:
        st.plotly_chart(fig_price, use_container_width=True)
    # Abaixo do gráfico de barras horizontais de custo
    st.markdown("#### 💡 Insight de Posicionamento de Preço")
    df_exploded_p = get_processed_cuisines(df_filtered)
    avg_p = df_exploded_p.groupby('Cuisines')['Average Cost for two'].mean()
    
    if not avg_p.empty:
        top_c = avg_p.idxmax()
        top_v = avg_p.max()
        
        st.info(f"""
        * **Segmento de Luxo:** A culinária **{top_c}** apresenta o maior ticket médio (**{top_v:,.2f}** na moeda local). 
        * **Estratégia:** Restaurantes que operam nestas categorias precisam focar em exclusividade e serviços premium, pois o custo por cliente é significativamente superior à média global.
        """)
    
    # 2. Gráfico de Melhores Notas (Culinárias Individuais)
    st.subheader("⭐ Performance por Tipo de Culinária")
    fig_best = plot_cuisine_ratings(df_filtered, top=True)
    if fig_best:
        st.plotly_chart(fig_best, use_container_width=True)
    # Abaixo do gráfico de barras verticais das melhores notas
    st.markdown("#### 💡 Insight de Excelência Gastronômica")
    df_exploded_r = get_processed_cuisines(df_filtered)
    # Filtramos apenas culinárias com volume relevante para o insight
    counts = df_exploded_r['Cuisines'].value_counts()
    valid_cuisines = counts[counts > 5].index
    df_relevant = df_exploded_r[df_exploded_r['Cuisines'].isin(valid_cuisines)]
    
    if not df_relevant.empty:
        best_c = df_relevant.groupby('Cuisines')['Aggregate rating'].mean().idxmax()
        best_v = df_relevant.groupby('Cuisines')['Aggregate rating'].mean().max()
        
        st.success(f"""
        * **Padrão Ouro:** A culinária **{best_c}** lidera em satisfação do cliente com média de **{best_v:.2f}/5.0**. 
        * **Fidelização:** Categorias com notas acima de 4.5 indicam alta consistência na entrega. São ótimos nichos para observar boas práticas de atendimento e preparo.
        """)
    
    # 3. Gráfico de Piores Notas (Culinárias Individuais)
    st.markdown("---")
    st.subheader("📉 Baixa Performance por Tipo de Cozinha")
    fig_worst = plot_cuisine_ratings(df_filtered, top=False)
    if fig_worst:
        st.plotly_chart(fig_worst, use_container_width=True)
    # Abaixo do gráfico de barras verticais das menores notas
    st.markdown("#### 💡 Insight de Oportunidade e Risco")
    df_exploded_w = get_processed_cuisines(df_filtered)
    df_voted = df_exploded_w[df_exploded_w['Votes'] > 0]
    avg_w = df_voted.groupby('Cuisines')['Aggregate rating'].mean()
    
    if not avg_w.empty:
        worst_c = avg_w.idxmin()
        worst_v = avg_w.min()
        
        st.error(f"""
        * **Ponto Crítico:** A categoria **{worst_c}** registra a menor aceitação média (**{worst_v:.2f}**).
        * **Diagnóstico:** Se uma culinária aparece aqui com um alto número de restaurantes, pode haver um problema estrutural de qualidade na região ou uma saturação de mercado com opções de baixo nível.
        """)

    st.markdown("---")
    st.subheader("🚚 Logística e Entrega")
    
    fig_delivery = plot_online_delivery_cuisines(df_filtered)
    
    if fig_delivery:
        st.plotly_chart(fig_delivery, use_container_width=True)
        
        # Insight dinâmico
        df_deliv_count = get_processed_cuisines(df_filtered[(df_filtered['Has Online delivery'] == True) & (df_filtered['Is delivering now'] == True)])
        most_common = df_deliv_count['Cuisines'].value_counts().idxmax()
        max_val = df_deliv_count['Cuisines'].value_counts().max()
        
        st.info(f"💡 **Foco no Delivery:** A culinária **'{most_common}'** é a mais preparada para o digital, com **{max_val}** estabelecimentos operando entregas em tempo real.")
    else:
        st.warning("Não há restaurantes realizando entregas online nos filtros selecionados.")