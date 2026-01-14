import pandas as pd
import streamlit as st
from PIL import Image
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Visão Restaurantes",page_icon='🍽️', layout="wide")

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

def plot_usa_cuisine_comparison(df):
    """Gera o comparativo de custo entre comida Japonesa e BBQ nos EUA 🥩🍣"""
    # 1. Filtro específico
    df_usa = df[df['Country Name'] == 'United States']
    
    if df_usa.empty:
        return None, None, None

    # 2. Cálculo das médias
    jp_avg = df_usa[df_usa['Cuisines'].str.contains('Japanese', case=False, na=False)]['Average Cost for two'].mean()
    bbq_avg = df_usa[df_usa['Cuisines'].str.contains('BBQ', case=False, na=False)]['Average Cost for two'].mean()

    # 3. Criação do DataFrame para o Plotly
    df_comp = pd.DataFrame({
        'Culinária': ['Japonesa 🍣', 'BBQ (Churrasco) 🥩'],
        'Preço Médio': [jp_avg, bbq_avg]
    }).dropna()

    if df_comp.empty:
        return None, None, None

    # 4. Construção do Gráfico
    fig = px.bar(
        df_comp, x='Culinária', y='Preço Médio', color='Culinária',
        text='Preço Médio', height=500,
        color_discrete_map={'Japonesa 🍣': '#FF4B4B', 'BBQ (Churrasco) 🥩': '#6D4C41'}
    )
    
    fig.update_traces(textposition='outside', texttemplate='$ %{text:.2f}', width=0.4)
    fig.update_layout(
        xaxis_title=None, 
        yaxis_title="Preço Médio (USD)", 
        showlegend=False, 
        margin=dict(t=50, b=50)
    )
    
    return fig, jp_avg, bbq_avg


def plot_booking_vs_cost(df):
    """Gera o comparativo de preço entre restaurantes que aceitam ou não reserva 📅"""
    # 1. Preparação dos dados
    df_booking = df.groupby('Has Table booking')['Average Cost for two'].mean().reset_index()
    
    # Mapeando labels e adicionando emojis para o gráfico
    df_booking['Reserva'] = df_booking['Has Table booking'].map({
        True: 'Faz Reserva 📅', 
        False: 'Não Faz Reserva 🍽️'
    })
    
    # 2. Criação do Gráfico
    fig = px.bar(
        df_booking,
        x='Reserva',
        y='Average Cost for two',
        color='Reserva',
        text='Average Cost for two',
        height=500,
        labels={'Reserva': 'Serviço de Reserva', 'Average Cost for two': 'Preço Médio (2 pessoas)'},
        color_discrete_map={'Faz Reserva 📅': '#3498DB', 'Não Faz Reserva 🍽️': '#95A5A6'}
    )
    
    # 3. Ajustes de Layout
    fig.update_traces(textposition='outside', texttemplate='%{text:,.2f}', width=0.4)
    fig.update_layout(
        xaxis_title=None,
        yaxis_title="Preço Médio (Moeda Local)",
        showlegend=False,
        margin=dict(t=50, b=50)
    )
    
    return fig, df_booking


def plot_top_luxury_restaurants(df):
    """Gera o gráfico horizontal dos 10 restaurantes mais caros 💎"""
    # 1. Preparação dos dados
    df_max_cost = (df.groupby(['Restaurant Name', 'Country Name'])['Average Cost for two']
                     .max()
                     .sort_values(ascending=False)
                     .reset_index()
                     .head(10))
    
    if df_max_cost.empty:
        return None, None

    # 2. Criação do Gráfico de Barras Horizontais
    fig = px.bar(
        df_max_cost,
        x='Average Cost for two',
        y='Restaurant Name', 
        color='Country Name',
        text='Average Cost for two',
        orientation='h',
        height=500,
        labels={'Average Cost for two': 'Custo para Dois', 'Restaurant Name': 'Restaurante', 'Country Name': 'País'},
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    
    # 3. Ajustes de Layout e Posicionamento do Texto
    fig.update_traces(
        textposition='outside', 
        texttemplate='%{text:,.2f}', 
        cliponaxis=False 
    )
    
    fig.update_layout(
        xaxis_range=[0, df_max_cost['Average Cost for two'].max() * 1.25], # Espaço para o texto
        yaxis={'categoryorder': 'total ascending'}, 
        xaxis_title="Custo (Moeda Local)",
        yaxis_title=None,
        margin=dict(t=30, b=30)
    )
    
    return fig, df_max_cost
    

def plot_delivery_engagement(df):
    """Gera o gráfico de engajamento (soma de votos) por disponibilidade de delivery 🚚"""
    # 1. Preparação dos dados (Soma de votos)
    df_delivery = df.groupby('Has Online delivery')['Votes'].sum().reset_index()
    
    # Mapeando labels e adicionando emojis
    df_delivery['Delivery'] = df_delivery['Has Online delivery'].map({
        True: 'Aceita Online 🚚', 
        False: 'Apenas Presencial 🍽️'
    })
    
    # 2. Criação do Gráfico
    fig = px.bar(
        df_delivery, 
        x='Delivery', 
        y='Votes', 
        color='Delivery',
        text='Votes', 
        labels={'Delivery': 'Tipo de Serviço', 'Votes': 'Soma Total de Votos'},
        color_discrete_map={'Aceita Online 🚚': '#2ECC71', 'Apenas Presencial 🍽️': '#E74C3C'}
    )
    
    # 3. Ajustes de Layout (Formatação .2s para números grandes como 100k)
    fig.update_traces(textposition='outside', texttemplate='%{text:.2s}')
    fig.update_layout(
        xaxis_title=None,
        yaxis_title="Total de Votos Acumulados",
        showlegend=False,
        margin=dict(t=20, b=20)
    )
    
    return fig, df_delivery

def plot_best_brazilian_ratings(df):
    """Gera o ranking das melhores notas de culinária brasileira no Brasil 🇧🇷"""
    # 1. Filtro: Culinária brasileira + País Brasil
    df_br_top = (df[(df['Cuisines'].str.contains('Brazilian', case=False, na=False)) & 
                    (df['Country Name'] == 'Brazil')]
                 .groupby(['Restaurant Name', 'Country Name'])['Aggregate rating']
                 .mean().sort_values(ascending=False).reset_index().head(10))
    
    if df_br_top.empty:
        return None, None

    # 2. Criação do Gráfico (Usando tons de verde/amarelo para o Brasil)
    fig = px.bar(
        df_br_top, 
        x='Restaurant Name', 
        y='Aggregate rating', 
        text='Aggregate rating',
        labels={'Restaurant Name': 'Restaurante', 'Aggregate rating': 'Nota Média'},
        color_discrete_sequence=['#228B22'] # Verde floresta
    )
    
    fig.update_traces(textposition='outside', texttemplate='%{text:.1f}')
    fig.update_layout(
        xaxis_title=None, 
        yaxis_title="Nota (0-5)", 
        margin=dict(t=20, b=20),
        yaxis_range=[0, 5.5] # Garante que o texto da nota apareça
    )
    
    return fig, df_br_top

def plot_lowest_brazilian_ratings(df):
    """Gera o gráfico horizontal das menores notas da culinária brasileira 📉"""
    # 1. Filtro: Culinária brasileira e com votos registrados
    df_br_base_low = df[(df['Cuisines'].str.contains('Brazilian', case=False, na=False)) & (df['Votes'] > 0)]
    
    # 2. Agrupamento e cálculo da média
    df_br_low = (df_br_base_low.groupby(['Restaurant Name', 'Country Name'])['Aggregate rating']
                 .mean().sort_values(ascending=True).reset_index().head(10))

    if df_br_low.empty:
        return None, None

    # 3. Formatação do Eixo Y (Nome do Restaurante - Nota)
    df_br_low['Nome com Nota'] = df_br_low.apply(lambda x: f"{x['Restaurant Name']} - {x['Aggregate rating']:.1f}", axis=1)

    # 4. Geração do gráfico
    fig = px.bar(
        df_br_low, 
        x='Aggregate rating', 
        y='Nome com Nota', 
        color='Country Name',
        orientation='h', 
        labels={'Aggregate rating': 'Nota Média', 'Nome com Nota': 'Restaurante', 'Country Name': 'País'},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    # 5. Ajustes de Layout
    fig.update_layout(
        xaxis_range=[0, 5], 
        yaxis={'categoryorder': 'total descending'}, 
        xaxis_title="Nota Média",
        yaxis_title=None,
        margin=dict(t=20, b=20)
    )
    
    return fig, df_br_low

def get_top_restaurants_table(df):
    """Processa os dados para a tabela dos 20 restaurantes com maiores notas ⭐"""
    # 1. Agrupamento e cálculo da média
    df_best = (df.groupby(['Restaurant ID', 'Restaurant Name', 'Country Name', 'City', 'Cuisines'])['Aggregate rating']
                 .mean().sort_values(ascending=False).reset_index().head(20))
    
    # 2. Renomeação de colunas para exibição amigável
    df_best.columns = ['ID', 'Restaurante', 'País', 'Cidade', 'Culinária', 'Nota Média']
    
    return df_best

def get_top_voted_restaurants(df):
    """Processa os dados dos 10 restaurantes com maior soma de votos 🗳️"""
    df_votes = (df.groupby(['Restaurant Name', 'Country Name'])['Votes']
                  .sum()
                  .sort_values(ascending=False)
                  .reset_index()
                  .head(10))
    return df_votes
    
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
# Layout Principal com Abas
# ==============================================================================
st.title("🍽️Visão Restaurantes")

# Criação das Abas
tab_aval, tab_preco = st.tabs(["⭐ Avaliações de Restaurantes", "💰 Preço Médio para Dois"])

# ------------------------------------------------------------------------------
# ABA 1: AVALIAÇÃO DE RESTAURANTES
# ------------------------------------------------------------------------------
with tab_aval:
    st.subheader("🗳️ Top 10 Restaurantes Mais Avaliados")
    
    df_rest_votes = get_top_voted_restaurants(df_filtered)
    
    # Exibição do gráfico usando a função genérica que você já tem
    st.plotly_chart(
        create_bar_chart(df_rest_votes, 'Restaurant Name', 'Votes', 'Total de Votos', '.2s'), 
        use_container_width=True
    )

    # Insight Dinâmico
    if not df_rest_votes.empty:
        top_rest = df_rest_votes.iloc[0]
        st.success(
            f"🏆 **Líder de Popularidade:** O restaurante **'{top_rest['Restaurant Name']}'** "
            f"({top_rest['Country Name']}) é o mais engajado da base, com um total de "
            f"**{top_rest['Votes']:,}** avaliações."
        )


    st.markdown("---")
    st.subheader("⭐ Top 20 Restaurantes com Maiores Notas Médias")
    
    df_top_table = get_top_restaurants_table(df_filtered)
    
    # Exibição da tabela interativa
    st.dataframe(df_top_table, use_container_width=True, hide_index=True)

    # Insight Dinâmico
    if not df_top_table.empty:
        top_r = df_top_table.iloc[0]
        st.success(
            f"⭐ **Destaque:** O restaurante **{top_r['Restaurante']}** em "
            f"**{top_r['Cidade']} ({top_r['País']})** é um dos mais bem avaliados "
            f"do mundo com nota **{top_r['Nota Média']:.1f}**."
        )

    st.markdown("---")
    st.subheader("Destaques da Culinária Brasileira")
    col_br1, col_br2 = st.columns(2)

    with col_br1:
        st.write("### 📉 Menores Notas Culinária Brasileira")
        
        fig_low, data_low = plot_lowest_brazilian_ratings(df_filtered)
        
        if fig_low:
            st.plotly_chart(fig_low, use_container_width=True)
            
            # Insight Dinâmico
            top_error = data_low.iloc[0]
            st.error(f"📉 **Foco de Melhoria:** O restaurante **'{top_error['Restaurant Name']}'** tem a menor avaliação média ({top_error['Aggregate rating']:.1f}).")
        else:
            st.warning("Não há dados de culinária brasileira para os países selecionados.")

    with col_br2:
        st.write("### 🏅 Melhores Notas Culinária brasileira (Brasil)")
        
        fig_br_top, data_br_top = plot_best_brazilian_ratings(df_filtered)
        
        if fig_br_top:
            st.plotly_chart(fig_br_top, use_container_width=True)
            
            # Insight Dinâmico
            top_r = data_br_top.iloc[0]
            st.success(f"🏅 **Melhor no Brasil:** '{top_r['Restaurant Name']}' com média {top_r['Aggregate rating']:.1f}.")
        else:
            st.warning("Selecione 'Brazil' nos filtros para ver o ranking nacional.")



### 🚚 Engajamento Total: Pedidos Online vs. Qtd. de Avaliações
    st.markdown("---")
    st.write("### 🚚 Engajamento Total: Pedidos Online vs. Qtd. de Avaliações")
    
    fig_del, data_del = plot_delivery_engagement(df_filtered)
    
    if fig_del:
        st.plotly_chart(fig_del, use_container_width=True)
        
        # Insight Dinâmico
        if len(data_del) > 1:
            # Recuperando as somas usando a coluna original booleana para segurança
            soma_sim = data_del.loc[data_del['Has Online delivery'] == True, 'Votes'].values[0]
            soma_nao = data_del.loc[data_del['Has Online delivery'] == False, 'Votes'].values[0]
            
            if soma_sim > soma_nao:
                st.info(f"💡 **Insight:** O volume total de votos com entrega online (**{soma_sim:,}**) supera o presencial, indicando maior engajamento digital.")
            else:
                st.info(f"💡 **Insight:** Restaurantes apenas presenciais ainda concentram a maior soma de votos (**{soma_nao:,}**).")
# ------------------------------------------------------------------------------
# ABA 2: PREÇO MÉDIO PARA DUAS PESSOAS
# ------------------------------------------------------------------------------
with tab_preco:
    # --- Na Aba 2: Preço Médio para Dois ---

    st.subheader("💎 Top 10 Restaurantes com Maior Custo para Dois")
    
    fig_lux, data_lux = plot_top_luxury_restaurants(df_filtered)
    
    if fig_lux:
        st.plotly_chart(fig_lux, use_container_width=True)
        
        # Insight Dinâmico
        top_luxury = data_lux.iloc[0]
        st.warning(f"💰 **Destaque de Luxo:** O restaurante **'{top_luxury['Restaurant Name']}'** ({top_luxury['Country Name']}) possui o maior custo nominal: **{top_luxury['Average Cost for two']:,.2f}**.")
    else:
        st.info("Nenhum dado disponível para exibir o ranking de luxo.")
        

    # --- Na Aba 2: Preço Médio para Dois ---

    st.markdown("---")
    st.subheader("📅 Relação entre Reservas de Mesa e Custo Médio")
    
    fig_book, data_book = plot_booking_vs_cost(df_filtered)
    
    if fig_book:
        st.plotly_chart(fig_book, use_container_width=True)
        
        # Insight Dinâmico
        if len(data_book) > 1:
            # Pegando os valores para o cálculo
            custo_reserva = data_book.loc[data_book['Has Table booking'] == True, 'Average Cost for two'].values[0]
            custo_sem_reserva = data_book.loc[data_book['Has Table booking'] == False, 'Average Cost for two'].values[0]
            
            if custo_reserva > custo_sem_reserva:
                diff = ((custo_reserva / custo_sem_reserva) - 1) * 100
                st.success(f"📈 **Insight:** Restaurantes com reserva são **{diff:.1f}% mais caros** em média, indicando um posicionamento premium.")
            else:
                st.info("📉 **Insight:** Não há diferença expressiva de preço entre restaurantes com e sem reserva nesta seleção.")


    # --- Na Aba 2: Preço Médio para Dois ---

    st.markdown("---")
    st.subheader("🥩 Comparativo de Custo: Comida Japonesa vs. BBQ (EUA)")

    fig_usa, jp_val, bbq_val = plot_usa_cuisine_comparison(df_filtered)

    if fig_usa:
        st.plotly_chart(fig_usa, use_container_width=True)

        # Insight Dinâmico
        if jp_val > bbq_val:
            st.info(f"🇺🇸 **Insight EUA:** A culinária Japonesa é mais cara que BBQ em média, com uma diferença de **${(jp_val - bbq_val):.2f}**.")
        elif bbq_val > jp_val:
            st.info(f"🇺🇸 **Insight EUA:** O BBQ Americano supera a culinária Japonesa em custo médio por cerca de **${(bbq_val - jp_val):.2f}**.")
        else:
            st.info("🇺🇸 **Insight EUA:** Ambas as culinárias possuem ticket médio idêntico.")
    else:
        st.warning("Os Estados Unidos não estão selecionados ou não há dados de 🥩 BBQ / 🍣 Sushi disponíveis.")
