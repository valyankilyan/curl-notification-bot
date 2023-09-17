#!/bin/bash
set -ex

if ! [[ -f .env ]]; then
    echo "Error: .env file not found. Create it from dotenv_example"
    exit 1
fi

SERVER_IP_ADDRESS=${SERVER_IP_ADDRESS:-"51.250.11.18"}
URL=${URL:-"curly-notifier.vkiel.com"}
REMOTE_DIR=${REMOTE_DIR:-"/var/curly-notifier"}
SSH_USER=${SSH_USER:-"val-kiel"}
SSH_KEY=${SSH_KEY:-"~/.ssh/yc"}


ssh -i "${SSH_KEY}" "${SSH_USER}@${SERVER_IP_ADDRESS}" << 'ENDSSH'
  if [ ! -d "/var/curly-notifier" ]; then
    sudo mkdir -p /var/curly-notifier
    sudo groupadd -f curly-notifier
    USERNAME=$(whoami)
    sudo usermod -aG curly-notifier $USERNAME
    sudo chown :curly-notifier /var/curly-notifier
    sudo chmod 770 /var/curly-notifier
  fi
ENDSSH


ssh -i "${SSH_KEY}" "${SSH_USER}@${SERVER_IP_ADDRESS}" << 'ENDSSH'
  if [ "$(lsb_release -is)" = "Ubuntu" ]; then
    if ! [ -x "$(command -v docker)" ]; then
      sudo apt update
      sudo apt install -y docker.io
      sudo systemctl start docker
      sudo systemctl enable docker
    fi
    if ! [ -x "$(command -v docker-compose)" ]; then
      sudo apt install -y docker-compose
    fi
    if ! [ -x "$(command -v jq)" ]; then
      sudo apt update && sudo apt install -y jq
    fi
  else
    echo "Warning: Script is designed for Ubuntu, compatibility issues may occur."
  fi
ENDSSH

ssh -i "${SSH_KEY}" "${SSH_USER}@${SERVER_IP_ADDRESS}" << 'ENDSSH'
  # Install Certbot if it's not already installed
  URL=curly-notifier.vkiel.com
  if ! [ -x "$(command -v certbot)" ]; then
    if [ "$(lsb_release -is)" = "Ubuntu" ]; then
      sudo apt update
      sudo apt install -y certbot python3-certbot-nginx
    else
      echo "Warning: Certbot installation is not supported on this system."
      exit 1
    fi
  fi

  # Create an Nginx configuration for the domain
  sudo certbot --nginx -d $URL
  sudo nginx -t && sudo systemctl reload nginx
ENDSSH


FILES=(".env" "docker_compose_up.sh" "docker-compose.yaml")

for FILE in "${FILES[@]}"; do
  scp -i "${SSH_KEY}" "$FILE" "${SSH_USER}@${SERVER_IP_ADDRESS}:${REMOTE_DIR}/"
done


ssh -i "${SSH_KEY}" "${SSH_USER}@${SERVER_IP_ADDRESS}" "cd ${REMOTE_DIR} && sudo bash docker_compose_up.sh"
