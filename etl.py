import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format


config = configparser.ConfigParser()
config.read("dl.cfg")

os.environ["AWS_ACCESS_KEY_ID"]=config["SECRET"]["AWS_ACCESS_KEY_ID"]
os.environ["AWS_SECRET_ACCESS_KEY"]=config["SECRET"]["AWS_SECRET_ACCESS_KEY"]


def create_spark_session():
    """
    Create Spark Session for connecting with clusters :

    Args:
        None

    Returns:
        spark: Spark Session object.
        
    """
        
        
    spark = SparkSession \
                .builder \
                .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
                .getOrCreate()
    return spark

def process_song_data(spark, df, output_data):
    """
    Processing song data to get songs and artists tables and store data in AWS S3 Bucket.

    Args:
        spark: Spark Session object.
        df: PySpark Dataframe of song data.
        output_data (str): AWS S3 Bucket path path to store songs and artists.

    Returns:
        None

    """
        
        
    # extract columns to create songs table
    songs_table = df.select("song_id", "title", "artist_id", "year", "duration").dropDuplicates(["song_id"])
    
    # write songs table to parquet files partiti oned by year and artist
    songs_table.write.mode("overwrite").partitionBy("year", "artist_id").parquet(os.path.join(output_data, "songs"))

    # extract columns to create artists table
    artists_table = df.selectExpr("artist_id", "artist_name as name", 
                                  "artist_location as location", 
                                  "artist_latitude as lattitude", 
                                  "artist_longitude as longitude").dropDuplicates(["artist_id"])
    
    # write artists table to parquet files
    artists_table.write.mode("overwrite").parquet(os.path.join(output_data, "artists"))

    
def process_log_data(spark, df, output_data):
    """
    Processing log data to get users and time tables and store data in AWS S3 Bucket.

    Args:
        spark: Spark Session object.
        df: PySpark Dataframe of log data.
        output_data (str): AWS S3 Bucket path to store users and time tables.

    Returns:
        None

    """
        
        
    # extract columns for users table    
    users_table = df.selectExpr("userId as user_id", 
                                "firstName as first_name", 
                                "lastName as last_name", 
                                "gender", "level").where("page = 'NextSong' and userId IS NOT NULL")
    
    # write users table to parquet files
    users_table.write.mode("overwrite").parquet(os.path.join(output_data, "users"))

    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x: str(int(int(x) / 1000)))
    df = df.withColumn("timestamp", get_timestamp(df["ts"]))

    # create datetime column from original timestamp column
    get_datetime = udf(lambda x: str(datetime.fromtimestamp(int(x) / 1000.0)))
    df = df.withColumn("datetime", get_datetime(df["ts"]))

    # extract columns to create time table
    time_table = df.selectExpr("datetime as start_time", 
                               "hour(datetime) as hour",
                                "day(datetime) as day",
                                "weekofyear(datetime) as week",
                                "month(datetime) as month",
                                "year(datetime) as year",
                                "dayofweek(datetime) as weekday").dropDuplicates(["start_time"])
    
    # write time table to parquet files partitioned by year and month
    time_table.write.mode("overwrite").partitionBy("year", "month").parquet(os.path.join(output_data, "time"))


def process_data_lake(spark, input_data, output_data):
    """
    Processing song and log data to songplays fact table and store data in AWS S3 Bucket.

    Args:
        spark: Spark Session object.
        input_data (str): AWS S3 Bucket path to input data.
        output_data (str): AWS S3 Bucket path to store songplays table.

    Returns:
        None

    """
        
        
    # get filepath to data files
    song_data = os.path.join(input_data, "song_data/*/*/*/*.json")
    log_data = os.path.join(input_data, "log_data/*/*/*.json")
    
    # read log files
    song_df = spark.read.json(song_data)
    log_df = spark.read.json(log_data)

    # extract columns from joined song and log datasets to create songplays table 
    songplays_table = song_df.join(log_df, log_df.artist ==  song_df.artist_name, how = "inner") \
                        .selectExpr("monotonically_increasing_id() as songplay_id",
                                    "to_timestamp(ts/1000) as start_time",
                                    "month(to_timestamp(ts/1000)) as month",
                                    "year(to_timestamp(ts/1000)) as year",
                                    "userId as user_id",
                                    "level as level",
                                    "song_id as song_id",
                                    "artist_id as artist_id",
                                    "sessionId as session_id",
                                    "location as location",
                                    "userAgent as user_agent")

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.mode("overwrite").partitionBy("year", "month").parquet(os.path.join(output_data, "songplays"))
    
    # process song data to create songs and artists tables
    process_song_data(spark, song_df, output_data)
    
    # process log data to create users and time tables
    process_log_data(spark, log_df, output_data)
    
    
def main():
    spark = create_spark_session()
    
    input_data = config["STORAGE"]["INPUT_DATA"]
    output_data = config["STORAGE"]["OUTPUT_DATA"]
    
    process_data_lake(spark, input_data, output_data)
    

if __name__ == "__main__":
    main()
