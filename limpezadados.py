# -*- coding: utf-8 -*-
"""limpezaDados.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1oID7eKAOCOTGN-Kxy_jxurgF_WKQI2sc
"""

import pyspark
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()

produtos = spark.read.csv("/content/drive/MyDrive/Material de apoio - M27/produtos.csv", header=True, inferSchema=True)
vendedores = spark.read.csv("/content/drive/MyDrive/Material de apoio - M27/vendedores.csv", header=True, inferSchema=True)
clientes = spark.read.csv("/content/drive/MyDrive/Material de apoio - M27/clientes.csv", header=True, inferSchema=True)
itens_pedido = spark.read.csv("/content/drive/MyDrive/Material de apoio - M27/itens_pedido.csv", header=True, inferSchema=True)
pagamentos_pedido = spark.read.csv("/content/drive/MyDrive/Material de apoio - M27/pagamentos_pedido.csv", header=True, inferSchema=True)
avaliacoes_pedido = spark.read.csv("/content/drive/MyDrive/Material de apoio - M27/avaliacoes_pedido.csv", header=True, inferSchema=True)
pedidos = spark.read.csv("/content/drive/MyDrive/Material de apoio - M27/pedidos.csv", header=True, inferSchema=True)

print('dataframe produto; \n', produtos.show(n=5, truncate=False))
print('dataframe vendedores; \n', vendedores.show(n=5, truncate=False))
print('dataframe clientes; \n', clientes.show(n=5, truncate=False))
print('dataframe itens_pedido; \n', itens_pedido.show(n=5, truncate=False))
print('dataframe pagamentos_pedido; \n', pagamentos_pedido.show(n=5, truncate=False))
print('dataframe avaliacoes_pedido; \n', avaliacoes_pedido.show(n=5, truncate=False))
print('dataframe pedidos; \n', pedidos.show(n=5, truncate=False))

# acessar colunas
from pyspark.sql.functions import col
clientes.select("id_cliente").show(n=5, truncate=False)

clientes.select(col("id_cliente")).show(1)
clientes.select(clientes['id_cliente']).show(1)
clientes.select(clientes.id_cliente).show(1)

# Tratando valores nulos
produtos_trat_null = produtos.na.fill({'categoria_produto': 'Não especificado'})

produtos_trat_null.filter(col('categoria_produto') == 'Não especificado').count()

print('Total de pedidos: ', pedidos.count())

pedidos_unicos = pedidos.dropDuplicates()
print('Total de pedidos únicos: ', pedidos_unicos.count())

pedidos_remove_nulos = pedidos_unicos.na.drop()
print('Total de pedidos após remover nulos: ', pedidos_remove_nulos.count())

id_pedidos_revome_nulos = pedidos_unicos.na.drop(subset=['id_cliente', 'id_pedido']) # subset especifica o que deve ser deletado
print('Total de pedidos após remover nulos: ', id_pedidos_revome_nulos.count())

# fazer varredura em várias colunas
colunas = ['peso_produto_g', 'comprimento_produto_cm', 'altura_produto_cm', 'largura_produto_cm']

for coluna in colunas:
  produtos = produtos.na.fill({coluna:0})

produtos.write.mode('overwrite').option('header', 'true').csv('/content/drive/MyDrive/Colab Notebooks/produtos_tratados.csv')

spark.read.option('header', 'true').csv('/content/drive/MyDrive/Colab Notebooks/produtos_tratados.csv').show(5)

spark.stop()