# Shopping Site Microservices Architecture

This document provides a comprehensive architectural overview of the Shopping Site Microservices application.

## System Overview

The application consists of 4 microservices deployed using Docker:
- **Account Service**: User registration and authentication
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

## Service Communication Flow

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

## Container Architecture

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

## Key Architectural Characteristics

### Communication Pattern
- **Synchronous HTTP/REST**: All inter-service communication uses REST APIs
- **No Message Queues**: No asynchronous messaging implemented
- **Docker DNS**: Services discover each other via container names

### Data Storage
- **Account Service**: In-memory list (planned migration to SQLite)
- **Currency Service**: In-memory dictionary with static exchange rates
- **Product Catalog**: External API (dummyjson.com) - no local storage
- **No Persistent Database**: All data is volatile and lost on restart

### Scalability
- **Independent Services**: Each service can be scaled independently
- **Stateless Design**: Services don't maintain session state
- **Docker Orchestration**: Uses Docker Compose for local deployment

### Security Considerations
- **Authentication**: Account service uses Authorization header
- **No API Gateway**: Services exposed directly on different ports
- **Plain Text Data**: Credentials stored in-memory without encryption
- **No HTTPS**: All communication over HTTP

### External Dependencies
- **dummyjson.com**: Provides product and user seed data
- **Single Point of Failure**: External API unavailability affects service

## Deployment Instructions

1. **Prerequisites**: Docker and Docker Compose installed

2. **Start Services**:
   ```bash
   docker-compose up
   ```

3. **Access Points**:
   - Web UI: http://localhost:8501
   - Account API: http://localhost:5010
   - Currency API: http://localhost:5020
   - Product API: http://localhost:5030

4. **Service Startup Order**:
   - Currency Service starts first
   - Product Catalog Service (depends on Currency)
   - UI Service (depends on Product Catalog)
   - Account Service (independent)

## Future Enhancement Opportunities

1. **Persistent Storage**: Migrate to SQLite or PostgreSQL
2. **API Gateway**: Add central routing and authentication layer
3. **Caching**: Implement Redis for product and currency data
4. **Message Queue**: Add RabbitMQ/Kafka for async operations
5. **Service Discovery**: Implement Consul or Eureka
6. **Load Balancing**: Add nginx or Traefik
7. **Monitoring**: Integrate Prometheus and Grafana
8. **Logging**: Centralized logging with ELK stack
9. **Security**: Add OAuth2, HTTPS, secret management
10. **Resilience**: Implement circuit breakers and retry patterns
