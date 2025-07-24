import pyodbc

def render_qualificadores():
    # Conexão com o SQL Server
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=sx-global.database.windows.net;"
        "DATABASE=sx_comercial;"
        "UID=paulo.ferraz;"
        "PWD=Gs!^42j$G0f0^EI#ZjRv"
    )

    df = pd.read_sql("SELECT * FROM vendas_qualificadoras", conn)
    conn.close()

    df['Vendedor'] = df['quali'].apply(lambda x: x if x in METAS else 'Outros')

    resumo = []

    for _, row in df.iterrows():
        vendedor = row['Vendedor']
        emoji = EMOJIS.get(vendedor, '')
        meta = METAS.get(vendedor, 0)
        carteira = row['carteira']
        faturado = row['faturado']
        total = row['total']
        pendente = max(meta - total, 0)
        pct_atingido = (total / meta) * 100 if meta else 0

        resumo.append({
            'pct_valor': pct_atingido,
            'Emoji': f"<span style='font-size:{TAMANHO_FONTE_ROTULOS}px'>{emoji}</span>",
            'Vendedor': f"<strong style='font-size:{TAMANHO_FONTE_ROTULOS}px'>{vendedor}</strong>",
            'Meta': f"<span style='color:#0160A2; font-size:{TAMANHO_FONTE}px'><strong>R$ {meta:,.2f}</strong></span>".replace(",", "X").replace(".", ",").replace("X", "."),
            'Faturado': f"<span style='color:#A0C63F; font-size:{TAMANHO_FONTE}px'><strong>R$ {faturado:,.2f}</strong></span>".replace(",", "X").replace(".", ",").replace("X", "."),
            'Carteira': f"<span style='color:#FFD85B; font-size:{TAMANHO_FONTE}px'><strong>R$ {carteira:,.2f}</strong></span>".replace(",", "X").replace(".", ",").replace("X", "."),
            'Pendente': f"<span style='color:#d62728; font-size:{TAMANHO_FONTE}px'><strong>R$ {pendente:,.2f}</strong></span>".replace(",", "X").replace(".", ",").replace("X", "."),
            '%': f"<strong style='font-size:{TAMANHO_FONTE_PERCENT}px'>{pct_atingido:.1f}%</strong>"
        })

    resumo.sort(key=lambda x: x['pct_valor'], reverse=True)

    metade = len(resumo) // 2 + len(resumo) % 2
    col_esq, col_dir = st.columns(2)

    def render_coluna(col, lista):
        headers = ['Emoji', 'Vendedor', 'Meta', 'Carteira', 'Faturado', 'Pendente', '%']
        with col:
            cols = st.columns([1, 3, 2, 2, 2, 2, 1])
            for i, campo in enumerate(headers):
                cols[i].markdown(f"<strong>{campo}</strong>", unsafe_allow_html=True)
            for linha in lista:
                st.markdown("<hr style='margin-top: 0.1rem; margin-bottom: 0.1rem'>", unsafe_allow_html=True)
                cols = st.columns([1, 3, 2, 2, 2, 2, 1])
                for i, campo in enumerate(headers):
                    cols[i].markdown(linha[campo], unsafe_allow_html=True)

    render_coluna(col_esq, resumo[:metade])
    render_coluna(col_dir, resumo[metade:])
