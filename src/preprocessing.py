import mne
import numpy as np

def load_eeg_recording(file_path, channels, bands, tmin=0.0, tmax=2.0):
    raw = mne.io.read_raw_edf(file_path, preload=True, verbose=False)
    raw.set_eeg_reference(ref_channels="average", projection=False, verbose=False)

    events, event_id = mne.events_from_annotations(raw, verbose=False)

    channel_lookup = {ch.rstrip(".").upper(): ch for ch in raw.ch_names}
    selected_channels = [channel_lookup[ch.upper()] for ch in channels]

    epoch_data = []
    reference_events = None

    for band_name, (fmin, fmax) in bands.items():
        raw_band = raw.copy().pick(selected_channels)
        raw_band.filter(l_freq=fmin, h_freq=fmax, verbose=False)

        epochs = mne.Epochs(raw_band, events, event_id={"T1": event_id["T1"], "T2": event_id["T2"]},
                            tmin=tmin, tmax=tmax, baseline=None, preload=True,
                            reject_by_annotation=True, verbose=False)
        epochs.reorder_channels(selected_channels)

        if reference_events is None:
            reference_events = epochs.events.copy()
        else:
            assert np.array_equal(epochs.events, reference_events), "Epoch mismatch between bands."

        epoch_data.append(epochs.get_data())

    X = np.stack(epoch_data, axis=1)
    y = np.where(reference_events[:, -1] == event_id["T1"], 0, 1)

    return X, y