## Dataset Description

This dataset contains rental property listings across various Dubai communities. It includes property characteristics, location information, accessibility metrics, furnishing details, lease conditions, and rental pricing data.

The dataset is designed to support rental market analysis, affordability studies, tenant behavior insights, and rental price modeling.

| Column               | Description                                                            |
| -------------------- | ---------------------------------------------------------------------- |
| `id`                 | Unique identifier for each rental listing.                             |
| `date_listed`        | Date when the rental property was listed.                              |
| `community`          | Community or neighborhood where the property is located.               |
| `zone`               | Broader geographic area or district.                                   |
| `lat`                | Latitude coordinate of the property location.                          |
| `lon`                | Longitude coordinate of the property location.                         |
| `property_category`  | General property category (e.g., apartment, villa, townhouse).         |
| `property_type`      | Specific property type and bedroom configuration.                      |
| `bedrooms`           | Number of bedrooms.                                                    |
| `area_sqft`          | Property size in square feet.                                          |
| `area_m2`            | Property size in square meters.                                        |
| `view`               | Primary view offered by the property (e.g., city, sea, Burj Khalifa).  |
| `furnishing`         | Furnishing status of the property (furnished or unfurnished).          |
| `chiller_included`   | Indicates whether cooling charges are included in the rent.            |
| `parking_spaces`     | Number of parking spaces included.                                     |
| `metro_station`      | Nearest Dubai Metro station.                                           |
| `metro_line`         | Metro line associated with the nearest station.                        |
| `metro_distance_min` | Estimated travel time or distance metric to the nearest metro station. |
| `to_burj_khalifa_km` | Distance from the property to Burj Khalifa in kilometers.              |
| `contract_type`      | Type of rental agreement (e.g., yearly).                               |
| `n_cheques`          | Number of cheque installments accepted for rent payment.               |
| `annual_rent_usd`    | Total annual rental price in USD.                                      |
| `rent_per_sqft_usd`  | Annual rent per square foot in USD.                                    |
| `rent_per_m2_usd`    | Annual rent per square meter in USD.                                   |

### Business Relevance

This dataset provides valuable insights into Dubai's rental market and tenant preferences.

Potential analysis includes:

* Rental price distribution across communities
* Furnished vs unfurnished rental premiums
* Impact of metro accessibility on rent prices
* Relationship between property size and rent
* Rental price differences by property type
* Effect of views and amenities on rental value
* Analysis of payment flexibility through cheque installments
* Identification of high-demand rental locations
* Rental affordability and market segmentation
* Rental price prediction and forecasting
