ARCH = x86
TARGET = sandnix
AS = gcc
ASFLAGS = -m32 -c  -DAAA=1 -DCHK1 -DCHK2 
ASRULE = $(AS) $(ASFLAGS) -o $@ $<
CC = gcc
CFLAGS = -c  -DAAA=1 -DCHK1 -DCHK2 
CCRULE = $(CC) $(CFLAGS) -o $@ $<
LD = gcc
LDFLAGS = 
LDRULE = $(LD) -o $@ $^
DEP = gcc
DEPRULE = $(DEP) -MM -o $@ $<;echo $(OBJDIR)/$(ARCH)/`cat $@` > $@
AFTER = 
OBJDIR = ../../obj
OUTPUT = ../../bin/$(ARCH)/$(TARGET)
sinclude $(OBJDIR)/$(ARCH)/a.dep
$(OBJDIR)/$(ARCH)/a.dep : a.c
	mkdir -p $(dir $@)
	$(DEPRULE)
$(OBJDIR)/$(ARCH)/a.o : a.c
	$(CCRULE)
sinclude $(OBJDIR)/$(ARCH)/b/b.dep
$(OBJDIR)/$(ARCH)/b/b.dep : b/b.c
	mkdir -p $(dir $@)
	$(DEPRULE)
$(OBJDIR)/$(ARCH)/b/b.o : b/b.c
	$(CCRULE)
sinclude $(OBJDIR)/$(ARCH)/c/cx86.dep
$(OBJDIR)/$(ARCH)/c/cx86.dep : c/cx86.c
	mkdir -p $(dir $@)
	$(DEPRULE)
$(OBJDIR)/$(ARCH)/c/cx86.o : c/cx86.c
	$(CCRULE)
$(OUTPUT) : $(OBJDIR)/$(ARCH)/a.o $(OBJDIR)/$(ARCH)/b/b.o $(OBJDIR)/$(ARCH)/c/cx86.o 
	mkdir -p $(dir $(OUTPUT))
	$(LDRULE)
.PHONY : $(TARGET) all clean delete rebuild
all : $(TARGET)
$(TARGET) : $(OUTPUT)
	$(AFTER)
	rm -f  $(OBJDIR)/$(ARCH)/a.dep $(OBJDIR)/$(ARCH)/b/b.dep $(OBJDIR)/$(ARCH)/c/cx86.dep
clean :
	rm -r $(OBJDIR)/$(ARCH)
delete :
	rm -rf $(OBJDIR)/$(ARCH)
	rm -rf $(OUTPUT)
rebuild :
	make delete
	make all
