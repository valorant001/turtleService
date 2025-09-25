# crud.py
from fastapi.responses import JSONResponse
import mysql
from connections import create_connection
from datetime import datetime
import logging
from datetime import datetime
from vaildation import validate_api

def turtleInsert(api: str, model_dict: dict):
    columns = list(model_dict.keys())
    table, safe_columns = validate_api(api, columns)
    if not safe_columns:
        raise ValueError("No valid columns provided for insertion.")
    values = [model_dict[col] for col in safe_columns]
    columns_str = ', '.join(f"`{col}`" for col in safe_columns)
    placeholders = ', '.join(['%s'] * len(safe_columns))
    query = f"INSERT INTO `{table}` ({columns_str}) VALUES ({placeholders})"
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            print(f"Executing query: {query} with values: {values}")
            cursor.execute(query, values)
        conn.commit()
        return True
    finally:
        conn.close()

def save_log(model_dict: dict):
    response = turtleInsert("CREATELOG", model_dict)
    return response

def read_data_with_Specific(api: str,selectedColumn: str ,modeldata: dict,singleFetch: bool):
    conn = create_connection()
    columns = list(modeldata.keys())
    table, safe_columns = validate_api(api, columns)
    if not safe_columns:
        raise ValueError("No valid columns provided for insertion.")
    values = [modeldata[col] for col in safe_columns]
    where_clause = ' AND '.join(f"`{col}` = %s" for col in safe_columns)
    query = f"SELECT {selectedColumn} FROM `{table}` WHERE {where_clause};"
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, values)
            results = cursor.fetchall()
        if results:
             if singleFetch:
                return True, results[0]
             else:
                return True, results
        else:
            return False, []
    finally:
        conn.close()


def read_data(api: str,selectedColumn: str ,modeldata: dict,singleFetch: bool):
    conn = create_connection()
    columns = list(modeldata.keys())
    table, safe_columns = validate_api(api, columns)
    if not safe_columns:
        raise ValueError("No valid columns provided for insertion.")
    query = f"SELECT {selectedColumn} FROM `{table}`;"
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        if results:
             if singleFetch:
                return True, results[0]
             else:
                return True, results
        else:
            return False, []
    finally:
        conn.close()
    
def read_data_using_multiple_source(api: str,selectedColumn: str ,modeldata: dict,singleFetch: bool, table2: str,column2: str,column1: str):
    conn = create_connection()
    columns = list(modeldata.keys())
    table, safe_columns = validate_api(api, columns)
    if not safe_columns:
        raise ValueError("No valid columns provided for insertion.")
    values = [modeldata[col] for col in safe_columns]
    where_clause = ' AND '.join(f"`{table}`.`{col}` = %s" for col in safe_columns)
    query = f"SELECT {selectedColumn} FROM `{table}` JOIN `{table2}` ON `{table}`.`{column1}` = `{table2}`.`{column2}` WHERE {where_clause};"
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, values)
            results = cursor.fetchall()
        if results:
             if singleFetch:
                return True, results[0]
             else:
                return True, results
        else:
            return False, []
    finally:
        conn.close()
