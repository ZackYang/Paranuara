from app.models import Company
from app.api import bp
from app.api.errors import error_response
from app.json_formatters import CompanyFormatter
from mongoengine.queryset.visitor import Q

@bp.route('/companies/<string:name>', methods=['GET'])
def get_company_by_name(name):
  company = Company.objects(Q(name__exact=name)).first()
  return render_company(company)

@bp.route('/companies/<int:id>', methods=['GET'])
def get_company_by_id(id):
  company = Company.objects(pk=id).first()
  return render_company(company)

def render_company(company):
  if company is None:
    return error_response(404, message='Your company id is incorrect')
  return CompanyFormatter.format(company)
