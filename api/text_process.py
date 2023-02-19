import re
#from audio2text import get_text
import os
import requests
import json
from nltk.stem.snowball import SnowballStemmer
import heapq


url_to_section = {'добавить проект': 'https://grants.myrosmol.ru/projects/create/386d79e1-1fa9-4e9d-9357-f8777644bcde:1c49a8d0-35c1-43c3-894e-ed03087dceaa',
                  'мои проекты': 'https://grants.myrosmol.ru/projects',
                  'мои заявки': 'https://grants.myrosmol.ru/participants',
                  'архив проектов': 'https://grants.myrosmol.ru/projects-archive',
                  'мероприятия': 'https://grants.myrosmol.ru/events',
                  'мои проекты': 'https://grants.myrosmol.ru/projects',
                  'грантовые соглашения': 'https://grants.myrosmol.ru/agreements',
                  'отчеты': 'https://grants.myrosmol.ru/reports',
                  'профиль': 'https://grants.myrosmol.ru/profile',
                  'часто задаваемые вопросы': 'https://grants.myrosmol.ru/help',
                  'база знаний': 'https://grants.myrosmol.ru/articles'}
action_words = {'навигация': ['сдела', 'добав', 'посмотрет', 'глянут', 'узна',
                              'отслед', 'перейт', 'провер', 'откр', 'ознаком', 'найт'],
                'заполнение': ['заполня', 'внос', 'написа', 'вписа', 'внест', 'добав',
                               'нужн', 'описа', 'писа', 'вписа', 'записа', 'снят']}
words_to_section = {'добавить проект': ['созда', 'сдела', 'описа', 'добав'],
               'мои проекты': ['сохранен', 'реализова', 'созда', 'посмотрет', 'глянут', 'узна', 'отслед', 'перейт',
                               'проект', 'мо'],
               'мои заявки': ['заявк', 'провер', 'посмотрет', 'откр', 'просмотрет', 'статус',
                              'глянут', 'узна', 'отслед', 'перейт', 'заявок', 'нов'],
                    'архив проектов': ['сохранен', 'реализова', 'созда', 'посмотрет', 'глянут', 'арх',
                                       'прошл', 'предыдущ', 'проект'],
                'мероприятия': ['нов', 'мероприят', 'событ', 'форум', 'встреч', 'перейт'],
                'грантовые соглашения': ['грант',' грантов', 'соглашен', 'договорен', 'договор', 'перейт'],
                'отчеты': ['отчетн', 'отчет', 'файл', 'смет', 'чек'],
                'профиль': ['личн', 'кабинет', 'анкет', 'информац', 'пользоаател', 'лк'],
                'часто задаваемые вопросы': ['вопрос', 'faq', 'задава'],
                'база знаний': ['файл', 'шаблон', 'cтат', 'документ', 'грант', 'базо', 'знан']}
detect_faq = {'обратная связь по гранту': ['обратн', 'связ', 'узна', 'грант', 'вопрос', 'информац'],
       'обновление данных профиля ГАИС': ['обновлен', 'дан', 'госуслуг', 'гаис', 'информац', 'профил'],
       'перезайти ЕСИА': ['перезайт', 'обнов', 'ес'],
       'не сохраняются изменения в профиле': ['сохраня', 'изменен', 'профил'],
       'не отображается созданный проект': ['отобража', 'созда', 'проект', 'вид', 'просматрива', 'отсутсв'],
       'ошибка 404': ['появля', 'выда', 'выскакива', '404', 'ошибк', 'error'],
       'аккаунт верифицирован, галочки в профиле нет (подтвердить профиль ЕСИА)': ['верифицирова', 'галочк', 'видн'],
       'баллы': ['балл', 'очк', 'цифр'],
       'отвязать ЕСИА (отменить верификацию)': ['отвяза', 'ес', 'отмен', 'верификац', 'отказа'],
       'не дает редактировать данные': ['ошибк', 'редактирован', 'дан', 'проблем', 'дает'],
       'узнать id профиля': ['узна', 'id', 'посмотрет', 'профил'],
       'создать кабинет НКО': ['созда', 'кабинет', 'нко', 'зарегистрирова'],
       'аккаунт иностранца': ['иностранц', 'аккаунт', 'иностра'],
       'регистрация мероприятия на АИ': ['регистрац', 'мероприят', 'зарегистрирова'],
       'смена почты от аккаунта': ['смен', 'почт', 'измен'],
       'удаление лк': ['удал', 'личн', 'кабинет', 'лк', 'профил', 'аккаунт']}
detect_doc_fields = {'название проекта': ['заполня', 'назван', 'проект'],
                      'регион реализации проекта': ['регион', 'район', 'област', 'выбра', 'выбир'],
                      'опыт руководителя проекта': ['оп', 'руководител', 'опыт', 'писа', 'форм'],
                     'описание функционала руководителя': ['функционал', 'руководител', 'действ', 'возможн', 'обязан'],
                     'адрес регистрации руководителя проекта': ['зарегистрирова', 'прописа', 'числ', 'адрес',
                                                                'регистрац', 'руководител'],
                    'логотип': ['логотип', 'лого', 'аватарк', 'аватар', 'фотограф', 'фот'],
                     'видео-визитка (ссылка на ролик на любой видеохостинге)': ['визитк', 'видеохостинг',
                                                                                'ролик', 'визиток', 'виде',
                                                                                'видеоролик', 'содерж', 'содержа',
                                                                                'показа', 'демонтрир', 'отраж']}
dictionary_number = {
    'ноль': 0, 'ноля': 0, 'нулевой': 0, 'нулевого': 0,
    'один': 1, 'одного': 1, 'одна': 1, 'одной': 1, 'первый': 1, 'первого': 1,
    'два': 2, 'две': 2, 'двух': 2, 'второй': 2, 'вторая': 2, 'второго': 2,
    'три': 3, 'третий': 3, 'трех': 3, 'трёх': 3, 'третьей': 3, 'третьего': 3, 'четыре': 4,
    'четвертая': 4, 'четвертой': 4, 'четвертого': 4, 'четырех': 4, 'четырёх': 4, 'четвёрт': 4,
    'пять': 5, 'пятый': 5, 'пятая': 5, 'пятого': 5, 'пятой': 5, 'пяти': 5,
    'шесть': 6, 'шестой': 6, 'шести': 6, 'шестого': 6,
    'семь': 7, 'седьмой': 7, 'седьмого': 7, 'семи': 7,
    'восемь': 8, 'восьмой': 8, 'восьмого': 8, 'восьми': 8, 'восьмую': 8,
    'девять': 9, 'девятый': 9, 'девятой': 9, 'девяти': 9,
    'десять': 10, 'десятый': 10, 'десяти': 10, 'десятого': 10,
    'одиннадцать': 11, 'одиннадцатый': 11, 'одиннадцатой': 11, 'одиннадцатая': 11,
    'двенадцать': 12, 'двенадцатый': 12, 'двенадцатая': 12, 'двенадцатой': 12,
    'тринадцать': 13, 'тринадцатый': 13, 'тринадцатая': 13, 'тринадцатой': 13,
    'четырнадцать': 14, 'четырнадцатый': 14, 'четырнадцатой': 14, 'четырнадцатая': 14,
    'пятнадцать': 15, 'пятнадцатый': 15, 'пятнадцатой': 15, 'пятнадцатая': 15,
    'шестнадцать': 16, 'шестнадцатый': 16,'шестнадцатой': 16, 'шестнадцатая': 16,
    'семнадцать': 17, 'семнадцатый': 17, 'семнадцатой': 17, 'семнадцатая': 17,
    'восемнадцать': 18, 'восемнадцатый': 18, 'восемнадцатой': 18, 'восемнадцатая': 18,
    'девятнадцать': 19, 'девятнадцатый': 19, 'девятнадцатой': 19, 'девятнадцатая': 19,
    'двадцать': 20, 'двадцатый': 20, 'двадцатой': 20, 'двадцатая': 20,
    'тридцать': 30, 'тридцатый': 30, 'тридцатой': 30, 'тридцатая': 30,
    'сорок': 40, 'сороковой': 40, 'сороковая': 40, 'сорокового': 40,
    'пятьдесят': 50, 'пятидесятый': 50, 'пятидесятого': 50, 'пятидесятая': 50, 'пятидесятой': 50,
    'шестьдесят': 60, 'шестидесятый': 60, 'шестидесятая': 60, 'шестидесятой': 60, 'шестидесятого': 60,
    'семьдесят': 70, 'семидесятый': 70, 'семидесятого': 70, 'семидесятая': 70, 'семидесятой': 70,
    'восемьдесят': 80, 'восьмидесятый': 80, 'восьмидесятого': 80, 'восьмидесятая': 80, 'восьмидесятой': 80,
    'девяносто': 90, 'девяностый': 90, 'девяностого': 90, 'девяностая': 90, 'девяностой': 90,
    'сто': 100, 'сотый': 0, 'сотого': 0, 'сотая': 0, 'сотой': 0,
    'двести': 200, 'двухсотый': 200, 'двухсотая': 200, 'двухсотой': 200, 'двухсотого': 200,
    'триста': 300, 'трехсотый': 300, 'трехсотая': 300, 'трехсотого': 300, 'трехсотой': 300,
    'четыреста': 400, 'четырехсотый': 400, 'четырехсотого': 400, 'четырехсотая': 400, 'четырехсотой': 400,
    'пятьсот': 500, 'пятисотый': 500, 'пятисотого': 500, 'пятисотая': 500, 'пятисотой': 500,
    'шестьсот': 600, 'шестисотый': 600, 'шестисотого': 600, 'шестисотая': 600, 'шестисотой': 600,
    'семьсот': 700, 'семисотый': 700, 'семисотого': 700, 'семисотая': 700, 'семисотой': 700,
    'восемьсот': 800, 'восьмисотый': 800, 'восьмисотого': 800, 'восьмисотая': 800, 'восьмисотой': 800,
    'девятьсот': 900, 'девятисотый': 900, 'девятисотого': 900, 'девятисотая': 900, 'девятисотой': 900,
    'тысяча': 1000, 'тысячи': 1000,  'тысячного': 1000, 'тысячной': 1000,
    'тысячный': 1000, 'тысяч': 1000,
    'миллион': 1000000, 'миллиона': 10000000,
}
decimal_words = ['ноль', 'один', 'два', 'три', 'четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять']
ending = ['ый', 'ий', 'ое', 'ой', 'ая', 'ые', 'ого', 'ых', 'ому', 'ым', 'ую', 'ыми', 'ом']

def number_formation(number_words):
    '''Форматирование чисел'''
    numbers = []
    for number_word in number_words:
        numbers.append(dictionary_number[number_word])
    if len(numbers) == 4:
        return (numbers[0] * numbers[1]) + numbers[2] + numbers[3]
    elif len(numbers) == 3:
        return numbers[0] * numbers[1] + numbers[2]
    elif len(numbers) == 2:
        if 100 in numbers:
            return numbers[0] * numbers[1]
        else:
            return numbers[0] + numbers[1]
    else:
        return numbers[0]

def get_decimal_sum(decimal_digit_words):
    decimal_number_str = []
    for dec_word in decimal_digit_words:
        if(dec_word not in decimal_words):
            return 0
        else:
            decimal_number_str.append(dictionary_number[dec_word])
    final_decimal_string = '0.' + ''.join(map(str, decimal_number_str))
    return float(final_decimal_string)

def word_to_num(number_sentence):
    '''Конвертирование из слов в числа'''
    if type(number_sentence) is not str:
        raise ValueError("Тип данных не соответствует строке")

    number_sentence = number_sentence.replace('-', ' ')
    number_sentence = number_sentence.lower()

    if (number_sentence.isdigit()):
        return int(number_sentence)

    split_words = number_sentence.strip().split()

    clean_numbers = []
    clean_decimal_numbers = []
    index = []
    return_str = ''

    for word in range(len(split_words)):
        if split_words[word] in dictionary_number:
            clean_numbers.append(split_words[word])
            index.append(word)

    #Обработка ошибок для миллиона, миллиарда
    if clean_numbers.count('тысяча') > 1 or clean_numbers.count('миллион') > 1\
            or clean_numbers.count('тысячи') > 1:
        raise ValueError("Неверное слово")

    #отделение десятичной части
    if clean_numbers.count('point') == 1:
        clean_decimal_numbers = clean_numbers[clean_numbers.index('point')+1:]
        clean_numbers = clean_numbers[:clean_numbers.index('point')]

    billion_index = clean_numbers.index('billion') if 'billion' in clean_numbers else -1
    million_index = clean_numbers.index('миллион') if 'миллион' in clean_numbers else -1
    thousand_index = clean_numbers.index('тысячи') if 'тысячи' in clean_numbers else -1

    if (thousand_index > -1 and (thousand_index < million_index or thousand_index < billion_index)) or \
            (million_index > -1 and million_index < billion_index):
        raise ValueError("-")

    total_sum = []

    if len(clean_numbers) > 0:
        # hack for now, better way TODO
        if len(clean_numbers) == 1:
                #total_sum += dictionary_number[clean_numbers[0]]
                total_sum.append(dictionary_number[clean_numbers[0]])
                #print(total_sum)

        else:
            if len(clean_numbers) == 2:
                for i in range(len(clean_numbers)):
                    total_sum.append(dictionary_number[clean_numbers[i]])
            if billion_index > -1:
                billion_multiplier = number_formation(clean_numbers[0:billion_index])
                total_sum.append(dictionary_number[clean_numbers[0]])

            if million_index > -1:
                if billion_index > -1:
                    million_multiplier = number_formation(clean_numbers[billion_index+1:million_index])
                else:
                    million_multiplier = number_formation(clean_numbers[0:million_index])
                total_sum.append(million_multiplier * 1000000)


            if thousand_index > -1:
                if million_index > -1:
                    thousand_multiplier = number_formation(clean_numbers[million_index+1:thousand_index])
                elif billion_index > -1 and million_index == -1:
                    thousand_multiplier = number_formation(clean_numbers[billion_index+1:thousand_index])
                else:
                    thousand_multiplier = number_formation(clean_numbers[0:thousand_index])
                total_sum.append(million_multiplier * 1000000)

            if thousand_index > -1 and thousand_index != len(clean_numbers)-1:
                hundreds = number_formation(clean_numbers[thousand_index+1:])
            elif million_index > -1 and million_index != len(clean_numbers)-1:
                hundreds = number_formation(clean_numbers[million_index+1:])
            elif billion_index > -1 and billion_index != len(clean_numbers)-1:
                hundreds = number_formation(clean_numbers[billion_index+1:])
            elif thousand_index == -1 and million_index == -1 and billion_index == -1:
                hundreds = number_formation(clean_numbers)
            else:
                hundreds = 0
            total_sum.append(hundreds)

    if len(clean_decimal_numbers) > 0:
        decimal_sum = get_decimal_sum(clean_decimal_numbers)
        total_sum.append(decimal_sum)

    if len(index) == 0:
        return_str = " ".join(str(x) for x in split_words)

    elif len(index) == 1:
        a = str(index[0])
        b = int(a)
        return_str = " ".join(str(x) for x in split_words[:b]) + ' ' + str(total_sum[0]) + ' ' \
                 + " ".join(str(x) for x in split_words[b+1:])

    else:
        if len(index) == 2:
            a = str(index[0])
            b = str(index[1])
            c = int(a)
            d = int(b)
            return_str = " ".join(str(x) for x in split_words[:c]) + ' ' + str(total_sum[0]) + ' ' \
                         + " ".join(str(x) for x in split_words[c + 1:d]) + ' ' + str(total_sum[1]) + ' ' \
                            + " ".join(str(x) for x in split_words[d+1:])

    return return_str

def pars_endings(texts):
    '''Парсинг окончаний для числительных'''
    return_texts = []
    for string in texts:
        split_string = string.strip().split()
        for index in range(len(split_string)):
            s_word = split_string[split_string.index(split_string[index])]
            if not split_string[index].isalpha():
                word = re.sub(r'[а-я]+\s?', '', split_string[index]).strip()
                s_word = word
            split_string[index] = s_word
        return_string = ' '.join(split_string)
        return_texts.append(return_string)

    return return_texts

def parse(texts):
    '''Замена числительных, написанных словами, на цифры'''
    new_text = []
    for i in texts:
        new_text.append(word_to_num(i))
    new_text = pars_endings(new_text)
    return new_text

def get_text(url, encoding='utf-8', to_lower=True):
    url = str(url)
    if url.startswith('http'):
        r = requests.get(url)
        if not r.ok:
            r.raise_for_status()
        return r.text.lower() if to_lower else r.text
    elif os.path.exists(url):
        with open(url, encoding=encoding) as f:
            return f.read().lower() if to_lower else f.read()
    else:
        raise Exception('parameter [url] can be either URL or a filename')

def stopwords_stem(text):
    '''Функция очистки текста от стоп-слов и стемминг'''
    #url_stopwords_ru = "https://raw.githubusercontent.com/stopwords-iso/stopwords-ru/master/stopwords-ru.txt"
    stopwords_ru = get_text('stopwords.txt').splitlines()
    text = " ".join([word for word in text.split() if word not in (stopwords_ru)])
    stemmer = SnowballStemmer("russian")
    text_processed = [stemmer.stem(word) for word in text.split()]
    print(text_processed)
    return text_processed

def show_field_info(field):
    '''Функция, отвечающая за нахождение информации о нужном поле, где
    dict_field - словарь, где key - название поля, value - информация по заполнению данного поля'''
    with open('instructions2fields.txt') as file:  # Читаем файл
        lines = file.read().splitlines()  # read().splitlines() - чтобы небыло пустых строк
    info_dict = {}
    for line in lines:
        key, value = line.split(':: ')  #разделение по двойному двоеточию (до двойного дветочия ключ, после - значение)
        info_dict.update({key: value})
    for key in info_dict:
        if key == field:
            return info_dict[key]

def choose_action(words):
    '''Функция, определяющая к какому классу относится вопрос, где
    words - массив слов'''
    porog_count = 1
    result = ''
    for key in action_words:
        count = 0
        for word in words:
            if word in action_words[key]:
                count += 1
                words.remove(word)
        if count >= porog_count:
            result = key
    if result == '':
        result = 'faq'
    return result, words

def answer_faq(problem):
    '''Функция, отвечающая за ответ на самые популярные вопросы, где
    dict_field - словарь, где key - название поля, value - информация по заполнению данного поля'''
    with open('faq.txt') as file:  # Читаем файл
        lines = file.read().splitlines()  # read().splitlines() - чтобы небыло пустых строк
    problem_dict = {}
    for line in lines:
        key, value = line.split(':: ')  #разделение по двойному двоеточию (до двойного дветочия ключ, после - значение)
        problem_dict.update({key: value})
    for key in problem_dict:
        if key == problem:
            return problem_dict[key]

def find_max_elem(d):
    res = heapq.nlargest(3, d.items(), key=lambda i: i[1])
    return res

def func(case, words):
    '''Функция, отвечающая за подбор ответа, где
    case - класс вопроса,
    words - массив слов'''
    mas_answer = []
    dict_answer = {}
    if len(words) >= 4:
        porog_count = 2
    else:
        porog_count = 1
    if case == 'навигация':
        dict_match = {}
        for key in words_to_section:
            count_navig = 0
            for word in words:
                if word in words_to_section[key]:
                    count_navig += 1
            dict_match[key] = count_navig
        if len(dict_match) != 0:
            res = find_max_elem(dict_match)
            for (i, j) in res:
                mas_answer.append([i, url_to_section[i]])
            return mas_answer
        else:
            return 'Я не смогла найти ответ на Ваш вопрос. Попробуйте перефразировать его или ' \
                   'отправьте его в тех.поддержку по адресу support@myrosmol.ru'
    elif case == 'заполнение':
        dict_match = {}
        for key in detect_doc_fields:
            count_field = 0
            for word in words:
                if word in detect_doc_fields[key]:
                    count_field += 1
            dict_match[key] = count_field
        if len(dict_match) != 0:
            res = find_max_elem(dict_match)
            for (i, j) in res:
                return show_field_info(i)
        else:
            return 'Я не смогла найти ответ на Ваш вопрос. Попробуйте перефразировать его или ' \
                   'отправьте его в тех.поддержку по адресу support@myrosmol.ru'
    elif case == 'faq':
        dict_match = {}
        for key in detect_faq:
            count_faq = 0
            for word in words:
                if word in detect_faq[key]:
                    count_faq += 1
            dict_match[key] = count_faq
        if len(dict_match) != 0:
            res = find_max_elem(dict_match)
            for (i, j) in res:
                return answer_faq(i)
        else:
            return 'Я не смогла найти ответ на Ваш вопрос. Попробуйте перефразировать его или ' \
               'отправьте его в тех.поддержку по адресу support@myrosmol.ru'

def web_bot(text):
    '''Главный алгоритм программы, получающий данные из API и передающий их туда,
    text - полученный из API текст'''
    text = text.lower()
    res = re.sub('[\W_]+', ' ', text)
    words = stopwords_stem(res) #удаление стоп-слов
    action, words = choose_action(words) #определение категории
    answer = func(action, words)
    #print(answer)
    return answer





#web_bot('Как снять видеоролик')

