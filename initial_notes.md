
# Protein Visualization Platform — Design Summary

**Project Goals:** Build a full-stack protein data explorer in 1 week using Vue.js (frontend), FastAPI (backend), and SQLite (database).


## Architecture Overview

### Backend Layers (Top to Bottom)

```
FastAPI Routes (HTTP endpoints)
    ↓
Services (business logic)
    ↓
Repository Pattern (data access abstraction)
    ↓
SQLAlchemy ORM (database interaction)
    ↓
SQLite Database
```

**Key principle:** Each layer depends on the one below it, but not vice versa. This makes testing and refactoring easy.

---

## Database Design

### Schema Structure
- **proteins** — protein metadata (id, name, gene_symbol)
- **isoforms** — variants of proteins (protein_id FK, length_aa)
- **domains** — functional regions (isoform_id FK, start_aa, end_aa, domain_type)
- **peptides** — observed peptide sequences (isoform_id FK, start_aa, end_aa)
- **variants** — genetic variations (isoform_id FK, position_aa)
- **samples** — experimental samples (id, sample_name, sample_class: Cancer/Normal/Cell line)
- **protein_expression** — abundance measurements (protein_id FK, sample_id FK, abundance)
- **interactions** — protein-protein relationships (protein_id_a FK, protein_id_b FK, interaction_type)

**Your task:** Write the SQL schema with primary keys, foreign keys, and indexes.

---

## Backend Architecture

### Repository Pattern (Testability)

**Concept:** Create an abstract `Repository` class that both real and mock implementations inherit from.

**Why:** Swap out real DB for mock data in tests without changing service code.

```python
# Your task: create these files

data/repository.py
├── Repository (abstract base class)
│   ├── abstract methods: get_protein(), get_isoforms(), get_domains(), etc.
│   └── Both real and mock repos implement this
├── ProteinRepository (real, talks to DB)
└── MockRepository (test, returns hardcoded data)

services/protein_service.py
├── ProteinService
│   ├── __init__(self, repo: Repository)  # Receives repository via dependency injection
│   ├── get_protein_detail(protein_id)  # Returns dict (not ORM object)
│   ├── get_feature_map(protein_id)     # Aggregates domains + peptides + variants
│   ├── get_expression(protein_id)      # Groups by sample_class
│   └── get_interactions(protein_id)    # Returns protein-protein relationships
```

### Pydantic Schemas

**Concept:** Define response shapes for each endpoint. Pydantic validates and auto-converts to JSON.

**Your task:** Create Pydantic models matching what the frontend needs:

```python
schemas/protein_schemas.py
├── ProteinDetailResponse
├── FeatureMapResponse (with nested IsoformFeatureMap, DomainFeature, PeptideMarker, VariantMarker)
├── ExpressionResponse (with SampleExpression)
└── InteractionResponse
```

### API Endpoints (UI-Driven Design)

**Key decision:** Build endpoints that return exactly what the frontend needs to render. Avoid generic CRUD endpoints.

**Your task:** Implement these 5 endpoints:

```
1. GET /api/proteins?search=<query>
   └─ Returns: List of matching proteins (id, name, gene_symbol)

2. GET /api/proteins/{protein_id}
   └─ Returns: Protein detail + basic isoform list

3. GET /api/proteins/{protein_id}/feature-map
   └─ Returns: All isoforms WITH domains, peptides, variants pre-joined
   └─ Frontend doesn't have to reshape this

4. GET /api/proteins/{protein_id}/expression
   └─ Returns: Samples with abundance, grouped with sample metadata

5. GET /api/proteins/{protein_id}/interactions
   └─ Returns: Protein-protein relationships for this protein
```

### Error Handling (Problem Details RFC 7807)

**Concept:** Return structured error responses so frontend knows what went wrong.

**Your task:** Create exception classes:

```python
core/exceptions.py
├── ProteinNotFoundError → 404
├── InvalidSearchQueryError → 400
└── DatabaseError → 500
```

Each exception contains: `type` (error category URL), `title`, `status`, `detail`, `instance`.

### Async DB Calls

**Key decision:** Use async/await for database operations. Enables FastAPI to handle concurrent requests efficiently.

**Your task:** When you query the DB, use `async def` and `await` syntax. If you call `await`, your function must be `async`.

---

## Frontend Architecture

### Component-Based (No MVC)

**Concept:** Vue.js already handles view rendering + reactivity. You just need:
1. Shared state (in App.vue)
2. Components (handle their own rendering)
3. API service (centralized axios calls)

**Your task:** Create these components:

```
src/App.vue (ROOT)
├── State: selectedProteinId, proteinDetail, featureMap, expressionData, interactions, isLoading
├── Event handlers: onProteinSelected() — fetches all 4 endpoints in parallel
│
├── ProteinSearch.vue
│   ├── Search input + debounce (300ms)
│   ├── Emits: protein-selected event to parent
│   └── Calls: api.searchProteins(query)
│
└── ProteinPanel.vue (when protein selected)
    ├── ProteinDetail.vue — protein metadata
    ├── FeatureMap.vue — SVG with domains/peptides/variants
    ├── ExpressionChart.vue — Plotly bar chart (grouped by sample_class)
    └── InteractionPanel.vue — interactions table
```

### Data Flow (User Selects a Protein)

```
1. User types in ProteinSearch.vue
2. Debounce waits 300ms, then calls api.searchProteins(query)
3. Results displayed in dropdown
4. User clicks a result → ProteinSearch emits 'protein-selected' event
5. App.vue receives event, sets selectedProteinId = protein.id
6. App.vue fetches 4 endpoints in PARALLEL using Promise.all():
   - api.getProteinDetail(id)
   - api.getFeatureMap(id)
   - api.getExpression(id)
   - api.getInteractions(id)
7. All results arrive ~simultaneously (1 request roundtrip, not 4)
8. App.vue updates state: proteinDetail, featureMap, expressionData, interactions
9. Child components automatically re-render (Vue reactivity)
10. User sees visualizations without page refresh
```

### Props & Events Pattern

**Props:** Data flows DOWN from parent to child.
```
App.vue passes: :proteinDetail="proteinDetail" to ProteinDetail.vue
```

**Events:** Interactions flow UP from child to parent.
```
ProteinSearch.vue emits: @protein-selected="onProteinSelected"
```

### API Service

**Your task:** Create a single file with all API calls:

```javascript
services/api.js
├── searchProteins(query)
├── getProteinDetail(proteinId)
├── getFeatureMap(proteinId)
├── getExpression(proteinId)
└── getInteractions(proteinId)
```

All functions use axios and return Promises. Call them with `await` in components.

---

## Testing Strategy

### Backend Testing (pytest)

**Your task:** Write tests for the Service layer (not the database directly):

```
tests/
├── conftest.py — Define pytest fixtures
│   └── @pytest.fixture: MockRepository (with hardcoded test data)
│   └── @pytest.fixture: ProteinService (receives mock repo)
│
├── test_services.py
│   └── Test business logic: joins, aggregations, error cases
│   └─ Example: test_get_feature_map() checks domains are included
│   └─ Use the mock repository, not a real database
│
└── test_integration.py (optional)
    └─ Spin up test SQLite DB
    └─ Test full flow: API endpoint → service → repository → database
```

**Why mock vs. real DB?** Mocking is fast and isolated. Integration tests with real DB catch join bugs.

### Frontend Testing (Vitest + Vue Test Utils)

**Your task:** Test that components render correctly with mock API data:

```
frontend/tests/
├── FeatureMap.test.js
│   └─ Mock the featureMapData prop with test data
│   └─ Verify SVG renders domains, peptides, variants
│
├── ExpressionChart.test.js
│   └─ Mock expressionData
│   └─ Verify bars are grouped by sample_class
│
├── ProteinSearch.test.js
│   └─ Mock api.searchProteins()
│   └─ Verify debounce works, emit event fires
│
└── App.integration.test.js (optional)
    └─ Mock all 4 API endpoints
    └─ Verify selecting protein loads all data
```

---

## Key Design Decisions

| Decision | Why |
|----------|-----|
| **SQLite (not PostgreSQL)** | Single file, no server overhead, fast 1-week setup. Can migrate to Postgres later. |
| **Vue.js (not React)** | Gentler learning curve, simpler syntax, faster to productive. |
| **Async DB calls** | FastAPI handles concurrent requests efficiently. Standard pattern. |
| **UI-driven endpoints** | Single frontend → simpler to build. Avoid generic CRUD endpoints that require client-side joins. |
| **Multiple small API calls** | Same latency as one big call (use Promise.all for parallelism), smaller payloads, easier to cache/test. |
| **Repository pattern** | Familiar from EF Core. Makes mocking tests trivial. Clean separation of concerns. |
| **Pydantic for responses** | Type-safe, auto-serializes to JSON, validates shape. FastAPI does the heavy lifting. |
| **SVG for feature map** | Simple, easy to overlay domains/peptides/variants. No canvas complexity. |
| **Plotly.js for charts** | Interactive, standard in science, works well with Vue. Handles color-coding by sample_class. |

---

## Implementation Roadmap

### Phase 1: Database & Backend Scaffold (Days 1–2)
- [ ] Write SQL schema (`sql/schema.sql`)
- [ ] Implement Repository abstract class + ProteinRepository
- [ ] Implement ProteinService with business logic
- [ ] Create Pydantic response schemas
- [ ] Write CSV loader script (`scripts/init_db.py`) with pandas → SQLite
- [ ] Test: `python scripts/init_db.py` creates DB with data

### Phase 2: API Endpoints (Days 2–3)
- [ ] Implement 5 endpoints (search, detail, feature-map, expression, interactions)
- [ ] Wire up FastAPI dependency injection (Depends)
- [ ] Test with curl: `curl http://localhost:8000/api/proteins?search=kinase`

### Phase 3: Testing (Days 3–4)
- [ ] Write 10–15 pytest tests for ProteinService (mocked repo)
- [ ] Write frontend component tests (mocked API)
- [ ] Create UML diagrams (Mermaid ERD + class diagram)

### Phase 4: Frontend (Days 4–5)
- [ ] Set up Vue.js with Vite
- [ ] Build 5 components (Search, Panel, Detail, FeatureMap, Chart, Interactions)
- [ ] Implement API service + Promise.all parallelism
- [ ] Wire up search → select protein → visualizations

### Phase 5: Polish (Day 5–6)
- [ ] Error handling + toast notifications
- [ ] README with setup & run instructions
- [ ] Fresh checkout → full system working in <10 minutes

---

## Concepts You Need to Know

### Promises & Async/Await (JavaScript)
- **Promise:** Represents a value that will be available in the future
- **Async/await:** Modern syntax for waiting on promises
- **Promise.all([...]):** Run multiple promises in parallel, wait for all to finish

### Props & Events (Vue)
- **Props:** Data flows down (parent → child)
- **Events:** Child notifies parent via emit; parent listens with @event-name

### Repository Pattern
- **Interface:** Abstract methods that both real & mock implement
- **Real repo:** Queries database
- **Mock repo:** Returns hardcoded test data
- **Service:** Doesn't know which repo it's using

### Pydantic (FastAPI)
- Defines response schema (structure + types)
- Validates response matches schema
- Auto-serializes to JSON
- Provides error messages if schema mismatch

### Async vs. Synchronous (Python)
- **Sync:** Blocks thread while waiting for I/O (database, network)
- **Async:** Yields control while waiting, allows other requests to execute
- **Rule:** If your function uses `await`, make it `async`

---

## What You'll Implement (Roughly)

**Backend:** ~15 files (models, repository, services, schemas, routes, tests, init script)
**Frontend:** ~6 components + 1 API service file + tests
**Database:** 1 schema file + 1 loader script

Total: ~25 files, most of which are modular and testable.

---

## Next Steps

1. **Start with the database:** Write `sql/schema.sql` (8 normalized tables)
2. **Then the loader:** `scripts/init_db.py` (pandas → SQLite)
3. **Then backend:** Models, Repository, Service, Schemas
4. **Then API endpoints:** Wire up Depends() and test with curl
5. **Then frontend:** Components that call your API

Each step is independently verifiable. You'll know when it works.

**Note:** You have the detailed architecture guide in session memory for deep-dives into specific areas. This summary is the high-level roadmap.
```

---

Done! This is a **condensed reference** that:
- Covers concepts without drowning you in code
- Tells you what files to create + what goes in them
- Gives you enough guidance to implement independently
- Points to session memory for detailed examples when you need them

Copy the markdown above and save it as `DESIGN_NOTES.md` in your workspace. Now you can implement while referring back to this guide.

Ready to start coding, or do you want clarification on any concept?---

Done! This is a **condensed reference** that:
- Covers concepts without drowning you in code
- Tells you what files to create + what goes in them
- Gives you enough guidance to implement independently
- Points to session memory for detailed examples when you need them

Copy the markdown above and save it as `DESIGN_NOTES.md` in your workspace. Now you can implement while referring back to this guide.

Ready to start coding, or do you want clarification on any concept?