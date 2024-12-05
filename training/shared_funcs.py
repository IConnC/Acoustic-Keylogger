def GET_ALL_LABELS(tf):
    return tf.constant(['Rctrl', 'p', 'esc', 'g', 'slash', 'down', '7', 'equal', 'w', 'a', 'dash', 'caps', 'l', 'd', 'backspace', 'bracketclose', 'z', '1', 'end', 'Rshift', 'comma', 'c', 'tab', 'b', 'j', 'right', 'Lctrl', 'n', 't', 'f', 'm', 'o', 'apostrophe', 'y', '8', 'space', 'backslash', 's', '9', 'i', 'r', 'bracketopen', 'semicolon', 'q', '5', 'k', '3', 'x', '4', '6', '2', 'Lshift', 'left', 'backtick', 'enter', 'fullstop', 'e', '0', 'h', 'v', 'up', 'u', 'delete'], dtype=tf.string)

# Encodes a list of instance labels into a binary vector
def multi_label_binary_encode_tensor(tf, instance_labels):
    ALL_LABELS = GET_ALL_LABELS(tf)
    # Ensure instance_labels is a list (to handle both single and multi-label cases)
    if isinstance(instance_labels, tf.Tensor) and instance_labels.shape == ():
        instance_labels = tf.expand_dims(instance_labels, axis=0)

    # Ensure instance_labels is a list
    if isinstance(instance_labels, str):
        instance_labels = [instance_labels]
        
    # print(f"Encoding labels: {instance_labels}")  # Debug

    # Create a tensor of zeros with the same length as all_labels
    binary_vector = tf.zeros(len(ALL_LABELS), dtype=tf.int32)

    # Iterate through instance_labels and set corresponding indices to 1
    for label in instance_labels:
        # Find the index of the label in ALL_LABELS using TensorFlow string matching
        matches = tf.equal(ALL_LABELS, label)
        indices = tf.where(matches)  # Indices where matches occur
        if tf.size(indices) > 0:  # Ensure the label exists in ALL_LABELS
            index = indices[0][0]
            binary_vector = tf.tensor_scatter_nd_update(
                binary_vector, indices=[[index]], updates=[1]
            )
    
    return binary_vector

def multi_label_binary_decode_tensor(tf, binary_vector):
    # binary_vector = binary_vector.numpy()
    ALL_LABELS = GET_ALL_LABELS(tf)
    decoded_labels = [ALL_LABELS[i] for i, val in enumerate(binary_vector) if val == 1]
    return decoded_labels

def get_waveform(tf, filepath):
    audio_binary = tf.io.read_file(filepath)
    audio = tf.squeeze(audio_binary)
    waveform, samplerate = tf.audio.decode_wav(audio)

    # Reduce to 1 channel by averaging
    waveform = tf.reduce_mean(waveform, axis=-1)
    
    if (samplerate != 44100):
        print("Incorrect sample rate: " + filepath)
    
    return waveform

def split_into_windows(tf, waveform, frame_length=2205, frame_step=1102): # 50ms windows with 50% overlap
    # print("Waveform shape before framing:", waveform.shape)
    frames = tf.signal.frame(waveform, frame_length=frame_length, frame_step=frame_step)
    # print("Frames shape after framing (with overlap):", frames.shape)
    return frames

def split_into_sequences(tf, frames, sequence_length=3):
    num_frames = tf.shape(frames)[0]
    sequence_step = 1
    start_indices = tf.range(0, num_frames - sequence_length + 1, sequence_step)
    sequences = tf.map_fn(
        lambda start: frames[start:start + sequence_length],
        start_indices,
        fn_output_signature=tf.TensorSpec(shape=(sequence_length, frames.shape[1]), dtype=frames.dtype)
    )
    # print("Frames grouped into sequences:", sequences.shape)
    return sequences