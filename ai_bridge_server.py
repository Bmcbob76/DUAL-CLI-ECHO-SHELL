#!/usr/bin/env python3
"""
AI Bridge Server - GitHub Copilot + Claude Code CLI Integration
ECHO PRIME XV4 - Commander Bobby Don McWilliams II - Authority 11.0

Unified HTTP bridge for parallel AI CLI queries with full CPU access.
Personality Intelligence System integrated for self-aware agent responses.
"""

import os
import sys
import time
import json
import platform
import subprocess
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import personality intelligence system
try:
    from personality_intelligence import inject_personality, get_personality_context
    PERSONALITY_SYSTEM_AVAILABLE = True
except ImportError:
    PERSONALITY_SYSTEM_AVAILABLE = False
    print("⚠️  Personality Intelligence System not found - personalities will be labels only")

# Debug logging setup
DEBUG_LOG = r'P:\ECHO_PRIME\CLI_BRIDGE_INTEGRATION\debug.log'
def debug_log(msg):
    with open(DEBUG_LOG, 'a', encoding='utf-8') as f:
        f.write(f"[{datetime.now().isoformat()}] {msg}\n")
        f.flush()

debug_log("="*50)
debug_log("BRIDGE SERVER STARTING")

# Use user's configured Claude CLI credentials (don't override API key)
# This allows Claude CLI to use whatever key is configured via 'claude auth'

try:
    import psutil
except ImportError:
    print("⚠️  psutil not found - installing...")
    subprocess.run([sys.executable, "-m", "pip", "install", "psutil", "--break-system-packages"], check=True)
    import psutil

# Configuration
BRIDGE_PORT = 8765
REQUEST_LOG = []
MAX_LOG_ENTRIES = 1000

# Flask app setup
app = Flask(__name__)
CORS(app)

class SystemMetrics:
    """Track system performance metrics"""
    def __init__(self):
        self.cpu_percent = 0
        self.memory_percent = 0
        self.last_update = time.time()
    
    def update(self):
        """Update system metrics"""
        self.cpu_percent = psutil.cpu_percent(interval=0.1)
        self.memory_percent = psutil.virtual_memory().percent
        self.last_update = time.time()
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'cpu_percent': self.cpu_percent,
            'memory_percent': self.memory_percent,
            'last_update': datetime.fromtimestamp(self.last_update).isoformat()
        }

system_metrics = SystemMetrics()

def log_request(provider, query, duration_ms, success=True, error=None):
    """Log request for analytics"""
    global REQUEST_LOG
    entry = {
        'timestamp': datetime.now().isoformat(),
        'provider': provider,
        'query': query[:100],  # Truncate long queries
        'duration_ms': duration_ms,
        'success': success,
        'error': error
    }
    REQUEST_LOG.append(entry)
    if len(REQUEST_LOG) > MAX_LOG_ENTRIES:
        REQUEST_LOG = REQUEST_LOG[-MAX_LOG_ENTRIES:]
    return entry

def check_cli_available(command):
    """Check if CLI tool is available"""
    try:
        if command == 'claude':
            claude_cmd = r'C:\Users\bobmc\AppData\Roaming\npm\claude.cmd'
            result = subprocess.run([claude_cmd, '--version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5,
                                  env=os.environ.copy())
        elif command == 'copilot':
            copilot_cmd = r'C:\Users\bobmc\AppData\Roaming\npm\copilot.cmd'
            result = subprocess.run([copilot_cmd, '--version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5,
                                  env=os.environ.copy())
        else:
            result = subprocess.run([command, '--version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
        return result.returncode == 0
    except:
        return False

def query_copilot_cli(query):
    """Query GitHub Copilot CLI"""
    try:
        copilot_cmd = r'C:\Users\bobmc\AppData\Roaming\npm\copilot.cmd'
        result = subprocess.run(
            [copilot_cmd, '-p', query, '--allow-all-tools'],
            capture_output=True,
            text=True,
            timeout=30,
            env=os.environ.copy()
        )
        return {
            'success': result.returncode == 0,
            'response': result.stdout if result.returncode == 0 else result.stderr,
            'exit_code': result.returncode
        }
    except Exception as e:
        return {
            'success': False,
            'response': None,
            'error': str(e)
        }

def query_claude_cli(query):
    """Query Claude Code CLI using PowerShell inline (proven working on Windows)"""
    try:
        # Escape quotes for PowerShell
        escaped_query = query.replace('"', '`"').replace("'", "''")
        
        # PowerShell inline - pipe ready before process starts
        ps_command = f'echo "{escaped_query}" | claude -p --dangerously-skip-permissions'
        
        # Debug logging to file
        debug_log(f"query_claude_cli called")
        debug_log(f"  Query: {query}")
        debug_log(f"  Escaped: {escaped_query}")
        debug_log(f"  PS Command: {ps_command}")
        
        result = subprocess.run(
            ['powershell', '-Command', ps_command],
            capture_output=True,
            text=True,
            timeout=60,
            env=os.environ.copy()
        )
        
        # Debug logging to file
        debug_log(f"  Return Code: {result.returncode}")
        debug_log(f"  STDOUT: [{result.stdout}]")
        debug_log(f"  STDERR: [{result.stderr}]")
        debug_log(f"  STDOUT len: {len(result.stdout)}")
        debug_log(f"  STDERR len: {len(result.stderr)}")
        
        return {
            'success': result.returncode == 0,
            'response': result.stdout.strip() if result.returncode == 0 else result.stderr.strip(),
            'exit_code': result.returncode
        }
                
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'response': None,
            'error': 'Claude CLI timeout after 60s'
        }
    except Exception as e:
        return {
            'success': False,
            'response': None,
            'error': str(e)
        }

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Server health check"""
    system_metrics.update()
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'copilot_available': check_cli_available('copilot'),
        'claude_available': check_cli_available('claude'),
        'metrics': system_metrics.to_dict()
    })

# GitHub Copilot endpoint
@app.route('/api/copilot', methods=['POST'])
def copilot_query():
    """Query GitHub Copilot CLI with optional personality context"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        context = data.get('context', {})
        personality = context.get('personality') if context else None
        
        if not query:
            return jsonify({'success': False, 'error': 'No query provided'}), 400
        
        # Inject personality context if available
        if PERSONALITY_SYSTEM_AVAILABLE and personality:
            query = inject_personality(query, personality)
        
        start_time = time.time()
        result = query_copilot_cli(query)
        duration_ms = int((time.time() - start_time) * 1000)
        
        log_request('copilot', query[:100], duration_ms, result['success'], result.get('error'))
        
        return jsonify({
            'success': result['success'],
            'provider': 'GitHub Copilot',
            'response': result.get('response'),
            'personality': personality if personality else None,
            'duration_ms': duration_ms,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Claude Code endpoint
@app.route('/api/claude', methods=['POST'])
def claude_query():
    """Query Claude Code CLI with optional personality context"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        context = data.get('context', {})
        personality = context.get('personality') if context else None
        
        if not query:
            return jsonify({'success': False, 'error': 'No query provided'}), 400
        
        # Inject personality context if available
        if PERSONALITY_SYSTEM_AVAILABLE and personality:
            query = inject_personality(query, personality)
        
        start_time = time.time()
        result = query_claude_cli(query)
        duration_ms = int((time.time() - start_time) * 1000)
        
        log_request('claude', query[:100], duration_ms, result['success'], result.get('error'))
        
        return jsonify({
            'success': result['success'],
            'provider': 'Claude Code',
            'response': result.get('response'),
            'personality': personality if personality else None,
            'duration_ms': duration_ms,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Parallel query endpoint
@app.route('/api/both', methods=['POST'])
def both_query():
    """Query both Copilot and Claude in parallel with optional personality context"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        context = data.get('context', {})
        personality = context.get('personality') if context else None
        
        if not query:
            return jsonify({'success': False, 'error': 'No query provided'}), 400
        
        # Inject personality context if available
        if PERSONALITY_SYSTEM_AVAILABLE and personality:
            query = inject_personality(query, personality)
        
        start_time = time.time()
        
        # Execute both queries in parallel
        with ThreadPoolExecutor(max_workers=2) as executor:
            copilot_future = executor.submit(query_copilot_cli, query)
            claude_future = executor.submit(query_claude_cli, query)
            
            copilot_result = copilot_future.result()
            claude_result = claude_future.result()
        
        duration_ms = int((time.time() - start_time) * 1000)
        log_request('both', query[:100], duration_ms)
        
        return jsonify({
            'success': True,
            'personality': personality if personality else None,
            'copilot': {
                'provider': 'GitHub Copilot',
                **copilot_result
            },
            'claude': {
                'provider': 'Claude Code',
                **claude_result
            },
            'duration_ms': duration_ms,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# System metrics endpoint
@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get current system metrics"""
    system_metrics.update()
    return jsonify({
        'success': True,
        'metrics': system_metrics.to_dict(),
        'platform': {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor()
        },
        'request_log_size': len(REQUEST_LOG)
    })

# Request log endpoint
@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Get recent request logs"""
    limit = int(request.args.get('limit', 50))
    return jsonify({
        'success': True,
        'logs': REQUEST_LOG[-limit:],
        'total_requests': len(REQUEST_LOG)
    })

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🌉 ECHO PRIME - AI BRIDGE SERVER")
    print("="*70)
    print(f"\n🖥️  Platform: {platform.system()} {platform.release()}")
    print(f"🐍 Python: {platform.python_version()}")
    print(f"\n📡 Bridge Server: http://localhost:{BRIDGE_PORT}")
    print(f"✅ GitHub Copilot CLI: {'Available' if check_cli_available('copilot') else 'NOT FOUND'}")
    print(f"✅ Claude Code CLI: {'Available' if check_cli_available('claude') else 'NOT FOUND'}")
    
    system_metrics.update()
    print(f"\n💾 CPU Access: FULL")
    print(f"📊 System Metrics: {system_metrics.cpu_percent}% CPU, {system_metrics.memory_percent}% RAM")
    print(f"\n🔗 For Spark to connect externally, use ngrok:")
    print(f"   ngrok http {BRIDGE_PORT}")
    print(f"\n📋 Endpoints:")
    print(f"   GET  /health         - Server status")
    print(f"   POST /api/copilot    - GitHub Copilot query")
    print(f"   POST /api/claude     - Claude Code query")
    print(f"   POST /api/both       - Parallel query both")
    print(f"   GET  /api/metrics    - System metrics")
    print(f"   GET  /api/logs       - Request logs")
    print(f"\n🚀 Server starting...\n")
    print("="*70 + "\n")
    
    app.run(host='0.0.0.0', port=BRIDGE_PORT, debug=False)
