Summary:        C, C++, Objective C and Objective C++ front-end for the LLVM compiler.
Name:           clang
Version:        12.0.0
Release:        3%{?dist}
License:        NCSA
URL:            http://clang.llvm.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/%{name}-%{version}.src.tar.xz
%define sha512  %{name}=f5613b9bffc962467d3bedb7f66b4e057e2781eb63c5dadfd3cf0b02453e29eff0a4f844889031292f06a8b4c081d4d41c515b7f719826ce5c4209a09df9f1f6

BuildRequires:  cmake
BuildRequires:  llvm-devel = %{version}
BuildRequires:  ncurses-devel
BuildRequires:  zlib-devel
BuildRequires:  libxml2-devel
BuildRequires:  python3-devel

Requires:       libstdc++-devel
Requires:       ncurses
Requires:       llvm
Requires:       zlib
Requires:       libxml2
Requires:       python3

%description
The goal of the Clang project is to create a new C based language front-end:
C, C++, Objective C/C++, OpenCL C and others for the LLVM compiler. You can get and build the source today.

%package        devel
Summary:        Development headers for clang
Requires:       %{name} = %{version}-%{release}
Requires:       ncurses-devel
%description    devel
The clang-devel package contains libraries, header files and documentation for developing applications that use clang.

%prep
%autosetup -p1 -n %{name}-%{version}.src

%build
CPPFLAGS="-Wno-dev"
%cmake \
    -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DLLVM_MAIN_INCLUDE_DIR=%{_includedir} \
    -DBUILD_SHARED_LIBS=OFF

%cmake_build

%install
%cmake_install

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%if 0%{?with_check}
%check
cd %{__cmake_builddir}
make clang-check %{?_smp_mflags}
%endif

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libexecdir}/*
%{_libdir}/*.so.*
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/cmake/*
%{_libdir}/clang/*
%{_includedir}/*

%changelog
* Mon Jun 20 2022 Shreenidhi Shedi <sshedi@vmware.com> 12.0.0-3
- Use cmake macros for build and install
* Wed Nov 17 2021 Nitesh Kumar <kunitesh@vmware.com> 12.0.0-2
- Release bump up to use libxml2 2.9.12-1.
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 12.0.0-1
- Automatic Version Bump
* Tue Mar 16 2021 Michael Paquier <mpaquier@vmware.com> 11.0.1-2
- Addition of required dependency to ncurses-devel for devel package.
* Thu Feb 04 2021 Shreenidhi Shedi <sshedi@vmware.com> 11.0.1-1
- Upgrade to v11.0.1
* Mon Aug 24 2020 Gerrit Photon <photon-checkins@vmware.com> 10.0.1-1
- Automatic Version Bump
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 6.0.1-2
- Build with python3
- Mass removal python2
* Thu Aug 09 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 6.0.1-1
- Update to version 6.0.1 to get it to build with gcc 7.3
* Wed Jun 28 2017 Chang Lee <changlee@vmware.com> 4.0.0-2
- Updated %check
* Fri Apr 7 2017 Alexey Makhalov <amakhalov@vmware.com> 4.0.0-1
- Version update
* Wed Jan 11 2017 Xiaolin Li <xiaolinl@vmware.com>  3.9.1-1
- Initial build.
