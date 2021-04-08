from izvuci_podatke import PreuzmiPodatke
from uvezi_podatke import IATA
from pprint import pprint

preuzmi_podatke = PreuzmiPodatke()
iata = IATA()

def pokreni_sve():
    skracenica = iata.uvezi()
    vreme_i_cena = preuzmi_podatke.termin_i_cena()
    rezultat = preuzmi_podatke.preuzmi_podatke(dictionary=vreme_i_cena, skracenica=skracenica)
    pprint(rezultat)

pokreni_sve()