import os
import sys
import mocker

from jasmine_runner.commands import run_specs
from StringIO import StringIO

TESTS_ROOT = os.path.abspath(os.path.dirname(__file__))
FIXTURES_ROOT = os.path.join(TESTS_ROOT, 'fixtures')

path_to_file = lambda filename: 'file://%s' % (os.path.join(FIXTURES_ROOT, filename))

class TestJasmineRunner(mocker.MockerTestCase):

    def setUp(self):
        self._buf = StringIO()
        self._stdout = sys.stdout
        sys.stdout = self._buf

    def tearDown(self):
        sys.stdout = self._stdout
        self.mocker.reset()

    def assert_printed(self, value):
        self._buf.seek(0)
        assert value in self._buf.read()

    def _mock_colored_output(self, color):
        colored = self.mocker.replace('termcolor.colored')
        colored(mocker.ANY, color)
        self.mocker.result('bla')
        self.mocker.replay()

    def test_should_print_the_resume_of_the_spec_running_for_passed_specs(self):
        "should print the resume of the spec running for passed specs"
        run_specs(path_to_file('passed-specs.html'))
        self.assert_printed('4 specs, 0 failures in 0.031s')

    def test_should_print_the_resume_of_the_spec_running_for_failed_specs(self):
        "should print the resume of the spec running for failed specs"
        run_specs(path_to_file('failed-specs.html'))
        self.assert_printed('4 specs, 1 failure in 0.028s')

    def test_green_resume(self):
        "should print a green resume for passed specs"
        self._mock_colored_output('green')

        run_specs(path_to_file('passed-specs.html'))
        self.assert_printed('bla')

        self.mocker.verify()

    def test_red_resume(self):
        "should print a red resume for failed specs"
        self._mock_colored_output('red')

        run_specs(path_to_file('failed-specs.html'))
        self.assert_printed('bla')

        self.mocker.verify()

    def test_splinter_driver(self):
        "should be able to customize the splinter driver to use"
        from splinter.browser import Browser
        chrome_mock = Browser('webdriver.firefox')
        firefox_mock = Browser('webdriver.firefox')

        Browser = self.mocker.replace('splinter.browser.Browser')
        Browser('webdriver.chrome')
        self.mocker.result(chrome_mock)

        Browser('webdriver.firefox')
        self.mocker.result(firefox_mock)
        self.mocker.replay()

        run_specs(path_to_file('failed-specs.html'), browser_driver='webdriver.chrome')
        run_specs(path_to_file('passed-specs.html'), browser_driver='webdriver.firefox')

        self.mocker.verify()

    def test_firefox_default_driver(self):
        "when no driver is specified, Firefox should be used"
        from splinter.browser import Browser
        browser = Browser('webdriver.firefox')

        Browser = self.mocker.replace('splinter.browser.Browser')
        Browser('webdriver.firefox')
        self.mocker.result(browser)
        self.mocker.replay()

        run_specs(path_to_file('passed-specs.html'))

        self.mocker.verify()

    def test_exit_status(self):
        "should return the proper exit status (very useful for continuous integration jobs)"
        assert 0 == run_specs(path_to_file('passed-specs.html'))
        assert 1 == run_specs(path_to_file('failed-specs.html'))