#!/bin/bash

beeline -u jdbc:hive2://localhost:10000 -n user < hiveInitialize.sql 

beeline -u jdbc:hive2://localhost:10000 -n user < queryExamples.sql