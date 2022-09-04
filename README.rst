StringAnalyzer
======================================

.. |buildstatus|_
.. |coverage|_
.. |docs|_
.. |packageversion|_

.. docincludebegin

This module analyzes character categories.

Quick Start (command line)
-----------

.. code-block:: python

   >>> from StringAnalyzer import analyze_string

   >>> # define parameters
   >>> input_string = 'Kennedystraße, 51147 Köln, ドイツ'
   >>> input_string += chr(165)

   >>> # execute function
   >>> result = analyze_string(
   >>>      input_string = input_string, 
   >>>      is_comprehensive = True
   >>> )

This ``result`` contains counts of all character categories. 

.. code-block:: sh

	{
		'numeric': 5,
		'lower_letter': 13,
		'upper_letter': 2,
		'ascii': 5,
		'extended_ascii': 0,
		'extended_alphabet': 2,
		'symbols': 1,
		'other': 3
	}

This categorization with the existing categories defined in ``Utilities`` can be updated in ``count_string_categories_comprehensive``. Categories defined in ``Utilities`` are:

	* numeric
	* alphabet_upper
	* alphabet_lower
	* ascii (except alphabets)
	* ascii control
	* extended_ascii
	* extended_ascii_non_printable
	* latin_upper
	* latin_lower
	* currency
	* math
	* other
