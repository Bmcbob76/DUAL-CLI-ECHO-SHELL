#!/usr/bin/env python3
"""
ECHO PRIME - GUI Backend Server
Connects web GUI to CLI bridge + MCP servers + file system
"""

import os
import json
import subprocess
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

GUI_PORT = 8766
CLI_BRIDGE_URL = 'http://localhost:8765'

# MCP Server endpoints mapping
MCP_SERVERS = {
    'CRYSTAL_MEMORY_HUB': 'http://localhost:8770',
    'DESKTOP_COMMANDER': 'http://localhost:8771',
    'DEVELOPER_GATEWAY': 'http://localhost:8772',
    'EPCP3O_AGENT': 'http://localhost:8773',
    'GS343_GATEWAY': 'http://localhost:8774',
    'HARVESTERS_GATEWAY': 'http://localhost:8775',
    'HEALING_ORCHESTRATOR': 'http://localhost:8776',
    'MASTER_ORCHESTRATOR_HUB': 'http://localhost:8777',
    'MEMORY_ORCHESTRATION_SERVER': 'http://localhost:8778',
    'NETWORK_GUARDIAN': 'http://localhost:8779',
    'TRAINERS_GATEWAY': 'http://localhost:8780',
    'VOICE_SYSTEM_HUB': 'http://localhost:8781',
    'WINDOWS_GATEWAY': 'http://localhost:8782',
    'WINDOWS_OPERATIONS': 'http://localhost:8783'
}

@app.route('/')
def serve_gui():
    """Serve the main GUI"""
    return send_file('index.html')

@app.route('/health')
def health():
    """GUI server health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'GUI_BACKEND',
        'cli_bridge': CLI_BRIDGE_URL,
        'mcp_servers': len(MCP_SERVERS)
    })

@app.route('/api/files/list', methods=['POST'])
def list_files():
    """List files in directory"""
    try:
        data = request.json
        path = data.get('path', 'P:\\')
        
        # Validate path exists
        path_obj = Path(path)
        if not path_obj.exists():
            return jsonify({'error': 'Path does not exist'}), 404
        
        items = []
        
        # Add parent directory option
        if path_obj.parent != path_obj:
            items.append({
                'name': '..',
                'type': 'dir',
                'path': str(path_obj.parent)
            })
        
        # List items
        try:
            for item in sorted(path_obj.iterdir()):
                items.append({
                    'name': item.name,
                    'type': 'dir' if item.is_dir() else 'file',
                    'path': str(item)
                })
        except PermissionError:
            return jsonify({'error': 'Permission denied'}), 403
        
        return jsonify({
            'success': True,
            'path': path,
            'items': items
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/files/read', methods=['POST'])
def read_file():
    """Read file contents"""
    try:
        data = request.json
        path = data.get('path')
        
        if not path:
            return jsonify({'error': 'No path provided'}), 400
        
        path_obj = Path(path)
        if not path_obj.exists():
            return jsonify({'error': 'File does not exist'}), 404
        
        if not path_obj.is_file():
            return jsonify({'error': 'Path is not a file'}), 400
        
        with open(path_obj, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        return jsonify({
            'success': True,
            'path': path,
            'content': content,
            'size': path_obj.stat().st_size
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/files/write', methods=['POST'])
def write_file():
    """Write file contents"""
    try:
        data = request.json
        path = data.get('path')
        content = data.get('content', '')
        
        if not path:
            return jsonify({'error': 'No path provided'}), 400
        
        path_obj = Path(path)
        
        # Create parent directories if needed
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path_obj, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return jsonify({
            'success': True,
            'path': path,
            'size': len(content)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mcp/<server>', methods=['POST'])
def mcp_proxy(server):
    """Proxy MCP server requests"""
    try:
        if server not in MCP_SERVERS:
            return jsonify({'error': f'Unknown MCP server: {server}'}), 404
        
        # For now, return placeholder
        # In production, forward to actual MCP server
        return jsonify({
            'success': True,
            'server': server,
            'message': 'MCP server integration coming soon',
            'data': request.json
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/execute', methods=['POST'])
def execute_command():
    """Execute system command"""
    try:
        data = request.json
        command = data.get('command')
        
        if not command:
            return jsonify({'error': 'No command provided'}), 400
        
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return jsonify({
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'exit_code': result.returncode
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Command timeout'}), 408
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mcp/query', methods=['POST'])
def mcp_query():
    """Query an MCP server"""
    try:
        data = request.json
        server = data.get('server', '').upper()
        query_text = data.get('query', '')
        
        if not server or not query_text:
            return jsonify({'error': 'Server and query required'}), 400
        
        if server not in MCP_SERVERS:
            return jsonify({'error': f'Unknown MCP server: {server}'}), 404
        
        # Route query to appropriate MCP server
        mcp_url = MCP_SERVERS[server]
        
        try:
            import requests
            response = requests.post(
                f'{mcp_url}/query',
                json={'query': query_text},
                timeout=30
            )
            
            if response.status_code == 200:
                return jsonify({
                    'success': True,
                    'result': response.json()
                })
            else:
                return jsonify({
                    'success': False,
                    'error': f'MCP server returned status {response.status_code}'
                }), response.status_code
                
        except requests.exceptions.ConnectionError:
            return jsonify({
                'success': False,
                'error': f'MCP server {server} not reachable at {mcp_url}'
            }), 503
        except requests.exceptions.Timeout:
            return jsonify({'success': False, 'error': 'MCP query timeout'}), 408
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/repos', methods=['GET'])
def list_repos():
    """List available repositories"""
    repos = [
        {
            'id': 'ECHO-PRIME-OMEGA',
            'name': 'Bmcbob76/ECHO-PRIME-OMEGA',
            'path': 'P:\\ECHO_PRIME',
            'type': 'local'
        }
    ]
    return jsonify({'success': True, 'repos': repos})

@app.route('/api/system/explorer', methods=['POST'])
def open_explorer():
    """Open Windows Explorer at specified path"""
    try:
        data = request.json
        path = data.get('path', 'P:\\ECHO_PRIME')
        
        # Validate path
        path_obj = Path(path)
        if not path_obj.exists():
            return jsonify({'error': 'Path does not exist'}), 404
        
        # Open Windows Explorer
        if os.name == 'nt':  # Windows
            subprocess.Popen(f'explorer "{path}"')
            return jsonify({
                'success': True,
                'path': path,
                'message': 'Windows Explorer opened'
            })
        else:
            return jsonify({'error': 'Not on Windows system'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/mcp/servers', methods=['GET'])
def get_mcp_servers():
    """Get list of all MCP servers with their status"""
    try:
        # Check which servers are online by trying to connect
        servers_status = []
        for server_name, server_port in MCP_SERVERS.items():
            try:
                # Try to connect to check if online
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex(('localhost', server_port))
                sock.close()
                online = (result == 0)
            except:
                online = False
            
            servers_status.append({
                'name': server_name,
                'port': server_port,
                'online': online
            })
        
        return jsonify({
            'success': True,
            'servers': servers_status,
            'total': len(servers_status)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/mcp/launch', methods=['POST'])
def launch_mcp_server():
    """Launch an MCP server"""
    try:
        data = request.json
        server_name = data.get('server')
        
        if not server_name or server_name not in MCP_SERVERS:
            return jsonify({'error': 'Invalid server name'}), 400
        
        # Map server names to their actual GATEWAYS directory folders
        gateway_map = {
            'developer-gateway': 'DEVELOPER_GATEWAY',
            'windows-gateway': 'WINDOWS_GATEWAY',
            'epcp3o-agent': 'EPCP3O_AGENT',
            'harvesters-gateway': 'HARVESTERS_GATEWAY',
            'gs343-gateway': 'GS343_GATEWAY',
            'voice-system-hub': 'VOICE_SYSTEM_HUB',
            'unified-mcp-master': 'UNIFIED_MCP_MASTER',
            'crystal-memory-hub': 'CRYSTAL_MEMORY_HUB',
            'memory-orchestration': 'MEMORY_ORCHESTRATION_SERVER',
            'network-guardian': 'NETWORK_GUARDIAN',
            'windows-operations': 'WINDOWS_OPERATIONS',
            'master-orchestrator-hub': 'MASTER_ORCHESTRATOR_HUB',
            'healing-orchestrator': 'HEALING_ORCHESTRATOR',
            'trainers-gateway': 'TRAINERS_GATEWAY',
            'ai-research-harvesters': 'AI_RESEARCH_HARVESTERS'
        }
        
        gateway_folder = gateway_map.get(server_name)
        if not gateway_folder:
            return jsonify({'error': 'Server launch not configured'}), 400
        
        gateway_path = Path(f'P:/ECHO_PRIME/MLS_CLEAN/PRODUCTION/GATEWAYS/{gateway_folder}')
        
        # Try multiple common server file patterns
        possible_files = [
            f'{server_name.replace("-", "_")}_http.py',
            f'{gateway_folder.lower()}_http.py',
            'server.py',
            f'{server_name.replace("-", "_")}_mcp.py',
            f'{gateway_folder.lower()}_mcp.py'
        ]
        
        server_file = None
        for filename in possible_files:
            test_file = gateway_path / filename
            if test_file.exists():
                server_file = test_file
                break
        
        if not server_file:
            return jsonify({'error': f'No server file found in {gateway_folder}'}), 404
        
        # Launch server in background
        python_path = 'H:/Tools/python.exe'
        subprocess.Popen(
            [python_path, str(server_file)],
            cwd=str(gateway_path),
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        
        return jsonify({
            'success': True,
            'server': server_name,
            'message': f'{server_name} launched'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/mcp/kill', methods=['POST'])
def kill_mcp_server():
    """Kill an MCP server"""
    try:
        data = request.json
        server_name = data.get('server')
        
        if not server_name or server_name not in MCP_SERVERS:
            return jsonify({'error': 'Invalid server name'}), 400
        
        server_port = MCP_SERVERS[server_name]
        
        # Find and kill process using this port
        import psutil
        for proc in psutil.process_iter(['pid', 'name', 'connections']):
            try:
                for conn in proc.connections():
                    if conn.laddr.port == server_port:
                        proc.kill()
                        return jsonify({
                            'success': True,
                            'server': server_name,
                            'message': f'{server_name} terminated'
                        })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return jsonify({'error': 'Server not found or already stopped'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🎖️ ECHO PRIME - GUI BACKEND SERVER")
    print("="*70)
    print(f"\n📡 GUI Backend: http://localhost:{GUI_PORT}")
    print(f"🌉 CLI Bridge: {CLI_BRIDGE_URL}")
    print(f"🔧 MCP Servers: {len(MCP_SERVERS)} available")
    print(f"\n🌐 Open in browser: http://localhost:{GUI_PORT}")
    print("\n🚀 Server starting...\n")
    print("="*70 + "\n")
    
    app.run(host='0.0.0.0', port=GUI_PORT, debug=False)
