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
        self._get_date_ranges()

    def _get_date_ranges(self):
        head_commit = next(self.repo.iter_commits())
        initial_commit: git.Commit
        *_, initial_commit = self.repo.iter_commits()
        self.time_bound = [initial_commit.committed_date, head_commit.committed_date]

    def _normalize_date_of_commit(self, commit: git.Commit):
        normalized_bound = self.time_bound[1] - self.time_bound[0]
        assert (normalized_bound > 1)
        normalized_value = (commit.committed_date - self.time_bound[0])
        percent = normalized_value / normalized_bound
        return percent

    def _get_file_score(self, filepath: Path) -> File:
        file_score = 0
        num = 1
        for [commit, lines] in self.repo.blame('HEAD', filepath):
            file_score += self._normalize_date_of_commit(commit) * len(lines)
            num = num + len(lines)

        file_score /= num
        return File(name=filepath, score=file_score)

    def process_target(self, filepath: Path, start: int, end: int ):
        assert (start < end)
        len_of_target_block = end - start
        target_score = 0
        num = 1
        for [commit, lines] in self.repo.blame('HEAD', filepath):
            delta = self._normalize_date_of_commit(commit)
            for line_number in range(num, num + len(lines)):
                if line_number == end:
                    return target_score / len_of_target_block
                if line_number >= start:
                    target_score += delta
            num = num + len(lines)

        return target_score / len_of_target_block

    def process_files(self) -> Files:
        files_to_process = []
        for (dir_path, dir_names, file_names) in os.walk(self.repo_path):
            if len(dir_names) != 0:
                ignored_dirs = self.repo.ignored(dir_names)
                dir_names[:] = [name for name in dir_names if name not in ignored_dirs]

            if ".git" in dir_names:
                dir_names.remove(".git")
            for file_name in file_names:
                if not Path(file_name).suffix in CPP_EXT:
                    continue
                full_path = Path(dir_path, file_name)
                files_to_process.append(str(full_path.absolute()))

        files_with_score = Files(files=[])
        for file in files_to_process:
            res = self._get_file_score(file)
            files_with_score.files.append(res)
        return files_with_score


if __name__ == '__main__':
    print(os.getcwd())
    parser = RepoParser(Path("."))
    files = parser.process_files()
