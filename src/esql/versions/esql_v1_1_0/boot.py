# esql/versions/esql_v1_1_0/boot.py

from .main import MainCls
import sqlite3

def run(db_name: str, callback, message: bool = False, use_generator: bool = False, query_name: str = "", esql_file: bool = True):
    """
    データベース操作を安全かつ簡潔に実行するための高レベル関数。
    """
    try:
        # MainCls に esql_file を渡す
        with MainCls(connect=db_name, message=message, use_generator=use_generator, esql_file=esql_file) as db:
            return callback(db)
    except (sqlite3.Error, ValueError, ConnectionError) as e:
        error_location = f" in '{query_name}'" if query_name else ""
        print(f"データベース処理中{error_location}にエラーが発生しました: {e}")
        return None