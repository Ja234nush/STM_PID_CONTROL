import serial
import matplotlib.pyplot as plt
from drawnow import drawnow
import time
from datetime import datetime

# Inicjalizacja portu szeregowego
ser = serial.Serial('COM7', baudrate=115200, timeout=1)
ser.write(b'30')
time.sleep(0.5)

# Inicjalizacja danych
temperature_data = []

# Inicjalizacja pliku do zapisu danych
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"temperature_data_{timestamp}.txt"

# Funkcja do aktualizacji wykresu
def update_plot():
    plt.plot(temperature_data, 'go', label='Temperature')
    plt.title('Wartosc temperatury w czasie')
    plt.xlabel('Czas [s]')
    plt.ylabel('Temperatura [°C]')
    plt.legend()
    plt.grid()

# Główna pętla programu
while True:
    try:
        # Odczyt danych z portu szeregowego
        line = ser.readline().decode('utf-8').strip()

        # Pominięcie pustej linii
        if not line:
            continue

        # Konwersja na float i dodanie do listy danych
        temperature = float(line)
        temperature_data.append(temperature)

        # Rysowanie wykresu w czasie rzeczywistym
        drawnow(update_plot)

        # Zapis danych do pliku co 10 próbek (opcjonalne usprawnienie)
        if len(temperature_data) % 10 == 0:
            with open(filename, 'a') as file:
                for i, temp in enumerate(temperature_data):
                    file.write(f"{i+1}\t{temp}\n")
                #temperature_data = []  # Opcjonalnie wyczyść zapisane dane, aby zmniejszyć rozmiar listy

    except KeyboardInterrupt:
        # Zatrzymaj pętlę w przypadku przerwania klawiszem
        print("Program zatrzymany.")

        # Dodaj zapis ostatnich danych do pliku przed zakończeniem programu
        with open(filename, 'a') as file:
            for i, temp in enumerate(temperature_data):
                file.write(f"{i+1}\t{temp}\n")
        break
    except ValueError:
        # Obsługa błędu konwersji na float (jeśli otrzymamy niepoprawną wartość)
        print("Error: Could not convert to float:", line)

# Zamknięcie połączenia z portem szeregowym
ser.close()
