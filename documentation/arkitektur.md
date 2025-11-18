# Shopping Site Microservices Arkitektur

Dette dokument giver et omfattende arkitektonisk overblik over Shopping Site Microservices applikationen.

## System Oversigt

Applikationen består af 5 microservices deployed ved hjælp af Docker:
- **API Gateway**: Central routing og indgangspunkt for alle services
- **Account Service**: Brugerregistrering og autentificering (modulariseret med separat database lag)
- **Currency Service**: Valutakonverteringsfunktionalitet
- **Product Catalog Service**: Produktlisting og administration
- **UI Service**: Web-baseret brugerinterface (Streamlit)

## Arkitektur Diagram

```mermaid
graph TB
    subgraph External["External Systems"]
        DummyJSON["dummyjson.com API<br/>(Product & User Data)"]
    end

    subgraph Docker["Docker Network (app-network)"]
        subgraph Gateway["API Gateway :8000"]
            GatewayService["Flask REST API<br/>- Request Routing<br/>- Simple Proxy<br/>- Unified API"]
        end

        subgraph UI["UI Service :8501"]
            Streamlit["Streamlit Web Interface<br/>- Product Display<br/>- Images & Details<br/>- Prices in DKK"]
        end

        subgraph Account["Account Service :5010"]
            AccService["Flask REST API<br/>- User Registration<br/>- Login/Logout<br/>- Profile Management<br/><br/>SQLite Database"]
        end

        subgraph Currency["Currency Service :5020"]
            CurService["Flask REST API<br/>- Currency Conversion<br/>- USD, EUR, DKK<br/><br/>In-Memory Exchange Rates"]
        end

        subgraph Product["Product Catalog Service :5030"]
            ProdService["Flask REST API<br/>- List Products<br/>- Search Products<br/>- Filter by Category<br/>- Price Conversion"]
        end
    end

    subgraph Users["Users"]
        Browser["Web Browser"]
        APIClient["API Client"]
    end

    Browser -->|HTTP :8501| Streamlit
    APIClient -->|HTTP :8000| GatewayService

    GatewayService -->|/api/account/*| AccService
    GatewayService -->|/api/currency/*| CurService
    GatewayService -->|/api/products/*| ProdService

    Streamlit -->|GET /products| ProdService
    Streamlit -->|POST /login, /profile| AccService
    ProdService -->|POST /convert| CurService
    ProdService -->|GET products| DummyJSON

    style Gateway fill:#ffe8e8
    style UI fill:#e1f5ff
    style Account fill:#fff4e1
    style Currency fill:#e8f5e9
    style Product fill:#f3e5f5
    style External fill:#ffebee
```

## Service Kommunikationsflow

```mermaid
sequenceDiagram
    actor User
    participant UI as UI Service<br/>(Streamlit)
    participant AS as Account<br/>Service
    participant PS as Product Catalog<br/>Service
    participant CS as Currency<br/>Service
    participant Ext as External API<br/>(dummyjson)

    User->>UI: Access Web Interface

    alt User Registration
        User->>UI: Register new account
        UI->>AS: POST /profile<br/>{username, password}
        AS-->>UI: Registration success
        UI-->>User: Show success message
    end

    alt User Login
        User->>UI: Login
        UI->>AS: POST /login<br/>{username, password}
        AS-->>UI: Auth token in header
        UI-->>User: Login successful
    end

    UI->>PS: GET /products
    PS->>Ext: Fetch product data
    Ext-->>PS: Product list (USD prices)

    loop For each product
        PS->>CS: POST /convert<br/>{amount, from:USD, to:DKK}
        CS-->>PS: Converted price (DKK)
    end

    PS-->>UI: Products with DKK prices
    UI-->>User: Display products with images
```

## API Endpoints

```mermaid
graph LR
    subgraph Account["Account Service :5010"]
        A1["/profile - POST<br/>Register User"]
        A2["/profile - GET<br/>View Profile"]
        A3["/profile - PUT<br/>Edit Profile"]
        A4["/login - POST<br/>Login"]
        A5["/logout - POST<br/>Logout"]
    end

    subgraph Currency["Currency Service :5020"]
        C1["/convert - POST<br/>Convert Currency"]
    end

    subgraph Product["Product Catalog :5030"]
        P1["/products - GET<br/>All Products"]
        P2["/products/&lt;id&gt; - GET<br/>Product by ID"]
        P3["/products/search - GET<br/>Search by Title"]
        P4["/products/category/&lt;name&gt;<br/>Filter by Category"]
    end

    subgraph UI["UI Service :8501"]
        U1["/ (Root)<br/>Web Interface<br/>Login & Registration"]
    end

    P1 --> C1
    P2 --> C1
    P3 --> C1
    P4 --> C1
    U1 --> P1
    U1 --> A4
    U1 --> A1

    style Account fill:#fff4e1
    style Currency fill:#e8f5e9
    style Product fill:#f3e5f5
    style UI fill:#e1f5ff
```

## Container Arkitektur

```mermaid
graph TB
    subgraph Deployment["Docker Compose Deployment"]
        subgraph Network["app-network (Bridge Network)"]
            ACC["Container: acc<br/>Image: python:slim-trixie<br/>Port: 5010:5000<br/>Restart: unless-stopped"]
            CUR["Container: cur<br/>Image: python:3.12-slim<br/>Port: 5020:5000<br/>Restart: unless-stopped"]
            PROD["Container: products<br/>Image: python:3.12-slim<br/>Port: 5030:5000<br/>Restart: unless-stopped<br/>depends_on: cur"]
            UI_C["Container: ui<br/>Image: python:3.12-slim<br/>Port: 8501:8501<br/>Restart: unless-stopped<br/>depends_on: products"]
        end
    end

    CUR -.->|dependency| PROD
    PROD -.->|dependency| UI_C

    style ACC fill:#fff4e1
    style CUR fill:#e8f5e9
    style PROD fill:#f3e5f5
    style UI_C fill:#e1f5ff
```

## Technology Stack

```mermaid
graph LR
    subgraph Backend["Backend Services"]
        Flask["Flask Framework<br/>Account, Currency, Product"]
        Python["Python 3.12<br/>All Services"]
    end

    subgraph Frontend["Frontend"]
        Streamlit["Streamlit Framework<br/>UI Service"]
    end

    subgraph Infrastructure["Infrastructure"]
        Docker["Docker Containers"]
        Network["Docker Bridge Network"]
    end

    subgraph External["External Dependencies"]
        Requests["Requests Library<br/>HTTP Client"]
        API["dummyjson.com API<br/>Data Source"]
    end

    Python --> Flask
    Python --> Streamlit
    Flask --> Requests
    Streamlit --> Requests
    Requests --> API
    Flask --> Docker
    Streamlit --> Docker
    Docker --> Network

    style Backend fill:#fff4e1
    style Frontend fill:#e1f5ff
    style Infrastructure fill:#e8f5e9
    style External fill:#ffebee
```

## Data Flow Arkitektur

```mermaid
flowchart TD
    Start([User Request]) --> UI[UI Service]
    UI --> Cache{Cache<br/>Available?}
    Cache -->|No| ProdAPI[Product Catalog API]
    Cache -->|Yes| Display

    ProdAPI --> ExtAPI[External API Call<br/>dummyjson.com]
    ExtAPI --> ProdData[Product Data<br/>USD Prices]

    ProdData --> ConvertLoop{For Each<br/>Product}
    ConvertLoop --> CurrAPI[Currency Service<br/>POST /convert]
    CurrAPI --> Rates[Exchange Rates<br/>In-Memory]
    Rates --> Converted[Converted Price<br/>DKK]
    Converted --> ConvertLoop

    ConvertLoop -->|All Done| Display[Display Products<br/>with DKK Prices]
    Display --> End([Rendered UI])

    style UI fill:#e1f5ff
    style ProdAPI fill:#f3e5f5
    style CurrAPI fill:#e8f5e9
    style ExtAPI fill:#ffebee
```

## Service Dependencies

```mermaid
graph TD
    UI[UI Service<br/>Streamlit :8501]
    PS[Product Catalog Service<br/>Flask :5030]
    CS[Currency Service<br/>Flask :5020]
    AS[Account Service<br/>Flask :5010]
    EXT[External APIs<br/>dummyjson.com]

    UI -->|depends on| PS
    UI -->|calls| AS
    PS -->|depends on| CS
    PS -->|calls| EXT
    AS -->|calls| EXT

    style UI fill:#e1f5ff
    style PS fill:#f3e5f5
    style CS fill:#e8f5e9
    style AS fill:#fff4e1
    style EXT fill:#ffebee
```

## Nøgle Arkitektoniske Karakteristika

### Kommunikationsmønster
- **API Gateway Mønster**: Simpelt centralt indgangspunkt routing requests til services
- **Synkron HTTP/REST**: Al inter-service kommunikation bruger REST APIs
- **Ingen Message Queues**: Ingen asynkron messaging implementeret
- **Docker DNS**: Services opdager hinanden via container navne
- **Simple Proxy**: Gateway kalder services direkte og returnerer responses

### Data Lagring
- **Account Service**: SQLite database med modulariseret database lag i `database.py`
  - Separat database modul for forbedret kodeorganisering
  - Persistent lagring i `users.db` fil
  - Schema: `users` tabel med id, username, password
  - Funktioner: `init_db()`, `get_db_connection()`, `find_user_by_username()`, `add_user()`, `get_all_users()`
- **Currency Service**: In-memory dictionary med statiske exchange rates
- **Product Catalog**: External API (dummyjson.com) - ingen lokal lagring
- **Delvis Persistence**: Brugerdata persisterer mellem genstart, produkt/valutadata er volatil

### Skalerbarhed
- **Uafhængige Services**: Hver service kan skaleres uafhængigt
- **Stateless Design**: Services vedligeholder ikke session state
- **Docker Orchestration**: Bruger Docker Compose til lokal deployment

### Sikkerhedsovervejelser
- **JWT Autentificering**: Account service bruger Flask-JWT-Extended til token-baseret autentificering
  - JWT tokens genereres ved login og returneres i Authorization header som `Bearer <token>`
  - Beskyttede endpoints valideres med `@jwt_required()` decorator
  - Secret key gemt i `.env` fil (ikke committed til git)
- **API Gateway**: Simpelt centralt indgangspunkt på port 8000, services også eksponeret på individuelle porte
  - Gateway forwarder JWT tokens korrekt i Authorization header
- **Minimal Fejlhåndtering**: Gateway returnerer responses som de er fra services
- **Password Storage**: Passwords gemmes i plaintext i SQLite (bør bruge hashing i produktion)
- **Ingen HTTPS**: Al kommunikation over HTTP (bør bruge HTTPS i produktion)

### Eksterne Afhængigheder
- **dummyjson.com**: Leverer produkt seed data
- **Single Point of Failure**: External API utilgængelighed påvirker Product Catalog Service

## Deployment Instruktioner

1. **Forudsætninger**: Docker og Docker Compose installeret

2. **Start Services**:
   ```bash
   docker-compose up
   ```

3. **Adgangspunkter**:
   - API Gateway: http://localhost:8000
   - Web UI: http://localhost:8501
   - Account API: http://localhost:5010 (eller via Gateway: http://localhost:8000/api/account/*)
   - Currency API: http://localhost:5020 (eller via Gateway: http://localhost:8000/api/currency/*)
   - Product API: http://localhost:5030 (eller via Gateway: http://localhost:8000/api/products/*)

4. **Service Opstartsrækkefølge**:
   - Account, Currency Services starter først (uafhængige)
   - Product Catalog Service (afhænger af Currency)
   - API Gateway (afhænger af Account, Currency, Product Catalog)
   - UI Service (afhænger af Product Catalog)

## Fremtidige Forbedringsmuligheder

1. **Password Hashing**: Implementer bcrypt eller argon2 til sikker password lagring
2. **HTTPS/TLS**: Tilføj SSL certificates til sikker kommunikation
3. **Forbedret Lagring**: Migrer Product/Currency services til persistent lagring
4. **Token Refresh**: Implementer refresh tokens til længere sessioner
5. **Caching**: Implementer Redis til produkt og valutadata
6. **Message Queue**: Tilføj RabbitMQ/Kafka til async operationer
7. **Service Discovery**: Implementer Consul eller Eureka
8. **Load Balancing**: Tilføj nginx eller Traefik
9. **Monitoring**: Integrer Prometheus og Grafana
10. **Logging**: Centraliseret logging med ELK stack
11. **Resilience**: Implementer circuit breakers og retry patterns
