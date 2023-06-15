import json
from typing import List
from git_parse import *
from files_with_score import *
from argparse import ArgumentParser
from parse_coverage import *

max_score = 100

def get_coverage_data() -> Files:    
    parser = CoverageParser("coverage.json", "coverage_sum.json")
    return Files.from_json(parser.process_files())

    return {
        'files': [
            {
                "name":"main.cpp", 
                "score": 100
            },
            {
                "name":"main2.cpp", 
                "score": 50
            }
        ]
    }

def get_git_data(repo_path: Path) -> Files:
    parser = RepoParser(repo_path)
    return parser.process_files()
    
def merge(git_files: Files, coverage_files: Files) -> Files:
    output = []
    for git_file in git_files.files:
        try:
            coverage_file = coverage_files.get_file_with_name(git_file.name)
        except Exception as e:
            print(f"Warn: file found in git but coverage missing. {e}")
            # If coverage not found assume no coverage at all
            # so, file should be surely checked
            coverage_file = File(name=git_file.name, score=max_score)
        output.append(File(name=git_file.name, score=git_file.score + coverage_file.score))
    return Files(files=output)

class Options:
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path

    @staticmethod
    def ParseFromArgv():
        parser = ArgumentParser()
        parser.add_argument("-p", "--path", help="Repo to analyse", required=True)
        args = parser.parse_args()
        return Options(args.path)

def main():
    options = Options.ParseFromArgv()
    
    coverage = get_coverage_data()
    print(coverage.toJson())
    git = get_git_data(Path(options.repo_path))
    
    total = merge(git, coverage)
    total.sort_by_score()
    print(total.toJson())
    

if __name__ == "__main__":
    main()