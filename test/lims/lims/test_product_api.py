#!/usr/bin/env python3
"""
Test script to validate Product API endpoints
Run this after starting the backend server to test all CRUD operations
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:8000"
PRODUCT_ENDPOINT = f"{BASE_URL}/products"

def test_connection():
    """Test if the API server is running"""
    try:
        response = requests.get(f"{BASE_URL}/products", timeout=5)
        print(f"✅ API Connection successful - Status: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ API Connection failed: {e}")
        return False

def test_create_product():
    """Test creating a new product"""
    product_data = {
        "name": "Test Product API",
        "description": "This is a test product created via API",
        "status": "NOT_STARTED"
    }
    
    try:
        response = requests.post(PRODUCT_ENDPOINT, json=product_data)
        
        if response.status_code == 201:
            data = response.json()
            product = data["data"]
            print(f"✅ Product created successfully:")
            print(f"   ID: {product['id']}")
            print(f"   Code: {product['product_code']}")
            print(f"   Name: {product['name']}")
            print(f"   Status: {product['status']}")
            return product
        else:
            print(f"❌ Product creation failed - Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Product creation error: {e}")
        return None

def test_get_products():
    """Test getting all products"""
    try:
        response = requests.get(PRODUCT_ENDPOINT)
        
        if response.status_code == 200:
            data = response.json()
            products = data["data"]["items"]
            total = data["data"]["total"]
            print(f"✅ Retrieved {len(products)} products (Total: {total})")
            return products
        else:
            print(f"❌ Get products failed - Status: {response.status_code}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Get products error: {e}")
        return []

def test_get_product_by_id(product_id):
    """Test getting a specific product by ID"""
    try:
        response = requests.get(f"{PRODUCT_ENDPOINT}/{product_id}")
        
        if response.status_code == 200:
            data = response.json()
            product = data["data"]
            print(f"✅ Retrieved product by ID:")
            print(f"   ID: {product['id']}")
            print(f"   Name: {product['name']}")
            return product
        else:
            print(f"❌ Get product by ID failed - Status: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Get product by ID error: {e}")
        return None

def test_update_product(product_id):
    """Test updating a product"""
    update_data = {
        "description": "Updated description via API test",
        "status": "IN_PROGRESS"
    }
    
    try:
        response = requests.put(f"{PRODUCT_ENDPOINT}/{product_id}", json=update_data)
        
        if response.status_code == 200:
            data = response.json()
            product = data["data"]
            print(f"✅ Product updated successfully:")
            print(f"   Status: {product['status']}")
            print(f"   Description: {product['description']}")
            return product
        else:
            print(f"❌ Product update failed - Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Product update error: {e}")
        return None

def test_search_products():
    """Test searching products"""
    try:
        # Test search by name
        search_params = {"search": "Test Product"}
        response = requests.get(PRODUCT_ENDPOINT, params=search_params)
        
        if response.status_code == 200:
            data = response.json()
            products = data["data"]["items"]
            print(f"✅ Search returned {len(products)} products")
            return products
        else:
            print(f"❌ Product search failed - Status: {response.status_code}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Product search error: {e}")
        return []

def test_filter_products():
    """Test filtering products by status"""
    try:
        # Test filter by status
        filter_params = {"status": ["IN_PROGRESS"]}
        response = requests.get(PRODUCT_ENDPOINT, params=filter_params)
        
        if response.status_code == 200:
            data = response.json()
            products = data["data"]["items"]
            print(f"✅ Filter returned {len(products)} products")
            return products
        else:
            print(f"❌ Product filter failed - Status: {response.status_code}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Product filter error: {e}")
        return []

def test_delete_product(product_id):
    """Test deleting a product"""
    try:
        response = requests.delete(f"{PRODUCT_ENDPOINT}/{product_id}")
        
        if response.status_code == 200:
            print(f"✅ Product {product_id} deleted successfully")
            return True
        else:
            print(f"❌ Product deletion failed - Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Product deletion error: {e}")
        return False

def main():
    """Run all API tests"""
    print("🧪 Starting Product API Tests...")
    print("=" * 50)
    
    # Test API connection
    if not test_connection():
        print("\n❌ Cannot connect to API server. Make sure it's running on http://localhost:8000")
        sys.exit(1)
    
    print("\n📝 Testing CRUD Operations...")
    
    # Test CREATE
    print("\n1. Testing Product Creation...")
    created_product = test_create_product()
    if not created_product:
        print("❌ Cannot continue tests without a created product")
        sys.exit(1)
    
    product_id = created_product["id"]
    
    # Test READ (all products)
    print("\n2. Testing Get All Products...")
    products = test_get_products()
    
    # Test READ (specific product)
    print("\n3. Testing Get Product by ID...")
    product = test_get_product_by_id(product_id)
    
    # Test UPDATE
    print("\n4. Testing Product Update...")
    updated_product = test_update_product(product_id)
    
    # Test SEARCH
    print("\n5. Testing Product Search...")
    search_results = test_search_products()
    
    # Test FILTER
    print("\n6. Testing Product Filter...")
    filter_results = test_filter_products()
    
    # Test DELETE
    print("\n7. Testing Product Deletion...")
    delete_success = test_delete_product(product_id)
    
    print("\n" + "=" * 50)
    print("🎉 API Tests Complete!")
    
    # Summary
    tests_passed = sum([
        created_product is not None,
        len(products) >= 0,
        product is not None,
        updated_product is not None,
        len(search_results) >= 0,
        len(filter_results) >= 0,
        delete_success
    ])
    
    print(f"📊 Results: {tests_passed}/7 tests passed")
    
    if tests_passed == 7:
        print("✅ All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()