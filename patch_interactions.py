import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. CSS Updates
css_updates = """
    /* ===================== PLAYABLE INTERACTIONS ===================== */
    .click-ripple {
      position: fixed;
      border-radius: 50%;
      border: 2px solid var(--accent-1);
      pointer-events: none;
      animation: ripple 0.6s cubic-bezier(0.1, 0.9, 0.2, 1) forwards;
      z-index: 9999;
      box-shadow: 0 0 10px var(--accent-1);
    }
    @keyframes ripple {
      0% { width: 0; height: 0; opacity: 1; transform: translate(-50%, -50%); border-width: 4px; }
      100% { width: 120px; height: 120px; opacity: 0; transform: translate(-50%, -50%); border-width: 0px; }
    }
    
    .interactive-impact {
      transition: transform 0.15s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .interactive-impact:active {
      transform: scale(0.92) !important;
    }
    
    .project-slice-cover {
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      z-index: 5;
      background: rgba(15, 23, 42, 0.9);
      backdrop-filter: blur(10px);
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      transition: opacity 0.5s;
      border-radius: inherit;
      color: var(--text-muted);
      font-size: 14px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 2px;
      overflow: hidden;
      cursor: pointer;
    }
    .project-slice-cover::after {
      content: '';
      position: absolute;
      width: 200%; height: 2px;
      background: var(--accent-1);
      transform: rotate(-30deg) translateY(-50px);
      box-shadow: 0 0 10px var(--accent-1);
      opacity: 0;
      transition: opacity 0.2s, transform 0.4s ease-out;
    }
    .project-slice-cover.sliced::after {
      opacity: 1;
      transform: rotate(-30deg) translateY(0);
    }
    .project-slice-cover.sliced {
      animation: shatter 0.8s forwards;
      pointer-events: none;
    }
    @keyframes shatter {
      0% { opacity: 1; transform: scale(1); }
      40% { opacity: 1; transform: scale(1.05) rotate(2deg); filter: brightness(1.5); }
      100% { opacity: 0; transform: scale(1.2) rotate(5deg) translateY(20px); filter: blur(5px); }
    }
    
    .nav-active-indicator {
      position: absolute;
      bottom: -4px;
      height: 3px;
      background: var(--gradient-main);
      border-radius: 4px;
      transition: left 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), width 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
      box-shadow: 0 0 10px rgba(124, 58, 237, 0.6);
      pointer-events: none;
    }
"""

# Replace old ripple and add new stuff
content = re.sub(r'/\* ===================== PLAYABLE INTERACTIONS ===================== \*/.*?(?=\.project-card\.spin)', css_updates, content, flags=re.DOTALL)

# Remove old scratch canvas CSS
content = re.sub(r'\.scratch-wrapper.*?(?=\.typing-text::after)', '', content, flags=re.DOTALL)

# Add nav-active-indicator HTML to nav-links
content = content.replace('<div class="nav-links">', '<div class="nav-links">\n            <div class="nav-active-indicator" id="nav-indicator"></div>')

# 2. Add impact class to a and buttons
content = re.sub(r'<a (.*?)class="([^"]*?)"', r'<a \1class="\2 interactive-impact"', content)
content = re.sub(r'<button (.*?)class="([^"]*?)"', r'<button \1class="\2 interactive-impact"', content)

# 3. Replace Canvas Scratch with Slice Cover
content = re.sub(r'<div class="project-img scratch-wrapper">\s*<canvas class="scratch-canvas"></canvas>', '<div class="project-img">\n                <div class="project-slice-cover"><span>Swipe to Reveal</span></div>', content)
content = content.replace('scratch-wrapper', '')

# 4. Replace JS block
js_update = """
    // 6. Project Slicer (Portfolio)
    const covers = document.querySelectorAll('.project-slice-cover');
    covers.forEach(cover => {
       cover.addEventListener('click', () => {
          cover.classList.add('sliced');
          setTimeout(() => cover.remove(), 800);
       });
       let startX = 0;
       cover.addEventListener('touchstart', (e) => {
          startX = e.touches[0].clientX;
       }, {passive: true});
       cover.addEventListener('touchmove', (e) => {
          if(Math.abs(e.touches[0].clientX - startX) > 40) {
             cover.classList.add('sliced');
             setTimeout(() => cover.remove(), 800);
          }
       }, {passive: true});
    });

    // 7. Jello Elastic Skills
    const skillCards = document.querySelectorAll('.skill-card-v2');
    skillCards.forEach(card => {
       let isDragging = false;
       let startX, startY;
       card.style.transition = 'transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)';
       
       function startDrag(e) {
          isDragging = true;
          const pos = e.touches ? e.touches[0] : e;
          startX = pos.clientX;
          startY = pos.clientY;
          card.style.transition = 'none';
          card.style.zIndex = '100';
       }
       function drag(e) {
          if(!isDragging) return;
          // Don't prevent default, allow scroll. Just stretch slightly.
          const pos = e.touches ? e.touches[0] : e;
          const dx = pos.clientX - startX;
          const dy = pos.clientY - startY;
          
          // Constrain the stretch (rubber band effect)
          const stretchX = dx * 0.2;
          const stretchY = dy * 0.2;
          
          card.style.transform = `translate(${stretchX}px, ${stretchY}px) scale(1.05) rotate(${stretchX * 0.1}deg)`;
       }
       function endDrag() {
          if(!isDragging) return;
          isDragging = false;
          card.style.transition = 'transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)';
          card.style.transform = 'translate(0px, 0px) scale(1) rotate(0deg)';
          card.style.zIndex = '';
       }
       
       card.addEventListener('mousedown', startDrag);
       window.addEventListener('mousemove', drag);
       window.addEventListener('mouseup', endDrag);
       
       card.addEventListener('touchstart', startDrag, {passive: true});
       window.addEventListener('touchmove', drag, {passive: true});
       window.addEventListener('touchend', endDrag);
    });
    
    // Navbar Interaction (Indicator and warp)
    const navLinks = document.querySelectorAll('.nav-links a');
    const indicator = document.getElementById('nav-indicator');
    function updateIndicator(link) {
       if(!link || !indicator) return;
       const rect = link.getBoundingClientRect();
       const parentRect = link.parentElement.getBoundingClientRect();
       indicator.style.left = (rect.left - parentRect.left) + 'px';
       indicator.style.width = rect.width + 'px';
    }
    
    navLinks.forEach(link => {
       link.addEventListener('mouseenter', () => updateIndicator(link));
       link.addEventListener('click', (e) => {
          updateIndicator(link);
          document.body.style.filter = 'blur(3px)';
          setTimeout(() => document.body.style.filter = 'none', 300);
       });
    });
    const activeLink = document.querySelector('.nav-links a.active') || navLinks[0];
    if(activeLink) {
       setTimeout(() => updateIndicator(activeLink), 500);
    }
"""

content = re.sub(r'// 6\. Scratch-to-Reveal.*?// 8\. Hacker Typer Mode', js_update + '\n    // 8. Hacker Typer Mode', content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)
