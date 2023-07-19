from django.shortcuts import render, redirect
from django.views import View
from .forms import SignupForm


class Signup(View):
    def get(self, req):
        form = SignupForm()
        print("form", form)
        context = {
            "form": form
        }
        return render(req, 'user/user_signup.html', context)
    
    def post(self, req):
        form = SignupForm(req.POST)
        if form.is_valid():
            user = form.save()
            
            return redirect('blog:list')
        
        context = {
            "form": form
        }
        return render(req, 'user/user_signup.html', context)