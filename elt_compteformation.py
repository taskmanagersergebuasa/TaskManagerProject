import pandas as pd

def load_clean_compteformation():
    url = 'https://opendata.caissedesdepots.fr/api/explore/v2.1/catalog/datasets/moncompteformation_catalogueformation/exports/json?select=date_extract%2C%20nom_of%2C%20nom_departement%2C%20nom_region%2C%20type_referentiel%2C%20code_inventaire%2C%20code_rncp%2C%20intitule_certification%2C%20libelle_niveau_sortie_formation%2C%20code_formacode_1%2C%20code_formacode_2%2C%20code_formacode_3%2C%20code_formacode_4%2C%20code_formacode_5%2C%20libelle_code_formacode_principal%2C%20libelle_nsf_1%2C%20code_nsf_1%2C%20code_certifinfo%2C%20siret%2C%20numero_formation%2C%20intitule_formation%2C%20points_forts%2C%20nb_action%2C%20nb_session_active%2C%20nb_session_a_distance%2C%20nombre_heures_total_min%2C%20nombre_heures_total_max%2C%20nombre_heures_total_mean%2C%20frais_ttc_tot_min%2C%20frais_ttc_tot_max%2C%20frais_ttc_tot_mean%2C%20code_departement%2C%20code_region%2C%20nbaction_nbheures%2C%20coderegion_export&where=code_nsf_1%20%3D%20%22326%22&limit=-1&timezone=UTC&use_labels=false&epsg=4326'
    df__cf_cleaned = pd.read_json(url)
    return df__cf_cleaned
    

def load_clean_test():
    url = 'https://opendata.caissedesdepots.fr/api/explore/v2.1/catalog/datasets/moncompteformation_catalogueformation/exports/json?select=date_extract%2C%20nom_of%2C%20nom_departement%2C%20nom_region%2C%20type_referentiel%2C%20code_inventaire%2C%20code_rncp%2C%20intitule_certification%2C%20libelle_niveau_sortie_formation%2C%20code_formacode_1%2C%20code_formacode_2%2C%20code_formacode_3%2C%20code_formacode_4%2C%20code_formacode_5%2C%20libelle_code_formacode_principal%2C%20libelle_nsf_1%2C%20code_nsf_1%2C%20code_certifinfo%2C%20siret%2C%20numero_formation%2C%20intitule_formation%2C%20points_forts%2C%20nb_action%2C%20nb_session_active%2C%20nb_session_a_distance%2C%20nombre_heures_total_min%2C%20nombre_heures_total_max%2C%20nombre_heures_total_mean%2C%20frais_ttc_tot_min%2C%20frais_ttc_tot_max%2C%20frais_ttc_tot_mean%2C%20code_departement%2C%20code_region%2C%20nbaction_nbheures%2C%20coderegion_export&where=code_nsf_1%20%3D%20%22326%22&limit=100&timezone=UTC&use_labels=false&epsg=4326'
    df_cf_test = pd.read_json(url).to_csv('test_cf')
    return df_cf_test

load_clean_compteformation()

#load_clean_test()

# transformer url via urlib et urlencode et request dont tu engegitres la reponse dans un json/csv
# conditions pour declencher ex: si mise a jour effectuée 