    document.addEventListener('DOMContentLoaded', () => {

      /* ==========================================
         1. SCROLL PROGRESS & HEADER SHRINK
         ========================================== */
      const header = document.getElementById('header');
      const scrollProgress = document.getElementById('scrollProgress');
      const scrollTopBtn = document.getElementById('scrollTopBtn');

      window.addEventListener('scroll', () => {
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        
        // Progress Bar
        const progress = (scrollTop / docHeight) * 100;
        scrollProgress.style.width = `${progress}%`;

        // Sticky Header shrink
        if (scrollTop > 50) {
          header.classList.add('scrolled');
        } else {
          header.classList.remove('scrolled');
        }

        // Scroll to top visibility
        if (scrollTop > 500) {
          scrollTopBtn.classList.add('active');
        } else {
          scrollTopBtn.classList.remove('active');
        }
      });

      scrollTopBtn.addEventListener('click', () => {
        window.scrollTo({
          top: 0,
          behavior: 'smooth'
        });
      });


      /* ==========================================
         2. LIGHT / DARK THEME SYSTEM
         ========================================== */
      const themeToggleBtn = document.getElementById('themeToggleBtn');

      themeToggleBtn.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const nextTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        document.documentElement.setAttribute('data-theme', nextTheme);
        localStorage.setItem('vane-portfolio-theme', nextTheme);
      });


      /* ==========================================
         3. MOBILE RESPONSIVE HAMBURGER & DRAWER
         ========================================== */
      const hamburgerBtn = document.getElementById('hamburgerBtn');
      const navDrawer = document.getElementById('navDrawer');
      const navOverlay = document.getElementById('navOverlay');
      const drawerLinks = document.querySelectorAll('.nav-drawer-link');

      function toggleMenu() {
        const isOpen = hamburgerBtn.classList.toggle('active');
        navDrawer.classList.toggle('active', isOpen);
        navOverlay.classList.toggle('active', isOpen);
        
        // Toggle accessibility state
        hamburgerBtn.setAttribute('aria-expanded', isOpen);
        
        // Lock body scroll
        document.body.style.overflow = isOpen ? 'hidden' : '';
      }

      function closeMenu() {
        hamburgerBtn.classList.remove('active');
        navDrawer.classList.remove('active');
        navOverlay.classList.remove('active');
        hamburgerBtn.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      }

      hamburgerBtn.addEventListener('click', toggleMenu);
      navOverlay.addEventListener('click', closeMenu);

      drawerLinks.forEach(link => {
        link.addEventListener('click', (e) => {
          closeMenu();
          // Let default smooth scroll happen
        });
      });


      /* ==========================================
         4. ACTIVE NAVBAR LINK HIGHLIGHTING
         ========================================== */
      const sections = document.querySelectorAll('section');
      const navLinks = document.querySelectorAll('.nav-link');

      const activeNavObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const id = entry.target.getAttribute('id');
            
            navLinks.forEach(link => {
              if (link.getAttribute('href') === `#${id}`) {
                link.classList.add('active');
              } else {
                link.classList.remove('active');
              }
            });
          }
        });
      }, {
        rootMargin: '-30% 0px -40% 0px' // Observe when section is in the middle of viewport
      });

      sections.forEach(section => {
        activeNavObserver.observe(section);
      });


      /* ==========================================
         5. SCROLL REVEAL (FADE-IN UP)
         ========================================== */
      const revealElements = document.querySelectorAll('.reveal');

      const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('reveal-visible');
            
            // Unobserve once revealed to keep layout performant
            revealObserver.unobserve(entry.target);
          }
        });
      }, {
        threshold: 0.15,
        rootMargin: '0px 0px -50px 0px' // Trigger slightly before element enters fully
      });

      revealElements.forEach(elem => {
        revealObserver.observe(elem);
      });


      /* ==========================================
         7. CONTACT FORM VALIDATION & MOCK SUBMIT
         ========================================== */
      const contactForm = document.getElementById('contactForm');
      const formSuccessCard = document.getElementById('contactSuccessCard');
      const formSubmitBtn = document.getElementById('formSubmitBtn');
      const formResetBtn = document.getElementById('formResetBtn');

      const nameInput = document.getElementById('formName');
      const emailInput = document.getElementById('formEmail');
      const messageInput = document.getElementById('formMessage');

      const nameError = document.getElementById('nameError');
      const emailError = document.getElementById('emailError');
      const messageError = document.getElementById('messageError');

      // Email regular expression check
      function isValidEmail(email) {
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-e0-9\-]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
      }

      contactForm.addEventListener('submit', (e) => {
        let hasError = false;

        // Reset error feedback
        nameError.style.display = 'none';
        emailError.style.display = 'none';
        messageError.style.display = 'none';

        // Check Name
        if (!nameInput.value.trim()) {
          nameError.style.display = 'inline-flex';
          hasError = true;
        }

        // Check Email
        if (!emailInput.value.trim() || !isValidEmail(emailInput.value)) {
          emailError.style.display = 'inline-flex';
          hasError = true;
        }

        // Check Message
        if (!messageInput.value.trim()) {
          messageError.style.display = 'inline-flex';
          hasError = true;
        }

        if (hasError) {
          e.preventDefault();
          return;
        }

        // Loading indicator state
        formSubmitBtn.disabled = true;
        formSubmitBtn.innerHTML = 'Sending message <i class="fa-solid fa-circle-notch fa-spin"></i>';
      });

      formResetBtn.addEventListener('click', () => {
        formSuccessCard.style.display = 'none';
        contactForm.style.display = 'flex';
        // Clean up URL query parameters so refresh doesn't show success card again
        if (window.location.search.includes('success=True')) {
          const cleanUrl = window.location.pathname + window.location.hash;
          window.history.replaceState({}, document.title, cleanUrl);
        }
      });

      const formErrorResetBtn = document.getElementById('formErrorResetBtn');
      const formErrorCard = document.getElementById('contactErrorCard');

      if (formErrorResetBtn && formErrorCard) {
        formErrorResetBtn.addEventListener('click', () => {
          formErrorCard.style.display = 'none';
          contactForm.style.display = 'flex';
          // Clean up URL query parameters so refresh doesn't show error card again
          if (window.location.search.toLowerCase().includes('error=true')) {
            const cleanUrl = window.location.pathname + window.location.hash;
            window.history.replaceState({}, document.title, cleanUrl);
          }
        });
      }

    });
