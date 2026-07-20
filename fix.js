    // 6. Scratch-to-Reveal (Portfolio)
    const scratchWrappers = document.querySelectorAll('.scratch-wrapper');
    scratchWrappers.forEach(wrapper => {
       const canvas = wrapper.querySelector('.scratch-canvas');
       if(!canvas) return;
       const ctx = canvas.getContext('2d');
       
       function initScratch() {
          canvas.width = wrapper.offsetWidth;
          canvas.height = wrapper.offsetHeight;
          
          const gradient = ctx.createLinearGradient(0,0, canvas.width, canvas.height);
          gradient.addColorStop(0, '#1e293b');
          gradient.addColorStop(0.5, '#475569');
          gradient.addColorStop(1, '#1e293b');
          ctx.fillStyle = gradient;
          ctx.fillRect(0, 0, canvas.width, canvas.height);
          
          ctx.font = "bold 20px Inter, sans-serif";
          ctx.fillStyle = "rgba(255,255,255,0.7)";
          ctx.textAlign = "center";
          ctx.fillText("Scratch to Reveal", canvas.width/2, canvas.height/2);
       }
       
       setTimeout(initScratch, 500);
       window.addEventListener('resize', initScratch);
       
       let isDrawing = false;
       let scratchedArea = 0;
       let revealed = false;
       let startScratchX = 0;
       let startScratchY = 0;
       
       function getPos(e) {
          const rect = canvas.getBoundingClientRect();
          if(e.touches) {
             return {x: e.touches[0].clientX - rect.left, y: e.touches[0].clientY - rect.top};
          }
          return {x: e.clientX - rect.left, y: e.clientY - rect.top};
       }
       
       canvas.addEventListener('mousedown', (e)=>{ 
           isDrawing = true; 
           startScratchX = e.clientX; startScratchY = e.clientY;
           scratch(e); 
       });
       
       canvas.addEventListener('touchstart', (e)=>{ 
           isDrawing = true; 
           startScratchX = e.touches[0].clientX; 
           startScratchY = e.touches[0].clientY;
           scratch(e); 
       }, {passive: true});
       
       function scratch(e) {
          if(!isDrawing || revealed) return;
          
          if(e.touches && e.touches.length > 0) {
             const dx = e.touches[0].clientX - startScratchX;
             const dy = e.touches[0].clientY - startScratchY;
             if(Math.abs(dy) > Math.abs(dx) * 1.5) {
                isDrawing = false;
                return;
             }
          }
          
          if(e.cancelable) e.preventDefault();
          
          const pos = getPos(e);
          ctx.globalCompositeOperation = 'destination-out';
          ctx.beginPath();
          ctx.arc(pos.x, pos.y, 40, 0, Math.PI*2);
          ctx.fill();
          
          scratchedArea++; 
          if(scratchedArea > 40) {
             revealed = true;
             canvas.style.transform = 'scale(1.1) rotate(5deg) translateY(20px)';
             canvas.style.filter = 'blur(10px)';
             canvas.style.opacity = '0';
             setTimeout(()=> canvas.remove(), 500);
          }
       }
       
       canvas.addEventListener('mousemove', scratch);
       canvas.addEventListener('mouseup', ()=> isDrawing = false);
       canvas.addEventListener('mouseleave', ()=> isDrawing = false);
       
       canvas.addEventListener('touchmove', scratch, {passive: false});
       canvas.addEventListener('touchend', ()=> isDrawing = false);
    });

    // 7. Gravity Box (Skills)
    const skillsGrid = document.querySelector('.skills-grid');
    const skillCards = document.querySelectorAll('.skill-card-v2');
    if(skillsGrid && skillCards.length > 0) {
       skillsGrid.style.position = 'relative';
       const observer = new IntersectionObserver((entries) => {
          if(entries[0].isIntersecting) {
             observer.disconnect();
             startGravity();
          }
       }, {threshold: 0.3});
       observer.observe(skillsGrid);
       
       let physicsEntities = [];
       
       function startGravity() {
          skillsGrid.style.minHeight = skillsGrid.offsetHeight + 'px';
          
          skillCards.forEach((card, i) => {
             const rect = card.getBoundingClientRect();
             const gridRect = skillsGrid.getBoundingClientRect();
             const initialX = rect.left - gridRect.left;
             const initialY = rect.top - gridRect.top;
             
             card.style.position = 'absolute';
             card.style.margin = '0';
             card.style.left = initialX + 'px';
             card.style.top = '0px';
             card.style.width = card.offsetWidth + 'px';
             card.style.cursor = 'grab';
             
             physicsEntities.push({
                el: card,
                x: initialX,
                y: -300 - (i*150),
                vx: (Math.random() - 0.5) * 8,
                vy: 0,
                width: card.offsetWidth,
                height: card.offsetHeight,
                isDragging: false,
                initialLeft: initialX
             });
             
             let dragStartX, dragStartY, startTime;
             
             function startDrag(e) {
                const entity = physicsEntities[i];
                entity.isDragging = true;
                const pos = e.touches ? e.touches[0] : e;
                dragStartX = pos.clientX;
                dragStartY = pos.clientY;
                startTime = Date.now();
                card.style.zIndex = '100';
                card.style.cursor = 'grabbing';
             }
             
             function drag(e) {
                const entity = physicsEntities[i];
                if(!entity.isDragging) return;
                const pos = e.touches ? e.touches[0] : e;
                const dx = pos.clientX - dragStartX;
                const dy = pos.clientY - dragStartY;
                
                if(e.touches && Math.abs(dy) > Math.abs(dx) * 1.2) {
                    entity.isDragging = false;
                    card.style.zIndex = '';
                    card.style.cursor = 'grab';
                    return;
                }
                
                if(e.cancelable) e.preventDefault();
                
                entity.x += pos.clientX - dragStartX;
                entity.y += pos.clientY - dragStartY;
                dragStartX = pos.clientX;
                dragStartY = pos.clientY;
             }
             
             function endDrag(e) {
                const entity = physicsEntities[i];
                if(!entity.isDragging) return;
                entity.isDragging = false;
                card.style.zIndex = '';
                card.style.cursor = 'grab';
                
                const endTime = Date.now();
                const pos = e.changedTouches ? e.changedTouches[0] : e;
                const timeDelta = Math.max(endTime - startTime, 10);
                
                const vxBoost = (pos.clientX - dragStartX) / timeDelta * 20;
                const vyBoost = (pos.clientY - dragStartY) / timeDelta * 20;
                
                entity.vx += isNaN(vxBoost) ? 0 : Math.max(Math.min(vxBoost, 30), -30);
                entity.vy += isNaN(vyBoost) ? 0 : Math.max(Math.min(vyBoost, 30), -30);
             }
             
             card.addEventListener('mousedown', startDrag);
             window.addEventListener('mousemove', drag, {passive: false});
             window.addEventListener('mouseup', endDrag);
             
             card.addEventListener('touchstart', startDrag, {passive: true});
             window.addEventListener('touchmove', drag, {passive: false});
             window.addEventListener('touchend', endDrag);
          });
          
          function physicsLoop() {
             const bounds = { w: skillsGrid.offsetWidth, h: skillsGrid.offsetHeight };
             
             physicsEntities.forEach(entity => {
                if(entity.isDragging) {
                   entity.el.style.transform = `translate(${entity.x - entity.initialLeft}px, ${entity.y}px) rotate(${entity.vx * 0.5}deg) scale(1.05)`;
                   return;
                }
                
                entity.vy += 0.8;
                entity.vx *= 0.98;
                entity.vy *= 0.98;
                
                entity.x += entity.vx;
                entity.y += entity.vy;
                
                if(entity.y + entity.height > bounds.h) {
                   entity.y = bounds.h - entity.height;
                   entity.vy *= -0.6;
                   entity.vx *= 0.8;
                }
                
                if(entity.y < 0) {
                   entity.y = 0;
                   entity.vy *= -0.6;
                }
                
                if(entity.x < 0) {
                   entity.x = 0;
                   entity.vx *= -0.7;
                } else if (entity.x + entity.width > bounds.w) {
                   entity.x = bounds.w - entity.width;
                   entity.vx *= -0.7;
                }
                
                physicsEntities.forEach(other => {
                   if(other === entity) return;
                   const dx = (entity.x + entity.width/2) - (other.x + other.width/2);
                   const dy = (entity.y + entity.height/2) - (other.y + other.height/2);
                   const dist = Math.sqrt(dx*dx + dy*dy);
                   const minDist = (entity.width + other.width) / 2.2;
                   
                   if(dist < minDist && dist > 0) {
                      const angle = Math.atan2(dy, dx);
                      const push = (minDist - dist) * 0.2;
                      
                      entity.x += Math.cos(angle) * push;
                      entity.y += Math.sin(angle) * push;
                      
                      entity.vx += Math.cos(angle) * push * 0.8;
                      entity.vy += Math.sin(angle) * push * 0.8;
                   }
                });
                
                entity.el.style.transform = `translate(${entity.x - entity.initialLeft}px, ${entity.y}px) rotate(${entity.vx * 0.5}deg)`;
             });
             
             requestAnimationFrame(physicsLoop);
          }
          physicsLoop();
       }
    }
