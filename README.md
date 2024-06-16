# НТ Прогресс 
Биржа - это такой "сервис", куда можно отправить заявку (ордер) на покупку или продажу какого-либо актива. Получив заявку, биржа, применяя некую торговую логику, ищет встречную заявку для заключения сделки. Заявка в итоге может быть исполнена, отклонена или же ее можно отменить самому. При выставлении заявки можно ориентироваться на текущие цены данного актива (котировки) для более вероятного исполнения заявки.

### Установка
1. Клонировать репозиторий
```bash
git clone https://github.com/Ivanmatv/NT_Progress.git
```
2. Создание виртуального коуржения
```bash
python3 -m venv venv
```
3. Активация виртуального окружения
- для MacOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```
- для Windows
```bash
python -m venv venv
source venv/Scripts/activate
```
4. Обновление установщика pip и установка зависимостей
```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```
7. Запуск приложения 
```bash
fastapi dev app.py
```

## API документация
http://127.0.0.1:8000/swagger/  
http://127.0.0.1:8000/redoc/

## Технологии
- Python
- FastAPI
- Pydentic
- HTML
- CSS
