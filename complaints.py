import tkinter as tk
import DB
import urllib.request
import io
from PIL import ImageTk, Image
import time
from tkinter import ttk
from tkinter import messagebox


def exit_to_home(window, id_session):
    for child in window.winfo_children():
        child.destroy()
    import profile
    return profile.profile_window(id_session, window)


def exit_to_solutions(window, id_session, bakery, prk):
    for child in window.winfo_children():
        child.destroy()
    import solutions
    return solutions.solutions_window(id_session, bakery, prk, window)


def complaints_window(auth_id, bakery, prk, window):
    id_session = int(auth_id)

    def insert_solution():
        def insert_solution_DB(id, cont):
            try:
                query.execute('INSERT INTO solutions (complaint, content, account) VALUES (%s,%s,%s)',
                              (id, cont, id_session))
                connection[1].commit()
            except:
                messagebox.showerror(title='Database Response', message='Except Occured!\nCheck your data...')
            win.destroy()

        win = tk.Toplevel(window)
        win.title("Offering Solution...")
        win.geometry("400x400")
        frame = tk.Frame(win, bg='#d0bca3')
        frame.place(x=0, y=0, width=400, height=400)
        id_comp = tk.Entry(
            frame,
            bg='#c4c4c4',
            cursor='heart',
            font=('Times New Roman', 14),
            fg='black'.upper()
        )
        solution = tk.Entry(
            frame,
            bg='#c4c4c4',
            cursor='heart',
            font=('Times New Roman', 14),
            fg='black'.upper()
        )
        id_comp.insert(0, 'Enter the number of complaint...')
        id_comp.place(width=380, height=50, x=10, y=50)
        solution.insert(0, 'Propose your solution...')
        solution.place(width=380, height=250, x=10, y=100)
        btn = tk.PhotoImage(file='btn.png')
        auth = tk.Button(
            frame,
            bg="black",
            fg="yellow",
            activeforeground='gray',
            image=btn,
            command=lambda: insert_solution_DB(id_comp.get(), solution.get())
        )
        auth.place(x=150, y=360, width=132, height=29)
        window.mainloop()

    def list_of_complaints():
        for child in sec_frame.winfo_children():
            child.destroy()
        if tone.get().lower() in ['positive', 'negative', 'neutral']:
            for i in data:
                cnt = 0
                if i[2] == tone.get().lower():
                    query.execute(
                        'SELECT complaint FROM solutions WHERE account = {} ORDER BY date DESC'.format(id_session))
                    resolved = query.fetchall()
                    tk.Label(sec_frame, text='№' + str(i[0]) + ' ' + str(i[1])[:19] + ' graded with ' + str(i[4]) +
                                             '\n' + 'Content: ' + i[5], font=('Times New Roman', '15'), bg='#d0bca3',
                             fg=['green' if (i[0],) in resolved else 'black']).pack()
                    cnt += 1

    def timing():
        # display current hour,minute,seconds
        current_time = time.ctime()[:10] + '\n' + time.ctime()[10:]
        # configure the clock
        dt.config(text=current_time)
        # clock will change after every 200 microseconds
        dt.after(200, timing)

    def fps():
        tone.config(
            bg=[
                '#3fcc48'.upper() if tone.get().lower() == 'positive' else '#e9d644'.upper() if tone.get().lower() == 'neutral'
                else '#ff7d7d' if tone.get().lower() == 'negative' else 'gray'][0])
        search_btn.config(
            bg=[
                '#3fcc48'.upper() if tone.get().lower() == 'positive' else '#e9d644'.upper() if tone.get().lower() == 'neutral'
                else '#ff7d7d' if tone.get().lower() == 'negative' else 'gray'][0])
        tone.after(200, fps)

    connection = DB.connect_to_DB()
    query = connection[0]
    query.execute("set search_path to 'personnel'")
    window.title("STAFF")
    window.geometry("768x540")
    content = tk.Frame(window)
    canvas = tk.Canvas(window, width=860, height=200)
    content.grid(column=0, row=0)
    bg = tk.PhotoImage(file='complaints.png')
    profile = tk.Label(content, image=bg)
    profile.grid(row=0, column=0, padx=0)
    # window.iconphoto(True, tk.PhotoImage(file='staff.png'))
    query.execute('SELECT photo FROM accounts WHERE id_acc = {}'.format(id_session))
    photo_url = query.fetchall()[0][0]
    u = urllib.request.urlopen(photo_url)
    raw_data = u.read()
    u.close()
    profile_photo = Image.open(io.BytesIO(raw_data))
    profile_photo = profile_photo.resize((153, 230))
    profile_photo = ImageTk.PhotoImage(profile_photo)
    photo_box = tk.Label(profile, image=profile_photo)
    # window.iconbitmap('staff.png')
    photo_box.place(x=2, y=45, width=150, height=230)

    dt = tk.Label(profile, bg='#d0bca3'.upper(), font=('Times New Roman', '14'), text=time.ctime()[:10] + '\n'
                                                                             + time.ctime()[10:], compound=tk.LEFT)
    dt.place(x=10, y=305, width=135, height=43)
    timing()

    home = tk.PhotoImage(file='home_icon.png')
    home_btn = tk.Button(
        bg="red",
        fg="yellow",
        activeforeground='gray',
        image=home,
        command=lambda: exit_to_home(window, id_session)
    )
    home_btn.place(x=395, y=4, width=90, height=27)
    solution = tk.PhotoImage(file='sol_icon.png')
    solution_btn = tk.Button(
        bg="red",
        fg="yellow",
        activeforeground='gray',
        image=solution,
        command=lambda: exit_to_solutions(window, id_session, bakery, prk)
    )
    solution_btn.place(x=515, y=4, width=90, height=27)
    perk = tk.Label(profile, bg='#d0bca3'.upper(), font=('Times New Roman', '20'), text=prk,
                    compound=tk.CENTER)
    perk.place(x=25, y=450, width=105, height=45)
    # размещаем жалобы этой пекарни по тонам
    tone = tk.Entry(
        bg='gray',
        cursor='heart',
        font=('Times New Roman', 14),
        fg='black'.upper()
    )
    tone.insert(0, 'neutral')
    tone.place(width=150, height=25, x=200, y=100)

    query.execute('SELECT address FROM bakeries WHERE id_bakeries = {}'.format(bakery))
    name_bakery = query.fetchall()[0][0]
    name_bg = tk.PhotoImage(file='name_comp.png')
    name = tk.Label(profile, image=name_bg, font=('Times New Roman', '20'))
    name.config(text=name_bakery, foreground="black", compound=tk.CENTER)
    name.place(x=365, y=50, width=254, height=38)

    query.execute('SELECT * FROM complaints WHERE bakery = {} ORDER BY date DESC'.format(bakery))
    data = query.fetchall()

    # упорядочим контент

    basement = tk.Frame(profile, bg='#d0bca3')
    basement.place(x=200, y=130, width=550, height=380)
    scroll_frame = tk.LabelFrame(basement, bg='#d0bca3')
    scroll_frame.place(x=0, y=0, width=550, height=380)
    canvas = tk.Canvas(scroll_frame, bg='#d0bca3')
    canvas.place(x=0, y=0, width=550, height=380)
    sb = ttk.Scrollbar(scroll_frame, orient='vertical', command=canvas.yview)
    sb.pack(side='right', fill='y')
    canvas.config(yscrollcommand=sb.set)
    canvas.bind('<Configure>', lambda e: canvas.config(scrollregion=canvas.bbox('all')))
    sec_frame = tk.Frame(canvas, bg='#d0bca3')
    canvas.create_window((0, 0), window=sec_frame, anchor='nw')
    sb.pack(side="right", fill="y")

    for i in range(100):
        tk.Label(sec_frame, bg='#d0bca3').pack()

    search_btn = tk.Button(
        bg=['#3fcc48'.upper() if tone.get() == 'positive' else '#e9d644'.upper() if tone.get() == 'neutral'
        else '#ff7d7d' if tone.get() == 'negative' else 'gray'][0],
        fg="black",
        activeforeground='gray',
        text='search',
        font=('Times New Roman', 10, 'bold'),
        command=list_of_complaints
    )

    solve_btn = tk.Button(
        bg='#d0bca2',
        fg="black",
        activeforeground='gray',
        text='Offer solution!',
        font=('Times New Roman', 10, 'bold'),
        command=insert_solution
    )
    search_btn.place(x=350, y=100, width=52, height=26)
    solve_btn.place(x=450, y=98, width=100, height=29)
    fps()

    window.mainloop()
