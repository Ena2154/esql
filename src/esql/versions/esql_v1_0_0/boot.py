# esql/versions/esql_v1_0_0/boot.py

from .main import MainCls

def run(db_name, callback, message=False, esql_file:bool = True):
    try:
        with MainCls(connect=db_name, message=message, esql_file=esql_file) as db:
            return callback(db)
    except Exception as e:
        print(f"処理中にエラー: {e}")
        return None