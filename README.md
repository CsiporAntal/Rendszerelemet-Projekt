# 📊 Átviteli Függvény Elemző – LTI Rendszerek Vizualizációja

Ez a Python-alapú alkalmazás egy **Lineáris Időinvariáns (LTI)** rendszer elemzésére és vizualizációjára szolgál. A program segítségével megadhatsz egy átviteli függvényt (számláló és nevező együtthatók alapján), majd interaktív ábrákon keresztül tanulmányozhatod a rendszer dinamikáját, stabilitását és frekvenciaviselkedését.

---

## 🧠 Fő funkciók

- 📌 Számláló és nevező beviteli mezők (pl. `1, 2, 3`)
- ⚙️ Átviteli függvény automatikus generálása: `H(s) = N(s)/D(s)`
- ✖️ **Pólus–zérus térkép** (komplex síkon)
- 🟰 **Impulzusválasz ábra** `h(t)`
- 🌐 **3D |H(s)| vizualizáció** – a komplex sík felett
- 🎛️ Csúszkával forgatható 3D ábra (azimut irány)
- 🎨 Világos / rendszer témaválasztó
- ℹ️ Súgó / Névjegy ablak
- 📦 Bővíthető menü (pl. Export lehetőségek)

---

## 🛠️ Telepítés

1. **Python 3.10+ szükséges**  
2. Virtuális környezet (opcionális, ajánlott):

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```
3.Szükséges csomagok telepítése:

```bash
pip install numpy matplotlib scipy control PyQt6
```

## ▶️ Használat
```bash
python main.py
```
Ezután megnyílik az alkalmazás, ahol beírhatod a számlálót és nevezőt pl.:

```
Számláló: 1
Nevező: 1, 2, 2
```

A program a megadott átviteli függvény alapján:

- meghatározza a rendszer **pólusait**,
- kiértékeli annak **stabilitását**,
- majd grafikusan ábrázolja a rendszer viselkedését **időtartományban** (impulzusválasz), valamint a **komplex síkon** (|H(s)| 3D felületként).

---

## 🖼️ Képernyőképek

*Képek hozzáadása opcionális: lásd az `img/` mappát a példák elhelyezéséhez.*

---

## 📚 Elméleti háttér

A program **LTI (Lineáris Időinvariáns)** rendszerek elemzésére épül. Ezek a rendszerek:

- **lineárisak**, azaz érvényes rájuk a homogenitás és szuperpozíció elve,
- **időinvariánsak**, vagyis a rendszer viselkedése nem függ az időponttól.

Az alábbi matematikai eszközök segítik a rendszerek elemzését:

- **Laplace-transzformáció** – lehetővé teszi a differenciálegyenletek algebrai formában való vizsgálatát:

  $
  Y(s) = X(s) ⋅ H(s)
  $

- **Konvolúció az időtartományban** – a rendszer válasza a bemenetre az impulzusválasszal való konvolúcióval számolható:

  $
  y(t) = x(t) * h(t)
  $

- **Stabilitásvizsgálat pólushelyek alapján** – egy LTI rendszer stabil, ha minden pólusa a komplex sík bal oldali (negatív valós részű) felén helyezkedik el:

  $
  \text{Stabil, ha minden } \operatorname{Re}(s_i) < 0
  $

---

## 🚀 Fejlesztési lehetőségek

- 📤 Ábrák és adatok exportálása (pl. PDF, PNG, CSV formátumban)
- 🔁 Lépésválasz (`step response`) és frekvenciamenet (`Bode-diagram`) megjelenítése
- 🌐 Webes alkalmazás létrehozása (pl. **Streamlit** vagy **Plotly Dash** alapokon)

