#!/usr/bin/env python3
"""
Test script for the heroicons checker hook
"""
import json
import subprocess
import sys

def run_test(description, content, should_pass=True):
    """Run a test case"""
    input_data = {
        "session_id": "test",
        "tool_name": "Write",
        "tool_input": {
            "file_path": "/path/to/resources/test.blade.php",
            "content": content
        }
    }

    result = subprocess.run(
        [sys.executable, "main.py"],
        input=json.dumps(input_data),
        capture_output=True,
        text=True
    )

    passed = (result.returncode == 0) if should_pass else (result.returncode != 0)
    status = "✓ PASS" if passed else "✗ FAIL"

    print(f"{status}: {description}")
    if result.stderr:
        print(f"      stderr: {result.stderr.strip()}")

    return passed

def main():
    print("Testing heroicons checker...\n")

    all_passed = True

    # Valid icons (should pass)
    print("Valid icon tests:")
    all_passed &= run_test(
        "Valid attribute icon",
        '<flux:button icon="ellipsis-horizontal" />',
        should_pass=True
    )
    all_passed &= run_test(
        "Valid trailing attribute icon",
        '<flux:button icon:trailing="chevron-down">Open</flux:button>',
        should_pass=True
    )
    all_passed &= run_test(
        "Valid component icon",
        '<flux:icon.bolt />',
        should_pass=True
    )
    all_passed &= run_test(
        "Valid component with arrow",
        '<flux:icon.arrow-down />',
        should_pass=True
    )
    all_passed &= run_test(
        "Special 'loading' icon",
        '<flux:input icon:trailing="loading" />',
        should_pass=True
    )
    all_passed &= run_test(
        "Multiple valid icons",
        '<flux:button icon="ellipsis-horizontal" /><flux:icon.bolt /><flux:button icon:trailing="chevron-down" />',
        should_pass=True
    )

    # Invalid icons (should fail)
    print("\nInvalid icon tests:")
    all_passed &= run_test(
        "Invalid attribute icon",
        '<flux:button icon="invalid-icon-name" />',
        should_pass=False
    )
    all_passed &= run_test(
        "Invalid component icon",
        '<flux:icon.fake-icon />',
        should_pass=False
    )
    all_passed &= run_test(
        "Mixed valid and invalid",
        '<flux:button icon="ellipsis-horizontal" /><flux:icon.not-real />',
        should_pass=False
    )

    # Edge cases
    print("\nEdge case tests:")
    all_passed &= run_test(
        "No icon references",
        '<flux:button>Click me</flux:button>',
        should_pass=True
    )
    all_passed &= run_test(
        "Icon with leading space",
        '<flux:icon.arrow-up />',
        should_pass=True
    )

    print("\n" + "="*50)
    if all_passed:
        print("All tests passed! ✓")
        return 0
    else:
        print("Some tests failed! ✗")
        return 1

if __name__ == "__main__":
    sys.exit(main())
