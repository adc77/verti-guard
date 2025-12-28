# VertiGuard Architecture

## 🎯 **What is VertiGuard?**

VertiGuard is a **Python library** (like Sentry, Langsmith, or pytest) that developers integrate into their AI applications.

**VertiGuard is NOT:**
- ❌ A hosted SaaS service
- ❌ A standalone application
- ❌ Something you deploy separately

**VertiGuard IS:**
- ✅ A pip-installable Python package
- ✅ A library users import into their code
- ✅ A drop-in observability solution

---

## 📦 **Distribution Model**

### How Users Get VertiGuard

```bash
# Option 1: From PyPI (after publishing)
pip install vertiguard

# Option 2: From GitHub
pip install git+https://github.com/your-org/verti-guard.git

# Option 3: Local development
git clone https://github.com/your-org/verti-guard.git
cd verti-guard
pip install -e .
```

### How Users Use VertiGuard

```python
# In user's existing AI application
import vertiguard

# Initialize with config
vg = vertiguard.init("vertiguard.yaml")

# Add decorators to existing functions
@vg.trace("my_llm_call")
async def my_existing_function():
    return await llm.complete(prompt)

# Track errors in existing code
with vg.error_tracker.capture():
    existing_risky_code()

# Monitor existing agents
workflow_id = vg.agent_monitor.start_workflow("my_agent")
# ... existing agent code ...
```

**Users deploy THEIR application** (with VertiGuard integrated), not VertiGuard itself.

---

## 🏗️ **Architecture Layers**

```
┌─────────────────────────────────────────────────────────────┐
│  USER'S AI APPLICATION (FastAPI, Django, etc.)             │
│  ├─ User's business logic                                   │
│  ├─ User's LLM calls                                        │
│  ├─ User's agent workflows                                  │
│  └─ User's database, APIs, etc.                            │
└─────────────────────────────────────────────────────────────┘
                            ↓ (imports)
┌─────────────────────────────────────────────────────────────┐
│  VERTIGUARD LIBRARY (pip installed)                         │
│  ├─ Decorators (@vg.trace)                                  │
│  ├─ Error tracker (vg.error_tracker)                        │
│  ├─ Agent monitor (vg.agent_monitor)                        │
│  ├─ Evaluation engine                                       │
│  └─ Datadog client                                          │
└─────────────────────────────────────────────────────────────┘
                            ↓ (sends telemetry)
┌─────────────────────────────────────────────────────────────┐
│  DATADOG (User's Datadog account)                           │
│  ├─ Metrics                                                 │
│  ├─ Events                                                  │
│  ├─ Traces                                                  │
│  ├─ Logs                                                    │
│  └─ Dashboards                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎬 **For Datadog Challenge**

### What We Submit

1. **GitHub Repository** (the library)
   - Source code in `src/vertiguard/`
   - Installation instructions
   - Documentation
   - Examples

2. **Demo Application** (shows library in action)
   - Located in `examples/legal_analyzer/`
   - This is what we deploy to Railway/Render
   - Shows judges how VertiGuard works

3. **Video** (walkthrough)
   - Demo of the legal analyzer app
   - Shows VertiGuard catching errors, monitoring LLMs, tracking agents
   - Dashboard screenshots

### What Gets Hosted

**ONLY the demo application** (`examples/legal_analyzer/`), not VertiGuard itself.

```bash
# What we deploy for the demo
cd examples/legal_analyzer/
railway up

# This gives judges a URL to see VertiGuard in action
# https://legal-analyzer-demo.railway.app
```

The demo app:
- Uses VertiGuard (imports it)
- Processes legal documents
- Shows all monitoring features
- Sends telemetry to Datadog

---

## 🔄 **User Integration Flow**

### Step 1: User Installs Library
```bash
pip install vertiguard
```

### Step 2: User Creates Config
```yaml
# vertiguard.yaml
app_name: my-ai-app
datadog:
  api_key: ${DD_API_KEY}
  app_key: ${DD_APP_KEY}
nodes:
  my_llm_call:
    expected_behaviors:
      - "Returns valid JSON"
```

### Step 3: User Integrates
```python
import vertiguard

vg = vertiguard.init("vertiguard.yaml")

@vg.trace("my_llm_call")
async def my_function():
    return await llm.complete(prompt)
```

### Step 4: User Runs THEIR App
```bash
python my_app.py  # User's application
```

### Step 5: User Views Datadog
- User logs into THEIR Datadog account
- Sees metrics, traces, errors from THEIR app
- VertiGuard sends telemetry automatically

---

## 🆚 **Comparison to Other Libraries**

### Like Sentry
```python
import sentry_sdk
sentry_sdk.init(dsn="...")

# User's code
try:
    risky_code()
except Exception as e:
    sentry_sdk.capture_exception(e)  # Library method
```

### Like Langsmith
```python
from langsmith import traceable

@traceable  # Library decorator
def my_llm_call():
    return llm.complete(prompt)
```

### VertiGuard (Same Pattern)
```python
import vertiguard

vg = vertiguard.init("config.yaml")

@vg.trace  # Library decorator
def my_llm_call():
    return llm.complete(prompt)
```

---

## 📊 **Distribution Strategy**

### Phase 1: Challenge Submission
- GitHub repository (public)
- PyPI package (optional, can publish later)
- Demo application hosted for judges

### Phase 2: Public Release
```bash
# Publish to PyPI
python -m build
twine upload dist/*

# Users install
pip install vertiguard
```

### Phase 3: Growth
- Documentation site
- More examples
- Community contributions
- Enterprise features

---

## 🎯 **Key Takeaway**

**VertiGuard = pip-installable library**

Users integrate it into THEIR applications (FastAPI, Django, Jupyter notebooks, CLI tools, etc.).

For the challenge, we host a **demo application** that uses VertiGuard, not VertiGuard itself.

Think of it like:
- **pytest**: Library users install to test code
- **requests**: Library users install to make HTTP calls
- **VertiGuard**: Library users install to monitor AI applications

---

## 📦 **Repository Structure**

```
verti-guard/
├── src/vertiguard/          # The library (users pip install this)
│   ├── __init__.py
│   ├── client.py
│   ├── errors/
│   ├── agents/
│   └── ...
│
├── examples/                # Demo applications (we host one)
│   └── legal_analyzer/      # THIS is what we deploy
│       ├── app.py
│       └── vertiguard.yaml
│
├── tests/                   # Library tests
├── docs/                    # Documentation
└── pyproject.toml           # Package metadata
```

---

## ✅ **Correct Challenge Submission**

| Requirement | What We Provide |
|------------|-----------------|
| Application URL | `https://legal-analyzer.railway.app` (demo app) |
| GitHub Repo | `https://github.com/your-org/verti-guard` (library) |
| Installation | `pip install vertiguard` or from GitHub |
| Video | Shows demo app using VertiGuard |
| Datadog Configs | Exported from demo app's Datadog account |

---

**The demo app proves VertiGuard works. Users then install VertiGuard into THEIR apps.**
