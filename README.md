# ABOUT #

The premise of this project is to examine the C functions used by web browsers and see what information can be extrapolated from them. Variations on this concept include running based on limited information (small windows of functions).

This repo contains the standard program that reads an entire strace file as well as the program that reads small chunks of strace files and determines which site they're generated from.

#Requirements#
- SciPy
- NumPy
- Scikit-learn


#Project Notes#

sites:

- info.cern.ch/hypertext/WWW/TheProject.html
- www.google.com
- en.wikipedia.org/wiki/South_African_labour_law
- www.reddit.com
- www.yahoo.com
- www.youtube.com/watch?v=dQw4w9WgXcQ
- www.cs.unm.edu/~forrest/publications/acsac08.pdf
- www.nyu.edu
- www.wfu.edu
- www.soundcloud.com/flume/lorde-tennis-court-flume-remix

Command to use:

```strace -o ./[etc.] wget -e robots=off --wait 1 --page-requisites [link]```

Soundcloud test links (streaming site example):
 - https://soundcloud.com/flume/lorde-tennis-court-flume-remix
 - https://soundcloud.com/favelamusic/easy-yoke
 - https://soundcloud.com/starslingeruk/h-town-they-like-it-slow-star

CERN test links (lightweight site example):
 - http://info.cern.ch/hypertext/WWW/TheProject.html
 - http://info.cern.ch/hypertext/WWW/Help.html
 - http://info.cern.ch/hypertext/WWW/Technical.html


//TODO:

group websites into categories, i.e. university sites, streaming sites,
news sites, wikipedia pages (lists vs articles), etc.

can it differentiate between website types?

Search site terms:
 - homepage
 - wake forest
 - nyu
 - linux
 - computer science

University sites:
 - wfu.edu
 - nyu.edu
 - duke.edu
 - unc.edu
 - utexas.edu
 - berkeley.edu
 - usc.edu
 - ucla.edu
 - cornell.edu
 - uchicago.edu

Valgrind on server:
 - run strace on valgrind runs
 - see if you can see the difference 
   between high and low memory usage
