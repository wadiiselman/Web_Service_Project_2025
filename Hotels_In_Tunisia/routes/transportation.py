from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas import TransportationSchema
from models import Transportation
from app import db

blp = Blueprint(
    "Transportation", "transportation",
    description="Operations on transportation",
    url_prefix="/api/transportation"
)

@blp.route("/")
class TransportationList(MethodView):
    @blp.response(200, TransportationSchema(many=True))
    def get(self):
        """List all transportation options"""
        try:
            transports = Transportation.query.all()
            return transports
        except Exception as e:
            abort(500, message=str(e))

    @jwt_required()
    @blp.arguments(TransportationSchema)
    @blp.response(201, TransportationSchema)
    def post(self, transport_data):
        """Add a new transportation option (Protected: requires JWT token)"""
        try:
            new_transport = Transportation(**transport_data)
            db.session.add(new_transport)
            db.session.commit()
            return new_transport
        except Exception as e:
            db.session.rollback()
            abort(500, message=str(e))

@blp.route("/<int:transport_id>")
class TransportationResource(MethodView):
    @blp.response(200, TransportationSchema)
    def get(self, transport_id):
        """Get specific transportation details"""
        transport = Transportation.query.get_or_404(transport_id)
        return transport

    @jwt_required()
    @blp.arguments(TransportationSchema)
    @blp.response(200, TransportationSchema)
    def put(self, transport_data, transport_id):
        """Update transportation details (Protected: requires JWT token)"""
        try:
            transport = Transportation.query.get_or_404(transport_id)
            for key, value in transport_data.items():
                setattr(transport, key, value)
            db.session.commit()
            return transport
        except Exception as e:
            db.session.rollback()
            abort(500, message=str(e))

    @jwt_required()
    def delete(self, transport_id):
        """Delete a transportation option (Protected: requires JWT token)"""
        try:
            transport = Transportation.query.get_or_404(transport_id)
            db.session.delete(transport)
            db.session.commit()
            return {"message": "Transportation deleted"}
        except Exception as e:
            db.session.rollback()
            abort(500, message=str(e))

@blp.route("/search")
class TransportationSearch(MethodView):
    @blp.response(200, TransportationSchema(many=True))
    def get(self):
        """Search for transportation options"""
        try:
            from flask import request
            from_location = request.args.get('from')
            to_location = request.args.get('to')
            means = request.args.get('means')

            query = Transportation.query
            if from_location:
                query = query.filter_by(from_location=from_location)
            if to_location:
                query = query.filter_by(to_location=to_location)
            if means:
                query = query.filter_by(means=means)

            results = query.all()
            return results
        except Exception as e:
            abort(500, message=str(e))