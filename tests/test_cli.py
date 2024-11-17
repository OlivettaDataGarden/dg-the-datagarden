import click
import pydantic

from the_datagarden.cli import main


def test_main():
    # Call main with standalone_mode=False to prevent sys.exit()
    result = main.main(standalone_mode=False)
    assert result is None  # Or whatever return value you expect


def test_main_with_arg():
    result = main.main(standalone_mode=False, arg1="test")
    assert result is None
    assert pydantic.BaseModel.model_validate_json(result)
    assert click.echo(result) == "test"
