from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from parser import parse_test_page
from ai_helper import get_ai_answers_sync
import time

def quick_analyze():
    """Быстрый анализ текущей страницы"""
    print("🚀 Запуск быстрого анализа...")
    
    # Настройка браузера
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Фоновый режим
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Получаем HTML текущей активной вкладки
        html_content = driver.page_source
        
        print("🔍 Парсинг вопросов...")
        questions = parse_test_page(html_content)
        
        if not questions:
            print("❌ Вопросы не найдены. Убедитесь что страница с тестом открыта.")
            return
        
        print(f"📚 Найдено вопросов: {len(questions)}")
        
        # Получаем ответы от ИИ
        print("🧠 Получение ответов от ИИ...")
        answers = get_ai_answers_sync(questions)
        
        # Выводим результаты
        print("\n" + "="*60)
        print("🤖 РЕЗУЛЬТАТЫ АНАЛИЗА")
        print("="*60)
        
        for i, (question, answer) in enumerate(zip(questions, answers), 1):
            print(f"\n{i}. {question['text']}")
            print(f"   ✅ Ответ: {answer['correct_answer']}")
            print(f"   📖 {answer['explanation'][:100]}...")
            print(f"   ⚡ Уверенность: {answer['confidence']}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    quick_analyze()