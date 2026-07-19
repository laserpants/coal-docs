#!/usr/bin/env python3
import json, subprocess

code = """module Main {
  import IO(println_string)
  fun main() = println_string("Hello, Coal!")
}"""

result = subprocess.run(['node', 'shiki/highlight.mjs'],
    input=json.dumps({'code': code, 'lang': 'coal'}),
    capture_output=True, text=True, timeout=30)
print('STDOUT:', result.stdout[:500])
print('STDERR:', result.stderr[:500] if result.stderr else 'none')