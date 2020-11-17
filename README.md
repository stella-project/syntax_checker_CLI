**RunValidator**
---
`RunValidator` is a super simple command line tool mainly for checking a run files proper TREC syntax.

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
`RunValidator` validates a whole runfile or `k` randomly chosen sample lines from a run file for


**Installation:**
---
1. Clone the `RunValidator` reposetory:
`git clone https://github.com/stella-project/syntax_checker_CLI.git`
2. Install `RunValidator`:
`cd syntax_checker_CLI && pip install --editable .`
