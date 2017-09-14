# Android Apps and User Feedback: a Dataset for Software Evolution and Quality Improvement

This dataset comprises 288,065 reviews extracted from the Google Play, related to 395 open source apps mined from F-Droid.
For some particular ones, we provide also these data for different versions of the same app.

An exhaustive list of the apks and apps included in our dataset is available [here](https://github.com/sealuzh/user_quality/blob/master/csv_files/versions.csv).

## APK Analysis
For each of the apks, we computer 22 different code quality metrics as well as 8 categories of distinct code-smells.

For a detailed description of the computed metrics, please refers to:
* [Code quality metrics](https://github.com/sealuzh/user_quality/wiki/Code-Quality-Metrics)
* [Code smells](https://github.com/sealuzh/user_quality/wiki/Code-Smells)

### Mining Scripts
We also provide a replication package which includes all the scripts used for the extraction of the code quality metrics. It is available at the following [link](https://github.com/sealuzh/user_quality/blob/master/code_metrics_scripts).

Moreover, [here](https://github.com/sealuzh/user_quality/tree/master/tools) we make available the tool we developed to crawl reviews from the Google Play Store, as well as the code used in order to download apks from F-Droid.

## Main Contributors

[Giovanni Grano](https://github.com/giograno) - (University of Zurich), [Sebastiano Panichella](https://github.com/panichella) - (University of Zurich), [Andrea di Sorbo](https://github.com/adisorbo) - (University of Sannio)
