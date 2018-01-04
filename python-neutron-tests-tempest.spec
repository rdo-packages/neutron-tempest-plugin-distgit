%global service neutron
%global plugin neutron-tempest-plugin
%global module neutron_tempest_plugin
%global with_doc 1

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora}
%global with_python3 1
%endif

%global common_desc \
This package contains Tempest tests to cover the Neutron project. \
Additionally it provides a plugin to automatically load these tests into Tempest.

Name:       python-%{service}-tests-tempest
Version:    XXX
Release:    XXX
Summary:    Tempest Integration of Neutron Project
License:    ASL 2.0
URL:        https://git.openstack.org/cgit/openstack/%{plugin}/

Source0:    http://tarballs.openstack.org/%{plugin}/%{plugin}-%{upstream_version}.tar.gz

BuildArch:  noarch

%description
%{common_desc}

%package -n python2-%{service}-tests-tempest
Summary: %{summary}
%{?python_provide:%python_provide python2-%{service}-tests-tempest}
BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git
BuildRequires:  openstack-macros

Requires:   python-ddt >= 1.0.1
Requires:   python-eventlet >= 0.18.2
Requires:   python-netaddr >= 0.7.13
Requires:   python-neutron-lib >= 1.9.0
Requires:   python-oslo-config >= 2:4.0.0
Requires:   python-oslo-log >= 3.22.0
Requires:   python-oslo-serialization >= 1.10.0
Requires:   python-oslo-utils >= 3.20.0
Requires:   python-pbr >= 2.0
Requires:   python-six  >= 1.9.0
Requires:   python-tempest >= 1:16.0.0
Requires:   python-testtools >= 1.4.0
Requires:   python-testscenarios >= 0.4

%description -n python2-%{service}-tests-tempest
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{service}-tests-tempest-doc
Summary:        python-%{service}-tests-tempest documentation

BuildRequires:  python-sphinx
BuildRequires:  python-openstackdocstheme

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
Requires:   python3-netaddr >= 0.7.13
Requires:   python3-neutron-lib >= 1.9.0
Requires:   python3-oslo-config >= 4.0.0
Requires:   python3-oslo-log >= 3.22.0
Requires:   python3-oslo-serialization >= 1.10.0
Requires:   python3-oslo-utils >= 3.20.0
Requires:   python3-pbr >= 2.0
Requires:   python3-six  >= 1.9.0
Requires:   python3-tempest >= 1:16.0.0
Requires:   python3-testtools >= 1.4.0
Requires:   python3-testscenarios >= 0.4

%description -n python3-%{service}-tests-tempest
%{common_desc}
%endif

%prep
%autosetup -n %{module}-%{upstream_version} -S git

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
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/neutron-tempest-plugin/commit/?id=c7afa073b4b9f3061ef75f20a1fc7f31e14fab47
