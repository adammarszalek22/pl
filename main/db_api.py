import requests
import json

url = "http://127.0.0.1:5000"

def create_user(username, password):
    user = requests.post(url + '/register', json={"username": username, "password": password})
    return json.loads(user.text)

def login(username, password):
    request = requests.post(url + '/login', json={"username": username, "password": password})
    try:
        access_token = json.loads(request.text)["access_token"]
        refresh_token = json.loads(request.text)["refresh_token"]
        user_id = json.loads(request.text)["user_id"]
        return [access_token, refresh_token, user_id]
    except KeyError:
        return json.loads(request.text)["message"]

def revoke_jwt(username, password):
    user = requests.post(url + '/logout', json={"username": username, "password": password})
    return json.loads(user.text)

def get_non_fresh_token(refresh_token, username, password):
    request = requests.post(url + '/refresh', headers={"Authorization": "Bearer " + refresh_token},
                         json={"username": username, "password": password})
    new_access_token = json.loads(request.text)["access_token"]
    return new_access_token

def my_user_info(access_token, id):
    user = requests.get(url + '/user/' + str(id), headers={"Authorization": "Bearer " + access_token})
    return json.loads(user.text)

def get_all_users(access_token):
    users = requests.get(url + '/get_all', headers={"Authorization": "Bearer " + access_token})
    return json.loads(users.text)

def delete_account(access_token, id):
    delete = requests.delete(url + "/user/" + str(id), headers={"Authorization": "Bearer " + access_token})
    return json.loads(delete.text)

def get_all_bets(access_token):
    bets = requests.get(url + '/bet', headers={"Authorization": "Bearer " + access_token})
    return json.loads(bets.text)

def get_bet(access_token, id):
    bet = requests.get(url + '/bet/' + str(id), headers={"Authorization": "Bearer " + access_token})
    return json.loads(bet.text)

def update_bet(access_token, match_id, goal1, goal2, user_id):
    new_bet = requests.put(url + '/bet',
                           headers={"Authorization": "Bearer " + access_token},
                           json={"match_id": match_id, "goal1": goal1,
                                 "goal2": goal2, "user_id": user_id})
    return json.loads(new_bet.text)

def delete_bet(access_token, id):
    bet = requests.delete(url + '/bet/' + str(id), headers={"Authorization": "Bearer " + access_token})
    return json.loads(bet.text)

def post_bet(access_token, match_id, goal1, goal2, user_id):
    bet = requests.post(url + '/bet', headers={"Authorization": "Bearer " + access_token},
                        json={"match_id": match_id, "goal1": goal1, "goal2": goal2, "user_id": user_id})
    return bet

#a = login("adam", "1234")[0]
#post_bet(a, "2293058", 3, 4, 1)