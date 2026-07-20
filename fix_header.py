import re

with open('index.html', 'r') as f:
    content = f.read()

# Fix the broken CSS
broken_css = """    #navbar.scrolled
    .nav-actions {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-direction: row;
    }

    .nav-inner {"""

fixed_css = """    #navbar.scrolled .nav-inner {
      max-width: 900px;
      width: 90%;
      border-radius: 50px;
      background: var(--glass-bg-strong);
      border: 1px solid var(--glass-border);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }

    .nav-actions {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-direction: row;
    }

    .nav-inner {"""
    
content = content.replace(broken_css, fixed_css)

with open('index.html', 'w') as f:
    f.write(content)
