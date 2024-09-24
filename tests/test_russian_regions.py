from region_finder_ru import RegionFinder


class RegionFinderForTests(RegionFinder):

    def define_regions(self):
        """Перезаписываем метод, для тестов
         внутренних методов не играет роли."""
        return -1


class TestRegion:
    def test_find_postcodes(self):
        """Последовательность из шести цифр
         - почтовый индекс."""

        address = ('125212 Ленинградское шоссе, д. 155 634009,'
                   ' пр-кт Ленина, Томск, Томская область,')

        assert (RegionFinderForTests(address)
                ._find_postcodes() == ['125212',
                                       '634009']
                )

    def test_find_postcodes_not_geographical_cords(self):
        """Географические координаты
         не определяются как почтовый индекс."""

        address = ('57.323161, 38.505162, Совхозная'
                   ' улица, 10А, посёлок городского типа')

        assert not RegionFinderForTests(address)._find_postcodes()

    def test_find_postcodes_five_symb_postcode(self):
        """Последовательность из 5 цифр
        не определяется как почтовый индекс."""

        address = ('Новые Лапсары, городской округ Чебоксары,'
                   ' Чувашская Республика, 42803')

        assert not RegionFinderForTests(address)._find_postcodes()

    def test_find_postcodes_first_3_symb(self):
        """Последовательность из шести цифр
         - почтовый индекс и возврат списка первых трех символов каждого."""

        address = ('125212 Ленинградское шоссе, д. 155 634009,'
                   ' пр-кт Ленина, Томск, Томская область,')

        assert (RegionFinderForTests(address)
                ._find_first_3_postcodes() == ['125',
                                               '634']
                )

    def test_find_region_names_federal_cities(self):
        """Названия федеральных городов определяются корректно."""

        address = ('Загородное шоссе, 2с5, Москва, 117152,'
                   'Партизанская улица, 14, Санкт-Петербург, 195248,'
                   'переулок Шевкопляса, 9, Инкерман,'
                   'Балаклавский район, Севастополь, 299703')
        address2 = ('улица Фрунзе, 19, Новосибирск, 630091,'
                    'Московское шоссе, д. 14, г. Киров')

        assert (RegionFinderForTests(address)
                ._find_region_names() == ['москва',
                                          'санкт-петербург',
                                          'севастополь']
                )
        assert not RegionFinderForTests(address2)._find_region_names()

    def test_find_region_names_republics(self):
        """Названия республик определяются корректно."""

        address = ('Полевая улица, 26А, село Высокая Гора,'
                   'Респ. Татарстан, 422701'
                   'улица Карла Маркса, 270А, Ижевск, '
                   'Удмуртская Республика, Коммунистическая улица,'
                   '21А, Сыктывкар, Республика Коми, 167000,'
                   'улица Орджоникидзе, 47, Нальчик,'
                   'Кабардино-Балкарская Республика')

        assert (RegionFinderForTests(address)
                ._find_region_names() == ['татарстан',
                                          'удмуртская',
                                          'коми',
                                          'кабардино-балкарская']
                )

    def test_find_region_names_autonomous_regions(self):
        """Названия автономных округов определяются корректно."""

        address = ('Анадырь, Чукотский автономный округ, 689000,'
                   'улица имени В.И. Ленина, 12, Нарьян-Мар,'
                   'Ненецкий автономный округ, 166000,'
                   'улица Чубынина, 12, Салехард,'
                   'Ямало-Ненецкий автономный округ, 629008')

        assert (RegionFinderForTests(address)
                ._find_region_names() == ['чукотский',
                                          'ненецкий',
                                          'ямало-ненецкий']
                )

    def test_find_region_names_regions(self):
        """Названия областей определяются корректно."""

        address = ('Советская улица, 6, Ивановская область, Иваново, 153000,'
                   'проспект Ленина, 82, обл. Мурманская Мурманск, 183038,'
                   'Обл Архангельская, г. Архангельск')

        assert (RegionFinderForTests(address)
                ._find_region_names() == ['ивановская',
                                          'мурманская',
                                          'архангельская']
                )

    def test_find_region_names_regions_dative(self):
        """Названия регионов в родительном падеже
        определяются корректно."""

        address = ('Советская улица, 6, Ивановской области, Иваново, 153000,'
                   'г. Казань, республики Татарстан')

        assert (RegionFinderForTests(address)
                ._find_region_names() == ['ивановская',
                                          'татарстан']
                )

    def test_find_region_names_side_regions(self):
        """Названия краев определяются корректно."""

        address = ('улица Карла Маркса, 137А, Красноярск,'
                   ' край Красноярский 660017,'
                   'бобр Красноярский мокр. Краснодарский,'
                   ' кр. Ставропольский,'
                   'ул. ленина 15 Ставропольский край ул. ленина 15')

        assert (RegionFinderForTests(address)
                ._find_region_names() == ['красноярский',
                                          'ставропольский',
                                          'ставропольский']
                )

    def test_find_region_names_hard_cases(self):
        """Другие случаи-исключения
         обрабатываются ожидаемым поведением."""

        address = ('Театральный переулок, 10, Биробиджан,'
                   'Еврейская автономная область, 679016,'
                   'проспект Ленина, 30/1, Якутск, '
                   'Республика Саха (Якутия), 677011,'
                   'алтайский край приморский край край край,'
                   'проспект Мира, 4, Владикавказ,'
                   'Республика Северная Осетия — Алания')

        assert (RegionFinderForTests(address)
                ._find_region_names() == ['еврейская',
                                          'автономная',
                                          'саха',
                                          'алтайский',
                                          'приморский',
                                          'край',
                                          'край',
                                          'край',
                                          'северная осетия']
                )

    def test_find_city_names(self):
        """Последовательность кириллических символов,
        между которыми может быть символ "-" (не более двух раз),
        перед которыми стоит буква "г" с точкой или без
        или слово "город"."""

        address = ('г. Ижевск, ул. Ленина 10 г Людиново,'
                   'мозг. Хабаровск город Надежд ул. героев 11')

        assert (RegionFinderForTests(address)
                ._find_city_names() == ['ижевск',
                                        'людиново',
                                        'надежд']
                )

    def test_find_city_names_with_hyphen(self):
        """Названия городов, содержащих дефис."""

        address = ('г. Ростов-на-Дону, ул. красная 11,'
                   'г. Ростов-на-Дону-на-Дону, ул. черная 15,'
                   'г Комсомольск-на-Амуре, д11')

        assert (RegionFinderForTests(address)
                ._find_city_names() == ['ростов-на-дону',
                                        'ростов-на-дону',
                                        'комсомольск-на-амуре']
                )

    def test_find_city_names_with_double_part(self):
        """Названия городов, состоящих из двух слов."""

        address = ('г. Нижний Новгород, ул. Печорская,'
                   'г. Супер Рофлов, ул. Тестов,'
                   '125313 г Сергиев Посад')

        assert (RegionFinderForTests(address)
                ._find_city_names() == ['нижний новгород',
                                        'супер',
                                        'сергиев посад']
                )

    def test_find_district_names(self):
        """Последовательность кириллических символов
        перед словами район, р-он, р-н."""

        address = ('Свердловская обл. Кушвинский район,'
                   'Пермский край, Красновишерский р-он,'
                   'Кемеровский р-н')

        assert (RegionFinderForTests(address)
                ._find_district_names() == ['кушвинский',
                                            'красновишерский',
                                            'кемеровский']
                )

    def test_find_district_names_with_hyphen(self):
        """Названия районов, в которых встречается символ "-"."""

        address = 'Мариинско-Посадский район с. Вурнары'

        assert (RegionFinderForTests(address)
                ._find_district_names() == ['мариинско-посадский']
                )

    def test_find_settlement_names(self):
        """Последовательность кириллических символов
        после слов р.п., н.п., п., с., пгт., пгт."""

        address = ('с. Вурнары, р.п. рабочий, н.п. тестовый,'
                   ' п. рофловый, с. вперед, пгт. вперед,'
                   ' пгт опять, село вперед, поселок опять')

        assert (RegionFinderForTests(address)
                ._find_settlement_names() == ['вурнары',
                                              'рабочий',
                                              'тестовый',
                                              'рофловый',
                                              'вперед',
                                              'вперед',
                                              'опять',
                                              'вперед',
                                              'опять',
                                              ]
                )

    def test_find_settlement_names_wrong_names(self):
        """Проверка корректности определения границ
        слов при поиске посёлков."""

        address = ('стресс. встретился в адресе, '
                   'пп. Полупоселок,'
                   'селовой агрегат')

        assert not RegionFinderForTests(address)._find_settlement_names()
