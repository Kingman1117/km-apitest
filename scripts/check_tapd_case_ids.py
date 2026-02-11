"""
检查所有API测试用例的TAPD用例ID

扫描所有测试文件，检查是否包含TAPD用例ID
"""
import re
from pathlib import Path

# 项目根目录
ROOT = Path(__file__).parent.parent
API_TESTS_DIR = ROOT / "api_tests"

def extract_tapd_case_id(file_path):
    """从测试文件中提取TAPD用例ID"""
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # 尝试匹配多种格式
        patterns = [
            r'用例\s*ID\s*:\s*(\d+)',           # 用例 ID: 1150695810001062392
            r'用例\s*(\d+)',                     # 用例 1150695810001062392
            r'用例ID:\s*(\d+)',                  # 用例ID:1150695810001062392
            r'TAPD\s*ID\s*:\s*(\d+)',           # TAPD ID: 1150695810001062392
            r'case_id\s*:\s*(\d+)',             # case_id: 1150695810001062392
            r'(\d{19})',                        # 直接匹配19位数字
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                return match.group(1)
        
        return None
    except Exception as e:
        return f"ERROR: {e}"

def check_all_test_files():
    """检查所有测试文件"""
    
    print("=" * 80)
    print("TAPD用例ID检查报告")
    print("=" * 80)
    
    # 收集所有测试文件
    test_files = sorted(API_TESTS_DIR.rglob("test_*.py"))
    
    # 排除conftest.py等非测试文件
    test_files = [f for f in test_files if f.name.startswith("test_") and f.name != "test_api_capture_replay.py"]
    
    missing_ids = []
    found_ids = []
    
    print(f"\n总共发现 {len(test_files)} 个测试文件\n")
    
    # 按模块分组
    modules = {
        'admin': [],
        'edupc': [],
        'h5': []
    }
    
    for file_path in test_files:
        relative_path = file_path.relative_to(API_TESTS_DIR)
        case_id = extract_tapd_case_id(file_path)
        
        # 确定模块
        if 'admin' in str(relative_path):
            module = 'admin'
        elif 'edupc' in str(relative_path):
            module = 'edupc'
        elif 'h5' in str(relative_path):
            module = 'h5'
        else:
            module = 'other'
        
        if case_id:
            found_ids.append({
                'file': str(relative_path),
                'id': case_id,
                'module': module
            })
            modules[module].append((str(relative_path), case_id, True))
        else:
            missing_ids.append({
                'file': str(relative_path),
                'module': module
            })
            modules[module].append((str(relative_path), None, False))
    
    # 打印结果
    for module_name in ['admin', 'edupc', 'h5']:
        if modules[module_name]:
            print(f"\n{'=' * 80}")
            print(f"{module_name.upper()} 模块 ({len(modules[module_name])} 个测试)")
            print(f"{'=' * 80}\n")
            
            for file, case_id, has_id in modules[module_name]:
                if has_id:
                    print(f"[OK] {file:50s} -> {case_id}")
                else:
                    print(f"[MISSING] {file:50s} -> 缺少用例ID")
    
    # 汇总
    print("\n" + "=" * 80)
    print("汇总统计")
    print("=" * 80)
    print(f"\n总测试文件数: {len(test_files)}")
    print(f"包含用例ID:   {len(found_ids)} ({len(found_ids)/len(test_files)*100:.1f}%)")
    print(f"缺少用例ID:   {len(missing_ids)} ({len(missing_ids)/len(test_files)*100:.1f}%)")
    
    if missing_ids:
        print("\n" + "=" * 80)
        print("缺少用例ID的文件列表")
        print("=" * 80)
        print("\n需要补充TAPD用例ID的文件:\n")
        for item in missing_ids:
            print(f"  - {item['file']}")
        
        print("\n" + "=" * 80)
        print("建议操作")
        print("=" * 80)
        print("""
1. 在每个测试文件的模块级docstring中添加用例ID
2. 格式示例:
   
   \"\"\"
   用例 ID: 1150695810001062XXX
   用例描述: XXX功能测试
   
   接口: POST /api/xxx
   \"\"\"

3. 或者使用简化格式:
   
   \"\"\"
   用例 1150695810001062XXX: XXX功能测试
   \"\"\"

4. 确保用例ID是19位数字
5. 用例ID应该在TAPD测试用例库中存在
        """)
    else:
        print("\n[OK] 所有测试文件都包含TAPD用例ID！")
    
    return missing_ids, found_ids

if __name__ == "__main__":
    missing, found = check_all_test_files()
    
    # 返回退出码
    import sys
    sys.exit(len(missing))
