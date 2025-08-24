#!/usr/bin/env bash
# setup-docker.sh
# Prepara servidor Ubuntu 24.04 com Docker Engine + Docker Compose Plugin v2
# e adiciona o usuário 'pedroct' ao grupo docker.

set -euo pipefail

USER_TO_ADD="${1:-pedroct}"

echo "==> Verificando privilégios..."
if [[ "$(id -u)" -ne 0 ]]; then
  echo "Este script precisa rodar como root. Tente: sudo bash setup-docker.sh"
  exit 1
fi

echo "==> Detectando distribuição..."
source /etc/os-release
if [[ "${ID:-}" != "ubuntu" || "${VERSION_ID:-}" != "24.04" ]]; then
  echo "Aviso: script foi escrito para Ubuntu 24.04; detectado ${PRETTY_NAME:-desconhecido}."
  echo "Continuando assim mesmo em 5s... (Ctrl+C para abortar)"; sleep 5
fi

echo "==> Removendo instalações antigas conflitantes (se houver)..."
apt-get remove -y docker.io docker-doc docker-compose docker-compose-v2 \
  podman-docker containerd runc || true

echo "==> Instalando dependências base..."
apt-get update -y
apt-get install -y ca-certificates curl gnupg lsb-release

echo "==> Configurando repositório oficial Docker..."
install -m 0755 -d /etc/apt/keyrings
if [[ ! -f /etc/apt/keyrings/docker.gpg ]]; then
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
    | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  chmod a+r /etc/apt/keyrings/docker.gpg
fi

ARCH="$(dpkg --print-architecture)"
UBU_CODENAME="$(. /etc/os-release && echo "$VERSION_CODENAME")"
echo \
  "deb [arch=${ARCH} signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu ${UBU_CODENAME} stable" \
  > /etc/apt/sources.list.d/docker.list

echo "==> Instalando Docker Engine + Compose Plugin..."
apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "==> Habilitando e iniciando serviços..."
systemctl enable docker
systemctl enable containerd
systemctl restart containerd
systemctl restart docker

echo "==> Adicionando usuário '${USER_TO_ADD}' ao grupo docker..."
if id -u "${USER_TO_ADD}" >/dev/null 2>&1; then
  usermod -aG docker "${USER_TO_ADD}"
else
  echo "Usuário '${USER_TO_ADD}' não encontrado. Pulei a etapa de grupo."
fi

# (Opcional) Configuração mínima do daemon.json, se não existir
DOCKER_DAEMON_JSON="/etc/docker/daemon.json"
if [[ ! -f "${DOCKER_DAEMON_JSON}" ]]; then
  echo '{
  "log-driver": "json-file",
  "log-opts": { "max-size": "10m", "max-file": "3" }
}' > "${DOCKER_DAEMON_JSON}"
  systemctl restart docker
fi

echo "==> Testando instalação..."
docker --version
docker compose version || true

echo "==> Testando execução de container (hello-world)..."
# roda em root só para teste rápido; depois você usará como 'pedroct'
docker run --rm hello-world || true

echo
echo "✅ Concluído!"
echo "- Docker: $(docker --version)"
echo "- Compose: $(docker compose version || echo 'compose plugin indisponível')"
echo
if id -nG "${USER_TO_ADD}" 2>/dev/null | grep -qw docker; then
  echo "⚠️  Saia e entre novamente na sessão do usuário '${USER_TO_ADD}' (ou 'newgrp docker') para aplicar o grupo."
fi
