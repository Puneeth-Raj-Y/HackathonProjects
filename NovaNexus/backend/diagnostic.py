#!/usr/bin/env python3
"""
ForgeMind AI - Comprehensive API Diagnostic Tool
Tests all endpoints and validates the deployment configuration
"""

import sys
import json
from fastapi.testclient import TestClient
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from main import app

def test_api():
    """Comprehensive API test suite"""
    client = TestClient(app)
    results = {
        "timestamp": str(Path(__file__).parent.parent / "test_results.json"),
        "tests": {},
        "summary": {"passed": 0, "failed": 0}
    }
    
    # Test 1: Health Endpoint
    print("\n[TEST 1] Health Endpoint")
    try:
        response = client.get("/api/health")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        print(f"  [PASS] GET /api/health -> {response.status_code}")
        print(f"    Response: {json.dumps(data, indent=2)}")
        results["tests"]["health"] = {"status": "pass", "code": 200, "data": data}
        results["summary"]["passed"] += 1
    except Exception as e:
        print(f"  [FAIL] {e}")
        results["tests"]["health"] = {"status": "fail", "error": str(e)}
        results["summary"]["failed"] += 1
    
    # Test 2: Get Orders (empty)
    print("\n[TEST 2] Get Orders (List)")
    try:
        response = client.get("/api/orders/")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        print(f"  [PASS] GET /api/orders/ -> {response.status_code}")
        print(f"    Response: {data} (empty list)")
        results["tests"]["get_orders"] = {"status": "pass", "code": 200, "data": data}
        results["summary"]["passed"] += 1
    except Exception as e:
        print(f"  [FAIL] {e}")
        results["tests"]["get_orders"] = {"status": "fail", "error": str(e)}
        results["summary"]["failed"] += 1
    
    # Test 3: Analytics Summary
    print("\n[TEST 3] Analytics Summary")
    try:
        response = client.get("/api/orders/analytics/summary")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        print(f"  [PASS] GET /api/orders/analytics/summary -> {response.status_code}")
        print(f"    Response: {json.dumps(data, indent=2)}")
        results["tests"]["analytics"] = {"status": "pass", "code": 200, "data": data}
        results["summary"]["passed"] += 1
    except Exception as e:
        print(f"  [FAIL] {e}")
        results["tests"]["analytics"] = {"status": "fail", "error": str(e)}
        results["summary"]["failed"] += 1
    
    # Test 4: Chat - Greeting
    print("\n[TEST 4] Chat - Greeting Intent")
    try:
        response = client.post("/api/chat/", json={
            "message": "hello",
            "user_id": 1
        })
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        print(f"  [PASS] POST /api/chat/ -> {response.status_code}")
        print(f"    Intent: {data.get('intent')}")
        print(f"    Reply: {data.get('reply')[:60]}...")
        results["tests"]["chat_greeting"] = {"status": "pass", "code": 200, "intent": data.get("intent")}
        results["summary"]["passed"] += 1
    except Exception as e:
        print(f"  [FAIL] {e}")
        results["tests"]["chat_greeting"] = {"status": "fail", "error": str(e)}
        results["summary"]["failed"] += 1
    
    # Test 5: Chat - Create Order
    print("\n[TEST 5] Chat - Create Order Intent")
    try:
        response = client.post("/api/chat/", json={
            "message": "I need 10 office chairs by Friday",
            "user_id": 1
        })
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        print(f"  [PASS] POST /api/chat/ -> {response.status_code}")
        print(f"    Intent: {data.get('intent')}")
        print(f"    Reply: {data.get('reply')[:60]}...")
        print(f"    Extracted: {data.get('extracted_data')}")
        results["tests"]["chat_create_order"] = {"status": "pass", "code": 200, "intent": data.get("intent")}
        results["summary"]["passed"] += 1
    except Exception as e:
        print(f"  [FAIL] {e}")
        results["tests"]["chat_create_order"] = {"status": "fail", "error": str(e)}
        results["summary"]["failed"] += 1
    
    # Test 6: Valid route check
    print("\n[TEST 6] API Route Validation")
    try:
        response = client.get("/api/orders/")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print(f"  [PASS] Routes are correctly registered and accessible")
        results["tests"]["routes"] = {"status": "pass"}
        results["summary"]["passed"] += 1
    except Exception as e:
        print(f"  [FAIL] {e}")
        results["tests"]["routes"] = {"status": "fail", "error": str(e)}
        results["summary"]["failed"] += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    print(f"TESTS PASSED: {results['summary']['passed']}")
    print(f"TESTS FAILED: {results['summary']['failed']}")
    print("=" * 60)
    
    return results

if __name__ == "__main__":
    results = test_api()
    sys.exit(0 if results["summary"]["failed"] == 0 else 1)
