
import requests

def login( url , email , password) -> str:
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(url+'/user/login/', data=data)
    if response.status_code == 200:
        
        return response.json() 
    else:
        return None

def get_products(url) -> list:
    data = requests.get(url+'/product/products/').json()
    return data

def get_buskets(url, email) -> list:
    data = requests.get(url+f'/user/users/?search={email}').json()
    if data:
        return data[0]['buskets']
    else:
        return None

def get_categories(url) -> list:
    data = requests.get(url+'/category/category/')
    if data.status_code == 200:
        return data.json()
    else:
        return None


def get_products_by_category(url , category):
    data = requests.get(url+f'/product/products/?search={category}')
    if data.status_code == 200:
        return data.json()
    else:
        return None


