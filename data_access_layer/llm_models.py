from data_access_layer.db_connection import get_connection

def add_llm_model(name, source, version):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO LLM_Models (name, source, version) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, source, version))
            connection.commit()
        finally:
            cursor.close()
            connection.close()

def get_all_llm_models():
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM LLM_Models")
            return cursor.fetchall()
        finally:
            cursor.close()
            connection.close()
    return None
