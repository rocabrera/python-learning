import requests

def func1(x):
    return 2*x

def check_shop_list(usr, ps):

    if usr.full():
        return "Ok"

    elif ps.qtd() < 2:
        return "Buy"
