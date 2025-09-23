# Account Service

Account Service håndterer brugerkonti, herunder registrering, autentificering og profiladministration. Behandler login, logout, passwordhåndtering og brugerroller.

## API Endpoints

### POST /profile
Registrerer en ny bruger
- **Body**: `{ "username": "string", "password": "string" }`
- **Response**: Success message ved succesfuld registrering

### GET /profile
Viser brugerprofil (kræver login)
- **Headers**: `Authorization: username`
- **Response**: Brugerdata

### PUT /profile
Redigerer brugerprofil
- **Response**: Success status

### POST /login
Logger bruger ind
- **Body**: `{ "username": "string", "password": "string" }`
- **Response**: Success message med Authorization header

### POST /logout
Logger bruger ud
- **Response**: Success status

## Kørsel

```bash
python app.py
```

Servicen kører på port 5000 som standard.

## Noter

- Bruger i øjeblikket in-memory database (skal skiftes til SQLite)
- Henter initial testdata fra dummyjson.com