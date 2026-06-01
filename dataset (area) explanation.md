## Dataset Description

This dataset provides monthly real estate market indicators across various Dubai communities. It combines property pricing data, rental market information, listing activity, and macroeconomic variables, enabling comprehensive analysis of market trends and investment opportunities.

| Column                             | Description                                                                                            |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `year_month`                       | The observation period recorded in YYYY-MM format.                                                     |
| `community`                        | The specific residential or commercial community where the property is located.                        |
| `zone`                             | The broader geographic area or district that contains the community.                                   |
| `is_freehold`                      | Indicates whether foreign investors are allowed to fully own properties within the area.               |
| `secondary_price_per_sqft_usd`     | Average resale (secondary market) property price per square foot in USD.                               |
| `secondary_price_per_m2_usd`       | Average resale (secondary market) property price per square meter in USD.                              |
| `offplan_price_per_sqft_usd`       | Average price per square foot for off-plan properties that are under development or not yet completed. |
| `rental_price_per_sqft_annual_usd` | Average annual rental price per square foot in USD.                                                    |
| `n_listings_secondary`             | Total number of active secondary-market property listings.                                             |
| `n_listings_offplan`               | Total number of active off-plan property listings.                                                     |
| `n_listings_rental`                | Total number of active rental property listings.                                                       |
| `cbuae_base_rate_pct`              | Official base interest rate set by the Central Bank of the United Arab Emirates (CBUAE).               |
| `avg_mortgage_rate_pct`            | Average mortgage interest rate available to property buyers.                                           |

### Business Relevance

These variables provide insights into several key aspects of Dubai's real estate market:

* Property value appreciation and depreciation trends
* Rental market performance
* Supply and demand dynamics
* Differences between off-plan and secondary markets
* Effects of interest rates on housing affordability
* Community-level investment opportunities
* Future property price forecasting
