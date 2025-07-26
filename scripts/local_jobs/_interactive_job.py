#!/usr/bin/env python3
"""
Interactive Job - Demo job that hangs, logs info, and has interactive elements.

This job demonstrates:
- Job timeout handling
- Interactive elements (but runs non-interactively in job runner)
- Detailed logging and progress reporting
- Graceful handling when user input is not available
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path


def check_if_interactive() -> bool:
    """Check if we're running in an interactive environment."""
    return sys.stdin.isatty() and sys.stdout.isatty()


def log_system_state():
    """Log detailed system state information."""
    print("📋 System State Analysis:")
    print(f"   Interactive mode: {check_if_interactive()}")
    print(f"   TTY attached: {sys.stdout.isatty()}")
    print(f"   Current user: {os.getenv('USER', 'unknown')}")
    print(f"   Process group ID: {os.getpgrp()}")
    print(f"   Session ID: {os.getsid(0)}")
    
    # Environment analysis
    important_env_vars = [
        'PATH', 'HOME', 'PWD', 'SHELL', 'TERM', 
        'CRONICLE_URL', 'CALMMAGE_DIR'
    ]
    
    print("\n🌍 Environment Variables:")
    for var in important_env_vars:
        value = os.getenv(var, '(not set)')
        # Truncate long paths for readability
        if len(value) > 50:
            value = value[:47] + "..."
        print(f"   {var}: {value}")


def simulate_long_running_task():
    """Simulate a task that takes time and provides progress updates."""
    print("\n⏳ Starting long-running analysis...")
    
    tasks = [
        ("Initializing connections", 2.0),
        ("Scanning file system", 1.5),
        ("Analyzing data patterns", 1.0),
        ("Generating reports", 0.8),
        ("Cleaning up resources", 0.5)
    ]
    
    for i, (task_name, duration) in enumerate(tasks, 1):
        print(f"   [{i}/{len(tasks)}] {task_name}...")
        time.sleep(duration)
        print(f"      ✅ Completed in {duration}s")
    
    print("✨ Long-running analysis completed!")


def attempt_user_interaction():
    """Attempt to interact with user, but handle non-interactive gracefully."""
    print("\n❓ Interactive Section:")
    
    if not check_if_interactive():
        print("   ℹ️  Running in non-interactive mode (job runner context)")
        print("   ⏭️  Skipping user input prompts")
        print("   📝 Would normally ask for configuration preferences")
        print("   🔧 Using default settings for automated execution")
        return
    
    # This code only runs if we're actually interactive
    print("   🤔 This job would normally ask questions like:")
    print("   • Should we enable verbose logging? (y/n)")
    print("   • Which data sources to analyze? (1-5)")
    print("   • Continue with resource-intensive operations? (y/n)")
    
    try:
        # Simulate waiting for input with a timeout
        print("\n   ⏰ Waiting for user input (5 second timeout)...")
        
        # In a real interactive scenario, you might use:
        # import signal
        # def timeout_handler(signum, frame): raise TimeoutError
        # signal.signal(signal.SIGALRM, timeout_handler)
        # signal.alarm(5)
        # user_input = input("   Enter your choice: ")
        
        time.sleep(1)  # Simulate brief wait
        print("   💭 User input timeout - proceeding with defaults")
        
    except Exception as e:
        print(f"   ⚠️  Input error: {e}")
        print("   🔄 Continuing with default configuration")


def generate_detailed_report():
    """Generate a detailed report of job execution."""
    print("\n📊 Execution Report:")
    
    # Calculate some metrics
    start_time = datetime.now()
    current_dir = Path.cwd()
    
    print(f"   📅 Execution date: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   📁 Working directory: {current_dir}")
    print(f"   🖥️  Hostname: {os.getenv('HOSTNAME', 'unknown')}")
    print(f"   🔢 Process ID: {os.getpid()}")
    
    # File system analysis
    try:
        python_files = list(current_dir.glob("**/*.py"))
        config_files = list(current_dir.glob("**/*.yaml")) + list(current_dir.glob("**/*.yml"))
        
        print(f"   🐍 Python files found: {len(python_files)}")
        print(f"   ⚙️  Config files found: {len(config_files)}")
        
        if python_files:
            print(f"   📄 Sample files: {', '.join([f.name for f in python_files[:3]])}")
            
    except Exception as e:
        print(f"   ⚠️  File analysis error: {e}")
    
    print("\n✅ Interactive Job completed with detailed logging!")


def main():
    """Main job function that demonstrates interactive/hanging behavior."""
    print("🔄 Interactive Job Starting...")
    print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    
    # Phase 1: System state logging
    log_system_state()
    
    # Phase 2: Long-running task simulation
    simulate_long_running_task()
    
    # Phase 3: Interactive elements (but handles non-interactive gracefully)
    attempt_user_interaction()
    
    # Phase 4: Detailed reporting
    generate_detailed_report()
    
    print(f"\n🎉 Job execution completed at {datetime.now().isoformat()}")
    return 0


if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        print("\n⚠️  Job interrupted by user")
        sys.exit(130)  # Standard exit code for SIGINT
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)