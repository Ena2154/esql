# esql/versions/esql_v1_1_0/main.py

import sqlite3
from pathlib import Path
from . import libs
from typing import Generator, Any, Iterable

class MainCls:
    def __init__(self, connect: str = "sample", message: bool = False, use_generator: bool = False, esql_file: bool = True):
        if esql_file:
            # esql_file=True (デフォルト) の場合、ライブラリ内のdbフォルダに接続
            base_dir = Path(__file__).parent.parent.parent.parent.parent
            self.db_path = base_dir / "db" / f"{connect}.db"
        else:
            # esql_file=False の場合、connect引数をフルパスとして扱う
            self.db_path = Path(connect)
        self.message = message
        self.use_generator = use_generator
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
                if self.message:
                    print(f"クエリは正常に実行され、変更がコミットされました。")
            self.conn.close()

    def execute(self, query: str, from_file: bool = False) -> list | None | Generator[list, Any, None]:
        if not self.cursor:
            raise ConnectionError("データベースに接続されていません。")
        query_string = libs.read_sql_from_file(query) if from_file else query
        if self.use_generator:
            return libs.execute_queries_generator(self.cursor, query_string)
        else:
            results = libs.execute_queries_list(self.cursor, query_string)
            return results if results else None

    def execute_with_params(self, sql: str, params: Iterable) -> list | None:
        if not self.cursor:
            raise ConnectionError("データベースに接続されていません。")
        try:
            self.cursor.execute(sql, params)
            if self.cursor.description:
                return self.cursor.fetchall()
            else:
                return None
        except sqlite3.Error as e:
            raise ValueError(f"パラメータ付きSQLの実行に失敗しました。エラー: {e}\nSQL: {sql}\nParams: {params}") from e

    def execute_batch(self, batch_data: dict[str, Iterable[Iterable]]) -> None:
        if not self.cursor:
            raise ConnectionError("データベースに接続されていません。")
        try:
            for sql, params_list in batch_data.items():
                self.cursor.executemany(sql, params_list)
        except sqlite3.Error as e:
            problem_sql = sql if 'sql' in locals() else "N/A"
            raise ValueError(f"バッチ処理の実行に失敗しました。エラー: {e}\n問題のSQLの可能性: {problem_sql}") from e

    def make_placeholder(self, table_name: str) -> str:
        if not self.cursor:
            raise ConnectionError("データベースに接続されていません。")
        table_info = self.execute_with_params(f"PRAGMA table_info(?);", (table_name,))
        if not table_info:
            raise ValueError(f"テーブル '{table_name}' が見つかりません。")
        num_columns = len(table_info)
        if num_columns == 0:
            raise ValueError(f"テーブル '{table_name}' には列がありません。")
        placeholders = ", ".join(['?'] * num_columns)
        return f"({placeholders})"