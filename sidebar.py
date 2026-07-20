import re

with open('index.html', 'r') as f:
    content = f.read()

# Make sure we remove any border or box-shadow from header/navbar in mobile
header_clean = """
    #navbar {
      border: none !important;
      box-shadow: none !important;
      outline: none !important;
    }
"""

content = content.replace("/* ===================== NAVBAR ===================== */", "/* ===================== NAVBAR ===================== */\n" + header_clean)

# Redesign Mobile Menu to Sidebar
old_mobile_menu = """    @media (max-width: 768px) {
      
      #nav-menu {
        position: absolute;
        top: 100%;
        left: 5%;
        width: 90%;
        max-height: 0;
        overflow: hidden;
        flex-direction: column;
        gap: 8px;
        padding: 0 24px;
        background: var(--glass-bg-strong);
        backdrop-filter: blur(40px);
        border: 1px solid transparent;
        border-radius: 24px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        transition: max-height 0.4s cubic-bezier(0.4, 0, 0.2, 1), padding 0.4s, border-color 0.4s;
        z-index: 90;
      }
      
      #nav-menu.open {
        max-height: 400px;
        padding: 24px;
        border-color: var(--glass-border);
        margin-top: 8px;
      }"""

new_mobile_menu = """    @media (max-width: 768px) {
      
      #nav-menu {
        position: fixed;
        top: 0;
        right: -110%;
        width: 280px;
        height: 100vh;
        max-height: 100vh;
        flex-direction: column;
        justify-content: center;
        gap: 20px;
        padding: 24px;
        background: var(--glass-bg-strong);
        backdrop-filter: blur(40px);
        border-left: 1px solid var(--glass-border);
        border-radius: 30px 0 0 30px;
        box-shadow: -10px 0 40px rgba(0, 0, 0, 0.2);
        transition: right 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
        z-index: 90;
      }
      
      #nav-menu.open {
        right: 0;
      }"""

content = content.replace(old_mobile_menu, new_mobile_menu)

# Ensure the hamburger icon gets transformed into an X when open
# (this might already be in place, but we need to ensure the hamburger itself is above the sidebar)
# It is inside .nav-actions which is inside .nav-inner which is inside #navbar (z-index 100)
# The sidebar z-index is 90, so the hamburger is above it. Perfect.

with open('index.html', 'w') as f:
    f.write(content)

