```mermaid
---
simplon formation schema
---
erDiagram

  FORMATION {
      id_formation int PK
      titre_formation varchar
      filiere varchar

  }

  CERTIFICATION {
      id_certif int PK
      certification_name varchar
      niveau varchar
      etat varchar
  }

  NSF {
      NSF_code String PK
      NSF_name varchar
  }

  FORMA {
      forma_code int PK
      forma_name varchar
  }

  CERTIFICATEUR {
      Siret int PK
      legal_name varchar
      Commercial_name varchar
      internet_site varchar
  }

  FORMATION_CERTIFICATION {
      id_formation int PK, FK
      id_certif int PK, FK
  }

  FORMATION_NSF {
      id_formation int PK, FK
      NSF_code int PK, FK
  }

  FORMATION_FORMA {
      id_formation int PK, FK
      forma_code int PK, FK
  }

  CERTIFICATION_CERTIFICATEUR {
      id_certif int PK, FK
      Siret int PK, FK
  }

  FORMATION_SESSION {
      id_session int PK
      id_formation int 
      date_debut date
      location varchar
  }

  COMPTE_FORMATION {
    id_compte_formation int PK
    date_extract
    nom_of
    nom_departement
    nom_region
    type_referentiel
    code_inventaire
    code_rncp
    intitule_certification
    libelle_niveau_sortie_formation
    code_formacode_1
    code_formacode_2
    code_formacode_3
    code_formacode_4
    code_formacode_5
    libelle_code_formacode_principal
    libelle_nsf_1
    code_nsf_1
    code_certifinfo
    siret
    nb_action
    nb_session_active
    nb_session_a_distance
    nombre_heures_total_min
    nombre_heures_total_max
    nombre_heures_total_mean
    frais_ttc_tot_min
    frais_ttc_tot_max
    frais_ttc_tot_mean
    code_departement
    code_region
    nbaction_nbheures
    coderegion_export
  }

  FORMATION ||--|{ FORMATION_CERTIFICATION : has
  FORMATION ||--|{ FORMATION_NSF : has
  FORMATION ||--|{ FORMATION_FORMA : has
  FORMATION ||--|{ FORMATION_SESSION : has
  CERTIFICATION ||--|{ CERTIFICATION_CERTIFICATEUR : has
  FORMATION_CERTIFICATION ||--|{ CERTIFICATION : has
  FORMATION_NSF ||--|{ NSF : has
  FORMATION_FORMA ||--|{ FORMA : has
  CERTIFICATION_CERTIFICATEUR ||--|{ CERTIFICATEUR : has
