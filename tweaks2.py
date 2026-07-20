import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Fix Navbar Scrolled Light Mode Bug & Glitch
# Replace `#navbar.scrolled .nav-inner` background and transition properties.
nav_css = """
    #navbar {
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
    }
"""
content = re.sub(r'#navbar\s*\{.*?(?=\.nav-logo)', nav_css, content, flags=re.DOTALL)

# 2. Fix Mobile Nav Menu to Dropdown Pill instead of Side Drawer
mobile_nav_css = """
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
      }

      #nav-menu a {
        font-size: 16px;
        padding: 12px 16px;
        text-align: center;
      }
"""
content = re.sub(r'#nav-menu\s*\{\s*position:\s*fixed;.*?padding:\s*12px\s*16px;\s*\}', mobile_nav_css, content, flags=re.DOTALL)


# 3. Add Slingshot JS & Theme Toggle animation
slingshot_js = """
    // Slingshot (Ketapel) Footer Effect
    let isSlingshotting = false;
    let slingshotStart = 0;
    let slingshotStretch = 0;
    const MAX_STRETCH = 250;
    const bodyEl = document.body;
    
    function updateSlingshot() {
        if(slingshotStretch > 0) {
            // Elastic rubber band pull
            const pull = Math.pow(slingshotStretch, 0.8);
            bodyEl.style.transform = `translateY(${-pull}px)`;
        }
    }
    
    window.addEventListener('touchstart', (e) => {
        const docHeight = document.documentElement.scrollHeight;
        const scrollY = window.scrollY;
        const winHeight = window.innerHeight;
        // Check if we are at the very bottom
        if (scrollY + winHeight >= docHeight - 10) {
            isSlingshotting = true;
            slingshotStart = e.touches[0].clientY;
            slingshotStretch = 0;
            bodyEl.style.transition = 'none';
        }
    }, {passive: true});
    
    window.addEventListener('touchmove', (e) => {
        if (isSlingshotting) {
            const currentY = e.touches[0].clientY;
            const deltaY = slingshotStart - currentY;
            if (deltaY > 0) {
                // Pulling up past the bottom
                slingshotStretch = deltaY;
                if(slingshotStretch > MAX_STRETCH) slingshotStretch = MAX_STRETCH;
                updateSlingshot();
                if (e.cancelable) e.preventDefault();
            }
        }
    }, {passive: false});
    
    window.addEventListener('touchend', () => {
        if (isSlingshotting) {
            isSlingshotting = false;
            bodyEl.style.transition = 'transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)';
            
            // If stretched enough, SHOOT to top!
            if (slingshotStretch > 100) {
                bodyEl.style.transform = `translateY(${window.scrollY}px)`; // shoot up
                setTimeout(() => {
                   window.scrollTo(0, 0);
                   bodyEl.style.transform = 'translateY(0)';
                }, 50);
            } else {
                // Snap back
                bodyEl.style.transform = 'translateY(0)';
            }
            slingshotStretch = 0;
        }
    });

    // Theme Toggle Game-like Animation
    const toggleBtns = document.querySelectorAll('#dark-mode-toggle-desktop, #dark-mode-toggle-mobile');
    toggleBtns.forEach(btn => {
       btn.addEventListener('click', function(e) {
           this.style.transition = 'transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)';
           this.style.transform = 'rotate(360deg) scale(1.2)';
           setTimeout(() => {
               this.style.transition = 'none';
               this.style.transform = 'rotate(0deg) scale(1)';
           }, 500);
           
           // Global shockwave flash
           const flash = document.createElement('div');
           flash.style.position = 'fixed';
           flash.style.top = '0'; flash.style.left = '0';
           flash.style.width = '100vw'; flash.style.height = '100vh';
           flash.style.background = 'var(--text-primary)';
           flash.style.opacity = '0.1';
           flash.style.zIndex = '9999';
           flash.style.pointerEvents = 'none';
           flash.style.transition = 'opacity 0.3s ease-out';
           document.body.appendChild(flash);
           setTimeout(() => flash.style.opacity = '0', 50);
           setTimeout(() => flash.remove(), 400);
       });
    });
"""

content = content.replace('// 8. Hacker Typer Mode', slingshot_js + '\n    // 8. Hacker Typer Mode')

with open('index.html', 'w') as f:
    f.write(content)
