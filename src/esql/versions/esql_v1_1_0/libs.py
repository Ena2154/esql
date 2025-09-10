# esql/versions/esql_v1_1_0/libs.py

import sqlite3
from pathlib import Path

def parseQuery(args: str):
    queries = args.split(';')
    for q in queries:
        cleaned_q = q.strip()
        if cleaned_q and not cleaned_q.startswith('--') and not cleaned_q.startswith('/*'):
            yield cleaned_q

def read_sql_from_file(file_path: str) -> str:
    try:
        path = Path(file_path)
        return path.read_text(encoding='utf-8')
    except FileNotFoundError:
        raise FileNotFoundError(f"指定されたクエリファイルが見つかりません: {file_path}")
    except Exception as e:
        raise IOError(f"クエリファイルの読み込み中にエラーが発生しました: {e}") from e

def execute_queries_list(cursor, query_string: str) -> list:
    select_results = []
    last_query = ""
    try:
        for q in parseQuery(query_string):
            last_query = q
            cursor.execute(q)
            if cursor.description:
                select_results.append(cursor.fetchall())
    except sqlite3.Error as e:
        raise ValueError(f"SQLの実行に失敗しました。エラー: {e}\n問題のクエリ: '{last_query}'") from e
    return select_results

def execute_queries_generator(cursor, query_string: str):
    last_query = ""
    try:
        for q in parseQuery(query_string):
            last_query = q
            cursor.execute(q)
            if cursor.description:
                yield cursor.fetchall()
    except sqlite3.Error as e:
        raise ValueError(f"SQLの実行に失敗しました。エラー: {e}\n問題のクエリ: '{last_query}'") from e