import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from scipy.stats import norm

# --------------------------
# Configuration de l'application
# --------------------------
st.set_page_config(page_title="Simulation Monte Carlo - Options", layout="wide")
st.title("📈 Simulation de Pricing d'Options")
st.markdown("""
Cette application utilise la **méthode Monte Carlo** pour estimer le prix de différentes options financières.
Vous pouvez tester les options suivantes :
- 📌 **Call Européen**
- 📌 **Put Européen**
- 📌 **Option Tunnel** (payoff valide uniquement si le sous-jacent reste dans un intervalle défini)
- 📌 **Option Himalaya** (calculée sur le maximum atteint par l’actif)
- 📌 **Option Napoléon** (calculée sur le minimum atteint)
""")

# --------------------------
# Paramètres de la simulation
# --------------------------
with st.form("parametres_option"):
    col_gauche, col_droite = st.columns(2)
    with col_gauche:
        prix_initial = st.number_input("Prix initial de l’actif (S0)", value=100.0, step=1.0)
        taux_sans_risque = st.number_input("Taux sans risque (r)", value=0.05, step=0.001, format="%.3f")
        volatilite = st.number_input("Volatilité (σ)", value=0.2, step=0.01, format="%.2f")
    with col_droite:
        maturite = st.number_input("Durée avant échéance (T en années)", value=1.0, step=0.1, format="%.1f")
        nb_pas = st.number_input("Nombre de subdivisions du temps", value=252, step=1)
        nb_simulations = st.number_input("Nombre de trajectoires simulées", value=10000, step=1000)

    type_option = st.selectbox("Sélectionner le type d’option", 
                               ("Call Européen", "Put Européen", "Option Tunnel", "Option Himalaya", "Option Napoléon"))
    prix_exercice = st.number_input("Prix d'exercice (Strike, K)", value=100.0, step=1.0)

    if type_option == "Option Tunnel":
        borne_basse = st.number_input("Borne inférieure", value=80.0, step=1.0)
        borne_haute = st.number_input("Borne supérieure", value=120.0, step=1.0)
    else:
        borne_basse, borne_haute = None, None

    bouton_simulation = st.form_submit_button("📊 Lancer la simulation")

# --------------------------
# Simulation des trajectoires et calcul du payoff
# --------------------------
if bouton_simulation:
    delta_t = maturite / nb_pas  # pas de temps

    # Matrice des trajectoires
    trajectoires = np.zeros((int(nb_simulations), int(nb_pas) + 1))
    trajectoires[:, 0] = prix_initial

    # Génération des mouvements aléatoires
    for t in range(1, int(nb_pas) + 1):
        aleatoire = np.random.normal(0, 1, int(nb_simulations))
        trajectoires[:, t] = trajectoires[:, t - 1] * np.exp(
            (taux_sans_risque - 0.5 * volatilite**2) * delta_t + volatilite * np.sqrt(delta_t) * aleatoire
        )

    # Calcul des gains en fonction du type d’option sélectionné
    if type_option == "Call Européen":
        gains = np.maximum(trajectoires[:, -1] - prix_exercice, 0)
    elif type_option == "Put Européen":
        gains = np.maximum(prix_exercice - trajectoires[:, -1], 0)
    elif type_option == "Option Tunnel":
        respect_tunnel = np.all((trajectoires >= borne_basse) & (trajectoires <= borne_haute), axis=1)
        gains = np.where(respect_tunnel, np.maximum(trajectoires[:, -1] - prix_exercice, 0), 0)
    elif type_option == "Option Himalaya":
        valeur_max = np.max(trajectoires, axis=1)
        gains = np.maximum(valeur_max - prix_exercice, 0)
    elif type_option == "Option Napoléon":
        valeur_min = np.min(trajectoires, axis=1)
        gains = np.maximum(prix_exercice - valeur_min, 0)
    else:
        gains = np.zeros(int(nb_simulations))

    # Actualisation des gains pour obtenir le prix de l’option
    gains_actualises = np.exp(-taux_sans_risque * maturite) * gains
    prix_estime = np.mean(gains_actualises)

    # Calcul de l’erreur à 99% de confiance
    erreur_standard = np.std(gains_actualises) / np.sqrt(nb_simulations)
    z_99 = norm.ppf(0.995)  
    erreur_conf = z_99 * erreur_standard

    # Suivi de la convergence des estimations
    convergence_moyenne = np.cumsum(gains_actualises) / np.arange(1, int(nb_simulations) + 1)
    df_convergence = pd.DataFrame({
        "Itérations": np.arange(1, int(nb_simulations) + 1),
        "Prix moyen estimé": convergence_moyenne
    })

    # --------------------------
    # Affichage des résultats
    # --------------------------
    st.subheader("📊 Résultats de la Simulation")
    st.write(f"**Prix estimé de l’option ({type_option})** : {prix_estime:,.2f} €")
    st.write(f"**Intervalle d'erreur à 99%** : ± {erreur_conf:,.2f} €")

    # Graphique de convergence du prix
    st.subheader("📉 Convergence du Prix de l’Option")
    convergence_graph = alt.Chart(df_convergence).mark_line().encode(
        x=alt.X("Itérations:Q", title="Nombre de simulations"),
        y=alt.Y("Prix moyen estimé:Q", title="Prix moyen (€)")
    ).properties(title="Évolution de l'estimation du prix de l’option")
    st.altair_chart(convergence_graph, use_container_width=True)

    # Histogramme des payoffs actualisés
    st.subheader("📊 Distribution des Payoffs")
    df_payoff = pd.DataFrame({"Payoff actualisé": gains_actualises})
    hist_payoff = alt.Chart(df_payoff).mark_bar().encode(
        x=alt.X("Payoff actualisé:Q", bin=alt.Bin(maxbins=30), title="Payoff actualisé (€)"),
        y=alt.Y("count()", title="Nombre d’occurrences")
    ).properties(title="Répartition des payoffs actualisés")
    st.altair_chart(hist_payoff, use_container_width=True)
