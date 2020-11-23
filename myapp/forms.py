from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from myapp.sub_models.notification_rules import ChangeStatusRule, ChangeThresholdRule, PriceThresholdRule, RecommendationAnalystRule


class CustomRegistrationFrom(UserCreationForm):
    first_name = forms.CharField(label='first_name', required=False,
                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}))

    last_name = forms.CharField(label='last_name', required=False, 
                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}))

    username = forms.EmailField(label='username', max_length=100,
                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}))

    password1 = forms.CharField(label='password1', min_length=4, max_length=30,
                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create password'}))

    password2 = forms.CharField(label='password2', min_length=4, max_length=30,
                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['username']
        user.save()
        return user


class CustomChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='old_password', min_length=4, max_length=30, 
                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter old password'}))

    new_password1 = forms.CharField(label='new_password1', min_length=4, max_length=30,
                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create new password'}))

    new_password2 = forms.CharField(label='new_password2', min_length=4, max_length=30,
                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'}))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


class ChangeStatusRuleForm(forms.ModelForm):
    num_of_days = forms.IntegerField(label='Number of days', initial=30, max_value=360, min_value=2,
            help_text=f"Enter a number between 2 and 360")
        
    fired = forms.BooleanField(required=False, label='Do not let this rule send me notifications')

    class Meta:
        model = ChangeStatusRule
        fields = ['watched_stock', 'status', 'num_of_days', 'fired']


class ChangeThresholdRuleForm(forms.ModelForm):    
    percentage_threshold = forms.FloatField(initial=0, max_value=100, min_value=-100,
                            help_text="Enter a percentage between -100 and 100")

    fired = forms.BooleanField(required=False, label='Do not let this rule send me notifications')
    
    class Meta:
        model = ChangeThresholdRule
        fields = ['watched_stock', 'when', 'percentage_threshold', 'fired']


class PriceThresholdRuleForm(forms.ModelForm):    
    price_threshold = forms.FloatField(initial=0, min_value=0,
                      help_text="Enter a value equal to or larger than 0")

    fired = forms.BooleanField(required=False, label='Do not let this rule send me notifications')

    class Meta:
        model = PriceThresholdRule
        fields = ['watched_stock', 'when', 'price_threshold', 'fired']


class RecommendationAnalystRuleForm(forms.ModelForm):   
    threshold_recommenders_percentage = forms.FloatField(initial=1, min_value=1, max_value=100,
                                        widget=forms.NumberInput(attrs={'class': 'form-control'}),
                                        help_text="Enter a value between 1 and 100")
    
    fired = forms.BooleanField(required=False, label='Do not let this rule send me notifications')

    class Meta:
        model = RecommendationAnalystRule
        fields = ['watched_stock', 'category', 'threshold_recommenders_percentage', 'fired']


def get_rule_from_str (request, rule_type, pk=""):
    instance = None
    if rule_type == 'change_status':
        if pk:
            instance = get_instance(ChangeStatusRule.objects.filter(pk=pk)[:1])
        return ChangeStatusRuleForm(request.POST or None, instance=instance), 'Status Change', instance

    elif rule_type == 'change_threshold':
        if pk:
            instance = get_instance(ChangeThresholdRule.objects.filter(pk=pk)[:1])
        return ChangeThresholdRuleForm(request.POST or None, instance=instance), 'Threshold Change', instance

    elif rule_type == 'price_threshold':
        if pk: 
            instance = get_instance(PriceThresholdRule.objects.filter(pk=pk)[:1])
        return PriceThresholdRuleForm(request.POST or None, instance=instance), 'Price Threshold', instance

    elif rule_type == 'recommendation_analyst':
        if pk: 
            instance = get_instance(RecommendationAnalystRule.objects.filter(pk=pk)[:1])
        return RecommendationAnalystRuleForm(request.POST or None, instance=instance), 'Analyst Recommendations', instance
    else:
        return None, None, None

def get_instance (queryset):
    if queryset.exists():
        return queryset[0]
    else:
        return None
