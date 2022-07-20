import pymongo


class DBHELPER:
    def __init__(self):
        client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
        mydb = client['Customer_Database']
        global information
        information = mydb.customerinformation       # Collection
        global prod
        prod = mydb.product_info

    def insert_user(
            self, username, email, phone, age, gender, no_products,
            products
    ):
        # for i in products:
        print(products)
        shopping_value = 0
        for i in products:
            shopping_value = shopping_value + int(i['productprice'])
        record = {
            'name': username,
            'email': email,
            'phone': phone,
            'age': age,
            'Gender': gender,
            'no_products': no_products,
            'products': products,
            'shopping_value': shopping_value
        }
        information.insert_one(record)
        print('user saved to db')

    def fetch_user(self, data, type):
        for record in information.find({type: data}):
            return record

    def fetch_all(self):
        dataset = information.find({})
        return dataset

    def compare(self, value, operator):
        if operator == 'gt':
            dataset = information.find({"shopping_value": {"$gt": value}})
        else:
            dataset = information.find({"shopping_value": {"$lt": value}})
        return dataset

    def delete_user(self, email):
        information.delete_one(
            {"email": email}
        )

    def update_user(
        self, username, email, phone, age, gender, no_products, products
    ):
        shopping_value = 0
        print(products)
        for i in products:
            print(i['productprice'])
            shopping_value = shopping_value + int(i['productprice'])
        information.update_one(
            {"email": email},
            {
                "$set": {
                    "name": username,
                    "email": email,
                    "phone": phone,
                    'age': age,
                    'Gender': gender,
                    'no_products': no_products,
                    'products': products,
                    'shopping_value': shopping_value
                }
            }
        ),
        print("Userid {} updated !".format(username))

    def get_prod_info(self, prod_name):
        for record in prod.find({'productname': prod_name}):
            return record

    def get_prod_info1(self, data, type):
        list = []
        for record in information.find({type: data}):
            # print(record)
            list.append(record)
            # print(list)
        return list
