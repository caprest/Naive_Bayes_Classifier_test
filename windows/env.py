import sys
import io
import os 
os.system("chcp 65001")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')