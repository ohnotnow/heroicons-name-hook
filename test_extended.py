#!/usr/bin/env python3
"""
Extended test script for multiple frameworks and icon sets
"""
import json
import subprocess
import sys


def run_test(description, content, iconset='heroicons', framework='fluxui', should_pass=True, file_path=None):
    """Run a test case"""
    if file_path is None:
        file_path = "/path/to/resources/test.blade.php"

    input_data = {
        "session_id": "test",
        "tool_name": "Write",
        "tool_input": {
            "file_path": file_path,
            "content": content
        }
    }

    cmd = [sys.executable, "main.py", f"--iconset={iconset}", f"--framework={framework}"]

    result = subprocess.run(
        cmd,
        input=json.dumps(input_data),
        capture_output=True,
        text=True
    )

    passed = (result.returncode == 0) if should_pass else (result.returncode != 0)
    status = "✓ PASS" if passed else "✗ FAIL"

    print(f"{status}: {description}")
    if not passed:
        print(f"      Expected: {'pass' if should_pass else 'fail'}, Got: {'pass' if result.returncode == 0 else 'fail'}")
    if result.stderr and "Warning" not in result.stderr:
        print(f"      stderr: {result.stderr.strip()}")

    return passed


def main():
    print("Extended testing for multiple frameworks and icon sets\n")

    all_passed = True

    # Test Flux UI with different icon sets
    print("=" * 60)
    print("FLUX UI WITH HEROICONS")
    print("=" * 60)
    all_passed &= run_test(
        "Valid Heroicons icon",
        '<flux:icon icon="star" />',
        iconset='heroicons',
        framework='fluxui',
        should_pass=True
    )
    all_passed &= run_test(
        "Invalid Heroicons icon",
        '<flux:icon icon="fake-star" />',
        iconset='heroicons',
        framework='fluxui',
        should_pass=False
    )

    print("\n" + "=" * 60)
    print("FLUX UI WITH LUCIDE")
    print("=" * 60)
    all_passed &= run_test(
        "Valid Lucide icon",
        '<flux:icon icon="check" />',
        iconset='lucide',
        framework='fluxui',
        should_pass=True
    )
    all_passed &= run_test(
        "Valid Lucide component form",
        '<flux:icon.activity />',
        iconset='lucide',
        framework='fluxui',
        should_pass=True
    )
    all_passed &= run_test(
        "Invalid Lucide icon",
        '<flux:icon icon="not-a-lucide-icon" />',
        iconset='lucide',
        framework='fluxui',
        should_pass=False
    )

    print("\n" + "=" * 60)
    print("FLUX UI WITH FONTAWESOME")
    print("=" * 60)
    all_passed &= run_test(
        "Valid FontAwesome icon",
        '<flux:icon icon="star" />',
        iconset='fontawesome',
        framework='fluxui',
        should_pass=True
    )
    all_passed &= run_test(
        "Valid FontAwesome icon (another)",
        '<flux:button icon:trailing="heart">Favorite</flux:button>',
        iconset='fontawesome',
        framework='fluxui',
        should_pass=True
    )
    all_passed &= run_test(
        "Invalid FontAwesome icon",
        '<flux:icon icon="totally-fake" />',
        iconset='fontawesome',
        framework='fluxui',
        should_pass=False
    )

    print("\n" + "=" * 60)
    print("BOOTSTRAP WITH FONTAWESOME")
    print("=" * 60)
    all_passed &= run_test(
        "Valid Bootstrap FontAwesome icon",
        '<i class="bi-star"></i>',
        iconset='fontawesome',
        framework='bootstrap',
        should_pass=True
    )
    all_passed &= run_test(
        "Valid Bootstrap FontAwesome in button",
        '<button class="btn bi-check">Submit</button>',
        iconset='fontawesome',
        framework='bootstrap',
        should_pass=True
    )
    all_passed &= run_test(
        "Multiple classes with icon",
        '<span class="btn btn-primary bi-heart text-danger"></span>',
        iconset='fontawesome',
        framework='bootstrap',
        should_pass=True
    )
    all_passed &= run_test(
        "Invalid Bootstrap icon",
        '<i class="bi-totally-fake"></i>',
        iconset='fontawesome',
        framework='bootstrap',
        should_pass=False
    )

    print("\n" + "=" * 60)
    print("BOOTSTRAP WITH LUCIDE")
    print("=" * 60)
    all_passed &= run_test(
        "Valid Lucide icon in Bootstrap",
        '<i class="bi-check"></i>',
        iconset='lucide',
        framework='bootstrap',
        should_pass=True
    )
    all_passed &= run_test(
        "Invalid Lucide icon in Bootstrap",
        '<i class="bi-not-in-lucide"></i>',
        iconset='lucide',
        framework='bootstrap',
        should_pass=False
    )

    print("\n" + "=" * 60)
    print("BOOTSTRAP WITH HEROICONS")
    print("=" * 60)
    all_passed &= run_test(
        "Valid Heroicons icon in Bootstrap",
        '<i class="bi-arrow-up"></i>',
        iconset='heroicons',
        framework='bootstrap',
        should_pass=True
    )
    all_passed &= run_test(
        "Multiple valid icons",
        '<span class="bi-star"></span><button class="bi-check"></button>',
        iconset='heroicons',
        framework='bootstrap',
        should_pass=True
    )
    all_passed &= run_test(
        "Invalid Heroicons icon in Bootstrap",
        '<i class="bi-made-up-icon"></i>',
        iconset='heroicons',
        framework='bootstrap',
        should_pass=False
    )

    print("\n" + "=" * 60)
    print("EDGE CASES")
    print("=" * 60)
    all_passed &= run_test(
        "No icons (should pass)",
        '<p>Hello world</p>',
        iconset='heroicons',
        framework='fluxui',
        should_pass=True
    )
    all_passed &= run_test(
        "File path without 'resources' (should pass)",
        '<flux:icon icon="fake-icon" />',
        iconset='heroicons',
        framework='fluxui',
        file_path='/path/to/app/test.blade.php',  # Not in resources/
        should_pass=True  # Should pass because file is not in resources/
    )

    print("\n" + "=" * 60)
    if all_passed:
        print("All extended tests passed! ✓")
        return 0
    else:
        print("Some extended tests failed! ✗")
        return 1


if __name__ == "__main__":
    sys.exit(main())
