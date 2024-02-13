# Installing Hadoop

Установим рандомные пакеты:
```bash
sudo apt install mc wget curl ssh rsync screen make ssh openssh-server
```
Скачаем Hadoop 2.10.2:
```bash
wget http://mirror.linux-ia64.org/apache/hadoop/common/hadoop-2.10.2/hadoop-2.10.2.tar.gz
```
Распакуем:
```bash
tar -xvf hadoop-2.10.2.tar.gz
```
Подключаем репозиторий в /etc/apt/sources.list
```bash
deb http://deb.debian.org/debian/ unstable main contrib non-free
```

Устанавливаем java:
```bash
sudo apt install openjdk-8-jdk openjdk-8-jre
```

Далее уберем из /etc/apt/sources.list добавленный ранее репозиторий.
Добавим в конец файла /etc/profile следующие строки:
```bash
JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
HADOOP_HOME=$HOME/hadoop-2.10.2
PATH=$PATH:$HADOOP_HOME/bin:$JAVA_HOME/bin
export HADOOP_HOME
export JAVA_HOME
export PATH
```
После перезапуска сессии эти изменения применятся и обновленные переменные окружения будут доступны в env:
```bash
env
```
Настроим беспарольный доступ по ssh к своем же машине:
```bash
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```

## Настройка Hadoop

В файл `hadoop-2.10.2/etc/hadoop/core-site.xml` вносим следующее:
```xml
<configuration>
    <property>
            <name>fs.defaultFS</name>
            <value>hdfs://192.168.122.8:9000</value>
    </property>
</configuration>
```
В файл `hadoop-2.10.2/etc/hadoop/hdfs-site.xml` вносим следующее:
```xml
<configuration>
    <property>
            <name>dfs.replication</name>
            <value>1</value>
    </property>
</configuration>
```
В файл `hadoop-2.10.2/etc/hadoop/mapred-site.xml` вносим следующее (предварительно его нужно создать на базе `hadoop-2.10.2/etc/hadoop/mapred-site.xml.template`):
```xml
<configuration>
    <property>
            <name>mapreduce.framework.name</name>
            <value>yarn</value>
    </property>
</configuration>
```
В файл `hadoop-2.10.2/etc/hadoop/yarn-site.xml` вносим следующее:
```xml
<configuration>
    <property>
            <name>yarn.nodemanager.aux-services</name>
            <value>mapreduce_shuffle</value>
    </property>
</configuration>
```
Также понадобятся скрипты из архива scripts.tar.gz на Google Drive, архив надо распаковать и переместить все файл в ~bin, например так:
```bash
tar -xvf scripts.tar.gz && sudo cp *.sh ~bin/
```

Дополнительно понадобится пропатчить скрипты Hadoop.
в libexec/hadoop-config.sh нужно следующее:
```bash
# Attempt to set JAVA_HOME if it is not set
if [[ -z $JAVA_HOME ]]; then
  # On OSX use java_home (or /Library for older versions)
  if [ "Darwin" == "$(uname -s)" ]; then
    if [ -x /usr/libexec/java_home ]; then
      export JAVA_HOME=($(/usr/libexec/java_home))
    else
      export JAVA_HOME=(/Library/Java/Home)
    fi
  fi

  # Bail if we did not detect it
  if [[ -z $JAVA_HOME ]]; then
    echo "Error: JAVA_HOME is not set and could not be found." 1>&2
    exit 1
  fi
fi
```
Поменять на вот это:
```bash
# Attempt to set JAVA_HOME if it is not set
if [[ -z $JAVA_HOME ]]; then
  # On OSX use java_home (or /Library for older versions)
  if [ "Darwin" == "$(uname -s)" ]; then
    if [ -x /usr/libexec/java_home ]; then
      export JAVA_HOME=($(/usr/libexec/java_home))
    else
      export JAVA_HOME=(/Library/Java/Home)
    fi
  fi
  export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

  # Bail if we did not detect it
  if [[ -z $JAVA_HOME ]]; then
    echo "Error: JAVA_HOME is not set and could not be found." 1>&2
    exit 1
  fi
fi
```
После чего запускаем скрипт форматирования:
```bash
hdpFormat.sh
```
Далее запускаем уже сам Hadoop:
```bash
hdpStart.sh
```

Web-интерфейс доступен по адресу:
`http://192.168.122.8:50070`