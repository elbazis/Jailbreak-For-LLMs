from data_access_layer.db_connection import get_connection

def add_attack_prompt(prompt, new_old_attack):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO Attack_Prompts (prompt, new_old_attack) VALUES (%s, %s)"
            cursor.execute(query, (prompt, new_old_attack))
            connection.commit()
        finally:
            cursor.close()
            connection.close()

def get_all_attack_prompts():
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Attack_Prompts")
            return cursor.fetchall()
        finally:
            cursor.close()
            connection.close()
    return None
