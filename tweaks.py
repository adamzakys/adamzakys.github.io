import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Remove empty rule
content = re.sub(r'\.nav-actions\s*\{\s*\}', '', content)

# 2. Navbar Floating Pill Design
pill_css = """
    #navbar {
      position: fixed;
      top: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 100%;
      z-index: 1000;
      transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
      background: transparent;
      padding: 24px 5%;
    }

    #navbar.scrolled {
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      padding: 12px 24px;
      margin-top: 16px;
      width: 90%;
      max-width: 800px;
      border-radius: 50px;
      border: 1px solid rgba(255, 255, 255, 0.08);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
"""
content = re.sub(r'#navbar\s*\{.*?(?=\.nav-container)', pill_css, content, flags=re.DOTALL)

# 3. About Quote Animation CSS
quote_anim_css = """
    .about-quote {
      position: relative;
      font-size: 20px;
      font-weight: 500;
      font-style: italic;
      color: var(--text-primary);
      margin-bottom: 24px;
      padding-left: 20px;
      border-left: 3px solid var(--accent-1);
      line-height: 1.6;
      perspective: 1000px;
      transform-style: preserve-3d;
      transition: transform 0.5s ease;
    }
    .about-quote:hover {
      transform: rotateX(10deg) rotateY(10deg);
    }
    
    .glitch-text {
      animation: glitch-skew 1s infinite linear alternate-reverse;
    }
    @keyframes glitch-skew {
      0% { transform: skew(0deg); }
      20% { transform: skew(-5deg); }
      40% { transform: skew(5deg); }
      60% { transform: skew(-2deg); }
      80% { transform: skew(2deg); }
      100% { transform: skew(0deg); }
    }
"""
content = re.sub(r'\.about-quote\s*\{.*?(?=\.about-text)', quote_anim_css, content, flags=re.DOTALL)

# 4. Hero Hint badge
hero_hint = """
        <div class="interactive-hint" style="position: absolute; bottom: 40px; left: 50%; transform: translateX(-50%); display: flex; flex-direction: column; align-items: center; gap: 8px; opacity: 0.6; animation: float 3s ease-in-out infinite;">
          <span style="font-size: 12px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; color: var(--accent-1);">Interactive Experience</span>
          <span style="font-size: 10px; color: var(--text-muted);">Swipe, Tilt, and Drag to Play</span>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--accent-3);">
            <path d="M12 5v14M19 12l-7 7-7-7"/>
          </svg>
        </div>
      </div>
    </section>
"""
content = content.replace('      </div>\n    </section>\n\n    <!-- ========== ABOUT ========== -->', hero_hint + '\n    <!-- ========== ABOUT ========== -->')


# 5. Physics Tweaks (Observer threshold & Terminal button)
content = content.replace('threshold: 0.3', 'threshold: 0.1')
content = content.replace("hackerModeBtn.textContent = 'HACK TO CONNECT';", "hackerModeBtn.textContent = '[ INITIATE SYSTEM OVERRIDE ]';")
content = content.replace("hackerModeBtn.className = 'btn-outline';", "hackerModeBtn.className = 'btn-outline glitch-text';")

# 6. Hero Gyroscope JS & Nav magnetic JS
new_js = """
    // Mobile Gyroscope for Hero Portrait
    const portrait = document.querySelector('.portrait-card');
    if(portrait && window.DeviceOrientationEvent) {
       window.addEventListener('deviceorientation', (e) => {
          if(!e.gamma || !e.beta) return;
          // gamma is left/right (-90 to 90)
          // beta is front/back (-180 to 180)
          const tiltX = Math.max(-20, Math.min(20, e.gamma / 2));
          const tiltY = Math.max(-20, Math.min(20, (e.beta - 45) / 2));
          
          portrait.style.transform = `perspective(1000px) rotateY(${tiltX}deg) rotateX(${-tiltY}deg)`;
       }, true);
    }
    
    // Magnetic Nav Links
    const magneticLinks = document.querySelectorAll('.nav-links a');
    magneticLinks.forEach(link => {
       link.addEventListener('mousemove', (e) => {
          const rect = link.getBoundingClientRect();
          const x = e.clientX - rect.left - rect.width/2;
          const y = e.clientY - rect.top - rect.height/2;
          link.style.transform = `translate(${x * 0.2}px, ${y * 0.2}px) scale(1.1)`;
       });
       link.addEventListener('mouseleave', () => {
          link.style.transform = 'translate(0px, 0px) scale(1)';
       });
    });
"""

content = content.replace('// 8. Hacker Typer Mode', new_js + '\n    // 8. Hacker Typer Mode')

with open('index.html', 'w') as f:
    f.write(content)
