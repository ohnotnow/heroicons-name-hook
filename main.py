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
import re
import sys


def load_icon_list(icon_set):
    """
    Load icon list for the specified icon set.
    Defaults to heroicons if file not found.
    """
    filename = f"{icon_set}-list.txt"
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            icons = set(f.read().splitlines())
    else:
        print(f"Warning: {filename} not found, falling back to heroicons", file=sys.stderr)
        with open('heroicon-list.txt', 'r') as f:
            icons = set(f.read().splitlines())

    # Add special icons that might be used in flux
    icons.add('loading')
    return icons


def extract_icons_fluxui(content):
    """
    Extract icon names from Flux UI templates.
    Attribute form: icon="icon-name" or icon:trailing="icon-name"
    Component form: <flux:icon.icon-name />
    """
    attribute_pattern = r'icon(?::\w+)?="([^\"]+)"'
    component_pattern = r'<flux:icon\.(\w+(?:-\w+)*)\s*/?>'

    found_icons = re.findall(attribute_pattern, content) + re.findall(component_pattern, content)
    return found_icons


def extract_icons_bootstrap(content):
    """
    Extract icon names from Bootstrap templates.
    Bootstrap uses class="bi-icon-name" pattern.
    """
    # Match bi-icon-name in class attributes
    pattern = r'class="[^"]*\bbi-(\w+(?:-\w+)*)\b[^"]*"'
    found_icons = re.findall(pattern, content)
    return found_icons


def check_valid_icons(content, icon_set, framework):
    """
    Check if the content contains valid icon names for the specified framework and icon set.
    """
    allowed_icons = load_icon_list(icon_set)

    # Extract icons based on framework
    if framework == 'fluxui':
        found_icons = extract_icons_fluxui(content)
    elif framework == 'bootstrap':
        found_icons = extract_icons_bootstrap(content)
    else:
        print(f"Error: Unknown framework: {framework}", file=sys.stderr)
        sys.exit(1)

    # Check for invalid icons
    results = []
    for icon in found_icons:
        if icon not in allowed_icons:
            results.append(icon)

    return results


def parse_hook_args():
    """
    Parse command line arguments from the hook configuration.
    Returns (icon_set, framework) tuple.
    """
    icon_set = 'heroicons'
    framework = 'fluxui'

    # Get arguments from command line
    for arg in sys.argv[1:]:
        if arg.startswith('--iconset='):
            icon_set = arg.split('=', 1)[1]
        elif arg.startswith('--framework='):
            framework = arg.split('=', 1)[1]

    return icon_set, framework


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    tool_name = input_data.get("tool_name", "")
    if tool_name not in ("Edit", "Write"):
        sys.exit(0)

    tool_input = input_data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    if 'resources' not in file_path:
        sys.exit(0)

    content = tool_input.get("content", "")
    if not content:
        sys.exit(0)

    # Parse hook arguments
    icon_set, framework = parse_hook_args()

    # Validate icon names
    results = check_valid_icons(content, icon_set, framework)
    if results:
        icon_set_display = icon_set.capitalize()
        framework_display = framework.upper().replace('UI', ' UI')
        print(f"Error: Invalid {icon_set_display} icon names in {framework_display}: {', '.join(results)}", file=sys.stderr)
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
