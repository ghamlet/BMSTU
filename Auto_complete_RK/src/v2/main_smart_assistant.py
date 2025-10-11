# main_smart_assistant.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import asyncio
from smart_parser import parse_page_with_ai, clean_parsed_questions
from smart_ai_helper import get_ai_answers_sync
import json

class SmartTestAssistant:
    def __init__(self):
        self.driver = None
        
    def setup_browser(self):
        """Настраивает браузер"""
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    async def analyze_current_page(self):
        """Анализирует текущую страницу"""
        if not self.driver:
            self.setup_browser()
        
        print("🚀 Умный помощник для тестов запущен!")
        print("📖 Перейдите на страницу с тестом и нажмите Enter...")
        input()
        
        # Получаем HTML страницы
        html_content = self.driver.page_source
        print(html_content)
        current_url = self.driver.current_url
        
        print(f"🌐 Анализирую страницу: {current_url}")
        print(f"📄 Размер HTML: {len(html_content)} символов")
        
        # Парсим страницу с помощью нейросети
        print("🔍 Нейросеть анализирует структуру страницы...")
        parsed_data = await parse_page_with_ai(html_content)
        
        # Очищаем и нормализуем вопросы
        questions = clean_parsed_questions(parsed_data)
        
        print(f"🎯 Найдено вопросов: {len(questions)}")
        
        if questions:
            # Показываем найденные вопросы
            self.display_questions(questions)
            
            # Получаем ответы от ИИ
            print("\n🤔 Нейросеть анализирует вопросы...")
            answers = get_ai_answers_sync(questions)
            
            # Показываем результаты
            self.display_results(answers)
            
            # Сохраняем результаты
            self.save_results(questions, answers, current_url)
            
        else:
            print("❌ Не удалось найти вопросы на странице")
            print("💡 Попробуйте:")
            print("   - Обновить страницу")
            print("   - Убедиться что тест загружен")
            print("   - Проверить подключение к интернету")
    
    def display_questions(self, questions: list):
        """Показывает найденные вопросы"""
        print("\n" + "📋 НАЙДЕННЫЕ ВОПРОСЫ:" + "="*50)
        for i, q in enumerate(questions, 1):
            print(f"\n{i}. {q['text'][:100]}...")
            print(f"   Варианты: {', '.join(q['options'][:3])}{'...' if len(q['options']) > 3 else ''}")
    
    def display_results(self, answers: list):
        """Показывает результаты"""
        print("\n" + "🎪 РЕЗУЛЬТАТЫ АНАЛИЗА:" + "="*50)
        
        correct_count = sum(1 for a in answers if a.get('is_correct', False))
        
        for i, answer in enumerate(answers, 1):
            print(f"\n{i}. {answer['question_text'][:80]}...")
            print(f"   ✅ ОТВЕТ: {answer['correct_answer']}")
            print(f"   📝 {answer['explanation'][:100]}...")
            print(f"   🎯 Уверенность: {answer.get('confidence', 'неизвестно')}")
            
            if not answer.get('is_correct', False):
                print(f"   ⚠️  Возможна ошибка в анализе")
        
        print(f"\n📊 ИТОГО: {correct_count}/{len(answers)} вопросов успешно проанализировано")
    
    def save_results(self, questions: list, answers: list, url: str):
        """Сохраняет результаты в файл"""
        results = {
            "url": url,
            "questions": questions,
            "answers": answers,
            "summary": {
                "total_questions": len(questions),
                "successful_answers": sum(1 for a in answers if a.get('is_correct', False)),
                "timestamp": asyncio.get_event_loop().time()
            }
        }
        
        with open("test_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Результаты сохранены в test_results.json")
    
    def close(self):
        """Закрывает браузер"""
        if self.driver:
            self.driver.quit()

async def main():
    assistant = SmartTestAssistant()
    
    try:
        await assistant.analyze_current_page()
    except Exception as e:
        print(f"💥 Критическая ошибка: {e}")
    finally:
        assistant.close()

if __name__ == "__main__":
    asyncio.run(main())

