cdef extern from "notefinder.h":
	struct NoteFinder:
		int freqbins # = 24
		int note_peaks; #Calculated from freqbins (not configurable)

	#For the "note_" section, the arrays are of size (freqbins/2)
		#OUTPUTS: You probably want these; the amplitude and frequency of each note the system found.
		float * note_positions;			#Position of note, in 0..freqbins frequency.  [note_peaks]
		float * note_amplitudes_out;	#Amplitude of note (after "chop") [note_peaks]
		float * note_amplitudes2;	#Amplitude of note (after "chop") [note_peaks] (using iir2)

		#Other note informations
		float * note_amplitudes;		#Amplitude of note (before "chop") [note_peaks]
		unsigned char * note_founds;	#Array of whether or note a note is taken by a frequency normal distribution [note_peaks]

		#Utility to search from [note_peaks] as index -> nf->dists as value.
		#This makes it possible to read dist_amps[note_peaks_to_dists_mapping[note]].
		char * note_peaks_to_dists_mapping;

		#Enduring note id:  From frame to frame, this will keep values the same.  That way you can know if a note has changed.
		int * enduring_note_id; #If value is 0, it is not in use.  [note_peaks]
		int current_note_id;

		#The unfolded spectrum.
		float * outbins;

		#The folded output of the unfolded spectrum.
		float * folded_bins;


	NoteFinder*CreateNoteFinder(int spsRec);
	void ChangeNFParameters(void *v);

	#void RunNoteFinder( struct NoteFinder * nf, const float * audio_stream, int head, int buffersize );

	void RunNoteFinder(NoteFinder*nf, float*audio_stream, int head, int buffersize);
