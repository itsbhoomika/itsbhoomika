from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Avg, Q, Count
from .models import Contract, PricingTerm, ValidationRule, ContractAnalytics
from .serializers import (
    ContractSerializer,
    ContractCreateUpdateSerializer,
    PricingTermSerializer,
    ValidationRuleSerializer,
    ContractAnalyticsSerializer,
)
from .pricing_parser import parse_contract_terms
from .analytics import calculate_contract_analytics
import pandas as pd


class ContractViewSet(viewsets.ModelViewSet):
    """ViewSet for Contract CRUD operations"""
    
    queryset = Contract.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["contract_id", "contract_name", "vendor_name", "client_name"]
    
    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ContractCreateUpdateSerializer
        return ContractSerializer
    
    @action(detail=False, methods=["get"])
    def analytics_summary(self, request):
        """Get analytics summary for all contracts"""
        contracts = self.get_queryset()
        total_contracts = contracts.count()
        active_contracts = contracts.filter(status="active").count()
        total_value = sum([
            float(c.analytics.total_contract_value) 
            for c in contracts if hasattr(c, 'analytics')
        ])
        
        return Response({
            "total_contracts": total_contracts,
            "active_contracts": active_contracts,
            "total_portfolio_value": total_value,
            "average_contract_value": total_value / total_contracts if total_contracts > 0 else 0,
        })
    
    @action(detail=True, methods=["post"])
    def parse_terms(self, request, pk=None):
        """Parse raw contract terms into structured pricing fields"""
        contract = self.get_object()
        pricing_terms = parse_contract_terms(contract)
        
        # Calculate analytics after parsing
        calculate_contract_analytics(contract)
        
        serializer = PricingTermSerializer(contract.pricing_terms.all(), many=True)
        return Response({
            "message": f"Parsed {len(pricing_terms)} pricing terms",
            "pricing_terms": serializer.data,
        })
    
    @action(detail=True, methods=["get"])
    def analytics(self, request, pk=None):
        """Get detailed analytics for a contract"""
        contract = self.get_object()
        analytics, created = ContractAnalytics.objects.get_or_create(contract=contract)
        calculate_contract_analytics(contract)
        analytics.refresh_from_db()
        
        serializer = ContractAnalyticsSerializer(analytics)
        return Response(serializer.data)
    
    @action(detail=True, methods=["post"])
    def validate_pricing(self, request, pk=None):
        """Validate pricing terms against active rules"""
        contract = self.get_object()
        rules = ValidationRule.objects.filter(is_active=True)
        
        validation_results = []
        for rule in rules:
            result = validate_contract_against_rule(contract, rule)
            validation_results.append(result)
        
        violations = [r for r in validation_results if not r["passed"]]
        return Response({
            "total_rules": len(validation_results),
            "passed": len(validation_results) - len(violations),
            "violations": violations,
        })
    
    @action(detail=False, methods=["get"])
    def pricing_comparison(self, request):
        """Compare pricing across contracts"""
        contracts = self.get_queryset()
        data = []
        
        for contract in contracts[:20]:  # Limit to 20 for performance
            if hasattr(contract, 'analytics'):
                data.append({
                    "contract_id": contract.contract_id,
                    "vendor_name": contract.vendor_name,
                    "total_value": float(contract.analytics.total_contract_value),
                    "avg_unit_price": float(contract.analytics.average_unit_price),
                    "highest_discount": float(contract.analytics.highest_discount_percent),
                })
        
        df = pd.DataFrame(data)
        if len(df) > 0:
            stats = {
                "min_total_value": float(df["total_value"].min()),
                "max_total_value": float(df["total_value"].max()),
                "avg_total_value": float(df["total_value"].mean()),
                "min_unit_price": float(df["avg_unit_price"].min()),
                "max_unit_price": float(df["avg_unit_price"].max()),
            }
        else:
            stats = {}
        
        return Response({
            "contracts": data,
            "statistics": stats,
        })


class PricingTermViewSet(viewsets.ModelViewSet):
    """ViewSet for PricingTerm CRUD operations"""
    
    queryset = PricingTerm.objects.all()
    serializer_class = PricingTermSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["contract__contract_id", "term_type", "description"]
    
    @action(detail=False, methods=["get"])
    def by_contract(self, request):
        """Get pricing terms filtered by contract_id"""
        contract_id = request.query_params.get("contract_id")
        if contract_id:
            terms = self.get_queryset().filter(contract__contract_id=contract_id)
            serializer = self.get_serializer(terms, many=True)
            return Response(serializer.data)
        return Response({"error": "contract_id parameter required"}, status=status.HTTP_400_BAD_REQUEST)


class ValidationRuleViewSet(viewsets.ModelViewSet):
    """ViewSet for ValidationRule CRUD operations"""
    
    queryset = ValidationRule.objects.all()
    serializer_class = ValidationRuleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["rule_name", "rule_type"]
    
    @action(detail=False, methods=["post"])
    def bulk_create(self, request):
        """Create multiple validation rules at once"""
        rules_data = request.data.get("rules", [])
        created_rules = []
        
        for rule_data in rules_data:
            serializer = self.get_serializer(data=rule_data)
            if serializer.is_valid():
                serializer.save()
                created_rules.append(serializer.data)
        
        return Response({
            "created": len(created_rules),
            "rules": created_rules,
        }, status=status.HTTP_201_CREATED)


def validate_contract_against_rule(contract, rule):
    """Validate a contract against a validation rule"""
    try:
        conditions = rule.get_conditions()
        
        # Simple rule validation logic
        if rule.rule_type == "min_price":
            min_price = conditions.get("min_price", 0)
            has_violation = contract.pricing_terms.filter(base_price__lt=min_price).exists()
            return {
                "rule_name": rule.rule_name,
                "passed": not has_violation,
                "action": rule.action if has_violation else None,
            }
        
        elif rule.rule_type == "max_discount":
            max_discount = conditions.get("max_discount", 0)
            has_violation = contract.pricing_terms.filter(discount_percent__gt=max_discount).exists()
            return {
                "rule_name": rule.rule_name,
                "passed": not has_violation,
                "action": rule.action if has_violation else None,
            }
        
        elif rule.rule_type == "required_field":
            required_field = conditions.get("field")
            has_all = contract.pricing_terms.exclude(**{required_field + "__isnull": True}).exists()
            return {
                "rule_name": rule.rule_name,
                "passed": has_all,
                "action": rule.action if not has_all else None,
            }
        
        return {
            "rule_name": rule.rule_name,
            "passed": True,
            "action": None,
        }
    except Exception as e:
        return {
            "rule_name": rule.rule_name,
            "passed": False,
            "error": str(e),
            "action": rule.action,
        }
