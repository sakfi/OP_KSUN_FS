with open('user_ascii.txt', 'r', encoding='utf-8') as f:
    lines = f.read().splitlines()

# Trim top and bottom empty lines
while lines and not lines[0].strip():
    lines.pop(0)
while lines and not lines[-1].strip():
    lines.pop()

# Find the minimum indentation of any non-empty line
min_indent = float('inf')
for line in lines:
    if line.strip():
        # Count leading spaces
        indent = len(line) - len(line.lstrip(' '))
        if indent < min_indent:
            min_indent = indent

if min_indent == float('inf'):
    min_indent = 0

print(f"Minimum indent found: {min_indent}")

# Trim that much indent from every line
trimmed_lines = []
for line in lines:
    if not line.strip():
        trimmed_lines.append('')
    else:
        # If a line has fewer spaces for some reason, just lstrip it, but generally we slice
        if len(line) >= min_indent and line[:min_indent].isspace():
            trimmed_lines.append(line[min_indent:])
        else:
            trimmed_lines.append(line.lstrip())

# Print out the trimmed version
print("============== TRIMMED ASCII ==============")
for line in trimmed_lines:
    print(line)

# Let's save the final sed/python replace script string format as well
print("\n============== ACTION PATCH FORMAT ==============")
for line in trimmed_lines:
    safe_line = line.replace('\\', '\\\\').replace('"', '\\"')
    print(f'ui_print "{safe_line}";')
