# -*- coding: utf-8 -*-

import re

def process(string):
	"""
	Processes a JSON-like string into a valid, minified JSON string.

	Examples:
	  Input:  [1, 2, 3,]
	  Output: [1,2,3]
	  Input:  [1, 2, /* comment */ 3]
	  Output: [1,2,3]
	  Input:  [1, 2, 3] // comment
	  Output: [1,2,3]

	@param  str string A JSON or JSON-like string to process.

	@return str Valid, minified JSON.
	"""
	if not string:
		return ''

	round_one   = re.compile(r'"|(/\*)|(\*/)|(//)|#|\n|\r')
	round_two   = re.compile(r'"|,')
	end_slashes = re.compile(r'(\\)*$')

	# We add a new-line here so that trailing comments get caught at the end of
	# the string (e.g., '[1, 2, 3] // foo') — it'll be stripped out later
	string     += "\n"
	new_string  = ''
	length      = len(string)
	index       = 0

	in_string         = False
	in_comment_multi  = False
	in_comment_single = False

	# First round — remove comments
	for match in re.finditer(round_one, string):
		# Append everything up to the match, stripping white-space along the way
		if not (in_comment_multi or in_comment_single):
			tmp = string[index:match.start()]

			if not in_string:
				tmp = re.sub('[ \t\n\r]+', '', tmp)

			new_string += tmp

		index = match.end()
		val   = match.group()

		# Handle strings
		if val == '"' and not (in_comment_multi or in_comment_single):
			escaped = end_slashes.search(string, 0, match.start())

			# Start of string or un-escaped " character to end string
			if not in_string or escaped is None or len(escaped.group()) % 2 == 0:
				in_string = not in_string
			# Include " character in next iteration
			index -= 1

		# Handle comment beginnings and trailing commas
		elif not (in_string or in_comment_multi or in_comment_single):
			if val == '/*':
				in_comment_multi = True
			elif val == '//' or val == '#':
				in_comment_single = True

		# Handle multi-line comment endings
		elif val == '*/' and in_comment_multi and not (in_string or in_comment_single):
			in_comment_multi = False
			while index < length and string[index] in ' \t\n\r':
				index += 1

		# Handle single-line comment endings
		elif val in '\n\r' and in_comment_single and not (in_string or in_comment_multi):
			in_comment_single = False

		# Anything else — just append
		elif not (in_comment_multi or in_comment_single):
			new_string += val

	new_string += string[index:]
	string      = new_string
	new_string  = ''
	length      = len(string)
	index       = 0
	in_string   = False

	# Second round — remove trailing commas
	# @todo There's a more performant way to remove these, just too lazy rn
	for match in re.finditer(round_two, string):
		# Append everything up to the match
		new_string += string[index:match.start()]

		index = match.end()
		val   = match.group()

		# Handle strings
		if val == '"':
			escaped = end_slashes.search(string, 0, match.start())

			# Start of string or un-escaped " character to end string
			if not in_string or escaped is None or len(escaped.group()) % 2 == 0:
				in_string = not in_string
			# Include " character in next iteration
			index -= 1

		# Handle commas
		elif val == ',':
			if string[index] not in ']}':
				new_string += val

		# Anything else — just append
		else:
			new_string += val

	new_string += string[index:]
	return new_string

