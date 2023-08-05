from core.settings import PROJECT_ROOT_URL
import requests

def user_token_service(request) -> dict:
    # returns a token with 200 or a message why failed to receive token

    url = PROJECT_ROOT_URL + "api/token/"

    params = {
        "username": request.POST['username'].lower(), 
        "password": request.POST['password']
        }
    
    headers = {"Content-Type": "application/json"}

    r = requests.post(url=url, headers=headers, json=params)
    body = r.json()
    payload = {
        "status_code": r.status_code,
        "body": body
    }
    return payload

def authenticate_service(request) -> bool:
    # checks if access token is valid

    access_token = request.COOKIES.get("access")
    if not access_token:
        return False

    url = PROJECT_ROOT_URL + "api/verify/"

    params = {
        "token": access_token
    }
    headers = {"Content-Type": "application/json"}

    r = requests.post(url=url, headers=headers, json=params)
    if r.status_code != 200:
        return False

    return True

def book_list_service(request) -> dict:
    url = PROJECT_ROOT_URL + "api/books/"
    params = []
    page_number = request.GET.get("page_number")
    items_per_page = request.GET.get("items_per_page")

    if page_number is not None and page_number != "":
        try:
            param1 = f"page={page_number}"
            params.append(param1)
        except:
            param1 = None
    
    if items_per_page is not None and items_per_page != "":
        try:
            param2 = f"items_per_page={items_per_page}"
            params.append(param2)
        except:
            param2 = None
    
    if len(params) > 0:
        url += "?"
        joined_params = ("&").join(params)
        url += joined_params


    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {request.COOKIES.get('access')}"}
    
    payload = {
        'q': request.GET.get('q'),
        'date_from': request.GET.get('date-from'),
        'date_to': request.GET.get('date-to'),
    }

    r = requests.get(url=url, headers=headers, json=payload)
    body = r.json()
    print(body)
    payload = {
        "status_code": r.status_code,
        "body": body
    }
    #print(payload)
    
    return payload

def book_detail_service(request, id) -> dict:
    url = PROJECT_ROOT_URL + f"api/books/{id}"
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {request.COOKIES.get('access')}"}

    r = requests.get(url=url, headers=headers)
    
    body = r.json()

    payload = {
        "status_code": r.status_code,
        "body": body
    }
    #print(payload)
    
    return payload

def book_delete_service(request, id) -> dict:
    url = PROJECT_ROOT_URL + f"api/books/{id}"
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {request.COOKIES.get('access')}"}

    r = requests.delete(url=url, headers=headers)
    body = r.json()

    payload = {
        "status_code": r.status_code,
        "body": body
    }
    #print(payload)
    
    return payload

def book_create_service(request) -> dict:
    url = PROJECT_ROOT_URL + f"api/books/"
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {request.COOKIES.get('access')}"}
    
    payload = {
        'title': request.POST['title'],
        'description': request.POST['description'],
        'pubdate': request.POST['pubdate'],
        'pagecount': request.POST['pagecount'],
        'author': request.POST['author']
    }

    r = requests.post(url=url, headers=headers, json=payload)
    body = r.json()

    payload = {
        "status_code": r.status_code,
        "body": body
    }
    
    return payload

def book_edit_service(request, id) -> dict:
    url = PROJECT_ROOT_URL + f"api/books/{id}/"
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {request.COOKIES.get('access')}"}
    
    payload = {
        'title': request.POST['title'],
        'description': request.POST['description'],
        'pubdate': request.POST['pubdate'],
        'pagecount': request.POST['pagecount'],
        'author': request.POST['author']
    }

    r = requests.put(url=url, headers=headers, json=payload)
    body = r.json()

    payload = {
        "status_code": r.status_code,
        "body": body
    }
    
    return payload

def book_patch_service(request, id) -> dict:
    url = PROJECT_ROOT_URL + f"api/books/{id}/"
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {request.COOKIES.get('access')}"}
    
    payload = {
        'title': request.POST['title'],
        'author': request.POST['author']
    }

    r = requests.patch(url=url, headers=headers, json=payload)
    body = r.json()

    payload = {
        "status_code": r.status_code,
        "body": body
    }
    
    return payload