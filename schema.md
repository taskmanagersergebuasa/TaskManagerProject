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
      NSF_code int PK
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

  FORMATION ||--|{ FORMATION_CERTIFICATION : has
  FORMATION ||--|{ FORMATION_NSF : has
  FORMATION ||--|{ FORMATION_FORMA : has
  FORMATION ||--|{ FORMATION_SESSION : has
  CERTIFICATION ||--|{ CERTIFICATION_CERTIFICATEUR : has
  FORMATION_CERTIFICATION ||--|{ CERTIFICATION : has
  FORMATION_NSF ||--|{ NSF : has
  FORMATION_FORMA ||--|{ FORMA : has
  CERTIFICATION_CERTIFICATEUR ||--|{ CERTIFICATEUR : has
