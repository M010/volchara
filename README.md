# volchara

## use example

### cd example
### g++ -fprofile-arcs -ftest-coverage -fPIC -O0 main.cpp foo.cpp -o program
### ./program
### gcovr --json coverage.json
### gcovr --json-summary coverage_sum.json
### python3 parse_coverage.py

