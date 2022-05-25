from datetime import datetime
from pymongo import MongoClient

from kfd_scraper import get_kfd_data
from sfd_scraper import get_sfd_data
from olimp_scraper import get_olimp_data
from bodypack_scraper import get_bodypack_data


LOG_FILE = r'C:/Users/48509/Desktop/supplements_scraper/logs.txt'

def log_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            with open(LOG_FILE, 'a') as file:
                file.write(f'{datetime.now()} {exc}/n')
    return wrapper

@log_error
def init_db(db_name):
    client = MongoClient('localhost', 27017)
    db = client[db_name]

    return db

@log_error
def get_db_collection(db, collection_name):
    return db[collection_name]


@log_error
def get_protein_data(*scrap_funcs):
    data = []
    for scrap_func in scrap_funcs:
        data += scrap_func()
    
    return data

@log_error
def insert_data(collection, data):
    collection.insert_many(data)


if __name__ == '__main__':
    db = init_db('supplements')
    protein_collection = get_db_collection(db, 'proteins')
    print(protein_collection)

    data = get_protein_data(get_kfd_data, 
                            get_sfd_data, 
                            get_olimp_data, 
                            get_bodypack_data)
    print(data[0])
    insert_data(protein_collection, data)

