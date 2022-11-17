#!/bin/bash

until $(curl --output /dev/null --silent --head --fail http://localhost:2368); do
    echo 'Waiting for ghost container'
    sleep 5
done

until $(curl --output /dev/null --silent --head --fail http://localhost:8802/admin/); do
    echo 'Waiting for django container'
    sleep 5
done