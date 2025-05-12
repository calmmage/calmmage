import sys
import os

print(sys.path)
print(os.environ)
print(f"TEST_KEY: {os.getenv('TEST_KEY')}")
