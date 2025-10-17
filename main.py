"""
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  }
}
"""

import json
import os
import sys

def check_valid_heroicons(content):
    """
    Check if the content contains valid heroicon names.
    """
    with open('heroicon-list.txt', 'r') as f:
        heroicon_list = f.read().splitlines()
    results = []
    for icon in content.split():
        if icon not in heroicon_list:
            results.append(icon)
    return results

def main():
    """
    """
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        # Exit code 1 shows stderr to the user but not to Claude
        sys.exit(1)

    tool_name = input_data.get("tool_name", "")
    if tool_name != "Edit|Write":
        sys.exit(0)

    tool_input = input_data.get("tool_input", {})
    command = tool_input.get("file_path", "")
    if 'resources' not in command:
        sys.exit(0)

    content = tool_input.get("content", "")
    if not content:
        sys.exit(0)

    results = check_valid_heroicons(content)
    if not results:
        print(f"Error: Invalid heroicon names: {results.join(', ')}", file=sys.stderr)
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
