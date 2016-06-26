# -*- coding: utf-8 -*-

import unittest
import jsonesque

class TestProcess(unittest.TestCase):
	def test_input_empty(self):
		self.assertEqual('', jsonesque.process(None))
		self.assertEqual('', jsonesque.process(''))

	def test_input_only_white_space(self):
		self.assertEqual('', jsonesque.process('    '))
		self.assertEqual('', jsonesque.process('\t'))
		self.assertEqual('', jsonesque.process('\n'))
		self.assertEqual('', jsonesque.process(' \t \n \r '))

	def test_input_leading_white_space(self):
		self.assertEqual('1', jsonesque.process(' 1'))
		self.assertEqual('1', jsonesque.process('\t1'))
		self.assertEqual('1', jsonesque.process('\n1'))
		self.assertEqual('1', jsonesque.process('\r1'))
		self.assertEqual('1', jsonesque.process(' \t\n 1'))

	def test_input_trailing_white_space(self):
		self.assertEqual('1', jsonesque.process('1 '))
		self.assertEqual('1', jsonesque.process('1\t'))
		self.assertEqual('1', jsonesque.process('1\n'))
		self.assertEqual('1', jsonesque.process('1\r'))
		self.assertEqual('1', jsonesque.process('1 \t\n '))

	def test_input_null(self):
		self.assertEqual('null', jsonesque.process('null'))
		self.assertEqual('null', jsonesque.process(' null '))

	def test_input_integer(self):
		self.assertEqual('1', jsonesque.process('1'))
		self.assertEqual('1', jsonesque.process(' 1 '))

	def test_input_string(self):
		self.assertEqual('"foo"',          jsonesque.process('"foo"'))
		self.assertEqual('"foo"',          jsonesque.process(' "foo" '))
		self.assertEqual('" foo "',        jsonesque.process('" foo "'))
		self.assertEqual('" foo "',        jsonesque.process(' " foo " '))
		self.assertEqual(r'"foo \"bar\""', jsonesque.process(r'"foo \"bar\""'))
		self.assertEqual(r'"foo \"bar\""', jsonesque.process(r' "foo \"bar\"" '))

	def test_input_array(self):
		self.assertEqual('[]',      jsonesque.process('[]'))
		self.assertEqual('[]',      jsonesque.process('[ ]'))
		self.assertEqual('[]',      jsonesque.process(' [] '))
		self.assertEqual('[1]',     jsonesque.process('[1]'))
		self.assertEqual('[1]',     jsonesque.process('[ 1 ]'))
		self.assertEqual('[1,2,3]', jsonesque.process('[1,2,3]'))
		self.assertEqual('[1,2,3]', jsonesque.process('[ 1, 2 , 3 ]'))

	def test_input_object(self):
		self.assertEqual('{}',            jsonesque.process('{}'))
		self.assertEqual('{}',            jsonesque.process('{ }'))
		self.assertEqual('{}',            jsonesque.process(' {} '))
		self.assertEqual('{"a":1}',       jsonesque.process('{"a":1}'))
		self.assertEqual('{"a":1}',       jsonesque.process('{ "a" : 1 }'))
		self.assertEqual('{"a":1,"b":2}', jsonesque.process('{"a":1,"b":2}'))
		self.assertEqual('{"a":1,"b":2}', jsonesque.process('{ "a": 1 , "b" : 2 }'))

	def test_input_array_with_trailing_comma(self):
		self.assertEqual('[1]',   jsonesque.process('[1,]'))
		self.assertEqual('[1]',   jsonesque.process('[1 ,]'))
		self.assertEqual('[1]',   jsonesque.process('[1, ]'))
		self.assertEqual('[1]',   jsonesque.process('[1 , ]'))
		self.assertEqual('[1,2]', jsonesque.process('[1,2,]'))
		self.assertEqual('[1,2]', jsonesque.process('[1 , 2 , ]'))
		self.assertEqual('[1,2]', jsonesque.process('''
			[
				1,
				2,
			]
		'''))

	def test_input_object_with_trailing_comma(self):
		self.assertEqual('{"a":1}',       jsonesque.process('{"a":1,}'))
		self.assertEqual('{"a":1}',       jsonesque.process('{"a":1 ,}'))
		self.assertEqual('{"a":1}',       jsonesque.process('{"a": 1, }'))
		self.assertEqual('{"a":1}',       jsonesque.process('{"a": 1 , }'))
		self.assertEqual('{"a":1,"b":2}', jsonesque.process('{"a":1,"b": 2,}'))
		self.assertEqual('{"a":1,"b":2}', jsonesque.process('{"a": 1 , "b" : 2 , }'))
		self.assertEqual('{"a":1,"b":2}', jsonesque.process('''
			{
				"a": 1,
				"b": 2,
			}
		'''))

	def test_input_only_single_line_python_comment(self):
		self.assertEqual('', jsonesque.process('# foo bar'))
		self.assertEqual('', jsonesque.process('  # foo bar'))
		self.assertEqual('', jsonesque.process('# foo bar\n'))
		self.assertEqual('', jsonesque.process('# foo "bar"'))
		self.assertEqual('', jsonesque.process('# foo bar # baz'))
		self.assertEqual('', jsonesque.process('# foo bar # baz\n'))

	def test_input_trailing_single_line_python_comment(self):
		self.assertEqual('1',   jsonesque.process('1# foo bar'))
		self.assertEqual('1',   jsonesque.process('1 # foo bar'))
		self.assertEqual('1',   jsonesque.process('1 # foo bar\n'))
		self.assertEqual('"a"', jsonesque.process('"a"# foo bar'))
		self.assertEqual('"a"', jsonesque.process('"a" # foo bar'))
		self.assertEqual('"a"', jsonesque.process('"a" # foo bar\n'))
		self.assertEqual('"a"', jsonesque.process('"a" # foo "bar"'))

	def test_input_misc_single_line_python_comment(self):
		self.assertEqual('1', jsonesque.process('''
			# foo bar
			1
		'''))
		self.assertEqual('"#"', jsonesque.process('''
			# foo bar
			"#"
		'''))
		self.assertEqual('["#"]', jsonesque.process('''
			# foo bar
			["#"]
		'''))
	def test_input_only_single_line_c_comment(self):
		self.assertEqual('', jsonesque.process('// foo bar'))
		self.assertEqual('', jsonesque.process('  // foo bar'))
		self.assertEqual('', jsonesque.process('// foo bar\n'))
		self.assertEqual('', jsonesque.process('// foo "bar"'))
		self.assertEqual('', jsonesque.process('// foo bar # baz'))
		self.assertEqual('', jsonesque.process('// foo bar # baz\n'))

	def test_input_trailing_single_line_c_comment(self):
		self.assertEqual('1',   jsonesque.process('1// foo bar'))
		self.assertEqual('1',   jsonesque.process('1 // foo bar'))
		self.assertEqual('1',   jsonesque.process('1 // foo bar\n'))
		self.assertEqual('"a"', jsonesque.process('"a"// foo bar'))
		self.assertEqual('"a"', jsonesque.process('"a" // foo bar'))
		self.assertEqual('"a"', jsonesque.process('"a" // foo bar\n'))
		self.assertEqual('"a"', jsonesque.process('"a" // foo "bar"'))

	def test_input_misc_single_line_c_comment(self):
		self.assertEqual('1', jsonesque.process('''
			// foo bar
			1
		'''))
		self.assertEqual('"//"', jsonesque.process('''
			// foo bar
			"//"
		'''))
		self.assertEqual('["//"]', jsonesque.process('''
			// foo bar
			["//"]
		'''))

	def test_input_only_multi_line_c_comment(self):
		self.assertEqual('', jsonesque.process('/* foo bar */'))
		self.assertEqual('', jsonesque.process('  /* foo bar */'))
		self.assertEqual('', jsonesque.process('/* foo bar */\n'))
		self.assertEqual('', jsonesque.process('/* foo "bar" */'))
		self.assertEqual('', jsonesque.process('/* foo bar # baz */'))
		self.assertEqual('', jsonesque.process('/* foo bar # baz */\n'))

	def test_input_trailing_multi_line_c_comment(self):
		self.assertEqual('1',   jsonesque.process('1/* foo bar */'))
		self.assertEqual('1',   jsonesque.process('1 /* foo bar */'))
		self.assertEqual('1',   jsonesque.process('1 /* foo bar */\n'))
		self.assertEqual('"a"', jsonesque.process('"a"/* foo bar */'))
		self.assertEqual('"a"', jsonesque.process('"a" /* foo bar */'))
		self.assertEqual('"a"', jsonesque.process('"a" /* foo bar */\n'))
		self.assertEqual('"a"', jsonesque.process('"a" /* foo "bar" */'))

	def test_input_misc_multi_line_c_comment(self):
		self.assertEqual('1', jsonesque.process('''
			/* foo bar */
			1
		'''))
		self.assertEqual('1', jsonesque.process('''
			/*
				foo
				bar
				// baz
			*/
			1
		'''))
		self.assertEqual('"/*"', jsonesque.process('''
			/* foo bar */
			"/*"
		'''))
		self.assertEqual('["/*"]', jsonesque.process('''
			/* foo bar */
			["/*"]
		'''))
		self.assertEqual('["/*"]', jsonesque.process('''
			[/* foo */"/*" /* bar */ ]
		'''))

	def test_input_misc_complex(self):
		self.assertEqual(
			r'{"//":"/* foo */","\"":"# bar #"}',
			jsonesque.process(r'''
				{//{
					"//": "/* foo */",
					"\"": "# bar #",
					// "\"": "// bar //",
				}//}
			''')
		)
		self.assertEqual(
			r'{"a":[1,2,3],"b":[1,2,3],"c":[1,2,3],"d":{"foo":[1],"bar":null,"baz":[1]}}',
			jsonesque.process(r'''
				// foo bar
				{
					// foo bar
					"a": [ 1,2,3 ],
					"b": [1, 2 , 3 ,/*foo bar*/],
					"c":# foo bar
					[
						# foo bar
						1,
						2,//foo bar
						3,
						/*
							foo
							bar
						 */
					],
					"d": {
						"foo": [1,],
						"bar": null,
						"baz": /*
							foo bar
						*/[
							/* foo bar */
							1
						]
					},
				}
			''')
		)

if __name__ == '__main__':
	unittest.main()

