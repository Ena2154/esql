# esql/__init__.py

from . import version as ver

# --- 各バージョンのモジュールをインポート ---
from .versions.esql_v1_1_0 import boot as boot_v1_1, main as main_v1_1
from .versions.esql_v1_0_0 import boot as boot_v1_0, main as main_v1_0

# --- ファクトリ関数（バージョンに応じて実体を切り替える） ---

def run(db_name, callback, message=False, use_generator=False, query_name: str = "", version=None, esql_file: bool = True): # esql_file を追加
    if version is None:
        version = ver.LATEST_VERSION

    if version == '1.1.0':
        # boot.run に esql_file を渡す
        return boot_v1_1.run(db_name, callback, message, use_generator, query_name, esql_file=esql_file)
    elif version == '1.0.0':
        # ...
        # boot.run に esql_file を渡す
        return boot_v1_0.run(db_name, callback, message, esql_file=esql_file)
    else:
        raise ValueError(f"指定されたバージョン '{version}' は利用できません。")

def Connection(connect="sample", message=False, use_generator=False, version=None, esql_file: bool = True): # esql_file を追加
    if version is None:
        version = ver.LATEST_VERSION
    
    if version == '1.1.0':
        # MainCls に esql_file を渡す
        return main_v1_1.MainCls(connect, message, use_generator, esql_file=esql_file)
    elif version == '1.0.0':
        # MainCls に esql_file を渡す
        return main_v1_0.MainCls(connect, message, esql_file=esql_file)
    else:
        raise ValueError(f"指定されたバージョン '{version}' は利用できません。")