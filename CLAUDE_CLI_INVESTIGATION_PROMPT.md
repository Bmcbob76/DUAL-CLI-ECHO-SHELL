CLAUDE CODE CLI - SUBPROCESS STDIN INVESTIGATION
ECHO PRIME XV4 - Commander Bobby Don McWilliams II - Authority 11.0

=====================================================================
MISSION OBJECTIVE
=====================================================================

Investigate why Claude CLI works perfectly in PowerShell but fails
when called from Python subprocess, specifically regarding stdin handling
for the -p (print) flag.

=====================================================================
SYSTEM CONFIGURATION
=====================================================================

Platform: Windows 10
Claude CLI: v2.0.37 (Claude Code)
Python: 3.10.0
Node: Latest
Authentication: VALID (OAuth tokens present, Claude Max subscription)
Installation: C:\Users\bobmc\AppData\Roaming\npm\node_modules\@anthropic-ai\claude-code\

=====================================================================
WHAT WORKS PERFECTLY
=====================================================================

✅ **PowerShell Direct Execution:**
```powershell
$input = "what is 2+2"
$input | claude -p --dangerously-skip-permissions
```
**Result:** Works instantly, returns "2+2 equals 4"

✅ **PowerShell Echo Pipe:**
```powershell
echo "what is 2+2" | claude -p --dangerously-skip-permissions
```
**Result:** Works perfectly

✅ **Interactive Mode (no -p flag):**
```powershell
claude
# Then type queries interactively
```
**Result:** Works flawlessly

✅ **Version Check:**
```powershell
claude --version
```
**Result:** Returns "2.0.37 (Claude Code)" instantly

=====================================================================
WHAT FAILS CONSISTENTLY
=====================================================================

❌ **Python subprocess.run() with argument:**
```python
subprocess.run(
    ['claude', '-p', '--dangerously-skip-permissions', 'what is 2+2'],
    stdin=subprocess.DEVNULL,
    capture_output=True,
    text=True,
    timeout=60
)
```
**Result:** Error: "Input must be provided either through stdin or as a prompt argument when using --print"

❌ **Python subprocess.run() with stdin input:**
```python
subprocess.run(
    ['claude', '-p', '--dangerously-skip-permissions'],
    input='what is 2+2',
    capture_output=True,
    text=True,
    timeout=60
)
```
**Result:** Same error

❌ **Python Popen with communicate:**
```python
process = subprocess.Popen(
    ['claude', '-p', '--dangerously-skip-permissions'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
stdout, stderr = process.communicate(input='what is 2+2', timeout=60)
```
**Result:** Same error

❌ **Python calling node/cli.js directly:**
```python
subprocess.Popen(
    ['node', 'C:\\...\\cli.js', '-p', '--dangerously-skip-permissions'],
    stdin=subprocess.PIPE,
    ...
).communicate(input='query')
```
**Result:** Same error

❌ **Python with shell=True PowerShell command:**
```python
subprocess.run(
    'echo "query" | claude -p --dangerously-skip-permissions',
    shell=True,
    capture_output=True,
    text=True
)
```
**Result:** Same error (stdin not recognized)

=====================================================================
EXACT ERROR MESSAGE
=====================================================================

"Error: Input must be provided either through stdin or as a prompt argument when using --print"

This error appears DESPITE:
- Using stdin=subprocess.PIPE with communicate()
- Using input='query' parameter
- Sending query as command argument
- Calling with shell=True
- Calling node/cli.js directly

=====================================================================
DISCOVERY: PowerShell vs Python Stdin Difference
=====================================================================

**Observation:**
The SAME command that works in PowerShell fails in Python subprocess:

**PowerShell (WORKS):**
```powershell
$input = "query"; $input | claude -p --dangerously-skip-permissions
```

**Python (FAILS):**
```python
subprocess.run(['powershell', '-Command', '$input = "query"; $input | claude -p --dangerously-skip-permissions'])
```

This suggests Claude CLI detects stdin differently when invoked from Python.

=====================================================================
TESTED CONFIGURATIONS
=====================================================================

1. ✅ claude.cmd wrapper - works in PowerShell
2. ❌ claude.cmd via Python subprocess
3. ✅ Direct PowerShell pipe - works
4. ❌ PowerShell command via Python shell=True
5. ❌ Direct node cli.js call
6. ❌ Batch file wrapper with stdin redirect
7. ❌ DEVNULL, PIPE, file handles - all fail

=====================================================================
INVESTIGATION QUESTIONS
=====================================================================

**Q1: Stdin Detection Mechanism**
How does Claude CLI's -p flag detect whether stdin is available?
Does it check:
- isatty()?
- File descriptor state?
- Environment variables?
- Process tree?
- TTY allocation?

**Q2: PowerShell vs Python Behavior**
Why does PowerShell's pipe work but Python's subprocess.PIPE doesn't?
What's different about how these create stdin file descriptors?

**Q3: Windows-Specific Issues**
Is this a Windows-specific problem with:
- .cmd wrapper behavior?
- Node.js stdin handling on Windows?
- Python subprocess on Windows?
- File descriptor inheritance?

**Q4: Node.js CLI Implementation**
Looking at cli.js:
- How does it read stdin in -p mode?
- Does it use process.stdin.isTTY?
- Does it check process.stdin.readable?
- What conditions must be met for stdin to be recognized?

**Q5: Workaround Viability**
Given that PowerShell pipes work, is there a way to:
- Invoke PowerShell from Python that preserves stdin behavior?
- Use a different stdin mechanism that Claude CLI recognizes?
- Bypass the stdin check programmatically?

**Q6: Alternative Input Methods**
Can Claude CLI accept input via:
- Environment variable?
- Temp file path?
- Named pipe?
- HTTP endpoint?
- Different flag combination?

**Q7: Debug Mode Analysis**
When running with --debug flag, what diagnostics show:
```python
subprocess.run(['claude', '-p', '--debug', '--dangerously-skip-permissions', 'query'])
```
vs
```powershell
echo "query" | claude -p --debug --dangerously-skip-permissions
```

**Q8: Process Execution Context**
Does Claude CLI check:
- Parent process name?
- Execution context (interactive vs batch)?
- Console window presence?
- Standard handle allocation?

=====================================================================
HTTP BRIDGE USE CASE
=====================================================================

**Goal:** Create HTTP bridge server that:
1. Receives query via POST /api/claude
2. Calls Claude CLI programmatically
3. Returns response synchronously
4. Must work from Python Flask server

**Current Blocker:**
Cannot invoke Claude CLI from Python subprocess in any tested configuration.

**Required Solution:**
Programmatic method to query Claude CLI that:
- Works from Python
- Returns response within 60 seconds
- Handles stdin properly
- Doesn't require user interaction

=====================================================================
REQUESTED DELIVERABLES
=====================================================================

1. **Root Cause Analysis**
   - Why Python subprocess fails vs PowerShell success
   - Exact stdin detection mechanism in Claude CLI
   - Technical explanation of the difference

2. **Working Solution**
   - Python code that successfully calls Claude CLI -p mode
   - Verified to work from subprocess (not shell=True if avoidable)
   - Production-ready error handling

3. **Alternative Approaches**
   - If subprocess is fundamentally incompatible:
     * Different input method?
     * API endpoint?
     * IPC mechanism?
     * Configuration change?

4. **Code Examples**
   - Complete working Python function
   - Test script to verify solution
   - HTTP bridge integration example

5. **Documentation**
   - Why this happens
   - How the fix works
   - Any limitations or caveats
   - Best practices for subprocess usage

=====================================================================
TEST VALIDATION CRITERIA
=====================================================================

Solution must pass:

✅ **Test 1: Direct subprocess.run()**
```python
result = subprocess.run(['claude', '-p', 'what is 2+2'], ...)
assert result.returncode == 0
assert '4' in result.stdout
```

✅ **Test 2: HTTP Bridge Integration**
```python
@app.route('/query', methods=['POST'])
def query():
    result = query_claude(request.json['query'])
    return jsonify(result)
```

✅ **Test 3: Complex Query**
```python
result = query_claude("write fibonacci function in python")
assert result['success'] == True
assert 'def fibonacci' in result['response']
```

✅ **Test 4: Parallel Execution**
```python
# Multiple simultaneous queries
with ThreadPoolExecutor() as executor:
    futures = [executor.submit(query_claude, f"test {i}") for i in range(5)]
    results = [f.result() for f in futures]
    assert all(r['success'] for r in results)
```

=====================================================================
ADDITIONAL CONTEXT
=====================================================================

**Bridge Server Architecture:**
- Flask HTTP server on localhost:8765
- Parallel queries to Copilot + Claude CLIs
- Full CPU access via subprocess
- External connectivity via ngrok for Spark AI

**Current Status:**
- Copilot CLI endpoint: ✅ FULLY OPERATIONAL
- Claude CLI endpoint: ❌ BLOCKED on stdin issue
- 50% functionality achieved
- Copilot works perfectly with same subprocess code

**Copilot Working Code (for reference):**
```python
def query_copilot_cli(query):
    result = subprocess.run(
        ['gh', 'copilot', 'suggest', query],
        capture_output=True,
        text=True,
        timeout=30
    )
    return result.stdout  # Works perfectly
```

=====================================================================
DIAGNOSTIC COMMANDS TO RUN
=====================================================================

Please analyze these and explain the differences:

**Command 1:**
```powershell
echo "test" | claude -p --dangerously-skip-permissions
```
**Expected:** Works (confirmed)

**Command 2:**
```python
import subprocess
subprocess.run(['powershell', '-Command', 'echo "test" | claude -p --dangerously-skip-permissions'], capture_output=True)
```
**Expected:** Fails (confirmed)

**Command 3:**
```python
import subprocess
p = subprocess.Popen(['claude', '-p'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(input="test", timeout=30)
print(out, err)
```
**Expected:** Fails (confirmed)

**WHY do these behave differently?**

=====================================================================
CRITICAL SUCCESS FACTORS
=====================================================================

- Must work from Python subprocess (HTTP bridge requirement)
- Must complete within 60 seconds
- Must handle arbitrary query strings (with quotes, special chars)
- Must be reliable for production use
- Should avoid shell=True if possible (security)
- Must work on Windows 10

=====================================================================
END OF INVESTIGATION REQUEST
=====================================================================

Please provide:
1. Technical explanation of the root cause
2. Working Python code solution
3. Any limitations or caveats
4. Alternative approaches if subprocess is impossible

Priority: HIGH - Blocking unified CLI bridge deployment
Authority: Level 11.0
Status: AWAITING CLAUDE CLI INVESTIGATION