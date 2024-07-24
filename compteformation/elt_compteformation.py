from urllib.parse import quote_plus, urlencode
import pandas as pd
import requests
import dateparser
import logging
from sqlalchemy import Date, String, create_engine
import os
from dotenv import load_dotenv

load_dotenv()


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

#modif nom type_referentiel en type_certif
def clean_typecertif_cf(df: pd.DataFrame):
        df = df.rename(columns={'type_referentiel': 'type_certif'})
        return df
      

#transformation en colonne avec valeurs index  de id_compte_formation
def add_idcompteformation(df: pd.DataFrame):
    """
    _
    """
    df.insert(0, 'id_compte_formation', range(0, len(df)))
    #df.set_index(keys=['id_compte_formation'], inplace=True)
    #df.reset_index()
    return df
                      


### EXEMPLES RNCP & RS 100 lignes en exemple####################################
#structure encode url :100 lignes rncp, puis fonction de requete qui renvoie un dataframe
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
    #print(df_cf_test_rncp.info())
    #print(df_cf_test_rncp.index)
    load_cf_test_rncp = df_cf_test_rncp.to_csv('compteformation/test_cf_rncp')
    return df_cf_test_rncp

#structure encode url :100 lignes rs, puis fonction de requete qui renvoie un dataframe
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
    #print(df_cf_test_rs.info())
    #print(df_cf_test_rs.index)
    df_cf_test_rs.to_csv('compteformation/test_cf_rs')
    print(df_cf_test_rs.info())
    return df_cf_test_rs
#
#load_clean_ex_rncp()
#load_clean_ex_rs()


### LOAD COMPTE FORMATION -60000 lignes! ###########################################

#structure encode url fichier complet, puis fonction de requete qui renvoie un dataframe
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
                 with open('last_update_file.txt', 'w') as date_reader_file2:
                     date_reader_file2.write(f"{current_date}")
                 return load_clean_ex_rs()
                 #return load_clean_ex_rncp()
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
# concatenation d' un choix de colonnes de compteformation origine pour construire les dataframes correspondant aux tables cibles
def processing_compteformation():
      # dictionnaire {nom_de_table : dataframe} des dataframes 
      df_dict = {}

      #df_source
      df_source = update_cf()
      print(df_source.info())
      df_source.drop_duplicates(subset=df_source.columns.difference(['id_compte_formation']))
     
      #df_compte_formation OK
      df_compte_formation = pd.concat([df_source['id_compte_formation'], df_source['nom_of'], df_source['intitule_certification']], axis=1)
      df_compte_formation.drop_duplicates(subset=df_compte_formation.columns.difference(['id_compte_formation']))
      df_dict['compteformation'] = df_compte_formation
      print(df_compte_formation.info())
      print(df_dict)

      #df_nfs OK
      df_nsf = pd.DataFrame()
      # concatenation verticale des codes nfs en NFS_code et suppression valeur nulles
      df_nsf['NSF_code'] = pd.concat([df_source['code_nsf_1'], df_source['code_nsf_2'], df_source['code_nsf_3']])
      se_code = df_nsf['NSF_code'].dropna()
      print(se_code.info())
      # concatenation verticale des libelles ou nfs name en NFS_name et suppression valeurs nulles
      df_nsf['NSF_name'] = pd.concat([df_source['libelle_nsf_1'], df_source['libelle_nsf_2'], df_source['libelle_nsf_3']])  
      se_name = df_nsf['NSF_name'].dropna()
      print(se_name.info())            
      # concatenation de NFS_code et NFS_name
      df_nsf = pd.concat([se_code, se_name], axis=1)
      # suppression lignes doublons
      df_nsf = df_nsf.drop_duplicates()
      # suppression lignes valeurs nulles ou manquantes
      #df_nsf = df_nsf.dropna()
      print(df_nsf.info())
      # ajout au dictionnaire de dataframe
      df_dict['nsf'] = df_nsf
      print(df_dict)

      #df_forma OK
      df_forma = pd.DataFrame()
      # concatenation verticale des codes formacodes  en NFS_code
      df_forma['forma_code'] = pd.concat([df_source['code_formacode_1'], df_source['code_formacode_2'], df_source['code_formacode_3'], df_source['code_formacode_4'], df_source['code_formacode_5']])
      #print(df_forma['forma_code'])
      # affectation des libelles_code_formacode_principalà colonne forma_name
      df_forma['forma_name'] = df_source['libelle_code_formacode_principal']
      #print(df_forma['forma_name'])             
      #A TRAITER concatenation de forma_code et forma_name => je veux juste les lignes ou forma_code est non nul!!!
      df_forma = pd.concat([df_forma['forma_code'], df_forma['forma_name']], axis=1)
      #suppression lignes doublons
      df_forma = df_forma.drop_duplicates()
      #suppression lignes avec au moins 1 valeur nulle dans colonne formacode)
      df_forma = df_forma.dropna(subset=['forma_code'])
      #print(df_forma.info())
      # ajout au dictionnaire de dataframe
      df_dict['forma'] = df_forma
      print(df_dict)
      #df_certification


      return df_dict


##### INGESTION DES TABLES A PARTIR DES DATAFRAMES du dictionnaire
# il faut construire  l' env de connection: done
def ingest_tables(df_dict: dict):
      #environnement de connection serveur bdd et sqlalchemy
      if bool(int(os.getenv("IS_POSTGRES"))):
        username = os.getenv("DB_USERNAME")
        hostname = os.getenv("DB_HOSTNAME")
        port = os.getenv("DB_PORT")
        database_name = os.getenv("DB_NAME")
        password = os.getenv("DB_PASSWORD")
        bdd_path = f"postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{database_name}"
      else:
            bdd_path = 'sqlite:///database.db'

      engine = create_engine(bdd_path)
      #engine = create_engine('sqlite://', echo=False)
     
      #  Base = declarative_base()
      if engine.dialect.name == 'sqlite':
        date_type = String
      elif engine.dialect.name == 'postgresql+psycopg2':
             date_type = Date
      else:
            raise ValueError(f"SGBD non pris en charge : {engine.dialect.name}")
      
      df = pd.DataFrame()
      for nom_table, df in df_dict.items():
            if isinstance(df, pd.DataFrame) & isinstance(nom_table, str):
                  df.to_sql(nom_table, engine)
            
      



#df_compteformation = df_source['id_compte_formation']
#load_ex_compteformation = df_compteformation.to_csv('compteformation/test_compteformation')



dict = processing_compteformation()

ingest_tables(dict)

