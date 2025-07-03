app = g_slice_new(loadmgr_app_param);
if (!app)
    return FALSE;

if (!_check_json_param(reader, PRIORITY, STRING)) goto fail;
...
if (!_check_json_param(reader, SWITCH_THRESH, INT)) goto fail;
...
if (app->device_affinity == NULL) goto fail;
...

return TRUE;

fail:
    g_slice_free(loadmgr_app_param, app);
    return FALSE;