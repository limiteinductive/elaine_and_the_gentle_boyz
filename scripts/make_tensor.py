from egbz.utils import *
import joblib
import tensorflow as tf
import numpy as np

data = joblib.load('training_data/processed_dataset.pkl')

L = []
for zone in data.zone:
    tableau = from_df(
            data.sel(
            zone=zone).drop_vars('classe_age').to_dataframe()).pd_dataframe()
    incidence_hosp = tableau['incid_hosp']
    tableau = tableau.drop(columns=['incid_hosp'])
    tableau['incid_hosp'] = incidence_hosp
    L.append(np.array(tableau))

tensor_tot = tf.convert_to_tensor(L)

tensor_f = tf.reshape(tensor_tot, (tensor_tot.shape[1],
                                   tensor_tot.shape[0],
                                   tensor_tot.shape[2]))

joblib.dump(tensor_f,'training_data/tensor_f.pkl')
