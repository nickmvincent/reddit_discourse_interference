with open('checked_handles.txt', 'r') as handles_file:
    lines = handles_file.read().split('\n')

print(lines)

lines.append('TEST')

with open('checked_handles.txt', 'w') as handles_file:
    handles_file.write('\n'.join(lines))