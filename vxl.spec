Name:       vxl
Version:    1.17.0.2018.06.18
Release:    1%{?dist}
Summary:    C++ Libraries for Computer Vision Research and Implementation
Group:      Development/Libraries
License:    BSD
URL:        http://vxl.sourceforge.net/

Source:         %{name}-%{version}.tar.gz
Patch3:         0003-Use-system-rply.patch
Patch27:        0027-dcmdata_dir.patch
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  expat-devel
BuildRequires:  Coin2-devel
BuildRequires:  dcmtk-devel
BuildRequires:  doxygen
BuildRequires:  expat-devel
BuildRequires:  expatpp-devel
BuildRequires:  freeglut-devel
BuildRequires:  klt-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  libXmu-devel
BuildRequires:  libXi-devel
BuildRequires:  libjpeg-devel
%ifnarch s390 s390x
BuildRequires:  libdc1394-devel
%endif
BuildRequires:  libgeotiff-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  minizip-devel
BuildRequires:  rply-devel
BuildRequires:  SIMVoleon-devel
BuildRequires:  shapelib-devel
BuildRequires:  texi2html
BuildRequires:  xerces-c-devel
BuildRequires:  zlib-devel

#GUI needs wx, a desktop file and an icon

%description
VXL (the Vision-something-Libraries) is a collection of C++ libraries designed
for computer vision research and implementation. It was created from TargetJr
and the IUE with the aim of making a light, fast and consistent system.
VXL is written in ANSI/ISO C++ and is designed to be portable over many
platforms.


%package    doc
Summary:    Documentation for VXL library
Group:      Documentation
Requires:   %{name} = %{version}-%{release}
BuildArch:  noarch

%description doc

Full documentation for VXL library.

%package    devel
Summary:    Headers and development libraries for VXL
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel

Development libraries and headers for VXL.

%prep
%setup -c -q
%patch3 -p1
# %patch27 -p1

#Remove bundled library (let's use FEDORA's ones)
# v3p/netlib (made by f2c) dependency not removed because of heavily modifications
# QV is a Silicon Graphics' VRML parser from the 90s. Now unmantained.
# DCMDK is left in because they are pinned to 5.2 and requires patching to get to 5.3
for l in jpeg png zlib tiff geotiff dcmtk bzlib
do
    find v3p/$l -type f ! -name 'CMakeLists.txt' -execdir rm {} +
done

find contrib/brl/b3p/shapelib -type f ! -name 'CMakeLists.txt' -execdir rm {} +
find contrib/brl/b3p/minizip -type f ! -name 'CMakeLists.txt' -execdir rm {} +
find contrib/brl/b3p/expat -type f ! -name 'CMakeLists.txt' -execdir rm {} +
find contrib/brl/b3p/expatpp -type f ! -name 'CMakeLists.txt' -execdir rm {} +

# v3p/mpeg2 lib in fedora is not enough to build the target. Moreover it is in rpmfusion repo

%build
%cmake \
        -DCMAKE_INSTALL_LIBRARY_DESTINATION:STRING="%{_lib}" \
        -DCMAKE_INSTALL_ARCHIVE_DESTINATION:STRING="%{_lib}" \
        -DVXL_INSTALL_LIBRARY_DIR:STRING="%{_lib}" \
        -DVXL_INSTALL_ARCHIVE_DIR:STRING="%{_lib}" \
        -DBUILD_SHARED_LIBS:BOOL=ON \
        -DVXL_FORCE_B3P_EXPAT:BOOL=OFF \
        -DVXL_FORCE_V3P_DCMTK:BOOL=ON \
        -DVXL_FORCE_V3P_GEOTIFF:BOOL=OFF \
        -DVXL_USING_NATIVE_KL=ON \
        -DVXL_FORCE_V3P_JPEG:BOOL=OFF \
        -DVXL_FORCE_V3P_MPEG2:BOOL=OFF \
        -DVXL_FORCE_V3P_PNG:BOOL=OFF \
        -DVXL_FORCE_V3P_TIFF:BOOL=OFF \
        -DVXL_FORCE_V3P_ZLIB:BOOL=OFF \
        -DVXL_USING_NATIVE_ZLIB=ON \
        -DVXL_USING_NATIVE_JPEG=ON \
        -DVXL_USING_NATIVE_PNG=ON \
        -DVXL_USING_NATIVE_TIFF=ON \
        -DVXL_USING_NATIVE_GEOTIFF=ON \
        -DVXL_USING_NATIVE_EXPAT=ON \
        -DVXL_USING_NATIVE_SHAPELIB=ON \
        -DVXL_USING_NATIVE_BZLIB2=ON \
        -DBUILD_VGUI=OFF \
        -DBUILD_BGUI3D=OFF \
        -DBUILD_OXL:BOOL=ON \
        -DBUILD_BRL=OFF \
        -DBUILD_CORE_GEOMETRY:BOOL=ON \
        -DBUILD_CORE_IMAGING:BOOL=ON \
        -DBUILD_CORE_NUMERICS:BOOL=ON \
        -DBUILD_CORE_PROBABILITY:BOOL=ON \
        -DBUILD_CORE_SERIALISATION:BOOL=ON \
        -DBUILD_CORE_UTILITIES:BOOL=ON \
        -DBUILD_CORE_VIDEO:BOOL=ON \
        -DBUILD_EXAMPLES:BOOL=OFF \
        -DBUILD_TESTING:BOOL=OFF \
        -DBUILD_DOCUMENTATION:BOOL=ON \
        -DCMAKE_BUILD_TYPE:STRING="RelWithDebInfo" \
        -DCMAKE_CXX_FLAGS:STRING="$RPM_OPT_FLAGS" \
        -DPYTHON_LIBRARY=/usr/%{_lib}/libpython2.7.so \
        -DVNL_CONFIG_LEGACY_METHODS=ON .

# Why is expat stated, but not shapelib?
# DCMDK Cmake -- Included in bundle, but why?
#BUILD_VGUI? NO, it depends on box2m which in turns relies on OPENCL which is not available in FEDORA
#wxwidgets seems to be found
#Multiple versions of QT found please set DESIRED_QT_VERSION
#TODO: Xerces for brl
#TODO: Testing?
#BR: coin2, coin3 (coin3d) brl, bbas

%make_build

%install
%make_install

%check
ctest .

%files
%doc core/vxl_copyright.h
%{_libdir}/*.so.*

%files devel
%{_datadir}/%{name}
%{_includedir}/%{name}
%{_libdir}/*.so

%files doc
%doc %{_docdir}/*

%changelog
* Mon Jun 18 2018 Mark Harfouche <mark.harfouche@gmail.com> - 1.17.0.2018.06.18-1
- Unbundle rply

* Mon Jun 18 2018 Mark Harfouche <mark.harfouche@gmail.com> - 1.17.0.2018.06.18-0
- Updated to post 2012 version

* Wed Mar 07 2018 Adam Williamson <awilliam@redhat.com> - 1.17.0-26
- Rebuild to fix GCC 8 mis-compilation
  See https://da.gd/YJVwk ("GCC 8 ABI change on x86_64")

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 25 2016 Tom Callaway <spot@fedoraproject.org> - 1.17.0-20
- remove non-free lena image file from source tarball (bz1310388)
- fix FTBFS (bz1303695, bz1308234)

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 16 2015 Sebastian Pölsterl <sebp@k-d-w.org> - 1.17.0-17
- Rebuilt using hardened build flags: https://fedoraproject.org/wiki/Changes/Harden_All_Packages

* Mon Feb 16 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.17.0-16
- Add vxl-0.17.0-gcc5.diff (Work-around GCC-5.0.0 FTBFS RHBZ#1192886).
- Fix bogus %%changelog date.

* Mon Aug 25 2014 Devrim Gündüz <devrim@gunduz.org> - 1.17.0-15
- Rebuilt for libgeotiff

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 04 2013 Mario Ceresa mrceresa fedoraproject org vxl 1.17.0-11
- Applied upstream patches (25, 26) to ensure compatibility with ITK

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 1.17.0-9
- rebuild due to "jpeg8-ABI" feature drop

* Wed Dec 05 2012 Dan Horák <dan[at]danny.cz> - 1.17.0-8
- fix build on non-x86 arches

* Sun Nov 25 2012 Mario Ceresa mrceresa fedoraproject org vxl 1.17.0-7%{?dist}
- Changed source0 path to point to vxl 1.17
- Added missing sonames

* Fri Nov 02 2012 Mario Ceresa mrceresa fedoraproject org vxl 1.17.0-6%{?dist}
- Patched to build BRL
- Updated to last version

* Mon Oct 29 2012 Mario Ceresa mrceresa fedoraproject org vxl 1.17.0-5%{?dist}
- Removed expatpp bundled library and added corresponding BR
- Removed bundled bzip


* Thu Oct 18 2012 Mario Ceresa mrceresa fedoraproject org vxl 1.17.0-4%{?dist}
- Fixed missing oxl_vrml lib
- Turn on compilation of BRL

* Sun Oct 14 2012 Mario Ceresa mrceresa fedoraproject org vxl 1.17.0-3%{?dist}
- More fixes from Volker's post https://bugzilla.redhat.com/show_bug.cgi?id=567086#c42
-

* Wed Oct 10 2012 Mario Ceresa mrceresa fedoraproject org vxl 1.17.0-2%{?dist}
- Added patches 12-16 from https://bugzilla.redhat.com/show_bug.cgi?id=567086#c42
- Minor rework of the spec file as pointed out by Volker in the previous link

* Wed Oct 10 2012 Mario Ceresa mrceresa fedoraproject org vxl 1.17.0-1%{?dist}
- Updated to new version
- Reworked patches to the new version
- Disabled BRL because it gives a compilation error

* Fri May 27 2011 Mario Ceresa mrceresa fedoraproject org vxl 1.14.0-1%{?dist}
- Updated to new version
- Added BR doxygen (thanks to Ankur for noticing it)
- Changed patch naming schema
- Work around a rply related bug (patches 3-6)
- Thanks to Thomas Bouffon for patch 7-8
- Patches 9-10 address http://www.itk.org/pipermail/insight-users/2010-July/037418.html
- Fixed 70 missing sonames in patch 11
- Removed bundled expact, shapelib, minizip, dcmtk
- Force brl build
- Use system shipped FindEXPAT


* Tue Mar 23 2010 Mario Ceresa mrceresa fedoraproject org vxl 1.13.0-4%{?dist}
- sed patch to add ${LIB_SUFFIX} to all lib install target
- Added soname version info to vil vil_algo lib

* Sun Mar 21 2010 Mario Ceresa mrceresa fedoraproject org vxl 1.13.0-3%{?dist}
- Applied patch to build against newly packaged rply

* Tue Mar 2 2010 Mario Ceresa mrceresa fedoraproject org vxl 1.13.0-2%{?dist}
- Applied patch from debian distribution to force the generation of versioned lib

* Fri Feb 19 2010 Mario Ceresa mrceresa fedoraproject org vxl 1.13.0-1%{?dist}
- Initial RPM Release
