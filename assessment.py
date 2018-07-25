import xlrd
import sqlite3
import os

def retrieve_excel_file(filename = None,db_name = None,db_table = None):
    work_book = xlrd.open_workbook(filename, on_demand = True)
    sheet_1 = work_book.sheet_by_name(work_book.sheet_names()[0])
    table_fields = sheet_1.row_values(0, start_colx = 0)

    create_database("F:\\"+db_name+".db", db_table, table_fields)

    for row in range(1,sheet_1.nrows-1):
        record = sheet_1.row_values(row, start_colx = 0)
        insert_data(record,"F:\\"+db_name+".db", db_table)

def execute_sql(db_name, sql):
    db_connection = sqlite3.connect(db_name)
    db_cursor = db_connection.cursor()
    db_cursor.execute(sql)
    db_connection.commit()
    db_connection.close()

def create_database(db_name, t_name, t_fields):
    statement = 'CREATE TABLE {table_name} {tab_fields}'
    tab_name_list = tuple(t_fields)
    sql = statement.format(table_name = t_name, tab_fields = tab_name_list)
    execute_sql(db_name, sql)

def insert_data(data, db_name, t_name):
    statement = 'INSERT INTO {table_name} VALUES{values}'
    values_list = tuple(data)
    sql = statement.format(table_name = t_name, values = values_list)

    execute_sql(db_name, sql)

def retrieve_data_from_db(db_name, table_name, *args, **kwargs):
    statement = 'SELECT * FROM {table_name}'
    sql = statement.format(table_name = table_name)
    db_connection = sqlite3.connect(db_name)
    db_cursor = db_connection.cursor()
    records = db_cursor.execute(sql)
    return records
    db_connection.close()

def retrieve_student_data(student_name,table_name,db_name):
    statement = "SELECT * FROM {table_name} WHERE name='{student_name}'"
    sql = statement.format(table_name=table_name,student_name = student_name)
    db_connection = sqlite3.connect(db_name)
    db_cursor = db_connection.cursor()
    records = db_cursor.execute(sql)
    return records
    db_connection.close()

def determine_performance(student_marks):
    total = 0
    EXCELLENT = '#5cf500'#>90
    VERY_GOOD = '#e5ea0b'#>80
    GOOD = '#0be8ea'#>60
    TRIAL = '#ff8300' #>40
    FAIL = '#ff00ba'#<40
    for mark in student_marks:
        total += int(mark)
    average = int(total/len(student_marks))
    if average>=90 and average<= 100:
        return EXCELLENT
    elif average>=80 and average<90:
        #give him VERY_GOOD
        return VERY_GOOD
    elif average>=60 and average <80:
        #give him GOOD
        return GOOD
    elif average>=40 and average <60:
        #give him TRIAL
        return TRIAL
    elif average>=0 and average<40:
        #give him FAIL
        return FAIL
    else:
        pass


def delete_data(data):
    pass

def update_database(data):
    pass

def edit_data(data):
    pass
