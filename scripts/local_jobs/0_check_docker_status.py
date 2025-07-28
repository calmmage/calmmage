#!/usr/bin/env python3
"""
Docker Status Check Job - Monitor Docker daemon status.

This job:
- Checks if Docker daemon is running
- Provides system information about Docker
- Placeholder for starting Docker if needed (requires sudo)
"""

import subprocess
import sys
import json
from datetime import datetime


def check_docker_running() -> dict:
    """Check if Docker daemon is running."""
    try:
        # Try to get Docker info - this will fail if daemon isn't running
        result = subprocess.run(
            ["docker", "info", "--format", "json"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            docker_info = json.loads(result.stdout)
            return {
                "status": "running",
                "version": docker_info.get("ServerVersion", "unknown"),
                "containers_running": docker_info.get("ContainersRunning", 0),
                "containers_total": docker_info.get("Containers", 0),
                "images": docker_info.get("Images", 0),
                "storage_driver": docker_info.get("Driver", "unknown"),
                "memory_total": docker_info.get("MemTotal", 0),
                "error": None
            }
        else:
            return {
                "status": "stopped",
                "error": result.stderr.strip() if result.stderr else "Docker daemon not responding"
            }
            
    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "error": "Docker command timed out - daemon may be starting or unresponsive"
        }
    except FileNotFoundError:
        return {
            "status": "not_installed",
            "error": "Docker command not found - Docker may not be installed"
        }
    except json.JSONDecodeError as e:
        return {
            "status": "error",
            "error": f"Failed to parse Docker info JSON: {e}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": f"Unexpected error checking Docker: {e}"
        }


def start_docker_daemon():
    """
    Placeholder for starting Docker daemon.
    
    TODO: Implement Docker daemon startup logic.
    This requires:
    - sudo privileges or Docker group membership
    - Platform-specific commands (systemctl on Linux, Docker Desktop on macOS, etc.)
    - Proper error handling and waiting for daemon to be ready
    """
    raise NotImplementedError(
        "Docker daemon startup not implemented yet. "
        "Manual intervention required:\n"
        "  - macOS: Start Docker Desktop application\n"
        "  - Linux: sudo systemctl start docker\n"
        "  - Windows: Start Docker Desktop or Docker service"
    )


def check_docker_compose() -> dict:
    """Check if Docker Compose is available."""
    try:
        result = subprocess.run(
            ["docker", "compose", "version", "--format", "json"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            version_info = json.loads(result.stdout)
            return {
                "available": True,
                "version": version_info.get("version", "unknown")
            }
        else:
            # Try legacy docker-compose
            result = subprocess.run(
                ["docker-compose", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return {
                    "available": True,
                    "version": result.stdout.strip(),
                    "type": "legacy"
                }
            
        return {"available": False, "error": "Docker Compose not found"}
        
    except Exception as e:
        return {"available": False, "error": str(e)}


def main():
    """Main job function."""
    print("🐳 Docker Status Check Starting...")
    print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    
    # Check Docker daemon status
    print("\n📊 Checking Docker daemon status...")
    docker_status = check_docker_running()
    
    if docker_status["status"] == "running":
        print("✅ Docker daemon is running!")
        print(f"   Version: {docker_status['version']}")
        print(f"   Containers running: {docker_status['containers_running']}/{docker_status['containers_total']}")
        print(f"   Images: {docker_status['images']}")
        print(f"   Storage driver: {docker_status['storage_driver']}")
        
        if docker_status['memory_total']:
            memory_gb = docker_status['memory_total'] / (1024**3)
            print(f"   Memory available: {memory_gb:.1f} GB")
            
    elif docker_status["status"] == "stopped":
        print("❌ Docker daemon is not running!")
        print(f"   Error: {docker_status['error']}")
        print("   💡 You may need to start Docker manually")
        # Uncomment when implementation is ready:
        # print("   🔄 Attempting to start Docker daemon...")
        # try:
        #     start_docker_daemon()
        #     print("   ✅ Docker daemon started successfully")
        # except NotImplementedError as e:
        #     print(f"   ⚠️  {e}")
        
    elif docker_status["status"] == "not_installed":
        print("❌ Docker is not installed!")
        print(f"   Error: {docker_status['error']}")
        print("   💡 Install Docker from https://docker.com/get-started")
        
    else:
        print(f"❌ Docker status check failed: {docker_status['status']}")
        print(f"   Error: {docker_status['error']}")
    
    # Check Docker Compose availability
    print("\n📦 Checking Docker Compose...")
    compose_status = check_docker_compose()
    
    if compose_status["available"]:
        compose_type = compose_status.get("type", "modern")
        print(f"✅ Docker Compose is available ({compose_type})")
        print(f"   Version: {compose_status['version']}")
    else:
        print("❌ Docker Compose is not available")
        print(f"   Error: {compose_status['error']}")
    
    # Summary with clear status indicators
    print("\n📋 Docker Status Summary:")
    print(f"   Daemon: {'✅ Running' if docker_status['status'] == 'running' else '❌ Not Running'}")
    print(f"   Compose: {'✅ Available' if compose_status['available'] else '❌ Not Available'}")
    
    # Clear final status message for job runner parsing
    if docker_status["status"] == "running":
        print("\n🎯 FINAL STATUS: success")
        print(f"📝 FINAL NOTES: {docker_status['containers_running']}/{docker_status['containers_total']} containers, {docker_status['images']} images")
        return 0
    elif docker_status["status"] == "stopped":
        print("\n🎯 FINAL STATUS: requires_attention")
        print("📝 FINAL NOTES: Daemon not running")
        return 1
    elif docker_status["status"] == "not_installed":
        print("\n🎯 FINAL STATUS: requires_attention")
        print("📝 FINAL NOTES: Not installed")
        return 1
    else:
        print("\n🎯 FINAL STATUS: fail")
        print(f"📝 FINAL NOTES: Check failed - {docker_status['error']}")
        return 1


if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        print("\n⚠️  Docker check interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n💥 Unexpected error during Docker check: {e}")
        sys.exit(1)