define FOOTER

##############################################################
# First define all the directory-specific variables we need #
#############################################################

# Build list of all lib directories so we can add it to $PYTHONPATH
TESTDIR := $(wildcard $(d)/lib)
ifneq ($(TESTDIR),)
ifeq ($(ALL_LIB_DIRS),)
ALL_LIB_DIRS := $(d)/lib
else
ALL_LIB_DIRS := $(ALL_LIB_DIRS):$(d)/lib
endif
endif

# Get list of sub-directories defined in Rules.mk, and add the full path
# as a prefix
SUBDIRS_$(d) := $(patsubst %/,%,$(addprefix $(d)/,$(SUBDIRS)))
ifdef DEBUG
$(info Scanning directory: $(d))
$(foreach x,$(SUBDIRS_$(d)),$(info -- Adding sub-directory: $(x)))
endif

# Get list of object files to construct by looking for files matching src/*.cc
# "wildcard" gets the files in src, "notdir" removes the directory part, "basename"
# removes the extension, "addprefix" adds the full path to the obj directory and finally
# "addsuffix" adds the .o extension
OBJS_$(d) := $(addsuffix .o, $(addprefix $(d)/obj/,$(basename $(notdir $(wildcard $(d)/$(SRC_DIR)/*.$(SRC_EXT))))))
ifdef DEBUG
$(info Target object files:)
$(foreach x,$(OBJS_$(d)),$(info -- Target file: $(x)))
endif

# If DICTIONARY has been specified, define DHEADERS_$(d) and DOBJ_$(d)
ifneq ($(DICTIONARY),)
DHEADERS_$(d) := $(addprefix $(d)/,$(DICTIONARY))
OBJS_$(d) += $(d)/obj/rootcint_dict.o
endif
ifdef DEBUG
$(info Target dictionary header files:)
$(foreach x,$(DHEADERS_$(d)),$(info -- Header file: $(x)))
endif

# Get list of exectutables to compile by looking for files matching test/*.cpp
# "wildcard" gets the files in test, "notdir" removes the directory part, "basename"
# removes the extension and "addprefix" adds the full path to the bin directory
EXES_$(d) := $(addprefix $(d)/bin/,$(basename $(notdir $(wildcard $(d)/test/*.cpp))))
ifdef DEBUG
$(info Target programs:)
$(foreach x,$(EXES_$(d)),$(info -- Target file: $(x)))
endif

# Get list of object files to compile by looking for files matching test/*.cpp
# "wildcard" gets the files in test, "notdir" removes the directory part, "basename"
# removes the extension, "addprefix" adds the full path to the bin directory and finally
# "addsuffix" adds the .o extension
EXE_OBJS_$(d) := $(addsuffix .o, $(addprefix $(d)/bin/,$(basename $(notdir $(wildcard $(d)/test/*.cpp)))))

ifdef DEBUG
$(info Determine library name...)
endif
ifeq ($(d),$(TOP))
# Special case if we're in the top directory: the shared library will be named
# after the enclosing folder, which we can simply extract using the notdir command
LIBNAME_$(d) := $(notdir $(d))
else
# Shared library will be named after the enclosing folders, up to but not including
# the top directory. e.g. if we're in dir1/dir2 then the library name will be formed
# from dir1_dir2. The command below removes the top directory string from the current
# directory and any leading '/' character, then substitutes '_' for any remaining '/'
LIBNAME_$(d) := $(subst /,_,$(patsubst /%,%,$(subst $(TOP),,$(d))))
endif

# Now define the full library target, but only in the case that we actually have
# some object files to link. The full library target adds a libCH prefix to reduce
# the chance of a naming clash with other linked libraries (eg. libCore in ROOT)
ifneq ($(OBJS_$(d)),)
 LIB_$(d) := $(addsuffix .so,$(addprefix $(d)/lib/libCH,$(LIBNAME_$(d))))
 ifdef DEBUG
  $(info -- Library: $(LIB_$(d)))
 endif
else
 ifdef DEBUG
  $(info -- No source files, library will not be generated!)
 endif
endif


# Only if the directory we're scanning is the directory the user is running from
# we define shortcut targets for compiling executables. This means the user can
# do 'make bin/MyProg' instead of having to do 'make /full/path/to/bin/MyProg'
ifeq ($(d),$(RUNDIR))
 SHORT_EXES := $(addprefix bin/,$(basename $(notdir $(wildcard $(d)/test/*.cpp))))
endif

# Setup the other libraries in the framework that this one depends on,
# using the user-supplied list in the Rules.mk file.
LIB_DEPS_$(d) := $(foreach x,$(LIB_DEPS),$(TOP)/$(x)/lib/libCH$(subst /,_,$(x)).so)

# Add LIB_EXTRA, defined in Rules.mk for other external libraries to link
# against in this directory
$(foreach x,$(EXES_$(d)),$(eval EXE_DEP_$(x) := $(LIB_EXTRA)))
$(foreach x,$(LIB_$(d)),$(eval LIB_DEP_$(x) := $(LIB_EXTRA)))
$(foreach x,$(OBJS_$(d)),$(eval FLAGS_$(x) := $(PKG_FLAGS)))

SKIP := 0
ifeq ($(CMSSW), 0)
  ifneq ($(REQUIRES_CMSSW), 0)
    # $(info Warning: directory '$(notdir $(d))' which requires CMSSW is skipped)
    SKIP := 1
  endif
endif

#######################################################################
# Only define rules for this folder is SKIP = 0 											#
#######################################################################
ifeq ($(SKIP), 0)

###################################
# Define directory-specific Rules #
###################################
# Targets for a directory are the shared library and the executables
TARGETS_$(d) := $(LIB_$(d)) $(EXES_$(d))

# Check if verbose mode is enabled, and if so we will echo commands
ifdef V
 DOECHO=
else
 DOECHO=@
endif

# If they exist (-include instead of include), load automatic rules in the
# .d files
-include $(OBJS_$(d):.o=.d)
-include $(d)/obj/rootcint_dict.d
-include $(EXE_OBJS_$(d):.o=.d)

# Rule for generating object files from source files
$(d)/obj/%.o: $(d)/$(SRC_DIR)/%.$(SRC_EXT)
	@echo -e "$(COLOR_BL)Compiling object file $(subst $(TOP)/,,$@)$(NOCOLOR)"
	$(DOECHO)$(CXX) $(CXXFLAGS) $(FLAGS_$(@)) -fPIC -c $< -o $@
	@echo -e "$(COLOR_CY)Generating dependency file $(subst $(TOP)/,,$(@:.o=.d))$(NOCOLOR)"
	@$(CXX) $(CXXFLAGS) -MM -MP -MT "$@" $< -o $(@:.o=.d)

# Rule for generating dictionary object
$(d)/obj/rootcint_dict.o: $(d)/obj/rootcint_dict.cc
	@echo -e "$(COLOR_YE)Compiling dictionary object file $(subst $(TOP)/,,$@)$(NOCOLOR)"
	$(DOECHO)$(CXX) $(CXXFLAGS) -fPIC -c $< -o $@
	@echo -e "$(COLOR_CY)Generating dependency file $(subst $(TOP)/,,$(@:.o=.d))$(NOCOLOR)"
	@$(CXX) $(CXXFLAGS) -MM -MP -MT "$@" $< -o $(@:.o=.d)

$(d)/obj/rootcint_dict.cc: $(DHEADERS_$(d)) $(d)/$(INC_DIR)/LinkDef.h
	@echo -e "$(COLOR_YE)Generating dictionary $(subst $(TOP)/,,$@)$(NOCOLOR)"
	$(DOECHO)$(ROOTSYS)/bin/rootcint -v3 -f $@ -c -p -I$(TOP) -I$(TOP)/../../.. -I$(ROOFITSYS)/include $^

# Rule for generating object files for executables from source files
$(d)/bin/%.o: $(d)/test/%.cpp
	@echo -e "$(COLOR_BL)Compiling object file $(subst $(TOP)/,,$@)$(NOCOLOR)"
	$(DOECHO)$(CXX) $(CXXFLAGS) -fPIC -c $<  -o $@
	@echo -e "$(COLOR_CY)Generating dependency file $(subst $(TOP)/,,$(@:.o=.d))$(NOCOLOR)"
	$(DOECHO)$(CXX) $(CXXFLAGS) -MM -MP -MT "$@" $< -o $(@:.o=.d)

# Rule for generating shared library
$(LIB_$(d)) : $(OBJS_$(d)) $(LIB_DEPS_$(d))
	@echo -e "$(COLOR_PU)Creating shared library $(subst $(TOP)/,,$@)$(NOCOLOR)"
	$(DOECHO)$(LD) $(LDFLAGS) -o $@ $^ $(LIBS) $(LIB_DEP_$(@))

# Shortcut rules for building an executable, if this is the run directory
# NB: don't remove the echo statement here or make will optimise-out this
# dependency
ifeq ($(d),$(RUNDIR))
bin/%: $(d)/bin/%
	@echo -e "==> $(COLOR_GR)Single executable '$@' updated$(NOCOLOR)"
endif

# Rules for making and linking the executables
$(d)/bin/%: $(d)/bin/%.o $(LIB_$(d)) $(LIB_DEPS_$(d))
	@echo -e "$(COLOR_PU)Linking executable $(subst $(TOP)/,,$@)$(NOCOLOR)"
	$(DOECHO)$(CXX) -o $@  $^ $(LIBS) $(EXE_DEP_$@)

########################################################################
# End of SKIP=0 section																								 #
########################################################################
endif

dir_$(d) : $(TARGETS_$(d))

# Defining the exe object files to .SECONDARY stops make from automatically
# deleting them
.SECONDARY: $(EXE_OBJS_$(d))

########################################################################
# Inclusion of subdirectories rules - only after this line one can     #
# refer to subdirectory targets and so on.                             #
########################################################################
$(foreach sd,$(SUBDIRS),$(eval $(call include_subdir_rules,$(sd))))

.PHONY: dir_$(d) clean_$(d) clean_tree_$(d)

# Whole tree targets
all_proxy :: $(TARGETS_$(d))

clean_all :: clean_$(d)

########################################################################
#                        Per directory targets                         #
########################################################################

clean_$(d) :
	rm -f $(subst clean_,,$@)/bin/* $(subst clean_,,$@)/obj/*.o $(subst clean_,,$@)/obj/*.d $(subst clean_,,$@)/lib/*.so

clean_tree_$(d) : clean_$(d) $(foreach sd,$(SUBDIRS_$(d)),clean_tree_$(sd))

tree_$(d) : $(TARGETS_$(d)) $(foreach sd,$(SUBDIRS_$(d)),tree_$(sd))

endef
