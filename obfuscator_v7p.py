#!/usr/bin/env python3
"""
Android Shell文本混淆工具 obfuscator_v7p.py
Copyright (c) 2026 KensaijoCiallo
License: MIT
GitHub仓库: https://github.com/KensaijoCiallo/AndroidShellconfusePython
"""
import sys
import os
import random
import string

def info(msg): print(f"\033[32m[√]\033[0m {msg}")
def warn(msg): print(f"\033[33m[!]\033[0m {msg}")
def fail(msg): print(f"\033[31m[×]\033[0m {msg}")

def show_banner():
    print("\033[36m" + "="*60 + "\033[0m")
    print("\033[36mAndroid Shell文本混淆工具 obfuscator_v7p.py\033[0m")
    print("\033[36mCopyright (c) 2026 KensaijoCiallo\033[0m")
    print("\033[36mLicense: MIT\033[0m")
    print("\033[36mGitHub仓库: https://github.com/KensaijoCiallo/AndroidShellconfusePython\033[0m")
    print("\033[36m" + "="*60 + "\033[0m")
    print()

def gen_varname():
    return '__' + ''.join(random.choices(string.ascii_letters + string.digits, k=6))

if len(sys.argv) != 2:
    show_banner()
    print("用法: python obfuscator_v7p.py 原脚本.sh")
    print("示例: python obfuscator_v7p.py test.sh")
    print("输出: test.obf.sh")
    print()
    print("注意：请确保原文件以.sh结尾，否则可能导致输出文件覆盖原文件！")
    sys.exit(1)

# 显示作者信息
show_banner()

src = sys.argv[1]
if not os.path.isfile(src):
    fail(f"文件不存在: {src}")
    sys.exit(1)

# 检查文件后缀名
if not src.endswith('.sh'):
    warn(f"警告：输入文件 '{src}' 不是以.sh结尾")
    warn("这可能导致输出文件覆盖原文件或产生意外行为")
    choice = input("是否继续处理？(y/N): ")
    if choice.lower() != 'y':
        info("已取消操作")
        sys.exit(0)
    warn("请确保你了解风险")

# 获取输出文件名 - 固定使用.obf.sh后缀
out_path = src + '.obf.sh' if not src.endswith('.sh') else src.replace('.sh', '.obf.sh')

# 检查输出文件是否已存在
if os.path.exists(out_path):
    warn(f"输出文件已存在: {out_path}")
    choice = input("是否覆盖？(y/N): ")
    if choice.lower() != 'y':
        # 生成带时间戳的新文件名
        import time
        timestamp = int(time.time())
        base_name = os.path.splitext(src)[0]
        out_path = f"{base_name}.obf.{timestamp}.sh"
        info(f"使用新文件名: {out_path}")

with open(src, 'r', encoding='utf-8') as f:
    original = f.read()

original = original.replace('\r', '')  # 统一行尾
lines = original.split('\n')

# 创建变量池
unique_chars = sorted(set(original))
varmap = {}
definitions = []

info(f"构建变量池: 共 {len(unique_chars)} 个字符")
for i, ch in enumerate(unique_chars):
    varname = gen_varname()
    while varname in varmap.values():  # 保证不重复
        varname = gen_varname()
    hexval = ch.encode('utf-8').hex()
    encoded = ''.join([f"\\x{hexval[j:j+2]}" for j in range(0, len(hexval), 2)])
    varmap[ch] = varname
    definitions.append(f"{varname}=$(printf '{encoded}')")
    if (i + 1) % 10 == 0 or i == len(unique_chars) - 1:
        print(f"  进度: {i+1}/{len(unique_chars)}", end='\r')
print()

# 构造输出
obf_lines = []
obf_lines.append("#!/system/bin/sh")
obf_lines.extend(definitions)
obf_lines.append('cmd=""')

info(f"拼接代码行: 共 {len(lines)} 行")
for i, line in enumerate(lines):
    encoded_line = ''.join([f"${{{varmap[ch]}}}" for ch in line])
    obf_lines.append(f'cmd="$cmd{encoded_line}"')
    obf_lines.append('cmd="$cmd\n"')  # 真正的换行
    if (i + 1) % 10 == 0 or i == len(lines) - 1:
        print(f"  进度: {i+1}/{len(lines)}", end='\r')
print()

obf_lines.append('eval "$cmd"')

# 写入输出文件
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(obf_lines))

info(f"写入输出文件: {out_path}")
info("混淆完成！可执行测试:")
print(f"\n  sh '{out_path}'\n")

# 显示成功信息和仓库地址
print("\033[36m" + "="*60 + "\033[0m")
print("\033[36m🎉 混淆成功！\033[0m")
print("\033[36m📂 输出文件: \033[0m" + out_path)
print("\033[36m📁 原文件: \033[0m" + src + " (未修改)")
print("\033[36m🔗 项目地址: \033[0mhttps://github.com/KensaijoCiallo/AndroidShellconfusePython")
print("\033[36m" + "="*60 + "\033[0m")