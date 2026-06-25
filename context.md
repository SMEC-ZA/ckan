# CKAN — Context & Deployment Notes

This is the upstream **CKAN 2.11** source repository (`github.com/ckan/ckan`), used as a reference and for local extension development. The running instance is deployed on the Cortex server (`10.12.5.23`) via Docker as part of the HorizonAI Collective data platform.

---

## Deployment

- **Live URL**: `http://10.12.5.23:5210`
- **Docker image**: `ckan/ckan-base:2.11`
- **Container name**: `ckan-dev`
- **Compose file**: `~/horizon-ai/deploy/docker-compose.cortex.yml` (Section 19)

### Active Plugins

```
image_view  text_view  datatables_view  datastore  datapusher  envvars  chat
```

The `chat` plugin is **ckanext-chat** — a third-party extension injected at runtime via the `ckan-plugins` deploy directory. It is not part of this source tree.

---

## Supporting Services

| Service | Internal address | Purpose |
| :--- | :--- | :--- |
| `ckan-db` | `ckan-db:5432` | PostGIS 15 — `ckan_default` & `datastore_default` databases |
| `ckan-solr` | `ckan-solr:8983` | Solr 9 search index (`ckan/ckan-solr:2.11-solr9`) |
| `ckan-redis` | `ckan-redis:6379` | Job queue and cache |
| `ckan-datapusher` | `ckan-datapusher:8800` | Tabular data ingestion |
| `litellm` | `litellm:4000` | LLM proxy — used by ckanext-chat |

---

## ckanext-chat Integration

The `chat` plugin is installed at container startup by a custom entrypoint script. It routes LLM requests through the Cortex LiteLLM proxy (`http://litellm:4000/v1`) to the local `cortex-coder` model (Qwen2.5-Coder-32B).

See `~/horizon-ai/deploy/ckan-plugins/context.md` for full details on the injection mechanism.

---

## CKAN vs GeoNetwork — Division of Roles

These two services are deployed together and are **complementary**, not overlapping:

| Concern | CKAN (`5210`) | GeoNetwork (`8080`) |
| :--- | :--- | :--- |
| **Primary purpose** | Structured data portal | Document & metadata library |
| **Content type** | Datasets, tabular resources, uploaded files | ISO 19139 metadata records for reports/documents |
| **Search** | Solr full-text + DataStore SQL queries | ISO metadata fields + spatial/corridor extent |
| **Spatial link** | — | `document_corridor_link` table joins GeoNetwork UUIDs to LRS `corridor_segment_id` |
| **AI interface** | ckanext-chat → LiteLLM conversational queries | — |
| **Ingestion** | DataPusher, manual upload, API | `scripts/push_record_to_geonetwork.py` (called from n8n / librarian agent) |

**GeoNetwork is the document library.** It holds NRMP technical reports (ITAs, engineering reports, network statements, standards, academic references) as formal ISO 19139 records, each spatially tagged to a corridor segment (e.g. `OOG-LEP-014`). The `document_corridor_link` PostGIS table in the main NRMP database enables queries like *"all documents touching the Oogies–Lephalale corridor"*.

**CKAN is the data catalogue.** It manages structured datasets (tabular data, shapefiles, file resources) and provides AI-assisted discovery via the `chat` plugin.

---

## Local Development

This repo is a **read-only reference clone** of upstream CKAN. Extension development happens in separate repos (e.g. `ckanext-chat`). Do not build or run CKAN directly from this directory for the Cortex deployment.
