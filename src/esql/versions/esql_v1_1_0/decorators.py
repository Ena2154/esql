# ESQL/src/esql/versions/esql_v1_1_0/decorators.py

from functools import wraps
# 同じバージョン内のboot.pyからrun関数をインポート
from .boot import run as esql_run_v1_1_0

def transaction(db_name: str, message: bool = False, use_generator: bool = False, query_name: str = ""):
    """
    関数をデータベーストランザクションとして実行するデコレータ。(v1.1.0専用)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            
            def callback(db):
                # デコレートされた関数の第一引数に 'db' オブジェクトを渡す
                return func(db, *args, **kwargs)

            # 処理名が指定されていなければ、デコレートされた関数名を使用
            final_query_name = query_name or func.__name__
            
            # v1.1.0のrun関数を内部で呼び出す
            return esql_run_v1_1_0(
                db_name=db_name,
                callback=callback,
                message=message,
                use_generator=use_generator,
                query_name=final_query_name
            )
        return wrapper
    return decorator