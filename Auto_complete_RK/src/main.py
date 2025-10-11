from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import json
import os
from parser import parse_test_page
from ai_helper import get_ai_answers

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Assistant</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            textarea { width: 100%; height: 300px; margin: 10px 0; }
            button { padding: 10px 20px; background: #007cba; color: white; border: none; cursor: pointer; }
            .question { border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }
            .correct { background: #d4edda; border-color: #c3e6cb; }
            .answer { margin: 5px 0; padding: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Test Assistant MVP</h1>
            
            <div>
                <h3>1. Вставьте HTML теста:</h3>
                <textarea id="htmlInput" placeholder="Вставьте HTML код теста здесь..."></textarea>
                <button onclick="parseTest()">Парсить тест</button>
            </div>

            <div id="questionsContainer" style="display: none;">
                <h3>2. Полученные вопросы:</h3>
                <div id="questionsList"></div>
                <button onclick="getAnswers()">Получить ответы от ИИ</button>
            </div>

            <div id="resultsContainer" style="display: none;">
                <h3>3. Результаты с правильными ответами:</h3>
                <div id="results"></div>
                <button onclick="injectAnswers()">Внедрить ответы на страницу</button>
            </div>
        </div>

        <script src="/static/injector.js"></script>
        <script>
            let currentQuestions = [];
            let aiAnswers = [];

            async function parseTest() {
                const html = document.getElementById('htmlInput').value;
                const response = await fetch('/parse', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ html: html })
                });
                
                const data = await response.json();
                currentQuestions = data.questions;
                
                displayQuestions(currentQuestions);
                document.getElementById('questionsContainer').style.display = 'block';
            }

            function displayQuestions(questions) {
                const container = document.getElementById('questionsList');
                container.innerHTML = questions.map((q, index) => `
                    <div class="question">
                        <strong>Вопрос ${index + 1}:</strong>
                        <div>${q.text}</div>
                        <div>Варианты: ${q.options.join(', ')}</div>
                    </div>
                `).join('');
            }

            async function getAnswers() {
                const response = await fetch('/get-answers', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ questions: currentQuestions })
                });
                
                const data = await response.json();
                aiAnswers = data.answers;
                
                displayResults(aiAnswers);
                document.getElementById('resultsContainer').style.display = 'block';
            }

            function displayResults(answers) {
                const container = document.getElementById('results');
                container.innerHTML = answers.map((answer, index) => `
                    <div class="question ${answer.is_correct ? 'correct' : ''}">
                        <strong>Вопрос ${index + 1}:</strong>
                        <div>${answer.question_text}</div>
                        <div class="answer"><strong>Правильный ответ:</strong> ${answer.correct_answer}</div>
                        <div><strong>Объяснение:</strong> ${answer.explanation}</div>
                    </div>
                `).join('');
            }

            function injectAnswers() {
                // Сохраняем ответы в localStorage для injector.js
                localStorage.setItem('aiAnswers', JSON.stringify(aiAnswers));
                alert('Ответы готовы для внедрения! Откройте консоль на странице теста и запустите injectAnswers()');
            }
        </script>
    </body>
    </html>
    """

@app.route('/parse', methods=['POST'])
def parse_test():
    data = request.json
    html_content = data['html']
    
    questions = parse_test_page(html_content)
    
    return jsonify({
        'success': True,
        'questions': questions,
        'count': len(questions)
    })


@app.route('/get-answers', methods=['POST'])
async def get_ai_answers_route():
    data = request.json
    questions = data['questions']
    
    # Используем асинхронную версию
    answers = await get_ai_answers(questions)
    
    return jsonify({
        'success': True,
        'answers': answers
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)