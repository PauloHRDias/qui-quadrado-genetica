import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="Calculadora Qui Quadrado Genetica II",
    page_icon="🧬",
    layout="wide"
)

st.title("Calculadora de Qui-quadrado Genético")
st.markdown("""
Teste de **Homogeneidade** e **Aderência** para Cruzamentos Dihíbridos
""")

tab_aderencia, tab_homogeneidade, tab_teoria = st.tabs(
    ["Qui² de Aderência", "Qui² de Homogeneidade", "Teoria & Fórmulas"]
)

# ============================================
# TAB 1: QUI² DE ADERÊNCIA
# ============================================
with tab_aderencia:
    st.header("📊 Dados Observados (F2 - Cruzamento Dihíbrido)")
    st.markdown("""
    Agrupe os dados por classe fenotípica do cruzamento dihíbrido
    **(proporção esperada 9:3:3:1)**
    """)

    col1, col2 = st.columns(2)

    with col1:
        selvagem = st.number_input(
            "Selvagem (Vg_ Ee):",
            value=165,
            min_value=0,
            help="Número de indivíduos selvagens"
        )
        vestigial = st.number_input(
            "Vestigial (vgvg Ee):",
            value=54,
            min_value=0,
            help="Número de indivíduos com asas vestigiais"
        )

    with col2:
        ebony = st.number_input(
            "Ebony (Vg_ ee):",
            value=62,
            min_value=0,
            help="Número de indivíduos ebony"
        )
        ebony_vest = st.number_input(
            "Ebony/Vestigial (vgvg ee):",
            value=17,
            min_value=0,
            help="Número de indivíduos ebony/vestigial"
        )

    # Botão de calcular dentro da aba aderência
    if st.button("🔢 Calcular Qui² de Aderência", type="primary"):
        # Dados
        observadas = [selvagem, vestigial, ebony, ebony_vest]
        total = sum(observadas)

        if total == 0:
            st.error("⚠️ Total deve ser maior que 0!")
            st.stop()

        # Esperadas (9:3:3:1)
        esperadas = [
            (9/16) * total,
            (3/16) * total,
            (3/16) * total,
            (1/16) * total
        ]

        # Calcular Chi²
        chi2 = sum(((o - e) ** 2) / e for o, e in zip(observadas, esperadas))

        # Graus de liberdade
        gl = 3
        chi_critico = 7.815

        # Mostrar resultados
        st.divider()
        st.subheader("📊 Resultados do Teste")

        # Métricas
        st.metric("Chi² Calculado:", f"{chi2:.4f}")
        st.metric("Graus de Liberdade (gl):", gl)
        st.metric("Chi² Crítico (α=0.05):", f"{chi_critico}")

        # Decisão
        st.divider()
        if chi2 < chi_critico:
            st.success("✅ **ACEITA H₀** - Dados SEGUEM proporção 9:3:3:1")
            st.info(f"""
            O valor de Chi² calculado (**{chi2:.4f}**) é menor que o Chi² crítico
            (**{chi_critico}**). Isso significa que os desvios entre os valores
            observados e esperados são pequenos e podem ser explicados pelo acaso.

            **Portanto, aceitamos a hipótese nula:** os dados seguem a proporção
            Mendeliana esperada 9:3:3:1 para cruzamento dihíbrido.
            """)
        else:
            st.error("❌ **REJEITA H₀** - Dados NÃO SEGUEM proporção 9:3:3:1")
            st.warning("""
            O valor de Chi² calculado é maior que o Chi² crítico. Isso significa
            que os desvios entre os valores observados e esperados são significativos.

            **Portanto, rejeitamos a hipótese nula:** os dados NÃO seguem a
            proporção Mendeliana esperada 9:3:3:1.
            """)

        # Tabela
        st.divider()
        st.subheader("📋 Tabela de Comparação: Observado vs Esperado")

        df = pd.DataFrame({
            "Classe Fenotípica": [
                "Selvagem (Vg_ Ee)",
                "Vestigial (vgvg Ee)",
                "Ebony (Vg_ ee)",
                "Ebony/Vestigial (vgvg ee)"
            ],
            "Observado (O)": observadas,
            "Esperado (E)": [round(e, 2) for e in esperadas],
            "Desvio (O-E)": [round(o - e, 2) for o, e in zip(observadas, esperadas)],
            "(O-E)²/E": [round(((o - e) ** 2) / e, 4) for o, e in zip(observadas, esperadas)]
        })

        st.dataframe(df, use_container_width=True)

        # Gráfico
        st.divider()
        st.subheader("📈 Gráfico Comparativo")

        fig = go.Figure()

        fig.add_trace(go.Bar(
            name='Observado',
            x=['Selvagem', 'Vestigial', 'Ebony', 'Ebony/Vest'],
            y=observadas,
            marker_color='#667eea',
            hovertemplate='Observado: %{y}<extra>'
        ))

        fig.add_trace(go.Bar(
            name='Esperado',
            x=['Selvagem', 'Vestigial', 'Ebony', 'Ebony/Vest'],
            y=esperadas,
            marker_color='#764ba2',
            hovertemplate='Esperado: %{y}<extra>'
        ))

        fig.update_layout(
            title="Comparação: Observado vs Esperado (Aderência)",
            barmode='group',
            height=500,
            xaxis_title="Classe Fenotípica",
            yaxis_title="Número de Indivíduos",
            legend_title="Tipo"
        )

        st.plotly_chart(fig, use_container_width=True)

# ============================================
# TAB 2: QUI² DE HOMOGENEIDADE
# ============================================
with tab_homogeneidade:
    st.header("📊 Dados por Amostra")
    st.markdown("""
    Insira os dados de **2 amostras separadas** para verificar se são homogêneas
    """)

    # Inputs para Amostra 1
    st.subheader("Amostra 1")
    col1, col2 = st.columns(2)

    with col1:
        s1_selvagem = st.number_input("Selvagem (Amostra 1):", value=115, min_value=0)
        s1_fvestigial = st.number_input("F. vestigial (Amostra 1):", value=19, min_value=0)
        s1_mvestigial = st.number_input("M. vestigial (Amostra 1):", value=17, min_value=0)
        s1_febony = st.number_input("F. ebony (Amostra 1):", value=21, min_value=0)

    with col2:
        s1_mebony = st.number_input("M. ebony (Amostra 1):", value=19, min_value=0)
        s1_fev = st.number_input("F. eb./vest. (Amostra 1):", value=6, min_value=0)
        s1_mev = st.number_input("M. eb./vest. (Amostra 1):", value=5, min_value=0)

    # Amostra 1 - total
    s1_dados = [s1_selvagem, s1_fvestigial, s1_mvestigial, s1_febony, s1_mebony, s1_fev, s1_mev]
    total1 = sum(s1_dados)
    st.info(f"**Total Amostra 1: {total1}**")

    st.divider()

    # Inputs para Amostra 2
    st.subheader("Amostra 2")
    col1, col2 = st.columns(2)

    with col1:
        s2_selvagem = st.number_input("Selvagem (Amostra 2):", value=50, min_value=0)
        s2_fvestigial = st.number_input("F. vestigial (Amostra 2):", value=10, min_value=0)
        s2_mvestigial = st.number_input("M. vestigial (Amostra 2):", value=8, min_value=0)
        s2_febony = st.number_input("F. ebony (Amostra 2):", value=10, min_value=0)

    with col2:
        s2_mebony = st.number_input("M. ebony (Amostra 2):", value=12, min_value=0)
        s2_fev = st.number_input("F. eb./vest. (Amostra 2):", value=3, min_value=0)
        s2_mev = st.number_input("M. eb./vest. (Amostra 2):", value=3, min_value=0)

    # Amostra 2 - total
    s2_dados = [s2_selvagem, s2_fvestigial, s2_mvestigial, s2_febony, s2_mebony, s2_fev, s2_mev]
    total2 = sum(s2_dados)
    st.info(f"**Total Amostra 2: {total2}**")

    # Botão de calcular Homogeneidade
    if st.button("🔢 Calcular Qui² de Homogeneidade", type="primary"):
        total_geral = total1 + total2

        if total_geral == 0:
            st.error("⚠️ Total deve ser maior que 0!")
            st.stop()

        classes = ['selvagem', 'fvestigial', 'mvestigial', 'febony', 'mebony', 'fev', 'mev']
        nomes_classe = ['Selvagem', 'F. vestigial', 'M. vestigial', 'F. ebony', 'M. ebony', 'F. eb./vest.', 'M. eb./vest.']

        totais_classe = [s1 + s2 for s1, s2 in zip(s1_dados, s2_dados)]
        frequencias = [t / total_geral for t in totais_classe]

        e1 = [total1 * f for f in frequencias]
        e2 = [total2 * f for f in frequencias]

        chi2_homog = 0
        for o1, o2, exp1, exp2 in zip(s1_dados, s2_dados, e1, e2):
            if exp1 > 0: chi2_homog += ((o1 - exp1) ** 2) / exp1
            if exp2 > 0: chi2_homog += ((o2 - exp2) ** 2) / exp2

        gl_homog = len(classes) - 1
        chi_critico_homog = 12.592  # Para gl=6 e alfa=0.05

        st.divider()
        st.subheader("Resultados - Homogeneidade")
        st.metric("Chi² Calculado:", f"{chi2_homog:.4f}")
        st.metric("Graus de Liberdade (gl):", gl_homog)
        st.metric("Chi² Crítico (α=0.05):", f"{chi_critico_homog}")

        if chi2_homog < chi_critico_homog:
            st.success("✅ **Amostras Homogêneas** - Não há diferença significativa entre as amostras.")
        else:
            st.error("❌ **Amostras Não Homogêneas** - Existe diferença significativa entre as amostras.")

# ============================================
# TAB 3: TEORIA
# ============================================
with tab_teoria:
    st.header("📚 Teoria e Fórmulas")
    st.latex(r"\chi^2 = \sum \frac{(O - E)^2}{E}")
    st.markdown("""
    * **O** = Valor Observado
    * **E** = Valor Esperado
    """)
