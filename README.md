# FlaskIntroduction

This repo has been updated to work with `Python v3.8` and up.

### How To Run
1. Install `virtualenv`:
```
$ pip install virtualenv
```

2. Open a terminal in the project root directory and run:
```
$ virtualenv env
```

3. Then run the command:
```
$ .\env\Scripts\activate
```

4. Then install the dependencies:
```
$ (env) pip install -r requirements.txt
```

5. Finally start the web server:
```
$ (env) python app.py
```

This server will start on port 5000 by default. You can change this in `app.py` by changing the following line to this:

```python
if __name__ == "__main__":
    app.run(debug=True, port=<desired port>)
    
   

```








For Kafka Consumer: 
Clone the following repo and run: python3 consumer.py -f python.config -t “data_stream” to connect with consumer
https://github.com/suravimandal/Team1_Kafka_Consumer.git

To run the Kafka Consumer for selected features topic: python3 consumer.py -f python.config -t "transformed_data_stream"
To run the Kafka Consumer for raw data features topic: python3 consumer.py -f python.config -t "raw_data_stream"

For The whole app, python flask app:

Clone the following repo and run: python3 pythonfile.py (if any error, run pip3 install -r requirements.txt)
https://github.com/suravimandal/team1_big_data.git , use the branch v0.0.1
Or Download app from GitHub: git clone https://github.com/suravimandal/team1_big_data.git

Run the following code in the terminal (local or GCE terminal to install the app set up)
cd team1_big_data
pip3 install -r requirements.txt —user
pip3 install gunicorn —user
~/.local/bin/gunicorn -b :5000 app:app 

In order to to run the python flask app, to view the UI, to upload and load data files in the UI, broadcast Kafka message topic, need to input the URL in chrome browser : "localhost:5000"
In case want to see the UI hosted in GCE, need to input the URL in chrome browser: ('external IP address': 5000)  [Note:-5000 is the port address]



Files Descriptions:

Uploaded files via UI:
train.csv - this one is raw data upload file with 83 features
test.csv - - this one is raw data upload file with 83 features with test data

Exported files after Data Cleaning, Data prepare and Data transformation is applied using ‘pythonfile.py’ 
y_train.csv - contains only salesprice
X_train.csv - contains selected features except  salesprice
selected.csv - this one is transformed data with 23 features selected exported in CSV file for  ML to be applied, contains id and sales-price

Following 2 are json object will be send to Kafka Producer to be consumed by 2 different consumer group:
selected.json - this one is selected features, with transformed data, send to kaafka topic:  “transformed_data_stream”. This data will be consumed and then apply ML algorithm to process the data in real-time.
train.json - this one is selected features, with transformed data, send to kaafka topic:  “raw_data_stream”. This one will be consumed to be stored into data lake for future use.


Steps to deploy the App in Google Compute Engine:
Ssh from cloud shell to compute engine
gcloud beta compute ssh --zone "us-central1-a" "instance-1" --project "charged-thought-310615”
Authorise shell
Input password: 123456
git clone https://github.com/suravimandal/team1_big_data.git -b v0.0.2

Install docker on GCE: sudo apt-get install docker.io
Install Postgres on GCE: sudo docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres






Use sudo ./start.sh instead of ./start.sh

In order to only explore the data analytics, data cleaning, data transformation part, can run the following python file:
python3 app.py








 












