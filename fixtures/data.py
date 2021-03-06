#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Роли полезователей
user_roles = (
               (u'superadmin'), # администратор myconomy
               (u'storeadmin'), # администратор магазина
               (u'customer'),   # покупатель
             )

# Cправочник пользовательских опций
user_options = (
                 (1, u'Определять местоположение'),
                 (2, u'Публиковать предложения анонимно'),
                 (3, u'Публиковать цены анонимно'),
                 (4, u'Публиковать магазины анонимно'),
               )

# Cправочник опций для списков
list_options = (
                 (1, u'Радиус поиска'),
                 (2, u'Приоритет поиска'),
                 (3, u'Метод сортировки'),
               )

# Типы транзакций
transactions_types = (
                       (0, u'Unknown'),
                       (1, u'Приход'),
                       (2, u'Расход')
                     )

# Cостояния счета
account_states = (
                   (0, u'Unknown'),
                   (1, u'Активный'),
                   (2, u'Блокирован'),
                   (3, u'Закрыт'),
)

# Cостояния транзакций
transaction_states = (
                       (0, u'Unknown'),
                       (1, u'Ok'),
                       (2, u'Удалена'),
                       (3, u'Сторнирована'),
)

# Типы единиц товаров
measures = (
             (0, u'Unknown'),
             (1, u'1шт'),
             (2, u'1упк'),
             (3, u'1кг'),
             (4, u'100гр'),
             (5, u'1л'),
             (6, u'1пучок'),
           )

# единицы измерения веса
weight_types = (
                 (0, u'Unknown', u'Unknown'),
                 (1, u'грамм', u'гр'),
                 (2, u'килограмм', u'кг'),
               )

# единицы измерения объема
volume_types = (
                 (0, u'Unknown', u'Unknown'),
                 (1, u'миллилитр', u'мл'),
                 (2, u'литр', u'л'),
               )

# Cостояния предложения
offer_states = (
                 (0, u'Unknown'),
                 (1, u'Ok'),
                 (2, u'Удалено'),
               )

# Cостояния магазина
store_states = (
                 (0, u'Unknown'),
                 (1, u'Ok'),
                 (2, u'Удалено'),
               )

# Состояния задания
task_states = (
                (0, u'Unknown'),
                (1, u'Инициализирована'),
                (2, u'Начата'),
                (3, u'Выполняется'),
                (4, u'Завершена с ошибками'),
                (5, u'Завершена с успехом'),
              )

# Cостояния элемента задания
taskitem_states = (
                    (0, u'Unknown'),
                    (1, u'Ok'),
                    (2, u'Ошибка'),
)

# Типы заданий
task_types = (
               (0, u'Unknown'),
               (1, u'Загрузка предложений'),
               (2, u'Загрузка магазинов'),
)