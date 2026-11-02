# Metro Stations Dataset Explanation

## Dataset Overview

### English

This dataset contains information about Dubai Metro stations, including station names, metro lines, geographic coordinates, opening years, and distance to Burj Khalifa. Unlike the sales and rental datasets, this file is mainly a supporting location dataset. It is useful for analyzing transport accessibility and connecting real estate listings with nearby metro infrastructure.

The dataset can be used to study the spatial distribution of metro stations, compare Red Line and Green Line coverage, evaluate accessibility to central Dubai, and analyze whether proximity to metro stations is associated with higher property prices or rents.

### Bahasa Indonesia

Dataset ini berisi informasi tentang stasiun Dubai Metro, termasuk nama stasiun, jalur metro, koordinat geografis, tahun pembukaan, dan jarak ke Burj Khalifa. Berbeda dari dataset sales dan rental, file ini lebih berfungsi sebagai dataset pendukung lokasi. Dataset ini berguna untuk menganalisis akses transportasi dan menghubungkan listing properti dengan infrastruktur metro terdekat.

Dataset ini dapat digunakan untuk mempelajari distribusi spasial stasiun metro, membandingkan cakupan Red Line dan Green Line, mengevaluasi aksesibilitas ke pusat Dubai, serta menganalisis apakah kedekatan dengan stasiun metro berkaitan dengan harga properti atau harga sewa yang lebih tinggi.

## Dataset Structure

- Rows: 55
- Columns: 6
- Metro lines: Red and Green
- Opening years: 2009 to 2021
- Main location fields: `lat`, `lon`
- Centrality metric: `to_burj_khalifa_km`

## Column Explanation

| Column | Data Type | English Explanation | Penjelasan Bahasa Indonesia | Analysis Notes |
| --- | --- | --- | --- | --- |
| `station_name` | String | Name of the Dubai Metro station. | Nama stasiun Dubai Metro. | Can be used to join or compare with the nearest metro station field in property datasets. |
| `line` | String | Metro line where the station is located, such as Red or Green. | Jalur metro tempat stasiun berada, seperti Red atau Green. | Useful for comparing accessibility by metro corridor. |
| `lat` | Float | Latitude coordinate of the metro station. | Koordinat latitude dari stasiun metro. | Useful for mapping stations and calculating spatial distance. |
| `lon` | Float | Longitude coordinate of the metro station. | Koordinat longitude dari stasiun metro. | Useful for mapping stations and calculating spatial distance. |
| `year_opened` | Integer | Year when the metro station opened. | Tahun ketika stasiun metro mulai beroperasi. | Useful for analyzing transport infrastructure expansion over time. |
| `to_burj_khalifa_km` | Float | Distance from the metro station to Burj Khalifa in kilometers. | Jarak stasiun metro ke Burj Khalifa dalam kilometer. | Can be used as a centrality proxy for each station. |

## Suggested Analysis Questions

### English

1. How are Dubai Metro stations distributed across the city?
2. Which metro line has more stations in the dataset?
3. Which stations are closest to Burj Khalifa?
4. Which stations are farthest from Dubai's central core?
5. How did Dubai Metro coverage expand by opening year?
6. Do properties near Red Line stations have different prices than properties near Green Line stations?
7. Does metro proximity increase rental or resale property value?
8. Which communities have strong metro accessibility?

### Bahasa Indonesia

1. Bagaimana distribusi stasiun Dubai Metro di seluruh kota?
2. Jalur metro mana yang memiliki jumlah stasiun lebih banyak dalam dataset?
3. Stasiun mana yang paling dekat dengan Burj Khalifa?
4. Stasiun mana yang paling jauh dari pusat utama Dubai?
5. Bagaimana perkembangan cakupan Dubai Metro berdasarkan tahun pembukaan?
6. Apakah properti dekat stasiun Red Line memiliki harga berbeda dari properti dekat Green Line?
7. Apakah kedekatan dengan metro meningkatkan harga jual atau harga sewa properti?
8. Komunitas mana yang memiliki akses metro yang kuat?

## How To Use With Property Datasets

### English

This dataset can be combined with `secondary_sales.csv`, `rentals.csv`, and `off_plan.csv` using station-related fields such as `metro_station` and `metro_line`. For example, you can compare property prices by nearest metro line or enrich real estate listings with station opening year and station distance to Burj Khalifa.

Possible joins:

- `metro_stations.station_name` with property dataset `metro_station`
- `metro_stations.line` with property dataset `metro_line`

### Bahasa Indonesia

Dataset ini dapat digabungkan dengan `secondary_sales.csv`, `rentals.csv`, dan `off_plan.csv` menggunakan kolom terkait stasiun seperti `metro_station` dan `metro_line`. Misalnya, kamu bisa membandingkan harga properti berdasarkan jalur metro terdekat atau menambahkan informasi tahun pembukaan stasiun dan jarak stasiun ke Burj Khalifa ke dataset properti.

Kemungkinan join:

- `metro_stations.station_name` dengan kolom `metro_station` pada dataset properti
- `metro_stations.line` dengan kolom `metro_line` pada dataset properti

## Important Notes

### English

- This dataset is not a property listing dataset. It is a supporting geographic and transportation dataset.
- `to_burj_khalifa_km` measures distance from the station to Burj Khalifa, not from a property to Burj Khalifa.
- When joining with property datasets, check station name consistency to avoid unmatched records caused by spelling differences.
- Metro accessibility should be interpreted as one factor among many. Property prices are also influenced by community, property type, size, view, developer, furnishing, and market timing.
- Latitude and longitude can support map-based analysis, but exact travel time may differ from straight-line distance.

### Bahasa Indonesia

- Dataset ini bukan dataset listing properti. Dataset ini berfungsi sebagai pendukung geografis dan transportasi.
- `to_burj_khalifa_km` mengukur jarak dari stasiun ke Burj Khalifa, bukan jarak dari properti ke Burj Khalifa.
- Saat melakukan join dengan dataset properti, cek konsistensi nama stasiun agar tidak ada record yang gagal cocok karena perbedaan penulisan.
- Akses metro sebaiknya dipahami sebagai salah satu faktor saja. Harga properti juga dipengaruhi oleh komunitas, tipe properti, ukuran, view, developer, furnishing, dan waktu pasar.
- Latitude dan longitude dapat mendukung analisis berbasis peta, tetapi waktu tempuh aktual bisa berbeda dari jarak garis lurus.
