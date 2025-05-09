from weatherutils import main


if __name__ == "__main__":
    
    apikey = ''
    city_names = ['London', 'Dubai', 'Port Louis', 'Paris']
    db = main(apikey=apikey, city_names=city_names)
    db.to_csv('output/weatherdb.csv', index=False)