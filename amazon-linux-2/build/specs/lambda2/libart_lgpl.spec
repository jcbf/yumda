Summary: Library of graphics routines used by libgnomecanvas
Name: libart_lgpl
Version: 2.3.21
Release: 10%{?dist}.0.2
URL: http://www.gnome.org/
Source0: http://ftp.gnome.org/pub/gnome/sources/libart_lgpl/2.3/%{name}-%{version}.tar.bz2
#Fedora specific patch
Patch0: libart-multilib.patch
License: LGPLv2+
Group: System Environment/Libraries 
BuildRequires: automake autoconf
BuildRequires: pkgconfig
BuildRequires: libtool

Prefix: %{_prefix}

%description
Graphics routines used by the GnomeCanvas widget and some other 
applications. libart renders vector paths and the like.

%prep
%setup -q
%patch0 -p1 -b .multilib

%build
libtoolize
autoreconf
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%files
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/lib*.so.*

%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_bindir}/libart2-config
%exclude %{_includedir}

%changelog
* Sun Nov 3 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Mon Aug 18 2014 Peter Robinson <probinson@redhat.com> - 2.3.21-10
- Generic 32/64 bit platform detection - fix ppc64le build

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.3.21-9
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.3.21-8
- Mass rebuild 2013-12-27

* Tue Jun 18 2013 Jochen Schmitt <Jochen herr-schmitt de> - 2.3.21-7
- Add aarch64 as a 65-Bit architecture (#975267)
- Add libtool as a BR
- Call libtoolize before autoreconf

* Fri Mar 29 2013 Jochen Schmitt <Jochen herr-schmitt de> - 2.3.21-6
- Try to fix aarch64 build issue (#925666)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 24 2010 Parag Nemade <paragn AT fedoraproject.org> - 2.3.21-2
- Merge-review cleanup (#225987)

* Wed Jul  7 2010 Jochen Schmitt <Jochen herr-schmitt de> - 2.3.21-1
- New upstream release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 13 2009 Caolán McNamara <caolanm@redhat.com> - 2.3.20-3
- rebuild to get provides pkgconfig(libart-2.0)

* Mon May 26 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.3.20-2
- add sparc64 for multilib

* Wed Jan 30 2008 Matthias Clasen <mclasen@redhat.com> - 2.3.20-1
- Update to 2.3.20
- Drop upstreamed patch
- Correct license field

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 2.3.19-3
- Rebuild for build ID

* Thu Mar 01 2007 Behdad Esfahbod <besfahbo@edhat.com> - 2.3.19-2
- Add upstreamed patch libart-2.3.19-header.patch
- Resolves: #230571

* Wed Feb 28 2007 Matthias Clasen <mclasen@redhat.com> - 2.3.19-1
- Update to 2.3.19

* Tue Feb 27 2007 Matthias Clasen <mclasen@redhat.com> - 2.3.18-1
- Update to 2.3.18

* Mon Jul 31 2006 Jesse Keating <jkeating@redhat.com> - 2.3.17-4
- Fix typo in header name

* Thu Jul 27 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.17-3
- Fix multilib conflicts
- Don't ship static libraries

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.3.17-2.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.3.17-2.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.3.17-2.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com> 2.3.17-2
- Rebuild with gcc4

* Wed Jan 26 2005 Matthias Clasen <mclasen@redhat.com> 2.3.17-1
- update to 2.3.17

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Oct  6 2003 Alexander Larsson <alexl@redhat.com> 2.3.16-1
- 2.3.16

* Tue Aug 12 2003 Alexander Larsson <alexl@redhat.com> 2.3.14-1
- 2.3.14

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Dec  9 2002 Alexander Larsson <alexl@redhat.com> 2.3.11
- Update to 2.3.11

* Tue Dec 03 2002 Elliot Lee <sopwith@redhat.com> 2.3.10-2
- Remove unpackaged file

* Sat Jul 27 2002 Havoc Pennington <hp@redhat.com>
- 2.3.10, required by nautilus 2.0.2 for some reason

* Mon Jun 24 2002 Havoc Pennington <hp@redhat.com>
- 2.3.9, should give gdm login screen a kick in the ass

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri May 17 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Wed Apr 24 2002 Havoc Pennington <hp@redhat.com>
 - rebuild in different environment

* Thu Apr  4 2002 Jeremy Katz <katzj@redhat.com>
- rebuild

* Thu Jan 24 2002 Havoc Pennington <hp@redhat.com>
- actually increase version to 2.3.8

* Thu Jan 24 2002 Havoc Pennington <hp@redhat.com>
- upgrade to 2.3.8 so header files don't break eel2

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan  2 2002 Havoc Pennington <hp@redhat.com>
- 2.3.7.91 snap

* Sun Nov 25 2001 Havoc Pennington <hp@redhat.com>
- cvs snap, rebuild with new glib

* Thu Oct  4 2001 Havoc Pennington <hp@redhat.com>
- 2.3.6

* Fri Sep 21 2001 Havoc Pennington <hp@redhat.com>
- new CVS snap with upstream changes merged

* Thu Sep 13 2001 Havoc Pennington <hp@redhat.com>
- Initial build.


