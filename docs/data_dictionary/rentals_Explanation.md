# Rentals Dataset Explanation

## Dataset Overview

### English

This dataset contains listing-level data for rental properties in Dubai. Each row represents one rental listing with information about location, property characteristics, accessibility, lease conditions, and rental prices. The dataset covers both apartments and villas across different communities and zones.

The dataset can be used to analyze rental market trends, compare rental prices across locations, study affordability, examine the impact of furnishing and amenities, and build models to estimate rental value.

### Bahasa Indonesia

Dataset ini berisi data listing properti sewa di Dubai. Setiap baris merepresentasikan satu listing rental dengan informasi lokasi, karakteristik properti, aksesibilitas, kondisi sewa, dan harga sewa. Dataset ini mencakup apartemen dan vila di berbagai komunitas serta zona.

Dataset ini dapat digunakan untuk menganalisis tren pasar rental, membandingkan harga sewa antar lokasi, mempelajari affordability, melihat pengaruh furnishing dan fasilitas, serta membangun model estimasi nilai sewa.

## Dataset Structure

- Rows: 25,000
- Columns: 24
- Date range: 2021-01-01 to 2026-04-29
- Main rent target: `annual_rent_usd`
- Normalized rent metrics: `rent_per_sqft_usd`, `rent_per_m2_usd`

## Column Explanation

| Column | Data Type | English Explanation | Penjelasan Bahasa Indonesia | Analysis Notes |
| --- | --- | --- | --- | --- |
| `id` | String | Unique identifier for each rental listing. | ID unik untuk setiap listing rental. | Useful as a row identifier, not usually used as an analytical feature. |
| `date_listed` | Date/String | Date when the rental property was listed. | Tanggal saat properti sewa dipasang sebagai listing. | Can be converted to datetime for monthly or yearly rental trend analysis. |
| `community` | String | Specific community or neighborhood where the rental property is located. | Komunitas atau kawasan spesifik tempat properti sewa berada. | Important for location-based rental price comparison. |
| `zone` | String | Broader district or geographic zone containing the community. | Zona atau distrik yang lebih luas dari komunitas properti. | Useful for aggregated rental market analysis. |
| `lat` | Float | Latitude coordinate of the rental property location. | Koordinat latitude dari lokasi properti sewa. | Useful for mapping and spatial analysis. |
| `lon` | Float | Longitude coordinate of the rental property location. | Koordinat longitude dari lokasi properti sewa. | Useful for mapping and spatial analysis. |
| `property_category` | String | General property category, such as apartment or villa. | Kategori umum properti, seperti apartemen atau vila. | Key segmentation variable because apartments and villas have different rental behavior. |
| `property_type` | String | More specific property type or bedroom configuration, such as studio, 1BR, 2BR, villa, or penthouse. | Tipe properti yang lebih spesifik atau konfigurasi kamar, seperti studio, 1BR, 2BR, vila, atau penthouse. | Useful for comparing rental prices between similar property formats. |
| `bedrooms` | Integer | Number of bedrooms in the rental property. Studio units are usually represented as 0 bedrooms. | Jumlah kamar tidur dalam properti sewa. Unit studio biasanya direpresentasikan sebagai 0 kamar tidur. | Strong driver of annual rent and property size. |
| `area_sqft` | Integer | Property area measured in square feet. | Luas properti dalam satuan kaki persegi. | Dubai commonly uses square feet for property size. |
| `area_m2` | Float | Property area measured in square meters. | Luas properti dalam satuan meter persegi. | Useful for international comparison. |
| `view` | String | Main view associated with the property, such as sea, marina, city, park, golf course, pool, community, or Burj Khalifa. | Pemandangan utama dari properti, seperti laut, marina, kota, taman, lapangan golf, kolam, komunitas, atau Burj Khalifa. | Premium views may increase rental value. |
| `furnishing` | String | Furnishing status of the rental property, such as unfurnished, semi-furnished, or fully furnished. | Status perabot properti sewa, seperti tanpa perabot, semi-furnished, atau fully furnished. | Fully furnished units may command higher rent, especially for short-term rentals. |
| `chiller_included` | Boolean | Indicates whether cooling or air-conditioning charges are included in the rent. | Menunjukkan apakah biaya pendingin udara atau chiller sudah termasuk dalam harga sewa. | Important for tenant cost comparison because cooling costs can affect total living expenses. |
| `parking_spaces` | Integer | Number of parking spaces included with the rental property. | Jumlah tempat parkir yang termasuk dalam properti sewa. | More parking spaces may increase rental value, especially for larger units or villas. |
| `metro_station` | String | Nearest Dubai Metro station to the rental property. | Stasiun Dubai Metro terdekat dari properti sewa. | Useful for analyzing transport accessibility. |
| `metro_line` | String | Metro line associated with the nearest station, such as Red or Green. | Jalur metro dari stasiun terdekat, seperti Red atau Green. | Can help compare rental prices by transport corridor. |
| `metro_distance_min` | Integer | Estimated travel time in minutes to the nearest metro station. | Estimasi waktu tempuh dalam menit ke stasiun metro terdekat. | Lower values usually indicate better accessibility and may support higher rent. |
| `to_burj_khalifa_km` | Float | Distance from the rental property to Burj Khalifa in kilometers. | Jarak properti sewa ke Burj Khalifa dalam kilometer. | Proxy for centrality and proximity to Dubai's prime business and tourism core. |
| `contract_type` | String | Type of rental contract, such as yearly or short-term. | Jenis kontrak sewa, seperti tahunan atau jangka pendek. | Important because short-term and yearly rentals can have different pricing behavior. |
| `n_cheques` | Integer | Number of cheque payments used for the rental contract. | Jumlah pembayaran cek dalam kontrak sewa. | In Dubai, rent is often paid through multiple cheques; more cheques can indicate payment flexibility. |
| `annual_rent_usd` | Integer | Total annual rent of the property in US dollars. | Total harga sewa tahunan properti dalam dolar AS. | Main target variable for rental price analysis or prediction. |
| `rent_per_sqft_usd` | Integer | Annual rent per square foot in US dollars. | Harga sewa tahunan per kaki persegi dalam dolar AS. | Better than total annual rent for comparing properties of different sizes. |
| `rent_per_m2_usd` | Integer | Annual rent per square meter in US dollars. | Harga sewa tahunan per meter persegi dalam dolar AS. | International equivalent of rent per square foot. |

## Suggested Analysis Questions

### English

1. Which Dubai zones and communities have the highest average annual rent?
2. Which areas have the highest rent per square foot?
3. Do fully furnished properties rent for more than unfurnished properties?
4. How much rental premium is associated with sea, marina, Burj Khalifa, or golf course views?
5. Does proximity to metro stations increase rental prices?
6. How do apartments and villas differ in rental price behavior?
7. Are short-term rentals more expensive on a per-square-foot basis than yearly rentals?
8. Does the number of cheques relate to rent level or tenant flexibility?
9. How did rental prices change from 2021 to 2026?
10. Which communities offer relatively affordable rent while still having good metro access?

### Bahasa Indonesia

1. Zona dan komunitas mana di Dubai yang memiliki rata-rata sewa tahunan tertinggi?
2. Area mana yang memiliki harga sewa per kaki persegi tertinggi?
3. Apakah properti fully furnished memiliki harga sewa lebih tinggi daripada properti unfurnished?
4. Seberapa besar premium sewa untuk view laut, marina, Burj Khalifa, atau lapangan golf?
5. Apakah kedekatan dengan stasiun metro meningkatkan harga sewa?
6. Bagaimana perbedaan perilaku harga sewa antara apartemen dan vila?
7. Apakah rental jangka pendek lebih mahal secara per kaki persegi dibanding rental tahunan?
8. Apakah jumlah pembayaran cek berhubungan dengan level harga sewa atau fleksibilitas penyewa?
9. Bagaimana perubahan harga sewa dari 2021 sampai 2026?
10. Komunitas mana yang relatif terjangkau tetapi tetap memiliki akses metro yang baik?

## Important Notes

### English

- `annual_rent_usd` is useful for understanding the total yearly rental cost, while `rent_per_sqft_usd` is better for comparing properties with different sizes.
- `contract_type` should be considered carefully because short-term and yearly rentals may not be directly comparable.
- `n_cheques` is relevant in the Dubai rental market because tenants often pay rent through one or multiple post-dated cheques.
- `metro_distance_min` is an accessibility proxy. It does not necessarily represent exact walking time for every listing.
- Furnishing, view, property category, and location should be analyzed together because rental premiums may differ by segment.
- The dataset documentation states that listing-level characteristics are generated using a hedonic pricing model. Therefore, analysis should be framed as exploratory and model-based, not as official transaction-level proof.

### Bahasa Indonesia

- `annual_rent_usd` berguna untuk memahami total biaya sewa tahunan, sedangkan `rent_per_sqft_usd` lebih baik untuk membandingkan properti dengan ukuran berbeda.
- `contract_type` perlu diperhatikan karena rental jangka pendek dan rental tahunan tidak selalu bisa dibandingkan secara langsung.
- `n_cheques` relevan dalam pasar rental Dubai karena penyewa sering membayar sewa melalui satu atau beberapa cek mundur.
- `metro_distance_min` adalah proxy aksesibilitas. Nilainya tidak selalu merepresentasikan waktu jalan kaki yang benar-benar presisi untuk setiap listing.
- Furnishing, view, kategori properti, dan lokasi sebaiknya dianalisis bersama karena premium harga sewa bisa berbeda antar segmen.
- Dokumentasi dataset menyebutkan bahwa karakteristik listing-level dibuat menggunakan hedonic pricing model. Jadi, analisis sebaiknya diposisikan sebagai eksplorasi berbasis model, bukan bukti resmi transaksi aktual.