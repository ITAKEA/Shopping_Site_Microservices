# Account Service

Account Service håndterer brugerkonti, herunder registrering, autentificering og profiladministration. Behandler login, logout, passwordhåndtering og brugerroller.

## Projektstruktur

- `app.py`: Flask applikation med API endpoints
- `database.py`: Database modul til brugerdata håndtering og lagring

## API Endpoints

### POST /profile
Registrerer en ny bruger
- **Body**: `{ "username": "string", "password": "string" }`
- **Response**: Success message ved succesfuld registrering

### GET /profile
Viser brugerprofil (kræver JWT token)
- **Headers**: `Authorization: Bearer <JWT_TOKEN>`
- **Response**: Brugerdata (username, id)
- **Kræver autentificering**: Ja (@jwt_required decorator)

### PUT /profile
Redigerer brugerprofil
- **Response**: Success status

### POST /login
Logger bruger ind og returnerer JWT token
- **Body**: `{ "username": "string", "password": "string" }`
- **Response**: Success message med JWT token i Authorization header
- **Header Response**: `Authorization: Bearer <JWT_TOKEN>`

### POST /logout
Logger bruger ud
- **Response**: Success status

## JWT Autentificering

Account Service bruger **Flask-JWT-Extended** til token-baseret autentificering:

### Konfiguration
- **JWT Secret Key**: Gemt i `.env` fil som `KEY` environment variable
- **Token Type**: Bearer tokens
- **Library**: Flask-JWT-Extended med PyJWT

### Autentificeringsflow
1. Bruger logger ind via `/login` endpoint
2. Server validerer credentials mod SQLite database
3. Ved success returneres JWT token i `Authorization` header som `Bearer <token>`
4. Client inkluderer token i Authorization header for beskyttede endpoints
5. `@jwt_required()` decorator validerer token på beskyttede routes

### Beskyttede Endpoints
- `GET /profile`: Kræver valid JWT token

## Kørsel

```bash
python app.py
```

Servicen kører på port 5000 som standard.

**Vigtigt**: Sørg for at `.env` filen eksisterer med `KEY=your-secret-key`

## Database Modul

Database funktionaliteten er separeret i `database.py` og bruger SQLite:

### Database Schema
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
```

### Funktioner
- `init_db()`: Initialiserer databasen med users tabel
- `get_db_connection()`: Opretter en database forbindelse
- `find_user_by_username(username)`: Finder bruger ved username
- `add_user(username, password)`: Tilføjer ny bruger til databasen
- `get_all_users()`: Returnerer alle brugere

### Database Fil
- Fil: `users.db` (oprettet automatisk)
- Placering: AccountService directory
- Starter tom - ingen testdata inkluderet

## Noter

- Bruger SQLite database for persistent datahåndtering
- Database initialiseres automatisk ved import af modulet
- Brugernavn skal være unikt (UNIQUE constraint)
- Database logik er modulariseret i separat fil for bedre kodestruktur
- Database fil gemmes lokalt og vil persistere mellem genstart