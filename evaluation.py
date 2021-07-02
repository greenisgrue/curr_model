import pymongo
  

connection_url = 'mongodb+srv://dbUser:dbUserPassword@cluster0.ifjkb.mongodb.net/CI_ratings?retryWrites=true&w=majority'
client = pymongo.MongoClient(connection_url)
  
# Database Name
db = client["CI_ratings"]
  
# Collection Name
col = db["ratings_opti"]


def get_average_rating(model):
    data = col.find({},{'_id': 0})
    total_rating = 0
    count = 0
    for d in data:
        metadata = list(d.values())
        for m in metadata:
            if type(m) is dict:
                if m.get('model_type') == model:
                    rating = m.get('rating')
                    total_rating += rating
                    count += 1

    return total_rating / count


def get_average_value(model):
    data = col.find({},{'_id': 0})
    value_dict = {'value_total': 0, 'value_up': 0, 'value_down': 0, 'count_total': 0, 'count_up': 0, 'count_down': 0}
    for d in data:
        metadata = list(d.values())
        for m in metadata:
            if type(m) is dict:
                if m.get('model_type') == model:
                    value = m.get('value')
                    rating = m.get('rating')
                    value_dict['value_total'] += float(value)
                    value_dict['count_total'] += 1
                    if rating == 1:
                        value_dict['value_up'] += float(value)
                        value_dict['count_up'] += 1
                    elif rating == -1:
                        value_dict['value_down'] += float(value)
                        value_dict['count_down'] += 1
   
    value_dict['value_total'] = value_dict['value_total'] / value_dict['count_total']
    value_dict['value_up'] = value_dict['value_up'] / value_dict['count_up']
    value_dict['value_down'] = value_dict['value_down'] / value_dict['count_down']

    return value_dict  

def get_value_list(model, rating):
    data = col.find({},{'_id': 0})
    value_list = []
    for d in data:
        metadata = list(d.values())
        for m in metadata:
            if type(m) is dict:
                if m.get('model_type') == model and m.get('rating') == rating:
                    value_list.append(m.get('value'))

    print(value_list)




model_type_1 = 'opti_cos'
model_type_2 = 'opti_wmd'

average_rating = get_average_rating(model_type_1)
print(f'Average rating for {model_type_1} is {average_rating}')
average_value = get_average_value(model_type_1)
print(f'Values for {model_type_1} is {average_value}')

average_rating = get_average_rating(model_type_2)
print(f'Average rating for {model_type_2} is {average_rating}')
average_value = get_average_value(model_type_2)
print(f'Values for {model_type_2} is {average_value}')

get_value_list(model_type_1, -1)


