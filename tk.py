#Menambahkan import Toplevel dengan tujuan mengelola 2 window dalam 1 aplikasi
"""
toplevel berfungsi membuat window atau jendela tambahan di dalam satu aplikasi tanpa membuat instance root window baru.

Pada kode ini juga menambahkan scrollbar agar layar bisa di scroll
"""
from tkinter import Tk, Canvas, Entry, font, Label, Button, Toplevel,Scrollbar, Frame
from datetime import datetime

def update_clock():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%d/%m/%Y")
    canvas.itemconfig(clock_text, text=f"Date: {current_date} \nTime: {current_time}")
    root.after(1000, update_clock)
    
def days_between_dates(date1, date2):
    time_between = str(date2 - date1)
    number_of_days = time_between.split(" ")
    return number_of_days[0]

root = Tk()
root.geometry("850x500")
# Frame untuk menampung Canvas dan Scrollbar
main_frame = Frame(root)
main_frame.pack(fill="both", expand=True)
canvas = Canvas(main_frame, width=800, height=500, bg="medium purple2")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_text(100, 50, anchor="w", fill="orange", font="ComicSansMS 28 bold underline", text='My Family Birthday')

# Scrollbar
scrollbar = Scrollbar(
    main_frame,
    orient="vertical",
    command=canvas.yview
)
scrollbar.pack(side="right", fill="y")

# Hubungkan Canvas dengan Scrollbar
canvas.configure(yscrollcommand=scrollbar.set)


def get_event():
    list_of_events = []
    with open("noted.txt") as file:
        for line in file:
            line = line.rstrip('\n')
            if not line.strip():
                continue
            
            current_event = line.split(",")
            event_date = datetime.strptime(current_event[1], '%d/%m/%y').date()
            current_event[1] = event_date
            list_of_events.append(current_event)
        return list_of_events

# Membungkus kode yang menampilkan tanggal ulang tahun, lalu memanggilnya di
# save_birthday() agar ketika tombol save diklik, birthday otomatis terupdate
def display_events():
    canvas.delete("birthday_event")
    events = get_event()
    events.sort(key=lambda x: x[1])
    today = datetime.now().date()
    vertical_space = 100
    for event in events:
        text_col = ""
        event_name = event[0]
        days_until = days_between_dates(event[1], today)
        display_text = f"It is {days_until} is in {event_name} days"
        if int(days_until) <= 7:
            text_col = "red"
        if int(days_until) >= 1:
            text_col = "light blue"
        
        canvas.create_text(100, vertical_space, anchor="w", fill=text_col, font="ComicSansMS 20 bold", text=display_text,tags="birthday_event")
        vertical_space += 50
    canvas.configure(scrollregion=canvas.bbox("all"))


display_events()
clock_text = canvas.create_text(750, 400, anchor="e", fill="white", font="arial 18 bold")
update_clock()


#Mengeluarkan fungsi save_birthday() dari input_birthday(), sebenernya ini tidak memberikan perubahan, hanya membuat code lebih clean saja

def save_birthday(entry_name,entry_date,dialog):
    name = entry_name.get()
    date = entry_date.get()
    with open("noted.txt", "a") as file:
        file.write(f"{name},{date}\n")

    #Panggil display_events untuk otomatis update data
    display_events()

    dialog.destroy()

    #Berfungsi agar ketika tombol save diklik, main window tidak berada di aplikasi lain
    root.after(100, root.lift)
    root.after(150, root.focus_force)
    

def input_birthday():
    #Menggunakan toplevel
    dialog = Toplevel(root)
    dialog.title("Add Birthday")
    dialog.configure(bg="light blue")
    dialog.geometry("400x200")
    dialog.tk.call('tk::PlaceWindow', dialog._w, 'center')
    
    custom_font = font.Font(size=12, weight="bold")
    
    label_name = Label(dialog, text="Enter Name:", font=custom_font, bg="light blue")
    label_name.pack()
    
    entry_name = Entry(dialog, font=custom_font)
    entry_name.pack()
    
    label_date = Label(dialog, text="Enter Date (dd/mm/yy):", font=custom_font, bg="light blue")
    label_date.pack()
    
    entry_date = Entry(dialog, font=custom_font)
    entry_date.pack()
    
    
    """
    Meggunakan lambda karena button save sudah diluar fungsi input_birthday().Hal ini bertujuan agar save_birthday() dijalankan hanya ketika button diklik saja.
    lambda sendiri hanyalah keyword untuk membuat fungsi anonymous
    """
    button_save = Button(dialog, 
                         text="Save", 
                         command=lambda: save_birthday(entry_name, entry_date, dialog), 
                         bg="light blue", 
                         font=custom_font)
    button_save.pack()

input_birthday()


root.mainloop()