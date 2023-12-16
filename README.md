# Bike Sharing prediction
>We are required to model the demand for shared bikes with the available independent variables. It will be used by the management to understand how exactly the demands vary with different features. They can accordingly manipulate the business strategy to meet the demand levels and meet the customer's expectations. Further, the model will be a good way for management to understand the demand dynamics of a new market. 


## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Conclusions](#conclusions)
* [Acknowledgements](#acknowledgements)

<!-- You can include any other section that is pertinent to your problem -->

## General Information
- A bike-sharing system is a service in which bikes are made available for shared use to individuals on a short  term basis for a price or free.
- A US bike-sharing provider BoomBikes has recently suffered considerable dips in their revenues due to the ongoing Corona pandemic.BoomBikes spires to understand the demand for shared bikes among the people after this ongoing quarantine situation ends across the nation due to Covid-19. 
- The day dataset which is analysed contain the year, month, weather, temp, etc information when bike was rented we need to predict the features which increase sells.

## Conclusions
- We can come up with below equation for the best fitting line to Bike Sharing linear model from the above Coefficient cnt = 0.3535 + 0.228*yr + 0.526*temp - 0.189*hum - 0.165*windspeed - 0.113*Spring + 0.045*Winter - 0.59*Aug - 0.124*Jul - 0.05*Jun - 0.045*Light_rainfall - 0.203*Thunderstrom

- Hypothesis Testing Hnull - as it is evident that all our coefficients are not equal to zero, which means we REJECT the NULL HYPOTHESIS

- Year, Winter, Temp increase the reting of bike while the other factors like hum, Spring, Winter, Aug, Jul, Jun,Light_rainfall, Thunderstrom decrease the renting.

- High coff of temp indicating temp has significant impact on bike renting 


## Technologies Used
- Pandas - version 1.3.3
- Numpy - version 1.24.4
- seaborn - version 0.12.2
- matplot.pyplot
- sklearn
- statsmodel


## Contact
Created by [@itsshaliniS] - feel free to contact me!


<!-- Optional -->
<!-- ## License -->
<!-- This project is open source and available under the [... License](). -->

<!-- You don't have to include all sections - just the one's relevant to your project -->