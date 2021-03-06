==Teaching idiomatic python with git==


As far as appending to strings, here are some tests:

	cody@zentop:~$ python -m timeit -s "s = ''" "for i in xrange(0, 100): s = s + 'stuff' + 'more stuff'"
	1000 loops, best of 3: 11.6 msec per loop

	python -m timeit -s "s = ''" "for i in xrange(0, 100): s = '{0}{1}{2}'.format(s, 'stuff', 'more stuff')"
	1000 loops, best of 3: 11.7 msec per loop

	cody@zentop:~$ python -m timeit -s "s = []" "for i in xrange(0, 100): s.append('stuff'); s.append('more stuff');" "''.join(s)"
	1000 loops, best of 3: 2 msec per loop

AND.... after looking at it again and thinking "That doesn't look right", here is my final version:

	cody@zentop:~$ python -m timeit -s "s = []" "for i in xrange(0, 100): s.extend(['stuff', 'more stuff']);" "''.join(s)"
	1000 loops, best of 3: 1.85 msec per loop

Another bout of testing... this time with 10,000 loops:

	python -m timeit -n 10000 -s "s = []" "for i in xrange(0, 100): s.extend(['stuff', 'more stuff']);" "''.join(s)"
	10000 loops, best of 3: 20.4 msec per loop
	
	cody@zentop:~$ python -m timeit -n 10000 -s "s = ''" "for i in xrange(0, 100): s = '{0}{1}{2}'.format(s, 'stuff', 'more stuff')"
	# has been 30 minutes and this hasn't finished... I think it's safe to say that is the best method

Lesson: Use lists to build strings whenever possible, especially if you are going through large amounts of data.
