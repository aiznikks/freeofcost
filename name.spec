
Name: tizen-pumanager
Version: 7.0
Release: 1.0.1
Summary: NPU Task Manager
License: Proprietary

# ===================== Build Type Control =====================
# Use '--define "buildtype test"' to build only test RPMs
# Use '--define "buildtype server"' to build only server RPMs
# Default (no buildtype): builds all RPMs
%{!?buildtype: %define buildtype all}

# Define macros for conditional RPM inclusion
%define build_test   %{!?buildtype:1}%{?buildtype:test}
%define build_server %{!?buildtype:1}%{?buildtype:server}
# ==============================================================
Source: %{name}-%{version}.tar.gz
Source 1001: %{name}.manifest
%define CHIP_NAME %{_vd_cfg_chip}
%define NPUMGR_VERSION
%define NPU_PLUGIN
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(ttrace)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(fconfig)
BuildRequires: soc-npu-user-libs-devel
%if ("%{CHIP_NAME}" == "CHIP_NIKEM")
    %define NPUMGR_VERSION "NPUMGR_1_0"
%endif
%if (*%{CHIP_NAME}" == "CHIP_NIKEM2") || (*%{CHIP_NAME} ==
    "CHIP_OSCARP") || (*%{CHIP_NAME}" == "CHIP_OSCARS") || (*%
    {CHIP_NAME)" == "CHIP_PONTUSM") || (*%{CHIP_NAME}" ==
    "CHIP_PONTUSML" || (*%{CHIP_NAME}" == "CHIP_ROSEP") || (*%
    {CHIP_NAME)" == "CHIP_ROSEM*) || (*%{CHIP_NAME}" ==
    "CHIP_ROSEL) || (*%{CHIP_NAME}" == "CHIP_ROSEW*)
    %define NPUMGR_VERSION "NPUMGR 2_0"
    %if (%{CHIP_NAME}" == "CHIP_OSCARP")
        %define NPU_PLUGIN "NEUS"
    %endif
    %if ((*%{CHIP_NAME}" == "CHIP_PONTUSM*) || (*%{CHIP_NAME}"
        == "CHIP_ROSEP*) || (%{CHIP_NAME}" == "CHIP_ROSEM*) || (*%
        (CHIP_NAME)" FE "CHIP ROSEL)
        %define NPU_PLUGIN "TRIV"
        %if ((*%{CHIP_NAME}" == "CHIP_NIKEM2") || (*%{CHIP_NAME}" ==
            "CHIP _OSCARS") || (*%{CHIP_NAME}" == "CHIP_PONTUSML))
            %define NPU_PLUGIN "VIPLITE"
        %endif
        %if (%{NPUMGR_VERSION} == "NPUMGR_2_0")
            BuildRequires: pkgconfig(json-glib-1.0)
            BuildRequires: pkgconfig(gmodule-2.0)
            BuildRequires: pkgconfig(jsoncpp)
            Build Requires: pkgconfig(libtbm)


            BuildRequires: pkgconfig(jsoncpp)
            BuildRequires: pkgconfig(libtbm)
            BuildRequires: gtest-devel
            BuildRequires: pkgconfig(tztv-kernel)
            BuildRequires: pkgconfig(vd_kernel-interfaces)
            %if (*%{_vd_cfg_system64}" == "y")
                BuildRequires: cross-aarch64-gcc-x86-arm
                BuildRequires: cross-aarch64-binutils-x86-arm %endif
                %define jbm_w_root %{TZ_SYS_DATA}/BM/JBM
                %define _module_name npu_dummy.ko %define_test_name test_npu_dummy
                BuildRequires: pkgconfig(libtzplatform-config)
            %endif|
            %define _prdbindir %{_prddir}%{_bindir}
            %define _prdlibdir %{_prddir}%{_libdir}
            ExclusiveArch: %arm aarch64
            %description
            General Framework for using NPU on Tizen Platform
            %package devel
            Summary: Development files for NPU Framework
            Requires: %{name} = %{version}-%{release}
            %description devel
            This package contains the development files for %(name).
            %package test
            Summary: Test files and tomato UT files for NPU Framework
            Requires: %{name} = %{version}-%(release)
            Requires: %{name}-ut-component-tomato = %{version}-%(release)
            %if 0%{!?debug_only: 1)
                %package release
                Summary: Tizen NPU MANAGER - Release version
                %description release
                Tizen NPU MANAGER %endif
                %description test
                This package contains the test files tomato UT files for % (name). %package models
                Summary: Model files for NPU Framework

                %description models
                This package contains the model files for %(name). %define
                _tomatodir %{TZ_SYS_RW_APP}/tomato/testcase/%
                {name}-ut
                %package ut-component-tomato
                Summary: Unit testing package with gtest
                Requires: % {name} = %{version}-%{release}
                %description ut-component-tomato
                tizen-pumanager tomato test suite



                %package bm-tc
                Summary: dummy ko modules and test app
                Requires: %(name) = %(version)-%{release}
                %description bm-tc
                This package contains dummy ko modules and test app %(name}.
                %prep
                %setup -9
                %install %if 0%{?debug_only:1}
                MODE=(debug_perf)
                %else|
                MODE=(debug_perf" release)
            %endif
            rm -rf %{buildroot}
            export PLATFORM_TYPE=%{_vd_cfg_platform_type}
            mkdir-p %{buildroot}%(_prdbindir)
            mkdir -p %{buildroot}%{_libdir/pkgconfig
            mkdir -p %(buildroot)%_prddir)/usr/lib/systemd/system
            mkdir -p %{buildroot}%(_prddir)/usr/share/dbus-1/
            mkdir -p %{buildroot}%{_prddir}/etc/spolicy/
            mkdir-p %(buildroot)/opt/usr/data/aifw-core/model/
            npu_manager/
            for CURRENT_MODE in "S(MODEr®i)" do
            echo "In build.....
            " SCURRENT_MODE
            echo "Build for Version: %{NPUMGR_VERSION}, Plugin: % (NPU_PLUGIN)
            export PLATFORM_TYPE=%{_vd_cfg_platform_type}
            #CFLAGS=$(echo SCFLAGS | seds/-02/-00/ | sed s/-01/-00/* | sed s/-Wp,-D_FORTIFY_SOURCE=2//*)
            #CXXFLAGS=$(echo SCXXFLAGS | sed s/-02/-00/* | sed s/-01/-
            00/ | sed s/-Wp,-D_FORTIFY_SOURCE=2//)
            cp %{SOURCE1001}:
            if [%{NPUMGR_VERSION} == "NPUMGR_1_0"]; then
            %configure -prefix=%(_prddir)/usr -libdir=%(_prdlibdir) -bindir=%
            {_prdbindir) pcdir=%{_libdir} -enable system-bus -enable-dlog -
            enable-platform-tizen make %?jobs:-j%jobs)
            elif [%{NPUMGR_VERSION} == "NPUMGR_2_0" ]; then
            export CHIP_NAME=%{_vd_cfg_chip}
            export CROSS_COMPILE=*
            export SYSTEM64=%{_vd_cfg_system64}

            echo "build for SCHIP_NAME"
            export RELEASE_MODE=debug
            %ifarch % arm,
                if ["$SYSTEM64" = "y" ]; then
                export CROSS_COMPILE=aarch64-tizen-linux-gnu-echo "build for SCHIP_NAME" echo "SPATH"
                PATH=SPATH:/emul/opt/cross/bin
                export RELEASE_MODE=debug
                export TOOLCHAIN_GCC_VERSION=%(gcc_flag)
                echo "gcc version %{gcc_flag}"
                cd ./2_0
                ENABLE_MULTLCORE_NPU=
                ENABLE_NIKEM2_NBINFO=*
                if [ SCURRENT_MODE = "release" ]; then
                ENABLE_STREAMLINE="
                ENABLE_PROFILING=*
                else
                ENABLE_STREAMLINE="-enable-streamline"
                ENABLE_PROFILING="-enable-profiling"
                fi

                if [%{NPU_PLUGIN} == VIPLITE" ] ; then
                ENABLE_NPU_PLUGIN=*-enable-viplite-plugin" elif [%(NPU_PLUGIN) == *TRIV" 1; then
                ENABLE_NPU_PLUGIN=-enable-triv2-plugin"
                if [%{CHIP_NAME} != "CHIP_ROSEL]; then ENABLE_MULTI_CORE_NPU=-enable-multi-core-npu*
                fi
                elif [%(NPU_PLUGIN) == "NEUS"]; then
                ENABLE NPU_PLUGIN=*-enable-neus-plugin"
                fi
                if ["%{_vd_cfg_product_type}" = "LD"]; then
                ENABLE_ARMNN=**
                else
                ENABLE_ARMNN=*-enable-armnn-plugin"
                fi
                if [%{CHIP_NAME} == *CHIP_NIKEM2 ]; then ENABLE_NIKEM2_NBINFO=*-enable-nikem2-nbinfo*
                fil
                export CFLAGS="SCFLAGS -Wall -Werror -D%{CHIP_NAME} -WI,-z,reiro,-z,now -fstack-protector-strong-D_FORTIFY_SOURCE=2-02" export CXXFLAGS="SCXXFLAGS -Wall -Werror -D%{CHIP_NAME}
                -Wi,-z,relro,-z,now -fstack-protector-strong -D_FORTIFY_SOURCE=2
                export LDFLAGS="SLDFLAGS -WI,-z,relro, z,now
                %reconfigure LIBDIR=%_prdlibdir) INCLUDEDIR=%(includedir)
                %configure -prefix=%(_prddir)%_prefix) - libdir=%Lprdlibdir) -
                bindir=%{_prdbindir} pcdir=%{_libdir} - enable system-bus -enable-
                platform-tizen -enable preload-mgr SENABLE_NPU_PLUGIN SENABLE_ARMNN -enable-build-ut -enable-load-mgr
                SENABLE_STREAMLINE SENABLE_PROFILING
                SENABLE_MULTI_CORE_NPU SENABLE_NIKEM2_NBINFO
                make %?jobs: j%jobs)
                else
                cd ./2_0
                export CFLAGS="SCFLAGS-Wall -Werror

                export CXXFLAGS=*SCXXFLAGS-Wall-Werror"
                %reconfigure LIBDIR=%{_prdlibdir} INCLUDEDIR=%(_includedir)
                %configure -prefix=%{_prddir}%(_prefix) -libdir=%_prdlibdir) -
                bindir=%{_prdbindir} pedir=%{_libdir} -enable-system-bus -enable-platform-tizen make clean make %?jobs: j%jobs)
                fi
                echo "In install 2 Current _MODE is SCURRENT_MODE"
                echo "builldroot = " %{buildroot}
                if [%{NPUMGR_VERSION} == "NPUMGR_1_0"]; then
                mkdir-p %{buildroot}/opt/us/apps/npumgr/sdk/data
                mkdir -p %{buildroot}%{_prddir}/usr/lib/systemd/system/
                install-m 644 data/org.tizen.NPUManager.capsign %(buildroot)% {_prddir)/etc/spolicy/
                make install DESTDIR=%{buildroot}/ cp-rf models/* %{buildroot}/opt/us/data/aifw-core/model/
                find %{buildroot}/opt/us/data/aifw-core/model/npu_manager/
                -iname* dat -exec rm f 0 ;
                cp -rf %{_builddir}/%{name}-%{version}/1_0/
                org.tizen.NPUManager.conf %{buildroot}%(_prddir)/usr/share/
                install -m 0644 data/org.tizen.NPUManager.busname %{buildroot}
                %{_prddir}/usr/lib/systemd/system/
                rm %{buildroot}%{_prdlibdir}/*.la
                elif [%{NPUMGR_VERSION} == "NPUMGR 2_0" ]; then
                export CHIP_NAME=%{_vd_cfg_chip}
                export CROSS_COMPILE=***
                export SYSTEM64=%{_vd_cfg_system64}
                echo "build for SCHIP_NAME export RELEASE_MODE=debug
                if ["SSYSTEM64" = "y" l; then
                export CROSS_COMPILE=aarch64-tizen-linux-gnu-echo "build for SCHIP_NAME"
                PATH=SPATH:/emul/opt/cross/bin export RELEASE_MODE=debug export TOOLCHAIN_GCC_VERSION=%{gcc_flag}
                echo "gcc version %{gcc_flag}”
                fi
            %endif

            mkdir -p %(buildroot)%(_includedir)
            mkdir-p %{buildroot}/opt/us/data/aifw-core/model/test_models
            mkdir -p %{buildroot}/%_prdbindiry/npu_perf_tool
            mkdir -p %{buildroot}%_prdlibdir)/SCURRENT_MODE/npumgr/
            devices
            mkdir -p %{buildroot}%{_prdlibdir}/SCURRENT_MODE/npumgr/
            memory
            mkdir -p %(buildroot)%{_tomatodir/tc
            mkdir-p %{buildroot}% jbm_rw_root//tizen-npumanager
            install-m 0644 res/org.tizen.NPUManager.capsign %{buildroot}%
            { prddir)/etc/spolicy/
            install -m 0644 res/org.tizen.NPUManager.busname %(buildroot)% { prddir)/usr/lib/systemd/system/
            make install DESTDIR=%{buildroot} cp-rf%_builddir)/%{name}-%{version}/2_0/
            org.tizen.NPUManager.conf%{buildroot}%_prddir)/usr/share/
            cp -rf %_builddir)/%{name} %(version)/2_0/include/*h %
            {buildroot)/%{_includedir}/

            cp-rf %{_builddir}/%{name}-%{version}/2_0/test/npu_perf_tool/
            inference.py %{buildroot}/%{_prdbindiry/npu_perf_tool
            if [*%{CHIP_NAME}* = "CHIP_PONTUSM" ] || [ *%{CHIP_NAME}" =
            "CHIP_ROSEP" ] || [*%{CHIP_NAME} = "CHIP_ROSEM" ] || [*%
            {CHIP_NAME)" = "CHIP_ROSEL* ],then
            cp -rf %{_builddir}/%{name}-%{version}/2_0/test/npu_perf_tool/
            memory.py %{buildroot}/%(_prdbindir)/npu_perf_tool
            fi

            mkdir -p %{buildroot}/%{_prdbindir}/SCURRENT_MODE/
            cp -f src/server/npumgr_server %{buildroot}/%_prdbindiry/
            SCURRENT_MODE/ rm-f %{buildroot}/%{_prdbindiry/npumgr_server
            rm-f %{buildroot}/debug_perf/%(_prdbindir}/npumgr_server.debug
            #its debug folder for debuginfo rpms
            cp -rf %{_builddir}/%{name}%(version)/2_0/test/models/%
            {CHIP_NAME)/*%{buildroot}/opt/us/data/aifw-core/model/
            test_models/


            cp-rf %{_builddir}/%{name}-%{version}/2_0/test/models/%
            {CHIP_NAME)/* %{buildroot}/opt/usr/data/aifw-core/model/
            test_models/
            cp -rf %{_builddir}/%{name}-%{version}/2_0/test/ut/TCList.dat%
            {buildroot)%{_tomatodir}/tc
            cp -rf%_builddir)/%{name}-%(version)/2_0/test/ut/tizen-
            npumanager-ut-component-tomato.xml %{buildroot}%{_tomatodir}/
            tc
            cp -rf %{_builddir}/%{name}-%{version}/2_0/test/npu_dummy/%
            (_module_name) %{buildroot}%{jbm_rw_root}/tizen-npumanager
            cp-rf%_builddir)/%{name}-%{version}/2_0/test/pu_dummy/test/
            %{_test_name} %{buildroot}%jbm_rw_root)/tizen-npumanager
            mv %{buildroot}%/_prdlibdir)/lib*device* %(buildroot)%{_prdlibdir}/
            SCURRENT_MODE/npumgr/devices mv %{buildroot}%{_prdlibdir}/lib*memory*%{buildroot}%
            {_prdlibdir)/SCURRENT_MODE/npumgr/memory
            mkdir-p %{buildroot}/%{_prdlibdir}/SCURRENT_MODE/
            cp -f %{buildroot}/%{_prdlibdir}/*.so* %(buildroot)/%{_prdlibdir}/
            SCURRENT_MODE/ rm %{buildroot}%{_prdlibdir}/*.so*
            rm %{buildroot}%{_prdlibdir}/*.la
            rm %{buildroot}%{_prdlibdir}/SCURRENT_MODE/npumgr/devices/*.la
            rm %{buildroot}%{_prdlibdir}/SCURRENT_MODE/npumgr/memory/*.la
            else cd ./2_0
            mkdir-p %{buildroot}%{_includedir}
            install -m 0644 res/org.tizen.NPUManager.capsign %{buildroot}% {_prddir)/etc/spolicy/
            install -m 0644 res/org.tizen.NPUManager.busname %{buildroot}% {_prddir)/usr/lib/systemd/system/ make install DESTDIR=%{buildroot}
            cp -rf %{_builddir}/%{name}-%{version}/2_0/
            org.tizen.NPUManager.conf %{buildroot}%(_prddir}/usr/share/ dbus-1/
            cp -+f %{_builddir}/%{name}-%(version)/2_0/include/*.h % {buildroot)/%{_includedir}/ rm %{(buildroot}%f_prdlibdir/*.la .fi cd .. done
            %post
            if [ %{NPUMGR_VERSION} != "NPUMGR_1_0" ]; then mv %{_prdbindir}/debug_perf/npumgr_server %{_prdbindir}/ npumgr_server
            cp -f %_prdlibdir)/debug_perf/libnpumgr_client.so*%{_prdlibdir}/ rm -rf %{_prdlibdir}/npumgr mv %_prdlibdir)/debug_perf/npumgr %(_prdlibdiry/ rm -tf %{_prdbindir}/debug_perf/ rm -rf %{_prdlibdir}/debug_perf/ fi export PLATFORM_TYPE=%{_vd_cfg_platform_type} export CHIP_NAME=%{_vd_cfg_chip}
            setcap cap_dac_override+ei /usr/bin/npumgr_server systemctl -system daemon-reload if [$1 -eq 1 ];then
            if [ %{NPUMGR_VERSION} == "NPUMGR_1_0"] ; then In -sf%(_prddir}/usr/lib/systemd/system/ org.tizen.NPUManager.service %{_prddir}/usr/lib/systemd/system/ starter.target.wants/org.tizen.NPUManager.service fi
            systemctl start org.tizen.NPUManager.service echo "Starting Complete!!! $1" fi


            if [ $1 -gt 1 ]: then # upgrade begins
            systemcti restart org.tizen.NPUManager.service echo "Upgrade Complete!!! $1" fi
            echo "Installation Complete!!! $1"
            %if 0%{!?debug_only:1}
                %post release
                if [ %{NPUMGR_VERSION} != "NPUMGR_1_0" ] ; then mv %{_prdbindir}/release/npumgr_server %{_prdbindir}/ npumgr_server
                cp -f %(_prdlibdir)/release/libnpumgr_client.so*%{_prdlibdir}/ rm-rf %{_prdlibdir}/npumgr mv %{_prdlibdir}/release/npumgr %{_prdlibdir}/ rm -rf %{_prdbindir}/release/ rm -rf %{_prdlibdir}/release/ fi
                export PLATFORM_TYPE=%{_vd_cfg_platform_type} export CHIP_NAME=%{_vd_cfg_chip}
                setcap cap_dac_override+ei /usr/bin/npumgr_server systemctl -system daemon-reload if [$1 -eq 1 ];then
                if [ %{NPUMGR_VERSION} == "NPUMGR_1_0" ] ; then In -sf %{_prddir}/usr/lib/systemd/system/
                org.tizen.NPUManager.service %(_prddir)/usr/lib/systemd/system/ starter.target.wants/org.tizen.NPUManager.service fi
                systemctl start org.tizen.NPUManager.service echo "Starting Complete!! S1" fl
                if [ $1 -gt 1 ]; then # upgrade begins
                systemctl restart org.tizen.NPUManager.service echo "Upgrade Complete!!! $1" fi
                echo "Installation Complete!!! $1"
            %endif
            %preun
            systemctl stop org.tizen.NPUManager.service rm %{_prdbindir}/npumgr_server rm %{_prddir}/usr/lib/systemd/system/ org.tizen.NPUManager.service rm %{_prddir}/usr/lib/systemd/system/ org.tizen.NPUManager.busname rm %{_prdlibdir}/npumgr/devices/ -rf rm %{_prdlibdir}/npumgr/memory/-rf rm %{_prdlibdir}/libnpumgr_client.* echo "Uninstall & remove the files"

            %if 0%{!?debug_only:1}
                %preun release systemctl stop org.tizen.NPUManager.service rm %{_prdbindir}/npumgr_server rm %{_prddir}/usr/lib/systemd/system/ org.tizen.NPUManager.service rm %{-prddir}/usr/lib/systemd/system/ org.tizen.NPUManager.busname rm %{_prdlibdir}/npumgr/devices/-rf rm %{_prdlibdir}/npumgr/memory/-rf rm %{_prdlibdir}/libnpumgr_client.* echo "Uninstall & remove the files"
            %endif
            %postun
            /sbin/Idconfig > /dev/null 2>&1
            %if 0%{!?debug_only:1}
                %postun release
                /sbin/Idconfig > /dev/null 2>&1
            %endif

            %files
            %manifest %{name}.manifest %defattr(-root,root,-)
            %if (%{NPUMGR_VERSION} == "NPUMGR_2_0")
                %{_prdbindir}/debug_perf/npumgr_server %{_prddir}/usr/lib/systemd/system/org.tizen.NPUManager.service %{_prddir}/usr/lib/systemd/system/ org.tizen.NPUManager.busname %{_prdlibdir}/debug_perf/npumgr/devices/*.so* %{_prdlibdir}/debug_perf/npumgr/memory/*.so*
                %{_prdlibdir}/debug_perf/*.so*
                %{_prddir}/etc/spolicy/org.tizen.NPUManager.capsign %{_prddir}/usr/share/dbus-1/org.tizen.NPUManager.conf %else
                %{_prdbindir}/npumgr_server %{_prddir}/usr/lib/systemd/system/org.tizen.NPUManager.service %{_prddir}/usr/lib/systemd/system/ org.tizen.NPUManager.busname %{_prdlibdir}/*.so*
                %{_prddir}/etc/spolicy/org.tizen.NPUManager.capsign %1_prddir)/usr/share/dbus-1/org.tizen.NPUManager.conf
            %endif

            %if 0%{!?debug_only:1}
                %files release
                %manifest %{name}.manifest %defattr(;root,root,-)
                %if (%{NPUMGR_VERSION} == "NPUMGR_2_0)
                    %{_prdbindir}/release/npumgr_server %{_prddir}/usr/lib/systemd/system/org.tizen.NPUManager.service %{_prddir}/usr/lib/systemd/system/ org.tizen.NPUManager.busname %{_prdlibdir}/release/npumgr/devices/*.so* %{_prdlibdir}/release/npumgr/memory/*.so*
                    %{_prdlibdir}/release/*.so*
                    • %{_prddir}/etc/spolicy/org.tizen.NPUManager.capsign %{_prddir}/usr/share/dbus-1/org.tizen.NPUManager.conf %else
                    %{_prdbindir}/npumgr_server %{_prddir}/usr/lib/systemd/system/org.tizen.NPUManager.service %{_prddir}/usr/lib/systemd/system/ org.tizen.NPUManager.busname %{_prdlibdir}/*.so*
                    %{_prddir}/etc/spolicy/orgtizen.NPUManager.capsign %{_prddir}/usr/share/dbus-1/org.tizen.NPUManager.conf
                %endif
            %endif

            %files devel
            %if (%{NPUMGR_VERSION} == "NPUMGR_1_0" )
                %{_libdir}/pkgconfig/*
                %else %{_includedir}/*
                %{_libdir}/pkgconfig/*
            %endif
            %files test
            %if (%{NPUMGR_VERSION} == "NPUMGR_1_0")
                %{_prdbindir}/npumgr_nbinfo %-prdbindir)/npumgr_vpmrun %{_prdbindir}/npumgr_vpm_append %{_prdbindir}/npumgr_sdk %endif
                %if (%{NPUMGR_VERSION} == "NPUMGR_2_0" )
                    %{_prabindir}/npumgr_simpletest %{_prdbindir}/npumgr_loadparsertest %{_prdbindir}/npumgr_executenetwork %{_prdbindir}/npumgr_ewtest %{_prdbindir}/npumgr_prioritytest %{_prdbindir}/npumgr_highmemory %{_prdbindir}/npumgr_advrun %{_prdbindir}/npumgr_dmabuf %{_prdbindir}/npu_perf_tool/*
                %endif

                %files ut-component-tomato
                %if (%{NPUMGR_VERSION} == "NPUMGR_2_0" )
                    %{_tomatodir}/*
                    %_prabindir//npumgr_ut_*
                    %{jbm_rw_root}/tizen-npumanager/*
                    /opt/usr/data/aifw-core/model/test_models/*
                %endif
                %if (%{NPUMGR_VERSION} == "NPUMGR_1_0" )
                    %files models
                    /opt/usr/apps/npumgr/sdk/*
                    /opt/usr/data/aifw-core/model/npu_manager/*
                %endif
                %files bm-tc
                %if (%{NPUMGR_VERSION} == "NPUMGR_2_0" )
                    %{jbm_rw_root}/tizen-npumanager/*
                %endif
