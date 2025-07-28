import streamlit as st
import pandas as pd



import base64

hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 1rem;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def add_bg_from_local(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    css = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)

# Appelle la fonction avec le chemin vers ton image locale
add_bg_from_local("Diapositive1.PNG")

st.title("Analyse des chiffres employés")

# Étape 1 : Upload des fichiers Excel
fichier1 = st.file_uploader("📁 Fichier .xlsx des programmes par semaines", type=["xlsx"])
fichier2 = st.file_uploader("📁 Fichier .xlsx des programmes par employés", type=["xlsx"])

# Champs de saisie affichés dès le départ
semaine_de_travail = st.text_input("📆 Saisis la semaine à traiter (ex: Week 01)", key="saisie_semaine").strip()
selection_employes = st.text_input("📆 Saisis les noms des employés (ex: MONIKA, CATHERINE)", key="saisie_employes").strip()

if fichier1 and fichier2:
    
    # Lecture des fichiers Excel
    df = pd.read_excel(fichier1)
    dfr = pd.read_excel(fichier2)
    st.success("✅ Fichiers bien chargés")

    colonne_weeks = df["Weeks"].tolist()

    # Construction des dictionnaires de semaines
    D_wk = {'Week 00':[0,0]}
    s = 1
    for i in range(1, len(colonne_weeks)):
        if str(colonne_weeks[i]).startswith("Week"):
            D_wk[colonne_weeks[i]] = [i, s]
            s += 1

    # Associer chaque semaine à un intervalle d’index
    clefs = list(D_wk.keys())
    D_wk_utilisable = {
        clefs[i + 1]: [D_wk[clefs[i]][0], D_wk[clefs[i + 1]][0]]
        for i in range(0,len(clefs) - 1)
    }

    

    if semaine_de_travail in D_wk_utilisable:
        # Filtrer les programmes pour la semaine choisie
        programs = df["Program"].tolist()[D_wk_utilisable[semaine_de_travail][0]:D_wk_utilisable[semaine_de_travail][1]]

        programs_sorted = []
        for i in programs:
            if 'Sgp' in str(i) or 'Abu' in str(i) or 'SGP' in str(i) : 
                programs_sorted.append('null')
            else:
                programs_sorted.append(i)

        if selection_employes:
            names = [nom.strip() for nom in selection_employes.split(',')]
            if all(nom in dfr.columns for nom in names): 
                liste_names = []
                for i in range(len(names)):
                    liste_names.append([str(s).split()[0] for s in dfr[names[i]].tolist()])

            # Dictionnaire des comptes
                L_D = []
                for i in liste_names:
                    chiffre_par_programme = {j: 0 for j in i}
                    L_D.append(chiffre_par_programme)

                
                # Liste des paires conflictuelles à ne pas mélanger
                conflits = [("CS", "CSB"),("LT", "LTP")]

                for i in programs_sorted:
                    for x in L_D:
                        for j in x:
                            match_valide = False

            # Vérifie s’il y a un conflit connu
                            est_conflit = any(
                                str(j).upper() == c1 and str(i).upper().startswith(c2)
                                for c1, c2 in conflits
                            )

                            if est_conflit:
                                continue  # on saute ce cas

            # Sinon, on utilise startswith classique
                            if str(i).lower().startswith(str(j).lower()):
                                x[j] += 1


                D_chiffres_finaux = {}
                for i in range(len(names)):
                    total = sum(L_D[i][j] for j in L_D[i] if j != 'nan')
                    D_chiffres_finaux[names[i]] = total

                L_Propre=[]
                for i in L_D:
                    D={}
                    for j in i:
                        if j!= 'nan' and i[j]!=0:
                            D[j]=i[j]
                    L_Propre.append(D)


                st.write("📊 Résultats :")
                s=0
                for cle, valeur in D_chiffres_finaux.items():
                    details = ', '.join(f"{k} : {v}" for k, v in L_Propre[s].items())
                    st.markdown(f"- **{cle}** : {valeur}. ℹ️ Le détail est le suivant : {details}")

                    s+=1
            else:
                st.error(f"❌ Un.e employé.e n'existe pas")

    elif semaine_de_travail != "":
        st.error(f"❌ La semaine '{semaine_de_travail}' n'est pas reconnue. Veuillez choisir parmi : {list(D_wk_utilisable.keys())}")
else:
    st.info("📥 Veuillez d'abord charger les deux fichiers Excel pour commencer.")
