%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x815AFEC729392386480E076DCC0DFE2D21C023C9
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

%global with_doc 1

%global sname barbicanclient

%global common_desc \
This is a client for the Barbican Key Management API. There is a \
Python library for accessing the API (barbicanclient module), and \
a command-line script (barbican).

Name:           python-barbicanclient
Version:        5.6.0
Release:        1%{?dist}
Summary:        Client Library for OpenStack Barbican Key Management API

License:        Apache-2.0
URL:            https://pypi.python.org/pypi/python-barbicanclient
Source0:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

BuildRequires:  git-core
%description
%{common_desc}

%package -n python3-%{sname}
Summary:        Client Library for OpenStack Barbican Key Management API

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
%description -n python3-%{sname}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{sname}-doc
Summary: Documentation for OpenStack Barbican API client

BuildRequires:  python3-sphinxcontrib-rsvgconverter

%description -n python-%{sname}-doc
Documentation for the barbicanclient module
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{name}-%{upstream_version} -S git


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# doc
%tox -e docs
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.buildinfo
%endif

%install
%pyproject_install
ln -s ./barbican %{buildroot}%{_bindir}/barbican-3

%files -n python3-%{sname}
%license LICENSE
%doc AUTHORS CONTRIBUTING.rst README.rst PKG-INFO ChangeLog
%{_bindir}/barbican
%{_bindir}/barbican-3
%{python3_sitelib}/barbicanclient
%{python3_sitelib}/python_barbicanclient-%{upstream_version}.dist-info

%if 0%{?with_doc}
%files -n python-%{sname}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Wed Sep 13 2023 RDO <dev@lists.rdoproject.org> 5.6.0-1
- Update to 5.6.0

