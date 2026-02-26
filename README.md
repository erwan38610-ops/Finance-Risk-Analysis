# 📊 Quantitative Finance Toolbox - Credit Risk & Option Pricing

Bienvenue sur mon portfolio de finance quantitative. Ce dépôt regroupe trois projets majeurs développés pour simuler, évaluer et piloter les risques financiers à l'aide de **Python** et de simulations de **Monte Carlo**.

---

## 🏗️ Structure du Projet

### 1. Simulation RaRoC (Risk-Adjusted Return on Capital)
Outil interactif de simulation du risque de crédit permettant d'évaluer la rentabilité des prêts accordés aux entreprises.
* **Objectif** : Calculer le profit net ajusté au risque en fonction de la probabilité de défaut (PD) et de la perte en cas de défaut (LGD).
* **Indicateurs clés** : Revenu d'intérêts, Perte attendue, Profit net.
* **Tech Stack** : Streamlit, Pandas, Altair.

### 2. Simulation Monte Carlo - Risque de Crédit
Application de gestion des risques pour estimer les pertes potentielles d'un portefeuille de crédits via une approche stochastique.
* **Objectif** : Modéliser les dépendances gaussiennes entre les crédits (corrélations sectorielles et globales).
* **Métriques de risque** : Valeur en Risque (VaR), Expected Shortfall (ES) et Expected Loss.
* **Tech Stack** : NumPy, SciPy, Pandas.

### 3. Pricing d'Options via Monte Carlo
Simulateur de valorisation d'options financières basé sur le mouvement brownien géométrique.
* **Options supportées** : Call/Put Européen, Option Tunnel, Himalaya et Napoléon.
* **Analyse** : Estimation du prix avec intervalle de confiance à 99% et visualisation de la convergence.
* **Tech Stack** : NumPy, SciPy, Altair.

---

## 🛠️ Installation et Utilisation

Chaque projet dispose de sa propre interface **Streamlit**. Pour les lancer localement :

1. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
