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

  CERTIFICATION_NSF {
      id_certif varchar PK, FK
      type_certif varchar PK,FK
      NSF_code int PK, FK
  }

  CERTIFICATION_FORMA {
    id_certif varchar PK, FK
    type_certif varchar PK,FK
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
  FORMATION_CERTIFICATION ||--|{ CERTIFICATION : has
  NSF ||--|{ CERTIFICATION_NSF : has
  FORMA ||--|{ CERTIFICATION_FORMA : has
  CERTIFICATION_NSF ||--|{ CERTIFICATION: has
  CERTIFICATION_FORMA ||--|{ CERTIFICATION: has
  FORMATION ||--|{ SESSION : has
  CERTIFICATION ||--|{ CERTIFICATION_CERTIFICATEUR : has 
  CERTIFICATION_CERTIFICATEUR ||--|{ CERTIFICATEUR : has
  COMPTEFORMATION ||--|{ COMPTEFORMATION_CERTIFICATION : has
  COMPTEFORMATION ||--|{ COMPTEFORMATION_NSF : has
  COMPTEFORMATION ||--|{ COMPTEFORMATION_FORMA : has
  COMPTEFORMATION_CERTIFICATION||--|{ CERTIFICATION : has
  COMPTEFORMATION_NSF ||--|{ NSF : has
  COMPTEFORMATION_FORMA ||--|{ FORMA : has