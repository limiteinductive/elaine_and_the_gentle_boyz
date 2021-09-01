import pandas as pd
import itertools
from darts import TimeSeries
from typing import Tuple, Optional, Callable, Any, List, Union
import xarray as xr




def create_dataset(
    df: pd.DataFrame,
    feat_cols: Optional[Union[List[str], str]]=None,
    zone_col: Optional[str]=None,
    time_col: Optional[str]=None,
    cat_cols: Optional[Union[List[str], str]]=None,
) -> xr.Dataset:
    """
    Returns a Dataset that encapsulates the zone, time, categorical
    and features dimension of the data.

    Parameters
    ----------
    df
        DataFrame from which the values are extracted.
    feat_cols
        Adds 'features' as variables inside the Dataset.
    zone_col
        Adds a 'zone' dimension to the DataArray where the values
        come from the zone_col columns of df.
    time_col
        Adds a 'time' dimension to the DataArray where the values
        come from the time_col columns of df.
    cat_cols
        Adds a 'categorical' dimension to the DataArray where the
        values come from the cat_cols.

    Returns
    ----------
    Dataset
        Multi-dimensional Dataset constructed from the df DataFrame
    """
    dims = []
    coords = []
    rename_dict = {}

    if zone_col:
        df[zone_col] = df[zone_col].astype('str')
        dims.append(zone_col)
        rename_dict[zone_col] = 'zone'

    if time_col:
        df[time_col] = pd.to_datetime(df[time_col])
        dims.append(time_col)
        rename_dict[time_col] = 'time'

    if cat_cols:
        if isinstance(cat_cols, str):
            cat_cols = [cat_cols]
        coords.append(cat_cols)
        dims.extend(cat_cols)

    if not feat_cols:
        feat_cols = [x for x in df if x not in dims]

    if isinstance(feat_cols, str):
        feat_cols = [feat_cols]

    index_df = df.set_index(dims)[feat_cols]
    xarray = index_df.to_xarray()

    return xarray.rename(rename_dict)



def from_df(df: pd.DataFrame,
            time_col: Optional[str] = None,
            cat_cols: Optional[Union[List[str], str]] = None,
            value_cols: Optional[Union[List[str], str]] = None
            ) -> 'Timeseries':
    """
    Returns a multivariate Timeseries instance from a DataFrame. The date_col is the column
    used to represent time, value_cols the features and cat_col is the column


    Parameters
    ----------
    filepath_or_buffer
        The path to the CSV file, or the file object.
    time_col
        The time column name. If set, the column will be cast to a pandas DatetimeIndex.
        If not set, the pandas Int64Index will be used.
    cat_cols
        For each value in the cat_cols columns, it will add a new Timeserie.
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

    if value_cols==None:
        if cat_cols:
            value_cols = list(df.drop(cat_cols, axis=1).columns)
        else:
            value_cols = list(df.columns)


    # Let's create the new dataframe creating a column for each value of cat_col
    if isinstance(value_cols, str):
        value_cols = [value_cols]
    if isinstance(cat_cols, str):
        cat_cols = [cat_cols]
    if cat_cols:
        for col in cat_cols:
            df[col] = df[col].astype('str')

        categories = itertools.product(*[df[cat].unique() for cat in cat_cols])
        d = {f'{col}_{"_".join([x for x in cat])}':
             df.query(' & '.join([f'{cat_name}=="{cat_value}"'
                                for cat_name, cat_value in zip(cat_cols, [x for x in cat])
                                ])
             )[col]
            for cat in categories
            for col in value_cols
        }
        df = pd.DataFrame(d)

    return TimeSeries.from_dataframe(df=df)

def from_csv(filepath_or_buffer: pd._typing.FilePathOrBuffer,
                            time_col: Optional[str] = None,
                            cat_cols: Optional[Union[List[str], str]] = None,
                            value_cols: Optional[Union[List[str], str]] = None,
                            **kwargs) -> 'Timeseries':
    """
    Returns a multivariate Timeseries instance from a CSV. The date_col is the column
    used to represent time, value_cols the features and cat_col is the column


    Parameters
    ----------
    filepath_or_buffer
        The path to the CSV file, or the file object.
    cat_cols
        For each value in the cat_cols columns, it will add a new Timeserie.
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
    return from_df(df, cat_cols=cat_cols, time_col=time_col, value_cols=value_cols)
