import re
import os
import click


def validator(TRECstr):
    def errorMessage(errorLog):
        message = []
        errorcount = sum([len(errorLog[s]) for s in errorLog])
        message.append('There are {} errors in your file:\n'.format(str(errorcount)))
        for errorType in errorLog:
            if len(errorLog[errorType]) > 1:
                message.append(
                    errorLog[errorType][0] + ' and {} more lines.'.format(str(len(errorLog[errorType]) - 1)))
            else:
                message.append(errorLog[errorType][0])
        return message

    errorLog = {}
    if TRECstr:
        lines = TRECstr.split('\n')[:-1]
        topics = {}

        with click.progressbar(lines, show_eta=True) as ranking:
            for line in ranking:
                if '\t' in line:
                    fields = line.split('\t')
                elif ' ' in line:
                    fields = line.split(' ')
                else:
                    error = 'Error line {} - Could not detect delimeter\n'.format(str(lines.index(line) + 1))
                    errorLog.setdefault('wrong delimeter', []).append(error)
                    continue

                if lines.index(line) == 0:
                    runTag = fields[5]

                if len(fields) != 6:
                    error = 'Error line {} - Missing fields\n'.format(str(lines.index(line) + 1))
                    errorLog.setdefault('missing fields', []).append(error)
                    continue

                if not re.search("^[A-Za-z0-9_.-]{1,24}$", fields[5]):
                    error = 'Error line {} - Run tag {} is malformed\n'.format(str(lines.index(line) + 1),
                                                                               str(fields[5]))
                    continue
                else:
                    if not fields[5] == runTag:
                        error = 'Error line {} - Run tag is inconsistent ({} and {})\n'.format(
                            str(lines.index(line) + 1),
                            str(fields[5]), str(runTag))
                        errorLog.setdefault('inconsistent run tag', []).append(error)
                        continue
                # if not fields[0].isdigit():
                #     error = 'Error line {} - Unknown topic {}\n'.format(str(lines.index(line) + 1), str(fields[0]))
                #     errorLog.setdefault('unknown topic', []).append(error)
                #     continue
                # else:
                #     if fields[0] not in topics:
                #         topics[fields[0]] = 1
                #     else:
                #         topics[fields[0]] += 1
                #     # todo: Topic anzahl abgleichen

                if 'Q0'.casefold() not in fields[1].casefold():
                    error = 'Error line {} - "Field 2 is {} not "Q0"\n'.format(str(lines.index(line) + 1),
                                                                               str(fields[1]))
                    errorLog.setdefault('Q0', []).append(error)
                    continue

                if not fields[3].isdigit():
                    error = 'Error line {} - "Column 4 (rank) {} must be an integer"\n'.format(
                        str(lines.index(line) + 1), str(fields[3]))
                    errorLog.setdefault('rank', []).append(error)
                    continue

                # if not re.search("^[A-Za-z0-9-]{1,24}$", fields[2]):
                # error = 'Error line {} - "Invalid docid {}"\n'.format(str(lines.index(line) + 1),
                # str(fields[2]))
                # errorLog.setdefault('docid', []).append(error)
                # continue
                if(errorLog):
                    print(errorLog)
            if len(errorLog) == 0:
                return False
    else:
        return 'TREC file is empty!'
    return errorMessage(errorLog)


@click.group()
def cli():
    pass

@cli.command()
@click.argument('input', type=click.File('r'), nargs=-1)
def validate(input):
    """Check the syntax of a ranking file."""
    ranking = str()
    for f in input:
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            ranking += chunk
    click.echo('Validation started:')
    result = validator(ranking)
    click.echo('Validation finished!')
    if result:
        click.echo(''.join(result))
    else:
        click.echo('Validation succeeded!')


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
def split(filename):
    """Split a run file by topic name into separate files."""
    with open(filename, 'r') as infile:
        ranking = infile.read()

    files = {}
    lines = ranking.split('\n')[:-1]
    for line in lines:
        if '\t' in line:
            fields = line.split('\t')
        elif ' ' in line:
            fields = line.split(' ')
        else:
            print('Error Line {} - Could not detect delimiter.\n'.format(str(lines.index(line) + 1)))

        files.setdefault(fields[0], []).append(line)

    if not os.path.exists(os.path.splitext(filename)[0]):
        os.makedirs(os.path.splitext(filename)[0])

    for file in files:
        with open(os.path.join(os.path.splitext(filename)[0], str(file)+'.txt'), 'w') as outfile:
            for line in files[file]:
                r = outfile.write(line + '\n')
