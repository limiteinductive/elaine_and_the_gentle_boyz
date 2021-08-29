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
    'https://static.data.gouv.fr/resources/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/20210826-190901/donnees-hospitalieres-covid19-2021-08-26-19h09.csv',
    "rea_dc_journalier":
    'https://static.data.gouv.fr/resources/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/20210826-190859/donnees-hospitalieres-nouveaux-covid19-2021-08-26-19h08.csv',
    "service_au_moins_un_cas_cumul":
    'https://static.data.gouv.fr/resources/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/20210826-190903/donnees-hospitalieres-etablissements-covid19-2021-08-26-19h09.csv'
}

link_incidence = {
    "quotidien_departement_classe_age":
    'https://static.data.gouv.fr/resources/taux-dincidence-de-lepidemie-de-covid-19/20210826-190514/sp-pe-tb-quot-dep-2021-08-26-19h05.csv',
    'quotidien_france':
    'https://static.data.gouv.fr/resources/taux-dincidence-de-lepidemie-de-covid-19/20210826-190517/sp-pe-tb-quot-fra-2021-08-26-19h05.csv',
    "incidence_std_quotidien_departement":
    "https://static.data.gouv.fr/resources/taux-dincidence-de-lepidemie-de-covid-19/20210826-190507/sp-pe-std-quot-dep-2021-08-26-19h05.csv",
    "incidence_std_quotidien_france":
    "https://static.data.gouv.fr/resources/taux-dincidence-de-lepidemie-de-covid-19/20210826-190509/sp-pe-std-quot-fra-2021-08-26-19h05.csv"
}

link_vaccination = {
    "nbre_vacc_dep":
    'https://www.data.gouv.fr/fr/datasets/r/f77106ed-6e27-48cf-85b7-daad2b7fce1e'
}

link_mutant = {
    'presence_mutant':
    'https://www.data.gouv.fr/fr/datasets/r/848debc4-0e42-4e3b-a176-afc285ed5401'
}

links = [link_hospitals, link_incidence]  #rajouter les liens manquants !!!!!!!


today = date.today().strftime("%d_%m_%Y") #La date d'aujourd'hui

source = 'raw_data/Actual'
destination = 'raw_data/History'
maison_data = 'raw_data'
maison_raw_data = 'data'

if not os.access(maison_data, os.F_OK):
    os.mkdir(maison_data)
if not os.access(maison_raw_data, os.F_OK):
    os.mkdir(maison_raw_data)

if not os.access(source, os.F_OK) or os.listdir(source) == [] or \
    np.array(pd.read_csv(link_incidence['quotidien_france'], sep=';')['jour'])[-1] != \
    np.array(pd.read_csv('raw_data/Actual/quotidien_france.csv',sep=';')['jour'])[-1] :


        #si le dir. Actual est vide, n'existe pas ou n'est pas à jour,
        # on lance le téléchargement des tableaux sinon rien
    if not os.access(source,os.F_OK):
        os.mkdir(source)
    if not os.access(destination,os.F_OK):
        os.mkdir(destination)

    if os.listdir(source) != []:                                                             #Si le répo. History existe et que Actual n'est pas vide

        os.system(f'cp -R {source} {destination}')                                           #On copie le dossier Actual dans le dossier History
        os.rename('raw_data/History/Actual',f'raw_data/History/data_uploaded_{today}')       #On le renomme en lui ajoutant la date du téléchargement
        os.system(f'rm -rf {source}')                                                        #On supprime le dossier Actual car son contenu a été copié (on évite une boucle sur les fichiers dans Actual)
        os.mkdir(source)                                                                         #On recréé le dossier Actual qu'on a supprimé ci-dessus


    for link in links:                                                                       #On télécharge lestableaux actualisés dans Actual
        for data_name, url in link.items():
            os.system(f"touch raw_data/Actual/{data_name}.csv")
            os.system(
                f"curl --silent {url} > 'raw_data/Actual/{data_name}.csv' ")

today_date = today