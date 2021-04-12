<a href="https://stella-project.org/"><img align="right" width="100" src="doc/img/logo-st.JPG" /></a>
**RunValidator**
---
`RunValidator` is a super simple command line tool mainly for checking a retrieval runs proper TREC syntax.<br><br>
A **run-file** is a tabular representation of retrieval results. It shouldn't contain the table headings must be seperated by <kbd>Tab</kbd> and <kbd>Space</kbd>. Each line consists of these fields:<br>

|**Field:**|`query-ID`|`iterator`|`document-id`|`rank`|`score`|`run-ID`|
|---|---|---|---|---|---|---|
|**Description:**|ID or number of the query |Reserved field, should be `Q0`or `0`|Id of the ranked document|Rank of the Document|Score of the document considering the query|ID for this run|

**Usage**
---

```commandline
Usage: RunValidator [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  split     Split a run-file by topic name into separate files.
  validate  Check the syntax of a ranking file.
```

**Validation**
---
`RunValidator` validates a whole retrieval run or `k` randomly chosen sample lines from a run. At the moment this tool checks:
1. The delimiter (<kbd>Tab</kbd> and <kbd>Space</kbd> are valid.),
2. if a line consists of 6 fields,
3. for a proper run tag,
4. if a run tag is consistent throughout the run,
5. if the `Q0` field exists,
6. for a correct ranking order.

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
