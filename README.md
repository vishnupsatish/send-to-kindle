# Send to Kindle
A Python script for sending books in a directory to a Kindle address.

Note: Installing and using send-to-kindle requires the ebook-convert command from calibre.

## Instructions
1. Clone this repository using `git clone https://github.com/vishnupsatish/send-to-kindle.git`

2. Create a `config.txt` file in the "Send to Kindle" folder. Create a comma separated list of all the email addresses you want to send books to.

3. Create a `Books` directory and a `Converted Books` directory in the "Send to Kindle" folder.

4. To run the program, use the command `cd "/path/to/Send to Kindle/src" && python3 kindle.py`

The next few steps are optional.

5. If you are running MacOS, you can use the Automator application to automate this script.

6. Open automator, and press "New".

7. Select "Folder Action" for the type of document and choose the folder "Books"

8. Add the action "Run AppleScript, and add the following in the AppleScript editor.

`set theDialogText to "Do you want to add the books to the Kindle now? If not, you must delete these files from this folder."`
`display dialog theDialogText buttons {"Don't Continue", "Continue"} default button "Continue" cancel button "Don't Continue"`
`do shell script "cd \"/Users/vishnu/Downloads/Send to Kindle/src\" && /usr/local/bin/python3 kindle.py"`
`display notification "Your files have been sent to the Kindle." with title "Sent"`

9. Now, whenever files are added to the "Books" folder, this script will be run, along with a confirmation dialog.