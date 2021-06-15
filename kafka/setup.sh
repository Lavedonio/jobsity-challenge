#!/bin/bash

wget https://downloads.apache.org/kafka/2.8.0/kafka_2.13-2.8.0.tgz
tar -xvf kafka_2.13-2.8.0.tgz
rm kafka_2.13-2.8.0.tgz
sudo mv kafka_2.13-2.8.0 $HOME
