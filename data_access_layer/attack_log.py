from data_access_layer.db_connection import get_connection

def add_attack_log(attack_prompt_id, target_model_id, response, grade):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """INSERT INTO Attack_Log (attack_prompt_id, target_model_id, model_response, evaluation_score)
                       VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, (attack_prompt_id, target_model_id, response, grade))
            connection.commit()
        finally:
            cursor.close()
            connection.close()

def get_all_attack_logs():
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Attack_Log")
            return cursor.fetchall()
        finally:
            cursor.close()
            connection.close()
