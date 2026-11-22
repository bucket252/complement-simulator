# complement-simulator
>本组无敌，一定能拿高分！
> 期末必过，代码一次跑通！
计算机导论大作业：8/16位补码加减法分步可视化演示程序。
# 补码加减法运算模拟器 (Twos Complement Simulator)

## 📖 项目简介
本项目是计算机导论课程的综合实验，旨在通过可视化界面的方式，分步演示 8 位/16 位整数的原码、反码、补码转换，以及补码加减法运算过程、进位产生与溢出判断。

## 🚀 安装与运行步骤
1. 确保您的电脑已安装 Python 3.8 或更高版本。
2. 将仓库代码下载到本地。
3. 在终端运行：`python src/main.py`

## 📸 运行截图
<img width="1556" height="1246" alt="ddbde26ee2a6245707945fa76fad6ddb" src="https://github.com/user-attachments/assets/91d96821-b1e3-49f8-a323-709f99717894" />
<img width="1566" height="1240" alt="9f82325a252f5e165af3b7e8b9bf30c7" src="https://github.com/user-attachments/assets/79c51d12-80fb-4669-91d7-4aaad593c9e3" />
图为程序运行界面。系统不仅能准确计算原反补码，还能精准判断溢出（如 120+10）并给出理论正确值，同时具备强大的异常输入拦截功能（如输入字母自动弹窗提示）
<img width="1342" height="1024" alt="a6c79ad075646ad8f95e5eb63d2a917e" src="https://github.com/user-attachments/assets/87c7c9a0-840a-404f-88c2-7824dc2925c6" />



## 👥 团队分工
| 姓名 | GitHub 用户名 | 负责模块 |
| :--- | :--- | :--- |
| 张伊涵| bucket252 | 组长、总装集成、PR审查、冲突解决 |
| 孙亚楠 |syn-333| 核心算法A：原反补码转换（convert.py） |
| 林飞飞 | linfeifei11 | 核心算法B：加减法与溢出（calc.py） |
| 姚欣婷 |yaoxinting |UI 界面开发与逻辑拼装（ui.py）   |
| 王晨曦| wangchenxi97707354 |文档主编、AI日志收集（md文档） |
| 苗瑄 | miao1291|测试质检、手算标准用例找Bug |

## 📄 开源协议
本项目采用 [MIT License](LICENSE) 协议。
