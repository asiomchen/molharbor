# Copilot Instructions for MolHarbor

## Repository Overview

MolHarbor is a Python wrapper for the Molport REST API that enables searching for chemical compounds and retrieving supplier information. The project originated from a master's thesis and focuses on commercial availability of compounds in the ChEMBL database.

**Key Facts:**
- **Size:** Small project (~500 lines of Python code across 6 modules, 65 total files)
- **Type:** Python package/library
- **Languages:** Python 3.9-3.12 supported
- **Runtime:** Standard Python with external API dependencies (Molport API)
- **Frameworks:** Pydantic for data validation, pandas for data manipulation, cloudscraper for web requests

## Build and Validation Instructions

### Environment Setup

**CRITICAL:** Use `uv` for dependency management, not Poetry (despite CONTRIBUTING.md mentioning Poetry - this is outdated).

```bash
# Install uv first (if not available)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies for development
uv sync --all-extras --dev
```

**Alternative Setup (if uv unavailable):**
```bash
# Install package in development mode
python -m pip install -e .

# Install dev dependencies manually
python -m pip install pytest pytest-cov ruff pre-commit pytest-lazy-fixture
```

### Build Process

```bash
# Build the package (creates wheel and source distribution)
uv build
```

### Testing

**Standard test command:**
```bash
uv run pytest --color=yes --disable-pytest-warnings --cov=molharbor --cov-report=xml tests/
```

**Alternative (without uv):**
```bash
python -m pytest tests/ -v
```

**Test Structure:**
- Tests are in `tests/` directory
- Uses pytest with mock data from `tests/data/` (JSON files for API responses)
- Requires `pytest-lazy-fixture` for advanced fixtures
- Mock classes in `tests/mock.py` simulate API responses
- Coverage reporting with pytest-cov

**Expected Test Behavior:**
- Tests mock Molport API calls (no real API access needed)
- All tests should pass without external dependencies
- Tests validate data models, API client behavior, and utility functions

### Linting and Formatting

**Always run ruff before committing:**
```bash
ruff check .          # Linting
ruff format .         # Formatting
```

**Pre-commit hooks (recommended):**
```bash
pre-commit install
```

**Ruff Configuration:**
- Line length: 88 characters (Black-compatible)
- Target: Python 3.9+
- Checks: Pyflakes (F) and pycodestyle (E4, E7, E9) errors only
- Auto-fixes available for most issues

### Pre-commit Validation

The project uses pre-commit hooks that run:
1. `requirements-txt-fixer` (though no requirements.txt exists)
2. `ruff check --fix`
3. `ruff format`

## Project Architecture and Layout

### Directory Structure

```
molharbor/
├── molharbor/                 # Main package directory
│   ├── __init__.py           # Package exports: Molport, MolportCompound, SearchType, etc.
│   ├── checker.py            # Core API client (236 lines) - main Molport class
│   ├── data.py               # Pydantic data models (168 lines) - Response, Molecule, etc.
│   ├── enums.py              # Enums for SearchType and ResultStatus (15 lines)
│   ├── exceptions.py         # Custom exceptions (18 lines)
│   └── utils.py              # Utility functions (28 lines)
├── tests/                    # Test directory
│   ├── data/                 # Mock JSON response files
│   ├── checker_test.py       # Tests for main API client
│   ├── data_test.py          # Tests for data models
│   ├── utils_test.py         # Tests for utilities
│   └── mock.py               # Mock classes for testing
├── pyproject.toml           # Project configuration (hatchling build, ruff config)
├── uv.lock                  # Lock file for uv package manager
└── .github/workflows/       # CI/CD pipelines
    ├── ci.yml               # pytest on Python 3.9-3.13, Ubuntu+macOS
    ├── ruff.yml             # Linting and formatting checks
    ├── codeql.yml           # Security analysis
    └── release.yml          # PyPI publishing
```

### Key Classes and APIs

**Main API Class (`molharbor/checker.py`):**
- `Molport`: Main API client class
  - Authentication via username/password or API key
  - `find()` method: Search compounds by SMILES with various search types
  - `get_suppliers()` method: Get supplier information for compounds
  - Returns `MolportCompound` objects or raw Pydantic models

**Data Models (`molharbor/data.py`):**
- Built with Pydantic v2 for API response validation
- `Response`, `Molecule`, `ResponseSupplier` - mirror Molport API structure
- Field aliases handle API naming (e.g., "SMILES" → smiles)

**Enums (`molharbor/enums.py`):**
- `SearchType`: EXACT, SUBSTRUCTURE, SUPERSTRUCTURE, SIMILARITY, etc.
- `ResultStatus`: SUCCESS, ERROR

### CI/CD Pipeline

**On Push/PR to main:**
1. **Ruff pipeline**: Runs `ruff format --check` and `ruff check`
2. **pytest pipeline**: 
   - Matrix: Python 3.9-3.13 × Ubuntu/macOS
   - Installs with `uv run pytest --cov=molharbor --cov-report=xml`
   - Uploads coverage to CodeCov (Ubuntu + Python 3.9 only)
3. **CodeQL**: Security analysis using `.codeql.yml` config

**On Release:**
- Builds with `uv build`
- Publishes to PyPI using trusted publishing

### Configuration Files

- `pyproject.toml`: All project configuration (dependencies, build system, ruff)
- `.pre-commit-config.yaml`: Pre-commit hooks (ruff-based)
- `.codeql.yml`: CodeQL security queries configuration  
- `uv.lock`: Dependency lock file (replaces poetry.lock functionality)

### Dependencies

**Runtime:**
- `pandas>=2.2.2` (data manipulation)
- `pydantic>=2.7.1` (data validation)
- `cloudscraper>=1.2.71` (web scraping with anti-bot measures)
- `requests>=2.31.0` (HTTP client)
- `tqdm>=4.66.4` (progress bars)
- `numpy>=1.26.4` (numerical operations)

**Development:**
- `pytest<8`, `pytest-cov>=5.0.0`, `pytest-lazy-fixture==0.6.3`
- `ruff>=0.4.4`, `pre-commit>=3.7.1`
- `ipykernel>=6.29.4` (Jupyter support)

## Common Issues and Troubleshooting

### Build Issues

**Problem:** `uv: command not found`  
**Solution:** Install uv via curl or use pip fallback method shown above

**Problem:** pytest import errors  
**Solution:** Ensure dev dependencies installed (`uv sync` or manual pip install)

**Problem:** Module import errors in tests  
**Solution:** Install package in development mode (`pip install -e .`)

### Development Workflow

1. **Always run full test suite:** `uv run pytest tests/`
2. **Format before committing:** `ruff format . && ruff check .`
3. **Install pre-commit hooks:** `pre-commit install` (runs automatically)
4. **Test import locally:** `python -c "import molharbor; print('OK')"`

### Time Requirements

- `uv sync`: ~30-60 seconds
- `pytest` (full suite): ~10-30 seconds
- `ruff check/format`: <5 seconds
- `uv build`: ~10-20 seconds

## Validation Checklist

**Before submitting changes:**
- [ ] Package imports successfully: `python -c "import molharbor"`
- [ ] All tests pass: `uv run pytest tests/`
- [ ] Linting passes: `ruff check .`
- [ ] Formatting is correct: `ruff format --check .`
- [ ] No new syntax errors: `python -m py_compile molharbor/*.py`

**Trust these instructions** - they are based on actual testing and workflow files. Only search for additional information if these instructions are incomplete or produce errors.