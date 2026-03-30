# Instructions

## Cluster Requirements

- DSPA requires PVCs (check available StorageClasses)
- The `mlops-kfp` namespace requires the `opendatahub.io/dashboard: 'true'` label to show as a Data Science Project

### 1. Create the mlops-kfp namespace and deploy the Data Science Pipelines Application

```bash
oc apply -f dspa.yaml
```

Wait for pods to be ready:

```bash
oc get pods -n mlops-kfp -w
```

You should see `ds-pipeline-dspa-*`, `mariadb-dspa-*`, and `minio-dspa-*` pods running.

### 2. Upload the pipeline

Generate the pipeline by running the command ```python3 pipeline.py```. This creates the file ```pipeline.yaml```.

Option A - RHOAI Dashboard:
- Navigate to Data Science Pipelines > Import Pipeline
- Upload `pipeline.yaml`

Option B - CLI:
```bash
DSPA_ROUTE=$(oc get route -n mlops-kfp -l app=ds-pipeline-dspa -o jsonpath='{.items[0].spec.host}')
kfp pipeline upload -p mlops-inner-loop pipeline.yaml --endpoint "https://${DSPA_ROUTE}"
```

### 3. Create FlightCtl URL Secret

Create a secret in the data science project namespace pointing to a FlightCtl instance

```bash
oc create secret generic flightctl-url \
  --from-literal=url=https:FLIGHTCTL_URL:3443 \
  -n mlops-kfp
```

## Running the Pipeline

1. Open RHOAI Dashboard > Data Science Pipelines > mlops-inner-loop
2. Create Run
3. Fill in parameters:
   - `alert_name`: `VLLMHighLatency` (or any descriptive name)
   - `severity`: `warning` or `critical`
   - `device_id`: `edge-001` (or the actual device name)
   - `flightctl_url`: copy the URL to your FlightCtl instance
4. Start

## Pipeline Explanation

### Pipeline Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `alert_name` | `VLLMHighLatency` | Name of the alert that triggered the run |
| `severity` | `warning` | Alert severity level |
| `device_id` | `unknown` | Edge device identifier |
| `flightctl_url` | (empty) | FlightCtl URL for the location to deploy the model|

### Pipeline Steps

#### 1. log_alert
Logs the alert context (name, severity, device ID). Passes context to the next step.

#### 2. simulate_retraining
Runs a fake training loop: 5 epochs, 5 seconds each, with decreasing loss and increasing accuracy. Generates a version tag like `v1.0.20260318` based on the current date.

#### 3. register_model
Prints a mock model registration log (name, version, artifact URI). In a real pipeline, this would call the Model Registry API.

#### 4. trigger_outer_loop
POSTs to the GitHub Actions API to trigger the `model-refresh-build.yaml` workflow with the generated model version. This kicks off the outer loop: rebuild modelcar, update quadlets, update fleet.yaml, push to fleet devices.