from os import system, name
import sys
import sqlite3
from datetime import date
# creating connection from host language to sqlite3
conn = sqlite3.connect('./MSDMS')
c = conn.cursor()
uids = []
aids = []
def login():
    '''
    The login screen, ask for id and password, could determine users and artists, allow new users to register.
    After signup, goto corresponding system.
    NOT providing logout option, it is in the inner interface AFTER login
    :return:(int)login_type: 1 (user), 2 (artist)
    '''
    uid = input("User ID:")
    if uid not in uids and uid not in aids:
        signup()
        return
    mode = ""
    if uid in uids and uid in aids:
        mode = input("Do you want to login in as user or artist(enter 1 for user, 2 for artist:")
    if mode == "1" or (uid in uids and uid not in aids):
        pwd = input("password")
        if pwd == checkuserpwd(uid, pwd):
            start_session(uid)
        else:
            signup()
            return
    if mode == "2" or (uid not in uids and uid in aids):
        pwd = input("password")
        if pwd == checkartpwd(uid, pwd):
            artist_interface(uid)
        else:
            signup()
            return

def signup():
    inp = input("Do you want to sign up?\n(type 'Y' or 'y' for Yes, other input would be consider as No)\n ")
    exit(inp)
    clear()
    if (inp.lower == "y"):
        while True:
            uid  = input("Enter your user ID:         ")
            exit(uid)
            pwd = input("Enter your password:        ")
            exit(pwd)
            insertid(uid, pwd)
            login()
            return
    else:
        login()
        return
    

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def id_check(id):
    '''
    check if an id is legal. If yes, determine it is a uid or an aid. If no, prompt for a uid register.
    :param: (str)input id
    :return: (int) 1: user 2:artist 3.both -1: exit
    '''
    pass
def exit(inp):
    if inp == "exit":
        conn.commit()
        sys.exit()

def checkuserpwd(id, pwd):
    '''
    goto user's or artist's db depend on login type
    prompt for password, then check if it matches the id
    ask for another try or quit when the not matching
    :param id: input id
    :param login_type: id type
    :return: (bool) true: valid, false: quit
    '''
    pass

def checkartpwd(id, pwd):
    '''
    goto user's or artist's db depend on login type
    prompt for password, then check if it matches the id
    ask for another try or quit when the not matching
    :param id: input id
    :param login_type: id type
    :return: (bool) true: valid, false: quit
    '''
    pass

def user_interface(uid):
    '''
    display user op, logout and exit options
    prompt for command, then execute it.
    :return:
    '''
    inp = input("Enter 1 to search for songs and playlists, Enter 2 to search for artists, Enter 3 to end the session")
    if inp == "1":
        kw = input("Input the keywords: ").split()
        search_songs(kw)
    if inp == "2":
        kw = input("Input the keywords: ").split()
        search_artists(kw)
    if inp == "3":
        end_session(uid)
        return
    pass

def start_session(uid):
    pass

def search_songs(kw):
    songs = []
    while True:
        inp = int(input("Enter 0 to end, Enter 1 to 5 to select the songs, Enter 6 to go the next page"))
        if inp == 0:
            user_interface()
            return
        if 1 <= inp and inp >= 5:
            song_actions(songs[inp])
            return
        if inp == 6:
            songs = songs[5:]
    pass

def select_song():
    pass

def search_artists():
    pass

def end_session(uid):
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
