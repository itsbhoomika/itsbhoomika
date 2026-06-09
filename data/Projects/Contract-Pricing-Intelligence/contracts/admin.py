from django.contrib import admin
from .models import Contract, PricingTerm, ValidationRule, ContractAnalytics


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['contract_id', 'contract_name', 'vendor_name', 'status', 'start_date', 'end_date']
    list_filter = ['status', 'created_at']
    search_fields = ['contract_id', 'contract_name', 'vendor_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PricingTerm)
class PricingTermAdmin(admin.ModelAdmin):
    list_display = ['id', 'contract', 'term_type', 'base_price', 'currency', 'is_recurring']
    list_filter = ['term_type', 'currency', 'is_recurring']
    search_fields = ['contract__contract_id', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ValidationRule)
class ValidationRuleAdmin(admin.ModelAdmin):
    list_display = ['rule_name', 'rule_type', 'is_active', 'created_at']
    list_filter = ['rule_type', 'is_active']
    search_fields = ['rule_name', 'description']
    readonly_fields = ['created_at']


@admin.register(ContractAnalytics)
class ContractAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['contract', 'total_contract_value', 'pricing_term_count', 'recurring_revenue']
    list_filter = ['contract__status']
    search_fields = ['contract__contract_id']
    readonly_fields = ['total_contract_value', 'average_unit_price', 'pricing_term_count', 'highest_discount_percent', 'currency_diversity', 'recurring_revenue', 'one_time_revenue', 'last_calculated']
