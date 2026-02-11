"""提交代码到 GitHub"""
import os
import subprocess
import sys

# 项目根目录
ROOT_DIR = r"e:\MCP测试\kmsk"
REMOTE_URL = "https://github.com/Kingman1117/km-apitest.git"

def run_cmd(cmd, cwd=ROOT_DIR):
    """执行命令"""
    print(f"[CMD] {cmd}")
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode

def main():
    os.chdir(ROOT_DIR)
    
    # 1. 初始化 git（如果未初始化）
    if not os.path.exists(os.path.join(ROOT_DIR, ".git")):
        print("\n[步骤1] 初始化 git 仓库...")
        run_cmd("git init")
    else:
        print("\n[步骤1] git 仓库已存在，跳过初始化")
    
    # 2. 配置用户信息（如果未配置）
    print("\n[步骤2] 配置 git 用户信息...")
    run_cmd('git config user.name "Kingman1117"')
    run_cmd('git config user.email "kingman1117@users.noreply.github.com"')
    
    # 3. 添加远程仓库
    print("\n[步骤3] 配置远程仓库...")
    run_cmd("git remote remove origin")  # 先删除旧的（如果有）
    run_cmd(f"git remote add origin {REMOTE_URL}")
    
    # 4. 添加所有文件
    print("\n[步骤4] 添加文件到暂存区...")
    run_cmd("git add .")
    
    # 5. 查看状态
    print("\n[步骤5] 查看 git 状态...")
    run_cmd("git status")
    
    # 6. 提交
    print("\n[步骤6] 提交代码...")
    commit_msg = "feat: 初始化接口自动化测试框架\n\n- 基于 Python + pytest + requests 三层架构\n- 支持 Admin/EduPC/H5 多端测试\n- 集成 TAPD 回填和企业微信通知\n- 32个核心用例覆盖"
    run_cmd(f'git commit -m "{commit_msg}"')
    
    # 6.5. 重命名分支为 main
    print("\n[步骤6.5] 重命名分支为 main...")
    run_cmd("git branch -M main")
    
    # 7. 推送到 GitHub
    print("\n[步骤7] 推送到 GitHub...")
    print("注意：首次推送需要输入 GitHub 用户名和密码（或 Personal Access Token）")
    ret = run_cmd("git push -u origin main")
    
    if ret != 0:
        print("\n[提示] 如果推送失败，可能需要：")
        print("1. 设置 GitHub Personal Access Token")
        print("2. 或使用 SSH 密钥")
        print("3. 手动执行: git push -u origin main")
    else:
        print("\n[成功] 代码已推送到 GitHub!")
        print(f"仓库地址: {REMOTE_URL.replace('.git', '')}")

if __name__ == "__main__":
    main()
