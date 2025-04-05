
This project ports various translations of the Infinity series to the PSP.

As of now, the repository contains English translations of Never7, Ever17, and Remember11, and a Chinese translation of Remember11.
A Russian translation of Ever17 is planned.

### Useful Links

[**Patch Downloads**](https://github.com/bibarub/Infinity-PSP-English/releases)

Credits for the English translation of Remember11 go to [TLWiki team](http://web.archive.org/web/20180819171103/https://tlwiki.org/?title=Remember11_-_the_age_of_infinity) (now defunct)

...

Current status
-----------

Scenes: Translated  
Append stories (N7): Okuhiko Cure and Yuka Cure are translated. Other append stories have speaker names replaced in them.  
Backgrounds/CGs (E17): Translated  
Shortcuts (init.bin): Translated  
TIPS (init.bin): Translated. Ever17 tips translation is ongoing.  
Names (init.bin): Translated  
Chronology (R11) (init.bin): Not translated in English. Translated in Chinese.  
Menus (BOOT.BIN): Translated. Help messages for the settings are not translated.  
Font (FONT00.FOP): Tweaked for English text, reduced spacing. EN glyphs are brightened and sharpened. Japanese quotation marks for speech are replaced with typographical quotes.


For Developers
-----------

This project is a bunch of scripts and programs in bash, python and C. Python and C programs unpack and repack game resources, decode text, fonts etc. Shell scripts automate the process of applying the translation. They should should work both on macos and linux.

For the full run:

1. Put your ISO at `iso/Never7-jap.iso`, `iso/Ever17-jap.iso`, or `iso/Remember11-jap.iso`

2. Set the `GAME` environment variable to `n7`, `e17`, or `r11`, depending on the game you are patching. Example: `export GAME=e17`

3. Run `./make.sh`

4. The resulting iso will be in the `iso` folder.

`./generate-patches.sh` can be used to generate xdelta3 diff files.

`./generate-eboot-pbp.sh` can generate a EBOOT.PBP file that runs on OFW.

For further details, read the contents of shell scripts (and other source files).

##### Dependencies:

The following tools should be available in your PATH:

`7z mkisofs gcc python3 xdelta3`

- `mkisofs` is a part of the `cdrtools` package.

- Brew command for macos to install dependencies: `brew install p7zip cdrtools python3 xdelta`.

- Last tested to be working with python 3.12, will likely work with later versions as well.
