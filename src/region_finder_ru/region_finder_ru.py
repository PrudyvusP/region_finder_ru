import re
from abc import ABC, abstractmethod
from typing import List


class RegionFinder(ABC):
    """Класс RegionFinder используется для поиска в адресной
    строке признаков принадлежности к регионам Российской Федерации

    Атрибуты
    ----------
    address : str
        адресная строка

    Методы
    -------
    _find_postcodes():
        Ищет почтовые индексы РФ и возвращает их список.
    _find_region_names():
        Ищет упоминания регионов РФ и возвращает их список.
    _find_city_names():
        Ищет упоминания городов РФ и возвращает их список.
    _find_district_names():
        Ищет упоминания районов РФ и возвращает их список.
    _find_settlement_names():
        Ищет упоминания посёлков и сёл РФ и возвращает их список.
    define_regions():
        абстрактный метод, реализующий логику работу по поиску
        совпадений в справочниках.
    """

    _postcode_regex = re.compile(r'((?<![.:\d])\d{6}(?![:\d]))')

    # https://regex101.com/r/jO3iI9/1
    _region_name_regex = re.compile(
        r'\b(?:северная осетия|марий эл|[а-яё]{2,}-?[а-яё]{2,})'
        r'(?= (?:автономн[аы][яй] о(?:бласть|круг|бл)'
        r'|область|обл\.?'
        r'|(?:народная )*республик[иа]'
        r'|респ\.?'
        r'|край'
        r'|кр\.?'
        r')\b)'
        r'|\b(?:москва|севастополь|санкт-петербург)\b'
        r'|(?:(?<=область )'
        r'|(?<=обл\. )'
        r'|(?<=\bобл )'
        r'|(?<=республик[аи] )'
        r'|(?<=\bресп\. )'
        r'|(?<=\bресп )'
        r'|(?<=край )'
        r'|(?<=\bкр\. ))'
        r'(?:северная осетия|марий эл|\b[а-яё]{2,}-?[а-яё]{2,})')

    # https://regex101.com/r/FO68Xo/1
    _city_name_regex = re.compile(
        r'\b(?:г\.?|город) ?'
        r'('
        r'(?:'
        r'(?:'
        r'стар[аы][йя]'
        r'|нов[аы][йя]'
        r'|нижн[ия][йея]'
        r'|красный'
        r'|верхн[ия][йея]'
        r'|велики[ей]'
        r'|белая'
        r'|советская'
        r'|сергиев'
        r'|полярные'
        r'|петров'
        r'|павловский'
        r'|набережные'
        r'|минеральные'
        r'|мариинский'
        r'|малая'
        r'|лодейное'
        r'|западная'
        r'|дагестанские'
        r'|горячий'
        r'|гаврилов'
        r'|вятские'
        r'|вышний|'
        r'большой'
        r')'
        r' )*'
        r'\b[а-яё]+-?[а-яё]+-?[а-яё]+)'
    )
    _district_regex = re.compile(
        r'\b\w+-?\w+\b(?= \bрайон\b| \bр-о?н\b)'
    )

    # https://regex101.com/r/wjUGj9/1
    _settlement_regex = re.compile(
        r'(?:(?<=\bр\.п\. )'
        r'|(?<=\bн\.п\. )'
        r'|(?<=\bп\. )'
        r'|(?<=\bс\. )'
        r'|(?<=\bпгт\. )'
        r'|(?<=\bпгт )'
        r'|(?<=\bсело )'
        r'|(?<=\bпоселок ))'
        r'(\b[а-яё]+-?[а-яё]+)'
    )

    _region_name_sub_regex = re.compile(r'\b(\w+)ой\b (\bобласт)[ьи]\b')
    _edge_name_sub_regex = re.compile(r'\b(\w+)ого\b (\bкра)[йя]\b')

    def __init__(self, address: str) -> None:
        """Конструктор класса."""

        if not address:
            raise ValueError('Адрес не должен быть пустым')

        self.address = self._beatify_address(address)

    def _beatify_address(self, address: str) -> str:
        """Удаляет лишние символы из адресной строки."""

        address = re.sub(r' {2,}', ' ', address.lower())
        return re.sub(u'\xa0', ' ', address)

    def _find_postcodes(self) -> List[str]:
        """Возвращает список почтовых индексов
         - последовательности из 6 цифр."""

        return self._postcode_regex.findall(self.address)

    def _find_region_names(self) -> List[str]:
        """Возвращает список названий регионов."""

        address = self._region_name_sub_regex.sub(r'\1ая \2ь', self.address)
        address = self._edge_name_sub_regex.sub(r'\1ий \2й', address)
        return self._region_name_regex.findall(address)

    def _find_city_names(self) -> List[str]:
        """Возвращает список названий городов
        по характерным признакам перед их названиями
        (буква г с точкой или без)."""

        return self._city_name_regex.findall(self.address)

    def _find_district_names(self) -> List[str]:
        """Возвращает список названий районов."""

        return self._district_regex.findall(self.address)

    def _find_settlement_names(self) -> List[str]:
        """Возвращает список названий поселков
         городского типа, поселков и сел."""

        return self._settlement_regex.findall(self.address)

    @abstractmethod
    def define_regions(self):
        """Метод должен быть перезаписан с учетом
        выбранной стратегии хранения и обработки справочной информации.
        Информацию о почтовых индексах и регионах РФ можно хранить
        в БД, или в хеш-таблицах, или в файлах."""

        pass
