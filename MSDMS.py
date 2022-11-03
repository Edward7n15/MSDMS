import sqlite3
import random
import datetime

# creating connection from host language to sqlite3
conn = sqlite3.connect('./MSDMS')
c = conn.cursor()
script = None

"""
def login(input_id):
    '''
    The login screen, ask for id and password, could determine users and artists, allow new users to register.
    After signup, goto corresponding system.
    NOT providing logout option, it is in the inner interface AFTER login
    :return:(int)login_type: 1 (user), 2 (artist)
    '''

    login_type = id_check(input_id)
    if login_type == '-1' or check_pwd(login_type, input_id) == False:
        print('closing app due to your choice or wrong password')
        quit()
    elif login_type == '3':
        # ask for specific login type
        login_type = input('enter 1 to login user account, enter 2 to longin artist account: ')
    return login_type
"""

def id_check(input_id):
    '''
    check if an id is legal. If yes, determine it is a uid or an aid. If no, prompt for a uid register.
    :param: (str)input id
    :return: (int) 1: user 2:artist 3.both -1: exit 0: signup
    '''
    user = False
    artist = False
    script = 'select uid from users where uid like "' + str(input_id) + '";'
    c.execute(script)
    row_u = c.fetchone()
    if row_u:
        user = True
    script = 'select aid from artists where aid like "' + str(input_id) + '";'
    c.execute(script)
    row_a = c.fetchone()
    if row_a:
        artist = True

    if user:
        if artist:
            return '3'
        else:
            return '1'
    elif artist:
        return '2'
    else:
        choice = input('cannot find your id, enter 1 to signup, enter 0 to quit: ')
        if choice == '1':
            return '0'
        elif choice == '0':
            return '-1'


def signup():
    '''
    create a new account for the user by inserting values to users table
    :return:
    '''
    c.execute('select uid from users;')
    ids = c.fetchall()
    id_list = []
    for i in ids:
        id_list.append(i[0])

    while True:
        uid = input('-> creating new user account\nenter your uid in exact 4 characters: ')
        if len(uid) != 4:
            print('input length is not exact 4, try again')
        elif uid in id_list:
            print('input id is taken, try again')
        else:
            break

    name = input('enter user name: ')
    pwd = input('enter password: ')
    c.execute('insert into users values (:uid, :name, :pwd);', {'uid': uid, 'name': name, 'pwd': pwd})
    user_interface(uid)


def check_pwd(login_type, input_id):
    '''
    goto user's or artist's db depend on login type
    prompt for password, then check if it matches the id
    ask for another try or quit when the not matching
    :param id: input id
    :param login_type: id type
    :return: (bool) true: valid, false: quit
    '''
    # input_id = input('-> checking password:\nenter id: ')
    pwd = input('enter your password: ')

    if login_type == '1' or login_type == '3':
        script = 'select pwd from users where uid like "' + str(input_id) + '";'
        c.execute(script)
        row = c.fetchone()

    elif login_type == '2':
        script = 'select pwd from artists where aid like "' + str(input_id) + '";'
        c.execute(script)
        row = c.fetchone()

    if row and pwd == row[0]:
        print('correct password')
        return True
    else:
        print('wrong password')
        return False


def user_interface(current_id):
    '''
    display user op, logout and exit options
    prompt for command, then execute it.
    :return:
    '''
    print("-> user face")
    sno = None
    while True:
        op = input('enter 1 to start a session, enter 2 to search for songs and playlists, enter 3 to search for '
                   'artists, enter 4 to end the session, enter 0 to logout: ')
        if op == '1':
            sno = start_session(current_id)
        elif op == '2':
            search_songs(current_id)
        elif op == '3':
            search_artists(current_id)
        elif op == '4':
            end_session(sno, current_id)
        elif op == '0':
            end_session(sno, current_id)
            return
        else:
            print('invalid command')


def start_session(current_id):
    c.execute('select sno from sessions;')
    all_sno = c.fetchall()
    sno_lst = []
    for sn in all_sno:
        sno_lst.append(sn)
    while True:
        sno = random.sample(range(0, 5000), 1)[0]
        if sno not in sno_lst:
            break
    now = datetime.datetime.now()
    date = now.strftime('%Y-%m-%d')
    c.execute('insert into sessions values (:uid, :sno, :start, null);', {'uid': current_id, 'sno': sno, 'start': date})
    print('-> session start')
    return sno


def search_songs(current_id):
    kw = input("Input the keywords: ").lower().split()
    c.execute('select * from songs;')
    pack = c.fetchall()
    cnt_list = []
    for song in pack:
        title = song[1].lower().split()
        joint = [value for value in title if value in kw]
        joint_num = len(set(joint))
        if joint_num != 0:
            cnt_list.append([song[0], song[1], song[2], joint_num, 'song'])
    c.execute('select * from playlists;')
    pack = c.fetchall()
    for playlist in pack:
        title = playlist[1].lower().split()
        joint = [value for value in title if value in kw]
        joint_num = len(set(joint))
        if joint_num != 0:
            cnt_list.append([playlist[0], playlist[1], playlist[2], joint_num, 'playlist'])
    cnt_list.sort(key=lambda x: x[3], reverse=True)
    songs = cnt_list
    m = 0
    while True:
        n = min(5, len(songs) - m)
        for i in range(m, m + n):
            print(songs[i])
        inp = int(input(
            "Enter 0 to end, Enter 1 to 5 to select the songs, Enter 6 to go the previous page, Enter 7 to go the "
            "next page: "))
        if inp == 0:
            return
        if 1 <= inp <= n:
            if songs[m + inp - 1][-1] == "song":
                select_song(songs[m + inp - 1][0], current_id)
                return
            if songs[m + inp - 1][-1] == "playlist":
                pid = songs[m + inp - 1][0]
                c.execute('select s.sid, s.title, s.duration from songs s join plinclude pi using (sid) where pi.pid = :pid', {'pid':pid})
                pack = c.fetchall()
                cnt_list = []
                for song in pack:
                    cnt_list.append([song[0], song[1], song[2], 'song'])
                songs = cnt_list
                m = 0
        if inp == 6:
            m -= 5
            m = max(0, m)
        elif inp == 7:
            m += 5
            m = min(int(len(songs) / 5) * 5, m)


def select_song(sid, uid):
    while True:
        inp = int(input(
            "Enter 0 to return to interface, Enter 1 to listen, Enter 2 to see more information about it, Enter 3 to "
            "add it to a playlist: "))
        if inp == 0:
            return
        elif inp == 1:
            # check if a session has already started
            c.execute('select * from sessions;')
            ret = c.fetchall()
            now = datetime.datetime.now()
            date = now.strftime('%Y-%m-%d')
            sno = None
            for sen in ret:
                if sen[0] == uid and sen[2] == date and sen[3] is None:
                    sno = sen[1]
            # if no, start a session
            if sno is None:
                sno = start_session(uid)
            # check if the song is played in this session
            c.execute('select * from listen l join songs s using (sid) where l.sno =:sno and l.uid =:uid and l.sid '
                      '=:sid;', {'sno': sno, 'uid':uid, 'sid':sid})
            ret = c.fetchall()
            # if yes, increase cnt by 1
            if ret:
                c.execute('select cnt from listen where uid = :uid and sno = :sno and sid = :sid;', {'sno': sno, 'uid':uid, 'sid':sid})
                cnt = c.fetchone()[0] + 1
                c.execute('update listen set cnt = :cnt where uid = :uid and sno = :sno and sid = :sid;', {'sno': sno, 'uid':uid, 'sid':sid, 'cnt':cnt})
            # if no, insert a value
            else:
                c.execute('insert into listen values (:uid, :sno, :sid, 1);', {'sno': sno, 'uid':uid, 'sid':sid})


        elif inp == 2:
            # output artist name, aid, title, duration, playlists[]
            c.execute('select distinct a.name, a.aid from artists a join perform p using (aid) where sid = :sid;', {'sid':sid})
            artist = c.fetchall()
            print('artists: (name, aid)')
            print(artist)

            c.execute('select title, duration from songs where sid = :sid', {'sid':sid})
            song = c.fetchall()
            print('song info: (song_title, duration)')
            print(song)

            c.execute('select distinct pl.pid, pl.title from plinclude p join playlists pl using (pid) where p.sid = '
                      ':sid', {'sid':sid})
            pl = c.fetchall()
            print('included in: (pid, playlist_title)')
            print(pl)


        elif inp == 3:
            pid = int(input('enter the pid of the playlist: '))
            # check if this pid exists
            c.execute('select pid from playlists')
            ret = c.fetchall()
            id_list = []
            for i in ret:
                id_list.append(i[0])
            if pid in id_list:
                c.execute('select pl.pid, max(pi.sorder) from plinclude pi join playlists pl using (pid) group by '
                          'pl.pid;')
                num = c.fetchall()
                for p in num:
                    if pid == p[0]:
                        index = p[1]+1
                        c.execute('insert into plinclude values (:pid, :sid, :sord)', {'pid':pid, 'sid':sid, 'sord': index})
            else:
                print('-> pid not exist')
                pid = random.sample(range(0, 5000), 1)[0]
                print('-> assign to', pid)
                ttl = input('name your new playlist: ')
                c.execute('insert into playlists values (:pid, :ttl, :uid)', {'pid':pid, 'ttl':ttl, 'uid':uid})
                c.execute('insert into plinclude values (:pid, :sid, 1)', {'pid':pid, 'sid':sid})

        else:
            print('invalid command')


def search_artists(uid):
    kw = input("Input the keywords: ").lower().split()
    c.execute('with song_num(aid, num) as (select a.aid, count(sid) from artists a join perform using (aid) join '
              'songs using (sid) group by a.aid)select * from artists join perform using (aid) join songs using (sid) '
              'join song_num using (aid); ')
    pack = c.fetchall()
    cnt_list = []
    cnt = {}
    total_song = {}
    for artist in pack:
        name = artist[1].lower()
        if artist[0] not in cnt:
            cnt[artist[0]] = 0
        if artist[0] not in total_song:
            total_song[artist[0]] = artist[-1]

        title = artist[-3].lower().split()
        joint_name = [value for value in name.split() if value in kw]
        joint_title = [value for value in title if value in kw]
        joint_num_name = len(set(joint_name))
        joint_num_title = len(set(joint_title))
        joint_num = joint_num_title + joint_num_name
        cnt[artist[0]] += joint_num
    c.execute('select * from artists;')

    bag = c.fetchall()
    for artist in bag:
        cnt_list.append([artist[0], artist[1], artist[2], total_song[artist[0]], cnt[artist[0]]])

    cnt_list.sort(key=lambda x: x[-1], reverse=True)

    artists = cnt_list
    for i in artists:
        if i[-1] == 0:
            del artists[artists.index(i)]
    mode = 1
    m = 0
    while True:
        n = min(5, len(artists) - m)
        for i in range(m, m + n):
            print(artists[i][:3])
        inp = int(input(
            "Enter 0 to end, Enter 1 to 5 to select, Enter 6 to go the previous page, Enter 7 to go the next page: "))
        if inp == 0:
            return
        if 1 <= inp <= n:
            if mode == 2:
                select_song(uid, artists[m + inp - 1][0])
                return
            if mode == 1:
                mode += 1
                aid = artists[m + inp - 1][0]
                c.execute(
                    'select s.sid, s.title, s.duration from songs s join perform p using (sid) where p.aid = :aid',
                    {'aid': aid})
                pack = c.fetchall()
                cnt_list = []
                for song in pack:
                    cnt_list.append([song[0], song[1], song[2]])
                artists = cnt_list
                m = 0
        if inp == 6:
            m -= 5
            m = max(0, m)
        elif inp == 7:
            m += 5
            m = min((len(artists) / 5) * 5, m)

    cnt_list.sort(key=lambda x: x[3], reverse=True)

    artists = cnt_list
    m = 0
    while True:
        n = min(5, len(artists) - m)
        for i in range(m, m + n):
            print(artists[i])
        inp = int(input(
            "Enter 0 to end, Enter 1 to 5 to select, Enter 6 to go the previous page, Enter 7 to go the next page"))
        if inp == 0:
            return
        if 1 <= inp <= n:
            if artists[m + inp - 1][3] == "song":
                select_artists(uid, artists[m + inp - 1][0])
                return
            if artists[m + inp - 1][3] == "artist":
                artists = []
                m = 0
        if inp == 6:
            m -= 5
            m = max(0, m)
        elif inp == 7:
            m += 5
            m = min((len(artists) / 5) * 5, m)

def end_session(sno, current_id):
    if sno is not None:
        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d')
        c.execute('update sessions set end =:date where sno =:sno and uid =:uid;',
                  {'date': date, 'sno': sno, 'uid': current_id})
    else:
        print('no starting session')


def artist_interface(current_id):
    '''
    display artist op, logout and exit options
    prompt for command, then execute it.
    :return:
    '''
    print("-> artist face")
    while True:
        op = input('enter 1 to add a song, enter 2 to find top fans and playlists, enter 0 to logout: ')
        if op == '0':
            return
        elif op == '1':
            add_song(current_id)
        elif op == '2':
            find_top(current_id)
        else:
            print('invalid command')


def add_song(current_id):
    '''
    add a song to the songs table, and add the relation to perform table
    add more relations to perform table if there is any co-artist
    :param current_id: current login aid
    :return:
    '''
    # get song info
    print('-> adding a song')
    title = input('enter song title: ')
    duration = input('enter duration: ')
    # check if there is a song with same title and duration
    script = 'select * from songs where title like "' + title + '" and duration = ' + str(duration) + ';'
    c.execute(script)
    ret = c.fetchone()
    # if yes, prompt a warning
    if ret:
        print('duplicate data detected')
        while True:
            warn = input('enter 1 to reject, enter 2 if you still want to add the song: ')
            if warn == '1':
                return
            elif warn == '2':
                break
            else:
                print('invalid command')

        # if no, assign the song an unique sid, and ask if there is any other co-artist

    # random sid
    c.execute('select sid from songs;')
    all_sid = c.fetchall()
    sid_lst = []
    for song in all_sid:
        sid_lst.append(song[0])
    while True:
        sid = random.sample(range(0, 5000), 1)[0]
        if sid not in sid_lst:
            break

    c.execute('insert into songs values (:sid, :title, :duration);',
              {'sid': sid, 'title': title, 'duration': duration})
    while True:
        have_co = input('any co-artist? y/n: ').lower()
        if have_co == 'y':
            co_num = int(input('enter the number of co-artists: '))
            for i in range(co_num):
                while True:
                    co_artist = input('enter the aid of artist ' + str(int(i) + 1) + ': ')
                    script = 'select aid from artists where aid like "' + co_artist + '";'
                    c.execute(script)
                    result = c.fetchone()
                    if not result:
                        print('invalid aid, try again')
                    else:
                        c.execute('insert into perform values (:aid, :sid);', {'aid': co_artist, 'sid': sid})
                        break
            break
        elif have_co == 'n':
            break
        else:
            print('invalid command')

    c.execute('insert into perform values (:aid, :sid);', {'aid': current_id, 'sid': sid})
    return


def find_top(current_id):
    # query the top 3 users who listen to their songs the longest time
    script = 'select u.uid, p.aid, sum(l.cnt) from users u join listen l using (uid) join perform p using (sid) group ' \
             'by uid having p.aid = "' + current_id + '" order by sum(l.cnt) desc limit 3; '
    c.execute(script)
    # list their uid and names
    ret = c.fetchall()
    print('your top 3 users are: ')
    for user in ret:
        c.execute('select * from users where uid =:uid;', {'uid':user[0]})
        get = c.fetchone()
        print(get)
    # query the top 3 playlists that include the largest number of their songs
    script = 'select p.aid, pl.pid, count(p.sid) from perform p join plinclude pl using (sid) group by pl.pid, ' \
             'p.aid having p.aid = "'+current_id+'" order by count(p.sid) desc limit 3; '
    c.execute(script)
    # list their pid, title, and uid
    ret = c.fetchall()
    print('your top 3 playlists are: ')
    for pl in ret:
        c.execute('select * from playlists where pid =:pid;', {'pid':pl[1]})
        get = c.fetchone()
        print(get)


if __name__ == '__main__':
    with open('prj-tables.txt', 'r') as infile:
        conn.executescript(infile.read())
    while True:
        print('-> This is the login screen')
        while True:
            input_id = input('enter your id to login, or enter 0 to quit: ')
            if len(input_id) == 4 or input_id == '0':
                break
            else:
                print('your id should in length 4')
        if input_id == '0':
            break

        login_type = id_check(input_id)
        if login_type == '-1':
            print('closing app')
            break
        elif login_type == '0':
            signup()
            break
        elif login_type == '3':
            # ask for specific login type
            login_type = input('enter 1 to login user account, enter 2 to longin artist account: ')

        user_type = login_type

        if user_type == '1' and check_pwd(user_type, input_id):
            user_interface(input_id)
        elif user_type == '2' and check_pwd(user_type, input_id):
            artist_interface(input_id)
    # end
    print('data saved')
    conn.commit()

