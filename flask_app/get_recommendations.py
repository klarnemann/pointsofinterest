import pandas as pd
import numpy as np

matsim_df = pd.read_csv('data/matsim.csv', index_col=0, low_memory=True )
info_df = pd.read_csv('data/information.csv', index_col=0, low_memory=True)

def get_recommendations(city, reference_city, max_distance=200, top_n=11, 
    matsim_df=matsim_df, info_df=info_df):
    '''Return most similar travel destinations, given input city.

    PARAMETERS
    ----------
    city : str
      city name in format = City, State (e.g. Peninsula, Ohio)
    reference_city : str or None
      Reference point from which to compute distance (e.g. Peninsula, Ohio)
    max_distance : int
      maximum travel distance in miles (relative to referance city)
    top_n : int
      number - 1 of reccomendations to return
    matsim_df : pandas.DataFrame (index=cities,columns=cities)
      similarity between each pair of cities (in topic space); 1=most similar, 0=least similar
    info_df : pandas.DataFrame (index=cities, columns=['POIs', 'Coords'])
      information about each city

    RETURNS
    -------
    html table of recommended travel desinations
    '''
    cities = np.array(matsim_df.index)
    vals = np.array(matsim_df.loc[city])
    if reference_city:
        exclude_mask = get_distance_mask(reference_city, max_distance)
        vals[exclude_mask] = 0.#Excludes far-away travel destinations
    vals[list(cities).index(city)] = 2.#Ensures input city always appears first
    n_cities = len(cities)
    inds = [x for _, x in sorted(zip(vals, np.arange(n_cities)), reverse=True)]
    top_inds = inds[:top_n]
    recommendations = cities[top_inds]
    pois = np.array(info_df.POIs.loc[recommendations])
    index = ['Input'] + list(np.array(np.arange(1,top_n), dtype=str))
    out_df = pd.DataFrame(np.array([recommendations, pois]).T, 
                          columns=['City', 'Points of Interest'], 
                          index=index)
    out_df[pd.isnull(out_df)] = ' '
    pd.set_option('display.max_colwidth', -1)
    out_html = out_df.to_html()
    out_html = out_html.replace('<td>', '<td style="white-space: normal">')
    return out_html

def get_distance_mask(city, max_distance, labels=matsim_df.columns):
    '''
    Make mask of areas further than 200 miles from city.

    PARAMETERS
    ----------
    city : str
      Reference point from which to compute distance (e.g. Peninsula, Ohio)
    max_distance : float
      (Optional) Maximum acceptable distance (in miles).
    '''
    distance_df = pd.read_csv('data/distance.csv', index_col=0)
    distance_df = distance_df.reindex(labels=labels)
    distance_df.fillna(5000, inplace=True)
    dist_vals = distance_df[city]
    return dist_vals > max_distance
