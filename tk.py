from tkinter import Tk, Canvas, messagebox, Entry, font, Label, Button
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
canvas = Canvas(root, width=800, height=500, bg="medium purple2")
canvas.pack()
canvas.create_text(100, 50, anchor="w", fill="orange", font="ComicSansMS 28 bold underline", text='My Family Birthday')

def get_event():
    list_of_events = []
    with open("noted.txt") as file:
        for line in file:
            line = line.rstrip('\n')
            
            current_event = line.split(",")
            event_date = datetime.strptime(current_event[1], '%d/%m/%y').date()
            current_event[1] = event_date
            list_of_events.append(current_event)
        print(list_of_events)
        return list_of_events
events = get_event()
today = datetime.now().date()
vertical_space = 100
events.sort(key=lambda x: x[1])
print(today)
clock_text = canvas.create_text(750, 400, anchor="e", fill="white", font="arial 18 bold")
update_clock()

for event in events:
    text_col = ""
    event_name = event[0]
    days_until = days_between_dates(event[1], today)
    display_text = f"It is {days_until} is in {event_name} days"
    if int(days_until) <= 7:
        text_col = "red"
    if int(days_until) >= 1:
        text_col = "light blue"
    
    canvas.create_text(100, vertical_space, anchor="w", fill=text_col, font="ComicSansMS 20 bold", text=display_text)
    vertical_space += 50

def input_birthday():
    dialog = Tk()
    dialog.title("Add Birthday")
    dialog.configure(bg="light blue")
    dialog.geometry("400x200")
    dialog.eval('tk::PlaceWindow . center')
    
    custom_font = font.Font(size=12, weight="bold")
    
    label_name = Label(dialog, text="Enter Name:", font=custom_font, bg="light blue")
    label_name.pack()
    
    entry_name = Entry(dialog, font=custom_font)
    entry_name.pack()
    
    label_date = Label(dialog, text="Enter Date (dd/mm/yy):", font=custom_font, bg="light blue")
    label_date.pack()
    
    entry_date = Entry(dialog, font=custom_font)
    entry_date.pack()
    
    def save_birthday():
        name = entry_name.get()
        date = entry_date.get()
        with open("noted.txt", "a") as file:
            file.write(f"{name},{date}\n")
        dialog.destroy()
    
    button_save = Button(dialog, text="Save", command=save_birthday, bg="light blue", font=custom_font)
    button_save.pack()

input_birthday()


root.mainloop()