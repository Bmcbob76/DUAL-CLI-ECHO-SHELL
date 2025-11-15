# EXTERNAL ACCESS - NGROK SETUP

**ECHO PRIME - Authority 11.0**

## 🎯 ENABLE REMOTE ACCESS

Allow external access to GUI + CLI Bridge via ngrok tunnel.

---

## 📥 INSTALL NGROK

**Option 1: Direct Download**
```powershell
# Visit: https://ngrok.com/download
# Extract to: C:\Tools\ngrok\
# Add to PATH
```

**Option 2: Chocolatey**
```powershell
choco install ngrok
```

---

## 🔑 AUTHENTICATE

**Get Token:**
1. Sign up: https://dashboard.ngrok.com/signup
2. Get token: https://dashboard.ngrok.com/get-started/your-authtoken

**Add Token:**
```powershell
ngrok config add-authtoken YOUR_TOKEN_HERE
```

---

## 🚀 LAUNCH TUNNELS

### **Method 1: Single Command (Recommended)**
```powershell
ngrok http 8766
```

**Result:**
- GUI accessible: `https://xyz123.ngrok-free.app`
- CLI Bridge accessible: `https://xyz123.ngrok-free.app` (proxied through GUI)

---

### **Method 2: Multiple Tunnels**

**Terminal 1 - GUI Tunnel:**
```powershell
ngrok http 8766 --subdomain=echo-gui
```

**Terminal 2 - CLI Bridge Tunnel:**
```powershell
ngrok http 8765 --subdomain=echo-cli
```

**Result:**
- GUI: `https://echo-gui.ngrok.io`
- CLI Bridge: `https://echo-cli.ngrok.io`

---

## ✅ VERIFY EXTERNAL ACCESS

**From external device (phone, different network):**

**Health Check:**
```bash
curl https://YOUR-NGROK-URL.ngrok-free.app/health
```

**Expected:**
```json
{
  "status": "healthy",
  "service": "GUI_BACKEND",
  "cli_bridge": "http://localhost:8765",
  "mcp_servers": 14
}
```

**Access GUI:**
```
https://YOUR-NGROK-URL.ngrok-free.app
```

Opens full ECHO PRIME interface, accessible from anywhere.

---

## 🔒 SECURITY CONSIDERATIONS

**Current Setup:**
- ❌ No authentication
- ❌ Anyone with URL can access
- ❌ Full file system exposed

**Production Hardening:**

### **Add Basic Auth (Ngrok)**
```powershell
ngrok http 8766 --basic-auth="commander:secret123"
```

### **Add IP Whitelist (Paid Plans)**
```powershell
ngrok http 8766 --cidr-allow="1.2.3.4/32"
```

### **Add API Key (Application Level)**

**Edit `gui_server.py`:**
```python
API_KEYS = ['echo_prime_key_123']

@app.before_request
def check_auth():
    if request.path.startswith('/api/'):
        key = request.headers.get('X-API-Key')
        if key not in API_KEYS:
            return jsonify({'error': 'Unauthorized'}), 401
```

**Client Usage:**
```javascript
fetch('https://ngrok-url/api/files/list', {
    headers: {
        'X-API-Key': 'echo_prime_key_123',
        'Content-Type': 'application/json'
    },
    // ...
})
```

---

## 📊 MONITORING

### **Ngrok Web Interface**
```
http://localhost:4040
```

**Features:**
- Real-time requests
- Response inspection
- Request replay
- Traffic logs

### **Application Logs**

**GUI Backend:**
```powershell
# Console output shows all requests
```

**CLI Bridge:**
```powershell
type P:\ECHO_PRIME\CLI_BRIDGE_INTEGRATION\debug.log
```

---

## 🌐 SPARK INTEGRATION

**With ngrok tunnel active:**

1. Get public URL: `https://xyz123.ngrok-free.app`
2. Configure Spark to use URL
3. Spark can now:
   - Access full GUI
   - Query CLI bridge
   - Execute on your CPU
   - Browse your files
   - Use MCP servers

**Spark Request Example:**
```http
POST https://xyz123.ngrok-free.app/api/execute
Content-Type: application/json

{
  "command": "dir P:\\ECHO_PRIME"
}
```

**Response:**
```json
{
  "success": true,
  "stdout": "Directory listing...",
  "exit_code": 0
}
```

---

## 💰 NGROK PLANS

**Free:**
- ✅ 1 online process
- ✅ 4 tunnels/process
- ✅ 40 connections/min
- ❌ Random URLs
- ❌ No custom domains

**Personal ($8/mo):**
- ✅ 3 reserved domains
- ✅ 500+ connections/min
- ✅ IP restrictions
- ✅ Persistent tunnels

---

## 🚨 TROUBLESHOOTING

**Tunnel Won't Start:**
```powershell
# Verify servers running:
netstat -ano | findstr :8765
netstat -ano | findstr :8766

# Check ngrok config:
ngrok config check
```

**502 Bad Gateway:**
- Servers not running
- Check: http://localhost:8766

**Rate Limits:**
- Free plan: 40 req/min
- Upgrade to paid

---

## 🎯 PRODUCTION DEPLOYMENT

**Recommended Setup:**

1. **Paid ngrok plan** - Reserved domain
2. **Basic auth** - Username/password
3. **API keys** - Application-level security
4. **HTTPS only** - Enforce encryption
5. **Monitoring** - Log all access
6. **Backups** - Regular system backups
7. **Updates** - Keep dependencies current

**Auto-restart Script:** `launch_with_ngrok.bat`
```batch
@echo off
:loop
start "Servers" P:\ECHO_PRIME\CLI_BRIDGE_INTEGRATION\LAUNCH_ALL.bat
timeout /t 5
start "Ngrok" ngrok http 8766 --basic-auth="commander:secret"
pause
goto loop
```

---

**🎖️ EXTERNAL ACCESS CONFIGURED**
**SPARK CAN NOW CONTROL YOUR CPU FROM ANYWHERE**
