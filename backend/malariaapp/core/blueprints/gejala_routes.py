
from .inventory_api import gejala_api
from models import Gejala


@gejala_api.route('/gejala', methods=['GET'])
def get_all_gejala():
    from models import Gejala
    gejalas = Gejala.query.all()
    result = []
    for gejala in gejalas:
        result.append({
            'id': gejala.id,
            'kode': gejala.kode,
            'nama': gejala.nama,
            'is_active': gejala.is_active
        })
    return {'gejalas': result}, 200


@gejala_api.route('/gejala/<int:gejala_id>', methods=['GET'])
def get_gejala_by_id(gejala_id):
    from models import Gejala
    gejala = Gejala.query.get(gejala_id)
    if gejala is None:
        return {'error': 'Gejala not found'}, 404
    return {
            'id': gejala.id,
            'kode': gejala.kode,
            'nama': gejala.nama,
            'is_active': gejala.is_active
        }, 200
    
@gejala_api.route('/gejala', methods=['POST'])
def create_gejala():
    from models import Gejala
    
    data = request.get_json()
    gejala = Gejala(
        kode=data['kode'],
        nama=data['nama'],
        is_active=data.get('is_active', True)
    )
    Gejala.save(gejala)
    return {'message': 'Gejala created successfully'}, 201

@gejala_api.route('/gejala/<int:gejala_id>', methods=['PUT'])
def update_gejala(gejala_id):
    from models import Gejala
    gejala = Gejala.query.get(gejala_id)
    if gejala is None:
        return {'error': 'Gejala not found'}, 404
    data = request.get_json()
    gejala.kode = data.get('kode', gejala.kode)
    gejala.nama = data.get('nama', gejala.nama)
    gejala.is_active = data.get('is_active', gejala.is_active)
    Gejala.save(gejala)
    return {'message': 'Gejala updated successfully'}, 200

@gejala_api.route('/gejala/<int:gejala_id>', methods=['DELETE'])
def delete_gejala(gejala_id):
    from models import Gejala
    gejala = Gejala.query.get(gejala_id)
    if gejala is None:
        return {'error': 'Gejala not found'}, 404
    Gejala.delete(gejala)
    return {'message': 'Gejala deleted successfully'}, 200
  