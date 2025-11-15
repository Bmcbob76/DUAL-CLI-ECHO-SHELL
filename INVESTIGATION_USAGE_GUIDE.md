# CLAUDE CLI INVESTIGATION - USAGE GUIDE

**Files Created:**
1. `CLAUDE_CLI_INVESTIGATION_PROMPT.md` - Comprehensive investigation request
2. `QUICK_QUESTION.md` - Concise version for quick query
3. `test_claude_subprocess.py` - Test script demonstrating the issue

---

## METHOD 1: Interactive Claude CLI Session (RECOMMENDED)

```powershell
# 1. Open interactive Claude
cd P:\ECHO_PRIME\CLI_BRIDGE_INTEGRATION
claude

# 2. Paste contents from QUICK_QUESTION.md
# OR paste full CLAUDE_CLI_INVESTIGATION_PROMPT.md for detailed analysis

# 3. Claude will investigate and provide solution
```

---

## METHOD 2: Run Test Script + Show Results

```powershell
# 1. Run test script
H:\Tools\python.exe P:\ECHO_PRIME\CLI_BRIDGE_INTEGRATION\test_claude_subprocess.py

# 2. Copy output

# 3. Open Claude interactive session
claude

# 4. Say: "I ran this test script and got these results. Why does PowerShell work but Python subprocess fail?"
# Then paste the test output
```

---

## METHOD 3: Direct Question

Open Claude interactive session and ask:

```
Why does this work in PowerShell:
  echo "query" | claude -p --dangerously-skip-permissions

But this fails in Python:
  subprocess.run(['claude', '-p'], input='query', capture_output=True)

Error: "Input must be provided either through stdin or as a prompt argument"

I need Python code to call Claude CLI from an HTTP bridge server.
```

---

## EXPECTED OUTCOMES

Claude CLI may provide:
1. **Working Python code** - Solution that fixes subprocess stdin issue
2. **Technical explanation** - Why PowerShell vs Python behave differently  
3. **Alternative approach** - Different method if subprocess is fundamentally broken
4. **Workaround** - Temp solution while waiting for CLI fix

---

## CURRENT STATUS

**Working:**
- ✅ Copilot CLI via Python subprocess
- ✅ Claude CLI via PowerShell direct
- ✅ Bridge server infrastructure ready

**Blocked:**
- ❌ Claude CLI via Python subprocess
- ❌ Unified bridge /api/both endpoint

**Progress:**
- Bridge server: 50% functional (Copilot only)
- Full CPU access: Confirmed
- Ready to deploy once Claude CLI issue resolved

---

## NEXT STEPS

1. **Use Method 1** to get Claude's investigation
2. **Implement solution** provided by Claude
3. **Test with test_claude_subprocess.py**
4. **Update bridge server** with working code
5. **Deploy fully operational unified bridge**

---

## FALLBACK OPTIONS

If Claude CLI cannot be fixed:

**Option A:** Deploy Copilot-only bridge (functional now)
**Option B:** Use direct Anthropic API instead of CLI
**Option C:** Create workaround with PowerShell subprocess
**Option D:** Wait for Claude CLI update from Anthropic

Authority Level: 11.0
Status: Investigation prompts ready
