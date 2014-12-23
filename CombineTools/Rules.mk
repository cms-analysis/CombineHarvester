SUBDIRS 	:=
LIB_DEPS 	:=
LIB_EXTRA := -lboost_python -L$(shell scramv1 tool tag python LIBDIR) -l$(shell scramv1 tool tag python LIB) -lPyROOT
