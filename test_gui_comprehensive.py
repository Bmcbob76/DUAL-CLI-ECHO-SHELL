# CLI BRIDGE GUI - COMPREHENSIVE TEST SUITE
# Tests ALL functions, buttons, tabs, and features

import requests
import json
import time

BASE_URL = "http://localhost:8766"
BRIDGE_URL = "http://localhost:8765"

def test_header(test_name):
    print(f"\n{'='*70}")
    print(f"🧪 TEST: {test_name}")
    print('='*70)

def test_result(passed, message):
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status}: {message}")
    return passed

# ===================================================================
# TEST 1: SERVER HEALTH CHECKS
# ===================================================================
def test_servers_health():
    test_header("Server Health Checks")
    
    # Test GUI Backend
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        gui_healthy = test_result(
            response.status_code == 200,
            f"GUI Backend: {response.json()}"
        )
    except Exception as e:
        gui_healthy = test_result(False, f"GUI Backend ERROR: {e}")
    
    # Test CLI Bridge
    try:
        response = requests.get(f"{BRIDGE_URL}/health", timeout=5)
        bridge_data = response.json()
        bridge_healthy = test_result(
            response.status_code == 200,
            f"CLI Bridge: Copilot={bridge_data.get('copilot_available')}, Claude={bridge_data.get('claude_available')}"
        )
    except Exception as e:
        bridge_healthy = test_result(False, f"CLI Bridge ERROR: {e}")
    
    return gui_healthy and bridge_healthy

# ===================================================================
# TEST 2: WINDOWS EXPLORER INTEGRATION
# ===================================================================
def test_windows_explorer():
    test_header("Windows Explorer Integration")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/system/explorer",
            json={"path": "P:\\ECHO_PRIME"},
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            return test_result(
                data.get('success') == True,
                f"Windows Explorer opened: {data.get('message')}"
            )
        else:
            return test_result(False, f"Status Code: {response.status_code}, Body: {response.text}")
            
    except Exception as e:
        return test_result(False, f"ERROR: {e}")

# ===================================================================
# TEST 3: FILE OPERATIONS
# ===================================================================
def test_file_operations():
    test_header("File Operations")
    
    # Test list files
    try:
        response = requests.post(
            f"{BASE_URL}/api/files/list",
            json={"path": "P:\\ECHO_PRIME"},
            timeout=5
        )
        list_passed = test_result(
            response.status_code == 200 and response.json().get('success'),
            f"List files: {len(response.json().get('items', []))} items found"
        )
    except Exception as e:
        list_passed = test_result(False, f"List files ERROR: {e}")
    
    # Test read file
    try:
        response = requests.post(
            f"{BASE_URL}/api/files/read",
            json={"path": "P:\\ECHO_PRIME\\CLI_BRIDGE_INTEGRATION\\README.md"},
            timeout=5
        )
        read_data = response.json()
        read_passed = test_result(
            response.status_code == 200 and read_data.get('success'),
            f"Read file: {read_data.get('size', 0)} bytes"
        )
    except Exception as e:
        read_passed = test_result(False, f"Read file ERROR: {e}")
    
    return list_passed and read_passed

# ===================================================================
# TEST 4: AI BRIDGE ENDPOINTS
# ===================================================================
def test_ai_bridge():
    test_header("AI Bridge Endpoints")
    
    # Test Copilot endpoint
    try:
        response = requests.post(
            f"{BRIDGE_URL}/api/copilot",
            json={"query": "print hello world in python"},
            timeout=30
        )
        copilot_data = response.json()
        copilot_passed = test_result(
            response.status_code == 200 and copilot_data.get('success'),
            f"Copilot query: {copilot_data.get('duration_ms')}ms"
        )
    except Exception as e:
        copilot_passed = test_result(False, f"Copilot ERROR: {e}")
    
    # Test Claude endpoint
    try:
        response = requests.post(
            f"{BRIDGE_URL}/api/claude",
            json={"query": "explain bubble sort"},
            timeout=30
        )
        claude_data = response.json()
        claude_passed = test_result(
            response.status_code == 200 and claude_data.get('success'),
            f"Claude query: {claude_data.get('duration_ms')}ms"
        )
    except Exception as e:
        claude_passed = test_result(False, f"Claude ERROR: {e}")
    
    # Test parallel query
    try:
        response = requests.post(
            f"{BRIDGE_URL}/api/both",
            json={"query": "fibonacci sequence"},
            timeout=60
        )
        both_data = response.json()
        both_passed = test_result(
            response.status_code == 200 and both_data.get('success'),
            f"Parallel query: {both_data.get('duration_ms')}ms (Copilot + Claude)"
        )
    except Exception as e:
        both_passed = test_result(False, f"Parallel query ERROR: {e}")
    
    return copilot_passed and claude_passed and both_passed

# ===================================================================
# TEST 5: SYSTEM METRICS
# ===================================================================
def test_metrics():
    test_header("System Metrics")
    
    try:
        response = requests.get(f"{BRIDGE_URL}/api/metrics", timeout=5)
        metrics = response.json()
        
        if response.status_code == 200:
            system_metrics = metrics.get('metrics', {})
            platform_info = metrics.get('platform', {})
            
            print(f"  CPU: {system_metrics.get('cpu_percent')}%")
            print(f"  Memory: {system_metrics.get('memory_percent')}%")
            print(f"  Platform: {platform_info.get('system')} {platform_info.get('release')}")
            print(f"  Request Log: {metrics.get('request_log_size')} entries")
            
            return test_result(True, "Metrics retrieved successfully")
        else:
            return test_result(False, f"Status Code: {response.status_code}")
            
    except Exception as e:
        return test_result(False, f"ERROR: {e}")

# ===================================================================
# TEST 6: LOGS ENDPOINT
# ===================================================================
def test_logs():
    test_header("Request Logs")
    
    try:
        response = requests.get(f"{BRIDGE_URL}/api/logs?limit=10", timeout=5)
        logs_data = response.json()
        
        if response.status_code == 200:
            logs = logs_data.get('logs', [])
            print(f"  Total Requests: {logs_data.get('total_requests')}")
            print(f"  Recent Logs: {len(logs)}")
            
            return test_result(True, f"Retrieved {len(logs)} log entries")
        else:
            return test_result(False, f"Status Code: {response.status_code}")
            
    except Exception as e:
        return test_result(False, f"ERROR: {e}")

# ===================================================================
# MAIN TEST RUNNER
# ===================================================================
def run_all_tests():
    print("\n" + "="*70)
    print("🎖️ ECHO PRIME - COMPREHENSIVE GUI TEST SUITE")
    print("="*70)
    print(f"Test Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"GUI Backend: {BASE_URL}")
    print(f"CLI Bridge: {BRIDGE_URL}")
    print("="*70)
    
    results = []
    
    # Run all tests
    results.append(("Servers Health", test_servers_health()))
    results.append(("Windows Explorer", test_windows_explorer()))
    results.append(("File Operations", test_file_operations()))
    results.append(("AI Bridge", test_ai_bridge()))
    results.append(("System Metrics", test_metrics()))
    results.append(("Request Logs", test_logs()))
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("="*70)
    print(f"TOTAL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("="*70)
    
    if passed == total:
        print("\n🎖️ ALL TESTS PASSED - SYSTEM FULLY OPERATIONAL")
    else:
        print(f"\n⚠️ {total - passed} TEST(S) FAILED - REVIEW REQUIRED")
    
    print("\n")

if __name__ == "__main__":
    run_all_tests()
