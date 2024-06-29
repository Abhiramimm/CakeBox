from django.shortcuts import render,redirect

from kart.forms import SignUpForm,SignInForm

from django.views.generic import View

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from kart.models import Cake,Size,BasketItem,CakeVariant,Order,Flavour,Occasion,Category,Tag

# Create your views here.


class RegistrationView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignUpForm()

        return render(request,"register.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SignUpForm(request.POST)

        if form_instance.is_valid():

            # data=form_instance.cleaned_data

            # User.objects.create_user(**data)

            form_instance.save()

            print("account created")

            return redirect("signin")
        
        return render(request,"register.html",{"form":form_instance})

class LoginView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignInForm()

        return render(request,"login.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SignInForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            uname=data.get("username")

            pwd=data.get("password")

            user_object=authenticate(request,username=uname,password=pwd)

            print(user_object)

            if user_object:

                login(request,user_object)

                print("session started")

                return redirect("index")
            
        print("failed to login")

        return render(request,"login.html",{"form":form_instance})

class IndexView(View):

    def get(self,request,*args,**kwargs):
        
        qs=Cake.objects.all()

        return render(request,"index.html",{"data":qs})

class CakeDetailView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Cake.objects.get(id=id)

        cake_variants=CakeVariant.objects.filter(cake_object=qs)

        default_price=cake_variants.first().price

        return render(request,"cake_detail.html",{"data":qs,"cake_variants": cake_variants,"default_price": default_price})
    
    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Cake.objects.get(id=id)

        cake_variants=CakeVariant.objects.filter(cake_object=qs)

        size_name=request.POST.get("size")

        size_obj=Size.objects.get(name=size_name)

        # selected_variant=cake_variants.get(size_object=size_obj)

        context= {
            "data": qs,
            # "selected_variant": selected_variant,
            "cake_variants": cake_variants
        }
    
        return render(request,"cake_detail.html",context)
    
class AddToCartView(View):

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        basket_obj=request.user.cart

        cake=Cake.objects.get(id=id)

        size_name=request.POST.get("size")

        size_obj=Size.objects.get(name=size_name)
        
        # cake_variant=CakeVariant.objects.filter(cake_object=cake,size_object=size_obj)
        cakevariant_obj = CakeVariant.objects.get(cake_object=cake, size_object=size_obj)

        qty=request.POST.get("qty")       

        print(cake,qty,size_obj)

        BasketItem.objects.create(

            basket_object=basket_obj,

            size_object=size_obj,

            cakevariant_object=cakevariant_obj,

            qty=qty,
        )

        print("item added to cart")

        return redirect("index")

class CartSummaryView(View):

    def get(self,request,*args,**kwargs):

        qs=request.user.cart.cartitems.filter(is_order_placed=False)

        return render(request,"cart_list.html",{"data":qs})        
    
class CartitemDestroyView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        BasketItem.objects.get(id=id).delete()

        return redirect("cart-summary")

class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")

class CartQuantityUpdateView(View):

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        basket_item_object=BasketItem.objects.get(id=id)

        action=request.POST.get("action")

        print(action)

        if action=="increment":

            basket_item_object.qty+=1

        else:

            basket_item_object.qty-=1
        
        basket_item_object.save()

        return redirect("cart-summary")

class PlaceOrderView(View):

    def  get(self,request,*args,**kwargs):

        return render(request,"place_order.html")
    
    def post(self,request,*args,**kwargs):

        message=request.POST.get("message")

        email=request.POST.get("email")

        phone=request.POST.get("phone")

        address=request.POST.get("address")

        pin=request.POST.get("pin")

        payment_mode=request.POST.get("payment_mode")

        user_obj=request.user

        cart_item_objects=request.user.cart.cartitems.filter(is_order_placed=False)

        if payment_mode=="cod":

            order_obj=Order.objects.create(

                user_object=user_obj,

                message=message,

                delivery_address=address,

                phone=phone,

                pin=pin,

                email=email,

                payment_mode=payment_mode

            )

            for bi in cart_item_objects:
                
                order_obj.basket_item_objects.add(bi)

                bi.is_order_placed=True

                bi.save()

            order_obj.save()


        print(email,phone,address,pin,payment_mode,)

        return redirect("index")

class OrderSummaryView(View):

    def get(self,request,*args,**kwargs):

        qs=Order.objects.filter(user_object=request.user).order_by("-created_date")

        return render(request,"order_summary.html",{"data":qs})

class FlavourFilterView(View):
    
    def get(self,request,*args,**kwrags):

        id=kwrags.get("pk")

        # qs=Flavour.objects.all()

        flavour=Flavour.objects.get(id=id)
        
        cakes=Cake.objects.filter(flavour_object=flavour)

        print(cakes)

        return render(request, 'cake_flavour.html', {"cakes": cakes, "flavour": flavour})
    
class OccasionFilterView(View):
    
    def get(self,request,*args,**kwrags):

        id=kwrags.get("pk")

        occasion=Occasion.objects.get(id=id)
        
        cakes=Cake.objects.filter(occasion_object=occasion)

        print(cakes)

        return render(request, 'cake_occasion.html', {"cakes": cakes, "occasion": occasion})

class CategoryFilterView(View):
    
    def get(self,request,*args,**kwrags):

        id=kwrags.get("pk")

        category=Category.objects.get(id=id)
        
        cakes=Cake.objects.filter(category_object=category)

        print(cakes)

        return render(request, 'cake_category.html', {"cakes": cakes, "category": category})

class TagFilterView(View):

    def get(self,request,*args,**kwrags):

        id=kwrags.get("pk")

        tag=Tag.objects.get(id=id)
        
        cakes=Cake.objects.filter(tag_object=tag)

        print(cakes)

        return render(request, 'cake_tag.html', {"cakes": cakes, "tag": tag})

class FilterListView(View):
    
    def get(self,request,*args,**kwrags):
        
        qs=Flavour.objects.all()

        all_occasions=Occasion.objects.all()

        all_category=Category.objects.all()

        all_tags=Tag.objects.all()

        return render(request,"filter.html",{"data":qs,"occasion":all_occasions,"category":all_category,"tag":all_tags})

class ContactView(View):

    def get(self,request,*args,**kwrags):

        return render(request,"contact.html")

class AboutView(View):

    def get(self,request,*args,**kwrags):

        return render(request,"about.html")
