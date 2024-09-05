document.addEventListener('DOMContentLoaded', function () {
    // Код, который выполняется после загрузки страницы

    function processTableRows() {
        // Находим div с id 'listing-results'
        const listingResultsDiv = document.getElementById('listing-results');

        if (listingResultsDiv) {
            // Находим таблицу с классом 'listing' внутри найденного div
            const listingTable = listingResultsDiv.querySelector('table.listing');

            if (listingTable) {
                // Находим tbody внутри таблицы
                const tbody = listingTable.querySelector('tbody');

                if (tbody) {
                    // Перебираем все строки tr внутри tbody
                    const rows = tbody.querySelectorAll('tr');

                    rows.forEach((row) => {
                        const lastCell = row.lastElementChild;
                        if (lastCell && lastCell.tagName === 'TD') {
                            // Значение lastCell
                            const cellValue = lastCell.textContent.trim();

                            // Список значений для сравнения
                            const validValuesOrangePeach = ['Подан в запрос', 'Позвали на собеседование', 'Ожидание обратной связи'];
                            const validValuesSilver = ['Не активен', 'В архиве'];
                            const validValuesDarkGreenSea = ['Согласован выход', 'Работает на проекте'];

                            const validValuesGreen = ['A'];
                            const validValuesYellow = ['B'];
                            const validValuesRed = ['C'];

                            // Проверка, что значение в lastCell равно одному из значений из списка
                            if (validValuesOrangePeach.includes(cellValue)) {
                                row.style.backgroundColor = '#ffd699'; // Оранжево-персиковый цвет фона
                                row.style.color = '#000000'; // Черный цвет текста
                                row.cells[1].children[0].style.color = '#B07D2B'; // Темно-желтый текста
                            } else if (validValuesSilver.includes(cellValue)) {
                                row.style.backgroundColor = '#c2c2c2'; // Серебристый цвет фона
                                row.style.color = '#000000'; // Черный цвет текста
                                row.cells[1].children[0].style.color = '#000000'; // Темно-желтый текста
                            } else if (validValuesDarkGreenSea.includes(cellValue)) {
                                row.style.backgroundColor = '#90a690'; // Тёмно-зелёный цвет фона
                                row.style.color = '#FFFFFF'; // Белый цвет текста
                                row.cells[1].children[0].style.color = '#000000'; // Темно-желтый текста
                                row.cells[1].children[0].children[0].addEventListener('mouseout', function () {
                                    row.cells[1].children[0].children[0].style.color = '#000000';
                                });

                                row.cells[1].children[0].children[0].addEventListener('mouseover', function () {
                                    row.cells[1].children[0].children[0].style.color = '#ffffff';
                                });
                            }
                            if (validValuesGreen.includes(cellValue)) {
                                row.style.backgroundColor = 'Green'; // Оранжево-персиковый цвет фона
                                row.style.color = '#ffffff'; // Черный цвет текста
                                row.cells[1].children[0].style.color = '#ffffff'; // Темно-желтый текста
                                row.cells[1].children[0].children[0].addEventListener('mouseout', function () {
                                    row.cells[1].children[0].children[0].style.color = '#ffffff';
                                });

                                row.cells[1].children[0].children[0].addEventListener('mouseover', function () {
                                    row.cells[1].children[0].children[0].style.color = '#000000';
                                });
                            } else if (validValuesYellow.includes(cellValue)) {
                                row.style.backgroundColor = 'Yellow'; // Желтый цвет фона
                                row.style.color = '#000000'; // Черный цвет текста
                                row.cells[1].children[0].style.color = '#000000'; // Темно-желтый текста
                                row.cells[1].children[0].children[0].addEventListener('mouseout', function () {
                                    row.cells[1].children[0].children[0].style.color = '#000000';
                                });

                                row.cells[1].children[0].children[0].addEventListener('mouseover', function () {
                                    row.cells[1].children[0].children[0].style.color = '#0000FF';
                                });
                            } else if (validValuesRed.includes(cellValue)) {
                                row.style.backgroundColor = 'Red'; // Зелёный цвет фона
                                row.style.color = '#FFFFFF'; // Белый цвет текста
                                row.cells[1].children[0].style.color = '#000000'; // Темно-желтый текста
                                row.cells[1].children[0].children[0].addEventListener('mouseout', function () {
                                    row.cells[1].children[0].children[0].style.color = '#000000';
                                });

                                row.cells[1].children[0].children[0].addEventListener('mouseover', function () {
                                    row.cells[1].children[0].children[0].style.color = '#ffffff';
                                });
                            }
                        } else {
                            console.error('Последний элемент не является td или отсутствует');
                        }
                    });
                } else {
                    console.error('tbody не найден в таблице');
                }
            } else {
                console.error('Таблица с классом "listing" не найдена');
            }
        } else {
            console.error('div с id "listing-results" не найден');
        }
    }

    // Вызов функции для обработки строк таблицы
    processTableRows();
});
