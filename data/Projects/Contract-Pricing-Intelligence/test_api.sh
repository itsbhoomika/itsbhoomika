#!/bin/bash

# API Test and Demo Script for Contract Pricing Intelligence Prototype

API_URL="http://localhost:8000/api"

echo "🧪 Contract Pricing Intelligence API Test Suite"
echo "=============================================="
echo ""

# Test 1: Get all contracts
echo "📋 Test 1: Listing all contracts..."
curl -s "$API_URL/contracts/" | python -m json.tool | head -30
echo ""
echo "---"
echo ""

# Test 2: Get contract analytics summary
echo "📊 Test 2: Analytics summary for all contracts..."
curl -s "$API_URL/contracts/analytics_summary/" | python -m json.tool
echo ""
echo "---"
echo ""

# Test 3: Get specific contract details
echo "📄 Test 3: Getting contract CTR-2024-002 details..."
curl -s "$API_URL/contracts/2/" | python -m json.tool | head -40
echo ""
echo "---"
echo ""

# Test 4: Get contract analytics
echo "💹 Test 4: Analytics for contract CTR-2024-002..."
curl -s "$API_URL/contracts/2/analytics/" | python -m json.tool
echo ""
echo "---"
echo ""

# Test 5: Validate pricing for a contract
echo "✅ Test 5: Validating pricing rules for contract CTR-2024-002..."
curl -s -X POST "$API_URL/contracts/2/validate_pricing/" | python -m json.tool
echo ""
echo "---"
echo ""

# Test 6: Get all pricing terms
echo "💰 Test 6: Listing all pricing terms..."
curl -s "$API_URL/pricing-terms/" | python -m json.tool | head -30
echo ""
echo "---"
echo ""

# Test 7: Get validation rules
echo "📏 Test 7: Listing all validation rules..."
curl -s "$API_URL/validation-rules/" | python -m json.tool
echo ""
echo "---"
echo ""

# Test 8: Get pricing comparison
echo "📈 Test 8: Pricing comparison across contracts..."
curl -s "$API_URL/contracts/pricing_comparison/" | python -m json.tool
echo ""
echo "---"
echo ""

# Test 9: Search contracts by vendor
echo "🔍 Test 9: Searching contracts by vendor 'Cloud'..."
curl -s "$API_URL/contracts/?search=Cloud" | python -m json.tool | head -40
echo ""
echo "---"
echo ""

echo "✨ API Test Suite Completed!"
echo ""
echo "📚 Sample Data Loaded:"
echo "   • 5 sample contracts (CTR-2024-001 to CTR-2024-005)"
echo "   • 20+ pricing terms extracted"
echo "   • 5 validation rules configured"
echo ""
echo "🌐 Access Points:"
echo "   • API: $API_URL"
echo "   • Admin: http://localhost:8000/admin"
echo "   • Documentation: http://localhost:8000/api"
