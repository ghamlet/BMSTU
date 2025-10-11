from selenium import webdriver
import requests
import json
from parser import parse_test_page
from ai_helper import get_ai_answers_sync

def auto_extract_and_analyze():
    """Автоматически извлекает HTML и анализирует"""
    print("🌐 Автоматический анализ страницы...")
    
    # Используем существующий браузер
    driver = webdriver.Chrome()
    
    try:
        # Даем время пользователю перейти на нужную страницу
        input("📖 Откройте страницу с тестом и нажмите Enter...")
        
        # Получаем текущий URL и HTML
        current_url = driver.current_url
        html_content = driver.page_source
        
        print(f"📄 Анализирую: {current_url}")
        print(f"📊 Размер HTML: {len(html_content)} символов")
        
        # Парсим вопросы
        questions = parse_test_page(html_content)
        print(f"🎯 Найдено вопросов: {len(questions)}")
        
        if questions:
            # Получаем ответы от ИИ
            print("🤔 Получаю ответы от нейросети...")
            answers = get_ai_answers_sync(questions)
            
            # Выводим результаты
            print("\n" + "🎪 РЕЗУЛЬТАТЫ:" + "\n" + "="*50)
            
            for i, (q, a) in enumerate(zip(questions, answers), 1):
                print(f"\n{i}. {q['text'][:80]}...")
                print(f"   🎯 ОТВЕТ: {a['correct_answer']}")
                print(f"   💡 {a['explanation'][:80]}...")
                
        else:
            print("❌ Не удалось найти вопросы. Проверьте HTML структуру.")
            
    except Exception as e:
        print(f"💥 Ошибка: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    auto_extract_and_analyze()