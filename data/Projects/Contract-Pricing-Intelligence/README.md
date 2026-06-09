# Contract Pricing Intelligence Prototype

A Django + PostgreSQL application that parses contract terms into structured pricing fields, implements CRUD workflows, and exposes contract-level analytics using Python, SQL, pandas, and AWS S3.

## Features

- **Contract Management**: Full CRUD operations for contracts
- **Pricing Term Parsing**: Automatic parsing of raw contract text into structured pricing fields
- **Analytics Dashboard**: Contract-level analytics including total value, recurring revenue, discounts
- **Validation Rules**: Payer-policy style rule extraction and validation
- **AWS S3 Integration**: Upload and manage contract documents in S3
- **RESTful API**: Complete REST API for all operations
- **Django Admin**: Full admin interface for data management

## Quick Start

### Prerequisites
- Python 3.9+
- pip

### Installation

1. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Create superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

5. **Load sample data**:
   ```bash
   python manage.py load_sample_data
   ```

6. **Start development server**:
   ```bash
   python manage.py runserver
   ```

Server will run at: http://localhost:8000

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following optional settings:

```
# Database (defaults to SQLite)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=contract_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# AWS S3 (optional)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_STORAGE_BUCKET_NAME=contract-pricing-bucket
AWS_S3_REGION_NAME=us-east-1
```

### Default Credentials

- **Admin User**: admin / admin123

## API Endpoints

### Contracts

- **List all contracts**: `GET /api/contracts/`
- **Create contract**: `POST /api/contracts/`
- **Get contract details**: `GET /api/contracts/{id}/`
- **Update contract**: `PUT /api/contracts/{id}/`
- **Delete contract**: `DELETE /api/contracts/{id}/`
- **Parse contract terms**: `POST /api/contracts/{id}/parse_terms/`
- **Get contract analytics**: `GET /api/contracts/{id}/analytics/`
- **Validate pricing**: `POST /api/contracts/{id}/validate_pricing/`
- **Analytics summary**: `GET /api/contracts/analytics_summary/`
- **Pricing comparison**: `GET /api/contracts/pricing_comparison/`

### Pricing Terms

- **List pricing terms**: `GET /api/pricing-terms/`
- **Create pricing term**: `POST /api/pricing-terms/`
- **Get by contract**: `GET /api/pricing-terms/by_contract/?contract_id=CTR-2024-001`

### Validation Rules

- **List rules**: `GET /api/validation-rules/`
- **Create rule**: `POST /api/validation-rules/`
- **Bulk create rules**: `POST /api/validation-rules/bulk_create/`

## Key Models

### Contract
- `contract_id`: Unique identifier
- `contract_name`: Human-readable name
- `vendor_name`: Vendor/supplier name
- `client_name`: Client/customer name
- `status`: Draft, Active, Expired, Terminated
- `raw_terms`: Raw contract text
- `start_date` / `end_date`: Contract validity period
- `s3_document_path`: Optional S3 location for PDF

### PricingTerm
- `term_type`: Fixed, Variable, Tiered, Usage, Hybrid
- `base_price`: Base pricing
- `currency`: Currency code (USD, EUR, etc.)
- `volume_tier_min/max`: Volume tier boundaries
- `discount_percent`: Applicable discount
- `is_recurring`: Recurring vs one-time
- `billing_frequency`: Monthly, Quarterly, Annual, etc.
- `payment_terms`: Net 30, Net 60, etc.
- `minimum_commitment`: Minimum contract value

### ValidationRule
- `rule_name`: Rule identifier
- `rule_type`: min_price, max_discount, required_field, etc.
- `condition_json`: Rule conditions as JSON
- `action`: Action to take on violation
- `is_active`: Enable/disable rule

### ContractAnalytics
- `total_contract_value`: Sum of all pricing terms
- `average_unit_price`: Mean unit price
- `pricing_term_count`: Number of pricing terms
- `highest_discount_percent`: Max discount applied
- `currency_diversity`: Number of different currencies
- `recurring_revenue`: Sum of recurring charges
- `one_time_revenue`: Sum of one-time charges

## Example API Usage

### Create a Contract
```bash
curl -X POST http://localhost:8000/api/contracts/ \
  -H "Content-Type: application/json" \
  -d '{
    "contract_id": "CTR-2024-006",
    "contract_name": "New Partnership Agreement",
    "vendor_name": "Tech Vendor Inc",
    "client_name": "My Company",
    "status": "active",
    "raw_terms": "Monthly fee: $5,000 per month. Additional users at $100 each. Annual discount: 10%.",
    "start_date": "2024-06-04",
    "end_date": "2025-06-04"
  }'
```

### Parse Contract Terms
```bash
curl -X POST http://localhost:8000/api/contracts/1/parse_terms/
```

### Get Analytics
```bash
curl http://localhost:8000/api/contracts/1/analytics/
```

### Validate Against Rules
```bash
curl -X POST http://localhost:8000/api/contracts/1/validate_pricing/
```

### Get Pricing Comparison
```bash
curl http://localhost:8000/api/contracts/pricing_comparison/
```

## Project Structure

```
contract/
├── contract_project/          # Django project settings
│   ├── settings.py           # Configuration
│   ├── urls.py              # URL routing
│   └── wsgi.py
├── contracts/               # Main application
│   ├── models.py            # Data models
│   ├── views.py             # ViewSets and views
│   ├── serializers.py       # DRF serializers
│   ├── urls.py              # App URLs
│   ├── pricing_parser.py    # Contract term parser
│   ├── analytics.py         # Analytics calculations
│   ├── s3_storage.py        # AWS S3 utilities
│   ├── admin.py             # Admin configuration
│   └── management/
│       └── commands/
│           └── load_sample_data.py  # Data loading command
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── .env                    # Environment variables
└── README.md               # This file
```

## Technologies Used

- **Framework**: Django 4.2
- **API**: Django REST Framework
- **Database**: PostgreSQL (or SQLite for development)
- **Data Analysis**: Pandas
- **Cloud Storage**: AWS S3 (boto3)
- **Python Version**: 3.9+

## Development

### Run Tests
```bash
python manage.py test
```

### Create New Migration
```bash
python manage.py makemigrations
```

### Apply Migrations
```bash
python manage.py migrate
```

### Access Django Admin
Visit: http://localhost:8000/admin
Login with superuser credentials

## Production Deployment

For production deployment:

1. Set `DEBUG = False` in settings
2. Configure allowed hosts
3. Use PostgreSQL database
4. Set up environment variables securely
5. Use a production WSGI server (gunicorn, uWSGI)
6. Configure AWS S3 credentials
7. Enable HTTPS and CORS as needed

## Notes

- The pricing parser uses regex patterns to extract pricing information from raw contract text
- Analytics are calculated on-demand but can be cached for performance
- Validation rules use JSON conditions for flexible rule definition
- S3 integration is optional and requires AWS credentials

## Future Enhancements

- AI-powered contract parsing using NLP
- Advanced analytics and reporting
- Contract comparison and benchmarking
- Approval workflows
- Automated pricing optimization suggestions
- Integration with accounting systems
