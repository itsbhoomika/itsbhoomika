from rest_framework import serializers
from .models import Contract, PricingTerm, ValidationRule, ContractAnalytics


class PricingTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingTerm
        fields = [
            "id",
            "term_type",
            "description",
            "base_price",
            "currency",
            "unit",
            "volume_tier_min",
            "volume_tier_max",
            "discount_percent",
            "is_recurring",
            "billing_frequency",
            "payment_terms",
            "minimum_commitment",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class ContractAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractAnalytics
        fields = [
            "total_contract_value",
            "average_unit_price",
            "pricing_term_count",
            "highest_discount_percent",
            "currency_diversity",
            "recurring_revenue",
            "one_time_revenue",
            "last_calculated",
        ]
        read_only_fields = [
            "total_contract_value",
            "average_unit_price",
            "pricing_term_count",
            "highest_discount_percent",
            "currency_diversity",
            "recurring_revenue",
            "one_time_revenue",
            "last_calculated",
        ]


class ContractSerializer(serializers.ModelSerializer):
    pricing_terms = PricingTermSerializer(many=True, read_only=True)
    analytics = ContractAnalyticsSerializer(read_only=True)
    
    class Meta:
        model = Contract
        fields = [
            "id",
            "contract_id",
            "contract_name",
            "vendor_name",
            "client_name",
            "status",
            "raw_terms",
            "start_date",
            "end_date",
            "created_at",
            "updated_at",
            "s3_document_path",
            "pricing_terms",
            "analytics",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "pricing_terms", "analytics"]


class ContractCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = [
            "contract_id",
            "contract_name",
            "vendor_name",
            "client_name",
            "status",
            "raw_terms",
            "start_date",
            "end_date",
            "s3_document_path",
        ]


class ValidationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValidationRule
        fields = [
            "id",
            "rule_name",
            "description",
            "rule_type",
            "condition_json",
            "action",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
