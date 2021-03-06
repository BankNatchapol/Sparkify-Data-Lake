[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">

  <h3 align="center">Sparkify Data Lake on AWS</h3>

  <p align="center">
    Create ETL and Data Lake on AWS.
    <br />
    <br />
    <a href="https://github.com/BankNatchapol/Sparkify-Data-Lake/issues">Report Bug</a>
    ·
    <a href="https://github.com/BankNatchapol/Sparkify-Data-Lake/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li><a href="#dataset">Dataset</a>
        <ul>
        <li><a href="#project-dataset">Project Dataset</a></li>
        <li><a href="#song-dataset">Song Dataset</a></li>
        <li><a href="#log-dataset">Log Dataset</a></li>
      </ul>
    </li>
<li>
      <a href="#data-model">Data Model</a>
    </li>
<li>
      <a href="#working-processes">Working Processes</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#config-files">Config files</a></li>
        <li><a href="#etl-process">ETL Process</a></li>
      </ul>
    </li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

A music streaming startup, Sparkify, has grown their user base and song database even more and want to move their data warehouse to a data lake. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

As their data engineer, you are tasked with building an ETL pipeline that extracts their data from S3, processes them using Spark, and loads the data back into S3 as a set of dimensional tables. This will allow their analytics team to continue finding insights in what songs their users are listening to.


<!-- Dataset -->
## Dataset
### Project Dataset
There are two datasets that reside in S3. Here are the S3 links for each:<br>
Song data:
>s3://udacity-dend/song_data

Log data:
>s3://udacity-dend/log_data

### Song Dataset
The first dataset is a subset of real data from the Million Song Dataset. Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset.
>song_data/A/B/C/TRABCEI128F424C983.json<br>
>song_data/A/A/B/TRAABJL12903CDCF1A.json

And below is an example of what a single song file, TRAABJL12903CDCF1A.json, looks like.

>{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}

### Log Dataset

The second dataset consists of log files in JSON format generated by this event simulator based on the songs in the dataset above. These simulate activity logs from a music streaming app based on specified configurations.

The log files in the dataset you'll be working with are partitioned by year and month. For example, here are filepaths to two files in this dataset.
>log_data/2018/11/2018-11-12-events.json <br>
>log_data/2018/11/2018-11-13-events.json

And below is an example of what the data in a log file, 2018-11-12-events.json, looks like.

<img src="https://video.udacity-data.com/topher/2019/February/5c6c15e9_log-data/log-data.png"/>

<!-- DATA MODEL -->
## Data Model
This is my database Star Schema.
<img src="https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/38715/1608661799/Song_ERD.png"/>

<!-- WORKING PROCESSES -->
## Working Processes

### Installation
install package with.
> pip install -r requirements.txt
### Config files
create config files for access AWS<br>
dl.cfg : 
> [SECRET]<br>
> AWS_ACCESS_KEY_ID= ?  &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;// AWS User Access Key<br> 
> AWS_SECRET_ACCESS_KEY= ?&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;// AWS User Secret Access Key<br>
>
> [STORAGE]<br>
> INPUT_DATA= ? &nbsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp; // Path to data that you want to transform<br>
> OUTPUT_DATA= ? &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp; // Your S3 Bucket Path<br>


### ETL Process
run this script to do ETL process for transforming your input data to your output path.
> python <span>etl.py</span>

this process will take some times.<br>
<br>
or you can use etl.ipynb notebook to do each step of ETL process seperately.

<!-- CONTACT -->
## Contact

Facebook - [@Natchapol Patamawisut](https://www.facebook.com/natchapol.patamawisut/)

Project Link: [https://github.com/BankNatchapol/Sparkify-Data-Lake](https://github.com/BankNatchapol/Sparkify-Data-Lake)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/natchapol-patamawisut
