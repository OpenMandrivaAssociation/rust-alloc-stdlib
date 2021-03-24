%bcond_without check
%global debug_package %{nil}

# The binary is useless
%global __cargo_is_bin() false

%global crate alloc-stdlib

Name:           rust-%{crate}
Version:        0.2.1
Release:        3
Summary:        Dynamic allocator example that may be used with the stdlib

# Upstream license specification: BSD-3-Clause
# * https://github.com/dropbox/rust-alloc-no-stdlib/issues/9
License:        BSD
URL:            https://crates.io/crates/alloc-stdlib
Source:         %{crates_source}

ExclusiveArch:  %{rust_arches}
%if %{__cargo_skip_build}
BuildArch:      noarch
%endif

BuildRequires:  rust-packaging

%global _description %{expand:
Dynamic allocator example that may be used with the stdlib.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages
which use "%{crate}" crate.

%files          devel
%doc README.md
%{cargo_registry}/%{crate}-%{version_no_tilde}/

%package     -n %{name}+default-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+default-devel %{_description}

This package contains library source intended for building other packages
which use "default" feature of "%{crate}" crate.

%files       -n %{name}+default-devel
%ghost %{cargo_registry}/%{crate}-%{version_no_tilde}/Cargo.toml

%package     -n %{name}+unsafe-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+unsafe-devel %{_description}

This package contains library source intended for building other packages
which use "unsafe" feature of "%{crate}" crate.

%files       -n %{name}+unsafe-devel
%ghost %{cargo_registry}/%{crate}-%{version_no_tilde}/Cargo.toml

%prep
%autosetup -n %{crate}-%{version_no_tilde} -p1
# https://github.com/dropbox/rust-alloc-no-stdlib/pull/8
find -type f -name '*.rs' -executable -exec chmod -x '{}' +
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build

%install
%cargo_install

%if %{with check}
%check
%cargo_test
%endif
