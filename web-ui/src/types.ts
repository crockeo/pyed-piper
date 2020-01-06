// Interface corresponding to the SynthButtonSetting model on the server. Used
// to represent button state on the client.
export interface ISynthButtonSetting {
  // Shared fields
  index: number;
  mode: "tone" | "wav";
  linger_time: number;

  // Tone-specific fields
  frequency: number | null;
  overtones: number | null;

  // Wav-specific fields
  wav_id: string | null;
}

// Interface corresponding to the WavFile model on the server. Used to
// represent the metadata around available samples on the server.
export interface IWavFile {
  id: string;
  path: string;
  name: string;
}
