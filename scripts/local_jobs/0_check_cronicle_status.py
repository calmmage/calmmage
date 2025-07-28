#!/usr/bin/env python3
"""
Cronicle Status Check Job - Monitor Cronicle job scheduler status.

This job:
- Checks if Cronicle server is running via HTTP API
- Verifies Cronicle processes are running
- Reports server status and basic metrics
- Provides guidance for starting Cronicle if needed
"""

import subprocess
import sys
import json
import os
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import socket


def check_cronicle_api(host: str = "localhost", port: int = 3012, timeout: int = 5) -> dict:
    """Check Cronicle API endpoint."""
    api_url = f"http://{host}:{port}"
    
    try:
        # Try to connect to the API endpoint
        with urlopen(f"{api_url}/api/app/get_status", timeout=timeout) as response:
            if response.status == 200:
                try:
                    data = json.loads(response.read().decode())
                    return {
                        "status": "running",
                        "url": api_url,
                        "response_code": response.status,
                        "server_data": data,
                        "error": None
                    }
                except json.JSONDecodeError:
                    return {
                        "status": "running_no_data",
                        "url": api_url,
                        "response_code": response.status,
                        "error": "API responded but returned invalid JSON"
                    }
            else:
                return {
                    "status": "error",
                    "url": api_url,
                    "response_code": response.status,
                    "error": f"API returned HTTP {response.status}"
                }
                
    except HTTPError as e:
        return {
            "status": "http_error",
            "url": api_url,
            "response_code": e.code,
            "error": f"HTTP error {e.code}: {e.reason}"
        }
    except URLError as e:
        return {
            "status": "connection_failed",
            "url": api_url,
            "error": f"Connection failed: {e.reason}"
        }
    except socket.timeout:
        return {
            "status": "timeout",
            "url": api_url,
            "error": f"Connection timed out after {timeout} seconds"
        }
    except Exception as e:
        return {
            "status": "error",
            "url": api_url,
            "error": f"Unexpected error: {e}"
        }


def check_cronicle_processes() -> dict:
    """Check for running Cronicle processes."""
    try:
        # Look for cronicle processes
        result = subprocess.run(
            ["ps", "aux"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return {
                "processes_found": False,
                "error": "Failed to run ps command"
            }
        
        cronicle_processes = []
        lines = result.stdout.split('\n')
        
        # Look for processes containing 'cronicle' (case insensitive)
        for line in lines:
            if 'cronicle' in line.lower() and 'grep' not in line.lower():
                # Extract useful process info
                parts = line.split()
                if len(parts) >= 11:
                    pid = parts[1]
                    cpu = parts[2]
                    mem = parts[3]
                    command = ' '.join(parts[10:])
                    cronicle_processes.append({
                        "pid": pid,
                        "cpu": cpu,
                        "mem": mem,
                        "command": command[:100] + "..." if len(command) > 100 else command
                    })
        
        return {
            "processes_found": len(cronicle_processes) > 0,
            "process_count": len(cronicle_processes),
            "processes": cronicle_processes,
            "error": None
        }
        
    except subprocess.TimeoutExpired:
        return {
            "processes_found": False,
            "error": "Process check timed out"
        }
    except Exception as e:
        return {
            "processes_found": False,
            "error": f"Process check failed: {e}"
        }


def check_cronicle_port(port: int = 3012) -> dict:
    """Check if Cronicle port is open."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        if result == 0:
            return {
                "port_open": True,
                "port": port,
                "error": None
            }
        else:
            return {
                "port_open": False,
                "port": port,
                "error": f"Port {port} is not accepting connections"
            }
            
    except Exception as e:
        return {
            "port_open": False,
            "port": port,
            "error": f"Port check failed: {e}"
        }


def start_cronicle_server() -> dict:
    """
    Attempt to start Cronicle server using the control script.
    
    Returns:
        dict: Status of the start attempt
    """
    try:
        # Try the standard control script location
        control_script = Path("/opt/cronicle/bin/control.sh")
        
        if not control_script.exists():
            return {
                "started": False,
                "error": f"Cronicle control script not found at {control_script}",
                "suggestion": "Check if Cronicle is installed in a different location"
            }
        
        # Run the start command
        result = subprocess.run(
            [str(control_script), "start"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return {
                "started": True,
                "output": result.stdout.strip(),
                "error": None
            }
        else:
            return {
                "started": False,
                "error": f"Control script failed: {result.stderr.strip()}",
                "output": result.stdout.strip()
            }
            
    except subprocess.TimeoutExpired:
        return {
            "started": False,
            "error": "Cronicle start command timed out after 30 seconds"
        }
    except Exception as e:
        return {
            "started": False,
            "error": f"Failed to start Cronicle: {e}"
        }


def get_cronicle_startup_guidance() -> str:
    """Provide guidance on starting Cronicle."""
    guidance = """
💡 To start Cronicle manually:

1. **Using control script (recommended):**
   - `/opt/cronicle/bin/control.sh start`
   - `/opt/cronicle/bin/control.sh stop`
   - `/opt/cronicle/bin/control.sh restart`

2. **Alternative methods:**
   - `cronicle start` (if globally installed)
   - `node /path/to/cronicle/lib/main.js` (direct start)
   - `pm2 start cronicle` (if using PM2)

3. **Check configuration:**
   - Config file: typically in conf/ directory
   - Default port: 3012 (configurable)
   - Data directory: check logs for storage location

4. **Environment variables:**
   - CRONICLE_URL: {cronicle_url}
   - May need NODE_ENV, port settings, etc.
""".format(
        cronicle_url=os.getenv('CRONICLE_URL', 'not set')
    )
    
    return guidance


def main():
    """Main job function."""
    print("🕒 Cronicle Status Check Starting...")
    print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    
    # Check environment
    cronicle_url = os.getenv('CRONICLE_URL')
    if cronicle_url:
        print(f"🌍 CRONICLE_URL environment variable: {cronicle_url}")
    else:
        print("🌍 CRONICLE_URL environment variable: not set")
    
    # Check API endpoint
    print("\n🔍 Checking Cronicle API...")
    api_status = check_cronicle_api()
    
    if api_status["status"] == "running":
        print("✅ Cronicle API is responding!")
        print(f"   URL: {api_status['url']}")
        print(f"   Response code: {api_status['response_code']}")
        
        # Try to extract useful server info
        if api_status.get("server_data"):
            server_data = api_status["server_data"]
            if isinstance(server_data, dict):
                if "version" in server_data:
                    print(f"   Version: {server_data['version']}")
                if "uptime" in server_data:
                    print(f"   Uptime: {server_data['uptime']} seconds")
                if "hostname" in server_data:
                    print(f"   Hostname: {server_data['hostname']}")
        
    else:
        print("❌ Cronicle API is not responding!")
        print(f"   Status: {api_status['status']}")
        print(f"   Error: {api_status['error']}")
        if api_status.get("url"):
            print(f"   Tried URL: {api_status['url']}")
    
    # Check port
    print("\n🔌 Checking Cronicle port...")
    port_status = check_cronicle_port()
    
    if port_status["port_open"]:
        print(f"✅ Port {port_status['port']} is open and accepting connections")
    else:
        print(f"❌ Port {port_status['port']} is not accessible")
        print(f"   Error: {port_status['error']}")
    
    # Check processes
    print("\n🔍 Checking Cronicle processes...")
    process_status = check_cronicle_processes()
    
    if process_status["processes_found"]:
        print(f"✅ Found {process_status['process_count']} Cronicle process(es)")
        for i, proc in enumerate(process_status["processes"], 1):
            print(f"   Process {i}:")
            print(f"     PID: {proc['pid']}")
            print(f"     CPU: {proc['cpu']}%")
            print(f"     Memory: {proc['mem']}%")
            print(f"     Command: {proc['command']}")
    else:
        print("❌ No Cronicle processes found")
        if process_status.get("error"):
            print(f"   Error: {process_status['error']}")
    
    # Overall status summary
    print("\n📋 Cronicle Status Summary:")
    api_ok = api_status["status"] == "running"
    port_ok = port_status["port_open"]
    process_ok = process_status["processes_found"]
    
    print(f"   API: {'✅ Responding' if api_ok else '❌ Not Responding'}")
    print(f"   Port: {'✅ Open' if port_ok else '❌ Closed'}")
    print(f"   Processes: {'✅ Running' if process_ok else '❌ Not Found'}")
    
    # Determine final status and attempt startup if needed
    if api_ok and port_ok and process_ok:
        print("   🚀 Cronicle is fully operational!")
        print("\n🎯 FINAL STATUS: success")
        if api_status.get("server_data", {}).get("version"):
            print(f"📝 FINAL NOTES: Version {api_status['server_data']['version']}, {process_status['process_count']} process(es)")
        else:
            print(f"📝 FINAL NOTES: {process_status['process_count']} process(es) running")
        return 0
        
    elif process_ok or port_ok:
        print("   ⚠️  Cronicle may be starting up or partially running")
        print("\n🎯 FINAL STATUS: requires_attention")
        print(f"📝 FINAL NOTES: Partially responding - API:{api_ok}, Port:{port_ok}, Process:{process_ok}")
        return 0
        
    else:
        print("   ❌ Cronicle appears to be stopped")
        
        # Attempt to start Cronicle
        print("\n🔄 Attempting to start Cronicle server...")
        start_result = start_cronicle_server()
        
        if start_result["started"]:
            print("✅ Cronicle startup command executed successfully!")
            if start_result.get("output"):
                print(f"   Output: {start_result['output']}")
            
            # Wait a moment and recheck
            print("   ⏳ Waiting 3 seconds for startup...")
            import time
            time.sleep(3)
            
            # Quick recheck of API
            recheck_api = check_cronicle_api(timeout=2)
            if recheck_api["status"] == "running":
                print("   🎉 Cronicle is now responding!")
                print("\n🎯 FINAL STATUS: success")
                print("📝 FINAL NOTES: Was stopped, started successfully using /opt/cronicle/bin/control.sh")
                return 0
            else:
                print("   ⏳ Cronicle may still be starting up...")
                print("\n🎯 FINAL STATUS: requires_attention")
                print("📝 FINAL NOTES: Started but API not responding yet, may need more time")
                return 0
        else:
            print(f"❌ Failed to start Cronicle: {start_result['error']}")
            print(get_cronicle_startup_guidance())
            print("\n🎯 FINAL STATUS: requires_attention")
            print(f"📝 FINAL NOTES: Stopped and auto-start failed - {start_result['error']}")
            return 1


if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        print("\n⚠️  Cronicle check interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n💥 Unexpected error during Cronicle check: {e}")
        sys.exit(1)