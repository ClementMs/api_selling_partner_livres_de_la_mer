import json

import requests
import urllib3
import re
import json
import os

import awswrangler as wr
import pandas
from sellingpartnerapi import request as selling_partner_api_request, get_access_token_production_de_fr

def lambda_handler(event, context):


    
    conn = wr.postgresql.connect("postgres_jdbc_connexion")
    data = wr.postgresql.read_sql_query(sql = "SELECT * from information_schema.tables;", con = conn)
    print(data.shape)

    access_token_data = get_access_token_production_de_fr()

    access_token_de_fr = access_token_data['access_token']


    headers_prod = {'Content-Type': 'application/json','x-amz-access-token': access_token_de_fr}

    data_prod = selling_partner_api_request(method = "GET", url = 'https://sellingpartnerapi-eu.amazon.com/listings/2021-08-01/items/A3T4EQ2GGC5WWL?marketplaceIds=A13V1IB3VIYZZH',
                            headers=headers_prod,
                            _preload_content=None,
                            _request_timeout=None,
                            query_params=None)

    print(json.loads(data_prod.data))

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

