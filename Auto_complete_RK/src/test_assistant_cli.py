#!/usr/bin/env python3
import argparse
from selenium import webdriver
from parser import parse_test_page
from ai_helper import get_ai_answers_sync

def main():
    parser = argparse.ArgumentParser(description='AI Test Assistant - автоматический анализ тестов')
    parser.add_argument('--url', help='URL страницы с тестом')
    parser.add_argument('--auto', action='store_true', help='Автоанализ текущей вкладки')
    
    args = parser.parse_args()
    
    driver = webdriver.Chrome()
    
    try:
        if args.url:
            print(f"🌐 Открываю: {args.url}")
            driver.get(args.url)
        else:
            print("📖 Используется текущая открытая страница")
        
        # Ждем загрузки
        input("Нажмите Enter когда страница загрузится...")
        
        # Анализируем
        html = driver.page_source
        questions = parse_test_page(html)
        
        print(f"🎯 Найдено вопросов: {len(questions)}")
        
        if questions:
            answers = get_ai_answers_sync(questions)
            
            print("\n" + "🤖 РЕЗУЛЬТАТЫ:" + "="*40)
            for i, (q, a) in enumerate(zip(questions, answers), 1):
                print(f"\n{i}. {q['text']}")
                print(f"   ✅ {a['correct_answer']}")
                print(f"   💡 {a['explanation']}")
                
    except KeyboardInterrupt:
        print("\n👋 Завершено")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()