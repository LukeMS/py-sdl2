"""Utility functions for the tests.

This file is placed under the public domain.
"""

import imp
import inspect
import optparse
import os
import random
import subprocess
import sys
import time
import traceback
import unittest
from unittest import TestResult, TestLoader


PY3K = sys.version_info[0] == 3

if sys.version_info[0] >= 3:
    MAXINT = sys.maxsize
else:
    MAXINT = sys.maxint


LINEDELIM = "-" * 70
HEAVYDELIM = "=" * 70

# Excludes
EXCLUDETAGS = ["interactive"]

try:
    getinput = raw_input
except NameError:
    getinput = input


def console_on():
    if sys.platform.startswith("win"):
        os.system("echo on")
    elif sys.platform.startswith("lin"):
        os.system("stty echo")
    else:
        print("Sorry, we don't currently have support for the %s OS" %
              sys.platform)

def console_off():
    if sys.platform.startswith("win"):
        os.system("echo off")
    elif sys.platform.startswith("lin"):
        os.system("stty -echo")
    else:
        print("Sorry, we don't currently have support for the %s OS" %
              sys.platform)

def printerror():
    """Print the last exception trace."""
    print(traceback.format_exc())


def include_tag(option, opt, value, parser, *args, **kwargs):
    try:
        if args:
            EXCLUDETAGS.remove(args[0])
        else:
            EXCLUDETAGS.remove(value)
    finally:
        pass


def exclude_tag(option, opt, value, parser, *args, **kwargs):
    if value not in EXCLUDETAGS:
        EXCLUDETAGS.append(value)


def list_tags(option, opt, value, parser, *args, **kwargs):
    alltags = []
    testsuites = []
    testdir, testfiles = gettestfiles(os.path.join
                                      (os.path.dirname(__file__), ".."))
    testloader = unittest.defaultTestLoader

    for test in testfiles:
        try:
            testmod = os.path.splitext(test)[0]
            fp, pathname, descr = imp.find_module(testmod, [testdir, ])
            package = imp.load_module(testmod, fp, pathname, descr)
            try:
                testsuites.append(loadtests_frompkg(package, testloader))
            except:
                printerror()
        except:
            pass
    for suite in testsuites:
        for test in suite:
            if hasattr(test, "__tags__"):
                tags = getattr(test, "__tags__")
                for tag in tags:
                    if tag not in alltags:
                        alltags.append(tag)
    print(alltags)
    sys.exit()


def create_options():
    """Create the accepatble options for the test runner."""
    optparser = optparse.OptionParser()
    optparser.add_option("-f", "--filename", type="string",
                         help="execute a single unit test file")
    optparser.add_option("-s", "--subprocess", action="store_true",
                         default=False,
                         help="run everything in an own subprocess "
                         "(default: use a single process)")
    optparser.add_option("-t", "--timeout", type="int", default=70,
                         help="Timout for subprocesses before being killed "
                         "(default: 70s per file)")
    optparser.add_option("-v", "--verbose", action="store_true", default=False,
                         help="be verbose and print anything instantly")
    optparser.add_option("-r", "--random", action="store_true", default=False,
                         help="randomize the order of tests")
    optparser.add_option("-S", "--seed", type="int",
                         help="seed the randomizer(useful to "
                         "recreate earlier randomized test cases)")
    optparser.add_option("-i", "--interactive", action="callback",
                         callback=include_tag,
                         callback_args=("interactive",),
                         help="also execute interactive tests")
    optparser.add_option("-e", "--exclude", action="callback",
                         callback=exclude_tag, type="string",
                         help="exclude test containing the tag")
    optparser.add_option("-l", "--listtags", action="callback",
                         callback=list_tags,
                         help="lists all available tags and exits")
    optparser.add_option("--logfile", type="string",
                         help="save output to log file")
    optkeys = ["filename",
               "subprocess",
               "timeout",
               "random",
               "seed",
               "verbose"
               ]
    return optparser, optkeys


def gettestfiles(testdir=None, randomizer=None):
    """Get all test files from the passed test directory.

    If none is passed, use the default sdl test directory.
    """
    if not testdir:
        testdir = os.path.dirname(__file__)
    if testdir not in sys.path:
        sys.path.append(testdir)

    names = os.listdir(testdir)
    testfiles = []
    for name in names:
        if name.endswith("_test" + os.extsep + "py"):
            testfiles.append(name)
    if randomizer:
        randomizer.shuffle(testfiles)
    else:
        testfiles.sort()
    return testdir, testfiles


def loadtests_frompkg(package, loader):
    for x in dir(package):
        val = package.__dict__[x]
        if hasattr(val, "setUp") and hasattr(val, "tearDown"):
            # might be a test.
            return loader.loadTestsFromTestCase(val)


def loadtests(package, test, testdir, writer, loader, options):
    """Load a test."""
    suites = []
    try:
        testmod = os.path.splitext(test)[0]

        fp, pathname, descr = imp.find_module(testmod, [testdir, ])
        print("%s.%s" % (package, testmod), fp, pathname,
                                  descr)
        exit()
        package = imp.load_module("%s.%s" % (package, testmod), fp, pathname,
                                  descr)
        if options.verbose:
            writer.writeline("Loading tests from [%s] ..." % testmod)
        else:
            writer.writesame("Loading tests from [%s] ..." % testmod)
        try:
            t = loadtests_frompkg(package, loader)
            if t:
                suites.append(t)
        except:
            printerror()
    except:
        printerror()
    return suites


def prepare_results(results):
    testcount = 0
    errors = []
    failures = []
    skips = []
    ok = 0
    for res in results:
        testcount += res.testsRun
        ok += res.testsRun - len(res.errors) - len(res.failures) - \
            len(res.skipped)
        errors.extend(res.errors)
        skips.extend(res.skipped)
        failures.extend(res.failures)
    return testcount, errors, failures, skips, ok


def validate_args(options):
    if options.subprocess and options.filename:
        raise RuntimeError("-s cannot be used together with -f")


def getanswer(question):
    answer = getinput("%s [y/n]: " % question)
    return answer.lower().strip() == 'y'


def doprint(text):
    console_on()
    getinput("%s (press enter to continue) " % text)
    console_off()


def run():
    optparser, optkeys = create_options()
    options, args = optparser.parse_args()
    validate_args(options)
    if options.logfile:
        openlog = open(options.logfile, 'wb')
        savedstd = sys.stderr, sys.stdout
        # copy stdout and stderr streams to log file
        sys.stderr = TeeOutput(sys.stderr, openlog)
        sys.stdout = TeeOutput(sys.stdout, openlog)
    writer = StreamOutput(sys.stdout)

    if options.verbose and not options.subprocess:
        writer.writeline(HEAVYDELIM)
        writer.writeline("-- Starting tests --")
        writer.writeline(HEAVYDELIM)

    randomizer = None
    if options.random:
        if options.seed is None:
            options.seed = random.randint(0, MAXINT)
        randomizer = random.Random(options.seed)
    loader = TagTestLoader(EXCLUDETAGS, randomizer)

    testdir, testfiles = None, None
    if options.filename is not None:
        testdir = os.path.dirname(os.path.abspath(options.filename))
        testfiles = [os.path.basename(options.filename), ]
    else:
        testdir, testfiles = gettestfiles(os.path.dirname(__file__),
                                          randomizer=randomizer)

    if options.subprocess:
        overall = 0
        timeout = options.timeout
        gettime = time.time
        curmodule = "%s.%s" % (__package__, inspect.getmodulename(__file__))
        for test in testfiles:
            writer.write("Executing tests from [%s]... " % test)
            procargs = [sys.executable, "-m", curmodule]
            procargs += ["-f", os.path.join(testdir, test)]
            proc = subprocess.Popen(procargs, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            maxtime = gettime() + timeout
            retval = None
            while retval is None and gettime() < maxtime:
                retval = proc.poll()
            if retval is None:
                proc.kill()
                writer.writeline("execution timed out")
            elif retval != 0:
                writer.writeline("ERROR")
                writer.write(proc.stdout.read().decode("utf-8"))
                writer.writeline()
                overall = 1
            else:
                writer.writeline("OK")
                if options.verbose:
                    writer.write(proc.stdout.read().decode("utf-8"))
                    writer.writeline()
        return overall

    testsuites = []
    package = __package__.rsplit(".", 1)[0]
    for test in testfiles:
        testsuites.extend(loadtests(package, test, testdir, writer, loader,
                                    options))
    if not options.verbose:
        writer.writesame("Tests loaded")
    runner = SimpleTestRunner(sys.stderr, options.verbose)

    results = []
    timetaken = 0

    if options.verbose:
        writer.writeline(HEAVYDELIM)
        writer.writeline("-- Executing tests --")
        writer.writeline(HEAVYDELIM)

    maxcount = 0
    for suite in testsuites:
        if suite:
            maxcount += suite.countTestCases()

    class writerunning:
        def __init__(self, maxcount, verbose):
            self.curcount = 0
            self.maxcount = maxcount
            self.verbose = verbose

        def __call__(self, test=None):
            self.curcount += 1
            if not self.verbose:
                if test:
                    writer.writesame("Running tests [ %d / %d ] [ %s ] ..." %
                                     (self.curcount, self.maxcount, test))
                else:
                    writer.writesame("Running tests [ %d / %d ] ..." %
                                     (self.curcount, self.maxcount))

    runwrite = writerunning(maxcount, options.verbose)

    for suite in testsuites:
        if suite:
            result = runner.run(suite, runwrite)
            timetaken += result.duration
            results.append(result)
    writer.writeline()
    testcount, errors, failures, skips, ok = prepare_results(results)

    writer.writeline(HEAVYDELIM)
    writer.writeline("-- Statistics --")
    writer.writeline(HEAVYDELIM)
    writer.writeline("Python:         %s" % sys.executable)
    writer.writeline("Options:")
    for key in optkeys:
        writer.writeline("                '%s' = '%s'" %
                         (key, getattr(options, key)))
    writer.writeline("                'excludetags' = '%s'" % EXCLUDETAGS)
    writer.writeline("Time taken:     %.3f seconds" % timetaken)
    writer.writeline("Tests executed: %d " % testcount)
    writer.writeline("Tests OK:       %d " % ok)
    writer.writeline("Tests SKIPPED:  %d " % len(skips))
    writer.writeline("Tests ERROR:    %d " % len(errors))
    writer.writeline("Tests FAILURE:  %d " % len(failures))

    if len(errors) > 0:
        writer.writeline("Errors:" + os.linesep)
        for err in errors:
            writer.writeline(LINEDELIM)
            writer.writeline("ERROR: %s" % err[0])
            writer.writeline(HEAVYDELIM)
            writer.writeline(err[1])
    if len(failures) > 0:
        writer.writeline("Failures:" + os.linesep)
        for fail in failures:
            writer.writeline(LINEDELIM)
            writer.writeline("FAILURE: %s" % fail[0])
            writer.writeline(HEAVYDELIM)
            writer.writeline(fail[1])
    if options.logfile:
        sys.stderr, sys.stdout = savedstd
        openlog.close()
    if len(errors) > 0 or len(failures) > 0:
        return 1
    return 0


class TagTestLoader(TestLoader):
    """Handle additional __tags__ attributes for test functions."""

    def __init__(self, excludetags, randomizer=None):
        TestLoader.__init__(self)
        self.excludetags = excludetags
        self.randomizer = randomizer

    def getTestCaseNames(self, testCaseClass):
        """Get only the tests which are not within the tag exclusion.

        The method overrides the original TestLoader.getTestCaseNames()
        method, so we need to keep them in sync on updates.
        """
        def isTestMethod(attrname, testCaseClass=testCaseClass,
                         prefix=self.testMethodPrefix):
            if not attrname.startswith(prefix):
                return False
            if not hasattr(getattr(testCaseClass, attrname), "__call__"):
                return False
            if hasattr(getattr(testCaseClass, attrname), "__tags__"):
                # Tagged test method
                tags = getattr(getattr(testCaseClass, attrname), "__tags__")
                for t in tags:
                    if t in self.excludetags:
                        return False
            return True

        if hasattr(testCaseClass, "__tags__"):
            tags = getattr(testCaseClass, "__tags__")
            for t in tags:
                if t in self.excludetags:
                    return []

        testFnNames = list(filter(isTestMethod, dir(testCaseClass)))
        cmpkey = getattr(unittest, "_CmpToKey", None) or \
            getattr(unittest, "CmpToKey", None)

        if self.randomizer:
            self.randomizer.shuffle(testFnNames)
        elif self.sortTestMethodsUsing:
            if cmpkey:
                testFnNames.sort(key=cmpkey(self.sortTestMethodsUsing))
            else:
                testFnNames.sort()
        return testFnNames


class SimpleTestResult(TestResult):
    """A simple TestResult class with output capabilities."""

    def __init__(self, stream=sys.stderr, verbose=False, countcall=None):
        TestResult.__init__(self)
        self.stream = stream
        self.duration = 0
        self.verbose = verbose
        self.countcall = countcall

    def startTest(self, test):
        super(SimpleTestResult, self).startTest(test)
        self.countcall(test)

    def addSkip(self, test, reason):
        TestResult.addSkip(self, test, reason)
        if self.verbose:
            self.stream.write("SKIPPED: %s [%s]%s" % (test, reason,
                                                      os.linesep))
            self.stream.flush()

    def addSuccess(self, test):
        TestResult.addSuccess(self, test)
        if self.verbose:
            self.stream.write("OK:      %s%s" % (test, os.linesep))
            self.stream.flush()

    def addError(self, test, err):
        TestResult.addError(self, test, err)
        if self.verbose:
            self.stream.write("ERROR:   %s%s" % (test, os.linesep))
            self.stream.flush()

    def addFailure(self, test, err):
        TestResult.addFailure(self, test, err)
        if self.verbose:
            self.stream.write("FAILED:  %s%s" % (test, os.linesep))
            self.stream.flush()


class SimpleTestRunner(object):

    def __init__(self, stream=sys.stderr, verbose=False):
        self.stream = stream
        self.verbose = verbose

    def run(self, test, countcall):
        result = SimpleTestResult(self.stream, self.verbose, countcall)
        starttime = time.time()
        test(result)
        endtime = time.time()
        result.duration = endtime - starttime
        return result


class StreamOutput(object):

    def __init__(self, stream):
        self.stream = stream
        try:
            self.startoffset = self.stream.tell()
        except IOError:
            self.startoffset = 0
        self.curoffset = 0

    def writeline(self, data=None):
        if data:
            self.stream.write(data)
        self.stream.write(os.linesep)
        if data:
            self.curoffset = len(data)
        else:
            self.curoffset = 0
        self.stream.flush()

    def write(self, data):
        self.stream.write(data)
        self.curoffset = len(data)
        self.stream.flush()

    def writesame(self, data):
        overhang = self.curoffset - len(data)
        if overhang > 0:
            self.stream.write("%s %s\r" % (data, " " * overhang))
        else:
            self.stream.write("%s\r" % data)
        self.curoffset = len(data)
        self.stream.flush()


class TeeOutput(object):

    def __init__(self, stream1, stream2):
        self.outputs = [stream1, stream2]

    # -- methods from sys.stdout / sys.stderr
    def write(self, data):
        for stream in self.outputs:
            if PY3K:
                if 'b' in stream.mode:
                    data = data.encode('utf-8')
            stream.write(data)

    def tell(self):
        raise IOError

    def flush(self):
        for stream in self.outputs:
            stream.flush()
    # --/ sys.stdout


class interactive(object):
    """Simple interactive question decorator for unit test methods."""

    def __init__(self, question=None):
        self.question = question

    def __call__(self, func):
        def wrapper(*fargs, **kw):
            if fargs and getattr(fargs[0], "__class__", None):
                instance = fargs[0]
                funcargs = fargs[1:]
                print(os.linesep)
                func(instance, *funcargs, **kw)
                if self.question:
                    if not getanswer(self.question):
                        instance.fail()

        wrapper.__name__ = func.__name__
        wrapper.__dict__.update(func.__dict__)
        wrapper.__tags__ = ['interactive']
        return wrapper


if __name__ == "__main__":
    sys.exit(run())
