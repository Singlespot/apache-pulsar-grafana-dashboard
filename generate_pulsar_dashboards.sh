#!/usr/bin/env bash

export PULSAR_PROMETHEUS_URL=PULSAR_PROMETHEUS_URL
export PULSAR_CLUSTER=prometheus
export PULSAR_CUSTOM_PROMETHEUS=yes
export GF_LOKI_URL=GF_LOKI_URL
export GF_LOKI_DATASOURCE_NAME=Loki

DASHBOARD_HOME=dashboards.kubernetes

scripts/generate_dashboards.sh
mv target/dashboards/zookeeper-3.6.json ${DASHBOARD_HOME}/
#rm -rf ${DASHBOARD_HOME}
#mkdir -p ${DASHBOARD_HOME}
#cp apache-pulsar-grafana-dashboard/dashboards.kubernetes/* ${DASHBOARD_HOME}
# rm kube-prometheus/grafana/data/dashboards/pulsar/zookeeper-3.6.json
sed -i '' 's/"jvm_memory_bytes_used{job=~\\".+\\"}"/"jvm_memory_bytes_used{component=~\\".+\\"}"/g' ${DASHBOARD_HOME}/logs.json
sed -i '' 's/"\/.*[^_]job=\\\\\\"(\[^\\\\\\"]+)\\\\\\".*\/"/"\/.*[^_]component=\\\\\\"([^\\\\\\"]+)\\\\\\".*\/"/g' ${DASHBOARD_HOME}/logs.json  # "\/.*[^_]component=\\\"([^\\\"]+)\\\".*\/"
for item in $(ls ${DASHBOARD_HOME}); do
  sed -i '' 's/"count(bookie_SERVER_STATUS{cluster=~\\"$cluster\\", kubernetes_pod_name=~\\"$kubernetes_pod_name\\"} == 0)\\n"/"count(bookie_SERVER_STATUS{cluster=~\\"$cluster\\", kubernetes_pod_name=~\\"$kubernetes_pod_name\\"} == 0) or vector(0)\\n"/g' ${DASHBOARD_HOME}/${item}
  sed -i '' "s/kubernetes_pod_name/pod/g" ${DASHBOARD_HOME}/${item}
  sed -i '' "s/pod_name/pod/g" ${DASHBOARD_HOME}/${item}
  sed -i '' 's/app=\\"pulsar\\"/app=\\"sn-platform\\"/g' ${DASHBOARD_HOME}/${item}
  sed -i '' 's/persistentvolumeclaim=~\\"\.\*bookie-journal\.\*\\"/persistentvolumeclaim=~\\".*journal.*bookie.*\\"/g' ${DASHBOARD_HOME}/${item}
  sed -i '' 's/persistentvolumeclaim=~\\"\.\*bookie-ledgers\.\*\\"/persistentvolumeclaim=~\\".*ledgers.*bookie.*\\"/g' ${DASHBOARD_HOME}/${item}
  sed -i '' 's/bookie_ledger_dir__pulsar_data_bookkeeper_ledgers_usage/bookie_ledger_dir__pulsar_data_bookkeeper_ledgers_0_usage/g' ${DASHBOARD_HOME}/${item}
  sed -i '' 's/container_name/container/g' ${DASHBOARD_HOME}/${item}
  sed -i '' 's/"title": "pulsar_detector"/"title": "Pulsar detector"/g' ${DASHBOARD_HOME}/${item}
  sed -i '' "s/{{ PULSAR_CLUSTER }}/${PULSAR_CLUSTER}/g" ${DASHBOARD_HOME}/${item}
  sed -i '' "s/{{ GF_LOKI_DATASOURCE_NAME }}/${GF_LOKI_DATASOURCE_NAME}/g" ${DASHBOARD_HOME}/${item}
  sed -i '' "s/DS_TEST-CLUSTER/DS_PROMETHEUS/g" ${DASHBOARD_HOME}/${item}
done
