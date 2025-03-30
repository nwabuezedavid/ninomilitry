/**
 * NATO MILITARY - Animations and Interactions
 * This file contains all the JavaScript functionality for animations,
 * transitions, and interactive elements on the NATO MILITARY website.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            if (this.getAttribute('href') === '#') return;
            
            e.preventDefault();
            const targetId = this.getAttribute('href');
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Animate elements when they come into view
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.card-hover, .animate-on-scroll');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementPosition < windowHeight - 100) {
                element.classList.add('animate-fadeIn');
            }
        });
    };

    // Run animation check on load and scroll
    animateOnScroll();
    window.addEventListener('scroll', animateOnScroll);

    // Mobile menu toggle animation
    const mobileMenuButton = document.querySelector('[x-data]');
    if (mobileMenuButton) {
        // Alpine.js handles this, no additional JS needed
    }

    // Form validation visual feedback
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (this.value.trim() !== '') {
                    this.classList.add('border-green-500');
                } else {
                    this.classList.remove('border-green-500');
                }
            });
        });
    });

    // Image preview for file uploads
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            const file = this.files[0];
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                const parent = this.closest('div');
                let preview = parent.querySelector('.file-preview');
                
                if (!preview) {
                    preview = document.createElement('div');
                    preview.className = 'file-preview mt-2';
                    parent.appendChild(preview);
                }
                
                reader.onload = function(e) {
                    preview.innerHTML = `
                        <div class="relative w-24 h-24 rounded-full overflow-hidden border border-gray-300">
                            <img src="${e.target.result}" alt="Preview" class="w-full h-full object-cover">
                        </div>
                    `;
                };
                
                reader.readAsDataURL(file);
            }
        });
    });

    // Auto-resize textarea
    const autoResizeTextareas = document.querySelectorAll('textarea.auto-resize');
    autoResizeTextareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
        
        // Trigger on load
        textarea.dispatchEvent(new Event('input'));
    });

    // Slug generator for post creation
    const titleInput = document.getElementById('id_title');
    const slugInput = document.getElementById('id_slug');
    
    if (titleInput && slugInput) {
        titleInput.addEventListener('blur', function() {
            // Only generate slug if it's empty
            if (slugInput.value === '') {
                const titleValue = titleInput.value.trim();
                if (titleValue) {
                    // Create slug: lowercase, replace spaces with hyphens, remove special chars
                    const slug = titleValue
                        .toLowerCase()
                        .replace(/[^\w\s-]/g, '')
                        .replace(/\s+/g, '-')
                        .replace(/-+/g, '-');
                    
                    slugInput.value = slug;
                }
            }
        });
    }

    // Comment form toggle
    const commentToggle = document.getElementById('comment-toggle');
    const commentForm = document.getElementById('comment-form');
    
    if (commentToggle && commentForm) {
        commentToggle.addEventListener('click', function(e) {
            e.preventDefault();
            commentForm.classList.toggle('hidden');
            
            if (!commentForm.classList.contains('hidden')) {
                commentForm.querySelector('textarea').focus();
                this.textContent = 'Cancel';
            } else {
                this.textContent = 'Add a Comment';
            }
        });
    }

    // Notification dismissal
    const notifications = document.querySelectorAll('.notification');
    notifications.forEach(notification => {
        const dismissButton = notification.querySelector('.dismiss-notification');
        if (dismissButton) {
            dismissButton.addEventListener('click', function() {
                notification.classList.add('opacity-0');
                setTimeout(() => {
                    notification.remove();
                }, 300);
            });
            
            // Auto dismiss after 5 seconds
            setTimeout(() => {
                notification.classList.add('opacity-0');
                setTimeout(() => {
                    notification.remove();
                }, 300);
            }, 5000);
        }
    });

    // Tab functionality
    const tabLinks = document.querySelectorAll('.tab-link');
    const tabContents = document.querySelectorAll('.tab-content');
    
    if (tabLinks.length && tabContents.length) {
        tabLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Remove active class from all tabs
                tabLinks.forEach(tab => {
                    tab.classList.remove('active', 'border-blue-500', 'text-blue-600');
                    tab.classList.add('border-transparent', 'text-gray-500');
                });
                
                // Add active class to clicked tab
                this.classList.add('active', 'border-blue-500', 'text-blue-600');
                this.classList.remove('border-transparent', 'text-gray-500');
                
                // Hide all tab contents
                tabContents.forEach(content => {
                    content.classList.add('hidden');
                    content.classList.remove('active');
                });
                
                // Show the corresponding tab content
                const targetId = this.getAttribute('href').substring(1);
                const targetContent = document.getElementById(targetId);
                if (targetContent) {
                    targetContent.classList.remove('hidden');
                    targetContent.classList.add('active');
                }
            });
        });
    }

    // Dropdown menus
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const dropdown = this.nextElementSibling;
            
            // Close all other dropdowns
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                if (menu !== dropdown) {
                    menu.classList.add('hidden');
                }
            });
            
            // Toggle this dropdown
            dropdown.classList.toggle('hidden');
        });
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', function() {
        document.querySelectorAll('.dropdown-menu').forEach(menu => {
            menu.classList.add('hidden');
        });
    });

    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('.confirm-delete');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // Back to top button
    const backToTopButton = document.getElementById('back-to-top');
    
    if (backToTopButton) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopButton.classList.remove('hidden');
                backToTopButton.classList.add('flex');
            } else {
                backToTopButton.classList.add('hidden');
                backToTopButton.classList.remove('flex');
            }
        });
        
        backToTopButton.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // Print article functionality
    const printButton = document.getElementById('print-article');
    
    if (printButton) {
        printButton.addEventListener('click', function(e) {
            e.preventDefault();
            window.print();
        });
    }

    // Share functionality
    const shareButtons = document.querySelectorAll('.share-button');
    
    if (shareButtons.length && navigator.share) {
        shareButtons.forEach(button => {
            button.classList.remove('hidden');
            
            button.addEventListener('click', async function(e) {
                e.preventDefault();
                
                const title = this.getAttribute('data-title');
                const url = this.getAttribute('data-url');
                
                try {
                    await navigator.share({
                        title: title,
                        url: url
                    });
                } catch (err) {
                    console.error('Share failed:', err);
                }
            });
        });
    }

    // Lazy load images
    if ('loading' in HTMLImageElement.prototype) {
        // Browser supports native lazy loading
        const lazyImages = document.querySelectorAll('img[loading="lazy"]');
        lazyImages.forEach(img => {
            img.src = img.dataset.src;
        });
    } else {
        // Fallback for browsers that don't support lazy loading
        const lazyImageObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    const lazyImage = entry.target;
                    lazyImage.src = lazyImage.dataset.src;
                    lazyImageObserver.unobserve(lazyImage);
                }
            });
        });
        
        const lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(function(lazyImage) {
            lazyImageObserver.observe(lazyImage);
        });
    }
});