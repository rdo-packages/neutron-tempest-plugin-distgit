%{!?upstream_version: %global upstream_version %{commit}}
%global commit 028c312ab0e32901c282c73fd402b8de874163fc
%global shortcommit %(c=%{commit}; echo ${c:0:7})
# DO NOT REMOVE ALPHATAG
%global alphatag .%{shortcommit}git

%global service neutron
%global plugin neutron-tempest-plugin
%global module neutron_tempest_plugin
# FIXME(ChandanKumar) FIx doc building step
%global with_doc 0

%if 0%{?fedora}
%global with_python3 1
%endif

%global common_desc \
This package contains Tempest tests to cover the Neutron project. \
Additionally it provides a plugin to automatically load these tests into Tempest.

Name:       python-%{service}-tests-tempest
Version:    0.0.1
Release:    0.1%{?alphatag}%{?dist}
Summary:    Tempest Integration of Neutron Project
License:    ASL 2.0
URL:        https://git.openstack.org/cgit/openstack/%{plugin}/

Source0:    http://github.com/openstack/%{plugin}/archive/%{commit}.tar.gz#/%{plugin}-%{shortcommit}.tar.gz

BuildArch:  noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python2-%{service}-tests-tempest
Summary: %{summary}
%{?python_provide:%python_provide python2-%{service}-tests-tempest}

Obsoletes: python-neutron-tests < 1:12.0.0

BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools

Requires:   python2-ddt >= 1.0.1
Requires:   python2-eventlet >= 0.18.2
%if 0%{?fedora} > 0
Requires:   python2-ipaddress
Requires:   python2-netaddr >= 0.7.18
%else
Requires:   python-ipaddress
Requires:   python-netaddr >= 0.7.18
%endif
Requires:   python2-neutron-lib >= 1.9.0
Requires:   python2-oslo-config >= 2:4.0.0
Requires:   python2-oslo-log >= 3.22.0
Requires:   python2-oslo-serialization >= 2.18.0
Requires:   python2-oslo-utils >= 3.20.0
Requires:   python2-pbr >= 2.0
Requires:   python2-six  >= 1.9.0
Requires:   python2-tempest >= 1:17.1.0
Requires:   python2-testtools >= 1.4.0
Requires:   python2-testscenarios >= 0.4

%description -n python2-%{service}-tests-tempest
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{service}-tests-tempest-doc
Summary:        python-%{service}-tests-tempest documentation

BuildRequires:  python2-sphinx
BuildRequires:  python2-openstackdocstheme

%description -n python-%{service}-tests-tempest-doc
It contains the documentation for the Neutron tempest plugin.
%endif

%if 0%{?with_python3}
%package -n python3-%{service}-tests-tempest
Summary: %{summary}
%{?python_provide:%python_provide python3-%{service}-tests-tempest}
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools

Requires:   python3-ddt >= 1.0.1
Requires:   python3-eventlet >= 0.18.2
Requires:   python3-neutron-lib >= 1.9.0
Requires:   python3-netaddr >= 0.7.18
Requires:   python3-oslo-config >= 2:4.0.0
Requires:   python3-oslo-log >= 3.22.0
Requires:   python3-oslo-serialization >= 2.18.0
Requires:   python3-oslo-utils >= 3.20.0
Requires:   python3-pbr >= 2.0
Requires:   python3-six  >= 1.9.0
Requires:   python3-tempest >= 1:17.1.0
Requires:   python3-testtools >= 1.4.0
Requires:   python3-testscenarios >= 0.4

%description -n python3-%{service}-tests-tempest
%{common_desc}
%endif

%prep
# Remove stadium projects tests which are provided by separate packages
rm -rf ${module}/bgpvpn
rm -rf ${module}/sfc
rm -rf ${module}/fwaas

%autosetup -n %{plugin}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup
# Remove bundled egg-info
rm -rf %{module}.egg-info

%build
%if 0%{?with_python3}
%py3_build
%endif
%py2_build

# Generate Docs
%if 0%{?with_doc}
%{__python2} setup.py build_sphinx -b html
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%if 0%{?with_python3}
%py3_install
%endif
%py2_install

%files -n python2-%{service}-tests-tempest
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{module}
%{python2_sitelib}/*.egg-info

%if 0%{?with_python3}
%files -n python3-%{service}-tests-tempest
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{module}
%{python3_sitelib}/*.egg-info
%endif

%if 0%{?with_doc}
%files -n python-%{service}-tests-tempest-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Mon Feb 19 2018 Chandan Kumar <chkumar@redhat.com> 0.0.1-0.1.028c312agit
- Update to pre-release 0.0.1 (028c312ab0e32901c282c73fd402b8de874163fc)
