import requests
import json

#url = "http://127.0.0.1:5000"
url = "https://pl-server.onrender.com"

'''
USER
'''

def create_user(username, password, password2):
    user = requests.post(url + '/register', 
                         json={"username": username,
                               "password": password,
                               "password2": password2})
    return {"status_code": user.status_code, **json.loads(user.text)}

# for i in range(3cd00, 1000):
#     create_user('test' + str(i), '1', '1')

def login(username, password):
    request = requests.post(url + '/login', 
                            json={"username": username, "password": password})
    return {"status_code": request.status_code, **json.loads(request.text)}

def get_all_users(access_token):
    users = requests.get(url + '/get_all',
                         headers={"Authorization": "Bearer " + access_token})
    return {"status_code": users.status_code, "users": json.loads(users.text)}

# print(login("adam", "1234"))
# print(get_all_users(login('adam', '1234')["access_token"]))

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

def user_info_by_pos(access_token, league_pos):
    user = requests.get(url + '/user_pos',
                        headers={"Authorization": "Bearer " + access_token},
                        json={"position": league_pos})
    return json.loads(user.text)

def first_ten(access_token):
    user = requests.get(url + '/first-ten',
                        headers={"Authorization": "Bearer " + access_token})
    return json.loads(user.text)

def get_by_username(access_token, username):
    user = requests.get(
        url + '/user',
        headers={"Authorization": "Bearer " + access_token},
        json={"username": username}
        )
    return {"status_code": user.status_code, **json.loads(user.text)}

def delete_account(access_token):
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

def post_bet(access_token, match_id, goal1, goal2):
    bet = requests.post(url + '/bet',
                        headers={"Authorization": "Bearer " + access_token},
                        json={"match_id": match_id,
                              "goal1": goal1,
                              "goal2": goal2,
                              "done": "no"})
    if bet.status_code == 405:
        return {"status_code": 405}
    elif bet.status_code == 500:
        return {"status_code": 500}
    else:
        return {"status_code": 200, **json.loads(bet.text)}

def update_bet(access_token, match_id, goal1, goal2):
    new_bet = requests.put(
        url + '/bet',
        headers={"Authorization": "Bearer " + access_token},
        json={
            "match_id": match_id,
            "goal1": goal1,
            "goal2": goal2,
            "done": "no"
            }
        )
    if new_bet.status_code == 405:
        return {"status_code": 405}
    else:
        return {"status_code": 200, **json.loads(new_bet.text)}

def update_multiple_bets(access_token, list_match_id, list_goal1, list_goal2):
    new_bets = requests.put(
        url + '/multiple_bets_update',
        headers={"Authorization": "Bearer " + access_token},
        json={
            "match_id": list_match_id,
            "goal1": list_goal1,
            "goal2": list_goal2
            }
        )
    # if new_bets.status_code == 405:
    #     return {"status_code": 405}
    # else:
    #     return {"status_code": 200, **json.loads(new_bets.text)}
    return {"status_code": new_bets.status_code, **json.loads(new_bets.text)}

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
    return {"status_code": groups.status_code, "list": json.loads(groups.text)}

