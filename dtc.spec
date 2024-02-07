# Copyright 2024 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global source_date_epoch_from_changelog 0

%global _lto_cflags %{?_lto_cflags} -ffat-lto-objects

Name: dtc
Epoch: 100
Version: 1.6.1
Release: 1%{?dist}
Summary: Device Tree Compiler
License: GPL-2.0-or-later
URL: https://github.com/dgibson/dtc/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: bison
BuildRequires: fdupes
BuildRequires: flex
BuildRequires: gcc
BuildRequires: libtool
BuildRequires: make
BuildRequires: meson
BuildRequires: ninja-build
BuildRequires: python-rpm-macros
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: swig

%description
Device Tree Compiler, dtc, takes as input a device-tree in a given
format and outputs a device-tree in another format for booting kernels
on embedded systems.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
%make_build \
    NO_PYTHON=1
python3 ./pylibfdt/setup.py build

%install
%make_install \
    NO_PYTHON=1 \
    PREFIX=/usr \
    DESTDIR=%{buildroot} \
    LIBDIR=%{_libdir}
python3 ./pylibfdt/setup.py install \
    --no-compile \
    --root=%{buildroot}
find %{buildroot}%{python3_sitearch} -type f -name '*.pyc' -exec rm -rf {} \;
fdupes -qnrps %{buildroot}%{python3_sitearch}

%check

%if 0%{?suse_version} > 1500
%package -n libfdt-devel
Summary: Development files for libfdt
Requires: libfdt1 = %{epoch}:%{version}-%{release}

%description -n libfdt-devel
This package provides development files for libfdt.

%package -n libfdt1
Summary: A multi-platform, multi-architecture disassembly framework

%description -n libfdt1
libfdt is a library to process Open Firmware style device trees on
various architectures.

%package -n python%{python3_version_nodots}-libfdt
Summary: Python3 bindings for libfdt
Requires: python3
Requires: libfdt1 = %{epoch}:%{version}-%{release}
Provides: python3-libfdt = %{epoch}:%{version}-%{release}
Provides: python3dist(libfdt) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}-libfdt = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}dist(libfdt) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}-libfdt = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}dist(libfdt) = %{epoch}:%{version}-%{release}

%description -n python%{python3_version_nodots}-libfdt
This package provides python bindings for libfdt.

%post -n libfdt1 -p /sbin/ldconfig
%postun -n libfdt1 -p /sbin/ldconfig

%files
%license GPL
%{_bindir}/*

%files -n libfdt1
%{_libdir}/libfdt-*.so
%{_libdir}/libfdt.so.*

%files -n libfdt-devel
%{_includedir}/*
%{_libdir}/libfdt.a
%{_libdir}/libfdt.so

%files -n python%{python3_version_nodots}-libfdt
%{python3_sitearch}/*
%endif

%if 0%{?sle_version} > 150000
%package -n libfdt-devel
Summary: Development files for libfdt
Requires: libfdt1 = %{epoch}:%{version}-%{release}

%description -n libfdt-devel
This package provides development files for libfdt.

%package -n libfdt1
Summary: A multi-platform, multi-architecture disassembly framework

%description -n libfdt1
libfdt is a library to process Open Firmware style device trees on
various architectures.

%package -n python3-libfdt
Summary: Python3 bindings for libfdt
Requires: python3
Requires: libfdt1 = %{epoch}:%{version}-%{release}
Provides: python3-libfdt = %{epoch}:%{version}-%{release}
Provides: python3dist(libfdt) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}-libfdt = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}dist(libfdt) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}-libfdt = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}dist(libfdt) = %{epoch}:%{version}-%{release}

%description -n python3-libfdt
This package provides python bindings for libfdt.

%post -n libfdt1 -p /sbin/ldconfig
%postun -n libfdt1 -p /sbin/ldconfig

%files
%license GPL
%{_bindir}/*

%files -n libfdt1
%{_libdir}/libfdt-*.so
%{_libdir}/libfdt.so.*

%files -n libfdt-devel
%{_includedir}/*
%{_libdir}/libfdt.a
%{_libdir}/libfdt.so

%files -n python3-libfdt
%{python3_sitearch}/*
%endif

%if !(0%{?suse_version} > 1500) && !(0%{?sle_version} > 150000)
%package -n libfdt
Summary: Device tree library

%description -n libfdt
libfdt is a library to process Open Firmware style device trees on
various architectures.

%package -n libfdt-devel
Summary: Development headers for device tree library
Requires: libfdt = %{epoch}:%{version}-%{release}

%description -n libfdt-devel
This package provides development files for libfdt.

%package -n python3-libfdt
Summary: Python3 bindings for libfdt
Requires: libfdt = %{epoch}:%{version}-%{release}
Requires: python3
Provides: python3-libfdt = %{epoch}:%{version}-%{release}
Provides: python3dist(libfdt) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}-libfdt = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}dist(libfdt) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}-libfdt = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}dist(libfdt) = %{epoch}:%{version}-%{release}

%description -n python3-libfdt
This package provides python bindings for libfdt.

%post -n libfdt -p /sbin/ldconfig
%postun -n libfdt -p /sbin/ldconfig

%files
%license GPL
%{_bindir}/*

%files -n libfdt
%{_libdir}/libfdt-*.so
%{_libdir}/libfdt.so.*

%files -n libfdt-devel
%{_includedir}/*
%{_libdir}/libfdt.a
%{_libdir}/libfdt.so

%files -n python3-libfdt
%{python3_sitearch}/*
%endif

%changelog
