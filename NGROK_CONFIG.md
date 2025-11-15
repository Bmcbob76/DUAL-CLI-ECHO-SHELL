# NGROK CONFIGURATION - EXTERNAL ACCESS

**ECHO PRIME XV4 - Authority 11.0**

## 🎯 PURPOSE

Enable external Spark AI to connect to local bridge server through secure tunnel.

---

## 🔧 INSTALLATION

### **Download & Install Ngrok**

**Option 1: Direct Download**
```powershell
# Visit: https://ngrok.com/download
# Download Windows 64-bit
# Extract to: C:\Tools\ngrok\
```

**Option 2: Chocolatey**
```powershell
choco install ngrok
```

**Option 3: Scoop**
```powershell
scoop install ngrok
```

---

## 🔑 AUTHENTICATION

### **Get Ngrok Auth Token**
1. Create free account: https://dashboard.ngrok.com/signup
2. Get token: https://dashboard.ngrok.com/get-started/your-authtoken
3. Copy token (looks like: `2abc...xyz`)

### **Add Token to Ngrok**
```powershell
ngrok config add-authtoken YOUR_TOKEN_HERE
```

**Verify configuration:**
```powershell
# Config stored at: C:\Users\Bobby\.ngrok2\ngrok.yml
cat $env:USERPROFILE\.ngrok2\ngrok.yml
```

---

## 🚀 LAUNCH TUNNEL

### **Basic Tunnel (HTTP)**
```powershell
ngrok http 8765
```

**Output:**
```
ngrok                                                                                                           

Session Status                online
Account                       Bobby McWilliams (Plan: Free)
Version                       3.x.x
Region                        United States (us)
Latency                       25ms
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123xyz.ngrok-free.app -> http://localhost:8765

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

### **Copy HTTPS URL**
```
https://abc123xyz.ngrok-free.app
```

**This is your public endpoint for Spark!**

---

## 🔒 ADVANCED CONFIGURATION

### **Custom Domain (Paid Plans)**
```powershell
ngrok http 8765 --domain=echo-bridge.ngrok.app
```

### **Authentication (Basic)**
```powershell
ngrok http 8765 --basic-auth="username:password"
```

### **IP Restrictions (Paid)**
```powershell
ngrok http 8765 --cidr-allow=1.2.3.4/32
```

### **Config File Method**

**Edit:** `C:\Users\Bobby\.ngrok2\ngrok.yml`

```yaml
version: "2"
authtoken: YOUR_TOKEN_HERE

tunnels:
  echo-bridge:
    proto: http
    addr: 8765
    inspect: true
    bind_tls: true
    # auth: "user:pass"  # Optional
    # host_header: rewrite  # Optional
```

**Launch with config:**
```powershell
ngrok start echo-bridge
```

---

## 📊 MONITORING

### **Web Interface**
- Open: http://127.0.0.1:4040
- View: Real-time requests, responses, replay
- Inspect: Full HTTP traffic details

### **Command Line Status**
```powershell
# View in terminal while ngrok runs
# Shows connections, latency, throughput
```

---

## ✅ VERIFICATION

### **Test Public Endpoint**

**From external machine or phone:**
```bash
curl https://YOUR-NGROK-URL.ngrok-free.app/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-14T...",
  "copilot_available": true,
  "claude_available": true
}
```

### **Test Query from External**
```bash
curl -X POST https://YOUR-NGROK-URL.ngrok-free.app/api/both \
  -H "Content-Type: application/json" \
  -d '{"query":"test external access"}'
```

---

## 🚨 TROUBLESHOOTING

### **Tunnel Won't Start**
```powershell
# Check port 8765 is in use (bridge server running):
netstat -ano | findstr :8765

# Verify ngrok auth:
ngrok config check
```

### **502 Bad Gateway**
- Bridge server not running
- Check: http://localhost:8765/health first

### **Rate Limits (Free Plan)**
- 40 connections/minute limit
- Upgrade to paid for unlimited

### **Tunnel Keeps Disconnecting**
- Free plan tunnels reset every 2 hours
- Use paid plan for persistent tunnels
- Or restart ngrok automatically

---

## 💰 FREE VS PAID

### **Free Plan**
- ✅ 1 online ngrok process
- ✅ 4 tunnels/ngrok process  
- ✅ 40 connections/minute
- ❌ Random URLs (changes each restart)
- ❌ No custom domains
- ❌ No IP restrictions

### **Personal Plan ($8/month)**
- ✅ 3 reserved domains
- ✅ 500+ connections/minute
- ✅ IP restrictions
- ✅ Persistent tunnels

---

## 🎯 PRODUCTION RECOMMENDATIONS

**For Spark integration:**
1. ✅ Use paid plan for stability
2. ✅ Reserve custom domain
3. ✅ Enable basic auth
4. ✅ Monitor via web interface
5. ✅ Set up auto-restart script
6. ✅ Log all access attempts

**Auto-restart script:** `launch_bridge_with_ngrok.bat`
```batch
@echo off
:loop
start "Bridge Server" H:\Tools\python.exe P:\ECHO_PRIME\CLI_BRIDGE_INTEGRATION\ai_bridge_server.py
timeout /t 5
start "Ngrok Tunnel" ngrok http 8765
echo Servers launched - press Ctrl+C to stop
pause
goto loop
```

---

**🎖️ NGROK READY - PROCEED TO SPARK_INTEGRATION.md**
