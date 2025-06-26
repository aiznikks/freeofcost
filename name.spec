## ---- Begin SERVER RPM block ----
%if "%{buildtype}" == "all" || "%{buildtype}" == "server"
%package devel
Summary: Development files for NPU Framework
Requires: %{name} = %{version}-%{release}
%description devel
This package contains the development files for %{name}.
%endif
## ---- End SERVER RPM block ----

## ---- Begin SERVER RPM block ----
%if "%{buildtype}" == "all" || "%{buildtype}" == "server"
%package release
Summary: Tizen NPU MANAGER - Release version
%description release
Tizen NPU MANAGER
%endif
## ---- End SERVER RPM block ----

## ---- Begin TEST RPM block ----
%if "%{buildtype}" == "all" || "%{buildtype}" == "test"
%package test
Summary: Test files for tomato UT
%description test
This package contains the test files and tomato UT for %{name}.
%endif
## ---- End TEST RPM block ----


## ---- Begin SERVER RPM block ----
%if "%{buildtype}" == "all" || "%{buildtype}" == "server"
%package models
Summary: Model files for NPU Framework
%description models
This package contains the model files for %{name}.
%endif
## ---- End SERVER RPM block ----

%define _tomatodir %{TZ_SYS_RW_APP}/tomato/testcase/%{name}-ut

## ---- Begin TEST RPM block ----
%if "%{buildtype}" == "all" || "%{buildtype}" == "test"
%package ut-component-tomato
Summary: Unit testing package with gtest
Requires: %{name} = %{version}-%{release}
%description ut-component-tomato
tizen-pumanager tomato test suite
%endif
## ---- End TEST RPM block ----

## ---- Begin SERVER RPM block ----
%if "%{buildtype}" == "all" || "%{buildtype}" == "server"
%package bm-tc
Summary: Dummy ko modules and test app
Requires: %{name} = %{version}-%{release}
%description bm-tc
This package contains dummy ko modules and test app for %{name}.
%endif
## ---- End SERVER RPM block ----

%prep
%setup -q

%install
%if 0%{?debug_only:1}
MODE=(debug_perf)
%else
MODE=(debug_perf release)
%endif

rm -rf %{buildroot}
export PLATFORM_TYPE=%{_vd_cfg_platform_type}
mkdir -p %{buildroot}%{_prdbindir}
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mkdir -p %{buildroot}%{_prddir}/usr/lib/systemd/system
mkdir -p %{buildroot}%{_prddir}/usr/share/dbus-1/
mkdir -p %{buildroot}%{_prddir}/etc/spolicy/
mkdir -p %{buildroot}/opt/usr/data/aifw-core/model/npu_manager/

for CURRENT_MODE in ${MODE[@]}; do
    echo "In build... CURRENT_MODE = $CURRENT_MODE"
    echo "Build for Version: %{NPUMGR_VERSION}, Plugin: %{NPU_PLUGIN}"
    export PLATFORM_TYPE=%{_vd_cfg_platform_type}

    if [ "%{NPUMGR_VERSION}" = "NPUMGR_1_0" ]; then
        %configure --prefix=%{_prddir}/usr \
                   --libdir=%{_prdlibdir} \
                   --bindir=%{_prdbindir} \
                   --enable-system-bus \
                   --enable-dlog \
                   --enable-platform-tizen
        make %{?jobs:-j%jobs}

    elif [ "%{NPUMGR_VERSION}" = "NPUMGR_2_0" ]; then
        export CHIP_NAME=%{_vd_cfg_chip}
        export SYSTEM64=%{_vd_cfg_system64}
        export RELEASE_MODE=debug

        if [ "$SYSTEM64" = "y" ]; then
            export CROSS_COMPILE=aarch64-tizen-linux-gnu-
            PATH=$PATH:/emul/opt/cross/bin
        fi

        export TOOLCHAIN_GCC_VERSION=%{gcc_flag}
        echo "gcc version: %{gcc_flag}"

        cd ./2_0

        ENABLE_MULTICORE_NPU=""
        ENABLE_NIKEM2_NBINFO=""

        if [ "$CURRENT_MODE" = "release" ]; then
            ENABLE_STREAMLINE=""
            ENABLE_PROFILING=""
        else
            ENABLE_STREAMLINE="--enable-streamline"
            ENABLE_PROFILING="--enable-profiling"
        fi

        if [ "%{NPU_PLUGIN}" = "VIPLITE" ]; then
            ENABLE_NPU_PLUGIN="--enable-viplite-plugin"
        elif [ "%{NPU_PLUGIN}" = "TRIV" ]; then
            ENABLE_NPU_PLUGIN="--enable-triv2-plugin"
            if [ "%{CHIP_NAME}" != "CHIP_ROSEL" ]; then
                ENABLE_MULTICORE_NPU="--enable-multi-core-npu"
            fi
        elif [ "%{NPU_PLUGIN}" = "NEUS" ]; then
            ENABLE_NPU_PLUGIN="--enable-neus-plugin"
        fi

        export CFLAGS="$CFLAGS -Wall -Werror -D%{CHIP_NAME} -Wl,-z,relro,-z,now -fstack-protector-strong -D_FORTIFY_SOURCE=2 -O2"
        export CXXFLAGS="$CXXFLAGS -Wall -Werror -D%{CHIP_NAME} -Wl,-z,relro,-z,now -fstack-protector-strong -D_FORTIFY_SOURCE=2"
        export LDFLAGS="$LDFLAGS -Wl,-z,relro,-z,now"

        %configure --prefix=%{_prddir}%{_prefix} \
                   --libdir=%{_prdlibdir} \
                   --bindir=%{_prdbindir} \
                   --pcdir=%{_libdir} \
                   --enable-system-bus \
                   --enable-platform-tizen \
                   --enable-preload-mgr \
                   $ENABLE_NPU_PLUGIN \
                   $ENABLE_ARMNN \
                   --enable-build-ut \
                   --enable-load-mgr \
                   $ENABLE_STREAMLINE \
                   $ENABLE_PROFILING \
                   $ENABLE_MULTICORE_NPU \
                   $ENABLE_NIKEM2_NBINFO

        make %{?jobs:-j%jobs}
    fi
done

%post
if [ %{NPUMGR_VERSION} != "NPUMGR_1_0" ]; then
    mv %{_prdbindir}/debug_perf/npumgr_server %{_prdbindir}/npumgr_server
    cp -f %{_prdlibdir}/debug_perf/libnpumgr_client.so* %{_prdlibdir}/
    rm -rf %{_prdlibdir}/npumgr
    mv %{_prdlibdir}/debug_perf/npumgr %{_prdlibdir}/
    rm -rf %{_prdbindir}/debug_perf/
    rm -rf %{_prdlibdir}/debug_perf/
fi

%preun
systemctl stop org.tizen.NPUManager.service
rm -f %{_prdbindir}/npumgr_server
rm -f %{_prddir}/usr/lib/systemd/system/org.tizen.NPUManager.service
rm -f %{_prddir}/usr/lib/systemd/system/org.tizen.NPUManager.busname
rm -rf %{_prdlibdir}/npumgr/devices/
rm -rf %{_prdlibdir}/npumgr/memory/
rm -f %{_prdlibdir}/libnpumgr_client.*

%postun
/sbin/ldconfig > /dev/null 2>&1

%if 0%{!?debug_only:1}
%postun release
/sbin/ldconfig > /dev/null 2>&1
%endif

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)

%if "%{NPUMGR_VERSION}" == "NPUMGR_2_0"
%{_prdbindir}/debug_perf/npumgr_server
%{_prddir}/usr/lib/systemd/system/org.tizen.NPUManager.service
%{_prddir}/usr/lib/systemd/system/org.tizen.NPUManager.busname
%{_prdlibdir}/debug_perf/npumgr/devices/*.so*
%{_prdlibdir}/debug_perf/npumgr/memory/*.so*
%{_prdlibdir}/debug_perf/*.so*
%{_prddir}/etc/spolicy/org.tizen.NPUManager.capsign
%{_prddir}/usr/share/dbus-1/org.tizen.NPUManager.conf
%else
%{_prdbindir}/npumgr_server
%{_prddir}/usr/lib/systemd/system/org.tizen.NPUManager.service
%{_prddir}/usr/lib/systemd/system/org.tizen.NPUManager.busname
%{_prdlibdir}/*.so*
%{_prddir}/etc/spolicy/org.tizen.NPUManager.capsign
%{_prddir}/usr/share/dbus-1/org.tizen.NPUManager.conf
%endif
%if 0%{!?debug_only:1}
%files release
%manifest %{name}.manifest
%defattr(-,root,root,-)

%if "%{NPUMGR_VERSION}" == "NPUMGR_2_0"
%{_prdbindir}/release/npumgr_server
%{_prddir}/usr/lib/systemd/system/org.tizen.NPUManager.service
%{_prddir}/usr/lib/systemd/system/org.tizen.NPUManager.busname
%{_prdlibdir}/release/npumgr/devices/*.so*
%{_prdlibdir}/release/npumgr/memory/*.so*
%{_prdlibdir}/release/*.so*
%{_prddir}/etc/spolicy/org.tizen.NPUManager.capsign
%{_prddir}/usr/share/dbus-1/org.tizen.NPUManager.conf
%else
%{_prdbindir}/npumgr_server
%{_prddir}/usr/lib/systemd/system/org.tizen.NPUManager.service
%{_prddir}/usr/lib/systemd/system/org.tizen.NPUManager.busname
%{_prdlibdir}/*.so*
%{_prddir}/etc/spolicy/org.tizen.NPUManager.capsign
%{_prddir}/usr/share/dbus-1/org.tizen.NPUManager.conf
%endif
%endif

%files devel
%if "%{NPUMGR_VERSION}" == "NPUMGR_1_0"
%{_libdir}/pkgconfig/*
%else
%{_includedir}/*
%{_libdir}/pkgconfig/*
%endif

%files test
%if "%{NPUMGR_VERSION}" == "NPUMGR_1_0"
%{_prdbindir}/npumgr_nbinfo
%{_prdbindir}/npumgr_vpmrun
%{_prdbindir}/npumgr_vpm_append
%{_prdbindir}/npumgr_sdk
%endif
%if "%{NPUMGR_VERSION}" == "NPUMGR_2_0"
%{_prdbindir}/npumgr_simpletest
%{_prdbindir}/npumgr_loadparsertest
%{_prdbindir}/npumgr_executenetwork
%{_prdbindir}/npumgr_ewtest
%{_prdbindir}/npumgr_prioritytest
%{_prdbindir}/npumgr_highmemory
%{_prdbindir}/npumgr_advrun
%{_prdbindir}/npumgr_dmabuf
%{_prdbindir}/npu_perf_tool/*
%endif
%files ut-component-tomato
%if "%{NPUMGR_VERSION}" == "NPUMGR_2_0"
%{_tomatodir}/*
%{_prdbindir}/npumgr_ut_*
%{jbm_w_root}/tizen-npumanager/*
/opt/usr/data/aifw-core/model/test_models/*
%endif

%if "%{NPUMGR_VERSION}" == "NPUMGR_1_0"
%files models
/opt/usr/apps/npumgr/sdk/*
/opt/usr/data/aifw-core/model/npu_manager/*
%endif

%files bm-tc
%if "%{NPUMGR_VERSION}" == "NPUMGR_2_0"
%{jbm_w_root}/tizen-npumanager/*
%endif







