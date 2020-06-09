# Link Graph Extractor

## Description

This is a crawler that only collects links of a number of domains that is specified in the configurations, stores the collected links on Neo4j.

## Prerequisites

```
pip3 install Scrapy kafka-python neo4j neobolt neotime PyYAML
```

## Usage

First edit `config.yml` file to appropriate values for the arguments. These are Kafka, Neo4j and Scrapy's arguments.

Then run the commands below.

```
python kafka_consumer.py
scrapy crawl graph -s JOBDIR=<crawl-location>
```

## Members

- [Yasin Uygun](https://github.com/yasinuygun)
- [Ramazan Faruk Oğuz](https://github.com/farukoguz)
