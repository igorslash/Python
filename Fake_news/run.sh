#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

case "$1" in
    build)
        echo -e "${BLUE}Building Docker image...${NC}"
        docker-compose build
        ;;
    train)
        echo -e "${GREEN}Starting training...${NC}"
        docker-compose up training
        ;;
    train-detached)
        echo -e "${GREEN}Starting training in background...${NC}"
        docker-compose up -d training
        ;;
    tensorboard)
        echo -e "${BLUE}Starting TensorBoard at http://localhost:6006${NC}"
        docker-compose up tensorboard
        ;;
    stop)
        echo -e "${BLUE}Stopping all containers...${NC}"
        docker-compose down
        ;;
    clean)
        echo -e "${BLUE}Cleaning up...${NC}"
        docker-compose down -v
        docker system prune -f
        ;;
    logs)
        docker-compose logs -f training
        ;;
    shell)
        docker-compose run --rm training bash
        ;;
    *)
        echo "Usage: $0 {build|train|train-detached|tensorboard|stop|clean|logs|shell}"
        exit 1
        ;;
esac