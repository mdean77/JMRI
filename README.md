# JMRI
This contains my JMRI configurations.  Several purposes include version control of changes, of course, as well as ability to clone the settings to other computers including my Raspberry Pi boards.  DropBox is not particularly friendly to Raspberry Pi implementation.

Obviously we make many changes to configurations, and in my instance, I have a layout, a programming track, and am building a test track for decoder calibration, based on Erich Whitney's exciting project shown in Kansas City.  I also have a simulation configuration so I can work with Jython without having hardware attached.

I got an incredibly confused spaghetti of files and folders using JMRI over the past four years, so I started over to try to organize this in an intelligent manner.  I only need ONE roster, as this will be the same regardless of profile selected upont starting PanelPro or DecoderPro.  Similarly, there is no need to have multiple jython locations.

The file structure looks like the following:
  Home
    JMRI (this git repository)
      Decoder_TestTrack (Profile directory, not expanded here)
      Mike_Basement_Layout (Profile directory, expanded here to illustrate)
        profile
        programmers
        signal
        throttle
      Programming_Track (Profile directory, not expanded here)
      roster (folder)
      roster.xml
      roster.xml.bak
      jython (directory of scripts)
