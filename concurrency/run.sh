#!/bin/sh
type="$1"
if [ "$type" == "akka" ] 
then
    mvn exec:java -Dexec.mainClass="akka.Main" -Dexec.args="indi.tamvm.blog.AppAkka"
else
    mvn exec:java -Dexec.mainClass="indi.tamvm.blog.App" 
fi; 
