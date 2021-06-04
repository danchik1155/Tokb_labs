from chek_time import message


def read_messages():
    try:
        f = open('messages.txt', 'r')
        st = dict(eval(f.readline().rstrip()))
        f.close()
        return st
    except FileNotFoundError:
        if_file_error_msg()
    except ValueError:
        if_file_error_msg()
    except SyntaxError:
        if_file_error_msg()
    return {}


def if_file_error_msg():
    f = open('messages.txt', 'w')
    users_msg = {}
    f.write(str(users_msg))
    f.close()


def write_messages(msges):
    f = open('messages.txt', 'w')
    f.write(str(msges))
    f.close()


#def write_message(user)