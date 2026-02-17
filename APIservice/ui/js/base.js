// ======================
// WAIT FOR DOM TO LOAD
// ======================
document.addEventListener('DOMContentLoaded', function() {

// ======================
// PARTICLE ANIMATION
// ======================
const canvas = document.getElementById('particleCanvas');
const ctx = canvas.getContext('2d');

function resizeCanvas() {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

class Particle {
    constructor() {
        this.reset();
    }

    reset() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.vx = (Math.random() - 0.5) * 0.5;
        this.vy = (Math.random() - 0.5) * 0.5;
        this.radius = Math.random() * 2 + 1;
        this.opacity = Math.random() * 0.5 + 0.2;
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;

        if (this.x < 0) this.x = canvas.width;
        if (this.x > canvas.width) this.x = 0;
        if (this.y < 0) this.y = canvas.height;
        if (this.y > canvas.height) this.y = 0;
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(0, 212, 255, ${this.opacity})`;
        ctx.fill();
    }
}

const particles = [];
const particleCount = 50;

for (let i = 0; i < particleCount; i++) {
    particles.push(new Particle());
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    particles.forEach(particle => {
        particle.update();
        particle.draw();
    });

    particles.forEach((p1, i) => {
        particles.slice(i + 1).forEach(p2 => {
            const dx = p1.x - p2.x;
            const dy = p1.y - p2.y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < 100) {
                ctx.beginPath();
                ctx.moveTo(p1.x, p1.y);
                ctx.lineTo(p2.x, p2.y);
                ctx.strokeStyle = `rgba(0, 212, 255, ${0.2 * (1 - distance / 100)})`;
                ctx.lineWidth = 0.5;
                ctx.stroke();
            }
        });
    });

    requestAnimationFrame(animate);
}

animate();

// ======================
// PROFILE DROPDOWN
// ======================
const profileBtn = document.getElementById('profileBtn');
const profileDropdown = document.getElementById('profileDropdown');

console.log('Profile button:', profileBtn);
console.log('Profile dropdown:', profileDropdown);

if (!profileBtn || !profileDropdown) {
    console.error('Profile elements not found!');
}

profileBtn.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();

    console.log('Profile button clicked!');

    const isActive = profileDropdown.classList.contains('active');

    // Close solutions dropdown if open
    const solutionsDropdown = document.getElementById('solutionsDropdown');
    const solutionsBtn = document.getElementById('solutionsBtn');
    solutionsDropdown.classList.remove('active');

    // Toggle profile dropdown
    if (isActive) {
        profileBtn.classList.remove('active');
        profileDropdown.classList.remove('active');
        console.log('Profile dropdown closed');
    } else {
        profileBtn.classList.add('active');
        profileDropdown.classList.add('active');
        console.log('Profile dropdown opened');
    }
});

// Close dropdowns when clicking outside
document.addEventListener('click', (e) => {
    // Close profile dropdown
    if (!profileBtn.contains(e.target) && !profileDropdown.contains(e.target)) {
        profileBtn.classList.remove('active');
        profileDropdown.classList.remove('active');
    }

    // Close solutions dropdown
    if (!solutionsBtn.contains(e.target) && !solutionsDropdown.contains(e.target)) {
        solutionsDropdown.classList.remove('active');
    }
});

// Profile dropdown item handlers
const dropdownItems = document.querySelectorAll('.dropdown-item');
dropdownItems.forEach(item => {
    item.addEventListener('click', async (e) => {
        e.preventDefault();
        const action = item.getAttribute('data-action');

        profileBtn.classList.remove('active');
        profileDropdown.classList.remove('active');

        switch(action) {
            case 'profile':
                await handleProfileClick();
                break;
            case 'settings':
                await handleSettingsClick();
                break;
            case 'logout':
                await handleLogout();
                break;
        }
    });
});

// API: Profile
async function handleProfileClick() {
    showNotification('Загрузка профиля...', 'info');

    try {
        const response = await fetch('/api/user/profile', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();
        showNotification('Профиль загружен', 'success');
        console.log('Profile data:', data);
        // Redirect or update UI
    } catch (error) {
        showNotification('Ошибка загрузки профиля', 'error');
        console.error('Profile error:', error);
    }
}

// API: Settings
async function handleSettingsClick() {
    showNotification('Открытие настроек...', 'info');

    try {
        const response = await fetch('/api/user/settings', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();
        showNotification('Настройки открыты', 'success');
        console.log('Settings data:', data);
    } catch (error) {
        showNotification('Ошибка загрузки настроек', 'error');
        console.error('Settings error:', error);
    }
}

// API: Logout
async function handleLogout() {
    const confirmation = confirm('Вы уверены, что хотите выйти?');
    if (!confirmation) return;

    showNotification('Выход из системы...', 'info');

    try {
        const response = await fetch('/api/auth/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            document.body.style.opacity = '0';
            document.body.style.transition = 'opacity 0.5s ease';

            setTimeout(() => {
                window.location.href = '/login';
            }, 500);
        }
    } catch (error) {
        showNotification('Ошибка выхода', 'error');
        console.error('Logout error:', error);
    }
}

// ======================
// SOLUTIONS DROPDOWN
// ======================
const solutionsBtn = document.getElementById('solutionsBtn');
const solutionsDropdown = document.getElementById('solutionsDropdown');

console.log('Solutions button:', solutionsBtn);
console.log('Solutions dropdown:', solutionsDropdown);

if (!solutionsBtn || !solutionsDropdown) {
    console.error('Solutions elements not found!');
}

solutionsBtn.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();

    console.log('Solutions button clicked!');

    const isActive = solutionsDropdown.classList.contains('active');

    // Close profile dropdown if open
    profileBtn.classList.remove('active');
    profileDropdown.classList.remove('active');

    // Toggle solutions dropdown
    if (isActive) {
        solutionsDropdown.classList.remove('active');
        console.log('Solutions dropdown closed');
    } else {
        solutionsDropdown.classList.add('active');
        console.log('Solutions dropdown opened');
    }
});

// Close dropdowns when clicking outside
document.addEventListener('click', (e) => {
    // Close profile dropdown
    if (!profileBtn.contains(e.target) && !profileDropdown.contains(e.target)) {
        profileBtn.classList.remove('active');
        profileDropdown.classList.remove('active');
    }

    // Close solutions dropdown
    if (!solutionsBtn.contains(e.target) && !solutionsDropdown.contains(e.target)) {
        solutionsDropdown.classList.remove('active');
    }
});

// Solution items handlers
const solutionItems = document.querySelectorAll('.solution-item');
solutionItems.forEach(item => {
    item.addEventListener('click', async (e) => {
        e.preventDefault();
        const solution = item.getAttribute('data-solution');

        solutionsBtn.classList.remove('active');
        solutionsDropdown.classList.remove('active');

        await handleSolutionClick(solution);
    });
});

// API: Solutions
async function handleSolutionClick(solutionType) {
    showNotification(`Загрузка решения: ${getSolutionName(solutionType)}...`, 'info');

    try {
        const response = await fetch(`/api/solutions/${solutionType}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();
        showNotification(`Решение "${getSolutionName(solutionType)}" загружено`, 'success');
        console.log('Solution data:', data);
        // Redirect or update UI with solution data
    } catch (error) {
        showNotification('Ошибка загрузки решения', 'error');
        console.error('Solution error:', error);
    }
}

function getSolutionName(type) {
    const names = {
        'traffic': 'Камера трафика',
        'restricted': 'Закрытые зоны',
        'parking': 'Управление парковкой',
        'license': 'Скан номеров'
    };
    return names[type] || type;
}

// ======================
// CHAT WIDGET
// ======================
const chatToggle = document.getElementById('chatToggle');
const chatContainer = document.getElementById('chatContainer');
const chatInput = document.getElementById('chatInput');
const chatSend = document.getElementById('chatSend');
const chatMessages = document.getElementById('chatMessages');

// Toggle chat
chatToggle.addEventListener('click', () => {
    chatToggle.classList.toggle('active');
    chatContainer.classList.toggle('active');

    if (chatContainer.classList.contains('active')) {
        chatInput.focus();
    }
});

// Send message on button click
chatSend.addEventListener('click', () => {
    sendMessage();
});

// Send message on Enter key
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Send message function
async function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;

    // Add user message to chat
    addMessage(message, 'user');
    chatInput.value = '';

    // Show typing indicator
    showTypingIndicator();

    // API call to chatbot
    try {
        const response = await fetch('/api/chat/message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                timestamp: new Date().toISOString()
            })
        });

        const data = await response.json();

        // Remove typing indicator
        removeTypingIndicator();

        // Add bot response
        if (data.response) {
            addMessage(data.response, 'bot');
        } else {
            // Fallback responses
            addMessage(getAutoResponse(message), 'bot');
        }
    } catch (error) {
        console.error('Chat error:', error);
        removeTypingIndicator();
        addMessage(getAutoResponse(message), 'bot');
    }
}

// Add message to chat
function addMessage(text, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;

    const avatarSvg = type === 'bot'
        ? `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
           </svg>`
        : `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
            <circle cx="12" cy="7" r="4"/>
           </svg>`;

    messageDiv.innerHTML = `
        <div class="message-avatar">${avatarSvg}</div>
        <div class="message-content">
            <div class="message-text">${text}</div>
            <div class="message-time">${getCurrentTime()}</div>
        </div>
    `;

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Typing indicator
function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message typing-message';
    typingDiv.innerHTML = `
        <div class="message-avatar">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
            </svg>
        </div>
        <div class="message-content">
            <div class="message-text">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        </div>
    `;

    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
    const typingMessage = chatMessages.querySelector('.typing-message');
    if (typingMessage) {
        typingMessage.remove();
    }
}

// Auto responses (fallback)
function getAutoResponse(userMessage) {
    const message = userMessage.toLowerCase();

    if (message.includes('трафик') || message.includes('traffic')) {
        return 'Наша система анализа трафика позволяет отслеживать потоки транспорта в реальном времени, определять плотность движения и прогнозировать пробки. Хотите узнать больше о настройке?';
    } else if (message.includes('номер') || message.includes('license') || message.includes('скан')) {
        return 'Система распознавания номеров использует AI для мгновенной идентификации автомобилей. Точность распознавания составляет 98.5%. Интересует интеграция с базами данных?';
    } else if (message.includes('парковк') || message.includes('parking')) {
        return 'Решение для управления парковкой автоматизирует контроль въезда/выезда, отслеживает свободные места и формирует отчеты. Поддерживаются любые парковочные системы.';
    } else if (message.includes('зон') || message.includes('доступ') || message.includes('restricted')) {
        return 'Система контроля доступа к закрытым зонам отправляет моментальные уведомления при несанкционированном проникновении. Настраивается гибкая система разрешений.';
    } else if (message.includes('стоимость') || message.includes('цена') || message.includes('price')) {
        return 'Стоимость зависит от количества камер и выбранных решений. Базовый тариф от 5000₽/мес. Предоставляем 14-дневный пробный период. Оставить заявку на расчет?';
    } else if (message.includes('камер') || message.includes('camera')) {
        return 'Мы поддерживаем любые IP-камеры с RTSP потоком. Совместимость с брендами: Hikvision, Dahua, Axis, Uniview и другими. Нужна помощь с подбором?';
    } else if (message.includes('демо') || message.includes('demo') || message.includes('тест')) {
        return 'Предоставляем демо-доступ на 14 дней с полным функционалом! Для получения доступа заполните форму заявки или напишите на demo@trackvision.io';
    } else if (message.includes('привет') || message.includes('hello') || message.includes('hi')) {
        return 'Здравствуйте! Я помогу вам разобраться с решениями TrackVision. Спрашивайте о наших продуктах, ценах или технических возможностях!';
    } else {
        return 'Спасибо за ваш вопрос! Я передам его специалисту, который свяжется с вами в ближайшее время. А пока можете задать вопрос о наших решениях: камера трафика, скан номеров, управление парковкой или закрытые зоны.';
    }
}

function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
}

// ======================
// NOTIFICATIONS
// ======================
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;

    let bgColor;
    switch(type) {
        case 'success':
            bgColor = '#00ff88';
            break;
        case 'error':
            bgColor = '#ff4444';
            break;
        case 'info':
        default:
            bgColor = '#00d4ff';
            break;
    }

    notification.style.cssText = `
        position: fixed;
        top: 90px;
        right: 30px;
        padding: 15px 25px;
        background: ${bgColor};
        color: #000;
        border-radius: 6px;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        z-index: 10000;
        animation: slideInNotif 0.3s ease-out;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOutNotif 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add notification animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInNotif {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOutNotif {
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

// ======================
// LOGO CLICK
// ======================
const navLogo = document.getElementById('navLogo');
navLogo.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// ======================
// STATS CARDS ANIMATION
// ======================
const statCards = document.querySelectorAll('.stat-card');
statCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.querySelector('.stat-icon').style.transform = 'scale(1.1) rotate(5deg)';
        card.querySelector('.stat-icon').style.transition = 'transform 0.3s ease';
    });

    card.addEventListener('mouseleave', () => {
        card.querySelector('.stat-icon').style.transform = 'scale(1) rotate(0deg)';
    });
});

// Close dropdowns on ESC
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        profileBtn.classList.remove('active');
        profileDropdown.classList.remove('active');
        solutionsDropdown.classList.remove('active');

        if (chatContainer.classList.contains('active')) {
            chatToggle.classList.remove('active');
            chatContainer.classList.remove('active');
        }
    }
});

// ======================
// INITIALIZATION
// ======================
console.log('%c🎯 TrackVision System Active', 'color: #00d4ff; font-size: 20px; font-weight: bold;');
console.log('%cВидеоаналитика для вашего бизнеса', 'color: #8b93b8; font-size: 12px;');

}); // End of DOMContentLoaded