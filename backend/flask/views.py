import re
from flask import request
from flask_restful import Resource, fields, marshal_with, abort
from bson import ObjectId
from .extentions import mongo, api


protein_fields = {
    'producer': fields.String,
    'name':    fields.String,
    'weight': fields.Integer,
    'price': fields.Float,
    'old_price': fields.Float,
    'discount': fields.Float,
    'price_standarized': fields.Float,
    'image': fields.String,
    'url':fields.String,
    'date_added': fields.String
}


producer_fields = {
    'producer': fields.String
}


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


def abort_if_no_data(data):
    if not data:
        abort(404, message="Not Found Any Data")


class Proteins(Resource):
    def get(self):
        print('get request')
        query_filter = self._get_filter(['producer', 'date_added', 'name'])
        page = int(request.args.get('page')) or 1
        limit = int(request.args.get('limit') or 10) 
        
        sort_props = request.args.get('sort') or '_id.desc'
        sort_props_splited = sort_props.split('.') 
        sort_col = sort_props_splited[0]
        sort_direction = 1 if sort_props_splited[1] == 'asc' else -1

        response = self._create_response(query_filter, sort_col, sort_direction, page, limit)

        return response

    def _get_filter(self, keys):
        return {
            key: {'$regex':re.compile(fr".*{value}.*", re.I)} if key == 'name' else value 
            for key in keys if (value := request.args.get(key))
        }

    def _create_response(self, query_filter, sort_col, sort_direction, page, limit):
        data = self._get_data(query_filter, sort_col, sort_direction, )

        response = {
            'count': len(data),
            'results': self._get_pagginated_data(data, page, limit)
        }

        return response

    def _get_data(self, query_filter,sort_col, sort_direction):
        protein_collection = mongo.db.proteins

        return list(protein_collection.find(query_filter).sort(sort_col, sort_direction)) 
    
    @marshal_with(protein_fields)
    def _get_pagginated_data(self, data, page, limit):
        offset = (int(page) - 1) * limit      
        
        return data[offset:offset + limit]


class Protein(Resource):
    @marshal_with(protein_fields)
    def get(self, _id):
        protein_collection = mongo.db.proteins
        
        data = protein_collection.find_one({'_id': ObjectId(_id)})
        abort_if_no_data(data)

        return data


class Producers(Resource):
    def get(self):
        protein_collection = mongo.db.proteins
        
        data = protein_collection.distinct('producer')
        abort_if_no_data(data)

        return data


api.add_resource(HelloWorld, '/')
api.add_resource(Producers, '/producers/')
api.add_resource(Proteins, '/proteins/')
api.add_resource(Protein, '/protein/<_id>')