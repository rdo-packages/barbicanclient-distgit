%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2:        %global __python2 /usr/bin/python2}
%{!?python2_sitelib:  %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif
%{!?_licensedir:%global license %%doc}

Name:           python-barbicanclient
Version:        3.3.0
Release:        1%{?dist}
Summary:        Client Library for OpenStack Barbican Key Management API

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/python-barbicanclient
Source0:        https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch

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
Requires:       python-iso8601
Requires:       python-babel
Requires:       python-oslo-config
Requires:       python-netaddr
Requires:       python-prettytable
Requires:       python-stevedore
Requires:       pyparsing
Requires:       python-cmd2
Requires:       pytz
Requires:       python-msgpack

%description
This is a client for the Barbican Key Management API. There is a
Python library for accessing the API (barbicanclient module), and
a command-line script (barbican).

%package doc
Summary: Documentation for OpenStack Barbican API client

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-oslo-utils
BuildRequires:  dos2unix
BuildRequires:  python-oslo-i18n

%description doc
Documentation for the barbicanclient module

%prep
%setup -q -n %{name}-%{version}
# Remove bundled egg-info
rm -rf %{name}.egg-info
# let RPM handle deps
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py
# make doc build compatible with python-oslo-sphinx RPM
sed -i 's/oslosphinx/oslo.sphinx/' doc/source/conf.py

rm -rf {test-,}requirements.txt

%build
%{__python2} setup.py build
# doc
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html -d build/doctrees   source build/html
popd
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.buildinfo

%install
%{__python2} setup.py install --skip-build --root %{buildroot}
dos2unix doc/build/html/_static/jquery.js


%files
%license LICENSE
%doc AUTHORS CONTRIBUTING.rst README.rst PKG-INFO ChangeLog
%{_bindir}/barbican
%{python2_sitelib}/barbicanclient
%{python2_sitelib}/python_barbicanclient-%{version}-py?.?.egg-info

%files doc
%doc doc/build/html
%license LICENSE

%changelog
* Wed Sep 09 2015 Alan Pevec <alan.pevec@redhat.com> 3.3.0-1
- Update to upstream 3.3.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 02 2015 Chandan Kumar <chkumar246@gmail.com> - 3.0.3-1
- Initial package.
