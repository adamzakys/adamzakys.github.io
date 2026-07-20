import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Fix Navbar Morphing Glitches (Light mode colors)
# We will replace the hardcoded rgba borders with CSS variables and fix the layout morph.
navbar_css = """
    #navbar {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      width: 100%;
      max-width: 100vw;
      z-index: 100;
      padding: 0;
      transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    #navbar.scrolled {
      padding: 16px 24px;
    }
    
    #navbar.scrolled .nav-inner {
      width: 90%;
      border-radius: 50px;
      background: var(--glass-bg-strong);
      border: 1px solid var(--glass-border);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }

    .nav-inner {
      width: 100%;
      max-width: 1200px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--bg-color);
      border: 1px solid transparent;
      border-bottom: 1px solid var(--glass-border);
      border-radius: 0;
      padding: 16px 24px;
      transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
"""
content = re.sub(r'#navbar\s*\{.*?(?=\.nav-logo\s*\{)', navbar_css, content, flags=re.DOTALL)

# 2. Fix Mobile Nav Tab (Match header rounded corners)
mobile_nav_css = """
    @media (max-width: 768px) {
      .nav-links {
        display: none;
      }

      #menu-hamburger {
        display: flex;
      }

      #nav-menu {
        position: absolute;
        top: calc(100% + 10px);
        left: 5%;
        width: 90%;
        background: var(--glass-bg-strong);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 24px;
        padding: 20px;
        display: flex;
        flex-direction: column;
        gap: 16px;
        opacity: 0;
        visibility: hidden;
        transform: translateY(-20px) scale(0.95);
        transform-origin: top;
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
      }

      #nav-menu.open {
        opacity: 1;
        visibility: visible;
        transform: translateY(0) scale(1);
      }
"""
content = re.sub(r'@media \(max-width: 768px\)\s*\{.*?#nav-menu\.open\s*\{.*?\}', mobile_nav_css, content, flags=re.DOTALL)

# 3. Light/Dark Toggle Game-like mechanics & 4. Footer Slingshot
js_inject = """
    // 9. Game-like Theme Toggle (Clipping wipe effect)
    function applyTheme(isDark, e) {
      const isAlreadyDark = document.body.classList.contains('dark');
      if(isDark === isAlreadyDark && !e) return;
      
      if(e && e.clientX) {
         // Create a game-like shockwave / clip-path transition
         const x = e.clientX;
         const y = e.clientY;
         
         const maxDist = Math.max(
           Math.hypot(x, y),
           Math.hypot(window.innerWidth - x, y),
           Math.hypot(x, window.innerHeight - y),
           Math.hypot(window.innerWidth - x, window.innerHeight - y)
         );
         
         document.documentElement.style.setProperty('--clip-size', maxDist + 'px');
         document.documentElement.style.setProperty('--clip-x', x + 'px');
         document.documentElement.style.setProperty('--clip-y', y + 'px');
         
         // Trigger view transition if supported (Chrome 111+)
         if (document.startViewTransition) {
            document.startViewTransition(() => {
               document.body.classList.toggle('dark', isDark);
            });
         } else {
            document.body.classList.toggle('dark', isDark);
         }
      } else {
         document.body.classList.toggle('dark', isDark);
      }
      
      localStorage.setItem('theme', isDark ? 'dark' : 'light');
      const SUN_SVG = `<svg class="dark-toggle-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`;
      const MOON_SVG = `<svg class="dark-toggle-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;
      toggleBtns.forEach(btn => { if (btn) btn.innerHTML = isDark ? MOON_SVG : SUN_SVG; });
    }
    
    // Replace the old applyTheme logic
"""
content = re.sub(r'function applyTheme\(isDark\).*?applyTheme\(!document\.body\.classList\.contains\(\'dark\'\)\);\s*\n\s*\}\);', 
    js_inject + """
    applyTheme(localStorage.getItem('theme') === 'dark');
    toggleBtns.forEach(btn => {
      if (btn) btn.addEventListener('click', (e) => applyTheme(!document.body.classList.contains('dark'), e));
    });
    """, content, flags=re.DOTALL)

# Footer Slingshot
footer_js = """
    // 10. Footer Slingshot (Ketapel)
    let slingshotPull = 0;
    let slingshotStart = 0;
    let isSlingshotting = false;
    
    window.addEventListener('touchstart', (e) => {
       // Only start slingshot if we are at the very bottom
       if(window.innerHeight + window.scrollY >= document.body.offsetHeight - 5) {
          isSlingshotting = true;
          slingshotStart = e.touches[0].clientY;
       }
    }, {passive: true});
    
    window.addEventListener('touchmove', (e) => {
       if(!isSlingshotting) return;
       const currentY = e.touches[0].clientY;
       const diff = slingshotStart - currentY; // Pulling UP means diff > 0
       
       if(diff > 0) {
          // E.preventDefault() here to stop normal bounce, but passive might prevent it. We use transform to stretch.
          slingshotPull = Math.min(diff * 0.5, 150); // Max stretch 150px
          document.body.style.transformOrigin = 'bottom center';
          document.body.style.transform = `scaleY(${1 + slingshotPull/1000})`;
          document.body.style.filter = `sepia(${slingshotPull/200}) hue-rotate(${slingshotPull}deg)`;
       }
    }, {passive: true});
    
    window.addEventListener('touchend', () => {
       if(!isSlingshotting) return;
       isSlingshotting = false;
       
       if(slingshotPull > 80) { // If pulled far enough, CATAPULT!
          document.body.style.transition = 'transform 0.1s cubic-bezier(0.1, 2, 0.5, 1), filter 0.1s';
          document.body.style.transform = 'scaleY(1.3) translateY(-100px)'; // The release snap
          
          setTimeout(() => {
             // Shoot to top
             window.scrollTo({top: 0, left: 0, behavior: 'instant'});
             document.body.style.transition = 'transform 1s cubic-bezier(0.34, 1.56, 0.64, 1)';
             document.body.style.transform = 'scaleY(1) translateY(0)';
             document.body.style.filter = 'none';
          }, 100);
       } else {
          // Snap back gently
          document.body.style.transition = 'transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), filter 0.4s';
          document.body.style.transform = 'scaleY(1)';
          document.body.style.filter = 'none';
       }
       slingshotPull = 0;
       
       setTimeout(() => {
          document.body.style.transition = '';
       }, 1000);
    });
"""

content = content.replace('// 8. Hacker Typer Mode', footer_js + '\n    // 8. Hacker Typer Mode')

# Add view transition css
css_add = """
    /* View Transitions for Theme Toggle */
    ::view-transition-old(root),
    ::view-transition-new(root) {
      animation: none;
      mix-blend-mode: normal;
    }
    ::view-transition-old(root) {
      z-index: 1;
    }
    ::view-transition-new(root) {
      z-index: 9999;
      clip-path: circle(0px at var(--clip-x) var(--clip-y));
      animation: wipe-in 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
    }
    .dark::view-transition-new(root) {
      animation: wipe-in-dark 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
    }
    
    @keyframes wipe-in {
      from { clip-path: circle(0px at var(--clip-x) var(--clip-y)); }
      to { clip-path: circle(var(--clip-size) at var(--clip-x) var(--clip-y)); }
    }
    @keyframes wipe-in-dark {
      from { clip-path: circle(0px at var(--clip-x) var(--clip-y)); }
      to { clip-path: circle(var(--clip-size) at var(--clip-x) var(--clip-y)); }
    }
    
    body {
       overflow-x: hidden;
    }
"""
content = content.replace('/* ===================== HERO ===================== */', css_add + '\n    /* ===================== HERO ===================== */')

with open('index.html', 'w') as f:
    f.write(content)
