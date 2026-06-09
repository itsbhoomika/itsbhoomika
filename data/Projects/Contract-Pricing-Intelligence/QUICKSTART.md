# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### 1. Start the Server
```bash
cd /Users/beee/Documents/bhoomi/contract
source venv/bin/activate
python manage.py runserver
```

The server will start at `http://localhost:8000`

### 2. Access the Application

- **API Root**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin (credentials: admin / admin123)
- **Contracts Endpoint**: http://localhost:8000/api/contracts/

## 📡 API Examples

### Create a New Contract
```bash
curl -X POST http://localhost:8000/api/contracts/ \
  -H "Content-Type: application/json" \
  -d '{
    "contract_id": "CTR-2024-006",
    "contract_name": "New SaaS Agreement",
    "vendor_name": "NewTech Inc",
    "client_name": "My Corp",
    "status": "active",
    "raw_terms": "Base price: $25,000 per month. Volume discount: 15% for 100+ users. Annual commitment: $250,000 with 20% discount.",
    "start_date": "2024-06-04",
    "end_date": "2025-06-04"
  }'
```

### Parse Contract Terms
```bash
# Automatically parse raw contract text into structured pricing fields
curl -X POST http://localhost:8000/api/contracts/1/parse_terms/
```

### Get Contract Analytics
```bash
curl http://localhost:8000/api/contracts/1/analytics/
```

### Validate Contract Pricing
```bash
curl -X POST http://localhost:8000/api/contracts/1/validate_pricing/
```

### Compare Pricing Across Contracts
```bash
curl http://localhost:8000/api/contracts/pricing_comparison/
```

### Get Analytics Summary
```bash
curl http://localhost:8000/api/contracts/analytics_summary/
```

### List All Pricing Terms
```bash
curl http://localhost:8000/api/pricing-terms/
```

### List Validation Rules
```bash
curl http://localhost:8000/api/validation-rules/
```

### Search Contracts
```bash
# Search by contract ID, name, vendor, or client
curl "http://localhost:8000/api/contracts/?search=CloudTech"
```

### Get Pricing Terms by Contract
```bash
curl "http://localhost:8000/api/pricing-terms/by_contract/?contract_id=CTR-2024-001"
```

## 📊 Key Features Demonstrated

### 1. Contract Management
- Full CRUD operations for contracts
- Contract status tracking (draft, active, expired, terminated)
- Raw contract term storage for reference

### 2. Intelligent Parsing
- Regex-based extraction of pricing information from contract text
- Automatic categorization of pricing types (fixed, tiered, usage-based, etc.)
- Currency and unit detection
- Discount and volume tier extraction

### 3. Analytics
- Total contract value calculation
- Average unit price computation
- Recurring vs one-time revenue split
- Discount analysis
- Currency diversity tracking
- Portfolio-level analytics and benchmarking

### 4. Validation Rules
- Payer-policy style rule engine
- Rules for minimum pricing, maximum discounts, required fields
- JSON-based condition definition
- Active/inactive rule toggling

### 5. RESTful API
- Complete pagination support
- Search and filter capabilities
- Comprehensive error handling
- Standardized JSON responses

## 📁 Sample Data

The system is pre-loaded with 5 sample contracts:

1. **CTR-2024-001**: SaaS Platform License ($50k+ annual)
2. **CTR-2024-002**: Data Processing Services (tiered pricing)
3. **CTR-2024-003**: Consulting Services (hourly & fixed rate)
4. **CTR-2024-004**: Infrastructure Services (hybrid pricing)
5. **CTR-2024-005**: Maintenance & Support (recurring charges)

## 🔧 Common Tasks

### Create Multiple Contracts
See `test_api.sh` for comprehensive API testing examples.

### Access Database Directly
```bash
python manage.py shell
```

Then in the shell:
```python
from contracts.models import Contract, PricingTerm
contracts = Contract.objects.all()
for contract in contracts:
    print(f"{contract.contract_id}: {contract.contract_name}")
    for term in contract.pricing_terms.all():
        print(f"  - {term.term_type}: ${term.base_price}")
```

### Export Data as CSV
```python
import pandas as pd
from contracts.models import Contract
from contracts.analytics import generate_pricing_report

contracts = Contract.objects.all()
report = generate_pricing_report(contracts)
if report:
    df = report['dataframe']
    df.to_csv('contract_pricing_report.csv', index=False)
```

### Load Additional Sample Data
```bash
python manage.py load_sample_data
```

## 🌐 Environment Variables

To use AWS S3 or PostgreSQL, create a `.env` file:

```
# PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=contract_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# AWS S3
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_STORAGE_BUCKET_NAME=contract-bucket
AWS_S3_REGION_NAME=us-east-1
```

## 📝 Notes

- The pricing parser uses regex patterns; real implementations might use NLP
- S3 integration requires AWS credentials (optional)
- Database defaults to SQLite; switch to PostgreSQL for production
- All timestamps are in UTC

## 🆘 Troubleshooting

**Port already in use?**
```bash
python manage.py runserver 8080
```

**Database errors?**
```bash
python manage.py migrate
```

**Want to reset everything?**
```bash
rm db.sqlite3
python manage.py migrate
python manage.py load_sample_data
```

## 🎓 Learning Resources

- Django Documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- PostgreSQL: https://www.postgresql.org/docs/
- Pandas Documentation: https://pandas.pydata.org/docs/
- AWS S3: https://docs.aws.amazon.com/s3/
