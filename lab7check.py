# 用法：
# 将lab7test放在和lab7check.py，同一目录下，运行lab7check.py即可
# 同时将自己的实验文件夹放到同一目录创建lab7/PBxxx_xxx 下
import os
import subprocess
import sys
import shutil
import filecmp

# 获取lab7文件夹下的所有文件夹名
for file in os.listdir('lab7'):
    # 进入学生文件夹
    if os.path.isdir('lab7/' + file):
        # 查找.cpp和.c文件
        for cpp_file in os.listdir('lab7/' + file):
            if cpp_file.endswith('.cpp'):
                subprocess.run(['g++', 'lab7/' + file + '/' + cpp_file, '-o', 'assembler', '-std=c++2a'])
            elif cpp_file.endswith('.c'):
                subprocess.run(['gcc', 'lab7/' + file + '/' + cpp_file, '-o', 'assembler'])
        # 新建result文件
        result = open('lab7/' + file + '/result.txt', 'w')
        # 检查是否编译成功
        if not os.path.exists('assembler.exe'):
            result.write('编译失败')
            continue
        if not os.path.exists('lab7/' + file + '/test_result'):
            os.mkdir('lab7/' + file + '/test_result')
        # 测试lab7test文件夹下的每个x.asm并且与x.out进行对比
        for test_file in os.listdir('lab7test'):
            if test_file.endswith('.asm'):
                # 运行assembler.exe
                subprocess.run(['lab7/' + file + '/assembler.exe', 'lab7test/' + test_file, 'lab7/' + file + '/test_result/' + test_file[:-4] + '.out'])
                # 对比结果
                if os.path.exists('lab7/' + file + '/test_result/' + test_file[:-4] + '.out'):
                    # 利用fc命令对比输出结果
                    os.chdir('lab7/' + file + '/test_result')
                    subprocess.run(['fc', test_file[:-4] + '.out', '../../../lab7test/' + test_file[:-4] + '.out'], stdout=result)
                    os.chdir('../../../')
                else:
                        result.write(test_file[:-4] + '未能生成输出文件\n')
        result.close()
