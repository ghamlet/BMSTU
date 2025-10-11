// injector.js - для выполнения в консоли браузера на странице теста

function injectAnswers() {
    const answers = JSON.parse(localStorage.getItem('aiAnswers') || '[]');
    
    answers.forEach(answer => {
        highlightCorrectAnswer(answer);
    });
    
    console.log('Ответы внедрены!');
}

function highlightCorrectAnswer(answer) {
    // Ищем вопрос на странице по тексту
    const questionText = answer.question_text.toLowerCase();
    let questionElement = null;
    
    // Поиск элемента вопроса
    const allElements = document.querySelectorAll('p, div, td, span');
    for (let elem of allElements) {
        const text = elem.textContent.toLowerCase();
        if (text.includes(questionText.substring(0, 50))) {
            questionElement = elem.closest('.que, .question, .quiz') || elem;
            break;
        }
    }
    
    if (!questionElement) {
        console.log('Не найден вопрос:', answer.question_text);
        return;
    }
    
    // Создаем элемент с правильным ответом
    const answerDiv = document.createElement('div');
    answerDiv.style.cssText = `
        background: #d4edda;
        border: 2px solid #28a745;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
        font-weight: bold;
        color: #155724;
    `;
    answerDiv.innerHTML = `
        <strong>🤖 AI Assistant:</strong><br>
        Правильный ответ: <span style="color: #155724">${answer.correct_answer}</span><br>
        <em>${answer.explanation}</em>
    `;
    
    // Вставляем после вопроса
    questionElement.parentNode.insertBefore(answerDiv, questionElement.nextSibling);
    
    // Также пытаемся отметить правильный вариант
    markCorrectOption(questionElement, answer.correct_answer);
}

function markCorrectOption(questionElement, correctAnswer) {
    const options = questionElement.querySelectorAll('input[type="radio"], label');
    const correctText = correctAnswer.toLowerCase();
    
    options.forEach(option => {
        const text = option.textContent?.toLowerCase() || '';
        if (text.includes(correctText.substring(0, 20))) {
            // Помечаем правильный вариант
            if (option.tagName === 'INPUT') {
                option.checked = true;
                option.style.accentColor = 'green';
            }
            
            // Подсвечиваем label
            const label = option.tagName === 'LABEL' ? option : 
                         option.nextElementSibling?.tagName === 'LABEL' ? option.nextElementSibling : null;
            
            if (label) {
                label.style.cssText = `
                    background: #90EE90 !important;
                    border: 2px solid #32CD32 !important;
                    padding: 5px;
                    border-radius: 3px;
                    font-weight: bold;
                `;
            }
        }
    });
}

// Автоматическое внедрение при загрузке страницы
if (localStorage.getItem('aiAnswers')) {
    setTimeout(injectAnswers, 2000);
}

// Экспортируем функции для использования в консоли
window.injectAnswers = injectAnswers;