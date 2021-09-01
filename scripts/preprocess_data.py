import pandas as pd
import numpy as np
import upload_data


correspondance_reg_dp = pd.read_csv(
    'https://www.data.gouv.fr/fr/datasets/r/efb60a2c-c27b-46a5-89a7-9ca4ffc3ebd5',
    sep=';')  #Dataframe région <-> départements


def make_str_out_of_dep(
        df):  #transforme le type dans les colonnes département en type str
    return df.dep.astype('str')



def hosp_rea():
    """
    Returns the dataframe with the columns:
    - department
    - rea : Nombre de personnes actuellement en services de réanimations ou de soins intensifs
    - rad : Nombre cumulés de personnes retournées à domicile
    - dc : Nombre cumulé de personnes décédées à l'hôpital

    1st day: 2020-03-18
    """
    df = pd.read_csv('raw_data/Actual/rea_dc_cumul.csv', sep=';')
    df = df.drop(columns=['HospConv', 'SSR_USLD', 'autres', 'sexe'])
    df.columns = ['dep', 'date', 'hosp', 'rea', 'rad', 'dc']
    df.dep = make_str_out_of_dep(df)
    dico = {}
    for i in set(df['dep'].values):
        dico[i] = df[df['dep'] == i]
    for dep in dico.keys():
        dico[dep] = dico[dep].groupby(by='date').sum()
        dico[dep]['dep'] = dep
    lf = pd.DataFrame()
    for dep in dico.keys():
        lf = pd.concat([lf, dico[dep]])

    return lf.reset_index()


def hosp_rea_1():
    """Returns the dataframe with the columns:
    - department
    - incid_rea : Nombre quotidien de personnes nouvellement hospitalisées
    - incid_dc : Nombre quotidien de personnes nouvellement décedées
    - incid_rad : Nombre quotidien de nouveaux retours à domicile
    """
    df = pd.read_csv('raw_data/Actual/rea_dc_journalier.csv', sep=';')
    df.dep = make_str_out_of_dep(df)

    return df


def hosp_rea_2():
    """Returns df with:
    - department
    - nb: nombre cumulé de services hospitaliers ayant eu au mois un cas
    """
    df = pd.read_csv('raw_data/Actual/service_au_moins_un_cas_cumul.csv',
                     sep=';')
    df.dep = make_str_out_of_dep(df)
    dico = {}
    for i in set(df['dep'].values):
        dico[i] = df[df['dep'] == i]
    for dep in dico.keys():
        dico[dep] = dico[dep].groupby(by='jour').sum()
        dico[dep]['dep'] = dep
    lf = pd.DataFrame()
    for dep in dico.keys():
        lf = pd.concat([lf, dico[dep]])

    return lf.reset_index()


def incidence():
    """Returns df with:
    - Classes d'âge
    - Departement
    - Population de la classe d'âge
    - Nombre de cas positifs par classe d'âge et département
    """
    df = pd.read_csv(('raw_data/Actual/quotidien_departement_classe_age.csv'), sep=';')
    df.columns = ['dep','date','nbre_tests_positifs','classe_age','population']
    df['population'] = df['population'].map(lambda col: int(col))

    df.dep = make_str_out_of_dep(df)
    return df


def incidence_france():
    """
    Début: 13-05-2021

    Retourne à l'échelle de la france
    - Nombre tests positifs femme
    - Nombre tests positifs homme
    - Nombre tests positifs total
    - Population féminine totale
    - Population homme totale
    - Classe d'âge
    - Population de la classe d'âge
    """
    df = pd.read_csv('raw_data/Actual/quotidien_france.csv', sep=';')
    df = df.drop(columns=['fra'])
    df.columns = [
        'date', 'test_positifs_femmes', 'tests_positifs_hommes',
        'tests_positifs_tot', 'pop_femme', 'pop_homme', 'classe_age',
        'population'
    ]
    df['zone'] = 'fr'
    return df


def incidence_std_dep():
    """
    Début: 13-05-2020
    Retourne:
    - dep
    - date
    - Population
    - nombre de tests positifs par jours
    - Taux d'incidence standardisé

    """

    df = pd.read_csv('raw_data/Actual/incidence_std_quotidien_departement.csv',
                     sep=';')
    df.columns = [
        'dep', 'date', 'population', 'nbre_tests_positifs',
        'taux_incidence_std'
    ]
    df.dep = make_str_out_of_dep(df)
    return df


def incidence_std_fr():
    """
    Début: 2020-05-13

    Returns:
    - date
    - population
    - nbre_tests_positifs
    - taux incidence standardisé
    """
    df = pd.read_csv('raw_data/Actual/incidence_std_quotidien_france.csv', sep=';')
    df.columns = [
        'zone','date', 'population', 'nbre_tests_positifs', 'taux_incidence_std'
    ]
    df['zone'] = df['zone'].map(lambda col : col.lower())

    return df


def vaccination_dep():
    """
    Début: 2020-12-27

    Returns:
    - nombre première dose et nombre cumulé première dose
    - nombre deuxième dose et nombre cumulé deuxième dose
    """
    df = pd.read_csv('raw_data/Actual/nbre_vacc_dep.csv', sep=';')
    df.columns = [
        'dep', 'date', 'nbre_dose_1', 'nbre_dose_complet', 'nbre_cum_dose_1',
        'nbre_cum_complet', 'couverture_dose1', 'couverture_complete'
    ]
    df.dep = make_str_out_of_dep(df)

    return df


def presence_mutant():
    df = pd.read_csv('raw_data/Actual/presence_mutant.csv',sep = ';')
    df['fra'] = df['fra'].map(lambda col: col.lower())
    df = df.drop(columns = ['nb_crib'])
    df['semaine'] = df['semaine'].map(lambda col: col[:10])
    df.columns = ['zone','date','nbre_positif','taux_crib','nbre_A0','nbre_A1','taux_A1',
                  'nbre_B0','nbre_B1','taux_B1','nbre_C0','nbre_C1','taux_C1']
    return df
