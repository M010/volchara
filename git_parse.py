import git
from files_with_score import *
from datetime import datetime
from pathlib import Path


class RepoParser:
    def __init__(self, repo_path: Path):
        if not repo_path.exists():
            raise Exception(f"Invalid path: {repo_path.absolute()}")
        self.repo_path = repo_path
        self.repo = git.Repo(repo_path)

    def process_file(self, filepath: Path) -> File:
        num = 1
        for [commit, line] in self.repo.blame('HEAD', filepath):
            ts = datetime.fromtimestamp(commit.committed_date).strftime('%Y-%m-%d %H:%M:%S')
            for i in range(num, num + len(line)):
                print(i, " ", commit, " ", commit.author, "", ts)
            num = num + len(line)
        file_score = 0 # TODO
        return File(name=filepath, score=file_score)

    def process_files(self) -> Files:
        filepath = "C:\\Users\\nik-1\\OneDrive\\Рабочий стол\\volk\\protobuf\\generate_changelog.py"
        files_to_process = [filepath]
        files_with_score = Files(files=[])
        for file in files_to_process:
            res = self.process_file(file)
            files_with_score.files.append(res)
        return files_with_score
        