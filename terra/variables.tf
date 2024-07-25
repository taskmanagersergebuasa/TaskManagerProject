variable "postgresql_server_name" {
  description = "Nom du serveur PostgreSQL"
  type        = string
  default     = "taskmanager-serveur-postgresql"
}

variable "postgresql_admin_login" {
  description = "Nom d'utilisateur de l'administrateur PostgreSQL"
  type        = string
  default     = "adminpostgresql"
}

variable "postgresql_admin_password" {
  description = "Mot de passe de l'administrateur PostgreSQL"
  type        = string
  sensitive   = true
}

variable "postgresql_db_name" {
  description = "Nom de la base de données PostgreSQL"
  type        = string
  default     = "taskmanager-db"
}

variable "postgresql_collation" {
  description = "Collation à utiliser pour la base de données PostgreSQL"
  type        = string
  default     = "French_France.1252"
}

variable "postgresql_charset" {
  description = "Charset à utiliser pour la base de données PostgreSQL"
  type        = string
  default     = "UTF8"
}
