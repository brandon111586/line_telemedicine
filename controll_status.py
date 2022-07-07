def update_status(user_line_id,new_status_number,collection):
    query_line_id = {"Line_id":user_line_id}
    new_status = {"$set":{"Status":new_status_number}}
    collection.update_one(query_line_id,new_status)
    return None
    
def update_data(user_line_id,key,new_data,collection):
    query_line_id = {"Line_id":user_line_id}
    new_data = {"$set":{key:new_data}}
    collection.update_one(query_line_id,new_data)
    return None
