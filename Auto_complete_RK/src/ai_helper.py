import os
import json
import aiohttp
import asyncio
from typing import List, Dict

# Настройка API ключа OpenRouter
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "your-openrouter-api-key-here")
OPENROUTER_API_KEY = "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"

# Модели OpenRouter
MODELS = [
    "meta-llama/llama-3.3-70b-instruct:free",
    "qwen/qwen2.5-vl-3b-instruct:free", 
    "meta-llama/llama-4-scout:free",
    "deepseek/deepseek-v3-base:free"
]

# Основная модель для финального ответа
MAIN_MODEL = "meta-llama/llama-4-scout:free"

# Системный промпт для тестов по английскому
ENGLISH_TEST_SYSTEM_PROMPT = """
Ты эксперт по английскому языку и образовательным тестам. Твоя задача - анализировать вопросы тестов по английскому языку и давать правильные ответы с объяснениями.

Ты должен:
1. Тщательно анализировать вопрос и варианты ответов
2. Выбирать правильный вариант на основе грамматики, лексики и контекста
3. Давать четкое объяснение выбора
4. Объяснять, почему другие варианты неправильные (если возможно)

Всегда отвечай в формате JSON:
{
    "correct_answer": "выбранный вариант ответа",
    "explanation": "развернутое объяснение на русском языке",
    "confidence": "высокая/средняя/низкая",
    "grammar_rules": "примененные грамматические правила",
    "why_others_wrong": "почему другие варианты неправильные"
}

Будь точным и уверенным в своих ответах!
"""

async def get_model_response(session: aiohttp.ClientSession, model: str, prompt: str) -> Dict:
    """Получает ответ от конкретной модели"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": ENGLISH_TEST_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 800
    }
    
    try:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                result = await response.json()
                return {
                    "model": model,
                    "response": result["choices"][0]["message"]["content"],
                    "status": "success"
                }
            else:
                error = await response.text()
                return {
                    "model": model,
                    "response": f"Ошибка: {response.status}, {error}",
                    "status": "error"
                }
    except Exception as e:
        return {
            "model": model,
            "response": f"Ошибка соединения: {str(e)}",
            "status": "error"
        }

async def get_all_models_responses(prompt: str) -> List[Dict]:
    """Получает ответы от всех моделей"""
    async with aiohttp.ClientSession() as session:
        tasks = [get_model_response(session, model, prompt) for model in MODELS]
        return await asyncio.gather(*tasks)

async def process_with_main_model(prompt: str, responses: List[Dict]) -> str:
    """Обрабатывает ответы с помощью основной модели"""
    # Выбираем только успешные ответы
    success_responses = [r for r in responses if r["status"] == "success"]
    
    if not success_responses:
        return "Все модели вернули ошибки"
    
    # Формируем контекст для основной модели
    context = "Ответы других моделей на этот вопрос:\n"
    for resp in success_responses:
        context += f"\n--- {resp['model']} ---\n{resp['response']}\n"
    
    # Запрашиваем анализ у основной модели
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    
    final_prompt = f"""
    Оригинальный вопрос: {prompt}
    
    {context}
    
    Проанализируй ответы других моделей и дай итоговый, самый точный ответ в формате JSON.
    Учти все мнения и выбери наиболее правильный вариант.
    """
    
    data = {
        "model": MAIN_MODEL,
        "messages": [
            {"role": "system", "content": ENGLISH_TEST_SYSTEM_PROMPT},
            {"role": "user", "content": final_prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 1000
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                result = await response.json()
                return result["choices"][0]["message"]["content"]
            else:
                error = await response.text()
                return f"Ошибка при запросе к основной модели: {error}"

async def get_single_model_response(prompt: str) -> str:
    """Получает ответ от одной модели (основной)"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    
    data = {
        "model": MAIN_MODEL,
        "messages": [
            {"role": "system", "content": ENGLISH_TEST_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 800
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                result = await response.json()
                return result["choices"][0]["message"]["content"]
            else:
                error = await response.text()
                return f"Ошибка: {response.status}, {error}"

async def get_neural_response(prompt: str, use_several_models: bool = False) -> str:
    """Основная функция для получения ответа"""
    
    if use_several_models:
        # Получаем ответы от всех моделей
        all_responses = await get_all_models_responses(prompt)
        
        # Обрабатываем ответы с помощью основной модели
        final_response = await process_with_main_model(prompt, all_responses)
        
        # Формируем полный отчет (для отладки)
        report = f"ФИНАЛЬНЫЙ ОТВЕТ:\n{final_response}\n\n"
        report += "ОТВЕТЫ ВСЕХ МОДЕЛЕЙ:\n"
        for resp in all_responses:
            report += f"\n--- {resp['model']} ({resp['status']}) ---\n{resp['response']}\n"
        
        return final_response  # Возвращаем только финальный ответ

    else:
        # Используем одну модель
        return await get_single_model_response(prompt)

def parse_ai_response(response_text: str) -> Dict:
    """Парсит ответ от ИИ в структурированный формат"""
    try:
        # Пытаемся найти JSON в ответе
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        
        if json_start != -1 and json_end != 0:
            json_str = response_text[json_start:json_end]
            return json.loads(json_str)
        else:
            # Если JSON не найден, создаем структурированный ответ из текста
            lines = response_text.split('\n')
            correct_answer = None
            explanation = response_text
            
            # Пытаемся извлечить правильный ответ из текста
            for line in lines:
                if 'correct_answer' in line.lower() or 'правильный ответ' in line.lower():
                    parts = line.split(':')
                    if len(parts) > 1:
                        correct_answer = parts[1].strip()
                        break
            
            return {
                "correct_answer": correct_answer or "Не удалось определить",
                "explanation": explanation,
                "confidence": "средняя",
                "grammar_rules": "Не указано",
                "why_others_wrong": "Не указано"
            }
            
    except Exception as e:
        return {
            "correct_answer": "Ошибка парсинга",
            "explanation": f"Не удалось распарсить ответ ИИ: {str(e)}",
            "confidence": "низкая",
            "grammar_rules": "Не указано", 
            "why_others_wrong": "Не указано"
        }

async def get_single_answer(question: Dict) -> Dict:
    """Получает ответ на один вопрос"""
    
    prompt = f"""
    Вопрос теста по английскому языку:
    
    {question['text']}
    
    Варианты ответов:
    {chr(10).join([f"{i+1}. {opt}" for i, opt in enumerate(question['options'])])}
    
    Проанализируй вопрос и дай правильный ответ с объяснением.
    """
    
    try:
        ai_response = await get_neural_response(prompt, use_several_models=False)
        result_data = parse_ai_response(ai_response)
        
        return {
            'question_id': question['id'],
            'question_text': question['text'],
            'correct_answer': result_data.get('correct_answer', 'Не определено'),
            'explanation': result_data.get('explanation', 'Объяснение не предоставлено'),
            'confidence': result_data.get('confidence', 'неизвестно'),
            'grammar_rules': result_data.get('grammar_rules', 'Не указано'),
            'why_others_wrong': result_data.get('why_others_wrong', 'Не указано'),
            'is_correct': True
        }
        
    except Exception as e:
        print(f"Ошибка получения ответа для вопроса {question['id']}: {e}")
        return {
            'question_id': question['id'],
            'question_text': question['text'],
            'correct_answer': 'Не удалось получить ответ',
            'explanation': f'Ошибка при обработке вопроса: {str(e)}',
            'confidence': 'низкая',
            'grammar_rules': 'Не указано',
            'why_others_wrong': 'Не указано',
            'is_correct': False
        }

async def get_ai_answers(questions: List[Dict]) -> List[Dict]:
    """Получает ответы на вопросы от ИИ (асинхронная версия)"""
    answers = []
    
    # Обрабатываем вопросы последовательно чтобы избежать rate limits
    for question in questions:
        answer = await get_single_answer(question)
        answers.append(answer)
        
        # Небольшая задержка между запросами
        await asyncio.sleep(1)
    
    return answers

# Синхронная обертка для совместимости
def get_ai_answers_sync(questions: List[Dict]) -> List[Dict]:
    """Синхронная версия для обратной совместимости"""
    return asyncio.run(get_ai_answers(questions))

# Альтернатива с использованием нескольких моделей для сложных вопросов
async def get_ai_answers_advanced(questions: List[Dict], use_multiple_models: bool = False) -> List[Dict]:
    """Продвинутая версия с возможностью использования нескольких моделей"""
    answers = []
    
    for i, question in enumerate(questions):
        print(f"Обработка вопроса {i+1}/{len(questions)}...")
        
        # Для сложных вопросов используем несколько моделей
        is_complex = len(question['options']) > 3 or any(keyword in question['text'].lower() for keyword in ['grammar', 'tense', 'conditional', 'subjunctive'])
        
        prompt = f"""
        Вопрос теста по английскому языку:
        
        {question['text']}
        
        Варианты ответов:
        {chr(10).join([f"{i+1}. {opt}" for i, opt in enumerate(question['options'])])}
        """
        
        try:
            ai_response = await get_neural_response(prompt, use_several_models=use_multiple_models and is_complex)
            result_data = parse_ai_response(ai_response)
            
            answer = {
                'question_id': question['id'],
                'question_text': question['text'],
                'correct_answer': result_data.get('correct_answer', 'Не определено'),
                'explanation': result_data.get('explanation', 'Объяснение не предоставлено'),
                'confidence': result_data.get('confidence', 'неизвестно'),
                'grammar_rules': result_data.get('grammar_rules', 'Не указано'),
                'why_others_wrong': result_data.get('why_others_wrong', 'Не указано'),
                'is_correct': True,
                'used_multiple_models': use_multiple_models and is_complex
            }
            
        except Exception as e:
            print(f"Ошибка получения ответа для вопроса {question['id']}: {e}")
            answer = {
                'question_id': question['id'],
                'question_text': question['text'],
                'correct_answer': 'Не удалось получить ответ',
                'explanation': f'Ошибка при обработке вопроса: {str(e)}',
                'confidence': 'низкая',
                'is_correct': False,
                'used_multiple_models': False
            }
        
        answers.append(answer)
        await asyncio.sleep(1.5)  # Увеличиваем задержку для rate limits
    
    return answers