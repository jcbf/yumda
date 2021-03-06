Summary: An XML parser library
Name: expat
Version: 2.1.0
Release: 10%{?dist}.0.2
Group: System Environment/Libraries
Source: http://downloads.sourceforge.net/expat/expat-%{version}.tar.gz
Patch0: expat-2.1.0-xmlwfargs.patch
Patch1: expat-2.1.0-CVE-2016-0718.patch
URL: http://www.libexpat.org/
License: MIT
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: autoconf, automake, libtool, check-devel

Prefix: %{_prefix}

%description
This is expat, the C library for parsing XML, written by James Clark. Expat
is a stream oriented XML parser. This means that you register handlers with
the parser prior to starting the parse. These handlers are called when the
parser discovers the associated structures in the document being parsed. A
start tag is an example of the kind of structures for which you may
register handlers.

%prep
%setup -q
%patch0 -p1 -b .xmlwfargs
%patch1 -p1 -b .cve0718

%build
rm -rf autom4te*.cache
libtoolize --copy --force --automake && aclocal && autoheader && autoconf
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}

chmod 644 COPYING

make install DESTDIR=$RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_libdir}/lib*.so.*

%exclude %{_includedir}
%exclude %{_mandir}
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Thu Nov 24 2016 Joe Orton <jorton@redhat.com> - 2.1.0-10
- updated security fix for CVE-2016-0718

* Thu Nov 24 2016 Joe Orton <jorton@redhat.com> - 2.1.0-9
- add security fix for CVE-2016-0718

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.1.0-8
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.1.0-7
- Mass rebuild 2013-12-27

* Mon Jun 17 2013 Joe Orton <jorton@redhat.com> - 2.1.0-6
- fix "xmlwf -h" output (#948534)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 13 2012 Joe Orton <jorton@redhat.com> - 2.1.0-3
- add -static subpackage (#722647)

* Fri Mar 30 2012 Joe Orton <jorton@redhat.com> - 2.1.0-1
- ship .pc file, move library back to libdir (#808399)

* Mon Mar 26 2012 Joe Orton <jorton@redhat.com> - 2.1.0-1
- update to 2.1.0 (#806602)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  8 2010 Joe Orton <jorton@redhat.com> - 2.0.1-10
- revised fix for CVE-2009-3560 regression (#544996)

* Sun Jan 31 2010 Joe Orton <jorton@redhat.com> - 2.0.1-9
- drop static libraries (#556046)
- add fix for regression in CVE-2009-3560 patch (#544996)

* Tue Dec  1 2009 Joe Orton <jorton@redhat.com> - 2.0.1-8
- add security fix for CVE-2009-3560 (#533174)
- add security fix for CVE-2009-3720 (#531697)
- run the test suite

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.1-5
- Autorebuild for GCC 4.3

* Wed Jan 23 2008 Joe Orton <jorton@redhat.com> 2.0.1-4
- chmod 644 even more documentation (#429806)

* Tue Jan  8 2008 Joe Orton <jorton@redhat.com> 2.0.1-3
- chmod 644 the documentation (#427950)

* Wed Aug 22 2007 Joe Orton <jorton@redhat.com> 2.0.1-2
- rebuild

* Wed Aug  8 2007 Joe Orton <jorton@redhat.com> 2.0.1-1
- update to 2.0.1
- fix the License tag
- drop the .la file

* Sun Feb  4 2007 Joe Orton <jorton@redhat.com> 1.95.8-10
- remove trailing dot in Summary (#225742)
- use preferred BuildRoot per packaging guidelines (#225742)

* Tue Jan 30 2007 Joe Orton <jorton@redhat.com> 1.95.8-9
- regenerate configure/libtool correctly (#199361)
- strip DSP files from examples (#186889)
- fix expat.h compilation with g++ -pedantic (#190244)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.95.8-8.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.95.8-8.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.95.8-8.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Joe Orton <jorton@redhat.com> 1.95.8-8
- restore .la file for apr-util

* Mon Jan 30 2006 Joe Orton <jorton@redhat.com> 1.95.8-7
- move library to /lib (#178743)
- omit .la file (#170031)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Mar  8 2005 Joe Orton <jorton@redhat.com> 1.95.8-6
- rebuild

* Thu Nov 25 2004 Ivana Varekova <varekova@redhat.com> 1.95.8
- update to 1.95.8

* Wed Jun 16 2004 Jeff Johnson <jbj@jbj.org> 1.95.7-4
- add -fPIC (#125586).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jun 11 2004 Jeff Johnson <jbj@jbj.org> 1.95.7-2
- fix: malloc failure from dbus test suite (#124747).

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Feb 22 2004 Joe Orton <jorton@redhat.com> 1.95.7-1
- update to 1.95.7, include COPYING file in main package

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Sep 17 2003 Matt Wilson <msw@redhat.com> 1.95.5-6
- rebuild again for #91211

* Tue Sep 16 2003 Matt Wilson <msw@redhat.com> 1.95.5-5
- rebuild to fix gzip'ed file md5sums (#91211)

* Tue Jun 17 2003 Jeff Johnson <jbj@redhat.com> 1.95.5-4
- rebuilt because of crt breakage on ppc64.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Nov 11 2002 Jeff Johnson <jbj@redhat.com> 1.95.5-1
- update to 1.95.5.

* Mon Aug 19 2002 Trond Eivind Glomsrød <teg@redhat.com> 1,95.4-1
- 1.95.4. 1.95.3 was withdrawn by the expat developers.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jun  6 2002 Trond Eivind Glomsrød <teg@redhat.com> 1,95.3-1
- 1.95.3

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Mar 22 2002 Trond Eivind Glomsrød <teg@redhat.com>
- Change a prereq in -devel on main package to a req
- License from MIT/X11 to BSD

* Mon Mar 13 2002 Trond Eivind Glomsrød <teg@redhat.com>
- 1.95.2

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Tue Oct 24 2000 Jeff Johnson <jbj@redhat.com>
- update to 1.95.1

* Sun Oct  8 2000 Jeff Johnson <jbj@redhat.com>
- Create.
