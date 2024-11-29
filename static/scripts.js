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
        responseContainer.innerHTML = result.message;
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при отправке файла. Проверьте консоль для подробностей.');
    }
}
