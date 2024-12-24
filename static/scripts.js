// Переключение между режимами (загрузка файла и текстовое общение)
function toggleMode() {
    const isDirectMode = document.getElementById('directModeToggle').checked;
    document.getElementById('uploadForm').style.display = isDirectMode ? 'none' : 'block';
    document.getElementById('chatForm').style.display = isDirectMode ? 'block' : 'none';
}

// Отправка файла на сервер
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
        const responseContainer = document.getElementById('responseContainer');
        responseContainer.innerHTML = `<ul>${result.message.map(msg => `<li>${msg}</li>`).join('')}</ul>`;
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при отправке файла. Проверьте консоль для подробностей.');
    }
}

// Отправка текста для общения с ИИ
async function sendChat() {
    const chatInput = document.getElementById('chatInput');
    const userMessage = chatInput.value.trim();

    if (!userMessage) {
        alert('Пожалуйста, введите сообщение.');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:10000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userMessage }),
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(errorText);
        }

        const result = await response.json();
        const responseContainer = document.getElementById('responseContainer');
        responseContainer.innerHTML = `<p>${result.reply}</p>`;
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при общении с ИИ. Проверьте консоль для подробностей.');
    }
}
