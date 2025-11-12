# Shopping Site Microservices Arkitektur

Dette dokument giver et omfattende arkitektonisk overblik over Shopping Site Microservices applikationen.

## System Oversigt

Applikationen består af 4 microservices deployed ved hjælp af Docker:
- **Account Service**: Brugerregistrering og autentificering
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
        subgraph UI["UI Service :8501"]
            Streamlit["Streamlit Web Interface<br/>- Product Display<br/>- Images & Details<br/>- Prices in DKK"]
        end

        subgraph Account["Account Service :5010"]
            AccService["Flask REST API<br/>- User Registration<br/>- Login/Logout<br/>- Profile Management<br/><br/>In-Memory Storage"]
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
    APIClient -->|HTTP :5010| AccService
    APIClient -->|HTTP :5020| CurService
    APIClient -->|HTTP :5030| ProdService

    Streamlit -->|GET /products| ProdService
    ProdService -->|POST /convert| CurService
    ProdService -->|GET products| DummyJSON
    AccService -->|GET users| DummyJSON

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
    participant PS as Product Catalog<br/>Service
    participant CS as Currency<br/>Service
    participant Ext as External API<br/>(dummyjson)

    User->>UI: Access Web Interface
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
        U1["/ (Root)<br/>Web Interface"]
    end

    P1 --> C1
    P2 --> C1
    P3 --> C1
    P4 --> C1
    U1 --> P1

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
- **Synkron HTTP/REST**: Al inter-service kommunikation bruger REST APIs
- **Ingen Message Queues**: Ingen asynkron messaging implementeret
- **Docker DNS**: Services opdager hinanden via container navne

### Data Lagring
- **Account Service**: In-memory liste (planlagt migration til SQLite)
- **Currency Service**: In-memory dictionary med statiske exchange rates
- **Product Catalog**: External API (dummyjson.com) - ingen lokal lagring
- **Ingen Persistent Database**: Al data er volatil og går tabt ved restart

### Skalerbarhed
- **Uafhængige Services**: Hver service kan skaleres uafhængigt
- **Stateless Design**: Services vedligeholder ikke session state
- **Docker Orchestration**: Bruger Docker Compose til lokal deployment

### Sikkerhedsovervejelser
- **Autentificering**: Account service bruger Authorization header
- **Ingen API Gateway**: Services eksponeres direkte på forskellige porte
- **Plain Text Data**: Credentials gemmes in-memory uden kryptering
- **Ingen HTTPS**: Al kommunikation over HTTP

### Eksterne Afhængigheder
- **dummyjson.com**: Leverer produkt og bruger seed data
- **Single Point of Failure**: External API utilgængelighed påvirker servicen

## Deployment Instruktioner

1. **Forudsætninger**: Docker og Docker Compose installeret

2. **Start Services**:
   ```bash
   docker-compose up
   ```

3. **Adgangspunkter**:
   - Web UI: http://localhost:8501
   - Account API: http://localhost:5010
   - Currency API: http://localhost:5020
   - Product API: http://localhost:5030

4. **Service Opstartsrækkefølge**:
   - Currency Service starter først
   - Product Catalog Service (afhænger af Currency)
   - UI Service (afhænger af Product Catalog)
   - Account Service (uafhængig)

## Fremtidige Forbedringsmuligheder

1. **Persistent Storage**: Migrer til SQLite eller PostgreSQL
2. **API Gateway**: Tilføj central routing og autentificeringslag
3. **Caching**: Implementer Redis til produkt og valutadata
4. **Message Queue**: Tilføj RabbitMQ/Kafka til async operationer
5. **Service Discovery**: Implementer Consul eller Eureka
6. **Load Balancing**: Tilføj nginx eller Traefik
7. **Monitoring**: Integrer Prometheus og Grafana
8. **Logging**: Centraliseret logging med ELK stack
9. **Security**: Tilføj OAuth2, HTTPS, secret management
10. **Resilience**: Implementer circuit breakers og retry patterns
