# Relazione densità – cose da fare

Tabelle e grafici sono già pronti in `materiale_analisi.tex`, basta copiarli. I numeri li stampa `main.py` quando lo lanciate.

## Analisi dati – da scrivere
- [ ] intro veloce: cosa facciamo (volumi → densità → fit), usato Python + NumPy + curve_fit
- [ ] formule dei volumi + incertezze (parallelepipedo, cilindro, sfera), basta richiamare quelle dei cenni teorici
- [ ] densità dei singoli pesetti + tabelle 4-6
- [ ] tabella valori tabulati
- [ ] cilindro 4: decidere l'incertezza sull'altezza (0.01 o 0.03 mm?), le misure variano parecchio
- [ ] grafico dispersione (m, V)
- [ ] dire come abbiamo fatto i gruppi e chi abbiamo escluso
- [ ] fit V = αm + β, poi ρ = 1/α e σρ = σα/α² (moltiplicare per 10⁶ per avere kg/m³)
- [ ] un grafico per gruppo + commento: compatibile col tabulato? β viene circa 0?
- [ ] acciaio: nei residui i punti escono dalle barre d'errore, spiegare
- [ ] alluminio e ottone: solo 2 punti, la retta ci passa per forza
- [ ] legge m = kr³ per le sfere: grafico bilogaritmico + pendenza

## Conclusioni – da scrivere
- [ ] riassunto delle densità trovate, compatibili o no
- [ ] pesetti che non sappiamo di cosa sono
- [ ] com'è andata la legge m = kr³
- [ ] errori / cosa si potrebbe fare meglio

---

## Gruppi
- **acciaio**: cilindro 1, sfere 1-2-3-4
- **alluminio**: cilindro 2, parallelepipedo 1
- **ottone**: cilindro 3, parallelepipedo 2
- **esclusi** (non corrispondono a niente della tabella, più del 5% di differenza):
  - cilindro 4 → ~2447 kg/m³ (sembra alluminio ma è più leggero del 10%, forse è cavo o un'altra lega, ed è anche quello irregolare)
  - cilindro 5 → ~6965 kg/m³
  - parallelepipedo 3 → ~4363 kg/m³
  - sfera 5 → ~6696 kg/m³

## Risultati dei fit (V = αm + β)
| gruppo    | α (mm³/g)      | β (mm³)        | ρ (kg/m³)    | tabulato   |
|-----------|----------------|----------------|--------------|------------|
| acciaio   | 130.31 ± 0.24  | -112.4 ± 9.3   | 7674 ± 14    | 7480-8000 ✅ |
| alluminio | 376.2 ± 1.3    | -32 ± 11       | 2658 ± 9     | 2710 ❌     |
| ottone    | 117.22 ± 0.95  | 32 ± 17        | 8531 ± 69    | 8400-8700 ✅ |

- acciaio: β non viene 0 (dovrebbe!) e i punti non stanno bene sulla retta. Il motivo è che le sfere 1 e 3 hanno ~7935 kg/m³, mentre le sfere 2, 4 e il cilindro 1 ~7795 → probabilmente sono due acciai diversi
- alluminio: viene un po' basso, ma anche i due pesetti da soli sono sotto 2710 → forse è una lega e non alluminio puro

## Cosa sono i residui
- residuo = volume misurato − volume previsto dalla retta → quanto il punto sta sopra/sotto la retta
- è il grafico piccolo sotto ogni fit, serve a vedere differenze di pochi mm³ che nel grafico grande non si notano
- **fit buono**: residui sparsi a caso intorno a 0, e la barra d'errore più o meno tocca lo 0
- **fit non buono**: punti lontani da 0 di tante barre d'errore, oppure seguono un andamento strano
- acciaio: la sfera 3 sta 27 mm³ sotto la retta con barra ±6 mm³ → più di 4 barre, non va bene
- alluminio/ottone: residui esattamente 0, ma solo perché i punti sono 2

## Legge m = kr³ (sfere)
- m = 4/3 π ρ r³ → in scala log-log è una retta con pendenza 3
- tutte le sfere: pendenza **3.159 ± 0.004** → no, ma la sfera 5 è di un altro materiale quindi non conta
- solo acciaio: pendenza **2.902 ± 0.008** → ancora lontano da 3
- perché: le sfere grandi (2 e 4) hanno densità più bassa delle piccole (1 e 3), quindi la massa cresce un po' meno di r³
- le incertezze sono piccolissime (0.01 mm sul diametro), quindi basta un 2% di differenza di densità per sballare tutto

## Cos'è β
- nel fit V = αm + β: α è la pendenza (da lì esce ρ = 1/α), β è l'intercetta
- β = il volume che dà la retta quando m = 0, cioè dove la retta taglia l'asse verticale
- la teoria dice V = m/ρ → massa 0 = volume 0 → **β dovrebbe venire 0**
- per vedere se è compatibile con 0: |β| / σβ → se viene ≲ 2 ok, se viene molto di più no
  - acciaio: -112.4 ± 9.3 → 12 volte σ → **no**
  - alluminio: -32 ± 11 → circa 3 → al limite
  - ottone: 32 ± 17 → circa 2 → **sì**
- acciaio: β lontano da 0 → stessa storia dei residui, i pesetti non stanno su una sola retta per l'origine perché non hanno tutti la stessa densità → il fit abbassa la retta e la ρ che esce (7674) è più bassa di tutti i pesetti presi da soli
- alluminio/ottone: 2 punti, β lo decidono quei due punti e basta → non conta molto

## Promemoria vari
- incertezze nelle tabelle = risoluzione dello strumento (0.001 g bilancia, 0.01 mm palmer, 0.02 mm calibro)
- valori nelle tabelle = media delle misure ripetute, arrotondata alla risoluzione
- densità sempre in kg/m³, massa in g, volume in mm³
- i grafici li salva `main.py` nella cartella `grafici/` (png), la cartella deve stare accanto al .tex

CORREZIONI DA APPORTARE
1- verificare correttezza sfera 5 potrebbe essere 9,52mm
2- il parallelepipedo 3 potrebbe essere titanio FATTO
3- Con d = 9.96 mm al posto di 10.96 (errore di 1 mm sulla scala principale) la densità diventa 8433 kg/m³, cioè ottone. Va proposta solo come ipotesi, da controllare rimisurando il pezzo.
4- per il cilindro 4 il criterio dichiarato dice che per i solidi irregolari si usa la media di più misure. Allora l’incertezza deve essere la deviazione standard della media, non la risoluzione di 0.01 mm riportata in tabella 1.
5- Per l’alluminio la tabella dà solo 2710, mentre le leghe comuni stanno tra circa 2640 e 2810. Con un intervallo, 2658 diventa compatibile, e la conclusione “non compatibile” va rivista.
Per l’acciaio i due gruppi suggeriscono materiali diversi:
circa 7795 kg/m³: acciaio da cuscinetti o al carbonio (~7810–7850);
circa 7935 kg/m³: inox austenitico 304/316 (~7900–8000).
6- definire concetto di compatibilità
 Per esempio |x − x_tab| < 2σ, e per gli intervalli “valore dentro l’intervallo entro 2σ”. Oggi si usano 2σ, 5σ, 11σ, 12σ in modo caso per caso.
 7- Le misure ripetute differiscono fino a 0.006 g, ma si assegna σ = 0.001 g. Va reso coerente: per esempio σ pari alla dispersione, o alla semidispersione. Non cambia i risultati, perché l’incertezza relativa resta circa 10⁻⁴, ma è un’incoerenza 
 
 9- Giustificare “è probabile che il volume sia sovrastimato”.  La motivazione è che il calibro legge l’ingombro massimo, quindi smussi, bordi arrotondati e facce non parallele portano a sovrastimare il volume. FATTO