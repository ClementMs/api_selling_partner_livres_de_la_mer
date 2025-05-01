import json

import requests
import urllib3
import re
import json
import os

import awswrangler as wr
import pandas
from sellingpartnerapi import request as selling_partner_api_request, get_access_token_production_de_fr, catalogue


def lambda_handler(event, context):


    
    conn = wr.postgresql.connect("postgres_jdbc_connexion")
    data = wr.postgresql.read_sql_query(sql = "SELECT * from information_schema.tables;", con = conn)
    #print(data.shape)

    access_token_data = get_access_token_production_de_fr()

    access_token_data = access_token_data['access_token']



    catalogue_données = catalogue(id_vendeur = 'A3T4EQ2GGC5WWL', id_marketplace = 'A13V1IB3VIYZZH', jeton_acces_de_fr = access_token_data)

    print(len(catalogue_données))

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

