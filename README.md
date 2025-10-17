# Icon Validator Hook

A Claude Code pre-tool hook that validates icon names before writing or editing templates. Supports multiple icon sets (Heroicons, Lucide, FontAwesome) and frameworks (Flux UI, Bootstrap).

## Overview

This hook intercepts `Write` and `Edit` operations targeting Laravel `resources/` paths and validates that any icon names referenced are valid for your chosen icon set and framework. It prevents Claude from accidentally introducing invalid icon names into your components.

## Why Use This?

- **Catch Mistakes Early**: Claude sometimes hallucinates or misremembers icon names. This hook catches those errors before they're written to your files.
- **Multiple Icon Sets**: Validate against Heroicons (324 icons), Lucide (500+ icons), or FontAwesome (1458+ icons).
- **Framework Support**: Works with Flux UI and Bootstrap components with different icon syntaxes.
- **Seamless Integration**: Works transparently as a Claude Code hook—no manual validation needed.

## Installation

1. **Copy the files to your project root:**
   ```bash
   cp heroicon-list.txt lucide-list.txt fontawesome-list.txt main.py /path/to/your/project/
   ```

2. **Update your Claude Code configuration** (`.claude/settings.local.json` or configure via Claude Code settings):

   For Flux UI with Heroicons (default):
   ```json
   {
     "description": "Validate icon names",
     "hooks": {
       "PreToolUse": [
         {
           "matcher": "Write|Edit",
           "hooks": [
             {
               "type": "command",
               "command": "python3 /path/to/main.py",
               "timeout": 3
             }
           ]
         }
       ]
     }
   }
   ```

   For Flux UI with Lucide:
   ```json
   {
     "description": "Validate icon names",
     "hooks": {
       "PreToolUse": [
         {
           "matcher": "Write|Edit",
           "hooks": [
             {
               "type": "command",
               "command": "python3 /path/to/main.py --iconset=lucide",
               "timeout": 3
             }
           ]
         }
       ]
     }
   }
   ```

   For Bootstrap with FontAwesome:
   ```json
   {
     "description": "Validate icon names",
     "hooks": {
       "PreToolUse": [
         {
           "matcher": "Write|Edit",
           "hooks": [
             {
               "type": "command",
               "command": "python3 /path/to/main.py --iconset=fontawesome --framework=bootstrap",
               "timeout": 3
             }
           ]
         }
       ]
     }
   }
   ```

## Configuration

### Icon Sets

Use the `--iconset` flag to specify which icon set to validate against:

- `heroicons` (default) - 324 icons
- `lucide` - 500+ icons
- `fontawesome` - 1458+ icons

### Frameworks

Use the `--framework` flag to specify which component framework you're using:

- `fluxui` (default) - Flux UI components
- `bootstrap` - Bootstrap classes

## How It Works

The hook:

1. Monitors all `Write` and `Edit` operations
2. Filters for files in `resources/` directories (Laravel convention)
3. Extracts icon references based on the framework syntax
4. Validates icon names against the chosen icon set
5. Blocks the operation with an error if invalid icons are found

## Supported Icon Syntaxes

### Flux UI

Icons are referenced using attribute or component syntax:

```blade
<!-- Attribute form -->
<flux:icon icon="star" />
<flux:button icon:trailing="arrow-right">Click me</flux:button>

<!-- Component form -->
<flux:icon.star />
<flux:icon.arrow-right />
```

Works with any icon set: Heroicons, Lucide, or FontAwesome.

### Bootstrap

Icons are referenced using CSS classes with the `bi-` prefix:

```html
<i class="bi-globe"></i>
<button class="btn bi-check">Submit</button>
<span class="bi-alarm"></span>
```

Works with any icon set. Note: Bootstrap Icons officially use this syntax, but this tool validates against any icon set.

## Updating Icon Lists

Run the refresh script to download the latest icons from official sources:

```bash
python3 refresh_icon_lists.py
```

This will update:
- `heroicon-list.txt` from Tailwind Labs GitHub
- `lucide-list.txt` from Lucide GitHub
- `fontawesome-list.txt` from Font Awesome GitHub

## Error Handling

If Claude tries to write invalid icons, you'll see an error like:

```
Error: Invalid Lucide icon names in FLUXUI: fake-icon, not-real-icon
Error: Invalid Fontawesome icon names in BOOTSTRAP: missing-icon
```

The operation will be blocked, and you can then correct Claude or provide the correct icon names.

## Requirements

- Python 3.6+
- Claude Code with hook support
- Icon list files (`heroicon-list.txt`, `lucide-list.txt`, `fontawesome-list.txt`)
- `main.py` in your project root

## License

MIT
