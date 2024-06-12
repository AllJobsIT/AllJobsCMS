document.addEventListener("DOMContentLoaded", (event) => {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Проверяем, начинается ли куки с нужного имени
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    // Если нашли куки с нужным именем, извлекаем его значение
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    const fileInput = document.getElementById('formFile');
// Получаем ссылку на кнопку отправки
    const submitBtn = document.getElementById('submitBtn');
    const modalTitle = document.getElementById('exampleModalLabel');
    const modalBody = document.querySelector('#successModal .modal-body');

// Добавляем слушатель события изменения значения в input
    fileInput.addEventListener('change', function () {
        // Проверяем, выбран ли файл
        if (fileInput.files.length > 0) {
            // Если файл выбран, показываем кнопку отправки
            submitBtn.style.display = 'block';
        } else {
            // Если файл не выбран, скрываем кнопку отправки
            submitBtn.style.display = 'none';
        }
    });

// Добавляем слушатель события клика по кнопке отправки
    submitBtn.addEventListener('click', function () {
        // Создаем объект FormData для отправки файла
        const formData = new FormData();
        // Добавляем выбранный файл в объект FormData
        formData.append('file', fileInput.files[0]);

        // Отправляем файл на указанный URL с помощью fetch
        fetch("/api/parser_resume/", {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrftoken // Добавляем CSRF-токен в заголовок запроса
            },
        })
            .then(response => {
                // Обрабатываем ответ
                if (response.ok) {
                    // Если ответ успешный, делаем что-то
                    modalTitle.textContent = 'Success';
                    modalBody.textContent = 'Резюме успешно загружено';
                    console.log('File uploaded successfully');
                } else {
                    // Если возникла ошибка, выводим сообщение об ошибке
                    modalTitle.textContent = 'Error';
                    modalBody.textContent = 'Ошибка при загрузке резюме';
                    console.error('Error uploading file');
                }
            })
            .catch(error => {
                // В случае ошибки выводим сообщение об ошибке
                console.error('Error:', error);
            });
    });
})
