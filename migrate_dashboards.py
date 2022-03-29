import os
import pathlib

output_name_template = 'grafana-dashboard-{name}.yaml'
output_template = '''#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

{{- if .Values.monitoring.grafana }}
apiVersion: v1
kind: ConfigMap
metadata:
  name: "{{ template "pulsar.fullname" . }}-{{ .Values.grafana.component }}-dashboard-%(name_dash)s"
  namespace: {{ .Values.namespace }}
  labels:
    {{- include "pulsar.standardLabels" . | nindent 4 }}
    component: {{ .Values.grafana.component }}
    grafana_dashboard: "1"
data:
  %(name_underscore)s.json: |
    %(content)s
{{- end }}'''


def main():
    inputs_dir = pathlib.Path('dashboards.kubernetes')
    outputs_dir = pathlib.Path('dashboards.configs')
    outputs_dir.mkdir(exist_ok=True)
    for input_dashboard in inputs_dir.iterdir():
        print(input_dashboard)
        name = os.path.splitext(input_dashboard.name)[0]
        output_dashboard_name = output_name_template.format(name=name)
        output_dashboard = outputs_dir / output_dashboard_name
        with input_dashboard.open('r') as fin, output_dashboard.open('w') as fout:
            content = fin.read().replace('{{ PULSAR_CLUSTER }}', 'Prometheus')
            content = content.replace('{{PULSAR_CLUSTER}}', 'Prometheus')
            content = content.replace('{{ cluster }}', '{{ "{{ cluster }}" }}')
            content = content.replace('{{cluster}}', '{{ "{{ cluster }}" }}')
            content = content.replace('{{ namespace }}', '{{ "{{ namespace }}" }}')
            content = content.replace('{{namespace}}', '{{ "{{ namespace }}" }}')
            content = content.replace('{{ remote_cluster }}', '{{ "{{ remote_cluster }}" }}')
            content = content.replace('{{remote_cluster}}', '{{ "{{ remote_cluster }}" }}')
            content = content.replace('{{ mode }}', '{{ "{{ mode }}" }}')
            content = content.replace('{{mode}}', '{{ "{{ mode }}" }}')
            content = content.replace('{{ device }}', '{{ "{{ device }}" }}')
            content = content.replace('{{device}}', '{{ "{{ device }}" }}')
            content = content.replace('{{ fqfn }}', '{{ "{{ fqfn }}" }}')
            content = content.replace('{{fqfn}}', '{{ "{{ fqfn }}" }}')
            content = content.replace('{{ topic }}', '{{ "{{ topic }}" }}')
            content = content.replace('{{topic}}', '{{ "{{ topic }}" }}')
            content = content.replace('{{ quantile }}', '{{ "{{ quantile }}" }}')
            content = content.replace('{{quantile}}', '{{ "{{ quantile }}" }}')
            content = content.replace('{{ job }}', '{{ "{{ job }}" }}')
            content = content.replace('{{job}}', '{{ "{{ job }}" }}')
            content = content.replace('{{ p99 }}', '{{ "{{ p99 }}" }}')
            content = content.replace('{{p99}}', '{{ "{{ p99 }}" }}')
            content = content.replace('{{ slice }}', '{{ "{{ slice }}" }}')
            content = content.replace('{{slice}}', '{{ "{{ slice }}" }}')
            content = content.replace('{{ chip }}', '{{ "{{ chip }}" }}')
            content = content.replace('{{chip}}', '{{ "{{ chip }}" }}')
            content = content.replace('{{ sensor }}', '{{ "{{ sensor }}" }}')
            content = content.replace('{{sensor}}', '{{ "{{ sensor }}" }}')
            content = content.replace('{{ collector }}', '{{ "{{ collector }}" }}')
            content = content.replace('{{collector}}', '{{ "{{ collector }}" }}')
            content = content.replace('{{ coordinator_id }}', '{{ "{{ coordinator_id }}" }}')
            content = content.replace('{{coordinator_id}}', '{{ "{{ coordinator_id }}" }}')
            content = content.replace('{{ GF_LOKI_DATASOURCE_NAME }}', '{{ "{{ GF_LOKI_DATASOURCE_NAME }}" }}')
            content = content.replace('{{GF_LOKI_DATASOURCE_NAME}}', '{{ "{{ GF_LOKI_DATASOURCE_NAME }}" }}')
            content = content.replace('{{ kubernetes_pod_name }}', '{{ "{{ kubernetes_pod_name }}" }}')
            content = content.replace('{{kubernetes_pod_name}}', '{{ "{{ kubernetes_pod_name }}" }}')
            lines = content.split('\n')
            content = '\n    '.join(lines)
            output = output_template % dict(name_dash=name.replace('_', '-'), name_underscore=name.replace('-', '_'),
                                            content=content)
            fout.write(output)


if __name__ == '__main__':
    main()
