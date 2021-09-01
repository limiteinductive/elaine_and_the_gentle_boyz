from egbz.utils import *
import os
import joblib
from process import *
from upload_data import *
from preprocess_data import *


training_path = 'data/training_data' #à changer en training_data
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

df_vaccination_dep = pd.read_csv(
    f'{processed_dataframe_path}/nbre_vacc_dep.csv')

df_mutant = pd.read_csv(f'{processed_dataframe_path}/presence_mutant.csv')



dataset_incid_std_dep= create_dataset(
    df_incid_std_dep, zone_col='dep', time_col='date')

dataset_rea_dc_cumul = create_dataset(
    df_rea_dc_cumul, zone_col = 'dep', time_col = 'date'
)

dataset_rea_dc_quo = create_dataset(df_rea_dc_quo,
                                    zone_col = 'dep',
                                    time_col = 'jour')

dataset_service_un_cas_cumul = create_dataset(df_rea_dc_quo,
                                              zone_col='dep',
                                              time_col='jour')

dataset_quo_dep_age = create_dataset(df_quo_dep_age,
                                     zone_col='dep',
                                     cat_cols='classe_age',
                                     time_col='date')

dataset_quo_france = create_dataset(df_quo_france,
                                    zone_col = 'zone',
                                    cat_cols='classe_age',
                                    time_col = 'date')

dataset_incid_quo_std_france = create_dataset(df_incid_quo_std_france,
                                              zone_col='zone',
                                              time_col='date')

dataset_vaccination_dep = create_dataset(df_vaccination_dep,
                                         zone_col='dep',
                                         time_col='date')


dataset_mutant = create_dataset(df_mutant,
                                zone_col='zone',
                                time_col='date')

joblib.dump(dataset_incid_std_dep, f'{training_path}/incid_std_departement.pkl')
joblib.dump(dataset_rea_dc_cumul, f'{training_path}/rea_dc_cumul.pkl')
joblib.dump(dataset_rea_dc_quo, f'{training_path}/rea_dc_quo.pkl')
joblib.dump(dataset_service_un_cas_cumul,
            f'{training_path}/service_un_cas_cumul.pkl')
joblib.dump(dataset_quo_dep_age, f'{training_path}/quo_dep_age.pkl')
joblib.dump(dataset_quo_france, f'{training_path}/quo_france.pkl')
joblib.dump(dataset_incid_quo_std_france, f'{training_path}/quo_std_france.pkl')
joblib.dump(dataset_vaccination_dep, f'{training_path}/vaccination_dep.pkl')
joblib.dump(dataset_mutant, f'{training_path}/mutant.pkl')

dataset_r = xr.merge([
    dataset_incid_std_dep, dataset_rea_dc_cumul, dataset_rea_dc_quo,
    dataset_service_un_cas_cumul, dataset_quo_dep_age, dataset_quo_france,
    dataset_incid_quo_std_france, dataset_vaccination_dep, dataset_mutant
],
                     compat='override')


joblib.dump(dataset_r,'training_data/dataset_r.pkl')

dataset = joblib.load('training_data/dataset.pkl')

final_dataset = xr.merge([dataset, dataset_r], compat = 'override')

joblib.dump(final_dataset,'training_data/final_dataset.pkl')
