#================================================================
# A Makefile for the java_cup package
# and subpackages.
#
# Author: Scott Sanner
# $Revision: 1.1 $
#================================================================

# environment settings:
JAVAC   = javac -classpath ..
JAVADOC = javadoc
JAVA    = java

# project specifics:
CLASSES      = Main.class lalr_item_set.class parse_action.class production_part.class  terminal.class \
	action_part.class lalr_state.class parse_action_row.class reduce_action.class    terminal_set.class \
	action_production.class lalr_transition.class parse_action_table.class shift_action.class version.class \
	assoc.class lexer.class parse_reduce_row.class sym.class \
	emit.class lr_item_core.class parse_reduce_table.class symbol.class \
	internal_error.class non_terminal.class parser.class symbol_part.class \
	lalr_item.class nonassoc_action.class production.class symbol_set.class


#
# list of subpackages:
PACKAGES     =

# Explain to make how compiling Java code works...
.SUFFIXES :     .class .java
.java.class :
	$(JAVAC) $<

# some other useful macros we can derive...
SRCS = $(CLASSES:.class=.java)
DOCS = $(CLASSES:.class=.html)

# Typical make targets:
all: $(CLASSES) $(PACKAGES)

clean:
	-rm ./*.class ./*~ ./*/*.class ./*/*~ ./*/*/*.class ./*/*/*~

# Packages:
docs: ALWAYS_BUILD
	-mkdir javadoc; \
	$(JAVADOC) -author -d javadoc $(ALL_PACKAGES)

# This is a dummy target that can be used to ensure that a target's
# dependencies are never satisfied.  This is useful because by default, make
# treats the presence of a directory with the same name as the target as an
# up-to-date target.
ALWAYS_BUILD:
