%global cpan_version 3.40
Name:           perl-PathTools
Version:        %(echo '%{cpan_version}' | tr _ .)
Release: 5%{?dist}.0.2
Summary:        PathTools Perl module (Cwd, File::Spec)
License:        (GPL+ or Artistic) and BSD
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/PathTools/
Source0:        http://www.cpan.org/authors/id/S/SM/SMUELLER/PathTools-%{cpan_version}.tar.gz
# Disable VMS test (bug #973713)
Patch0:         PathTools-3.40-Disable-VMS-tests.patch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
# File::Basename not needed because of removed File::Spec::VMS
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Tests:
BuildRequires:  perl(Carp::Heavy)
BuildRequires:  perl(Config)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Carp)
Requires:       perl(Scalar::Util)

%{?perl_default_filter}

Prefix: %{_prefix}

%description
This is the combined distribution for the File::Spec and Cwd modules.

%prep
%setup -q -n PathTools-%{cpan_version}
%patch0 -p1
# Remove bundled modules
rm -r t/lib
sed -i -e '/^t\/lib\//d' MANIFEST
# Do not distribute File::Spec::VMS as it works on VMS only (bug #973713)
rm lib/File/Spec/VMS.pm
sed -i -e '/^lib\/File\/Spec\/VMS.pm/d' MANIFEST

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS" \
  PREFIX=%{_prefix} \
  INSTALLVENDORLIB=%{perl_vendorlib} \
  INSTALLVENDORARCH=%{perl_vendorarch}
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%files
%license README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Cwd.pm
%{perl_vendorarch}/File/

%exclude %{_mandir}

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.40-5
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.40-4
- Mass rebuild 2013-12-27

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 3.40-3
- Disable VMS test (bug #973713)

* Fri Jun 14 2013 Petr Pisar <ppisar@redhat.com> - 3.40-2
- Do not distribute File::Spec::VMS (bug #973713)

* Mon Feb 04 2013 Petr Pisar <ppisar@redhat.com> - 3.40-1
- 3.40 bump

* Tue Sep 18 2012 Petr Pisar <ppisar@redhat.com> - 3.39.01-1
- 3.39_01 bump

* Wed Aug 15 2012 Petr Pisar <ppisar@redhat.com> - 3.33-8
- Specify all dependencies

* Wed Aug 15 2012 Daniel Mach <dmach@redhat.com> - 3.33-7.1
- Rebuild for perl 5.16

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.33-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 3.33-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.33-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 25 2011 Petr Pisar <ppisar@redhat.com> - 3.33-4
- RPM 4.9 dependency filtering added

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.33-3
- Perl mass rebuild

* Sun May 29 2011 Ville Skyttä <ville.skytta@iki.fi> - 3.33-2
- Own the %%{perl_vendorarch}/File dir.

* Mon Feb 28 2011 Marcela Mašláňová <mmaslano@redhat.com> 3.33-1
- Specfile autogenerated by cpanspec 1.79.
