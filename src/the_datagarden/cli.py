import click


@click.command()
@click.argument("arg1", required=False)
def main(arg1):
    """Command-line tool for my_package_name."""
    print(f"Received arguments: arg1={arg1}")
    print("Running your command...")
