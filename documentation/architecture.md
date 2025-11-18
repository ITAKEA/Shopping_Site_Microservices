# Shopping Site Microservices Architecture

This document provides a comprehensive architectural overview of the Shopping Site Microservices application.

## System Overview

The application consists of 5 microservices deployed using Docker:
- **API Gateway**: Central routing and entry point for all services
- **Account Service**: User registration and authentication (modularized with separate database layer)
- **Currency Service**: Currency conversion functionality
- **Product Catalog Service**: Product listing and management
- **UI Service**: Web-based user interface (Streamlit)

## Architecture Diagram

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

## Service Communication Flow

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
    subgraph Gateway["API Gateway :8000"]
        G1["/api/account/*<br/>Account Routes"]
        G2["/api/currency/*<br/>Currency Routes"]
        G3["/api/products/*<br/>Product Routes"]
        G4["/health<br/>Health Check"]
    end

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

    G1 --> A1
    G1 --> A2
    G1 --> A3
    G1 --> A4
    G1 --> A5
    G2 --> C1
    G3 --> P1
    G3 --> P2
    G3 --> P3
    G3 --> P4

    P1 --> C1
    P2 --> C1
    P3 --> C1
    P4 --> C1
    U1 --> P1
    U1 --> A4
    U1 --> A1

    style Gateway fill:#ffe8e8
    style Account fill:#fff4e1
    style Currency fill:#e8f5e9
    style Product fill:#f3e5f5
    style UI fill:#e1f5ff
```

## Container Architecture

```mermaid
graph TB
    subgraph Deployment["Docker Compose Deployment"]
        subgraph Network["app-network (Bridge Network)"]
            GW["Container: gateway<br/>Image: python:3.12-slim<br/>Port: 8000:5000<br/>Restart: unless-stopped<br/>depends_on: acc, cur, products"]
            ACC["Container: acc<br/>Image: python:slim-trixie<br/>Port: 5010:5000<br/>Restart: unless-stopped"]
            CUR["Container: cur<br/>Image: python:3.12-slim<br/>Port: 5020:5000<br/>Restart: unless-stopped"]
            PROD["Container: products<br/>Image: python:3.12-slim<br/>Port: 5030:5000<br/>Restart: unless-stopped<br/>depends_on: cur"]
            UI_C["Container: ui<br/>Image: python:3.12-slim<br/>Port: 8501:8501<br/>Restart: unless-stopped<br/>depends_on: products"]
        end
    end

    ACC -.->|dependency| GW
    CUR -.->|dependency| GW
    CUR -.->|dependency| PROD
    PROD -.->|dependency| GW
    PROD -.->|dependency| UI_C

    style GW fill:#ffe8e8
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

## Data Flow Architecture

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
    GW[API Gateway<br/>Flask :8000]
    UI[UI Service<br/>Streamlit :8501]
    PS[Product Catalog Service<br/>Flask :5030]
    CS[Currency Service<br/>Flask :5020]
    AS[Account Service<br/>Flask :5010]
    EXT[External APIs<br/>dummyjson.com]

    GW -->|routes to| AS
    GW -->|routes to| CS
    GW -->|routes to| PS
    UI -->|depends on| PS
    UI -->|calls| AS
    PS -->|depends on| CS
    PS -->|calls| EXT

    style GW fill:#ffe8e8
    style UI fill:#e1f5ff
    style PS fill:#f3e5f5
    style CS fill:#e8f5e9
    style AS fill:#fff4e1
    style EXT fill:#ffebee
```

## Key Architectural Characteristics

### Communication Pattern
- **API Gateway Pattern**: Simple central entry point routing requests to services
- **Synchronous HTTP/REST**: All inter-service communication uses REST APIs
- **No Message Queues**: No asynchronous messaging implemented
- **Docker DNS**: Services discover each other via container names
- **Simple Proxy**: Gateway calls services directly and returns responses

### Data Storage
- **Account Service**: SQLite database with modularized database layer in `database.py`
  - Separate database module for improved code organization
  - Persistent storage in `users.db` file
  - Schema: `users` table with id, username, password
  - Functions: `init_db()`, `get_db_connection()`, `find_user_by_username()`, `add_user()`, `get_all_users()`
- **Currency Service**: In-memory dictionary with static exchange rates
- **Product Catalog**: External API (dummyjson.com) - no local storage
- **Partial Persistence**: User data persists between restarts, product/currency data is volatile

### Scalability
- **Independent Services**: Each service can be scaled independently
- **Stateless Design**: Services don't maintain session state
- **Docker Orchestration**: Uses Docker Compose for local deployment

### Security Considerations
- **Authentication**: Account service uses Authorization header
- **API Gateway**: Simple central entry point on port 8000, services also exposed on individual ports
- **Minimal Error Handling**: Gateway returns responses as-is from services
- **Plain Text Data**: Credentials stored without encryption
- **No HTTPS**: All communication over HTTP

### External Dependencies
- **dummyjson.com**: Provides product seed data
- **Single Point of Failure**: External API unavailability affects Product Catalog Service

## Deployment Instructions

1. **Prerequisites**: Docker and Docker Compose installed

2. **Start Services**:
   ```bash
   docker-compose up
   ```

3. **Access Points**:
   - API Gateway: http://localhost:8000
   - Web UI: http://localhost:8501
   - Account API: http://localhost:5010 (or via Gateway: http://localhost:8000/api/account/*)
   - Currency API: http://localhost:5020 (or via Gateway: http://localhost:8000/api/currency/*)
   - Product API: http://localhost:5030 (or via Gateway: http://localhost:8000/api/products/*)

4. **Service Startup Order**:
   - Account, Currency Services start first (independent)
   - Product Catalog Service (depends on Currency)
   - API Gateway (depends on Account, Currency, Product Catalog)
   - UI Service (depends on Product Catalog)

## Future Enhancement Opportunities

1. **Enhanced Storage**: Migrate Product/Currency services to persistent storage
2. **Gateway Authentication**: Add JWT/OAuth2 authentication at gateway level
3. **Caching**: Implement Redis for product and currency data
4. **Message Queue**: Add RabbitMQ/Kafka for async operations
5. **Service Discovery**: Implement Consul or Eureka
6. **Load Balancing**: Add nginx or Traefik
7. **Monitoring**: Integrate Prometheus and Grafana
8. **Logging**: Centralized logging with ELK stack
9. **Security**: Add OAuth2, HTTPS, secret management
10. **Resilience**: Implement circuit breakers and retry patterns
