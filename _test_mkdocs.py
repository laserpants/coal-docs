#!/usr/bin/env python3
"""Test the MkDocs build with debug output for the Shiki extension."""
import sys
sys.path.insert(0, '.')

from markdown import Markdown
from coal_shiki import CoalShikiExtension

# Patch to debug the formatter
import coal_shiki
original_format = coal_shiki.coal_fence_format
def debug_format(*args, **kwargs):
    print(f"  DEBUG coal_fence_format called with args={args}, kwargs={kwargs}")
    result = original_format(*args, **kwargs)
    print(f"  DEBUG coal_fence_format returned: {repr(result[:100])}")
    return result
coal_shiki.coal_fence_format = debug_format

# Simulate what MkDocs does
print("=== Testing with Markdown ===")
md = Markdown(extensions=['pymdownx.superfences', CoalShikiExtension()])

print("\nRegistered extensions:")
for ext in md.registeredExtensions:
    print(f"  - {ext.__class__.__name__}")

# Check superfences config
for ext in md.registeredExtensions:
    if ext.__class__.__name__ == "SuperFencesCodeExtension":
        print(f"\n  SuperFences entries ({len(ext.superfences)}):")
        for sf in ext.superfences:
            print(f"    - name={sf.get('name')}, formatter={sf.get('formatter') is not None}")

# Test conversion
test_md = """```coal
module Main {
  fun main() = 42
}
```"""

print("\n=== Converting ===")
html = md.convert(test_md)
print("\nHTML output:")
print(repr(html))