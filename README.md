# Writernote

<table border="0px" ><tr><td width = 600px>


</td><td>

</td></tr></table>


<table>
<tr>
<td>

## Linux

<img src="readme/linux-example.png" width=100% title="writernote Screenshot on Linux"/>

</td>
</tr><tr><td>

</td></tr><tr>
</tr></table>

## Experimental Features:

- Compress video

## Installing
  - Linux: 
    
    Install stable version
    ```bash
    sudo snap install writernote --edge
    sudo snap connect writernote:audio-record
    ```

    Install unstable version [last]
    With multipass you can specify how many thread, ram, and disk, for the virtual machine for compilation.
    Personaly i use 20 thread, 18G ram, and 100G of disk.

    ```bash
    sudo snap install multipass 
    sudo snap install snapcraft --classic
    git clone https://github.com/giacomogroppi/writernote.git
    cd writernote
    multipass launch --name snapcraft-writernote --cpus 20 --mem 18G --disk 100G
    snapcraft

    sudo snap install writernote*.snap --devmode --dangerous
    sudo snap connect writernote:audio-record
    ```

  - Windows:
  Coming soon

  

## File format

The _.writer format is a compressed archive, in which a file `` index.json '' can be found, in which all the notebooks and all the audio are saved, whether they are recorded, or whether they are imported via the application.

When the file is opened, it is compressed and saved in a folder, called `` .temporaneo '', within the file location, when you then decide to save the file it is compressed and replaced with the original.

In case the program closes due to some problem, without compressing the `` .temporaneo '' folder, it can be recovered using the appropriate function within the application.

## Development

The application is entirely developed by Giacomo Groppi.
For developing new features, write a Ticket, so others know what you are doing. For development create a fork, and use the test as base. Create a Pull request for each fix. Do not create big pull requests, as long as you don't break anything features also can be merged, even if they are not 100% finished.. To report a problem send an email to the same address [possible with the error log and with a photo].

See [GitHub:writernote](http://github.com/giacomogroppi/writernote) for current development.
