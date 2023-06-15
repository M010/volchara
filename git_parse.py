import git
from files_with_score import *
from datetime import datetime
from pathlib import Path
import os

CPP_EXT = (".h", ".cpp", ".hpp", ".cxx", ".hxx", ".cc", ".c")


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
                #print(i, " ", commit, " ", commit.author, "", ts)
                pass
            num = num + len(line)
        file_score = 0  # TODO
        return File(name=filepath, score=file_score)

    def process_files(self) -> Files:
        files_to_process = []
        for (dir_path, dir_names, file_names) in os.walk(self.repo_path):
            if ".git" in dir_names:
                dir_names.remove(".git")
            for file_name in file_names:
                if not Path(file_name).suffix in CPP_EXT:
                    continue
                full_path = Path(dir_path, file_name)
                files_to_process.append(str(full_path.absolute()))

        files_with_score = Files(files=[])
        for file in files_to_process:
            res = self.process_file(file)
            files_with_score.files.append(res)
        return files_with_score
