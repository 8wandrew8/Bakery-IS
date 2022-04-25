import psycopg2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def init(cur, since):
    plt.rcParams['figure.figsize'] = 36, 14
    cur.execute("set search_path to 'personnel'")
    cur.execute("SELECT * FROM density WHERE tm>%s::date", (since,))
    dt = pd.DataFrame(np.array(cur.fetchall()))

    plt.figure(figsize=(10, 5))
    for i in range(1, 4):
        plt.subplot(int('31' + str(i)))
        plt.title('Bakery {}'.format(i))
        plt.plot(dt.loc[dt[1] == i, 4])
    plt.suptitle('Check Average Dynamic')
    plt.show()

    plt.figure(figsize=(10, 5))
    for i in range(1, 4):
        plt.subplot(int('31' + str(i)))
        plt.title('Bakery {}'.format(i))
        plt.plot(dt.loc[dt[1] == i, 3])
    plt.suptitle('Orders to complete in turn')
    plt.show()

    plt.figure(figsize=(10, 5))
    for i in range(1, 4):
        plt.subplot(int('31' + str(i)))
        plt.title('Bakery {}'.format(i))
        plt.plot(dt.loc[dt[1] == i, 2])
    plt.suptitle('Client Density')
    plt.show()

    plt.figure(figsize=(10, 5))
    for i in range(1, 4):
        plt.subplot(int('31' + str(i)))
        plt.title('Bakery {}'.format(i))
        plt.plot(dt.loc[dt[1] == i, 3] / (dt.loc[dt[1] == i, 2] + 1))
    plt.suptitle('Client Density / Orders. Values more that 1 indicate low effectiveness of sellers')
    plt.show()

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    cnt = 1
    cur.execute(
        "SELECT bakery, dens, address, trim(trailing from to_char(tm,'Day')) FROM density JOIN bakeries ON bakery = id_bakeries".format(
            cnt))
    check = pd.DataFrame(np.array(cur.fetchall()))
    check = check.dropna(axis=0)
    check[1] = check[1].astype(int)
    check[0] = check[0].astype(int)
    plt.figure(figsize=(11, 6))
    for i in days:
        f = plt.subplot(int('71' + str(cnt)))
        plt.title('{}s'.format(i))
        cnt += 1
        for j in range(1, 4):
            series = check.loc[(check[0] == j) & (check[3] == i), 1:3][1]
            series.reset_index(inplace=True, drop=True)
            plt.plot(series, label='Bakery ' + str(j))
        plt.legend(loc='right')
    plt.suptitle('Daywise client stream')
    plt.show()
