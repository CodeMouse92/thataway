#!/usr/bin/env python3

import os

import click

from thataway import targets
from thataway import rules


@click.command()
@click.argument('target', required=False)
@click.option('--add-rule', nargs=3)
@click.pass_context
def cli(ctx, target, add_rule):
    if add_rule:
        target_type, rule, cmd = add_rule
        target_type == target_type.lower()
        rules.add_rule(target_type, rule, cmd)
        return

    if target is None:
        cmd = rules.find_rule(targets.TargetType.URL, '*')
        cmd = cmd.replace('%', '')
        os.system(cmd)
        return

    try:
        target_type, target_part = targets.parse(target)
    except ValueError:
        click.echo(
            "Unknown target. URLs should start with http(s)://, or file://",
            err=True
        )
        return

    cmd = rules.find_rule(target_type, target_part)
    if target == '*':
        cmd = cmd.replace('%', '')
    else:
        cmd = cmd.replace('%', f"'{target}'")
    os.system(cmd)


if __name__ == "__main__":
    cli()
