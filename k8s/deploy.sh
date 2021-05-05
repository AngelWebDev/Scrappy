#!/bin/bash
kubectl apply -f app-deployment.yaml -f app-service.yaml -f mailer-deployment.yaml -f mailer-service.yaml
