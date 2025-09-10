# esql/versions/esql_v1_0_0/main.py

import sqlite3
from pathlib import Path

class MainCls:
    def __init__(self, connect: str = "sample", message: bool = False, esql_file: bool = True):
        if esql_file:
            base_dir = Path(__file__).parent.parent.parent.parent.parent
            self.db_path = base_dir / "db" / f"{connect}.db"
        else:
            self.db_path = Path(connect)
        self.message = message
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
                if self.message: print("正常にコミットされました。")
            self.conn.close()
            
    def execute(self, query: str):
        self.cursor.execute(query)
        if self.cursor.description:
            return self.cursor.fetchall()
        return None