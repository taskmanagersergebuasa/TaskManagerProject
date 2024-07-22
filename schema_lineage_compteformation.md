```mermaid
---
simplon formation schema
---
erDiagram

COMPTE_FORMATION_ORIGINE {
    id_compte_formation int PK
    date_extract date
    nom_of varchar
    nom_departement varchar
    nom_region varchar
    type_referentiel varchar
    id_certif int
    intitule_certification varchar
    libelle_niveau_sortie_formation varchar
    code_formacode_1 int
    code_formacode_2 int
    code_formacode_3 int
    code_formacode_4 int
    code_formacode_5 int
    libelle_code_formacode_principal varchar
    libelle_nsf_1 varchar
    libelle_nsf_2 varchar
    libelle_nsf_3 varchar
    code_nsf_1 int
    code_nsf_2 int
    code_nsf_3 int
    code_certifinfo int
    siret string
    nb_action int
    nb_session_active int
    nb_session_a_distance int
    nombre_heures_total_min int
    nombre_heures_total_max int
    nombre_heures_total_mean int
    frais_ttc_tot_min int
    frais_ttc_tot_max int
    frais_ttc_tot_mean int
    code_departement int
    code_region int
    nbaction_nbheures int    
    coderegion_export int
  }