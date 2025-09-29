#!/bin/bash
# Boot Recovery Script for Logivore
# This script runs at boot time to ensure all services start properly

# Configuration
LOG_FILE="/var/log/logivore-boot-recovery.log"
BOT_USER="logivore"  # Change to your bot user
DOCKER_COMPOSE_DIRS=("/opt/docker-apps" "/home/$BOT_USER/docker")  # Add your docker-compose directories

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

log_message "=== Boot Recovery Script Started ==="

# Wait for system to be ready
sleep 30

# 1. Start Docker service if not running
if ! systemctl is-active --quiet docker; then
    log_message "Starting Docker service..."
    systemctl start docker
    sleep 5
fi

# 2. Start Docker containers with restart policies
log_message "Starting Docker containers with restart policies..."
docker container ls -a --filter "restart-policy=always" --format "{{.Names}}" | while read container; do
    if [ ! -z "$container" ]; then
        log_message "Starting container: $container"
        docker start "$container" 2>&1 | tee -a "$LOG_FILE"
    fi
done

# 3. Start docker-compose services
for compose_dir in "${DOCKER_COMPOSE_DIRS[@]}"; do
    if [ -d "$compose_dir" ]; then
        log_message "Checking docker-compose services in: $compose_dir"
        find "$compose_dir" -name "docker-compose.yml" -o -name "docker-compose.yaml" | while read compose_file; do
            compose_dir_path=$(dirname "$compose_file")
            log_message "Starting services in: $compose_dir_path"
            cd "$compose_dir_path"
            docker-compose up -d 2>&1 | tee -a "$LOG_FILE"
        done
    fi
done

# 4. Set proper Docker restart policies for running containers
log_message "Setting restart policies for running containers..."
docker ps --format "{{.Names}}" | while read container; do
    if [ ! -z "$container" ]; then
        docker update --restart=unless-stopped "$container" 2>&1 | tee -a "$LOG_FILE"
    fi
done

# 5. Start custom systemd services (define your services here)
CUSTOM_SERVICES=()  # Add your services like: ("nginx" "mysql" "redis")

for service in "${CUSTOM_SERVICES[@]}"; do
    if systemctl list-unit-files | grep -q "^$service.service"; then
        log_message "Starting service: $service"
        systemctl start "$service" 2>&1 | tee -a "$LOG_FILE"
    fi
done

# 6. Wait for Logivore to start and trigger recovery
sleep 60
log_message "Triggering Logivore recovery check..."

# Send a signal to the bot (you can customize this)
# For example, create a file that the bot checks for
touch /tmp/logivore-boot-recovery-trigger

log_message "=== Boot Recovery Script Completed ==="
