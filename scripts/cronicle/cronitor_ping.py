#!/usr/bin/env python3
"""
Cronicitor Heartbeat Ping Job - Send ping to Cronitor monitoring service.

This job:
- Sends HTTP GET request to Cronitor heartbeat URL
- Reports success/failure status using standardized format
- Designed to be run via Cronicle scheduler to test the complete pipeline

Usage:
    python cronitor_ping.py
    python cronitor_ping.py --timeout 10
"""

import sys
import argparse
from datetime import datetime
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import socket


# Cronitor heartbeat URL - update the app name for this specific job
CRONITOR_URL = "https://cronitor.link/p/5a7f896b06994a358a6232b57e99153d/macbook-python-cronicle-heartbeat"


def ping_cronitor(url: str, timeout: int = 10) -> dict:
    """
    Send ping to Cronitor monitoring service.
    
    Args:
        url: Cronitor heartbeat URL
        timeout: Request timeout in seconds
        
    Returns:
        dict: Status information
    """
    try:
        print(f"📡 Pinging Cronitor: {url}")
        print(f"⏰ Timeout: {timeout} seconds")
        
        with urlopen(url, timeout=timeout) as response:
            response_text = response.read().decode('utf-8')
            
            return {
                "success": True,
                "status_code": response.status,
                "response_text": response_text.strip(),
                "url": url,
                "error": None
            }
            
    except HTTPError as e:
        return {
            "success": False,
            "status_code": e.code,
            "response_text": None,
            "url": url,
            "error": f"HTTP error {e.code}: {e.reason}"
        }
        
    except URLError as e:
        return {
            "success": False,
            "status_code": None,
            "response_text": None,
            "url": url,
            "error": f"URL error: {e.reason}"
        }
        
    except socket.timeout:
        return {
            "success": False,
            "status_code": None,
            "response_text": None,
            "url": url,
            "error": f"Request timed out after {timeout} seconds"
        }
        
    except Exception as e:
        return {
            "success": False,
            "status_code": None,
            "response_text": None,
            "url": url,
            "error": f"Unexpected error: {e}"
        }


def main():
    """Main job function."""
    parser = argparse.ArgumentParser(description="Cronitor heartbeat ping job")
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Request timeout in seconds (default: 10)"
    )
    parser.add_argument(
        "--url",
        type=str,
        default=CRONITOR_URL,
        help="Cronitor heartbeat URL (uses default if not specified)"
    )
    
    args = parser.parse_args()
    
    print("💓 Cronitor Heartbeat Ping Job Starting...")
    print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    print(f"🌐 Target URL: {args.url}")
    
    # Send the ping
    result = ping_cronitor(args.url, args.timeout)
    
    # Report results
    if result["success"]:
        print("✅ Cronitor ping successful!")
        print(f"   Status code: {result['status_code']}")
        if result["response_text"]:
            print(f"   Response: {result['response_text']}")
        
        print("\n🎯 FINAL STATUS: success")
        print(f"📝 FINAL NOTES: Cronitor heartbeat sent successfully (HTTP {result['status_code']})")
        return 0
        
    else:
        print("❌ Cronitor ping failed!")
        print(f"   Error: {result['error']}")
        if result["status_code"]:
            print(f"   Status code: {result['status_code']}")
        
        print("\n🎯 FINAL STATUS: fail")
        print(f"📝 FINAL NOTES: Cronitor heartbeat failed - {result['error']}")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⚠️  Cronitor ping interrupted by user")
        print("\n🎯 FINAL STATUS: fail")
        print("📝 FINAL NOTES: Job interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n💥 Unexpected error during Cronitor ping: {e}")
        print("\n🎯 FINAL STATUS: fail")
        print(f"📝 FINAL NOTES: Unexpected error - {e}")
        sys.exit(1)
