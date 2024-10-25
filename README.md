PROJEKT ZESPOŁOWY:

Installation:




1.

```python
python -m venv venv
```

2.

```python
venv/scripts/activate
```

3.

```python
pip install -r requirements.txt
```

4. Install pyspark from [https://spark.apache.org/downloads.html]() and put it in *C:\Spark* then add SPARK_HOME variable in your User Environment Variables with path: *C:\Spark\spark-3.5.3-bin-hadoop3.5*
5. Get winutils from [https://github.com/cdarlint/winutils/blob/master/hadoop-3.3.6/bin/winutils.exe]() and hadoop.dll from [https://github.com/cdarlint/winutils/blob/master/hadoop-3.3.6/bin/hadoop.dll]() and create a directory *C:\hadoop\bin.* Add HADOOP_HOME variable in your User Environment Variables with path: *C:\hadoop.* Add the two files to *bin.*
