import DB
from tkinter import messagebox
import tkinter as tk


def user_check(lg, pswd, window):
    query = DB.connect_to_DB()[0]
    query.execute("set search_path to 'personnel'")
    query.execute('SELECT mail FROM admins')
    adm = query.fetchall()
    query.execute('SELECT mail FROM managers')
    man = query.fetchall()
    query.execute('SELECT mail FROM sellers')
    sel = query.fetchall()
    res = []
    # print(adm + man + sel)
    for i in adm + man + sel:
        if i[0] != None:
            res.append(i[0][0])
    if lg not in res:
        messagebox.showerror(title='Authorization', message='User not found')
        return
    else:
        query.execute('SELECT pswd FROM accounts')
        acc = query.fetchall()
        res = []
        for i in acc:
            if i[0] != None:
                res.append(i[0])
        if pswd not in res:
            messagebox.showerror(title='Authorization', message='Wrong Password and/or Login')
            return
        else:
            from profile import profile_window
            query.execute('SELECT id_acc FROM accounts WHERE pswd IN %s', ((pswd,),))
            id_session = query.fetchall()[0][0]
            window.destroy()
            window_next = tk.Tk()

            return profile_window(id_session, window_next)
