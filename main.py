import sqlite3
import time
import asyncio
from datetime import datetime

con = sqlite3.connect("Projects\Banka\db\Banka.db")
cursor = con.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS kullanici_tablosu (ad VARCHAR(50), parola INT, para MONEY, acildiği_tarih REAL)")

async def wait():
    print("İşlem gerçekleştiriliyor..")
    return "İşlem gerçekleştirildi"

async def loginAccount():
    bekleme = asyncio.create_task(wait())
    login_status = 0
    while login_status < 1:
        try:
            cursor.execute(f"SELECT * FROM kullanici_tablosu WHERE ad = '{loginName}' AND parola = {loginPass} ")
            global veri
            veri = cursor.fetchall()
            if len(veri) != 0:
                login_status = 1
                await asyncio.sleep(1)
                sonuc = await bekleme
                print(sonuc)
                inAccount()
            else:
                login_status = 0
                print("Giriş başarısız")
                loginRepName = input("Kullanıcı isminizi yeniden giriniz --> ")
                durum = 0
                while durum < 1:
                    try:
                        loginRepPass = int(input("6 Haneli şifrenizi yeniden giriniz --> "))
                        if len(str(loginPass)) ==6:
                            durum = 1
                        else:
                            print("Lütfen 6 haneli şifre giriniz.")
                            durum = 0
                    except ValueError:
                        print("Şifre rakamlardan(0-1-2-3-4-5-6-7-8-9) oluşmalıdır.")
                        durum = 0
                cursor.execute(f"SELECT * FROM kullanici_tablosu WHERE ad = '{loginRepName}' AND parola = {loginRepPass} ")
                veri = cursor.fetchall()
                await asyncio.sleep(1)
                sonuc = await bekleme
                print(sonuc)
                inAccount()
                login_status = 1
        except IndexError:
            pass

async def signUp():
    bekleme = asyncio.create_task(wait())
    durum_kullanıcı = 0
    global signName
    while durum_kullanıcı < 1:
        signName = input("Seçtiğiniz kullanıcı isminizi giriniz ( 50 Karakterden az olmalıdır. ) --> ")
        if len(signName) > 50:
            print("Kullanıcı isminiz 50 karakterden uzundur lütfen daha kısa bir isim seçiniz.")
            durum_kullanıcı = 0
        else: 
            print("Kullanıcı isminiz uygundur.")
            durum_kullanıcı = 1
    print("------------")
    durum = 0
    global signPass
    while durum < 1:
        try:
            signPass = int(input("Seçtiğiniz 6 haneli şifrenizi giriniz --> "))
            if len(str(signPass)) == 6:
                durum = 1
            else:
                print("Lütfen 6 haneli şifre giriniz.")
                durum = 0
        except ValueError:
            print("Şifre rakamlardan(0-1-2-3-4-5-6-7-8-9) oluşmalıdır.")
            durum = 0
    print("------------")
    zaman = time.time()
    tarih = str(datetime.fromtimestamp(zaman).strftime('%Y-%m-%d %H:%M:%S'))
    para = 0

    cursor.execute("INSERT INTO kullanici_tablosu (ad, parola, para, acildiği_tarih) VALUES(?,?,?,?)",(signName,signPass,para,tarih))
    con.commit()

def inAccount():
    personal_data = {
            "kullanıcı_ismi" : veri[0][0],
            "sifre" : veri[0][1],
            "para" : veri[0][2],
            "hesap_kurulus_tarihi" : veri[0][3]
        }
    kontrol = 0
    global güncel_para
    güncel_para = personal_data["para"]
    newPass = personal_data["sifre"]
    while kontrol != 1:
        print(f"{personal_data['kullanıcı_ismi']}, banka hesabınıza hoş geldiniz")
        print("------------")
        print(f"Hesap bilgileriniz : \n1- Kullanıcı İsmi = {personal_data['kullanıcı_ismi']} \n2- Mevcut Bakiyeniz = {güncel_para}TL \n3- Şifreniz = {newPass} \n4- Hesap Kuruluş Tarihi = {personal_data['hesap_kurulus_tarihi']}")
        print("------------")
        hesap_islemi = input("Yapmak istediğiniz işlemi lütfen seçiniz. \n1- Para Yükle \n2- Para Çek \n3- Şifreyi değiştir \n4- Güvenli Çıkış \n----------------------\nSeçilen İşlem : ")
        print("------------")
        if hesap_islemi == "1":
            yüklenececek_para = float(input("Yüklemek istediğiniz para miktarını giriniz : "))
            güncel_para = personal_data["para"]+yüklenececek_para
            cursor.execute(f"UPDATE kullanici_tablosu SET para = {güncel_para} WHERE ad = '{personal_data['kullanıcı_ismi']}' AND parola = {personal_data['sifre']} AND para = {personal_data['para']}")
            con.commit()
        
        elif hesap_islemi == "2":
            çekilecek_para = float(input("Çekmek istediğiniz para miktarını giriniz : "))
            güncel_para = personal_data["para"]- çekilecek_para
            cursor.execute(f"UPDATE kullanici_tablosu SET para = {güncel_para} WHERE ad = '{personal_data['kullanıcı_ismi']}' AND parola = {personal_data['sifre']} AND para = {personal_data['para']}")
            con.commit()
        
        elif hesap_islemi == "3":
            durum = 0
            while durum < 1:
                try:
                    newPass = int(input("Seçtiğiniz yeni 6 haneli şifrenizi giriniz --> "))
                    if len(str(newPass)) == 6:
                        durum = 1
                    else:
                        print("Lütfen 6 haneli şifre giriniz.")
                        durum = 0
                except ValueError:
                    print("Şifre rakamlardan(0-1-2-3-4-5-6-7-8-9) oluşmalıdır.")
                    durum = 0
            cursor.execute(f"UPDATE kullanici_tablosu SET parola = {newPass} WHERE ad = '{personal_data['kullanıcı_ismi']}' AND parola = {personal_data['sifre']} ")
            con.commit()

        elif hesap_islemi == "4":
            kontrol = 1
            print("Çıkış işlemi gerçekleştiriliyor...")

print("Efeisky Bankasına hoş geldiniz. Yapmak istediğiniz işlemi lütfen seçiniz.")
yapılacak_islem = input("----------------------\n1- Banka Hesabına giriş yap \n2- Yeni bir hesap oluştur \n3- Çıkış yap \n----------------------\nSeçilen İşlem : ")


if yapılacak_islem == "1":
    print("Banka Hesabına giriş yapmak istediğinizi belirttiniz.")
    loginName = input("Kullanıcı isminizi giriniz --> ")
    durum = 0
    while durum < 1:
        try:
            loginPass = int(input("6 Haneli şifrenizi giriniz --> "))
            if len(str(loginPass)) ==6:
                durum = 1
            else:
                print("Lütfen 6 haneli şifre giriniz.")
                durum = 0
        except ValueError:
            print("Şifre rakamlardan(0-1-2-3-4-5-6-7-8-9) oluşmalıdır.")
            durum = 0
    print("------------")
    asyncio.run(loginAccount())
    print("------------")

elif yapılacak_islem == "2":
    print("Yeni bir hesap oluşturmak istediğinizi belirttiniz.")
    print("------------")
    asyncio.run(signUp())
    loginName = signName
    loginPass = signPass
    asyncio.run(loginAccount())

elif yapılacak_islem == "3":
    print("Çıkış işlemi gerçekleştiriliyor...")

con.close()