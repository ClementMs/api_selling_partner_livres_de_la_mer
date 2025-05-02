import json

import requests
import urllib3
import re
import json
import os

import awswrangler as wr
import pandas
from sellingpartnerapi import request as selling_partner_api_request, get_access_token_production_de_fr, catalogue_extraction, transformation_catalogue


def lambda_handler(event, context):


    
    #conn = wr.postgresql.connect("postgres_jdbc_connexion")
    conn = wr.postgresql.connect("les_livres_de_la_mer_postgresql")
    data = wr.postgresql.read_sql_query(sql = "SELECT * from information_schema.tables;", con = conn)
    #print(data.shape)

    access_token_data = get_access_token_production_de_fr()

    access_token_data = access_token_data['access_token']



    catalogue_liste = catalogue_extraction(id_vendeur = 'A3T4EQ2GGC5WWL', id_marketplace = 'A13V1IB3VIYZZH', jeton_acces_de_fr = access_token_data)

    catalogue = transformation_catalogue(catalogue_liste)

    catalogue['genre'] = ''

    catalogue['sous_genre'] = ''

    catalogue['quantites_disponibles'] = 1


    catalogue['magasin_id'] = 1

    catalogue['librairie_id'] = 1

    catalogue.rename(columns = {'amazon_objet_id': 'magasin_objet_id', 
                                'marketplace_id':'magasin_pays', 
                                'type': 'categorie',
                                'nom': 'titre',
                                'lien_image': 'image',
                                'date_creation': 'date_referencement',
                                'status': 'statut'}, inplace=True)

    catalogue = catalogue.reset_index()
    catalogue = catalogue.iloc[:, 1:]
    print(catalogue.head())
    catalogue = catalogue.reset_index().rename(columns = {'index': 'id'})

    print(catalogue.head())

    catalogue = catalogue[['id','magasin_objet_id','magasin_id', 'librairie_id', 'quantites_disponibles', 'magasin_pays', 'categorie', 'genre', 'sous_genre','condition','statut', 'titre', 'date_referencement','date_mise_a_jour', 'image']]

    wr.postgresql.to_sql(catalogue, conn, schema = 'public', table = 'librairies_livres',  mode = 'append')









    print(catalogue.shape)

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

