# esql

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

`esql`は、PythonでSQLiteをよりシンプル、安全、そして直感的に扱うためのラッパーライブラリです。定型的なコードをカプセル化することで、開発者はデータベース操作の本質的なロジックに集中でき、SQLインジェクションのような一般的なミスを未然に防ぎます。

## 主な機能

- **高レベルAPI (`run`)**: `try...with...except`といった定型処理を完全に隠蔽します。
- **安全なパラメータ処理**: `execute_with_params()`により、SQLインジェクションを確実に防ぎます。
- **バッチ処理**: `execute_batch()`により、大量の`INSERT`や`UPDATE`を高速に実行できます。
- **多様な実行方法**: 単純なSQL文、複数文のスクリプト、`.sql`ファイルからの読み込みに対応しています。
- **ジェネレータ対応**: `use_generator=True`オプションにより、メモリ効率を向上させます。
- **動的プレースホルダ生成**: `make_placeholder()`により、`INSERT`文のプレースホルダを自動生成します。
- **バージョン管理**: パッケージのバージョンを指定して、過去のAPIとの後方互換性を保ちながら利用できます。

## インストール

プロジェクトのルートディレクトリに `esql` パッケージフォルダをコピーしてください。

## クイックスタート

```python
import esql

def setup_and_show(db):
    db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT); DELETE FROM users;")
    
    insert_sql = "INSERT INTO users (id, name) VALUES (?, ?)"
    users_data = [(1, 'Alice'), (2, 'Bob')]
    db.execute_batch({insert_sql: users_data})
    
    return db.execute("SELECT * FROM users;")

results = esql.run("my_database", setup_and_show)

if results:
    for row in results[0]:
        print(row)
```
導入手順
    解凍する
    このフォルダを適当な場所に置く
    以下のコードをターミナル上でうつ
    python -m install (esql-mainのあるパス)
    完了