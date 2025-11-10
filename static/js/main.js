// Основен JavaScript файл с анимации и интерактивност
document.addEventListener('DOMContentLoaded', function() {
    console.log('AI Language Assistant loaded successfully!');

    // Създаване на particle background
    createParticles();

    // Добавяне на интерактивност за флаш картите
    initFlashcards();

    // Автоматично скриване на съобщенията за грешка
    initErrorMessages();

    // Добавяне на анимации при скрол
    initScrollAnimations();

    // Инициализация на tooltips
    initTooltips();
});

// Particle background
function createParticles() {
    const particlesContainer = document.createElement('div');
    particlesContainer.className = 'particles';
    document.body.appendChild(particlesContainer);

    const particleCount = 30;

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';

        const size = Math.random() * 60 + 10;
        const posX = Math.random() * 100;
        const delay = Math.random() * 20;
        const duration = Math.random() * 10 + 20;

        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.left = `${posX}vw`;
        particle.style.bottom = `-${size}px`;
        particle.style.animationDelay = `${delay}s`;
        particle.style.animationDuration = `${duration}s`;
        particle.style.opacity = Math.random() * 0.1 + 0.05;

        // Случаен gradient цвят
        const gradients = [
            'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
            'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
        ];
        const randomGradient = gradients[Math.floor(Math.random() * gradients.length)];
        particle.style.background = randomGradient;

        particlesContainer.appendChild(particle);
    }
}

// Флаш карти
function initFlashcards() {
    const flashcards = document.querySelectorAll('.flashcard');

    flashcards.forEach((card, index) => {
        // Забавяне на анимацията
        card.style.animationDelay = `${index * 0.1}s`;

        // Клик функционалност
        card.addEventListener('click', function() {
            const inner = this.querySelector('.flashcard-inner');
            const isFlipped = inner.style.transform === 'rotateY(180deg)';

            inner.style.transform = isFlipped ? 'rotateY(0deg)' : 'rotateY(180deg)';
        });

        // Hover ефект
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
        });

        card.addEventListener('mouseleave', function() {
            if (this.querySelector('.flashcard-inner').style.transform !== 'rotateY(180deg)') {
                this.style.transform = 'translateY(0)';
            }
        });
    });
}

// Грешки и съобщения
function initErrorMessages() {
    const errorMessages = document.querySelectorAll('.errors');

    errorMessages.forEach(error => {
        setTimeout(() => {
            error.style.opacity = '0';
            error.style.transform = 'translateY(-20px)';
            setTimeout(() => {
                error.style.display = 'none';
            }, 300);
        }, 5000);
    });
}

// Анимации при скрол
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Наблюдаване на елементи за анимация
    const animatedElements = document.querySelectorAll('.feature-card, .word-card, .input-section, .output-section');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// Tooltips
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');

    tooltipElements.forEach(el => {
        el.addEventListener('mouseenter', showTooltip);
        el.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(e) {
    const tooltipText = this.getAttribute('data-tooltip');
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = tooltipText;
    tooltip.style.cssText = `
        position: absolute;
        background: var(--dark-gradient);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-size: 0.875rem;
        white-space: nowrap;
        z-index: 1000;
        pointer-events: none;
        transform: translateY(-100%);
        margin-top: -10px;
    `;

    document.body.appendChild(tooltip);

    const rect = this.getBoundingClientRect();
    tooltip.style.left = `${rect.left + rect.width / 2 - tooltip.offsetWidth / 2}px`;
    tooltip.style.top = `${rect.top - 10}px`;

    this._tooltip = tooltip;
}

function hideTooltip() {
    if (this._tooltip) {
        this._tooltip.remove();
        this._tooltip = null;
    }
}

// Функция за търсене на синоними
async function searchSynonyms() {
    const word = prompt('Въведете дума за търсене на синоними:');
    if (word) {
        await performApiCall(
            `/api/v1/synonyms/${encodeURIComponent(word)}`,
            `Синоними на "${word}":`,
            'Не са намерени синоними за'
        );
    }
}

// Функция за проверка на трудността на дума
async function checkDifficulty() {
    const word = prompt('Въведете дума за проверка на трудността:');
    if (word) {
        await performApiCall(
            `/api/v1/difficulty-level/${encodeURIComponent(word)}`,
            `Дума "${word}" е с трудност:`,
            'Грешка при проверка на трудността'
        );
    }
}

// Обща функция за API заявки
async function performApiCall(url, successPrefix, errorPrefix) {
    const button = event?.target;
    const originalText = button?.innerHTML;

    if (button) {
        button.innerHTML = '<span class="loading"></span> Зареждане...';
        button.disabled = true;
    }

    try {
        const response = await fetch(url);
        const data = await response.json();

        let message = '';
        if (url.includes('synonyms')) {
            if (data.synonyms.length > 0) {
                message = `${successPrefix} ${data.synonyms.join(', ')}`;
            } else {
                message = `${errorPrefix} "${data.word}"`;
            }
        } else if (url.includes('difficulty-level')) {
            const levelText = getDifficultyText(data.difficulty_level);
            message = `${successPrefix} ${levelText}`;
        }

        showNotification(message, 'success');
    } catch (error) {
        console.error('Грешка при API заявка:', error);
        showNotification(`${errorPrefix}.`, 'error');
    } finally {
        if (button) {
            button.innerHTML = originalText;
            button.disabled = false;
        }
    }
}

function getDifficultyText(level) {
    const levels = {
        'beginner': '🟢 Начинаещ',
        'intermediate': '🟡 Напреднал',
        'advanced': '🔴 Експерт'
    };
    return levels[level] || level;
}

// Система за известия
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-icon">${getNotificationIcon(type)}</span>
            <span class="notification-message">${message}</span>
            <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
    `;

    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        border-left: 4px solid ${getNotificationColor(type)};
        z-index: 10000;
        animation: slideInRight 0.3s ease;
        max-width: 400px;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

function getNotificationIcon(type) {
    const icons = {
        'success': '✅',
        'error': '❌',
        'info': 'ℹ️',
        'warning': '⚠️'
    };
    return icons[type] || 'ℹ️';
}

function getNotificationColor(type) {
    const colors = {
        'success': '#43e97b',
        'error': '#f5576c',
        'info': '#4facfe',
        'warning': '#f093fb'
    };
    return colors[type] || '#4facfe';
}

// Добавяне на CSS анимации за известията
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .notification-content {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .notification-close {
        background: none;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        padding: 0;
        margin-left: auto;
        color: #666;
    }
    
    .tooltip {
        animation: fadeIn 0.2s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
`;
document.head.appendChild(style);

// Typewriter ефект за заглавията
function initTypewriter() {
    const titles = document.querySelectorAll('h1[data-typewriter]');

    titles.forEach(title => {
        const text = title.textContent;
        title.textContent = '';
        title.style.borderRight = '2px solid #667eea';

        let i = 0;
        const typeWriter = () => {
            if (i < text.length) {
                title.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            } else {
                title.style.borderRight = 'none';
            }
        };

        typeWriter();
    });
}

// Инициализиране на typewriter ефекта при зареждане
if (document.querySelector('h1[data-typewriter]')) {
    initTypewriter();
}