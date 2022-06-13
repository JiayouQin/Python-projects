def show_window(_input,named_window=False):
	if type(_input) == str:
		cv.imshow(_input,eval(_input))
		cv.namedWindow(_input,eval(_input))
	if type(_input) == tuple or list:
		for name in _input:
			cv.imshow(name,eval(name))
			cv.namedWindow(name,eval(name))