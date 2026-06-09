"""
Analytics calculations for contracts
"""
from decimal import Decimal
from django.db.models import Sum, Avg, Max, Count, Q
from .models import ContractAnalytics, PricingTerm
import pandas as pd


def calculate_contract_analytics(contract):
    """Calculate analytics for a contract"""
    analytics, created = ContractAnalytics.objects.get_or_create(contract=contract)
    
    pricing_terms = contract.pricing_terms.all()
    
    if not pricing_terms.exists():
        analytics.total_contract_value = Decimal("0.00")
        analytics.average_unit_price = Decimal("0.00")
        analytics.pricing_term_count = 0
        analytics.save()
        return analytics
    
    # Calculate total contract value
    total_value = Decimal("0.00")
    recurring_revenue = Decimal("0.00")
    one_time_revenue = Decimal("0.00")
    
    for term in pricing_terms:
        term_value = term.base_price
        if term.minimum_commitment:
            term_value = max(term.base_price, term.minimum_commitment)
        
        total_value += term_value
        
        if term.is_recurring:
            recurring_revenue += term_value
        else:
            one_time_revenue += term_value
    
    # Calculate average unit price
    avg_unit_price = Decimal("0.00")
    unit_prices = pricing_terms.values_list('base_price', flat=True)
    if unit_prices:
        avg_unit_price = sum(unit_prices) / len(unit_prices)
    
    # Get highest discount
    highest_discount = pricing_terms.aggregate(Max('discount_percent'))['discount_percent__max'] or Decimal("0.00")
    
    # Count unique currencies
    currency_count = pricing_terms.values('currency').distinct().count()
    
    # Update analytics
    analytics.total_contract_value = total_value
    analytics.average_unit_price = avg_unit_price
    analytics.pricing_term_count = pricing_terms.count()
    analytics.highest_discount_percent = highest_discount
    analytics.currency_diversity = currency_count
    analytics.recurring_revenue = recurring_revenue
    analytics.one_time_revenue = one_time_revenue
    analytics.save()
    
    return analytics


def generate_pricing_report(contracts):
    """Generate a pricing report across multiple contracts"""
    data = []
    
    for contract in contracts:
        if hasattr(contract, 'analytics'):
            analytics = contract.analytics
            data.append({
                'contract_id': contract.contract_id,
                'vendor_name': contract.vendor_name,
                'client_name': contract.client_name,
                'status': contract.status,
                'total_value': float(analytics.total_contract_value),
                'avg_unit_price': float(analytics.average_unit_price),
                'pricing_terms': analytics.pricing_term_count,
                'highest_discount': float(analytics.highest_discount_percent),
                'recurring_revenue': float(analytics.recurring_revenue),
                'one_time_revenue': float(analytics.one_time_revenue),
            })
    
    if not data:
        return None
    
    df = pd.DataFrame(data)
    return {
        'dataframe': df,
        'summary': {
            'total_contracts': len(df),
            'total_portfolio_value': float(df['total_value'].sum()),
            'average_contract_value': float(df['total_value'].mean()),
            'median_contract_value': float(df['total_value'].median()),
            'total_recurring_revenue': float(df['recurring_revenue'].sum()),
            'total_one_time_revenue': float(df['one_time_revenue'].sum()),
            'contracts_by_status': df['status'].value_counts().to_dict(),
            'highest_contract_value': float(df['total_value'].max()),
            'lowest_contract_value': float(df['total_value'].min()),
        }
    }


def get_pricing_insights(contract):
    """Get key pricing insights for a contract"""
    pricing_terms = contract.pricing_terms.all()
    
    if not pricing_terms.exists():
        return {}
    
    recurring_terms = pricing_terms.filter(is_recurring=True)
    fixed_price_terms = pricing_terms.filter(term_type='fixed')
    discounted_terms = pricing_terms.filter(discount_percent__gt=0)
    
    insights = {
        'total_pricing_terms': pricing_terms.count(),
        'recurring_terms_count': recurring_terms.count(),
        'fixed_price_terms_count': fixed_price_terms.count(),
        'discounted_terms_count': discounted_terms.count(),
        'has_tiered_pricing': pricing_terms.filter(term_type='tiered').exists(),
        'has_usage_based_pricing': pricing_terms.filter(term_type='usage').exists(),
        'pricing_types': list(pricing_terms.values_list('term_type', flat=True).distinct()),
        'currencies': list(pricing_terms.values_list('currency', flat=True).distinct()),
    }
    
    # Add pricing term details
    insights['terms_detail'] = [
        {
            'type': term.term_type,
            'base_price': float(term.base_price),
            'currency': term.currency,
            'discount': float(term.discount_percent),
            'recurring': term.is_recurring,
            'billing_frequency': term.billing_frequency,
        }
        for term in pricing_terms
    ]
    
    return insights
