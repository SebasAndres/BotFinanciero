from pyspark.sql import SparkSession
from pyspark import SparkContext

if __name__ == '__main__':

    # initialize Spark
    session = SparkSession.builder.appName("training session").getOrCreate()
    context = session.sparkContext  

    # load MEP data
    data = session.read.csv("datasources/dolarMEP.csv", header=True, inferSchema=True)

    # train timeSeries model

    # train reinforcement learning model

    # evaluate models with test data

    # save models into '/trained/type_model/timestamp/'
    # --> add evaluation results to /trained/type_model/timestamp/metrics
    # --> add model metadata to /trained/type_model/timestamp/metadata 
    
    # close Spark
    session.stop()


