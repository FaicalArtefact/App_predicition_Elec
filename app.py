from flask import Flask, request, render_template
import numpy as np
import pickle
import pandas as pd
import os

# Créer l'application Flask
app = Flask(__name__)

# Charger le modèle sauvegardé
with open('model_entr.pkl', 'rb') as file:
    model = pickle.load(file)

# Charger le scaler
with open('scale_entr.pkl', 'rb') as file:
    scaler = pickle.load(file)

# Route pour afficher le formulaire HTML
@app.route('/')
def home():
    return render_template('index.html')

# Route pour recevoir les données du formulaire et faire des prédictions
@app.route('/predict', methods=['POST'])
def predict():
    # Récupérer les données du formulaire
    s_geom_groupe = float(request.form['s_geom_groupe'])
    hauteur_mean = float(request.form['hauteur_mean'])
    max_hauteur = float(request.form['max_hauteur'])
    altitude_sol_mean = float(request.form['altitude_sol_mean'])
    nb_pdl_res = float(request.form['nb_pdl_res'])
    nb_niveau = float(request.form['nb_niveau'])
    annee_construction = float(request.form['annee_construction'])
    nb_log = float(request.form['nb_log'])
    code_departemental = int(request.form['code_départemental'])
    
   
    #Créer les features pour scaler sauf code_departemental
    ma_liste = [[s_geom_groupe, hauteur_mean, max_hauteur, altitude_sol_mean, nb_pdl_res, nb_niveau, annee_construction, nb_log]]
    
    print(ma_liste)

    features_to_scale = pd.DataFrame(ma_liste, columns=['s_geom_groupe', 'hauteur_mean', 'max_hauteur', 'altitude_sol_mean', 'nb_pdl_res', 'nb_niveau', 'annee_construction', 'nb_log'])
    
    print(features_to_scale)
    
    features_scaled = pd.DataFrame(  
    scaler.transform(features_to_scale),
    columns= ['s_geom_groupe', 'hauteur_mean',
       'max_hauteur', 'altitude_sol_mean', 'nb_pdl_res', 
       'nb_niveau', 'annee_construction', 'nb_log'])
    
    print(features_scaled)
    
    # Concaténer la feature non-scalée (code_departemental)
    features_scaled['code_départemental']=[code_departemental]
    
    print(features_scaled)
    
    prediction = model.predict(features_scaled)
    
    print(prediction)
    
    # Retourner la prédiction à la page HTML
    return render_template('index.html', prediction=prediction[0])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)), debug=True)

