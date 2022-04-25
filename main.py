import tkinter as tk
import user_check


# sel: rivp@tsekh.ru thebestik111
# man: ilyi@tsekh.ru ilyusha1990
# adm: eleg@tsekh.ru elenavlad1995

def enter_window():
    main_window = tk.Tk()
    main_window.title("STAFF")
    main_window.geometry("768x540")
    content = tk.Frame(main_window)
    content.grid(column=0, row=0)
    bg = tk.PhotoImage(file='login.png')
    btn = tk.PhotoImage(file='btn.png')
    main_window.iconphoto(True, tk.PhotoImage(file='staff.png'))
    login = tk.Label(content, image=bg)
    login.grid(row=0, column=0, padx=0)

    email = tk.Entry(
        bg='#c4c4c4'.upper(),
        cursor='heart',
        font=('Times New Roman', 14),
        fg='#777777'.upper()
    )
    email.insert(0, 'login')
    email.place(width=200, height=32, x=72, y=273)
    pswrd = tk.Entry(
        bg='#c4c4c4'.upper(),
        cursor='heart',
        font=('Times New Roman', 14),
        fg='#777777'.upper()
    )
    pswrd.insert(0, 'password')
    pswrd.place(width=200, height=32, x=72, y=326)

    auth = tk.Button(
        bg="black",
        fg="yellow",
        activeforeground='gray',
        image=btn,
        command=lambda: user_check.user_check(email.get(), pswrd.get(), main_window)
    )
    auth.place(x=105, y=416, width=132, height=29)
    main_window.mainloop()


enter_window()
