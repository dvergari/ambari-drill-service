"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""
import sys, os, pwd, grp, io
from resource_management import *
from resource_management.libraries.functions import check_process_status

class Master(Script):
  def install(self, env):
    import params
    Execute('echo Installing packages')

    self.create_linux_user(params.drill_user, params.drill_group)

    Directory([params.drill_install_dir,params.drill_log_dir], mode=0755, owner=params.drill_user, group=params.drill_group, recursive=True)
    File(params.drill_log_file, mode=0644, owner=params.drill_user, group=params.drill_group, content='')
    
    if not os.path.exists(params.drill_temp_file):
      Execute('wget http://it.apache.contactlab.it/drill/drill-1.6.0/apache-drill-1.6.0.tar.gz -O ' + params.drill_temp_file + ' -a ' + params.drill_log_file, user=params.drill_user)
    Execute('tar -xzvf ' + params.drill_temp_file + ' -C ' + params.drill_install_dir + ' >> ' + params.drill_log_file + ' 2>&1')

    self.configure(env, True)

  def stop(self, env):
    import params
    self.configure(env)
    Execute(params.drill_install_dir + '/apache-drill-1.6.0/bin/drillbit.sh stop', user=params.drill_user)

  def start(self, env):
    import params
    self.configure(env)
    Execute(params.drill_install_dir + '/apache-drill-1.6.0/bin/drillbit.sh start', user=params.drill_user)

  def status(self, env):
    import params
    env.set_params(params)
    check_process_status(params.drill_pid_file)

  def configure(self, env, isInstall=False):
    import params
    env.set_params(params)

    drill_override_content=InlineTemplate(params.drill_override_content)
    drill_env_content=InlineTemplate(params.drill_env_content)

    if isInstall:
      Execute('chown -R ' + params.drill_user + ':' + params.drill_group + ' ' + params.drill_install_dir)

    File(params.drill_install_dir + '/apache-drill-1.6.0/conf/drill-override.conf', content=drill_override_content, owner=params.drill_user, group=params.drill_group)
    File(params.drill_install_dir + '/apache-drill-1.6.0/conf/drill-env.sh', content=drill_env_content, owner=params.drill_user, group=params.drill_group)
    XmlConfig("hdfs-site.xml", 
              conf_dir=params.drill_install_dir + '/apache-drill-1.6.0/conf',
              configurations=params.config['configurations']['hdfs-site'],
              configuration_attributes=params.config['configuration_attributes']['hdfs-site'],
              owner=params.drill_user,
              group=params.drill_group,
              mode=0644)
    XmlConfig("core-site.xml", 
              conf_dir=params.drill_install_dir + '/apache-drill-1.6.0/conf',
              configurations=params.config['configurations']['core-site'],
              configuration_attributes=params.config['configuration_attributes']['core-site'],
              owner=params.drill_user,
              group=params.drill_group,
              mode=0644)
    Execute('hdfs dfs -mkdir -p ' + params.sys_store_provider_zk_blobroot, user='hdfs')
    Execute('hdfs dfs -chown -R ' + params.drill_user + ':' + params.drill_group + ' ' + params.sys_store_provider_zk_blobroot, user='hdfs')

  def create_linux_user(self, user, group):
    try: pwd.getpwnam(user)
    except KeyError: Execute('adduser ' + user)
    try: grp.getgrnam(group)
    except KeyError: Execute('groupadd ' + group)



if __name__ == "__main__":
  Master().execute()
