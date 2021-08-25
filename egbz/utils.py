import pandas as pd
from darts import TimeSeries
from typing import Tuple, Optional, Callable, Any, List, Union


def from_df(df: pd.DataFrame,
            cat_col: Optional[str] = None,
            time_col: Optional[str] = None,
            value_cols: Optional[Union[List[str], str]] = None
            ) -> 'Timeseries':
    """
    Returns a multivariate Timeseries instance from a DataFrame. The date_col is the column
    used to represent time, value_cols the features and cat_col is the column 
    

    Parameters
    ----------
    filepath_or_buffer
        The path to the CSV file, or the file object.
    cat_col 
        For each value in the cat_col columns, it will add a new Timeserie.
    time_col
        The time column name. If set, the column will be cast to a pandas DatetimeIndex.
        If not set, the pandas Int64Index will be used.
    value_col
        A string or a list of strings representing the features to be extracted from 
        the csv. If None, all the columns will be extracted.
    kwargs
        Optional arguments to be passed to 'pandas.read_csv' function.
        

    Returns
    -----------
    Timeseries
        Univariate or Multivariate Timeseries constructed from inputs.
    """

    # We add the time_col as a DatetimeIndex for df
    if time_col:
        datetime_series = pd.to_datetime(df[time_col])
        datetime_index = pd.DatetimeIndex(datetime_series.values)
        df = df.set_index(datetime_index)
        df.drop(time_col, axis=1, inplace=True)



    # Let's create the new dataframe creating a column for each value of cat_col
    if isinstance(value_cols, str):
        value_cols = [value_cols]
    d = {f'{col}_{cat}': df[df[cat_col]==cat][col]
            for cat in df[cat_col].unique()
            for col in value_cols
    }
    new_df = pd.DataFrame(d)

    return TimeSeries.from_dataframe(df=new_df)

def from_csv(filepath_or_buffer: pd._typing.FilePathOrBuffer,
                            cat_col: Optional[str] = None,
                            time_col: Optional[str] = None,
                            value_cols: Optional[Union[List[str], str]] = None,
                            **kwargs) -> 'Timeseries':
    """
    Returns a multivariate Timeseries instance from a CSV. The date_col is the column
    used to represent time, value_cols the features and cat_col is the column 
    

    Parameters
    ----------
    filepath_or_buffer
        The path to the CSV file, or the file object.
    cat_col 
        For each value in the cat_col columns, it will add a new Timeserie.
    time_col
        The time column name. If set, the column will be cast to a pandas DatetimeIndex.
        If not set, the pandas Int64Index will be used.
    value_col
        A string or a list of strings representing the features to be extracted from 
        the csv. If None, all the columns will be extracted.
    kwargs
        Optional arguments to be passed to 'pandas.read_csv' function.
        

    Returns
    -----------
    Timeseries
        Univariate or Multivariate Timeseries constructed from inputs.
    """
    # Let's open the CSV as a DataFrame with time_col as a DatetimeIndex
    df = pd.read_csv(filepath_or_buffer=filepath_or_buffer, **kwargs)
    return from_df(df, cat_col=cat_col, time_col=time_col, value_cols=value_cols)
