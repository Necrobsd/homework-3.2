import time, json
try:
    import vk_requests
except:
    import sys, subprocess, os

    pip_path = os.path.join(sys.base_prefix, 'Scripts', 'pip')
    subprocess.run('{} install vk-requests'.format(pip_path))
    import vk_requests


api = vk_requests.create_api(app_id=5862361, interactive=True, scope='friends')
my_friends = api.friends.get(fields = 'first_name, last_name')['items']

friends_of_friends = {} # Словарь "друзья друзей" с ФИО
friend_name_by_id = {}  # Словарь соответствия ID и ФИО

#Заполням словарь с друзьями друзей
for friend in my_friends:
    time.sleep(0.3) # Задержка при обращении к API (3 запроса в секунду)
    try:
        friend_name_by_id[friend['id']] = '{} {}'.format(friend['first_name'], friend['last_name'])
        friends_of_friends[friend['id']] = api.friends.get(user_id = friend['id'], fields = 'first_name, last_name')['items']
    except:
        continue

for user, his_friends in friends_of_friends.items():
    for friend in his_friends:
        friend_name_by_id[friend['id']] = '{} {}'.format(friend['first_name'], friend['last_name'])

common_friends = {}

# Удаляем из словаря с друзьями лишние данные, и оставляем только их ID
for user, friends in friends_of_friends.items():
    friends_of_friends[user] = [friend['id'] for friend in friends]

found_pairs = [] # Найденые пары, чтобы не искать повторно

for user1, friends1 in friends_of_friends.items():
    for user2, friends2 in friends_of_friends.items():
        if user1 is not user2 and {user1, user2} not in found_pairs:
            found_pairs.append({user1, user2})
            common = list(set(friends1) & set(friends2))
            if len(common) > 1: # Если общий друг не только я
                common = [friend_name_by_id[int(user)] for user in common]
                common_friends['{} и {}'.format(friend_name_by_id[int(user1)], friend_name_by_id[int(user2)])] = common
print('Результаты сохранены в файле "common_friends.json"')
with open('common_friends.json', 'w', encoding='utf8') as f:
    json.dump(common_friends, f, indent=True, ensure_ascii=False)
