import sqlite3
# creating connection from host language to sqlite3
conn = sqlite3.connect('./MSDMS')
c = conn.cursor()

def login():
    '''
    The login screen, ask for id and password, could determine users and artists, allow new users to register.
    After signup, goto corresponding system.
    NOT providing logout option, it is in the inner interface AFTER login
    :return:(int)login_type: 1 (user), 2 (artist)
    '''
    print('This is the login screen:')
    print('enter your id:')
    id = input()
    login_type = id_check(id)
    if login_type == -1 or check_pwd(id, login_type) == False:
        exit()
    elif login_type == 3:
        # ask for specific login type
        pass
    return login_type

def id_check(id):
    '''
    check if an id is legal. If yes, determine it is a uid or an aid. If no, prompt for a uid register.
    :param: (str)input id
    :return: (int) 1: user 2:artist 3.both -1: exit
    '''
    pass

def exit():
    pass

def check_pwd(id, login_type):
    '''
    goto user's or artist's db depend on login type
    prompt for password, then check if it matches the id
    ask for another try or quit when the not matching
    :param id: input id
    :param login_type: id type
    :return: (bool) true: valid, false: quit
    '''
    pass

def user_interface():
    '''
    display user op, logout and exit options
    prompt for command, then execute it.
    :return:
    '''
    pass

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

def artist_interface():
    '''
    display artist op, logout and exit options
    prompt for command, then execute it.
    :return:
    '''
    pass

def add_song():
    pass

def find_top():
    pass

if __name__ == '__main__':
    if login() == 1:
        user_interface()
    else
        artist_interface()



    '''    
    # end
    conn.commit()
    '''
