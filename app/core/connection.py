from app.core.config import settings
import pyodbc
from fastapi import HTTPException
# import streamlit as st

MSSQL_SERVER =settings.MSSQL_SERVER
MSSQL_DATABASE= settings.MSSQL_DATABASE
MSSQL_USER= settings.MSSQL_USER
MSSQL_PASSWORD= settings.MSSQL_PASSWORD
    

def get_db_connection():
    try:
        drivers = ['{SQL Server}', '{ODBC Driver 17 for SQL Server}']
        for driver in drivers:
            try:
                conn_str = (
                    f'DRIVER={driver};'
                    f'SERVER={MSSQL_SERVER};'
                    f'DATABASE={MSSQL_DATABASE};'
                    f'UID={MSSQL_USER};'
                    f'PWD={MSSQL_PASSWORD}'
                )
                return pyodbc.connect(conn_str)
            except pyodbc.Error:
                continue
        raise Exception("No working driver found")
    except Exception as e:
        return None
    


# @st.cache_data(ttl=3600)
def load_all_icd_codes():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                SELECT code, summary
                FROM MedicalCodes 
                WHERE code_type = 'icd'
                AND code LIKE '%[0-9].%'
            """
            cursor.execute(query)
            results = cursor.fetchall()
            return [(str(row[0]), str(row[1])) for row in results]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching ICD codes: {e}")
        finally:
            connection.close()
    raise HTTPException(status_code=500, detail="Database connection failed")


# @st.cache_data(ttl=3600)
def load_all_cpt_codes():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                SELECT code, summary
                FROM MedicalCodes 
                WHERE code_type = 'cpt'
            """
            cursor.execute(query)
            results = cursor.fetchall()
            return [(str(row[0]), str(row[1])) for row in results]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching CPT codes: {e}")
        finally:
            connection.close()
    raise HTTPException(status_code=500, detail="Database connection failed")


# @st.cache_data(ttl=3600)
def load_all_sbs_codes():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                SELECT code, summary
                FROM MedicalCodes 
                WHERE code_type = 'sbs'
            """
            cursor.execute(query)
            results = cursor.fetchall()
            return [(str(row[0]), str(row[1])) for row in results]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching SBS codes: {e}")
        finally:
            connection.close()
    raise HTTPException(status_code=500, detail="Database connection failed")


def get_icd_descriptions(codes: str):
 
    try:
        # Split the comma-separated ICD codes into a list
        icd_codes = codes.split(',')
 
        # Establish a database connection
        conn = get_db_connection()
        cur = conn.cursor()
 
        # Prepare the query to get the summaries for the provided ICD codes
        query = """
        SELECT code, code_type as type, summary
        FROM MedicalCodes
        WHERE code IN ({})
        """.format(','.join(['?'] * len(icd_codes)))
 
        # Execute the query and fetch the results
        cur.execute(query, icd_codes)
        rows = cur.fetchall()
 
        # Prepare the response
        result = []
        for row in rows:
            result.append({'code' : row[0], 'type' : row[1], 'summary' : row[2]})
 
        # Close the connection
        cur.close()
        conn.close()
        
        # Return the structured response
        return {"data": result}
        # return JSONResponse(
        #     status_code=200,
        #     content={
        #         "status": "success",
        #         "data": result
        #     }
        # )
 
    except Exception as e: 
        return None