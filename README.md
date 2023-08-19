# THE SUPER DUPER SUMMER DIY TAX CALCULATOR

## Running the project

- Assuming you have docker set up, (if not download it from https://www.docker.com).
- Open a terminal inside the project directory and run
```
$ docker compose up --build
```

- **Make sure** migrations are up to date for the project, in the docker CLI run **if necessary**
```
$ python manage.py migrate
```

### Running the docs
- Now go tο your browser at ```localhost:8000/docs```

#### Uploading transactions
- To upload the transactions, hit the POST ```transactions/``` endpoint with your data.csv file and a name for the report
- This returns the uuid and name of the report, you will need to copy the uuid in order to retrieve the report

#### Retrieving a report
- To retrieve a report, hit the GET ```reports/<uuid>/``` endpoint with the copied uuid from above, you should now see your tax data

#### Retrieving all reports
- In case you lost your report uuid or have multiple reports and would like to see all of them you can hit the GET ```reports/``` endpoint, which would respond with a list of all available reports in the database together with their uuid.

### Running the tests
- In your docker CLI run 
``` 
$ python manage.py tests
```


## Additional Context
- I added a lot of things in this project, taking a little over 3 development hours. When starting the project I wanted something that would check the following 3 things.
1. Run on all machines
2. Run correctly
3. Be well documented, and a bit automated

- In my mind all of these 3 were checked, using docker to run on everything, having some basic tests in order to ensure correct implementation, and using drf-spectacular in order to ensure API documentation
- I chose django because it really is a "batteries included" framework, that ensures fast development time.
- My thought process behind creating the design was that the users should be able to upload multiple files (for api re-use) and to somehow identify them so he doesn't get confused.

- Some assumptions made:
1. A basic understanding of running APIs by the user
2. A somewhat "clean" data file

## Shortcomings
- No environment vars. I wanted to extract some things to an .env file in order to increase security (currently my django secret is exposed inside the app)
- More testing, I only created 4 basic tests given the time, I would test the input file more thoroughly and the other 2 endpoints to get the reports (such as invalid uuid), or trying to save duplicate uuid in db (which is unlikely)
- I think I would change my POST ```/transactions``` to a POST ```/reports```since that makes more sense in my mind. (but that was a "client requirement" that I couldn't change)

## Additional Time
- There could be several features added in case of more time such as:
1. Group transactions by date/memo/
2. Clean the data better, prepare for worse csv files
3. Support more file extensions
4. Filter transactions by date/memo/type
5. Add ordering
6. Add option for currency (or conversion)