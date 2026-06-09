"""
Pricing term parser for extracting structured pricing fields from raw contract text
"""
import re
from decimal import Decimal
from .models import PricingTerm


def parse_contract_terms(contract):
    """
    Parse raw contract terms and create PricingTerm objects
    Uses simple regex and keyword extraction to simulate AI parsing
    """
    raw_text = contract.raw_terms.lower()
    pricing_terms = []
    
    # Clear existing pricing terms
    contract.pricing_terms.all().delete()
    
    # Extract base prices
    price_patterns = [
        r'\$[\d,]+(?:\.\d{2})?',
        r'(?:price|cost|charge)[\s:]*\$?([\d,]+(?:\.\d{2})?)',
    ]
    
    prices = []
    for pattern in price_patterns:
        matches = re.findall(pattern, raw_text)
        prices.extend(matches)
    
    # Determine pricing type
    pricing_type = determine_pricing_type(raw_text)
    
    # Extract volume tiers
    tier_pattern = r'(?:tier|volume|quantity)[\s:]*(\d+)\s*(?:to|-)?\s*(\d+)?'
    tier_matches = re.findall(tier_pattern, raw_text)
    
    # Extract discount information
    discount_pattern = r'(?:discount)[\s:]*(\d+)%?'
    discount_matches = re.findall(discount_pattern, raw_text)
    
    # Extract payment terms
    payment_pattern = r'(?:payment|net|terms)[\s:]*(net\s*\d+|due\s*(?:upon|on)\s*\w+)'
    payment_matches = re.findall(payment_pattern, raw_text)
    payment_terms = payment_matches[0] if payment_matches else ""
    
    # Extract billing frequency
    frequency_pattern = r'(?:billing|charged?|invoiced?)[\s:]*(monthly|quarterly|annually|weekly|daily)'
    frequency_matches = re.findall(frequency_pattern, raw_text)
    billing_frequency = frequency_matches[0] if frequency_matches else ""
    
    # Extract minimum commitment
    commitment_pattern = r'(?:minimum|commitment|guarantee)[\s:]*\$?([\d,]+(?:\.\d{2})?)'
    commitment_matches = re.findall(commitment_pattern, raw_text)
    minimum_commitment = commitment_matches[0] if commitment_matches else None
    
    # Create pricing term entries
    if prices:
        for idx, price_str in enumerate(prices[:5]):  # Limit to 5 terms
            try:
                base_price = Decimal(price_str.replace('$', '').replace(',', ''))
                
                # Determine tier if available
                tier_min = None
                tier_max = None
                if idx < len(tier_matches):
                    tier_min = int(tier_matches[idx][0])
                    tier_max = int(tier_matches[idx][1]) if tier_matches[idx][1] else None
                
                # Get discount
                discount = Decimal(discount_matches[idx]) if idx < len(discount_matches) else Decimal(0)
                
                # Extract currency
                currency = "USD"
                
                # Extract unit
                unit_pattern = r'(?:per|each|unit|license|seat|user|transaction)[\s:]*(\w+)?'
                unit_match = re.search(unit_pattern, raw_text)
                unit = unit_match.group(1) if unit_match else "unit"
                
                # Determine recurring
                is_recurring = any(word in raw_text for word in ['monthly', 'quarterly', 'annually', 'recurring', 'subscription'])
                
                # Create pricing term
                term = PricingTerm.objects.create(
                    contract=contract,
                    term_type=pricing_type,
                    description=f"Pricing term {idx + 1} extracted from contract",
                    base_price=base_price,
                    currency=currency,
                    unit=unit,
                    volume_tier_min=tier_min,
                    volume_tier_max=tier_max,
                    discount_percent=discount,
                    is_recurring=is_recurring,
                    billing_frequency=billing_frequency,
                    payment_terms=payment_terms,
                    minimum_commitment=Decimal(minimum_commitment.replace(',', '')) if minimum_commitment else None,
                )
                pricing_terms.append(term)
            except (ValueError, AttributeError):
                continue
    
    # If no pricing terms extracted, create a default one
    if not pricing_terms:
        term = PricingTerm.objects.create(
            contract=contract,
            term_type="variable",
            description="Default pricing term - no specific price extracted",
            base_price=Decimal("0.00"),
            currency="USD",
            is_recurring=False,
        )
        pricing_terms.append(term)
    
    return pricing_terms


def determine_pricing_type(text):
    """Determine the pricing type based on keyword analysis"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['fixed', 'flat', 'fixed price']):
        return "fixed"
    elif any(word in text_lower for word in ['tiered', 'volume tier', 'quantity discount']):
        return "tiered"
    elif any(word in text_lower for word in ['usage', 'per unit', 'pay-per', 'metered']):
        return "usage"
    elif any(word in text_lower for word in ['variable', 'dynamic', 'adjustable']):
        return "variable"
    else:
        return "hybrid"


def extract_currency(text):
    """Extract currency from text"""
    currencies = {
        '$': 'USD',
        '€': 'EUR',
        '£': 'GBP',
        '¥': 'JPY',
        '₹': 'INR',
    }
    
    for symbol, code in currencies.items():
        if symbol in text:
            return code
    
    return "USD"
