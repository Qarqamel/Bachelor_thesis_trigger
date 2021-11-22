GENERATOR_PERIOD
Function: Generuje PWM o zadanym okresie w przedziale 1ms-262ms.

Zadawanie: UART, liczba całkowita dodatnia + '/n'

z jaką rozdzielczościa czyli w jakich jednostkach przychodzi z uarta? - W milisekundach
Input-Output:

Uno: 10-PB.2
Leonardo: 10-PB.6
Uart boderate: 9600

Implementacja

timer1 (16 bit,non inverting fast PWM, prescaler 64)
generuje przebieg prostkątny (PWM 50%) Okres przebiegu wpisywany z UART-a do rejestru Output compare timera
UWAGI:

zamiast zwracania okresu zwracać "ok\n"
GENERATOR_PERIOD_VARIABLE
Function: Generuje PWM o okresie w zakresie 1ms-262ms zmieniającym się co jeden okres.

Zadawanie okresów:

lista okresów w ms w tabeli okresów ("T_ms_tbl") [czy napewno w ms? - tak]
przemiatana bez przrwy, cyklicznie
Output:

Uno: 10-PB.2
Leonardo: 10-PB.6
Auxiliary connections:

Uno: 2-PD.2 - 10-PB.2
Leonardo: 2-PD.1 - 10-PB.6
Implementation

timer1 (16 bit,non inverting fast PWM, prescaler 64)
okres PWM zmienieny na kolejną wartość z tabeli okresów na każdym zboczu rosnącym sygnału wyjściowego
GENERATOR_PULSE
Function: Generuje impulsy.

Zadawanie wartości(czas, okres) impulsów: -lista impulsów w tabeli structów("sPulses"), w formacie {start, width}, gdzie: start - czas od resetu do początku impulsu, width - długość impulsu -po ostatnim impulsie progrtam zawiesza działanie

Output:

Uno: 5-PD.5
Leonardo: 5-PC.6
Implementacja: -Przerabia tablicę struct'ów na tablicę int'ów, następnie w funkcji wywoływanej cyklicznie(co 1 ms) nalicza counter i zmienia stan pinu wyjściowego na przeciwny, gdy counter jest równy jednej z wartości w tablicy

METER_EDGES_4us
Funkcjonalność:

rejestruje czas wystpienia zbocza na jednym z wejść uC z rozdzielczością us
możliwy jiter +/-4us, okres przepełnienie licznika us: 4294967295
wysyła zarejestrowany czas przez uarta
Ograniczenie: następny impuls może przyjśc dopiero po podesłaniu przez uarta czasu rejestracji poprzedniego

Input:

Uno: 2-PD.2
Leonardo: 2-PD.1
Uart boderate: 115200

Implementacja:

Na rosnących zboczach na pinie wejściowym, rejestruje czas, a następnie wysyła pomiar przez UART.
Rejestracja czasu funkcją "micros" na przerwaniu od pinu
METER_EDGES_BUFFERED_4us
Baseline: "#METER_EDGES_4us"

Motywacja: usunięcie ogranicznenia odległości zboczy w "#METER"

Funkcjonalność:

W odróżnieniu od "#METER" zarejestrowane czasy wystąpienia zbocza zapisywane sa do tablicy
Liczba rejestracji definiowana w kodzie (SAMPLE_NR)
Rejestracja rozpoczyna się po odebraniu dowolnego łąńcucha z UART-a
Po zakonczeniu rejestracji następuje odesłanie zarejestrowanych czasów, każda liczba zakonczona znakiem terminatora
skąd aplikacja odbierająca ma wiedzieć na ile liczb ma czekać ? - nie wie
Input:

Uno: 2/PD.2
Leonardo: 2/PD.1
Uart boderate: 115200

#METER_EDGES_BUFFERED_0.5uS

Baseline: "#METER_EDGES_BUFFERED_4us"

Motywacja: usunięcia jitera występującego w Baseline

Funkcjonalność: jak w Baseline ale:

rozdzielczosć: 1/2 us bez jittera
przepełnienie licznika / maksymalny odstęp zboczy : 32767us
Input:

Uno: 8\PB.0
Leonardo: 4\PD.4
Implementacja:

rejestracja zboczy za pomocą funkcji input capture timer1 (16bit)
konfiguracja timear: rybie CTC z preskalerem ustawionym na 8
METER_PERIOD_BUFFERED_0.5uS
Baseline: #METER_EDGES_BUFFERED_0.5uS

Motywacja: pomiar okresu zamaiast czasu wystąpienia zboczy

Liczba rejestrowanych okresów:

Uno: ? ~500
Leonardo: ? ~500
Mega: 2900
Input:

Uno: 8\PB.0
Leonardo: 4\PD.4
Mega: 49\PL.0
Implementacja: jak w Baseline oprócz wersja dla MEGA (co to "defaultowym-mode" ? - Normal mode; Czy są dwie wersje kodu ? - w roznych komitach na tym samym branchu)

REGENERATOR
Funkcjonalność:

generuje na wyjściu przebieg prostokątny o okresie proporcjonalnym do okresu przebiegu na wejsciu
współczynnik proporcjonalności ustalany przez określenie porządanego okresu na wyjściu (przy aktualnym okresie na wejściu)
określenie porządanego przez UART, jaka jednostka ? - mikrosekundy
jaki boderate uarta ? - 9600
Nie rozumiem "Okres: 0-4095us" ? - najdluzszy okres jaki możemy wygenerować to 4095us
I\O:

Uno:
I: 2\PD.2
O: 10\PB.2
Leonardo:
I: 2\PD.1
O: 10\PB.6
Implementacja

pomiar okresu: przrwania na zbocza i funkcja "micros" (analogicznie jak w #METER)
generowanie przebiegu: timer1 (16-bit), trybi non inverting fast PWM, prescalerem 1 (podobnie jak w #GENERATOR)
RECORDER
Funkcjonalność:

rejestrowanie stanu na pinie x w momencie wystąpienia zbocza na pinie y i wysyłanie stanu przez UART-a
częstotliwośći rejestracji: zależy od częstotliwości sygnału na pinie y
jaki boderate uarta 115200
jaki format danych wysyłanych prze uarta ? - '0' lub '1'
Inputs:

Uno:
zbocze: 2\PD.2
stan: 3\PD.3
Leonardo:
zbocze: 2\PD.1
stan: 3\PD.0
Implementacja: rejestracja stanu pinu x na przerwaniu od zbocza na pinie y

SELECTOR
Funkcjonalność:
gromadzi timestampy odebrane po uarcie
zlicza zbocza na wejściu
gdy wartość licznika zboczy jest większa niż któregoś z timestampów
generuje impuls na pinie
usuwa timestamp
jaki boderate uarta 9600
jaki format danych wysyłanych prze uarta ? - "tstamp_" + wartosc timestampa + "\n"
(w wersji do testbencha nie ma Uarta, zamiast tego program generuje impulsy)

Inputs:

Uno: 2\PD.2
Leonardo: 2\PD.1
Implementacja:

Zbocza rosnące generują przerwania, w których inkrementowany jest licznik zboczy .
W pętli głównej równolegle nastęopuje
odbieranie timestampów,
generowanie impulsów i usuwanie timestampów [i zwraca informację przez UART. - dyskusja]
========================================== Gdzie program do PC symulujący obróbkę obrazu (odbierjący sample z #RECORDER i wysyałający timestampy do #SELECTOR) ? - branch SelektorTB/COM_driver
