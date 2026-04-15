#!/usr/bin/env python
"""Quick test script to verify CLI structure."""

import sys
import io

# Fix encoding on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from budgetcli.cli import main

def verify_structure():
    """Verify CLI structure is correct."""

    print("✓ Checking CLI structure...")

    # Check main app
    assert main.app is not None, "Main app not found"
    print("  ✓ Main app exists")

    # Check commands
    assert len(main.app.registered_commands) > 0, "No commands registered"
    print(f"  ✓ {len(main.app.registered_commands)} commands registered")

    # Check sub-apps
    assert len(main.app.registered_groups) > 0, "No sub-apps registered"
    print(f"  ✓ {len(main.app.registered_groups)} sub-apps registered")

    # List all commands
    print("\n[COMMANDS]")
    for cmd in main.app.registered_commands:
        print(f"  - {cmd.name}")

    # List all sub-apps and their commands
    print("\n[SUB-APPS]")
    for group in main.app.registered_groups:
        # Access typer_instance (available in Typer 0.9.0+)
        sub_app = getattr(group, 'typer_instance', None)

        if sub_app is None:
            # Fallback: try to access through __click_app__ (Typer internal)
            click_app = getattr(main.app, '__click_app__', None)
            if click_app is not None:
                click_command = click_app.commands.get(group.name)
                if click_command and hasattr(click_command, 'list_commands'):
                    num_commands = len(click_command.list_commands(None))
                    print(f"  - {group.name}: {num_commands} commands")
                    for cmd_name in click_command.list_commands(None):
                        print(f"    • {cmd_name}")
                else:
                    print(f"  - {group.name}: (unable to inspect)")
            continue

        # Use typer_instance to get registered commands
        if hasattr(sub_app, 'registered_commands'):
            num_commands = len(sub_app.registered_commands)
            print(f"  - {group.name}: {num_commands} commands")
            for cmd in sub_app.registered_commands:
                print(f"    • {cmd.name}")
        else:
            print(f"  - {group.name}: (unable to inspect)")


if __name__ == "__main__":
    try:
        verify_structure()
        print("\n[SUCCESS] CLI structure is correct!\n")
        print("Test the CLI with:")
        print("  budget --help")
        print("  budget budget --help")
        print("  budget transaction --help")
        print("  budget report --help")
    except AssertionError as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
