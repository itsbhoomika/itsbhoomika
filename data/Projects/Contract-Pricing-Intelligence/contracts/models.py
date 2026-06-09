from django.db import models
from django.core.validators import MinValueValidator
import json


class Contract(models.Model):
    """Contract model to store contract information"""
    
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("active", "Active"),
        ("expired", "Expired"),
        ("terminated", "Terminated"),
    ]
    
    contract_id = models.CharField(max_length=100, unique=True)
    contract_name = models.CharField(max_length=255)
    vendor_name = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    raw_terms = models.TextField(help_text="Raw contract terms text")
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    s3_document_path = models.CharField(max_length=512, blank=True, null=True)
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.contract_id} - {self.contract_name}"


class PricingTerm(models.Model):
    """Structured pricing fields extracted from contract terms"""
    
    PRICING_TYPE_CHOICES = [
        ("fixed", "Fixed Price"),
        ("variable", "Variable"),
        ("tiered", "Tiered"),
        ("usage", "Usage-Based"),
        ("hybrid", "Hybrid"),
    ]
    
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="pricing_terms")
    term_type = models.CharField(max_length=50, choices=PRICING_TYPE_CHOICES, default="fixed")
    description = models.TextField()
    base_price = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, default="USD")
    unit = models.CharField(max_length=50, blank=True, default="unit")
    volume_tier_min = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    volume_tier_max = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    is_recurring = models.BooleanField(default=False)
    billing_frequency = models.CharField(max_length=50, blank=True)  # e.g., "monthly", "annual"
    payment_terms = models.CharField(max_length=255, blank=True)  # e.g., "Net 30", "Net 60"
    minimum_commitment = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.contract.contract_id} - {self.term_type}"


class ValidationRule(models.Model):
    """Payer-policy style validation rules for pricing"""
    
    rule_name = models.CharField(max_length=255)
    description = models.TextField()
    rule_type = models.CharField(max_length=50)  # e.g., "min_price", "max_discount", "required_field"
    condition_json = models.TextField(help_text="JSON conditions for rule validation")
    action = models.CharField(max_length=255, help_text="Action to take when rule is violated")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.rule_name
    
    def get_conditions(self):
        """Parse JSON conditions"""
        return json.loads(self.condition_json)


class ContractAnalytics(models.Model):
    """Cached analytics for contracts"""
    
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, related_name="analytics")
    total_contract_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    average_unit_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    pricing_term_count = models.IntegerField(default=0)
    highest_discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    currency_diversity = models.IntegerField(default=0)  # Count of different currencies
    recurring_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    one_time_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    last_calculated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Analytics for {self.contract.contract_id}"
