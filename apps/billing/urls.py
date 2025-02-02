from django.urls import path
from .views.company import company_handler
from .views import (company_address_handler, company_working_handler, quotation_handler, DownloadQuotationPDF,
                    unit_handler)


urlpatterns = [
    path("companies/", company_handler, name='companyHandler'),
    path("companies/<int:pk>/", company_handler, name='getCompany'),
    path("company_address/", company_address_handler, name='addressHandler'),
    path("company_address/<int:pk>/", company_address_handler, name='addressHandler'),
    path("company_working/", company_working_handler, name='workingHandler'),
    path("company_working/<int:pk>/", company_working_handler, name='workingHandler'),
    path("quotation/", quotation_handler, name='quotationHandler'),
    path('download-quotation-pdf/<int:quotation_id>/', DownloadQuotationPDF.as_view(), name='download_quotation_pdf'),
    path('unit/', unit_handler, name='unitHandler'),
    path('unit/<int:pk>/', unit_handler, name='unitHandler')
]
