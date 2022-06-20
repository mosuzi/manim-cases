import sys

sys.path.append(".")
from util.get_voice import generate
import os

# 当前路径
currentPath = os.getcwd()
# 当前系统分隔符
delimiter = os.sep

introduce = delimiter + 'util' + delimiter + 'introduce.xml'

absPath = currentPath + introduce



appKey = ''
token = ''
target = 'introduce'

with open(absPath, 'r+', encoding="utf8") as file:
  text = file.read()

generate(appKey, token, text, target)