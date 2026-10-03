import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="24h du Mans", page_icon="🏎️", layout="centered"
)

# Style CSS pour imiter l'interface mobile / Glide
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f7f7f9;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-title {
        font-size: 0.85rem;
        color: #666;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #111;
    }
    .item-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        margin-bottom: 10px;
    }
    div.stButton > button:first-child {
        background-color: #d81b60;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: bold;
        width: 100%;
    }
    </style>
""",
    unsafe_allow_html=True,
)

SHEET_URL = "https://docs.google.com/spreadsheets/d/1yj3nioXvEvf9Pt4tFaFziAZLD5fijqPYGUdssmx2kD0/edit?usp=sharing"


def load_data(sheet_name):
    sheet_id = SHEET_URL.split("/d/")[1].split("/")[0]
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame()


st.title("🏎️ 24h du Mans")

tab1, tab2, tab3, tab4 = st.tabs(
    ["💳 Budget", "📅 Planning", "📦 Logistique", "📷 Photos"]
)

with tab1:
    df_budget = load_data("budget")

    # Calculs indicateurs
    total = 0
    nb_items = 0
    if not df_budget.empty and "Montant" in df_budget.columns:
        total = df_budget["Montant"].fillna(0).sum()
        nb_items = len(df_budget)

    # Cartes synthétiques comme sur Glide
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Total engagé</div>
                <div class="metric-value">{total:.2f} €</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Dépenses</div>
                <div class="metric-value">{nb_items} entrées</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.write("---")

    # Bouton d'ajout / récap
    if df_budget.empty:
        st.info("Aucune dépense enregistrée pour l'instant.")
    else:
        for idx, row in df_budget.iterrows():
            depense = row.get("Dépense", "Dépense")
            montant = row.get("Montant", 0)
            payeur = row.get("Payé par", "Inconnu")
            st.markdown(
                f"""
                <div class="item-card">
                    <strong>{depense}</strong><br>
                    <span style="color: #d81b60; font-size: 1.1rem; font-weight: bold;">{montant} €</span> 
                    <span style="color: #777; font-size: 0.9rem;">— Payé par {payeur}</span>
                </div>
            """,
                unsafe_allow_html=True,
            )

with tab2:
    st.subheader("Planning")
    df_plan = load_data("planning")
    if df_plan.empty:
        st.info("Aucune activité planifiée.")
    else:
        for idx, row in df_plan.iterrows():
            st.markdown(
                f"""
                <div class="item-card">
                    📌 <strong>{row.iloc[0]}</strong><br>
                    <small>{row.iloc[1] if len(row) > 1 else ''}</small>
                </div>
            """,
                unsafe_allow_html=True,
            )

with tab3:
    st.subheader("Logistique & Matériel")
    df_log = load_data("logistique")
    if df_log.empty:
        st.info("Rien dans la liste logistique.")
    else:
        for idx, row in df_log.iterrows():
            st.markdown(
                f"""
                <div class="item-card">
                    📦 <strong>{row.iloc[0]}</strong>
                </div>
            """,
                unsafe_allow_html=True,
            )

with tab4:
    st.subheader("Photos du séjour")
    st.info("Ajoutez vos liens de photos partagées ici.")
