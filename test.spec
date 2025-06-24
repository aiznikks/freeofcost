%if "%{?buildtype}" == "" || "%{buildtype}" == "test"
... test-related RPM stuff ...
%endif

%if "%{?buildtype}" == "" || "%{buildtype}" == "server"
... server-related RPM stuff ...
%endif






%if "%{?buildtype}" == "" || "%{buildtype}" == "test"

cp -rf %{buildroot}%{name}-%{version}/2.0/test/npu_perf_tool/inference.py %{buildroot}%{_prdbindir}/npu_perf_tool
if [ "%{CHIP_NAME}" = "CHIP_PONTUSM" ] || [ "%{CHIP_ROSEP}" = "1" ] || [ "%{CHIP_NAME}" = "CHIP_ROSEM" ]; then
    cp -rf %{buildroot}%{name}-%{version}/2.0/test/npu_perf_tool/memory.py %{buildroot}%{_prdbindir}/npu_perf_tool
fi

mkdir -p %{buildroot}%{_prdbindir}/%{CURRENT_MODE}
cp -rf %{buildroot}/%{_prdbindir}/%{CURRENT_MODE}/npu_perf_tool %{buildroot}%{_prdbindir}/%{CURRENT_MODE}/

# Debug files for test
mkdir -p %{buildroot}/opt/usr/data/aifw-core/model/test_models
cp -rf %{buildroot}/test_models/* %{buildroot}/opt/usr/data/aifw-core/model/test_models/

# Tomato UT-related test files
cp -rf %{buildroot}/tclist.xml %{buildroot}%{_tomatodir}/tclist.xml
cp -rf %{buildroot}/tomato_model.xml %{buildroot}%{_tomatodir}/tomato_model.xml
cp -rf %{_jbm_rw_root}/tizen-npumanager/* %{buildroot}/%{_jbm_rw_root}/tizen-npumanager/

%endif