# Project Title

This projects demonstrates how to index multiple documents(tagged videos here) in elastic search and query those using keywords.
I have used flask framework to publish rest api which takes keywords as input, triggers elastic search to retrieve matched documents and returns formatted response to caller.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

- Elasticsearch should be installed and running locally on 9200 port.You can download it from link https://www.elastic.co/downloads/elasticsearch. Follow the instrunctions based on operating system(unix,windows,macos etc.) .Upon installation verify it on broweser by URL http://localhost:9200/ and you should see response as below:

    ```
    {
      "name" : "",
      "cluster_name" : "elasticsearch",
      "cluster_uuid" : "UIpupB-nRtqAlmpcATlLjw",
      "version" : {
        "number" : "7.3.1",
        "build_flavor" : "oss",
        "build_type" : "zip",
        "build_hash" : "4749ba6",
        "build_date" : "2019-08-19T20:19:25.651794Z",
        "build_snapshot" : false,
        "lucene_version" : "8.1.0",
        "minimum_wire_compatibility_version" : "6.8.0",
        "minimum_index_compatibility_version" : "6.0.0-beta1"
      },
      "tagline" : "You Know, for Search"
    }
    ```
- Python 3.6 or above is required to run this project.Additional dependencies can be downloaded from pip (python package manager).Refer requirement.txt in project directory. Command to install all required packages through pip:
     ```
     pip install -r requirement.txt
     ```
- File video_details.csv should be placed inside data directory as it is data source for this application. It contains tagged videos information (video id,link and objects with their durations(in seconds)). Few samples:

     
    | id | link                  | objects                                                                 |
    |----|-----------------------|-------------------------------------------------------------------------|
    | 1  | https://testelk.com/1 | car:(0-10)\|\|dog:(2-5)&(55-58)\|\|tree:(13-45)\|\|bird:(22-31)\|\|girl:(10-60) |
    | 2  | https://testelk.in/2  | tree:(3-40)\|\|bird:(50-60)\|\|girl:(20-30)                                 |
    | 3  | https://testelk.in/3  | tree:(2-20)\|\|dog:(45-55)\|\|cat:(20-30)                                   |
       
### Installing



- Clone this repository.
- Install all required packages as mentioned in pre-requisites.
- Execute index_documents.py module (from indexing package) to transform csv to json and index all documents in elastic search.Its one time activity unless we have fresh batch of data or we need to update existing documents.
- After indexing, search can be made on indexed document.Start flask server and publish end point for search api.Command to start flask application is :

    ```
    cd microservice
    python flask_app.py
    ```
- Default port for flask is : 5000 . Once flask is up and running, you should see logs in terminal as below:
    ```
    * Debug mode: off
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    ```
- End point to serve user requests over POST method is : http://localhost:5000/api/search 
   



## Running the tests

Sample requests and responses for API : http://localhost:5000/api/search

- Sample-1 (single keyword as "dog","cat","boy"):
    ```json
        {
      "userInput":"cat"	
        }  
    ```
    
     ```json
       {
      "searchResults": [
        {
          "link": "https://testelk.in/3",
          "objects": [
            {
              "duration": "(20-30)",
              "object": "cat"
            }
          ]
        },
        {
          "link": "https://testelk.in/4",
          "objects": [
            {
              "duration": "(5-20)",
              "object": "cat"
            }
          ]
        }
      ]
    }
    ```
- Sample-2 (Multiple keywords seperated by '&' character.Example -"dog&cat" which means videos with dog and cat together):           
    ```json
    {
    "userInput":"dog&cat"	
    }
    ```
    ```json
    {
      "searchResults": [
        {
          "link": "https://testelk.in/3",
          "objects": [
            {
              "duration": "(45-55)",
              "object": "dog"
            },
            {
              "duration": "(20-30)",
              "object": "cat"
            }
          ]
        },
        {
          "link": "https://testelk.in/4",
          "objects": [
            {
              "duration": "(5-20)",
              "object": "cat"
            },
            {
              "duration": "(10-60)",
              "object": "dog"
            }
          ]
        }
      ]
    }
   ```
- Sample-3 (Multiple keywords seperated by '||' character.Example -"dog||cat" which means videos with dog or cat):
   ```json
    {
    "userInput":"dog||cat"	
    }
    ```  
   ```json
       {
      "searchResults": [
        {
          "link": "https://testelk.in/3",
          "objects": [
            {
              "duration": "(45-55)",
              "object": "dog"
            },
            {
              "duration": "(20-30)",
              "object": "cat"
            }
          ]
        },
        {
          "link": "https://testelk.in/4",
          "objects": [
            {
              "duration": "(5-20)",
              "object": "cat"
            },
            {
              "duration": "(10-60)",
              "object": "dog"
            }
          ]
        },
        {
          "link": "https://testelk.com/1",
          "objects": [
            {
              "duration": "(2-5)&(55-58)",
              "object": "dog"
            }
          ]
        },
        {
          "link": "https://testelk.in/9",
          "objects": [
            {
              "duration": "(37-60)",
              "object": "dog"
            }
          ]
        },
        {
          "link": "https://testelk.in/10",
          "objects": [
            {
              "duration": "(37-60)",
              "object": "dog"
            }
          ]
        },
        {
          "link": "https://testelk.in/12",
          "objects": [
            {
              "duration": "(2-5)&(55-58)",
              "object": "dog"
            }
          ]
        },
        {
          "link": "https://testelk.in/15",
          "objects": [
            {
              "duration": "(3-40)",
              "object": "dog"
            }
          ]
        },
        {
          "link": "https://testelk.in/21",
          "objects": [
            {
              "duration": "(4-5)&(35-38)",
              "object": "dog"
            }
          ]
        },
        {
          "link": "https://testelk.in/22",
          "objects": [
            {
              "duration": "(2-5)&(55-58)",
              "object": "dog"
            }
          ]
        },
        {
          "link": "https://testelk.in/23",
          "objects": [
            {
              "duration": "(2-5)&(55-58)",
              "object": "dog"
            }
          ]
        }
      ]
    }
     ```


