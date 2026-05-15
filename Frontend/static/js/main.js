// ===== MODERN ATTENDANCE SYSTEM JAVASCRIPT =====

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Main initialization function
function initializeApp() {
    initializeAnimations();
    initializeFormValidation();
    initializeTooltips();
    initializeModals();
    initializeAttendance();
    initializeTheme();
}

// ===== ANIMATIONS =====
function initializeAnimations() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });

    // Add slide-in animation to sidebar items
    const sidebarItems = document.querySelectorAll('.sidebar .nav-link');
    sidebarItems.forEach((item, index) => {
        item.style.animationDelay = `${index * 0.05}s`;
        item.classList.add('slide-in');
    });
}

// ===== FORM VALIDATION =====
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                showNotification('Please fill in all required fields correctly.', 'error');
            }
        });
    });

    // Real-time validation
    const inputs = document.querySelectorAll('input[required], select[required]');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
    });
}

function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!validateField(field)) {
            isValid = false;
        }
    });
    
    return isValid;
}

function validateField(field) {
    const value = field.value.trim();
    const fieldType = field.type;
    let isValid = true;
    let errorMessage = '';

    // Remove existing error styling
    field.classList.remove('is-invalid');
    const existingError = field.parentNode.querySelector('.invalid-feedback');
    if (existingError) {
        existingError.remove();
    }

    // Check if field is required and empty
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        errorMessage = 'This field is required.';
    }
    // Email validation
    else if (fieldType === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid email address.';
        }
    }
    // Password validation
    else if (fieldType === 'password' && value && value.length < 6) {
        isValid = false;
        errorMessage = 'Password must be at least 6 characters long.';
    }

    // Show error if invalid
    if (!isValid) {
        field.classList.add('is-invalid');
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = errorMessage;
        field.parentNode.appendChild(errorDiv);
    }

    return isValid;
}

// ===== TOOLTIPS =====
function initializeTooltips() {
    // Initialize Bootstrap tooltips if available
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

// ===== MODALS =====
function initializeModals() {
    // Add loading state to modal forms
    const modalForms = document.querySelectorAll('.modal form');
    modalForms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.classList.add('loading');
                submitBtn.disabled = true;
            }
        });
    });
}

// ===== ATTENDANCE SPECIFIC =====
function initializeAttendance() {
    // Attendance form functionality
    const attendanceForm = document.getElementById('attendanceForm');
    if (attendanceForm) {
        initializeAttendanceForm();
    }

    // Statistics animation
    animateStatistics();
}

function initializeAttendanceForm() {
    const form = document.getElementById('attendanceForm');
    const radios = form.querySelectorAll('input[type="radio"]');
    
    // Add change listeners to radio buttons
    radios.forEach(radio => {
        radio.addEventListener('change', function() {
            updateAttendanceSummary();
            highlightRow(this);
        });
    });

    // Initialize summary
    updateAttendanceSummary();
}

function markAll(status) {
    const radios = document.querySelectorAll('input[type="radio"]');
    radios.forEach(radio => {
        if (radio.value === status) {
            radio.checked = true;
            highlightRow(radio);
        }
    });
    updateAttendanceSummary();
    
    // Show feedback
    showNotification(`All students marked as ${status.toLowerCase()}.`, 'success');
}

function updateAttendanceSummary() {
    const presentCount = document.querySelectorAll('input[value="Present"]:checked').length;
    const absentCount = document.querySelectorAll('input[value="Absent"]:checked').length;
    const totalCount = document.querySelectorAll('input[type="radio"][value="Present"]').length;

    // Update summary if elements exist
    const presentElement = document.getElementById('presentCount');
    const absentElement = document.getElementById('absentCount');
    const totalElement = document.getElementById('totalCount');

    if (presentElement) presentElement.textContent = presentCount;
    if (absentElement) absentElement.textContent = absentCount;
    if (totalElement) totalElement.textContent = totalCount;

    // Update progress bar if exists
    updateAttendanceProgress(presentCount, totalCount);
}

function updateAttendanceProgress(present, total) {
    const progressBar = document.getElementById('attendanceProgress');
    if (progressBar && total > 0) {
        const percentage = (present / total) * 100;
        progressBar.style.width = `${percentage}%`;
        progressBar.textContent = `${Math.round(percentage)}%`;
        
        // Change color based on percentage
        progressBar.className = 'progress-bar';
        if (percentage >= 80) {
            progressBar.classList.add('bg-success');
        } else if (percentage >= 60) {
            progressBar.classList.add('bg-warning');
        } else {
            progressBar.classList.add('bg-danger');
        }
    }
}

function highlightRow(radio) {
    const row = radio.closest('tr');
    if (row) {
        // Remove existing classes
        row.classList.remove('attendance-present', 'attendance-absent');
        
        // Add appropriate class
        if (radio.value === 'Present' && radio.checked) {
            row.classList.add('attendance-present');
        } else if (radio.value === 'Absent' && radio.checked) {
            row.classList.add('attendance-absent');
        }
    }
}

// ===== STATISTICS ANIMATION =====
function animateStatistics() {
    const statNumbers = document.querySelectorAll('.stats-number');
    
    statNumbers.forEach(stat => {
        const finalValue = parseInt(stat.textContent);
        animateNumber(stat, 0, finalValue, 1000);
    });
}

function animateNumber(element, start, end, duration) {
    const startTime = performance.now();
    
    function updateNumber(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = Math.floor(start + (end - start) * easeOutCubic(progress));
        element.textContent = current;
        
        if (progress < 1) {
            requestAnimationFrame(updateNumber);
        }
    }
    
    requestAnimationFrame(updateNumber);
}

function easeOutCubic(t) {
    return 1 - Math.pow(1 - t, 3);
}

// ===== NOTIFICATIONS =====
function showNotification(message, type = 'info', duration = 3000) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show notification-toast`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        box-shadow: var(--shadow-lg);
        animation: slideInRight 0.3s ease-out;
    `;
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Auto remove after duration
    setTimeout(() => {
        if (notification.parentNode) {
            notification.classList.add('fade-out');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }
    }, duration);
}

// ===== THEME MANAGEMENT =====
function initializeTheme() {
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('attendanceTheme');
    if (savedTheme) {
        document.body.setAttribute('data-theme', savedTheme);
    }
}

function toggleTheme() {
    const currentTheme = document.body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.body.setAttribute('data-theme', newTheme);
    localStorage.setItem('attendanceTheme', newTheme);
    
    showNotification(`Switched to ${newTheme} theme`, 'info');
}

// ===== UTILITY FUNCTIONS =====
function formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(new Date(date));
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ===== SEARCH FUNCTIONALITY =====
function initializeSearch() {
    const searchInputs = document.querySelectorAll('[data-search]');
    
    searchInputs.forEach(input => {
        const targetSelector = input.getAttribute('data-search');
        const searchFunction = debounce((query) => {
            filterTable(targetSelector, query);
        }, 300);
        
        input.addEventListener('input', (e) => {
            searchFunction(e.target.value);
        });
    });
}

function filterTable(tableSelector, query) {
    const table = document.querySelector(tableSelector);
    if (!table) return;
    
    const rows = table.querySelectorAll('tbody tr');
    const searchTerm = query.toLowerCase();
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        const shouldShow = text.includes(searchTerm);
        
        row.style.display = shouldShow ? '' : 'none';
        
        if (shouldShow && searchTerm) {
            row.classList.add('search-highlight');
        } else {
            row.classList.remove('search-highlight');
        }
    });
}

// ===== EXPORT FUNCTIONS =====
window.attendanceSystem = {
    markAll,
    updateAttendanceSummary,
    showNotification,
    toggleTheme,
    validateForm
};

// ===== CSS ANIMATIONS =====
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .fade-out {
        animation: fadeOut 0.3s ease-out forwards;
    }
    
    @keyframes fadeOut {
        to { opacity: 0; transform: translateX(100%); }
    }
    
    .search-highlight {
        background-color: rgba(255, 235, 59, 0.2) !important;
    }
    
    .notification-toast {
        animation: slideInRight 0.3s ease-out;
    }
`;
document.head.appendChild(style);