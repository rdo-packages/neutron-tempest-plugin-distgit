%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0xa7475c5f2122fec3f90343223fe3bf5aad1080e4
%global service neutron
%global plugin neutron-tempest-plugin
%global module neutron_tempest_plugin
%global with_doc 1


%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
This package contains Tempest tests to cover the Neutron project. \
Additionally it provides a plugin to automatically load these tests into Tempest.

Name:       python-%{service}-tests-tempest
Version:    2.1.0
Release:    1%{?dist}
Summary:    Tempest Integration of Neutron Project
License:    ASL 2.0
URL:        https://git.openstack.org/cgit/openstack/%{plugin}/

Source0:    http://tarballs.openstack.org/%{plugin}/%{plugin}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        http://tarballs.openstack.org/%{plugin}/%{plugin}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  git-core
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python3-%{service}-tests-tempest
Summary: %{summary}
%{?python_provide:%python_provide python3-%{service}-tests-tempest}

Obsoletes: python-neutron-tests < 1:12.0.0

Provides: python3-networking-bgpvpn-tests-tempest = %{version}-%{release}
Provides: python-networking-bgpvpn-tests-tempest = %{version}-%{release}
Obsoletes: python3-networking-bgpvpn-tests-tempest

Provides: python3-networking-sfc-tests-tempest = 9.0.0-%{release}
Provides: python-networking-sfc-tests-tempest = 9.0.0-%{release}
Obsoletes: python3-networking-sfc-tests-tempest < 9.0.0

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools

Requires:   python3-ddt >= 1.0.1
Requires:   python3-eventlet >= 0.20.1
Requires:   python3-netaddr >= 0.7.19
Requires:   python3-debtcollector >= 1.2.0
Requires:   python3-neutron-lib >= 1.25.0
Requires:   python3-os-ken >= 0.3.0
Requires:   python3-oslo-config >= 2:5.2.0
Requires:   python3-oslo-log >= 3.36.0
Requires:   python3-oslo-serialization >= 2.18.0
Requires:   python3-oslo-utils >= 3.33.0
Requires:   python3-paramiko >= 2.0.0
Requires:   python3-pbr >= 3.3.1
Requires:   python3-six  >= 1.10.0
Requires:   python3-tempest >= 1:18.0.0
Requires:   python3-testtools >= 2.2.0
Requires:   python3-testscenarios >= 0.5.0
Requires:   python3-tenacity >= 3.2.1
Requires:   nmap

%description -n python3-%{service}-tests-tempest
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{service}-tests-tempest-doc
Summary:        Documentation for python-%{service}-tests-tempest

BuildRequires:  python3-sphinx
BuildRequires:  python3-openstackdocstheme

%description -n python-%{service}-tests-tempest-doc
It contains the documentation for the Neutron tempest plugin.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{plugin}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup
# Remove bundled egg-info
rm -rf %{module}.egg-info

%build
%{py3_build}

# Generate Docs
%if 0%{?with_doc}
sphinx-build -W -b html doc/source doc/build/html
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

%files -n python3-%{service}-tests-tempest
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{module}
%{python3_sitelib}/*.egg-info

%if 0%{?with_doc}
%files -n python-%{service}-tests-tempest-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Mon Feb 06 2023 RDO <dev@lists.rdoproject.org> 2.1.0-1
- Update to 2.1.0

* Wed Sep 28 2022 RDO <dev@lists.rdoproject.org> 2.0.0-1
- Update to 2.0.0

