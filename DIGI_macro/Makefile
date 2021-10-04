
CC=g++

LD=$(CC)

CPPFLAGS= -Wall -g -O2

# Library definition
LIBS=

ROOTCFLAGS   = $(shell root-config --cflags)
ROOTLIBS     = $(shell root-config --libs)
ROOTGLIBS    = $(shell root-config --glibs)

SOFLAGS       = -shared

CPPFLAGS     += $(ROOTCFLAGS)
LIBS         += $(ROOTLIBS) 
GLIBS         = $(ROOTGLIBS)
# -lfftw3
SRCS = ana_compass.C
OBJS = $(SRCS:%.C=%.o)

all:	ana_compass

clean:	
	/bin/rm -f $(OBJS) $(EXE)
	/bin/rm -f *.o
.SUFFIXES: .o .c .cpp .cc .cxx .C

.C.o:   $(OBJS) $(RLIB)
	$(CC) -c $(CPPFLAGS) $<

ana_compass: $(OBJS) $(RLIB)
	 $(CC) -o ana_compass $(OBJS) $(QTINCLUDE) $(LIBS) $(QTLIBS) 

dep depend:
	$(CC) -E $(CPPFLAGS)  $(QTINCLUDE) -M $(SRCS) $(QTLIBS) ana_compass.C > .depend

ifeq (.depend,$(wildcard .depend))
include .depend
endif
