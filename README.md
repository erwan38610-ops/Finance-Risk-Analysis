# 📊 Quantitative Finance Toolbox - Credit Risk & Option Pricing

Bienvenue sur mon portfolio de finance quantitative. Ce dépôt regroupe trois projets majeurs développés pour simuler, évaluer et piloter les risques financiers à l'aide de **Python** et de simulations de **Monte Carlo**.

---

## 🏗️ Structure du Projet

### 1. Simulation RaRoC (Risk-Adjusted Return on Capital)
[cite_start]Outil interactif de simulation du risque de crédit permettant d'évaluer la rentabilité des prêts accordés aux entreprises[cite: 3].
* [cite_start]**Objectif** : Évaluer la rentabilité ajustée au risque en tenant compte de la probabilité de défaut (PD), de la perte en cas de défaut (LGD) et du rendement attendu[cite: 4].
* [cite_start]**Fonctionnalités** : Calcul automatisé du revenu d'intérêts total, de la probabilité cumulée de défaut, de la perte attendue et du profit net[cite: 9, 10, 11, 12].
* [cite_start]**Technique** : Traitement de données Excel (feuilles Portfolio et Params) via Pandas et interface dynamique développée sous Streamlit[cite: 5, 15].

### 2. Simulation Monte Carlo - Risque de Crédit
[cite_start]Application de gestion des risques pour estimer les pertes potentielles d'un portefeuille de crédits via une approche stochastique[cite: 19].
* [cite_start]**Objectif** : Modéliser les pertes du portefeuille à l'aide d'un modèle de dépendance gaussienne intégrant des corrélations globales et sectorielles entre les crédits[cite: 22].
* [cite_start]**Métriques de risque** : Calcul et suivi de la Valeur en Risque (VaR), de l'Expected Shortfall (ES) et de la Perte Attendue (Expected Loss)[cite: 23, 24].
* [cite_start]**Technique** : Simulations statistiques avec NumPy/SciPy et visualisation de la convergence de la perte moyenne avec Altair[cite: 25].

### 3. Pricing d'Options via Monte Carlo
[cite_start]Simulateur de valorisation d'options financières basé sur une modélisation stochastique du prix d'un actif sous-jacent[cite: 29, 31].
* [cite_start]**Options supportées** : Pricing de Call/Put Européens et d'options exotiques telles que l'Option Tunnel, l'Option Himalaya et l'Option Napoléon[cite: 30].
* [cite_start]**Méthodologie** : Génération de trajectoires via le mouvement brownien géométrique en prenant en compte le taux sans risque, la volatilité et l'actualisation des payoffs[cite: 32, 34].
* [cite_start]**Analyse** : Estimation du prix avec un intervalle d'erreur à 99% et suivi dynamique de la convergence du prix moyen[cite: 36].

---

## 🛠️ Installation et Utilisation

Chaque projet dispose de sa propre interface **Streamlit**. Pour les lancer localement :

1. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
