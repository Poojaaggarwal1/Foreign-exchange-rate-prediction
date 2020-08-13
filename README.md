# Foreign-exchange-rate-prediction
Long short term memory (LSTM ) is used to predict currency exchange rate for 22 countries-currencies against United States Dollar(USD) simultaneously. The model is trained to predict foreign currency exchange rate for 30 consecutive days by taking input of last 365 days for 22 countries simultaneously.<br />
Data source : https://www.kaggle.com/brunotly/foreign-exchange-rates-per-dollar-20002019
### Data plot 
Foreign exchange rate values plot of 2019-12-31
![alt tag](https://user-images.githubusercontent.com/50958067/90127723-410c4980-dd83-11ea-81c9-ed297f94b63d.png)


Foreign exchange rate values Indian rupees against USD plot from 2017-01-01 to 2019-12-31
![alt tag](https://user-images.githubusercontent.com/50958067/90128846-3357c380-dd85-11ea-8fa2-7c8781a92945.png)



### Result
Prediction of Foreign exchange rate values for Indian rupees against USD plot from date 2018-01-25 to 2018-02-24 (i.e. 365th to 395th day from
2017-01-25) actual (green) vs predicted(red)<br />
![alt tag](https://user-images.githubusercontent.com/50958067/90128027-ce4f9e00-dd83-11ea-8e6d-d1853c92a634.png)

Loss function<br />
![alt tag](https://user-images.githubusercontent.com/50958067/90128184-1c64a180-dd84-11ea-8742-666d58b8e9b0.png)
 
Dataset| Mean squared error(mse) | Mean absolute error(mae) |
--- | --- | --- | 
Training  | 0.004 | 0.048 |
Validation  | 0.020 | 0.112 |
