function appendMessage(content, sender) {
    const responseContainer = document.getElementById('responseContainer');

    // Создаём общий контейнер для сообщения
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', sender);

    // Если контент - это массив, выводим как список
    if (Array.isArray(content)) {
        const ul = document.createElement('ul');
        content.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            ul.appendChild(li);
        });
        messageElement.appendChild(ul);
    } else if (typeof content === 'string') {
        // Обработка перевода строк и табуляции
        const formattedContent = content
            .replace(/\n/g, '<br>') // Перевод строки -> <br>
            .replace(/\t/g, '&nbsp;&nbsp;&nbsp;&nbsp;'); // Табуляция -> 4 пробела

        // Добавляем в div как HTML
        messageElement.innerHTML = formattedContent;
    }

    // Добавляем сообщение в контейнер
    responseContainer.appendChild(messageElement);

    if (sender === 'bot') {
        chatResponses.push(content);
    }

    // Прокручиваем вниз
    responseContainer.scrollTop = responseContainer.scrollHeight;
}


async function sendFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (!file) {
        alert('Пожалуйста, выберите файл.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('http://127.0.0.1:10000/', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(errorText);
        }

        const result = await response.json();

        // Добавляем сообщение пользователя (имя файла) и ответы сервера
        appendMessage(file.name, 'user');
        result.message.forEach(msg => appendMessage(msg, 'bot'));
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при отправке файла. Проверьте консоль для подробностей.');
    }
}

function toggleChatMode() {
    const chatToggle = document.getElementById('chatToggle');
    const chatInterface = document.getElementById('chatInterface');

    // Отображаем или скрываем интерфейс чата в зависимости от состояния галочки
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

    // Добавляем сообщение пользователя
    appendMessage(userMessage, 'user');

    try {
        const response = await fetch('http://127.0.0.1:10000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userMessage }),
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(errorText);
        }

        const result = await response.json();

        // Добавляем сообщение от бота
        appendMessage(result.reply, 'bot');
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при отправке сообщения. Проверьте консоль для подробностей.');
    } finally {
        chatInput.value = ''; // Очищаем поле ввода
    }
}

let chatResponses = []; // Массив для хранения ответов Gigachat

// Добавление ответа в массив и создание текстового файла
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

