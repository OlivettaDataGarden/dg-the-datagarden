from the_datagarden.cli import main

def test_main():
    # Call main with standalone_mode=False to prevent sys.exit()
    result = main.main(standalone_mode=False)
    assert result is None # Or whatever return value you expect
