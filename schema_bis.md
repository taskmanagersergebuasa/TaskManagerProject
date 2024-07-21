```mermaid
---
simplon formation schema
---
erDiagram

  FORMATION {
      id_formation int PK
      titre_formation varchar
      intitule_certification varchar
      nom_of varchar
      id_certif varchar   
            
  }

   CERTIFICATION {
      id_certif int PK
      certification_name varchar
      niveau varchar
      etat varchar
  }


  NSF {
      NSF_code int PK
      NSF_name varchar
  }

  FORMA {
      forma_code int PK
      forma_name varchar
  }

  CERTIFICATEUR {
      siret int PK
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
      siret int PK, FK
  }

  SESSION {
      id_session int PK
      id_formation int FK
      date_debut date
      location varchar
  }

  COMPTE_FORMATION_ORIGINE {
    id_formation int PK
    date_extract date
    nom_of varchar
    nom_departement varchar
    nom_region varchar
    type_referentiel varchar
    code_certif int FK
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

  
  FORMATION ||--|{ FORMATION_CERTIFICATION : has
  FORMATION ||--|{ FORMATION_NSF : has
  FORMATION ||--|{ FORMATION_FORMA : has
  FORMATION ||--|{ SESSION : has
  CERTIFICATION ||--|{ CERTIFICATION_CERTIFICATEUR : has
  FORMATION_CERTIFICATION ||--|{ CERTIFICATION : has
  FORMATION_NSF ||--|{ NSF : has
  FORMATION_FORMA ||--|{ FORMA : has
  CERTIFICATION_CERTIFICATEUR ||--|{ CERTIFICATEUR : has
  