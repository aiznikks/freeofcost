# freeofcost

#include "npumgr_api.h"
#include <unordered_map>
#include <string>
#include <stdio.h> // Use your project's logger if needed

// Step 1: Function to map status codes to their enum names
const char* getNpumgrStatusName(int statusCode) {
    static const std::unordered_map<int, const char*> statusMap = {
        {-8, "NPUMGR_STATUS_ERR_FAIL"},
        {-2, "NPUMGR_STATUS_ERR_TIMEOUT"},
        {-1, "NPUMGR_STATUS_ERR_UNKNOWN"},
        {0,  "NPUMHR_STATUS_SUCCESS"}
        // Add more enum values here as needed
    };

    auto it = statusMap.find(statusCode);
    return it != statusMap.end() ? it->second : "Unknown NPU Status";
}

// Step 2: Replace the old macro with this clean version
#define CHECK_STATUS(status, lbl) \
    do { \
        if (NPUMHR_STATUS_SUCCESS != status) { \
            NPU_CONTROL_IMPL_ERROR("Error [%d]: %s", status, getNpumgrStatusName(status)); \
            goto lbl; \
        } \
    } while (0)

// Step 3: Use the macro normally
// Example:
// CHECK_STATUS(api_call_status, fail_handler);
//
// Output if status = -2:
// Error [-2]: NPUMGR_STATUS_ERR_TIMEOUT
