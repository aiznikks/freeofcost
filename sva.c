constexpr int MIN_SLEEP_USEC = 1;
constexpr int MAX_SLEEP_USEC = 1000000;
constexpr int MAX_INNER_COUNT = 10000;

int sleep_usec = period * inner_ex_count;

if (period < MIN_SLEEP_USEC || period > MAX_SLEEP_USEC ||
    inner_ex_count < 1 || inner_ex_count > MAX_INNER_COUNT ||
    sleep_usec <= 0 || sleep_usec > MAX_SLEEP_USEC * MAX_INNER_COUNT) {

    DLOGW("IntegTest: Invalid sleep values (period=%d, count=%d, total=%d). Using fallback 1000us.",
          period, inner_ex_count, sleep_usec);
    sleep_usec = 1000;
}

DLOGI("IntegTest: sleep for %d usec", sleep_usec);
usleep(sleep_usec);