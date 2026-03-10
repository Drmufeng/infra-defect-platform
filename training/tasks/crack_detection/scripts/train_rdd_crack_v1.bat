@echo off
REM 激活用于训练的 Python 虚拟环境。
call B:\dome\.venv311\Scripts\activate
REM 为避免 Python 与 bat 两套训练参数分离，bat 入口统一转调 Python 主脚本。
REM 这样后续只需要维护 training/tasks/crack_detection/scripts/train_rdd_crack_v1.py 一份训练配置。
python B:\dome\training\tasks\crack_detection\scripts\train_rdd_crack_v1.py
