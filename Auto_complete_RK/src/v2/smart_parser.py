# smart_parser.py
import aiohttp
import asyncio
import json
from typing import List, Dict

OPENROUTER_API_KEY = "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"

PARSER_SYSTEM_PROMPT = """
Ты - эксперт по парсингу веб-страниц образовательных тестов. Твоя задача - анализировать HTML код страницы теста и извлекать структурированную информацию о вопросах.

Ты должен:
1. Найти все вопросы на странице
2. Извлечь текст каждого вопроса
3. Найти все варианты ответов для каждого вопроса
4. Определить тип вопроса (multiple choice, multianswer, etc.)
5. Сохранить структуру в JSON формате

Формат ответа:
{
    "questions": [
        {
            "id": "уникальный идентификатор",
            "text": "полный текст вопроса",
            "type": "multiple_choice/multianswer/etc",
            "options": ["вариант1", "вариант2", "вариант3"],
            "context": "дополнительный контекст если есть"
        }
    ],
    "total_questions": число,
    "test_title": "название теста"
}

Будь внимателен к деталям и извлекай всю информацию точно!
"""

async def parse_page_with_ai(html_content: str) -> Dict:
    """Парсит страницу с помощью нейросети"""
    
    # Ограничиваем размер HTML чтобы влезло в контекст
    truncated_html = html_content[:15000]  # Первые 15к символов обычно достаточно
    
    prompt = f"""
    Проанализируй этот HTML код страницы теста и извлеки все вопросы с вариантами ответов:
    
    ```html
    {truncated_html}
    ```
    
    ВАЖНО: Обрати внимание на:
    - Элементы с классами содержащими "que", "question", "quiz"
    - Таблицы с вариантами ответов
    - Radio buttons и их labels
    - Текст вопросов и вариантов
    
    Верни только чистый JSON без дополнительного текста.
    """
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    
    data = {
        "model": "meta-llama/llama-4-scout:free",
        "messages": [
            {"role": "system", "content": PARSER_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,
        "max_tokens": 2000
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                result = await response.json()
                response_text = result["choices"][0]["message"]["content"]
                
                # Пытаемся извлечь JSON из ответа
                try:
                    json_start = response_text.find('{')
                    json_end = response_text.rfind('}') + 1
                    if json_start != -1 and json_end != 0:
                        json_str = response_text[json_start:json_end]
                        return json.loads(json_str)
                    else:
                        # Если JSON не найден, создаем базовую структуру
                        return {
                            "questions": [],
                            "total_questions": 0,
                            "test_title": "Не удалось распарсить",
                            "error": "Неверный формат ответа ИИ"
                        }
                except Exception as e:
                    return {
                        "questions": [],
                        "total_questions": 0, 
                        "test_title": "Ошибка парсинга",
                        "error": str(e)
                    }
            else:
                error = await response.text()
                return {
                    "questions": [],
                    "total_questions": 0,
                    "test_title": "Ошибка API",
                    "error": f"HTTP {response.status}: {error}"
                }

def clean_parsed_questions(parsed_data: Dict) -> List[Dict]:
    """Очищает и нормализует данные от нейросети"""
    questions = []
    print(parsed_data)
    
    if "questions" not in parsed_data:
        return questions
    
    for i, q in enumerate(parsed_data["questions"]):
        # Нормализуем структуру вопроса
        question_text = q.get("text", "").strip()
        options = q.get("options", [])
        
        # Фильтруем пустые варианты
        options = [opt.strip() for opt in options if opt and opt.strip()]
        
        if question_text and options:
            questions.append({
                "id": q.get("id", f"question_{i}"),
                "text": question_text,
                "options": options,
                "type": q.get("type", "multiple_choice"),
                "context": q.get("context", "")
            })
    
    return questions