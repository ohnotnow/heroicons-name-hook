# Heroicons Checker Hook

A Claude Code pre-tool hook that validates icon names against the Heroicons library before writing or editing Laravel Flux UI blade templates.

## Overview

This hook intercepts `Write` and `Edit` operations targeting Laravel `resources/` paths and validates that any icon names referenced are valid Heroicons. It prevents Claude from accidentally introducing invalid icon names into your Flux UI components.

## Why Use This?

- **Catch Mistakes Early**: Claude sometimes hallucinates or misremembers icon names. This hook catches those errors before they're written to your files.
- **Maintain Code Quality**: Ensures your blade templates only reference valid Heroicons.
- **Seamless Integration**: Works transparently as a Claude Code hookno manual validation needed.

## Installation

1. **Copy the files to your project root:**
   ```bash
   cp heroicon-list.txt /path/to/your/project/
   ```

2. **Update your Claude Code configuration** (`.claude/settings.local.json` or configure via Claude Code settings):
   ```json
   {
     "description": "Check for invalid heroicon names",
     "hooks": {
       "PreToolUse": [
         {
           "matcher": "Write|Edit",
           "hooks": [
             {
               "type": "command",
               "command": "python3 /path/to/this/main.py",
               "timeout": 3
             }
           ]
         }
       ]
     }
   }
   ```

## How It Works

The hook:

1. Monitors all `Write` and `Edit` operations
2. Filters for files in `resources/` directories (Laravel convention)
3. Extracts icon references from the content using two patterns:
   - **Attribute form**: `icon="icon-name"` or `icon:trailing="icon-name"`
   - **Component form**: `<flux:icon.icon-name />`
4. Validates icon names against the list in `heroicon-list.txt`
5. Blocks the operation with an error if invalid icons are found

## Icon Name Formats Supported

The hook recognizes icons in these contexts:

```blade
<!-- Attribute form -->
<flux:icon icon="star" />
<flux:button icon:trailing="arrow-right">Click me</flux:button>

<!-- Component form -->
<flux:icon.star />
<flux:icon.arrow-right />
```

## Valid Icons

See `heroicon-list.txt` for the complete list of 315+ valid Heroicon names. The hook also recognizes a special `loading` icon that may not be in the standard list.

## Error Handling

If Claude tries to write invalid icons, you'll see an error like:

```
Error: Invalid heroicon names: fake-icon, not-real-icon
```

The operation will be blocked, and you can then correct Claude or provide the correct icon names.

## Requirements

- Python 3.6+
- Claude Code with hook support
- `heroicon-list.txt` in your project root
- `main.py` in your project root

## License

MIT
