# Secondary Sales Dataset Explanation

## Dataset Overview

### English

This dataset contains listing-level data for Dubai secondary market property sales. The secondary market refers to resale properties that are already owned and are being sold again, rather than newly launched off-plan units. Each row represents one property listing with information about location, property characteristics, building attributes, accessibility, pricing, and mortgage conditions at the time of listing.

The dataset can be used to analyze resale property prices, identify pricing drivers, compare communities and zones, study the effect of metro accessibility, and build predictive models for property values.

### Bahasa Indonesia

Dataset ini berisi data listing properti di pasar sekunder Dubai. Pasar sekunder berarti properti yang sudah pernah dimiliki lalu dijual kembali, bukan unit off-plan atau proyek baru yang belum selesai dibangun. Setiap baris merepresentasikan satu listing properti dengan informasi lokasi, karakteristik properti, atribut bangunan, aksesibilitas, harga, dan kondisi suku bunga KPR pada saat listing dibuat.

Dataset ini dapat digunakan untuk menganalisis harga properti resale, mengidentifikasi faktor yang memengaruhi harga, membandingkan komunitas dan zona, melihat pengaruh akses metro, serta membangun model prediksi nilai properti.

## Dataset Structure

- Rows: 50,000
- Columns: 29
- Date range: 2020-01-01 to 2026-04-29
- Main price target: `price_usd`
- Normalized price metrics: `price_per_sqft_usd`, `price_per_m2_usd`

## Column Explanation

| Column | Data Type | English Explanation | Penjelasan Bahasa Indonesia | Analysis Notes |
| --- | --- | --- | --- | --- |
| `id` | String | Unique identifier for each property listing. | ID unik untuk setiap listing properti. | Useful as a row identifier, not usually used as a predictive feature. |
| `date_listed` | Date/String | Date when the property was listed for sale. | Tanggal saat properti dipasang sebagai listing penjualan. | Can be converted to datetime for trend analysis by month or year. |
| `community` | String | Specific community or neighborhood where the property is located. | Komunitas atau kawasan spesifik tempat properti berada. | Important for location-based price comparison. |
| `zone` | String | Broader district or geographic zone containing the community. | Zona atau distrik yang lebih luas dari komunitas properti. | Useful for aggregated market analysis. |
| `is_freehold` | Boolean | Indicates whether the area allows full property ownership by foreign buyers. | Menunjukkan apakah area tersebut mengizinkan kepemilikan penuh oleh pembeli asing. | Freehold areas may attract stronger investor demand. |
| `lat` | Float | Latitude coordinate of the property location. | Koordinat latitude dari lokasi properti. | Useful for mapping and spatial analysis. |
| `lon` | Float | Longitude coordinate of the property location. | Koordinat longitude dari lokasi properti. | Useful for mapping and spatial analysis. |
| `property_category` | String | General property category, such as apartment or villa. | Kategori umum properti, seperti apartemen atau vila. | Major segmentation variable because apartments and villas behave differently. |
| `property_type` | String | More specific property type or bedroom configuration, such as studio, 1BR, 2BR, villa, or penthouse. | Tipe properti yang lebih spesifik atau konfigurasi kamar, seperti studio, 1BR, 2BR, vila, atau penthouse. | Useful for comparing similar property formats. |
| `bedrooms` | Integer | Number of bedrooms in the property. Studio units are usually represented as 0 bedrooms. | Jumlah kamar tidur dalam properti. Unit studio biasanya direpresentasikan sebagai 0 kamar tidur. | Strong driver of total price and property size. |
| `area_sqft` | Integer | Property area measured in square feet. | Luas properti dalam satuan kaki persegi. | Dubai commonly uses square feet for property size. |
| `area_m2` | Float | Property area measured in square meters. | Luas properti dalam satuan meter persegi. | Useful for international comparison. |
| `floor` | Float | Floor number where the unit is located. Mostly relevant for apartments. | Nomor lantai tempat unit berada. Biasanya relevan untuk apartemen. | Contains missing values, especially for villas where floor level may not apply. |
| `total_floors` | Float | Total number of floors in the building. Mostly relevant for apartment buildings. | Jumlah total lantai dalam bangunan. Biasanya relevan untuk gedung apartemen. | Contains missing values where building height is not applicable or unavailable. |
| `year_built` | Integer | Year when the property or building was completed. | Tahun ketika properti atau bangunan selesai dibangun. | Can be used to estimate property age. |
| `view` | String | Main view associated with the property, such as sea, marina, city, park, golf course, pool, community, or Burj Khalifa. | Pemandangan utama dari properti, seperti laut, marina, kota, taman, lapangan golf, kolam, komunitas, atau Burj Khalifa. | Premium views may increase property value. |
| `furnishing` | String | Furnishing status of the property, such as unfurnished, semi-furnished, or fully furnished. | Status perabot properti, seperti tanpa perabot, semi-furnished, atau fully furnished. | Furnishing can affect asking price and buyer appeal. |
| `condition` | String | Listing or occupancy condition, such as vacant on transfer, tenanted, or off-plan resale. | Kondisi listing atau okupansi, seperti kosong saat transfer, sedang disewa, atau resale off-plan. | Can affect liquidity and buyer preference. |
| `parking_spaces` | Integer | Number of parking spaces included with the property. | Jumlah tempat parkir yang termasuk dalam properti. | More parking spaces may increase value, especially for larger units. |
| `chiller_included` | Boolean | Indicates whether cooling or air-conditioning charges are included. | Menunjukkan apakah biaya pendingin udara atau chiller sudah termasuk. | May influence attractiveness and ownership cost. |
| `metro_station` | String | Nearest Dubai Metro station to the property. | Stasiun Dubai Metro terdekat dari properti. | Useful for accessibility analysis. |
| `metro_line` | String | Metro line associated with the nearest station, such as Red or Green. | Jalur metro dari stasiun terdekat, seperti Red atau Green. | Can help compare areas by transport corridor. |
| `metro_distance_min` | Integer | Estimated travel time in minutes to the nearest metro station. | Estimasi waktu tempuh dalam menit ke stasiun metro terdekat. | Lower values usually indicate better accessibility. |
| `metro_distance_type` | String | Travel mode used for the metro distance estimate, such as walk or drive. | Jenis perjalanan yang digunakan untuk estimasi jarak metro, seperti jalan kaki atau berkendara. | Important because walking and driving distances are not directly equivalent. |
| `to_burj_khalifa_km` | Float | Distance from the property to Burj Khalifa in kilometers. | Jarak properti ke Burj Khalifa dalam kilometer. | Proxy for centrality and proximity to Dubai's prime core. |
| `price_usd` | Integer | Total listed sale price of the property in US dollars. | Total harga jual listing properti dalam dolar AS. | Main target variable for price analysis or prediction. |
| `price_per_sqft_usd` | Integer | Sale price per square foot in US dollars. | Harga jual per kaki persegi dalam dolar AS. | Better than total price for comparing properties of different sizes. |
| `price_per_m2_usd` | Integer | Sale price per square meter in US dollars. | Harga jual per meter persegi dalam dolar AS. | International equivalent of price per square foot. |
| `mortgage_rate_at_listing` | Float | Mortgage interest rate at the time the property was listed. | Suku bunga KPR pada saat properti dipasang sebagai listing. | Useful for studying the relationship between financing conditions and property prices. |

## Suggested Analysis Questions

### English

1. Which Dubai zones and communities have the highest average resale price per square foot?
2. Do freehold areas have higher property prices than non-freehold areas?
3. How does distance to Burj Khalifa relate to property prices?
4. Does metro accessibility affect resale property values?
5. Which property characteristics create the strongest price premiums?
6. How do apartments and villas differ in price behavior?
7. How did resale prices change from 2020 to 2026?
8. Is there a visible relationship between mortgage rates and listing prices?

### Bahasa Indonesia

1. Zona dan komunitas mana di Dubai yang memiliki harga resale per kaki persegi tertinggi?
2. Apakah area freehold memiliki harga properti lebih tinggi dibanding area non-freehold?
3. Bagaimana hubungan jarak ke Burj Khalifa dengan harga properti?
4. Apakah akses ke metro memengaruhi nilai properti resale?
5. Karakteristik properti apa yang memberikan premium harga paling besar?
6. Bagaimana perbedaan perilaku harga antara apartemen dan vila?
7. Bagaimana perubahan harga resale dari 2020 sampai 2026?
8. Apakah ada hubungan yang terlihat antara suku bunga KPR dan harga listing?

## Important Notes

### English

- `price_usd` is useful for total market value analysis, but `price_per_sqft_usd` is usually better for fair comparison across different property sizes.
- `floor` and `total_floors` have missing values because those fields are mainly relevant for apartments and high-rise buildings.
- `metro_distance_min` should be interpreted together with `metro_distance_type`, because walking time and driving time are different accessibility measures.
- The dataset documentation states that listing-level characteristics are generated using a hedonic pricing model. Therefore, analysis should be framed as exploratory and model-based, not as official transaction-level proof.

### Bahasa Indonesia

- `price_usd` berguna untuk analisis total nilai properti, tetapi `price_per_sqft_usd` biasanya lebih adil untuk membandingkan properti dengan ukuran berbeda.
- `floor` dan `total_floors` memiliki missing value karena kolom tersebut lebih relevan untuk apartemen dan gedung tinggi.
- `metro_distance_min` sebaiknya dibaca bersama `metro_distance_type`, karena waktu jalan kaki dan waktu berkendara adalah ukuran aksesibilitas yang berbeda.
- Dokumentasi dataset menyebutkan bahwa karakteristik listing-level dibuat menggunakan hedonic pricing model. Jadi, analisis sebaiknya diposisikan sebagai eksplorasi berbasis model, bukan bukti resmi transaksi aktual.
