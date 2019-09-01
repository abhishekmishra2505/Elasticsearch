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
    | 1  | https://testelk.com/1 | car:(0-10)||dog:(2-5)&(55-58)||tree:(13-45)||bird:(22-31)||girl:(10-60) |
    | 2  | https://testelk.in/2  | tree:(3-40)||bird:(50-60)||girl:(20-30)                                 |
    | 3  | https://testelk.in/3  | tree:(2-20)||dog:(45-55)||cat:(20-30)                                   |
       
### Installing



Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system


