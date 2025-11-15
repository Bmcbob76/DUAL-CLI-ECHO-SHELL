import subprocess
import tempfile
import os

query = "what is 5 times 5"

# Create temp file
with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
    f.write(query)
    temp_file = f.name

print(f"Temp file: {temp_file}")

try:
    with open(temp_file, 'r') as stdin_file:
        result = subprocess.run(
            ['claude', '-p', '--dangerously-skip-permissions'],
            stdin=stdin_file,
            capture_output=True,
            text=True,
            timeout=30
        )
    
    print(f"Return code: {result.returncode}")
    print(f"Stdout: {result.stdout[:500]}")
    print(f"Stderr: {result.stderr[:500]}")
finally:
    if os.path.exists(temp_file):
        os.remove(temp_file)
