import datetime


class Szoba:
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar


class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, 5000)


class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, 9000)


class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum


class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def szoba_hozzaadasa(self, szoba):
        self.szobak.append(szoba)

    def foglalas(self, szobaszam, datum):
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                for foglalas in self.foglalasok:
                    if foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum:
                        return False
                foglalas = Foglalas(szoba, datum)
                self.foglalasok.append(foglalas)
                return True, szoba.ar
        return False, None

    def lemondas(self, szobaszam, datum):
        for foglalas in self.foglalasok:
            if foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum:
                self.foglalasok.remove(foglalas)
                return True
        return False

    def foglalasok_listazasa(self):
        return [{"szobaszam": foglalas.szoba.szobaszam, "datum": foglalas.datum.strftime('%Y-%m-%d')}
                for foglalas in self.foglalasok]


def szoba_foglalasa(szalloda):
    szobaszam = input("Kérem, adja meg a foglalni kívánt szoba számát! ")
    lehetséges_szobaszámok = ["1", "7", "19"]
    if szobaszam not in lehetséges_szobaszámok:
        print("Sajnálom, a megadott szobaszám nem létezik.")
        return
    datum_str = input("Kérem, adja meg a foglalás dátumát (ÉÉÉÉ-HH-NN formátumban)! ")
    try:
        datum = datetime.datetime.strptime(datum_str, "%Y-%m-%d").date()
        success, ar = szalloda.foglalas(szobaszam, datum)
        if success:
            print(f"Sikeres foglalás! Ár: {ar}Ft")
        else:
            print("Valamely szöveg hibás vagy a szoba már foglalt ezen a napon.")
    except ValueError:
        print("Hibás dátumformátum! Kérem, adjon meg egy érvényes dátumot!")


def foglalas_lemondasa(szalloda):
    szobaszam = input("Kérem, adja meg a lemondani kívánt foglalás szoba számát! ")
    datum_str = input("Kérem, adja meg a foglalás dátumát (ÉÉÉÉ-HH-NN formátumban)! ")
    try:
        datum = datetime.datetime.strptime(datum_str, "%Y-%m-%d").date()
        if szalloda.lemondas(szobaszam, datum):
            print("Sikeres lemondás.")
        else:
            print("Nem található ilyen foglalás.")
    except ValueError:
        print("Hibás dátumformátum! Kérem, adjon meg egy érvényes dátumot!")


def foglalasok_listazasa(szalloda):
    print("Lefoglalt szobák:")
    foglalasok = szalloda.foglalasok_listazasa()
    if foglalasok:
        for foglalas in foglalasok:
            print(f"Foglalt szoba: {foglalas['szobaszam']}, Dátum: {foglalas['datum']}")
    else:
        print("Jelenleg nincsenek foglalások.")


def main():
    szalloda = Szalloda("Szálloda")

    szalloda.szoba_hozzaadasa(EgyagyasSzoba("1"))
    szalloda.szoba_hozzaadasa(EgyagyasSzoba("7"))
    szalloda.szoba_hozzaadasa(KetagyasSzoba("19"))

    szalloda.foglalas("1", datetime.date(2024, 6, 1))
    szalloda.foglalas("1", datetime.date(2024, 11, 11))
    szalloda.foglalas("19", datetime.date(2024, 12, 24))
    szalloda.foglalas("7", datetime.date(2024, 8, 15))
    szalloda.foglalas("19", datetime.date(2024, 10, 20))

    while True:
        print("\nVálasszon egy opciót!")
        print("1. Szoba foglalása")
        print("2. Foglalás lemondása")
        print("3. Foglalások listázása")
        print("0. Kilépés")
        valasztas = input("Kérem, adja meg a választott opció számát! ")

        if valasztas == "1":
            szoba_foglalasa(szalloda)
        elif valasztas == "2":
            foglalas_lemondasa(szalloda)
        elif valasztas == "3":
            foglalasok_listazasa(szalloda)
        elif valasztas == "0":
            print("Kilépés...")
            break
        else:
            print("Érvénytelen opció! Kérem, válasszon újra!")


if __name__ == "__main__":
    main()
