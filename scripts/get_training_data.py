from egbz.utils import *
import os
import joblib
from process import *
from upload_data import *
from preprocess_data import *


training_path = 'data/training_data'
processed_dataframe_path = 'data/processed_dataframes'


if not os.access(training_path, os.F_OK):  #si le path n'existe pas
    os.mkdir(training_path)

df_incid_std_dep = pd.read_csv(
    f'{processed_dataframe_path}/incidence_std_quotidien_departement.csv')
df_rea_dc_cumul = pd.read_csv(f'{processed_dataframe_path}/rea_dc_cumul.csv')
df_rea_dc_quo = pd.read_csv(
    f'{processed_dataframe_path}/rea_dc_journalier.csv')
df_service_un_cas_cumul = pd.read_csv(
    f'{processed_dataframe_path}/service_au_moins_un_cas_cumul.csv')
df_quo_dep_age= pd.read_csv(
    f'{processed_dataframe_path}/quotidien_departement_classe_age.csv')
df_quo_france = pd.read_csv(
    f'{processed_dataframe_path}/quotidien_france.csv')
df_incid_quo_std_france = pd.read_csv(
    f'{processed_dataframe_path}/incidence_std_quotidien_france.csv')
#df_vaccination_dep = vaccination_dep()

dataset_incid_std_dep= create_dataset(
    df_incid_std_dep, zone_col='dep', time_col='date')

dataset_rea_dc_cumul = create_dataset(
    df_rea_dc_cumul, zone_col = 'dep', time_col = 'date'
)

dataset_rea_dc_quo = create_dataset(df_rea_dc_quo, zone_col = 'dep', time_col = 'time',)

joblib.dump(dataset_incid_std_dep, f'{training_path}/incid_std_departement.pkl')
#joblib.dump(dataset_hosp_rea, f'{training_path}/hosp_rea')
