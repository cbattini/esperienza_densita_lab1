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
    return np.sqrt(sigma_media**2 + delta_strum**2) # somma in quadratura delle incertezze

def analizza(dati):
    """Per ogni oggetto: id, media, dev. std. campione, dev. std. media, incertezza finale."""
    # Gli oggetti si riconoscono dalla colonna 0 del file...
    risultati = []
    for ogg in np.unique(dati[:, 0]): # np.unique(...) della colonna [:, 0] distingue i vari valori e ne genera una lista (es. [1, 2, 3, 4]) 
        sel = dati[dati[:, 0] == ogg] # dati[:, 0] == ogg crea una lista di True/False (True se il numero oggetto corrisponde), con dati[maschera] si ottengono solo gli oggetti True in una lista (sel)
        x = sel[:, 2] # estrae da sel i valori misurati
        delta_strum = sel[:, 3].max() # errore dello strumento
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


# ---------------------------------------------------------------
# volumi, densità e propagazione delle incertezze
# tutto in unità SI: mm³ -> m³ (× 1e-9), g -> kg (× 1e-3), densità in kg/m³
# ---------------------------------------------------------------

def errore_relativo(r):
    # r = riga di analizza: incertezza finale / media
    return r[:, 4] / r[:, 1]

# cilindro: V = π d²/4 h  ->  σV/V = √((2σd/d)^2 + (σh/h)^2)
cil_d, cil_h, cil_m = analizza(cilindro_diametro), analizza(cilindro_altezza), analizza(cilindro_massa)
cil_V = volume_cilindro(cil_d[:, 1], cil_h[:, 1]) * 1e-9
cil_contrib = {'diametro (×2)': 2*errore_relativo(cil_d),
               'altezza': errore_relativo(cil_h),
               'massa': errore_relativo(cil_m)}

# parallelepipedo: V = l1 l2 l3  ->  σV/V = √(Σ (σli/li)^2)
par_l1, par_l2, par_l3 = analizza(parallelepipedo_l1), analizza(parallelepipedo_l2), analizza(parallelepipedo_l3)
par_m = analizza(parallelepipedo_massa)
par_V = volume_parallepipedo(par_l1[:, 1], par_l2[:, 1], par_l3[:, 1]) * 1e-9
par_contrib = {'lato 1': errore_relativo(par_l1),
               'lato 2': errore_relativo(par_l2),
               'lato 3': errore_relativo(par_l3),
               'massa': errore_relativo(par_m)}

# sfera: V = π d^3/6  ->  σV/V = 3σd/d (uso l'errore relativo per il prodotto)
sfe_d, sfe_m = analizza(sfera_diametro), analizza(sfera_massa)
sfe_V = volume_sfera(sfe_d[:, 1]) * 1e-9
sfe_contrib = {'diametro (×3)': 3*errore_relativo(sfe_d),
               'massa': errore_relativo(sfe_m)}

def errore_volume(contrib):
    # somma in quadratura dei contributi delle dimensioni (tutti tranne la massa)
    return np.sqrt(sum(v**2 for k, v in contrib.items() if k != 'massa'))

# tabella unica di tutti gli oggetti
oggetti = []
for forma, V, m, contrib in [('cilindro', cil_V, cil_m, cil_contrib),
                             ('parallelepipedo', par_V, par_m, par_contrib),
                             ('sfera', sfe_V, sfe_m, sfe_contrib)]:
    sV = V * errore_volume(contrib)
    ids, m, sm = m[:, 0], m[:, 1] * 1e-3, m[:, 4] * 1e-3
    rho = m / V
    s_rho = rho * np.sqrt((sm/m)**2 + (sV/V)**2)
    for i in range(len(V)):
        oggetti.append(dict(forma=forma, id=int(ids[i]), V=V[i], sV=sV[i],
                            m=m[i], sm=sm[i], rho=rho[i], s_rho=s_rho[i],
                            contrib={k: v[i] for k, v in contrib.items()}))

# materiale: il valore tabulato più vicino, se entro il 5%
# valori tabulati (tabella della relazione), in kg/m³: (minimo, massimo)
materiali_intervallo = {'alluminio': (2710, 2710), 'acciaio': (7480, 8000), 'ottone': (8400, 8700)}
# per riconoscere il materiale uso il centro dell'intervallo
materiali_rif = {k: (a + b) / 2 for k, (a, b) in materiali_intervallo.items()}

def riconosci_materiale(rho, tolleranza=0.05):
    nome, rif = min(materiali_rif.items(), key=lambda kv: abs(kv[1] - rho))
    return nome if abs(rho - rif) / rif < tolleranza else 'non identificato'

for o in oggetti:
    o['materiale'] = riconosci_materiale(o['rho'])

# fit m = ρ V (retta per l'origine), pesato con la varianza efficace
# σ_eff² = σm² + ρ² σV², che tiene conto degli errori su entrambi gli assi
def fit_densita(V, sV, m, sm, iterazioni=10):
    rho = np.sum(m*V) / np.sum(V**2)          # stima iniziale senza pesi
    for _ in range(iterazioni):
        w = 1 / (sm**2 + rho**2 * sV**2)
        rho = np.sum(w*V*m) / np.sum(w*V**2)
    s_rho = 1 / np.sqrt(np.sum(w*V**2))
    return rho, s_rho, w

fit = {}
for mat in materiali_rif:
    gruppo = [o for o in oggetti if o['materiale'] == mat]
    if len(gruppo) >= 2:
        arr = lambda k: np.array([o[k] for o in gruppo])
        rho, s_rho, w = fit_densita(arr('V'), arr('sV'), arr('m'), arr('sm'))
        fit[mat] = dict(rho=rho, s_rho=s_rho, gruppo=gruppo)

print("\n\nDENSITÀ DEI SINGOLI OGGETTI")
print(f"{'oggetto':<20} {'V [m³]':>20} {'m [kg]':>20} {'ρ [kg/m³]':>12}  materiale")
for o in oggetti:
    print(f"{o['forma'] + ' ' + str(o['id']):<20} {o['V']:>9.4e} ± {o['sV']:.1e} "
          f"{o['m']:>9.6f} ± {o['sm']:.6f} {o['rho']:>6.0f} ± {o['s_rho']:<3.0f}  {o['materiale']}")

print("\nFIT m = ρ V PER MATERIALE")
for mat, f in fit.items():
    print(f"{mat:<10} ρ = {f['rho']:.0f} ± {f['s_rho']:.0f} kg/m³  "
          f"(tabulato {materiali_intervallo[mat]}, {len(f['gruppo'])} oggetti)")


# ---------------------------------------------------------------
# legge di scala per le sfere: m = (4/3) π ρ r³ = k r³
# in scala bilogaritmica: log m = 3 log r + log k  ->  una retta
# ---------------------------------------------------------------

def fit_retta(x, y, sx, sy, a0=1, iterazioni=10):
    """Fit pesato y = a x + b con errori su x e y (varianza efficace σy² + a² σx²).
    Restituisce a, σa, b, σb e il chi quadro."""
    a = a0
    for _ in range(iterazioni):
        w = 1 / (sy**2 + a**2 * sx**2)
        S, Sx, Sy = np.sum(w), np.sum(w*x), np.sum(w*y)
        Sxx, Sxy = np.sum(w*x*x), np.sum(w*x*y)
        D = S*Sxx - Sx**2
        a = (S*Sxy - Sx*Sy) / D
        b = (Sxx*Sy - Sx*Sxy) / D
    chi2 = np.sum(w * (y - a*x - b)**2)
    return a, np.sqrt(S/D), b, np.sqrt(Sxx/D), chi2

# raggio e massa delle sfere in SI (r = d/2, σr = σd/2)
sfe_r, sfe_sr = sfe_d[:, 1] / 2 * 1e-3, sfe_d[:, 4] / 2 * 1e-3
sfe_mk, sfe_smk = sfe_m[:, 1] * 1e-3, sfe_m[:, 4] * 1e-3
sfe_id = sfe_m[:, 0].astype(int)

# logaritmi in base 10 e loro errori: σ(log10 x) = σx / (x ln10)
log_r, log_m = np.log10(sfe_r), np.log10(sfe_mk)
s_log_r, s_log_m = sfe_sr / (sfe_r*np.log(10)), sfe_smk / (sfe_mk*np.log(10))

# valore atteso dell'intercetta: k = 4/3 π ρ, con la densità dell'acciaio dal fit
rho_sfere, s_rho_sfere = fit['acciaio']['rho'], fit['acciaio']['s_rho']
k_atteso = 4/3 * np.pi * rho_sfere
s_k_atteso = 4/3 * np.pi * s_rho_sfere

# due fit: tutte le sfere, e solo quelle di acciaio (la sfera 5 ha un'altra densità)
acciaio = np.array([o['materiale'] == 'acciaio' for o in oggetti if o['forma'] == 'sfera'])
fit_scala = {}
for nome, sel in [('tutte le sfere', np.ones(len(sfe_id), bool)), ('sfere di acciaio', acciaio)]:
    a, sa, b, sb, chi2 = fit_retta(log_r[sel], log_m[sel], s_log_r[sel], s_log_m[sel], a0=3)
    k, sk = 10**b, 10**b * np.log(10) * sb      # intercetta con r = 1 m
    fit_scala[nome] = dict(a=a, sa=sa, k=k, sk=sk, chi2=chi2, gdl=sel.sum() - 2, sel=sel)

print("\nLEGGE DI SCALA m = k r³ (fit di log m in funzione di log r)")
print(f"atteso: pendenza 3, k = 4/3 π ρ = {k_atteso:.0f} ± {s_k_atteso:.0f} kg/m³ "
      f"(ρ acciaio = {rho_sfere:.0f} ± {s_rho_sfere:.0f} kg/m³)")
for nome, f in fit_scala.items():
    print(f"{nome:<17} pendenza = {f['a']:.3f} ± {f['sa']:.3f} ({abs(f['a'] - 3)/f['sa']:.0f}σ da 3)   "
          f"k = {f['k']:.0f} ± {f['sk']:.0f} kg/m³   χ²/gdl = {f['chi2']:.1f}/{f['gdl']}")


# ---------------------------------------------------------------
# grafici: ognuno in una finestra separata (salvati in fondo in 'grafici/')
# ---------------------------------------------------------------
from matplotlib.lines import Line2D

# colori fissi: le prime tre posizioni distinguibili anche da chi è daltonico,
# sempre affiancati da un marker diverso
BLU, ARANCIO, ACQUA, GIALLO = '#2a78d6', '#eb6834', '#1baf7a', '#eda100'
GRIGIO, INCHIOSTRO, INCHIOSTRO_2 = '#8a8984', '#0b0b0b', '#52514e'

colore_forma = {'cilindro': BLU, 'parallelepipedo': ARANCIO, 'sfera': ACQUA}
marker_forma = {'cilindro': 'o', 'parallelepipedo': 's', 'sfera': '^'}
colore_mat = {'alluminio': BLU, 'acciaio': ARANCIO, 'ottone': ACQUA, 'non identificato': GRIGIO}

plt.rcParams.update({
    'figure.facecolor': '#fcfcfb', 'axes.facecolor': '#fcfcfb',
    'axes.edgecolor': '#c9c8c2', 'axes.labelcolor': INCHIOSTRO_2,
    'xtick.color': INCHIOSTRO_2, 'ytick.color': INCHIOSTRO_2,
    'text.color': INCHIOSTRO, 'axes.spines.top': False, 'axes.spines.right': False,
    'axes.grid': True, 'axes.axisbelow': True, 'grid.color': '#e8e7e2', 'grid.linewidth': 0.8,
    'axes.titleweight': 'bold', 'axes.titlelocation': 'left',
    'legend.frameon': True, 'legend.framealpha': 0.9, 'legend.edgecolor': '#e8e7e2',
    'lines.linewidth': 2,
    # numeri molto piccoli (volumi ~1e-6 m³) mostrati come ×10⁻⁶ in cima all'asse
    'axes.formatter.use_mathtext': True, 'axes.formatter.limits': (-3, 4),
})
stile_err = dict(linestyle='none', markersize=8, capsize=3, elinewidth=1.2,
                 markeredgecolor='#fcfcfb', markeredgewidth=1.5)

# voci di legenda costruite a mano
def voce_marker(label, colore=GRIGIO, marker='o'):
    return Line2D([], [], marker=marker, color=colore, linestyle='none', markersize=8, label=label)

def voce_linea(label, colore, stile='-'):
    return Line2D([], [], color=colore, linestyle=stile, label=label)

def legenda(ax, voci, loc, titolo=None, **kw):
    # legenda dentro il grafico; add_artist evita che la successiva cancelli questa
    ax.add_artist(ax.legend(handles=voci, loc=loc, title=titolo, **kw))

def legenda_fuori(fig, voci, titolo=None, pos='upper'):
    # legenda a destra del grafico (il layout le lascia spazio)
    fig.legend(handles=voci, loc=f'outside right {pos}', title=titolo)

voci_forme = [voce_marker(f, GRIGIO, marker_forma[f]) for f in marker_forma]

# oggetti la cui etichetta va a sinistra del punto per non sovrapporsi ad altre
A_SINISTRA = {('sfera', 4), ('parallelepipedo', 3)}

def nome_breve(o):
    # es. 'cil. 3', lo stesso numero di oggetto usato nei file di dati
    return f"{o['forma'][:3]}. {o['id']}"

def etichetta(ax, o, testo, x, y, dy=-10, va='baseline'):
    sx = (o['forma'], o['id']) in A_SINISTRA
    ax.annotate(testo, (x, y), xytext=(-6 if sx else 6, dy), textcoords='offset points',
                ha='right' if sx else 'left', va=va, fontsize=8, color=INCHIOSTRO_2)


# 1) dispersione delle misure ripetute: un grafico per ogni grandezza
for nome, dati, unita in grandezze:
    fig, ax = plt.subplots(figsize=(7, 5), constrained_layout=True, num=f'1 - {nome}')
    for ogg, m, s, sm, st in analizza(dati):
        x = dati[dati[:, 0] == ogg, 2]
        jitter = np.linspace(-0.12, 0.12, len(x))
        ax.plot(ogg + jitter, x - m, 'o', color=GRIGIO, markersize=5, alpha=0.8)
        ax.errorbar(ogg + 0.3, 0, yerr=st, fmt='D', color=BLU, **{**stile_err, 'markersize': 6})
    ax.axhline(0, color=INCHIOSTRO_2, linewidth=0.8)
    ax.set_title(f'Misure ripetute: {nome}')
    ax.set_xticks(np.unique(dati[:, 0]))
    ax.set_xlabel('oggetto')
    ax.set_ylabel(f'scarto dalla media [{unita}]')
    legenda_fuori(fig, [voce_marker('singole misure', GRIGIO),
                        Line2D([], [], marker='D', color=BLU, markersize=6,
                               label='media ± incertezza finale')])


# 2) massa in funzione del volume, colorati per forma
fig, ax = plt.subplots(figsize=(8, 6), constrained_layout=True, num='2 - massa e volume')
for forma in colore_forma:
    g = [o for o in oggetti if o['forma'] == forma]
    ax.errorbar([o['V'] for o in g], [o['m'] for o in g],
                xerr=[o['sV'] for o in g], yerr=[o['sm'] for o in g],
                fmt=marker_forma[forma], color=colore_forma[forma], **stile_err)
    for o in g:
        etichetta(ax, o, nome_breve(o), o['V'], o['m'])
ax.set_xlabel('volume V [m³]')
ax.set_ylabel('massa m [kg]')
ax.set_title('Massa in funzione del volume')
legenda(ax, [voce_marker(f, colore_forma[f], marker_forma[f]) for f in colore_forma],
        loc='upper left', titolo='forma')
ax.set_xlim(left=0); ax.set_ylim(bottom=0)


# 3) fit lineare m = ρ V per materiale
fig, ax = plt.subplots(figsize=(8, 6), constrained_layout=True, num='3 - fit densità')
Vmax = max(o['V'] for o in oggetti) * 1.1
voci_mat = []
for mat, col in colore_mat.items():
    g = [o for o in oggetti if o['materiale'] == mat]
    for o in g:
        ax.errorbar(o['V'], o['m'], xerr=o['sV'], yerr=o['sm'],
                    fmt=marker_forma[o['forma']], color=col, **stile_err)
        etichetta(ax, o, nome_breve(o), o['V'], o['m'])
    if mat in fit:
        f = fit[mat]
        Vs = np.array([0, Vmax])
        ax.plot(Vs, f['rho']*Vs, color=col, linewidth=2, zorder=0)
        voci_mat.append(voce_linea(f"{mat}: ρ = {f['rho']:.0f} ± {f['s_rho']:.0f} kg/m³", col))
    elif g:
        voci_mat.append(voce_marker(mat, col))
legenda(ax, voci_mat, loc='upper left', titolo='fit m = ρV')
legenda(ax, voci_forme, loc='upper left', titolo='forma', bbox_to_anchor=(0, 0.72))
ax.set_xlabel('volume V [m³]')
ax.set_ylabel('massa m [kg]')
ax.set_title('Fit m = ρ V per materiale')
ax.set_xlim(0, Vmax); ax.set_ylim(bottom=0)


# 4) densità di ogni oggetto e confronto con i valori tabulati
fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True, num='4 - densità oggetti')
etichette = [nome_breve(o) for o in oggetti]
for i, o in enumerate(oggetti):
    ax.errorbar(i, o['rho'], yerr=o['s_rho'], fmt=marker_forma[o['forma']],
                color=colore_mat[o['materiale']], **stile_err)
    ax.annotate(nome_breve(o), (i, o['rho']), xytext=(0, -14), textcoords='offset points',
                ha='center', va='top', fontsize=8, color=INCHIOSTRO_2)
for mat, rif in materiali_rif.items():
    lo, hi = materiali_intervallo[mat]
    if hi > lo:   # leghe: fascia con l'intervallo tabulato
        ax.axhspan(lo, hi, color=colore_mat[mat], alpha=0.12, linewidth=0, zorder=0)
    ax.axhline(rif, color=colore_mat[mat], linestyle='--', linewidth=1.2, zorder=0)
    testo_rif = f'{lo}' if hi == lo else f'{lo}–{hi}'
    ax.annotate(f'{mat} {testo_rif}', (len(oggetti) - 0.5, hi), xytext=(0, 3),
                textcoords='offset points', ha='right', fontsize=9, color=INCHIOSTRO_2)
ax.set_xticks(range(len(oggetti)), etichette, rotation=45, ha='right')
ax.set_ylabel('densità ρ [kg/m³]')
ax.set_ylim(bottom=2000)   # spazio per l'etichetta sotto il punto più basso
ax.set_title('Densità dei singoli oggetti')
legenda_fuori(fig, [voce_marker(m, c) for m, c in colore_mat.items()]
                   + [voce_linea('valore tabulato', GRIGIO, '--')], titolo='materiale')
legenda_fuori(fig, voci_forme, titolo='forma', pos='lower')


# 5) residui del fit: m - ρV, con la loro incertezza efficace
fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True, num='5 - residui')
for mat, f in fit.items():
    for o in f['gruppo']:
        r = o['m'] - f['rho']*o['V']
        s_eff = np.sqrt(o['sm']**2 + f['rho']**2 * o['sV']**2)
        ax.errorbar(o['V'], r, yerr=s_eff, fmt=marker_forma[o['forma']],
                    color=colore_mat[mat], **stile_err)
        etichetta(ax, o, nome_breve(o), o['V'], r, dy=0, va='center')
ax.axhline(0, color=INCHIOSTRO_2, linewidth=0.8)
legenda_fuori(fig, [voce_marker(m, colore_mat[m]) for m in fit], titolo='materiale')
legenda_fuori(fig, voci_forme, titolo='forma', pos='lower')
ax.set_xlabel('volume V [m³]')
ax.set_ylabel('residuo m − ρV [kg]')
ax.set_title('Residui del fit')


# 6) peso di ogni grandezza nell'incertezza sulla densità, un grafico per forma
#    (quota della varianza relativa: (σx/x)² / Σ(σ/·)²)
colori_contrib = [BLU, ARANCIO, ACQUA, GIALLO]
for forma in colore_forma:
    g = [o for o in oggetti if o['forma'] == forma]
    fig, ax = plt.subplots(figsize=(9, 1.2 + 0.6*len(g)), constrained_layout=True,
                           num=f'6 - contributi {forma}')
    chiavi = list(g[0]['contrib'])
    var = np.array([[o['contrib'][k]**2 for k in chiavi] for o in g])
    quote = 100 * var / var.sum(axis=1, keepdims=True)
    sinistra = np.zeros(len(g))
    for j, k in enumerate(chiavi):
        ax.barh(range(len(g)), quote[:, j], left=sinistra, height=0.6,
                color=colori_contrib[j], edgecolor='#fcfcfb', linewidth=2, label=k)
        sinistra += quote[:, j]
    ax.set_yticks(range(len(g)), [f"{forma} {o['id']}" for o in g])
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.grid(axis='y', visible=False)
    ax.set_xlabel('quota della varianza relativa di ρ [%]')
    ax.set_title(f'Contributi all\'incertezza sulla densità: {forma}')
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), title='misura')


# 7) legge di scala per le sfere, in scala bilogaritmica
fig, ax = plt.subplots(figsize=(8, 6), constrained_layout=True, num='7 - legge di scala sfere')
for i, o in enumerate(o for o in oggetti if o['forma'] == 'sfera'):
    ax.errorbar(sfe_r[i], sfe_mk[i], xerr=sfe_sr[i], yerr=sfe_smk[i], fmt='^',
                color=colore_mat[o['materiale']], **stile_err)
    etichetta(ax, o, nome_breve(o), sfe_r[i], sfe_mk[i])
r_linea = np.array([sfe_r.min() * 0.85, sfe_r.max() * 1.15])
voci = []
for (nome, f), col, stile in zip(fit_scala.items(), [BLU, ARANCIO], ['--', '-']):
    ax.plot(r_linea, f['k'] * r_linea**f['a'], color=col, linestyle=stile, zorder=0)
    voci.append(voce_linea(f"fit {nome}: pendenza {f['a']:.3f} ± {f['sa']:.3f}", col, stile))
ax.plot(r_linea, k_atteso * r_linea**3, color=GRIGIO, linestyle=':', zorder=0)
voci.append(voce_linea(f'atteso: m = 4/3 π ρ r³, pendenza 3', GRIGIO, ':'))
voci += [voce_marker('sfere di acciaio', ARANCIO, '^'), voce_marker('sfera non identificata', GRIGIO, '^')]
ax.set_xscale('log'); ax.set_yscale('log')
ax.set_xlabel('raggio r [m]')
ax.set_ylabel('massa m [kg]')
ax.set_title('Legge di scala m = k r³ per le sfere (scala bilogaritmica)')
legenda(ax, voci, loc='upper left')


# 8) confronto scala lineare / bilogaritmica: la legge di potenza diventa una retta
#    curve m ∝ rⁿ (n = 2, 3, 4) che passano tutte per lo stesso punto r0,
#    con la normalizzazione attesa k = 4/3 π ρ
fig, axs = plt.subplots(1, 2, figsize=(13, 5.5), constrained_layout=True,
                        num='8 - confronto lineare e bilogaritmico')
r0 = 0.01                                   # 1 cm, al centro dei dati
r_curva = np.linspace(0.001, 0.015, 300)    # da 1 a 15 mm
esponenti = {2: (GRIGIO, '--'), 3: (INCHIOSTRO, '-'), 4: (GRIGIO, '-.')}
apice = {2: '²', 3: '³', 4: '⁴'}
for ax, scala in zip(axs, ['lineare', 'bilogaritmica']):
    for n, (col, stile) in esponenti.items():
        ax.plot(r_curva, k_atteso * r0**3 * (r_curva/r0)**n, color=col, linestyle=stile,
                linewidth=2 if n == 3 else 1.2, zorder=0)
        m0 = k_atteso * r0**3
        if scala == 'lineare':
            # in fondo alla curva, o dove esce dal grafico (m = 0.11 kg)
            r_lab = min(r_curva[-1], r0 * (0.11/m0)**(1/n))
            pos = dict(xytext=(4, 0), va='center')
        else:
            # a sinistra, dove le rette sono ben separate
            r_lab = r_curva[0] * 1.15
            pos = dict(xytext=(0, 10), va='bottom')
        ax.annotate(f'm ∝ r{apice[n]}', (r_lab, m0 * (r_lab/r0)**n), textcoords='offset points',
                    fontsize=9, color=INCHIOSTRO_2, **pos,
                    bbox=dict(facecolor='#fcfcfb', edgecolor='none', pad=1))
    for i, o in enumerate(o for o in oggetti if o['forma'] == 'sfera'):
        ax.errorbar(sfe_r[i], sfe_mk[i], xerr=sfe_sr[i], yerr=sfe_smk[i], fmt='^',
                    color=colore_mat[o['materiale']], **stile_err)
        etichetta(ax, o, nome_breve(o), sfe_r[i], sfe_mk[i])
    if scala == 'bilogaritmica':
        ax.set_xscale('log'); ax.set_yscale('log')
    else:
        ax.set_xlim(0, r_curva[-1] * 1.12); ax.set_ylim(0, 0.12)
    ax.set_xlabel('raggio r [m]')
    ax.set_ylabel('massa m [kg]')
    ax.set_title(f'Scala {scala}')
legenda(axs[0], [voce_linea('m ∝ r² (pendenza 2)', GRIGIO, '--'),
                 voce_linea('m ∝ r³ (atteso, pendenza 3)', INCHIOSTRO),
                 voce_linea('m ∝ r⁴ (pendenza 4)', GRIGIO, '-.'),
                 voce_marker('sfere di acciaio', ARANCIO, '^'),
                 voce_marker('sfera non identificata', GRIGIO, '^')], loc='upper left')
fig.suptitle('Legge di potenza m = k rⁿ: curva in scala lineare, retta in scala bilogaritmica',
             x=0.01, ha='left', fontweight='bold')


# ---------------------------------------------------------------
# grafici per la relazione: fit del volume in funzione della massa
# V = α m + β con curve_fit, come descritto nella relazione
# uso gli stessi valori delle tabelle: media arrotondata alla risoluzione
# dello strumento e incertezza = risoluzione; m in g, V in mm³
# ---------------------------------------------------------------
from decimal import Decimal, ROUND_HALF_UP
from scipy.optimize import curve_fit

def media_tabella(dati):
    """Per ogni oggetto: media arrotondata alla risoluzione e risoluzione (come nelle tabelle)."""
    medie, ris = [], []
    for ogg in np.unique(dati[:, 0]):
        sel = dati[dati[:, 0] == ogg]
        delta = Decimal(str(sel[:, 3].max()))
        cifre = Decimal(1).scaleb(delta.as_tuple().exponent)   # 0.02 -> 0.01, 0.001 -> 0.001
        m = Decimal(str(media(sel[:, 2]))).quantize(cifre, ROUND_HALF_UP)
        medie.append(float(m)); ris.append(float(delta))
    return np.array(medie), np.array(ris)

tab = []   # una riga per oggetto: forma, id, m, σm, V, σV
for forma, dati_m, dim in [('cilindro', cilindro_massa, [cilindro_diametro, cilindro_altezza]),
                           ('parallelepipedo', parallelepipedo_massa,
                            [parallelepipedo_l1, parallelepipedo_l2, parallelepipedo_l3]),
                           ('sfera', sfera_massa, [sfera_diametro])]:
    m, sm = media_tabella(dati_m)
    misure = [media_tabella(d) for d in dim]
    if forma == 'cilindro':
        (d, sd), (h, sh) = misure
        V = volume_cilindro(d, h); sV = V * np.sqrt((2*sd/d)**2 + (sh/h)**2)
    elif forma == 'parallelepipedo':
        (a, sa), (b, sb), (c, sc) = misure
        V = volume_parallepipedo(a, b, c); sV = V * np.sqrt((sa/a)**2 + (sb/b)**2 + (sc/c)**2)
    else:
        (d, sd), = misure
        V = volume_sfera(d); sV = V * 3*sd/d
    for i in range(len(m)):
        rho = m[i] / V[i] * 1e6                              # g/mm³ -> kg/m³
        s_rho = rho * np.sqrt((sm[i]/m[i])**2 + (sV[i]/V[i])**2)
        tab.append(dict(forma=forma, id=i + 1, m=m[i], sm=sm[i], V=V[i], sV=sV[i],
                        rho=rho, s_rho=s_rho, materiale=riconosci_materiale(rho)))

print("\n\nVALORI COME NELLE TABELLE DELLA RELAZIONE (m in g, V in mm³, ρ in kg/m³)")
for o in tab:
    print(f"{o['forma']:<16}{o['id']}  m = {o['m']:.3f}  V = {o['V']:8.1f} ± {o['sV']:4.1f}"
          f"  ρ = {o['rho']:7.1f} ± {o['s_rho']:4.1f}  {o['materiale']}")

def retta(x, alpha, beta):
    return alpha * x + beta

# fit per ogni gruppo con almeno due oggetti
# l'incertezza su m è trascurabile rispetto a quella su V (errore relativo ~1e-4 contro ~1e-3)
fit_rel = {}
for mat in materiali_rif:
    g = [o for o in tab if o['materiale'] == mat]
    if len(g) < 2:
        continue
    x = np.array([o['m'] for o in g]); y = np.array([o['V'] for o in g])
    sy = np.array([o['sV'] for o in g])
    popt, pcov = curve_fit(retta, x, y, sigma=sy, absolute_sigma=True)
    alpha, beta = popt
    s_alpha, s_beta = np.sqrt(np.diag(pcov))
    chi2 = np.sum(((y - retta(x, *popt)) / sy)**2)
    rho = 1e6 / alpha                       # α in mm³/g -> ρ in kg/m³
    s_rho = 1e6 * s_alpha / alpha**2
    fit_rel[mat] = dict(alpha=alpha, s_alpha=s_alpha, beta=beta, s_beta=s_beta,
                        rho=rho, s_rho=s_rho, chi2=chi2, gdl=len(g) - 2, gruppo=g)

print("\nFIT V = α m + β (curve_fit)")
for mat, f in fit_rel.items():
    lo, hi = materiali_intervallo[mat]
    print(f"{mat:<10} n = {len(f['gruppo'])}  α = {f['alpha']:.3f} ± {f['s_alpha']:.3f} mm³/g"
          f"  β = {f['beta']:.2f} ± {f['s_beta']:.2f} mm³  χ²/gdl = {f['chi2']:.2f}/{f['gdl']}"
          f"  ρ = {f['rho']:.1f} ± {f['s_rho']:.1f} kg/m³  (tabulato {lo}–{hi})")
    print("           oggetti:", ', '.join(f"{o['forma']} {o['id']}" for o in f['gruppo']))


# A) dispersione (m, V) di tutti gli oggetti, con le rette dei valori tabulati come guida
SPOSTA_A = {('cilindro', 2): (-6, 4), ('parallelepipedo', 3): (6, -4), ('cilindro', 5): (6, -12),
            ('sfera', 5): (6, -8), ('sfera', 4): (-6, 6), ('sfera', 2): (6, -12)}
fig, ax = plt.subplots(figsize=(8, 6), constrained_layout=True, num='A - dispersione massa volume')
m_max = max(o['m'] for o in tab) * 1.08
for mat, rif in materiali_rif.items():
    ms = np.array([0, m_max])
    ax.plot(ms, ms / rif * 1e6, color=colore_mat[mat], linestyle=':', linewidth=1.2, zorder=0)
for forma in colore_forma:
    g = [o for o in tab if o['forma'] == forma]
    ax.errorbar([o['m'] for o in g], [o['V'] for o in g],
                xerr=[o['sm'] for o in g], yerr=[o['sV'] for o in g],
                fmt=marker_forma[forma], color=colore_forma[forma], **stile_err)
    for o in g:
        # spostamento dell'etichetta (in punti) scelto a mano per non sovrapporle
        dx, dy = SPOSTA_A.get((o['forma'], o['id']), (6, -12))
        ax.annotate(nome_breve(o), (o['m'], o['V']), xytext=(dx, dy), textcoords='offset points',
                    ha='right' if dx < 0 else 'left', fontsize=8, color=INCHIOSTRO_2)
legenda(ax, [voce_marker(f, colore_forma[f], marker_forma[f]) for f in colore_forma],
        loc='upper left', titolo='forma')
legenda(ax, [voce_linea(f'{mat} (tabulato)', colore_mat[mat], ':') for mat in materiali_rif],
        loc='lower right', titolo='V = m/ρ')
ax.set_xlabel('massa m [g]')
ax.set_ylabel('volume V [mm³]')
ax.set_title('Dispersione (m, V) di tutti i pesetti')
ax.set_xlim(0, m_max); ax.set_ylim(0, 10000)
ax.ticklabel_format(axis='y', style='plain')   # niente ×10⁴ in cima all'asse


# B) un grafico per ogni gruppo: fit in alto, residui in basso
for mat, f in fit_rel.items():
    g = f['gruppo']; col = colore_mat[mat]
    fig, (ax, axr) = plt.subplots(2, 1, figsize=(7, 6.5), sharex=True, constrained_layout=True,
                                  gridspec_kw=dict(height_ratios=[3, 1.3]), num=f'B - fit {mat}')
    x = np.array([o['m'] for o in g])
    margine = 0.08 * (x.max() - x.min())
    xs = np.linspace(x.min() - margine, x.max() + margine, 100)
    ax.plot(xs, retta(xs, f['alpha'], f['beta']), color=col, zorder=0,
            label=f"fit: α = {f['alpha']:.2f} ± {f['s_alpha']:.2f} mm³/g\n"
                  f"      β = {f['beta']:.1f} ± {f['s_beta']:.1f} mm³")
    for o in g:
        ax.errorbar(o['m'], o['V'], xerr=o['sm'], yerr=o['sV'], fmt=marker_forma[o['forma']],
                    color=col, **stile_err)
        sx = o['forma'] == 'sfera' and o['id'] == 4      # sfera 4 e 2 hanno quasi la stessa massa
        ax.annotate(nome_breve(o), (o['m'], o['V']), xytext=(-8 if sx else 8, 8 if sx else -12),
                    textcoords='offset points', ha='right' if sx else 'left',
                    fontsize=8, color=INCHIOSTRO_2)
        r = o['V'] - retta(o['m'], f['alpha'], f['beta'])
        axr.errorbar(o['m'], r, yerr=o['sV'], fmt=marker_forma[o['forma']], color=col, **stile_err)
    axr.axhline(0, color=INCHIOSTRO_2, linewidth=0.8)
    ax.legend(loc='upper left')
    ax.set_ylabel('volume V [mm³]')
    ax.set_title(f"Fit V = α m + β: {mat} (ρ = {f['rho']:.0f} ± {f['s_rho']:.0f} kg/m³)")
    axr.set_xlabel('massa m [g]')
    axr.set_ylabel('residui [mm³]')


# ---------------------------------------------------------------
# salvataggio dei grafici nella cartella 'grafici/' accanto a questo file
# ogni figura prende il nome dalla sua etichetta (num=...), es.
# '3 - fit densità' -> grafici/3_fit_densita.png
# png a 300 dpi, da usare in LaTeX con \includegraphics
# ---------------------------------------------------------------
import os
import re
import unicodedata

CARTELLA_GRAFICI = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'grafici')
FORMATI = ('png',)

def nome_file(etichetta):
    # niente accenti né spazi nei nomi dei file (LaTeX e alcuni sistemi non li gradiscono)
    testo = unicodedata.normalize('NFKD', etichetta).encode('ascii', 'ignore').decode()
    testo = re.sub(r'[^A-Za-z0-9]+', '_', testo)   # ogni gruppo di simboli/spazi -> '_'
    return testo.strip('_').lower()

os.makedirs(CARTELLA_GRAFICI, exist_ok=True)   # crea la cartella se non esiste

for n in plt.get_fignums():                     # tutte le figure aperte
    fig = plt.figure(n)
    nome = nome_file(fig.get_label() or f'figura_{n}')
    for formato in FORMATI:
        percorso = os.path.join(CARTELLA_GRAFICI, f'{nome}.{formato}')
        fig.savefig(percorso, dpi=300, bbox_inches='tight')
    print(f'salvato: grafici/{nome}.{{{",".join(FORMATI)}}}')

plt.show()