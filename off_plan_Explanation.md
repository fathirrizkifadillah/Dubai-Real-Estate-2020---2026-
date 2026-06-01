# Off-Plan Dataset Explanation

## Dataset Overview

### English

This dataset contains listing-level data for Dubai off-plan properties. Off-plan properties are units sold before construction is completed, often during the launch or development stage. Each row represents one off-plan listing with information about the project, developer, location, property characteristics, payment plan, accessibility, price, and mortgage conditions at the time of listing.

The dataset can be used to analyze Dubai's new development market, compare developer positioning, study price premiums across locations and views, evaluate payment plan structures, and identify potential investment opportunities in future handover projects.

### Bahasa Indonesia

Dataset ini berisi data listing properti off-plan di Dubai. Properti off-plan adalah unit yang dijual sebelum konstruksi selesai, biasanya saat tahap peluncuran atau pembangunan proyek. Setiap baris merepresentasikan satu listing off-plan dengan informasi proyek, developer, lokasi, karakteristik properti, skema pembayaran, aksesibilitas, harga, dan kondisi suku bunga KPR pada saat listing dibuat.

Dataset ini dapat digunakan untuk menganalisis pasar proyek baru Dubai, membandingkan positioning developer, mempelajari premium harga berdasarkan lokasi dan view, mengevaluasi struktur payment plan, serta mengidentifikasi peluang investasi pada proyek yang akan handover di masa depan.

## Dataset Structure

- Rows: 12,000
- Columns: 28
- Date range: 2021-01-01 to 2026-04-29
- Launch years: 2021 to 2025
- Handover years: 2024 to 2028
- Main price target: `price_usd`
- Normalized price metrics: `price_per_sqft_usd`, `price_per_m2_usd`

## Column Explanation

| Column | Data Type | English Explanation | Penjelasan Bahasa Indonesia | Analysis Notes |
| --- | --- | --- | --- | --- |
| `id` | String | Unique identifier for each off-plan property listing. | ID unik untuk setiap listing properti off-plan. | Useful as a row identifier, not usually used as a predictive feature. |
| `date_listed` | Date/String | Date when the off-plan property was listed. | Tanggal saat properti off-plan dipasang sebagai listing. | Can be converted to datetime for launch and listing trend analysis. |
| `project_id` | String | Unique identifier for the development project. | ID unik untuk proyek pengembangan properti. | Useful for grouping listings by project. |
| `project_name` | String | Name of the off-plan development project. | Nama proyek properti off-plan. | Useful for project-level comparison and ranking. |
| `developer` | String | Name of the real estate developer responsible for the project. | Nama developer properti yang mengembangkan proyek. | Important for analyzing developer reputation and pricing power. |
| `developer_tier` | String | Developer classification based on reputation, scale, or market positioning. | Klasifikasi developer berdasarkan reputasi, skala, atau posisi pasar. | Tier 1 developers may command price premiums due to brand trust. |
| `community` | String | Specific community or neighborhood where the project is located. | Komunitas atau kawasan spesifik tempat proyek berada. | Important for location-based price comparison. |
| `zone` | String | Broader district or geographic zone containing the community. | Zona atau distrik yang lebih luas dari komunitas proyek. | Useful for aggregated market analysis. |
| `lat` | Float | Latitude coordinate of the project location. | Koordinat latitude dari lokasi proyek. | Useful for mapping and spatial analysis. |
| `lon` | Float | Longitude coordinate of the project location. | Koordinat longitude dari lokasi proyek. | Useful for mapping and spatial analysis. |
| `property_category` | String | General property category, such as apartment or villa. | Kategori umum properti, seperti apartemen atau vila. | Key segmentation variable because apartments and villas have different price behavior. |
| `property_type` | String | More specific property type or bedroom configuration, such as studio, 1BR, 2BR, villa, or penthouse. | Tipe properti yang lebih spesifik atau konfigurasi kamar, seperti studio, 1BR, 2BR, vila, atau penthouse. | Useful for comparing similar off-plan product types. |
| `bedrooms` | Integer | Number of bedrooms in the property. Studio units are usually represented as 0 bedrooms. | Jumlah kamar tidur dalam properti. Unit studio biasanya direpresentasikan sebagai 0 kamar tidur. | Strong driver of total price and unit size. |
| `area_sqft` | Integer | Property area measured in square feet. | Luas properti dalam satuan kaki persegi. | Dubai commonly uses square feet for property size. |
| `area_m2` | Float | Property area measured in square meters. | Luas properti dalam satuan meter persegi. | Useful for international comparison. |
| `view` | String | Main view associated with the property, such as sea, marina, city, park, golf course, pool, community, or Burj Khalifa. | Pemandangan utama dari properti, seperti laut, marina, kota, taman, lapangan golf, kolam, komunitas, atau Burj Khalifa. | Premium views may increase off-plan pricing. |
| `launch_year` | Integer | Year when the project was launched to the market. | Tahun ketika proyek diluncurkan ke pasar. | Useful for analyzing launch cycles and developer activity. |
| `handover_year` | Integer | Expected year when the project will be completed and handed over to buyers. | Tahun perkiraan saat proyek selesai dan diserahkan kepada pembeli. | Can be used to calculate time-to-handover and delivery pipeline. |
| `total_project_units` | Integer | Total number of units planned within the development project. | Jumlah total unit yang direncanakan dalam proyek pengembangan. | Useful for understanding project scale and potential supply impact. |
| `payment_plan` | String | Payment structure offered by the developer, such as 60/40, 70/30, 80/20, or post-handover plans. | Struktur pembayaran yang ditawarkan developer, seperti 60/40, 70/30, 80/20, atau skema post-handover. | Important for investor affordability and cash flow analysis. |
| `metro_station` | String | Nearest Dubai Metro station to the project. | Stasiun Dubai Metro terdekat dari proyek. | Useful for accessibility analysis. |
| `metro_line` | String | Metro line associated with the nearest station, such as Red or Green. | Jalur metro dari stasiun terdekat, seperti Red atau Green. | Can help compare projects by transport corridor. |
| `metro_distance_min` | Integer | Estimated travel time in minutes to the nearest metro station. | Estimasi waktu tempuh dalam menit ke stasiun metro terdekat. | Lower values usually indicate better transport accessibility. |
| `to_burj_khalifa_km` | Float | Distance from the project to Burj Khalifa in kilometers. | Jarak proyek ke Burj Khalifa dalam kilometer. | Proxy for centrality and proximity to Dubai's prime core. |
| `price_usd` | Integer | Total listed price of the off-plan property in US dollars. | Total harga listing properti off-plan dalam dolar AS. | Main target variable for off-plan price analysis or prediction. |
| `price_per_sqft_usd` | Integer | Listed price per square foot in US dollars. | Harga listing per kaki persegi dalam dolar AS. | Better than total price for comparing units of different sizes. |
| `price_per_m2_usd` | Integer | Listed price per square meter in US dollars. | Harga listing per meter persegi dalam dolar AS. | International equivalent of price per square foot. |
| `mortgage_rate_at_listing` | Float | Mortgage interest rate at the time the property was listed. | Suku bunga KPR pada saat properti dipasang sebagai listing. | Useful for studying the relationship between financing conditions and off-plan pricing. |

## Suggested Analysis Questions

### English

1. Which developers have the highest average off-plan price per square foot?
2. Do tier 1 developers command a clear price premium over tier 2 developers?
3. Which communities and zones dominate Dubai's off-plan supply?
4. How does time-to-handover relate to price per square foot?
5. Are post-handover payment plans associated with higher prices?
6. Which views create the strongest price premiums in off-plan listings?
7. Does metro accessibility increase off-plan property prices?
8. How do apartments and villas differ in off-plan pricing?
9. Which launch years had the highest number of listed units?
10. Which projects combine relatively attractive prices, strong developer tier, and good accessibility?

### Bahasa Indonesia

1. Developer mana yang memiliki rata-rata harga off-plan per kaki persegi tertinggi?
2. Apakah developer tier 1 memiliki premium harga yang jelas dibanding developer tier 2?
3. Komunitas dan zona mana yang mendominasi suplai off-plan Dubai?
4. Bagaimana hubungan waktu menuju handover dengan harga per kaki persegi?
5. Apakah payment plan post-handover berkaitan dengan harga yang lebih tinggi?
6. View apa yang memberikan premium harga paling besar pada listing off-plan?
7. Apakah akses ke metro meningkatkan harga properti off-plan?
8. Bagaimana perbedaan harga off-plan antara apartemen dan vila?
9. Tahun launch mana yang memiliki jumlah listing unit paling tinggi?
10. Proyek mana yang memiliki kombinasi harga relatif menarik, developer tier kuat, dan aksesibilitas bagus?

## Important Notes

### English

- `price_usd` is useful for total unit value analysis, but `price_per_sqft_usd` is usually better for comparing units with different sizes.
- `launch_year` and `handover_year` can be combined to calculate development duration or time-to-handover.
- `payment_plan` should be treated as an investment feature because flexible payment terms can affect buyer demand.
- Developer tier is a simplified classification and should be interpreted as a broad market signal, not a complete measure of developer quality.
- Off-plan prices may reflect expectations about future value, not only current market conditions.
- The dataset documentation states that listing-level characteristics are generated using a hedonic pricing model. Therefore, analysis should be framed as exploratory and model-based, not as official transaction-level proof.

### Bahasa Indonesia

- `price_usd` berguna untuk analisis nilai total unit, tetapi `price_per_sqft_usd` biasanya lebih baik untuk membandingkan unit dengan ukuran berbeda.
- `launch_year` dan `handover_year` dapat digabungkan untuk menghitung durasi pengembangan atau waktu menuju handover.
- `payment_plan` sebaiknya diperlakukan sebagai fitur investasi karena fleksibilitas pembayaran dapat memengaruhi permintaan pembeli.
- Developer tier adalah klasifikasi sederhana dan sebaiknya dipahami sebagai sinyal pasar secara umum, bukan ukuran lengkap kualitas developer.
- Harga off-plan dapat mencerminkan ekspektasi nilai masa depan, bukan hanya kondisi pasar saat ini.
- Dokumentasi dataset menyebutkan bahwa karakteristik listing-level dibuat menggunakan hedonic pricing model. Jadi, analisis sebaiknya diposisikan sebagai eksplorasi berbasis model, bukan bukti resmi transaksi aktual.
