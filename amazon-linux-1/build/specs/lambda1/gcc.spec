%define _buildid .59

# BEGIN of Amazon Linux AMI Settings

# Build a main compiler package, not an alternatives option by commenting out gccv definition
%global gccv 72

# for the alternatives setup
%if 0%{?gccv:1}
%global gcc_prio 721
%endif

%global libstdcplusplus_ver 6.0.24
%global libquadmath_ver 0.0.0
%global libitm_ver 1.0.0
%global libgo_ver 5.0.0

# triggers and obsoletes for these old versions to ensure upgradeability
%global hard_obsolete_ver 4.6.2-2

# define for obsoleting the old gcc builds
#global obsolete_gcc 1

# END OF Amazon Linux AMI Settings

%global DATE 20170915
%global SVNREV 252800
%global gcc_version 7.2.1
%global gcc_major 7

# Note, gcc_release must be integer, if you want to add suffixes to
# %{release}, append them after %{gcc_release} on Release: line.
%global gcc_release 2

%global _unpackaged_files_terminate_build 1

%global build_multilib 0

%global build_ada 1
%global build_go 1
%global build_libquadmath 1

%global build_libsanitizer 1

%global build_libcilkrts 1
%global build_libatomic 1
%global build_libitm 1
%global build_libmpx 1
%global build_isl 0
%global build_libstdcxx_docs 0
%global attr_ifunc 1

%global build_libgomp 1

%global build_libgccjit 1

%global _skip_check 0


# Amazon compiler build options
%if 0%{?amzn:1}
%global _skip_check 1
%global _build_minimal 1
%endif


# A minimal compiler package definition
%if 0%{?_build_minimal}
# do not build golang
%global build_go 0
# no support for objc by unpopular non-demand
%global build_objc 0
# no support for Ada
%global build_ada 0
# do not enable fortran support
%global build_fortran 0
%global build_libquadmath 0
# no docs
%global build_libstdcxx_docs 0
# no multilib support
%global build_multilib 0
# no libgccjit
%global build_libgccjit 0
# minimal compiler... keep additional libs to a minimum
%global build_libitm 0
%global build_libmpx 0
%global build_libatomic 0
%global build_libsanitizer 0
%global build_libcilkrts 0
%global build_libgomp 0
%endif # build_minimal

Summary: Various compilers (C, C++, Objective-C, Java, ...)
Name: gcc%{?gccv}
Version: %{gcc_version}
Release: %{gcc_release}%{?_buildid}%{?dist}
%if 0%{?gccv:1}
Provides: gcc = %{version}-%{release}
%{?obsolete_gcc:Obsoletes: gcc < %{version}-%{release}}
%endif
# libgcc, libgfortran, libgomp, libstdc++ and crtstuff have
# GCC Runtime Exception.
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
Group: Development/Languages
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# svn export svn://gcc.gnu.org/svn/gcc/branches/redhat/gcc-6-branch@%{SVNREV} gcc-%{version}-%{DATE}
# tar cf - gcc-%{version}-%{DATE} | bzip2 -9 > gcc-%{version}-%{DATE}.tar.bz2
Source0: gcc-%{version}-%{DATE}.tar.bz2
%global isl_version 0.16.1
URL: http://gcc.gnu.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Need binutils with -pie support >= 2.14.90.0.4-4
# Need binutils which can omit dot symbols and overlap .opd on ppc64 >= 2.15.91.0.2-4
# Need binutils which handle -msecure-plt on ppc >= 2.16.91.0.2-2
# Need binutils which support .weakref >= 2.16.91.0.3-1
# Need binutils which support --hash-style=gnu >= 2.17.50.0.2-7
# Need binutils which support mffgpr and mftgpr >= 2.17.50.0.2-8
# Need binutils which support --build-id >= 2.17.50.0.17-3
# Need binutils which support %gnu_unique_object >= 2.19.51.0.14
# Need binutils which support .cfi_sections >= 2.19.51.0.14-33
# Need binutils which support --no-add-needed >= 2.20.51.0.2-12
# Need binutils which support -plugin
BuildRequires: binutils >= 2.20.51.0.2-12
# While gcc doesn't include statically linked binaries, during testing
# -static is used several times.
BuildRequires: glibc-static
BuildRequires: zlib-devel, gettext, dejagnu, bison, flex, sharutils
BuildRequires: texinfo, texinfo-tex, /usr/bin/pod2man
BuildRequires: systemtap-sdt-devel >= 1.3
BuildRequires: gmp-devel >= 4.1.2-8, mpfr-devel >= 2.2.1, libmpc-devel >= 0.8.1
BuildRequires: automake >= 1.11
BuildRequires: system-python-devel
# Needed for dwarf4 support, otherwise the debuginfo packages are useless
BuildRequires: rpm-build >= 4.8.0-32
%if %{build_go}
BuildRequires: /bin/hostname, procps
%endif
# For VTA guality testing
BuildRequires: gdb
# Make sure pthread.h doesn't contain __thread tokens
# Make sure glibc supports stack protector
# Make sure glibc supports DT_GNU_HASH
BuildRequires: glibc-devel >= 2.4.90-13
BuildRequires: elfutils-devel >= 0.147
BuildRequires: elfutils-libelf-devel >= 0.147
%if %{build_multilib}
%endif #multilib
%if %{build_ada}
# Ada requires Ada to build
BuildRequires: gcc-gnat >= 3.1, libgnat >= 3.1
%endif
%if %{build_isl}
BuildRequires: isl = %{isl_version}
BuildRequires: isl-devel = %{isl_version}
%if 0%{?__isa_bits} == 64
Requires: libisl.so.15()(64bit)
%else
Requires: libisl.so.15
%endif
%endif
%if %{build_libstdcxx_docs}
BuildRequires: doxygen >= 1.7.1
BuildRequires: graphviz, texlive-latex, docbook5-style-xsl
%endif
# these are required to make this compiler functional
Requires: cpp%{?gccv}%{?_isa} >= %{version}
Requires: libgcc%{?gccv}%{?_isa} >= %{version}
# Need .eh_frame ld optimizations
# Need proper visibility support
# Need -pie support
# Need --as-needed/--no-as-needed support
# On ppc64, need omit dot symbols support and --non-overlapping-opd
# Need binutils that owns /usr/bin/c++filt
# Need binutils that support .weakref
# Need binutils that supports --hash-style=gnu
# Need binutils that support mffgpr/mftgpr
# Need binutils that support --build-id
# Need binutils that support %gnu_unique_object
# Need binutils that support .cfi_sections
# Need binutils that support --no-add-needed
# Need binutils that support -plugin
Requires: binutils >= 2.20.51.0.2-12
# Make sure gdb will understand DW_FORM_strp
Conflicts: gdb < 5.1-2
Requires: glibc-devel%{?_isa} >= 2.2.90-12
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7 || 0%{?amzn}
%ifarch %{arm}
Requires: glibc >= 2.16
%endif
%endif
%if 0%{?gccv:1}
Requires: libgcc%{?_isa} >= %{version}
%if %{build_libgomp}
Requires: libgomp%{?_isa} >= %{version}
%endif #libgomp
%endif
#%if !%{build_ada}
#Obsoletes: gcc-gnat < %{version}-%{release}
#%endif
AutoReq: true
Provides: bundled(libiberty)

Provides: gcc(major) = %{gcc_major}

Patch0: gcc7-hack.patch
Patch1: gcc7-ppc32-retaddr.patch
Patch2: gcc7-i386-libgomp.patch
Patch3: gcc7-sparc-config-detection.patch
Patch4: gcc7-libgomp-omp_h-multilib.patch
Patch5: gcc7-libtool-no-rpath.patch
Patch6: gcc7-isl-dl.patch
Patch7: gcc7-libstdc++-docs.patch
Patch8: gcc7-no-add-needed.patch
Patch9: gcc7-aarch64-async-unw-tables.patch
Patch10: gcc7-foffload-default.patch
Patch11: gcc7-Wno-format-security.patch
Patch12: gcc7-pr81314.patch
Patch13: gcc7-pr81325.patch
Patch14: gcc7-pr82112-1.patch
Patch15: gcc7-pr82112-2.patch
Patch16: gcc7-pr81929.patch

#retpoline patches
Patch1001: 0001-i386-Move-struct-ix86_frame-to-machine_function.patch
Patch1002: 0002-i386-Use-reference-of-struct-ix86_frame-to-avoid-cop.patch
Patch1003: 0003-i386-More-use-reference-of-struct-ix86_frame-to-avoi.patch
Patch1004: 0004-x86-Add-mindirect-branch.patch
Patch1005: 0005-x86-Add-mindirect-branch-loop.patch
Patch1006: 0006-x86-Add-mfunction-return.patch
Patch1007: 0007-x86-Add-mindirect-branch-register.patch
Patch1008: 0008-x86-Add-V-register-operand-modifier.patch

# On ARM EABI systems, we do want -gnueabi to be part of the
# target triple.
%ifnarch %{arm}
%global _gnu %{nil}
%else
%global _gnu -gnueabi
%endif
%global gcc_target_platform %{_target_platform}

Obsoletes: libmudflap-devel
Obsoletes: libmudflap44-devel
Obsoletes: libmudflap46-devel
Obsoletes: libmudflap48-devel
Obsoletes: libmudflap-static
Obsoletes: libmudflap44-static
Obsoletes: libmudflap46-static
Obsoletes: libmudflap48-static

# Main package now inclues static libraries for which we used to have
# versioned subpackages
Obsoletes: libatomic%{?gccv}-static
%if %{build_libatomic}
Provides: libatomic%{?gccv}-static = %{version}-%{release}
%if 0%{?gccv:1}
Provides: libatomic-static = %{version}-%{release}
%endif
%endif
Obsoletes: libitm%{?gccv}-static
Obsoletes: libitm%{?gccv}-devel
%if %{build_libitm}
Provides: libitm%{?gccv}-static = %{version}-%{release}
Provides: libitm%{?gccv}-devel = %{version}-%{release}
%endif
Obsoletes: libquadmath%{?gccv}-devel
Obsoletes: libquadmath%{?gccv}-static
%if %{build_libquadmath}
Provides: libquadmath%{?gccv}-devel = %{version}-%{release}
Provides: libquadmath%{?gccv}-static = %{version}-%{release}
%endif
Obsoletes: libgcj-devel < %{version}-%{release}
Obsoletes: libgcj-src < %{version}-%{release}

Prefix: %{_prefix}

%description
The gcc package contains the GNU Compiler Collection version 7.
You'll need this package in order to compile C code.

%package -n libgcc%{?gccv}
Summary: GCC version 7 shared support library
Group: System Environment/Libraries
%if 0%{?gccv:1}
Provides: libgcc = %{version}-%{release}
%{?obsolete_gcc:Obsoletes: libgcc < %{version}-%{release}}
#Obsoletes: libgcc < %{hard_obsolete_ver}
Provides: libgcc%{?_isa} = %{version}-%{release}
%endif
#%if !%{build_ada}
#Obsoletes: libgnat < %{version}-%{release}
#%endif
#Obsoletes: libmudflap
Obsoletes: libgcj < %{version}-%{release}

Prefix: %{_prefix}

%description -n libgcc%{?gccv}
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package c++
Summary: C++ support for GCC
Group: Development/Languages
Requires: gcc%{?gccv}%{?_isa} >= %{version}
Requires: libstdc++%{?gccv}%{?_isa} >= %{version}
Autoreq: true
%if 0%{?gccv:1}
Provides: gcc-c++ = %{version}-%{release}
%{?obsolete_gcc:Obsoletes: gcc-c++ < %{version}-%{release}}
%endif
Obsoletes: libstdc++%{?gccv}-devel
Obsoletes: libstdc++%{?gccv}-static
Provides: libstdc++%{?gccv}-devel = %{version}-%{release}
Provides: libstdc++%{?gccv}-static = %{version}-%{release}
%if 0%{?gccv:1}
%{?obsolete_gcc:Obsoletes: libstdc++-devel < %{version}-%{release}}
%{?obsolete_gcc:Obsoletes: libstdc++-static < %{version}-%{release}}
Provides: libstdc++-devel = %{version}-%{release}
Provides: libstdc++-devel%{?_isa} = %{version}-%{release}
Provides: libstdc++-static = %{version}-%{release}
Provides: libstdc++-static%{?_isa} = %{version}-%{release}
%endif

Prefix: %{_prefix}

%description c++
This package adds C++ support to the GNU Compiler Collection.
It includes support for most of the current C++ specification,
including templates and exception handling.

%if %{build_objc}
%package objc
Summary: Objective-C support for GCC
Group: Development/Languages
Requires: gcc%{?gccv}%{?_isa} >= %{version}
Requires: libobjc%{?gccv}%{?_isa} >= %{version}
Autoreq: true
%if 0%{?gccv:1}
Provides: gcc-objc = %{version}-%{release}
%{?obsolete_gcc:Obsoletes: gcc-objc < %{version}-%{release}}
%endif

Prefix: %{_prefix}

%description objc
gcc-objc provides Objective-C support for the GCC.
Mainly used on systems running NeXTSTEP, Objective-C is an
object-oriented derivative of the C language.

%package objc++
Summary: Objective-C++ support for GCC
Group: Development/Languages
Requires: gcc%{?gccv}-c++%{?_isa} >= %{version}
Requires: gcc%{?gccv}-objc%{?_isa} >= %{version}
Autoreq: true
%if 0%{?gccv:1}
Provides: gcc-objc++ = %{version}-%{release}
%{?obsolete_gcc:Obsoletes: gcc-objc++ < %{version}-%{release}}
%endif

Prefix: %{_prefix}

%description objc++
gcc-objc++ package provides Objective-C++ support for the GCC.

%package -n libobjc%{?gccv}
Summary: Objective-C runtime
Group: System Environment/Libraries
Autoreq: true
%if 0%{?gccv:1}
Provides: libobjc = %{version}-%{release}
%{?obsolete_gcc:Obsoletes: libobjc < %{version}-%{release}}
Provides: libobjc%{?_isa} = %{version}-%{release}
%endif

Prefix: %{_prefix}

%description -n libobjc%{?gccv}
This package contains Objective-C shared library which is needed to run
Objective-C dynamically linked programs.

%endif # build_objc

%package gfortran
Summary: Fortran support
Group: Development/Languages
Requires: gcc%{?gccv}%{?_isa} >= %{version}
# rely on automatic rpm dependencies
#Requires: libgfortran >= %{version}-%{release}
Autoreq: true
%if 0%{?gccv:1}
Provides: gcc-gfortran = %{version}-%{release}
%{?obsolete_gcc:Obsoletes: gcc-gfortran < %{version}-%{release}}
%else
Obsoletes: gcc44-gfortran
Obsoletes: gcc48-gfortran
%endif

Prefix: %{_prefix}

%description gfortran
The gcc-gfortran package provides support for compiling Fortran
programs with the GNU Compiler Collection.

%package -n libgfortran
Summary: Fortran runtime
Group: System Environment/Libraries
Autoreq: true
%if %{build_libquadmath}
Requires: %{_prefix}/%{_lib}/libquadmath.so.%{libquadmath_ver}
%endif

Prefix: %{_prefix}

%description -n libgfortran
This package contains Fortran shared library which is needed to run
Fortran dynamically linked programs.

%if %{build_libgomp}
%package -n libgomp
Summary: GCC OpenMP v4.5 shared support library
Group: System Environment/Libraries

Prefix: %{_prefix}

%description -n libgomp
This package contains GCC shared support library which is needed
for OpenMP v4.5 support.
%endif #libgomp

%package gdb-plugin
Summary: GCC plugin for GDB
Group: Development/Debuggers
Requires: gcc >= %{version}

Prefix: %{_prefix}

%description gdb-plugin
This package contains GCC plugin for GDB C expression evaluation.

%if %{build_libgccjit}
%package -n libgccjit
Summary: Library for embedding GCC inside programs and libraries
Group: System Environment/Libraries
Requires: gcc >= %{version}

Prefix: %{_prefix}

%description -n libgccjit
This package contains shared library with GCC JIT front-end.
%endif #build_libgccjit

%package -n libquadmath
Summary: GCC __float128 shared support library
Group: System Environment/Libraries

Prefix: %{_prefix}

%description -n libquadmath
This package contains GCC shared support library which is needed
for __float128 math support and for Fortran REAL*16 support.

%package -n libitm
Summary: The GNU Transactional Memory library
Group: System Environment/Libraries

Prefix: %{_prefix}

%description -n libitm
This package contains the GNU Transactional Memory library
which is a GCC transactional memory support runtime library.

%package -n libatomic
Summary: The GNU Atomic library
Group: System Environment/Libraries

Prefix: %{_prefix}

%description -n libatomic
This package contains the GNU Atomic library which is a GCC support runtime
library for atomic operations not supported by hardware.

%package -n libsanitizer
Summary: Sanitizer runtime library
Group: System Environment/Libraries
Obsoletes: libtsan = 4.8.5
Obsoletes: libtsan = 4.8.3

Prefix: %{_prefix}

%description -n libsanitizer
This package contains sanitizer libraries which are automatically used when
the appropriate -fsanitize option is used for instrumented programs
   -fsanitize=address           will use the Address Sanitizer (libasan)
   -fsanitize=thread            will use the Thread Sanitizer (libtsan)
   -fsanitize=undefined         will use the Undefined Behaviour Sanitizer (libubsan)
   -fsanitize=leak              will use the Leak Sanitizer library (liblsan)

%package -n libcilkrts
Summary: The Cilk+ runtime library
Group: System Environment/Libraries

Prefix: %{_prefix}

%description -n libcilkrts
This package contains the Cilk+ runtime library.

%package -n libmpx
Summary: The Memory Protection Extensions runtime libraries
Group: System Environment/Libraries

Prefix: %{_prefix}

%description -n libmpx
This package contains the Memory Protection Extensions runtime libraries
which is used for -fcheck-pointer-bounds -mmpx instrumented programs.

%package -n cpp%{?gccv}
Summary: The C Preprocessor
Group: Development/Languages
#Requires: filesystem >= 3
Provides: /lib/cpp
Autoreq: true
%if 0%{?gccv:1}
Provides: cpp = %{version}-%{release}
%{?obsolete_gcc:Obsoletes: cpp < %{version}-%{release}}
%endif

Prefix: %{_prefix}

%description -n cpp%{?gccv}
Cpp is the GNU C-Compatible Compiler Preprocessor.
Cpp is a macro processor which is used automatically
by the C compiler to transform your program before actual
compilation. It is called a macro processor because it allows
you to define macros, abbreviations for longer
constructs.

The C preprocessor provides four separate functionalities: the
inclusion of header files (files of declarations that can be
substituted into your program); macro expansion (you can define macros,
and the C preprocessor will replace the macros with their definitions
throughout the program); conditional compilation (using special
preprocessing directives, you can include or exclude parts of the
program according to various conditions); and line control (if you use
a program to combine or rearrange source files into an intermediate
file which is then compiled, you can use line control to inform the
compiler about where each source line originated).

You should install this package if you are a C programmer and you use
macros.

%package gnat
Summary: Ada 83, 95, 2005 and 2012 support for GCC
Group: Development/Languages
Requires: gcc%{?gccv}%{?_isa} >= %{version}
Requires: libgnat%{?gccv}%{?_isa} >= %{version}
Autoreq: true
%if 0%{?gccv:1}
Provides: gcc-gnat = %{version}-%{release}
%{?obsolete_gcc:Obsoletes: gcc-gnat < %{version}-%{release}}
%{?obsolete_gcc:Obsoletes: libgnat-devel < %{version}-%{release}}
%{?obsolete_gcc:Obsoletes: libgnat-static < %{version}-%{release}}
%endif
Obsoletes: libgnat%{?gccv}-devel
Provides: libgnat%{?gccv}-devel = %{version}-%{release}
Obsoletes: libgnat%{?gccv}-static
Provides: libgnat%{?gccv}-static = %{version}-%{release}
%if 0%{?gccv:1}
Provides: libgnat-devel = %{version}-%{release}
Provides: libgnat-devel%{?_isa} = %{version}-%{release}
Provides: libgnat-static = %{version}-%{release}
Provides: libgnat-static%{?_isa} = %{version}-%{release}
%else
Obsoletes: libgnat44-devel
Obsoletes: libgnat44-static
Obsoletes: libgnat48-devel
Obsoletes: libgnat48-static
%endif

Prefix: %{_prefix}

%description gnat
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
development tools, the documents and Ada compiler.

%package -n libgnat%{?gccv}
Summary: GNU Ada 83, 95, 2005 and 2012 runtime shared libraries
Group: System Environment/Libraries
Autoreq: true
%if 0%{?gccv:1}
Provides: libgnat = %{version}-%{release}
%{?obsolete_gcc:Obsoletes: libgnat < %{version}-%{release}}
Provides: libgnat%{?_isa} = %{version}-%{release}
%endif

Prefix: %{_prefix}

%description -n libgnat%{?gccv}
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
shared libraries, which are required to run programs compiled with the GNAT.

%package go
Summary: Go support
Group: Development/Languages
Autoreq: true
%if 0%{?gccv:1}
Provides: gcc-go = %{version}-%{release}
%endif
Requires: gcc%{?gccv}%{?_isa} >= %{version}
Requires: libgo%{?gccv}-devel%{?_isa} >= %{version}
%if 0%{?gccv:1}
Provides: libgo-devel = %{version}-%{release}
Provides: libgo-devel%{?_isa} = %{version}-%{release}
Provides: libgo-static = %{version}-%{release}
Provides: libgo-static%{?_isa} = %{version}-%{release}
%endif
Obsoletes: libgo%{?gccv}-devel
Provides: libgo%{?gccv}-devel = %{version}-%{release}
Obsoletes: libgo%{?gccv}-static
Provides: libgo%{?gccv}-static = %{version}-%{release}

Prefix: %{_prefix}

%description go
The gcc-go package provides support for compiling Go programs
with the GNU Compiler Collection.

%package -n libgo
Summary: Go runtime
Group: System Environment/Libraries
Autoreq: true
%if 0%{?gccv:1}
Provides: libgo = %{version}-%{release}
Provides: libgo%{?_isa} = %{version}-%{release}
%endif

Prefix: %{_prefix}

%description -n libgo
This package contains Go shared library which is needed to run
Go dynamically linked programs.

%prep
%setup -q -n gcc-%{version}-%{DATE}
%patch0 -p0 -b .hack~
%patch1 -p0 -b .ppc32-retaddr~
%patch2 -p0 -b .i386-libgomp~
%patch3 -p0 -b .sparc-config-detection~
%patch4 -p0 -b .libgomp-omp_h-multilib~
%patch5 -p0 -b .libtool-no-rpath~
%if %{build_isl}
%patch6 -p0 -b .isl-dl~
%endif
%if %{build_libstdcxx_docs}
%patch7 -p0 -b .libstdc++-docs~
%endif
%patch8 -p0 -b .no-add-needed~
%patch9 -p0 -b .aarch64-async-unw-tables~
%patch10 -p0 -b .foffload-default~
%patch11 -p0 -b .Wno-format-security~
%patch12 -p0 -b .pr81314~
%patch13 -p0 -b .pr81325~
%patch14 -p0 -b .pr82112-1~
%patch15 -p0 -b .pr82112-2~
%patch16 -p0 -b .pr81929~

#retpoline patches
%patch1001 -p1
%patch1002 -p1
%patch1003 -p1
%patch1004 -p1
%patch1005 -p1
%patch1006 -p1
%patch1007 -p1
%patch1008 -p1

echo 'Red Hat %{version}-%{gcc_release}' > gcc/DEV-PHASE

cp -a libstdc++-v3/config/cpu/i{4,3}86/atomicity.h

./contrib/gcc_update --touch

sed -i -e 's/Common Driver Var(flag_report_bug)/& Init(1)/' gcc/common.opt

# This test causes fork failures, because it spawns way too many threads
rm -f gcc/testsuite/go.test/test/chan/goroutines.go

%build

# Undo the broken autoconf change in recent Fedora versions
export CONFIG_SITE=NONE

CC=gcc
CXX=g++
OPT_FLAGS=`echo %{optflags}|sed -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[12]//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-m64//g;s/-m32//g;s/-m31//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mfpmath=sse/-mfpmath=sse -msse2/g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/ -pipe / /g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-Werror=format-security/-Wformat-security/g'`
%ifarch sparc
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mcpu=ultrasparc/-mtune=ultrasparc/g;s/-mcpu=v[78]//g'`
%endif
%ifarch %{ix86}
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-march=i.86//g'`
%endif
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/[[:blank:]]\+/ /g'`
case "$OPT_FLAGS" in
  *-fasynchronous-unwind-tables*)
    sed -i -e 's/-fno-exceptions /-fno-exceptions -fno-asynchronous-unwind-tables /' \
      libgcc/Makefile.in
    ;;
esac


rm -rf obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

enablelgo=
enablelada=
enablefortran=
enableobjc=
%if %{build_ada}
enablelada=,ada
%endif
%if %{build_go}
enablelgo=,go
%endif
%if %{build_fortran}
enablefortran=,fortran
%endif
%if %{build_objc}
enableobjc=,objc,obj-c++
%endif

CONFIGURE_OPTS="\
	--prefix=%{_prefix} \
	--with-bugurl=http://bugzilla.redhat.com/bugzilla \
	--enable-shared --enable-threads=posix --enable-checking=release \
%if %{build_multilib}
	--enable-multilib \
%else
        --disable-multilib \
%endif
	--with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions \
	--enable-gnu-unique-object --enable-linker-build-id --with-gcc-major-version-only \
	--with-linker-hash-style=gnu \
	--enable-plugin --enable-initfini-array \
%if 0 && 0%{?fedora} >= 21 && 0%{?fedora} <= 22 || 0%{?amzn}
	--with-default-libstdcxx-abi=gcc4-compatible \
%endif
%if %{build_isl}
	--with-isl \
%else
	--without-isl \
%endif
%if %{build_libmpx}
	--enable-libmpx \
%else
	--disable-libmpx \
%endif
%if %{build_libsanitizer}
        --enable-libsanitizer \
%else
        --disable-libsanitizer \
%endif
%if %{attr_ifunc}
	--enable-gnu-indirect-function \
%endif
%ifarch %{arm}
	--disable-sjlj-exceptions \
%endif
%if %{build_libcilkrts}
        --enable-libcilkrts \
%else
        --disable-libcilkrts \
%endif
%if %{build_libatomic}
        --enable-libatomic \
%else
        --disable-libatomic \
%endif
%if %{build_libquadmath}
        --enable-libquadmath \
%else
        --disable-libquadmath --disable-libquadmath-suport \
%endif
%if %{build_libitm}
       --enable-libitm \
%else
       --disable-libitm \
%endif
%if %{build_libgomp}
       --enable-libgomp \
%else
       --disable-libgomp \
%endif
%ifarch %{ix86} x86_64
	--with-tune=generic \
%endif
%if 0%{?rhel} >= 7 || 0%{?amzn}
%ifarch %{ix86}
	--with-arch=x86-64 \
%endif
%ifarch x86_64
	--with-arch_32=x86-64 \
%endif
%else
%ifarch %{ix86}
	--with-arch=i686 \
%endif
%ifarch x86_64
	--with-arch_32=i686 \
%endif
%endif
%ifarch armv7hl
	--with-tune=cortex-a8 --with-arch=armv7-a \
	--with-float=hard --with-fpu=vfpv3-d16 --with-abi=aapcs-linux \
%endif
	--build=%{gcc_target_platform} \
	"

CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
		  | sed 's/ -Wformat-security / -Wformat -Wformat-security /'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	../configure --enable-bootstrap \
	--enable-languages=c,c++${enableobjc}${enablefortran}${enablelada}${enablelgo},lto \
	$CONFIGURE_OPTS

make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" profiledbootstrap

CC="`%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-cc`"
CXX="`%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-cxx` `%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-includes`"

%if %{build_libgccjit}
# Build libgccjit separately, so that normal compiler binaries aren't -fpic
# unnecessarily.
mkdir objlibgccjit
cd objlibgccjit
CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
		  | sed 's/ -Wformat-security / -Wformat -Wformat-security /'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	../../configure --disable-bootstrap --enable-host-shared \
	--enable-languages=jit $CONFIGURE_OPTS
make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" all-gcc
cp -a gcc/libgccjit.so* ../gcc/
cd ../gcc/
ln -sf xgcc %{gcc_target_platform}-gcc-%{gcc_major}
cp -a Makefile{,.orig}
sed -i -e '/^CHECK_TARGETS/s/$/ check-jit/' Makefile
touch -r Makefile.orig Makefile
rm Makefile.orig
cd ..
%endif

cd ..

%install
rm -rf %{buildroot}

cd obj-%{gcc_target_platform}

TARGET_PLATFORM=%{gcc_target_platform}

# There are some MP bugs in libstdc++ Makefiles
make -C %{gcc_target_platform}/libstdc++-v3

make prefix=%{buildroot}%{_prefix} install

mv %{buildroot}%{_prefix}/lib64/* %{buildroot}%{_libdir}/

FULLPATH=%{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
FULLEPATH=%{buildroot}%{_libexecdir}/gcc/%{gcc_target_platform}/%{gcc_major}

# fix some things
# ln -sf gcc %{buildroot}%{_prefix}/bin/cc
# rm -f %{buildroot}%{_prefix}/lib/cpp
# ln -sf ../bin/cpp %{buildroot}/%{_prefix}/lib/cpp
# ln -sf gfortran %{buildroot}%{_prefix}/bin/f95
# gzip -9 %{buildroot}%{_infodir}/*.info*
%if %{build_ada}
# target will be renamed to a gccv-base suffix if needed later on in this spec file
ln -sf gcc%{?gccv} %{buildroot}%{_bindir}/gnatgcc
%endif

%if %{build_go}
mv %{buildroot}%{_bindir}/go{,.gcc}
mv %{buildroot}%{_bindir}/gofmt{,.gcc}
ln -sf /etc/alternatives/go %{buildroot}%{_bindir}/go
ln -sf /etc/alternatives/gofmt %{buildroot}%{_bindir}/gofmt
%endif

cxxconfig="`find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h`"
for i in `find %{gcc_target_platform}/[36]*/libstdc++-v3/include -name c++config.h 2>/dev/null`; do
  if ! diff -up $cxxconfig $i; then
    cat > %{buildroot}%{_includedir}/c++/%{gcc_major}/%{gcc_target_platform}/bits/c++config.h <<EOF
#ifndef _CPP_CPPCONFIG_WRAPPER
#define _CPP_CPPCONFIG_WRAPPER 1
#include <bits/wordsize.h>
#if __WORDSIZE == 32
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
#else
`cat $(find %{gcc_target_platform}/64/libstdc++-v3/include -name c++config.h)`
#endif
#endif
EOF
    break
  fi
done

for f in `find %{buildroot}%{_includedir}/c++/%{gcc_major}/%{gcc_target_platform}/ -name c++config.h`; do
  for i in 1 2 4 8; do
    sed -i -e 's/#define _GLIBCXX_ATOMIC_BUILTINS_'$i' 1/#ifdef __GCC_HAVE_SYNC_COMPARE_AND_SWAP_'$i'\
&\
#endif/' $f
  done
done

# Nuke bits/*.h.gch dirs
# 1) there is no bits/*.h header installed, so when gch file can't be
#    used, compilation fails
# 2) sometimes it is hard to match the exact options used for building
#    libstdc++-v3 or they aren't desirable
# 3) there are multilib issues, conflicts etc. with this
# 4) it is huge
# People can always precompile on their own whatever they want, but
# shipping this for everybody is unnecessary.
rm -rf %{buildroot}%{_includedir}/c++/%{gcc_major}/%{gcc_target_platform}/bits/*.h.gch

FULLLSUBDIR=
if [ -n "$FULLLSUBDIR" ]; then
  FULLLPATH=$FULLPATH/$FULLLSUBDIR
  mkdir -p $FULLLPATH
else
  FULLLPATH=$FULLPATH
fi

find %{buildroot} -name \*.la | xargs rm -f

%if %{build_fortran}
mv %{buildroot}%{_libdir}/libgfortran.spec $FULLPATH/
%endif
%if %{build_libitm}
mv %{buildroot}%{_libdir}/libitm.spec $FULLPATH/
%endif
%if %{build_libsanitizer}
mv %{buildroot}%{_libdir}/libsanitizer.spec $FULLPATH/
%endif
%if %{build_libcilkrts}
mv %{buildroot}%{_libdir}/libcilkrts.spec $FULLPATH/
%endif
%if %{build_libmpx}
mv %{buildroot}%{_libdir}/libmpx.spec $FULLPATH/
%endif

mv -f %{buildroot}%{_libdir}/libgcc_s.so.1 %{buildroot}%{_libdir}/libgcc_s-%{gcc_major}-%{DATE}.so.1
chmod 755 %{buildroot}%{_libdir}/libgcc_s-%{gcc_major}-%{DATE}.so.1
ln -sf libgcc_s-%{gcc_major}-%{DATE}.so.1 %{buildroot}%{_libdir}/libgcc_s.so.1
ln -sf %{_libdir}/libgcc_s-%{gcc_major}-%{DATE}.so.1 $FULLPATH/libgcc_s.so

%if %{build_libgomp}
mv -f %{buildroot}%{_libdir}/libgomp.spec $FULLPATH/
%endif

%if %{build_ada}
mv -f $FULLPATH/adalib/libgnarl-*.so %{buildroot}%{_libdir}/
mv -f $FULLPATH/adalib/libgnat-*.so %{buildroot}%{_libdir}/
rm -f $FULLPATH/adalib/libgnarl.so* $FULLPATH/adalib/libgnat.so*
%endif

mkdir -p %{buildroot}%{_libexecdir}/getconf
if gcc/xgcc -B gcc/ -E -P -dD -xc /dev/null | grep '__LONG_MAX__.*\(2147483647\|0x7fffffff\($\|[LU]\)\)'; then
  ln -sf POSIX_V6_ILP32_OFF32 %{buildroot}%{_libexecdir}/getconf/default
else
  ln -sf POSIX_V6_LP64_OFF64 %{buildroot}%{_libexecdir}/getconf/default
fi

mkdir -p %{buildroot}%{_datadir}/gdb/auto-load/%{_libdir}
mv -f %{buildroot}%{_libdir}/libstdc++*gdb.py* \
      %{buildroot}%{_datadir}/gdb/auto-load/%{_libdir}/
pushd ../libstdc++-v3/python
for i in `find . -name \*.py`; do
  touch -r $i %{buildroot}%{_prefix}/share/gcc-%{gcc_major}/python/$i
done
touch -r hook.in %{buildroot}%{_datadir}/gdb/auto-load/%{_libdir}/libstdc++*gdb.py
popd
for f in `find %{buildroot}%{_prefix}/share/gcc-%{gcc_major}/python/ \
	       %{buildroot}%{_datadir}/gdb/auto-load/%{_libdir}/ -name \*.py`; do
  r=${f/$RPM_BUILD_ROOT/}
  %{__sys_python} -c 'import py_compile; py_compile.compile("'$f'", dfile="'$r'")'
  %{__sys_python} -O -c 'import py_compile; py_compile.compile("'$f'", dfile="'$r'")'
done

rm -f $FULLEPATH/libgccjit.so
%if %{build_libgccjit}
cp -a objlibgccjit/gcc/libgccjit.so* %{buildroot}%{_libdir}/
cp -a ../gcc/jit/libgccjit*.h %{buildroot}%{_includedir}/
%endif

pushd $FULLPATH
%if %{build_objc}
ln -sf ../../../libobjc.so.4 libobjc.so
%endif
ln -sf ../../../libstdc++.so.6.*[0-9] libstdc++.so
%if %{build_fortran}
ln -sf ../../../libgfortran.so.4.* libgfortran.so
%endif
%if %{build_libgomp}
ln -sf ../../../libgomp.so.1.* libgomp.so
%endif
%if %{build_go}
ln -sf ../../../libgo.so.11.* libgo.so
%endif
%if %{build_libquadmath}
ln -sf ../../../libquadmath.so.0.* libquadmath.so
%endif
%if %{build_libitm}
ln -sf ../../../libitm.so.1.* libitm.so
%endif
%if %{build_libatomic}
ln -sf ../../../libatomic.so.1.* libatomic.so
%endif
%if %{build_libsanitizer}
ln -sf ../../../libasan.so.4.* libasan.so
mv ../../../libasan_preinit.o libasan_preinit.o
ln -sf ../../../libubsan.so.0.* libubsan.so
rm -f libtsan.so
echo 'INPUT ( %{_libdir}/'`echo ../../../libtsan.so.0.* | sed 's,^.*libt,libt,'`' )' > libtsan.so
mv ../../../libtsan_preinit.o libtsan_preinit.o
rm -f liblsan.so
echo 'INPUT ( %{_libdir}/'`echo ../../../liblsan.so.0.* | sed 's,^.*libl,libl,'`' )' > liblsan.so
%endif
%if %{build_libcilkrts}
ln -sf ../../../libcilkrts.so.5.* libcilkrts.so
%endif
%if %{build_libmpx}
ln -sf ../../../libmpx.so.2.* libmpx.so
ln -sf ../../../libmpxwrappers.so.2.* libmpxwrappers.so
%endif
mv -f %{buildroot}%{_libdir}/libstdc++.*a $FULLLPATH/
mv -f %{buildroot}%{_libdir}/libstdc++fs.*a $FULLLPATH/
mv -f %{buildroot}%{_libdir}/libsupc++.*a $FULLLPATH/
%if %{build_fortran}
mv -f %{buildroot}%{_libdir}/libgfortran.*a $FULLLPATH/
%endif
%if %{build_objc}
mv -f %{buildroot}%{_libdir}/libobjc.*a .
%endif
%if %{build_libgomp}
mv -f %{buildroot}%{_libdir}/libgomp.*a .
%endif
%if %{build_libquadmath}
mv -f %{buildroot}%{_libdir}/libquadmath.*a $FULLLPATH/
%endif
%if %{build_libitm}
mv -f %{buildroot}%{_libdir}/libitm.*a $FULLLPATH/
%endif
%if %{build_libatomic}
mv -f %{buildroot}%{_libdir}/libatomic.*a $FULLLPATH/
%endif
%if %{build_libsanitizer}
mv -f %{buildroot}%{_libdir}/libasan.*a $FULLLPATH/
mv -f %{buildroot}%{_libdir}/libubsan.*a $FULLLPATH/
%ifarch x86_64 aarch64
mv -f %{buildroot}%{_libdir}/libtsan.*a $FULLLPATH/
mv -f %{buildroot}%{_libdir}/liblsan.*a $FULLLPATH/
%endif
%endif
%if %{build_libcilkrts}
mv -f %{buildroot}%{_libdir}/libcilkrts.*a $FULLLPATH/
%endif
%if %{build_libmpx}
mv -f %{buildroot}%{_libdir}/libmpx.*a $FULLLPATH/
mv -f %{buildroot}%{_libdir}/libmpxwrappers.*a $FULLLPATH/
%endif
%if %{build_go}
mv -f %{buildroot}%{_libdir}/libgo.*a $FULLLPATH/
mv -f %{buildroot}%{_libdir}/libgobegin.*a $FULLLPATH/
mv -f %{buildroot}%{_libdir}/libgolibbegin.*a $FULLLPATH/
%endif

%if %{build_ada}
if [ "$FULLPATH" != "$FULLLPATH" ]; then
mv -f $FULLPATH/ada{include,lib} $FULLLPATH/
pushd $FULLLPATH/adalib
ln -sf ../../../../../libgnarl-*.so libgnarl.so
ln -sf ../../../../../libgnarl-*.so libgnarl-6.so
ln -sf ../../../../../libgnat-*.so libgnat.so
ln -sf ../../../../../libgnat-*.so libgnat-7.so
popd
else
pushd $FULLPATH/adalib
ln -sf ../../../../libgnarl-*.so libgnarl.so
ln -sf ../../../../libgnarl-*.so libgnarl-6.so
ln -sf ../../../../libgnat-*.so libgnat.so
ln -sf ../../../../libgnat-*.so libgnat-7.so
popd
fi
%endif

pwd
popd
pwd

%if %{build_fortran}
chmod 755 %{buildroot}%{_libdir}/libgfortran.so.4.*
%endif
%if %{build_libgomp}
chmod 755 %{buildroot}%{_libdir}/libgomp.so.1.*
%endif
chmod 755 %{buildroot}%{_libdir}/libcc1.so.0.*
%if %{build_libquadmath}
chmod 755 %{buildroot}%{_libdir}/libquadmath.so.0.*
%endif
%if %{build_libitm}
chmod 755 %{buildroot}%{_libdir}/libitm.so.1.*
%endif
%if %{build_libatomic}
chmod 755 %{buildroot}%{_libdir}/libatomic.so.1.*
%endif
%if %{build_libsanitizer}
chmod 755 %{buildroot}%{_libdir}/libasan.so.4.*
chmod 755 %{buildroot}%{_libdir}/libubsan.so.0.*
%ifarch x86_64 aarch64
chmod 755 %{buildroot}%{_libdir}/libtsan.so.0.*
chmod 755 %{buildroot}%{_libdir}/liblsan.so.0.*
%endif
%endif
%if %{build_libcilkrts}
chmod 755 %{buildroot}%{_libdir}/libcilkrts.so.5.*
%endif
%if %{build_libmpx}
chmod 755 %{buildroot}%{_libdir}/libmpx.so.2.*
chmod 755 %{buildroot}%{_libdir}/libmpxwrappers.so.2.*
%endif
%if %{build_go}
chmod 755 %{buildroot}%{_libdir}/libgo.so.11.*
%endif
%if %{build_objc}
chmod 755 %{buildroot}%{_libdir}/libobjc.so.4.*
%endif
%if %{build_ada}
chmod 755 %{buildroot}%{_libdir}/libgnarl*so*
chmod 755 %{buildroot}%{_libdir}/libgnat*so*
%endif

mv $FULLPATH/include-fixed/syslimits.h $FULLPATH/include/syslimits.h
mv $FULLPATH/include-fixed/limits.h $FULLPATH/include/limits.h
for h in `find $FULLPATH/include -name \*.h`; do
  if grep -q 'It has been auto-edited by fixincludes from' $h; then
    rh=`grep -A2 'It has been auto-edited by fixincludes from' $h | tail -1 | sed 's|^.*"\(.*\)".*$|\1|'`
    diff -up $rh $h || :
    rm -f $h
  fi
done

cat > %{buildroot}%{_bindir}/%{?gccv:%{name}-}c89 <<"EOF"
#!/bin/sh
fl="-std=c89"
for opt; do
  case "$opt" in
    -ansi|-std=c89|-std=iso9899:1990) fl="";;
    -std=*) echo "`basename $0` called with non ANSI/ISO C option $opt" >&2
	    exit 1;;
  esac
done
exec %{name} $fl ${1+"$@"}
EOF
cat > %{buildroot}%{_bindir}/%{?gccv:%{name}-}c99 <<"EOF"
#!/bin/sh
fl="-std=c99"
for opt; do
  case "$opt" in
    -std=c99|-std=iso9899:1999) fl="";;
    -std=*) echo "`basename $0` called with non ISO C99 option $opt" >&2
	    exit 1;;
  esac
done
exec %{name} $fl ${1+"$@"}
EOF
chmod 755 %{buildroot}%{_bindir}/%{?gccv:%{name}-}c?9

cd ..

%if 0%{?gccv:1}
# rename binaries in user directories to avoid conflicts
%if %{build_ada}
for i in %{buildroot}%{_bindir}/gnat* ; do
  mv -f $i ${i}%{gccv}
done
%endif
pushd %{buildroot}%{_bindir}
for i in $(ls {*gcc,*++,gcov,cpp,*gccgo,*gfortran} 2>/dev/null) ; do
  mv -f $i ${i}%{gccv}
done
for i in $(ls *gcc-{ar,nm,ranlib} 2>/dev/null) ; do
  mv -f $i ${i/gcc-/gcc%{gccv}-}
done
# rename binaries and man pages for gcov-tool and gcov-dump
for b in tool dump ; do
  mv -f -v gcov-${b} gcov%{gccv}-${b}
done
popd
%endif # gccv binary rename
 
# Remove binaries we will not be including, so that they don't end up in
# gcc-debuginfo
rm -f %{buildroot}%{_libdir}/{libffi*,libiberty.a} || :
rm -f %{buildroot}%{_libdir}/{32,64}/libiberty.a
rm -f %{buildroot}%{_libdir}/libssp*
rm -rf $FULLPATH/install-tools $FULLEPATH/install-tools
rm -rf $FULLPATH/include-fixed $FULLPATH/include/ssp
%if !%{build_ada}
rm -f $FULLEPATH/gnat*
%endif
%if 0%{?gccv:1}
rm -f %{buildroot}%{_libdir}/libstdc++.so{,.?}
rm %{buildroot}%{_libdir}/libgcc_s.so.1 #%{buildroot}/%{_prefix}/%{_lib}/libgcc_s*
rm -f %{buildroot}%{_infodir}/gccinstall*
rm -f %{buildroot}%{_libdir}/libvtv* || :
%endif #?gccv

# man pages not related to gcc
rm -f %{buildroot}%{_mandir}/man7/*
# the file from the %{_lib} was installed, get rid of the other copy
rm -f %{buildroot}%{_prefix}/lib*/lib{gomp,gfortran,itm,cilkrts,sanitizer,mpx}.spec
# for now we don't expose the .so libs to the general public for these internally shared libs
rm -f %{buildroot}%{_libdir}/lib{gcc_s,gomp,objc,quadmath,stdc++,go,gfortran,itm,asan,atomic,lsan,tsan,ubsan,cilkrts,mpx,mpxwrappers}.so

rm -f %{buildroot}%{_bindir}/%{_target_platform}-gcc%{?gccv}-ar || :
rm -f %{buildroot}%{_bindir}/%{_target_platform}-gcc%{?gccv}-nm || :
rm -f %{buildroot}%{_bindir}/%{_target_platform}-gcc%{?gccv}-ranlib || :

## not shipping ffi.... we have a separate libffi package for this
rm -f $FULLPATH/include/ffi*
rm -f %{buildroot}%{_mandir}/man3/ffi*

# Help plugins find out nvra.
echo gcc-%{version}-%{release}.%{_arch} > $FULLPATH/rpmver

%clean
rm -rf %{buildroot}

%files
%license gcc/COPYING* COPYING.RUNTIME
%defattr(-,root,root,-)
%{_bindir}/%{?gccv:%{name}-}c89
%{_bindir}/%{?gccv:%{name}-}c99
%{_bindir}/gcc%{?gccv}
%{_bindir}/gcov%{?gccv}
%{_bindir}/gcov%{?gccv}-dump
%{_bindir}/gcov%{?gccv}-tool
%{_bindir}/gcc%{?gccv}-ar
%{_bindir}/gcc%{?gccv}-nm
%{_bindir}/gcc%{?gccv}-ranlib

%{_bindir}/%{gcc_target_platform}-gcc%{?gccv}
%{_bindir}/%{gcc_target_platform}-gcc-%{gcc_major}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_libexecdir}/gcc
%dir %{_libexecdir}/gcc/%{gcc_target_platform}
%dir %{_libexecdir}/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%{_libexecdir}/gcc/%{gcc_target_platform}/%{gcc_major}/lto1
%{_libexecdir}/gcc/%{gcc_target_platform}/%{gcc_major}/lto-wrapper
%{_libexecdir}/gcc/%{gcc_target_platform}/%{gcc_major}/liblto_plugin.so*
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/rpmver
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stddef.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdfix.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/varargs.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/float.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/gcov.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/limits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdbool.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/iso646.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/syslimits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/unwind.h
%if %{build_libgomp}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/omp.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/openacc.h
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdint.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdint-gcc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdalign.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdnoreturn.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdatomic.h
%ifarch %{ix86} x86_64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/emmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/pmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/tmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ammintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/smmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/nmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/wmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/immintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/x86intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/fma4intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xopintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/lwpintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/popcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/tbmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ia32intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmi2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/f16cintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/fmaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/lzcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/rtmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xtestintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/adxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/prfchwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/rdseedintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/fxsrintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsaveintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsaveoptintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512cdintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512erintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512fintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512pfintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/shaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mm_malloc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mm3dnow.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cpuid.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cross-stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512bwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512dqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512ifmaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512ifmavlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vbmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vbmivlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vlbwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vldqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/clflushoptintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/clwbintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mwaitxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsavecintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsavesintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/clzerointrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/pkuintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx5124fmapsintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx5124vnniwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vpopcntdqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/sgxintrin.h
%endif
%ifarch %{arm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/unwind-arm-common.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_neon.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_acle.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_cmse.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_fp16.h
%endif
%ifarch aarch64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_neon.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_acle.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_fp16.h
%endif
%if %{build_libcilkrts}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cilk
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libcilkrts.spec
%endif
%if %{build_libmpx}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libmpx.spec
%endif
%if %{build_libsanitizer}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/sanitizer
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libsanitizer.spec
%endif
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/collect2
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcc_s.so
%if %{build_libgomp}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgomp.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgomp.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.spec
%endif

%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libatomic.so
%endif
%if %{build_libsanitizer}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan_preinit.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libubsan.so
%ifarch x86_64 aarch64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libtsan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libtsan_preinit.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/liblsan.so
%endif
%endif
%if %{build_libcilkrts}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libcilkrts.so
%endif
%if %{build_libmpx}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libmpx.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libmpxwrappers.so
%endif
%{_libexecdir}/getconf/default

# MERGED SUBPACKAGES
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libatomic.a
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.a
%endif
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/quadmath.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/quadmath_weak.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libquadmath.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libquadmath.a
%endif
%if %{build_ada}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib
%endif
%if %{build_libsanitizer}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libubsan.a
%ifarch x86_64 aarch64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libtsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/liblsan.a
%endif
%license libsanitizer/LICENSE.TXT
%endif
%if %{build_libcilkrts}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libcilkrts.a
%endif
%if %{build_libmpx}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libmpx.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libmpxwrappers.a
%endif

%files -n cpp%{?gccv}
%defattr(-,root,root,-)
%{_prefix}/bin/cpp%{?gccv}
%dir %{_libexecdir}/gcc
%dir %{_libexecdir}/gcc/%{gcc_target_platform}
%dir %{_libexecdir}/gcc/%{gcc_target_platform}/%{gcc_major}
%{_libexecdir}/gcc/%{gcc_target_platform}/%{gcc_major}/cc1

%files -n libgcc%{?gccv}
%defattr(-,root,root,-)
%{_libdir}/libgcc_s-%{gcc_major}-%{DATE}.so.1
%if ! 0%{?gccv:1}
%{_libdir}/libgcc_s.so.1
%endif
%license gcc/COPYING* COPYING.RUNTIME

%files c++
%defattr(-,root,root,-)
%{_prefix}/bin/%{gcc_target_platform}-*++%{?gccv}
%{_prefix}/bin/g++%{?gccv}
%{_prefix}/bin/c++%{?gccv}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_libexecdir}/gcc
%dir %{_libexecdir}/gcc/%{gcc_target_platform}
%dir %{_libexecdir}/gcc/%{gcc_target_platform}/%{gcc_major}
%{_libexecdir}/gcc/%{gcc_target_platform}/%{gcc_major}/cc1plus
%{_prefix}/include/c++/%{gcc_major}/[^gjos]*
%{_prefix}/include/c++/%{gcc_major}/optional
%{_prefix}/include/c++/%{gcc_major}/os*
%{_prefix}/include/c++/%{gcc_major}/s[^u]*
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libsupc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++fs.a

%if %{build_objc}
%files objc
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_libexecdir}/gcc
%dir %{_libexecdir}/gcc/%{gcc_target_platform}
%dir %{_libexecdir}/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/objc
%{_libexecdir}/gcc/%{gcc_target_platform}/%{gcc_major}/cc1obj
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libobjc.so

%files objc++
%dir %{_libexecdir}/gcc
%dir %{_libexecdir}/gcc/%{gcc_target_platform}
%dir %{_libexecdir}/gcc/%{gcc_target_platform}/%{gcc_major}
%{_libexecdir}/gcc/%{gcc_target_platform}/%{gcc_major}/cc1objplus

%files -n libobjc%{?gccv}
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libobjc.so.4*
%endif # build_objc

%if %{build_fortran}
%files gfortran
%defattr(-,root,root,-)
%{_prefix}/bin/gfortran%{?gccv}
%{_prefix}/bin/%{_target_platform}-gfortran%{?gccv}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_libexecdir}/gcc
%dir %{_libexecdir}/gcc/%{gcc_target_platform}
%dir %{_libexecdir}/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib.f90
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib_kinds.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc.f90
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc_kinds.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc_lib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/ieee_arithmetic.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/ieee_exceptions.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/ieee_features.mod
%{_libexecdir}/gcc/%{gcc_target_platform}/%{gcc_major}/f951
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgfortran.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgfortran.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgfortran.a

%files -n libgfortran
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgfortran.so.4*
%endif # build_fortran

%if %{build_ada}
%files gnat
%defattr(-,root,root,-)
#{_prefix}/bin/gnat[^i]*
%{_prefix}/bin/gnat%{?gccv}
%{_prefix}/bin/gnatfind%{?gccv}
%{_prefix}/bin/gnatname%{?gccv}
%{_prefix}/bin/gnatlink%{?gccv}
%{_prefix}/bin/gnatgcc%{?gccv}
%{_prefix}/bin/gnatmake%{?gccv}
%{_prefix}/bin/gnatxref%{?gccv}
%{_prefix}/bin/gnatkr%{?gccv}
%{_prefix}/bin/gnatchop%{?gccv}
%{_prefix}/bin/gnatls%{?gccv}
%{_prefix}/bin/gnatbind%{?gccv}
%{_prefix}/bin/gnatprep%{?gccv}
%{_prefix}/bin/gnatclean%{?gccv}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/gnat1

%files -n libgnat%{?gccv}
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgnat-*.so
%{_prefix}/%{_lib}/libgnarl-*.so
%endif #build_ada

%if %{build_libgomp}
%files -n libgomp
%{_prefix}/%{_lib}/libgomp.so.1*
#%{_prefix}/%{_lib}/libgomp-plugin-host_nonshm.so.1*
#%{_prefix}/%{_lib}/libgomp-plugin-host_nonshm.so
%endif # libgomp

%if %{build_libquadmath}
%files -n libquadmath
%{_prefix}/%{_lib}/libquadmath.so.0*
%license rpm.doc/libquadmath/COPYING*
%endif #build_libquadmath

%if %{build_libitm}
%files -n libitm
%{_prefix}/%{_lib}/libitm.so.1*
%endif #build_libitm

%if %{build_libatomic}
%files -n libatomic
%{_prefix}/%{_lib}/libatomic.so.1*
%endif

%if %{build_libsanitizer}
%files -n libsanitizer
%{_prefix}/%{_lib}/libasan.so.4*
%{_prefix}/%{_lib}/libubsan.so.0*
%ifarch x86_64 aarch64
%{_prefix}/%{_lib}/libtsan.so.0*
%{_prefix}/%{_lib}/liblsan.so.0*
%endif
%license libsanitizer/LICENSE.TXT
%endif #build_libsanitizer

%if %{build_libcilkrts}
%files -n libcilkrts
%{_prefix}/%{_lib}/libcilkrts.so.5*
%endif #build_libcilkrts

%if %{build_libmpx}
%files -n libmpx
%{_prefix}/%{_lib}/libmpx.so.2*
%{_prefix}/%{_lib}/libmpxwrappers.so.2*
%endif #build_libmpx

%if %{build_go}
%files go
%defattr(-,root,root,-)
%{_prefix}/bin/gccgo%{?gccv}
%{_prefix}/bin/%{_target_platform}-gccgo%{?gccv}
%{_prefix}/bin/go.gcc%{?gccv}
%{_prefix}/bin/gofmt.gcc%{?gccv}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_libexecdir}/gcc
%dir %{_libexecdir}/gcc/%{gcc_target_platform}
%dir %{_libexecdir}/gcc/%{gcc_target_platform}/%{gcc_major}
%{_libexecdir}/gcc/%{gcc_target_platform}/%{gcc_major}/go1
%{_libexecdir}/gcc/%{gcc_target_platform}/%{gcc_major}/cgo
%{_prefix}/%{_lib}/go/%{gcc_major}/%{gcc_target_platform}

%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgolibbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgo.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgo.a

%files -n libgo
%{_prefix}/%{_lib}/libgo.so.11*

%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/%{_lib}/go
%dir %{_prefix}/%{_lib}/go/%{gcc_major}
%{_prefix}/%{_lib}/go/%{gcc_major}/%{gcc_target_platform}
%endif #build_go

%if %{build_libgccjit}
%files -n libgccjit
%{_prefix}/%{_lib}/libgccjit.so.*
%endif

%files gdb-plugin
%{_prefix}/%{_lib}/libcc1.so*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/libcc1plugin.so*
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/libcp1plugin.so*

%exclude %{_mandir}
%exclude %{_infodir}
%exclude %{_datadir}/locale
%exclude %{_libdir}/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/include
%exclude %{_libdir}/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/gtype.state
%exclude %{_libexecdir}/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/gengtype
%exclude %{_libdir}/libstdc++.so.6.*
%exclude %{_datadir}/gdb/auto-load/%{_libdir}/libstdc*gdb.py*
%exclude %{_prefix}/share/gcc-%{gcc_major}/python/libstdcxx

%changelog
* Wed Oct 30 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Sat Jan 13 2018 Cristian Gafton <gafton@amazon.com>
- build a minimal compiler with retpoline support

* Thu Jan 11 2018 Cristian Gafton <gafton@amazon.com>
- add support for building a minimal compiler set
- handle building libgomp as an optional support library
- conditionalize support for building multilib

* Thu Jan 11 2018 Praveen K Paladugu <praween@amazon.com>
- Add retpoline patches for gcc 7.2

* Tue Jan 9 2018 Cristian Gafton <gafton@amazon.com>
- correctly disable building libquadmath when requested by the spec file

* Sat Sep 23 2017 Cristian Gafton <gafton@amazon.com>
- add obsoletes for older name-versioned GCC builds when building as the main compiler

* Fri Sep 22 2017 Cristian Gafton <gafton@amazon.com>
- build it as the main compiler
- remove support for nvptx-tools

* Thu Sep 21 2017 Cristian Gafton <gafton@amazon.com>
- import source package F26/gcc-7.2.1-2.fc26
- import source package F26/gcc-7.1.1-3.fc26

* Fri Sep 15 2017 Jakub Jelinek <jakub@redhat.com> 7.2.1-2
- update from the 7 branch
  - PRs ada/62235, ada/79441, ada/79542, bootstrap/81926, c++/81355,
	c++/81852, c++/82039, c++/82040, c/45784, c/81687, driver/81650,
	fortran/81770, inline-asm/82001, ipa/81128, libstdc++/70483,
	libstdc++/81338, libstdc++/81468, libstdc++/81599, libstdc++/81835,
	libstdc++/81891, libstdc++/81912, middle-end/81052, middle-end/81768,
	other/39851, sanitizer/63361, sanitizer/81923, target/80695,
	target/81504, target/81593, target/81621, target/81833, target/81988,
	target/82181, testsuite/82114, testsuite/82120, tree-opt/81696,
	tree-optimization/81503, tree-optimization/81987
- fix OpenMP implicit firstprivate handling of references (PR c++/81314)
- fix -fcompare-debug failures with PowerPC atomics (PR target/81325)
- fix compile time hog in C++ replace_placeholders (PR sanitizer/81929)
- fix __atomic* and PowerPC vec_ld/vec_st handling of array arguments
  (PR target/82112)

* Fri Sep 8 2017 Cristian Gafton <gafton@amazon.com>
- add option to control when libgccjit is built

* Mon Sep 4 2017 Cristian Gafton <gafton@amazon.com>
- add Obsoletes for older libtsan packages
- use an unversioned name for libstdc++ docs package
- move obsoletes for components of older compilers to the main compiler package
- mereg static libraries into the main compiler package
- merge devel and static libstdc++ into the main gcc-c++ compiler package
- merge devel and static libgo into the main gcc-go compiler package
- merge devel and static libgnat into the main gcc-gnat package
- merge static and devel libquadmath into the main compiler package
- merge devel and static libitm into main compiler package
- merge libatomic static libs into the main compiler package

* Fri Sep 1 2017 Cristian Gafton <gafton@amazon.com>
- fix obsoletes for older libmudflap subpackages
- do not onsolete the old sanitizer library packages
- enable the Fortran compiler

* Thu Aug 31 2017 Cristian Gafton <gafton@amazon.com>
- add buildrequire for a version of rpm-build that supports dwarf4
- on i686/32bit, not all the modules/modes of libsanitizer are available
- fix description test for the libatomic subpackage
- spec file simplification: remove build sections for legacy and unsupported platforms
- coalesce all the -fsanitize libraries into a single libsanitizer package
- properly disable optional libraries from building when requested in the spec file

* Wed Aug 30 2017 Cristian Gafton <gafton@amazon.com>
- handle the new gcov-dump and gcov-tool binaries through alternatives as well

* Tue Aug 29 2017 Jakub Jelinek <jakub@redhat.com> 7.2.1-1
- update from the 7 branch
  - 7.2 release
  - PRs c++/67054, c++/81607, debug/81993, driver/81523, fortran/80164,
	fortran/81296, ipa/77732, libstdc++/53984, libstdc++/79820,
	libstdc++/81751, middle-end/81065, middle-end/81088, middle-end/81766,
	middle-end/81884, sanitizer/80932, target/67712, target/72804,
	target/78460, target/80210, target/81170, target/81295, target/81861,
	target/81894, target/81910, target/81921, testsuite/81056,
	tree-optimization/81181, tree-optimization/81354,
	tree-optimization/81723, tree-optimization/81977

* Tue Aug 29 2017 Cristian Gafton <gafton@amazon.com>
- import source package F25/gcc-6.4.1-1.fc25

* Wed Aug  2 2017 Jakub Jelinek <jakub@redhat.com> 7.1.1-7
- update from the 7 branch
  - 7.2-rc1
  - PRs c++/71570, gcov-profile/81561, libgcc/61152, libquadmath/65757,
	libstdc++/80553, libstdc++/80721, libstdc++/80737, libstdc++/80939,
	libstdc++/81017, lto/81487, middle-end/79499, middle-end/81505,
	rtl-optimization/75964, sanitize/81186, sanitizer/81021,
	sanitizer/81224, sanitizer/81302, sanitizer/81604, target/79041,
	target/80569, target/81069, target/81175, target/81193, target/81407,
	target/81414, target/81471, target/81473, target/81534, target/81622,
	target/81641, tree-optimization/71752, tree-optimization/80769,
	tree-optimization/81162, tree-optimization/81388,
	tree-optimization/81410, tree-optimization/81455,
	tree-optimization/81555, tree-optimization/81556,
	tree-optimization/81588, tree-optimization/81633,
	tree-optimization/81655

* Tue Jul 18 2017 Jakub Jelinek <jakub@redhat.com> 7.1.1-6
- update from the 7 branch
  - PRs ada/81446, c++/81258, middle-end/80929, rtl-optimization/81424,
	target/79883, target/81225, tree-optimization/81365,
	tree-optimization/81428
- fix bootstrap on s390{,x} in libgo (PR go/81393)
- rebuilt against hopefully fixed glibc to reenable TLS support on ppc64le
  in libstdc++ (#1470692)

* Tue Jul 11 2017 Jakub Jelinek <jakub@redhat.com> 7.1.1-5
- update from the 7 branch
  - PRs libstdc++/80316, target/81375
- fix libsanitizer build against recent glibc (PR sanitizer/81066)

* Sun Jul  9 2017 Jakub Jelinek <jakub@redhat.com> 7.1.1-4
- update from the 7 branch
  - PRs c++/54769, c++/61022, c++/72801, c++/79056, c++/81164, c++/81180,
	c++/81187, c++/81188, c++/81204, c++/81215, c++/81257, driver/31468,
	driver/56469, gcov-profile/53915, gcov-profile/81080, ipa/79849,
	ipa/79850, ipa/80663, ipa/81112, libfortran/81195, libgfortran/53029,
	libstdc++/81221, middle-end/80692, middle-end/80902, middle-end/81007,
	middle-end/81207, other/80589, other/80909, sanitizer/80879,
	sanitizer/81209, target/79155, target/79799, target/80618,
	target/80966, target/81294, target/81300, target/81305, target/81348,
	tree-optimization/80612, tree-optimization/81083,
	tree-optimization/81192
- fix ppc* float128 ifunc (#1467526)

* Thu Jun 22 2017 Jakub Jelinek <jakub@redhat.com> 7.1.1-3
- update from the 7 branch
  - PRs ada/80921, ada/81070, ada/81105, c++/60063, c++/66297, c++/70844,
	c++/71747, c++/80179, c++/80384, c++/80465, c++/80562, c++/80593,
	c++/80605, c++/80614, c++/80639, c++/80829, c++/80831, c++/80840,
	c++/80856, c++/80972, c++/80973, c++/80984, c++/81011, c++/81045,
	c++/81073, c++/81074, c++/81102, c++/81130, c++/81154, c/80919,
	c/81006, fortran/70601, fortran/80766, fortran/80904, fortran/80918,
	fortran/80975, libgcc/80037, libgomp/80822, libstdc++/80675,
	libstdc++/80940, libstdc++/81002, libstdc++/81092,
	rtl-optimization/80474, rtl-optimization/80903, sanitizer/81111,
	sanitizer/81125, target/59874, target/71607, target/71778,
	target/80718, target/80968, target/80970, target/81015, target/81121,
	target/81151, tree-optimization/80293, tree-optimization/80549,
	tree-optimization/80705, tree-optimization/80842,
	tree-optimization/80906

* Fri May 26 2017 Jakub Jelinek <jakub@redhat.com> 7.1.1-2
- update from the 7 branch
  - PRs ada/80626, ada/80784, documentation/50642, fortran/78659,
	fortran/80121, fortran/80333, fortran/80392, fortran/80484,
	fortran/80741, fortran/80752, go/64238, libgfortran/80333,
	libgfortran/80727, libgfortran/80741, libstdc++/78939, libstdc++/80478,
	libstdc++/80761, libstdc++/80796, middle-end/80539, middle-end/80809,
	middle-end/80853, rtl-optimization/80754, sanitizer/80659,
	sanitizer/80875, target/68163, target/79027, target/79202,
	target/79203, target/80090, target/80510, target/80671, target/80706,
	target/80799, tree-optimization/80453, tree-optimization/80492
- fix s390 indirect_jump reloading (#1450353, PR target/80725)

* Sat May 6 2017 Cristian Gafton <gafton@amazon.com>
- use system python to compile system python support

* Fri May 5 2017 Cristian Gafton <gafton@amazon.com>
- import source package F24/gcc-6.3.1-1.fc24

* Thu May 4 2017 Cristian Gafton <gafton@amazon.com>
- import source package F24/gcc-6.2.1-2.fc24
- udpate libstdc++ soname version for gcc6.1 build

* Wed May  3 2017 Jakub Jelinek <jakub@redhat.com> 7.1.1-1
- update from the 7 branch
  - GCC 7.1 release
  - PRs bootstrap/80531, c++/80534, c/80468, target/68491, target/79430,
	target/80530, tree-optimization/80591

* Wed May 3 2017 Cristian Gafton <gafton@amazon.com>
- import source package F24/gcc-6.1.1-3.fc24
- import source package F24/gcc-6.1.1-2.fc24

* Tue May 2 2017 Cristian Gafton <gafton@amazon.com>
- disable hardcode obsoletes on Ada95/libgnat libraries
- remove build references to obsolete mudflap header files
- update packaging scripts for the new libstdc++ soname version
- import source package F22/gcc-5.3.1-6.fc22
- import source package F22/gcc-5.3.1-2.fc22

* Mon May 1 2017 Cristian Gafton <gafton@amazon.com>
- disable fortran build
- update file list for new libgomp plugin lib
- add new libgfortran static library when building fortran backend
- update packaging for new libmpx artifacts

* Sat Apr 29 2017 Cristian Gafton <gafton@amazon.com>
- rename gcov-tool as well
- update sphinx-build build requirement to accomodate different verions of python backends

* Fri Apr 28 2017 Cristian Gafton <gafton@amazon.com>
- spec fix - exclude files which are not included in packages

* Thu Apr 27 2017 Cristian Gafton <gafton@amazon.com>
- import source package F22/gcc-5.1.1-4.fc22
- import source package F22/gcc-5.1.1-3.fc22
- import source package F22/gcc-5.1.1-1.fc22

* Tue Apr 25 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.16
- update from the 7 branch
  - ABI change on ARM and AArch64 (PR target/77728)
  - PRs middle-end/79931, rtl-optimization/80500, rtl-optimization/80501,
	target/79895, target/80080, target/80464, target/80482,
	tree-optimization/80497

* Fri Apr 21 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.15
- update from the trunk and 7 branch
  - PRs bootstrap/77661, c++/80176, c++/80241, c++/80244, c++/80287,
	c++/80294, c++/80363, c++/80370, c++/80415, c++/80459, c++/80473,
	c/80163, debug/80263, debug/80436, debug/80461, fortran/80046,
	fortran/80361, fortran/80440, gcov-profile/78783, gcov-profile/80413,
	gcov-profile/80435, ipa/65972, libgomp/80394, libstdc++/80446,
	libstdc++/80448, lto/50345, lto/69953, middle-end/79671,
	middle-end/79788, middle-end/80100, middle-end/80364,
	middle-end/80375, middle-end/80422, middle-end/80423,
	rtl-optimization/80343, rtl-optimization/80357,
	rtl-optimization/80385, rtl-optimization/80429, sanitizer/70878,
	sanitizer/80349, sanitizer/80403, sanitizer/80404, sanitizer/80405,
	sanitizer/80414, sanitizer/80444, target/74563, target/79453,
	target/80057, target/80098, target/80099, target/80108, target/80315,
	target/80376, target/80381, target/80382, target/80389, target/80462,
	testsuite/79867, testsuite/80221, testsuite/80416,
	tree-optimization/80153, tree-optimization/80359,
	tree-optimization/80374, tree-optimization/80426,
	tree-optimization/80443
- reenable {gcc,libgomp}-offload-nvptx on ppc64le

* Mon Apr 10 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.14
- update from the trunk
  - PRs ada/80117, ada/80146, c++/60992, c++/69487, c++/79572, c++/80095,
	c++/80267, c++/80296, c++/80297, c++/80309, c++/80356, c/79730,
	debug/79255, debug/80025, debug/80234, documentation/78732,
	fortran/78661, fortran/80254, gcov-profile/80224, go/80226, ipa/77333,
	ipa/79776, ipa/80104, ipa/80205, ipa/80212, libgfortran/78670,
	libgomp/79876, libstdc++/79141, libstdc++/80137, libstdc++/80229,
	libstdc++/80251, middle-end/80162, middle-end/80163, middle-end/80173,
	middle-end/80222, middle-end/80281, middle-end/80341,
	middle-end/80344, middle-end/80362, rtl-optimization/60818,
	rtl-optimization/70478, rtl-optimization/70703,
	rtl-optimization/79405, rtl-optimization/80193,
	rtl-optimization/80233, sanitizer/79993, sanitizer/80067,
	sanitizer/80166, sanitizer/80308, sanitizer/80348, sanitizer/80350,
	target/45053, target/53383, target/78002, target/78543, target/79733,
	target/79889, target/79890, target/79905, target/80102, target/80103,
	target/80107, target/80206, target/80246, target/80250, target/80286,
	target/80298, target/80307, target/80310, target/80322, target/80323,
	target/80324, target/80325, target/80326, target/80358,
	testsuite/43496, translation/80189, tree-optimization/49498,
	tree-optimization/77498, tree-optimization/78644,
	tree-optimization/79390, tree-optimization/80181,
	tree-optimization/80216, tree-optimization/80218,
	tree-optimization/80262, tree-optimization/80275,
	tree-optimization/80304, tree-optimization/80334
- fix dwarf ICE with nested function self-inlining (PR debug/80321)

* Mon Mar 27 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.13
- update from the trunk
  - PRs bootstrap/79771, bootstrap/79952, c++/35878, c++/52477, c++/77339,
	c++/77563, c++/77752, c++/78345, c++/79393, c++/79519, c++/79548,
	c++/79640, c++/79687, c++/79896, c++/79899, c++/79960, c++/79962,
	c++/79967, c++/79984, c++/80029, c++/80043, c++/80059, c++/80073,
	c++/80077, c++/80084, c++/80096, c++/80119, c++/80129, c++/80141,
	c++/80150, c/67338, c/78165, c/79921, c/79936, c/80097, driver/79875,
	fortran/33271, fortran/39239, fortran/69498, fortran/71838,
	fortran/79602, fortran/79676, fortran/79838, fortran/79844,
	fortran/79853, fortran/79859, fortran/79860, fortran/79886,
	fortran/80010, fortran/80011, fortran/80142, fortran/80156,
	gcov-profile/80081, libfortran/79956, libgfortran/78854,
	libgfortran/78881, libstdc++/62045, libstdc++/67440, libstdc++/79162,
	libstdc++/79511, libstdc++/79980, libstdc++/80034, libstdc++/80041,
	libstdc++/80064, libstdc++/80183, middle-end/78339, middle-end/79753,
	middle-end/79831, middle-end/80020, middle-end/80050,
	middle-end/80075, middle-end/80171, other/79991, plugins/80094,
	rtl-optimization/63191, rtl-optimization/78911,
	rtl-optimization/79150, rtl-optimization/79728,
	rtl-optimization/79909, rtl-optimization/79910,
	rtl-optimization/80112, rtl-optimization/80159,
	rtl-optimization/80160, sanitizer/78158, sanitizer/79757,
	sanitizer/80063, sanitizer/80110, sanitizer/80168, target/71294,
	target/71436, target/78857, target/79769, target/79770, target/79892,
	target/79893, target/79906, target/79907, target/79911, target/79912,
	target/79925, target/79941, target/79947, target/79951, target/79963,
	target/80017, target/80019, target/80052, target/80082, target/80083,
	target/80123, target/80125, target/80148, target/80180,
	testsuite/79356, testsuite/80092, translation/79848,
	translation/79923, translation/80001, tree-optimization/71437,
	tree-optimization/77975, tree-optimization/79800,
	tree-optimization/79908, tree-optimization/79981,
	tree-optimization/80030, tree-optimization/80032,
	tree-optimization/80048, tree-optimization/80054,
	tree-optimization/80072, tree-optimization/80079,
	tree-optimization/80109, tree-optimization/80113,
	tree-optimization/80122, tree-optimization/80136,
	tree-optimization/80158, tree-optimization/80167,
	tree-optimization/80170

* Thu Mar  9 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.12
- update from the trunk
  - PRs c++/71966, c++/79672, c++/79797, c++/79900, ipa/79761, ipa/79764,
	ipa/79970, middle-end/79971, rtl-optimization/79949, target/65705,
	target/69804, target/79913, target/79928, tree-optimization/79631,
	tree-optimization/79977
- fix DW_AT_decl_line on DW_TAG_enumeration_type for C enumeration
  definitions following forward declarations (#1423460, PR c/79969)
- fix ICE with -Walloca (PR tree-optimization/79972)

* Wed Mar  8 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.11
- update from the trunk
  - PRs ada/79903, ada/79945, c++/42000, c++/64574, c++/70266, c++/71568,
	c++/79414, c++/79681, c++/79746, c++/79782, c++/79791, c++/79796,
	c++/79821, c++/79822, c++/79825, c/79756, c/79758, c/79834, c/79836,
	c/79837, c/79847, c/79855, c/79940, demangler/67264, demangler/70909,
	fortran/51119, fortran/78379, fortran/79739, fortran/79841,
	fortran/79894, libstdc++/79789, libstdc++/79798, lto/78140, lto/79625,
	lto/79760, middle-end/68270, middle-end/79692, middle-end/79721,
	middle-end/79731, middle-end/79805, middle-end/79809,
	middle-end/79818, rtl-optimization/79571, rtl-optimization/79584,
	rtl-optimization/79780, rtl-optimization/79901, sanitize/79783,
	sanitizer/79897, sanitizer/79904, target/43763, target/68739,
	target/79395, target/79439, target/79514, target/79544, target/79729,
	target/79742, target/79749, target/79752, target/79793, target/79807,
	target/79812, tree-optimization/45397, tree-optimization/66768,
	tree-optimization/77536, tree-optimization/79345,
	tree-optimization/79690, tree-optimization/79691,
	tree-optimization/79699, tree-optimization/79723,
	tree-optimization/79732, tree-optimization/79734,
	tree-optimization/79737, tree-optimization/79740,
	tree-optimization/79777, tree-optimization/79803,
	tree-optimization/79824, tree-optimization/79894,
	tree-optimization/79920, tree-optimization/79943,
	tree-optimization/79955
- fix 64 avx512vl and 6 avx512bw intrinsics that were not available with -O0
  (PR target/79932)
- temporarily disable incorrect folding of Altivec vmul[oe]u[bh] intrinsics
  (#1429961, PR middle-end/79941)
- fix -fsanitize=address with some atomic/sync builtins (PR sanitizer/79944)

* Sat Feb 25 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.10
- update from the trunk
  - PRs c++/17729, c++/41727, c++/50308, c++/69523, c++/78139, c++/78282,
	c++/79361, c++/79380, c++/79400, c++/79470, c++/79500, c++/79503,
	c++/79535, c++/79566, c++/79580, c++/79588, c++/79606, c++/79607,
	c++/79639, c++/79641, c++/79653, c++/79654, c++/79655, c++/79657,
	c++/79664, c++/79679, c/79662, c/79677, c/79684, debug/77589,
	fortran/79229, fortran/79382, fortran/79402, fortran/79434,
	fortran/79447, fortran/79523, fortran/79597, fortran/79599,
	fortran/79601, go/79642, lto/79579, lto/79587, middle-end/79396,
	middle-end/79537, middle-end/79665, rtl-optimization/68749,
	rtl-optimization/79286, sanitizer/79558, sanitizer/79589,
	target/71017, target/78012, target/78056, target/78660, target/79211,
	target/79473, target/79494, target/79568, target/79570, target/79593,
	target/79633, translation/79638, translation/79705,
	tree-optimization/61441, tree-optimization/68644,
	tree-optimization/79389, tree-optimization/79578,
	tree-optimization/79621, tree-optimization/79649,
	tree-optimization/79663, tree-optimization/79666,
	tree-optimization/79673, tree-optimization/79683

* Sun Feb 19 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.9
- update from the trunk
  - PRs bootstrap/79567, c++/77659, c++/77790, c++/78572, c++/78690,
	c++/79050, c++/79296, c++/79301, c++/79363, c++/79420, c++/79461,
	c++/79463, c++/79464, c++/79502, c++/79508, c++/79512, c++/79533,
	c++/79549, c++/79556, c/79471, c/79478, c/79515, fortran/65542,
	ipa/79224, libstdc++/78723, libstdc++/79348, libstdc++/79467,
	libstdc++/79486, libstdc++/79513, middle-end/61225, middle-end/79432,
	middle-end/79448, middle-end/79496, middle-end/79505,
	middle-end/79521, middle-end/79536, middle-end/79576,
	rtl-optimization/78127, rtl-optimization/79286,
	rtl-optimization/79541, rtl-optimization/79574,
	rtl-optimization/79577, sanitizer/79562, target/79261, target/79282,
	target/79404, target/79421, target/79449, target/79462, target/79481,
	target/79487, target/79495, target/79498, target/79559, target/79569,
	tree-optimization/79095, tree-optimization/79347,
	tree-optimization/79529, tree-optimization/79552, tree-ssa/56727

* Wed Feb 15 2017 Cristian Gafton <gafton@amazon.com>
- disable go language support

* Sat Feb 11 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.8
- update from the trunk
  - PRs c++/71285, c++/78897, c++/78908, c++/79143, c++/79184, c++/79316,
	c++/79350, c++/79401, c++/79435, c++/79457, ipa/70795,
	middle-end/79454, target/79295, tree-optimization/66612,
	tree-optimization/79411
- fix combiner get_last_value handling (PRs rtl-optimization/79388,
  rtl-optimization/79450)

* Thu Feb  9 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.7
- update from the trunk
  - PRs c++/70448, c++/71193, c++/79360, c++/79372, c++/79377, c++/79379,
	c++/79429, c/79413, c/79428, c/79431, fortran/78958, fortran/79230,
	fortran/79335, fortran/79344, ipa/79375, libstdc++/79323,
	middle-end/79278, middle-end/79399, rtl-optimization/68664,
	rtl-optimization/79386, target/66144, target/68972, target/78604,
	target/78883, target/79299, target/79353, translation/79397,
	tree-optimization/69823, tree-optimization/78348,
	tree-optimization/79284, tree-optimization/79376,
	tree-optimization/79408, tree-optimization/79409, tree-ssa/79347
- fix addition of OFFLOAD_TARGET_DEFAULT env var in gcc driver
- use isl 0.16.1 instead of 0.14
- fix s390x libasan __tls_get_offset interception (PR sanitizer/79341)
- list fixed RHEL{6,7} kernels in CVE-2016-2143 s390x libsanitizer whitelist

* Thu Feb 9 2017 Cristian Gafton <gafton@amazon.com>
- change package and subpackage renames to make it work with alternatives

* Sat Feb  4 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.6
- update from the trunk
  - PRs ada/79309, c++/12245, c++/69637, c++/78689, c++/79294, cp/14179,
	ipa/79337, libstdc++/60936, libstdc++/78346, lto/66295,
	middle-end/32003, middle-end/78142, middle-end/78468,
	middle-end/79275, sanitizer/78663, target/70012, target/78862,
	target/79158, target/79354, testsuite/76957, testsuite/79272,
	testsuite/79324, tree-optimization/79327, tree-optimization/79338,
	tree-optimization/79339, tree-optimization/79340,
	tree-optimization/79352
- default to -march=zEC12 -mtune=z13 on s390x (#1404991)

* Wed Feb  1 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.5
- update from the trunk
  - PRs c++/67273, c++/79253, c++/79264, c++/79290, c++/79298, c++/79304,
	fortran/79305, ipa/79285, middle-end/79315, preprocessor/79210,
	target/78597, target/79038, tree-optimization/71691,
	tree-optimization/71824, tree-optimization/77318

* Tue Jan 31 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.4
- update from the trunk
  - PRs bootstrap/78985, debug/63238, debug/79289, gcov-profile/79259,
	target/78945, target/79170, target/79240, target/79260, target/79268,
	testsuite/70583, testsuite/79293, tree-optimization/79256,
	tree-optimization/79267, tree-optimization/79276
- fix ICEs with powerpc conversion of float/double to 64-bit unsigned integer
  (PR target/79197)
- fix C++ ICE with comma expression on lhs of assignment (PR c++/79232)
- fix default TLS model for C++ non-inline static data members (PR c++/79288)
- libcp1plugin.so added to gcc-gdb-plugin for C++ support

* Sat Jan 28 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.3
- update from the trunk
  - PRs c++/64382, c++/68727, c++/78771, c++/79176, debug/78835, debug/79129,
	libstdc++/79190, libstdc++/79243, libstdc++/79254,
	rtl-optimization/78559, rtl-optimization/79194, target/65484,
	target/79131, target/79239, tree-optimization/71374,
	tree-optimization/79244, tree-optimization/79245

* Thu Jan 26 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.2
- update from the trunk
  - PRs bootstrap/79132, bootstrap/79198, c++/71290, c++/71406, c++/71710,
	c++/77508, c++/77914, c++/78469, c++/78896, c++/79118, c++/79205,
	c/79199, debug/78363, fortran/79154, ipa/79108, libstdc++/61791,
	libstdc++/70607, libstdc++/79195, libstdc++/79206, middle-end/78703,
	middle-end/79123, middle-end/79212, middle-end/79236,
	rtl-optimization/71724, rtl-optimization/78634,
	rtl-optimization/79125, sanitizer/79168, target/61729, target/66669,
	target/70465, target/77439, target/77850, target/79145, target/79179,
	testsuite/72850, testsuite/78421, testsuite/79169, translation/79208,
	tree-optimization/69264, tree-optimization/70754,
	tree-optimization/78384, tree-optimization/79088,
	tree-optimization/79159, tree-optimization/79186,
	tree-optimization/79188, tree-optimization/79196
- temporarily disable {gcc,libgomp}-offload-nvptx on ppc64le, further
  debugging there is needed
- enable libasan and libubsan on s390x and libtsan and liblsan on
  ppc64{,le}

* Fri Jan 20 2017 Jakub Jelinek <jakub@redhat.com> 7.0.1-0.1
- update from the trunk
  - PRs c++/77829, c++/78495, c++/78656, c++/79495, c/64279, c/79152,
	libstdc++/69240, target/71270

* Fri Jan 20 2017 Jakub Jelinek <jakub@redhat.com> 7.0.0-0.3
- update from the trunk
  - PRs ada/67205, bootstrap/78616, bootstrap/79052, bootstrap/79069,
	c++/24511, c++/61636, c++/68666, c++/70182, c++/70565, c++/71166,
	c++/71497, c++/71537, c++/71737, c++/72813, c++/77489, c++/77812,
	c++/78337, c++/78341, c++/78488, c++/78894, c++/79091, c++/79130,
	c/47931, c/78304, c/78768, c/79074, c/79089, c/79116, debug/71669,
	debug/78839, driver/49726, driver/78877, fortran/50069, fortran/55086,
	fortran/70696, fortran/70697, ipa/71190, ipa/71207, ipa/79043,
	libobjc/78697, libobjc/78698, libstdc++/64903, libstdc++/65411,
	libstdc++/66145, libstdc++/66284, libstdc++/67085, libstdc++/68925,
	libstdc++/69301, libstdc++/69321, libstdc++/69699, libstdc++/72792,
	libstdc++/72793, libstdc++/77528, libstdc++/78134, libstdc++/78273,
	libstdc++/78361, libstdc++/78389, libstdc++/78702, libstdc++/78905,
	libstdc++/78979, libstdc++/79075, libstdc++/79114, libstdc++/79156,
	lto/69188, lto/78407, lto/79042, lto/79061, middle-end/77445,
	middle-end/78411, other/79046, rtl-optimization/78626,
	rtl-optimization/78727, rtl-optimization/78751,
	rtl-optimization/78952, rtl-optimization/79032,
	rtl-optimization/79121, sanitizer/78887, target/72749, target/76731,
	target/77416, target/78176, target/78253, target/78478, target/78516,
	target/78633, target/78875, target/79004, target/79040, target/79044,
	target/79058, target/79066, target/79079, target/79080, target/79098,
	target/79127, target/79140, target/79144, testsuite/52563,
	testsuite/71237, testsuite/77737, testsuite/79051, testsuite/79073,
	testsuite/79115, tree-optimization/33562, tree-optimization/61912,
	tree-optimization/71264, tree-optimization/71433,
	tree-optimization/71854, tree-optimization/72488,
	tree-optimization/77283, tree-optimization/77485,
	tree-optimization/78319, tree-optimization/78608,
	tree-optimization/79090
- add gcc-offload-nvptx and libgomp-offload-nvptx packages for offloading
  to NVPTX on x86_64 or ppc64le

* Thu Jan 12 2017 Jakub Jelinek <jakub@redhat.com> 7.0.0-0.2
- new package

* Fri Jul 31 2015 Rodrigo Novo <rodarvus@amazon.com>
- Fix Build Dependencies for Amazon Linux AMI
- import source package F21/gcc-4.9.2-6.fc21
