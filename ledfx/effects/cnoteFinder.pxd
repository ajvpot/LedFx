cdef extern from "notefinder.h":
	struct NoteFinder:
		pass

	NoteFinder*CreateNoteFinder(int spsRec);
	void ChangeNFParameters(void *v);

	#void RunNoteFinder( struct NoteFinder * nf, const float * audio_stream, int head, int buffersize );

	void RunNoteFinder(NoteFinder*nf, float*audio_stream, int head, int buffersize);
