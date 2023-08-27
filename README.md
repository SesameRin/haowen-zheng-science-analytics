# Science Analytics

## Overview

This is the science analytics repository. The code mainly consists of 3 parts: openalex flatten csv, fetch faculty information and face recognition. 

- **openalex flatten csv:** I transformed openalex objects into reformatted csv files. The original object is quite long so I extract important properties and flatten its structure. The properties can be divided as self-property(Id, Name, Doi ...) and relationship-property(Concepts, Related Works, Last Known Institution). After getting the csv file, it's much easier to load the data into graph database Neo4j. You can create nodes based on self-properties and create relationships based on relationship-properties.
- **fetch faculty information:** I implemented code to fetch faculty info based on faculty's name and affiliation provided. I'll first search the faculty in google scholar, if not found, then search him in openalex. The google scholar id, image url and openalex id are appended in the csv results.
- **face recognition:** I use OpenCV lib and their pretrained age, gender detecting model to predict faculty's age and gender.

## File Structure

```bash
haowen-zheng-science-analytics
 ┣ code
 ┃ ┣ face_recognition
 ┃ ┃ ┣ cv2
 ┃ ┃ ┃ ┣ age_deploy.prototxt
 ┃ ┃ ┃ ┣ age_net.caffemodel
 ┃ ┃ ┃ ┣ gender_deploy.prototxt
 ┃ ┃ ┃ ┣ gender_net.caffemodel
 ┃ ┃ ┃ ┣ opencv_face_detector.pbtxt
 ┃ ┃ ┃ ┗ opencv_face_detector_uint8.pb
 ┃ ┃ ┣ test_data
 ┃ ┃ ┃ ┣ cs_100.csv
 ┃ ┃ ┃ ┣ cs_100_age_gender.csv
 ┃ ┃ ┃ ┗ cs_100_with_age_gender.csv
 ┃ ┃ ┗ face_recognition.py
 ┃ ┣ fetch_faculty_info
 ┃ ┃ ┣ example_results
 ┃ ┃ ┃ ┗ 500_faculty_example.csv
 ┃ ┃ ┣ faculty_data
 ┃ ┃ ┃ ┗ Faculty_CS_ECE-20230806.csv
 ┃ ┃ ┣ optimized_search_faculty.py
 ┃ ┃ ┣ result.csv
 ┃ ┃ ┗ testcase.ipynb
 ┃ ┗ openalex_flatten_csv
 ┃ ┃ ┣ csv_results
 ┃ ┃ ┃ ┣ authors.csv
 ┃ ┃ ┃ ┣ funders.csv
 ┃ ┃ ┃ ┣ institutions.csv
 ┃ ┃ ┃ ┣ publishers.csv
 ┃ ┃ ┃ ┗ works.csv
 ┃ ┃ ┣ openalex-snapshot
 ┃ ┃ ┃ ┗ data
 ┃ ┃ ┃ ┃ ┣ authors
 ┃ ┃ ┃ ┃ ┃ ┗ updated_date=2023-06-08
 ┃ ┃ ┃ ┃ ┃ ┃ ┗ part_000.gz
 ┃ ┃ ┃ ┃ ┣ concepts
 ┃ ┃ ┃ ┃ ┃ ┗ updated_date=2023-06-08
 ┃ ┃ ┃ ┃ ┃ ┃ ┗ part_000.gz
 ┃ ┃ ┃ ┃ ┣ funders
 ┃ ┃ ┃ ┃ ┃ ┗ updated_date=2023-06-08
 ┃ ┃ ┃ ┃ ┃ ┃ ┗ part_000.gz
 ┃ ┃ ┃ ┃ ┣ institutions
 ┃ ┃ ┃ ┃ ┃ ┗ updated_date=2023-06-08
 ┃ ┃ ┃ ┃ ┃ ┃ ┗ part_000.gz
 ┃ ┃ ┃ ┃ ┣ publishers
 ┃ ┃ ┃ ┃ ┃ ┗ updated_date=2023-06-08
 ┃ ┃ ┃ ┃ ┃ ┃ ┗ part_000.gz
 ┃ ┃ ┃ ┃ ┣ sources
 ┃ ┃ ┃ ┃ ┃ ┗ updated_date=2023-06-08
 ┃ ┃ ┃ ┃ ┃ ┃ ┗ part_000.gz
 ┃ ┃ ┃ ┃ ┗ works
 ┃ ┃ ┃ ┃ ┃ ┗ updated_date=2023-06-08
 ┃ ┃ ┃ ┃ ┃ ┃ ┗ part_000.gz
 ┃ ┃ ┗ python code
 ┃ ┃ ┃ ┣ __pycache__
 ┃ ┃ ┃ ┃ ┣ json_to_csv.cpython-311.pyc
 ┃ ┃ ┃ ┃ ┗ json_to_csv.cpython-39.pyc
 ┃ ┃ ┃ ┣ flatten_author.py
 ┃ ┃ ┃ ┣ flatten_concept.py
 ┃ ┃ ┃ ┣ flatten_funder.py
 ┃ ┃ ┃ ┣ flatten_institution.py
 ┃ ┃ ┃ ┣ flatten_publisher.py
 ┃ ┃ ┃ ┣ flatten_source.py
 ┃ ┃ ┃ ┣ flatten_work.py
 ┃ ┃ ┃ ┗ json_to_csv.py
 ┣ report
 ┃ ┣ figs
 ┃ ┃ ┣ concept_node.png
 ┃ ┃ ┣ multiple_records.jpg
 ┃ ┃ ┣ node_relationship.jpg
 ┃ ┃ ┣ reformat_example.png
 ┃ ┃ ┗ schema.png
 ┃ ┣ subfiles
 ┃ ┃ ┣ conclusion.tex
 ┃ ┃ ┣ facerecognition.tex
 ┃ ┃ ┣ futurework.tex
 ┃ ┃ ┣ intro.tex
 ┃ ┃ ┣ mainwork.tex
 ┃ ┃ ┗ neo4j.tex
 ┃ ┣ indent.log
 ┃ ┣ report.aux
 ┃ ┣ report.log
 ┃ ┣ report.out
 ┃ ┣ report.pdf
 ┃ ┣ report.synctex.gz
 ┃ ┗ report.tex
 ┣ README.md
 ┗ requirements.txt
```

## Demo video

https://drive.google.com/file/d/1vxYMjJZl99S6WMsgOmDbdbNJx_MHBUqu/view?usp=sharing

## Issues and Future Work

* scholarly web-scraping package has a dayly use limit. If you reach the limit, it will show: too many requests.

## References 

* Dataset: https://openalex.s3.amazonaws.com/browse.html#data/
* Scholarly: https://scholarly.readthedocs.io/en/stable/quickstart.html
* SerpAPI: https://serpapi.com/google-scholar-api

  

