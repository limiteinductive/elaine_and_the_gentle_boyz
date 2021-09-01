import pandas as pd
from preprocess_data import *
import os





processed_dataframe_path = 'data/processed_dataframes'


if not os.access(processed_dataframe_path, os.F_OK):  #si le path n'existe pas
    os.mkdir(processed_dataframe_path)




hosp_rea_1().to_csv(f'{processed_dataframe_path}/rea_dc_journalier.csv',index = False)

hosp_rea_2().to_csv(
        f'{processed_dataframe_path}/service_au_moins_un_cas_cumul.csv', index = False)

incidence().to_csv(
        f'{processed_dataframe_path}/quotidien_departement_classe_age.csv',index = False)
incidence_france().to_csv(
        f'{processed_dataframe_path}/quotidien_france.csv', index = False)
incidence_std_dep().to_csv(
        f'{processed_dataframe_path}/incidence_std_quotidien_departement.csv', index = False)
incidence_std_fr().to_csv(
        f'{processed_dataframe_path}/incidence_std_quotidien_france.csv', index = False)

vaccination_dep().to_csv(f'{processed_dataframe_path}/nbre_vacc_dep.csv',index = False)

hosp_rea().to_csv(
    f'{processed_dataframe_path}/rea_dc_cumul.csv', index = False )

presence_mutant().to_csv(f'{processed_dataframe_path}/presence_mutant.csv', index = False)
