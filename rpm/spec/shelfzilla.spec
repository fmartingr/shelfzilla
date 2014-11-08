Summary: Shelfzilla
Name: shelfzilla
Version: %{_gs_version}
Release: %{_gs_revision}
BuildRoot: %{_topdir}/BUILD/%{name}
BuildArch: x86_64
Provides: shelfzilla
Requires: python27
License:  Comercial
Group: FDB
Distribution: FDB Global Services
Vendor: FDB

%description
Shelfzilla is a website which save all your Manga

%define _app_dir /opt/shelfzilla
%define _init_path /etc/init.d
%define _binaries_in_noarch_packages_terminate_build 0

# Do not check unpackaged files
%undefine __check_files

# -------------------------------------------------------------------------------------------- #
# prep section:
# -------------------------------------------------------------------------------------------- #
# Remove previous build files
%prep
rm -rf  $RPM_BUILD_ROOT*

# clean up development-only files
find %{_gitdir} -depth -name .git -exec rm -rf {} \;

# -------------------------------------------------------------------------------------------- #
# install section:
# -------------------------------------------------------------------------------------------- #
%install
# Make structure
[ -d $RPM_BUILD_ROOT%{_app_dir} ] || mkdir -p $RPM_BUILD_ROOT%{_app_dir}
[ -d $RPM_BUILD_ROOT%{_app_dir}/config ] || mkdir -p $RPM_BUILD_ROOT%{_app_dir}/config
[ -d $RPM_BUILD_ROOT%{_app_dir}/init ] || mkdir -p $RPM_BUILD_ROOT%{_app_dir}/init

# Copy Source Code
cp -r %{_gitdir}/shelfzilla $RPM_BUILD_ROOT%{_app_dir}
cp -r %{_gitdir}/config/production $RPM_BUILD_ROOT%{_app_dir}/config
cp -r %{_gitdir}/config/requirements.txt $RPM_BUILD_ROOT%{_app_dir}/config
cp -r %{_gitdir}/*.json $RPM_BUILD_ROOT%{_app_dir}/
cp -r %{_gitdir}/*.py $RPM_BUILD_ROOT%{_app_dir}/
cp -f %{_gitdir}/.bowerrc $RPM_BUILD_ROOT%{_app_dir}/
cp -r %{_gitdir}/gruntfile.coffee $RPM_BUILD_ROOT%{_app_dir}/
cp -r %{_gitdir}/rpm/scripts/shelfzilla $RPM_BUILD_ROOT%{_app_dir}/init/

# -------------------------------------------------------------------------------------------- #
# post-install section:
# -------------------------------------------------------------------------------------------- #
%post
## Install init script
mv %{_app_dir}/init/shelfzilla %{_init_path}/
chmod 775 %{_init_path}/shelfzilla
chkconfig --add shelfzilla
rmdir %{_app_dir}/init/

## Npm install
cd %{_app_dir} && npm install --production

## pip install
pip install -r %{_app_dir}/config/production/requirements.txt

## Migrate
python2.7 %{_app_dir}/manage.py migrate --no-initial-data

## Bower
cd %{_app_dir}
bower install --allow-root

## Collect static
python2.7 manage.py collectstatic --clear --noinput

# -------------------------------------------------------------------------------------------- #
# pre-uninstall section:
# -------------------------------------------------------------------------------------------- #
%preun
if [ $1 == 0 ]; then
echo "Cleaning application files"
[ -e /etc/logrotate.d/shelzilla ] && rm -fv /etc/logrotate.d/shelfzilla
[ -e %{_init_path}/shelfzilla ] && rm -fv %{_init_path}/shelfzilla
echo "Uninstall finished"

fi


# -------------------------------------------------------------------------------------------- #
# post-uninstall section:
# -------------------------------------------------------------------------------------------- #
%postun

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_app_dir}/*
%{_app_dir}/.bowerrc
%{_init_path/shelfzilla


