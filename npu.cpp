void printStatusDetails(const std::string& enumName) {
    static const std::unordered_map<std::string, int> statusMap = {
        {"NPUMGR_STATUS_ERR_FAIL", NPUMGR_STATUS_ERR_FAIL},
        {"NPUMGR_STATUS_ERR_TIMEOUT", NPUMGR_STATUS_ERR_TIMEOUT},
        {"NPUMGR_STATUS_ERR_UNKNOWN", NPUMGR_STATUS_ERR_UNKNOWN},
        {"NPUMHR_STATUS_SUCCESS", NPUMHR_STATUS_SUCCESS}
    };

    auto it = statusMap.find(enumName);
    if (it != statusMap.end()) {
        std::cout << "Enum: " << it->first << ", Code: " << it->second << std::endl;
    } else {
        std::cout << "Enum name not found!" << std::endl;
    }
}