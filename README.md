# region_finder_ru

region_finder_ru - это набор регулярных выражений для поиска признаков регионов РФ в адресных строках.
Основной метод _define_regions_ класса _RegionFinder_ необходимо определить пользователю самостоятельно.

## Установка

Предполагается, что в будущем пакет можно будет установить из [PyPI](https://pypi.org/) командой:

```bash
python -m pip install region_finder_ru
```

В настоящее время данный пакет устанавливается локально.

## Пример использования

Пример переопределения метода _define_regions_ с помощью СУБД представлен [тут](https://github.com/PrudyvusP/region_finder).

## Тесты

Для тестирования используется [pytest](https://docs.pytest.org) (coverage 98%).