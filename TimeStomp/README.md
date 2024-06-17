# TimeStomp_bof
This is a very simple BOF that can be used with Cobalt Strike and other post exploitation frameworks that I reimplemented from one of my C++ tools. This BOF timestomps a target file to have the time attributes that match those of a source file on the same Windows system.

## Purpose
While Cobalt Strike includes a native timestomp functionality, this was just an endeavor to continue learning about BOF development, C vs. C++ code integrations for those capabilities, and to make a publicly available timestomp BOF since other frameworks often don't natively include that capability but do support BOFs.

## Usage
timestomp-bof 'target-file' 'source-file'

## Compiling
The Makefile includes the Mingw command for compiling the BOF and can be executed by running 'make' from within the src directory.

## Disclaimer
I made an honest attempt to include explicit error handling in this code but as with every thing you find on the internet, proper testing with your framework and to ensure this meets your use case is highly recommended prior to using this on any live assessments. This code is provided as is with no guarantees and is intended to only be used on authorized systems where you have approval to perform testing and/or research. 
