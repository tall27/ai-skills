# NGTS platform operation endpoints

Base URL: `https://api.strata.paloaltonetworks.com/ngts`. Read `../../_shared/conventions.md`.

## Event Logs

| Method | Path | Action | Main input | Response |
|---|---|---|---|---|
| POST | `/v1/activitylogsearch` | Search activity logs and retrieve count | `ActivityLogFilter` | `ActivityLogEntriesResponse` |
| POST | `/v1/activitylogsearch/export` | Export filtered activity-log data | `ActivityLogFilter` | `ExportedActivityLogEntryInformation[]`; JSON/CSV |
| GET | `/v1/activitytypes` | List activity types | None | `ActivityLogType[]` |

`ActivityLogEntryInformation` includes `id`, `activityName`, `activityType`, `activityDate`, `criticality`, `message`, `payload`, and `tsgId`.

Source: [NGTS OpenAPI](https://raw.githubusercontent.com/PaloAltoNetworks/pan.dev/master/openapi-specs/scm/config/ngts/tlsprotect-cloud.json).
