import streamlit as st
import pandas as pd
import altair as alt

# --------------------------
# Chargement du fichier Excel et mise en cache
# --------------------------
@st.cache_data
def lire_fichier_excel(fichier):
    """Ouvre un fichier Excel et renvoie son contenu sous forme de dictionnaire."""
    try:
        contenu = pd.read_excel(fichier, sheet_name=None, engine="openpyxl")
        return contenu
    except Exception as e:
        st.error(f"Erreur lors de l'ouverture du fichier : {e}")
        return None

# --------------------------
# Extraction du mapping PD
# --------------------------
def recuperer_correspondance_pd(contenu):
    """Extrait les probabilités de défaut (PD) depuis la feuille "Params"."""
    if "Params" not in contenu:
        st.error("La feuille 'Params' est introuvable.")
        return {}
    
    try:
        df_params = contenu["Params"]
        df_params.columns = df_params.columns.astype(str).str.strip()

        pd_table = df_params.iloc[1:20, 4:8].copy()
        pd_table.columns = ["Notation", "1Y", "3Y", "5Y"]

        def convertir_pourcentage(val):
            if isinstance(val, str):
                val = val.replace(",", ".").replace("%", "").strip()
            try:
                return float(val) / 100.0
            except Exception:
                return None

        for col in ["1Y", "3Y", "5Y"]:
            pd_table[col] = pd_table[col].apply(convertir_pourcentage)

        return pd_table.set_index("Notation").to_dict("index")
    
    except Exception as e:
        st.error(f"Erreur lors de l'extraction des données PD : {e}")
        return {}

# --------------------------
# Calcul des indicateurs pour un crédit
# --------------------------
def evaluer_credit(credit, taux_annuel, duree, mapping_pd):
    """Effectue les calculs liés au risque et au rendement d'un crédit donné."""
    try:
        montant = float(credit["Exposure"])
        notation = str(credit["Rating"]).strip()
        lgd = credit["LGD"]
        lgd = float(lgd.replace("%", "").strip()) / 100.0 if isinstance(lgd, str) else float(lgd)

        pd_val = mapping_pd.get(notation, {}).get(f"{int(duree)}Y", 0.0001)

        revenus_interets = montant * taux_annuel * duree
        probabilite_defaut_cumulee = 1 - (1 - pd_val) ** duree
        perte_estimee = probabilite_defaut_cumulee * lgd * montant
        profit = revenus_interets - perte_estimee

        return {
            "Montant": montant,
            "Notation": notation,
            "LGD": lgd,
            "Taux_Annuel": taux_annuel,
            "Duree": duree,
            "Revenus_Interets": revenus_interets,
            "PD_Annuelle": pd_val,
            "PD_Cumulee": probabilite_defaut_cumulee,
            "Perte_Estimee": perte_estimee,
            "Profit": profit
        }
    except Exception as e:
        st.error(f"Erreur lors du calcul du crédit : {e}")
        return None

# --------------------------
# Interface Streamlit
# --------------------------
st.set_page_config(page_title="Simulation RaRoC", layout="wide")

st.title("📊 Outil de Simulation du Risque de Crédit")
st.markdown("Importez un fichier Excel pour analyser et évaluer un crédit en fonction de sa notation.")

# --------------------------
# Chargement du fichier via Streamlit
# --------------------------
st.sidebar.header("📂 Importer un fichier Excel")
fichier_excel = st.sidebar.file_uploader("Sélectionnez un fichier (.xlsx)", type=["xlsx"])

if fichier_excel is not None:
    contenu = lire_fichier_excel(fichier_excel)
    if contenu:
        mapping_pd = recuperer_correspondance_pd(contenu)

        if "Portfolio" in contenu:
            df_portfolio = contenu["Portfolio"]
            df_portfolio.columns = df_portfolio.columns.str.strip()

            st.subheader("🔍 Aperçu du Portefeuille de Crédits")
            st.dataframe(df_portfolio.head(10))

            if "Exposure" in df_portfolio.columns:
                st.subheader("📊 Répartition des Montants Exposés")
                histo = alt.Chart(df_portfolio).mark_bar().encode(
                    alt.X("Exposure:Q", bin=alt.Bin(maxbins=30), title="Montant Exposé (€)"),
                    alt.Y("count()", title="Nombre de crédits"),
                    tooltip=["count()"]
                ).properties(title="Distribution des Montants Exposés")
                st.altair_chart(histo, use_container_width=True)

        else:
            st.error("⚠ La feuille 'Portfolio' est absente du fichier.")
    else:
        st.error("Erreur lors du chargement du fichier.")
else:
    st.info("📢 Veuillez importer un fichier Excel.")

# --------------------------
# Paramètres de simulation
# --------------------------
st.markdown("## ⚙ Paramètres de la Simulation")

default_taux_annuel = 0.05
default_duree = 3.0  

with st.form("formulaire_parametres"):
    taux_annuel = st.number_input("Taux d'intérêt annuel", value=default_taux_annuel, step=0.001, format="%.3f")
    duree = st.number_input("Durée du crédit (années)", value=default_duree, step=1.0)
    bouton_valider = st.form_submit_button("✅ Appliquer")
    if bouton_valider:
        st.success(f"✅ Paramètres mis à jour : {taux_annuel:.3f} - {duree} ans")

# --------------------------
# Évaluation d'un crédit
# --------------------------
st.markdown("## 🔍 Évaluation d'un Crédit")

with st.form("formulaire_credit"):
    id_credit = st.text_input("ID du crédit à analyser")
    bouton_calculer = st.form_submit_button("📊 Lancer l'analyse")

if bouton_calculer:
    if fichier_excel is None:
        st.error("❌ Aucun fichier chargé.")
    elif "Portfolio" not in contenu:
        st.error("⚠ La feuille 'Portfolio' est introuvable.")
    elif id_credit == "":
        st.error("⚠ Veuillez entrer un ID.")
    else:
        try:
            id_credit = int(id_credit)
            credit_data = df_portfolio[df_portfolio["Id"] == id_credit]
            if credit_data.empty:
                st.error(f"⚠ Aucun crédit trouvé pour l'ID {id_credit}.")
            else:
                credit = credit_data.iloc[0]
                resultat = evaluer_credit(credit, taux_annuel, duree, mapping_pd)
                if resultat:
                    st.markdown("### 📋 Résultats de l'Évaluation")
                    st.write(f"**Montant Exposé :** {resultat['Montant']:,.2f} €")
                    st.write(f"**Probabilité de Défaut Annuelle :** {resultat['PD_Annuelle']:.4%}")
                    st.write(f"**Perte Estimée :** {resultat['Perte_Estimee']:,.2f} €")
                    st.write(f"**Profit Net :** {resultat['Profit']:,.2f} €")
        except Exception as e:
            st.error(f"❌ Erreur lors de l'analyse du crédit : {e}")
