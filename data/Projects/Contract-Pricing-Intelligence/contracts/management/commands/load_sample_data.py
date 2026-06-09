from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from contracts.models import Contract, ValidationRule
from contracts.pricing_parser import parse_contract_terms
from contracts.analytics import calculate_contract_analytics
import json


class Command(BaseCommand):
    help = 'Load sample contract data and validation rules'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Loading sample data...'))
        
        # Create sample contracts
        sample_contracts = [
            {
                'contract_id': 'CTR-2024-001',
                'contract_name': 'SaaS Platform License Agreement',
                'vendor_name': 'CloudTech Solutions',
                'client_name': 'Enterprise Corp',
                'status': 'active',
                'raw_terms': '''
                Software License: $50,000 per year fixed price.
                Volume Tier 1: 1-100 users at $500 per user.
                Volume Tier 2: 101-500 users at $450 per user.
                Volume Tier 3: 500+ users at $400 per user.
                Monthly billing available at 10% premium.
                Payment Terms: Net 30 from invoice date.
                Minimum Commitment: $150,000 per year.
                Usage-based surcharges apply at $0.50 per API call above 1M calls/month.
                Annual discount: 15% for prepayment.
                '''
            },
            {
                'contract_id': 'CTR-2024-002',
                'contract_name': 'Data Processing Services',
                'vendor_name': 'DataFlow Inc',
                'client_name': 'Analytics Firm Ltd',
                'status': 'active',
                'raw_terms': '''
                Base Processing Fee: $25,000 per month.
                Data Storage: $0.50 per GB per month.
                Volume discount: 20% for processing >10TB per month.
                Real-time processing premium: +$5,000/month.
                Quarterly billing with Net 45 payment terms.
                Minimum monthly commitment: $30,000.
                '''
            },
            {
                'contract_id': 'CTR-2024-003',
                'contract_name': 'Consulting Services Agreement',
                'vendor_name': 'Advisory Partners',
                'client_name': 'Tech Startup XYZ',
                'status': 'draft',
                'raw_terms': '''
                Senior Consultant Rate: $250 per hour.
                Mid-level Consultant Rate: $150 per hour.
                Junior Consultant Rate: $75 per hour.
                Project Fixed Price: $100,000 for 6-month engagement.
                Retainer model available at $15,000 per month.
                Discount for annual commitment: 25%.
                Payment terms: Net 60 for invoices over $50,000, otherwise Net 30.
                '''
            },
            {
                'contract_id': 'CTR-2024-004',
                'contract_name': 'Infrastructure Services',
                'vendor_name': 'CloudHost Provider',
                'client_name': 'Media Company ABC',
                'status': 'active',
                'raw_terms': '''
                Virtual Machines: $500 per instance per month.
                Storage: $0.10 per GB per month.
                Bandwidth: $0.05 per GB beyond 10TB monthly allocation.
                Compute Units: $100 per vCPU per month.
                Premium support tier: +$5,000 per month.
                Hybrid pricing model combining fixed and usage-based.
                Volume tier: 10% discount for >50 instances.
                Annual prepayment option: 20% discount.
                '''
            },
            {
                'contract_id': 'CTR-2024-005',
                'contract_name': 'Maintenance and Support',
                'vendor_name': 'TechSupport Global',
                'client_name': 'Insurance Group',
                'status': 'expired',
                'raw_terms': '''
                24/7 Support Coverage: $8,000 per month.
                Incident Response (up to 5 tickets/month): Included.
                Additional Incidents: $500 per ticket.
                Preventive Maintenance: $2,000 per quarter.
                Emergency On-Site Support: $3,000 per visit.
                Payment: Monthly billing with Net 30 terms.
                Annual commitment required for 15% discount.
                '''
            }
        ]
        
        created_contracts = []
        for contract_data in sample_contracts:
            start_date = timezone.now().date()
            end_date = start_date + timedelta(days=365)
            
            contract, created = Contract.objects.get_or_create(
                contract_id=contract_data['contract_id'],
                defaults={
                    'contract_name': contract_data['contract_name'],
                    'vendor_name': contract_data['vendor_name'],
                    'client_name': contract_data['client_name'],
                    'status': contract_data['status'],
                    'raw_terms': contract_data['raw_terms'],
                    'start_date': start_date,
                    'end_date': end_date,
                }
            )
            
            if created:
                created_contracts.append(contract)
                self.stdout.write(f'  Created contract: {contract.contract_id}')
                
                # Parse terms and calculate analytics
                parse_contract_terms(contract)
                calculate_contract_analytics(contract)
            else:
                self.stdout.write(f'  Contract already exists: {contract.contract_id}')
        
        # Create validation rules
        validation_rules = [
            {
                'rule_name': 'Minimum Unit Price',
                'description': 'Ensure all pricing terms have a minimum unit price of $50',
                'rule_type': 'min_price',
                'condition_json': json.dumps({'min_price': 50}),
                'action': 'WARN: Unit price below minimum threshold'
            },
            {
                'rule_name': 'Maximum Discount Limit',
                'description': 'Prevent discounts exceeding 30%',
                'rule_type': 'max_discount',
                'condition_json': json.dumps({'max_discount': 30}),
                'action': 'BLOCK: Discount exceeds maximum allowed'
            },
            {
                'rule_name': 'Required Payment Terms',
                'description': 'All pricing terms must have payment terms defined',
                'rule_type': 'required_field',
                'condition_json': json.dumps({'field': 'payment_terms'}),
                'action': 'WARN: Payment terms not specified'
            },
            {
                'rule_name': 'Volume Tier Consistency',
                'description': 'Tiered pricing must have volume tiers defined',
                'rule_type': 'required_field',
                'condition_json': json.dumps({'field': 'volume_tier_min'}),
                'action': 'ERROR: Tiered pricing without volume tier definition'
            },
            {
                'rule_name': 'Currency Consistency',
                'description': 'Contract should use consistent currency',
                'rule_type': 'currency_check',
                'condition_json': json.dumps({'allowed_currencies': ['USD', 'EUR', 'GBP']}),
                'action': 'WARN: Unsupported currency detected'
            }
        ]
        
        for rule_data in validation_rules:
            rule, created = ValidationRule.objects.get_or_create(
                rule_name=rule_data['rule_name'],
                defaults={
                    'description': rule_data['description'],
                    'rule_type': rule_data['rule_type'],
                    'condition_json': rule_data['condition_json'],
                    'action': rule_data['action'],
                    'is_active': True,
                }
            )
            
            if created:
                self.stdout.write(f'  Created rule: {rule.rule_name}')
            else:
                self.stdout.write(f'  Rule already exists: {rule.rule_name}')
        
        self.stdout.write(self.style.SUCCESS(
            f'\nSuccessfully loaded {len(created_contracts)} contracts and {len(validation_rules)} validation rules!'
        ))
