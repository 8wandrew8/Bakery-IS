import tkinter as tk

import psycopg2

import DB
import urllib.request
import io
from PIL import ImageTk, Image
import time
import pandas as pd
import numpy as np
from tkinter import messagebox


def exit_to_solutions(window, id_session, bakery, prk):
    for child in window.winfo_children():
        child.destroy()
    import solutions
    return solutions.solutions_window(id_session, bakery, prk, window)


def exit_to_main(window):
    window.destroy()
    import main
    return main.enter_window()


def exit_to_complaints(window, id_session, bakery, prk):
    for child in window.winfo_children():
        child.destroy()
    import complaints
    return complaints.complaints_window(id_session, int(bakery), prk, window)


def vizualize(query, dt, con):
    try:
        import algorithm
        algorithm.init(query, dt)
    except:
        messagebox.showerror(title='Visualiztion', message='Somethig went wrong...\nTry precise format!')
        con.rollback()


def profile_window(auth_id, window):
    def get_analytics(query):
        win = tk.Toplevel(window)
        win.title("Getting Analytics...")
        win.geometry("400x400")
        frame1 = tk.Frame(win, bg='#d0bca3')
        frame1.place(x=0, y=0, width=400, height=400)
        frame = tk.Frame(win)
        frame.place(x=10, y=0, width=380, height=300)
        query.execute('SELECT avg(grade) FROM complaints WHERE bakery = {}'.format(bakery_id))
        average = query.fetchall()[0][0]
        tk.Label(frame, text='Bakery: ' + address, font=('Times New Roman', 18, 'bold')).pack()
        tk.Label(frame, text='Average grade from customers: ' + str(round(average, 2)),
                 font=('Times New Roman', 14, 'bold')).pack()
        days = ['Mondays', 'Tuesdays', 'Wednesdays', 'Thursdays', 'Fridays', 'Saturdays', 'Sundays']
        for i in range(1, 8):
            query.execute(
                'SELECT dens FROM density WHERE bakery = {} AND extract(isodow from tm) = {}'.format(bakery_id, i))
            check = pd.DataFrame(np.array(query.fetchall()))
            temp = check.mean()[0]
            tk.Label(frame, text='Average density on ' + days[i - 1] + ': ' + str(round(temp, 2)),
                     font=('Times New Roman', 10, 'bold')).pack()
        date = tk.Entry(
            frame,
            bg='white',
            fg='black',
            font=('Times New Roman', 10, 'bold')
        )
        date.insert(0, 'Start date: YYYY-MM-DD')
        date.place(x=110, y=260, width=153, height=20)
        auth = tk.Button(
            frame1,
            bg='#d0bcaa',
            fg='black',
            text='visualize'.upper(),
            activeforeground='gray',
            command=lambda: vizualize(query, date.get(), connection[1]),
            font=('Times New Roman', 10, 'bold')
        )
        auth.place(x=150, y=330, width=100, height=40)

        window.mainloop()

    def rating(id_session):
        query.execute('with res AS (SELECT grade FROM sellers_est WHERE target = %s UNION ALL SELECT grade FROM '
                      'solution_est INNER JOIN solutions ON solution = id_solutions WHERE account = %s) SELECT '
                      'round(avg(grade), 2) FROM res', (id_session, id_session))
        res = query.fetchall()[0][0]
        if res != None:
            return float(res)
        else:
            return 0

    def perk(rating):
        pk = rating * 200 * (int(time.ctime()[8:10])) / (30 * 5)
        return round(pk, 2)

    def timing():
        current_time = time.ctime()[:10] + '\n' + time.ctime()[10:]
        dt.config(text=current_time)
        dt.after(200, timing)
        return dt

    connection = DB.connect_to_DB()
    # psycopg2.connection.se .setAutoCommit(True)
    query = connection[0]
    query.execute("set search_path to 'personnel'")
    id_session = int(auth_id)
    window.title("STAFF")
    window.geometry("768x540")
    content = tk.Frame(window)
    window.iconphoto(True, tk.PhotoImage(file='staff.png'))
    content.grid(column=0, row=0)
    bg = tk.PhotoImage(file='profile.png')
    profile = tk.Label(content, image=bg)
    profile.grid(row=0, column=0, padx=0)

    try:
        query.execute('SELECT photo FROM accounts WHERE id_acc = {}'.format(id_session))
        photo_url = query.fetchall()[0][0]
        u = urllib.request.urlopen(photo_url)
        raw_data = u.read()
        u.close()
        profile_photo = Image.open(io.BytesIO(raw_data))
        profile_photo = profile_photo.resize((153, 230))
        profile_photo = ImageTk.PhotoImage(profile_photo)
        photo_box = tk.Label(profile, image=profile_photo)
        photo_box.place(x=2, y=45, width=153, height=230)
    finally:
        # Заполняем основной информацией и запоминаем должность для сценария
        query.execute('SELECT * FROM employees WHERE id_acc = {}'.format(id_session))
        main_data = query.fetchall()
        position = main_data[0][3]
        name_bg = tk.PhotoImage(file='name.png')
        name = tk.Label(profile, image=name_bg, font=('Times New Roman', '28'))
        name.config(text=main_data[0][1] + ' ' + main_data[0][2], foreground="black", compound=tk.CENTER)
        name.place(x=170, y=45, width=457, height=39)
        pos = tk.Label(profile, bg='#d0bca3'.upper(), font=('Times New Roman', '10'), text=main_data[0][3], compound=tk.LEFT)
        pos.place(x=230, y=157, width=60, height=10)
        # window.iconbitmap('staff.png')
        # Заполняем до конца
        query.execute('SELECT * FROM {}s WHERE account = {}'.format(position, id_session))
        data = query.fetchall()
        try:
            birth = tk.Label(profile, bg='#d0bca3'.upper(), font=('Times New Roman', '10'), text=data[0][3], compound=tk.LEFT)
            birth.place(x=322, y=315, width=120, height=13)
            dt = tk.Label(profile, bg='#d0bca3'.upper(), font=('Times New Roman', '14'), text=time.ctime()[:10] + '\n'
                                                                                     + time.ctime()[10:],
                          compound=tk.LEFT)
            dt.place(x=10, y=305, width=140, height=43)
            timing()
        finally:
            try:
                seniority = tk.Label(profile, bg='#d0bca3'.upper(), font=('Times New Roman', '10'), text=data[0][4],
                                     compound=tk.LEFT)
                seniority.place(x=238, y=231, width=20, height=15)
            finally:
                wage = tk.Label(profile, bg='#d0bca3'.upper(), font=('Times New Roman', '10'),
                                text=str(['qualified' if data[0][6] else 'not qualified'][0]),
                                compound=tk.LEFT)
                wage.place(x=228, y=204, width=80, height=15)
                try:
                    if position != 'admin':
                        query.execute('SELECT * FROM bakeries WHERE id_bakeries = {}'.format(data[0][7]))
                        temp = query.fetchall()
                        bakery_id = data[0][7]
                        address = temp[0][2]
                        id_admin = temp[0][4]
                        bakery = tk.Label(profile, bg='#d0bca3'.upper(), font=('Times New Roman', '10'), text=address,
                                          compound=tk.LEFT)
                        bakery.place(x=227, y=173, width=120, height=15)
                        query.execute('SELECT fname, lname FROM admins WHERE id_admins = {}'.format(id_admin))
                        temp = query.fetchall()
                        name_admin = temp[0][0] + ' ' + temp[0][1]
                        admin = tk.Label(profile, bg='#d0bca3'.upper(), font=('Times New Roman', '10'), text=name_admin,
                                         compound=tk.LEFT)
                        admin.place(x=229, y=192, width=120, height=10)
                        number = tk.Label(profile, bg='#d0bca3'.upper(), font=('Times New Roman', '10'), text=data[0][10],
                                          compound=tk.LEFT)
                        number.place(x=450, y=172, width=100, height=11)
                        email_tsekh = tk.Label(profile, bg='#d0bca3'.upper(), font=('Times New Roman', '10'),
                                               text=data[0][11][0],
                                               compound=tk.LEFT)
                        email_tsekh.place(x=450, y=150, width=100, height=20)
                        email_private = tk.Label(profile, bg='#d0bca3'.upper(), font=('Times New Roman', '10'),
                                                 text=data[0][11][1],
                                                 compound=tk.LEFT)
                        email_private.place(x=337, y=343, width=145, height=20)
                    else:
                        analytics = tk.PhotoImage(file='analytics.png')
                        analytics_btn = tk.Button(
                            bg='#d0bca3',
                            fg="yellow",
                            activeforeground='gray',
                            image=analytics,
                            command=lambda: get_analytics(query)
                        )
                        analytics_btn.place(x=590, y=330, width=162, height=166)
                        query.execute(
                            'SELECT id_admins, fname, lname FROM admins WHERE account = {}'.format(id_session))
                        temp = query.fetchall()
                        name_admin = temp[0][1] + ' ' + temp[0][2]
                        admin = tk.Label(profile, bg='#d0bca3'.upper(), font=('Times New Roman', '10'), text=name_admin,
                                         compound=tk.LEFT)
                        admin.place(x=229, y=192, width=120, height=10)
                        query.execute('SELECT address, id_bakeries FROM bakeries WHERE admin = {}'.format(temp[0][0]))
                        temp = query.fetchall()
                        bakery_id = temp[0][1]
                        address = temp[0][0]
                        bakery = tk.Label(profile, bg='#d0bca3'.upper(), font=('Times New Roman', '10'), text=address,
                                          compound=tk.LEFT)
                        bakery.place(x=227, y=173, width=120, height=15)
                        number = tk.Label(profile, bg='#d0bca3'.upper(), font=('Times New Roman', '10'), text=data[0][9],
                                          compound=tk.LEFT)
                        number.place(x=450, y=172, width=100, height=11)
                        email_tsekh = tk.Label(profile, bg='#d0bca3'.upper(), font=('Times New Roman', '10'),
                                               text=data[0][10][0],
                                               compound=tk.LEFT)
                        email_tsekh.place(x=450, y=150, width=100, height=20)
                        email_private = tk.Label(profile, bg='#d0bca3'.upper(), font=('Times New Roman', '10'),
                                                 text=data[0][10][1],
                                                 compound=tk.LEFT)
                        email_private.place(x=337, y=343, width=145, height=20)
                    rate = rating(id_session)
                    rating = tk.Label(profile, bg='#d0bca3'.upper(), font=('Times New Roman', '10'), text=rate,
                                      compound=tk.LEFT)
                    rating.place(x=243, y=222, width=30, height=10)
                    perk1 = tk.Label(profile, bg='#d0bca3'.upper(), font=('Times New Roman', '20'), text='$ ' + str(perk(rate)),
                                     compound=tk.CENTER)
                    perk1.place(x=25, y=450, width=105, height=45)
                    prk = '$ ' + str(perk(rate))
                finally:
                    ext = tk.PhotoImage(file='exit.png')
                    ext_btn = tk.Button(
                        bg="black",
                        fg="yellow",
                        activeforeground='gray',
                        image=ext,
                        command=lambda: exit_to_main(window)
                    )
                    ext_btn.place(x=695, y=216, width=43, height=28)
                    complaints = tk.PhotoImage(file='complaints_icon.png')
                    comp_btn = tk.Button(
                        bg="red",
                        fg="yellow",
                        activeforeground='gray',
                        image=complaints,
                        command=lambda: exit_to_complaints(window, id_session, bakery_id, prk)
                    )
                    comp_btn.place(x=388, y=4, width=86, height=27)
                    solution = tk.PhotoImage(file='sol_icon.png')
                    solution_btn = tk.Button(
                        bg="red",
                        fg="yellow",
                        activeforeground='gray',
                        image=solution,
                        command=lambda: exit_to_solutions(window, id_session, bakery_id, prk)
                    )
                    solution_btn.place(x=515, y=4, width=90, height=27)
                    window.mainloop()
