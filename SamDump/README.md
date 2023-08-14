# About
Beacon Object File(BOF) for CobaltStrike that will acquire the necessary privileges and dump SAM - SYSTEM - SECURITY registry keys for offline parsing and hash extraction.

## Instructions

CNA will register the command `bof-regsave`:

```
beacon> bof-regsave c:\temp\
```

By default the output will be saved in the following files:

```
samantha.txt - SAM
systemic.txt - SYSTEM
security.txt - SECURITY
```

You can modify the file names by changing `entry.c`.

## Credits

Template & Makefile based on repo from [@realoriginal](https://github.com/realoriginal/beacon-object-file)


## Reading material for BOF

[CS Beacon Object Files](https://www.cobaltstrike.com/help-beacon-object-files)

[Aggressor-Script functions](https://www.cobaltstrike.com/aggressor-script/functions.html)

[Beacon Object Files - Luser Demo](https://www.youtube.com/watch?v=gfYswA_Ronw)

[A Developer's Introduction To Beacon Object Files](https://www.trustedsec.com/blog/a-developers-introduction-to-beacon-object-files/)

_Github repos_

```
https://github.com/rsmudge/ZeroLogon-BOF
https://github.com/rsmudge/CVE-2020-0796-BOF
https://github.com/trustedsec/CS-Situational-Awareness-BOF
https://github.com/tomcarver16/BOF-DLL-Inject
https://github.com/m57/cobaltstrike_bofs/
https://github.com/rvrsh3ll/BOF_Collection/
https://github.com/realoriginal/bof-NetworkServiceEscalate
```

## Author
[@leftp](https://github.com/leftp)
