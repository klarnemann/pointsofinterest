import pandas as pd
import numpy as np

info_df = pd.read_csv('data/information.csv', index_col=0, low_memory=True)

def get_recommendations(city, reference_city, top_n=11, info_df=info_df):
    '''Return most similar travel destinations, given input city.

    PARAMETERS
    ----------
    city : str
      city name in format = City, State (e.g. Peninsula, Ohio)
    reference_city : str or None
      Reference point from which to compute distance (e.g. Peninsula, Ohio)
    top_n : int
      number - 1 of reccomendations to return
    info_df : pandas.DataFrame (index=cities, columns=['POIs', 'Coords'])
      information about each city

    RETURNS
    -------
    html table of recommended travel desinations
    '''
    if reference_city:
        matsim_df_f = 'data/matsim_%s.csv' % (format_city(reference_city))
        matsim_df = pd.read_csv(matsim_df_f, index_col=0, low_memory=True)
        vals = np.array(matsim_df.loc[city])# get similarities to input city
        cities = np.array(matsim_df.columns)# cities within range of reference city
        n_cities = len(cities)
        # order city indices by similiary to input city (i.e. from most to least similar)
        inds = [x for _, x in sorted(zip(vals, np.arange(n_cities)), reverse=True)]
        # input city within range of reference_city
        if city in set(cities):
            vals[list(cities).index(city)] = 2.#Ensures input city always appears first
            top_inds = inds[:top_n]
            recommendations = cities[top_inds]
        # input city outside range of reference_city
        else:
            top_n = int(top_n) - 1
            top_inds = inds[:top_n]
            recommendations = list(cities[top_inds])
            recommendations = [city] + recommendations
    else:
        top_n_df = pd.read_csv('data/recommendations_top_10.csv', index_col=0, low_memory=True)
        recommendations = list(top_n_df.loc[city])
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

def format_city(city):
    city, state = city.split(', ')
    city = city.replace(' ', '')
    state = state.replace(' ', '')
    return('%s_%s' % (city, state))
