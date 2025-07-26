// Sidebar JavaScript - HealthLife Sistema Clínico

class SidebarManager {
    constructor() {
        this.sidebar = document.getElementById('sidebar');
        this.mainContent = document.getElementById('mainContent');
        this.sidebarToggle = document.getElementById('sidebarToggle');
        this.mobileMenuBtn = document.getElementById('mobileMenuBtn');
        this.sidebarOverlay = document.getElementById('sidebarOverlay');
        this.isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
        this.isMobile = window.innerWidth <= 768;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setInitialState();
        this.setupResponsive();
        this.setupTooltips();
    }

    setupEventListeners() {
        // Toggle del sidebar (desktop)
        if (this.sidebarToggle) {
            this.sidebarToggle.addEventListener('click', () => {
                this.toggleSidebar();
            });
        }

        // Menú móvil
        if (this.mobileMenuBtn) {
            this.mobileMenuBtn.addEventListener('click', () => {
                this.toggleMobileMenu();
            });
        }

        // Overlay para cerrar en móvil
        if (this.sidebarOverlay) {
            this.sidebarOverlay.addEventListener('click', () => {
                this.closeMobileMenu();
            });
        }

        // Cerrar sidebar en móvil al hacer clic en un enlace
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (this.isMobile) {
                    this.closeMobileMenu();
                }
            });
        });

        // Resize listener
        window.addEventListener('resize', () => {
            this.handleResize();
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            this.handleKeyboardShortcuts(e);
        });
    }

    setInitialState() {
        if (this.isCollapsed && !this.isMobile) {
            this.collapseSidebar();
        }
    }

    setupResponsive() {
        this.handleResize();
    }

    setupTooltips() {
        // Agregar data-title a los enlaces para tooltips
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            const text = link.querySelector('span');
            if (text) {
                link.setAttribute('data-title', text.textContent);
            }
        });
    }

    toggleSidebar() {
        if (this.isCollapsed) {
            this.expandSidebar();
        } else {
            this.collapseSidebar();
        }
    }

    collapseSidebar() {
        this.sidebar.classList.add('collapsed');
        this.mainContent.classList.add('expanded');
        this.isCollapsed = true;
        localStorage.setItem('sidebarCollapsed', 'true');
        
        // Animar el contenido
        this.animateContentTransition();
    }

    expandSidebar() {
        this.sidebar.classList.remove('collapsed');
        this.mainContent.classList.remove('expanded');
        this.isCollapsed = false;
        localStorage.setItem('sidebarCollapsed', 'false');
        
        // Animar el contenido
        this.animateContentTransition();
    }

    toggleMobileMenu() {
        if (this.sidebar.classList.contains('active')) {
            this.closeMobileMenu();
        } else {
            this.openMobileMenu();
        }
    }

    openMobileMenu() {
        this.sidebar.classList.add('active');
        this.sidebarOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
        
        // Animar entrada
        this.sidebar.style.animation = 'slideIn 0.3s ease-out';
    }

    closeMobileMenu() {
        this.sidebar.classList.remove('active');
        this.sidebarOverlay.classList.remove('active');
        document.body.style.overflow = '';
        
        // Animar salida
        this.sidebar.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => {
            this.sidebar.style.animation = '';
        }, 300);
    }

    handleResize() {
        const wasMobile = this.isMobile;
        this.isMobile = window.innerWidth <= 768;

        if (wasMobile !== this.isMobile) {
            if (this.isMobile) {
                // Cambió a móvil
                this.sidebar.classList.remove('collapsed');
                this.mainContent.classList.remove('expanded');
                this.closeMobileMenu();
            } else {
                // Cambió a desktop
                if (this.isCollapsed) {
                    this.collapseSidebar();
                }
            }
        }
    }

    handleKeyboardShortcuts(e) {
        // Ctrl/Cmd + B para toggle del sidebar
        if ((e.ctrlKey || e.metaKey) && e.key === 'b') {
            e.preventDefault();
            if (!this.isMobile) {
                this.toggleSidebar();
            }
        }

        // Escape para cerrar menú móvil
        if (e.key === 'Escape' && this.isMobile) {
            this.closeMobileMenu();
        }
    }

    animateContentTransition() {
        // Agregar clase de transición temporal
        this.mainContent.classList.add('transitioning');
        
        setTimeout(() => {
            this.mainContent.classList.remove('transitioning');
        }, 300);
    }

    // Métodos públicos para uso externo
    showLoading() {
        this.sidebar.classList.add('loading');
    }

    hideLoading() {
        this.sidebar.classList.remove('loading');
    }

    // Actualizar información del usuario
    updateUserInfo(userData) {
        const userDetails = document.querySelector('.user-details h6');
        const userRole = document.querySelector('.user-role');
        
        if (userDetails && userData.name) {
            userDetails.textContent = userData.name;
        }
        
        if (userRole && userData.role) {
            userRole.innerHTML = userData.role;
        }
    }

    // Notificaciones en el sidebar
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `sidebar-notification ${type}`;
        notification.innerHTML = `
            <i class="bi bi-${this.getNotificationIcon(type)}"></i>
            <span>${message}</span>
        `;
        
        this.sidebar.appendChild(notification);
        
        // Animar entrada
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        
        // Remover después de 3 segundos
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }

    getNotificationIcon(type) {
        const icons = {
            'success': 'check-circle',
            'error': 'exclamation-triangle',
            'warning': 'exclamation-circle',
            'info': 'info-circle'
        };
        return icons[type] || 'info-circle';
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Verificar si el usuario está autenticado
    const isAuthenticated = document.querySelector('.sidebar') !== null;
    
    if (isAuthenticated) {
        window.sidebarManager = new SidebarManager();
        
        // Agregar estilos adicionales para transiciones
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideOut {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(-100%);
                    opacity: 0;
                }
            }
            
            .main-content.transitioning {
                transition: margin-left 0.3s ease;
            }
            
            .sidebar-notification {
                position: fixed;
                top: 20px;
                right: 20px;
                background: var(--white);
                border-radius: var(--border-radius);
                padding: 12px 16px;
                box-shadow: var(--shadow-medium);
                display: flex;
                align-items: center;
                gap: 8px;
                transform: translateX(100%);
                transition: transform 0.3s ease;
                z-index: 1002;
                max-width: 300px;
            }
            
            .sidebar-notification.show {
                transform: translateX(0);
            }
            
            .sidebar-notification.success {
                border-left: 4px solid var(--medical-green);
            }
            
            .sidebar-notification.error {
                border-left: 4px solid var(--medical-red);
            }
            
            .sidebar-notification.warning {
                border-left: 4px solid #f59e0b;
            }
            
            .sidebar-notification.info {
                border-left: 4px solid var(--primary-blue);
            }
            
            .sidebar-notification i {
                font-size: 1.1rem;
            }
            
            .sidebar-notification.success i {
                color: var(--medical-green);
            }
            
            .sidebar-notification.error i {
                color: var(--medical-red);
            }
            
            .sidebar-notification.warning i {
                color: #f59e0b;
            }
            
            .sidebar-notification.info i {
                color: var(--primary-blue);
            }
        `;
        document.head.appendChild(style);
        
        // Ejemplo de uso de notificaciones
        // window.sidebarManager.showNotification('Sistema actualizado correctamente', 'success');
    }
});

// Exportar para uso en otros módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SidebarManager;
} 