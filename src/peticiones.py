from flask import request, jsonify
from google.cloud import bigquery
from google.oauth2 import service_account
from datetime import datetime
import json

# Define el token Bearer para la autenticación
BEARER_TOKEN = '49fce305f98ee39bbb89c3da8c6e94d1'

#Variables de autenticacion
private_key = "36edd0099f88b73fd3c5eb72c74220d6a3264f6d"
client_id = "113747543962999405569"

# BigQuery configuration
# Replace with your actual project ID, dataset ID, and table ID
PROJECT_ID = "consejo-colombiano-seguridad"
DATASET_ID = "PortalAfiliadosStaging"
TABLE_ID = "STG_logs_usuarios_adm"

def autenticar(client_id, private_key):
    # Tu función de autenticación aquí
    try:
        credentials_info = {
            "type": "service_account",
            "project_id": PROJECT_ID,
            "private_key_id": private_key,
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCVZBW3yAISP76f\nkB2dpzzfwh9s96GpmDH6hBCyOVyN8t+j3g+ZxnNQlxhCzu43UNz/LZDoPaKoU55z\ntcDm/kcjXdUX9WD600Aem650NZ0xfNv8/LTNOHmSrUiDz7KjImlF/hRH5G3yxbEq\ndL/drHZL2FOREMkWlYpfXrG8/w3Tk9czmQHFF1omEkyn/AeKk/ymfuaTjuX+Mexa\n6s2kYc/mVZOP2OgtC7GfdZu2qBuaxyJprvf9CtJNddFq5rOz8OsXz7zFnsqWUwmk\nJ3j5Ql5MfqIBM6W4sSk5rtRbyCCjCEVzWtea412ksXxohPURC3K3GLHUMHAgzTHs\nyI8XL0U1AgMBAAECggEAFBt9hNgJ11T3Hljyc4bP/boOKseF3eLbT0G5UZPA7mYz\nTcYUyXjZio5buJpLm+xpYntKlse8/fULTb238h9lidAWX3wqingmmDgSGhghSUjp\n/zowR7MDQgfKy9sHy0dVbhNNvYN0fQm41+MQ9BBDd9/tF4hv2HdWQZHoUGzv+nsl\n4HqiulkpfehG6bhPi8hB+P4mVg3vEMvv4MNeCVPvC0FnIFc4PDxF8JtaXq36FWfY\nusH8ngzAGFFg0N/OYfIT6hCewmomLXC8oQKqK325iIaTNrIglgP+OnmpyeWtOtgt\n7j1GyUg/eCrID4zL6L3K98MKkfq66oeEY3/jkx9l3QKBgQDSvd7uE0Cx8TtglmhA\nMCMEzUCvQd7qG5OMvth8aokeFNw1If8Mv/Jr8gVci5FDefMTC99YarYA+nc7fBZ4\ns1TF6rjKA6cde2fUlV5aohxCxBbznj7igUH0V4X/V9AUErpOgPR0eBgdXuPmso+q\n3OH5Ghwz3MFtv76dX0hq5udjnwKBgQC1eUgaV1K6sPFdt7DSWYwcSuNl1bpmMwme\nMGTjw9/SuSuFjsfRZoZq4wEB5xTZP70KvAYHLYdIOVNaomGfGvK/+TZiQgN/9Zlz\nhQpTLzBo1tjuZoQQNPNko7VCnTCUXrHVrQg9gfR4Ebse1BY3UvZvNRao8m7lb9/b\nmOXjnXYGqwKBgEz+odxJnHFmuVLooN4SuDig5OkjH9ZYjOf3MhECu2YKKQogiZaW\n6nMV0W+mbkRA4dYrmEYtdqGU4MsS4wLmQiqtPyZPf1b+J0k76WUjpT+fdOM9Bayr\nnPUwpPxNkPBEh1z3MFj9J5JTgOBgjKzYVpc0OumX1fPLAlFs5oBoLFHxAoGBAJ9h\nMxgfVUMtn+4lJCC6ELnQc8K+YQTdEjdiXVlEcFEL29NiwM+B8c/yKrJXFxJuTkMd\nO1YWgFfIMRLKxl4MNuKvpznIrHY3Z1vznkvMiAGrn75RPu9U8eaTeOBWWZIVUK5P\nV4tdlS3WtLawogpYzKKCx7H9qbPL+5lLwauUYVIdAoGAGaZ/97OcN1v/9ReWK08U\nmHJMj0ZEMMlCUYnNYCscGW2vgoKycq8tbJ8tNgPpe2j4DqQ9Iy5XPySyRpIxvYs2\nN8Zc5tkcsR0jhCpRg6qMdLl/pnbO6qbcMWTotfoJLQ9IPtHjmo81bgI6WOuOHAS5\n64MHPUCGmmt0vzcngjJ3Bfo=\n-----END PRIVATE KEY-----\n",
            "client_email": "consejo-colombiano-seguridad-o@consejo-colombiano-seguridad.iam.gserviceaccount.com",
            "client_id": client_id,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/consejo-colombiano-seguridad-o%40consejo-colombiano-seguridad.iam.gserviceaccount.com",
        }
        credentials_json = json.dumps(credentials_info)
        credentials = service_account.Credentials.from_service_account_info(json.loads(credentials_json))

        return credentials

    except Exception as e:
        print(f"Error creando credenciales: {e}")
        return None

def process_data(raw_data):
    # Tu función de procesamiento de datos aquí
    if isinstance(raw_data, dict):
        processed_data = [raw_data]
    elif isinstance(raw_data, list):
        processed_data = raw_data
    else:
        raise ValueError("Formato no soportado")
    return processed_data


def insertar():

    try:
        # Verificar la clave de autenticación en los encabezados de la solicitud
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            print("error: Unauthorized"), 401
            return jsonify({"error": "Unauthorized"})

        token = auth_header.split(' ')[1]
        if token != BEARER_TOKEN:
            print("error: Unauthorized")
            return jsonify({"error": "Unauthorized"}), 401


        raw_data = request.get_json()
        if not raw_data:
            return {"error": "No data provided"}, 400

        credentials = autenticar(client_id, private_key) # Reemplaza con tus valores
        if not credentials:
             return {"error": "Error autenticando 1"}, 401

        client = bigquery.Client(project=PROJECT_ID, credentials=credentials)
        table_ref = client.dataset(DATASET_ID).table(TABLE_ID)
        table = client.get_table(table_ref)

        processed_data = process_data(raw_data)

        errors = client.insert_rows(table, processed_data)
        if errors:
            print(f"Errores al insertar filas: {errors}")
            return errors[0], 400
        else:
            return {"message": "Datos insertados exitosamente"}, 201

    except Exception as e:
        print(f"Error al insertar: {e}")
        return {"error": str(e)}, 500


def query():
    try:
        # Verificar la clave de autenticación en los encabezados de la solicitud
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            print("error: Unauthorized"), 401
            return jsonify({"error": "Unauthorized"})

        token = auth_header.split(' ')[1]
        if token != BEARER_TOKEN:
            print("error: Unauthorized")
            return jsonify({"error": "Unauthorized"}), 401

        credentials = autenticar(client_id, private_key) # Reemplaza con tus valores

        if not credentials:
            print("error: Autenticación fallida")
            return {"error": "Error autenticando 2"}, 401

        client = bigquery.Client(project=PROJECT_ID, credentials=credentials)
        table_ref = client.dataset(DATASET_ID).table(TABLE_ID)

        # Verificar si el encabezado 'Origen' contiene 'pruebas' y ajustar la tabla
        query = f"SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}` WHERE CONTAINS_SUBSTR(LOWER(origen), 'pruebas')"

        query_job = client.query(query)
        results = query_job.result()

        data = [dict(row) for row in results]

        return {"data": data}, 200

    except Exception as e:
        return {"error": str(e)}, 500
