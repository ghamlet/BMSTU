# simple_sync_assistant.py
from selenium import webdriver
import requests
import json
import time

OPENROUTER_API_KEY = "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"

def parse_page_simple(html_content):
    """Простой парсинг страницы"""
    from bs4 import BeautifulSoup
    import re
    
    soup = BeautifulSoup(html_content, 'html.parser')
    questions = []
    
    # Ищем элементы с вопросами
    question_elements = soup.find_all(class_=re.compile(r'que|question|qtext'))
    
    for i, elem in enumerate(question_elements):
        question_text = elem.get_text(strip=True)
        
        # Ищем варианты ответов рядом
        options = []
        next_elem = elem.find_next(class_=re.compile(r'answer|option|choice'))
        if next_elem:
            for opt in next_elem.find_all(['label', 'td', 'div']):
                text = opt.get_text(strip=True)
                if text and len(text) > 1:
                    options.append(text)
        
        if question_text and len(question_text) > 10 and options:
            questions.append({
                'id': f'q_{i}',
                'text': question_text,
                'options': options[:10]  # ограничиваем количество вариантов
            })
    
    return questions

def get_ai_answer_sync(question):
    """Синхронный запрос к ИИ"""
    prompt = f"""
    Вопрос теста по английскому:
    {question['text']}
    
    Варианты:
    {chr(10).join(question['options'])}
    
    Дай правильный ответ в формате JSON:
    {{"answer": "правильный вариант", "explanation": "объяснение"}}
    """
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    
    data = {
        "model": "meta-llama/llama-4-scout:free",
        "messages": [
            {"role": "system", "content": "Ты эксперт по английскому. Отвечай в JSON формате."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            text = result["choices"][0]["message"]["content"]
            
            # Парсим JSON ответ
            try:
                start = text.find('{')
                end = text.rfind('}') + 1
                if start != -1 and end != 0:
                    json_data = json.loads(text[start:end])
                    return {
                        'correct_answer': json_data.get('answer', 'Не найден'),
                        'explanation': json_data.get('explanation', 'Нет объяснения')
                    }
            except:
                pass
            
            # Если JSON не распарсился, возвращаем текст
            return {
                'correct_answer': 'Смотри объяснение',
                'explanation': text
            }
        else:
            return {
                'correct_answer': f'Ошибка {response.status_code}',
                'explanation': 'Не удалось получить ответ'
            }
    except Exception as e:
        return {
            'correct_answer': 'Ошибка',
            'explanation': f'Исключение: {str(e)}'
        }

def main():
    """Главная функция"""
    driver = webdriver.Chrome()
    
    try:
        print("🚀 Автоматический помощник для тестов")
        print("=" * 50)
        input("📖 Откройте страницу с тестом и нажмите Enter...")
        
        # Получаем HTML
        html = driver.page_source
        url = driver.current_url
        
        print(f"🌐 Страница: {url}")
        print("🔍 Анализирую структуру...")
        
        # Парсим вопросы
        questions = parse_page_simple(html)
        print(f"🎯 Найдено вопросов: {len(questions)}")
        
        if not questions:
            print("❌ Вопросы не найдены. Попробуйте:")
            print("   - Обновить страницу")
            print("   - Убедиться что тест загружен")
            return
        
        # Обрабатываем каждый вопрос
        print("\n🤔 Получаю ответы от нейросети...")
        print("=" * 50)
        
        for i, question in enumerate(questions, 1):
            print(f"\n{i}. {question['text'][:100]}...")
            
            # Получаем ответ
            answer = get_ai_answer_sync(question)
            
            print(f"   ✅ ОТВЕТ: {answer['correct_answer']}")
            print(f"   💡 {answer['explanation'][:100]}...")
            
            # Пауза между запросами
            time.sleep(2)
            
        print("\n" + "=" * 50)
        print("🎉 Анализ завершен!")
        
    except Exception as e:
        print(f"💥 Ошибка: {e}")
    finally:
        input("Нажмите Enter для закрытия браузера...")
        driver.quit()

if __name__ == "__main__":
    main()