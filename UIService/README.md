# UI Service

UI Service leverer en web-baseret brugerinterface til Shopping Site ved hjælp af Streamlit. Viser produktkataloget og håndterer brugerautentificering.

## Funktioner

### Produktkatalog
- Viser alle produkter fra Product Catalog Service
- Produktinformation inkluderer:
  - Billede (thumbnail)
  - Titel
  - Pris i DKK
  - Mærke
  - Kategori
  - Beskrivelse

### Brugerautentificering
- **Login**: Brugere kan logge ind med eksisterende konto
- **Registrering**: Nye brugere kan oprette konto
- **Logout**: Brugere kan logge ud
- Session management via Streamlit session state
- Integration med Account Service for autentificering

## Sidebar Funktionalitet

Når **ikke logget ind**:
- Login tab med brugernavn og adgangskode felter
- Register tab til oprettelse af ny konto med bekræftelse af adgangskode

Når **logget ind**:
- Viser brugernavn
- Logout knap

## Service Integration

- **Account Service** (http://acc:5000): Brugerautentificering og registrering
  - POST /login: Login endpoint
  - POST /profile: Registrering endpoint
- **Product Catalog Service** (http://products:5000): Produktdata
  - GET /products: Henter alle produkter med DKK priser

## Session State

Applikationen vedligeholder følgende session state:
- `logged_in`: Boolean - brugerens login status
- `username`: String - den aktuelle brugers brugernavn
- `auth_token`: String - autorisation token fra Account Service

## Kørsel

```bash
streamlit run app.py
```

Servicen kører på port 8501 som standard.

## Teknologi

- **Framework**: Streamlit
- **HTTP Client**: Requests library
- **UI Komponenter**:
  - Tabs for login/registrering
  - Sidebar til brugerinteraktion
  - Container og kolonner til produktvisning
  - Session state til autentificering

## Noter

- Brugersession er kun gemt i browseren og går tabt ved refresh
- Authorization token gemmes i session state for fremtidige API kald
- Fejlhåndtering for både Account Service og Product Service forbindelser
