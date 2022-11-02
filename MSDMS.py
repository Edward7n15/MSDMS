import sqlite3
import uuid

# creating connection from host language to sqlite3
conn = sqlite3.connect('./MSDMS')
c = conn.cursor()

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

def id_check(input_id):
    '''
    check if an id is legal. If yes, determine it is a uid or an aid. If no, prompt for a uid register.
    :param: (str)input id
    :return: (int) 1: user 2:artist 3.both -1: exit
    '''
    user = False
    artist = False
    c.execute('select uid from users where uid=:input_id', {'input_id': input_id})
    row_u = c.fetchone()
    if row_u:
        user = True
    c.execute('select aid from artists where aid=:input_id;', {'input_id': input_id})
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
            signup()
        elif choice == '0':
            quit()


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
    print(id_list)
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
    c.execute('insert into users values (:uid, :name, :pwd);', {'uid':uid, 'name':name, 'pwd': pwd})
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
        c.execute('select pwd from users where uid =:id;', {'id':input_id})
        row = c.fetchone()

    elif login_type == '2':
        c.execute('select pwd from artists where aid =:id;', {'id':input_id})
        row = c.fetchone()

    if row and pwd == row[0]:
        return True
    else:
        return False

def user_interface(current_id):
    '''
    display user op, logout and exit options
    prompt for command, then execute it.
    :return:
    '''
    print("-> user face")
    while True:
        op = input('enter 1 to start a session, enter 2 to search for songs and playlists, enter 3 to search for '
                   'artists enter 4 to end the session, enter 0 to quit: ')
        if op == '1':
            start_session()
        elif op == '2':
            search_songs()
        elif op == '3':
            search_artists()
        elif op == '0':
            quit()
        else:
            print('invalid command')

def start_session():
    pass

def search_songs():
    pass

def select_song():
    pass

def search_artists():
    pass

def end_session():
    pass

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
            quit()
        elif op == '1':
            add_song(current_id)
        elif op == '2':
            find_top()
        else:
            print('invalid command')

def add_song(current_id):
    # get song info
    print('-> adding songs')
    title = input('enter song title: ')
    duration = input('enter duration: ')
    # check if there is a song with same title and duration
    c.execute('select * from songs where title =:title and duration =:duration;', {'title':title, 'duration':duration})
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
    sid = str(uuid.uuid4())
    c.execute('insert into songs values (:sid, :title, :duration);',
              {'sid': sid, 'title': title, 'duration': duration})
    while True:
        have_co = input('any co-artist? y/n: ').lower()
        if  have_co == 'y':
            co_num = input('enter the number of co-artists: ')
            for i in range(co_num):
                while True:
                    co_artist = input('enter the aid of artist ' + (i + 1) + ': ')
                    c.execute('select aid from artists where aid =:aid;', {'aid': co_artist})
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

    c.execute('select * from songs;')
    get = c.fetchall()
    print('all songs:')
    print(get)
    return

def find_top():
    pass

if __name__ == '__main__':
    with open('prj-tables.txt', 'r') as infile:
        conn.executescript(infile.read())
    while True:
        print('-> This is the login screen')
        input_id = input('enter your id: ')
        user_type = login(input_id)
        if user_type == '1':
            user_interface(input_id)
        elif user_type == '2':
            artist_interface(input_id)



    '''    
    # end
    conn.commit()
    '''
