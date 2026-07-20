import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Remove border-bottom from .nav-inner so mobile and un-scrolled header have no ugly line
content = content.replace('border-bottom: 1px solid var(--glass-border);', '')

# 2. Dark/Light Mode Icon Style Fix (Remove button-like border/bg)
# It originally had hover states that set border/bg.
content = re.sub(r'#dark-mode-toggle-desktop:hover,.*?\}', """
    #dark-mode-toggle-desktop, #dark-mode-toggle-mobile {
      background: transparent;
      border: none;
      color: var(--text-primary);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 10px;
      border-radius: 50%;
      transition: transform 0.3s, filter 0.3s;
    }
    #dark-mode-toggle-desktop:hover, #dark-mode-toggle-mobile:hover {
      transform: scale(1.15) rotate(15deg);
      filter: drop-shadow(0 0 10px var(--accent-1));
    }
""", content, flags=re.DOTALL)

# Make sure Mobile toggle displays properly in the dropdown (removing border/bg of mobile list item)
content = content.replace('padding:16px 0;', 'padding:8px 0; border:none;')

# 3. Change Timeline Explorer to Plane
plane_svg = """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="transform: rotate(-45deg);">
                 <path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.2-1.1.5l-1.3 2.6c-.3.6.1 1.2.7 1.4l6.1 1.8 1.4 6.1c.2.6.8 1 1.4.7l2.6-1.3c.3-.2.6-.6.5-1.1z"/>
               </svg>"""
content = re.sub(r'<div class="timeline-explorer" id="timeline-explorer">.*?</div>', 
                 f'<div class="timeline-explorer" id="timeline-explorer" style="background:transparent; border:none; box-shadow:none;">\n              {plane_svg}\n            </div>', 
                 content, flags=re.DOTALL)

# 4. Plane Ngeden / Charge Physics
plane_js = """      window.addEventListener('scroll', () => {
        cancelAnimationFrame(idleAnimFrame);
        
        const rect = timeline.getBoundingClientRect();
        const windowHeight = window.innerHeight;
        let progress = (windowHeight/2 - rect.top) / rect.height;
        progress = Math.max(0, Math.min(1, progress));
        currentProgress = progress;
        drawTrail(progress);
        
        const totalH = timeline.offsetHeight;
        const targetY = progress * totalH;
        const centerX = timelineCanvas.width / 2;
        const targetX = centerX + Math.sin(targetY * 0.015) * 12;
        
        if (!isScrolling) {
           // Ngeden (Squash/Charge)
           isScrolling = true;
           explorer.style.transition = 'transform 0.2s';
           explorer.style.transform = 'scale(1.4, 0.6) translateY(5px)';
           explorer.style.filter = 'drop-shadow(0 0 15px var(--accent-1))';
           
           setTimeout(() => {
              // Lepas Landas (Shoot)
              explorer.style.transition = 'top 0.5s cubic-bezier(0.34, 1.56, 0.64, 1), left 0.5s cubic-bezier(0.34, 1.56, 0.64, 1), transform 0.3s';
              explorer.style.top = `${targetY - 16}px`;
              explorer.style.left = `${targetX - 14 - 16}px`;
              explorer.style.transform = 'scale(0.8, 1.2)';
              
              setTimeout(() => {
                 isScrolling = false;
                 explorer.style.transition = 'transform 0.4s';
                 explorer.style.transform = 'rotate(135deg) scale(1)';
                 explorer.style.filter = 'none';
                 
                 idleTime = 0;
                 function idleAnimate() {
                    idleTime += 0.05;
                    const hoverY = Math.sin(idleTime) * 3;
                    const hoverRot = 135 + Math.cos(idleTime) * 5;
                    explorer.style.transform = `translateY(${hoverY}px) rotate(${hoverRot}deg) scale(1)`;
                    idleAnimFrame = requestAnimationFrame(idleAnimate);
                 }
                 idleAnimFrame = requestAnimationFrame(idleAnimate);
              }, 500);
           }, 250);
        } else {
           // If already moving/charging, update target but let current animation finish shooting to new target smoothly
           explorer.style.top = `${targetY - 16}px`;
           explorer.style.left = `${targetX - 14 - 16}px`;
        }
      }, { passive: true });"""
content = re.sub(r'window\.addEventListener\(\'scroll\', \(\) => \{\n\s*cancelAnimationFrame\(idleAnimFrame\);.*?idleAnimate\(\);\n\s*\}, 150\);\n\s*\}, 100\);\n\s*\}, \{ passive: true \}\);', plane_js, content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)
