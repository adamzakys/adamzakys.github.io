with open('index.html', 'r') as f:
    lines = f.readlines()

# The user's IDE error mentions:
# "Cannot redeclare block-scoped variable 'isSlingshotting'." starts at 3976 and 4067.
# We want to remove the block from 3974 to 4063.
# Wait, let's verify line numbers haven't shifted. I'll search for the exact strings to delete them safely instead of hardcoding lines.

def get_content():
    return "".join(lines)
    
content = get_content()

# Find the block to remove for old slingshot
start_idx = content.find("    // Slingshot (Ketapel) Footer Effect")
end_idx = content.find("        // 10. Footer Slingshot (Ketapel)")

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + content[end_idx:]

with open('index.html', 'w') as f:
    f.write(content)

