from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm

app_name = 'app'  # Ensure your app is namespaced

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path("category/<slug:val>", views.CategoryView.as_view(), name="category"),
    path("category-title/<val>", views.CategoryTitle.as_view(), name="category-title"),
    path("product-detail/<int:pk>", views.ProductDetail.as_view(), name="product-detail"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("address/", views.address, name="address"),
    path('address/update/<int:pk>/', views.UpdateAddress.as_view(), name='updateAddress'),
    path('add-to-cart/', views.add_to_cart, name="add-to-cart"),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('pluscart/', views.plus_cart, name='pluscart'),  # Increment cart
    path('minuscart/', views.minus_cart, name='minuscart'),  # Decrement cart
    path('removecart/', views.remove_cart, name='removecart'),  # Remove from cart
    path('search/', views.product_search, name='product_search'),
    # path('orders/', views.orders_view, name='orders'),  # URL for orders
    path('wishlist/', views.wishlist_view, name='wishlist'),  # URL for wishlist
    path('create-payment-intent/', views.create_payment_intent, name='create-payment-intent'),
    path('thank-you/', views.thank_you, name='thank-you'),
    #path('product-search', views.product_search, name='product-search'),
    path('search/', views.product_search, name='product_search'),
     
    #path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
     
    # path('product_page', views.product_page, name='product_page'),
    # path('payment_successful', views.payment_successful, name='payment_successful'),
    # path('payment_cancelled', views.payment_cancelled, name='payment_cancelled'),
    # path('stripe_webhook', views.stripe_webhook, name='stripe_webhook'),

    # Login authentication
    path('registration/', views.CustomerRegistrationView.as_view(), name="customerregistration"),
    path('accounts/login/', auth_view.LoginView.as_view(template_name="app/login.html", authentication_form=LoginForm), name='login'),
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name="app/password_reset.html", form_class=MyPasswordResetForm), name='password_reset'),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name="app/changepassword.html", form_class=MyPasswordChangeForm, success_url='/passwordchangedone'), name='passwordchange'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name="app/passwordchangedone.html"), name='passwordchangedone'),
    path("logout/", auth_view.LogoutView.as_view(next_page='app:login'), name="logout"),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name="app/password_reset_done.html"), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name="app/password_reset_confirm.html", form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name="app/password_reset_complete.html"), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
