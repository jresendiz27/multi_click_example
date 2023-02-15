import json
import logging
import os.path
import sys

import pkg_resources

import click

HOME_LOCATION = os.path.expanduser('~')
CONFIG_FILE_LOCATION = os.path.join(HOME_LOCATION, ".cli-config.json")

logger = logging.getLogger()


def ensure_config_file(func):
    def inner1(*args, **kwargs):
        logging.debug("Before Execution")
        if not os.path.isfile(CONFIG_FILE_LOCATION):
            with open(CONFIG_FILE_LOCATION, 'x') as fp:
                content = {}
                json_string = json.dumps(content)
                fp.write(json_string)
        returned_value = func(*args, **kwargs)
        logging.debug("After Execution")

        return returned_value

    return inner1


@click.group(name='command-config', invoke_without_command=True, no_args_is_help=True)
@click.option('--debug/--no-debug', required=False, default=False, help='Enables verbose mode')
@click.option('--version', '-v', is_flag=True, help='Shows the version and exits the program')
@ensure_config_file
def command_config(debug, version):
    """Simple configuration management.

    This is a very long second paragraph and as you
    can see wrapped very early in the source text
    but will be rewrapped to the terminal width in
    the final output.

    \b
    This is
    a paragraph
    without rewrapping.

    And this is a paragraph
    that will be rewrapped again.
    """
    if version:
        click.secho(pkg_resources.get_distribution('multi-click-example').version)
        sys.exit(0)
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)


@click.command(name='add', help='Add an item to the config')
@click.option('-k', '--key', type=str, required=True, help='Key to be added to the config')
@click.option('-v', '--value', type=str, required=True,
              help='Value to be added to the config, must be valid Json values')
@ensure_config_file
def add(key, value):
    logger.debug('Opening file: %s' % CONFIG_FILE_LOCATION)
    with open(CONFIG_FILE_LOCATION, 'r') as file:
        json_content = json.load(file)
    with open(CONFIG_FILE_LOCATION, 'w') as file:
        json_content[key] = value
        json.dump(json_content, file)
        logger.debug('File Updated!')
    logger.info("Value successfully added! key: %s, val: %s" % (key, value))


@click.command(name='delete', help='Removes a key from the config')
@click.option('-k', '--key', type=str, required=True, help='Key to be searched and deleted if found')
@ensure_config_file
def delete(key):
    with open(CONFIG_FILE_LOCATION, 'r') as file:
        content = json.load(file)
    with open(CONFIG_FILE_LOCATION, 'w') as file:
        if content[key]:
            del content[key]
            logger.info('Item deleted: %s' % key)
        else:
            logger.info('Item Not found!')
        json.dump(content, file)


@click.command(name='list', help='List all the saved config, can be also shown as json')
@click.option('-j', '--as-json', is_flag=True, default=False, required=False)
@ensure_config_file
def list_config(as_json):
    with open(CONFIG_FILE_LOCATION, 'r') as file:
        content = json.load(file)
        if as_json:
            print(content)
        else:
            for k, v in content.items():
                print(f"{k} -> {v}")


def run_cli():
    command_config.add_command(add)
    command_config.add_command(delete)
    command_config.add_command(list_config)
    command_config()


if __name__ == '__main__':
    run_cli()
