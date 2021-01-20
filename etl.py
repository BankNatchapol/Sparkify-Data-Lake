import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format


config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['SECRET']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['SECRET']['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    sc=spark.sparkContext
    sc.setSystemProperty("com.amazonaws.services.s3.enableV4", "true")
    return spark


def process_song_data(spark, input_data, output_data):
    # get filepath to song data file
    song_data = os.path.join(input_data, "song_data/A/A/A/*.json")
    
    # read song data file
    df = spark.read.json(song_data)

    # extract columns to create songs table
    songs_table = df.select("song_id", "title", "artist_id", "year", "duration").dropDuplicates(["song_id"])
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.partitionBy("year", "artist_id").parquet(os.path.join(output_data, "songs.parquet"), "overwrite")

    # extract columns to create artists table
    artists_table = df.selectExpr("artist_id", "artist_name as name", "artist_location as location", "artist_latitude as lattitude", "artist_longitude as longitude").dropDuplicates(["artist_id"])
    
    # write artists table to parquet files
    artists_table.write.mode("overwrite").parquet(output_data + "artists")





def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://bank-data-lake/"
    
    process_song_data(spark, input_data, output_data)    
    

if __name__ == "__main__":
    main()
