#!/usr/bin/bash

# Define the output file name
OUTPUT_FILE="recording.wav"

# Use arecord with the specified options
arecord -D plughw:0 -c2 -r 48000 -f S32_LE -t wav -V stereo -v -d 10 "$OUTPUT_FILE"

# Check if the recording was successful
if [ $? -eq 0 ]; then
    echo "Recording completed successfully."
else
    echo "Recording encountered an error."
fi
