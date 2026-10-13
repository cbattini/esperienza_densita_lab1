import numpy as np
from matplotlib import pyplot as plt
import scipy as sp

""" LETTURA DATI """

# colonne: 0 = oggetto, 1 = misura_oggetto, 2 = misura, 3 = incertezza
# (la colonna 4, l'unità di misura, è testo: la escludiamo con usecols)

# opzioni per ogni lettura
opz = dict(delimiter=',', usecols=(0, 1, 2, 3))

# cilindro
cilindro_altezza = np.loadtxt('cilindro_altezza.txt', **opz)
cilindro_diametro = np.loadtxt('cilindro_diametro.txt', **opz)
cilindro_massa = np.loadtxt('cilindro_massa.txt', **opz)

# parallelepipedo
parallelepipedo_l1 = np.loadtxt('parallelepipedo_l1.txt', **opz)
parallelepipedo_l2 = np.loadtxt('parallelepipedo_l2.txt', **opz)
parallelepipedo_l3 = np.loadtxt('parallelepipedo_l3.txt', **opz)
parallelepipedo_massa = np.loadtxt('parallelepipedo_massa.txt', **opz)

# sfera
sfera_diametro = np.loadtxt('sfera_diametro.txt', **opz)
sfera_massa = np.loadtxt('sfera_massa.txt', **opz)


""" FUNZIONI VOLUMI """

def volume_cilindro(diametro, altezza):
    return np.pi*diametro**2/4*altezza

def volume_parallepipedo(l1, l2, l3):
    return l1*l2*l3

def volume_sfera(diametro):
    return np.pi*diametro**3/6


""" FUNZIONI STATISTICHE """
# agisce su liste di dati

def media(x):
    return np.sum(x) / len(x)

# divide per n-1 (deviazione standard campionaria)
def dev_std_campione(x):
    return np.sqrt(np.sum((x - media(x))**2) / (len(x) - 1))

# errore statistico: s / sqrt(n)
def dev_std_media(x):
    return dev_std_campione(x) / np.sqrt(len(x))

# errore statistico e strumentale sommati in quadratura
def incertezza_finale(sigma_media, delta_strum):
    return np.sqrt(sigma_media**2 + delta_strum**2)

def analizza(dati):
    """Per ogni oggetto: id, media, dev. std. campione, dev. std. media, incertezza finale."""
    # Gli oggetti si riconoscono dalla colonna 0 del file...
    risultati = []
    for ogg in np.unique(dati[:, 0]): # np.unique(...) della colonna [:, 0] distingue i vari valori e ne genera una lista (es. [1, 2, 3, 4]) 
        sel = dati[dati[:, 0] == ogg] # dati[:, 0] == ogg crea una lista di True/False (True se il numero oggetto corrisponde), con dati[maschera] si ottengono solo gli oggetti True in una lista (sel)
        x = sel[:, 2] # estrae da sel i valori misurati
        delta_strum = sel[:, 3].max()
        s_media = dev_std_media(x)
        risultati.append((ogg, media(x), dev_std_campione(x), s_media,
                          incertezza_finale(s_media, delta_strum)))
    return np.array(risultati)

np.set_printoptions(suppress=True, precision=3)
# print(volume_cilindro(cilindro_diametro[0], cilindro_altezza[0]))
# Accesso solo al valore misurato (colonna 2 = misura)
# Se vuoi tutti i valori misurati della colonna:
# print(cilindro_diametro[:, 2])

# Esempio: masse del cilindro 1 e relativa incertezza
# m = cilindro_massa[cilindro_massa[:, 0] == 1, 2]
# dm = cilindro_massa[cilindro_massa[:, 0] == 1, 3]
# print(m, dm)
# stampa finale: per ogni grandezza e ogni oggetto
grandezze = [
    ('cilindro altezza', cilindro_altezza, 'mm'),
    ('cilindro diametro', cilindro_diametro, 'mm'),
    ('cilindro massa', cilindro_massa, 'g'),
    ('parallelepipedo l1', parallelepipedo_l1, 'mm'),
    ('parallelepipedo l2', parallelepipedo_l2, 'mm'),
    ('parallelepipedo l3', parallelepipedo_l3, 'mm'),
    ('parallelepipedo massa', parallelepipedo_massa, 'g'),
    ('sfera diametro', sfera_diametro, 'mm'),
    ('sfera massa', sfera_massa, 'g'),
]

for nome, dati, unita in grandezze:
    print(f"\n{nome} [{unita}]")
    print(f"{'ogg':>4} {'media':>10} {'s':>8} {'σ_media':>8} {'σ_finale':>9}")
    for ogg, m, s, sm, st in analizza(dati):
        print(f"{int(ogg):>4} {m:>10.3f} {s:>8.3f} {sm:>8.3f} {st:>9.3f}")
