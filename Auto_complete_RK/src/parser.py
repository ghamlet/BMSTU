from bs4 import BeautifulSoup
import re

def parse_test_page(html_content):
    """Парсит HTML страницу теста и извлекает вопросы"""
    soup = BeautifulSoup(html_content, 'html.parser')
    questions = []
    
    # Ищем вопросы по разным возможным структурам
    question_elements = soup.find_all(class_=re.compile(r'que|question|quiz'))
    
    for i, element in enumerate(question_elements):
        try:
            question_data = extract_question_data(element, i)
            if question_data:
                questions.append(question_data)
        except Exception as e:
            print(f"Ошибка парсинга вопроса {i}: {e}")
            continue
    
    # Если не нашли по классам, ищем по структуре
    if not questions:
        questions = fallback_parse(soup)
    
    return questions

def extract_question_data(question_element, index):
    """Извлекает данные из элемента вопроса"""
    
    # Извлекаем текст вопроса
    question_text = ""
    qtext_elem = question_element.find(class_=re.compile(r'qtext|question-text'))
    if qtext_elem:
        question_text = qtext_elem.get_text(strip=True)
    else:
        # Альтернативный поиск
        for elem in question_element.find_all(['p', 'div']):
            text = elem.get_text(strip=True)
            if len(text) > 20 and '?' in text:
                question_text = text
                break
    
    if not question_text:
        return None
    
    # Извлекаем варианты ответов
    options = []
    answer_elements = question_element.find_all(class_=re.compile(r'answer|option|choice'))
    
    for answer_elem in answer_elements:
        # Ищем radio buttons и их labels
        radios = answer_elem.find_all('input', type='radio')
        for radio in radios:
            label = answer_elem.find('label')
            if label:
                option_text = label.get_text(strip=True)
                if option_text and option_text not in options:
                    options.append(option_text)
        
        # Если не нашли radio, ищем текст напрямую
        if not options:
            text_elements = answer_elem.find_all(['td', 'div', 'span'])
            for elem in text_elements:
                text = elem.get_text(strip=True)
                if text and len(text) > 1 and text not in options:
                    options.append(text)
    
    # Убираем дубликаты и очищаем
    options = list(dict.fromkeys([opt.strip() for opt in options if opt.strip()]))
    
    return {
        'id': f'question_{index}',
        'text': question_text,
        'options': options,
        'element_html': str(question_element)
    }

def fallback_parse(soup):
    """Альтернативный метод парсинга"""
    questions = []
    
    # Ищем все элементы с текстом, похожим на вопросы
    all_elements = soup.find_all(['p', 'div', 'td'])
    
    current_question = None
    for elem in all_elements:
        text = elem.get_text(strip=True)
        
        # Определяем, является ли элемент вопросом
        if is_likely_question(text):
            if current_question:
                questions.append(current_question)
            
            current_question = {
                'id': f'question_{len(questions)}',
                'text': text,
                'options': []
            }
        
        # Если это вариант ответа
        elif current_question and is_likely_option(text):
            current_question['options'].append(text)
    
    if current_question:
        questions.append(current_question)
    
    return questions

def is_likely_question(text):
    """Определяет, похож ли текст на вопрос"""
    if len(text) < 10:
        return False
    
    question_indicators = ['?', '…', '_____', 'choose', 'select', 'what', 'which', 'how']
    return any(indicator in text.lower() for indicator in question_indicators)

def is_likely_option(text):
    """Определяет, похож ли текст на вариант ответа"""
    if len(text) < 2 or len(text) > 100:
        return False
    
    # Варианты ответов обычно короткие
    return text[0].isalpha() and text[0].islower() and len(text.split()) < 10