# 🎓 Dolg API — Final Defense Presentation Guide

---

## 1. Project Overview & Aim

- **Topic**: Dolg API & Web Platform — RESTful Service for Group Expense Tracking & Debt Minimization.
- **Aim**: Create a high-performance, developer-friendly REST API and interactive web interface to track shared group expenses, split bills equally or exactly, and optimize debt settlements using a **Greedy Minimization Algorithm**.
- **Key Objectives**:
  1. Build a robust backend using **FastAPI** and **SQLAlchemy**.
  2. Implement secure authentication using **JWT** and **bcrypt**.
  3. Implement **Greedy Debt Minimization Algorithm** to simplify inter-member transactions from $O(N^2)$ potential transfers down to a minimal $O(N)$ path.
  4. Perform data science category analytics using **Pandas**.
  5. Provide a responsive, bilingual (Russian / English) Single Page Web Dashboard.

---

## 2. Market Analysis & Technology Comparison

| Feature | Splitwise | Tricount | **Dolg API (Our Solution)** |
| :--- | :--- | :--- | :--- |
| **API Accessibility** | Restricted / Paid API | Closed | **Open RESTful API (FastAPI)** |
| **Splitting Modes** | Equal / Exact / % | Equal / Share | **Equal & Exact Splits** |
| **Debt Minimization** | Premium feature (Splitwise Pro) | Basic | **Greedy Algorithm Included (Free)** |
| **Analytics & Data Science**| Basic summary | None | **Pandas Category & Trend Analytics** |
| **Language Support** | Fixed per region | English default | **Instant RU / EN Toggle** |
| **Open Source & Self-Host**| No | No | **Yes (Docker & Compose Ready)** |

---

## 3. Project Architecture & MVC Pattern

```
                       ┌─────────────────────────┐
                       │   Client / Web SPA      │
                       │ (HTML5 / CSS3 / JS ES6) │
                       └────────────┬────────────┘
                                    │ HTTP / JSON
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           FastAPI Controller                            │
│  (/auth, /groups, /groups/{id}/expenses, /groups/{id}/settle-up, ...)  │
└────────────┬──────────────────────┬──────────────────────┬──────────────┘
             │                      │                      │
             ▼                      ▼                      ▼
┌────────────────────────┐┌───────────────────┐┌────────────────────────┐
│  Debt Solver Service   ││ Security Engine   ││ Analytics Service      │
│  (Greedy Algorithm)    ││ (JWT / bcrypt)    ││ (Pandas DataFrames)    │
└────────────┬───────────┘└─────────┬─────────┘└───────────┬────────────┘
             │                      │                      │
             └──────────────────────┼──────────────────────┘
                                    │ ORM Sessions
                                    ▼
                       ┌─────────────────────────┐
                       │ SQLAlchemy / SQLite DB  │
                       └─────────────────────────┘
```

---

## 4. Relevance & Practical Significance

- **Real-World Problem**: In group trips, shared apartment living, or student events, calculating who owes whom after dozens of transactions creates confusion and unnecessary money transfers.
- **Our Solution**:
  - Automatically calculates net balance for each person.
  - Matches the largest debtor with the largest creditor to resolve all group debts in the fewest possible transfers.
  - Generates clear financial analytics by category.

---

## 5. Live Defense Demo Walkthrough

### Step 1: Open Interactive Swagger Documentation
1. Launch app: `uvicorn app.main:app --reload`
2. Open `http://127.0.0.1:8000/docs`
3. Show clean OpenAPI tags: `Authentication`, `Groups`, `Expenses`, `Balance & Settlements`, `Analytics (Data Science)`.

### Step 2: Live Flow Execution
1. Register 3 users: `Alice`, `Bob`, `Charlie`.
2. Login as `Alice` and copy access token into `Authorize` button.
3. Create Group: `"Almaty Trip"`.
4. Add `Bob` and `Charlie` as members.
5. Create Expense: `Alice pays 300₸` (Equal split -> 100₸ each).
6. Call `GET /groups/{id}/balance`:
   - Alice: `+200₸` (Creditor)
   - Bob: `-100₸` (Debtor)
   - Charlie: `-100₸` (Debtor)
7. Call `GET /groups/{id}/settle-up`:
   - Returns 2 minimal payments: `Bob -> Alice (100₸)` and `Charlie -> Alice (100₸)`.
8. Call `GET /groups/{id}/analytics`:
   - Displays category breakdown and top spender metrics using `pandas`.
9. Open Web SPA at `http://127.0.0.1:8000/` and toggle language (RU <-> EN) to show bilingual frontend.
