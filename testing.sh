#!/bin/bash
# osascript -e 'display notification "" with title "RUNNING"'
USB_FILE="/Volumes/Kindle/documents/My Clippings.txt"
DEST_DIR="$HOME/Desktop"
PYTHON_SCRIPT="/Users/amer_/Documents/GitHub/KindleProject/KindleObsidianV2.py"

if diskutil list | grep -q "Kindle"; then
    if [ $? -eq 0 ]; then
        rsync -av "$USB_FILE" "$DEST_DIR"
        osascript -e 'display notification "File copied successfully" with title "USB File Copied"'
        python3 "$PYTHON_SCRIPT"
    
    # Check if Python script had an error
        if [ $? -ne 0 ]; then
            # Display error notification
            osascript -e 'display notification "Python script encountered an error. Check log file." with title "Python Script Error"'
            # Save Python log to desktop
            mv "$LOG_FILE" "$HOME/Desktop/python_script_error.log"
        else
            # Delete copied file
            rm "$DEST_DIR/My Clippings.txt"
            # Display completion notification
            osascript -e 'display notification "Script execution completed successfully" with title "Script Execution Completed"'
        fi
    else
        osascript -e 'display notification "Failed to copy file from USB. Check USB connection and try again." with title "Rsync Error"'
    fi
else
    echo "USB device not found."
fi
