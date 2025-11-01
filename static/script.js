// Chat functionality for Samarth Q&A System

const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const exampleChips = document.querySelectorAll('.example-chip');

// API endpoint
const API_URL = '/api/chat';

// Add message to chat
function addMessage(content, isUser = false, type = 'text') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    let messageHTML = `
        <div class="message-content">
            <div class="avatar ${isUser ? 'user-avatar' : 'bot-avatar'}">
                <i class="fas ${isUser ? 'fa-user' : 'fa-robot'}"></i>
            </div>
            <div class="message-text">
    `;
    
    if (type === 'table' && Array.isArray(content)) {
        if (content.length === 0) {
            messageHTML += '<p>No data found for your query.</p>';
        } else {
            messageHTML += '<table class="data-table"><thead><tr>';
            const headers = Object.keys(content[0]);
            headers.forEach(header => {
                messageHTML += `<th>${header.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</th>`;
            });
            messageHTML += '</tr></thead><tbody>';
            content.forEach(row => {
                messageHTML += '<tr>';
                headers.forEach(header => {
                    let value = row[header];
                    if (typeof value === 'number') {
                        value = value.toLocaleString('en-IN', { maximumFractionDigits: 2 });
                    }
                    messageHTML += `<td>${value || 'N/A'}</td>`;
                });
                messageHTML += '</tr>';
            });
            messageHTML += '</tbody></table>';
        }
    } else {
        // Format text content with line breaks
        const formattedContent = String(content).replace(/\n/g, '<br>');
        messageHTML += `<p>${formattedContent}</p>`;
    }
    
    messageHTML += '</div></div>';
    messageDiv.innerHTML = messageHTML;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return messageDiv;
}

// Show loading indicator
function showLoading() {
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message bot-message';
    loadingDiv.id = 'loadingMessage';
    loadingDiv.innerHTML = `
        <div class="message-content">
            <div class="avatar bot-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-text">
                <div class="loading">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
    `;
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Remove loading indicator
function removeLoading() {
    const loadingMessage = document.getElementById('loadingMessage');
    if (loadingMessage) {
        loadingMessage.remove();
    }
}

// Send message to API
async function sendMessage(query) {
    if (!query.trim()) return;
    
    // Add user message
    addMessage(query, true);
    
    // Clear input
    userInput.value = '';
    
    // Disable input
    userInput.disabled = true;
    sendButton.disabled = true;
    
    // Show loading
    showLoading();
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        });
        
        const data = await response.json();
        removeLoading();
        
        if (data.success) {
            if (data.type === 'table') {
                addMessage(data.response, false, 'table');
            } else {
                addMessage(data.response, false, 'text');
            }
        } else {
            const errorDiv = addMessage(data.response || 'An error occurred', false, 'text');
            errorDiv.querySelector('.message-text').classList.add('error-message');
        }
    } catch (error) {
        removeLoading();
        const errorDiv = addMessage('Sorry, I couldn\'t connect to the server. Please try again.', false, 'text');
        errorDiv.querySelector('.message-text').classList.add('error-message');
        console.error('Error:', error);
    } finally {
        // Re-enable input
        userInput.disabled = false;
        sendButton.disabled = false;
        userInput.focus();
    }
}

// Event listeners
sendButton.addEventListener('click', () => {
    const query = userInput.value.trim();
    if (query) {
        sendMessage(query);
    }
});

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        const query = userInput.value.trim();
        if (query) {
            sendMessage(query);
        }
    }
});

// Example chip click handlers
exampleChips.forEach(chip => {
    chip.addEventListener('click', () => {
        const text = chip.textContent.trim();
        userInput.value = text;
        sendMessage(text);
    });
});

// Focus input on load
window.addEventListener('load', () => {
    userInput.focus();
});

