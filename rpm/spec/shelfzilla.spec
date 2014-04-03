Summary: M2M Global Service - Portal Common
Name: %{_gs_prefix}portal-common
Version: %{_gs_version}
Release: %{_gs_revision}
License: TID
BuildRoot: %{_topdir}/BUILD/%{name}
BuildArch: noarch
Provides:  %{_gs_prefix}portal-common
Requires: %{_gs_prefix}kermit
Group: M2M Global Services
Distribution: Global Services
Vendor: Telefónica I+D


%description
M2M Portal Common files between initiatives DCA and SmartM2M 

%define _packages_dir /opt/globsrv/apps/m2m-kermit/packages
%define _app_dir %{_packages_dir}/m2m-portal
%define _binaries_in_noarch_packages_terminate_build 0

# Do not check unpackaged files
%undefine __check_files

# -------------------------------------------------------------------------------------------- #
# prep section:
# -------------------------------------------------------------------------------------------- #
# Remove previous build files
%prep
rm -rf  $RPM_BUILD_ROOT*
[ -d $RPM_BUILD_ROOT%{_app_dir} ] || mkdir -p $RPM_BUILD_ROOT%{_app_dir}

# clean up development-only files
find %{_gitdir}/src/ -depth -name .git -exec rm -rf {} \;

# -------------------------------------------------------------------------------------------- #
# install section:
# -------------------------------------------------------------------------------------------- #
%install
# Copy Source Code
cp -r %{_gitdir}/src/* $RPM_BUILD_ROOT%{_app_dir} 
[ -h $RPM_BUILD_ROOT%{_app_dir}/dmm  ] && unlink $RPM_BUILD_ROOT%{_app_dir}/dmm
[ -h $RPM_BUILD_ROOT%{_app_dir}/mc  ] && unlink $RPM_BUILD_ROOT%{_app_dir}/mc

# -------------------------------------------------------------------------------------------- #
# post-install section:
# -------------------------------------------------------------------------------------------- #
%post
chmod -R 775 %{_packages_dir}

# -------------------------------------------------------------------------------------------- #
# pre-uninstall section:
# -------------------------------------------------------------------------------------------- #
%preun


# -------------------------------------------------------------------------------------------- #
# post-uninstall section:
# -------------------------------------------------------------------------------------------- #
%postun

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_app_dir}/*


