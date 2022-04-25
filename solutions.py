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


def exit_to_complaints(window, id_session, bakery, prk):
    for child in window.winfo_children():
        child.destroy()
    import complaints
    return complaints.complaints_window(id_session, int(bakery), prk, window)


def solutions_window(auth_id, bakery, prk, window):
    id_session = int(auth_id)

    def estimate_solution_DB(if_manager):
        def insert_BD(id, gr):
            if (id_session,) not in if_manager:
                messagebox.showerror(title='Access Response', message='Only managers can grade solutions!')
            else:
                try:
                    query.execute('SELECT id_managers FROM managers WHERE account = {}'.format(id_session))
                    idd = query.fetchall()[0][0]
                    query.execute(
                        'INSERT INTO solution_est (grade, solution, manager) VALUES ({},{},{})'.format(int(gr), int(id),
                                                                                                       int(idd)))
                    connection[1].commit()
                except:
                    messagebox.showerror(title='Database Response', message='Except Occured!\nCheck your data...')
            win1.destroy()

        win1 = tk.Toplevel(window)
        win1.title("Estimating Solution...")
        win1.geometry("400x400")
        frame1 = tk.Frame(win1, bg='#d0bca3')
        frame1.place(x=0, y=0, width=400, height=400)
        id_comp = tk.Entry(
            frame1,
            bg='#c4c4c4',
            cursor='heart',
            font=('Times New Roman', 14),
            fg='black'.upper()
        )
        solution = tk.Entry(
            frame1,
            bg='#c4c4c4',
            cursor='heart',
            font=('Times New Roman', 14),
            fg='black'.upper()
        )
        id_comp.insert(0, 'Enter the number of solution...')
        id_comp.place(width=380, height=50, x=10, y=50)
        solution.insert(0, 'Grade...')
        solution.place(width=380, height=250, x=10, y=100)
        btn = tk.PhotoImage(file='btn.png')
        auth1 = tk.Button(
            frame1,
            bg="black",
            fg="red",
            activeforeground='gray',
            image=btn,
            font=('Times New Roman', 14, 'bold'),
            command=lambda: insert_BD(id_comp.get(), solution.get())
        )
        auth1.place(x=150, y=360, width=132, height=29)
        win1.mainloop()

    def all_solutions():
        query.execute('SELECT account FROM managers')
        if_manager = query.fetchall()
        win = tk.Toplevel(window)
        win.title("All solutions...")
        win.geometry("400x600")
        frame = tk.Frame(win, bg='#d0bca3')
        frame.place(x=0, y=0, width=400, height=600)
        basement = tk.Frame(win)
        basement.place(x=10, y=50, width=390, height=500)
        scroll_frame = tk.LabelFrame(basement, bg='#d0bca3')
        scroll_frame.place(x=0, y=0, width=390, height=500)
        canvas = tk.Canvas(scroll_frame, bg='#d0bca3')
        canvas.place(x=0, y=0, width=390, height=500)
        sb = ttk.Scrollbar(scroll_frame, orient='vertical', command=canvas.yview)
        sb.pack(side='right', fill='y')
        canvas.config(yscrollcommand=sb.set)
        canvas.bind('<Configure>', lambda e: canvas.config(scrollregion=canvas.bbox('all')))
        sec_frame = tk.Frame(canvas, bg='#d0bca3')
        canvas.create_window((0, 0), window=sec_frame, anchor='nw')
        sb.pack(side="right", fill="y")
        query.execute(
            'SELECT id_solutions, solutions.content, solutions.date, fname, lname, positions, complaints.content FROM solutions JOIN employees ON account = id_acc JOIN complaints'
            ' ON complaint = id_complaints WHERE account!={} ORDER BY solutions.date DESC'.format(id_session))
        dt = query.fetchall()
        query.execute('SELECT solution, avg(grade) FROM solution_est GROUP BY solution')
        current_score = query.fetchall()
        for i in dt:
            aver = 'No grades yet'
            for j in current_score:
                if i[0] == j[0]:
                    aver = str(round(j[1], 2))
            tk.Label(sec_frame, text='№' + str(i[0]) + ' ' + str(i[2])[:19] +
                                     '\n' + 'Content: ' + i[1] + '\nEmployee: ' + i[3] + ' ' + i[
                                         4] + '\nPosition: ' + i[5] +
                                     '\nComplaint content: ' + i[6] +
                                     '\nAverage score: ' + aver + '\n\n', font=('Times New Roman', '15'),
                     bg='#d0bca3').pack(anchor=tk.CENTER)
        btn = tk.PhotoImage(file='btn.png')
        auth2 = tk.Button(
            frame,
            bg='#d0bca2',
            fg="black",
            text='GRADE!',
            font=('Times New Roman', 10, 'bold'),
            activeforeground='gray',
            command=lambda: estimate_solution_DB(if_manager)
        )
        auth2.place(x=135, y=555, width=130, height=29)
        window.mainloop()

    def timing():
        current_time = time.ctime()[:10] + '\n' + time.ctime()[10:]
        dt.config(text=current_time)
        dt.after(200, timing)

    def list_of_solutions():
        list_box = []
        query.execute('SELECT solution, avg(grade) FROM solution_est GROUP BY solution')
        current_score = query.fetchall()
        for i in data:
            aver = 'No grades yet'
            for j in current_score:
                if i[0] == j[0]:
                    aver = str(round(j[1], 2))
            list_box.append(
                tk.Label(sec_frame, text='№' + str(i[1]) + ' ' + str(i[3])[:19] +
                                         '\n' + 'Content: ' + i[2] +
                                         '\nAverage score: ' + aver + '\n\n', font=('Times New Roman', '15'),
                         bg='#d0bca3'))
        for j in list_box:
            j.pack()

    connection = DB.connect_to_DB()
    query = connection[0]
    query.execute("set search_path to 'personnel'")
    window.title("STAFF")
    window.geometry("768x540")
    content = tk.Frame(window)
    content.grid(column=0, row=0)
    bg = tk.PhotoImage(file='sollutions.png')
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
                                                                                      + time.ctime()[10:],
                  compound=tk.LEFT)
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
    complaints = tk.PhotoImage(file='complaints_icon.png')
    complaints_btn = tk.Button(
        bg="red",
        fg="yellow",
        activeforeground='gray',
        image=complaints,
        command=lambda: exit_to_complaints(window, id_session, bakery, prk)
    )
    home_btn.place(x=515, y=4, width=90, height=27)
    complaints_btn.place(x=395, y=4, width=90, height=27)
    perk = tk.Label(profile, bg='#d0bca3'.upper(), font=('Times New Roman', '20'), text=prk,
                    compound=tk.CENTER)
    perk.place(x=25, y=450, width=105, height=45)

    query.execute('SELECT * FROM solutions WHERE account = {} ORDER BY date DESC'.format(id_session))
    data = query.fetchall()

    # упорядочим контент
    basement = tk.Frame(profile)
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
    list_of_solutions()
    for i in range(50):
        tk.Label(sec_frame, bg='#d0bca3').pack()

    all_btn = tk.Button(
        bg='#d0bca2',
        fg="black",
        activeforeground='gray',
        text='All solutions',
        font=('Times New Roman', 10, 'bold'),
        command=lambda: all_solutions()
    )
    all_btn.place(x=200, y=98, width=100, height=29)
    window.mainloop()
