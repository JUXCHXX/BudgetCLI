# BudgetCLI Roadmap

This document outlines the planned features and improvements for BudgetCLI.

## Current Version: 1.0.0

### ✅ Released Features

- Transaction management (income/expense tracking)
- Budget management with monthly limits
- Monthly reports and summaries
- ASCII chart visualization
- CSV and JSON export
- PNG chart generation
- SQLite persistence
- Comprehensive validation
- Full test coverage (>80%)

---

## Planned Releases

### 🎯 v1.1.0 (Q2 2026)

**Theme:** Enhanced Tracking & Notifications

#### Features

- **Recurring Transactions**
  - Set up automatic monthly transactions
  - Edit/skip recurring items
  - Auto-tracking of utilities, subscriptions

- **Budget Alerts**
  - Threshold-based alerts (80%, 100%)
  - Email notifications
  - Configurable alert frequency

- **Multi-Currency Support**
  - Track expenses in different currencies
  - Automatic conversion with exchange rates
  - Currency-specific reports

- **Advanced Filtering**
  - Filter by date range
  - Filter by amount range
  - Complex queries with AND/OR logic
  - Save filters as templates

#### Implementation Details

```
New Database Tables:
- recurring_transactions
- alerts_config
- currency_conversion_rates

New CLI Commands:
- budget recurring --help
- budget alert --help
- budget settings --help
```

---

### 🎯 v1.2.0 (Q3 2026)

**Theme:** Advanced Analytics & Insights

#### Features

- **Investment Tracking**
  - Track stock, crypto, bonds
  - Portfolio overview
  - Investment returns calculation

- **Tax Report Generation**
  - Categorized expense summary
  - Tax deduction calculations
  - Export for tax filing

- **Financial Goals**
  - Set savings goals
  - Track progress
  - Goal-based budgeting

- **Spending Predictions**
  - ML-based predictions
  - Trend analysis
  - Seasonal adjustment

- **Budget Analytics**
  - Spending trends over time
  - Category analysis
  - Comparison to previous periods

#### Implementation Details

```
New Database Tables:
- goals
- investments
- analytics_cache

New Services:
- InvestmentService
- GoalService
- TrendAnalysisService
- PredictionService

New CLI Commands:
- budget goal --help
- budget investment --help
- budget analytics --help
- budget predict --help
```

---

### 🎯 v2.0.0 (Q4 2026+)

**Theme:** Web & Mobile Experience

#### Major Features

- **Web Dashboard**
  - Real-time financial overview
  - Interactive charts
  - Mobile-responsive design

- **REST API**
  - FastAPI backend
  - Full CRUD operations
  - Authentication/authorization
  - Rate limiting

- **Mobile App**
  - iOS app (Swift)
  - Android app (Kotlin)
  - Offline support
  - Cloud sync

- **Cloud Synchronization**
  - Optional cloud backup
  - Multi-device sync
  - Conflict resolution

- **Advanced Features**
  - Bank account integration
  - Credit card feeds
  - Receipt scanning
  - Expense categorization (AI)

#### Architecture Changes

```
budgetcli-v2/
├── core/              (unchanged)
├── database/          (enhanced with migrations)
├── cli/               (enhanced)
├── api/               (new - FastAPI)
│   ├── routes/
│   ├── models/
│   └── auth/
├── web/               (new - React)
├── mobile/            (new - Flutter)
└── cloud/             (new - Sync service)
```

---

## Future Ideas (Post v2.0)

### Short-term (6-12 months)

- [ ] Receipt OCR for smart categorization
- [ ] Expense splitting between people
- [ ] Bill reminders and automatic payments
- [ ] Grocery price comparison
- [ ] Cashback tracking

### Medium-term (1-2 years)

- [ ] Real estate portfolio tracking
- [ ] Business expense management
- [ ] Advanced tax optimization
- [ ] Financial advisor integration
- [ ] Cryptocurrency integration

### Long-term (2+ years)

- [ ] Robo-advisor integration
- [ ] Automated investment service
- [ ] Insurance optimization
- [ ] Retirement planning tools
- [ ] Blockchain-based security

---

## Development Priorities

### Phase 1: Core Stability (Current)
1. Bug fixes and stability
2. Performance optimization
3. Documentation and examples
4. Community feedback

### Phase 2: Enhancement (v1.1-1.2)
1. User-requested features
2. Advanced analytics
3. Integration capabilities
4. Plugin system

### Phase 3: Platform Expansion (v2.0)
1. Web and mobile
2. API first approach
3. Cloud services
4. Enterprise features

---

## Contributing to Roadmap

We welcome community input! To suggest features:

1. **Check existing issues**: Avoid duplicates
2. **Create GitHub Discussion**: Describe use case
3. **Provide feedback**: Vote on features using 👍
4. **Join Development**: Contribute code!

---

## Dependencies & Technology

### Current Stack
- Python 3.11+
- Typer, Rich
- SQLite
- Pydantic

### Planned Technology

#### v1.1-1.2
- Redis (caching)
- Celery (background tasks)
- Machine Learning libraries (scikit-learn, etc.)

#### v2.0+
- FastAPI (web framework)
- PostgreSQL (cloud database)
- React (web frontend)
- Flutter (mobile)
- Docker/Kubernetes (deployment)

---

## Stability & Support

### Version Support Timeline

| Version | Release | End of Life |
|---------|---------|-------------|
| 1.0.x   | 2026-04 | 2026-10     |
| 1.1.x   | 2026-06 | 2027-06     |
| 1.2.x   | 2026-09 | 2027-09     |
| 2.0.x   | 2026-12 | 2028-12     |

- **Patch releases**: Security & critical bugs
- **Full support**: 6 months from release
- **Maintenance**: 12 months from release

---

## Breaking Changes Policy

We follow Semantic Versioning:
- **Major** (X.0.0): Breaking changes allowed
- **Minor** (0.X.0): New features, no breaking changes
- **Patch** (0.0.X): Bug fixes only

Breaking changes are announced 1+ releases in advance.

---

## Get Involved

Want to shape BudgetCLI's future?

1. **Vote on features**: Use GitHub reactions
2. **Suggest improvements**: Open discussions
3. **Contribute code**: Submit pull requests
4. **Report issues**: Help us squash bugs
5. **Write documentation**: Share knowledge

See [CONTRIBUTING.md](CONTRIBUTING.md) for details!

---

## License & Acknowledgments

This roadmap is part of the BudgetCLI project (MIT License).

**Last Updated:** 2026-04-15
**Maintained by:** Budget CLI Team
