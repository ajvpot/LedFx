cimport cython
cimport cnoteFinder
from libc.stdlib cimport malloc, free

cdef read_floats(float *ptr, int n):
	cdef int i
	lst=[]
	for i in range(n):
		lst.append(ptr[i])
	return lst


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
		cdef:
			float * cfloats
			int i
		cfloats = <float *> malloc(len(samples)*cython.sizeof(float))
		if cfloats is NULL:
			raise MemoryError()
		for i in range(len(samples)):
			cfloats[i] = samples[i]/float(255)
		#todo: https://cython.readthedocs.io/en/latest/src/userguide/memoryviews.html use memory view
		cnoteFinder.RunNoteFinder(self._c_note_finder, cfloats, 0, len(samples))
		free(cfloats)

	def get_amplitudes(self):
		return dict(zip(read_floats(self._c_note_finder.note_positions, self._c_note_finder.note_peaks), read_floats(self._c_note_finder.note_amplitudes, self._c_note_finder.note_peaks)))

	def get_current(self):
		return self._c_note_finder.current_note_id

