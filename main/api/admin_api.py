import requests
import json

'''
THIS FILE WON'T BE INCLUDED IN THE APP
'''

url = "http://127.0.0.1:5000"
#url = "https://pl-server.onrender.com"

'''
USER
'''

def login(username, password):
    request = requests.post(
        url + '/admin/login', 
        json={"username": username, "password": password}
        )
    return {"code": request.status_code, **json.loads(request.text)}

def update(access_token, user_id, points, three_pointers, one_pointers):
    request = requests.put(
        url + '/admin/update',
        headers = {"Authorization": "Bearer " + access_token},
        json = {
            "user_id": user_id,
            "points": points,
            "three_pointers": three_pointers,
            "one_pointers": one_pointers
            }
            )
    return json.loads(request.text)

access_token = login("adam1234", "SIGNUP77//88")["access_token"]
#print(update(access_token, 1, -5, 0, 0))

def delete_user(access_token, user_id):
    request = requests.delete(
        url + '/admin/delete',
        headers={"Authorization": "Bearer " + access_token},
        json={"user_id": user_id}
        )
    return {"code": request.status_code, **json.loads(request.text)}

print(delete_user(access_token, 14))