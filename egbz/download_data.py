# The aim of this module is to contain all the functions
# to download .csv and store them into raw_data
import pandas as pd



def basic_COVID():
    '''
    Downloads data for hosp (number of hospitalization), rea (number 
    of patients in reanimation and dchosp (number of death due to COVID at 
    hospital and returns as CSV with those features per departement +
    aggregated result for France
    '''
    link = 'https://www.data.gouv.fr/fr/datasets/r/5c4e1452-3850-4b59-b11c-3dd51d7fb8b5'
    df = pd.read_csv(link)

    # Let's select the features we're interested in
    df = df[['date', 'dep', 'dchosp', 'hosp', 'rea']]
    
    # We convert the index of the series as a DateTime object
    datetime_series = pd.to_datetime(df['date'])
    datetime_index = pd.DatetimeIndex(datetime_series.values)
    df=df.set_index(datetime_index)
    df.drop('date',axis=1,inplace=True)

    # Let's add all departements Timeseries as a column in the df
    new_d = {f'{feat}_{dep}': df[df['dep']==dep][feat]
            for dep in df.dep.unique() 
            for feat in ['dchosp', 'rea', 'hosp']
    }
    new_df = pd.DataFrame(new_d)

    return new_df

