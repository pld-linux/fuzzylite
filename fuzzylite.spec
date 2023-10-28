#
# Conditional build:
%bcond_without	static_libs	# static libraries
#
Summary:	A Fuzzy Logic Control Library in C++
Name:		fuzzylite
Version:	6.0
Release:	1
License:	GPL v3
Group:		Libraries
Source0:	https://github.com/fuzzylite/fuzzylite/archive/refs/tags/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	34f3e1b27aa2abd9210b7d90f9d45785
Patch0:		cxxflags.patch
Patch1:		soname.patch
Patch2:		libdir.patch
URL:		https://github.com/fuzzylite/fuzzylite/
BuildRequires:	cmake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The goal of the FuzzyLite Libraries is to easily design and
efficiently operate fuzzy logic controllers following an
object-oriented programming model without relying on external
libraries.

%package common
Summary:	Common files for %{name} library
Summary(pl.UTF-8):	Wspólne pliki biblioteki %{name}
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description common
Common files for %{name} library.

%description common -l pl.UTF-8
Wspólne pliki biblioteki %{name}.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
mkdir -p build
cd build
%cmake ../fuzzylite \
	%cmake_on_off static_libs FL_BUILD_STATIC \
	-DFL_BUILD_TESTS=NO

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHOR README.md THANKS
%attr(755,root,root) %{_libdir}/libfuzzylite.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libfuzzylite.so.6

%files common
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/fuzzylite

%files devel
%defattr(644,root,root,755)
%doc CHANGELOG NEWS
%attr(755,root,root) %{_libdir}/libfuzzylite.so
%{_includedir}/fl
%{_pkgconfigdir}/fuzzylite.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfuzzylite.a
%endif
