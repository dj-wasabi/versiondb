"""Run tests."""
import os
import sys
# class for handling a set of commands
from flask_script import Manager
from app import create_app


app = create_app(config_name=os.getenv('FLASK_ENV'))
manager = Manager(app)


@manager.command
def test():
    """Run the tests."""
    try:
        import pytest
    except Exception as error:
        print(error)
        sys.exit(1)

    test_args = ['--strict', '--verbose', '--cov-report', 'term-missing',
                 '--cov=app.modules', '--tb=long', '--junitxml=/tmp/results.xml',
                 'modules/artifactV1/tests/', 'tests/']
    pytest.main(test_args)


if __name__ == '__main__':
    manager.run()
