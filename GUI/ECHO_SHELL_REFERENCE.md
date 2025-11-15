# ECHO SHELL - QUICK REFERENCE CARD

**Commander Bobby Don McWilliams II - Authority 11.0**

---

## ⚡ BASIC COMMANDS

```bash
help                    # Show all commands
clear                   # Clear terminal screen
status                  # System health & metrics
```

---

## 🤖 PERSONALITY COMMANDS

```bash
personality list                    # List all 7 personalities
personality echo_prime              # Activate ECHO PRIME
personality bree                    # Activate BREE (Intelligence Analyst)
personality c3po                    # Activate C3PO (Protocol Droid)
personality r2d2                    # Activate R2D2 (Astromech)
personality gs343                   # Activate GS343 (Guilty Spark)
personality phoenix                 # Activate PHOENIX (Healer)
personality hephaestion             # Activate HEPHAESTION (Wizard)
```

---

## 🎙️ VOICE COMMANDS

```bash
voice speak Hello Commander        # TTS output with current personality
voice echo_prime                   # Switch to ECHO PRIME voice
voice bree                         # Switch to BREE voice
voice c3po                         # Switch to C3PO voice
voice gs343                        # Switch to GS343 voice
```

---

## 🔧 MCP SERVER COMMANDS

```bash
mcp list                           # List all 17 MCP servers
mcp query CRYSTAL_MEMORY_HUB       # Query specific server
mcp query DESKTOP_COMMANDER        # Query Desktop Commander
mcp query GS343_GATEWAY            # Query GS343 Gateway
```

**Available MCP Servers:**
- CRYSTAL_MEMORY_HUB
- DESKTOP_COMMANDER
- DEVELOPER_GATEWAY
- EPCP3O_AGENT
- GS343_GATEWAY
- HARVESTERS_GATEWAY
- HEALING_ORCHESTRATOR
- MASTER_ORCHESTRATOR_HUB
- MEMORY_ORCHESTRATION_SERVER
- NETWORK_GUARDIAN
- TRAINERS_GATEWAY
- VOICE_SYSTEM_HUB
- WINDOWS_GATEWAY
- WINDOWS_OPERATIONS
- PDF_TOOLS
- HUGGING_FACE
- UNIFIED_MCP_MASTER

---

## 🤖 AI QUERY COMMANDS

```bash
query How do I optimize Python code?           # Direct AI query
query Fix this bug: [code]                     # Debug assistance
query Explain machine learning                 # Knowledge query
```

**Note:** AI provider is selected in GUI sidebar (Both/Copilot/Claude)

---

## ⌨️ KEYBOARD SHORTCUTS

```bash
Enter                   # Execute command
↑ (Up Arrow)            # Previous command (history)
↓ (Down Arrow)          # Next command (history)
```

---

## 🎯 PERSONALITY WAKE WORDS

**For Voice Control Tab:**
- "ECHO" / "ECHO PRIME" / "PRIME" → ECHO PRIME
- "BREE" / "B" → BREE
- "C3PO" / "THREEPIO" → C3PO
- "R2D2" / "ARTOO" / "R2" → R2D2
- "GUILTY SPARK" / "343" / "GS343" / "SPARK" → GS343
- "PHOENIX" / "HEALER" → PHOENIX
- "HEPHAESTION" / "RAISTLIN" / "WIZARD" → HEPHAESTION

---

## 📊 STATUS OUTPUT EXAMPLE

```
═══════════════════════════════════════════════════════
SYSTEM STATUS
═══════════════════════════════════════════════════════
Bridge Server:    ✅ OPERATIONAL
GitHub Copilot:   ✅ AVAILABLE
Claude Code CLI:  ✅ AVAILABLE

CPU Usage:        15.3%
Memory Usage:     42.7%

MCP Servers:      17 available
Personalities:    7 loaded
Authority Level:  11.0
═══════════════════════════════════════════════════════
```

---

## 🎯 QUICK WORKFLOW EXAMPLES

### **Example 1: Code Review with BREE**
```bash
personality bree
query Review this Python function for security issues: [code]
```

### **Example 2: Debug with C3PO**
```bash
personality c3po
query Why is this throwing a NullReferenceException? [code]
```

### **Example 3: System Health Check**
```bash
status
mcp list
personality gs343
query Check all server health
```

### **Example 4: Voice Announcement**
```bash
personality echo_prime
voice speak Mission accomplished Commander
```

---

## 🚨 COMMON ISSUES

**Command Not Found:**
- Check spelling (case-insensitive)
- Type `help` for full list

**AI Query Fails:**
- Run `status` to check bridge health
- Verify AI provider selected in GUI

**Personality Not Responding:**
- Ensure personality activated: `personality list`
- Check personality_config.json exists

**Voice Not Working:**
- Verify Voice System Hub running (port 8781)
- Check ElevenLabs API keys configured
- Some voices pending creation (Phoenix, Hephaestion)

---

**🎖️ ECHO SHELL v4.0 - READY FOR DEPLOYMENT**
