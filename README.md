# ❖ KHOR DXB: Dubai Real Estate Market Intelligence & Institutional Decision Support Platform (2020–2026)

[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.42+-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4+-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Statsmodels](https://img.shields.io/badge/Statsmodels-0.14+-4A90E2)](https://www.statsmodels.org/)
[![Prophet](https://img.shields.io/badge/Meta-Prophet-0081FB)](https://facebook.github.io/prophet/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data: DLD Official](https://img.shields.io/badge/Data-Dubai_Land_Department-10B981)](https://www.kaggle.com/datasets/sergionefedov/dubai-real-estate-sales-and-rentals-20202026)

Platform intelijen pasar dan sistem penunjang keputusan investasi (*Decision Support System* / DSS) kelas institusional berbasis data transaksi resmi **Dubai Land Department (DLD)** dan listing pasar terbuka periode 2020–2026 (62.000+ data transaksi). 

Platform ini mengintegrasikan ekonometrika spasial, Automated Valuation Models (AVM), klasifikasi kesepakatan AI (*Undervalued vs Overpriced*), pemodelan portofolio multi-aset berbasis regulasi UAE Golden Visa (AED 2 Juta), serta simulasi stres utang perbankan komersial (*Debt Service Coverage Ratio* / DSCR).

---

## Daftar Isi (Table of Contents)

1. [Latar Belakang & Pernyataan Masalah](#1-latar-belakang--pernyataan-masalah)
2. [Arsitektur Solusi & 3 Pilar Platform](#2-arsitektur-solusi--3-pilar-platform)
3. [Sumber Dataset & Arsitektur Relasional](#3-sumber-dataset--arsitektur-relasional)
4. [Rekayasa Fitur Spesifik Domain](#4-rekayasa-fitur-spesifik-domain)
5. [17-Stage Exploratory Data Analysis (EDA)](#5-17-stage-exploratory-data-analysis-eda)
6. [Arsitektur Model Machine Learning](#6-arsitektur-model-machine-learning)
7. [Metodologi Pelatihan & Validasi Walk-Forward](#7-metodologi-pelatihan--validasi-walk-forward)
8. [Landasan Matematis & Formulasi Ekonometrika](#8-landasan-matematis--formulasi-ekonometrika)
9. [Decision Support System (DSS) & Pemodelan Finansial](#9-decision-support-system-dss--pemodelan-finansial)
10. [Tech Stack & Desain Sistem](#10-tech-stack--desain-sistem)
11. [Panduan Instalasi & Eksekusi Lokal](#11-panduan-instalasi--eksekusi-lokal)
12. [Struktur Repositori](#12-struktur-repositori)
13. [Batasan Penelitian & Tata Kelola Data](#13-batasan-penelitian--tata-kelola-data)

---

## 1. Latar Belakang & Pernyataan Masalah

Pasar real estat Dubai merupakan salah satu pasar properti dengan pertumbuhan likuiditas global tercepat di dunia. Namun, investor institusional, pengelola aset (*family offices*), maupun pembeli internasional menghadapi **tiga asimetri informasi kritis**:

1. **Distorsi Valuasi & Spekulasi Listing**: Sulit membedakan secara objektif apakah harga penawaran suatu properti berada pada nilai wajar (*Fair Value*), diskon riil (*Undervalued*), atau markup spekulatif (*Overpriced*).
2. **Kesenjangan Yield Nyata vs Bruto**: Angka *gross rental yield* sering kali menyesatkan investor karena belum memperhitungkan biaya pemeliharaan (*service charges* per sqft), cadangan kekosongan (*vacancy allowance*), dan biaya registrasi pemerintah (DLD Fee 4%).
3. **Sensitivitas Utang & Risiko Makro**: Ketergantungan pembiayaan KPR terhadap suku bunga mengambang bank sentral (CBUAE) menciptakan kerentanan arus kas ketika terjadi kontraksi sewa atau lonjakan suku bunga acuan.

KHOR DXB dirancang sebagai platform analitik terpadu untuk menyelesaikan ketiga persoalan tersebut melalui pemodelan berbasis data empiris, inferensi kausal ekonometrika, dan algoritma *supervised machine learning*.

---

## 2. Arsitektur Solusi & 3 Pilar Platform

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           ❖ KHOR DXB CORE ENGINE                                │
├─────────────────────────┬─────────────────────────────┬─────────────────────────┤
│ PILAR 1: SPASIAL &      │ PILAR 2: AI VALUATION &     │ PILAR 3: INSTITUTIONAL  │
│ MAKRO EKONOMETRIKA      │ DEAL SCREENER               │ DECISION SUPPORT (DSS)  │
│                         │                             │                         │
│ • Pemetaan 62k+ listing │ • Dual-Ensemble AVM:        │ • Alokator Portofolio:  │
│ • Dekopling CBUAE Rate  │   - Resale (HistBoost R²=82)│   - Barbell Strategy    │
│ • Autokorelasi Moran's I│   - Off-Plan (RF R²=0.83)   │   - Golden Visa AED 2M  │
│ • Dekomposisi Hedonik   │ • Supervised Deal Screener: │ • Stress-Test Perbankan:│
│ • Supply Risk 2024-2028+│   - 95.35% Akurasi Holdout  │   - DSCR Debt Coverage  │
│ • 4 Klaster K-Means/PCA │   - ROC-AUC 0.9944          │   - Breakeven Drop      │
└─────────────────────────┴─────────────────────────────┴─────────────────────────┘
```

---

## 3. Sumber Dataset & Arsitektur Relasional

* **Tautan Sumber Resmi**: [Kaggle: Dubai Real Estate Sales and Rentals 2020–2026](https://www.kaggle.com/datasets/sergionefedov/dubai-real-estate-sales-and-rentals-20202026) (Kompilasi oleh Sergio Nefedov).
* **Entitas Asal**: Catatan resmi transaksi **Dubai Land Department (DLD)** dan listing pasar terbuka periode Januari 2020 hingga April 2026.
* **Integrasi Otomatis**: Dataset diunduh dan di-cache secara otomatis via `kagglehub` pada inisialisasi pertama.

### Spesifikasi 5 Tabel Relasional Terindeks

```
                         ┌───────────────────────────┐
                         │   metro_stations.csv      │
                         │   (49 stasiun, Red/Green) │
                         └─────────────┬─────────────┘
                                       │ Jarak Spasial
         ┌─────────────────────────────┼─────────────────────────────┐
         ▼                             ▼                             ▼
┌──────────────────┐          ┌──────────────────┐          ┌──────────────────┐
│ secondary_sales  │          │ off_plan.csv     │          │ rentals.csv      │
│ (49.641 baris)   │          │ (6.425 baris)    │          │ (6.319 baris)    │
│ Resale Siap Huni │          │ Proyek Konstruksi│          │ Sewa Tahunan/ST  │
└────────┬─────────┘          └────────┬─────────┘          └────────┬─────────┘
         │                             │                             │
         └─────────────────────────────┼─────────────────────────────┘
                                       ▼ Agregasi Spasial-Temporal
                         ┌───────────────────────────┐
                         │ area_prices_monthly.csv   │
                         │ (1.782 baris panel bulanan│
                         │ + CBUAE Base Rate %)      │
                         └───────────────────────────┘
```

| Berkas CSV | Baris | Granularitas | Kolom Kunci / Fitur | Kamus Data |
| :--- | :---: | :--- | :--- | :---: |
| [secondary_sales.csv](file:///c:/CODING/EDA/Dubai%20Real%20Estate%20(2020-2026)/secondary_sales.csv) | 49.641 | Transaksi unit siap huni (*resale*) | `price_usd`, `area_sqft`, `bedrooms`, `zone`, `view`, `condition`, `furnishing`, `is_freehold`, `to_burj_khalifa_km`, `metro_distance_min`, `year_built` | [Dokumentasi](file:///c:/CODING/EDA/Dubai%20Real%20Estate%20(2020-2026)/docs/data_dictionary/secondary_sales_Explanation.md) |
| [off_plan.csv](file:///c:/CODING/EDA/Dubai%20Real%20Estate%20(2020-2026)/off_plan.csv) | 6.425 | Listing proyek baru developer (*under-construction*) | `price_usd`, `developer`, `developer_tier`, `launch_year`, `handover_year`, `payment_plan`, `total_project_units`, `lat`, `lon` | [Dokumentasi](file:///c:/CODING/EDA/Dubai%20Real%20Estate%20(2020-2026)/docs/data_dictionary/off_plan_Explanation.md) |
| [rentals.csv](file:///c:/CODING/EDA/Dubai%20Real%20Estate%20(2020-2026)/rentals.csv) | 6.319 | Kontrak sewa aktif | `annual_rent_usd`, `contract_type` (*yearly* / *short_term*), `area_sqft`, `zone`, `rent_per_sqft_usd` | [Dokumentasi](file:///c:/CODING/EDA/Dubai%20Real%20Estate%20(2020-2026)/docs/data_dictionary/rentals_Explanation.md) |
| [area_prices_monthly.csv](file:///c:/CODING/EDA/Dubai%20Real%20Estate%20(2020-2026)/area_prices_monthly.csv) | 1.782 | Panel bulanan per komunitas | `year_month`, `community`, `secondary_price_per_sqft_usd`, `offplan_price_per_sqft_usd`, `rental_price_per_sqft_annual_usd`, `cbuae_base_rate_pct` | [Dokumentasi](file:///c:/CODING/EDA/Dubai%20Real%20Estate%20(2020-2026)/docs/data_dictionary/area_prices_monthly_Explanation.md) |
| [metro_stations.csv](file:///c:/CODING/EDA/Dubai%20Real%20Estate%20(2020-2026)/metro_stations.csv) | 49 | Jaringan transit publik | `station_name`, `line` (*Red* / *Green*), `lat`, `lon` | [Dokumentasi](file:///c:/CODING/EDA/Dubai%20Real%20Estate%20(2020-2026)/docs/data_dictionary/metro_stations_Explanation.md) |

---

## 4. Rekayasa Fitur Spesifik Domain

Semua rekayasa fitur diimplementasikan di [analytics_core.py](file:///c:/CODING/EDA/Dubai%20Real%20Estate%20(2020-2026)/analytics_core.py):

* **`property_age` & `is_brand_new`**: Menghitung usia depresiasi fisik properti (`listing_year - year_built`). Properti dengan usia $\le 1$ tahun diklasifikasikan sebagai properti baru tanpa diskon depresiasi fisik iklim gurun.
* **`floor_ratio` & `is_penthouse_tier`**: Mengukur elevasi vertikal unit terhadap total lantai gedung (`floor / total_floors`). Properti pada 2 lantai teratas dengan lantai $\ge 15$ diklasifikasikan sebagai unit *penthouse*.
* **`is_golden_visa_tier`**: Mengkodekan kepatuhan regulasi statutori imigrasi UEA pasca-Oktober 2022. Menandai properti bernilai $\ge \$544.500$ USD (setara $\text{AED } 2.000.000$) yang berhak mendapatkan visa residensi 10 tahun.
* **`implied_gross_yield_pct`**: Sintesis fundamental lintas tabel: menggabungkan median tarif sewa per distrik dan jumlah kamar dari `rentals.csv` ke setiap listing jual di `secondary_sales.csv` untuk menghasilkan estimasi *capitalization rate* sintetis.
* **`construction_lead_time` & `years_to_handover`**: Mengisolasi durasi pembangunan (`handover_year - launch_year`) dan sisa waktu tunggu penyelesaian proyek off-plan.

---

## 5. 17-Stage Exploratory Data Analysis (EDA)

Riset eksploratif dibagi ke dalam 4 pilar analisis komprehensif di [main.ipynb](file:///c:/CODING/EDA/Dubai%20Real%20Estate%20(2020-2026)/main.ipynb):

### I. Makro & Geografi Ekonomi
* **2.1 & 2.2 Sebaran Harga Distrik & Volume Transaksi**: Polarisasi tajam antara zona *Ultra-Luxury* (Palm Jumeirah, Downtown, Jumeirah Bay $> \$1.200$/sqft) vs zona likuiditas volume tinggi (Jumeirah Village Circle/JVC dan Business Bay).
* **2.3 Penggerak Nilai Properti**: Identifikasi korelasi luas lantai, kedekatan metro, dan fasilitas gedung terhadap nilai jual.
* **2.4 Pemetaan Geospasial**: Visualisasi koordinat listing yang ditumpangkan dengan rute Dubai Metro Red & Green lines serta inti Downtown Burj Khalifa.
* **2.5 Dekopling Suku Bunga Makro (CBUAE vs Real Estate)**: Analisis struktural yang membuktikan pasar properti Dubai tidak mengalami penurunan saat bank sentral menaikkan suku bunga dari ~1,5% ke >5,0%, didorong oleh dominasi pembeli tunai internasional non-leverage ($> 70\%$).
* **2.6 Kurva Peluruhan Jarak (*Distance Decay*)**: 
  - Penurunan harga eksponensial terhadap jarak Burj Khalifa (berkurang rata-rata $-4{,}55\%$ per km).
  - Penurunan harga linier terhadap waktu tempuh ke stasiun metro terdekat (berkurang $-0{,}33\%$ per menit).

### II. Struktur Hukum & Musiman Sewa
* **2.7 Uji Hipotesis Freehold vs Non-Freehold**: Uji *Welch's t-test* pada tingkat komunitas membuktikan premi freehold signifikan ($p < 0{,}001$), namun sebagian besar dipengaruhi oleh usia infrastruktur baru dan master-plan terintegrasi.
* **2.8 Musiman Kontrak Sewa (Short-Term vs Yearly)**: Kontrak sewa jangka pendek mencatatkan markup sewa rata-rata $+32\%$ pada musim puncak turisme musim dingin (November–Februari), namun terdiskon tajam pada musim panas (Juni–Agustus).
* **2.9 Divergensi Struktural Apartemen vs Villa**: Pertumbuhan harga villa pasca-2020 mengungguli apartemen sebesar $> 40\%$ akibat kelangkaan pasokan tanah horizontal di koridor utama.

### III. Fundamental Pengembang & Risiko Pasokan
* **2.10 Matriks Korelasi & Multikolinearitas**: Pemeriksaan interdependensi variabel penjelas.
* **2.11 Ekuitas Merek Developer (Tier 1 vs Tier 2)**: Diferensial harga mentah Tier 1 (Emaar, Nakheel) tercatat $+11{,}4\%$ pada apartemen dan $+31{,}9\%$ pada villa.
* **2.12 Analisis Net Rental Yield**: Perhitungan yield bersih pasca-pemotongan biaya pemeliharaan (*service charge* $\$4$/sqft) dan cadangan kekosongan ($5\%$). Koridor transit JVC dan Al Furjan menghasilkan net yield paling optimal ($6{,}8\% - 7{,}5\%$).
* **2.13 Kesenjangan Harga Off-Plan vs Resale**: Analisis premi peluncuran proyek baru terhadap unit siap huni di zona yang sama.
* **2.16 Horison Pipa Pasokan Off-Plan (2024–2028+)**: Identifikasi konsentrasi risiko pasokan baru yang memuncak pada tahun 2026 (3.773 unit) dan 2027 (2.845 unit) di Green Community dan Jumeirah 1.

### IV. Ekonometrika Spasial & Rekayasa Fitur
* **2.14 Autokorelasi Spasial (Global Moran's $I$)**: Pembuktian formal klasterisasi geografis ($I = 0{,}1584, z = 7{,}379, p = 0{,}00100$).
* **2.15 Dekomposisi Nilai Hedonik OLS**: Mengisolasi kontribusi marjinal tiap atribut fisik ($R^2 = 0{,}8315$).
* **2.17 Validasi Distribusi Fitur Rekayasa**: Pemeriksaan kestabilan fitur sintetis.

---

## 6. Arsitektur Model Machine Learning

```
                      ┌────────────────────────────────────────┐
                      │          EKOSISTEM MODEL AI            │
                      └──────────────────┬─────────────────────┘
         ┌───────────────────────────────┼───────────────────────────────┐
         ▼                               ▼                               ▼
┌──────────────────┐           ┌──────────────────┐           ┌──────────────────┐
│  CLASSIFICATION  │           │    CLUSTERING    │           │    REGRESSION    │
│ HistGradient-    │           │ K-Means (k=4)    │           │ • Resale AVM     │
│ Boosting Deal    │           │ + PCA Spatial    │           │ • Off-Plan RF    │
│ Screener (95.3%) │           │ Archetypes       │           │ • Prophet Trend  │
└──────────────────┘           └──────────────────┘           └──────────────────┘
```

### Matriks Kinerja & Benchmark Model

Semua model dievaluasi pada data uji holdout kronologis (20% data terbaru / 9.928 transaksi):

| Nama Model | Kategori Model | Arsitektur Algoritma | Metrik Utama (Holdout) | Baseline Pembanding |
| :--- | :--- | :--- | :--- | :--- |
| **Investment Deal Screener** | Supervised Classification | `HistGradientBoostingClassifier` | **Akurasi: 95,35%**<br>**Macro F1: 93,81%**<br>**ROC-AUC: 0,9944** | Dummy Stratified Classifier (Akurasi: 34,1%) |
| **Investor District Archetypes** | Unsupervised Clustering | `KMeans(k=4)` + `PCA(2 Comp)` | **Davies-Bouldin: 0,81**<br>**Silhouette: 0,44** | Random Spatial Partition |
| **Secondary Resale AVM** | Supervised Regression | `HistGradientBoostingRegressor` | **Holdout $R^2$: 0,825**<br>**MAPE: 21,9%**<br>**MdAPE: 15,6%** | Median Baseline (MAPE: 108,6%, $R^2$: -0,104) |
| **Off-Plan Project Estimator** | Supervised Regression | `RandomForestRegressor` | **Holdout $R^2$: 0,829**<br>**MAPE: 15,5%**<br>**PE20: 69,4%** | OLS Linier Sederhana ($R^2$: 0,612, MAPE: 39,8%) |
| **Macro City Price Trend** | Time-Series Forecasting | `Meta Prophet` | **RMSE: $48,20/sqft**<br>**MAPE: 8,4%** | Naive Persistence Model (MAPE: 12,1%) |
| **Hedonic Value Decomposition** | Inferensi Ekonometrika | `Statsmodels OLS` | **$R^2$: 0,8315**<br>**F-Stat: 2.148 ($p < 0{,}001$)** | Uncontrolled Mean Difference |

---

## 7. Metodologi Pelatihan & Validasi Walk-Forward

Untuk mencegah kebocoran data masa depan (*temporal lookahead leakage*), pemisahan data dilakukan secara ketat berdasarkan urutan waktu pendaftaran listing (`date_listed`):

* **Data Pelatihan (Train Split)**: 80% data kronologis awal (Januari 2020 s/d awal 2025; 39.713 baris).
* **Data Pengujian (Holdout Test Split)**: 20% data kronologis akhir (pertengahan 2025 s/d April 2026; 9.928 baris).

### Evaluasi Validasi Silang Ekspansi Waktu (`TimeSeriesSplit` 3-Fold)

```
Fold 1: [===== Train: 9.928 =====] -> [ Test: 9.928 ]                 | Akurasi: 84,88% | F1: 81,12%
Fold 2: [========== Train: 19.856 ==========] -> [ Test: 9.928 ]      | Akurasi: 91,10% | F1: 88,45%
Fold 3: [=============== Train: 29.784 ===============] -> [ Test ]   | Akurasi: 94,18% | F1: 92,30%
Final Holdout Evaluation (9.928 Unseen Latest Transactions)           | Akurasi: 95,35% | F1: 93,81%
```

Peningkatan performa yang konsisten pada setiap penambahan data latih membuktikan konvergensi model yang stabil dan bebas overfit.

---

## 8. Landasan Matematis & Formulasi Ekonometrika

### A. Autokorelasi Spasial — Global Moran's $I$

Menguji hipotesis nol ($H_0$) penyebaran harga acak vs klasterisasi spasial terstruktur:

$$I = \frac{N}{S_0} \frac{\sum_{i=1}^N \sum_{j=1}^N w_{ij} (x_i - \bar{x})(x_j - \bar{x})}{\sum_{i=1}^N (x_i - \bar{x})^2}$$

Di mana matriks pembobotan spasial $w_{ij}$ dihitung dari inversi jarak Euclidean antar-distrik:

$$w_{ij} = \frac{1}{d_{ij}} = \frac{1}{\sqrt{(\text{lat}_i - \text{lat}_j)^2 + (\text{lon}_i - \text{lon}_j)^2}} \quad (\forall i \neq j, \text{ dan } w_{ii} = 0)$$

$$S_0 = \sum_{i=1}^N \sum_{j=1}^N w_{ij}, \quad E[I] = -\frac{1}{N - 1} = -\frac{1}{25} = -0{,}0400$$

Uji signifikansi Monte Carlo (999 permutasi):

$$Z_I = \frac{I - E[I]}{\sqrt{\text{Var}(I)}} = \frac{+0{,}1584 - (-0{,}0400)}{0{,}0268} = \mathbf{+7{,}379} \quad (p = 0{,}00100)$$

*Menolak $H_0$ secara mutlak ($p < 0{,}001$). Terbukti bahwa harga properti di Dubai terklasterisasi kuat secara geografis.*

### B. Dekomposisi Hedonik Log-Linier & Semi-Elastisitas

Estimasi nilai marjinal implisit atribut fisik dan institusional:

$$\ln(P_i) = \beta_0 + \beta_1 \ln(\text{Area}_i) + \beta_2 \text{Beds}_i + \beta_3 \text{DistBurj}_i + \beta_4 \text{DistMetro}_i + \beta_5 \text{Age}_i + \beta_6 \text{FloorRatio}_i + \sum_{m} \gamma_m D_{im} + \epsilon_i$$

Untuk variabel dummy biner $D$, koefisien $\gamma$ dikonversi menjadi persentase premi harga murni menggunakan formulasi **Halvorsen-Palmquist**:

$$\% \Delta P = \left(e^{\gamma} - 1\right) \times 100\%$$

* **Status Kepemilikan Asing (Freehold)**: $\gamma = 0{,}5638 \implies (e^{0{,}5638} - 1) = \mathbf{+75{,}7\%}$
* **Pemandangan Tepi Air (Sea View)**: $\gamma = 0{,}2086 \implies (e^{0{,}2086} - 1) = \mathbf{+23{,}2\%}$
* **Pemandangan Ikonik Burj Khalifa**: $\gamma = 0{,}1807 \implies (e^{0{,}1807} - 1) = \mathbf{+19{,}8\%}$
* **Peluruhan Jarak Burj Khalifa**: $\beta_3 = -0{,}0455 \implies \mathbf{-4{,}55\% \text{ per km menjauh}}$
* **Peluruhan Akses Metro Transit**: $\beta_4 = -0{,}0033 \implies \mathbf{-0{,}33\% \text{ per menit tempuh menjauh}}$

### C. Amortisasi Utang KPR — Equated Monthly Installment (EMI)

$$M = P \times \frac{r(1 + r)^n}{(1 + r)^n - 1}$$

Di mana $P$ adalah pokok pinjaman bank, $r = \frac{\text{Suku Bunga Tahunan}}{12}$, dan $n = \text{Tenor (Tahun)} \times 12$.

### D. Rasio Perbankan Komersial — Debt Service Coverage Ratio (DSCR)

$$\text{DSCR} = \frac{\text{NOI}}{\text{Annual Debt Service}}$$

Di mana:
$$\text{NOI} = \text{Effective Rent} - \text{Annual Service Charges}$$
$$\text{Annual Debt Service} = M \times 12$$

*Ambang Batas Penilaian Risiko Institusional*:
- $\text{DSCR} \ge 1{,}25\times$: **Resilient (Investment Grade)** — Arus kas sangat aman terhadap siklus bunga.
- $1{,}00\times \le \text{DSCR} < 1{,}25\times$: **Marginal Buffer (Moderate Risk)** — Arus kas positif namun rentan.
- $\text{DSCR} < 1{,}00\times$: **Cash Deficit Warning (High Risk)** — Arus kas operasional gagal menutupi cicilan bank.

### E. Ambang Batas Penurunan Sewa Maksimal (Breakeven Rental Contraction)

$$\Delta \text{Rent}_{\text{BE}}\% = \left[ 1 - \frac{\text{Annual Debt Service} + \text{Annual Service Charges}}{\text{Gross Annual Rent} \times \left(1 - \frac{\text{Vacancy Rate}}{100}\right)} \right] \times 100\%$$

---

## 9. Decision Support System (DSS) & Pemodelan Finansial

Platform menyediakan 3 modul pendukung keputusan terintegrasi di [app.py](file:///c:/CODING/EDA/Dubai%20Real%20Estate%20(2020-2026)/app.py) (Modul 5):

```
[ MODUL PENGAMBILAN KEPUTUSAN INVESTASI (DSS) ]
 ├── 1. Buy-to-Let Single Modeler -> Amortisasi KPR, NOI, Waterfall Arus Kas, & Payback
 ├── 2. Strategic Allocator (DSS) -> Optimasi multi-aset, Golden Visa AED 2M, & Proyeksi 5 Tahun
 └── 3. Macro Stress Simulator    -> Uji guncangan bunga (+bps), drop sewa (%), & rasio DSCR
```

1. **Cash-Flow Waterfall Modeler**:
   Membongkar arus kas operasional tahunan:
   $$\text{Gross Potential Rent} \longrightarrow \text{Vacancy Allowance (5\%)} \longrightarrow \text{Service Charges} \longrightarrow \text{NOI} \longrightarrow \text{KPR Debt Service} \longrightarrow \text{Net Cash Flow}$$
2. **Algorithmic Multi-Asset Portfolio Allocator**:
   Mengalokasikan anggaran modal investor ($100k s/d $10M+) ke dalam 3 arketipe portofolio teroptimasi:
   - *Balanced Institutional Barbell (50/50)*: Net yield 5,70%, total ROI 5-tahun 57,3%, IRR 9,49%.
   - *Cash-Flow Maximizer (High Yield)*: Fokus JVC & Al Furjan, net yield 7,15%, total ROI 54,5%.
   - *Capital Growth & Prestige (Prime Core)*: Fokus Palm Jumeirah & Downtown, net yield 4,25%, total ROI 60,2%.
   - *Validasi Otomatis UAE Golden Visa*: Memverifikasi pemenuhan ekuitas statutori $\ge \text{AED } 2.000.000$ ($\approx \$544.500$ USD).
3. **Macroeconomic "What-If" Adverse Stress Testing**:
   Mensimulasikan skenario guncangan moneter (lonjakan suku bunga $+50$ s/d $+300$ bps dan kontraksi pasar sewa $-5\%$ s/d $-30\%$) dengan menghasilkan vonis risiko kredit perbankan berbasis rasio DSCR.

---

## 10. Tech Stack & Desain Sistem

* **Bahasa & Runtime**: Python 3.11.x
* **Data Science & ML**: `scikit-learn`, `statsmodels`, `prophet`, `scipy`, `pandas`, `numpy`
* **Visualisasi & Geospasial**: `plotly`, `matplotlib`, `seaborn`, `MapLibre GL`, ubin peta `OpenFreeMap` & `ESRI Canvas`
* **Arsitektur Dashboard**: `streamlit` dengan custom CSS injection
* **Design System Token (Institutional Dark Luxury)**:
  - Latar Belakang: `--bg-main: #090d16`, `--bg-card: #111726`
  - Aksen Mewah: `--gold-primary: #c5a880`, `--sky-transit: #38bdf8`
  - Sinyal Risiko Finansial: `--emerald-alpha: #10b981`, `--crimson-risk: #ef4444`
* **Optimasi Performa**: Implementasi *lazy loading* pada library ekonometrika berat (`statsmodels`), memangkas waktu start aplikasi dari ~16 detik menjadi $< 0{,}5$ detik.

---

## 11. Panduan Instalasi & Eksekusi Lokal

### Prasyarat Sistem
- Python 3.10 atau 3.11 (direkomendasikan Python 3.11)
- Git & PowerShell (Windows) atau Terminal Bash (macOS/Linux)

### Langkah Eksekusi

```powershell
# 1. Kloning repositori proyek
git clone https://github.com/fathir-hub/dubai-real-estate-intelligence.git
cd "Dubai Real Estate (2020-2026)"

# 2. Buat dan aktifkan virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1    # Pada Linux/macOS: source .venv/bin/activate

# 3. Instal dependensi library
pip install -r requirements.txt

# 4. Jalankan platform dashboard interaktif
streamlit run app.py
```

Dashboard akan otomatis terbuka pada peramban web di alamat `http://localhost:8501`.

### Menjalankan Jupyter Notebook Riset

Buka berkas [main.ipynb](file:///c:/CODING/EDA/Dubai%20Real%20Estate%20(2020-2026)/main.ipynb) di VS Code atau Jupyter Lab. Seluruh 80 sel kode telah divalidasi dan dapat dieksekusi secara berurutan dari atas ke bawah (*Run All*) tanpa error.

---

## 12. Struktur Repositori

```text
Dubai Real Estate (2020-2026)/
├── analytics_core.py                  # Single source of truth: kalkulasi ekonometrika, ML, & finansial
├── app.py                             # Frontend platform intelijen Streamlit (7 modul alur kerja)
├── main.ipynb                         # Notebook riset end-to-end (EDA, Moran's I, OLS, AVM, & DSS)
├── requirements.txt                   # Manifest dependensi pustaka Python
├── LICENSE                            # Lisensi sumber terbuka MIT
├── models/                            # Artefak serialisasi model Scikit-Learn (.joblib & .csv)
│   ├── investment_deal_classifier.joblib  # Classifier HistGradientBoosting (Akurasi 95,35%)
│   ├── secondary_valuation_model.joblib   # Regressor AVM Resale Sekunder
│   ├── offplan_valuation_package.joblib   # Regressor Random Forest Off-Plan
│   └── zone_clusters.csv                  # Taksonomi klaster distrik K-Means (k=4) + PCA
├── plots/                             # Galeri grafik ekonometrika resolusi publikasi (300 DPI)
│   ├── spatial_moran_hotspots.png
│   ├── hedonic_marginal_elasticities.png
│   ├── offplan_handover_supply_pipeline.png
│   ├── engineered_features_distribution.png
│   ├── classification_confusion_matrix.png
│   ├── classification_roc_curves.png
│   ├── classification_time_series_cv.png
│   ├── classification_feature_importance.png
│   └── dss_portfolio_and_stress_simulation.png
└── docs/                              # Kamus data bilingual resmi (5 tabel relasional DLD)
    └── data_dictionary/
        ├── area_prices_monthly_Explanation.md
        ├── metro_stations_Explanation.md
        ├── off_plan_Explanation.md
        ├── rentals_Explanation.md
        └── secondary_sales_Explanation.md
```

---

## 13. Batasan Penelitian & Tata Kelola Data

1. **Harga Penawaran vs Harga Akta Selesai**: Dataset bersumber dari listing pasar terbuka dan agregasi DLD. Nilai yang disajikan mencerminkan dinamika penawaran pasar aktif dan bukan merupakan jaminan akta resmi notaris pemerintah.
2. **Keterbatasan Peramalan Deret Waktu**: Proyeksi Meta Prophet mengekstrapolasi pola musiman historis 2020–2026 dan tidak memprediksi guncangan geopolitik tak terduga (*black-swan events*) atau perubahan drastis regulasi perpajakan.
3. **Penyangkalan Finansial**: Metrik yield dan simulasi DSCR ditujukan untuk analisis kuantitatif profesional dan pengujian skenario portofolio, bukan merupakan nasihat keuangan legal atau investasi perseorangan mengikat.

---

**Author**: Fathir  
**Platform**: KHOR DXB Real Estate Intelligence & Decision Support  
**Tahun Rilis**: 2026 | **Lisensi**: MIT License
