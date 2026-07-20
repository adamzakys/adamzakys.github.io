import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Desktop Nav Layout (Don't stack Let's Talk and Mode toggle)
# The issue is that `.nav-actions` doesn't have `display: flex; flex-direction: row;`
nav_actions_css = """
    .nav-actions {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-direction: row;
    }
"""
content = re.sub(r'\.nav-inner\s*\{', nav_actions_css + '\n    .nav-inner {', content, count=1)


# 2. Timeline Discrete Jump (Ngeden di setiap titik)
plane_js_new = """      const items = timeline.querySelectorAll('.timeline-item');
      
      let targetNodeIdx = 0;
      let isFlying = false;
      let isNgeden = false;
      
      window.addEventListener('scroll', () => {
        cancelAnimationFrame(idleAnimFrame);
        
        const windowHeight = window.innerHeight;
        const currentScroll = window.scrollY;
        const timelineRect = timeline.getBoundingClientRect();
        
        // Find which item is mostly in view
        let activeIdx = 0;
        items.forEach((item, idx) => {
           const rect = item.getBoundingClientRect();
           // If the item dot is above the middle of the screen
           if (rect.top < windowHeight * 0.6) {
               activeIdx = idx;
           }
        });
        
        // Calculate progress for the glowing trail
        let progress = (windowHeight/2 - timelineRect.top) / timelineRect.height;
        progress = Math.max(0, Math.min(1, progress));
        drawTrail(progress);
        
        // If we need to move to a new node
        if (activeIdx !== targetNodeIdx && !isFlying) {
           targetNodeIdx = activeIdx;
           const targetItem = items[targetNodeIdx];
           
           // Calculate exactly where the dot is relative to timeline top
           // We'll use the item's offsetTop (approximate since timeline is relative)
           const targetY = targetItem.offsetTop + 15; // center of dot roughly
           const centerX = timelineCanvas.width / 2;
           const targetX = centerX + Math.sin(targetY * 0.015) * 12;
           
           isFlying = true;
           isNgeden = true;
           
           // NGEDEN (squash and vibrate) at current position before shooting
           explorer.style.transition = 'transform 0.3s';
           explorer.style.transform = 'scale(1.5, 0.5) translateY(5px)';
           explorer.style.filter = 'drop-shadow(0 0 15px var(--accent-1))';
           
           setTimeout(() => {
              isNgeden = false;
              // SHOOT to new node
              explorer.style.transition = 'top 0.6s cubic-bezier(0.34, 1.56, 0.64, 1), left 0.6s cubic-bezier(0.34, 1.56, 0.64, 1), transform 0.4s';
              explorer.style.top = `${targetY - 16}px`;
              explorer.style.left = `${targetX - 14 - 16}px`;
              explorer.style.transform = 'scale(0.8, 1.2)'; // stretch while flying
              
              setTimeout(() => {
                 isFlying = false;
                 // Settle at target
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
              }, 600);
           }, 400); // 400ms charge up delay
        } else if (!isFlying && !isNgeden && items.length > 0) {
           // On initial load or resize, just position it safely
           const targetItem = items[targetNodeIdx];
           if(targetItem) {
               const targetY = targetItem.offsetTop + 15;
               const centerX = timelineCanvas.width / 2;
               const targetX = centerX + Math.sin(targetY * 0.015) * 12;
               explorer.style.transition = 'top 0.1s, left 0.1s';
               explorer.style.top = `${targetY - 16}px`;
               explorer.style.left = `${targetX - 14 - 16}px`;
           }
        }
      }, { passive: true });
"""

content = re.sub(r'window\.addEventListener\(\'scroll\', \(\) => \{\n\s*cancelAnimationFrame\(idleAnimFrame\);.*?explorer\.style\.left = `\$\{targetX - 14 - 16\}px`;\n\s*\}\n\s*\}, \{ passive: true \}\);', plane_js_new, content, flags=re.DOTALL)

# 3. Mobile Skills Patah-Patah Fix (Cancel drag if scrolling vertically)
# Look inside drag function
cancel_drag_logic = """         function drag(e) {
            if(!isDragging) return;
            const pos = e.touches ? e.touches[0] : e;
            const dx = pos.clientX - startX;
            const dy = pos.clientY - startY;

            if (e.touches && Math.abs(dy) > 15 && Math.abs(dy) > Math.abs(dx)) {
                endDrag();
                return;
            }

            const stretchX = dx * 0.2;"""
content = content.replace("""         function drag(e) {
            if(!isDragging) return;
            // Don't prevent default, allow scroll. Just stretch slightly.
            const pos = e.touches ? e.touches[0] : e;
            const dx = pos.clientX - startX;
            const dy = pos.clientY - startY;

            // Constrain the stretch (rubber band effect)
            const stretchX = dx * 0.2;""", cancel_drag_logic)

with open('index.html', 'w') as f:
    f.write(content)
