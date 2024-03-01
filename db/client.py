from pymongo import MongoClient

## Conection at remote data base

db_client = MongoClient("mongodb+srv://luchosarli13:lucho2213L@cluster0.pvxlsbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").Backend

## Conecction at local data base
#db_client = MongoClient().local

#print(db_client.list_database_names())