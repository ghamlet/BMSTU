# backup_ai_helper.py
import requests
import json
import time
from typing import List, Dict

OPENROUTER_API_KEY = "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"

def get_ai_answer_simple(question: Dict) -> Dict:
    """Метод через OpenRouter"""
    
    prompt = f"""
    Вопрос теста по английскому:
    {question['text']}
    
    Варианты ответов:
    {chr(10).join([f"{chr(65+i)}. {opt}" for i, opt in enumerate(question['options'])])}
    
    Ответь в JSON формате:
    {{
        "correct_answer": "правильный вариант",
        "explanation": "объяснение на русском",
        "confidence": "уровень уверенности"
    }}
    """
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/educational-assistant",
                "X-Title": "Test Assistant"
            },
            json={
                "model": "meta-llama/llama-3.3-70b-instruct:free",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500,
                "temperature": 0.1
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            text = result["choices"][0]["message"]["content"]
            
            # Парсим JSON ответ
            try:
                json_start = text.find('{')
                json_end = text.rfind('}') + 1
                if json_start != -1 and json_end != 0:
                    answer_data = json.loads(text[json_start:json_end])
                    return {
                        'question_id': question['id'],
                        'question_text': question['text'],
                        'correct_answer': answer_data.get('correct_answer', 'Не найден'),
                        'explanation': answer_data.get('explanation', text),
                        'confidence': answer_data.get('confidence', 'средняя'),
                        'is_correct': True
                    }
            except:
                pass
            
            return {
                'question_id': question['id'],
                'question_text': question['text'],
                'correct_answer': 'Смотри объяснение',
                'explanation': text,
                'confidence': 'средняя',
                'is_correct': True
            }
        else:
            error_text = response.text
            return create_error_response(question, f"HTTP {response.status_code}: {error_text}")
            
    except Exception as e:
        return create_error_response(question, f"Ошибка: {str(e)}")

def create_error_response(question: Dict, error: str) -> Dict:
    return {
        'question_id': question['id'],
        'question_text': question['text'],
        'correct_answer': 'Ошибка',
        'explanation': error,
        'confidence': 'низкая',
        'is_correct': False
    }

def get_ai_answers_sync(questions: List[Dict]) -> List[Dict]:
    answers = []
    for i, question in enumerate(questions):
        print(f"🤔 Анализирую вопрос {i+1}/{len(questions)}...")
        answer = get_ai_answer_simple(question)
        answers.append(answer)
        time.sleep(1)  # Задержка между запросами
    return answers