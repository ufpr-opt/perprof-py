import unittest
import perprof
from perprof.main import process_arguments
from perprof.main import set_arguments
from perprof import bokeh
from perprof import tikz
from perprof import matplotlib
from perprof import prof

class TestPerprof(unittest.TestCase):

    goodfiles = ' '.join(['perprof/examples/' + s + '.table' \
            for s in ['alpha', 'beta', 'gamma']])
    backends = ['bokeh', 'tikz', 'mp', 'raw']
    back_profilers = {
            "bokeh": bokeh.Profiler,
            "tikz": tikz.Profiler,
            "mp": matplotlib.Profiler,
            "raw": prof.Pdata }

    def test_backends(self):
        for backend in self.backends:
            args = '--' + backend + ' --demo'
            isTrue = {'bokeh': False, 'tikz': False, 'mp': False, 'raw': False }
            isTrue[backend] = True
            args = set_arguments(args.split())
            self.assertEqual(args.bokeh, isTrue['bokeh'])
            self.assertEqual(args.tikz, isTrue['tikz'])
            self.assertEqual(args.mp,   isTrue['mp'])
            self.assertEqual(args.raw,  isTrue['raw'])

    def test_output_formats(self):
        outputs = {
                "bokeh": ["html"],
                "tikz": ["pdf", "tex"],
                "mp": ["png", "eps", "pdf", "ps", "svg"],
                "raw": [] }
        backends = self.backends
        for backend in backends:
            for output in outputs[backend]:
                args = '--' + backend + ' --' + output + ' --demo'
                args = set_arguments(args.split())
                parser_options, profiler_options = process_arguments(args)
                self.assertEqual(profiler_options['output_format'], output)
                data = self.back_profilers[backend](parser_options,
                        profiler_options)
                if backend != "tikz":
                    self.assertEqual(data.output, 'performance-profile.{}'.format(output))

    def test_only_name(self):
        for backend in self.backends:
            args = '--' + backend + ' perprof/tests/only-name.sample ' + self.goodfiles
            args = set_arguments(args.split())
            parser_options, profiler_options = process_arguments(args)
            self.assertRaises(ValueError, self.back_profilers[backend],
                    parser_options, profiler_options)

    def test_columns(self):
        for backend in self.backends:
            baseargs = '--' + backend + ' ' + self.goodfiles
            #Default comparison needs 3 columns
            args = baseargs + ' perprof/tests/2-col.sample '
            args = set_arguments(args.split())
            parser_options, profiler_options = process_arguments(args)
            self.assertRaises(ValueError, self.back_profilers[backend],
                    parser_options, profiler_options)
            #Default values should fail with 5 or less columns.
            #Unconstrained Default values should fail with 5 or less columns
            #(because dual default column is 5).
            baseargs = '--compare optimalvalues ' + baseargs
            for xtra in ['', '--unconstrained ']:
                baseargs = xtra + baseargs
                for n in [2,3,4,5]:
                    args = baseargs + ' perprof/tests/{}-col.sample '.format(n)
                    args = set_arguments(args.split())
                    parser_options, profiler_options = process_arguments(args)
                    self.assertRaises(ValueError, self.back_profilers[backend],
                            parser_options, profiler_options)

    def test_without_time(self):
        for backend in self.backends:
            args = '--' + backend + ' perprof/tests/without-time.sample ' + self.goodfiles
            args = set_arguments(args.split())
            parser_options, profiler_options = process_arguments(args)
            self.assertRaises(ValueError, self.back_profilers[backend],
                    parser_options, profiler_options)

    def test_without_c_or_d(self):
        for backend in self.backends:
            args = '--' + backend + ' perprof/tests/c-or-d.sample ' + self.goodfiles
            args = set_arguments(args.split())
            parser_options, profiler_options = process_arguments(args)
            self.assertRaises(ValueError, self.back_profilers[backend],
                    parser_options, profiler_options)

    def test_zero_time(self):
        for backend in self.backends:
            args = '--' + backend + ' perprof/tests/zero-time.sample ' + self.goodfiles
            args = set_arguments(args.split())
            parser_options, profiler_options = process_arguments(args)
            self.assertRaises(ValueError, self.back_profilers[backend],
                    parser_options, profiler_options)

    def test_yaml_fail(self):
        for backend in self.backends:
            args = '--' + backend + ' perprof/tests/yaml-fail.sample ' + self.goodfiles
            args = set_arguments(args.split())
            parser_options, profiler_options = process_arguments(args)
            self.assertRaises(ValueError, self.back_profilers[backend],
                    parser_options, profiler_options)

    def test_empty_file(self):
        for backend in self.backends:
            args = '--' + backend + ' perprof/tests/empty.sample ' + self.goodfiles
            args = set_arguments(args.split())
            parser_options, profiler_options = process_arguments(args)
            self.assertRaises(ValueError, self.back_profilers[backend],
                    parser_options, profiler_options)

    def test_empty_subset(self):
        for backend in self.backends:
            args = '--' + backend + ' --demo --subset perprof/tests/empty.subset'
            args = set_arguments(args.split())
            self.assertRaises(AttributeError, process_arguments, args)

    def test_empty_intersection(self):
        for backend in self.backends:
            args = '--' + backend + ' --demo --subset perprof/tests/fantasy.subset'
            args = set_arguments(args.split())
            parser_options, profiler_options = process_arguments(args)
            self.assertRaises(ValueError, self.back_profilers[backend],
                    parser_options, profiler_options)

    def test_no_success(self):
        for backend in self.backends:
            if backend == "raw":
                continue
            args = '--' + backend + ' perprof/tests/no-success.sample ' + self.goodfiles
            args = set_arguments(args.split())
            parser_options, profiler_options = process_arguments(args)
            data = self.back_profilers[backend](parser_options, profiler_options)
            self.assertRaises(ValueError, data.plot)

    def test_repeated_problem(self):
        for backend in self.backends:
            args = '--' + backend + ' perprof/tests/repeat.sample ' + self.goodfiles
            args = set_arguments(args.split())
            parser_options, profiler_options = process_arguments(args)
            self.assertRaises(ValueError, self.back_profilers[backend],
                    parser_options, profiler_options)

if __name__ == '__main__':
    unittest.main()
