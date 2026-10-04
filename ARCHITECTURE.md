# Web Coach Project Architecture

## Current State

The project works, but the current structure puts too much responsibility into a single file.

Main characteristics today:

- `app.py` contains app setup, routes, match data, parsing helpers, statistics logic, and Match Center view preparation.
- `PARTIDOS_DATA` lives inside `app.py`, so content changes and code changes are mixed together.
- Match Center logic is duplicated in several places.
- Templates are functional, but some presentation concerns are still split between templates and large global CSS.
- There are a few stray files in the project root that do not belong to the deployable app.

## Main Architectural Problems

### 1. `app.py` is doing too much

Right now `app.py` acts as:

- application bootstrap
- route controller
- data store
- domain logic layer
- view-model builder

That makes every change riskier than it needs to be.

### 2. Data and logic are tightly coupled

`PARTIDOS_DATA` is hardcoded in the same file as production logic. This creates a few issues:

- harder to edit content safely
- harder to validate match data
- harder to reuse the same data in future admin tools or APIs

### 3. Statistics logic is repeated

Stats are calculated in more than one place using similar loops and assumptions. That increases the chance of inconsistent numbers between:

- leaderboard
- team table
- goalkeeper table
- match detail summaries

### 4. Routes are building too much UI state

The `/partidos` route currently:

- normalizes matches
- parses dates
- decides upcoming status
- calculates filters
- calculates stats
- calculates tables
- sorts leaderboard
- injects played matches
- prepares template context

That is too much work for a route handler.

### 5. Encoding/content quality issues are mixed into the app

There are mojibake strings like `SÃ¡bado`, `MetodologÃ­a`, `PrÃ³ximo`. These are content/data quality issues, but today they are embedded directly in code and templates.

## Target Architecture

The best next version of this project is still simple. We do not need a heavy enterprise structure. We just need clean separation.

Recommended target:

```text
web_coach_project/
|
├── app/
│   ├── main.py
│   ├── core/
│   │   └── config.py
│   ├── data/
│   │   └── partidos.py
│   ├── domain/
│   │   ├── models.py
│   │   └── normalizers.py
│   ├── services/
│   │   ├── matches.py
│   │   ├── stats.py
│   │   └── filters.py
│   └── routes/
│       ├── pages.py
│       └── match_center.py
|
├── templates/
├── static/
├── tests/
├── requirements.txt
└── start.sh
```

## Responsibility Split

### `app/main.py`

Only bootstraps FastAPI:

- create `app`
- mount static files
- register routers
- configure templates if needed

### `app/data/partidos.py`

Contains only match data loading.

Short-term:

- move `PARTIDOS_DATA` here as Python data

Better medium-term:

- move it to `partidos.json`
- load and validate it in one place

### `app/domain/models.py`

Defines the shapes we care about:

- Match
- MatchEvent
- TeamSummary
- PlayerSummary
- GoalkeeperSummary

This can start with simple `TypedDict` or Pydantic models.

### `app/domain/normalizers.py`

Central place for:

- date parsing
- score parsing
- player name normalization
- result derivation

### `app/services/matches.py`

Handles match preparation:

- enrich matches for UI
- order past/upcoming matches
- derive filter lists

### `app/services/stats.py`

Single source of truth for:

- leaderboard
- player totals
- goalkeeper table
- team summary table
- per-match goal and assist summaries

### `app/routes/pages.py`

Static/simple pages only:

- `/`
- `/sobre-mi`
- `/metodologia`
- `/contacto`

### `app/routes/match_center.py`

Only Match Center pages:

- `/partidos`
- `/partidos/{id}`

Routes should mostly call services and pass a clean template context.

## Suggested Refactor Order

### Phase 1. Safe cleanup

- keep current behavior
- move `PARTIDOS_DATA` out of `app.py`
- move helpers out of `app.py`
- split page routes and Match Center routes

This gives the biggest maintainability win with low design risk.

### Phase 2. Statistics consolidation

- create one stats service
- remove duplicated goal/assist/MVP loops
- make team, player, and goalkeeper tables depend on shared normalized data

This is where correctness becomes much easier.

### Phase 3. Content cleanup

- fix text encoding issues
- normalize player names consistently
- clean root-level stray files
- move non-template assets out of `templates/`

### Phase 4. UI system cleanup

- organize CSS by sections
- define reusable layout blocks for cards, tables, filters, hero sections
- reduce one-off inline styling in templates

### Phase 5. Testing

Minimum useful tests:

- score parsing
- result derivation
- team summary table
- player totals
- `/`, `/partidos`, and `/partidos/{id}` return `200`

## First Refactor I Recommend

If we start implementation next, the best first move is:

1. Create `app/data/partidos.py`
2. Create `app/services/stats.py`
3. Move helper functions out of `app.py`
4. Reduce `app.py` to app setup plus router registration

That will make the codebase easier to evolve before we redesign the visual side.

## Notes About Design Direction

Your site should eventually behave like a hybrid of:

- professional portfolio
- coaching methodology site
- live match archive
- lightweight scouting/performance dashboard

That means the architecture should support both:

- editorial pages with strong storytelling
- structured football data with repeatable stats logic

The current code already proves the concept. The next step is to turn it into a cleaner system so future redesigns are much easier.
