import pandas as pd
from darts.timeseries import TimeSeries as TS
import numpy as np
import os
from datetime import date
from preprocess_data import *
from egbz.utils import *
"""
==========================================================================================================================================================

Lien des données hospitalières = https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/

Lien taux d'incidence = https://www.data.gouv.fr/fr/datasets/taux-dincidence-de-lepidemie-de-covid-19/

Lien Vaccination = https://static.data.gouv.fr/resources/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/20210825-190608/donnees-hospitalieres-covid19-2021-08-25-19h06.csv

Lien mutant = https://www.data.gouv.fr/fr/datasets/donnees-de-laboratoires-pour-le-depistage-indicateurs-sur-les-mutations/

Lien variant = https://www.data.gouv.fr/fr/datasets/donnees-de-laboratoires-pour-le-depistage-indicateurs-sur-les-variants/

Lien variant = https://www.data.gouv.fr/fr/datasets/donnees-de-laboratoires-pour-le-depistage-indicateurs-sur-les-mutations/

==========================================================================================================================================================
"""

############################# API ##################################





link_hospitals = {
    "rea_dc_cumul":
    'https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7',
    "rea_dc_journalier":
    'https://www.data.gouv.fr/fr/datasets/r/6fadff46-9efd-4c53-942a-54aca783c30c',
    "service_au_moins_un_cas_cumul":
    'https://www.data.gouv.fr/fr/datasets/r/41b9bd2a-b5b6-4271-8878-e45a8902ef00'
}

link_incidence = {
    "quotidien_departement_classe_age":
    'https://www.data.gouv.fr/fr/datasets/r/19a91d64-3cd3-42fc-9943-d635491a4d76',
    'quotidien_france':
    'https://www.data.gouv.fr/fr/datasets/r/57d44bd6-c9fd-424f-9a72-7834454f9e3c',
    "incidence_std_quotidien_departement":
    'https://www.data.gouv.fr/fr/datasets/r/4180a181-a648-402b-92e4-f7574647afa6',
    "incidence_std_quotidien_france":
    "https://www.data.gouv.fr/fr/datasets/r/59ad717b-b64e-4779-85f6-cd1b25b24703"
}

link_vaccination = {
    "nbre_vacc_dep":
    'https://www.data.gouv.fr/fr/datasets/r/f77106ed-6e27-48cf-85b7-daad2b7fce1e'
}

link_mutant = {
    'presence_mutant':
    'https://www.data.gouv.fr/fr/datasets/r/848debc4-0e42-4e3b-a176-afc285ed5401'
}

links = [link_hospitals,link_incidence,link_vaccination,link_mutant]  #rajouter les liens manquants !!!!!!!


today = date.today().strftime("%d_%m_%Y") #La date d'aujourd'hui

source = 'raw_data/Actual'
destination = 'raw_data/History'
maison_data = 'raw_data'
maison_raw_data = 'data'

if not os.access(maison_data, os.F_OK):
    os.mkdir(maison_data)
if not os.access(maison_raw_data, os.F_OK):
    os.mkdir(maison_raw_data)

if not os.access(source, os.F_OK) or 'rea_dc_cumul.csv' not in os.listdir(source) or \
    np.array(pd.read_csv(link_hospitals['rea_dc_cumul'], sep=';')['jour'])[-1] != \
    np.array(pd.read_csv('raw_data/Actual/rea_dc_cumul.csv',sep=';')['jour'])[-1] :


    #si le dir. Actual est vide, n'existe pas ou n'est pas à jour,
    # on lance le téléchargement des tableaux sinon rien
    if not os.access(source,os.F_OK):
        os.mkdir(source)
    if not os.access(destination,os.F_OK):
        os.mkdir(destination)

    if os.listdir(source) != []:                                                             #Si le répo. History existe et que Actual n'est pas vide

        os.system(f'cp -R {source} {destination}')                                           #On copie le dossier Actual dans le dossier History
        os.rename('raw_data/History/Actual',f'raw_data/History/in_history_on_{today}')                             #On le renomme en lui ajoutant la date du téléchargement
        os.system(f'rm -rf {source}')                                                        #On supprime le dossier Actual car son contenu a été copié (on évite une boucle sur les fichiers dans Actual)
        os.mkdir(source)                                                                         #On recréé le dossier Actual qu'on a supprimé ci-dessus


    for link in links:                                                                       #On télécharge lestableaux actualisés dans Actual
        for data_name, url in link.items():
            os.system(f"touch raw_data/Actual/{data_name}.csv")
            os.system(
                f"curl --silent {url} -L > 'raw_data/Actual/{data_name}.csv' ")

today_date = today
