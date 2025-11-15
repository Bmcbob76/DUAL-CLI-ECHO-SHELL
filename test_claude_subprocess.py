#!/usr/bin/env python3
"""Test Claude CLI via subprocess"""
import subprocess
import os

query = "what is 3 plus 4"
escaped_query = query.replace('"', '`"').replace("'", "''")
ps_command = f'echo "{escaped_query}" | claude -p --dangerously-skip-permissions'

print(f"Query: {query}")
print(f"Escaped: {escaped_query}")
print(f"PS Command: {ps_command}")
print("\nExecuting...\n")

result = subprocess.run(
    ['powershell', '-Command', ps_command],
    capture_output=True,
    text=True,
    timeout=20,
    env=os.environ.copy()
)

print(f"RETURN CODE: {result.returncode}")
print(f"STDOUT: [{result.stdout}]")
print(f"STDERR: [{result.stderr}]")
print(f"STDOUT LEN: {len(result.stdout)}")
print(f"STDERR LEN: {len(result.stderr)}")
