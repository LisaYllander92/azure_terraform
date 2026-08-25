# Spin up en Windows VM i Azure + Bastion

Guide för att skapa en Windows-VM via Azure Portal, förstå vad som skapas automatiskt, och logga in säkert via Bastion.

## 1. Skapa VM:n

Görs i **Azure Portal** (portal.azure.com) – inte via VS Code/Terraform. Poängen är att förstå manuellt vad en VM drar med sig innan man automatiserar det.

1. Sök på **"Virtual machines"** → **"+ Create"** → **"Azure virtual machine"**
2. **Basics**:
   - Resource group: skapa ny
   - Image: t.ex. Windows Server 2025 Datacenter
   - Size: **Standard_B2s** (billig, B-serien funkar oftast bäst för studentkonton – D-serien kan ge felet `NotAvailableForSubscription` i vissa regioner)
   - Username/password: sätt admin-uppgifter – spara dessa, de behövs för inloggning
   - Public inbound ports: **None** (Bastion kräver inte öppen RDP-port, och det är säkrare)
3. **Disks**: Standard HDD räcker för test (billigast)
4. **Networking**: Public IP → **None** om möjligt (Bastion sköter åtkomsten)
5. **Management**: aktivera **Auto-shutdown** som säkerhetsnät mot att glömma VM:n igång
6. **Monitoring/Advanced/Tags**: standardvärden räcker
7. **Review + create** → **Create**

## 2. Logga in via Azure Bastion

Bastion låter dig ansluta till VM:n **i webbläsaren**, utan att VM:n behöver en publik IP eller öppen RDP-port (port 3389). Trafiken går internt i Azures nätverk istället för över internet – vilket skyddar mot brute-force-attacker mot öppna RDP-portar.

1. Gå till VM:n → **"Connect"** → **"Bastion"**
2. Om Bastion inte redan finns, skapa den via guiden (kräver ett eget subnät `AzureBastionSubnet` + en publik IP)
3. Logga in med admin-uppgifterna från steg 1

**RDP** = Remote Desktop Protocol, Microsofts protokoll för fjärrskrivbord. Bastion kör en RDP-session åt dig i bakgrunden, fast över en säker tunnel.

## 3. Vad skapas automatiskt? (bra att titta igenom)

| Resurs | Vad den gör |
|---|---|
| **Virtual Machine** | Själva servern |
| **Network Interface (NIC)** | VM:ns "nätverkskort", har VM:ns privata IP |
| **Network Security Group (NSG)** | Brandväggen – kolla "Inbound security rules" för att se att RDP inte är öppet mot internet |
| **Virtual Network (VNet) + Subnet** | Nätverket VM:n lever i |
| **AzureBastionSubnet** | Eget obligatoriskt subnät för Bastion |
| **Azure Bastion** | Själva Bastion-resursen (kolla SKU: Basic är billigast) |
| **Public IP** | Kopplad till Bastion (inte VM:n om du valde "None") – Bastion behöver en egen publik IP |
| **OS-disk** | Kostar lite pengar även när VM:n är avstängd, tills resursgruppen tas bort |
| **Boot diagnostics storage account** | Skapas ibland automatiskt för att lagra boot-skärmdumpar |

Tips: **Resursgrupp → "Cost analysis"** visar vilken resurs som drar mest kostnad.

## 4. Stänga ner ordentligt (viktigt för att spara kredit!)

Att bara stänga webbläsarfönstret stänger **bara anslutningen** – VM:n fortsätter köra och kosta pengar.

1. (Valfritt) Logga ut ur Windows inifrån VM:n
2. Stäng Bastion-fönstret/webbläsarfliken
3. **Gå till VM:n i Azure Portal → klicka "Stop"**
4. Vänta tills status blir **"Stopped (deallocated)"** – först då slutar du betala för compute (CPU/minne). Bara "Stopped" utan "deallocated" kan fortfarande kosta.

Disk och ev. Bastion/Public IP fortsätter kosta lite tills resursgruppen tas bort helt.

## 5. Ta bort allt permanent

När du är helt klar med momentet:

- Ta bort hela **resursgruppen** i Azure Portal (raderar alla resurser i den, inkl. VM, disk, NSG, Bastion, public IP)