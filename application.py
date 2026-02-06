"""
📝 **Instructions** :
- Installez toutes les bibliothèques nécessaires en fonction des imports présents dans le code, utilisez la commande suivante :conda create -n projet python pandas numpy ..........
- Complétez les sections en écrivant votre code où c’est indiqué.
- Ajoutez des commentaires clairs pour expliquer vos choix.
- Utilisez des emoji avec windows + ;
- Interprétez les résultats de vos visualisations (quelques phrases).
"""

### 1. Importation des librairies et chargement des données
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

# Chargement des données
df = pd.read_csv("data/ds_salaries.csv")


### 2. Exploration visuelle des données
#votre code 
st.title("📊 Visualisation des Salaires en Data Science")
st.markdown("Explorez les tendances des salaires à travers différentes visualisations interactives.")

if st.checkbox("Afficher un aperçu des données"):
    st.write(df.head(10))
    st.info(f"Le dataset contient {df.shape[0]} lignes et {df.shape[1]} colonnes.")

#Statistique générales avec describe pandas 
#votre code 
st.subheader("📌 Statistiques générales")
st.write(df.describe(), "On peut voir la dispersion des salaires (moyenne, écart-type) et les quartiles. Cela permet de repérer les différentes valeurs aberrantes ")


### 3. Distribution des salaires en France par rôle et niveau d'expérience, uilisant px.box et st.plotly_chart
#votre code

st.subheader("📈 Distribution des salaires aux Etats-Unis")
# Filtrage sur les USA
df_USA = df[df['company_location'] == 'US']

fig_box = px.box(df_USA, x='job_title', y='salary_in_usd', color='experience_level',
                    title="Salaires aux Etats-Unis par poste et expérience",
                    labels={'salary_in_usd': 'Salaire (USD)', 'job_title': 'Poste'})
st.plotly_chart(fig_box)
st.info("Ce graphique montre que le niveau d'expérience influence fortement la médiane salariale aux Etats-Unis.")

### 4. Analyse des tendances de salaires :
#### Salaire moyen par catégorie : en choisisant une des : ['experience_level', 'employment_type', 'job_title', 'company_location'], utilisant px.bar et st.selectbox 
Option_cate = st.selectbox("Choisissez une catégorie pour analyser le salaire moyen :", 
                          ['experience_level', 'employment_type', 'job_title', 'company_location'])

moy_salary = df.groupby(Option_cate)['salary_in_usd'].mean().sort_values(ascending=False).reset_index()
fig_bar = px.bar(moy_salary, x=Option_cate, y='salary_in_usd', color='salary_in_usd',
                 title=f"Salaire moyen par {Option_cate}")
st.plotly_chart(fig_bar)


### 5. Corrélation entre variables
# Sélectionner uniquement les colonnes numériques pour la corrélation
#votre code 
# Sélectionner uniquement les colonnes numériques
num_df = df.select_dtypes(include=[np.number])

# Calcul de la matrice de corrélation
#votre code

corr_matrice = num_df.corr()

# Affichage du heatmap avec sns.heatmap
#votre code 
st.subheader("🔗 Corrélations entre variables numériques")
fig_corr, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(corr_matrice, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
st.pyplot(fig_corr)
st.write("On regarde si l'année (colonne work_year) ou le ratio de télétravail ont un impact sur le montant du salaire")
st.write("Plus la corrélation est proche de 1 (couleur plus rouge), plus il y a de corrélation entre ces deux variables")

### 6. Analyse interactive des variations de salaire
# Une évolution des salaires pour les 10 postes les plus courants
# count of job titles pour selectionner les postes
# calcule du salaire moyen par an
#utilisez px.line
#votre code 
st.subheader("Évolution des salaires pour les 10 postes les plus courants")
top_10_jobs = df['job_title'].value_counts().nlargest(10).index
df_top_jobs = df[df['job_title'].isin(top_10_jobs)]

# Calcul du salaire moyen par an
evolution_salary = df_top_jobs.groupby(['work_year', 'job_title'])['salary_in_usd'].mean().reset_index()

fig_ligne = px.line(evolution_salary, x='work_year', y='salary_in_usd', color='job_title',
                   title="Évolution du salaire moyen par an (Top 10 jobs)")
st.plotly_chart(fig_ligne)


### 7. Salaire médian par expérience et taille d'entreprise
# utilisez median(), px.bar
#votre code 
st.subheader("Salaire médian par expérience et taille d'entreprise")
median_salaire = df.groupby(['experience_level', 'company_size'])['salary_in_usd'].median().reset_index()
fig_median = px.bar(median_salaire, x='experience_level', y='salary_in_usd', color='company_size',
                    barmode='group', title="Salaire médian par niveau d'expérience et taille d'entreprise")
st.plotly_chart(fig_median)



### 8. Ajout de filtres dynamiques
#Filtrer les données par salaire utilisant st.slider pour selectionner les plages 
#votre code 
st.subheader("Filtrage par plage de salaire")
min_sal, max_sal = int(df['salary_in_usd'].min()), int(df['salary_in_usd'].max())
salaire_range = st.slider("Sélectionnez une plage de salaire (USD) :", min_sal, max_sal, (min_sal, max_sal))

filtered_df = df[(df['salary_in_usd'] >= salaire_range[0]) & (df['salary_in_usd'] <= salaire_range[1])]
st.write(f"Nombre de résultats : {len(filtered_df)}")



### 9.  Impact du télétravail sur le salaire selon le pays
st.subheader("Impact du télétravail sur le salaire")
fig_remote = px.scatter(df, x='remote_ratio', y='salary_in_usd', color='company_location',
                        title="Salaire vs Télétravail par pays", hover_data=['job_title'])
st.plotly_chart(fig_remote)



### 10. Filtrage avancé des données avec deux st.multiselect, un qui indique "Sélectionnez le niveau d'expérience" et l'autre "Sélectionnez la taille d'entreprise"
#votre code 
st.subheader("Filtrage Avancé")
col1, col2 = st.columns(2)

with col1:
    exp_filter = st.multiselect("Sélectionnez le niveau d'expérience :", options=df['experience_level'].unique())
with col2:
    size_filter = st.multiselect("Sélectionnez la taille d'entreprise :", options=df['company_size'].unique())

# Application des filtres
final_df = df.copy()
if exp_filter:
    final_df = final_df[final_df['experience_level'].isin(exp_filter)]
if size_filter:
    final_df = final_df[final_df['company_size'].isin(size_filter)]

st.dataframe(final_df)
