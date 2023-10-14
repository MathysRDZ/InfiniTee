# from django.shortcuts import render, redirect, get_object_or_404
# from .forms import RegistrationForm, UserForm, UserProfileForm
# from .models import Account, UserProfile
# from django.contrib import messages, auth
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse


# ## mail verification
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import  render_to_string
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes
# from django.contrib.auth.tokens import default_token_generator
# from django.core.mail import EmailMessage
# from carts.views import _cart_id
# from carts.models import Cart, CartItem, CartItemAccessoire

# import requests
# from orders.models import Order, OrderProduct




# def register(request):   ## creation de compte

#     if request.method == 'POST':       ## recuperer le request envoyer par l'utilisateur ( request html)
#         form = RegistrationForm(request.POST)   ### le mettre dans le formulaire

#         if form.is_valid():    ## si tout les element sont validé ( tous les elements remplit )

#             first_name = form.cleaned_data['first_name']   ##   recupere le nomù de famille
#             last_name = form.cleaned_data['last_name']
#             phone_number = form.cleaned_data['phone_number']
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']

#             username =  email.split("@")[0]  ##crrer un username à partir de l'adresse mail en enlevant le @

#              ## on creer un utilisateur à partir des données rentré pas l'utilisateur
#             user = Account.objects.create_user(first_name = first_name, username = username,  last_name=last_name, email=email, password=password )
#             user.phone_number = phone_number ## remplir le numero de l'utlisateur
#             user.save() ## on save l'utilisateur

#              ######### Creer en paralele le userprofile ######
#             profile = UserProfile()  ## creer userprofil de l'user
#             profile.user_id = user.id  ## lui associé l'id de l'user
#             profile.profile_picture = 'default/default_user.png'
#             profile.save()


#             ##  Activation de compte
#             current_site = get_current_site(request)  ## obtenir le domaine
#             mail_subject = 'Activez votre Compte'    ## Suject de mail ( objet)

#             token = default_token_generator.make_token(user)   ## crrer token pour l'utilisateur il est unique
#             message = render_to_string('accounts/account_verification_email.html', {   ## creer le message avec le template html
#                 'user': user,   ## passer le nom de l'utiliasteur
#                 'domain':  current_site,    ## passer le domaine
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),   ## passer la clef de l'utilisateur
#                 'token': default_token_generator.make_token(user),    ## passer le token
#             })


#             to_email = email ## recupere l'adresse eamil de l'user

#             send_email = EmailMessage(mail_subject, message, to=[to_email])    ##crée l'email  à envoyé
#             send_email.send()   ## envoie l'email
#             return redirect('/accounts/login/?command=verification&email='+email)   ## rediriger l'user vers un template explicatif du lien de verif

#         #    messages.success(request, 'Merci pour votre inscription, nous vous avons envoyé un mail de verification a votre adresse mail. ')




#     else :

#         form = RegistrationForm()
#     context={
#              'form':form

#     }
#     return render(request, 'accounts/register.html', context)











# def login(request):
#     if request.method == 'POST':    ## Si l'utilisateur à rempli le formulaire

#         email = request.POST['email']    ## recuperer l'email
#         password = request.POST['password']  ## recuperer le mot de passe

#         user= auth.authenticate(email = email, password =password)   ## mettre l'authentification dans la variable user

#         if user is not None :       ## si l'utilisateur existe faire
 

#             auth.login(request, user)  ## le connecter
#             messages.success(request, 'Vous êtes connecté') ## renvoyé vous etes connecté
#             url = request.META.get('HTTP_REFERER')

#             try :
#                 query = requests.utils.urlparse(url).query    ## recuperer l'url next:/
#                 params = dict(x.split('=')for x in query.split('&'))
#                 if 'next' in params :
#                     nextPage = params['next']
#                     return redirect(nextPage)   ## le rediriger vers le pannier de l'user quans il a appuyer sur chekout alors qu'il n'etait pas encore connecté

#             except :
#                     return redirect('dashboard')   ## le rediriger vers le dashboard


#         else :  ## si aucun utilisateur ne correspond
#             messages.error(request, 'Mauvais mot de passe ou Email') ## dire mauvais mot de passe

#             return redirect('login')  ## retourner le login

#     return render(request, 'accounts/login.html')  ## envoyé le template html à l'user











# @login_required(login_url = 'login')
# def logout(request):  ##     fonction qui deconnecte
#     auth.logout(request)  ##   deconnecter l'utilisateur
#     messages.success(request, ' Vous etes deconnecté ') ## envoyé messagege quand deconnecté
#     return redirect('login')           ## retour à la page login











# def activate(request, uidb64, token):  ## activé compte user
#     try :

#         uid = urlsafe_base64_decode(uidb64).decode()  ## decode la clef de l'utilisateur
#         user= Account._default_manager.get(pk = uid)  ## recupere l'utilisateur

#     except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
#         user =None   ## si pas d'utilisteur

#     if user is not None and default_token_generator.check_token(user, token):      ## si il y un utilisateur et que c'est le bon token associé au bon user
#         user.is_active =True   ## activer le compte
#         user.save()            ## sauver l'utilisateur
#         messages.success(request, 'Felicitaion, votre compte est activé.')   ## envoyé un msg de succée
#         return redirect('login')        ## redireigé vers le login
#     else :                                                                         ## sinon
#         messages.error(request, "lien d'activation invalide")   ## message d'erreur
#         return redirect('register')  ## redirige vers le formulaire d'inscription










# @login_required(login_url = 'login')
# def dashboard(request):   ## vue du dashboard
#     orders = Order.objects.order_by('-created_at').filter(user_id= request.user.id, is_ordered= True)   ## calcul le nombre de commande effectué par l'user
#     orders_count = orders.count()  ## aplique la fonction compte
#     userprofile = UserProfile.objects.get(user_id = request.user.id)

#     context = {

#          'orders_count': orders_count,  ## nb de commande effectué par l'user
#          'userprofile': userprofile,
#     }

#     return render(request, 'accounts/dashboard.html', context)









# def forgotPassword(request):   ##  fonction qui permet de reinitialiser le MDP

#     if request.method == 'POST':    ## si l'user envoie sa requeste
#         email = request.POST['email']  ## recuperer son email
#         if Account.objects.filter(email =email).exists():  ##  si elle existe
#             user = Account.objects.get(email__exact =email)  ## recuperer l'user existant



#             ## reset password email  --> envoyer l'email de chg de mdp

#             current_site = get_current_site(request)  ## obtenir le domaine
#             mail_subject = 'Changer votre mot de passe '    ## Suject de mail ( objet)

#             token = default_token_generator.make_token(user)   ## crrer token pour l'utilisateur il est unique
#             message = render_to_string('accounts/reset_password_email.html', {   ## creer le message avec le template html
#                 'user': user,   ## passer le nom de l'utiliasteur
#                 'domain':  current_site,    ## passer le domaine
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),   ## passer la clef de l'utilisateur
#                 'token': default_token_generator.make_token(user),    ## passer le token qui permet de crrer un lien temporaitre à une utilisation
#             })


#             to_email = email ## recupere l'adresse eamil de l'user

#             send_email = EmailMessage(mail_subject, message, to=[to_email])    ##crée l'email  à envoyé
#             send_email.send()   ## envoie l'email

#             messages.success(request, " Un email vous a été envoyé pour reinitialiser votre mot de passe")
#             return redirect('login')



#         else:  ## si le mail n'existe pas
#              messages.error(request, "Le compte n'existe pas" )   ## message d'erreur
#              return redirect('forgotPassword')

#     return render(request, 'accounts/forgotPassword.html')  ## renvoyer le template tant que l'user n'a rien submit









# def resetpassword_validate(request, uidb64, token):     # permet de diriger le lien de changement de mdp vers le template pr redefinir le new
#     try :

#         uid = urlsafe_base64_decode(uidb64).decode()  ## decode la clef de l'utilisateur
#         user= Account._default_manager.get(pk = uid)  ## recupere l'utilisateur

#     except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
#         user =None   ## si pas d'utilisteur


#     if user is not None and default_token_generator.check_token(user, token):      ## si il y un utilisateur et que c'est le bon token associé au bon user
#         request.session['uid'] = uid  ## recupere sa cled d'id dans les droit de sessions
#         messages.success(request, "Redefinissez votre mot de passe")
#         return redirect('resetPassword')   ## renvoie à un url qui va permettre de renseigner le new mdp

#     else :   ## si lien expriré
#         messages.error(request, 'Ce lien a expiré ')
#         return redirect('login')










# def resetPassword(request):

#     if request.method == 'POST':    ## si l'user envoie sa requeste
#         password = request.POST['password']
#         confirm_password = request.POST['confirm_password']


#         if password == confirm_password :

#              uid = request.session.get('uid')
#              user = Account.objects.get(pk = uid )
#              user.set_password(password)
#              user.save()
#              messages.success(request, "Changement de mot de passe reussi")
#              return redirect('login')


#         else :
#             messages.error(request, "Les mots de passe ne correpondent pas")
#             return redirect('resetPassword')





#     else :

#           return render(request, 'accounts/resetPassword.html')




# @login_required(login_url= 'login') ## si l'user n'est pas connecté, il ne peut pas acceder à cette page de changement de mot de passe
# def my_orders(request):  ## Permet d'afficher toutes les commandes effectué par l'user
#     orders = Order.objects.filter(user=request.user, is_ordered =True).order_by('-created_at')   ## recuperes toutes les commandes faites par l'user et les classes pas date
#     context = {

#       'orders':orders,
#     }
#     return render(request, 'accounts/my_orders.html', context)












# @login_required(login_url= 'login') ## si l'user n'est pas connecté, il ne peut pas acceder à cette page de changement de mot de passe
# def edit_profile(request): ## Permet d'editer le profil
# ## dans ce cas la, on lie un modele à un formulaire, il faut donc crrer un forms

#     userprofile = get_object_or_404(UserProfile, user=request.user) ##  Recuperer le profil user de l'utilisateur
#     if request.method == 'POST':  ## si l'user à envoyé le formulaire

#         user_form = UserForm(request.POST, instance=request.user)  ## recuperer le userform
#         profile_form = UserProfileForm(request.POST, request.FILES, instance = userprofile)  ## recuperer le userprofileForm mise a jour

#         if user_form.is_valid() and profile_form.is_valid():  ## si les formulaire sont valide
#             user_form.save()  ## sauvegarder le 1er formulaire modifié
#             profile_form.save() ## Sauvegarder le 2nd formualire modifié
#             messages.success(request, 'Votre profile a été mis à jour')  ## Meesage de succé
#             return redirect('edit_profile')

#     else :  ## si l'user n'as pas envoyé le formaulaire, alors l'affiché :

#         user_form = UserForm(instance=request.user)
#         profile_form = UserProfileForm(instance=userprofile)

#         context = {

#                  'user_form':user_form,
#                  'profile_form': profile_form,
#                  'userprofile': userprofile,

#          }
#     return render(request, 'accounts/edit_profile.html', context)



# @login_required(login_url= 'login') ## si l'user n'est pas connecté, il ne peut pas acceder à cette page de changement de mot de passe
# def change_password(request):       ## fonction qui permet de changer de mot de passe dans le dashboard

#     if request.method == 'POST':   #recupere le formaulaire
#         current_password = request.POST['current_password']  #recupere l'ancien mot de passe renseigné par l'user
#         new_password = request.POST['new_password']           #recupere le new mot de passe renseigné par l'user
#         confirm_password = request.POST['confirm_password']   #recupere la confirm du new mot de passe renseigné par l'user

#         ## Dans ce cas la on lie pas le formulaire à un modele, donc pas besoin de crrer de forms

#         user = Account.objects.get(username__exact= request.user.username)   ## recuperer l'user connecté

#         if new_password == confirm_password:   ## verifie si les deux nouveau MdP correspondent
#             success = user.check_password(current_password) ## Regarder si le mot de passe actuel rempli par l'user est le bon

#             if success:  ## si c'est le bon
#                 user.set_password(new_password)   ## met le nouveau mot de passe dans l'user en le cryptant
#                 user.save()  ## sauvgarder
#                 messages.success(request, 'Mot de passe actualisé')   ## envoyer message
#                 return redirect('change_password')

#             else :  ## si mauvais mot de passe
#                 messages.error(request, 'Mauvais de passe actuel')  ## message d'erreur
#                 return redirect('change_password')

#         else :  ## si les mots de passes ne correpondent pas :
#             messages.error(request, 'Les mots de passes ne correspondent pas')
#             return redirect('change_password')

#     return render(request, 'accounts/change_password.html')




# @login_required(login_url= 'login') ## si l'user n'est pas connecté, il ne peut pas acceder à cette page de changement de mot de passe
# def order_detail(request, order_id): ## fonction qui permet de donné accées au detail de la commande en ayant le num de commande dans le dashboard_sidebar

#     order_detail = OrderProduct.objects.filter(order__order_number= order_id)  ## on recupere les  produits de la commande avec le num de commande
#     order = Order.objects.get(order_number = order_id) ## on recupere la commande associé au numero de commande

#     subtotal = 0  ## calcul du subtotal car pas dans l'object order_product
#     for i in order_detail:
#         subtotal += 0 #i.product_price*i.quantity

#     if order.status == 'Accepted':
#         variable = True
#     else :
#         variable = False
#     context = {
#           'order_detail' : order_detail,
#           'order' : order,
#           'subtotal' : subtotal,
#           'variable' : variable,
#     }
#     return render(request, 'accounts/order_detail.html', context)
