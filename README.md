**RunValidator**
---
`RunValidator` is a super simple command line tool mainly for checking a retrieval runs proper TREC syntax.

**Usage**
---

```commandline
Usage: RunValidator [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  split     Split a run file by topic name into separate files.
  validate  Check the syntax of a ranking file.
```

**Validation**
---
`RunValidator` validates a whole retrieval run or `k` randomly chosen sample lines from a run. At the moment this tool checks:
1. the delimeter
2. if a line consists of 6 fields
3. for a proper run tag
4. if a runtag is consistent throughout the run
5. the `Q0` field
6. for a correct ranking

**Installation:**
---
1. Clone the `RunValidator` reposetory:
```
git clone https://github.com/stella-project/syntax_checker_CLI.git
```

2. Install `RunValidator`:
```
cd syntax_checker_CLI && pip install --editable .
```
