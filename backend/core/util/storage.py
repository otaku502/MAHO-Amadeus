import sqlite3
from pathlib import Path

def get_database_connection(db_name: str = "database.db") -> sqlite3.Connection:
    """
    获取SQLite数据库连接。如果数据库文件不存在，则创建一个新的数据库文件。

    参数:
        db_name (str): 数据库文件名，默认为"database.db"。

    返回:
        sqlite3.Connection: SQLite数据库连接对象。
    """
    db_path = Path(db_name)
    connection = sqlite3.connect(db_path)
    return connection