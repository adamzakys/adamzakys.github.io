import re

with open('index.html', 'r') as f:
    lines = f.readlines()

def get_content():
    return "".join(lines)

content = get_content()

# 1. Navbar Morphing (using exactly matched strings to be safe)
old_navbar = """    #navbar {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      width: 100%;
      max-width: 100vw;
      z-index: 100;
      padding: 0;
      transition: padding 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    #navbar.scrolled {
      padding: 16px 24px;
    }

    #navbar.scrolled .nav-inner {
      max-width: 900px;
      width: 90%;
      border-radius: 50px;
      background: var(--glass-bg-strong);
      border: 1px solid var(--glass-border);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }

    .nav-inner {
      width: 100%;
      max-width: 100%;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--bg-color);
      border: none;
      border-bottom: 1px solid var(--glass-border);
      border-radius: 0;
      padding: 16px 24px;
      transition: max-width 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), border-radius 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), width 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), background 0.3s;
    }"""
    
original_navbar_block = """    #navbar {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      width: 100%;
      max-width: 100vw;
      z-index: 100;
      padding: 0;
      transition: padding 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    #navbar.scrolled {
      padding: 16px 24px;
    }

    #navbar.scrolled .nav-inner {
      max-width: 900px;
      width: 90%;
      border-radius: 50px;
      background: var(--glass-bg-strong);
      border: 1px solid var(--glass-border);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }

    .nav-inner {
      width: 100%;
      max-width: 100%;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--bg-color);
      border: none;
      border-bottom: 1px solid var(--glass-border);
      border-radius: 0;
      padding: 16px 24px;
      transition: max-width 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), border-radius 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), width 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), background 0.3s;
    }"""
# In this case the original is actually different since I reverted. Let me construct the original to replace:
original_navbar_block = """    #navbar {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      width: 100%;
      max-width: 100vw;
      z-index: 100;
      padding: 16px 24px;
      transition: var(--transition-base);
    }

    #navbar.scrolled {
      padding: 10px 24px;
    }

    .nav-inner {
      width: 100%;
      max-width: 1200px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--glass-bg-strong);
      backdrop-filter: blur(32px) saturate(180%);
      -webkit-backdrop-filter: blur(32px) saturate(180%);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-full);
      padding: 10px 20px;
      box-shadow: var(--glass-shadow);
      transition: var(--transition-base);
    }"""

content = content.replace(original_navbar_block, old_navbar)

# 2. Fix Mobile Nav Tab
old_mobile_nav = """      #nav-menu {
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
      
new_mobile_nav = """      #nav-menu {
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
        z-index: 90;
      }

      #nav-menu.open {
        opacity: 1;
        visibility: visible;
        transform: translateY(0) scale(1);
      }"""
content = content.replace(old_mobile_nav, new_mobile_nav)

# 3. Game-like Theme Toggle
old_theme_js = """    function applyTheme(isDark) {
      document.body.classList.toggle('dark', isDark);
      localStorage.setItem('theme', isDark ? 'dark' : 'light');
      toggleBtns.forEach(btn => { if (btn) btn.innerHTML = isDark ? MOON_SVG : SUN_SVG; });
    }

    applyTheme(localStorage.getItem('theme') === 'dark');
    toggleBtns.forEach(btn => {
      if (btn) btn.addEventListener('click', () => applyTheme(!document.body.classList.contains('dark')));
    });"""
    
new_theme_js = """    function applyTheme(isDark, e) {
      const isAlreadyDark = document.body.classList.contains('dark');
      if(isDark === isAlreadyDark && !e) return;
      
      if(e && e.clientX) {
         const x = e.clientX;
         const y = e.clientY;
         const maxDist = Math.max(
           Math.hypot(x, y), Math.hypot(window.innerWidth - x, y),
           Math.hypot(x, window.innerHeight - y), Math.hypot(window.innerWidth - x, window.innerHeight - y)
         );
         
         document.documentElement.style.setProperty('--clip-size', maxDist + 'px');
         document.documentElement.style.setProperty('--clip-x', x + 'px');
         document.documentElement.style.setProperty('--clip-y', y + 'px');
         
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
      toggleBtns.forEach(btn => { if (btn) btn.innerHTML = isDark ? MOON_SVG : SUN_SVG; });
    }

    applyTheme(localStorage.getItem('theme') === 'dark');
    toggleBtns.forEach(btn => {
      if (btn) btn.addEventListener('click', (e) => applyTheme(!document.body.classList.contains('dark'), e));
    });"""
content = content.replace(old_theme_js, new_theme_js)

# 4. View Transitions CSS
css_add = """    /* View Transitions for Theme Toggle */
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
if "/* View Transitions for Theme Toggle */" not in content:
    content = content.replace('/* ===================== HERO ===================== */', css_add + '\n    /* ===================== HERO ===================== */')


# 5. Footer Slingshot
footer_js = """    // 10. Footer Slingshot (Ketapel)
    let slingshotPull = 0;
    let slingshotStart = 0;
    let isSlingshotting = false;
    
    window.addEventListener('touchstart', (e) => {
       if(window.innerHeight + window.scrollY >= document.body.offsetHeight - 5) {
          isSlingshotting = true;
          slingshotStart = e.touches[0].clientY;
       }
    }, {passive: true});
    
    window.addEventListener('touchmove', (e) => {
       if(!isSlingshotting) return;
       const currentY = e.touches[0].clientY;
       const diff = slingshotStart - currentY;
       
       if(diff > 0) {
          slingshotPull = Math.min(diff * 0.5, 150);
          document.body.style.transformOrigin = 'bottom center';
          document.body.style.transform = `scaleY(${1 + slingshotPull/1000})`;
          document.body.style.filter = `sepia(${slingshotPull/200}) hue-rotate(${slingshotPull}deg)`;
       }
    }, {passive: true});
    
    window.addEventListener('touchend', () => {
       if(!isSlingshotting) return;
       isSlingshotting = false;
       
       if(slingshotPull > 80) {
          document.body.style.transition = 'transform 0.1s cubic-bezier(0.1, 2, 0.5, 1), filter 0.1s';
          document.body.style.transform = 'scaleY(1.3) translateY(-100px)';
          
          setTimeout(() => {
             window.scrollTo({top: 0, left: 0, behavior: 'instant'});
             document.body.style.transition = 'transform 1s cubic-bezier(0.34, 1.56, 0.64, 1)';
             document.body.style.transform = 'scaleY(1) translateY(0)';
             document.body.style.filter = 'none';
          }, 100);
       } else {
          document.body.style.transition = 'transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), filter 0.4s';
          document.body.style.transform = 'scaleY(1)';
          document.body.style.filter = 'none';
       }
       slingshotPull = 0;
       setTimeout(() => document.body.style.transition = '', 1000);
    });
"""
if "// 10. Footer Slingshot" not in content:
    content = content.replace('// 8. Hacker Typer Mode', footer_js + '\n    // 8. Hacker Typer Mode')

with open('index.html', 'w') as f:
    f.write(content)
