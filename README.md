# Link Graph Extractor

## Usage

First edit `config.yml` file to appropriate values for the arguments. These are Kafka, Neo4j and Scrapy's arguments.

Then run the commands below.

```
python kafka_consumer.py
scrapy crawl graph -s JOBDIR=<crawl-location>
```
