# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global with_doc 1

%global sname barbicanclient

%global common_desc \
This is a client for the Barbican Key Management API. There is a \
Python library for accessing the API (barbicanclient module), and \
a command-line script (barbican).

Name:           python-barbicanclient
Version:        XXX
Release:        XXX
Summary:        Client Library for OpenStack Barbican Key Management API

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/python-barbicanclient
Source0:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch:      noarch

BuildRequires:  git
%description
%{common_desc}

%package -n python%{pyver}-%{sname}
Summary:        Client Library for OpenStack Barbican Key Management API
%{?python_provide:%python_provide python%{pyver}-%{sname}}
%if %{pyver} == 3
Obsoletes: python2-%{sname} < %{version}-%{release}
%endif

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools
Requires:       python%{pyver}-requests
Requires:       python%{pyver}-six >= 1.10.0
Requires:       python%{pyver}-oslo-i18n >= 3.15.3
Requires:       python%{pyver}-oslo-serialization >= 2.18.0
Requires:       python%{pyver}-oslo-utils >= 3.33.0
Requires:       python%{pyver}-prettytable
Requires:       python%{pyver}-keystoneauth1 >= 3.4.0
Requires:       python%{pyver}-pbr >= 2.0.0
Requires:       python%{pyver}-cliff

%description -n python%{pyver}-%{sname}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{sname}-doc
Summary: Documentation for OpenStack Barbican API client

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-oslo-utils
BuildRequires:  python%{pyver}-oslo-i18n
BuildRequires:  python%{pyver}-prettytable

%description -n python-%{sname}-doc
Documentation for the barbicanclient module
%endif

%prep
%autosetup -n %{name}-%{upstream_version} -S git
# let RPM handle deps
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

rm -rf {test-,}requirements.txt

%build
%{pyver_build}

%if 0%{?with_doc}
# doc
%{pyver_bin} setup.py build_sphinx -b html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.buildinfo
%endif

%install
%{pyver_install}
ln -s ./barbican %{buildroot}%{_bindir}/barbican-%{pyver}

%files -n python%{pyver}-%{sname}
%license LICENSE
%doc AUTHORS CONTRIBUTING.rst README.rst PKG-INFO ChangeLog
%{_bindir}/barbican
%{_bindir}/barbican-%{pyver}
%{pyver_sitelib}/barbicanclient
%{pyver_sitelib}/python_barbicanclient-%{upstream_version}-py?.?.egg-info

%if 0%{?with_doc}
%files -n python-%{sname}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/python-barbicanclient/commit/?id=e5fdd10f04488d6f6e252a63c57bf2be92a06c8f
