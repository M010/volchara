#!/bin/env python3
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
                print(
                    f"Trace: Header file missing in coverage, skip it - assume no func implementations in header file found ({e})")
                continue

            print(f"Warn: file found in git but coverage missing. {e}")
            # If coverage not found assume no coverage at all
            # so, file should be surely checked
            coverage_file = File(name=git_file.name, score=max_score)


        git_rate = (1 - git_file.score) * 100
        assert (git_rate >= 0 and git_rate < 101)
        output.append(File(name=git_file.name, score=coverage_file.score + git_rate))
    return Files(files=output)


class Options:
    def __init__(self, repo_path: Path, root_dir: str, coverage_targets: str, coverage_summary: str, output_folder: str):
        self.repo_path = repo_path
        self.root_dir = root_dir
        self.coverage_targets = coverage_targets
        self.coverage_summary = coverage_summary
        self.output_folder = output_folder

    @staticmethod
    def ParseFromArgv():
        parser = ArgumentParser()
        parser.add_argument("-p", "--path", help="Repo to analyse(it must contains .git folder!)", default=".")
        parser.add_argument("-r", "--source_root", help="Root source folder(it used as root in coverage json files)",
                            default="./example")
        parser.add_argument("-t", "--coverage_targets", help="Path to file with coverage info per files",
                            default="./example/coverage.json")
        parser.add_argument("-f", "--coverage_summary", help="Path to file with coverage summary",
                            default="./example/coverage_sum.json")
        parser.add_argument("-o", "--output_folder", help="Folder to save output artifacts to", default="./output")
        args = parser.parse_args()
        return Options(
            repo_path=args.path,
            root_dir=args.source_root,
            coverage_targets=args.coverage_targets,
            coverage_summary=args.coverage_summary,
            output_folder=args.output_folder,
        )


def main():
    options = Options.ParseFromArgv()
    
    # creating output dir if not exists
    Path(options.output_folder).mkdir(parents=True, exist_ok=True)

    coverage_score_by_files = get_coverage_data(root_dir=options.root_dir,
                                 coverage_targets=options.coverage_targets,
                                 coverage_summary=options.coverage_summary)
    coverage_score_by_files.sort_by_score()
    coverage_score_by_files.save_to_file(Path(options.output_folder, "coverage_score_by_files.json")),
    
    git_score_by_files = get_git_data(Path(options.repo_path))
    git_score_by_files.sort_by_score()
    git_score_by_files.save_to_file(Path(options.output_folder, "git_score_by_files.json")),
    
    total_score_by_files = merge(git_score_by_files, coverage_score_by_files)
    total_score_by_files.sort_by_score()
    total_score_by_files.save_to_file(Path(options.output_folder, "total_score_by_files.json")),
    
    print()
    print("==========================")
    print("============DONE==========")
    print("===TOTAL=SCORE=BY=FILES:==")
    print(total_score_by_files.toJson())
    print("==========================")


if __name__ == "__main__":
    main()
