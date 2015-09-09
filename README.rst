MathML to SVG Service
=====================

.. Not on travis because oer.exports is a private repo.

   .. image:: https://travis-ci.org/Connexions/cnx-mathml2svg.svg
      :target: https://travis-ci.org/Connexions/cnx-mathml2svg

   .. image:: https://badge.fury.io/py/cnx-mathml2svg.svg
      :target: http://badge.fury.io/py/cnx-mathml2svg

A simple web application for accepting MathML to convert to SVG.

Install & Run
-------------

The installation requires access to the `oer.exports <https://github.com/Connexions/oer.exports>` repository for access to the MathML2SVG XSLT and Saxon executable.

::

    git clone git@github.com:Connexions/oer.exports
    python setup.py install
    pserve development.ini

Usage
-----

This application does not have a web interface.
You can post to it directly at ``/``, which will return the SVG in the response.
The POST parameter at this time is ``MathML``.

Example::

    curl -F 'MathML=<math xmlns="http://www.w3.org/1998/Math/MathML"><mstyle displaystyle="true"><mrow><mi>sin</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow></mstyle></math>' http://localhost:5689/

or::

   echo '<math xmlns="http://www.w3.org/1998/Math/MathML"><mstyle displaystyle="true"><mrow><mi>sin</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow></mstyle></math>' | curl -F 'MathML=@-' http://localhost:5689/

License
-------

This software is subject to the provisions of the GNU Affero General
Public License Version 3.0 (AGPL). See LICENSE.txt for details.
Copyright (c) 2015 Rice University
