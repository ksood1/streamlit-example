import json
import pandas as pd
import os

os.getcwd()
os.listdir()
os.listdir("../..")

# set `<your-endpoint>` and `<your-key>` variables with the values from the Azure portal


with open("karan_config_key-copy.json") as config:
    config_json = json.load(config)
config_json

key = config_json["azure_doc_intel_key"]
endpoint = config_json["azure_doc_intel_endpoint"]

document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
with open("Client Call Center Strategy RFP_vFinal.pdf", "rb") as f:
    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-document", document=f
    )
doc_components = poller.result()

paragraphs = []
for doc_idx, doc in enumerate(doc_components.paragraphs):
    paragraph = {}
    paragraph["id"] = doc_idx
    paragraph["role"] = doc.role
    paragraph["content"] = doc.content
    for bounding_idx, bounding_region in enumerate(doc.bounding_regions):
        paragraph["page_number"] = bounding_region.page_number
        paragraph["polygon"] = bounding_region.polygon
    paragraphs.append(paragraph)  
paragraphs[0]


df_paragraphs = pd.json_normalize(paragraphs)
df_paragraphs

df_paragraphs.to_csv('Client Call Center Strategy RFP_vFinal_paragraphs.csv')


tables_json = []
for table_idx, table in enumerate(doc_components.tables):
    for cell_idx, cell in enumerate(table.cells):
        table_json = {}
        table_json["table_id"] =  table_idx
        table_json["cell_id"] = cell_idx
        table_json["kind"] = cell.kind
        table_json["row_index"] =  cell.row_index
        table_json["column_index"] = cell.column_index
        table_json["row_span"] = cell.row_span
        table_json["column_span"] = cell.column_span
        table_json["content"] = cell.content
        tables_json.append(table_json)
tables_json[100:102]

df_tables = pd.json_normalize(tables_json)
df_tables

df_tables.to_csv("Client Call Center Strategy RFP_tables.csv")
