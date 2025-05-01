from google.cloud.sql.connector import Connector, IPTypes
import pg8000.native
import os

connector = Connector()

def getconn() -> pg8000.native.Connection:
        return connector.connect(
            os.environ["INSTANCE_CONNECTION_NAME"],
            "pg8000",
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASS"],
            db=os.environ["DB_NAME"],
            ip_type=IPTypes.PUBLIC
        )