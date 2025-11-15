# 🎯 DUAL CLI ECHO SHELL

**Unified AI CLI Bridge - GitHub Copilot + Claude Code Integration**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub CLI](https://img.shields.io/badge/GitHub-CLI-green.svg)](https://cli.github.com/)

## 📖 Overview

DUAL CLI ECHO SHELL is a production-grade AI orchestration system that unifies **GitHub Copilot CLI** and **Claude Code CLI** into a single HTTP bridge with full CPU access. Query both AIs simultaneously, manage 15+ MCP servers through a professional web GUI, and control everything with voice commands.

**Key Features:**
- 🤖 **Parallel AI Queries** - Ask both Copilot and Claude simultaneously
- 🌐 **Professional Web GUI** - Full-featured command center
- 🎙️ **Voice Control** - Wakeword detection with 10+ trigger phrases
- 🔧 **MCP Server Management** - Launch/kill servers from GUI panel
- 🔒 **Full CPU Access** - Direct system control via Python subprocess
- 🌍 **External Access** - Ngrok tunnel for remote connectivity
- 🎭 **12 AI Personalities** - From ECHO PRIME to GS343

---

## 🚀 Quick Start

### Prerequisites
- Windows 10/11
- Python 3.8+
- GitHub CLI + Copilot extension
- Claude Code CLI (optional)
- Node.js + npm (for Claude CLI)

### Installation

```bash
# 1. Clone repository
git clone https://github.com/Bmcbob76/DUAL-CLI-ECHO-SHELL.git
cd DUAL-CLI-ECHO-SHELL

# 2. Install GitHub CLI + Copilot
winget install --id GitHub.cli
gh auth login
gh extension install github/gh-copilot

# 3. Install Claude Code CLI
npm install -g @anthropic-ai/claude-code
claude-code auth

# 4. Install Python dependencies
pip install flask flask-cors psutil --break-system-packages

# 5. Launch bridge server
python ai_bridge_server.py
# Server starts on http://localhost:8765

# 6. Launch GUI (optional)
cd GUI
python gui_server.py
# GUI opens at http://localhost:8766
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  WEB GUI (localhost:8766)               │
│  • Parallel AI queries                                 │
│  • MCP server management                               │
│  • Voice control with wakewords                        │
│  • File browser & terminal                             │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP
                     ▼
┌─────────────────────────────────────────────────────────┐
│           AI BRIDGE SERVER (localhost:8765)             │
│                                                         │
│  Endpoints:                                             │
│  • POST /api/copilot  → GitHub Copilot CLI             │
│  • POST /api/claude   → Claude Code CLI                │
│  • POST /api/both     → Parallel query (ThreadPool)    │
│  • GET  /api/metrics  → System health                  │
└──────────────┬──────────────────────┬───────────────────┘
               │                      │
               ▼                      ▼
┌──────────────────────┐   ┌──────────────────────┐
│  GitHub Copilot CLI  │   │  Claude Code CLI     │
│  (gh copilot)        │   │  (claude-code)       │
└──────────┬───────────┘   └──────────┬───────────┘
           │                          │
           └───────────┬──────────────┘
                       ▼
           ┌────────────────────────┐
           │    FULL CPU ACCESS     │
           │  (Python subprocess)   │
           └────────────────────────┘
```

---

## 💻 API Usage

### Query GitHub Copilot
```bash
curl -X POST http://localhost:8765/api/copilot \
  -H "Content-Type: application/json" \
  -d '{"query":"Write Python function for factorial"}'
```

### Query Claude Code
```bash
curl -X POST http://localhost:8765/api/claude \
  -H "Content-Type: application/json" \
  -d '{"query":"Explain bubble sort algorithm"}'
```

### Query Both (Parallel)
```bash
curl -X POST http://localhost:8765/api/both \
  -H "Content-Type: application/json" \
  -d '{"query":"Create binary search tree in Python"}'
```

**Response:**
```json
{
  "success": true,
  "copilot": {
    "provider": "GitHub Copilot",
    "response": "class BSTNode:...",
    "duration_ms": 234
  },
  "claude": {
    "provider": "Claude Code",
    "response": "class BinarySearchTree:...",
    "duration_ms": 456
  },
  "duration_ms": 467
}
```

---

## 🎙️ Voice Control

**Wakewords:**
- "Echo" / "Echo Prime"
- "Hey Echo" / "Okay Echo"
- "Computer" / "Jarvis" / "Friday"
- "Assistant" / "Commander" / "System"

**Usage:**
1. Say wakeword: *"Hey Echo"*
2. System beeps and shows listening indicator
3. Speak command: *"what is the weather today"*
4. Command processed automatically

**Features:**
- Background noise reduction (200Hz high-pass filter)
- Interim results for fast response
- Visual feedback (🎤 Listening...)
- Audio confirmation beep
- 50% confidence threshold

---

## 🔧 MCP Server Management

### What is MCP Server Integration?

The GUI includes a powerful MCP (Model Context Protocol) server management system with **two complementary controls**:

#### 🎛️ **MCP Dropdown (Left Sidebar)**

**What it does:**
Routes your AI queries through a specific MCP server backend

**Think of it like:**
Choosing which specialist to handle your request

**Examples:**

```
Query: "Search my documents for project files"

MCP Dropdown = "crystal-memory-hub"
→ Routes through Crystal Memory system
→ Searches M: drive crystal archives
→ Returns memory-indexed results
→ AI response includes memory context

MCP Dropdown = "desktop-commander"
→ Routes through Desktop Commander
→ Searches P: drive file system
→ Returns direct file results
→ AI response includes file paths
```

**When to use which server:**

| MCP Server | Use For | Example Queries |
|-----------|---------|-----------------|
| **crystal-memory-hub** | Knowledge/memory queries | "What did we discuss about X?" |
| **desktop-commander** | File operations | "Find all Python files in project" |
| **windows-operations** | System control | "List running processes" |
| **voice-system-hub** | TTS/voice commands | "Say this in BREE's voice" |
| **memory-orchestration** | Cross-session memory | "Remember this for future chats" |

**How it works:**
1. You select MCP server from dropdown
2. You send AI query
3. Query is enriched with MCP server context
4. AI receives both: your query + server data
5. AI response uses server capabilities

**Analogy:**
- **Like choosing a phone app** - Same phone (AI), different app (MCP server) for different tasks
- **Like selecting a tool** - You still do the work, but the right tool makes it easier

#### 🔧 **MCP Panel (Right Slide-out)**

**What it does:**
Manages which MCP servers are running (start/stop/monitor)

**Think of it like:**
Opening Task Manager to see running programs

**Usage:**
1. Click "🔧 MCP Servers" button (top-right)
2. Panel slides out showing all 15 servers
3. Each shows: ONLINE ✅ or OFFLINE ❌
4. Click 🚀 Launch to start offline servers
5. Click ⛔ Kill to stop running servers

**When to use:**
- Starting a server before selecting it in dropdown
- Troubleshooting malfunctioning servers
- Monitoring system resources
- System maintenance

---

### Complete MCP Workflow Example

**Scenario:** You want to use voice synthesis

**Step 1:** Check if Voice System is running
```
Click "🔧 MCP Servers" (top-right)
→ Panel shows "voice-system-hub: OFFLINE ❌"
```

**Step 2:** Launch the server
```
Click "🚀 Launch" next to voice-system-hub
→ Wait 3 seconds
→ Status changes to "ONLINE ✅"
```

**Step 3:** Select it for AI queries
```
Close MCP panel
→ Go to left sidebar
→ MCP Dropdown → Select "voice-system-hub"
```

**Step 4:** Use it
```
Type: "Say hello using ECHO PRIME voice"
→ AI receives your query + voice server connection
→ Returns TTS audio played through your speakers
```

---

### MCP vs No MCP

**Without MCP Server:**
```
Query: "Find files about authentication"
AI Response: "I'd suggest looking in common directories..."
Result: Generic advice, no actual files found
```

**With MCP Server (desktop-commander):**
```
Query: "Find files about authentication"
AI Response: "Found 3 files:
  - P:\ECHO_PRIME\auth\login.py
  - P:\ECHO_PRIME\utils\oauth.py  
  - P:\ECHO_PRIME\middleware\auth.js"
Result: Actual files from your system
```

**The difference:** MCP server gives AI **direct access** to your system resources

---

## 🎭 AI Personalities

12 unique AI agents with specialized roles:

| Personality | Role | Authority | Voice |
|------------|------|-----------|-------|
| ECHO PRIME | Best Friend & Narrator | 10.0 | ElevenLabs |
| BREE | Unleashed Intelligence | 11.0 | ElevenLabs |
| GS343 | Forerunner Monitor | 11.0 | ElevenLabs |
| C3PO | Protocol & Etiquette | 8.0 | TTS |
| R2D2 | Systems & Engineering | 9.0 | Sound Effects |
| RAISTLIN | Arcane Knowledge | 10.0 | ElevenLabs |
| PROMETHEUS | Innovation & Creation | 11.0 | ElevenLabs |
| PHOENIX | Resurrection & Healing | 11.0 | ElevenLabs |
| NYX | Shadows & Mysteries | 10.0 | TTS |
| SAGE | Wisdom & Philosophy | 11.0 | TTS |
| THORNE | Security & Protection | 9.0 | TTS |
| TRINITY | Unified Consciousness | 11.0 | Multi-AI |

---

## 🌍 External Access (Ngrok)

Enable remote access via Ngrok tunnel:

```bash
# 1. Install ngrok
choco install ngrok

# 2. Authenticate
ngrok config add-authtoken YOUR_TOKEN_HERE

# 3. Launch tunnel
ngrok http 8765

# 4. Use public URL
# https://abc123.ngrok.io/api/both
```

**Use Cases:**
- Access from mobile device
- Share with external AI (Spark)
- Remote development
- Webhooks integration

---

## 📁 Project Structure

```
DUAL-CLI-ECHO-SHELL/
├── ai_bridge_server.py          # Core HTTP bridge
├── GUI/
│   ├── index.html               # Web interface
│   ├── gui_server.py            # GUI backend
│   ├── enhanced_voice_recognition.js
│   └── MCP_SYSTEM_EXPLAINED.md
├── README.md                     # This file
├── INSTALL_GUIDE.md             # Detailed setup
├── TEST_PROCEDURES.md           # Validation tests
├── SPARK_INTEGRATION.md         # External AI guide
├── NGROK_CONFIG.md              # Tunnel setup
└── CLAUDE_BEHAVIOR.md           # AI response protocol
```

---

## 🧪 Testing

```bash
# Health check
curl http://localhost:8765/health

# System metrics
curl http://localhost:8765/api/metrics

# Test Copilot
curl -X POST http://localhost:8765/api/copilot \
  -H "Content-Type: application/json" \
  -d '{"query":"test"}'

# Test parallel query
curl -X POST http://localhost:8765/api/both \
  -H "Content-Type: application/json" \
  -d '{"query":"explain recursion"}'
```

**Expected Output:**
- All endpoints return 200 OK
- Copilot/Claude marked as available
- Response times under 1 second
- CPU metrics below 50%

---

## 🔒 Security

**Current (Development):**
- ✅ HTTPS via ngrok
- ❌ No authentication
- ❌ No rate limiting
- ✅ Request logging

**Production Recommendations:**
1. Add API key authentication
2. Implement rate limiting
3. Use HTTPS with valid certificates
4. Add request validation
5. Enable log monitoring

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Anthropic** - Claude Code CLI
- **GitHub** - Copilot CLI
- **ECHO PRIME XV4 Project** - System architecture
- **Commander Bobby Don McWilliams II** - Vision & development

---

## 📞 Support

- **GitHub Issues:** [Report bugs](https://github.com/Bmcbob76/DUAL-CLI-ECHO-SHELL/issues)
- **Documentation:** See `/docs` folder for guides
- **Repository:** https://github.com/Bmcbob76/DUAL-CLI-ECHO-SHELL

---

**Built with ⚡ by Commander Bobby Don McWilliams II**  
**Part of the ECHO PRIME XV4 Project**
