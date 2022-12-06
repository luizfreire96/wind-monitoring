# Wind Monitoring

Forecasting wind speed have a lot of benefits, like manage the power transmission and distribution grid, protect the equipaments from over production, 
doing the maintenance in a good moment, etc. 
With that in mind, this project was developed to create a interface to expose the predictions data based in previous data.<br>
To develop this project, an docker image was created for each statistical model used and another to expose the data in a dashboard.
To orchastarte the containers, kubernetes was used.
The database was created locally to store the models parameters, wind speed data and turbine locations.
A test database filled with 10% of nan's in random locations was created to test the model used to fill the nan's.<br><br>

## Kriging

Also named gaussian process regression, kriging is a method to make some predictions in space. This method was used to predict missing data.
The method uses a covariance function to describe how the values are distributed. Kriging method assumes that the values in a field are centered
in a mean value. The model used in this project is the ordinary krigin, that assumes a constant mean value. All data from a turbine was deleted
to test the method. 
For that case, **the score of the method is almost 0.99**, and a graph with the real values and predicted values is shown below (turbine #6):
<br>

![image](https://github.com/luizfreire96/windMonitoring/blob/main/krigingBuild/kriging.png)
<br>
For each time a model is created to fill the nan values in random places, like this: <br>

![image](https://github.com/luizfreire96/windMonitoring/blob/main/krigingBuild/nanfill.png)
<br><br>

## Short-term Prediction (Auto Regressive Moving Average Model)

The arma model uses the previous and current variable values to forecast new variable values.
A correlation with the target variable with itself lagged can show the best order to the model.
This is called autocorrelation. If the autocorrelation is high even with high number lags, the best model will be **probably** high.
But for that case, the variable have significant autocorrelation up to 3 lags. We can see the autocorrelation for turbine #6 for example:<br>

![image](https://github.com/luizfreire96/windMonitoring/blob/main/armaBuild/partial-autocorrelation.png)

<br><br>
## Long-term Approximation (Weibull curve)

For long-term approximation, when using autorregressive model doesn't make sense anymore, it would be ok to use the mean value,
but the distribution is skewd. So, the median of a popular probability density function used in wind data, the Weibull curve, is used
to get rid of the skew problem. Since the data is limited, it's needed to group bins to have a significant amount of ocurrencies to test it.
The statistical test used to verify if the curve fits good is chi squared test. In the end, the weibull distribution looks like this:
<br>
![image](https://github.com/luizfreire96/windMonitoring/blob/main/weibullBuild/weibulpdf.png)

## Conclusion

A lot can be done to turn the project more interactive, with more metrics to show and aesthetic. So, this is a initial project.
With all that data and models stored, a dashboard is created to expose the important metrics to operation of wind energy sites.<br>

![image](https://github.com/luizfreire96/windMonitoring/blob/main/app/dashboard.png)
