# Reviews Crawling Tool

This tool has been developed with the purpose to mine reviews from the Google Play Store.
It's entirely written in Java, and relies on [Selenium](http://www.seleniumhq.org/) and on [PhantomJS](http://phantomjs.org).

The tool can save the reviews in a csv format as well storing them using a MongoDB instance.

## How to use
First of all, you need to download ([here](http://phantomjs.org/download.html)) the right PhantomJS executable according to your underlying operating system. It have to be placed in the same directory of the jar and the properties file.
### Configuration
The tool must be set through its configuration file. You need to specify the input and the output file name. 

Most parameters are self explained in the `config.properties` file. The most important ones are detailed in the following paragraph.

#### Parameters
> export_to=...

For this option you can select the option `file` or `mongodb`. The first one will save the reviews on a csv file, the second one will use a mongodb instance.

> input_file=xxx.csv

This is the file with the list of app of which the reviews need to be extracted. The file need to report the package name of the app as the first field in the csv. 
### How to run
In order to start the reviews mining, you have to run the following command:

`java -jar extractor.jar extractor=reviews`

The tool will start to extract the reviews for the apps specified in the `input_file` parameter.

#### Extract from mongodb database

When you are collecting you reviews storing them on a mongodb database, you can export the reviews for the apps you are interested to with the following command:

`java -jar extractor.jar extractor=export`

You have specify the name of the csv file in output through the `output_file` field in the `config.properties`. Similarly, the `input_file` field should contain a list of the app for which you want to extract the reviews.

