%global service neutron
%global plugin neutron-tempest-plugin
%global module neutron_tempest_plugin
%global with_doc 1

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

%global common_desc \
This package contains Tempest tests to cover the Neutron project. \
Additionally it provides a plugin to automatically load these tests into Tempest.

Name:       python-%{service}-tests-tempest
Version:    0.9.0
Release:    2%{?dist}
Summary:    Tempest Integration of Neutron Project
License:    ASL 2.0
URL:        https://git.openstack.org/cgit/openstack/%{plugin}/

Source0:    http://tarballs.openstack.org/%{plugin}/%{plugin}-%{upstream_version}.tar.gz

BuildArch:  noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python%{pyver}-%{service}-tests-tempest
Summary: %{summary}
%{?python_provide:%python_provide python%{pyver}-%{service}-tests-tempest}

Obsoletes: python-neutron-tests < 1:12.0.0

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools

Requires:   python%{pyver}-ddt >= 1.0.1
Requires:   python%{pyver}-eventlet >= 0.20.1
%if %{pyver} == 2
Requires:   python-ipaddress
Requires:   python-netaddr >= 0.7.19
%else
Requires:   python%{pyver}-netaddr >= 0.7.19
%endif
Requires:   python%{pyver}-debtcollector >= 1.2.0
Requires:   python%{pyver}-neutron-lib >= 1.25.0
Requires:   python%{pyver}-os-ken >= 0.3.0
Requires:   python%{pyver}-oslo-config >= 2:5.2.0
Requires:   python%{pyver}-oslo-log >= 3.36.0
Requires:   python%{pyver}-oslo-serialization >= 2.18.0
Requires:   python%{pyver}-oslo-utils >= 3.33.0
Requires:   python%{pyver}-paramiko >= 2.0.0
Requires:   python%{pyver}-pbr >= 3.3.1
Requires:   python%{pyver}-six  >= 1.10.0
Requires:   python%{pyver}-tempest >= 1:18.0.0
Requires:   python%{pyver}-testtools >= 1.8.0
Requires:   python%{pyver}-testscenarios >= 0.5.0

%if %{pyver} == 2
Requires:   python-ipaddress >= 1.0.17
%endif

%description -n python%{pyver}-%{service}-tests-tempest
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{service}-tests-tempest-doc
Summary:        python-%{service}-tests-tempest documentation

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-openstackdocstheme

%description -n python-%{service}-tests-tempest-doc
It contains the documentation for the Neutron tempest plugin.
%endif

%prep
%autosetup -n %{plugin}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup
# Remove bundled egg-info
rm -rf %{module}.egg-info

%build
%{pyver_build}

# Generate Docs
%if 0%{?with_doc}
%{pyver_bin} setup.py build_sphinx -b html
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

%files -n python%{pyver}-%{service}-tests-tempest
%license LICENSE
%doc README.rst
%{pyver_sitelib}/%{module}
%{pyver_sitelib}/*.egg-info

%if 0%{?with_doc}
%files -n python-%{service}-tests-tempest-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Mon Mar 30 2020 Yatin Karel <ykarel@redhat.com> - 0.9.0-2
- Add dep on os-ken explicitly

* Mon Mar 23 2020 RDO <dev@lists.rdoproject.org> 0.9.0-1
- Update to 0.9.0

* Wed Aug 14 2019 RDO <dev@lists.rdoproject.org> 0.5.0-1
- Update to 0.5.0

* Mon Jul 29 2019 RDO <dev@lists.rdoproject.org> 0.4.0-1
- Update to 0.4.0

* Thu Mar 28 2019 RDO <dev@lists.rdoproject.org> 0.3.0-1
- Update to 0.3.0

