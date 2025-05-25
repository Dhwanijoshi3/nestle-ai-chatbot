async function sendMessage() {
  const input = document.getElementById('userInput');
  const message = input.value;
  if (!message) return;

  const chatBox = document.getElementById('chatMessages');
  chatBox.innerHTML += `<div><strong>You:</strong> ${message}</div>`;

  input.value = "";

  const res = await fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question: message })
  });

  const data = await res.json();

  chatBox.innerHTML += `<div><strong>Bot:</strong> ${data.answer}</div>`;

  // Check if sources exist and display them as clickable links
  if (data.sources && data.sources.length > 0) {
    const sourcesHtml = data.sources.map(src => 
      `<li><a href="${src}" target="_blank" rel="noopener noreferrer">${src}</a></li>`
    ).join("");
    chatBox.innerHTML += `<div><strong>Sources:</strong><ul>${sourcesHtml}</ul></div>`;
  }

  chatBox.scrollTop = chatBox.scrollHeight;
}
// Initialize the chatbot when DOM is loaded
class NestleChatbot {
  constructor() {
    this.chatbotToggle = document.getElementById('chatbotToggle');
    this.chatbox = document.getElementById('chatbox');
    this.chatClose = document.getElementById('chatClose');
    this.userInput = document.getElementById('userInput');
    this.sendButton = document.getElementById('sendButton');
    this.chatMessages = document.getElementById('chatMessages');
    this.typingIndicator = document.getElementById('typingIndicator');
    
    this.isOpen = false;
    this.isTyping = false;
    
    this.initializeEventListeners();
  }
  
  initializeEventListeners() {
    this.chatbotToggle.addEventListener('click', () => this.toggleChat());
    this.chatClose.addEventListener('click', () => this.closeChat());
    this.sendButton.addEventListener('click', () => this.sendMessage());
    this.userInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') this.sendMessage();
    });
    
    // Auto-focus input when chat opens
    this.chatbox.addEventListener('transitionend', () => {
      if (this.isOpen) this.userInput.focus();
    });
  }
  
  toggleChat() {
    if (this.isOpen) {
      this.closeChat();
    } else {
      this.openChat();
    }
  }
  
  openChat() {
    this.isOpen = true;
    this.chatbox.classList.add('active');
    this.chatbotToggle.classList.add('active');
    this.chatbotToggle.innerHTML = '×';
  }
  
  closeChat() {
    this.isOpen = false;
    this.chatbox.classList.remove('active');
    this.chatbotToggle.classList.remove('active');
    this.chatbotToggle.innerHTML = '💬';
  }
  
  async sendMessage() {
    const message = this.userInput.value.trim();
    if (!message || this.isTyping) return;
    
    // Add user message
    this.addMessage(message, 'user');
    this.userInput.value = '';
    
    // Show typing indicator
    this.showTyping();
    
    try {
      // Send request to backend
      const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: message })
      });
      
      const data = await response.json();
      
      // Hide typing indicator
      this.hideTyping();
      
      // Add bot response
      this.addBotMessage(data.answer, data.sources);
      
    } catch (error) {
      console.error('Error:', error);
      this.hideTyping();
      this.addMessage('Sorry, I encountered an error. Please try again later.', 'bot');
    }
  }
  
  addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    if (sender === 'user') {
      messageDiv.innerHTML = text;
    } else {
      messageDiv.innerHTML = `<strong>Nestlé Assistant:</strong> ${text}`;
    }
    
    this.chatMessages.appendChild(messageDiv);
    this.scrollToBottom();
  }
  
  addBotMessage(text, sources) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot';
    
    // Format the text with proper line breaks and structure
    const formattedText = this.formatBotResponse(text);
    let html = `<strong>Nestlé Assistant:</strong> ${formattedText}`;
    
    if (sources && sources.length > 0) {
      // Remove duplicates from sources
      const uniqueSources = [...new Set(sources)];
      const maxPreviewSources = 3;
      const hasMoreSources = uniqueSources.length > maxPreviewSources;
      
      html += '<div class="sources">';
      html += '<div class="sources-header">';
      html += `<strong>References: <span class="source-count">(${uniqueSources.length})</span></strong>`;
      
      if (hasMoreSources) {
        html += `<button class="toggle-sources" onclick="this.closest('.sources').querySelector('.sources-list').classList.toggle('expanded'); this.querySelector('.toggle-text').textContent = this.querySelector('.toggle-text').textContent === 'Show All' ? 'Show Less' : 'Show All';">
          <span class="toggle-text">Show All</span>
          <span class="toggle-icon">▼</span>
        </button>`;
      }
      
      html += '</div>';
      html += '<ul class="sources-list">';
      
      uniqueSources.forEach((source, index) => {
        // Clean and decode the source URL
        const cleanedSource = this.cleanSourceUrl(source);
        const displayUrl = this.getDisplayUrl(cleanedSource);
        const isHidden = index >= maxPreviewSources;
        
        html += `<li class="source-item ${isHidden ? 'hidden-source' : ''}">
          <a href="${cleanedSource}" target="_blank" rel="noopener noreferrer">
            <span class="reference-number">${index + 1}</span>${displayUrl}
          </a>
        </li>`;
      });
      
      html += '</ul></div>';
    }
    
    messageDiv.innerHTML = html;
    this.chatMessages.appendChild(messageDiv);
    this.scrollToBottom();
  }
  
  formatBotResponse(text) {
    // Split text into lines for better processing
    let lines = text.split('\n');
    let formatted = '';
    
    for (let i = 0; i < lines.length; i++) {
      let line = lines[i].trim();
      if (!line) continue;
      
      // Check for ### headings
      if (line.startsWith('### ')) {
        const headingText = line.replace('### ', '').replace(/\*\*/g, '');
        formatted += `<h3 class="response-heading">${headingText}</h3>`;
        continue;
      }
      
      // Check for ## headings
      if (line.startsWith('## ')) {
        const headingText = line.replace('## ', '').replace(/\*\*/g, '');
        formatted += `<h2 class="response-heading">${headingText}</h2>`;
        continue;
      }
      
      // Check if line starts with a number followed by a dot
      if (/^\d+\.\s/.test(line)) {
        // Split the numbered line into number and content
        const match = line.match(/^(\d+\.\s)(.*)$/);
        if (match) {
          const number = match[1];
          const content = match[2];
          
          // Check if content has bold text at the beginning
          const boldMatch = content.match(/^(\*\*[^*]+\*\*:?)\s*(.*)$/);
          if (boldMatch) {
            const boldText = boldMatch[1].replace(/\*\*/g, '');
            const restText = boldMatch[2];
            formatted += `<div class="numbered-item">
              <span class="item-number">${number}</span>
              <div class="item-content">
                <strong class="item-title">${boldText}</strong>
                ${restText ? `<span class="item-description">${this.wrapLongText(restText)}</span>` : ''}
              </div>
            </div>`;
          } else {
            formatted += `<div class="numbered-item">
              <span class="item-number">${number}</span>
              <div class="item-content">${this.wrapLongText(content)}</div>
            </div>`;
          }
        }
      } else {
        // Regular line - convert **text** to bold and add as paragraph
        line = line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        if (line.length > 0) {
          formatted += `<p class="response-paragraph">${this.wrapLongText(line)}</p>`;
        }
      }
    }
    
    // If no numbered items were found, use simple formatting
    if (!formatted.includes('numbered-item') && !formatted.includes('response-heading')) {
      formatted = text
        .replace(/### (.*?)(\n|$)/g, '<h3 class="response-heading">$1</h3>')
        .replace(/## (.*?)(\n|$)/g, '<h2 class="response-heading">$1</h2>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/(\d+\.\s)/g, '<br><br><span class="list-number">$1</span>')
        .replace(/\n\n/g, '</p><p class="response-paragraph">')
        .replace(/\n/g, '<br>')
        .replace(/^(<br>)+/, '');
      
      if (formatted && !formatted.includes('<p')) {
        formatted = `<p class="response-paragraph">${this.wrapLongText(formatted)}</p>`;
      }
    }
    
    return formatted;
  }
  
  wrapLongText(text) {
    // Add word break opportunities for long words and URLs
    return text
      .replace(/([a-zA-Z0-9]{15,})/g, '<span class="breakable-text">$1</span>')
      .replace(/(https?:\/\/[^\s]+)/g, '<span class="breakable-url">$1</span>');
  }
  
  cleanSourceUrl(url) {
    if (!url) return '';
    
    // Decode URL-encoded characters
    let cleaned = decodeURIComponent(url);
    
    // Fix common encoding issues
    cleaned = cleaned
      .replace(/\?uddg=https%3A%2F%2F/, '')
      .replace(/&rut=.*$/, '')
      .replace(/\?uddg=/, '')
      .replace(/%3A/g, ':')
      .replace(/%2F/g, '/')
      .replace(/%2E/g, '.')
      .replace(/%3F/g, '?')
      .replace(/%3D/g, '=')
      .replace(/%26/g, '&');
    
    // Extract the actual URL if it contains redirects
    const urlMatch = cleaned.match(/https?:\/\/[^\s&]+/);
    if (urlMatch) {
      cleaned = urlMatch[0];
    }
    
    // Ensure it starts with http or https
    if (!cleaned.startsWith('http')) {
      cleaned = 'https://' + cleaned;
    }
    
    return cleaned;
  }
  
  getDisplayUrl(url) {
    try {
      const urlObj = new URL(url);
      let displayName = urlObj.hostname.replace('www.', '');
      
      // Create more readable display names
      if (displayName.includes('nestle')) {
        if (displayName.includes('madewithnestle')) {
          displayName = 'Made with Nestlé';
        } else {
          displayName = 'Nestlé Official';
        }
      }
      
      // Add path info if it's meaningful
      const pathParts = urlObj.pathname.split('/').filter(part => part && part !== 'index.html');
      if (pathParts.length > 0 && pathParts[0] !== '') {
        const lastPart = pathParts[pathParts.length - 1];
        if (lastPart.length < 30) {
          displayName += ` - ${lastPart.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}`;
        }
      }
      
      return displayName;
    } catch (e) {
      // Fallback for malformed URLs
      return url.length > 50 ? url.substring(0, 47) + '...' : url;
    }
  }
  
  showTyping() {
    this.isTyping = true;
    this.typingIndicator.style.display = 'flex';
    this.sendButton.disabled = true;
    this.scrollToBottom();
  }
  
  hideTyping() {
    this.isTyping = false;
    this.typingIndicator.style.display = 'none';
    this.sendButton.disabled = false;
  }
  
  scrollToBottom() {
    setTimeout(() => {
      this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }, 100);
  }
}

// Initialize chatbot when page loads
document.addEventListener('DOMContentLoaded', () => {
  new NestleChatbot();
});

// Add some smooth scrolling for the page
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

// Legacy function for backward compatibility with existing backend
async function sendMessage() {
  const chatbot = window.nestleChatbot || new NestleChatbot();
  await chatbot.sendMessage();
}