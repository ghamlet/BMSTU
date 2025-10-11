from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from parser import parse_test_page
from ai_helper import get_ai_answers_sync
import os

class TestAssistant:
    def __init__(self):
        self.setup_driver()
        
    def setup_driver(self):
        """Настраивает Chrome драйвер"""
        chrome_options = Options()
        chrome_options.add_argument("--user-data-ddir=./chrome_profile")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
    def get_current_page_html(self):
        """Получает HTML текущей страницы"""
        return self.driver.page_source
    
    def extract_test_questions(self, html_content):
        """Извлекает вопросы из HTML"""
        return parse_test_page(html_content)
    
    def display_answers_in_terminal(self, questions, answers):
        """Красиво выводит ответы в терминал"""
        print("\n" + "="*80)
        print("🤖 AI TEST ASSISTANT - РЕЗУЛЬТАТЫ")
        print("="*80)
        
        for i, (question, answer) in enumerate(zip(questions, answers), 1):
            print(f"\n{'━'*40}")
            print(f"ВОПРОС {i}:")
            print(f"{'━'*40}")
            print(f"📝 {question['text']}")
            print(f"\n📋 Варианты:")
            for j, option in enumerate(question['options'], 1):
                print(f"   {j}. {option}")
            
            print(f"\n✅ ПРАВИЛЬНЫЙ ОТВЕТ:")
            print(f"   🎯 {answer['correct_answer']}")
            
            print(f"\n📚 Объяснение:")
            print(f"   {answer['explanation']}")
            
            print(f"\n⚡ Уверенность: {answer['confidence']}")
            
            if answer.get('grammar_rules') and answer['grammar_rules'] != 'Не указано':
                print(f"\n📖 Грамматические правила:")
                print(f"   {answer['grammar_rules']}")
            
            if answer.get('why_others_wrong') and answer['why_others_wrong'] != 'Не указано':
                print(f"\n❌ Почему другие неправильные:")
                print(f"   {answer['why_others_wrong']}")
    
    def analyze_current_page(self):
        """Анализирует текущую страницу и выводит ответы"""
        print("🔄 Получаю HTML текущей страницы...")
        
        # Получаем HTML
        html_content = self.get_current_page_html()
        
        print("🔍 Парсинг вопросов...")
        questions = self.extract_test_questions(html_content)
        
        if not questions:
            print("❌ Не удалось найти вопросы на странице")
            return
        
        print(f"📚 Найдено вопросов: {len(questions)}")
        
        # Показываем найденные вопросы
        for i, q in enumerate(questions, 1):
            print(f"\n{i}. {q['text']}")
            print(f"   Варианты: {', '.join(q['options'][:3])}{'...' if len(q['options']) > 3 else ''}")
        
        # Получаем ответы от ИИ
        print(f"\n🧠 Запрашиваю ответы у ИИ...")
        answers = get_ai_answers_sync(questions)
        
        # Выводим результаты
        self.display_answers_in_terminal(questions, answers)
        
        return questions, answers
    
    def wait_for_user_input(self):
        """Ждет команды пользователя"""
        print(f"\n{'='*80}")
        print("Управление:")
        print("  [Enter] - обновить и проанализировать страницу")
        print("  'q' + [Enter] - выйти")
        print("  's' + [Enter] - сохранить результаты в файл")
        return input("Введите команду: ").strip().lower()
    
    def save_to_file(self, questions, answers):
        """Сохраняет результаты в файл"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"test_results_{timestamp}.json"
        
        data = {
            "timestamp": timestamp,
            "questions": questions,
            "answers": answers
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Результаты сохранены в {filename}")
    
    def run(self):
        """Основной цикл работы"""
        print("🚀 AI Test Assistant запущен!")
        print("📖 Откройте страницу с тестом в браузере и нажмите Enter для анализа")
        
        try:
            while True:
                command = self.wait_for_user_input()
                
                if command == 'q':
                    break
                elif command == 's':
                    # Сохраняем последние результаты
                    if hasattr(self, 'last_questions') and hasattr(self, 'last_answers'):
                        self.save_to_file(self.last_questions, self.last_answers)
                    else:
                        print("❌ Сначала проанализируйте страницу")
                    continue
                elif command == '':
                    # Анализируем текущую страницу
                    try:
                        self.last_questions, self.last_answers = self.analyze_current_page()
                    except Exception as e:
                        print(f"❌ Ошибка при анализе: {e}")
                else:
                    print("❌ Неизвестная команда")
        
        except KeyboardInterrupt:
            print("\n👋 Завершение работы...")
        finally:
            self.driver.quit()

def main():
    """Точка входа для автоматического анализа"""
    assistant = TestAssistant()
    
    # Можно также сделать автоматический анализ при запуске
    print("🎯 Автоматический анализ активной страницы...")
    assistant.analyze_current_page()
    
    # Или запустить интерактивный режим
    # assistant.run()

if __name__ == "__main__":
    main()