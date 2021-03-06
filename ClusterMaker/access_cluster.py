#!/usr/bin/env python3
#
################################################################################
# Name:         access_cluster.py
# Author:       Rodney Marable <rodney.marable@gmail.com>
# Created On:   April 20, 2019
# Last Changed: May 10, 2019
# Purpose:	Provide a mechanism for SSH-ing into pcluster master instances
################################################################################

# Load some required Python libraries

import argparse
import subprocess

# Import some external lists.
# Source: parallelclustermaker_aux_data.py

from parallelclustermaker_aux_data import p_fail

# Parse input from the command line.

parser = argparse.ArgumentParser(description='access_cluster.py: Provide quick SSH access to ParallelCluster head nodes')

# Configure arguments for the required variables.

parser.add_argument('--cluster_name', '-N', help='full name of the cluster (example: rmarable-stage02)', required=True)
parser.add_argument('--prod_level', '-P', choices=['dev', 'test', 'stage', 'prod'], help='operating level of the cluster (default = dev)', required=False, default='dev')

args = parser.parse_args()
cluster_name = args.cluster_name
prod_level = args.prod_level

cmd_string = 'python3 cluster_data/' + prod_level + '/' + cluster_name + '/access_cluster.' + cluster_name + '.py'
subprocess.run(cmd_string, shell=True)
