import random

# Daftar User-Agent template tanpa bot, termasuk perangkat yang diperbarui
user_agents = [
    # Realme Android
    "Mozilla/5.0 (Linux; Android {android_version}; Realme {device_name} Build/{build}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.{build}.0 Mobile Safari/537.36",
    
    # Vivo Android
    "Mozilla/5.0 (Linux; Android {android_version}; Vivo {device_name} Build/{build}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.{build}.0 Mobile Safari/537.36",
    
    # Xiaomi Android
    "Mozilla/5.0 (Linux; Android {android_version}; Xiaomi {device_name} Build/{build}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.{build}.0 Mobile Safari/537.36",
    
    # Samsung Android
    "Mozilla/5.0 (Linux; Android {android_version}; Samsung {device_name} Build/{build}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.{build}.0 Mobile Safari/537.36",
    
    # iPhone iOS
    "Mozilla/5.0 (iPhone; CPU iPhone OS {ios_version} like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/{version}.0 Mobile/15E148 Safari/537.36",
    
    # Lenovo Laptop (Windows)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.{build}.0 Safari/537.36 Lenovo/{device_name}",
    
    # Asus Laptop (Windows)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.{build}.0 Safari/537.36 Asus/{device_name}",
]

# Daftar perangkat Android dan iOS
android_devices = ["Realme GT", "Vivo V21", "Xiaomi Mi 11", "Samsung Galaxy S21", "Realme X50", "Vivo Y20", "Xiaomi Redmi Note 10"]
ios_devices = ["iPhone 13", "iPhone 14", "iPhone 15", "iPhone SE 3", "iPhone 12"]
laptop_devices = ["ThinkPad X1", "ZenBook", "Yoga 9i", "Legion 5", "Acer Swift 3"]

# Fungsi untuk menghasilkan User-Agent acak
def generate_user_agents(count):
    user_agent_set = set()  # Menggunakan set untuk menghindari duplikasi
    while len(user_agent_set) < count:
        ua_template = random.choice(user_agents)
        version = random.randint(90, 130)  # Simulasikan versi browser
        build = random.randint(1000, 1500)  # Simulasikan build
        android_version = random.randint(10, 15)  # Simulasikan versi Android
        ios_version = random.randint(10, 16)  # Simulasikan versi iOS
        device_name = random.choice(android_devices + ios_devices + laptop_devices)  # Pilih perangkat Android/iOS/laptop secara acak

        # Pilih template sesuai kondisi dan sesuaikan format
        if "Android" in ua_template:
            user_agent = ua_template.format(version=version, build=build, android_version=android_version, device_name=device_name)
        elif "iPhone" in ua_template:
            user_agent = ua_template.format(version=version, ios_version=ios_version)
        elif "Windows" in ua_template:
            user_agent = ua_template.format(version=version, build=build, device_name=device_name)
        
        user_agent_set.add(user_agent)  # Menambahkan User-Agent ke dalam set (duplikasi akan dihindari)
    
    return list(user_agent_set)

# Menyimpan User-Agent ke file txt
user_agents = generate_user_agents(500000)
with open("ua.txt", "w") as file:
    file.write("\n".join(user_agents))

print("File ua.txt berhasil dibuat.")
