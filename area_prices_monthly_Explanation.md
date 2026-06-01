# Area Prices Monthly Dataset Explanation

## Dataset Overview

### English

This dataset contains monthly real estate market indicators for Dubai communities. Each row represents one community in one month, with information about secondary market prices, off-plan prices, rental prices, listing volumes, freehold status, and mortgage-related macroeconomic conditions.

Unlike the listing-level datasets, this file is already aggregated at the community-month level. It is especially useful for market trend analysis, price movement comparison, supply and demand monitoring, rental yield approximation, and forecasting.

### Bahasa Indonesia

Dataset ini berisi indikator pasar real estate bulanan untuk komunitas-komunitas di Dubai. Setiap baris merepresentasikan satu komunitas pada satu bulan tertentu, dengan informasi harga pasar sekunder, harga off-plan, harga rental, volume listing, status freehold, dan kondisi makroekonomi terkait suku bunga KPR.

Berbeda dari dataset listing-level, file ini sudah berbentuk agregasi pada level komunitas-bulanan. Dataset ini sangat cocok untuk analisis tren pasar, perbandingan pergerakan harga, monitoring supply dan demand, estimasi rental yield, serta forecasting.

## Dataset Structure

- Rows: 6,384
- Columns: 13
- Time range: 2020-01 to 2026-04
- Aggregation level: community by month
- Main time column: `year_month`
- Main price metrics: `secondary_price_per_sqft_usd`, `offplan_price_per_sqft_usd`, `rental_price_per_sqft_annual_usd`
- Main volume metrics: `n_listings_secondary`, `n_listings_offplan`, `n_listings_rental`

## Column Explanation

| Column | Data Type | English Explanation | Penjelasan Bahasa Indonesia | Analysis Notes |
| --- | --- | --- | --- | --- |
| `year_month` | Date/String | Observation month in YYYY-MM format. | Bulan observasi dalam format YYYY-MM. | Convert to datetime or monthly period for time series analysis. |
| `community` | String | Specific Dubai community or neighborhood represented in the monthly observation. | Komunitas atau kawasan spesifik di Dubai yang direpresentasikan dalam observasi bulanan. | Useful for community-level trend comparison. |
| `zone` | String | Broader district or geographic zone containing the community. | Zona atau distrik yang lebih luas dari komunitas tersebut. | Useful for aggregated zone-level market analysis. |
| `is_freehold` | Boolean | Indicates whether the community allows full property ownership by foreign buyers. | Menunjukkan apakah komunitas tersebut mengizinkan kepemilikan penuh oleh pembeli asing. | Freehold areas may behave differently due to investor demand. |
| `secondary_price_per_sqft_usd` | Integer | Average secondary market resale price per square foot in US dollars for that community and month. | Rata-rata harga resale pasar sekunder per kaki persegi dalam dolar AS untuk komunitas dan bulan tersebut. | Key metric for tracking resale price trends. |
| `secondary_price_per_m2_usd` | Integer | Average secondary market resale price per square meter in US dollars for that community and month. | Rata-rata harga resale pasar sekunder per meter persegi dalam dolar AS untuk komunitas dan bulan tersebut. | International equivalent of secondary price per square foot. |
| `offplan_price_per_sqft_usd` | Float | Average off-plan property price per square foot in US dollars for that community and month. | Rata-rata harga properti off-plan per kaki persegi dalam dolar AS untuk komunitas dan bulan tersebut. | Contains missing values where off-plan activity may be unavailable or not recorded. |
| `rental_price_per_sqft_annual_usd` | Integer | Average annual rental price per square foot in US dollars for that community and month. | Rata-rata harga sewa tahunan per kaki persegi dalam dolar AS untuk komunitas dan bulan tersebut. | Useful for rent trend analysis and approximate rental yield calculations. |
| `n_listings_secondary` | Integer | Number of active secondary sale listings in the community during the month. | Jumlah listing aktif penjualan pasar sekunder di komunitas tersebut pada bulan itu. | Proxy for secondary market supply. |
| `n_listings_offplan` | Integer | Number of active off-plan listings in the community during the month. | Jumlah listing aktif off-plan di komunitas tersebut pada bulan itu. | Proxy for new development or off-plan supply. |
| `n_listings_rental` | Integer | Number of active rental listings in the community during the month. | Jumlah listing aktif rental di komunitas tersebut pada bulan itu. | Proxy for rental market supply. |
| `cbuae_base_rate_pct` | Float | Central Bank of the UAE base interest rate in percent during the observation period. | Suku bunga dasar Central Bank of the UAE dalam persen pada periode observasi. | Useful for studying macroeconomic effects on property prices. |
| `avg_mortgage_rate_pct` | Float | Average mortgage interest rate in percent during the observation period. | Rata-rata suku bunga KPR dalam persen pada periode observasi. | Can be used to analyze financing affordability and price movement. |

## Suggested Analysis Questions

### English

1. How did Dubai secondary market prices change from 2020 to 2026?
2. Which communities experienced the strongest price growth?
3. Which zones have the highest average secondary price per square foot?
4. How do off-plan prices compare with secondary market prices over time?
5. Which communities have the highest annual rent per square foot?
6. How did rental prices move compared with sale prices?
7. Are listing volumes increasing or decreasing across market segments?
8. Do freehold communities have higher prices or stronger price growth?
9. How do mortgage rates relate to property price trends?
10. Which communities show attractive rental yield potential based on rent and sale price per square foot?
11. Can monthly price trends be used to forecast future market movement?

### Bahasa Indonesia

1. Bagaimana perubahan harga pasar sekunder Dubai dari 2020 sampai 2026?
2. Komunitas mana yang mengalami pertumbuhan harga paling kuat?
3. Zona mana yang memiliki rata-rata harga sekunder per kaki persegi tertinggi?
4. Bagaimana perbandingan harga off-plan dengan harga pasar sekunder dari waktu ke waktu?
5. Komunitas mana yang memiliki harga sewa tahunan per kaki persegi tertinggi?
6. Bagaimana pergerakan harga sewa dibandingkan dengan harga jual?
7. Apakah volume listing meningkat atau menurun di setiap segmen pasar?
8. Apakah komunitas freehold memiliki harga atau pertumbuhan harga yang lebih tinggi?
9. Bagaimana hubungan suku bunga KPR dengan tren harga properti?
10. Komunitas mana yang menunjukkan potensi rental yield menarik berdasarkan harga sewa dan harga jual per kaki persegi?
11. Apakah tren harga bulanan dapat digunakan untuk memprediksi pergerakan pasar ke depan?

## Useful Derived Features

### English

You can create additional features from this dataset:

| Derived Feature | Formula / Idea | Purpose |
| --- | --- | --- |
| `year` | Extract year from `year_month` | Yearly trend comparison |
| `month` | Extract month from `year_month` | Seasonality analysis |
| `secondary_yoy_growth_pct` | Year-over-year change in `secondary_price_per_sqft_usd` | Measures annual resale price growth |
| `rental_yoy_growth_pct` | Year-over-year change in `rental_price_per_sqft_annual_usd` | Measures annual rental growth |
| `offplan_secondary_gap_pct` | `(offplan_price_per_sqft_usd - secondary_price_per_sqft_usd) / secondary_price_per_sqft_usd * 100` | Measures off-plan premium or discount |
| `rental_yield_proxy_pct` | `rental_price_per_sqft_annual_usd / secondary_price_per_sqft_usd * 100` | Approximate gross rental yield |
| `total_listings` | Sum of secondary, off-plan, and rental listings | Overall market activity proxy |
| `sales_listing_share` | Secondary listings divided by total listings | Segment supply mix |

### Bahasa Indonesia

Kamu bisa membuat fitur tambahan dari dataset ini:

| Fitur Turunan | Formula / Ide | Tujuan |
| --- | --- | --- |
| `year` | Ekstrak tahun dari `year_month` | Perbandingan tren tahunan |
| `month` | Ekstrak bulan dari `year_month` | Analisis musiman |
| `secondary_yoy_growth_pct` | Perubahan year-over-year dari `secondary_price_per_sqft_usd` | Mengukur pertumbuhan tahunan harga resale |
| `rental_yoy_growth_pct` | Perubahan year-over-year dari `rental_price_per_sqft_annual_usd` | Mengukur pertumbuhan tahunan harga rental |
| `offplan_secondary_gap_pct` | `(offplan_price_per_sqft_usd - secondary_price_per_sqft_usd) / secondary_price_per_sqft_usd * 100` | Mengukur premium atau diskon off-plan |
| `rental_yield_proxy_pct` | `rental_price_per_sqft_annual_usd / secondary_price_per_sqft_usd * 100` | Estimasi kasar gross rental yield |
| `total_listings` | Jumlah listing secondary, off-plan, dan rental | Proxy aktivitas pasar keseluruhan |
| `sales_listing_share` | Listing secondary dibagi total listing | Komposisi supply berdasarkan segmen |

## Important Notes

### English

- This dataset is aggregated monthly, so it is better for market trends than individual property-level analysis.
- `offplan_price_per_sqft_usd` contains missing values. These may indicate months or communities without off-plan activity or unavailable off-plan pricing.
- `price_per_sqft` metrics are generally better than total price for comparing areas because they control for property size differences.
- `rental_price_per_sqft_annual_usd` can be compared with `secondary_price_per_sqft_usd` to create a rough rental yield proxy, but it should not be treated as exact investment return.
- Mortgage rates and CBUAE base rates are macro indicators. They can help explain broad market movement but may not explain all community-level differences.
- The dataset documentation states that listing-level data in the broader dataset is generated using a hedonic pricing model. Therefore, analysis should be framed as exploratory and model-based, not as official transaction-level proof.

### Bahasa Indonesia

- Dataset ini sudah diagregasi secara bulanan, sehingga lebih cocok untuk analisis tren pasar daripada analisis detail per properti individu.
- `offplan_price_per_sqft_usd` memiliki missing value. Ini dapat menunjukkan bulan atau komunitas tanpa aktivitas off-plan atau harga off-plan yang tidak tersedia.
- Metrik `price_per_sqft` umumnya lebih baik daripada total harga untuk membandingkan area karena sudah mengontrol perbedaan ukuran properti.
- `rental_price_per_sqft_annual_usd` dapat dibandingkan dengan `secondary_price_per_sqft_usd` untuk membuat proxy rental yield kasar, tetapi tidak boleh dianggap sebagai return investasi yang presisi.
- Suku bunga KPR dan CBUAE base rate adalah indikator makro. Keduanya dapat membantu menjelaskan pergerakan pasar secara luas, tetapi belum tentu menjelaskan semua perbedaan antar komunitas.
- Dokumentasi dataset menyebutkan bahwa data listing-level pada dataset yang lebih luas dibuat menggunakan hedonic pricing model. Jadi, analisis sebaiknya diposisikan sebagai eksplorasi berbasis model, bukan bukti resmi transaksi aktual.
