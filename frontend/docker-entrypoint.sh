#!/bin/sh
set -e
: "${PORT:=8080}"
: "${TRIAGE_API_URL:=http://localhost:8003/triage}"
cat > /usr/share/nginx/html/env.js <<EOF
window.__ENV = {
  TRIAGE_API_URL: "${TRIAGE_API_URL}"
};
EOF
envsubst '${PORT}' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf
