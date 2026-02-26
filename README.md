# 📊 Quantitative Finance Toolbox - Credit Risk & Option Pricing

Bienvenue sur mon portfolio de finance quantitative. Ce dépôt regroupe trois projets majeurs développés pour simuler, évaluer et piloter les risques financiers à l'aide de **Python** et de simulations de **Monte Carlo**.

---

## 🏗️ Structure du Projet

### 1. Simulation RaRoC (Risk-Adjusted Return on Capital)
[cite_start]Outil interactif de simulation du risque de crédit permettant d'évaluer la rentabilité des prêts accordés aux entreprises[cite: 3].
* [cite_start]**Objectif** : Calculer le profit net ajusté au risque en fonction de la probabilité de défaut (PD) et de la perte en cas de défaut (LGD)[cite: 4].
* [cite_start]**Indicateurs clés** : Revenu d'intérêts, Perte attendue, Profit net[cite: 9, 11, 12].
* [cite_start]**Tech Stack** : Streamlit, Pandas, Altair[cite: 15].

### 2. Simulation Monte Carlo - Risque de Crédit
[cite_start]Application de gestion des risques pour estimer les pertes potentielles d'un portefeuille de crédits via une approche stochastique[cite: 19, 20].
* [cite_start]**Objectif** : Modéliser les dépendances gaussiennes entre les crédits (corrélations sectorielles et globales)[cite: 22].
* [cite_start]**Métriques de risque** : Valeur en Risque (VaR), Expected Shortfall (ES) et Expected Loss[cite: 23].
* [cite_start]**Tech Stack** : NumPy, SciPy, Pandas[cite: 25].

### 3. Pricing d'Options via Monte Carlo
[cite_start]Simulateur de valorisation d'options financières basé sur le mouvement brownien géométrique[cite: 29, 32].
* [cite_start]**Options supportées** : Call/Put Européen, Option Tunnel, Himalaya et Napoléon[cite: 30].
* [cite_start]**Analyse** : Estimation du prix avec intervalle de confiance à 99% et visualisation de la convergence[cite: 36].
* [cite_start]**Tech Stack** : NumPy, SciPy, Altair[cite: 37].

---

## 🛠️ Installation et Utilisation

Chaque projet dispose de sa propre interface **Streamlit**. Pour les lancer localement :

1. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
