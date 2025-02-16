Summary:        OSS implementation of the TCG TPM2 Software Stack (TSS2)
Name:           tpm2-pkcs11
Version:        1.6.0
Release:        3%{?dist}
License:        BSD 2-Clause
URL:            https://github.com/tpm2-software/tpm2-pkcs11
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/tpm2-software/tpm2-pkcs11/releases/download/1.6.0/%{name}-%{version}.tar.gz
%define sha512  tpm2=418fc74db897c5ca2e44d91e9dcb926bbd8009d66f4a31ca72d1fb6f76ee21c36b033750b15921098828ce605ecea1e45e084236db675fcdc56c391dd29f2999

Patch0:         0001-openssl-3.0.0-compatibility.patch

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  openssl-devel
BuildRequires:  tpm2-tools
BuildRequires:  tpm2-tss-devel
BuildRequires:  tpm2-abrmd-devel
BuildRequires:  libyaml-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  sqlite-devel
BuildRequires:  autoconf-archive
BuildRequires:  python3-devel
BuildRequires:  python3-cryptography
BuildRequires:  python3-setuptools
BuildRequires:  python3-PyYAML
BuildRequires:  python3-pyasn1-modules
BuildRequires:  cmocka-devel
BuildRequires:  dbus

Requires:   openssl
Requires:   tpm2-tools
Requires:   tpm2-tss
Requires:   tpm2-abrmd
Requires:   libyaml
Requires:   sqlite-libs

%description
OSS implementation of the TCG TPM2 PKCSv11 Software Stack

%package          tools
Summary:          The tools required to setup and configure TPM2 for PKCSv11
Requires:         %{name} = %{version}-%{release}
Requires:         python3
Requires:         python3-cryptography
Requires:         python3-setuptools
Requires:         python3-pyasn1-modules
Requires:         python3-PyYAML

%description tools
Tools for TCG TPM2 PKCSv11 Software Stack

%prep
%autosetup -p1 -n %{name}-%{version}

%build
sh ./bootstrap
%configure --enable-unit
make %{?_smp_mflags} PACKAGE_VERSION=%{version}

cd tools
python3 setup.py build

%install
# make doesn't support _smp_mflags
make %{?_smp_mflags} DESTDIR=%{buildroot} install

rm %{buildroot}%{_libdir}/pkgconfig/tpm2-pkcs11.pc \
   %{buildroot}%{_libdir}/libtpm2_pkcs11.la

cd tools
python3 setup.py install --root=%{buildroot} --optimize=1 --skip-build

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
cd tools
python3 setup.py test
%endif

%files
%defattr(-,root,root,-)
%license LICENSE
%{_libdir}/libtpm2_pkcs11.so
%{_libdir}/libtpm2_pkcs11.so.0*

%files tools
%defattr(-,root,root,-)
%{_bindir}/tpm2_ptool
%{python3_sitelib}/*

%changelog
* Mon Jun 20 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.6.0-3
- Fix cmocka dependency
* Thu Sep 02 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.6.0-2
- openssl 3.0.0 compatibility
* Sun Aug 8 2021 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.6.0-1
- Initial build. First version
