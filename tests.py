# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2015, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###
import os
import unittest


try:
    OEREXPORTS_PATH = os.environ['OEREXPORTS_PATH']
except KeyError:
    raise RuntimeError("You must set the OEREXPORTS_PATH environment "
                       "variable to the location of oer.exports.")


class SVGGeneration(unittest.TestCase):

    def setUp(self):
        settings = self.settings = {'oer.exports_path': OEREXPORTS_PATH}
        settings['_saxon_jar_filepath'] = os.path.abspath(os.path.join(
            OEREXPORTS_PATH, 'lib', 'saxon9he.jar'))
        settings['_mathml2svg_xsl_filepath'] = os.path.abspath(os.path.join(
            OEREXPORTS_PATH, 'xslt2', 'math2svg-in-docbook.xsl'))

    @property
    def target(self):
        from cnxmathml2svg import mathml2svg
        return mathml2svg

    def test_success(self):
        mathml = b"""<math xmlns="http://www.w3.org/1998/Math/MathML"><mstyle displaystyle="true"><mrow><mi>sin</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow></mstyle></math>"""
        expected = b"""\
<svg xmlns="http://www.w3.org/2000/svg" xmlns:pmml2svg="https://sourceforge.net/projects/pmml2svg/" version="1.1" width="27.009999999999998pt" height="12.524999999999999pt" viewBox="0 0 27.009999999999998 12.524999999999999"><metadata><pmml2svg:baseline-shift>3.6949999999999985</pmml2svg:baseline-shift></metadata><g stroke="none" fill="#000000" text-rendering="optimizeLegibility" font-family="STIXGeneral,STIXSizeOneSym,STIXIntegralsD,STIXIntegralsSm,STIXIntegralsUp,STIXIntegralsUpD,STIXIntegralsUpSm,STIXNonUnicode,STIXSizeFiveSym,STIXSizeFourSym,STIXSizeThreeSym,STIXSizeTwoSym,STIXVariants"><g xmlns:doc="http://nwalsh.com/xsl/documentation/1.0" style="font-family: STIXGeneral,STIXSizeOneSym,STIXIntegralsD,STIXIntegralsSm,STIXIntegralsUp,STIXIntegralsUpD,STIXIntegralsUpSm,STIXNonUnicode,STIXSizeFiveSym,STIXSizeFourSym,STIXSizeThreeSym,STIXSizeTwoSym,STIXVariants; fill: ; background-color: transparent; "><g style="font-family: STIXGeneral,STIXSizeOneSym,STIXIntegralsD,STIXIntegralsSm,STIXIntegralsUp,STIXIntegralsUpD,STIXIntegralsUpSm,STIXNonUnicode,STIXSizeFiveSym,STIXSizeFourSym,STIXSizeThreeSym,STIXSizeTwoSym,STIXVariants; fill: ; background-color: transparent; "><g style="font-family: STIXGeneral,STIXSizeOneSym,STIXIntegralsD,STIXIntegralsSm,STIXIntegralsUp,STIXIntegralsUpD,STIXIntegralsUpSm,STIXNonUnicode,STIXSizeFiveSym,STIXSizeFourSym,STIXSizeThreeSym,STIXSizeTwoSym,STIXVariants; fill: ; background-color: transparent; "><text style="font-family: STIXGeneral, STIXSizeOneSym, STIXIntegralsD, STIXIntegralsSm, STIXIntegralsUp, STIXIntegralsUpD, STIXIntegralsUpSm, STIXNonUnicode, STIXSizeFiveSym, STIXSizeFourSym, STIXSizeThreeSym, STIXSizeTwoSym, STIXVariants; fill: black; background-color: transparent; " x="2" y="8.83" font-size="10">sin</text><g style="font-family: STIXGeneral,STIXSizeOneSym,STIXIntegralsD,STIXIntegralsSm,STIXIntegralsUp,STIXIntegralsUpD,STIXIntegralsUpSm,STIXNonUnicode,STIXSizeFiveSym,STIXSizeFourSym,STIXSizeThreeSym,STIXSizeTwoSym,STIXVariants; fill: ; background-color: transparent; "><g style="font-family: STIXGeneral, STIXSizeOneSym, STIXIntegralsD, STIXIntegralsSm, STIXIntegralsUp, STIXIntegralsUpD, STIXIntegralsUpSm, STIXNonUnicode, STIXSizeFiveSym, STIXSizeFourSym, STIXSizeThreeSym, STIXSizeTwoSym, STIXVariants; fill: black; background-color: transparent; "><text x="13.65" y="8.764999999999999" font-size="10">(</text></g><text style="font-family: STIXGeneral, STIXSizeOneSym, STIXIntegralsD, STIXIntegralsSm, STIXIntegralsUp, STIXIntegralsUpD, STIXIntegralsUpSm, STIXNonUnicode, STIXSizeFiveSym, STIXSizeFourSym, STIXSizeThreeSym, STIXSizeTwoSym, STIXVariants; font-style: italic; fill: black; background-color: transparent; " x="17.23" y="8.83" font-size="10">x</text><g style="font-family: STIXGeneral, STIXSizeOneSym, STIXIntegralsD, STIXIntegralsSm, STIXIntegralsUp, STIXIntegralsUpD, STIXIntegralsUpSm, STIXNonUnicode, STIXSizeFiveSym, STIXSizeFourSym, STIXSizeThreeSym, STIXSizeTwoSym, STIXVariants; fill: black; background-color: transparent; "><text x="21.689999999999998" y="8.764999999999999" font-size="10">)</text></g></g></g></g></g></g></svg>"""
        svg = self.target(mathml, self.settings)
        self.assertEqual(svg, expected)
