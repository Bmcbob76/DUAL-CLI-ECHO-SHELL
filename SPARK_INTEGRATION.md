# SPARK INTEGRATION - EXTERNAL AI CONNECTION

**ECHO PRIME XV4 - Authority 11.0**

## 🎯 OVERVIEW

Connect Spark AI to ECHO PRIME bridge for parallel Copilot + Claude Code queries with full CPU access.

---

## 🏗️ CONNECTION ARCHITECTURE

```
┌─────────────────────────────────────┐
│         SPARK AI (External)         │
│    Anthropic Cloud / OpenRouter     │
└────────────────┬────────────────────┘
                 │ HTTPS
                 ▼
┌─────────────────────────────────────┐
│      NGROK TUNNEL (Public URL)      │
│  https://abc123.ngrok-free.app      │
└────────────────┬────────────────────┘
                 │ localhost:8765
                 ▼
┌─────────────────────────────────────┐
│      AI BRIDGE SERVER (Local)       │
│      Commander's CPU - FULL ACCESS  │
└────────────────┬────────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
┌──────────────┐   ┌──────────────┐
│   Copilot    │   │  Claude Code │
└──────────────┘   └──────────────┘
```

---

## 🔌 SPARK CONFIGURATION

### **Endpoint Setup**

**Base URL:** `https://YOUR-NGROK-URL.ngrok-free.app`

**Available Endpoints:**
```
GET  /health              - Bridge health check
POST /api/copilot         - Query GitHub Copilot only
POST /api/claude          - Query Claude Code only
POST /api/both            - Query both in parallel (RECOMMENDED)
GET  /api/metrics         - System metrics
GET  /api/logs?limit=N    - Recent request logs
```

### **Request Format**

**Headers:**
```json
{
  "Content-Type": "application/json"
}
```

**Body:**
```json
{
  "query": "Your coding question or task here"
}
```

### **Response Format**

**Parallel Query Response (/api/both):**
```json
{
  "success": true,
  "copilot": {
    "provider": "GitHub Copilot",
    "success": true,
    "response": "...",
    "exit_code": 0
  },
  "claude": {
    "provider": "Claude Code",
    "success": true,
    "response": "...",
    "exit_code": 0
  },
  "duration_ms": 523,
  "timestamp": "2025-11-14T12:34:56.789012"
}
```

---

## 🚀 SPARK PROMPT EXAMPLES

### **Example 1: Code Generation**

**Spark sends:**
```
Generate a Python function to validate email addresses using regex
```

**Bridge translates to:**
```json
POST /api/both
{
  "query": "Generate a Python function to validate email addresses using regex"
}
```

**Spark receives:**
- Copilot's implementation
- Claude's implementation  
- Can compare approaches
- Merge best features

---

### **Example 2: Debugging**

**Spark sends:**
```
This Python code has a memory leak in the cache manager. Find and fix it:
[code here]
```

**Bridge response:**
- Copilot identifies leak location
- Claude suggests fix + explanation
- Both responses available for analysis

---

### **Example 3: Code Review**

**Spark sends:**
```
Review this authentication middleware for security vulnerabilities:
[code here]
```

**Bridge response:**
- Copilot security analysis
- Claude security recommendations
- Comprehensive coverage from multiple perspectives

---

## 💡 SPARK INTEGRATION PATTERNS

### **Pattern 1: Best-of-Both**
```python
def spark_query(prompt):
    response = bridge.post('/api/both', {'query': prompt})
    
    # Compare responses
    copilot_score = evaluate(response['copilot']['response'])
    claude_score = evaluate(response['claude']['response'])
    
    # Return best
    return max(copilot_score, claude_score)
```

### **Pattern 2: Consensus Building**
```python
def spark_consensus(prompt):
    response = bridge.post('/api/both', {'query': prompt})
    
    # Find common elements
    copilot_ideas = extract_concepts(response['copilot'])
    claude_ideas = extract_concepts(response['claude'])
    
    # Build consensus
    return merge_approaches(copilot_ideas, claude_ideas)
```

### **Pattern 3: Fallback Strategy**
```python
def spark_robust(prompt):
    response = bridge.post('/api/both', {'query': prompt})
    
    # Try primary (Claude)
    if response['claude']['success']:
        return response['claude']['response']
    
    # Fallback to Copilot
    if response['copilot']['success']:
        return response['copilot']['response']
    
    # Both failed
    return handle_failure(response)
```

---

## 🔒 SECURITY CONSIDERATIONS

### **Current Setup (Development)**
- ✅ HTTPS via ngrok (encrypted)
- ❌ No authentication (add token validation)
- ❌ No rate limiting (implement in production)
- ✅ Request logging enabled

### **Production Hardening**

**Add to ai_bridge_server.py:**
```python
# Token validation
VALID_TOKENS = ['spark_secret_token_here']

@app.before_request
def validate_token():
    token = request.headers.get('X-API-Token')
    if token not in VALID_TOKENS:
        return jsonify({'error': 'Unauthorized'}), 401
```

**Spark configuration:**
```python
headers = {
    'Content-Type': 'application/json',
    'X-API-Token': 'spark_secret_token_here'
}
```

---

## 📊 MONITORING & ANALYTICS

### **Check Bridge Health**
```python
health = bridge.get('/health')
print(f"Copilot: {health['copilot_available']}")
print(f"Claude: {health['claude_available']}")
print(f"CPU: {health['metrics']['cpu_percent']}%")
```

### **Query Metrics**
```python
metrics = bridge.get('/api/metrics')
print(f"Platform: {metrics['platform']['system']}")
print(f"Total requests: {metrics['request_log_size']}")
```

### **View Request History**
```python
logs = bridge.get('/api/logs?limit=50')
for entry in logs['logs']:
    print(f"{entry['timestamp']}: {entry['provider']} - {entry['duration_ms']}ms")
```

---

## ⚡ PERFORMANCE OPTIMIZATION

### **Spark-Side Caching**
```python
cache = {}

def spark_cached_query(prompt):
    if prompt in cache:
        return cache[prompt]
    
    response = bridge.post('/api/both', {'query': prompt})
    cache[prompt] = response
    return response
```

### **Timeout Handling**
```python
import requests

def spark_query_with_timeout(prompt, timeout=30):
    try:
        response = requests.post(
            f'{BRIDGE_URL}/api/both',
            json={'query': prompt},
            timeout=timeout
        )
        return response.json()
    except requests.Timeout:
        return {'error': 'Query timeout', 'success': False}
```

---

## 🎯 EXAMPLE SPARK INTEGRATION

**Complete Spark → Bridge → CPU workflow:**

```python
import requests

class EchoBridge:
    def __init__(self, ngrok_url):
        self.base_url = ngrok_url
        self.token = 'spark_secret_token'  # Optional
    
    def health(self):
        """Check bridge health"""
        return requests.get(f'{self.base_url}/health').json()
    
    def query_both(self, prompt):
        """Query both Copilot and Claude"""
        return requests.post(
            f'{self.base_url}/api/both',
            json={'query': prompt},
            headers={'X-API-Token': self.token}
        ).json()
    
    def query_copilot(self, prompt):
        """Query Copilot only"""
        return requests.post(
            f'{self.base_url}/api/copilot',
            json={'query': prompt}
        ).json()
    
    def query_claude(self, prompt):
        """Query Claude only"""
        return requests.post(
            f'{self.base_url}/api/claude',
            json={'query': prompt}
        ).json()

# Usage in Spark
bridge = EchoBridge('https://abc123.ngrok-free.app')

# Check status
if bridge.health()['status'] == 'healthy':
    # Query both AIs
    result = bridge.query_both("Create Python class for blockchain")
    
    print(f"Copilot: {result['copilot']['response']}")
    print(f"Claude: {result['claude']['response']}")
```

---

**🎖️ SPARK INTEGRATION COMPLETE - FULL CPU ACCESS OPERATIONAL**
