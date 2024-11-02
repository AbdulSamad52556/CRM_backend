# urls.py
from django.urls import path
from .views import BaseOwnerCreateView, MyOwnerView, AgreementDocumentListView, VerifyAgreementDocumentView, UserAgreementDocumentsView, SignAgreementDocumentView

urlpatterns = [
    path('create-owners/', BaseOwnerCreateView.as_view(), name='add-owner'),
    path('get-owners/', MyOwnerView.as_view(), name='add-owner'),
    path('agreement-documents/', AgreementDocumentListView.as_view(), name='agreement-document-list'),
    path('agreement-documents/verify/<int:pk>/', VerifyAgreementDocumentView.as_view(), name='verify-agreement-document'),
    path('agreement-documents/owner/<int:user_id>/', UserAgreementDocumentsView.as_view(), name='owner-agreement-documents'),
    path('agreement-documents/owner/signed/<int:id>/', SignAgreementDocumentView.as_view(), name='sign_agreement_document'),

]
