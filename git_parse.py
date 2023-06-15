import git
import time

from git import Repo
from datetime import datetime

repo = Repo("C:\\Users\\nik-1\\OneDrive\\Рабочий стол\\volk\\protobuf")

filepath = "C:\\Users\\nik-1\\OneDrive\\Рабочий стол\\volk\\protobuf\\generate_changelog.py"

num = 1
for [commit, line] in repo.blame('HEAD', filepath):
    ts = datetime.fromtimestamp(commit.committed_date).strftime('%Y-%m-%d %H:%M:%S')
    for i in range(num, num + len(line)):
        print(i, " ", commit, " ", commit.author, "", ts)
    num = num + len(line)