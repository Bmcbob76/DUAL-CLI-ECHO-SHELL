# INSTALLATION GUIDE - CLI BRIDGE

**Commander Bobby Don McWilliams II - Authority 11.0**

## ⚡ PREREQUISITES

### **System Requirements**
- Windows 10/11
- Python 3.8+ (using `H:\Tools\python.exe`)
- Internet connection
- Git installed

---

## 🔧 STEP 1: GITHUB CLI + COPILOT

### **Install GitHub CLI**
```powershell
# Download and install from:
# https://cli.github.com/

# Or use winget:
winget install --id GitHub.cli

# Verify installation:
gh --version
```

### **Authenticate GitHub CLI**
```powershell
gh auth login
# Follow prompts:
# - GitHub.com
# - HTTPS
# - Login with browser
# - Complete authentication
```

### **Install Copilot Extension**
```powershell
gh extension install github/gh-copilot

# Verify:
gh copilot --version
```

### **Test Copilot**
```powershell
gh copilot suggest "Write Python hello world"
gh copilot explain "def foo(x): return x**2"
```

---

## 🔧 STEP 2: CLAUDE CODE CLI

### **Option A: NPM Install (Recommended)**
```powershell
npm install -g @anthropic-ai/claude-code

# Verify:
claude-code --version
```

### **Option B: Direct Download**
- Visit: https://github.com/anthropics/claude-code
- Download latest release
- Add to PATH

### **Authenticate Claude Code**
```powershell
claude-code auth

# Enter Anthropic API key when prompted
# Get key from: https://console.anthropic.com/
```

### **Test Claude Code**
```powershell
claude-code --help
claude-code execute "print hello world in python"
```

---

## 🔧 STEP 3: PYTHON DEPENDENCIES

### **Install Flask + psutil**
```powershell
H:\Tools\python.exe -m pip install flask flask-cors psutil --break-system-packages
```

### **Verify Installation**
```powershell
H:\Tools\python.exe -c "import flask; import psutil; print('OK')"
```

---

## 🔧 STEP 4: DEPLOY BRIDGE SERVER

### **Copy Server File**
```powershell
# File already at:
P:\ECHO_PRIME\CLI_BRIDGE_INTEGRATION\ai_bridge_server.py
```

### **Launch Server**
```powershell
cd P:\ECHO_PRIME\CLI_BRIDGE_INTEGRATION
H:\Tools\python.exe ai_bridge_server.py
```

### **Verify Server Running**
```powershell
# In new terminal:
curl http://localhost:8765/health

# Expected response:
# {"status":"healthy","timestamp":"..."}
```

---

## 🔧 STEP 5: NGROK EXTERNAL ACCESS (Optional)

### **Install Ngrok**
```powershell
# Download from: https://ngrok.com/download
# Or use:
choco install ngrok
```

### **Authenticate Ngrok**
```powershell
ngrok config add-authtoken YOUR_TOKEN_HERE
# Get token from: https://dashboard.ngrok.com/
```

### **Launch Ngrok Tunnel**
```powershell
# In separate terminal:
ngrok http 8765

# Copy the HTTPS URL (looks like):
# https://abc123.ngrok.io
```

---

## ✅ VERIFICATION CHECKLIST

**Check all before proceeding:**

- [ ] `gh --version` shows GitHub CLI installed
- [ ] `gh copilot suggest "test"` returns response
- [ ] `claude-code --version` shows Claude Code installed
- [ ] `H:\Tools\python.exe -c "import flask"` succeeds
- [ ] Bridge server starts without errors
- [ ] `curl http://localhost:8765/health` returns OK
- [ ] (Optional) Ngrok tunnel shows HTTPS URL

---

## 🚨 TROUBLESHOOTING

### **GitHub CLI Not Found**
```powershell
# Add to PATH:
$env:Path += ";C:\Program Files\GitHub CLI\"
```

### **Copilot Not Authenticated**
```powershell
gh auth refresh
gh auth status
```

### **Claude Code API Error**
```powershell
# Re-authenticate:
claude-code auth
# Enter valid API key from console.anthropic.com
```

### **Python Module Not Found**
```powershell
# Reinstall:
H:\Tools\python.exe -m pip install --force-reinstall flask flask-cors psutil --break-system-packages
```

### **Port 8765 Already In Use**
```powershell
# Find process using port:
netstat -ano | findstr :8765

# Kill process (replace PID):
taskkill /F /PID <PID>
```

---

## 📋 POST-INSTALLATION

**Next steps:**
1. ✅ Review TEST_PROCEDURES.md
2. ✅ Test all endpoints
3. ✅ Configure SPARK_INTEGRATION.md
4. ✅ Set up monitoring

---

**🎖️ INSTALLATION COMPLETE - PROCEED TO TESTING**
