from managedb import *
from flask import Flask, request
import json

app = Flask(__name__, template_folder = '/templates')

try:
    db = Pgadmin() # create postgres connection with default settings : database = 'postgres', user = 'postgres', password = 'postgres', host = '127.0.0.1', port = '5432'
except:
    db = SimpleDB(dbname = "apidb.db")

# create tables, insertion, updating, deleting, have a link for selecting with option to join two tables 
# separately write a code to interface with this api and use to create tables add data and select data

@app.route("/help", methods = ['POST', 'GET'])
def help_():
    help_statement = """
    the following statements are a samples of making a change in the database using get and post method (you can make requests using neither of two method):
        query commands:
            selection_by_attribute = requests.get("http://127.0.0.1:5000/selection-by-attribute", params = {"join-tables":'false',"tbname":table_name, "columns":"column1, column2 ..", "condition":"WHERE Condition_Statement"})
            selection_by_attribute_with_join = requests.get("http://127.0.0.1:5000/selection-by-attribute", params = {"join-tables":'true',"tbnames":json.dumps(join_keys), "columns":"column1, column2 ..", "condition":"WHERE Condition_Statement"})
        insertion and adding new table commands:
            create_table = requests.post("http://127.0.0.1:5000/create-table", params = {"tbname":table_name, "columns":json.dumps(columns_data_types)})
            insert_record = requests.post("http://127.0.0.1:5000/insert-record", params = {"tbname":table_name, "items":json.dumps(items)})
        updating operation:
            update_record = requests.post("http://127.0.0.1:5000/update-table", params = {"tbname":table_name, "columns-and-values":json.dump(columns),"condition":"Condition_Statement"})
            update_full_table = requests.post("http://127.0.0.1:5000/update-full-table", params = {"tbname":table_name, "columns-and-values":json.dump(columns)})
        delete operations :
            delete_table = requests.post("http://127.0.0.1:5000/delete-function", params = {"delete":"table", "tbname":table_name})
            delete_column = requests.post("http://127.0.0.1:5000/delete-function", params = {"delete":"column", "tbname":table_name, "column":column_name})
            delete_row = requests.post("http://127.0.0.1:5000/delete-function", params = {"delete":"record|row", "tbname":table_name, "condition":"Condition_Statement"})
    """
    return help_statement

@app.route("/create-table", methods = ['POST', 'GET'])
def create_table():
    tbname = request.args.get("tbname", type = str)
    columns = request.args.get("columns", type = str)
    db.add_table(tbname, **(json.loads(columns)))
    return "New table created successfully"

@app.route("/insert-record", methods = ['POST', 'GET'])
def insert_record():
    tbname = request.args.get("tbname", type = str)
    items = request.args.get("items", type = str)
    db.add_record(tbname, **(json.loads(items)))
    return f"New record inserted successfully"

@app.route("/update-table", methods = ['POST', 'GET'])
def update_table():
    tbname = request.args.get("tbname", type = str)
    columns_and_values = request.args.get("columns-and-values", type = str)
    condition = request.args.get("condition", default = "", type = str)
    db.update_table(tbname, condition, **(json.loads(columns_and_values)))
    return f"Table {tbname} updated successfully"

@app.route("/update-full-table", methods = ['POST', 'GET'])
def update_all_columns():
    tbname = request.args.get("tbname", type = str)
    columns_and_values = request.args.get("columns-and-values", type = str)
    db.update_full_table(tbname, **(json.loads(columns_and_values)))
    return f"All specified columns from table {tbname} updated successfully"

@app.route("/delete-function", methods = ['POST', 'GET'])
def deleting():
    choice = request.args.get("delete", type = str)
    choice = choice.lower()
    if choice == "table":
        tbname = request.args.get("tbname", type = str)
        db.remove_table(tbname)
        return f"Table {tbname} removed successfully from the database"
    elif choice == "column":
        tbname = request.args.get("tbname", type = str)
        column_name = request.args.get("column", type = str)
        db.remove_column(tbname, column_name)
        return f"Column {column_name} removed successfully from the table {tbname}"
    elif choice == "record" or choice == "row":
        tbname = request.args.get("tbname", type = str)
        condition = request.args.get("condition", type = str)
        db.remove_record(tbname, condition)
        return f"Record removed successfully from the table {tbname} based on the condition 'WHERE {condition}'"
    else:
        return "Undefined choice the choice parameter takes one of the following argument : table, column and record or row"
    
@app.route("/selection-by-attribute", methods = ['POST', 'GET'])
def selection():
    choice = request.args.get("join-tables", type = str)
    if choice.lower() == "true":
        tbname = request.args.get("tbnames", type = str)
        columns = request.args.get("columns", default = "*",type = str)
        condition = request.args.get("condition", default = "",type = str)
        output = db.join_tables(columns, condition, **(json.loads(tbname)))
        # return pd.DataFrame(output, columns = columns.split(","))
        return str(output)
    elif choice.lower() == "false":
        tbname = request.args.get("tbname", type = str)
        columns = request.args.get("columns", default = "*", type = str)
        condition = request.args.get("condition", default = "", type = str)
        output = db.call_record(tbname, columns, condition)
        # return str(pd.DataFrame(output, columns = columns.split(",")))
        return str(output)


if __name__ == "__main__":
    app.run(debug = True)

