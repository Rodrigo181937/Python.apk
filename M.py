import readline
import rlcompleter
import sys
import os
import traceback

# Autocomplete
readline.parse_and_bind("tab: complete")
readline.set_completer(rlcompleter.Completer(namespace={}).complete)

# Terminal colors
RESET = "\033[0m"
PROMPT_COLOR = "\033[92m"   # Green
ERROR_COLOR = "\033[91m"    # Red
INFO_COLOR = "\033[94m"     # Blue

print(f"{PROMPT_COLOR}Mini Python Ultra (Interactive Interpreter){RESET}")
print(f"{INFO_COLOR}Commands: 'runfile <file.py>', 'help', 'graphics_mode', 'exit'{RESET}")

# Persistent environment
env = {}
buffer = []

while True:
    try:
        prompt = f"{PROMPT_COLOR}... {RESET}" if buffer else f"{PROMPT_COLOR}>>> {RESET}"
        line = input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nExiting Mini Python Ultra.")
        break

    if line.lower() in ("exit", "quit"):
        print("Exiting Mini Python Ultra. Goodbye!")
        break
    elif line.startswith("runfile "):
        filename = line.split(maxsplit=1)[1]
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    code_file = f.read()
                exec(code_file, env)
                print(f"{INFO_COLOR}File '{filename}' executed successfully.{RESET}")
            except Exception:
                print(f"{ERROR_COLOR}Error executing file:{RESET}\n{traceback.format_exc()}")
        else:
            print(f"{ERROR_COLOR}File '{filename}' not found.{RESET}")
        continue
    elif line == "graphics_mode":
        try:
            import turtle
            print(f"{INFO_COLOR}Opening graphics mode. Close window to return.{RESET}")
            t = turtle.Turtle()
            turtle.done()
        except Exception:
            print(f"{ERROR_COLOR}Error in graphics mode:{RESET}\n{traceback.format_exc()}")
        continue
    elif line == "help":
        print(f"{INFO_COLOR}Mini Python Ultra Commands:\n"
              "- Regular Python commands\n"
              "- runfile <file.py> to execute scripts\n"
              "- graphics_mode for Turtle graphics\n"
              "- Tab for autocomplete\n"
              "- Up/Down arrows for history\n"
              "- exit to quit{RESET}")
        continue

    buffer.append(line)
    code = "\n".join(buffer)

    try:
        result = eval(code, env)
        if result is not None:
            print(result)
        buffer = []
    except SyntaxError as e:
        if str(e).startswith("unexpected EOF") or str(e).startswith("invalid syntax"):
            continue
        else:
            try:
                exec(code, env)
                buffer = []
            except Exception:
                print(f"{ERROR_COLOR}Error:{RESET}\n{traceback.format_exc()}")
                buffer = []
    except Exception:
        print(f"{ERROR_COLOR}Error:{RESET}\n{traceback.format_exc()}")
        buffer = []
