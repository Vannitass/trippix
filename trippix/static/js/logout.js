window.addEventListener('beforeunload', function(event) {
    // Отправить запрос на завершение сеанса при закрытии вкладки
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/logout', false);  // Поменяйте URL на тот, который обрабатывает logout в Django
    xhr.send();
});
