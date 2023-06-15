import json
from typing import List
from git_parse import *
from files_with_score import *
from argparse import ArgumentParser
from parse_coverage import *

max_score = 100

def get_coverage_data(root_dir: str, coverage_targets: str, coverage_summary: str) -> Files:
    parser = CoverageParser(root_dir=root_dir, coverage_targets=coverage_targets, coverage_summary=coverage_summary)
    return Files.from_json(parser.process_files())

def get_git_data(repo_path: Path) -> Files:
    parser = RepoParser(repo_path)
    return parser.process_files()
    
def merge(git_files: Files, coverage_files: Files) -> Files:
    output = []
    for git_file in git_files.files:
        try:
            coverage_file = coverage_files.get_file_with_name(git_file.name)
        except Exception as e:
            if Path(git_file.name).suffix in ('.hpp', ".h"):
                print(f"Header file missing in coverage, skip it - assume no func implementations in header file found ({e})")
                continue
            
            print(f"Warn: file found in git but coverage missing. {e}")
            # If coverage not found assume no coverage at all
            # so, file should be surely checked
            coverage_file = File(name=git_file.name, score=max_score)
        output.append(File(name=git_file.name, score=git_file.score + coverage_file.score))
    return Files(files=output)

class Options:
    def __init__(self, repo_path: Path, root_dir: str, coverage_targets: str, coverage_summary: str):
        self.repo_path = repo_path
        self.root_dir = root_dir
        self.coverage_targets = coverage_targets
        self.coverage_summary = coverage_summary
        

    @staticmethod
    def ParseFromArgv():
        parser = ArgumentParser()
        parser.add_argument("-p", "--path", help="Repo to analyse", default=".")
        parser.add_argument("-r", "--source_root", help="Root of target project (it must contains .git folder!)", default="./example")
        parser.add_argument("-t", "--coverage_targets", help="Path to file with coverage info per files", default="./example/coverage.json")
        parser.add_argument("-f", "--coverage_summary", help="Path to file with coverage summary", default="./example/coverage_sum.json")
        args = parser.parse_args()
        return Options(
            repo_path=args.path, 
            root_dir=args.source_root,
            coverage_targets=args.coverage_targets, 
            coverage_summary=args.coverage_summary
        )

def main():
    options = Options.ParseFromArgv()
    
    coverage = get_coverage_data(root_dir=options.root_dir, 
                                 coverage_targets=options.coverage_targets, 
                                 coverage_summary=options.coverage_summary)
    print(coverage.toJson())
    git = get_git_data(Path(options.repo_path))
    
    total = merge(git, coverage)
    total.sort_by_score()
    print(total.toJson())
    

if __name__ == "__main__":
    main()