// Camera Surveillance System
const camera = document.querySelector('.camera');
const cameraLight = document.querySelector('.camera-light');
let mouseX = 0;
let mouseY = 0;
let cameraX = 0;
let cameraY = 0;

// Smooth camera movement
function updateCameraPosition() {
    // Smooth interpolation
    cameraX += (mouseX - cameraX) * 0.1;
    cameraY += (mouseY - cameraY) * 0.1;

    camera.style.left = cameraX + 'px';
    camera.style.top = cameraY + 'px';

    requestAnimationFrame(updateCameraPosition);
}

// Track mouse movement
document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX - 30; // Center the camera
    mouseY = e.clientY - 30;
});

// Start camera animation
updateCameraPosition();

// Form Validation & Animation
const form = document.getElementById('registrationForm');
const inputs = document.querySelectorAll('input');

// Input focus effects
inputs.forEach(input => {
    input.addEventListener('focus', function() {
        this.parentElement.style.transform = 'scale(1.02)';
    });

    input.addEventListener('blur', function() {
        this.parentElement.style.transform = 'scale(1)';
    });

    // Real-time validation indicators
    input.addEventListener('input', function() {
        if (this.value.length > 0) {
            this.style.borderColor = 'var(--accent-cyan)';
        } else {
            this.style.borderColor = 'var(--border-color)';
        }

        // Email validation
        if (this.type === 'email' && this.value.length > 0) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (emailRegex.test(this.value)) {
                this.style.borderColor = '#00ff88';
            } else {
                this.style.borderColor = '#ff4444';
            }
        }

        // Password strength indicator
        if (this.type === 'password' && this.value.length > 0) {
            if (this.value.length < 6) {
                this.style.borderColor = '#ff4444';
            } else if (this.value.length < 10) {
                this.style.borderColor = '#ffaa00';
            } else {
                this.style.borderColor = '#00ff88';
            }
        }
    });
});

// Form submission
form.addEventListener('submit', (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Validation
    if (username.length < 3) {
        showNotification('Имя пользователя должно содержать минимум 3 символа', 'error');
        return;
    }

    if (password.length < 6) {
        showNotification('Пароль должен содержать минимум 6 символов', 'error');
        return;
    }

    // Success animation
    const submitBtn = document.querySelector('.submit-btn');
    submitBtn.style.background = 'linear-gradient(135deg, #00ff88, #00cc66)';
    submitBtn.innerHTML = '<span>✓ Успешный вход!</span>';

    setTimeout(() => {
        showNotification('Добро пожаловать в TrackVision!', 'success');
    }, 500);
});

// Notification system
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;

    notification.style.cssText = `
        position: fixed;
        top: 30px;
        right: 30px;
        padding: 15px 25px;
        background: ${type === 'error' ? '#ff4444' : '#00ff88'};
        color: #000;
        border-radius: 4px;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add notification animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Easter egg: Konami code
let konamiCode = [];
const konamiSequence = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];

document.addEventListener('keydown', (e) => {
    konamiCode.push(e.key);
    konamiCode = konamiCode.slice(-10);

    if (konamiCode.join(',') === konamiSequence.join(',')) {
        activateSecurityMode();
    }
});

function activateSecurityMode() {
    const grid = document.querySelector('.surveillance-grid');
    grid.style.backgroundImage = `
        linear-gradient(rgba(255, 0, 0, 0.1) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 0, 0, 0.1) 1px, transparent 1px)
    `;

    showNotification('🚨 РЕЖИМ ПОВЫШЕННОЙ БЕЗОПАСНОСТИ АКТИВИРОВАН', 'error');

    setTimeout(() => {
        grid.style.backgroundImage = `
            linear-gradient(rgba(0, 212, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 212, 255, 0.03) 1px, transparent 1px)
        `;
    }, 5000);
}

// Parallax effect on mouse move
const panel = document.querySelector('.registration-panel');
document.addEventListener('mousemove', (e) => {
    const x = (e.clientX / window.innerWidth - 0.5) * 10;
    const y = (e.clientY / window.innerHeight - 0.5) * 10;
    panel.style.transform = `perspective(1000px) rotateY(${x}deg) rotateX(${-y}deg)`;
});

// Reset transform on mouse leave
document.addEventListener('mouseleave', () => {
    panel.style.transform = 'perspective(1000px) rotateY(0deg) rotateX(0deg)';
});