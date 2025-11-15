# ECHO PRIME - UNIFIED AI GUI

**Commander Bobby Don McWilliams II - Authority 11.0**

## 🎯 OVERVIEW

Claude Code-style GUI with complete CPU access, MCP server integration, and parallel AI querying.

---

## 🏗️ ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                  WEB GUI (localhost:8766)                   │
│                                                             │
│  Features:                                                  │
│  • Claude Code-style interface                             │
│  • Repository selector                                     │
│  • Environment dropdown (Windows/Linux/WSL)                │
│  • File/folder/drive browser                               │
│  • MCP server dropdown (17 servers)                        │
│  • AI provider selector (Copilot/Claude/Both)             │
│  • Session management                                      │
│  • Real-time status indicators                            │
└──────────────┬──────────────────────────────────────────────┘
               │ HTTP (localhost:8766)
               ▼
┌─────────────────────────────────────────────────────────────┐
│              GUI BACKEND SERVER (Python Flask)              │
│                                                             │
│  Responsibilities:                                          │
│  • Serve web GUI                                           │
│  • File system operations                                  │
│  • Command execution                                       │
│  • MCP server proxy                                        │
└──────────────┬──────────────────────────────────────────────┘
               │
        ┌──────┴───────┬───────────────┐
        │              │               │
        ▼              ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ CLI BRIDGE  │ │ FILE SYSTEM │ │ MCP SERVERS │
│ (port 8765) │ │   (P: drive)│ │  (17 total) │
│             │ │             │ │             │
│ • Copilot   │ │ • Read      │ │ • Crystals  │
│ • Claude    │ │ • Write     │ │ • Desktop   │
│ • Parallel  │ │ • Browse    │ │ • Voice     │
└─────────────┘ └─────────────┘ └─────────────┘
```

---

## 🚀 QUICK START

### **Option 1: One-Click Launch**
```batch
P:\ECHO_PRIME\CLI_BRIDGE_INTEGRATION\LAUNCH_ALL.bat
```

Opens browser automatically to GUI.

---

### **Option 2: Manual Launch**

**Terminal 1 - CLI Bridge:**
```powershell
cd P:\ECHO_PRIME\CLI_BRIDGE_INTEGRATION
H:\Tools\python.exe ai_bridge_server.py
```

**Terminal 2 - GUI Backend:**
```powershell
cd P:\ECHO_PRIME\CLI_BRIDGE_INTEGRATION\GUI
H:\Tools\python.exe gui_server.py
```

**Browser:**
```
http://localhost:8766
```

---

## 🎮 GUI FEATURES

### **Left Sidebar Controls**

**Repository Selector:**
- Pre-configured: `Bmcbob76/ECHO-PRIME-OMEGA`
- Custom path option

**Environment Selector:**
- Windows (Local CPU) - Direct system access
- Linux Container - Containerized execution
- WSL - Windows Subsystem for Linux

**File/Folder/Drive Access:**
- Browse button opens file browser modal
- Navigate: P:, H:, M:, G: drives
- Select files or directories
- Full read/write access

**MCP Server Dropdown:**
- **Direct CLI Query** (default) - No MCP, direct AI
- **Crystal Memory Hub** - 565+ crystals
- **Desktop Commander** - File operations
- **Developer Gateway** - Code generation
- **EPCP3O Agent** - Autonomous tasks
- **GS343 Gateway** - Error patterns
- **Harvesters Gateway** - Knowledge harvesting
- **Healing Orchestrator** - System healing
- **Master Orchestrator** - Multi-model routing
- **Memory Orchestration** - 9-layer memory
- **Network Guardian** - Network security
- **Trainers Gateway** - Model training
- **Voice System Hub** - TTS characters
- **Windows Gateway** - Windows API
- **Windows Operations** - Process management

**AI Provider:**
- **Both (Parallel)** - Query Copilot + Claude simultaneously
- **GitHub Copilot** - Copilot only
- **Claude Code** - Claude only

---

### **Main Chat Area**

**Status Indicators (Top Right):**
- 🟢 Green = Online/Available
- 🔴 Red = Offline/Unavailable
- 🟠 Orange = Warning/Degraded

**Message Display:**
- User messages: Blue, right-aligned
- AI responses: Gray, left-aligned
- Code blocks: Syntax highlighted
- Parallel queries: Both responses shown

**Input Controls:**
- Quick Actions dropdown (fix bug, optimize, audit, test, docs)
- Output Format (Markdown, Code Only, JSON)
- Multi-line textarea (Shift+Enter for newline)
- Send button

---

## 📂 FILE BROWSER

**Access:** Click "📁 Browse Files" button

**Features:**
- Navigate entire file system
- Click directories to descend
- Click ".." to go up
- Click files to select
- Selected path auto-fills in sidebar
- Close modal to return to chat

**Supported:**
- All drives (P:, H:, M:, G:, C:, etc.)
- Network paths
- Hidden folders (shown)
- Large directories (paginated)

---

## ⚡ USAGE EXAMPLES

### **Example 1: File Analysis**
1. Click "Browse Files"
2. Navigate to `P:\ECHO_PRIME\MLS_CLEAN\`
3. Select `ULTIMATE_MLS_LAUNCHER.py`
4. AI Provider: "Both (Parallel)"
5. Type: "Analyze this file for security vulnerabilities"
6. Send

**Result:** Both Copilot and Claude analyze the file, compare findings.

---

### **Example 2: MCP Server Query**
1. MCP Server: "Crystal Memory Hub"
2. Type: "Search crystals for TypeScript patterns"
3. Send

**Result:** Queries Crystal Memory Hub MCP, returns results.

---

### **Example 3: Code Generation**
1. Repository: "ECHO-PRIME-OMEGA"
2. Environment: "Windows (Local CPU)"
3. Path: "P:\ECHO_PRIME\NEW_MODULE\"
4. AI Provider: "Claude Code"
5. Quick Action: "Generate tests"
6. Type: "Create comprehensive test suite for authentication module"
7. Send

**Result:** Claude generates tests, can save to specified path.

---

## 🔧 API ENDPOINTS

### **GUI Backend (localhost:8766)**

**Health Check:**
```http
GET /health
```

**List Files:**
```http
POST /api/files/list
Content-Type: application/json

{
  "path": "P:\\ECHO_PRIME"
}
```

**Read File:**
```http
POST /api/files/read
Content-Type: application/json

{
  "path": "P:\\ECHO_PRIME\\README.md"
}
```

**Write File:**
```http
POST /api/files/write
Content-Type: application/json

{
  "path": "P:\\ECHO_PRIME\\new_file.txt",
  "content": "File contents here"
}
```

**Execute Command:**
```http
POST /api/execute
Content-Type: application/json

{
  "command": "dir P:\\ECHO_PRIME"
}
```

**MCP Server Proxy:**
```http
POST /api/mcp/CRYSTAL_MEMORY_HUB
Content-Type: application/json

{
  "action": "search",
  "query": "TypeScript patterns"
}
```

---

### **CLI Bridge (localhost:8765)**

See: `ai_bridge_server.py` documentation

**Key Endpoints:**
- `GET /health` - Status check
- `POST /api/copilot` - Query Copilot
- `POST /api/claude` - Query Claude
- `POST /api/both` - Parallel query
- `GET /api/metrics` - System metrics

---

## 🔒 SECURITY

**Current:**
- ✅ CORS enabled (all origins)
- ✅ Local binding (localhost only)
- ❌ No authentication
- ❌ No rate limiting
- ❌ No input sanitization (file paths)

**Production Hardening:**
1. Add API key authentication
2. Implement rate limiting
3. Validate all file paths
4. Restrict allowed directories
5. Add HTTPS
6. Log all operations

---

## 📊 SYSTEM REQUIREMENTS

**Minimum:**
- Windows 10/11
- Python 3.8+
- 4GB RAM
- GitHub CLI + Copilot extension
- Claude Code CLI
- Web browser (Chrome/Edge/Firefox)

**Recommended:**
- Windows 11
- Python 3.11+
- 8GB RAM
- SSD storage
- Modern browser
- Stable internet

---

## 🚨 TROUBLESHOOTING

### **GUI Won't Load**
```powershell
# Check if servers running:
netstat -ano | findstr :8765
netstat -ano | findstr :8766

# Kill and restart:
P:\ECHO_PRIME\CLI_BRIDGE_INTEGRATION\LAUNCH_ALL.bat
```

### **File Browser Empty**
- Check path permissions
- Try different drive (C:, P:, H:)
- Use absolute paths

### **AI Not Responding**
- Check status indicators (top right)
- Verify CLI tools authenticated:
  ```powershell
  gh auth status
  claude --version
  ```

### **MCP Server Unavailable**
- MCP proxying is placeholder currently
- Direct CLI queries always work
- Full MCP integration in next phase

---

## 🎯 ROADMAP

**Phase 1: COMPLETE**
- ✅ GUI interface
- ✅ CLI bridge integration
- ✅ File browser
- ✅ Repository selector
- ✅ Environment dropdown
- ✅ AI provider selector

**Phase 2: IN PROGRESS**
- ⏳ MCP server integration
- ⏳ Code editor pane
- ⏳ Syntax highlighting
- ⏳ Git integration

**Phase 3: PLANNED**
- ⏳ Multi-file editing
- ⏳ Terminal embedded
- ⏳ Project templates
- ⏳ Team collaboration
- ⏳ Cloud sync

---

## 📞 SUPPORT

**Commander Bobby Don McWilliams II**
Authority Level: 11.0

**Files:**
- GUI: `P:\ECHO_PRIME\CLI_BRIDGE_INTEGRATION\GUI\index.html`
- Backend: `P:\ECHO_PRIME\CLI_BRIDGE_INTEGRATION\GUI\gui_server.py`
- CLI Bridge: `P:\ECHO_PRIME\CLI_BRIDGE_INTEGRATION\ai_bridge_server.py`
- Launcher: `P:\ECHO_PRIME\CLI_BRIDGE_INTEGRATION\LAUNCH_ALL.bat`

---

**🎖️ ECHO PRIME - UNIFIED AI COMMAND CENTER**
**FULL OPERATIONAL CAPABILITY ACHIEVED**
