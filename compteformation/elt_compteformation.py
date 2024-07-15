from urllib.parse import quote_plus, urlencode
import pandas as pd
import requests


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

def load_clean_compteformation():
    """_summary_

    Returns:
        _type_: _description_
    """
    #url = 'https://opendata.caissedesdepots.fr/api/explore/v2.1/catalog/datasets/moncompteformation_catalogueformation/exports/json?select=date_extract%2C%20nom_of%2C%20nom_departement%2C%20nom_region%2C%20type_referentiel%2C%20code_inventaire%2C%20code_rncp%2C%20intitule_certification%2C%20libelle_niveau_sortie_formation%2C%20code_formacode_1%2C%20code_formacode_2%2C%20code_formacode_3%2C%20code_formacode_4%2C%20code_formacode_5%2C%20libelle_code_formacode_principal%2C%20libelle_nsf_1%2C%20code_nsf_1%2C%20code_certifinfo%2C%20siret%2C%20numero_formation%2C%20intitule_formation%2C%20points_forts%2C%20nb_action%2C%20nb_session_active%2C%20nb_session_a_distance%2C%20nombre_heures_total_min%2C%20nombre_heures_total_max%2C%20nombre_heures_total_mean%2C%20frais_ttc_tot_min%2C%20frais_ttc_tot_max%2C%20frais_ttc_tot_mean%2C%20code_departement%2C%20code_region%2C%20nbaction_nbheures%2C%20coderegion_export&where=code_nsf_1%20%3D%20%22326%22&limit=-1&timezone=UTC&use_labels=false&epsg=4326'
    df__cf_cleaned = pd.read_json(URL)
    return df__cf_cleaned
    

def load_clean_test_rncp():
    """_summary_

    Returns:
        _type_: _description_
    """
    #url = 'https://opendata.caissedesdepots.fr/api/explore/v2.1/catalog/datasets/moncompteformation_catalogueformation/exports/json?select=date_extract%2C%20nom_of%2C%20nom_departement%2C%20nom_region%2C%20type_referentiel%2C%20code_inventaire%2C%20code_rncp%2C%20intitule_certification%2C%20libelle_niveau_sortie_formation%2C%20code_formacode_1%2C%20code_formacode_2%2C%20code_formacode_3%2C%20code_formacode_4%2C%20code_formacode_5%2C%20libelle_code_formacode_principal%2C%20libelle_nsf_1%2C%20code_nsf_1%2C%20code_certifinfo%2C%20siret%2C%20numero_formation%2C%20intitule_formation%2C%20points_forts%2C%20nb_action%2C%20nb_session_active%2C%20nb_session_a_distance%2C%20nombre_heures_total_min%2C%20nombre_heures_total_max%2C%20nombre_heures_total_mean%2C%20frais_ttc_tot_min%2C%20frais_ttc_tot_max%2C%20frais_ttc_tot_mean%2C%20code_departement%2C%20code_region%2C%20nbaction_nbheures%2C%20coderegion_export&where=code_nsf_1%20%3D%20%22326%22&limit=100&timezone=UTC&use_labels=false&epsg=4326'
    df_cf_test_rncp = pd.read_json(URL_test_rncp).to_csv('compteformation/test_cf_rncp')
    return df_cf_test_rncp

def load_clean_test_rs():
    """_summary_

    Returns:
        _type_: _description_
    """
    #url = 'https://opendata.caissedesdepots.fr/api/explore/v2.1/catalog/datasets/moncompteformation_catalogueformation/exports/json?select=date_extract%2C%20nom_of%2C%20nom_departement%2C%20nom_region%2C%20type_referentiel%2C%20code_inventaire%2C%20code_rncp%2C%20intitule_certification%2C%20libelle_niveau_sortie_formation%2C%20code_formacode_1%2C%20code_formacode_2%2C%20code_formacode_3%2C%20code_formacode_4%2C%20code_formacode_5%2C%20libelle_code_formacode_principal%2C%20libelle_nsf_1%2C%20code_nsf_1%2C%20code_certifinfo%2C%20siret%2C%20numero_formation%2C%20intitule_formation%2C%20points_forts%2C%20nb_action%2C%20nb_session_active%2C%20nb_session_a_distance%2C%20nombre_heures_total_min%2C%20nombre_heures_total_max%2C%20nombre_heures_total_mean%2C%20frais_ttc_tot_min%2C%20frais_ttc_tot_max%2C%20frais_ttc_tot_mean%2C%20code_departement%2C%20code_region%2C%20nbaction_nbheures%2C%20coderegion_export&where=code_nsf_1%20%3D%20%22326%22&limit=100&timezone=UTC&use_labels=false&epsg=4326'
    df_cf_test_rs = pd.read_json(URL_test_rs).to_csv('compteformation/test_cf_rs')
    return df_cf_test_rs


#load_clean_compteformation()
load_clean_test_rs()
load_clean_test_rncp()

# transformer url via urlib et urlencode et request dont tu enregistres la reponse dans un json/csv eventuellement DONE

# conditions pour declencher ex: si mise a jour effectuée via critere date  A FAIRE
# recuperer la date extract
# la stocker en l ecrasant dans un fichier cible
# la comparer avec 
# une par jour des 12h40

# affectation des download: ds un dossier en csv/json par date?