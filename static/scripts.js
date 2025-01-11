function appendMessage(content, sender) {
    const responseContainer = document.getElementById('responseContainer');
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', sender);
    if (Array.isArray(content)) {
        const ul = document.createElement('ul');
        content.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            ul.appendChild(li);
        });
        messageElement.appendChild(ul);
    } else if (typeof content === 'string') {
        const formattedContent = content
            .replace(/\n/g, '<br>')
            .replace(/\t/g, '&nbsp;&nbsp;&nbsp;&nbsp;');
        messageElement.innerHTML = formattedContent;
    }
    responseContainer.appendChild(messageElement);
    if (sender === 'bot') {
        chatResponses.push(content);
    }
    if (!chatToggleAdded) {
        addChatToggle();
        chatToggleAdded = true;
    }
    responseContainer.scrollTop = responseContainer.scrollHeight;
}

async function sendFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    if (!file) {
        alert('Пожалуйста, выберите файл.');
        return;
    }
    const allowedExtensions = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    if (!allowedExtensions.includes(file.type)) {
        alert('Поддерживаются только файлы форматов PDF и DOCX.');
        return;
    }
    const formData = new FormData();
    formData.append('file', file);
    try {
        const response = await fetch('http://0.0.0.0:8000/upload-file', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(errorText);
        }
        const result = await response.json();
        appendMessage(file.name, 'user');
        result.message.forEach(msg => appendMessage(msg, 'bot'));
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при отправке файла. Проверьте консоль для подробностей.');
    }
}

function addChatToggle() {
    const toggleContainer = document.getElementById('toggleContainer');
    const chatToggleLabel = document.createElement('label');
    chatToggleLabel.innerHTML = `
        <input type="checkbox" id="chatToggle" onchange="toggleChatMode()">
        Переключиться на чат
    `;
    toggleContainer.appendChild(chatToggleLabel);
}

function toggleChatMode() {
    const chatToggle = document.getElementById('chatToggle');
    const chatInterface = document.getElementById('chatInterface');
    if (chatToggle.checked) {
        chatInterface.style.display = 'block';
    } else {
        chatInterface.style.display = 'none';
    }
}

async function sendChatMessage() {
    const chatInput = document.getElementById('chatInput');
    const userMessage = chatInput.value.trim();
    if (!userMessage) {
        alert('Пожалуйста, введите сообщение.');
        return;
    }
    appendMessage(userMessage, 'user');
    try {
        const response = await fetch('http://0.0.0.0:8000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userMessage }),
        });
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(errorText);
        }
        const result = await response.json();
        appendMessage(result.reply, 'bot');
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при отправке сообщения. Проверьте консоль для подробностей.');
    } finally {
        chatInput.value = '';
    }
}

let chatResponses = [];
let chatToggleAdded = false;

function saveResponsesToFile() {
    if (chatResponses.length === 0) {
        alert('Нет данных для сохранения.');
        return;
    }
    const blob = new Blob([chatResponses.join('\n\n')], { type: 'text/plain' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'chat_responses.txt';
    link.click();
}

function toggleChatMode() {
    const chatToggle = document.getElementById('chatToggle');
    const chatInterface = document.getElementById('chatInterface');
    if (chatToggle.checked) {
        chatInterface.style.display = 'block';
    } else {
        chatInterface.style.display = 'none';
    }
}
