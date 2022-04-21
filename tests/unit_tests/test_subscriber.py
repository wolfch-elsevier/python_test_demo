
def test_subscriber_collection(mongodb):
    cols = mongodb.list_collection_names()
    print(cols)
    assert "subscribers" in cols
    record = mongodb.subscribers.find_one({'name': 'Reginald Miller'})
    assert record != None
    print(record)
    
