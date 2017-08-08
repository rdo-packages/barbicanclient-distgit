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
URL:            https://pypi.python.org/pypi/python-barbicanclient
Source0:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch:      noarch


%description
This is a client for the Barbican Key Management API. There is a
Python library for accessing the API (barbicanclient module), and
a command-line script (barbican).


%package -n python2-%{sname}
Summary:        Client Library for OpenStack Barbican Key Management API

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git

Requires:       python-requests
Requires:       python-six >= 1.9.0
Requires:       python-cliff
Requires:       python-oslo-i18n >= 2.1.0
Requires:       python-oslo-serialization >= 1.10.0
Requires:       python-oslo-utils >= 3.20.0
Requires:       python-prettytable
Requires:       python-keystoneauth1 >= 3.1.0
Requires:       python-pbr >= 2.0.0

%{?python_provide:%python_provide python2-%{sname}}

%description -n python2-%{sname}
This is a client for the Barbican Key Management API. There is a
Python library for accessing the API (barbicanclient module), and
a command-line script (barbican).


%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:        Client Library for OpenStack Barbican Key Management API

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools

Requires:       python3-requests
Requires:       python3-six >= 1.9.0
Requires:       python3-cliff
Requires:       python3-oslo-i18n >= 2.1.0
Requires:       python3-oslo-serialization >= 1.10.0
Requires:       python3-oslo-utils >= 3.20.0
Requires:       python3-prettytable
Requires:       python3-keystoneauth1 >= 3.1.0
Requires:       python3-pbr >= 2.0.0

%{?python_provide:%python_provide python3-%{sname}}

%description -n python3-%{sname}
This is a client for the Barbican Key Management API. There is a
Python library for accessing the API (barbicanclient module), and
a command-line script (barbican).
%endif


%package doc
Summary: Documentation for OpenStack Barbican API client

BuildRequires:  python-sphinx
BuildRequires:  python-openstackdocstheme
BuildRequires:  python-oslo-utils
BuildRequires:  dos2unix
BuildRequires:  python-oslo-i18n
BuildRequires:  python-prettytable

%description doc
Documentation for the barbicanclient module

%prep
%autosetup -n %{name}-%{upstream_version} -S git
# let RPM handle deps
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

rm -rf {test-,}requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# doc
export PYTHONPATH="$( pwd ):$PYTHONPATH"
%{__python2} setup.py build_sphinx -b html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.buildinfo

%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/barbican %{buildroot}%{_bindir}/barbican-%{python3_version}
ln -s ./barbican-%{python3_version} %{buildroot}%{_bindir}/barbican-3
%endif

%py2_install
mv %{buildroot}%{_bindir}/barbican %{buildroot}%{_bindir}/barbican-%{python2_version}
ln -s ./barbican-%{python2_version} %{buildroot}%{_bindir}/barbican-2

ln -s ./barbican-2 %{buildroot}%{_bindir}/barbican

dos2unix doc/build/html/_static/jquery.js


%files -n python2-%{sname}
%license LICENSE
%doc AUTHORS CONTRIBUTING.rst README.rst PKG-INFO ChangeLog
%{_bindir}/barbican
%{_bindir}/barbican-2*
%{python2_sitelib}/barbicanclient
%{python2_sitelib}/python_barbicanclient-%{upstream_version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{sname}
%license LICENSE
%doc AUTHORS CONTRIBUTING.rst README.rst PKG-INFO ChangeLog
%{_bindir}/barbican-3*
%{python3_sitelib}/barbicanclient
%{python3_sitelib}/python_barbicanclient-%{upstream_version}-py?.?.egg-info
%endif

%files doc
%doc doc/build/html
%license LICENSE

%changelog
