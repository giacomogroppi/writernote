# Xournal++

[![Build Status](https://dev.azure.com/xournalpp/xournalpp/_apis/build/status/CI?branchName=master)](https://dev.azure.com/xournalpp/xournalpp/_build/latest?definitionId=1&branchName=master)
[![Join the chat at https://gitter.im/xournalpp/xournalpp](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/xournalpp/xournalpp?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

<table border="0px" ><tr><td width = 600px>

<img src="readme/main.png" width=550px% title="Xournal++ Screenshot on Linux"/>

</td><td>

</td></tr></table>

## Features

Xournal++ is a hand note taking software written in C++ with the target of flexibility, functionality and speed.
Stroke recognizer and other parts are based on Xournal Code, which you can find at [sourceforge](http://sourceforge.net/projects/xournal/)

Xournal++ features:

- Support for pen pressure, e.g. Wacom Tablet
- Support for annotating PDFs
- Fill shape functionality
- PDF Export (with and without paper style)
- PNG Export (with and without transparent background)
- Allow to map different tools / colors etc. to stylus buttons / mouse buttons
- Sidebar with Page Previews with advanced page sorting, PDF Bookmarks and Layers (can be individually hidden, editing layer can be selected)
- enhanced support for image insertion
- Eraser with multiple configurations
- Significantly reduced memory usage and code to detect memory leaks compared to Xournal
- LaTeX support (requires a working LaTeX install)
- bug reporting, auto-save, and auto backup tools
- Customizable toolbar, with multiple configurations, e.g. to optimize toolbar for portrait / landscape
- Page Template definitions
- Shape drawing (line, arrow, circle, rect, splines)
- Shape resizing and rotation
- Rotation snapping every 45 degrees
- Rect snapping to grid
- Audio recording and playback alongside with handwritten notes
- Multi Language Support, Like English, German (Deutsch), Italian (Italiano)...
- Plugins using LUA Scripting

<table>
<tr>
<td>

## Linux

<img src="readme/linux-example.png" width=100% title="Xournal++ Screenshot on Linux"/>

</td>
</tr><tr><td>

</td></tr><tr><td>

## Toolbar / Page Background / Layer

Multiple page background, easy selectable on the toolbar
<img src="readme/background.png" width=100% title="Xournal++ Screenshot"/>

</td><td>

## Layer sidebar and advance Layer selection.

<img src="readme/layer.png" width=100% title="Xournal++ Screenshot"/>

</td></tr><tr><td>

## Multiple predefined and fully customizable Toolbar.

<img src="readme/toolbar.png" width=100% title="Xournal++ Screenshot"/>

</td></tr></table>

## Experimental Features:

- Compress video

## Installing
  - Linux: 
    ```bash
    sudo snap install writernote --edge
    ```

  - Windows:
  Coming soon

## File format

The _.writer format is a compressed archive, in which a file `` index.json '' can be found, in which all the notebooks and all the audio are saved, whether they are recorded, or whether they are imported via the application.

When the file is opened, it is compressed and saved in a folder, called `` .temporaneo '', within the file location, when you then decide to save the file it is compressed and replaced with the original.

In case the program closes due to some problem, without compressing the `` .temporaneo '' folder, it can be recovered using the appropriate function within the application.

**We are currently introducing a new file format that can efficiently store attached PDF files and other attachments internally. We will still allow for attachments that are linked to external files. Please refer to [#937](https://github.com/xournalpp/xournalpp/issues/937) for futher details.**

## Development

The application is entirely developed by Giacomo Groppi, and to become part of the development send an email to giamg01@gmail.com. To report a problem send an email to the same address [possible with the error log and with a photo].

See [GitHub:xournalpp](http://github.com/giacomogroppi/writernote) for current development.
