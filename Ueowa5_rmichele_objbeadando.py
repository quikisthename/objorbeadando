from datetime import datetime


class Szoba:
    def __init__(szálloda, szobaszam, ar):
        szálloda.szobaszam = szobaszam
        szálloda.ar = ar


class EgyagyasSzoba(Szoba):
    def __init__(szálloda, szobaszam, ar):
        super().__init__(szobaszam, ar)


class KetagyasSzoba(Szoba):
    def __init__(szálloda, szobaszam, ar):
        super().__init__(szobaszam, ar)


class Foglalás:
    def __init__(szálloda, szoba, datum):
        szálloda.szoba = szoba
        szálloda.datum = datum


class Szalloda:
    def __init__(szálloda, nev, egyagyas_ar, ketagyas_ar):
        szálloda.nev = nev
        szálloda.egyagyas_ar = egyagyas_ar
        szálloda.ketagyas_ar = ketagyas_ar
        szálloda.szobak = []
        szálloda.foglalasok = []

    def foglalás(szálloda, szobaszam, datum):
        for foglalás in szálloda.foglalasok:
            if foglalás.szoba.szobaszam == szobaszam and foglalás.datum == datum:
                print("Ez a szoba már foglalt ezen a napon!\n")
                return None
        for szoba in szálloda.szobak:
            if szoba.szobaszam == szobaszam:
                foglalás = Foglalás(szoba, datum)
                szálloda.foglalasok.append(foglalás)
                return szoba.ar
        return None

    def lemondás(szálloda, foglalás):
        if foglalás in szálloda.foglalasok:
            szálloda.foglalasok.remove(foglalás)
            return True
        else:
            return False

    def listázás(szálloda):
        for foglalás in szálloda.foglalasok:
            print(f"Szobaszám: {foglalás.szoba.szobaszam}, Dátum: {foglalás.datum}\n")


def új_szálloda_felvétele(szállodák):
    nev = input("Adja meg az új szálloda nevét: ")
    egyagyas_ar = int(input("Adja meg az egyágyas szobák árát! "))
    ketagyas_ar = int(input("Adja meg a kétágyas szobák árát! "))
    szobák_száma = int(input("Adja meg a szobák számát! "))
    szobák = []
    for i in range(szobák_száma):
        ágyak_száma = int(input(f"Adja meg a(z) {i + 1}. szoba ágyainak számát (1 vagy 2)! "))
        if ágyak_száma == 1:
            szoba = EgyagyasSzoba(i + 1, egyagyas_ar)
        elif ágyak_száma == 2:
            szoba = KetagyasSzoba(i + 1, ketagyas_ar)
        else:
            print("Érvénytelen szám! Válasszon (1 v. 2)!.")
            continue
        szobák.append(szoba)
    szálloda = Szalloda(nev, egyagyas_ar, ketagyas_ar)
    szálloda.szobak = szobák
    szállodák.append(szálloda)
    print(f"{nev} szálloda sikeresen hozzáadva\n")


def foglalás(szálloda):
    szobaszam = int(input("\nAdja meg a szobaszámot! "))
    datum = input("Adja meg a foglalás dátumát (YYYY-MM-DD formátumban)! ")
    try:
        datum = datetime.strptime(datum, "%Y-%m-%d")
        if datum < datetime.now():
            print("Hibás dátum! Adjon meg jövőbeli dátumot!")
            return
    except ValueError:
        print("Hibás dátum formátum! Próbálja újra!")
        return

    szoba = None
    for szoba in szálloda.szobak:
        if szoba.szobaszam == szobaszam:
            break

    if not szoba:
        print("Nem létezik ilyen szobaszám a kiválasztott szállodában.\n")
        return

    ár = szálloda.foglalás(szobaszam, datum)
    if ár:
        print(f"A foglalás sikeres! A szoba ára (Ft): {ár}\n")
        return
    else:
        print("Nem sikerült foglalni a szobát.\n")
        return

def lemondás(szálloda):
    szobaszam = input("Adja meg a lemondani kívánt foglalás szobaszámát! ")
    datum = input("Adja meg a lemondani kívánt foglalás dátumát (YYYY-MM-DD formátumban)! ")
    try:
        datum = datetime.strptime(datum, "%Y-%m-%d")
    except ValueError:
        print("Hibás dátum formátum! Próbálja újra!")
        return

    for foglalás in szálloda.foglalasok:
        if foglalás.szoba.szobaszam == szobaszam and foglalás.datum == datum:
            if szálloda.lemondás(foglalás):
                print("A foglalás sikeresen törölve.\n")
                return
            else:
                print("A foglalás nem található.\n")
                return
    print("A megadott foglalás nem található.\n")


def mentés(szállodák):
    with open("foglalasi_adatok.txt", "w") as f:
        for szálloda in szállodák:
            f.write(f"{szálloda.nev},{szálloda.egyagyas_ar},{szálloda.ketagyas_ar}\n")
            for szoba in szálloda.szobak:
                f.write(f"{szoba.szobaszam},{szoba.ar}\n")
            for foglalás in szálloda.foglalasok:
                f.write(f"{foglalás.datum.strftime('%Y-%m-%d')},{foglalás.szoba.szobaszam},{foglalás.szoba.ar}\n")



def betöltés():
    szállodák = []
    try:
        with open("foglalasi_adatok.txt", "r") as f:
            sorok = f.readlines()
            szálloda = None
            for sor in sorok:
                adatok = sor.strip().split(",")
                if len(adatok) == 3:
                    nev, egyagyas_ar, ketagyas_ar = adatok
                    szálloda = Szalloda(nev, int(egyagyas_ar), int(ketagyas_ar))
                    szállodák.append(szálloda)
                elif len(adatok) == 2:
                    szobaszam, ar = adatok
                    szoba = Szoba(szobaszam, int(ar))
                    szálloda.szobak.append(szoba)
                elif len(adatok) == 4:
                    datum, szobaszam, ar = adatok
                    foglalás = Foglalás(None, datetime.strptime(datum, "%Y-%m-%d"))
                    foglalás.szoba = Szoba(int(szobaszam), int(ar))
                    szálloda.foglalasok.append(foglalás)
    except FileNotFoundError:
        pass
    return szállodák



def menü(szállodák):
    while True:
        print("1. Szálloda kiválasztása")
        print("2. Új szálloda felvétele")
        print("3. Kilépés\n")

        választás = input("Válassz egy műveletet (1-3): ")

        if választás == "1":
            if not szállodák:
                print("Nincs elérhető szálloda. Kérjük, előbb vegyen fel egy szállodát!")
                continue
            print("Válassz egy szállodát!")
            for i, szálloda in enumerate(szállodák, 1):
                print(f"{i}. {szálloda.nev}")
            választott_szálloda = szállodák[int(input("Szálloda száma: ")) - 1]
            while True:
                print("\n1. Foglalás")
                print("2. Lemondás")
                print("3. Foglalások listázása")
                print("4. Vissza a főmenübe\n")
                választás = input("Válassz egy műveletet (1-4)! ")

                if választás == "1":
                    foglalás(választott_szálloda)
                elif választás == "2":
                    lemondás(választott_szálloda)
                elif választás == "3":
                    választott_szálloda.listázás()
                elif választás == "4":
                    break
                else:
                    print("Érvénytelen választás! Válasszon 1 és 4 közötti számot!")

        elif választás == "2":
            új_szálloda_felvétele(szállodák)

        elif választás == "3":
            print("Kilépés...")
            mentés(szállodák)
            break

        else:
            print("Érvénytelen választás! Válasszon 1 és 3 közötti számot!")


mentü = betöltés()
menü(mentü)