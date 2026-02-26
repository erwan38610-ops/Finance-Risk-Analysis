import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from scipy.stats import norm

# --------------------------
# Chargement du fichier Excel avec mise en cache
# --------------------------
@st.cache_data
def charger_fichier_excel(fichier):
    """Lit un fichier Excel et renvoie un dictionnaire contenant toutes ses feuilles."""
    try:
        contenu = pd.read_excel(fichier, sheet_name=None, engine="openpyxl")
        return contenu
    except Exception as e:
        st.error(f"Erreur lors de l'ouverture du fichier : {e}")
        return None

# --------------------------
# Extraction des probabilités de défaut
# --------------------------
def obtenir_pd(contenu):
    """Récupère les valeurs des probabilités de défaut depuis la feuille 'Params'."""
    if "Params" not in contenu:
        st.error("La feuille 'Params' est absente du fichier.")
        return {}

    df_params = contenu["Params"]
    df_params.columns = df_params.columns.astype(str).str.strip()

    table_pd = df_params.iloc[1:20, 4:8].copy()
    table_pd.columns = ["Notation", "1Y", "3Y", "5Y"]

    def convertir_pourcentage(val):
        """Transforme un pourcentage en décimal."""
        if isinstance(val, str):
            val = val.replace(",", ".").replace("%", "").strip()
        try:
            return float(val) / 100.0
        except Exception:
            return None

    for col in ["1Y", "3Y", "5Y"]:
        table_pd[col] = table_pd[col].apply(convertir_pourcentage)

    return table_pd.set_index("Notation").to_dict("index")

# --------------------------
# Simulation Monte Carlo des pertes du portefeuille
# --------------------------
def simulation_pertes_portefeuille(df_portefeuille, simulations, corr_global, corr_secteur, mapping_pd, horizon):
    """
    Simule les pertes du portefeuille à l’aide d’un modèle de dépendance gaussienne.
    On utilise un facteur de corrélation pour modéliser les relations entre les crédits.
    """
    nb_credits = df_portefeuille.shape[0]

    # Récupération des PD en fonction de la notation et de l'horizon choisi
    PDs = []
    for _, ligne in df_portefeuille.iterrows():
        note = str(ligne["Rating"]).strip()
        horizon_str = f"{int(horizon)}Y" if horizon in [1, 3, 5] else "3Y"
        PDs.append(mapping_pd.get(note, {}).get(horizon_str, 0.0001))
    PDs = np.array(PDs)

    # Extraction des valeurs LGD et des expositions
    LGDs = []
    Exposures = []
    for _, ligne in df_portefeuille.iterrows():
        lgd = ligne["LGD"]
        lgd = float(lgd.replace("%", "").strip()) / 100.0 if isinstance(lgd, str) else float(lgd)
        LGDs.append(lgd)
        Exposures.append(float(ligne["Exposure"]))

    LGDs = np.array(LGDs)
    Exposures = np.array(Exposures)
    total_exposition = np.sum(Exposures)

    # Génération des facteurs aléatoires
    X = np.random.normal(0, 1, size=(simulations, 1))
    Y = np.random.normal(0, 1, size=(simulations, 1))
    epsilon = np.random.normal(0, 1, size=(simulations, nb_credits))
    facteur_idio = np.sqrt(max(0, 1 - corr_global - corr_secteur))

    # Calcul des variables latentes
    Z = np.sqrt(corr_global) * X + np.sqrt(corr_secteur) * Y + facteur_idio * epsilon  

    # Détermination des seuils de défaut
    seuil_defaut = norm.ppf(PDs)

    # Matrice d'indicateurs de défaut
    defaut = (Z < seuil_defaut)

    # Matrice des pertes associées aux crédits en défaut
    pertes_credits = np.outer(np.ones(simulations), Exposures * LGDs)

    # Pertes effectives pour chaque simulation
    pertes_totales = (defaut.astype(float) * pertes_credits).sum(axis=1)

    return pertes_totales, total_exposition

# --------------------------
# Calcul des indicateurs de risque
# --------------------------
def evaluer_risque(pertes, niveau_confiance):
    perte_attendue = np.mean(pertes)
    var = np.quantile(pertes, niveau_confiance)
    expected_shortfall = np.mean(pertes[pertes >= var])
    return perte_attendue, var, expected_shortfall

# --------------------------
# Configuration de l'interface Streamlit
# --------------------------
st.set_page_config(page_title="Simulation Monte Carlo - Risque de Crédit", layout="wide")
st.title("📊 Simulation des Risques de Crédit via Monte Carlo")

st.markdown("""
Cet outil simule les pertes d’un portefeuille de crédits en utilisant un modèle de dépendance gaussienne et 
calcule les indicateurs suivants :
- **Perte attendue (Expected Loss)**
- **Valeur en risque (VaR)**
- **Expected Shortfall (ES)**
""")

# --------------------------
# Importation du fichier Excel
# --------------------------
st.sidebar.header("📂 Importer un fichier Excel")
fichier_excel = st.sidebar.file_uploader("Sélectionnez un fichier Excel", type=["xlsx"])

# --------------------------
# Paramètres de simulation
# --------------------------
st.markdown("## ⚙ Paramètres de Simulation")
with st.form("param_simulation"):
    simulations = st.number_input("Nombre de simulations", value=10000, step=1000)
    niveau_confiance = st.slider("Niveau de confiance (VaR / ES)", 0.90, 0.99, 0.99, 0.01)
    corr_global = st.number_input("Corrélation globale", value=0.2, step=0.01, format="%.2f")
    corr_secteur = st.number_input("Corrélation sectorielle", value=0.1, step=0.01, format="%.2f")
    horizon = st.number_input("Horizon en années", value=3, step=1)

    bouton_lancer = st.form_submit_button("🔄 Lancer la simulation")

# --------------------------
# Exécution de la simulation
# --------------------------
if bouton_lancer:
    if fichier_excel is None:
        st.error("❌ Veuillez importer un fichier Excel.")
    else:
        contenu = charger_fichier_excel(fichier_excel)
        if contenu is None or "Portfolio" not in contenu:
            st.error("⚠ Impossible de trouver la feuille 'Portfolio' dans le fichier.")
        else:
            mapping_pd = obtenir_pd(contenu)
            df_portefeuille = contenu["Portfolio"]
            df_portefeuille.columns = df_portefeuille.columns.str.strip()

            pertes, exposition_totale = simulation_pertes_portefeuille(df_portefeuille, int(simulations), corr_global, corr_secteur, mapping_pd, horizon)
            perte_attendue, var, expected_shortfall = evaluer_risque(pertes, niveau_confiance)

            st.subheader("📊 Résultats de la Simulation")
            st.write(f"**Perte Attendue :** {perte_attendue:,.2f} €")
            st.write(f"**VaR ({niveau_confiance*100:.0f}%) :** {var:,.2f} €")
            st.write(f"**Expected Shortfall (ES) :** {expected_shortfall:,.2f} €")
            st.write(f"**Exposition totale du portefeuille :** {exposition_totale:,.2f} €")

            df_convergence = pd.DataFrame({
                "Simulation": np.arange(1, len(pertes)+1),
                "Perte Moyenne Cumulative": np.cumsum(pertes) / np.arange(1, len(pertes)+1)
            })

            st.subheader("📉 Convergence de la Perte Moyenne")
            st.altair_chart(alt.Chart(df_convergence).mark_line().encode(
                x="Simulation", y="Perte Moyenne Cumulative"
            ), use_container_width=True)
