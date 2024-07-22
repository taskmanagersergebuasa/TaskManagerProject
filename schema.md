```mermaid
---
simplon formation schema
---
erDiagram

  FORMATION {
      id_formation int PK
      titre_formation varchar
      filiere varchar
      nom_of varchar

  }

  CERTIFICATION {
      id_certif varchar PK
      type_certif varchar PK
      certification_name varchar
      niveau varchar
      etat int
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
      siret string PK
      legal_name varchar
      
  }

  FORMATION_CERTIFICATION {
      id_formation int PK, FK
      id_certif string PK, FK
      type_certif string PK, FK
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
      id_certif string PK, FK
      type_certif string PK,FK
      siret string PK, FK
  }

  SESSION {
      id_session int PK
      id_formation int FK
      date_debut date
      location varchar
      duree int
  }

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

  COMPTEFORMATION {
    id_compte_formation int PK, FK
    nom_of varchar
    inititule_certification varchar

  }
  COMPTEFORMATION_CERTIFICATION {
    id_compte_formation int PK, FK
    id_certif varchar PK, FK
    type_certif varchar PK, FK
  }
  COMPTEFORMATION_NSF {
    id_compte_formation int PK, FK
    NSF_code int PK, FK
  }
  COMPTEFORMATION_FORMA {
    id_compte_formation int PK, FK
    forma_code int PK, FK
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
  COMPTEFORMATION ||--|{ COMPTEFORMATION_CERTIFICATION : has
  COMPTEFORMATION ||--|{ COMPTEFORMATION_NSF : has
  COMPTEFORMATION ||--|{ COMPTEFORMATION_FORMA : has
  COMPTEFORMATION_CERTIFICATION||--|{ CERTIFICATION : has
  COMPTEFORMATION_NSF ||--|{ NSF : has
  COMPTEFORMATION_FORMA ||--|{ FORMA : has