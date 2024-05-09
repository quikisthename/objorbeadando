from datetime import datetime

class Szoba:
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar

class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar):
        super().__init__(szobaszam, ar)

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar):
        super().__init__(szobaszam, ar)

class Foglalás:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

class Szalloda:
    def __init__(self, nev, egyagyas_ar, ketagyas_ar):
        self.nev = nev
        self.egyagyas_ar = egyagyas_ar
        self.ketagyas_ar = ketagyas_ar
        self.szobak = []
        self.foglalasok = []

    def foglalás(self, szobaszam, datum):
        for foglalás in self.foglalasok:
            if foglalás.szoba.szobaszam == szobaszam and foglalás.datum == datum:
                print("Ez a szoba már foglalt ezen a napon!\n")
                return None
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                foglalás = Foglalás(szoba, datum)
                self.foglalasok.append(foglalás)
                return szoba.ar
        return None

    def lemondás(self, foglalás):
        if foglalás in self.foglalasok:
            self.foglalasok.remove(foglalás)
            return True
        else:
            return False

    def listázás(self):
        for foglalás in self.foglalasok:
            print(f"Szobaszám: {foglalás.szoba.szobaszam}, Dátum: {foglalás.datum}\n")

def új_szálloda_felvétele(szállodák):
    nev = input("Adja meg az új szálloda nevét: ")
    egyagyas_ar = int(input("Adja meg az egyágyas szobák árát: "))
    ketagyas_ar = int(input("Adja meg a kétágyas szobák árát: "))
    szobák_száma = int(input("Adja meg a szobák számát: "))
    szobák = []
    for i in range(szobák_száma):
        ágyak_száma = int(input(f"Adja meg a(z) {i+1}. szoba ágyainak számát (1 vagy 2): "))
        if ágyak_száma == 1:
            szoba = EgyagyasSzoba(i+1, egyagyas_ar)
        elif ágyak_száma == 2:
            szoba = KetagyasSzoba(i+1, ketagyas_ar)
        else:
            print("Érvénytelen szám! Csak 1 vagy 2 lehet.")
            continue
        szobák.append(szoba)
    szálloda = Szalloda(nev, egyagyas_ar, ketagyas_ar)
    szálloda.szobak = szobák
    szállodák.append(szálloda)
    print(f"{nev} szálloda sikeresen hozzáadva!\n")

def foglalás(szálloda):
    szobaszam = input("\nAdja meg a szobaszámot: ")
    datum = input("Adja meg a foglalás dátumát (YYYY-MM-DD formátumban): ")
    try:
        datum = datetime.strptime(datum, "%Y-%m-%d")
        if datum < datetime.now():
            print("Hibás dátum! Kérjük, adjon meg jövőbeli dátumot.")
            return
    except ValueError:
        print("Hibás dátum formátum! Kérjük, próbálja újra.")
        return

    for szoba in szálloda.szobak:
        if szoba.szobaszam == szobaszam:
            ár = szálloda.foglalás(szobaszam, datum)
            if ár:
                print(f"A foglalás sikeres! A szoba ára: {ár}\n")
                return
            else:
                print("Nem sikerült foglalni a szobát.\n")
                return
    print("Nem létezik ilyen szobaszám a kiválasztott szállodában.\n")

def lemondás(szálloda):
    szobaszam = input("Adja meg a lemondani kívánt foglalás szobaszámát: ")
    datum = input("Adja meg a lemondani kívánt foglalás dátumát (YYYY-MM-DD formátumban): ")
    try:
        datum = datetime.strptime(datum, "%Y-%m-%d")
    except ValueError:
        print("Hibás dátum formátum! Kérjük, próbálja újra.")
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
    with open("adatok.txt", "w") as f:
        for szálloda in szállodák:
            f.write(f"{szálloda.nev},{szálloda.egyagyas_ar},{szálloda.ketagyas_ar}\n")
            for szoba in szálloda.szobak:
                f.write(f"{szoba.szobaszam},{szoba.ar}\n")
            for foglalás in szálloda.foglalasok:
                f.write(f"{foglalás.szoba.szobaszam},{foglalás.datum}\n")

def betöltés():
    szállodák = []
    try:
        with open("adatok.txt", "r") as f:
            sorok = f.readlines()
            for sor in sorok:
                adatok = sor.strip().split(",")
                if len(adatok) == 3:
                    nev, egyagyas_ar, ketagyas_ar = adatok
                    szálloda = Szalloda(nev, int(egyagyas_ar), int(ketagyas_ar))
                    szállodák.append(szálloda)
                elif len(adatok) == 2:
                    szobaszam, ar = adatok
                    szoba = Szoba(szobaszam, int(ar))
                    szállodák[-1].szobak.append(szoba)
                elif len(adatok) == 4:
                    szobaszam, datum = adatok
                    for szálloda in szállodák:
                        for szoba in szálloda.szobak:
                            if szoba.szobaszam == szobaszam:
                                foglalás = Foglalás(szoba, datetime.strptime(datum, "%Y-%m-%d"))
                                szálloda.foglalasok.append(foglalás)
                            else:
                                print(f"Nem található szoba a(z) {szobaszam} számú szobához tartozó foglalásnak.")
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
                print("Nincs elérhető szálloda. Kérjük, előbb vegyen fel egy szállodát.")
                continue
            print("Válassz egy szállodát:")
            for i, szálloda in enumerate(szállodák, 1):
                print(f"{i}. {szálloda.nev}")
            választott_szálloda = szállodák[int(input("Szálloda száma: ")) - 1]
            while True:
                print("\n1. Foglalás")
                print("2. Lemondás")
                print("3. Foglalások listázása")
                print("4. Vissza a főmenübe\n")
                választás = input("Válassz egy műveletet (1-4): ")

                if választás == "1":
                    foglalás(választott_szálloda)
                elif választás == "2":
                    lemondás(választott_szálloda)
                elif választás == "3":
                    választott_szálloda.listázás()
                elif választás == "4":
                    break
                else:
                    print("Érvénytelen választás! Kérjük, válasszon 1 és 4 közötti számot.")

        elif választás == "2":
            új_szálloda_felvétele(szállodák)

        elif választás == "3":
            print("Kilépés...")
            mentés(szállodák)
            break

        else:
            print("Érvénytelen választás! Kérjük, válasszon 1 és 3 közötti számot.")

mentü = betöltés()
menü(mentü)
