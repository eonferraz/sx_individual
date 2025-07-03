import streamlit as st
import pandas as pd
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
    'Alvaro Marinho': 746951.22,
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

# Função principal

def render_vendedores(df_fat, df_cart):
    hoje = datetime.today()
    mes = hoje.month
    ano = hoje.year

    df_fat_mes = df_fat[df_fat['Data Emissão'].dt.month.eq(mes) & df_fat['Data Emissão'].dt.year.eq(ano)].copy()
    df_cart_mes = df_cart[df_cart['Data Entrega'].dt.month.eq(mes) & df_cart['Data Entrega'].dt.year.eq(ano)].copy()

    df_fat_mes['Vendedor'] = df_fat_mes['Vendedor'].apply(lambda x: x if x in METAS else 'Outros')
    df_cart_mes['Vendedor'] = df_cart_mes['Vendedor'].apply(lambda x: x if x in METAS else 'Outros')

    todos_vendedores = list(METAS.keys())
    resumo = []

    for vendedor in todos_vendedores:
        emoji = EMOJIS.get(vendedor, '')
        meta = METAS.get(vendedor, 0)

        fat = df_fat_mes[df_fat_mes['Vendedor'] == vendedor]['Total Produto'].sum()
        cart = df_cart_mes[df_cart_mes['Vendedor'] == vendedor]['Valor Receita Bruta Pedido'].sum()
        pend = max(meta - fat - cart, 0)

        pct_atingido = ((fat + cart) / meta) * 100 if meta else 0

        resumo.append({
            'pct_valor': pct_atingido,
            'Emoji': f"<span style='font-size:28px'>{emoji}</span>",
            'Vendedor': f"<strong style='font-size:18px'>{vendedor}</strong>",
            'Meta': f"<span style='color:#0160A2'><strong>R$ {meta:,.2f}</strong></span>".replace(",", "X").replace(".", ",").replace("X", "."),
            'Faturado': f"<span style='color:#A0C63F'><strong>R$ {fat:,.2f}</strong></span>".replace(",", "X").replace(".", ",").replace("X", "."),
            'Carteira': f"<span style='color:#5BA4FF'><strong>R$ {cart:,.2f}</strong></span>".replace(",", "X").replace(".", ",").replace("X", "."),
            'Pendente': f"<span style='color:#d62728'><strong>R$ {pend:,.2f}</strong></span>".replace(",", "X").replace(".", ",").replace("X", "."),
            '% Atingido': f"<strong>{pct_atingido:.1f}%</strong>"
        })

    resumo.sort(key=lambda x: x['pct_valor'], reverse=True)

    metade = len(resumo) // 2 + len(resumo) % 2
    col_esq, col_dir = st.columns(2)

    def render_coluna(col, lista):
        for linha in lista:
            with col:
                st.markdown("<hr style='margin-top: 0.5rem; margin-bottom: 0.5rem'>", unsafe_allow_html=True)
                st.markdown(linha['Emoji'], unsafe_allow_html=True)
                st.markdown(linha['Vendedor'], unsafe_allow_html=True)
                st.markdown(linha['Meta'], unsafe_allow_html=True)
                st.markdown(linha['Carteira'], unsafe_allow_html=True)
                st.markdown(linha['Faturado'], unsafe_allow_html=True)
                st.markdown(linha['Pendente'], unsafe_allow_html=True)
                st.markdown(linha['% Atingido'], unsafe_allow_html=True)

    render_coluna(col_esq, resumo[:metade])
    render_coluna(col_dir, resumo[metade:])
