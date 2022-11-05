<h1 align='center'>Aliexpress parser</h1>

Данная программа парсит c [aliexpress.com](https://www.aliexpress.com) названия, стартовые и скидочные цены, ссылки товаров и структурирует собранное в csv-файл.

## Библиотеки:

- [Selenium](https://pypi.org/project/selenium/)
- [Beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

## Настройка:

1. Создать и активировать виртуальное окружение.

Windows
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Linux/MacOS
```
python3 -m venv venv
source venv/bin/activate
```

2. Установить нужные модули с файла `requirements.txt`.
```
pip install -r requirements.txt
```

3. Установить в директорию cхожую версию [chromedriver](https://chromedriver.chromium.org/downloads) с вашим браузером.
 
4. Вставить путь до chromedriver.exe в driver_path класса Parser.
```
if __name__ == '__main__':
    parser = Parser(
        driver_path=r'chromedriver.exe',
        site_url='https://aliexpress.ru/category/202001195/cellphones.html?brandValueIds=200012332&g=n&page=1&spm='
    )
    parser.main()
```
<h1></h1>