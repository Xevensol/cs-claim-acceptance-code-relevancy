from app.core.config import settings
import pyodbc
from fastapi import HTTPException

MSSQL_SERVER = settings.MSSQL_SERVER
MSSQL_DATABASE = settings.MSSQL_DATABASE
MSSQL_USER = settings.MSSQL_USER
MSSQL_PASSWORD = settings.MSSQL_PASSWORD
    

def get_db_connection():
    try:
        drivers = settings.MSQL_DRIVERS
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
def load_all_sbs_codes(sbs_chapter_names: list[str] = None):
    try:
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                base_query = """
                    SELECT code, summary, chapter_name
                    FROM MedicalCodes 
                    WHERE code_type = 'sbs'
                """

                # Add filtering based on chapter names if provided
                if sbs_chapter_names:
                    # Create placeholders for parameterized query
                    placeholders = ','.join(['?'] * len(sbs_chapter_names))
                    base_query += f" AND chapter_name IN ({placeholders})"
                    cursor.execute(base_query, tuple(sbs_chapter_names))
                else:
                    cursor.execute(base_query)

                results = cursor.fetchall()
                return [(str(row[0]), str(row[1])) for row in results]
            except Exception as e:
                print(f"Query execution error: {e}")
                return []
            finally:
                connection.close()
        return []
    except Exception as e:
        print(f"Database connection error: {e}")
        return []
    

# @st.cache_data(ttl=3600)
def load_all_sbs_codes_chapter_names():
    try:
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                    SELECT DISTINCT chapter_name
                    FROM MedicalCodes 
                    WHERE code_type = 'sbs'
                """
                cursor.execute(query)
                results = cursor.fetchall()
                return [str(row[0]) for row in results if row[0] is not None]
            except Exception as e:
                print(f"Query execution error: {e}")
                return []
            finally:
                connection.close()
        return []
    except Exception as e:
        print(f"Database connection error: {e}")
        return []



def get_icd_descriptions(codes: str):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Split the comma-separated ICD codes into a list
            icd_codes = codes.split(',')

            # Prepare the query with placeholders
            query = f"""
                SELECT code, code_type as type, summary
                FROM MedicalCodes
                WHERE code IN ({','.join(['?'] * len(icd_codes))})
            """
            cursor.execute(query, icd_codes)
            rows = cursor.fetchall()

            # Format results
            result = [
                {'code': row[0], 'type': row[1], 'summary': row[2]}
                for row in rows
            ]

            return {"data": result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching ICD descriptions: {e}")
        finally:
            connection.close()
    raise HTTPException(status_code=500, detail="Database connection failed")