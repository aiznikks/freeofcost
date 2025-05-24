#include "npumgr_api.h"
#include <unordered_map>
#include <string>
#include <stdio.h> // Or your project’s logger

// Step 1: Function to map status codes to their enum names
const char* getNpumgrStatusName(int statusCode) {
    static const std::unordered_map<std::string, int> statusMap = {
        {"NPUMGR_STATUS_ERR_FAIL",    NPUMGR_STATUS_ERR_FAIL},
        {"NPUMGR_STATUS_ERR_TIMEOUT", NPUMGR_STATUS_ERR_TIMEOUT},
        {"NPUMGR_STATUS_ERR_UNKNOWN", NPUMGR_STATUS_ERR_UNKNOWN},
        {"NPUMHR_STATUS_SUCCESS",     NPUMHR_STATUS_SUCCESS}
    };

    for (const auto& entry : statusMap) {
        if (entry.second == statusCode) {
            return entry.first.c_str(); // Return enum name
        }
    }

    return "Unknown NPU Status";
}







//2nd

#define CHECK_STATUS(status, lbl) \
    do { \
        if (NPUMHR_STATUS_SUCCESS != status) { \
            NPU_CONTROL_IMPL_ERROR("Error [%d]: %s", status, getNpumgrStatusName(status)); \
            goto lbl; \
        } \
    } while (0)