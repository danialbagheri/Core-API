#!/bin/bash

base_dir="/var/www"

read -r -p "Enter project names (space-separated): " projects

for project in $projects; do
  project_dir="$base_dir/$project"

  if [ -d "$project_dir" ]; then
    echo "Deploying $project..."

    cd "$project_dir" || exit
    git pull
    docker-compose build && docker-compose up -d

    echo "Deployment of $project is complete."
  else
    echo "Project $project does not exist."
  fi
done
