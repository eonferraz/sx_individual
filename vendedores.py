import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Emojis por vendedor
EMOJIS = {
    'Aline Ferreira': '💣',
    'Alvaro Marinho': '🐿️',
    'Christiana Carvalho': '🧸',
    'Letícia Louzada': '🐅',
    'Luciana Guisard': '🤝🏻',
    'Maria Bianca Benco': '🍺',
    'Maria Luiza Santos': '🐋',
    'Maria Schmidt': '🦋',
    'Mirian Goffi': '🍣',
    'Monica Reis': '🤩',
    'Stefania Andrade': '🧚🏻‍♀️',
    'Yuri Rodrigues': '🐨'
}

# Metas por vendedor
METAS = {
    'Christiana Carvalho': 746951.22,
    'Letícia Louzada': 746951.22,
    'Maria Schmidt': 190548.78,
    'Maria Bianca Benco': 121951.22,
    'Mirian Goffi': 609756.10,
    'Stefania Andrade': 640243.90,
    'Yuri Rodrigues': 190548.78,
    'Celso Marinho': 190548.78,
    'Aline Ferreira': 1832877.67,
    'Monica Reis': 746951.22,
    'Luciana Guisard': 190548.78,
    'Outros': 0.0
}

# Função termômetro individual
def gerar_termometro(faturado, carteira, pendente, meta, pct_pendente):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=[faturado], marker_color='#A0C63F', name='Faturado', orientation='h'))
    fig.add_trace(go.Bar(x=[carteira], marker_color='#FFD85B', name='Carteira', orientation='h'))
    fig.add_trace(go.Bar(x=[pendente], marker_color='#d62728', name='Pendente', orientation='h',
                         text=[f'{pct_pendente:.1f}%'], textposition='outside', textfont=dict(size=12)))
    fig.update_layout(
        barmode='stack', height=30, margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(range=[0, meta], showticklabels=False), showlegend=False
    )
    return fig

# Função principal
def render_vendedores(df_fat, df_cart):
    hoje = datetime.today()
    mes = hoje.month
    ano = hoje.year

    df_fat_mes = df_fat[df_fat['Data Emissão'].dt.month.eq(mes) & df_fat['Data Emissão'].dt.year.eq(ano)].copy()
    df_cart_mes = df_cart[df_cart['Data Entrega'].dt.month.eq(mes) & df_cart['Data Entrega'].dt.year.eq(ano)].copy()

    df_fat_mes['Vendedor'] = df_fat_mes['Vendedor'].apply(lambda x: x if x in METAS else 'Outros')
    df_cart_mes['Vendedor'] = df_cart_mes['Vendedor'].apply(lambda x: x if x in METAS else 'Outros')

    resumo = []
    vendedores = sorted(set(df_fat_mes['Vendedor']).union(df_cart_mes['Vendedor']))

    for vendedor in vendedores:
        emoji = EMOJIS.get(vendedor, '')
        meta = METAS.get(vendedor, 0)

        fat = df_fat_mes[df_fat_mes['Vendedor'] == vendedor]['Total Produto'].sum()
        cart = df_cart_mes[df_cart_mes['Vendedor'] == vendedor]['Valor Receita Bruta Pedido'].sum()
        pend = max(meta - fat - cart, 0)

        pct_atingido = ((fat + cart) / meta) * 100 if meta else 0
        pct_pendente = (pend / meta) * 100 if meta else 0

        termo = gerar_termometro(fat, cart, pend, meta, pct_pendente)

        resumo.append({
            'pct_valor': pct_atingido,
            'Emoji': f"<span style='font-size:28px'>{emoji}</span>",
            'Vendedor': f"<strong style='font-size:18px'>{vendedor}</strong>",
            'Meta': f"<span style='color:#0160A2'><strong>R$ {meta:,.2f}</strong></span>".replace(",", "X").replace(".", ",").replace("X", "."),
            'Faturado': f"<span style='color:#A0C63F'><strong>R$ {fat:,.2f}</strong></span>".replace(",", "X").replace(".", ",").replace("X", "."),
            'Carteira': f"<span style='color:#FFD85B'><strong>R$ {cart:,.2f}</strong></span>".replace(",", "X").replace(".", ",").replace("X", "."),
            'Pendente': f"<span style='color:#d62728'><strong>R$ {pend:,.2f}</strong></span>".replace(",", "X").replace(".", ",").replace("X", "."),
            '% Atingido': f"<strong>{pct_atingido:.1f}%</strong>",
            'Termômetro': termo
        })

    # Ordenar por % Atingido
    resumo.sort(key=lambda x: x['pct_valor'], reverse=True)

    header_cols = st.columns([1, 3, 2, 2, 2, 2, 2, 8])
    headers = ['Emoji', 'Vendedor', 'Meta', 'Carteira', 'Faturado', 'Pendente', '% Atingido', 'Termômetro']
    for col, title in zip(header_cols, headers):
        col.markdown(f"**{title}**")

    for linha in resumo:
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1, 3, 2, 2, 2, 2, 2, 8])
        col1.markdown(linha['Emoji'], unsafe_allow_html=True)
        col2.markdown(linha['Vendedor'], unsafe_allow_html=True)
        col3.markdown(linha['Meta'], unsafe_allow_html=True)
        col4.markdown(linha['Carteira'], unsafe_allow_html=True)
        col5.markdown(linha['Faturado'], unsafe_allow_html=True)
        col6.markdown(linha['Pendente'], unsafe_allow_html=True)
        col7.markdown(linha['% Atingido'], unsafe_allow_html=True)
        col8.plotly_chart(linha['Termômetro'], use_container_width=True)
