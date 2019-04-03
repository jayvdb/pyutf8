import doctest
import os.path
import sys
import unittest


class OptionalExtensionTestSuite(unittest.TestSuite):
    def run(self, result):
        import pyutf8
        run = unittest.TestSuite.run
        run(self, result)
        pyutf8._toggle_speedups(False)
        run(self, result)
        pyutf8._toggle_speedups(True)
        return result


def additional_tests(suite=None):
    import pyutf8
    import pyutf8.ref
    if suite is None:
        suite = unittest.TestSuite()
    for mod in (pyutf8, pyutf8.ref):
        suite.addTest(doctest.DocTestSuite(mod))
    if os.path.exists('./README.rst'):
        suite.addTest(doctest.DocFileSuite('README.rst', module_relative=False))
    else:
        print('Can not find README.rst')
    return suite


def all_tests_suite():
    suite = unittest.TestLoader().loadTestsFromNames([
        'pyutf8.tests.test_ref',
        'pyutf8.tests.test_valid_utf8_bytes',
    ])
    suite = additional_tests(suite)
    # Python 3 doesnt like OptionalExtensionTestSuite
    if sys.version_info[0] == 3:
        return suite

    return OptionalExtensionTestSuite([suite])


def main():
    runner = unittest.TextTestRunner()
    suite = all_tests_suite()
    runner.run(suite)

if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    main()
