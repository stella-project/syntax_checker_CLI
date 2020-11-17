import re
import os
import click
import random


def validator(ranking_str, k=None):
    def _construct_error_string(error_log):
        message = []
        error_count = sum([len(error_log[s]) for s in error_log])
        message.append('There are {} errors in your file:\n'.format(str(error_count)))
        for error_type in error_log:
            if len(error_log[error_type]) > 1:
                message.append(
                    error_log[error_type][0] + ' and {} more lines.\n'.format(str(len(error_log[error_type]) - 1)))
            else:
                message.append(error_log[error_type][0] + '\n')
        return message

    error_log = {}
    run_tag = {}
    topics = {}
    samples = []
    if ranking_str:
        lines = ranking_str.split('\n')[:-1]
        if k:
            for _ in range(0, k):
                s = lines[random.randint(0, len(lines) - 1)]
                samples.append(s)
        else:
            samples = lines

        with click.progressbar(samples, show_eta=True) as ranking:
            for line in ranking:
                if '\t' in line:
                    fields = line.split('\t')
                elif ' ' in line:
                    fields = line.split(' ')
                else:
                    error_log.setdefault('wrong delimeter', []).append(
                        'Error line {} - Could not detect delimeter'.format(str(lines.index(line) + 1)))
                    continue

                if len(fields) != 6:
                    error_log.setdefault('missing fields', []).append(
                        'Error line {} - Missing fields'.format(str(lines.index(line) + 1)))
                    continue

                run_tag.setdefault('run_tag', fields[5])
                if not re.search("^[A-Za-z0-9_.-]{1,24}$", fields[5]):
                    error_log.setdefault('malformed run tag', []).append(
                        'Error line {} - Run tag {} is malformed'.format(str(lines.index(line) + 1), str(fields[5])))
                    continue
                else:
                    if not fields[5] == run_tag['run_tag']:
                        error_log.setdefault('inconsistent run tag', []).append(
                            'Error line {} - Run tag is inconsistent ({} and {})'.format(
                                str(lines.index(line) + 1),
                                str(fields[5]), str(run_tag['run_tag'])))
                        continue
                # todo: Topic anzahl abgleichen

                if 'Q0'.casefold() not in fields[1].casefold():
                    error_log.setdefault('Q0', []).append('Error line {} - "Field 2 is {} not "Q0"'.format(
                        str(lines.index(line) + 1), str(fields[1])))
                    continue

                if not fields[3].isdigit():
                    error_log.setdefault('rank', []).append(
                        'Error line {} - "Column 4 (rank) {} must be an integer"'.format(
                            str(lines.index(line) + 1), str(fields[3])))
                    continue

                # if not re.search("^[A-Za-z0-9-]{1,24}$", fields[2]):
                # error = 'Error line {} - "Invalid docid {}"\n'.format(str(lines.index(line) + 1),
                # str(fields[2]))
                # error_log.setdefault('docid', []).append(error)
                # continue
                # if(error_log):
                #     print(error_log)
        if len(error_log) == 0:
            return False
    else:
        return 'Runfile is empty!'
    return _construct_error_string(error_log)


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
    result = validator(ranking, k=500)
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
            # print('Error Line {} - Could not detect delimiter.\n'.format(str(lines.index(line) + 1)))
            pass

        files.setdefault(fields[0], []).append(line)

    if not os.path.exists(os.path.splitext(filename)[0]):
        os.makedirs(os.path.splitext(filename)[0])

    for file in files:
        with open(os.path.join(os.path.splitext(filename)[0], str(file) + '.txt'), 'w') as outfile:
            for line in files[file]:
                r = outfile.write(line + '\n')
