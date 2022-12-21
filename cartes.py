#!/usr/bin/env python
# coding: utf-8

# In[369]:


get_ipython().system('pip install --upgrade botocore==1.23.26')
get_ipython().system('pip install --upgrade urllib3==1.22.0')
get_ipython().system('pip install py7zr')
get_ipython().system('pip install s3fs')
get_ipython().system('git clone https://github.com/InseeFrLab/cartogether.git')
get_ipython().run_line_magic('cd', './cartogether')
get_ipython().system('pip install -r requirements.txt')
get_ipython().system('pip install .')
get_ipython().system('pip install requests py7zr geopandas openpyxl tqdm s3fs PyYAML xlrd')
get_ipython().system('pip install git+https://github.com/inseefrlab/cartogether')
get_ipython().system('pip install pandas fiona shapely pyproj rtree')
get_ipython().system('pip install contextily')
get_ipython().system('pip install geopandas')
get_ipython().system('pip install pygeos')
get_ipython().system('pip install geopy')
get_ipython().system('pip install pynsee[full]')


# In[370]:


import contextily as ctx
from geopy.geocoders import Nominatim
from shapely.geometry import Point
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib


# In[371]:


niveau_vie = gpd.read_file('/home/onyxia/work/Projet-2A/niveau_de_vie_commune.csv')


# In[372]:


df_boulangeries = pd.read_csv('/home/onyxia/work/Projet-2A/boulangeries.csv')
gdf_boulangeries = gpd.GeoDataFrame(
    df_boulangeries.loc[:, [c for c in df_boulangeries.columns if c != "geometry"]],
    geometry=gpd.GeoSeries.from_wkt(df_boulangeries["geometry"]),
    crs="epsg:3005",
)


# In[373]:


df_boucheries =pd.read_csv('/home/onyxia/work/Projet-2A/boucheries.csv')
gdf_boucheries = gpd.GeoDataFrame(
    df_boucheries.loc[:, [c for c in df_boucheries.columns if c != "geometry"]],
    geometry=gpd.GeoSeries.from_wkt(df_boucheries["geometry"]),
    crs="epsg:3005",
)


# In[374]:


df_chocolateries = pd.read_csv('/home/onyxia/work/Projet-2A/chocolateries.csv')
gdf_chocolateries = gpd.GeoDataFrame(
    df_chocolateries.loc[:, [c for c in df_chocolateries.columns if c != "geometry"]],
    geometry=gpd.GeoSeries.from_wkt(df_chocolateries["geometry"]),
    crs="epsg:3005",
)


# In[ ]:





# In[375]:


df_librairies = pd.read_csv('/home/onyxia/work/Projet-2A/librairies.csv')
gdf_librairies = gpd.GeoDataFrame(
    df_librairies.loc[:, [c for c in df_librairies.columns if c != "geometry"]],
    geometry=gpd.GeoSeries.from_wkt(df_librairies["geometry"]),
    crs="epsg:3005",
) 


# In[376]:


df_pharmacies = pd.read_csv('/home/onyxia/work/Projet-2A/pharmacies.csv')
gdf_pharmacies = gpd.GeoDataFrame(
    df_pharmacies.loc[:, [c for c in df_pharmacies.columns if c != "geometry"]],
    geometry=gpd.GeoSeries.from_wkt(df_pharmacies["geometry"]),
    crs="epsg:3005",
)


# In[379]:


def limit_coord(gdf, liste_departements):
    if liste_departements == ["75", "77", "78", "91", "92", "93", "94", "95"]:
        return(gdf.loc[(gdf["lat"] > 48) & (gdf["lat"] < 49.4) & (gdf["long"] > 1.4) & (gdf["long"] < 3.5)])
    if liste_departements == ["75", "92", "93", "94"]:
        return(gdf.loc[(gdf["lat"] > 48.68) & (gdf["lat"] < 49.03) & (gdf["long"] > 2.15) & (gdf["long"] < 2.63)])
    else:
        return(gdf)


# In[380]:


def get_map(gdf, liste_departements):
    gdf = limit_coord(gdf, liste_departements)
    gdf = gdf.loc[gdf.departement.isin([ int(x) for x in liste_departements ])]
    gdf = gdf.reset_index(drop = True)
    
    niveau_vie = gpd.read_file('/home/onyxia/work/Projet-2A/niveau_de_vie_commune.csv')
    departement = []
    for ville in niveau_vie.CODGEO:
        departement.append(ville[:2])
    niveau_vie['departement']=departement
    niveau_vie = niveau_vie[niveau_vie.departement.isin(liste_departements)]
    niveau_vie = niveau_vie.reset_index(drop = True)
    
    cities = cartiflette.s3.download_vectorfile_url_all(
    values = liste_departements,
    level="COMMUNE_ARRONDISSEMENT",
    vectorfile_format="geojson",
    decoupage="departement",
    year=2022)
    cities["MED14"] = [np.NaN for k in range(len(cities))]
    
    for k in range(len(cities)):
        if cities["INSEE_DEP"].iloc[k] == '75':
            cities["MED14"].iloc[k] = niveau_vie.loc[niveau_vie["CODGEO"] == cities["INSEE_ARM"].iloc[k], "MED14"]
        else:
            cities["MED14"].iloc[k] = niveau_vie.loc[niveau_vie["CODGEO"] == cities["INSEE_COM"].iloc[k], "MED14"]
    cities = cities.replace(',', '.', regex=True)
    cities = cities.loc[cities["MED14"] != ""]
    cities = cities.reset_index(drop = True)
    for k in range(len(cities)):
        cities["MED14"][k] = (cities["MED14"].iloc[k])[0]
    cities = cities.replace(',', '.', regex=True)
    cities = cities.loc[cities["MED14"] != ""]
    cities = cities.reset_index(drop = True)
    
    MED_14 = [float(cities["MED14"].iloc[k]) for k in range(len(cities))]
    MED_14_norm = (MED_14-np.min(MED_14))/(np.max(MED_14) - np.min(MED_14))
    cities["MED_14_norm"] = MED_14_norm
    
    fig,ax = plt.subplots(figsize=(20, 20))
    gdf.plot(ax = ax, color = "red", markersize = 5.0,  alpha = 0.3, zorder = 1.5)
    cities.plot(ax = ax, column = "MED_14_norm", legend = True)
    plt.show()


# In[381]:


get_map(gdf_chocolateries, ["75", "92", "93", "94"])


# In[382]:


get_map(gdf_pharmacies, ["75", "92", "93", "94"])


# In[383]:


get_map(gdf_boucheries, ["75", "92", "93", "94"])


# In[384]:


get_map(gdf_boulangeries, ["75", "92", "93", "94"])


# In[385]:


get_map(gdf_librairies, ["75", "92", "93", "94"])


# In[386]:


get_map(gdf_chocolateries, ["75", "77", "78", "91", "92", "93", "94", "95"])


# In[387]:


get_map(gdf_pharmacies, ["75", "77", "78", "91", "92", "93", "94", "95"])


# In[388]:


get_map(gdf_boucheries, ["75", "77", "78", "91", "92", "93", "94", "95"])


# In[389]:


get_map(gdf_boulangeries, ["75", "77", "78", "91", "92", "93", "94", "95"])


# In[390]:


get_map(gdf_librairies, ["75", "77", "78", "91", "92", "93", "94", "95"])


# In[ ]:




