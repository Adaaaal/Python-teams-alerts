import requests
import pyodbc

# URL del Webhook de Power Automate
webhook_url = "URL to power automate"

# Var for conecction to the DB
server = 'DB Server' 
database = 'DB'
username = 'username'
password = 'password'

#Windows autentication
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

#In case you use username and password
conn_str = (
    f'DRIVER={{SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
)


# Función para ejecutar la consulta SQL y obtener resultados
def get_data_from_table(table):
    query = f"""
    Query with the {table}
    """
    
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return results

# Listado de tablas
tables = [
    "[DB].[dbo].[table]"
]

for table in tables:
    results = get_data_from_table(table)
    
    if results:
        for row in results:
            var1, var2 = row

            # Message 
            data = {
                "attachments": [
                    {
                        "contentType": "application/vnd.microsoft.card.adaptive",
                        "content": {
                            "type": "AdaptiveCard",
                            "version": "1.2",
                            "body": [
                                {
                                    "type": "TextBlock",
                                    "text": "**🚨 Alerta de conexión:**",
                                    "weight": "Bolder", 
                                    "size": "Medium" 
                                },
                                {
                                    "type": "TextBlock",
                                    "text": f"Maecenas a massa ut mauris accumsan finibus. Cras a tellus in augue ",
                                    "weight": "Lighter",
                                    "size": "Small"
                                },
                                {
                                    "type": "TextBlock",
                                    "text": f"Praesent ullamcorper libero ut lacus porttitor, ut euismod lacus efficitur.",
                                    "weight": "Lighter", 
                                    "size": "Small"
                                }
                            ]
                        }
                    }
                ]
            }

            # Enviar mensaje a Power Automate
            response = requests.post(webhook_url, json=data)

            if response.status_code == 202:
                print(f"✅ Alert sent successfully")
            else:
                print(f"❌ Error to sent alert")
    else:
        print(f"Ok")