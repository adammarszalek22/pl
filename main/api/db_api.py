import requests
import json

url = "http://127.0.0.1:5000"
#url = "https://pl-server.onrender.com"

'''
USER
'''

def create_user(username, password):
    user = requests.post(url + '/register', 
                         json={"username": username, "password": password})
    return json.loads(user.text)

def login(username, password):
    request = requests.post(url + '/login', 
                            json={"username": username, "password": password})
    try:
        access_token = json.loads(request.text)["access_token"]
        refresh_token = json.loads(request.text)["refresh_token"]
        user_id = json.loads(request.text)["user_id"]
        return [access_token, refresh_token, user_id]
    except KeyError:
        return json.loads(request.text)["message"]
    
# def update(access_token, user_id, points, position, three_pointers, one_pointers):
#     request = requests.update(url + f"/update/{user_id}",
#                               headers = {"Authorization": "Bearer " + access_token},
#                               json = {
#                                 "points": points,
#                                 "position": position,
#                                 "three_pointes": three_pointers,
#                                 "one_pointers": one_pointers
#                               })
#     return json.loads(request.text)

def get_all_users(access_token):
    users = requests.get(url + '/get_all',
                         headers={"Authorization": "Bearer " + access_token})
    return json.loads(users.text)

def get_non_fresh_token(refresh_token, username, password):
    request = requests.post(url + '/refresh',
                            headers={"Authorization": "Bearer " + refresh_token},
                            json={"username": username, "password": password})
    new_access_token = json.loads(request.text)["access_token"]
    return new_access_token

def revoke_jwt(access_token):
    user = requests.post(url + '/logout',
                         headers={"Authorization": "Bearer " + access_token})
    return json.loads(user.text)

def my_user_info(access_token, id):
    user = requests.get(url + '/user/' + str(id),
                        headers={"Authorization": "Bearer " + access_token})
    return json.loads(user.text)

def delete_account(access_token, id):
    delete = requests.delete(url + "/delete",
                             headers={"Authorization": "Bearer " + access_token})
    return json.loads(delete.text)

'''
BETS
'''

def get_bet(access_token, id):
    bet = requests.get(url + '/bet/' + str(id),
                       headers={"Authorization": "Bearer " + access_token})
    return json.loads(bet.text)

def delete_bet(access_token, id):
    bet = requests.delete(url + '/bet/' + str(id),
                          headers={"Authorization": "Bearer " + access_token})
    return json.loads(bet.text)

def delete_all_bets(access_token, id):
    bet = requests.delete(url + '/bet',
                          headers={"Authorization": "Bearer " + access_token})
    return json.loads(bet.text)

def get_all_bets(access_token):
    try:
        bets = requests.get(url + '/bet',
                            headers={"Authorization": "Bearer " + access_token})
        return {"status_code": 200, "list": json.loads(bets.text)}
    except json.decoder.JSONDecodeError:
        return {"status_code": 500}

def get_all_bets_by_user_id(access_token):
    try:
        bets = requests.get(url + '/bet_by_user_id',
                            headers={"Authorization": "Bearer " + access_token})
        return {"status_code": 200, "list": json.loads(bets.text)}
    except json.decoder.JSONDecodeError:
        return {"status_code": 500}

def post_bet(access_token, match_id, goal1, goal2, user_id):
    bet = requests.post(url + '/bet',
                        headers={"Authorization": "Bearer " + access_token},
                        json={"match_id": match_id,
                              "goal1": goal1,
                              "goal2": goal2,
                              "user_id": user_id,
                              "done": "no"})
    return bet

def update_bet(access_token, match_id, goal1, goal2, user_id):
    new_bet = requests.put(
        url + '/bet',
        headers={"Authorization": "Bearer " + access_token},
        json={
            "match_id": match_id,
            "goal1": goal1,
            "goal2": goal2,
            "user_id": user_id,
            "done": "no"
            }
        )
    return json.loads(new_bet.text)

def update_multiple_bets(access_token, list_match_id, list_goal1, list_goal2, user_id):
    new_bets = requests.put(
        url + '/multiple_bets_update',
        headers={"Authorization": "Bearer " + access_token},
        json={
            "match_id": list_match_id,
            "goal1": list_goal1,
            "goal2": list_goal2,
            "user_id": user_id
            }
        )
    return json.loads(new_bets.text)

#a = login("adam", "1234")[0]
#post_bet(a, "2293058", 3, 4, 1)

'''
GROUPS
'''

def get_all_groups(access_token):
    groups = requests.get(
        url + '/all_groups',
        headers={"Authorization": "Bearer " + access_token}
    )
    return json.loads(groups.text)

def delete_all_groups(access_token, username, password):
    delete = requests.delete(
        url + '/all_groups',
        headers={"Authorization": "Bearer " + access_token},
        json={"username": username,
              "password": password}
    )
    return json.loads(delete.text)

def get_group_by_id(access_token, id):
    group = requests.get(
        url + '/groups',
        headers={"Authorization": "Bearer " + access_token},
        json={"id": id}
    )
    return json.loads(group.text)

def create_group(access_token, name):
    newgroup = requests.post(
        url + '/groups',
        headers={"Authorization": "Bearer " + access_token},
        json={"name": name}
    )
    return json.loads(newgroup.text)

def join_group(access_token, id):
    group = requests.put(
        url + '/groups',
        headers={"Authorization": "Bearer " + access_token},
        json={"id": id}
    )
    if group.status_code == 200: 
        return {"status_code": 200, **json.loads(group.text)}
    elif group.status_code == 409:
        return {"status_code": 409}

def delete_group(access_token, id):
    delete_group = requests.delete(
        url + '/groups',
        headers={"Authorization": "Bearer " + access_token},
        json={"id": id}
    )
    return json.loads(delete_group.text)

def delete_user_from_group(access_token, id, user_id):
    delete_user = requests.delete(
        url + '/groups_users',
        headers={"Authorization": "Bearer " + access_token},
        json={"id": id,
              "user_id": user_id}
    )
    return json.loads(delete_user.text)

def my_groups(access_token):
    groups = requests.get(
        url + '/my_groups',
        headers={"Authorization": "Bearer " + access_token}
        )
    return {"status_code": groups.status_code, "list": json.loads(groups.text)}

def groups_im_in(access_token):
    groups = requests.get(
        url + '/groups_im_in',
        headers={"Authorization": "Bearer " + access_token}
        )
    return {"status_code": groups.status_code, **json.loads(groups.text)}