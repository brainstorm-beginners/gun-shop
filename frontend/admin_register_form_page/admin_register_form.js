window.addEventListener("DOMContentLoaded", (event) => {
    window.adminUserLogin = function() {
        // Получение данных из полей ввода
        const username = document.querySelector('input[name="uname"]').value;
        const password = document.querySelector('input[name="psw"]').value;

        // Создание объекта с данными пользователя
        const userData = {
            username: username,
            password: password
        };

        // Отправка запроса на сервер
        fetch('http://localhost:8000/auth/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `username=${encodeURIComponent(userData.username)}&password=${encodeURIComponent(userData.password)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.access_token) {
                // Если данные верны, сохраняем токен в localStorage
                localStorage.setItem('token', data.access_token);
                // Затем перенаправляем пользователя на страницу API
                window.location.href = '/docs';
            } else {
                // Если данные неверны, показываем сообщение об ошибке
                document.querySelector('.authErrorText').style.opacity = 1;
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
});

