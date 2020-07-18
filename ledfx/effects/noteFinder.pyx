from ledfx.effects cimport cnoteFinder

cdef class NoteFinder:
	cdef cnoteFinder.NoteFinder* _c_note_finder

	def __cinit__(self, sample_rate):
		self._c_note_finder = cnoteFinder.CreateNoteFinder(sample_rate)
		if self._c_note_finder is NULL:
			raise MemoryError()

	def __dealloc__(self):
		if self._c_note_finder is not NULL:
			# todo: free
			pass

	def reconfigure(self):
		cnoteFinder.ChangeNFParameters(self._c_note_finder)

	def samples_updated(self, samples):
		cnoteFinder.RunNoteFinder(self._c_note_finder, samples, 0, len(samples))