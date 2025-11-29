#!/usr/bin/env python3
import sys
import os

# Automatically add the folder containing this script to Python's path
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from binpy.processer import process

def main():
    if len(sys.argv) < 2:
        print("Usage: bpy <file.bpy>")
        sys.exit(1)
    filepath = sys.argv[1]
    process(filepath)

if __name__ == "__main__":
    main()

