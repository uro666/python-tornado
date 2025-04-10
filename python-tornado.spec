%define module tornado
%bcond_without test
# disabled doc generation due to build issue
# left it behind the conditional for a revisit
%bcond_with docs

Name:		python-tornado
Version:	6.4.2
Release:	1
Summary:	Scalable, non-blocking web server and tools
Group:		Development/Python
License:	Apache-2.0
URL:		https://www.tornadoweb.org
Source0:	https://files.pythonhosted.org/packages/source/t/tornado/tornado-%{version}.tar.gz
Source1:	%{name}.rpmlintrc
BuildSystem: python

BuildRequires:	gcc-c++
BuildRequires:	python
BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(pycurl)
BuildRequires:	python%{pyver}dist(wheel)
%if %{with docs}
BuildRequires:	python%{pyver}dist(sphinx)
BuildRequires:	python%{pyver}dist(sphinx-rtd-theme)
BuildRequires:	python%{pyver}dist(sphinxcontrib-applehelp)
BuildRequires:	python%{pyver}dist(sphinxcontrib-asyncio)
BuildRequires:	python%{pyver}dist(sphinxcontrib-devhelp)
BuildRequires:	python%{pyver}dist(sphinxcontrib-htmlhelp)
BuildRequires:	python%{pyver}dist(sphinxcontrib-jquery)
BuildRequires:	python%{pyver}dist(sphinxcontrib-jsmath)
BuildRequires:	python%{pyver}dist(sphinxcontrib-qthelp)
BuildRequires:	python%{pyver}dist(sphinxcontrib-serializinghtml)
BuildRequires:	python%{pyver}dist(docutils)
BuildRequires:	python%{pyver}dist(imagesize)
BuildRequires:	python%{pyver}dist(jinja2)
BuildRequires:	python%{pyver}dist(pygments)
BuildRequires:	python%{pyver}dist(requests)
BuildRequires:	python%{pyver}dist(snowballstemmer)
%endif

%description
Tornado is an open source version of the scalable, non-blocking web server and
and tools.

The framework is distinct from most mainstream web server frameworks (and
certainly most Python frameworks) because it is non-blocking and reasonably
fast. Because it is non-blocking and uses epoll, it can handle thousands of
simultaneous standing connections, which means it is ideal for real-time web
services.

%if %{with docs}
%package doc
Summary:        Examples for python-tornado
Group:          Development/Python
Requires:       %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Tornado is an open source version of the scalable, non-blocking web server and
and tools. This package contains some example applications.
%endif

%prep 
%autosetup -n %{module}-%{version} -p1
# Remove bundled egg-info
rm -rf %{module}.egg-info

%build
%py_build
%if %{with docs}
cd docs
sphinx-build -q -E -n -W -b html . build/html
%endif

%install
%py3_install

%if %{with test}
%check
# Skip the same timing-related tests that upstream skips when run in Travis CI.
# https://github.com/tornadoweb/tornado/commit/abc5780a06a1edd0177a399a4dd4f39497cb0c57
export TRAVIS=true
# Increase timeout for tests on riscv64
%ifarch riscv64
	export ASYNC_TEST_TIMEOUT=80
%else
	export ASYNC_TEST_TIMEOUT=30
%endif

%{__python} -m tornado.test.runtests --verbose --fail-if-logs=false

%endif

%files
%{py_platsitedir}/%{module}/
%{py_platsitedir}/%{module}-%{version}.dist-info
%doc README.rst
%license LICENSE

%if %{with docs}
%files doc
%doc docs
%endif
