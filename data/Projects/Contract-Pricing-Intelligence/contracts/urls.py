from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContractViewSet, PricingTermViewSet, ValidationRuleViewSet

router = DefaultRouter()
router.register(r'contracts', ContractViewSet, basename='contract')
router.register(r'pricing-terms', PricingTermViewSet, basename='pricing-term')
router.register(r'validation-rules', ValidationRuleViewSet, basename='validation-rule')

urlpatterns = [
    path('', include(router.urls)),
]
