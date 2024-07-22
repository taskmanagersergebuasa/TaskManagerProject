from urllib.parse import quote_plus, urlencode
import pandas as pd
import requests
import dateparser
import logging


### CLEAN DATAFRAME COMPTEFORMATIONORIGINE (type ref & id_certif(code_rncp & code_inventaire) ,id_certif ,indexation id_compte_formation)

#affectation des codes inventaire & code rncp a une colonne id_certif dediée
def clean_idcertif_cf(df: pd.DataFrame):
    """
    
    """
    for i in range(len(df['code_inventaire'].values.tolist())):
         if df.loc[i, 'type_referentiel'] == 'RS':
                                              df.loc[i, 'code_rncp'] = df.loc[i, 'code_inventaire']
    del df['code_inventaire']
    df = df.rename(columns={'code_rncp': 'id_certif'})
    df['id_certif'] = df['id_certif'].astype(str)
    return df  

#"ajout" de val de type_referentiel a valeurs de colonne id_certif 
#def clean_idcertif_cf(df: pd.DataFrame):
    """

    """
    df['id_certif'] = df['id_certif'].astype(str)
    df['id_certif'] = df['type_referentiel'] + df['id_certif']
    del df['type_referentiel']
    return df
#modif nom type_referentiel en type_certif
def clean_typecertif_cf(df: pd.DataFrame):
        df = df.rename(columns={'type_referentiel': 'type_certif'})
        return df
      

#transformation en index de id_compte_formation
def add_idcompteformation(df: pd.DataFrame):
    """
    _
    """
    df.insert(0, 'id_compte_formation', range(0, len(df)))
    df.set_index(keys=['id_compte_formation'], inplace=True)
    return df
                      


### EXEMPLES RNCP & RS 100 lignes en exemple####################################
#
base_url = "https://opendata.caissedesdepots.fr/api/explore/v2.1/catalog/datasets/moncompteformation_catalogueformation/exports/json"
query_params_test_rncp = {
    "select": "date_extract, nom_of, nom_departement, nom_region, type_referentiel, code_inventaire, code_rncp, intitule_certification, libelle_niveau_sortie_formation, code_formacode_1, code_formacode_2, code_formacode_3, code_formacode_4, code_formacode_5, libelle_code_formacode_principal, libelle_nsf_1, libelle_nsf_2, libelle_nsf_3, code_nsf_1, code_nsf_2, code_nsf_3, code_certifinfo, siret, nb_action, nb_session_active, nb_session_a_distance, nombre_heures_total_min, nombre_heures_total_max, nombre_heures_total_mean, frais_ttc_tot_min, frais_ttc_tot_max, frais_ttc_tot_mean, code_departement, code_region, nbaction_nbheures, coderegion_export",
    #"where": 'libelle_nsf_1 like "Informatique, traitement de l\'information, réseaux de transmission"',
    "where": 'code_nsf_1 like "326" AND type_referentiel like "RNCP"',
    "limit": 100,
    "offset": 0,
    "timezone": "UTC",
    "include_links": "false",
    "include_app_metas": "false"
}
encoded_query_params_test_rncp = urlencode(query_params_test_rncp, quote_via=quote_plus)
URL_test_rncp  = f"{base_url}?{encoded_query_params_test_rncp}"

def load_clean_ex_rncp():
    """_summary_

    Returns:
        _type_: _description_
    """
    #url = 'https://opendata.caissedesdepots.fr/api/explore/v2.1/catalog/datasets/moncompteformation_catalogueformation/exports/json?select=date_extract%2C%20nom_of%2C%20nom_departement%2C%20nom_region%2C%20type_referentiel%2C%20code_inventaire%2C%20code_rncp%2C%20intitule_certification%2C%20libelle_niveau_sortie_formation%2C%20code_formacode_1%2C%20code_formacode_2%2C%20code_formacode_3%2C%20code_formacode_4%2C%20code_formacode_5%2C%20libelle_code_formacode_principal%2C%20libelle_nsf_1%2C%20code_nsf_1%2C%20code_certifinfo%2C%20siret%2C%20numero_formation%2C%20intitule_formation%2C%20points_forts%2C%20nb_action%2C%20nb_session_active%2C%20nb_session_a_distance%2C%20nombre_heures_total_min%2C%20nombre_heures_total_max%2C%20nombre_heures_total_mean%2C%20frais_ttc_tot_min%2C%20frais_ttc_tot_max%2C%20frais_ttc_tot_mean%2C%20code_departement%2C%20code_region%2C%20nbaction_nbheures%2C%20coderegion_export&where=code_nsf_1%20%3D%20%22326%22&limit=100&timezone=UTC&use_labels=false&epsg=4326'
    df_cf_test_rncp = pd.read_json(URL_test_rncp)
    df_cf_test_rncp = clean_idcertif_cf(df_cf_test_rncp)
    df_cf_test_rncp = clean_typecertif_cf(df_cf_test_rncp)
    df_cf_test_rncp = add_idcompteformation(df_cf_test_rncp)
    print(df_cf_test_rncp.info())
    print(df_cf_test_rncp.index)
    load_cf_test_rncp = df_cf_test_rncp.to_csv('compteformation/test_cf_rncp')
    return df_cf_test_rncp

# 
query_params_test_rs = {
    "select": "date_extract, nom_of, nom_departement, nom_region, type_referentiel, code_inventaire, code_rncp, intitule_certification, libelle_niveau_sortie_formation, code_formacode_1, code_formacode_2, code_formacode_3, code_formacode_4, code_formacode_5, libelle_code_formacode_principal, libelle_nsf_1, libelle_nsf_2, libelle_nsf_3, code_nsf_1, code_nsf_2, code_nsf_3, code_certifinfo, siret, nb_action, nb_session_active, nb_session_a_distance, nombre_heures_total_min, nombre_heures_total_max, nombre_heures_total_mean, frais_ttc_tot_min, frais_ttc_tot_max, frais_ttc_tot_mean, code_departement, code_region, nbaction_nbheures, coderegion_export",
    #"where": 'libelle_nsf_1 like "Informatique, traitement de l\'information, réseaux de transmission"',
    "where": 'code_nsf_1 like "326"',
    "limit": 100,
    "offset": 0,
    "timezone": "UTC",
    "include_links": "false",
    "include_app_metas": "false"
}
encoded_query_params_test_rs = urlencode(query_params_test_rs, quote_via=quote_plus)
URL_test_rs  = f"{base_url}?{encoded_query_params_test_rs}"

def load_clean_ex_rs():
    """_summary_

    Returns:
        _type_: _description_
    """
    #url = 'https://opendata.caissedesdepots.fr/api/explore/v2.1/catalog/datasets/moncompteformation_catalogueformation/exports/json?select=date_extract%2C%20nom_of%2C%20nom_departement%2C%20nom_region%2C%20type_referentiel%2C%20code_inventaire%2C%20code_rncp%2C%20intitule_certification%2C%20libelle_niveau_sortie_formation%2C%20code_formacode_1%2C%20code_formacode_2%2C%20code_formacode_3%2C%20code_formacode_4%2C%20code_formacode_5%2C%20libelle_code_formacode_principal%2C%20libelle_nsf_1%2C%20code_nsf_1%2C%20code_certifinfo%2C%20siret%2C%20numero_formation%2C%20intitule_formation%2C%20points_forts%2C%20nb_action%2C%20nb_session_active%2C%20nb_session_a_distance%2C%20nombre_heures_total_min%2C%20nombre_heures_total_max%2C%20nombre_heures_total_mean%2C%20frais_ttc_tot_min%2C%20frais_ttc_tot_max%2C%20frais_ttc_tot_mean%2C%20code_departement%2C%20code_region%2C%20nbaction_nbheures%2C%20coderegion_export&where=code_nsf_1%20%3D%20%22326%22&limit=100&timezone=UTC&use_labels=false&epsg=4326'
    df_cf_test_rs = pd.read_json(URL_test_rs)
    df_cf_test_rs = clean_idcertif_cf(df_cf_test_rs)
    df_cf_test_rs = clean_typecertif_cf(df_cf_test_rs)
    df_cf_test_rs = add_idcompteformation(df_cf_test_rs)
    print(df_cf_test_rs.info())
    print(df_cf_test_rs.index)
    load_cf_test_rs = df_cf_test_rs.to_csv('compteformation/test_cf_rs')
    return df_cf_test_rs
#
#load_clean_ex_rncp()
#load_clean_ex_rs()


### LOAD COMPTE FORMATION -60000 lignes! ###########################################


#affiner avec des criteres proches de simplon(listes codes nfs et formacode)
query_params = {
    "select": "date_extract, nom_of, nom_departement, nom_region, type_referentiel, code_inventaire, code_rncp, intitule_certification, libelle_niveau_sortie_formation, code_formacode_1, code_formacode_2, code_formacode_3, code_formacode_4, code_formacode_5, libelle_code_formacode_principal, libelle_nsf_1, libelle_nsf_2, libelle_nsf_3, code_nsf_1, code_nsf_2, code_nsf_3, code_certifinfo, siret, nb_action, nb_session_active, nb_session_a_distance, nombre_heures_total_min, nombre_heures_total_max, nombre_heures_total_mean, frais_ttc_tot_min, frais_ttc_tot_max, frais_ttc_tot_mean, code_departement, code_region, nbaction_nbheures, coderegion_export",
    #"where": 'libelle_nsf_1 like "Informatique, traitement de l\'information, réseaux de transmission"',
    "where": 'code_nsf_1 like "326"',
    "limit": -1,
    "offset": 0,
    "timezone": "UTC",
    "include_links": "false",
    "include_app_metas": "false"
}
encoded_query_params = urlencode(query_params, quote_via=quote_plus)
URL  = f"{base_url}?{encoded_query_params}"

#response = requests.get(URL)

def load_compteformation():
    """_summary_

    Returns:
        _type_: _description_
    """
    #url = 'https://opendata.caissedesdepots.fr/api/explore/v2.1/catalog/datasets/moncompteformation_catalogueformation/exports/json?select=date_extract%2C%20nom_of%2C%20nom_departement%2C%20nom_region%2C%20type_referentiel%2C%20code_inventaire%2C%20code_rncp%2C%20intitule_certification%2C%20libelle_niveau_sortie_formation%2C%20code_formacode_1%2C%20code_formacode_2%2C%20code_formacode_3%2C%20code_formacode_4%2C%20code_formacode_5%2C%20libelle_code_formacode_principal%2C%20libelle_nsf_1%2C%20code_nsf_1%2C%20code_certifinfo%2C%20siret%2C%20numero_formation%2C%20intitule_formation%2C%20points_forts%2C%20nb_action%2C%20nb_session_active%2C%20nb_session_a_distance%2C%20nombre_heures_total_min%2C%20nombre_heures_total_max%2C%20nombre_heures_total_mean%2C%20frais_ttc_tot_min%2C%20frais_ttc_tot_max%2C%20frais_ttc_tot_mean%2C%20code_departement%2C%20code_region%2C%20nbaction_nbheures%2C%20coderegion_export&where=code_nsf_1%20%3D%20%22326%22&limit=-1&timezone=UTC&use_labels=false&epsg=4326'
    df_cf_origin = pd.read_json(URL)
    df_cf = clean_idcertif_cf(df_cf_origin)
    df_cf = clean_typecertif_cf(df_cf)
    df_cf = add_idcompteformation(df_cf)
    return df_cf


     


#load_compteformation()


### UPDATE COMPTEFORMATION  ##########################################
#requete pour obtenir date_extract au moment de l execution du fichier
query_params_current_date = {
    "select": "date_extract",
    #"where": 'libelle_nsf_1 like "Informatique, traitement de l\'information, réseaux de transmission"',
    "where": 'code_nsf_1 like "326"',
    "limit": 1,
    "offset": 0,
    "timezone": "UTC",
    "include_links": "false",
    "include_app_metas": "false"
}

encoded_query_params_current_date = urlencode(query_params_current_date, quote_via=quote_plus)
URL_current_date  = f"{base_url}?{encoded_query_params_current_date}"

def get_current_date():
    """_summary_

    Returns:
        _type_: _description_
    """
    response = requests.get(URL_current_date)
    current_date = response.json()
    current_date = current_date[0]['date_extract']
    #print(type(current_date)) = str
    return current_date

#get_current_date()

def update_cf():
    """

    """  
    try:
        with open('last_update_file.txt', 'r+') as date_reader_file:
             date_buffer = date_reader_file.read()
             current_date = get_current_date()
             if dateparser.parse(date_buffer) != dateparser.parse(current_date):                 
                 with open('last_update_file.txt', 'w')as date_reader_file2:
                     date_reader_file2.write(f"{current_date}")
                 return load_clean_ex_rs()
                 #load_clean_ex_rncp()
                 #return load_compteformation                
             else:
                 pass
                 
       
    except FileNotFoundError:        
        with open('last_update_file.txt', 'a') as date_reader_file:
            last_update = get_current_date()
            date_reader_file.write(f"{last_update}")
        return load_clean_ex_rs()
        #return load_clean_ex_rncp()
        #return load_compteformation


#update_cf()

### PROCESSING COMPTEFORMATION
#creation des dataframes a partir de la source compte formation nettoyée et mise a jour
df_source = update_cf()
#df_compte_formation
df_compte_formation = df_source['id_compte_formation'] + ['']

#df_nfs

#df_formacode

#df_cf_nfs

#df_cf_formacode

#df_cf_certification

#df_certification_certificateur

#df_certificateur

## INGESTION EN BDD DIRECTEMENT, MODELS 
#suppression de la source compteformationorigine à l etape des models?
#to sql des dataframes?




