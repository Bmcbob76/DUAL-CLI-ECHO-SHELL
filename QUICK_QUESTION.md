QUICK QUESTION FOR CLAUDE CLI INTERACTIVE SESSION:

I'm building an HTTP bridge that needs to call Claude CLI from Python subprocess.

PROBLEM:
- PowerShell: `echo "query" | claude -p` → ✅ WORKS
- Python: `subprocess.run(['claude', '-p'], input='query')` → ❌ FAILS
- Error: "Input must be provided either through stdin or as a prompt argument"

WHY DOES THIS HAPPEN?
Why does PowerShell pipe work but Python subprocess.PIPE with communicate(input='query') fail?

WHAT I NEED:
Python code that successfully calls `claude -p` and gets a response.

My HTTP bridge server needs to:
1. Receive query via POST
2. Call Claude CLI programmatically  
3. Return response synchronously
4. Must work from Python subprocess

Working Copilot example for comparison:
```python
subprocess.run(['gh', 'copilot', 'suggest', query], capture_output=True)
# This works perfectly
```

Can you provide working Python code to call Claude CLI -p mode?
Or explain why it's impossible and suggest alternatives?

See full investigation: P:\ECHO_PRIME\CLI_BRIDGE_INTEGRATION\CLAUDE_CLI_INVESTIGATION_PROMPT.md