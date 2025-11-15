# TEST PROCEDURES - CLI BRIDGE

**ECHO PRIME XV4 - Authority 11.0**

## ⚡ PRE-FLIGHT CHECKLIST

**Before testing, verify:**
- [ ] GitHub CLI installed and authenticated
- [ ] Copilot extension active
- [ ] Claude Code CLI installed and authenticated
- [ ] Python dependencies installed
- [ ] Bridge server file present at `P:\ECHO_PRIME\CLI_BRIDGE_INTEGRATION\ai_bridge_server.py`

---

## 🧪 TEST SEQUENCE

### **TEST 1: Server Launch**

```powershell
cd P:\ECHO_PRIME\CLI_BRIDGE_INTEGRATION
H:\Tools\python.exe ai_bridge_server.py
```

**Expected Output:**
```
======================================================================
🌉 ECHO PRIME - AI BRIDGE SERVER
======================================================================

🖥️  Platform: Windows ...
🐍 Python: 3.x.x

📡 Bridge Server: http://localhost:8765
✅ GitHub Copilot CLI: Available
✅ Claude Code CLI: Available

💾 CPU Access: FULL
📊 System Metrics: XX% CPU, XX% RAM

🔗 For Spark to connect externally, use ngrok:
   ngrok http 8765

📋 Endpoints:
   GET  /health         - Server status
   POST /api/copilot    - GitHub Copilot query
   POST /api/claude     - Claude Code query
   POST /api/both       - Parallel query both
   GET  /api/metrics    - System metrics
   GET  /api/logs       - Request logs

🚀 Server starting...
======================================================================

 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8765
 * Running on http://192.168.x.x:8765
```

**✅ PASS:** Server starts without errors
**❌ FAIL:** Check troubleshooting section

---

### **TEST 2: Health Check**

**In new PowerShell terminal:**
```powershell
curl http://localhost:8765/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-14T...",
  "copilot_available": true,
  "claude_available": true,
  "metrics": {
    "cpu_percent": 15.3,
    "memory_percent": 42.7,
    "last_update": "2025-11-14T..."
  }
}
```

**✅ PASS:** Returns healthy status with both CLIs available
**⚠️ PARTIAL:** One CLI unavailable (proceed with caution)
**❌ FAIL:** Server not responding

---

### **TEST 3: Copilot Query**

```powershell
curl -X POST http://localhost:8765/api/copilot `
  -H "Content-Type: application/json" `
  -d '{"query":"Write Python function to calculate factorial"}'
```

**Expected Response:**
```json
{
  "success": true,
  "provider": "GitHub Copilot",
  "response": "def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n-1)",
  "duration_ms": 234,
  "timestamp": "2025-11-14T..."
}
```

**✅ PASS:** Returns code suggestion from Copilot
**❌ FAIL:** Check Copilot authentication

---

### **TEST 4: Claude Query**

```powershell
curl -X POST http://localhost:8765/api/claude `
  -H "Content-Type: application/json" `
  -d '{"query":"explain bubble sort algorithm"}'
```

**Expected Response:**
```json
{
  "success": true,
  "provider": "Claude Code",
  "response": "Bubble sort is a simple sorting algorithm...",
  "duration_ms": 456,
  "timestamp": "2025-11-14T..."
}
```

**✅ PASS:** Returns response from Claude Code
**❌ FAIL:** Check Claude Code authentication

---

### **TEST 5: Parallel Query**

```powershell
curl -X POST http://localhost:8765/api/both `
  -H "Content-Type: application/json" `
  -d '{"query":"create Python class for binary search tree"}'
```

**Expected Response:**
```json
{
  "success": true,
  "copilot": {
    "provider": "GitHub Copilot",
    "success": true,
    "response": "class BSTNode:...",
    "exit_code": 0
  },
  "claude": {
    "provider": "Claude Code",
    "success": true,
    "response": "class BinarySearchTree:...",
    "exit_code": 0
  },
  "duration_ms": 523,
  "timestamp": "2025-11-14T..."
}
```

**✅ PASS:** Both AIs respond successfully
**⚠️ PARTIAL:** One AI fails (check individual endpoints)
**❌ FAIL:** Both fail or server error

---

### **TEST 6: System Metrics**

```powershell
curl http://localhost:8765/api/metrics
```

**Expected Response:**
```json
{
  "success": true,
  "metrics": {
    "cpu_percent": 12.5,
    "memory_percent": 38.2,
    "last_update": "2025-11-14T..."
  },
  "platform": {
    "system": "Windows",
    "release": "10",
    "version": "...",
    "machine": "AMD64",
    "processor": "..."
  },
  "request_log_size": 5
}
```

**✅ PASS:** Returns system metrics
**❌ FAIL:** Server error

---

### **TEST 7: Request Logs**

```powershell
curl "http://localhost:8765/api/logs?limit=10"
```

**Expected Response:**
```json
{
  "success": true,
  "logs": [
    {
      "timestamp": "2025-11-14T...",
      "provider": "copilot",
      "query": "Write Python function...",
      "duration_ms": 234,
      "success": true,
      "error": null
    }
  ],
  "total_requests": 10
}
```

**✅ PASS:** Returns request history
**❌ FAIL:** Server error

---

## 🎯 PERFORMANCE BENCHMARKS

**Target metrics for optimal operation:**

| Metric | Target | Acceptable | Warning |
|--------|--------|------------|---------|
| Server response time | <50ms | <100ms | >100ms |
| Copilot response | 200-500ms | <1000ms | >1000ms |
| Claude response | 300-800ms | <1500ms | >1500ms |
| Parallel query | ~max(both) | <2000ms | >2000ms |
| CPU usage (idle) | <5% | <10% | >10% |
| Memory usage | <200MB | <500MB | >500MB |

**Run performance test:**
```powershell
# Send 10 queries and measure:
for ($i=1; $i -le 10; $i++) {
    Measure-Command {
        curl -X POST http://localhost:8765/api/both `
          -H "Content-Type: application/json" `
          -d "{`"query`":`"test query $i`"}" | Out-Null
    }
}
```

---

## 🚨 TROUBLESHOOTING

### **Server Won't Start**
```powershell
# Check port availability:
netstat -ano | findstr :8765

# Kill conflicting process:
taskkill /F /PID <PID>

# Verify Python:
H:\Tools\python.exe --version

# Reinstall dependencies:
H:\Tools\python.exe -m pip install --force-reinstall flask flask-cors psutil --break-system-packages
```

### **Copilot Not Available**
```powershell
gh auth status
gh copilot --version
gh extension install github/gh-copilot
```

### **Claude Not Available**
```powershell
claude-code --version
claude-code auth
```

### **Timeout Errors**
- Increase timeout in ai_bridge_server.py (line 82, 104)
- Check internet connection
- Verify CLI authentication

---

## ✅ ACCEPTANCE CRITERIA

**All tests must pass for production deployment:**
- [x] Server starts without errors
- [x] Health check returns healthy
- [x] Copilot query succeeds
- [x] Claude query succeeds
- [x] Parallel query returns both responses
- [x] Metrics endpoint functional
- [x] Logs endpoint functional
- [x] Performance within acceptable range

---

**🎖️ TESTING COMPLETE - PROCEED TO SPARK INTEGRATION**
