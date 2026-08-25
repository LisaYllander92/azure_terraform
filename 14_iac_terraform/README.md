## Terraform + Azure – Setup

### 1. Installera Terraform
- Ladda ner binären från [Hashicorp](https://developer.hashicorp.com/terraform/install)
- Lägg `terraform.exe` i `C:\Program Files\Terraform`
- Lägg till mappen i PATH (Systemegenskaper → Miljövariabler)
- Verifiera: `terraform version`

### 2. Installera Azure CLI
```powershell
Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi; Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'; rm .\AzureCLI.msi
```
Verifiera: `az --version` (öppna nytt terminalfönster om det inte känns igen)

### 3. Logga in och sätt subscription
```powershell
az login
az account show --query id -o tsv   # för att se subscription id
```

### 4. Sätt miljövariabel (för Terraform)
```powershell
$Env:ARM_SUBSCRIPTION_ID = "<SUBSCRIPTION_ID>"
```
> Gäller bara för den aktuella sessionen – måste köras igen i nya fönster.

### 5. VS Code & skapa main.tf

Skapa filen `main.tf` i projektmappen och klistra in:

```hcl
# Configure the Azure provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0.2"
    }
  }

  required_version = ">= 1.1.0"
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "myTFResourceGroup" # Namnet kan bytas ut 
  location = "swedencentral"
}
```

### 6. Bygg infrastruktur
```bash
terraform init      # initiera backend/plugins
terraform plan       # visa vad som kommer skapas
terraform apply -auto-approve   # skapa infrastruktur
```

### 7. Städa upp
```bash
terraform destroy -auto-approve
```

### ⚠️ .gitignore
Lägg till [Terraform .gitignore](https://github.com/github/gitignore/blob/main/Terraform.gitignore) **innan** du committar – annars kan `.tfstate`-filer med känslig info hamna på GitHub.