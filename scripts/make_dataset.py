import joblib
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

feat_dep = [
        'hosp', 'rea', 'rad', 'dchosp', 'incid_hosp', 'incid_rea', 'incid_rad',
        'incid_dchosp', 'reg_incid_rea', 'nbre_tests_positifs', 'dc',
        'indic_dc', 'pos', 'pos_7j'
    ]

def scale_features(data):
    for feature in feat_dep:
        for zone in data.zone:
            try:
                data[feature].loc[{
                    'zone': zone
                }] = 100000 * data[feature].sel(zone=zone) / (np.array(
                    data['population'].sel(zone=zone))[0])
            except:
                continue
    return data


def scaling(data):
    for feature in dict(data.data_vars).keys():
        for zone in data.zone:
            min_max = MinMaxScaler()
            try:
                data[feature].loc[{
                    'zone': zone
                }] = min_max.fit_transform(data[feature].sel(zone=zone))
            except:
                continue
    return data


def read_dataframe():
    dataset = joblib.load('training_data/final_dataset.pkl')
    df_mutant = pd.read_csv('data/processed_dataframes/presence_mutant.csv')
    to_delete = list(df_mutant.columns[2:]) + ['dc_tot'] + [
    'nbre_dose_1', 'nbre_dose_complet', 'nbre_cum_dose_1', 'nbre_cum_complet',
    'couverture_dose1', 'couverture_complete', 'esms_dc', 'conf',
    'test_positifs_femmes', 'tests_positifs_hommes', 'tests_positifs_tot',
    'pop_femme', 'pop_homme', 'TX', 'UX', 'RR'
    ]
    mdep = [
        x for x in dataset.zone.values if x not in [
            'france', '971', '972', '973', '974', '975', '976', '978', '977',
            'fr', '2A', '2B'
        ]
    ]
    data = (dataset.sel(zone=mdep,
                        time=slice('2021-01-01',
                                   '2021-07-28')).drop_vars(names=to_delete))

    propor_data = scale_features(data)
    scaled_data = scaling(propor_data)

    return scaled_data

dataset = read_dataframe()

joblib.dump(dataset, 'training_data/processed_dataset.pkl')
