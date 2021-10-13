import requests

def func1(x):
    return 2*x

def check_shop_list(usr, ps):

    if usr.full():
        return "Ok"

    elif ps.qtd():
        return f"Comprar {ps.qtd()+2}"

    elif ps.qtd() < usr:
        return f"Comprar {usr.max_qtd - ps.qtd()}"
    else:
        return "Erro"
        
