resource "azurerm_resource_group" "storage_rg" {
  name = "youtube-analytics-rg"
  location = var.location
}