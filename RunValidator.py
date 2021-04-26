import re
import os
import click
import random


def validator(run_str, **kwargs):
    """Validates a run file string.
    
    Args:
        run_str (str): Ranking string of a run file.
        k (int): Number random sample lines to validate in-depth.

    Returns:
        list: List of error messages
        str: Error message string if the run is empty
    """
    def _construct_error_string(error_log):
        """Construct a reasonable in-depth error message from all errors.

        Args:
            error_log (dict): Dictionary with errors and occurrence counts.

        Returns:
            list: list of error strings
        """
        message = []
        error_count = sum([len(error_log[s]) for s in error_log])  # sum all errors for all types
        message.append('There are {} errors in your file:\n'.format(str(error_count)))
        for error_type in error_log:
            if len(error_log[error_type]) > 1:
                message.append(
                    error_log[error_type][0] + ' and {} more lines.\n'.format(str(len(error_log[error_type]) - 1)))
            else:
                message.append(error_log[error_type][0] + '\n')
        return message

    k = int(kwargs.get('k', 0))
    error_log = {}
    run_tag = {}
    topics = {}
    samples = []
    if run_str:
        lines = run_str.split('\n')[:-1]
        if k > 0:
            for _ in range(0, k):
                s = lines[random.randint(0, len(lines) - 1)]  # Pick k random lines to validate.
                samples.append(s)
        else:
            samples = lines

        with click.progressbar(samples, show_eta=True) as ranking:
            for line in ranking:
                # Check for and split at delimiter.
                if '\t' in line:
                    fields = line.split('\t')
                elif ' ' in line:
                    fields = line.split(' ')
                else:
                    error_log.setdefault('wrong delimiter', []).append(
                        'Error line {} - Could not detect delimiter'.format(str(lines.index(line) + 1)))
                    continue

                # Check if all 6 required fields exist.
                if len(fields) < 6:
                    error_log.setdefault('missing fields', []).append(
                        'Error line {} - Missing fields'.format(str(lines.index(line) + 1)))
                    continue

                if len(fields) > 6:
                    error_log.setdefault('too many fields', []).append(
                        'Error line {} - Too Many fields'.format(str(lines.index(line) + 1)))
                    continue

                # Check if run tag is valid and consistent.
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

                # Check for Q0 field.
                if fields[1].casefold() not in ["Q0", "0"]:
                    error_log.setdefault('Q0', []).append('Error line {} - Field 2 is "{}" not "Q0"'.format(
                        str(lines.index(line) + 1), str(fields[1])))
                    continue

                # check if score is a digit.
                if not fields[3].isdigit():
                    error_log.setdefault('rank', []).append(
                        'Error line {} - "Column 4 (rank) {} must be a digit"'.format(
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
            return error_log
    else:
        return 'Run file is empty!'
    return _construct_error_string(error_log)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('filename', type=click.File('r'), nargs=-1)
@click.option('--k', help='limit validation to k randomly chosen lines')
def validate(filename, k):
    """Check the syntax of a run file."""
    ranking = str()

    if filename:
        for f in filename:
            while True:
                chunk = f.read(1024)
                if not chunk:
                    break
                ranking += chunk
        click.echo('Validation started:')
        result = validator(ranking, k=k)
        click.echo('Validation finished!')
        if result:
            click.echo(''.join(result))
        else:
            click.echo('Validation succeeded!')
    else:
        click.echo('No file for validation specified.')


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
def split(filename):
    """Split a run file by topic name into separate files.

    Args:
        filename: Run file or path to run file.

    """
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
            click.echo(r'RunValidator just supports `\n` and \s as delimiter.')

        files.setdefault(fields[0], []).append(line)

    if not os.path.exists(os.path.splitext(filename)[0]):
        os.makedirs(os.path.splitext(filename)[0])

    for file in files:
        with open(os.path.join(os.path.splitext(filename)[0], str(file) + '.txt'), 'w') as outfile:
            for line in files[file]:
                r = outfile.write(line + '\n')
