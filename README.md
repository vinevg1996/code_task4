# code_task4
Проект содержит следующие классы

* CodeBuilder - класс, генерирующий код с заданными параметрами

* Encoder - класс, осуществляющий кодирование сообщения

* Decoder - класс, осуществляющий декодирование сообщения

* Help - класс со вспомогательными функциями

* Combinatorics - класс со вспомогательными функциями комбинаторики

Проект запускается из файла task_4.py

Проект допускает 3 режима:

* Режим 1 или режим генерации кода

* Режим 2 или режим кодирования

* Режим 3 или режим декодирования

## Режим 1

Чтобы сгенерировать линейный код запустите:

  python3 task_4.py mode=1 n p out_inf.txt

где:

* n - размер блока

* p - вероятность ошибки двоичного симметричного канала

* out_inf.txt - файл, куда записывается необходимая информация для кодера и декодера

Программа выводит значения:

* k - размер сообщения (получается из неравенства Варшамова-Гильберта)

* d - кодовое расстояние (получается из неравенства Варшамова-Гильберта и границы Синглтона)

* t - число ошибок, исправляемых кодом

* dictionary_for_decoder - словарь для декодирования сообщений с границей числа ошибок t

* prob for decode error - вероятность ошибки декодирования

### Алгоритм работы

1 Строится проверочная матрица H (для простоты реализации строится H транспонированная):

1.1 Сначала строится единичная подматрица размера k.

1.2 Затем она достраивается так, чтобы каждые d - 1 столбцов были линейно-независимы

1.3 Последним добавляется строка такая, чтобы она образовывала с первыми d - 1 строками линейно-зависимую систему

1.4 Затем транспонируется матрица H

2 По матрице H строится кодовая матрица G

3 Строится матрица, реализующая стандартное распоожеие

4 Вычисляются синдромы лидеров смежных классов

5 Код записывается в выходной файл в следующем формате:

5.1 вероятность неверного декодирования

5.2 параметры [n, k, r, d, t]

5.3 список [синдром, лидер смежного класса]

5.4 матрица G

5.5 матрица H

### Пример работы
Для примера с n = 8 и p = 0.1 код записан в файле out_info_n_8_p_0_1.txt. Запустите:

python3 task_4.py mode=1 8 0.1 out_info_n_8_p_0_1.txt

## Режим 2

Чтобы закодировать кодовое слово m с вектором ошибок e запустите:

  python3 task_4.py mode=2 out_info.txt m e

Если вектор ошибок e отсутствует, то он генерируется случайно.

### Пример работы

Для примера с n = 8 и p = 0.1, код для которого записан в файле out_info_n_8_p_0_1.txt, чтобы закодировать сообщение с вектором ошибок 0001 00000001 запустите:

python3 task_4.py mode=2 out_info_n_8_p_0_1.txt 0001 00000001

Тогда

* code_word =  [0, 0, 0, 1, 1, 1, 0, 0]

* noise_word =  [0, 0, 0, 1, 1, 1, 0, 1]

## Режим 3

Чтобы декодировать кодовое слово y запустите:

  python3 task_4.py mode=3 out_inf.txt y

### Пример работы

Для примера с n = 8 и p = 0.1, код для которого записан в файле out_info_n_8_p_0_1.txt, чтобы декодировать сообщение с вектором ошибок 00011001 запустите:

python3 task_4.py mode=3 out_inf.txt 00011001