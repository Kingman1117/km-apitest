"""清除所有客户端 session 缓存"""
from pathlib import Path

API_TESTS_DIR = Path(__file__).parent.parent / "api_tests"

CACHE_FILES = [
    ".session_cache.pkl",        # Admin
    ".edupc_session_cache.pkl",  # EduPC
    ".h5_session_cache.pkl",     # H5
]


def main():
    cleared = 0
    for filename in CACHE_FILES:
        cache_file = API_TESTS_DIR / filename
        if cache_file.exists():
            cache_file.unlink()
            print(f"[OK] 已删除: {filename}")
            cleared += 1
        else:
            print(f"[SKIP] 不存在: {filename}")
    
    if cleared:
        print(f"\n共清除 {cleared} 个缓存文件")
    else:
        print("\n没有缓存文件需要清除")


if __name__ == "__main__":
    main()
