# For the reference here are some automatic variables defined by make.
# There are also their D/F variants e.g. $(<D) - check the manual.
#
# $@ - file name of the target of the rule
# $% - target member name when the target is archive member
# $< - the name of the first dependency
# $? - the names of all dependencies that are newer then the target
# $^ - the names of all dependencies

define include_subdir_rules
dir_stack := $(d) $(dir_stack)
d := $(d)/$(1)
$$(eval $$(value HEADER))
include $(addsuffix /Rules.mk,$$(d))
$$(eval $$(value FOOTER))
d := $$(firstword $$(dir_stack))
dir_stack := $$(wordlist 2,$$(words $$(dir_stack)),$$(dir_stack))
endef
