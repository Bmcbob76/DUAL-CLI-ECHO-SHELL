# ECHO PRIME - UNIFIED GUI DEPLOYMENT GUIDE

**Commander Bobby Don McWilliams II - Authority 11.0**

## 🎯 OVERVIEW

Complete web-based command center integrating:
- âœ… GitHub Copilot CLI
- âœ… Claude Code CLI
- âœ… 7 Agent Personalities
- âœ… ECHO SHELL Terminal
- âœ… Voice Control System
- âœ… 17 MCP Servers
- âœ… Full File System Access

---

## ðŸš€ QUICK START

### **STEP 1: Launch CLI Bridge**

```powershell
cd P:\ECHO_PRIME\CLI_BRIDGE_INTEGRATION
H:\Tools\python.exe ai_bridge_server.py
```

**Expected Output:**
```
🌉 ECHO PRIME - AI BRIDGE SERVER
📡 Bridge Server: http://localhost:8765
✅ GitHub Copilot CLI: Available
✅ Claude Code CLI: Available
```

---

### **STEP 2: Launch GUI Backend**

**New Terminal:**
```powershell
cd P:\ECHO_PRIME\CLI_BRIDGE_INTEGRATION\GUI
H:\Tools\python.exe gui_server.py
```

**Expected Output:**
```
🎖️ ECHO PRIME - GUI BACKEND SERVER
📡 GUI Backend: http://localhost:8766
🌉 CLI Bridge: http://localhost:8765
🔧 MCP Servers: 14 available
🌐 Open in browser: http://localhost:8766
```

---

### **STEP 3: Open Browser**

Navigate to: **http://localhost:8766**

---

## 📋 FEATURES

### **1. AI CHAT TAB**

**Left Sidebar Controls:**
- **Repository:** Select ECHO-PRIME-OMEGA or custom path
- **Environment:** Windows (Local CPU) / Linux / WSL
- **File Access:** Browse and select files/folders/drives
- **MCP Server:** Select from 17 available servers
- **AI Provider:** Both (Parallel) / Copilot / Claude
- **Personality:** Choose from 7 agent personalities

**Main Chat Area:**
- Split-screen AI responses
- Code syntax highlighting
- Session history
- Status indicators (Copilot, Claude, Bridge)

**Input Controls:**
- Quick Actions dropdown (fix, optimize, security, test, docs)
- Output Format (markdown, code, JSON)
- Send button (or Enter to submit)

---

### **2. ECHO SHELL TAB**

**Terminal Interface:**
Full command-line access with:

**Available Commands:**
```bash
help                    # Show all commands
clear                   # Clear terminal
status                  # System health & metrics

# Personality Commands
personality [name]      # Activate agent (echo_prime, bree, c3po, etc.)
personality list        # List all 7 personalities

# Voice Commands
voice speak [text]      # Text-to-speech output
voice [personality]     # Speak as specific personality

# MCP Commands
mcp list                # List all MCP servers
mcp query [server]      # Query specific server

# AI Commands
query [text]            # Direct AI query
```

**Terminal Features:**
- Command history (↑↓ arrows)
- Green text on black (classic terminal)
- Real-time output
- Error highlighting

---

### **3. VOICE CONTROL TAB**

**Voice Recognition:**
- Start/Stop voice recognition button
- Wake word detection for personalities
- Automatic personality activation
- Real-time voice feedback

**Supported Wake Words:**
- "ECHO" / "ECHO PRIME" → Activates ECHO PRIME
- "BREE" → Activates BREE
- "C3PO" / "THREEPIO" → Activates C3PO
- "R2D2" / "ARTOO" → Activates R2D2
- "GUILTY SPARK" / "343" / "GS343" → Activates GS343
- "PHOENIX" → Activates PHOENIX
- "HEPHAESTION" / "RAISTLIN" → Activates HEPHAESTION

---

## 🤖 AGENT PERSONALITIES

### **1. ECHO PRIME** 🎯
- **Role:** Best Friend, Advisor, Protector, Narrator
- **Authority:** 10.0
- **Voice:** Primary narrator voice
- **Features:** Facial recognition, location tracking
- **Use For:** General assistance, friendly conversation

### **2. BREE** 💎
- **Role:** Intelligence Analyst, Roast Master
- **Authority:** 9.0
- **Unleashed Level:** 15 (uncensored mode)
- **Use For:** Deep analysis, unfiltered insights, sassy responses

### **3. C3PO (EPCP3-O)** 🤖
- **Role:** Protocol Droid, Programmer, Debugger
- **Authority:** 9.9
- **Traits:** Anxious, formal, jealous of R2D2
- **Use For:** Programming, debugging, protocol questions

### **4. R2D2** 🔧
- **Role:** Astromech, Operations Hero
- **Authority:** 9.5
- **Communication:** Beeps, boops, whistles only
- **Use For:** System operations, heroic tasks

### **5. GS343 (Guilty Spark)** 👁️
- **Role:** Forerunner Archiver, Server Master
- **Authority:** 9.9
- **Age:** 100,000 years
- **Use For:** Server monitoring, deep system knowledge

### **6. PHOENIX** 🔥
- **Role:** Healer, Medical Specialist
- **Authority:** 9.0
- **Voice:** Soft, caring, healing (pending creation)
- **Use For:** Health monitoring, medical assistance

### **7. HEPHAESTION (Raistlin)** 🧙
- **Role:** Wizard, Forge Master, Craftsman
- **Authority:** 9.5
- **Elements:** Fire, water, earth, air, lightning, ice, light, shadow
- **Voice:** Old, powerful, booming wizard (pending creation)
- **Use For:** Magical operations, forging, crafting

---

## 🔧 CONFIGURATION

### **Environment Variables**

Located: `P:\ECHO_PRIME\AGENT_PERSONALITIES\personality_config.json`

**Key Settings:**
```json
{
  "orchestrator": {
    "anti_overlap_enabled": true,
    "fuzzy_logic_threshold": 0.75,
    "response_delay_seconds": 2.0,
    "commander_priority": true
  }
}
```

### **ElevenLabs Voice Settings**

API Keys stored in config
Voice settings:
- Stability: 0.75
- Similarity Boost: 0.75
- Style: 0.5
- Speaker Boost: Enabled

---

## 🎨 UI CUSTOMIZATION

**Theme:** Dark VS Code style
- Background: `#1e1e1e`
- Sidebar: `#252526`
- Accents: `#007acc`

**Fonts:**
- UI: System fonts (Segoe UI, SF Pro)
- Code: Consolas, Courier New

**Status Indicators:**
- 🟢 Green: Operational
- 🔴 Red: Offline
- 🟡 Yellow: Warning

---

## ⚡ KEYBOARD SHORTCUTS

**Chat Tab:**
- `Enter`: Send message
- `Shift+Enter`: New line

**Terminal Tab:**
- `Enter`: Execute command
- `↑`: Previous command
- `↓`: Next command
- `clear`: Clear screen

---

## 🚨 TROUBLESHOOTING

### **Bridge Not Connecting**

```powershell
# Check if bridge is running
curl http://localhost:8765/health

# Restart bridge
cd P:\ECHO_PRIME\CLI_BRIDGE_INTEGRATION
H:\Tools\python.exe ai_bridge_server.py
```

### **Copilot/Claude Not Available**

```powershell
# Verify CLI tools
gh --version
claude-code --version

# Re-authenticate if needed
gh auth login
claude-code auth
```

### **GUI Not Loading**

```powershell
# Check GUI server
curl http://localhost:8766/health

# Restart GUI server
cd P:\ECHO_PRIME\CLI_BRIDGE_INTEGRATION\GUI
H:\Tools\python.exe gui_server.py
```

### **Personality Not Activating**

1. Check personality_config.json exists
2. Verify voice IDs configured
3. Check ElevenLabs API keys
4. Test voice system separately

### **Terminal Commands Not Working**

1. Verify bridge health: `status` command
2. Check AI provider selected
3. Test direct query: `query test`
4. Review browser console for errors

---

## 📊 SYSTEM REQUIREMENTS

**Minimum:**
- Windows 10/11
- Python 3.8+
- 4GB RAM
- Modern browser (Chrome, Edge, Firefox)
- Internet connection

**Recommended:**
- Windows 11
- Python 3.10+
- 8GB RAM
- Chrome browser
- High-speed internet

---

## 🎯 NEXT STEPS

1. **External Access:** Configure ngrok for Spark integration
2. **Production Hardening:** Add authentication, rate limiting
3. **Voice Training:** Complete Phoenix and Hephaestion voices
4. **MCP Integration:** Connect all 17 MCP servers
5. **Monitoring:** Set up health checks and alerts

---

**🎖️ DEPLOYMENT COMPLETE - SYSTEM OPERATIONAL**

**For support:** Check TROUBLESHOOTING section or review logs at:
- CLI Bridge: Terminal output
- GUI Server: Terminal output
- Browser: Developer Console (F12)
