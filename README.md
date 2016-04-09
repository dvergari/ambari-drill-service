# ambari-drill-service
Ambari service for Apache Drill

Ambari service to run and manage Apache Drill. For more information about Apache Drill visit <a href>https://drill.apache.org/</a>

  Features:
    - Allows to install Apache Drill on an Ambari-managed cluster
    - Edit drill-overrides.conf and drill-env.sh via ambari
    - Integration with zookeeper



### Setup

Download the Drill Service:

<code>
git clone https://github.com/dvergari/ambari-drill-service.git /var/lib/ambari-server/resources/stacks/HDP/2.4/services/DRILL 
</code>

Restart ambari

<code>
ambari-server restart
</code>

Now you can install Drill by clicking on "Add Service" button in Ambari
