%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname barbicanclient

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-barbicanclient
Version:        XXX
Release:        XXX
Summary:        Client Library for OpenStack Barbican Key Management API

License:        ASL 2.0
URL:            https://bugs.launchpad.net/python-barbicanclient
Source0:        http://tarballs.openstack.org/python-barbicanclient/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch

%description
This is a client for the Barbican Key Management API. There is a
Python library for accessing the API (barbicanclient module), and
a command-line script (barbican).

%package -n python2-%{sname}
Summary:        Client Library for OpenStack Barbican Key Management API
%{?python_provide:%python_provide python2-%{sname}}

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools

Requires:       python-setuptools
Requires:       python-requests
Requires:       python-six >= 1.9.0
Requires:       python-keystoneclient
Requires:       python-cliff
Requires:       python-oslo-i18n
Requires:       python-oslo-serialization
Requires:       python-oslo-utils

%description -n python2-%{sname}
This is a client for the Barbican Key Management API. There is a
Python library for accessing the API (barbicanclient module), and
a command-line script (barbican).

%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:        Client Library for OpenStack Barbican Key Management API
%{?python_provide:%python_provide python3-%{sname}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools

Requires:       python3-setuptools
Requires:       python3-requests
Requires:       python3-six >= 1.9.0
Requires:       python3-keystoneclient
Requires:       python3-cliff
Requires:       python3-oslo-i18n
Requires:       python3-oslo-serialization
Requires:       python3-oslo-utils

%description -n python3-%{sname}
This is a client for the Barbican Key Management API. There is a
Python library for accessing the API (barbicanclient module), and
a command-line script (barbican).
%endif

%package doc
Summary: Documentation for OpenStack Barbican API client

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx

%description doc
Documentation for the barbicanclient module

%prep
%setup -q -n %{name}-%{upstream_version}

rm -rf {test-,}requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/barbican %{buildroot}%{_bindir}/barbican-%{python3_version}
ln -s ./barbican-%{python3_version} %{buildroot}%{_bindir}/barbican-3
# Delete tests
rm -fr %{buildroot}%{python3_sitelib}/barbicanclient/tests
%endif

%py2_install
mv %{buildroot}%{_bindir}/barbican %{buildroot}%{_bindir}/barbican-%{python2_version}
ln -s ./barbican-%{python2_version} %{buildroot}%{_bindir}/barbican-2

ln -s ./barbican-2 %{buildroot}%{_bindir}/barbican

# Delete tests
rm -fr %{buildroot}%{python2_sitelib}/barbicanclient/tests


export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html

%files -n python2-%{sname}
%doc README.rst
%license LICENSE
%{python2_sitelib}/%{sname}
%{python2_sitelib}/*.egg-info
%{_bindir}/barbican
%{_bindir}/barbican-2
%{_bindir}/barbican-%{python2_version}

%if 0%{?with_python3}
%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sname}
%{python3_sitelib}/*.egg-info
%{_bindir}/barbican-3
%{_bindir}/barbican-%{python3_version}
%endif

%files doc
%doc html
%license LICENSE

%changelog
