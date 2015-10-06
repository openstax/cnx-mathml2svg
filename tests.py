# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2015, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###
import os
import unittest

from pyramid import httpexceptions
from pyramid import testing as pyramid_testing
from pyramid.request import Request

from saxon import Saxon
from subprocess import CalledProcessError

try:
    OEREXPORTS_PATH = os.environ['OEREXPORTS_PATH']
except KeyError:
    raise RuntimeError("You must set the OEREXPORTS_PATH environment "
                       "variable to the location of oer.exports.")
SETTINGS = {
    'oerexports_path': os.path.abspath(OEREXPORTS_PATH),
    '_saxon_jar_filepath': os.path.abspath(os.path.join(
        OEREXPORTS_PATH, 'lib', 'saxon9he.jar')),
    '_mathml2svg_xsl_filepath': os.path.abspath(os.path.join(
        OEREXPORTS_PATH, 'xslt2', 'math2svg-in-docbook.xsl')),
    }

MATHML = """<math xmlns="http://www.w3.org/1998/Math/MathML"><mstyle displaystyle="true"><mrow><mi>sin</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow></mstyle></math>"""
# This isn't really invalid, but the pmml2svg process trips over it.
INVALID_MATHML = """<math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow> <mi>x</mi> <mo>=</mo> <mfrac> <mrow> <mo>&#8722;<!-- &#8722; --></mo> <mi>b</mi> <mo>&#177;<!-- &#177; --></mo> <msqrt> <msup> <mi>b</mi> <mn>2</mn> </msup> <mo>&#8722;<!-- &#8722; --></mo> <mn>4</mn> <mi>a</mi> <mi>c</mi> </msqrt> </mrow> <mrow> <mn>2</mn> <mi>a</mi> </mrow> </mfrac> </mrow><annotation encoding="math/tex">x=\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}</annotation></semantics></math>"""


def load_data(file_name):
    with open(file_name, 'r') as f:
        data = f. read()
    return data

SVG = load_data('test_data/svg.xml')
INVALID_MATHML_2= load_data('test_data/bad_mathml.xml')

class Test_Saxon(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._saxon = Saxon()

    @classmethod
    def tearDownClass(cls):
        cls._saxon.stop()

    def setUp(self):
        self.saxon = self._saxon

    def test_class_setup(self):
        returned_svg = self.saxon.convert(MATHML).strip('\t\r\n ')
        expected_svg = SVG.strip('\t\r\n ')
        self.assertEqual(returned_svg, expected_svg)

    def test_multiple_saxon_calls(self):
        for i in range(0, 10):
            returned_svg = self.saxon.convert(MATHML).strip('\t\r\n ')
            expected_svg = SVG.strip('\t\r\n ')
            self.assertEqual(returned_svg, expected_svg)

    def test_invalid_mathml_error(self):
        self.addCleanup(self.setUpClass)
        with self.assertRaises(CalledProcessError):
            self.saxon.convert(INVALID_MATHML)

    def test_transform_failure_4(self):
        """test freezing mathmls"""
        self.addCleanup(self.setUpClass)
        from lxml import etree
        import re
        import os
        import threading
        import signal
        import time
#        from cnxmathml2svg import convert
        def sax_thread(self,mathml):
            print self.saxon.convert(etree.tostring(mathml))

        def failure(self):
#            os.close(self.saxon.process.stdout.fileno())
#            self.saxon._close()
            os.kill(self.saxon.process.pid, signal.SIGUSR1)
#            os.kill(self.saxon.process.pid, signal.SIGUSR1)
            self.saxon._close()
#            self.saxon._flush()
#            self.saxon.stop()
#            self.saxon.process.terminate()
#            self.saxon.stop()
#            import ipdb; ipdb.set_trace()
            
#            self.fail()

        root = etree.fromstring(load_data("./test_data/mathml_tree.xml"))
#        root = root[10:224]
#        del root[100:101]
#        del root[106:165]
#        for mathml in root[9:225]:
        doc_length = len(self.test_transform_failure_4.__doc__)
        count = 0
        for mathml in root:
            
            count = count+1
#            print count
#            print self.test_transform_failure_4.__doc__," ... ",count/len(root)*100," percent complete\r",

            doc_string = self.test_transform_failure_4.__doc__ + " ... "
            percent_complete = "{0:.0f}% complete".format((float(count)/float(len(root)) * 100.0))
            status_string = "\r{0} {1}".format(doc_string,percent_complete)
            print status_string,
#            print mathml
#            t=threading.Timer(4.0,failure,args=(self,))
            t=threading.Thread(target=sax_thread,args=(self,mathml))
            t.setDaemon(True)
            t.start()
            start_time = time.time()
            while t.is_alive():
                current_time = time.time()
#                if count == 10:
                if current_time - start_time > 4.0:
#                    print "\r"," "*len(status_string),"\r",
#                    print "\r{0} ... ".format(doc_string),
#                    print "\r",doc_string,
                    self.fail("saxon process took too long")

#                    print "{0} ... \r".format(doc_string),
#                    self.fail("saxon process took too long")
            t.join()
#            t.start()
#            self.saxon.convert(etree.tostring(mathml))
#            t.cancel()
#            request = Request.blank('/', POST={'MathML': etree.tostring(mathml)})
#            print etree.tostring(mathml)
#            print mathml
#            convert(request)

    @unittest.skip("Run this test to generate performance graphics")
    def test_performance_gain(self):
        """Compare Saxon class to subprocss performance"""
        import math
        import timeit
        import numpy as np
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        x=[]
        y_single=[]
        y_multi=[]
        for iterations in [int(math.pow(2,i)) for i in range(0,5)]:
            stmt="saxon.convert('{}')".format(MATHML)
            setup='from saxon import Saxon;saxon=Saxon()'
            single_process_call=timeit.timeit(stmt,setup,number=iterations)
            setup="import subprocess;cmd = 'java -jar {_saxon_jar_filepath} -s:- -xsl:{_mathml2svg_xsl_filepath}'".format(**SETTINGS)
            stmt="p = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True);p.communicate('{}')".format(MATHML)
            multiple_process_call=timeit.timeit(stmt,setup,number=iterations)
            self.assertLess(single_process_call,multiple_process_call)
            x.append(iterations)
            y_single.append(single_process_call)
            y_multi.append(multiple_process_call)

        slope_single, intercept_single = np.polyfit(x,y_single,1)
        slope_multi, intercept_multi = np.polyfit(x,y_multi,1)
        plt.title("Estimated {0:.1f}x performance gain ".format(slope_multi/slope_single))
        
        plot_single, =plt.plot(x, y_single)
        plot_multi, =plt.plot(x, y_multi)
        plt.legend([plot_single,plot_multi],['single process','multiple processes'],loc=0)
        plt.axis([0,max(x),0,max(max(y_single),max(y_multi))])
        plt.ylabel("Time (s)")
        plt.xlabel("Loop iterations")
        plt.show()        

         

class SVGGeneration(unittest.TestCase):

    def setUp(self):
        self.settings = SETTINGS.copy()

    @property
    def target(self):
        from cnxmathml2svg import mathml2svg
        return mathml2svg

    def test_success(self):
        mathml = MATHML.encode('utf-8')
        expected = b"""\
<svg xmlns="http://www.w3.org/2000/svg" xmlns:pmml2svg="https://sourceforge.net/projects/pmml2svg/" version="1.1" width="27.009999999999998pt" height="12.524999999999999pt" viewBox="0 0 27.009999999999998 12.524999999999999"><metadata><pmml2svg:baseline-shift>3.6949999999999985</pmml2svg:baseline-shift></metadata><g stroke="none" fill="#000000" text-rendering="optimizeLegibility" font-family="STIXGeneral,STIXSizeOneSym,STIXIntegralsD,STIXIntegralsSm,STIXIntegralsUp,STIXIntegralsUpD,STIXIntegralsUpSm,STIXNonUnicode,STIXSizeFiveSym,STIXSizeFourSym,STIXSizeThreeSym,STIXSizeTwoSym,STIXVariants"><g xmlns:doc="http://nwalsh.com/xsl/documentation/1.0" style="font-family: STIXGeneral,STIXSizeOneSym,STIXIntegralsD,STIXIntegralsSm,STIXIntegralsUp,STIXIntegralsUpD,STIXIntegralsUpSm,STIXNonUnicode,STIXSizeFiveSym,STIXSizeFourSym,STIXSizeThreeSym,STIXSizeTwoSym,STIXVariants; fill: ; background-color: transparent; "><g style="font-family: STIXGeneral,STIXSizeOneSym,STIXIntegralsD,STIXIntegralsSm,STIXIntegralsUp,STIXIntegralsUpD,STIXIntegralsUpSm,STIXNonUnicode,STIXSizeFiveSym,STIXSizeFourSym,STIXSizeThreeSym,STIXSizeTwoSym,STIXVariants; fill: ; background-color: transparent; "><g style="font-family: STIXGeneral,STIXSizeOneSym,STIXIntegralsD,STIXIntegralsSm,STIXIntegralsUp,STIXIntegralsUpD,STIXIntegralsUpSm,STIXNonUnicode,STIXSizeFiveSym,STIXSizeFourSym,STIXSizeThreeSym,STIXSizeTwoSym,STIXVariants; fill: ; background-color: transparent; "><text style="font-family: STIXGeneral, STIXSizeOneSym, STIXIntegralsD, STIXIntegralsSm, STIXIntegralsUp, STIXIntegralsUpD, STIXIntegralsUpSm, STIXNonUnicode, STIXSizeFiveSym, STIXSizeFourSym, STIXSizeThreeSym, STIXSizeTwoSym, STIXVariants; fill: black; background-color: transparent; " x="2" y="8.83" font-size="10">sin</text><g style="font-family: STIXGeneral,STIXSizeOneSym,STIXIntegralsD,STIXIntegralsSm,STIXIntegralsUp,STIXIntegralsUpD,STIXIntegralsUpSm,STIXNonUnicode,STIXSizeFiveSym,STIXSizeFourSym,STIXSizeThreeSym,STIXSizeTwoSym,STIXVariants; fill: ; background-color: transparent; "><g style="font-family: STIXGeneral, STIXSizeOneSym, STIXIntegralsD, STIXIntegralsSm, STIXIntegralsUp, STIXIntegralsUpD, STIXIntegralsUpSm, STIXNonUnicode, STIXSizeFiveSym, STIXSizeFourSym, STIXSizeThreeSym, STIXSizeTwoSym, STIXVariants; fill: black; background-color: transparent; "><text x="13.65" y="8.764999999999999" font-size="10">(</text></g><text style="font-family: STIXGeneral, STIXSizeOneSym, STIXIntegralsD, STIXIntegralsSm, STIXIntegralsUp, STIXIntegralsUpD, STIXIntegralsUpSm, STIXNonUnicode, STIXSizeFiveSym, STIXSizeFourSym, STIXSizeThreeSym, STIXSizeTwoSym, STIXVariants; font-style: italic; fill: black; background-color: transparent; " x="17.23" y="8.83" font-size="10">x</text><g style="font-family: STIXGeneral, STIXSizeOneSym, STIXIntegralsD, STIXIntegralsSm, STIXIntegralsUp, STIXIntegralsUpD, STIXIntegralsUpSm, STIXNonUnicode, STIXSizeFiveSym, STIXSizeFourSym, STIXSizeThreeSym, STIXSizeTwoSym, STIXVariants; fill: black; background-color: transparent; "><text x="21.689999999999998" y="8.764999999999999" font-size="10">)</text></g></g></g></g></g></g></svg>"""
        svg = self.target(mathml, self.settings)
        self.assertEqual(svg, expected)


class Views(unittest.TestCase):

    def setUp(self):
        self.config = pyramid_testing.setUp(settings=SETTINGS)

    def tearDown(self):
        pyramid_testing.tearDown()

    def test_success_w_form_post(self):
        """Test MathML2SVG post using a text based form value."""
        request = Request.blank('/', POST={'MathML': MATHML})

        from cnxmathml2svg import convert
        response = convert(request)

        self.assertIn(b'<svg ', response.body)
        self.assertEqual(response.content_type, 'image/svg+xml')

    def test_success_w_multiform_post(self):
        """Test MathML2SVG post using a multipart form value."""
        request = Request.blank('/', POST={'MathML': ('mathml.xml', MATHML)})

        from cnxmathml2svg import convert
        response = convert(request)

        self.assertIn(b'<svg ', response.body)
        self.assertEqual(response.content_type, 'image/svg+xml')

    def test_missing_parameters(self):
        """Test response for a Bad Request when parameters are missing."""
        request = Request.blank('/')

        from cnxmathml2svg import convert
        with self.assertRaises(httpexceptions.HTTPBadRequest):
            convert(request)

    def test_transform_failure(self):
        """Test MathML2SVG post with content that won't transform,
        but contains valid xml and MathML elements.
        """
        request = Request.blank('/', POST={'MathML': INVALID_MATHML})

        from cnxmathml2svg import convert
        exception_cls = httpexceptions.HTTPInternalServerError
        with self.assertRaises(exception_cls) as caught_exc:
            convert(request)

        exception = caught_exc.exception
        self.assertIn('XMLSyntaxError: PCDATA invalid Char',exception.message)

    @unittest.skip("bad")
    def test_transform_failure_2(self):
        """Test MathML2SVG post with content that won't transform,
        but contains valid xml and MathML elements.
        """
        import re
        def atoi(text):
            return int(text) if text.isdigit() else text
        
        def natural_keys(text):
            '''
            alist.sort(key=natural_keys) sorts in human order
            http://nedbatchelder.com/blog/200712/human_sorting.html
            (See Toothy's implementation in the comments)
            '''
            return [ atoi(c) for c in re.split('(\d+)', text) ]
        import os
        from cnxmathml2svg import convert
        from lxml import etree
        from io import BytesIO
        files = [f for f in os.listdir('./test_data/bad_mathmls') if "xml" in f]
        files.sort(key=natural_keys)
        for i in range(0,len(files)):
            print files[i]
            f = open(os.path.join("./test_data/bad_mathmls",files[i]))
            mathml = f.read()
            parser = etree.XMLParser(recover=True) 
            etree.parse(BytesIO(mathml), parser)
            etree.fromstring(mathml) 
            f.close()
            request = Request.blank('/', POST={'MathML': mathml})
            convert(request)

    @unittest.skip("bad")
    def test_transform_failure_3(self):
        """Test MathML2SVG post with content that won't transform,
        but contains valid xml and MathML elements.
        """
        import sys
        import re
        import time
        def atoi(text):
            return int(text) if text.isdigit() else text
        
        def natural_keys(text):
            '''
            alist.sort(key=natural_keys) sorts in human order
            http://nedbatchelder.com/blog/200712/human_sorting.html
            (See Toothy's implementation in the comments)
            '''
            return [ atoi(c) for c in re.split('(\d+)', text) ]
        def failure(self):
            import thread
            import os
            import signal
            os.kill(os.getpid(), signal.SIGUSR1)
#            import ipdb; ipdb.set_trace()
#            self.fail()
#            thread.interrupt_main()
#            os._exit(1)
#            sys.exit(1)
            
        import os
        from cnxmathml2svg import convert
        from lxml import etree
        import threading
        import pickle

        files = [f for f in os.listdir('./test_data/bad_mathmls') if "xml" in f]
        files.sort(key=natural_keys)
        root =etree.Element("root")
        parser = etree.XMLParser()
#        files = [f for f in files if f not in files[:]]
        if False:
            range_list=[]
            for i in range(0,len(files)):
                for j in range(0,len(files)):
                    if i<j:
                        range_list.append((i,j,j-i))
            sorted_by_diff = sorted(range_list, key=lambda tup: tup[2])
            range_list=[]
            for item in sorted_by_diff:
                range_list.append((item[0],item[1]))
#            range_list=list(set(range_list))
            test_args = { 'range_set':range_list,'broken_set':[],'working_set':[], 'total_items':len(range_list)}
            output = open('test_args.pkl', 'wb')
            pickle.dump(test_args,output)
            output.close()
#            import ipdb; ipdb.set_trace()
            self.fail()
        else:
            test_input = open('test_args.pkl', 'rb')
            test_args=pickle.load(test_input)
            test_input.close()
            try:
                current=test_args['range_set'].pop()
            except(IndexError):
                import ipdb; ipdb.set_trace()
                self.fail("nothing to test")
            test_args['broken_set'].append(current)
            output = open('test_args.pkl', 'wb')
            pickle.dump(test_args,output)
            output.close()
#        import ipdb; ipdb.set_trace()
#        print test_args['range_set']
#        self.fail()
#        if len(test_args['range_set'])<=0:
#            import ipdb; ipdb.set_trace()
#            self.fail("nothing to test")
#        import ipdb; ipdb.set_trace()
#        for i in [current[0],current[1]]:
        precent_remaining = (len(test_args['range_set'])*1.0) / (test_args['total_items']*1.0)
        print("items left to check = {0:.2f}, current range = {1}".format(precent_remaining,current))
        for i in range(current[0],current[1]):
#        for i in range(0,20):

#            print files[i]
            f = open(os.path.join("./test_data/bad_mathmls",files[i]))
            mathml = f.read()
            f.close()
            etree.XML(mathml,parser)
            mathml = etree.fromstring(mathml)
            root = etree.Element("root")
            root.append(mathml)
            root = etree.tostring(root)
            request = Request.blank('/', POST={'MathML': root})
#            ct=threading.current_thread() 
            t=threading.Timer(4.0,failure,args=(self,))
            t.daemon=True
            t.start()
            convert(request)
            t.cancel()
        test_args['broken_set'].pop()
        test_args['working_set'].append(current)
        for test_arg in test_args['range_set']:
            ti = test_arg[0]
            tj = test_arg[1]
            ci = current[0]
            cj = current[1]
            if ci<=ti and tj<=cj:
                test_args['range_set'].remove(test_arg)

        output = open('test_args.pkl', 'wb')
        pickle.dump(test_args,output)
        output.close() 
#        import ipdb; ipdb.set_trace()
#        self.fail()
#        request = Request.blank('/', POST={'MathML': INVALID_MATHML_2})

#        from cnxmathml2svg import convert
#        exception_cls = httpexceptions.HTTPInternalServerError
#        with self.assertRaises(exception_cls) as caught_exc:
#            convert(request)

#        exception = caught_exc.exception
#        self.assertIn('XMLSyntaxError: PCDATA invalid Char',exception.message)
    @unittest.skip("bad")
    def test_transform_failure_4(self):
        from lxml import etree
        import re
        import os
        from cnxmathml2svg import convert
        root = etree.fromstring(load_data("./test_data/mathml_tree.xml"))
        import ipdb; ipdb.set_trace()
#        root = root[10:224]
#        del root[100:101]
#        del root[106:165]
        for mathml in root:
            request = Request.blank('/', POST={'MathML': etree.tostring(mathml)})
#            print etree.tostring(mathml)
            print mathml
            convert(request)
#        def atoi(text):
#            return int(text) if text.isdigit() else text

#        def natural_keys(text):
#            return [ atoi(c) for c in re.split('(\d+)', text) ]
#        files = [f for f in os.listdir('./test_data/bad_mathmls') if "xml" in f]
#        files.sort(key=natural_keys)
#        root = etree.Element("root")
#        wrapper = etree.Element("wrapper")

#        for i in range(0,len(files)):
#        for i in range(10,224):
#            with open(os.path.join("./test_data/bad_mathmls",files[i])) as f:
#                mathml=f.read()
#            root.append(etree.fromstring(mathml))
#        root=etree.tostring(root)
#        with open("./test_data/mathml_tree.xml","w") as f:
#            f.write(root)

#        request = Request.blank('/', POST={'MathML': root})
#        convert(request)
#        import ipdb; ipdb.set_trace()
        
