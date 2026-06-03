document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const themeToggleBtn = document.getElementById('theme-toggle');
    const generateBtn = document.getElementById('generate-btn');
    const contentInput = document.getElementById('content');
    const categorySelect = document.getElementById('category');
    const inputError = document.getElementById('input-error');
    
    const outputSection = document.getElementById('output-section');
    const loadingState = document.getElementById('loading-state');
    const errorState = document.getElementById('error-state');
    const apiErrorMsg = document.getElementById('api-error-msg');
    const retryBtn = document.getElementById('retry-btn');
    const faqContainer = document.getElementById('faq-container');
    const faqCount = document.getElementById('faq-count');
    const exportPdfBtn = document.getElementById('export-pdf');

    // Theme Management
    const initTheme = () => {
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', savedTheme);
        updateThemeIcon(savedTheme);
    };

    const toggleTheme = () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    };

    const updateThemeIcon = (theme) => {
        const icon = themeToggleBtn.querySelector('i');
        if (theme === 'dark') {
            icon.className = 'ri-sun-line';
        } else {
            icon.className = 'ri-moon-line';
        }
    };

    themeToggleBtn.addEventListener('click', toggleTheme);
    initTheme();

    // Toast Notification
    const showToast = (message) => {
        let toast = document.getElementById('toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'toast';
            toast.className = 'toast';
            toast.innerHTML = `<i class="ri-checkbox-circle-fill" style="color: var(--primary-color);"></i> <span></span>`;
            document.body.appendChild(toast);
        }
        
        toast.querySelector('span').textContent = message;
        
        // Trigger reflow
        void toast.offsetWidth;
        
        toast.classList.add('show');
        
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    };

    // API Integration
    const generateFAQs = async () => {
        const content = contentInput.value.trim();
        const category = categorySelect.value;
        
        // Validation
        if (!content) {
            inputError.style.display = 'block';
            contentInput.focus();
            return;
        }
        
        inputError.style.display = 'none';
        
        // UI Updates for Loading
        outputSection.style.display = 'block';
        loadingState.style.display = 'flex';
        errorState.style.display = 'none';
        faqContainer.innerHTML = '';
        faqCount.textContent = 'Generating...';
        faqContainer.style.display = 'none';
        
        // Scroll to output
        outputSection.scrollIntoView({ behavior: 'smooth' });

        try {
            const response = await fetch('/api/generate-faq', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ content, category })
            });
            
            const data = await response.json();
            
            if (!response.ok || !data.success) {
                throw new Error(data.error || 'Failed to generate FAQs');
            }
            
            renderFAQs(data.faqs);
            
        } catch (error) {
            showError(error.message);
        }
    };

    const renderFAQs = (faqs) => {
        loadingState.style.display = 'none';
        errorState.style.display = 'none';
        faqContainer.style.display = 'flex';
        
        if (!faqs || faqs.length === 0) {
            showError('No FAQs were generated. Please try again with different content.');
            return;
        }
        
        faqCount.textContent = `${faqs.length} Questions Generated`;
        
        faqs.forEach((faq, index) => {
            const card = document.createElement('div');
            card.className = 'faq-card';
            
            card.innerHTML = `
                <div class="faq-header">
                    <h3 class="faq-question">${faq.question}</h3>
                    <button class="copy-btn" title="Copy QA" data-index="${index}">
                        <i class="ri-file-copy-line"></i>
                    </button>
                </div>
                <div class="faq-answer">${faq.answer}</div>
            `;
            
            // Add copy functionality
            const copyBtn = card.querySelector('.copy-btn');
            copyBtn.addEventListener('click', () => {
                const textToCopy = `Q: ${faq.question}\nA: ${faq.answer}`;
                navigator.clipboard.writeText(textToCopy).then(() => {
                    const icon = copyBtn.querySelector('i');
                    icon.className = 'ri-check-line';
                    icon.style.color = 'var(--primary-color)';
                    showToast('FAQ copied to clipboard!');
                    
                    setTimeout(() => {
                        icon.className = 'ri-file-copy-line';
                        icon.style.color = '';
                    }, 2000);
                });
            });
            
            faqContainer.appendChild(card);
        });
    };

    const showError = (message) => {
        loadingState.style.display = 'none';
        faqContainer.style.display = 'none';
        errorState.style.display = 'flex';
        apiErrorMsg.textContent = message;
        faqCount.textContent = 'Error';
    };

    // PDF Export
    const exportToPDF = () => {
        const element = document.getElementById('faq-container');
        if (!element || element.children.length === 0) {
            showToast('No FAQs to export.');
            return;
        }
        
        showToast('Generating PDF...');
        
        // Create a temporary clone for PDF formatting (avoiding dark mode issues in print)
        const clone = element.cloneNode(true);
        const wrapper = document.createElement('div');
        wrapper.style.padding = '20px';
        wrapper.style.color = '#000';
        wrapper.style.background = '#fff';
        
        // Apply basic styling to clone for PDF
        const cards = clone.querySelectorAll('.faq-card');
        cards.forEach(card => {
            card.style.border = '1px solid #ccc';
            card.style.marginBottom = '15px';
            card.style.padding = '15px';
            card.style.borderRadius = '5px';
            
            const btn = card.querySelector('.copy-btn');
            if(btn) btn.remove(); // Remove copy buttons from PDF
            
            const q = card.querySelector('.faq-question');
            if(q) {
                q.style.fontSize = '16px';
                q.style.fontWeight = 'bold';
                q.style.marginBottom = '8px';
            }
        });
        
        const title = document.createElement('h1');
        title.textContent = `Generated FAQs - ${categorySelect.value}`;
        title.style.marginBottom = '20px';
        wrapper.appendChild(title);
        wrapper.appendChild(clone);
        
        const opt = {
            margin:       10,
            filename:     'generated-faqs.pdf',
            image:        { type: 'jpeg', quality: 0.98 },
            html2canvas:  { scale: 2 },
            jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' }
        };
        
        html2pdf().set(opt).from(wrapper).save().then(() => {
            showToast('PDF Exported Successfully!');
        });
    };

    // Event Listeners
    generateBtn.addEventListener('click', generateFAQs);
    retryBtn.addEventListener('click', generateFAQs);
    exportPdfBtn.addEventListener('click', exportToPDF);
    
    // Allow Ctrl+Enter to generate
    contentInput.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            generateFAQs();
        }
    });
});
