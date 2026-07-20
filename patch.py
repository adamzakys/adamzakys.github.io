import re

with open('index.html', 'r') as f:
    content = f.read()
    
with open('fix.js', 'r') as f:
    fix_js = f.read()
    
# Find block from // 6. Scratch to // 8. Hacker mode and replace it with fix_js
content = re.sub(r'// 6\. Scratch-to-Reveal.*?// 8\. Hacker Typer Mode', fix_js + '\n    // 8. Hacker Typer Mode', content, flags=re.DOTALL)

navbar_js = """
    // Navbar Interaction (Warp Scroll & Neon Indicator)
    const navLinks = document.querySelectorAll('.nav-links a');
    const navLinksContainer = document.querySelector('.nav-links');
    
    // Create neon indicator
    const indicator = document.createElement('div');
    indicator.style.position = 'absolute';
    indicator.style.bottom = '-4px';
    indicator.style.height = '3px';
    indicator.style.background = 'var(--gradient-main)';
    indicator.style.borderRadius = '4px';
    indicator.style.transition = 'left 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), width 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)';
    indicator.style.boxShadow = '0 0 10px rgba(124, 58, 237, 0.8)';
    indicator.style.pointerEvents = 'none';
    if(navLinksContainer) navLinksContainer.appendChild(indicator);
    
    function updateIndicator(link) {
       if(!link || !indicator) return;
       const rect = link.getBoundingClientRect();
       const parentRect = navLinksContainer.getBoundingClientRect();
       indicator.style.left = (rect.left - parentRect.left) + 'px';
       indicator.style.width = rect.width + 'px';
    }
    
    // Tactile Impact Effect globally
    const interactables = document.querySelectorAll('a, button, .social-pill');
    interactables.forEach(el => {
       el.addEventListener('mousedown', () => {
           el.style.transform = 'scale(0.92)';
           el.style.transition = 'transform 0.1s';
       });
       const resetScale = () => {
           el.style.transform = '';
           el.style.transition = 'transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)';
       };
       el.addEventListener('mouseup', resetScale);
       el.addEventListener('mouseleave', resetScale);
       el.addEventListener('touchend', resetScale);
    });
    
    navLinks.forEach(link => {
       link.addEventListener('mouseenter', () => updateIndicator(link));
       link.addEventListener('click', (e) => {
          updateIndicator(link);
          // Warp Speed Scroll Effect
          document.body.style.filter = 'blur(4px) contrast(1.1)';
          document.body.style.transition = 'filter 0.3s ease-out';
          setTimeout(() => {
             document.body.style.filter = 'none';
          }, 400);
       });
    });
    const activeLink = document.querySelector('.nav-links a.active') || navLinks[0];
    if(activeLink) {
       setTimeout(() => updateIndicator(activeLink), 500);
    }
"""
content = content.replace('// 8. Hacker Typer Mode', navbar_js + '\n    // 8. Hacker Typer Mode')

# Fix nav css since it needs position relative for indicator
content = content.replace('<div class="nav-links">', '<div class="nav-links" style="position:relative;">')

with open('index.html', 'w') as f:
    f.write(content)
