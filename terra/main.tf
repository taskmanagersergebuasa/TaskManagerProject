provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "TaskManagerResourceGroup"
  location = "France Central"
}

resource "azurerm_storage_account" "storage_account" {
  name                     = "taskmgrstorageacct"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_service_plan" "app_service_plan" {
  name                = "TaskManagerAppServicePlan"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  sku {
    tier = "Basic"
    size = "B1"
  }
}

resource "azurerm_function_app" "function_app" {
  name                       = "ScrapingFunctionApp"
  resource_group_name        = azurerm_resource_group.rg.name
  location                   = azurerm_resource_group.rg.location
  app_service_plan_id        = azurerm_app_service_plan.app_service_plan.id
  storage_account_name       = azurerm_storage_account.storage_account.name
  storage_account_access_key = azurerm_storage_account.storage_account.primary_access_key

  app_settings = {
    "WEBSITE_NODE_DEFAULT_VERSION" = "~14"
    "FUNCTIONS_WORKER_RUNTIME"     = "python"
    "AzureWebJobsStorage"          = "DefaultEndpointsProtocol=https;AccountName=${azurerm_storage_account.storage_account.name};AccountKey=${azurerm_storage_account.storage_account.primary_access_key};EndpointSuffix=core.windows.net"
    "POSTGRESQL_SERVER"            = var.postgresql_server_name
    "POSTGRESQL_DB_NAME"           = var.postgresql_db_name
    "POSTGRESQL_ADMIN_LOGIN"       = var.postgresql_admin_login
    "POSTGRESQL_ADMIN_PASSWORD"    = var.postgresql_admin_password
  }

  site_config {
    always_on = true
  }
}

resource "azurerm_postgresql_server" "server" {
  name                         = var.postgresql_server_name
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = azurerm_resource_group.rg.location
  version                      = "11"
  administrator_login          = var.postgresql_admin_login
  administrator_login_password = var.postgresql_admin_password
  ssl_enforcement_enabled      = true
  sku_name                     = "B_Gen5_1"
}

resource "azurerm_postgresql_database" "db" {
  name                = var.postgresql_db_name
  resource_group_name = azurerm_resource_group.rg.name
  server_name         = azurerm_postgresql_server.server.name
  charset             = var.postgresql_charset
  collation           = var.postgresql_collation
}

resource "azurerm_storage_blob" "python_script" {
  name                   = "function_app.py"
  storage_account_name   = azurerm_storage_account.storage_account.name
  storage_container_name = azurerm_storage_container.container.name
  type                   = "Block"
  source                 = "function_app.py"
}

resource "azurerm_storage_container" "container" {
  name                  = "scripts"
  storage_account_name  = azurerm_storage_account.storage_account.name
  container_access_type = "private"
}
