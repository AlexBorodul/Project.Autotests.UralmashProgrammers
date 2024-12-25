function appendMessage(content, sender) {
    const responseContainer = document.getElementById('responseContainer');

    // Создаём новый элемент для сообщения
    const messageElement = document.createElement('p');
    messageElement.classList.add('chat-message', sender); // Добавляем класс в зависимости от отправителя
    messageElement.textContent = content;

    // Добавляем сообщение в контейнер
    responseContainer.appendChild(messageElement);

    // Прокручиваем вниз, чтобы видеть последнее сообщение
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
