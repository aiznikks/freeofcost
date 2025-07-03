int sleep_usec = period * inner_ex_count;

if (inner_ex_count < 1 || inner_ex_count > MAX_INNER_COUNT ||
    sleep_usec <= 0 || sleep_usec > MAX_SLEEP * MAX_INNER_COUNT) {
    
    DLOGW("IntegTest: Invalid sleep values: period=%d, count=%d, total=%d → fallback %dus",
          period, inner_ex_count, sleep_usec, SAFE_SLEEP_FALLBACK);

    sleep_usec = SAFE_SLEEP_FALLBACK;
}

DLOGI("IntegTest: sleep for %d usec", sleep_usec);
usleep(sleep_usec);