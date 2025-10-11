# quick_start.py
from selenium import webdriver
import asyncio
from smart_parser import parse_page_with_ai, clean_parsed_questions
from smart_ai_helper import get_ai_answers

async def quick_analyze():
    """Быстрый анализ текущей страницы"""
    driver = webdriver.Chrome()
    
    try:
        print("🚀 Быстрый анализ теста")
        input("📖 Откройте страницу с тестом и нажмите Enter...")
        
        html = driver.page_source
        current_url = driver.current_url
        print(f"🌐 Анализирую: {current_url}")
        print("🔍 Нейросеть анализирует страницу...")
        
        # Парсинг нейросетью
        parsed = await parse_page_with_ai(html)
        questions = clean_parsed_questions(parsed)
        
        print(f"🎯 Найдено вопросов: {len(questions)}")
        
        if questions:
            # Показываем вопросы
            for i, q in enumerate(questions, 1):
                print(f"\n{i}. {q['text'][:100]}...")
                print(f"   Варианты: {', '.join(q['options'][:3])}{'...' if len(q['options']) > 3 else ''}")
            
            # Получаем ответы (асинхронно)
            print("\n🤔 Нейросеть анализирует вопросы...")
            answers = await get_ai_answers(questions)
            
            # Выводим результаты
            print("\n" + "🎪 РЕЗУЛЬТАТЫ:" + "="*50)
            for i, answer in enumerate(answers, 1):
                print(f"\n{i}. {answer['question_text'][:80]}...")
                print(f"   ✅ ОТВЕТ: {answer['correct_answer']}")
                print(f"   💡 {answer['explanation'][:80]}...")
                print(f"   🎯 Уверенность: {answer.get('confidence', 'неизвестно')}")
                
        else:
            print("❌ Не удалось найти вопросы на странице")
            
    except Exception as e:
        print(f"💥 Ошибка: {e}")
    finally:
        driver.quit()

def main():
    """Главная функция для запуска"""
    asyncio.run(quick_analyze())

if __name__ == "__main__":
    main()