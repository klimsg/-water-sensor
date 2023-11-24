import serial
import datetime
import os
import csv
import pystray
import PIL.Image
import tkinter as tk

Exit = False
v=0

# Участок с созданием папки
if not os.path.isdir("Показания"):
     os.mkdir("Показания")

#Иконка в трее картинка
imagetree = PIL.Image.open('Logo.png')

# Участок кода Окно
def window():
    def testimony():
        global V
        volume.config(text=V+" Литров")
        volume.after(1000, testimony)
        if (Exit == True):
            volume.after(2, testimony)
            win.quit()
    win = tk.Tk()
    win.title('Объем воды в колодце')
    win.geometry("400x100+500+500")
    win.tk.call("wm", "iconphoto", win._w, tk.PhotoImage(file="logo.png"))
    #resizable.Так
    win.resizable(False, False)

    volume = tk.Label(win, font='Calibri 50 bold', foreground='black')
    volume.pack(anchor='center')

    testimony()
    global Exit

    win.mainloop()


# Участок кода с нажатием на список в трее
def on_clicked(icon, item):
    if str(item) == 'Выход':
        global Exit
        Exit = True
        icon.stop()
    elif str(item) == 'Окно':
        window()

#Код иконки в трее
icon = pystray.Icon('Serg', imagetree, menu=pystray.Menu(
        pystray.MenuItem('Окно', on_clicked),
        pystray.MenuItem('Выход', on_clicked)
    ))

# Выключение
if(Exit==True):
    exit()
#Запуск иконки
icon.run_detached()

#Настройка конфигурации COM порта
port = "COM4"  # Replace with the appropriate COM port name
baudrate = 9600

#Исключение ошибки COM порта
try:
    # Open the COM port
    ser = serial.Serial(port, baudrate=baudrate)
    print("Порт подключен.")

    # Read data from the Arduino
    while True:
        # Read a line of data from the serial port
        global V
        line = ser.readline().decode().strip()

        if line:

            begin_char = line.find('Объём ')  # мы знаем, что список начинается с 'Объём '
            end_char = line.find(' Л')  # убираем 2 последних символов с конца
            global V
            V=line[begin_char+6:end_char]
            # Подготовка времени
            current_date_time = datetime.datetime.now()
            current_time = current_date_time.time().strftime("%H:%M:%S")

            # Работа с файлом
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d")
            # convert datetime obj to string
            str_current_datetime = str(current_datetime)

            # create a file object along with extension
            file_name = str_current_datetime + ".CSV"
            file_fold = "Показания/"+file_name

            file = open(file_fold, 'a')
            with open(file_fold, mode="a", encoding='utf-8') as w_file:
                file = csv.writer(w_file, delimiter=",", lineterminator="\r")
                file.writerow([current_time, V])

            print(line)

            # Отключение COM порта
            if (Exit == True):

                ser.close()
                print("Serial connection END SG.")

except serial.SerialException as se:
    print("Serial port error:", str(se))

except KeyboardInterrupt:
    pass

finally:
    # Close the serial connection
    if ser.is_open:
        ser.close()
        print("Serial connection closed.")








