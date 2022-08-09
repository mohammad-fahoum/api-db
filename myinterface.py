import requests, json, ast
import pandas as pd

greeting_statement = """
welcome to the database adminstration interface , the following command are used to make changes to the database:
    API requests help:
        api_help()
    query commands:
        single_query(tbname, columns = '*', cond = '')
        multitable_query(columns = "*", condition = "", **tbnamesandkeys)
    insertion and adding new table commands:
        new_table(table_name, **columns_data_types)
        insert_record(table_name, **items)
    updating operation:
        update_record(table_name, Condition_Statement, **columns_and_values)
        update_table(table_name, **columns_and_values)
    delete operations :
        del_table(table_name)
        del_column(table_name, column_name)
        del_row(table_name, Condition_Statement)
"""
print(greeting_statement)

# this interface should help the user adminstration the database using the command line 

def api_help():
    help_command = requests.post("http://127.0.0.1:5000/help")
    return help_command.text

def single_query(tbname, columns = '*', cond = ''):
    selection_by_attribute = requests.get("http://127.0.0.1:5000/selection-by-attribute", params = {"join-tables":'false',"tbname":tbname, "columns":columns, "condition":cond})
    return pd.DataFrame(ast.literal_eval(selection_by_attribute.text))

def multitable_query(columns = "*", condition = "", **tbnamesandkeys):
    selection_by_attribute_with_join = requests.get("http://127.0.0.1:5000/selection-by-attribute", params = {"join-tables":'true',"tbnames":json.dumps(tbnamesandkeys), "columns":columns, "condition":condition})
    return pd.DataFrame(ast.literal_eval(selection_by_attribute_with_join.text))

def new_table(table_name, **columns_data_types):
    create_table = requests.post("http://127.0.0.1:5000/create-table", params = {"tbname":table_name, "columns":json.dumps(columns_data_types)})
    return f"status : {create_table.text}  |  connection status : {create_table.status_code}"

def insert_record(table_name, **items):
    insert_record = requests.post("http://127.0.0.1:5000/insert-record", params = {"tbname":table_name, "items":json.dumps(items)})
    return f"status : {insert_record.text}  |  connection status : {insert_record.status_code}"

def update_record(table_name, Condition_Statement, **columns_and_values):
    update_table = requests.post("http://127.0.0.1:5000/update-table", params = {"tbname":table_name, "columns-and-values":json.dumps(columns_and_values),"condition":Condition_Statement})
    return f"status : {update_table.text}  |  connection status : {update_table.status_code}"

def update_table(table_name, **columns_and_values):   
    update_full_table = requests.post("http://127.0.0.1:5000/update-full-table", params = {"tbname":table_name, "columns-and-values":json.dumps(columns_and_values)})
    return f"status : {update_full_table.text}  |  connection status : {update_full_table.status_code}"

def del_table(table_name):    
    delete_table = requests.post("http://127.0.0.1:5000/delete-function", params = {"delete":"table", "tbname":table_name})
    return f"status : {delete_table.text}  |  connection status : {delete_table.status_code}"

def del_column(table_name, column_name):    
    delete_column = requests.post("http://127.0.0.1:5000/delete-function", params = {"delete":"column", "tbname":table_name, "column":column_name})
    return f"status : {delete_column.text}  |  connection status : {delete_column.status_code}"

def del_row(table_name, Condition_Statement):        
    delete_row = requests.post("http://127.0.0.1:5000/delete-function", params = {"delete":"record", "tbname":table_name, "condition":Condition_Statement})
    return f"status : {delete_row.text}  |  connection status : {delete_row.status_code}"



# sample of the commands

# faculty = {
#      'faculty_ID' : 'INT PRIMARY KEY NOT NULL',
#      'faculty_name' : 'VARCHAR(100)',
#      'adminstrator' : 'VARCHAR(100)',
#      'openning_date' : 'VARCHAR(100)'
# }
# apartment = {
#     'apt_ID' : 'INT PRIMARY KEY NOT NULL',
#     'faculty_id' : 'INT NOT NULL',
#     'apt_name' : 'VARCHAR(100)',
#     'adminstrator' : 'VARCHAR(100)',
#     'FOREIGN KEY (faculty)' : 'REFERENCES faculty(faculty_ID)'
# }

# data1 = {
#     'faculty_id' : '1',
#     'faculty_name' : "'institute of earth and enviromental science'",
#     'adminstrator' : "'ali nouh'",
#     'openning_date' : "'2014-12-01'"
# }
# data2 = {
#     'apt_ID' : '1',
#     'faculty_id' : '1',
#     'apt_name' : "'geographic information system and remote sensing'",
#     'adminstrator' : "'mohammad fahoum'",
# }
# joins = {
#     "faculty" : "faculty_id",
#     "apartment" : "faculty_id"
# }
# new_table("faculty", **faculty)
# new_table("apartment", **apartment)
# insert_record("faculty", **data1)
# insert_record("apartment", **data2)
# single_query("faculty")
# single_query("apartment")
# multitable_query(faculty = "fauculty_id", apartment = "faculty_id")
# # multitable_query(**joins)
# update_record("faculty", "faculty_id = 1", adminstrator = "'yazan'")
# update_table("apartment", apt_name = "'cypersecurity'", adminstrator = "'mahmoud hammad'")
# insert_record("faculty", faculty_id = "2")
# insert_record("faculty", faculty_id = "3", faculty_name = "'Prince Alhussien Bin Abdullah for Information Technology'")
# del_row("faculty", "faulty_id = 2")
# del_column("apartment", "apt_name")
# del_table("apartment")
# print(api_help())